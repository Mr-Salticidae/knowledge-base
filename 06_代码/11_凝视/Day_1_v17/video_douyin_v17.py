"""
《凝视 The Gaze》v17
关键改动:
- 应用排序 A:Scarlatta / NULL-07 / Selenwë / Vesper / Morgana / Veritia
- 第 3 张(Selenwë)入场点从 8.80s 提前到 8.60s
- 钟表音效已在 v16 完全去除,继续保持

时间线:
0.000 - 3.000  开场字幕              (3.00s)
3.000 - 5.900  位置1 SCARLATTA       (2.90s, 带字幕)
5.900 - 8.600  位置2 NULL-07         (2.70s, 带字幕)
8.600 - 11.300 位置3 SELENWË         (2.70s, 带字幕)
11.300-11.900  位置4 VESPER (快闪)    (0.60s, 无字幕)
11.900-13.300  位置5 MORGANA          (1.40s, 带字幕)
13.300-14.000  位置6 VERITIA (压轴)   (0.70s, 无字幕,强化色差)
14.000-15.000  收尾 SIX EYES         (1.00s)
"""

import sys
sys.path.insert(0, "{运行环境}")

from moviepy import (
    ImageClip, CompositeVideoClip, concatenate_videoclips,
    ColorClip, AudioFileClip,
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

W, H = DOUYIN_RESOLUTION
FPS = DOUYIN_FPS
TOTAL_DURATION = 15.00

# ============================================================
# 时间线 + 排序
# ============================================================

# 角色编号映射(原始编号)
CHAR_BY_NUM = {c.num: c for c in CHARACTERS}

# 排序 A:位置 → 角色编号
# 位置 1: Scarlatta (01)
# 位置 2: NULL-07   (03)
# 位置 3: Selenwë   (05)
# 位置 4: Vesper    (02)
# 位置 5: Morgana   (04)
# 位置 6: Veritia   (06)
ORDER = ['01', '03', '05', '02', '04', '06']

# 每个位置的 (start_time, duration, show_name, is_veritia)
POSITIONS = [
    # pos 1
    {'start': 3.000, 'duration': 2.900, 'show_name': True,  'special': None},
    # pos 2
    {'start': 5.900, 'duration': 2.700, 'show_name': True,  'special': None},
    # pos 3 - 起点提前到 8.60
    {'start': 8.600, 'duration': 2.700, 'show_name': True,  'special': None},
    # pos 4 - Vesper 快闪
    {'start': 11.300, 'duration': 0.600, 'show_name': False, 'special': None},
    # pos 5 - Morgana
    {'start': 11.900, 'duration': 1.400, 'show_name': True,  'special': None},
    # pos 6 - Veritia 压轴
    {'start': 13.300, 'duration': 0.700, 'show_name': False, 'special': 'veritia'},
]

OPENING_DURATION = 3.000
ENDING_START = 14.000
ENDING_DURATION = 1.000

# 色差转场参数
GLITCH_DURATION_NORMAL = 0.06
GLITCH_OFFSET_NORMAL = 8
GLITCH_DURATION_VERITIA = 0.12
GLITCH_OFFSET_VERITIA = 14

ENDING_FADEOUT = 0.30

OUTPUT_NO_BGM = OUTPUT_DIR / "douyin_15s_v17_no_bgm.mp4"
OUTPUT_WITH_BGM = OUTPUT_DIR / "complete_15s_v17_with_bgm.mp4"
BGM_FILE = "{运行环境}/bgm_clip_15s.wav"


# ============================================================
# 文字渲染(沿用)
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
# 图片处理 + 色差
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
    img_array = fit_image_to_canvas(image_path, (W, H))
    r = img_array[:, :, 0].copy()
    g = img_array[:, :, 1].copy()
    b = img_array[:, :, 2].copy()
    r_shifted = np.zeros_like(r)
    r_shifted[:, :-offset] = r[:, offset:]
    b_shifted = np.zeros_like(b)
    b_shifted[:, offset:] = b[:, :-offset]
    return np.stack([r_shifted, g, b_shifted], axis=-1)


def build_character_with_glitch(char, total_duration, show_name=True,
                                glitch_duration=GLITCH_DURATION_NORMAL,
                                glitch_offset=GLITCH_OFFSET_NORMAL):
    glitched = make_chromatic_aberration_image(char.image_path, offset=glitch_offset)
    glitch_clip = ImageClip(glitched, duration=glitch_duration)
    
    normal_duration = total_duration - glitch_duration
    img_clip = make_image_clip(char.image_path, normal_duration)
    
    layers = [img_clip]
    
    if show_name:
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
        
        layers.extend([name_clip, num_clip])

    normal_clip = CompositeVideoClip(layers, size=(W, H))
    combined = concatenate_videoclips([glitch_clip, normal_clip], method="chain")
    return combined


def build_opening():
    bg = ColorClip(size=(W, H), color=(0, 0, 0), duration=OPENING_DURATION)
    title_clip = make_text_clip(
        "THIS TIME,\nWHO IS WATCHING?",
        font_path=FONT_EN, font_index=FONT_EN_INDEX,
        font_size=70, duration=OPENING_DURATION,
        letter_spacing=2, max_width=W - 100,
    )
    title_clip = title_clip.with_position(center_position(title_clip, (W, H), 0.45))
    title_clip = title_clip.with_effects([FadeIn(0.4), FadeOut(0.4)])
    return CompositeVideoClip([bg, title_clip], size=(W, H))


def build_ending():
    bg = ColorClip(size=(W, H), color=(0, 0, 0), duration=ENDING_DURATION)
    
    main_clip = make_text_clip(
        "SIX EYES.\nONE DIRECTION.",
        font_path=FONT_EN, font_index=FONT_EN_INDEX,
        font_size=88, duration=ENDING_DURATION,
        letter_spacing=2, max_width=W - 100,
    )
    main_clip = main_clip.with_position(center_position(main_clip, (W, H), 0.42))
    main_clip = main_clip.with_effects([FadeOut(ENDING_FADEOUT)])
    
    sig_clip = make_text_clip(
        "THE GAZE  ·  MR. JUMPING SPIDER",
        font_path=FONT_EN_REG, font_index=FONT_EN_REG_INDEX,
        font_size=28, duration=ENDING_DURATION,
        letter_spacing=2, max_width=W - 100,
    )
    sig_clip = sig_clip.with_position(
        center_position(sig_clip, (W, H), 0.78)
    ).with_opacity(0.5).with_effects([FadeIn(0.2), FadeOut(ENDING_FADEOUT)])

    return CompositeVideoClip([bg, main_clip, sig_clip], size=(W, H))


# ============================================================
# 主流程
# ============================================================

def build_video():
    print("构建视频镜头...")
    
    clips = []
    
    opening = build_opening()
    clips.append(opening)
    print(f"  ✓ 开场 ({OPENING_DURATION:.3f}s)")
    
    # 6 张图按排序 A 排列
    for i, (char_num, pos) in enumerate(zip(ORDER, POSITIONS)):
        char = CHAR_BY_NUM[char_num]
        duration = pos['duration']
        show_name = pos['show_name']
        is_veritia = pos['special'] == 'veritia'
        
        if is_veritia:
            clip = build_character_with_glitch(
                char, duration, show_name=show_name,
                glitch_duration=GLITCH_DURATION_VERITIA,
                glitch_offset=GLITCH_OFFSET_VERITIA,
            )
            print(f"  ✓ 位置{i+1}: {char.num} {char.name_en} ({duration:.3f}s, 强化色差, 无字幕)")
        else:
            clip = build_character_with_glitch(char, duration, show_name=show_name)
            name_state = "" if show_name else " (无字幕)"
            print(f"  ✓ 位置{i+1}: {char.num} {char.name_en} ({duration:.3f}s){name_state}")
        
        clip = clip.with_duration(duration)
        clips.append(clip)
    
    ending = build_ending()
    clips.append(ending)
    print(f"  ✓ 收尾 ({ENDING_DURATION:.3f}s)")
    
    video = concatenate_videoclips(clips, method="chain")
    print(f"\n  视频总时长: {video.duration:.3f}s (目标: {TOTAL_DURATION}s)")
    
    return video


def export_no_bgm_version(video):
    print("\n========== 导出抖音版(完全静音) ==========")
    final = video.without_audio()
    
    final.write_videofile(
        str(OUTPUT_NO_BGM),
        fps=FPS, codec='libx264',
        audio=False,
        preset='medium', threads=4, logger=None,
    )
    
    size_mb = OUTPUT_NO_BGM.stat().st_size / (1024 * 1024)
    print(f"✓ 完成: {OUTPUT_NO_BGM.name} ({size_mb:.1f} MB)")


def export_with_bgm_version(video):
    print("\n========== 导出完整版(只有 BGM) ==========")
    
    bgm = AudioFileClip(BGM_FILE)
    print(f"  BGM 加载: {bgm.duration:.3f}s")
    
    final = video.with_audio(bgm)
    
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
    print("《凝视》v17 - 排序A + 第3张提前到8.60s")
    print("="*60)
    
    print("\n排序方案 A:")
    pos_names = ['Scarlatta', 'NULL-07', 'Selenwë', 'Vesper', 'Morgana', 'Veritia']
    for i, (num, name) in enumerate(zip(ORDER, pos_names)):
        char = CHAR_BY_NUM[num]
        pos = POSITIONS[i]
        print(f"  位置 {i+1}: 原编号 {num} {name:<10}  起 {pos['start']:>5.3f}s  时长 {pos['duration']:.2f}s")
    
    print()
    video = build_video()
    export_no_bgm_version(video)
    export_with_bgm_version(video)
    
    print("\n" + "="*60)
    print("v17 生成完成")
    print("="*60)


if __name__ == "__main__":
    main()
