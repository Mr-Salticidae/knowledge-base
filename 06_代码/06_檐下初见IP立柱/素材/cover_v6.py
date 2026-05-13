"""《花期很短，她很慢》封面 · v6
阳文(朱文)印章 — 文人雅士款
- 字是红色 + 细红边框 + 中间留白(透明)
- 比阴文更典雅、更秀气
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_原图.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_代码版_v6_阳文.png"
KAI_FONT  = "/sessions/tender-admiring-galileo/.local/share/fonts/ukai.ttc"
ZHUAN_FONT = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/zhuanshu.ttf"

img = Image.open(SRC).convert("RGB")
W, H = img.size

# Step 2: 调色
arr = np.asarray(img, dtype=np.float32) / 255.0
lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
shadow_mask    = np.clip(1.0 - lum * 1.6, 0, 1)
highlight_mask = np.clip((lum - 0.55) * 2.2, 0, 1)
arr[..., 2] += shadow_mask * 0.014
arr[..., 0] -= shadow_mask * 0.006
arr[..., 0] += highlight_mask * 0.025
arr[..., 1] += highlight_mask * 0.012
arr[..., 2] -= highlight_mask * 0.015
yy, xx = np.meshgrid(np.linspace(-1, 1, H), np.linspace(-1, 1, W), indexing="ij")
radius = np.sqrt(xx ** 2 + yy ** 2)
vignette = 1.0 - np.clip((radius - 0.65) * 0.20, 0, 0.13)
arr *= vignette[..., None]
mid = 0.5
arr = mid + (np.clip(arr, 0, 1) - mid) * 1.05
arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
canvas = Image.fromarray(arr).convert("RGBA")

# Step 3: 三行竖排楷书诗
char_size = int(H / 34)
font_kai  = ImageFont.truetype(KAI_FONT, char_size)
columns   = ["风一吹，花就落了一地", "她还站在那儿", "像是没听见"]
margin_right = int(W * 0.030)
col_gap   = int(char_size * 1.50)
start_y   = int(H * 0.53)
text_color = (250, 244, 232, 240)

def draw_columns(draw_obj, fill_color, dx=0, dy=0):
    for ci, col_text in enumerate(columns):
        x = W - margin_right - ci * col_gap - char_size
        y = start_y
        for ch in col_text:
            if ch in "，。：；":
                ch_size = int(char_size * 0.75)
                font_ch = ImageFont.truetype(KAI_FONT, ch_size)
                ox = (char_size - ch_size) // 2
                oy = int(char_size * 0.05)
                draw_obj.text((x + ox + dx, y + oy + dy), ch, font=font_ch, fill=fill_color)
                y += int(char_size * 0.85)
            else:
                draw_obj.text((x + dx, y + dy), ch, font=font_kai, fill=fill_color)
                y += int(char_size * 1.12)

shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_columns(ImageDraw.Draw(shadow_layer), (0, 0, 0, 200), dx=3, dy=3)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=5))
canvas = Image.alpha_composite(canvas, shadow_layer)
text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_columns(ImageDraw.Draw(text_layer), text_color)
glow = text_layer.filter(ImageFilter.GaussianBlur(radius=2))
glow_arr = np.asarray(glow, dtype=np.uint8).copy()
glow_arr[..., 3] = (glow_arr[..., 3].astype(np.float32) * 0.30).astype(np.uint8)
canvas = Image.alpha_composite(canvas, Image.fromarray(glow_arr))
canvas = Image.alpha_composite(canvas, text_layer)

# ============ Step 4: 阳文(朱文)印章 ============
seal_size = int(W * 0.10)
SEAL_RED  = (188, 42, 33)

# 字单独渲染 → 撑满格子(同 v5.2 的印面分布逻辑)
def render_char_to_cell(char, font_path, cell_w, cell_h, fill_ratio=0.92):
    big_size = 400
    font = ImageFont.truetype(font_path, big_size)
    bb = font.getbbox(char)
    big_img = Image.new("L", (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), 0)
    bd = ImageDraw.Draw(big_img)
    bd.text((10 - bb[0], 10 - bb[1]), char, font=font, fill=255)
    big_arr = np.asarray(big_img)
    rows = np.any(big_arr > 50, axis=1)
    cols = np.any(big_arr > 50, axis=0)
    if not rows.any() or not cols.any():
        return Image.new("L", (cell_w, cell_h), 0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    cropped = big_img.crop((cmin, rmin, cmax + 1, rmax + 1))
    cropped_w, cropped_h = cropped.size
    target_w = int(cell_w * fill_ratio)
    target_h = int(cell_h * fill_ratio)
    scale = (target_w / cropped_w + target_h / cropped_h) / 2
    new_w = int(cropped_w * scale)
    new_h = int(cropped_h * scale)
    if new_w > cell_w * 0.95: new_w = int(cell_w * 0.95)
    if new_h > cell_h * 0.95: new_h = int(cell_h * 0.95)
    resized = cropped.resize((new_w, new_h), Image.LANCZOS)
    cell = Image.new("L", (cell_w, cell_h), 0)
    paste_x = (cell_w - new_w) // 2
    paste_y = (cell_h - new_h) // 2
    cell.paste(resized, (paste_x, paste_y))
    return cell

# 边框宽度(占总尺寸的比例)
border_width = max(2, int(seal_size * 0.04))
inner_pad   = border_width + int(seal_size * 0.03)  # 字与边框的留白
cell_w = seal_size - 2 * inner_pad
cell_h = (seal_size - 2 * inner_pad) // 2

# 渲染两个字
cell_yan = render_char_to_cell("檐", ZHUAN_FONT, cell_w, cell_h, fill_ratio=0.95)
cell_xia = render_char_to_cell("下", ZHUAN_FONT, cell_w, cell_h, fill_ratio=0.95)

# 文字 mask
char_mask = Image.new("L", (seal_size, seal_size), 0)
char_mask.paste(cell_yan, (inner_pad, inner_pad))
char_mask.paste(cell_xia, (inner_pad, inner_pad + cell_h))

# 边框 mask(只画一道方框)
frame_mask = Image.new("L", (seal_size, seal_size), 0)
fdraw = ImageDraw.Draw(frame_mask)
# 外框矩形 - 内框矩形 = 边框
fdraw.rectangle([(0, 0), (seal_size - 1, seal_size - 1)], outline=255, width=border_width)

# 合并:边框 + 字
combined_mask = np.maximum(np.asarray(char_mask), np.asarray(frame_mask))

# 创建透明底,只在 mask 处填红色
seal_layer = Image.new("RGBA", (seal_size, seal_size), (0, 0, 0, 0))
seal_arr = np.zeros((seal_size, seal_size, 4), dtype=np.float32)
seal_arr[..., 0] = SEAL_RED[0]
seal_arr[..., 1] = SEAL_RED[1]
seal_arr[..., 2] = SEAL_RED[2]
seal_arr[..., 3] = combined_mask.astype(np.float32)  # alpha = mask 值

# 印泥不均(在红色上加扰动)
rng = np.random.RandomState(42)
noise = rng.rand(seal_size, seal_size)

# alpha 扰动:笔画粗细微变,有些地方略浅(印泥不均)
ink_var = 0.85 + noise * 0.15
seal_arr[..., 3] = np.clip(seal_arr[..., 3] * ink_var, 0, 255)

# 红色微变(模拟印泥色不均)
seal_arr[..., 0] = np.clip(seal_arr[..., 0] * (0.92 + noise * 0.08), 0, 255)
seal_arr[..., 1] = np.clip(seal_arr[..., 1] * (0.95 + noise * 0.05), 0, 255)

# 笔画断裂感:随机让 ~ 1% 的"红色像素"alpha 归零(老印章常见)
red_pixels = combined_mask > 128
break_spots = (rng.rand(seal_size, seal_size) < 0.025) & red_pixels
seal_arr[..., 3][break_spots] = 0

# 边框轻度断裂(更显古意)
frame_pixels = np.asarray(frame_mask) > 128
frame_break = (rng.rand(seal_size, seal_size) < 0.04) & frame_pixels
seal_arr[..., 3][frame_break] = 0

seal_layer = Image.fromarray(seal_arr.astype(np.uint8))

# 微旋转(老印章按下不正)
seal_layer = seal_layer.rotate(random.Random(7).uniform(-1.5, 1.5), resample=Image.BICUBIC, expand=True)

seal_x = W - seal_layer.width - int(W * 0.05)
seal_y = H - seal_layer.height - int(H * 0.04)
canvas.paste(seal_layer, (seal_x, seal_y), seal_layer)

canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")

# 印章特写
zoom_pad = 12
zx0 = max(0, seal_x - zoom_pad)
zy0 = max(0, seal_y - zoom_pad)
zx1 = min(W, seal_x + seal_layer.width + zoom_pad)
zy1 = min(H, seal_y + seal_layer.height + zoom_pad)
seal_zoom = canvas.crop((zx0, zy0, zx1, zy1))
seal_zoom.convert("RGB").save("/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/_seal_zoom_v6.png")
