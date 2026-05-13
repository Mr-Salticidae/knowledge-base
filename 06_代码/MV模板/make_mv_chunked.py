#!/usr/bin/env python3
"""
静态背景 MV 生成器 — 分块渲染版

和 make_mv.py 同滤镜链 / 同输出参数,但把渲染拆成 N 个时间片,逐片渲染再无损
拼接 + 挂音轨。每片之间 zoompan 推近表达式按全局帧号校正,所以镜头是连续的。

适用场景:
    - 2 核 / 慢机器,单次 ffmpeg 跑不动整曲
    - 沙箱/CI 环境,单条命令有时间上限 (e.g. <= 45s)
    - 想要看渲染进度,失败了能从某一片重跑

输入 / 输出 / 配置接口和 make_mv.py 完全一致 (可以直接互换)。
用法:
    python make_mv_chunked.py
    # 自定义分块数 (默认按音频时长自动算):
    MV_CHUNKS=6 python make_mv_chunked.py

依赖:ffmpeg(系统级)、Python 3.8+
"""

import subprocess
import os
import sys

# ============ 配置区 ============
# 和 make_mv.py 同样的配置面板,新歌只需要改 title_text。
CONFIG = {
    # ---- 输入 / 输出 ----
    "image_path": "",                # 留空 = 自动找 input.{png,jpg,...}
    "audio_path": "",                # 留空 = 自动找 input.{mp3,wav,...}
    "output_path": "output.mp4",
    "workdir": ".",                  # 中间文件 (chunk_*.mp4, concat.txt) 的位置

    # ---- 画面基础 ----
    "width": 1920,
    "height": 1080,
    "fps": 30,

    # ---- 运镜 ----
    "zoom_end": 1.12,

    # ---- 胶片质感 ----
    "noise_strength": 20,
    "vignette_angle": 0.4,

    # ---- 音频波形 ----
    "waveform_height": 80,
    "waveform_color": "0xFF6BB5",
    "waveform_opacity": 0.6,

    # ---- 片头标题 ----
    "title_text": os.environ.get("MV_TITLE", "Your Song Title"),
    "title_duration": 4,
    "title_fontsize": 72,
    "title_color": "white",

    # ---- 编码 ----
    # 分块版默认用 ultrafast,因为目的就是单步能在限时内完成。
    # 如果机器够快、想要更小体积/更好质量,可以改成 veryfast / fast。
    "preset": "ultrafast",
    "video_bitrate": "5M",           # ultrafast 压缩率低,5M 已经够干净
    "audio_bitrate": "192k",

    # ---- 分块策略 ----
    # 每块目标时长 (秒)。默认 35 秒 → 在 2 核 1080p ultrafast 上单次 ffmpeg
    # 耗时 ~32 秒,稳稳卡在 45 秒以内。机器快可以加大到 60-90。
    "chunk_seconds": int(os.environ.get("MV_CHUNK_SECONDS", "35")),
    # 也可以直接指定块数,优先级高于 chunk_seconds (0 = 不启用)
    "chunk_count_override": int(os.environ.get("MV_CHUNKS", "0")),
}
# =================================


IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")
AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg")


def auto_find(prefix, exts):
    for ext in exts:
        c = f"{prefix}{ext}"
        if os.path.exists(c):
            return c
    return ""


def resolve_inputs():
    img = CONFIG["image_path"] or auto_find("input", IMAGE_EXTS)
    aud = CONFIG["audio_path"] or auto_find("input", AUDIO_EXTS)
    if not img or not os.path.exists(img):
        print("找不到图片"); sys.exit(1)
    if not aud or not os.path.exists(aud):
        print("找不到音频"); sys.exit(1)
    return img, aud


def get_audio_duration(p):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", p],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())


def find_font():
    cands = [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for f in cands:
        if os.path.exists(f):
            return f
    return ""


def build_chunk_filter(chunk_idx, total_chunks, start_frame, total_frames,
                       chunk_duration, font_path, include_title):
    """
    构建某一块的滤镜链。和 make_mv.py 的区别:
    - zoompan 表达式用全局帧号: 1 + (zoom_end-1) * (start_frame + on) / total_frames
      这样块之间镜头是连续的,不会在每段开头跳回原始大小
    - 标题文字只在 chunk_0 (前 title_duration 秒落在这里) 时叠加
    - 音频不在每块里输出 (写 -an),最后统一挂音轨
    """
    w, h, fps = CONFIG["width"], CONFIG["height"], CONFIG["fps"]
    zoom_end = CONFIG["zoom_end"]
    zoom_expr = f"1+({zoom_end}-1)*({start_frame}+on)/{total_frames}"

    fc = (
        f"[0:v]scale={int(w*1.2)}:{int(h*1.2)}:force_original_aspect_ratio=increase,"
        f"crop={int(w*1.2)}:{int(h*1.2)},"
        f"loop=loop=-1:size=1,trim=duration={chunk_duration},fps={fps},"
        f"zoompan=z='{zoom_expr}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
        f"s={w}x{h}:fps={fps},"
        f"noise=alls={CONFIG['noise_strength']}:allf=t,"
        f"vignette=angle={CONFIG['vignette_angle']}"
        f"[bg];"
        f"[1:a]showwaves=s={w}x{CONFIG['waveform_height']}:"
        f"mode=line:colors={CONFIG['waveform_color']}:rate={fps}[wave];"
        f"[bg][wave]overlay=0:H-{CONFIG['waveform_height']}-30:"
        f"format=auto:alpha={CONFIG['waveform_opacity']}"
    )

    if include_title:
        font_escaped = font_path.replace("\\", "/").replace(":", "\\:")
        title_escaped = CONFIG["title_text"].replace("'", "\\'").replace(":", "\\:")
        title_dur = CONFIG["title_duration"]
        fade_in, fade_out = 0.5, 0.5
        alpha_expr = (
            f"if(lt(t,{fade_in}),t/{fade_in},"
            f"if(lt(t,{title_dur - fade_out}),1,"
            f"if(lt(t,{title_dur}),({title_dur}-t)/{fade_out},0)))"
        )
        fc += (
            f"[withwave];"
            f"[withwave]drawtext=fontfile='{font_escaped}':"
            f"text='{title_escaped}':"
            f"fontsize={CONFIG['title_fontsize']}:"
            f"fontcolor={CONFIG['title_color']}:"
            f"x=(w-text_w)/2:y=(h-text_h)/2:"
            f"alpha='{alpha_expr}':"
            f"enable='lt(t,{title_dur})'"
            f"[final]"
        )
    else:
        fc += "[final]"
    return fc


def render_chunk(chunk_idx, total_chunks, start_frame, end_frame, total_frames,
                 img, aud, font, workdir):
    fps = CONFIG["fps"]
    chunk_duration = (end_frame - start_frame) / fps
    start_time = start_frame / fps
    out_path = os.path.join(workdir, f"chunk_{chunk_idx}.mp4")

    print(f"[chunk {chunk_idx+1}/{total_chunks}] "
          f"frames {start_frame}-{end_frame}, "
          f"t={start_time:.2f}s + {chunk_duration:.2f}s → {out_path}")

    fc = build_chunk_filter(
        chunk_idx, total_chunks, start_frame, total_frames,
        chunk_duration, font, include_title=(chunk_idx == 0)
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img,
        "-ss", str(start_time), "-t", str(chunk_duration), "-i", aud,
        "-filter_complex", fc,
        "-map", "[final]",
        "-c:v", "libx264",
        "-threads", "0",
        "-preset", CONFIG["preset"],
        "-b:v", CONFIG["video_bitrate"],
        "-pix_fmt", "yuv420p",
        "-an",                          # 每块都不带音频,最后统一挂
        "-t", str(chunk_duration),
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"chunk {chunk_idx} FFmpeg 报错:")
        print(r.stderr[-2000:])
        sys.exit(1)
    return out_path


def concat_chunks(chunk_paths, workdir, out_video_only):
    """用 concat demuxer + 流复制(无重编码)拼接视频块。"""
    list_path = os.path.join(workdir, "concat.txt")
    with open(list_path, "w", encoding="utf-8") as f:
        for p in chunk_paths:
            f.write(f"file '{os.path.abspath(p)}'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
           "-i", list_path, "-c", "copy", out_video_only]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("concat 报错:")
        print(r.stderr[-2000:]); sys.exit(1)


def mux_audio(video_only, audio_path, out_path):
    """挂音轨:视频流复制 + 音频转 aac,不重编码视频。"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_only, "-i", audio_path,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", CONFIG["audio_bitrate"],
        "-shortest",
        out_path
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("mux 报错:")
        print(r.stderr[-2000:]); sys.exit(1)


def cleanup(workdir, total_chunks):
    """删中间产物 (chunk_*.mp4, concat.txt, video_only.mp4)。"""
    for i in range(total_chunks):
        p = os.path.join(workdir, f"chunk_{i}.mp4")
        if os.path.exists(p):
            os.remove(p)
    for name in ("concat.txt", "video_only.mp4"):
        p = os.path.join(workdir, name)
        if os.path.exists(p):
            os.remove(p)


def main():
    img, aud = resolve_inputs()
    print(f"图片: {img}\n音频: {aud}")

    font = find_font()
    if not font:
        print("找不到可用字体"); sys.exit(1)
    print(f"字体: {font}")

    duration = get_audio_duration(aud)
    fps = CONFIG["fps"]
    total_frames = int(duration * fps)

    # 算分块数
    if CONFIG["chunk_count_override"] > 0:
        total_chunks = CONFIG["chunk_count_override"]
    else:
        total_chunks = max(1, int(duration // CONFIG["chunk_seconds"]) +
                              (1 if duration % CONFIG["chunk_seconds"] > 0.5 else 0))
    chunk_frames = total_frames // total_chunks

    print(f"音频时长: {duration:.2f}s  总帧: {total_frames}  分 {total_chunks} 块")

    workdir = CONFIG["workdir"]
    os.makedirs(workdir, exist_ok=True)

    # 渲染各块
    chunk_paths = []
    for i in range(total_chunks):
        start_frame = i * chunk_frames
        end_frame = total_frames if i == total_chunks - 1 else start_frame + chunk_frames
        chunk_paths.append(render_chunk(
            i, total_chunks, start_frame, end_frame, total_frames,
            img, aud, font, workdir
        ))

    # 拼接(无重编码)
    video_only = os.path.join(workdir, "video_only.mp4")
    print(f"\n拼接 {total_chunks} 块 → {video_only}")
    concat_chunks(chunk_paths, workdir, video_only)

    # 挂音轨
    print(f"挂音轨 → {CONFIG['output_path']}")
    mux_audio(video_only, aud, CONFIG["output_path"])

    # 清理
    cleanup(workdir, total_chunks)

    out_size = os.path.getsize(CONFIG["output_path"]) / 1024 / 1024
    print(f"\n完成! 输出: {CONFIG['output_path']} ({out_size:.1f} MB)")


if __name__ == "__main__":
    main()
