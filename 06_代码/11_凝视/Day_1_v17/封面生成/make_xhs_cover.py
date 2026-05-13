"""
《凝视 The Gaze》小红书封面终极版
布局: 2列 x 3行,智能裁剪保留人脸区域
比例: 3:4
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

INPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_series")
OUTPUT_PATH = Path("/mnt/user-data/outputs/the_gaze_series/the_gaze_xhs_cover.jpg")

FONT_EN_LIGHT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf"
FONT_CN_PATH = "/usr/share/fonts/opentype/noto/NotoSerifCJK-ExtraLight.ttc"
FONT_CN_INDEX = 2

LAYOUT = [
    ["the_gaze_01_scarlatta.jpg", "the_gaze_02_vesper.jpg"],
    ["the_gaze_03_null-07.jpg",   "the_gaze_04_morgana.jpg"],
    ["the_gaze_05_selenwe.jpg",   "the_gaze_06_veritia.jpg"],
]

TARGET_W = 1200
TARGET_H = 1600

MARGIN_X = 50
MARGIN_TOP = 130
MARGIN_BOTTOM = 90
GAP = 6

BG_COLOR = (0, 0, 0)


def add_letter_spacing(text, spacing=2):
    return (" " * spacing).join(text)


def main():
    grid_w = TARGET_W - MARGIN_X * 2
    grid_h = TARGET_H - MARGIN_TOP - MARGIN_BOTTOM

    cell_w = (grid_w - GAP) // 2
    cell_h = (grid_h - GAP * 2) // 3

    images = []
    for row in LAYOUT:
        row_imgs = []
        for filename in row:
            img = Image.open(INPUT_DIR / filename)
            iw, ih = img.size

            cell_ratio = cell_w / cell_h
            src_ratio = iw / ih

            if src_ratio < cell_ratio:
                # 原图更竖,缩放到cell_w,裁剪上下
                scale = cell_w / iw
                scaled_h = int(ih * scale)
                img = img.resize((cell_w, scaled_h), Image.LANCZOS)
                # 从上往下裁,保留人脸(通常在画面上1/3到中间)
                top = int((scaled_h - cell_h) * 0.30)
                img = img.crop((0, top, cell_w, top + cell_h))
            else:
                scale = cell_h / ih
                scaled_w = int(iw * scale)
                img = img.resize((scaled_w, cell_h), Image.LANCZOS)
                left = (scaled_w - cell_w) // 2
                img = img.crop((left, 0, left + cell_w, cell_h))

            row_imgs.append(img)
        images.append(row_imgs)

    canvas = Image.new("RGB", (TARGET_W, TARGET_H), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # 顶部标题
    title_en_size = 50
    title_en_font = ImageFont.truetype(FONT_EN_LIGHT, title_en_size)
    title_en_text = add_letter_spacing("THE GAZE", spacing=3)
    bbox = title_en_font.getbbox(title_en_text)
    title_en_w = bbox[2] - bbox[0]
    title_en_x = (TARGET_W - title_en_w) // 2
    title_en_y = 28
    draw.text((title_en_x, title_en_y), title_en_text, font=title_en_font, fill=(255, 255, 255))

    title_cn_size = 22
    title_cn_font = ImageFont.truetype(FONT_CN_PATH, title_cn_size, index=FONT_CN_INDEX)
    title_cn_text = "凝  视"
    bbox = title_cn_font.getbbox(title_cn_text)
    title_cn_w = bbox[2] - bbox[0]
    title_cn_x = (TARGET_W - title_cn_w) // 2
    title_cn_y = title_en_y + title_en_size + 20
    draw.text((title_cn_x, title_cn_y), title_cn_text, font=title_cn_font, fill=(180, 180, 180))

    # 图片
    for row_idx, row_imgs in enumerate(images):
        for col_idx, img in enumerate(row_imgs):
            x = MARGIN_X + col_idx * (cell_w + GAP)
            y = MARGIN_TOP + row_idx * (cell_h + GAP)
            canvas.paste(img, (x, y))

    # 底部署名
    footer_y = TARGET_H - MARGIN_BOTTOM + 18

    name_size = 17
    name_en_font = ImageFont.truetype(FONT_EN_LIGHT, name_size)
    name_cn_font = ImageFont.truetype(FONT_CN_PATH, name_size - 2, index=FONT_CN_INDEX)

    cn_part = "跳 蛛 先 生"
    sep_part = "  /  "
    en_part = add_letter_spacing("MR. JUMPING SPIDER", spacing=1)

    cn_w = name_cn_font.getbbox(cn_part)[2] - name_cn_font.getbbox(cn_part)[0]
    sep_w = name_en_font.getbbox(sep_part)[2] - name_en_font.getbbox(sep_part)[0]
    en_w = name_en_font.getbbox(en_part)[2] - name_en_font.getbbox(en_part)[0]

    total_w = cn_w + sep_w + en_w
    start_x = (TARGET_W - total_w) // 2

    draw.text((start_x, footer_y + 2), cn_part, font=name_cn_font, fill=(200, 200, 200))
    draw.text((start_x + cn_w, footer_y), sep_part, font=name_en_font, fill=(200, 200, 200))
    draw.text((start_x + cn_w + sep_w, footer_y), en_part, font=name_en_font, fill=(200, 200, 200))

    sub_size = 12
    sub_font = ImageFont.truetype(FONT_EN_LIGHT, sub_size)
    sub_text = add_letter_spacing("SIX PORTRAITS  ·  MMXXVI", spacing=2)
    sub_w = sub_font.getbbox(sub_text)[2] - sub_font.getbbox(sub_text)[0]
    sub_x = (TARGET_W - sub_w) // 2
    sub_y = footer_y + name_size + 12
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=(120, 120, 120))

    canvas.save(OUTPUT_PATH, "JPEG", quality=92, optimize=True)
    print(f"✓ Saved: {OUTPUT_PATH}")
    print(f"  Size: {TARGET_W}x{TARGET_H}, Cell: {cell_w}x{cell_h}")
    print(f"  File: {OUTPUT_PATH.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
