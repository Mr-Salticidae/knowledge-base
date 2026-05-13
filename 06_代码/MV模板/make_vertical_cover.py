#!/usr/bin/env python3
"""
横版 MV → 竖版抖音版（黑胶唱片套框式构图）

把一个 16:9 (或 4:3 / 任何横版) 的成片视频，转成 1080×1920 9:16 抖音/小红书竖
版。**思路不是模糊填充**——是把项目的 3:4 海报封面切出顶部标题条 + 底部页脚
条，拼成一个黑胶唱片套式的固定边框，中间放视频。

适用场景:
    - 同一首歌的 MV 已经有 16:9 成片 + 3:4 唱片套封面
    - 想要竖版和封面是"同一套设计语言"，不是粗暴的模糊外扩
    - 抖音/小红书首图也是 3:4，竖版视频和首图视觉接得上

为什么不用模糊填充:
    实测发现，同画面的"清晰中段 + 模糊上下"会产生肉眼挑得出的"两个图层"
    感，因为背景的内容、亮度、清晰度都和前景不一致。改成"完全不同的固定边框
    (深底色 + 标题条 + 页脚条)"反而更有秩序、更像一张专辑封面在动。

依赖:ffmpeg、Python 3.8+
输入:
    - 源视频 (任何分辨率，会自动 letterbox 到 1080 宽)
    - 3:4 封面 PNG/JPG (脚本会自动从顶部切标题条、从底部切页脚条)

用法:
    python make_vertical_cover.py
    # 或环境变量覆盖:
    SRC=path/to/video.mp4 COVER=path/to/cover.png python make_vertical_cover.py
"""

import subprocess
import os
import sys

# ============ 配置区 ============
CONFIG = {
    # ---- 输入 / 输出 ----
    "src": os.environ.get("SRC", "input.mp4"),         # 源横版视频
    "cover": os.environ.get("COVER", "cover_3_4.png"), # 3:4 海报封面
    "out": "output_vertical.mp4",
    "workdir": ".",

    # ---- 输出尺寸 ----
    "canvas_w": 1080,
    "canvas_h": 1920,
    "fps": 30,                       # 抖音建议 30fps，不必跟源视频走 60fps

    # ---- 封面切片配置 (按你 3:4 封面的布局调) ----
    # 标题条:从封面顶部切出的高度。默认 230 (针对 1080×1440 的 3:4 封面)
    # 你的封面如果是别的尺寸，按比例调
    "title_strip_h": 230,
    # 页脚条:从封面底部切出的高度
    "footer_strip_h": 160,

    # ---- 标题/页脚条在画布上的位置 ----
    "title_y": 80,                   # 标题条贴顶部留 80px 边距
    "footer_y_from_bottom": 240,     # 页脚条距画布底部 240px (即 y = 1920-240-160 = 1520... 等下重新算)
    # 实际页脚 y 位置 = canvas_h - footer_y_from_bottom (页脚条底部贴住这个位置)
    # 即 footer 占据 [canvas_h - footer_y_from_bottom - footer_strip_h, canvas_h - footer_y_from_bottom]

    # ---- 主视频在画布上的处理 ----
    # video_aspect: "1:1" / "4:3" / "16:9"
    # 1:1 最像封面 (中心方块)；4:3 略宽；16:9 保留全部源内容但条带感强
    "video_aspect": "1:1",
    "video_y": 420,                  # 视频在画布上的 y 位置 (顶部对齐)

    # ---- 背景色 ----
    # 留空 = 自动从封面 (5,5) 像素采样；填了就用指定的 (格式 "0xRRGGBB" 或十六进制)
    "bg_color": "",

    # ---- 编码 ----
    "preset": "ultrafast",
    "video_bitrate": "6M",

    # ---- 分块策略 ----
    # 单条命令时长限制下，按多少秒切一块。30fps 渲染下，70 秒源在 2 核机器约 23s
    "chunk_seconds": 70,
}
# =================================


def get_duration(p):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", p],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())


def sample_bg_color(cover_path):
    """采样封面左上角像素颜色，返回 0xRRGGBB 字符串。"""
    r = subprocess.run(
        ["ffmpeg", "-i", cover_path, "-vf", "crop=2:2:5:5",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True
    )
    if r.returncode != 0 or len(r.stdout) < 3:
        return "0x000000"
    rgb = r.stdout[:3]
    return f"0x{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def get_cover_dims(p):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=p=0:s=x", p],
        capture_output=True, text=True, check=True
    )
    w, h = r.stdout.strip().split("x")
    return int(w), int(h)


def build_frame_template(cover_path, output_path, bg_color):
    """把"深底色 + 顶部标题条 + 底部页脚条"合成成一张静态 PNG。
    渲染时每帧不用重新计算这些，直接当背景叠视频。"""
    w, h = CONFIG["canvas_w"], CONFIG["canvas_h"]
    cw, ch = get_cover_dims(cover_path)
    title_h = CONFIG["title_strip_h"]
    footer_h = CONFIG["footer_strip_h"]
    title_y = CONFIG["title_y"]
    footer_y = h - CONFIG["footer_y_from_bottom"] - footer_h

    # 如果封面宽度不是目标宽度，要先 scale；高度跟着比例走
    if cw != w:
        scale_filter = f"scale={w}:-2,"
    else:
        scale_filter = ""

    fc = (
        f"color=c={bg_color}:s={w}x{h}[bg];"
        f"[0:v]{scale_filter}split=2[c1][c2];"
        f"[c1]crop={w}:{title_h}:0:0[title];"
        f"[c2]crop={w}:{footer_h}:0:{ch - footer_h}[footer];"
        f"[bg][title]overlay=0:{title_y}[t1];"
        f"[t1][footer]overlay=0:{footer_y}[out]"
    )
    cmd = [
        "ffmpeg", "-y", "-i", cover_path,
        "-filter_complex", fc, "-map", "[out]",
        "-frames:v", "1", output_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("build_frame_template ffmpeg error:")
        print(r.stderr[-1500:])
        sys.exit(1)


def video_crop_filter():
    """根据 video_aspect 返回 crop 滤镜。"""
    aspect = CONFIG["video_aspect"]
    w = CONFIG["canvas_w"]
    # 源视频会先 scale 到 w 宽，然后按比例 crop 高度
    # 我们假设源宽高比一般是 16:9 = 1920:1080，对应 scale 后 = 1080:608
    # 1:1: 宽高都为 w，从源中心横向裁，纵向用全部
    # 实际上我们要的是:从源 (任意宽:任意高) 中央裁出目标宽高比，再 scale 到 w 宽
    if aspect == "1:1":
        target_h = w        # 输出 1080×1080
    elif aspect == "4:3":
        target_h = int(w * 3 / 4)   # 1080×810
    elif aspect == "16:9":
        target_h = int(w * 9 / 16)  # 1080×608
    else:
        raise ValueError(f"unknown aspect: {aspect}")
    # crop 用 ih/iw 自动计算源中心 crop
    return f"crop='min(iw,ih*{w}/{target_h})':'min(ih,iw*{target_h}/{w})':(iw-ow)/2:(ih-oh)/2,scale={w}:{target_h}"


def render_chunk(idx, start, dur, frame_template, workdir):
    out = os.path.join(workdir, f"cvchunk_{idx}.mp4")
    crop_filter = video_crop_filter()

    fc = (
        f"[0:v]{crop_filter},fps={CONFIG['fps']}[vid];"
        f"[1:v]fps={CONFIG['fps']}[bg];"
        f"[bg][vid]overlay=0:{CONFIG['video_y']}[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start), "-t", str(dur), "-i", CONFIG["src"],
        "-i", frame_template,
        "-filter_complex", fc,
        "-map", "[out]",
        "-r", str(CONFIG["fps"]),
        "-c:v", "libx264",
        "-threads", "0",
        "-preset", CONFIG["preset"],
        "-b:v", CONFIG["video_bitrate"],
        "-pix_fmt", "yuv420p",
        "-an",
        "-t", str(dur),
        out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"chunk {idx} ffmpeg error:")
        print(r.stderr[-1500:]); sys.exit(1)
    return out


def concat_chunks(paths, workdir, out_path):
    lst = os.path.join(workdir, "cvconcat.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
    cmd = ["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",out_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("concat error:"); print(r.stderr[-1500:]); sys.exit(1)


def mux_audio(video_only, src_with_audio, out):
    cmd = [
        "ffmpeg","-y",
        "-i", video_only, "-i", src_with_audio,
        "-map","0:v","-map","1:a",
        "-c:v","copy","-c:a","copy",
        "-shortest", out
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("mux error:"); print(r.stderr[-1500:]); sys.exit(1)


def cleanup(workdir, n):
    for i in range(n):
        p = os.path.join(workdir, f"cvchunk_{i}.mp4")
        if os.path.exists(p):
            os.remove(p)
    for name in ("cvconcat.txt", "cvvideo_only.mp4", "frame_template.png"):
        p = os.path.join(workdir, name)
        if os.path.exists(p):
            os.remove(p)


def main():
    if not os.path.exists(CONFIG["src"]):
        print(f"找不到源视频: {CONFIG['src']}"); sys.exit(1)
    if not os.path.exists(CONFIG["cover"]):
        print(f"找不到封面: {CONFIG['cover']}"); sys.exit(1)

    # 采样底色
    bg = CONFIG["bg_color"] or sample_bg_color(CONFIG["cover"])
    print(f"背景色: {bg}")

    # 1. 烤静态帧模板
    workdir = CONFIG["workdir"]
    os.makedirs(workdir, exist_ok=True)
    frame_template = os.path.join(workdir, "frame_template.png")
    print(f"烤静态帧模板 → {frame_template}")
    build_frame_template(CONFIG["cover"], frame_template, bg)

    # 2. 算分块
    duration = get_duration(CONFIG["src"])
    cs = CONFIG["chunk_seconds"]
    n = int(duration // cs) + (1 if duration % cs > 0.5 else 0)
    print(f"源时长 {duration:.2f}s，分 {n} 块 (每块约 {cs}s)")

    # 3. 渲染各块
    chunk_paths = []
    for i in range(n):
        start = i * cs
        dur = (duration - start) if i == n - 1 else cs
        print(f"[chunk {i+1}/{n}] start={start:.1f}s dur={dur:.1f}s")
        chunk_paths.append(render_chunk(i, start, dur, frame_template, workdir))

    # 4. 拼接 + 挂音轨
    video_only = os.path.join(workdir, "cvvideo_only.mp4")
    print(f"拼接 → {video_only}")
    concat_chunks(chunk_paths, workdir, video_only)
    print(f"挂音轨 → {CONFIG['out']}")
    mux_audio(video_only, CONFIG["src"], CONFIG["out"])

    cleanup(workdir, n)

    sz = os.path.getsize(CONFIG["out"]) / 1024 / 1024
    print(f"完成! 输出: {CONFIG['out']} ({sz:.1f} MB)")


if __name__ == "__main__":
    main()
