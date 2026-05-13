#!/usr/bin/env python3
"""
静态背景 MV 生成器 — 质量优先 / 单次渲染版

输入:同目录下 input.{png,jpg,jpeg} + input.{mp3,wav,m4a,flac,aac}(自动识别)
输出:output.mp4 — 带运镜、噪点、暗角、底部音频波形、片头标题的 1080p mp4

依赖:ffmpeg(系统级,需带 libx264/aac/libfreetype)、Python 3.8+
用法:
    python make_mv.py
    # 或覆盖标题:
    MV_TITLE="新歌名" python make_mv.py

适用场景:
    - 桌面级机器(>=4 核 / >=8GB)
    - 想要 medium preset 的画质
    - 渲染时间无所谓 (135s 音频在 4 核机器约 5-8 分钟)

如果机器只有 2 核 / 沙箱环境 / 渲染会超时,改用同目录 make_mv_chunked.py。
"""

import subprocess
import os
import sys
from pathlib import Path

# ============ 配置区 ============
# 这是整个模板对外的配置面板。给一首新歌做 MV,通常只需要改 title_text 和
# (可选)调一下 zoom_end / vignette_angle / waveform_color 配色。
CONFIG = {
    # ---- 输入 / 输出 ----
    # 留空让脚本自动识别 input.{png,jpg,...} / input.{mp3,wav,...},
    # 也可以填具体文件名 (例如 "cover.jpg") 覆盖自动识别
    "image_path": "",
    "audio_path": "",
    "output_path": "output.mp4",

    # ---- 画面基础 ----
    "width": 1920,
    "height": 1080,
    "fps": 30,

    # ---- 运镜:线性推近 (Ken Burns 效果) ----
    # 1.0 = 不动;1.12 = 渲染结束时画面被推近到 112%。建议 1.05-1.20。
    # 太大会出现明显采样模糊,因为我们是从静态图缩放的。
    "zoom_end": 1.12,

    # ---- 胶片质感:噪点 + 暗角 ----
    # noise 0-100,越大颗粒越粗。City Pop / Lo-fi 建议 15-30。
    "noise_strength": 20,
    # vignette 0-PI/2,越大边缘越暗。0.3 微弱,0.5 明显,0.7+ 偏戏剧化。
    "vignette_angle": 0.4,

    # ---- 底部音频波形 ----
    # 颜色是 0xBBGGRR (注意 BGR 不是 RGB!),粉色 0xFF6BB5、绿色 0x6BFFB5、
    # 蓝色 0xB56BFF、白色 0xFFFFFF。透明度 0.0-1.0。
    "waveform_height": 80,
    "waveform_color": "0xFF6BB5",
    "waveform_opacity": 0.6,

    # ---- 片头标题 (淡入淡出) ----
    # 通过环境变量 MV_TITLE 可临时覆盖,方便批量出片
    "title_text": os.environ.get("MV_TITLE", "Your Song Title"),
    "title_duration": 4,            # 标题总显示时长 (秒)
    "title_fontsize": 72,
    "title_color": "white",

    # ---- 编码参数 ----
    # preset: ultrafast / superfast / veryfast / faster / fast / medium / slow / slower / veryslow
    # 越往右越慢但压缩率越高 (相同码率下画质更好,或相同画质下文件更小)
    "preset": "medium",
    "video_bitrate": "8M",          # 1080p City Pop 风格,8M 足够干净
    "audio_bitrate": "192k",
}
# =================================


# ----- 输入自动识别 -----
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg")


def auto_find(prefix: str, exts: tuple) -> str:
    """在当前目录找 input.* 文件,返回第一个命中的扩展名版本。"""
    for ext in exts:
        candidate = f"{prefix}{ext}"
        if os.path.exists(candidate):
            return candidate
    return ""


def resolve_inputs():
    img = CONFIG["image_path"] or auto_find("input", IMAGE_EXTS)
    aud = CONFIG["audio_path"] or auto_find("input", AUDIO_EXTS)
    if not img or not os.path.exists(img):
        print(f"找不到图片: 期望 input.{{png,jpg,...}} 或在 CONFIG['image_path'] 指定")
        sys.exit(1)
    if not aud or not os.path.exists(aud):
        print(f"找不到音频: 期望 input.{{mp3,wav,...}} 或在 CONFIG['audio_path'] 指定")
        sys.exit(1)
    return img, aud


def get_audio_duration(audio_path: str) -> float:
    """用 ffprobe 拿音频时长(秒)。"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def find_font() -> str:
    """找一个系统里能用的字体(优先中文支持,回退到 DejaVu)。"""
    candidates = [
        # Linux 中文字体
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        # Windows
        "C:/Windows/Fonts/msyh.ttc",          # 微软雅黑
        "C:/Windows/Fonts/SourceHanSerifSC-ExtraLight.otf",   # 跳蛛先生品牌字体
        # Linux 回退
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for f in candidates:
        if os.path.exists(f):
            return f
    return ""


def build_filter_complex(duration: float, font_path: str) -> str:
    """
    构建 ffmpeg 滤镜链(整个脚本的核心)。
    顺序: 缩放 → 推近运镜 → 噪点 → 暗角 → 叠音频波形 → 标题文字
    """
    w, h, fps = CONFIG["width"], CONFIG["height"], CONFIG["fps"]
    total_frames = int(duration * fps)
    zoom_end = CONFIG["zoom_end"]

    # zoompan 表达式:线性推近。on 是当前输出帧编号 (0..total_frames-1)
    zoom_expr = f"1+({zoom_end}-1)*on/{total_frames}"

    # 标题淡入 / 持续 / 淡出 的 alpha 表达式
    title_dur = CONFIG["title_duration"]
    fade_in, fade_out = 0.5, 0.5
    alpha_expr = (
        f"if(lt(t,{fade_in}),t/{fade_in},"
        f"if(lt(t,{title_dur - fade_out}),1,"
        f"if(lt(t,{title_dur}),({title_dur}-t)/{fade_out},0)))"
    )

    # 字体路径在 ffmpeg filter 内部要转义 (反斜杠 + 冒号)
    font_escaped = font_path.replace("\\", "/").replace(":", "\\:")
    title_escaped = CONFIG["title_text"].replace("'", "\\'").replace(":", "\\:")

    return (
        # 1. 把图片放大到目标尺寸的 120% (给推近运镜留余量,否则推到边会黑屏)
        f"[0:v]scale={int(w*1.2)}:{int(h*1.2)}:force_original_aspect_ratio=increase,"
        f"crop={int(w*1.2)}:{int(h*1.2)},"
        # 2. 把静态图当循环视频流,设帧率和总时长
        f"loop=loop=-1:size=1,trim=duration={duration},fps={fps},"
        # 3. 推近运镜 (d=1: 每帧重算,避免阶梯感)
        f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={w}x{h}:fps={fps},"
        # 4. 噪点 (模拟胶片颗粒)
        f"noise=alls={CONFIG['noise_strength']}:allf=t,"
        # 5. 暗角
        f"vignette=angle={CONFIG['vignette_angle']}"
        f"[bg];"

        # 6. 音频波形可视化
        f"[1:a]showwaves=s={w}x{CONFIG['waveform_height']}:"
        f"mode=line:colors={CONFIG['waveform_color']}:rate={fps}[wave];"

        # 7. 波形叠加到底部
        f"[bg][wave]overlay=0:H-{CONFIG['waveform_height']}-30:"
        f"format=auto:alpha={CONFIG['waveform_opacity']}[withwave];"

        # 8. 片头标题文字
        f"[withwave]drawtext=fontfile='{font_escaped}':"
        f"text='{title_escaped}':"
        f"fontsize={CONFIG['title_fontsize']}:"
        f"fontcolor={CONFIG['title_color']}:"
        f"x=(w-text_w)/2:y=(h-text_h)/2:"
        f"alpha='{alpha_expr}':"
        f"enable='lt(t,{title_dur})'"
        f"[final]"
    )


def main():
    img, aud = resolve_inputs()
    print(f"图片: {img}")
    print(f"音频: {aud}")

    font = find_font()
    if not font:
        print("找不到可用字体,请在 find_font() 里加自己机器的字体路径")
        sys.exit(1)
    print(f"字体: {font}")

    duration = get_audio_duration(aud)
    print(f"音频时长: {duration:.2f} 秒  ->  视频帧数: {int(duration * CONFIG['fps'])}")

    filter_complex = build_filter_complex(duration, font)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img,
        "-i", aud,
        "-filter_complex", filter_complex,
        "-map", "[final]",
        "-map", "1:a",
        "-c:v", "libx264",
        "-preset", CONFIG["preset"],
        "-b:v", CONFIG["video_bitrate"],
        "-pix_fmt", "yuv420p",          # 兼容性最好的像素格式
        "-c:a", "aac",
        "-b:a", CONFIG["audio_bitrate"],
        "-shortest",                     # 以最短流为准,防止图片循环超过音频
        CONFIG["output_path"]
    ]

    print(f"\n开始渲染 (preset={CONFIG['preset']}, bitrate={CONFIG['video_bitrate']})...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("\nFFmpeg 报错 (尾部 2000 字符):")
        print(result.stderr[-2000:])
        sys.exit(1)

    out_size_mb = os.path.getsize(CONFIG["output_path"]) / 1024 / 1024
    print(f"\n完成! 输出: {CONFIG['output_path']} ({out_size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
