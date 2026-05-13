"""
《大地之上》封面 · 纪录片标题卡排版

设计:
- 顶部:小字英文 "RECOVERED FOOTAGE · 2027" + "A DOCUMENTARY"
- 中下部:大字中文标题《大地之上》(衬线宋体,字距 +60)
- 底部小字:发现年份 / 序号 / 模拟纪录片元数据
- 全英文/数字用衬线西文,中文用宋体(uming)
- 一切克制,文字总占面积 < 12%
- 加微薄的胶片噪点
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/mr_jumping_spider_cinematic_still_ultra_wide_establishing_sho_9c654027-54aa-4e33-acfe-9e7b6af9a7bf_2.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/00_封面_大地之上.png"

MING_FONT  = "/sessions/tender-admiring-galileo/.local/share/fonts/uming.ttc"   # 中文衬线
SERIF_LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"               # 英文衬线
SERIF_LATIN_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"封面尺寸: {W}x{H}")

# Step 1: 极轻调色(让胶片感更强一点,不是动颜色)
arr = np.asarray(img, dtype=np.float32) / 255.0
mid = 0.5
arr = mid + (arr - mid) * 1.05  # 微提对比
arr = np.clip(arr, 0, 1)

# 加胶片噪点(很轻)
rng = np.random.RandomState(2027)
noise = (rng.rand(H, W) - 0.5) * 0.025  # ±1.25% 强度
arr = np.clip(arr + noise[..., None], 0, 1)

# 微暗角(纪录片质感)
yy, xx = np.meshgrid(np.linspace(-1, 1, H), np.linspace(-1, 1, W), indexing="ij")
radius = np.sqrt(xx ** 2 + yy ** 2)
vignette = 1.0 - np.clip((radius - 0.5) * 0.20, 0, 0.18)
arr *= vignette[..., None]

arr = np.clip(arr * 255, 0, 255).astype(np.uint8)
canvas = Image.fromarray(arr).convert("RGBA")

# ============ 文字层 ============

def draw_letter_spaced(draw, text, font, x, y, fill, letter_spacing):
    """手动逐字渲染以实现自定义字距"""
    cur_x = x
    for ch in text:
        bb = draw.textbbox((0, 0), ch, font=font)
        draw.text((cur_x, y), ch, font=font, fill=fill)
        cur_x += (bb[2] - bb[0]) + letter_spacing

def text_width_with_spacing(font, text, letter_spacing):
    """计算字距文本总宽度"""
    total = 0
    tmp_img = Image.new("L", (10, 10))
    d = ImageDraw.Draw(tmp_img)
    for ch in text:
        bb = d.textbbox((0, 0), ch, font=font)
        total += (bb[2] - bb[0]) + letter_spacing
    return total - letter_spacing  # 最后一个字不要加 spacing


text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
tdraw = ImageDraw.Draw(text_layer)

# ---- 顶部小字 1: A DOCUMENTARY ----
top_label = "A   DOCUMENTARY"
top_size = int(H / 60)
top_font = ImageFont.truetype(SERIF_LATIN, top_size)
top_spacing = int(top_size * 0.5)
top_w = text_width_with_spacing(top_font, top_label, top_spacing)
top_x = (W - top_w) // 2
top_y = int(H * 0.045)
draw_letter_spaced(tdraw, top_label, top_font, top_x, top_y, (235, 230, 215, 220), top_spacing)

# 顶部细线
line_y = int(H * 0.075)
line_w = int(W * 0.30)
line_x = (W - line_w) // 2
tdraw.line([(line_x, line_y), (line_x + line_w, line_y)], fill=(235, 230, 215, 160), width=1)

# ---- 顶部小字 2: RECOVERED FOOTAGE · 2027 ----
top2_label = "RECOVERED  FOOTAGE  ·  2027"
top2_size = int(H / 75)
top2_font = ImageFont.truetype(SERIF_LATIN, top2_size)
top2_spacing = int(top2_size * 0.4)
top2_w = text_width_with_spacing(top2_font, top2_label, top2_spacing)
top2_x = (W - top2_w) // 2
top2_y = int(H * 0.085)
draw_letter_spaced(tdraw, top2_label, top2_font, top2_x, top2_y, (220, 215, 200, 200), top2_spacing)

# ---- 主标题《大地之上》— 衬线宋体,大字距 ----
title = "大地之上"
title_size = int(H / 13)
title_font = ImageFont.truetype(MING_FONT, title_size)
title_spacing = int(title_size * 0.18)
title_w = text_width_with_spacing(title_font, title, title_spacing)
title_x = (W - title_w) // 2
title_y = int(H * 0.74)

# 标题阴影(轻度)
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sdraw = ImageDraw.Draw(shadow_layer)
draw_letter_spaced(sdraw, title, title_font, title_x + 3, title_y + 3, (0, 0, 0, 180), title_spacing)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))
canvas = Image.alpha_composite(canvas, shadow_layer)

# 标题正文
draw_letter_spaced(tdraw, title, title_font, title_x, title_y, (245, 240, 225, 245), title_spacing)

# ---- 底部元数据 ----
meta_label = "FILE · 0427-A · DEPTH UNCONFIRMED"
meta_size = int(H / 75)
meta_font = ImageFont.truetype(SERIF_LATIN, meta_size)
meta_spacing = int(meta_size * 0.35)
meta_w = text_width_with_spacing(meta_font, meta_label, meta_spacing)
meta_x = (W - meta_w) // 2
meta_y = int(H * 0.92)
draw_letter_spaced(tdraw, meta_label, meta_font, meta_x, meta_y, (210, 205, 190, 190), meta_spacing)

# 底部细线
bline_y = int(H * 0.91)
bline_w = int(W * 0.25)
bline_x = (W - bline_w) // 2
tdraw.line([(bline_x, bline_y), (bline_x + bline_w, bline_y)], fill=(210, 205, 190, 140), width=1)

canvas = Image.alpha_composite(canvas, text_layer)

# 输出
canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")
