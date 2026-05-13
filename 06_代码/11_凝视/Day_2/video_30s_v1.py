"""
《凝视 The Gaze》Day 2 · 184 秒 VERITIA 独白剧场 · 主代码

性能优化:
  - PREVIEW_MODE = True  → 跳过 Ken Burns + 540p 渲染,~1.5 分钟出预演,适合调字幕/卡点
  - PREVIEW_MODE = False → 完整渲染(1080×1920 + Ken Burns),适合 review 和发布

时间线见 video_config_day2.py 的 SHOTS。
"""

from pathlib import Path

from moviepy import (
    VideoFileClip, CompositeVideoClip, concatenate_videoclips,
    ColorClip, AudioFileClip,
)
from moviepy.video.fx import FadeIn, FadeOut

import video_config_day2 as cfg
from pipeline_utils import (
    make_text_clip, center_position, make_image_clip,
)


# ============================================================
# 性能开关(改这两个值控制速度 vs 质量)
# ============================================================

PREVIEW_MODE = False   # True = 快速预演(跳 ken_burns + 540p),False = 完整质量
ENCODE_PRESET = 'ultrafast'  # 'ultrafast' / 'fast' / 'medium' — 发布前可改 'medium' 出小文件
ENCODE_THREADS = 8

if PREVIEW_MODE:
    W, H = 540, 960            # 1/2 分辨率,像素量 1/4
    FPS = cfg.FPS
    KEN_BURNS = False
    print("[预演模式] 540p + 跳过 Ken Burns,目标 ~1.5 分钟出片")
else:
    W, H = cfg.RESOLUTION       # 1080×1920
    FPS = cfg.FPS
    KEN_BURNS = True


def resolve_asset(shot):
    if shot.asset and Path(shot.asset).exists():
        return Path(shot.asset), False
    if getattr(shot, 'placeholder', None) and Path(shot.placeholder).exists():
        return Path(shot.placeholder), True
    if shot.kind == 'static_image':
        return cfg.PLACEHOLDER_FULLBODY, True
    if shot.kind == 'ai_video':
        return cfg.PLACEHOLDER_HALFBODY, True
    return None, False


# ============================================================
# 镜头构建
# ============================================================

def build_title_shot(shot):
    return ColorClip(size=(W, H), color=(0, 0, 0), duration=shot.duration)


def build_ai_video_shot(shot):
    asset, is_placeholder = resolve_asset(shot)

    if is_placeholder:
        print(f"  [占位] 镜头 {shot.idx} ({shot.desc}) 用占位图 {asset.name}")
        zoom = cfg.KEN_BURNS_ZOOM * 1.5 if KEN_BURNS else 0.0
        return make_image_clip(asset, shot.duration, (W, H),
                               ken_burns=KEN_BURNS, zoom_amount=zoom)

    print(f"  [视频] 镜头 {shot.idx} ({shot.desc}) 加载 {asset.name}")
    video = VideoFileClip(str(asset))

    if video.duration >= shot.duration:
        video = video.subclipped(0, shot.duration)
    else:
        print(f"  [WARN] 视频时长 {video.duration:.2f}s < 镜头需求 {shot.duration:.2f}s")
        video = video.with_duration(shot.duration)

    if video.size != [W, H]:
        from moviepy.video.fx import Resize
        scale = max(W / video.w, H / video.h)
        video = video.with_effects([Resize(scale)])

    return video


def build_static_image_shot(shot):
    asset, is_placeholder = resolve_asset(shot)
    label = "[占位]" if is_placeholder else "[图片]"
    print(f"  {label} 镜头 {shot.idx} ({shot.desc}) 用 {asset.name}")
    zoom = cfg.KEN_BURNS_ZOOM if KEN_BURNS else 0.0
    return make_image_clip(asset, shot.duration, (W, H),
                           ken_burns=KEN_BURNS, zoom_amount=zoom)


def build_main_track():
    print("\n构建镜头...")
    clips = []
    for shot in cfg.SHOTS:
        if shot.kind == 'title':
            clip = build_title_shot(shot)
        elif shot.kind == 'ai_video':
            clip = build_ai_video_shot(shot)
        elif shot.kind == 'static_image':
            clip = build_static_image_shot(shot)
        else:
            raise ValueError(f"未知镜头类型: {shot.kind}")
        clip = clip.with_duration(shot.duration)
        clips.append(clip)
        print(f"  ✓ 镜头 {shot.idx}: {shot.start:.1f}-{shot.end:.1f}s ({shot.duration:.2f}s)")

    track = concatenate_videoclips(clips, method="chain")
    print(f"\n  主轨道总时长: {track.duration:.3f}s (目标: {cfg.TOTAL_DURATION}s)")
    return track


# ============================================================
# 字幕轨道
# ============================================================

def build_subtitle_clip(sub):
    if sub.style == 'opening':
        font_path, font_index = cfg.FONT_EN, cfg.FONT_EN_INDEX
        font_size = cfg.FONT_SIZE_OPENING
        spacing = cfg.LETTER_SPACING_OPENING
        y_offset = 0.45
    elif sub.style == 'ending':
        font_path, font_index = cfg.FONT_EN, cfg.FONT_EN_INDEX
        font_size = cfg.FONT_SIZE_ENDING
        spacing = cfg.LETTER_SPACING_ENDING
        y_offset = 0.45
    else:
        font_path, font_index = cfg.FONT_CN, cfg.FONT_CN_INDEX
        font_size = cfg.FONT_SIZE_MONOLOGUE
        spacing = cfg.LETTER_SPACING_MONOLOGUE
        y_offset = 0.78

    # 预演模式字号缩放(540p 上字号要按比例缩小)
    if PREVIEW_MODE:
        font_size = int(font_size * W / cfg.RESOLUTION[0])

    duration = sub.total_duration
    clip = make_text_clip(
        sub.text,
        font_path=font_path, font_index=font_index,
        font_size=font_size, duration=duration,
        letter_spacing=spacing, color=(255, 255, 255),
        stroke=True, max_width=W - int(120 * W / cfg.RESOLUTION[0]),
    )
    clip = clip.with_position(center_position(clip, (W, H), y_offset))
    clip = clip.with_start(sub.fade_in_at)
    clip = clip.with_effects([FadeIn(sub.fade_in_duration), FadeOut(sub.fade_out_duration)])
    return clip


def build_subtitle_layers():
    print("\n构建字幕...")
    clips = []
    for sub in cfg.SUBTITLES:
        clip = build_subtitle_clip(sub)
        clips.append(clip)
        first_line = sub.text.split('\n')[0]
        print(f"  ✓ {sub.fade_in_at:.1f}s - {sub.hold_until + sub.fade_out_duration:.1f}s [{sub.style}] {first_line}")
    return clips


# ============================================================
# 音频
# ============================================================

def build_audio():
    audio_clips = []
    if cfg.BGM_FILE.exists():
        bgm = AudioFileClip(str(cfg.BGM_FILE))
        if bgm.duration > cfg.TOTAL_DURATION:
            bgm = bgm.subclipped(0, cfg.TOTAL_DURATION)
        audio_clips.append(bgm)
        print(f"  [BGM] 加载 {cfg.BGM_FILE.name} ({bgm.duration:.2f}s)")
    else:
        print(f"  [BGM] 文件不存在: {cfg.BGM_FILE.name}(跳过)")

    if not audio_clips:
        return None
    if len(audio_clips) == 1:
        return audio_clips[0]

    from moviepy import CompositeAudioClip
    return CompositeAudioClip(audio_clips)


# ============================================================
# 主流程
# ============================================================

def build_video():
    main_track = build_main_track()
    subtitle_layers = build_subtitle_layers()
    final = CompositeVideoClip([main_track] + subtitle_layers, size=(W, H))
    final = final.with_duration(cfg.TOTAL_DURATION)
    return final


def export(video, audio, output_path: Path, with_audio: bool):
    suffix = '_preview' if PREVIEW_MODE else ''
    output_path = output_path.parent / f"{output_path.stem}{suffix}{output_path.suffix}"

    print(f"\n========== 导出 {'含音频' if with_audio else '无音频'} 版 ==========")
    print(f"  目标: {output_path}")
    print(f"  分辨率: {W}×{H}, FPS: {FPS}, preset: {ENCODE_PRESET}, threads: {ENCODE_THREADS}")

    if with_audio and audio is not None:
        final = video.with_audio(audio)
        final.write_videofile(
            str(output_path),
            fps=FPS, codec='libx264',
            audio_codec='aac', audio_bitrate='192k',
            preset=ENCODE_PRESET, threads=ENCODE_THREADS, logger='bar',
        )
    else:
        final = video.without_audio()
        final.write_videofile(
            str(output_path),
            fps=FPS, codec='libx264', audio=False,
            preset=ENCODE_PRESET, threads=ENCODE_THREADS, logger='bar',
        )

    size_mb = output_path.stat().st_size / (1024 * 1024)
    print(f"✓ 完成: {output_path.name} ({size_mb:.1f} MB)")


def main():
    mode_label = "预演模式" if PREVIEW_MODE else "完整质量"
    print("=" * 60)
    print(f"《凝视》Day 2 · 184s VERITIA 独白剧场 · {mode_label}")
    print("=" * 60)

    print("\n时间线:")
    for shot in cfg.SHOTS:
        print(f"  镜头 {shot.idx:>2}: {shot.start:>5.1f}-{shot.end:>5.1f}s ({shot.duration:>5.2f}s) [{shot.kind:>12s}] {shot.desc}")

    video = build_video()
    audio = build_audio()

    export(video, audio, cfg.OUTPUT_NO_AUDIO, with_audio=False)

    if audio is not None:
        export(video, audio, cfg.OUTPUT_WITH_BGM, with_audio=True)
    else:
        print("\n[跳过] BGM 不存在,不生成含 BGM 版本。")

    print("\n" + "=" * 60)
    print(f"完成。{'快速预演' if PREVIEW_MODE else '完整质量'}版本已写入 Day_2_输出/")
    print("=" * 60)


if __name__ == "__main__":
    main()
