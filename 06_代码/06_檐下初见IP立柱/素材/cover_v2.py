"""《花期很短，她很慢》封面 · 代码版 v2"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_原图.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_代码版_v2.png"
KAI_FONT  = "/sessions/tender-admiring-galileo/.local/share/fonts/ukai.ttc"
MING_FONT = "/sessions/tender-admiring-galileo/.local/share/fonts/uming.ttc"

# Step 1: load
img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"原图尺寸: {W}x{H}")

# Step 2: color grade
arr = np.asarray(img, dtype=np.float32) / 255.0
lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
shadow_mask    = np.clip(1.0 - lum * 1.6, 0, 1)
highlight_mask = np.clip((lum - 0.55) * 2.2, 0, 1)
arr[..., 2] += shadow_mask * 0.012
arr[..., 0] -= shadow_mask * 0.006
arr[..., 0] += highlight_mask * 0.020
arr[..., 1] += highlight_mask * 0.010
arr[..., 2] -= highlight_mask * 0.012
yy, xx = np.meshgrid(np.linspace(-1, 1, H), np.linspace(-1, 1, W), indexing="ij")
radius = np.sqrt(xx ** 2 + yy ** 2)
vignette = 1.0 - np.clip((radius - 0.7) * 0.18, 0, 0.10)
arr *= vignette[..., None]
mid = 0.5
arr = mid + (np.clip(arr, 0, 1) - mid) * 1.04
arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
canvas = Image.fromarray(arr).convert("RGBA")

# Step 3: vertical poetry text
char_size = int(H / 30)
font_kai  = ImageFont.truetype(KAI_FONT, char_size)
columns = ["风一吹，花就落了一地", "她还站在那儿", "像是没听见"]
margin_right = int(W * 0.05)
col_gap = int(char_size * 2.00)
start_y = int(H * 0.36)
text_color = (245, 240, 232, 235)

# Helper to walk through chars
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
                y += int(char_size * 1.10)

# Soft shadow layer
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_columns(ImageDraw.Draw(shadow_layer), (0, 0, 0, 175), dx=2, dy=2)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=4))
canvas = Image.alpha_composite(canvas, shadow_layer)

# Main text layer
text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_columns(ImageDraw.Draw(text_layer), text_color)

glow = text_layer.filter(ImageFilter.GaussianBlur(radius=2))
glow_arr = np.asarray(glow, dtype=np.uint8).copy()
glow_arr[..., 3] = (glow_arr[..., 3].astype(np.float32) * 0.35).astype(np.uint8)
canvas = Image.alpha_composite(canvas, Image.fromarray(glow_arr))
canvas = Image.alpha_composite(canvas, text_layer)

# Step 4: red seal "檐下" (阴文)
seal_size = int(W * 0.075)
SEAL_RED = (185, 40, 32)
seal_font_size = int(seal_size * 0.50)
seal_font = ImageFont.truetype(MING_FONT, seal_font_size)

seal_block = Image.new("RGBA", (seal_size, seal_size), (*SEAL_RED, 255))
text_mask = Image.new("L", (seal_size, seal_size), 0)
mdraw = ImageDraw.Draw(text_mask)

b1 = mdraw.textbbox((0, 0), "檐", font=seal_font)
b2 = mdraw.textbbox((0, 0), "下", font=seal_font)
w1 = b1[2] - b1[0]
w2 = b2[2] - b2[0]
mdraw.text(((seal_size - w1) / 2 - b1[0], int(seal_size * 0.05) - b1[1]), "檐", font=seal_font, fill=255)
mdraw.text(((seal_size - w2) / 2 - b2[0], int(seal_size * 0.50) - b2[1]), "下", font=seal_font, fill=255)

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
edge_factor = np.clip(edge_dist / (seal_size * 0.08), 0, 1)
ink_var = 0.85 + noise * 0.15
seal_arr[..., 3] = np.clip(seal_arr[..., 3] * edge_factor * ink_var, 0, 255)
seal_arr[..., 0] = np.clip(seal_arr[..., 0] * (0.92 + noise * 0.08), 0, 255)
seal_arr[..., 1] = np.clip(seal_arr[..., 1] * (0.95 + noise * 0.05), 0, 255)

seal_block = Image.fromarray(seal_arr.astype(np.uint8))
seal_block = seal_block.rotate(random.Random(7).uniform(-1.8, 1.8), resample=Image.BICUBIC, expand=True)

seal_x = W - seal_block.width - int(W * 0.05)
seal_y = H - seal_block.height - int(H * 0.04)
canvas.paste(seal_block, (seal_x, seal_y), seal_block)

# Step 5: save
canvas.convert("RGB").save(DST, optimize=True)
print(f"✅ {DST}")
