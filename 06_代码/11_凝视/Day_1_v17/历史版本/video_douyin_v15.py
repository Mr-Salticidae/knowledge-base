"""
《凝视 The Gaze》v15
关键改动:
- 所有视觉切换对齐 onset(打击瞬间),消除"画面滞后"
- 所有 6 张图都加色差转场入场:5 普通(8px / 0.06s) + Veritia 强化(14px / 0.12s)
- 收尾 14.05s 出字幕,0.92s 总显示时间(可读性 + 14.37 强 onset 二次冲击)

时间线:
0.000 - 3.790  开场字幕(BGM 静默→build up)
3.790 - 5.870  Scarlatta(★ 最强 onset 0.245 入场)
5.870 - 7.680  Vesper
7.680 - 9.050  NULL-07(★ 最强 onset 0.245 入场)
9.050 - 11.200 Morgana
11.200 - 12.970 Selenwë
12.970 - 14.050 Veritia(★ 强 onset 0.137 入场,色差强化)
14.050 - 15.000 收尾(14.05s 字幕硬切,14.37s 强 onset 二次冲击,15.00s 淡出结束)
"""

import sys
sys.path.insert(0, "/home/claude")

from moviepy import (
    ImageClip, CompositeVideoClip, concatenate_videoclips,
    ColorClip, CompositeAudioClip, AudioFileClip,
)
from moviepy.video.fx import FadeIn, FadeOut, Resize
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pathlib import Path

from video_config import (
    CHARACTERS, OUTPUT_DIR,
    FONT_EN, FONT_EN_INDEX,
    FONT_EN_REG, FONT_EN_REG_INDEX,
    DOUYIN_RESOLUTION, DOUYIN_FPS,
)
from sound_effects import pulse

W, H = DOUYIN_RESOLUTION
FPS = DOUYIN_FPS

# ============================================================
# 时间线(基于 onset 数据精确设计)
# ============================================================

TOTAL_DURATION = 15.00

# 8 段时间线 (start_time, duration)
SEG = {
    'opening':   (0.000, 3.790),    # 开场字幕
    'scarlatta': (3.790, 2.080),    # ★ onset 3.79s 最强 0.245
    'vesper':    (5.870, 1.810),    # onset 5.87s 0.078
    'null07':    (7.680, 1.370),    # ★ onset 9.05s 最强 0.245(在NULL-07末尾切到Morgana)
    'morgana':   (9.050, 2.150),    # onset 9.05s 入场
    'selenwe':   (11.200, 1.770),   # onset 11.20s 入场
    'veritia':   (12.970, 1.080),   # ★ onset 12.97s 入场,onset 14.05s 切走
    'ending':    (14.050, 0.950),   # onset 14.05s 字幕入场,14.37s 强onset二次冲击
}

# 色差转场参数
GLITCH_DURATION_NORMAL = 0.06   # 普通色差 60ms
GLITCH_OFFSET_NORMAL = 8        # 普通色差偏移 8px
GLITCH_DURATION_VERITIA = 0.12  # Veritia 色差 120ms
GLITCH_OFFSET_VERITIA = 14      # Veritia 色差偏移 14px

# 收尾字幕动画
ENDING_HOLD = 0.62      # 字幕停留 0.62s(硬切到 14.67s)
ENDING_FADEOUT = 0.30   # 字幕淡出 0.30s(14.67s → 14.97s)
# 14.05 + 0.62 + 0.30 = 14.97s,留 30ms 黑屏结尾

OUTPUT_NO_BGM = OUTPUT_DIR / "douyin_15s_v15_no_bgm.mp4"
OUTPUT_WITH_BGM = OUTPUT_DIR / "complete_15s_v15_with_bgm.mp4"
BGM_FILE = "/home/claude/bgm_clip_15s.wav"

# ============================================================
# 文字渲染(沿用 v14)
# ============================================================

def load_font(font_path, font_size, index=0):
    if font_path.endswith('.ttc'):
        return ImageFont.truetype(font_path, font_size, index=index)
    return ImageFont.truetype(font_path, font_size)


def render_text_image(text, font_path, font_size, font_index=0,
                     color=(255, 255, 255), letter_spacing=0,
                     align='center', stroke=False, max_width=None):
    lines = text.split('\n')

    if max_width:
        for try_size in range(font_size, 10, -2):
            try_font = load_font(font_path, try_size, font_index)
            test_lines = lines
            if letter_spacing > 0:
                test_lines = [(' ' * letter_spacing).join(line) for line in lines]
            max_line_w = 0
            for line in test_lines:
                bbox = try_font.getbbox(line)
                max_line_w = max(max_line_w, bbox[2] - bbox[0])
            if max_line_w <= max_width - try_size:
                font_size = try_size
                break

    font = load_font(font_path, font_size, font_index)
    if letter_spacing > 0:
        lines = [(' ' * letter_spacing).join(line) for line in lines]

    line_metrics = []
    max_w = 0
    for line in lines:
        bbox = font.getbbox(line)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        line_metrics.append((line, line_w, line_h, bbox))
        max_w = max(max_w, line_w)

    line_spacing = int(font_size * 0.4)
    total_h = sum(m[2] for m in line_metrics) + line_spacing * (len(lines) - 1)

    padding = font_size
    canvas_w = max_w + padding * 2
    canvas_h = total_h + padding * 2

    img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = padding
    for line, line_w, line_h, bbox in line_metrics:
        if align == 'center':
            x = (canvas_w - line_w) // 2 - bbox[0]
        elif align == 'left':
            x = padding - bbox[0]
        else:
            x = canvas_w - line_w - padding - bbox[0]

        if stroke:
            for dx, dy in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1),(0,-1),(1,0),(-1,0)]:
                draw.text((x + dx, y + dy - bbox[1]), line, font=font, fill=(0,0,0,180))

        draw.text((x, y - bbox[1]), line, font=font, fill=color)
        y += line_h + line_spacing

    return np.array(img)


def make_text_clip(text, font_path, font_size, duration, font_index=0,
                   color=(255, 255, 255), letter_spacing=0,
                   stroke=False, max_width=None):
    img_array = render_text_image(
        text, font_path, font_size, font_index=font_index,
        color=color, letter_spacing=letter_spacing,
        stroke=stroke, max_width=max_width
    )
    return ImageClip(img_array, duration=duration, transparent=True)


def center_position(clip, canvas_size, y_offset_ratio=0.5):
    cw, ch = canvas_size
    clip_w, clip_h = clip.size
    x = (cw - clip_w) // 2
    y = int(ch * y_offset_ratio - clip_h / 2)
    return (x, y)


# ============================================================
# 图片处理 + 色差转场
# ============================================================

def fit_image_to_canvas(image_path, canvas_size, face_offset=0.05):
    img = Image.open(image_path)
    iw, ih = img.size
    cw, ch = canvas_size
    scale = max(cw / iw, ch / ih)
    new_w = int(iw * scale)
    new_h = int(ih * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - cw) // 2
    top = max(0, (new_h - ch) // 2 - int(ch * face_offset))
    top = min(top, new_h - ch)
    img = img.crop((left, top, left + cw, top + ch))
    return np.array(img)


def make_image_clip(image_path, duration, ken_burns=True, zoom_amount=0.06):
    img_array = fit_image_to_canvas(image_path, (W, H))
    clip = ImageClip(img_array, duration=duration)
    if ken_burns:
        clip = clip.with_effects([Resize(lambda t: 1.0 + zoom_amount * (t / duration))])
    return clip


def make_chromatic_aberration_image(image_path, offset=8):
    """色差效果:红通道左偏 offset,蓝通道右偏 offset"""
    img_array = fit_image_to_canvas(image_path, (W, H))
    
    r = img_array[:, :, 0].copy()
    g = img_array[:, :, 1].copy()
    b = img_array[:, :, 2].copy()
    
    r_shifted = np.zeros_like(r)
    r_shifted[:, :-offset] = r[:, offset:]
    
    b_shifted = np.zeros_like(b)
    b_shifted[:, offset:] = b[:, :-offset]
    
    result = np.stack([r_shifted, g, b_shifted], axis=-1)
    return result


def build_character_with_glitch(char, total_duration, 
                                glitch_duration=GLITCH_DURATION_NORMAL,
                                glitch_offset=GLITCH_OFFSET_NORMAL):
    """
    带色差转场的角色镜头
    总时长 = glitch_duration + 正常画面时长
    """
    # 色差闪烁
    glitched = make_chromatic_aberration_image(char.image_path, offset=glitch_offset)
    glitch_clip = ImageClip(glitched, duration=glitch_duration)
    
    # 正常画面(含 ken burns 和字幕)
    normal_duration = total_duration - glitch_duration
    
    img_clip = make_image_clip(char.image_path, normal_duration)
    name_clip = make_text_clip(
        char.name_en,
        font_path=FONT_EN_REG, font_index=FONT_EN_REG_INDEX,
        font_size=42, duration=normal_duration,
        letter_spacing=3, color=(255, 255, 255),
        stroke=True, max_width=W - 80,
    )
    name_clip = name_clip.with_position(
        center_position(name_clip, (W, H), 0.86)
    ).with_opacity(0.9).with_effects([FadeIn(0.15)])

    num_clip = make_text_clip(
        f"{char.num} / 06",
        font_path=FONT_EN_REG, font_index=FONT_EN_REG_INDEX,
        font_size=24, duration=normal_duration,
        letter_spacing=4, color=(255, 255, 255),
        stroke=True, max_width=W - 80,
    )
    num_clip = num_clip.with_position(
        center_position(num_clip, (W, H), 0.92)
    ).with_opacity(0.6).with_effects([FadeIn(0.2)])

    normal_clip = CompositeVideoClip([img_clip, name_clip, num_clip], size=(W, H))
    
    # 拼接 glitch + normal
    combined = concatenate_videoclips([glitch_clip, normal_clip], method="chain")
    
    return combined


def build_opening():
    """开场字幕(0-3.79s)"""
    duration = SEG['opening'][1]
    bg = ColorClip(size=(W, H), color=(0, 0, 0), duration=duration)
    title_clip = make_text_clip(
        "THIS TIME,\nWHO IS WATCHING?",
        font_path=FONT_EN, font_index=FONT_EN_INDEX,
        font_size=70, duration=duration,
        letter_spacing=2, max_width=W - 100,
    )
    title_clip = title_clip.with_position(center_position(title_clip, (W, H), 0.45))
    # 充分利用 3.79s 的时长:慢渐入 + 久停留 + 渐出在 onset 前完成
    title_clip = title_clip.with_effects([FadeIn(0.5), FadeOut(0.4)])
    return CompositeVideoClip([bg, title_clip], size=(W, H))


def build_ending():
    """收尾字幕(14.05-15.00s,共0.95s)"""
    duration = SEG['ending'][1]
    bg = ColorClip(size=(W, H), color=(0, 0, 0), duration=duration)
    
    # 主字幕硬切出现 → 0.62s 停留 → 0.30s 淡出
    main_clip = make_text_clip(
        "SIX EYES.\nONE DIRECTION.",
        font_path=FONT_EN, font_index=FONT_EN_INDEX,
        font_size=88, duration=duration,
        letter_spacing=2, max_width=W - 100,
    )
    main_clip = main_clip.with_position(center_position(main_clip, (W, H), 0.42))
    main_clip = main_clip.with_effects([FadeOut(ENDING_FADEOUT)])
    
    sig_clip = make_text_clip(
        "THE GAZE  ·  MR. JUMPING SPIDER",
        font_path=FONT_EN_REG, font_index=FONT_EN_REG_INDEX,
        font_size=28, duration=duration,
        letter_spacing=2, max_width=W - 100,
    )
    sig_clip = sig_clip.with_position(
        center_position(sig_clip, (W, H), 0.78)
    ).with_opacity(0.5).with_effects([FadeIn(0.2), FadeOut(ENDING_FADEOUT)])

    return CompositeVideoClip([bg, main_clip, sig_clip], size=(W, H))


# ============================================================
# 音效编排
# ============================================================

def build_sfx_track(for_bgm_version=False):
    """
    构建咔嗒音效轨
    咔嗒卡在每个角色"色差转场结束、正常画面开始"的时刻
    
    实际上,咔嗒应该在视觉切换的瞬间,即色差闪烁开始时
    """
    audio_elements = []
    
    click_volume = 0.55 if for_bgm_version else 0.95
    
    # 5 个普通角色的入场咔嗒(Scarlatta, Vesper, NULL-07, Morgana, Selenwë)
    # 时间是该角色 segment 的开始时间
    char_keys = ['scarlatta', 'vesper', 'null07', 'morgana', 'selenwe']
    for key in char_keys:
        t = SEG[key][0]
        click = pulse(duration=0.04, volume=click_volume).with_start(t)
        audio_elements.append(click)
    
    return CompositeAudioClip(audio_elements)


# ============================================================
# 主流程
# ============================================================

def build_video():
    """构建视频(无音频)"""
    print("构建视频镜头...")
    
    clips = []
    
    # 0-3.79s 开场
    opening = build_opening()
    clips.append(opening)
    print(f"  ✓ 开场 ({SEG['opening'][1]:.3f}s)")
    
    # 6 个角色镜头(都带色差转场)
    char_keys = ['scarlatta', 'vesper', 'null07', 'morgana', 'selenwe', 'veritia']
    for key in char_keys:
        char = next(c for c in CHARACTERS if c.name_en.lower().replace('-', '').replace('null07', 'null-07') == key.replace('null07', 'null-07') or c.num == {
            'scarlatta': '01', 'vesper': '02', 'null07': '03', 
            'morgana': '04', 'selenwe': '05', 'veritia': '06'
        }[key])
        
        duration = SEG[key][1]
        
        if key == 'veritia':
            # Veritia: 强化色差
            clip = build_character_with_glitch(
                char, duration,
                glitch_duration=GLITCH_DURATION_VERITIA,
                glitch_offset=GLITCH_OFFSET_VERITIA,
            )
            print(f"  ✓ 06 VERITIA ({duration:.3f}s, 色差强化 {GLITCH_OFFSET_VERITIA}px / {GLITCH_DURATION_VERITIA}s)")
        else:
            # 普通角色:统一色差
            clip = build_character_with_glitch(char, duration)
            print(f"  ✓ {char.num} {char.name_en} ({duration:.3f}s)")
        
        # 强制设置精确时长(消除拼接精度损失)
        clip = clip.with_duration(duration)
        clips.append(clip)
    
    # 收尾
    ending = build_ending()
    clips.append(ending)
    print(f"  ✓ 收尾 ({SEG['ending'][1]:.3f}s)")
    
    # 拼接
    video = concatenate_videoclips(clips, method="chain")
    
    print(f"\n  各 clip 时长: ", end="")
    for c in clips:
        print(f"{c.duration:.3f} ", end="")
    print()
    print(f"  视频总时长: {video.duration:.3f}s (目标: {TOTAL_DURATION}s)")
    
    return video


def export_no_bgm_version(video):
    print("\n========== 导出抖音版(无 BGM) ==========")
    sfx = build_sfx_track(for_bgm_version=False)
    final = video.with_audio(sfx)
    
    final.write_videofile(
        str(OUTPUT_NO_BGM),
        fps=FPS, codec='libx264',
        audio_codec='aac', audio_bitrate='192k',
        preset='medium', threads=4, logger=None,
    )
    
    size_mb = OUTPUT_NO_BGM.stat().st_size / (1024 * 1024)
    print(f"✓ 完成: {OUTPUT_NO_BGM.name} ({size_mb:.1f} MB)")


def export_with_bgm_version(video):
    print("\n========== 导出完整版(含 BGM) ==========")
    
    bgm = AudioFileClip(BGM_FILE)
    print(f"  BGM 加载: {bgm.duration:.3f}s")
    
    sfx = build_sfx_track(for_bgm_version=True)
    full_audio = CompositeAudioClip([bgm, sfx])
    
    final = video.with_audio(full_audio)
    
    final.write_videofile(
        str(OUTPUT_WITH_BGM),
        fps=FPS, codec='libx264',
        audio_codec='aac', audio_bitrate='192k',
        preset='medium', threads=4, logger=None,
    )
    
    size_mb = OUTPUT_WITH_BGM.stat().st_size / (1024 * 1024)
    print(f"✓ 完成: {OUTPUT_WITH_BGM.name} ({size_mb:.1f} MB)")


def main():
    print("="*60)
    print("《凝视》v15 - onset 精确卡点 + 全图色差转场")
    print("="*60)
    
    # 显示时间线
    print("\n时间线:")
    print(f"{'段':<12} {'起':<8} {'止':<8} {'时长':<8}")
    print('-' * 50)
    for key, (start, dur) in SEG.items():
        end = start + dur
        print(f"  {key:<10} {start:>5.3f}s  {end:>5.3f}s  {dur:>5.3f}s")
    
    print()
    video = build_video()
    export_no_bgm_version(video)
    export_with_bgm_version(video)
    
    print("\n" + "="*60)
    print("v15 生成完成")
    print("="*60)


if __name__ == "__main__":
    main()
