"""《花期很短，她很慢》封面 · v5.1
篆书印章优化:字号放大、紧贴方框、加粗笔画
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import os

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_原图.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_代码版_v5_1.png"
KAI_FONT  = "/sessions/tender-admiring-galileo/.local/share/fonts/ukai.ttc"
ZHUAN_FONT = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/zhuanshu.ttf"

img = Image.open(SRC).convert("RGB")
W, H = img.size

# Step 2: color grade
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

# Step 3: 三行竖排楷书诗(沿用 v4.1)
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

# ============ Step 4: 篆书印章 v5.1(字饱满压满) ============
seal_size = int(W * 0.095)        # 印章再放大一点
SEAL_RED  = (188, 42, 33)

# 关键改动:每个字单独画在自己的"半区"里,字号设到能填满
# 上半区 / 下半区 各自占 (seal_size, seal_size/2)
half_h = seal_size // 2
inner_pad = int(seal_size * 0.08)   # 字距方框边的内边距(很小)

# 算字号:取能填满半区的最大值
def fit_size(char, font_path, max_w, max_h):
    """二分搜索能装进 (max_w, max_h) 的最大字号"""
    lo, hi = 8, 400
    best = 8
    while lo <= hi:
        mid = (lo + hi) // 2
        f = ImageFont.truetype(font_path, mid)
        bb = f.getbbox(char)
        cw, ch = bb[2] - bb[0], bb[3] - bb[1]
        if cw <= max_w and ch <= max_h:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best

cell_w = seal_size - 2 * inner_pad
cell_h = half_h - inner_pad

size_yan  = fit_size("檐", ZHUAN_FONT, cell_w, cell_h)
size_xia  = fit_size("下", ZHUAN_FONT, cell_w, cell_h)
print(f"檐 字号: {size_yan}, 下 字号: {size_xia}")

# 画方块 + 文字 mask
seal_block = Image.new("RGBA", (seal_size, seal_size), (*SEAL_RED, 255))
text_mask = Image.new("L", (seal_size, seal_size), 0)
mdraw = ImageDraw.Draw(text_mask)

# 上半:檐
font_yan = ImageFont.truetype(ZHUAN_FONT, size_yan)
bb_yan = font_yan.getbbox("檐")
yan_w, yan_h = bb_yan[2] - bb_yan[0], bb_yan[3] - bb_yan[1]
yan_x = (seal_size - yan_w) // 2 - bb_yan[0]
yan_y = inner_pad + (cell_h - yan_h) // 2 - bb_yan[1]
mdraw.text((yan_x, yan_y), "檐", font=font_yan, fill=255)

# 下半:下
font_xia = ImageFont.truetype(ZHUAN_FONT, size_xia)
bb_xia = font_xia.getbbox("下")
xia_w, xia_h = bb_xia[2] - bb_xia[0], bb_xia[3] - bb_xia[1]
xia_x = (seal_size - xia_w) // 2 - bb_xia[0]
xia_y = half_h + (cell_h - xia_h) // 2 - bb_xia[1]
mdraw.text((xia_x, xia_y), "下", font=font_xia, fill=255)

# 用字体原生笔画粗细,不膨胀(避免笔画黏连)

# 阴文镂空
seal_arr = np.asarray(seal_block).copy()
mask_arr = np.asarray(text_mask)
seal_arr[..., 3] = np.where(mask_arr > 128, 0, seal_arr[..., 3])

# 印泥不均
seal_arr = seal_arr.astype(np.float32)
rng = np.random.RandomState(42)
noise = rng.rand(seal_size, seal_size)
xs = np.arange(seal_size)
edge_dist = np.minimum(
    np.minimum(xs[None, :], seal_size - 1 - xs[None, :]),
    np.minimum(xs[:, None], seal_size - 1 - xs[:, None]),
)
edge_factor = np.clip(edge_dist / (seal_size * 0.05), 0, 1)
ink_var = 0.85 + noise * 0.15
seal_arr[..., 3] = np.clip(seal_arr[..., 3] * edge_factor * ink_var, 0, 255)
seal_arr[..., 0] = np.clip(seal_arr[..., 0] * (0.92 + noise * 0.08), 0, 255)
seal_arr[..., 1] = np.clip(seal_arr[..., 1] * (0.95 + noise * 0.05), 0, 255)

# 印泥磨损斑(老印章感)
worn_spots = rng.rand(seal_size, seal_size) < 0.006
seal_arr[..., 3][worn_spots] = 0

seal_block = Image.fromarray(seal_arr.astype(np.uint8))
seal_block = seal_block.rotate(random.Random(7).uniform(-1.5, 1.5), resample=Image.BICUBIC, expand=True)

seal_x = W - seal_block.width - int(W * 0.05)
seal_y = H - seal_block.height - int(H * 0.04)
canvas.paste(seal_block, (seal_x, seal_y), seal_block)

canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")

# 同时保存印章特写以便检查
seal_zoom = canvas.crop((seal_x - 10, seal_y - 10, seal_x + seal_block.width + 10, seal_y + seal_block.height + 10))
seal_zoom.convert("RGB").save("/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/_seal_zoom_v5_1.png")
