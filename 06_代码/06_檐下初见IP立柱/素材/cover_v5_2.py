"""《花期很短，她很慢》封面 · v5.2
篆书印章 · 印面分布优化
- 每个字单独渲染,各自撑满"自己的格子"
- 上下二字字面均衡,不再"上密下疏"
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_原图.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_代码版_v5_2.png"
KAI_FONT  = "/sessions/tender-admiring-galileo/.local/share/fonts/ukai.ttc"
ZHUAN_FONT = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/zhuanshu.ttf"

img = Image.open(SRC).convert("RGB")
W, H = img.size

# Step 2: color grade (sealed)
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

# Step 3: 三行竖排楷书诗(沿用)
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

# ============ Step 4: 篆书印章 v5.2 (印面分布) ============
seal_size = int(W * 0.10)        # 大一档,~ 82px
SEAL_RED  = (188, 42, 33)

# 每个字单独渲染 → 裁紧 → 缩放到目标格子 → 撑满
def render_char_to_cell(char, font_path, cell_w, cell_h, fill_ratio=0.92):
    """高分辨率渲染字符,裁紧,缩放到 cell_w × cell_h,字面占 fill_ratio"""
    target_w = int(cell_w * fill_ratio)
    target_h = int(cell_h * fill_ratio)

    # 先大尺寸渲染
    big_size = 400
    font = ImageFont.truetype(font_path, big_size)
    bb = font.getbbox(char)
    cw, ch = bb[2] - bb[0], bb[3] - bb[1]

    # 在大画布上画字
    big_img = Image.new("L", (cw + 20, ch + 20), 0)
    bd = ImageDraw.Draw(big_img)
    bd.text((10 - bb[0], 10 - bb[1]), char, font=font, fill=255)

    # 裁剪到字的实际边界
    big_arr = np.asarray(big_img)
    rows = np.any(big_arr > 50, axis=1)
    cols = np.any(big_arr > 50, axis=0)
    if not rows.any() or not cols.any():
        return Image.new("L", (cell_w, cell_h), 0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    cropped = big_img.crop((cmin, rmin, cmax + 1, rmax + 1))

    # 计算缩放比例:取较小的那个,保持宽高比但允许微拉伸
    cropped_w, cropped_h = cropped.size
    scale_w = target_w / cropped_w
    scale_h = target_h / cropped_h
    # 取平均 — 让字"几乎方形",像真正的印章
    avg_scale = (scale_w + scale_h) / 2
    new_w = int(cropped_w * avg_scale)
    new_h = int(cropped_h * avg_scale)
    # 限制不超出 cell
    if new_w > cell_w * 0.95: new_w = int(cell_w * 0.95)
    if new_h > cell_h * 0.95: new_h = int(cell_h * 0.95)

    resized = cropped.resize((new_w, new_h), Image.LANCZOS)

    # 居中放进 cell
    cell = Image.new("L", (cell_w, cell_h), 0)
    paste_x = (cell_w - new_w) // 2
    paste_y = (cell_h - new_h) // 2
    cell.paste(resized, (paste_x, paste_y))
    return cell

# 计算上下两个 cell 的尺寸
inner_pad = int(seal_size * 0.04)
cell_w = seal_size - 2 * inner_pad
cell_h = (seal_size - 2 * inner_pad) // 2

cell_yan = render_char_to_cell("檐", ZHUAN_FONT, cell_w, cell_h, fill_ratio=0.95)
cell_xia = render_char_to_cell("下", ZHUAN_FONT, cell_w, cell_h, fill_ratio=0.95)

# 拼装到方块
text_mask = Image.new("L", (seal_size, seal_size), 0)
text_mask.paste(cell_yan, (inner_pad, inner_pad))
text_mask.paste(cell_xia, (inner_pad, inner_pad + cell_h))

# 创建红方块
seal_block = Image.new("RGBA", (seal_size, seal_size), (*SEAL_RED, 255))

# 阴文镂空
seal_arr = np.asarray(seal_block).copy()
mask_arr = np.asarray(text_mask)
seal_arr[..., 3] = np.where(mask_arr > 128, 0, seal_arr[..., 3])

# 印泥不均(轻度)
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
worn_spots = rng.rand(seal_size, seal_size) < 0.005
seal_arr[..., 3][worn_spots] = 0

seal_block = Image.fromarray(seal_arr.astype(np.uint8))
seal_block = seal_block.rotate(random.Random(7).uniform(-1.5, 1.5), resample=Image.BICUBIC, expand=True)

seal_x = W - seal_block.width - int(W * 0.05)
seal_y = H - seal_block.height - int(H * 0.04)
canvas.paste(seal_block, (seal_x, seal_y), seal_block)

canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")

# 印章特写
seal_zoom = canvas.crop((seal_x - 10, seal_y - 10, seal_x + seal_block.width + 10, seal_y + seal_block.height + 10))
seal_zoom.convert("RGB").save("/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/_seal_zoom_v5_2.png")
