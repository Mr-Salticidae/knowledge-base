"""
============================================================
「檐下」IP 系列封面 · 代码生成模板
============================================================

> 入档日期:2026-05-03
> 首次实战:《花期很短，她很慢》(5/4 发布)
> 性质:IP 视觉系统的稳定性护城河

为什么需要这个模板:
- 生图模型(GPT Image 2 / MJ)无法保证视觉一致性,每次都会"自由发挥"
- 「檐下」作为长期 IP,需要一个稳定的视觉签名(印章 + 字体 + 布局)
- 代码生成 = 像素级保真原图 + 100% 一致的排版 + 阳文篆书印章

使用方法:
1. 把要做封面的原图放到 SRC 路径
2. 改 columns 列表为本作品的诗句(三列竖排)
3. 改 DST 输出路径
4. 运行:python3 檐下系列封面模板.py

依赖:
- PIL (Pillow) + numpy
- 楷书字体:ukai.ttc (AR PL UKai CN — 用 apt download fonts-arphic-ukai 获取)
- 篆书字体:zhuanshu.ttf (任意 篆书 ttf,放到 ZHUAN_FONT 路径)

设计哲学:
- 文字克制 → 印章也克制(阳文留白)
- 大片留白 → 印章中央也留白
- 安静低语的诗 → 安静低调的印
- 不喧宾夺主的字 → 不喧宾夺主的章
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random

# ============ 配置区(修改这里) ============

# 输入原图(无文字版)
SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_原图.png"

# 输出路径
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/06_檐下初见IP立柱/素材/花期很短_最终封面.png"

# 三列竖排诗句(从右往左)
COLUMNS = [
    "风一吹，花就落了一地",  # 列 0:最右
    "她还站在那儿",          # 列 1:中
    "像是没听见",            # 列 2:最左
]

# 印章二字(上 / 下)
SEAL_CHARS = ("檐", "下")

# ============ 字体路径(2026-05-04 起统一从字体资产库调用) ============
# 字体资产库:{旧工作区}/字体\(详见该目录 README.md)
FONT_DIR   = "/sessions/tender-admiring-galileo/mnt/小红书运营/字体"
KAI_FONT   = f"{FONT_DIR}/ukai.ttc"
ZHUAN_FONT = f"{FONT_DIR}/zhuanshu.ttf"

# ============ 视觉参数(克制原则,微调即可) ============
# 文字
CHAR_SIZE_RATIO  = 1 / 34   # 字号 = H * 此比例
COL_GAP_RATIO    = 1.50     # 列距 = char_size * 此比例
MARGIN_RIGHT     = 0.030    # 右边距 = W * 此比例
START_Y          = 0.53     # 文字起始 y = H * 此比例
TEXT_COLOR       = (250, 244, 232, 240)

# 印章(阳文/朱文)
SEAL_SIZE_RATIO  = 0.10     # 印章宽 = W * 此比例
SEAL_RED         = (188, 42, 33)
BORDER_RATIO     = 0.04     # 边框宽度
SEAL_X_MARGIN    = 0.05     # 距右边
SEAL_Y_MARGIN    = 0.04     # 距底边


# ============ 实现(下面一般不需要改) ============

def color_grade(img: Image.Image) -> Image.Image:
    """微调色:暗部抬冷,高光抬暖,轻晕影"""
    arr = np.asarray(img, dtype=np.float32) / 255.0
    H, W = arr.shape[:2]
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
    return Image.fromarray(np.clip(arr * 255.0, 0, 255).astype(np.uint8))


def render_char_to_cell(char, font_path, cell_w, cell_h, fill_ratio=0.95):
    """高分辨率渲染 → 裁紧 → 缩放到 cell,字面率 fill_ratio"""
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
    cw, ch = cropped.size
    scale = (cell_w * fill_ratio / cw + cell_h * fill_ratio / ch) / 2
    new_w = min(int(cw * scale), int(cell_w * 0.95))
    new_h = min(int(ch * scale), int(cell_h * 0.95))
    resized = cropped.resize((new_w, new_h), Image.LANCZOS)
    cell = Image.new("L", (cell_w, cell_h), 0)
    cell.paste(resized, ((cell_w - new_w) // 2, (cell_h - new_h) // 2))
    return cell


def make_yang_seal(seal_size, top_char, bottom_char):
    """阳文(朱文)篆书印章 — 红边框 + 红字 + 中央留白"""
    border_width = max(2, int(seal_size * BORDER_RATIO))
    inner_pad = border_width + int(seal_size * 0.03)
    cell_w = seal_size - 2 * inner_pad
    cell_h = (seal_size - 2 * inner_pad) // 2

    cell_top = render_char_to_cell(top_char, ZHUAN_FONT, cell_w, cell_h)
    cell_bot = render_char_to_cell(bottom_char, ZHUAN_FONT, cell_w, cell_h)

    char_mask = Image.new("L", (seal_size, seal_size), 0)
    char_mask.paste(cell_top, (inner_pad, inner_pad))
    char_mask.paste(cell_bot, (inner_pad, inner_pad + cell_h))

    frame_mask = Image.new("L", (seal_size, seal_size), 0)
    fdraw = ImageDraw.Draw(frame_mask)
    fdraw.rectangle([(0, 0), (seal_size - 1, seal_size - 1)], outline=255, width=border_width)

    combined = np.maximum(np.asarray(char_mask), np.asarray(frame_mask))

    seal_arr = np.zeros((seal_size, seal_size, 4), dtype=np.float32)
    seal_arr[..., 0] = SEAL_RED[0]
    seal_arr[..., 1] = SEAL_RED[1]
    seal_arr[..., 2] = SEAL_RED[2]
    seal_arr[..., 3] = combined.astype(np.float32)

    rng = np.random.RandomState(42)
    noise = rng.rand(seal_size, seal_size)
    seal_arr[..., 3] = np.clip(seal_arr[..., 3] * (0.85 + noise * 0.15), 0, 255)
    seal_arr[..., 0] = np.clip(seal_arr[..., 0] * (0.92 + noise * 0.08), 0, 255)
    seal_arr[..., 1] = np.clip(seal_arr[..., 1] * (0.95 + noise * 0.05), 0, 255)

    # 笔画与边框断裂感(老印章)
    red_pixels = combined > 128
    seal_arr[..., 3][(rng.rand(seal_size, seal_size) < 0.025) & red_pixels] = 0
    frame_pixels = np.asarray(frame_mask) > 128
    seal_arr[..., 3][(rng.rand(seal_size, seal_size) < 0.04) & frame_pixels] = 0

    seal_img = Image.fromarray(seal_arr.astype(np.uint8))
    return seal_img.rotate(random.Random(7).uniform(-1.5, 1.5), resample=Image.BICUBIC, expand=True)


def draw_columns(draw_obj, columns, font_kai, char_size, W, fill_color, dx=0, dy=0):
    margin_right = int(W * MARGIN_RIGHT)
    col_gap = int(char_size * COL_GAP_RATIO)
    for ci, col_text in enumerate(columns):
        x = W - margin_right - ci * col_gap - char_size
        y_offset = 0
        for ch in col_text:
            if ch in "，。：；":
                cs = int(char_size * 0.75)
                f = ImageFont.truetype(KAI_FONT, cs)
                ox = (char_size - cs) // 2
                draw_obj.text((x + ox + dx, START_Y_PX + y_offset + int(char_size * 0.05) + dy), ch, font=f, fill=fill_color)
                y_offset += int(char_size * 0.85)
            else:
                draw_obj.text((x + dx, START_Y_PX + y_offset + dy), ch, font=font_kai, fill=fill_color)
                y_offset += int(char_size * 1.12)


# ============ 主流程 ============
img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"[INFO] 原图: {W}x{H}")

canvas = color_grade(img).convert("RGBA")

char_size = int(H * CHAR_SIZE_RATIO)
font_kai  = ImageFont.truetype(KAI_FONT, char_size)
START_Y_PX = int(H * START_Y)

# 阴影
shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_columns(ImageDraw.Draw(shadow_layer), COLUMNS, font_kai, char_size, W, (0, 0, 0, 200), dx=3, dy=3)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=5))
canvas = Image.alpha_composite(canvas, shadow_layer)

# 主文字
text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw_columns(ImageDraw.Draw(text_layer), COLUMNS, font_kai, char_size, W, TEXT_COLOR)
glow = text_layer.filter(ImageFilter.GaussianBlur(radius=2))
glow_arr = np.asarray(glow, dtype=np.uint8).copy()
glow_arr[..., 3] = (glow_arr[..., 3].astype(np.float32) * 0.30).astype(np.uint8)
canvas = Image.alpha_composite(canvas, Image.fromarray(glow_arr))
canvas = Image.alpha_composite(canvas, text_layer)

# 阳文印章
seal_size = int(W * SEAL_SIZE_RATIO)
seal_img = make_yang_seal(seal_size, *SEAL_CHARS)
seal_x = W - seal_img.width - int(W * SEAL_X_MARGIN)
seal_y = H - seal_img.height - int(H * SEAL_Y_MARGIN)
canvas.paste(seal_img, (seal_x, seal_y), seal_img)

canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")
