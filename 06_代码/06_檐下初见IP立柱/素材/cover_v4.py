"""《花期很短，她很慢》封面 · 代码版 v4
修复:
1. 列间距压紧 (col_gap 2.20 → 1.55)
2. 整列右移 (margin_right 4.5% → 2.5%) 避免"像"字撞下巴
3. 印章字体临时改用楷书(ukai)— 比宋体优雅,等用户下载篆书后用 v5 替换
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_原图.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_代码版_v4_1.png"
KAI_FONT  = "/sessions/tender-admiring-galileo/.local/share/fonts/ukai.ttc"
MING_FONT = "/sessions/tender-admiring-galileo/.local/share/fonts/uming.ttc"

# ============ Step 1: load ============
img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"原图: {W}x{H}")

# ============ Step 2: color grade ============
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

# ============ Step 3: 三行竖排楷书诗(紧凑版) ============
char_size = int(H / 34)
font_kai  = ImageFont.truetype(KAI_FONT, char_size)
columns   = ["风一吹，花就落了一地", "她还站在那儿", "像是没听见"]

margin_right = int(W * 0.030)        # ⬅ 整体右移
col_gap   = int(char_size * 1.50)    # ⬅ 列距更紧
start_y   = int(H * 0.53)            # ⬅ 下移避开下巴
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

# ============ Step 4: 印章 ============
import os
ZHUAN_FONT = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/zhuanshu.ttf"
if not os.path.exists(ZHUAN_FONT):
    ZHUAN_FONT = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/zhuanshu.otf"
if not os.path.exists(ZHUAN_FONT):
    ZHUAN_FONT = KAI_FONT  # 临时:楷书
    print("⚠️  未找到 zhuanshu.ttf,临时使用楷书")
else:
    print(f"✅ 使用篆书: {ZHUAN_FONT}")

seal_size = int(W * 0.085)
SEAL_RED  = (188, 42, 33)
seal_font_size = int(seal_size * 0.50)
seal_font = ImageFont.truetype(ZHUAN_FONT, seal_font_size)

seal_block = Image.new("RGBA", (seal_size, seal_size), (*SEAL_RED, 255))
text_mask = Image.new("L", (seal_size, seal_size), 0)
mdraw = ImageDraw.Draw(text_mask)

for char, y_frac in [("檐", 0.05), ("下", 0.50)]:
    bb = mdraw.textbbox((0, 0), char, font=seal_font)
    cw = bb[2] - bb[0]
    mdraw.text(
        ((seal_size - cw) / 2 - bb[0], int(seal_size * y_frac) - bb[1]),
        char, font=seal_font, fill=255,
    )

seal_arr = np.asarray(seal_block).copy()
mask_arr = np.asarray(text_mask)
seal_arr[..., 3] = np.where(mask_arr > 128, 0, seal_arr[..., 3])

seal_arr = seal_arr.astype(np.float32)
rng = np.random.RandomState(42)
noise = rng.rand(seal_size, seal_size)
xs = np.arange(seal_size)
edge_dist = np.minimum(
    np.minimum(xs[None, :], seal_size - 1 - xs[None, :]),
    np.minimum(xs[:, None], seal_size - 1 - xs[:, None]),
)
edge_factor = np.clip(edge_dist / (seal_size * 0.06), 0, 1)
ink_var = 0.82 + noise * 0.18
seal_arr[..., 3] = np.clip(seal_arr[..., 3] * edge_factor * ink_var, 0, 255)
seal_arr[..., 0] = np.clip(seal_arr[..., 0] * (0.90 + noise * 0.10), 0, 255)
seal_arr[..., 1] = np.clip(seal_arr[..., 1] * (0.95 + noise * 0.05), 0, 255)
worn_spots = rng.rand(seal_size, seal_size) < 0.008
seal_arr[..., 3][worn_spots] = 0

seal_block = Image.fromarray(seal_arr.astype(np.uint8))
seal_block = seal_block.rotate(random.Random(7).uniform(-2.0, 2.0), resample=Image.BICUBIC, expand=True)

seal_x = W - seal_block.width - int(W * 0.05)
seal_y = H - seal_block.height - int(H * 0.04)
canvas.paste(seal_block, (seal_x, seal_y), seal_block)

# ============ Step 5: save ============
canvas.convert("RGB").save(DST, optimize=True)
print(f"✅ {DST}")
