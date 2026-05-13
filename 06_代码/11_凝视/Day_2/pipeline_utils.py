"""
《凝视 The Gaze》Day 2 · 通用工具函数

从 Day 1 v17 的 video_douyin_v17.py 抽出可复用的工具,
保持 Day 2 模块的自包含(不依赖父目录的相对 import)。

包含:
- load_font / render_text_image / make_text_clip  :PIL 字幕渲染(MoviePy 自带 TextClip 中文字体不可控)
- center_position                                  :文字定位
- fit_image_to_canvas / make_image_clip            :图片适配 + Ken Burns 缩放
- make_chromatic_aberration_image                  :色差转场素材生成
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageClip
from moviepy.video.fx import Resize


# ============================================================
# 字体 + 文字渲染
# ============================================================

def load_font(font_path: str, font_size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    """加载字体。.ttc 多字重容器需要传 index 选择具体字重。"""
    if str(font_path).endswith('.ttc'):
        return ImageFont.truetype(str(font_path), font_size, index=index)
    return ImageFont.truetype(str(font_path), font_size)


def render_text_image(text, font_path, font_size, font_index=0,
                      color=(255, 255, 255), letter_spacing=0,
                      align='center', stroke=False, max_width=None,
                      stroke_alpha=180):
    """
    用 PIL 把文字渲染成 RGBA numpy 数组,可直接给 MoviePy.ImageClip。

    参数:
      text          : 文字内容,支持 \n 多行
      font_path     : 字体文件绝对路径
      font_size     : 字号
      font_index    : .ttc 字重索引
      color         : 文字 RGB 颜色
      letter_spacing: 字间距(用空格模拟)
      align         : 'center' / 'left' / 'right'
      stroke        : 是否描黑边(浅色背景下兜底可读性)
      max_width     : 自动缩字保证不超过该宽度(像素)
      stroke_alpha  : 描边的不透明度(0-255)
    """
    lines = text.split('\n')

    # 如果指定了最大宽度,从大到小试,直到所有行都能放下
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

    # 测量每行
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
                draw.text((x + dx, y + dy - bbox[1]), line, font=font, fill=(0, 0, 0, stroke_alpha))

        draw.text((x, y - bbox[1]), line, font=font, fill=color)
        y += line_h + line_spacing

    return np.array(img)


def make_text_clip(text, font_path, font_size, duration, font_index=0,
                   color=(255, 255, 255), letter_spacing=0,
                   stroke=False, max_width=None) -> ImageClip:
    """渲染文字 PNG 并返回 MoviePy ImageClip。"""
    img_array = render_text_image(
        text, font_path, font_size, font_index=font_index,
        color=color, letter_spacing=letter_spacing,
        stroke=stroke, max_width=max_width,
    )
    return ImageClip(img_array, duration=duration, transparent=True)


def center_position(clip, canvas_size, y_offset_ratio=0.5):
    """
    计算 clip 在画布中居中(水平)+ 在画布高度 y_offset_ratio 处垂直对齐(中心)的坐标。
    """
    cw, ch = canvas_size
    clip_w, clip_h = clip.size
    x = (cw - clip_w) // 2
    y = int(ch * y_offset_ratio - clip_h / 2)
    return (x, y)


# ============================================================
# 图片处理 + Ken Burns
# ============================================================

def fit_image_to_canvas(image_path, canvas_size, face_offset=0.05):
    """
    把任意尺寸图片精准填满目标画布(cover 模式)。
    face_offset:面部黄金分割位向上偏移(0.05 = 画布高度 5%),让构图重心更舒服。
    """
    img = Image.open(image_path).convert("RGB")
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


def make_image_clip(image_path, duration, canvas_size,
                    ken_burns=True, zoom_amount=0.06) -> ImageClip:
    """
    生成单张静态图的 ImageClip,默认带 Ken Burns 缓慢推近。
    zoom_amount:在 duration 内累计缩放的比例(0.06 = 6%)
    """
    img_array = fit_image_to_canvas(image_path, canvas_size)
    clip = ImageClip(img_array, duration=duration)
    if ken_burns:
        clip = clip.with_effects([Resize(lambda t: 1.0 + zoom_amount * (t / duration))])
    return clip


def make_chromatic_aberration_image(image_path, canvas_size, offset=8):
    """
    生成色差转场素材:R 通道左移、B 通道右移,产生类似信号扭曲的视觉冲击。
    offset 范围保持在画布宽度的 5% 以内(超过会出现明显黑边)。
    """
    img_array = fit_image_to_canvas(image_path, canvas_size)
    r = img_array[:, :, 0].copy()
    g = img_array[:, :, 1].copy()
    b = img_array[:, :, 2].copy()
    r_shifted = np.zeros_like(r)
    r_shifted[:, :-offset] = r[:, offset:]
    b_shifted = np.zeros_like(b)
    b_shifted[:, offset:] = b[:, :-offset]
    return np.stack([r_shifted, g, b_shifted], axis=-1)
