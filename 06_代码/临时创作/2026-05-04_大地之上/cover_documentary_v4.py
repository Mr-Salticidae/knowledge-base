"""
《大地之上》封面 v4 · 思源宋体 Heavy + 方案 A 取色融入

修复 v3 两处:
1. 字体:宋体 → 思源宋体 Heavy(粗重、文献感、不卡通)
2. 黑条 → 取色暗区(从照片底部采样,降亮 → 自然融入,无硬切)
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/mr_jumping_spider_cinematic_still_ultra_wide_establishing_sho_9c654027-54aa-4e33-acfe-9e7b6af9a7bf_2.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/00_封面_大地之上_v4.png"

TITLE_FONT      = "/sessions/tender-admiring-galileo/mnt/小红书运营/字体/SourceHanSerifSC-Heavy.otf"
SUBTITLE_FONT   = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SUBMARK_FONT    = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

img = Image.open(SRC).convert("RGB")
W, H = img.size

# 比例:照片 78% / 暗区 22%
PHOTO_RATIO = 0.78
photo_h = int(H * PHOTO_RATIO)
bar_h = H - photo_h

# ---- Step 1: 处理照片(裁剪 + 微 grain) ----
photo_aspect_target = W / photo_h
photo_aspect_orig = W / H

if photo_aspect_orig > photo_aspect_target:
    new_h_orig = int(W / photo_aspect_target)
    crop_top = (H - new_h_orig) // 2
    photo_crop = img.crop((0, crop_top, W, crop_top + new_h_orig))
else:
    new_w_orig = int(H * photo_aspect_target)
    crop_left = (W - new_w_orig) // 2
    photo_crop = img.crop((crop_left, 0, crop_left + new_w_orig, H))

photo = photo_crop.resize((W, photo_h), Image.LANCZOS)

photo_arr = np.asarray(photo, dtype=np.float32) / 255.0
mid = 0.5
photo_arr = mid + (photo_arr - mid) * 1.04
rng = np.random.RandomState(2027)
grain = (rng.rand(photo_h, W) - 0.5) * 0.018
photo_arr = np.clip(photo_arr + grain[..., None], 0, 1)

# ---- Step 2: 方案 A · 取色融入 ----
# 采样照片底部 5% 的平均色作为色调基准
sample_zone = photo_arr[int(photo_h * 0.95):, :, :]
sampled_color = sample_zone.mean(axis=(0, 1))  # (R, G, B) in [0,1]
print(f"[INFO] 照片底部采样色: RGB {(sampled_color * 255).astype(np.uint8).tolist()}")

# 降亮到 ~38%(暗到能压字,但仍带原色调)
DARKEN_FACTOR = 0.38
bar_color_normalized = sampled_color * DARKEN_FACTOR
bar_color_rgb = (bar_color_normalized * 255).astype(np.uint8)
print(f"[INFO] 暗区基准色(降亮后): RGB {bar_color_rgb.tolist()}")

# ---- Step 3: 拼装(照片 + 暗区) + 软过渡 ----
canvas_arr = np.zeros((H, W, 3), dtype=np.float32)
# 上半:照片
canvas_arr[:photo_h] = photo_arr * 255

# 下半:暗区基准色
canvas_arr[photo_h:] = bar_color_rgb

# ---- 软过渡区(在 photo_h 上下各 3% 做 alpha 渐变) ----
transition_h = int(H * 0.05)  # 5% 高度的过渡带
trans_start = photo_h - transition_h // 2
trans_end   = photo_h + transition_h // 2

for y in range(trans_start, trans_end):
    if y < 0 or y >= H:
        continue
    # 渐变权重:0 = 完全照片, 1 = 完全暗区
    t = (y - trans_start) / transition_h
    t = max(0, min(1, t))
    # smoothstep 让过渡更柔
    t = t * t * (3 - 2 * t)
    # 照片底部行的色作为起点(避免突然出现一道明亮)
    photo_row = photo_arr[min(y, photo_h - 1)] * 255
    bar_row = np.full_like(photo_row, bar_color_rgb)
    canvas_arr[y] = photo_row * (1 - t) + bar_row * t

canvas_arr = np.clip(canvas_arr, 0, 255).astype(np.uint8)
canvas = Image.fromarray(canvas_arr).convert("RGBA")

# ---- Step 4: 标题(思源宋体 Heavy) ----
title_size = int(bar_h * 0.48)  # 标题占暗区 48% 高度
title_font = ImageFont.truetype(TITLE_FONT, title_size)

title_text = "大地之上"
char_spacing = int(title_size * 0.20)  # 字间距 +20%
chars = list(title_text)
char_widths = []
for ch in chars:
    bb = title_font.getbbox(ch)
    char_widths.append(bb[2] - bb[0])
total_title_w = sum(char_widths) + char_spacing * (len(chars) - 1)
title_x = (W - total_title_w) // 2
title_y = photo_h + int(bar_h * 0.20)

# ---- 风化效果(Heavy 字重可以承受更明显的风化) ----
mask_pad = title_size
mask_w = total_title_w + mask_pad * 2
mask_h = title_size + mask_pad * 2
title_mask = Image.new("L", (mask_w, mask_h), 0)
mdraw = ImageDraw.Draw(title_mask)

cur_x = mask_pad
for ch, cw in zip(chars, char_widths):
    bb = title_font.getbbox(ch)
    mdraw.text((cur_x - bb[0], mask_pad - bb[1]), ch, font=title_font, fill=255)
    cur_x += cw + char_spacing

mask_arr = np.asarray(title_mask, dtype=np.float32)
rng2 = np.random.RandomState(123)

# 1. 大块掉漆斑(0.4% 像素中心,扩散到 5-8 px)
big_holes = rng2.rand(mask_h, mask_w) < 0.004
big_holes_img = Image.fromarray((big_holes * 255).astype(np.uint8))
big_holes_img = big_holes_img.filter(ImageFilter.GaussianBlur(radius=2.5))
big_holes_dilated = np.asarray(big_holes_img) > 70
mask_arr[big_holes_dilated] = 0

# 2. 中等斑驳(让边缘更碎)
medium_holes = rng2.rand(mask_h, mask_w) < 0.012
medium_holes_img = Image.fromarray((medium_holes * 255).astype(np.uint8))
medium_holes_img = medium_holes_img.filter(ImageFilter.GaussianBlur(radius=1.0))
medium_holes_dilated = np.asarray(medium_holes_img) > 60
# 只对已经有字的地方挖
mask_arr[medium_holes_dilated & (mask_arr > 50)] *= 0.3

# 3. 细颗粒
fine_noise = rng2.rand(mask_h, mask_w)
mask_arr = mask_arr * (0.82 + fine_noise * 0.18)

mask_arr = np.clip(mask_arr, 0, 255).astype(np.uint8)

# ---- 渲染奶白色文字(略带暖,接画面色调) ----
TITLE_COLOR = (240, 232, 215)
title_arr_rgba = np.zeros((mask_h, mask_w, 4), dtype=np.uint8)
title_arr_rgba[..., 0] = TITLE_COLOR[0]
title_arr_rgba[..., 1] = TITLE_COLOR[1]
title_arr_rgba[..., 2] = TITLE_COLOR[2]
title_arr_rgba[..., 3] = mask_arr
title_layer = Image.fromarray(title_arr_rgba)

paste_x = title_x - mask_pad
paste_y = title_y - mask_pad
canvas.paste(title_layer, (paste_x, paste_y), title_layer)

# ---- Step 5: 副标 RECOVERED FOOTAGE ----
sub_text = "RECOVERED  FOOTAGE"
sub_size = int(bar_h * 0.12)
sub_font = ImageFont.truetype(SUBTITLE_FONT, sub_size)
sub_spacing = int(sub_size * 0.18)
sub_chars = list(sub_text)
sub_widths = [sub_font.getbbox(ch)[2] - sub_font.getbbox(ch)[0] for ch in sub_chars]
total_sub_w = sum(sub_widths) + sub_spacing * (len(sub_chars) - 1)
sub_x = (W - total_sub_w) // 2
sub_y = title_y + title_size + int(bar_h * 0.06)

draw = ImageDraw.Draw(canvas)
cur_x = sub_x
for ch, cw in zip(sub_chars, sub_widths):
    bb = sub_font.getbbox(ch)
    draw.text((cur_x - bb[0], sub_y), ch, font=sub_font, fill=(220, 213, 195, 235))
    cur_x += cw + sub_spacing

# ---- Step 6: 右下小角标 EP.01 ----
mark_font = ImageFont.truetype(SUBMARK_FONT, int(bar_h * 0.07))
mark_text = "EP.01"
bb = mark_font.getbbox(mark_text)
mark_x = W - int(W * 0.04) - (bb[2] - bb[0])
mark_y = H - int(bar_h * 0.15) - (bb[3] - bb[1])
draw.text((mark_x, mark_y), mark_text, font=mark_font, fill=(180, 175, 160, 200))

canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")
