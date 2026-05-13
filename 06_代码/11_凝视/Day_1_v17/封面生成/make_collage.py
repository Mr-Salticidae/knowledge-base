"""
《凝视 The Gaze》系列主视觉拼贴生成

布局: 2列 x 3行
顶部: 中英双语标题(THE GAZE / 凝视)
底部: 创作者署名(中英双语)

排列顺序(基于色彩节奏):
01 银面具(暗红+银)  | 02 金发(黑+银)
03 赛博格(蓝+橙)    | 04 女巫(紫+金)
05 精灵(绿+银)     | 06 末代皇女(暗红+金)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ==================== 配置 ====================

INPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_series")
OUTPUT_PATH = Path("/mnt/user-data/outputs/the_gaze_series/the_gaze_00_cover_collage.jpg")

# 字体
FONT_EN_LIGHT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf"
FONT_EN_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
# 思源宋体 ExtraLight,简体中文(index=2)
FONT_CN_PATH = "/usr/share/fonts/opentype/noto/NotoSerifCJK-ExtraLight.ttc"
FONT_CN_INDEX = 2  # SC = Simplified Chinese

# 拼贴排列(2列x3行)
LAYOUT = [
    ["the_gaze_01_scarlatta.jpg", "the_gaze_02_vesper.jpg"],
    ["the_gaze_03_null-07.jpg",   "the_gaze_04_morgana.jpg"],
    ["the_gaze_05_selenwe.jpg",   "the_gaze_06_veritia.jpg"],
]

# 单张缩略尺寸(用于拼贴)
THUMB_W = 600
THUMB_H = int(THUMB_W * 16 / 9)  # 9:16比例

# 拼贴间隙
GAP = 8

# 标题区域高度
TITLE_HEIGHT = 200

# 底部署名区域高度
FOOTER_HEIGHT = 100

# 边距
MARGIN = 50

# 背景色(纯黑,作品集风格)
BG_COLOR = (0, 0, 0)

# ==================== 函数 ====================

def add_letter_spacing(text, spacing=2):
    """加宽字间距"""
    return (" " * spacing).join(text)

def main():
    # 加载6张图,缩放到统一缩略尺寸
    images = []
    for row in LAYOUT:
        row_imgs = []
        for filename in row:
            path = INPUT_DIR / filename
            img = Image.open(path)
            img = img.resize((THUMB_W, THUMB_H), Image.LANCZOS)
            row_imgs.append(img)
        images.append(row_imgs)

    # 计算画布尺寸
    canvas_w = THUMB_W * 2 + GAP + MARGIN * 2
    grid_h = THUMB_H * 3 + GAP * 2
    canvas_h = TITLE_HEIGHT + grid_h + FOOTER_HEIGHT + MARGIN * 2

    # 创建画布
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # ---- 绘制顶部标题 ----
    # 主标题 THE GAZE
    title_en_size = 70
    title_en_font = ImageFont.truetype(FONT_EN_LIGHT, title_en_size)
    title_en_text = add_letter_spacing("THE GAZE", spacing=3)
    bbox = title_en_font.getbbox(title_en_text)
    title_en_w = bbox[2] - bbox[0]
    title_en_x = (canvas_w - title_en_w) // 2
    title_en_y = MARGIN + 30
    draw.text((title_en_x, title_en_y), title_en_text, font=title_en_font, fill=(255, 255, 255))

    # 副标题 凝视
    title_cn_size = 36
    title_cn_font = ImageFont.truetype(FONT_CN_PATH, title_cn_size, index=FONT_CN_INDEX)
    title_cn_text = "凝  视"  # 用空格手动控制字间距,避免let-spacing对中文的副作用
    bbox = title_cn_font.getbbox(title_cn_text)
    title_cn_w = bbox[2] - bbox[0]
    title_cn_x = (canvas_w - title_cn_w) // 2
    title_cn_y = title_en_y + title_en_size + 25
    draw.text((title_cn_x, title_cn_y), title_cn_text, font=title_cn_font, fill=(180, 180, 180))

    # ---- 绘制6张缩略图 ----
    grid_start_y = TITLE_HEIGHT + MARGIN
    for row_idx, row_imgs in enumerate(images):
        for col_idx, img in enumerate(row_imgs):
            x = MARGIN + col_idx * (THUMB_W + GAP)
            y = grid_start_y + row_idx * (THUMB_H + GAP)
            canvas.paste(img, (x, y))

    # ---- 绘制底部署名 ----
    footer_y = grid_start_y + grid_h + 30

    # 中英姓名:分别渲染中文和英文部分
    name_size = 22

    # 英文部分
    name_en_font = ImageFont.truetype(FONT_EN_LIGHT, name_size)
    # 中文部分(用同样字号,但稍微调小一点,因为中文字符视觉上比英文字符大)
    name_cn_font = ImageFont.truetype(FONT_CN_PATH, name_size - 2, index=FONT_CN_INDEX)

    # 文本组成: 跳蛛先生  /  MR. JUMPING SPIDER
    cn_part = "跳 蛛 先 生"  # 加宽中文字间距
    sep_part = "  /  "
    en_part = add_letter_spacing("MR. JUMPING SPIDER", spacing=1)

    # 测量每段宽度
    cn_bbox = name_cn_font.getbbox(cn_part)
    cn_w = cn_bbox[2] - cn_bbox[0]
    sep_bbox = name_en_font.getbbox(sep_part)
    sep_w = sep_bbox[2] - sep_bbox[0]
    en_bbox = name_en_font.getbbox(en_part)
    en_w = en_bbox[2] - en_bbox[0]

    total_w = cn_w + sep_w + en_w
    start_x = (canvas_w - total_w) // 2

    # 依次绘制
    # 中文(稍微往下调一点对齐基线)
    draw.text((start_x, footer_y + 2), cn_part, font=name_cn_font, fill=(200, 200, 200))
    # 分隔符
    draw.text((start_x + cn_w, footer_y), sep_part, font=name_en_font, fill=(200, 200, 200))
    # 英文
    draw.text((start_x + cn_w + sep_w, footer_y), en_part, font=name_en_font, fill=(200, 200, 200))

    # 编号信息
    sub_size = 16
    sub_font = ImageFont.truetype(FONT_EN_LIGHT, sub_size)
    sub_text = add_letter_spacing("SIX PORTRAITS  ·  MMXXVI", spacing=2)
    bbox = sub_font.getbbox(sub_text)
    sub_w = bbox[2] - bbox[0]
    sub_x = (canvas_w - sub_w) // 2
    sub_y = footer_y + name_size + 18
    draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=(120, 120, 120))

    # 保存
    canvas.save(OUTPUT_PATH, "JPEG", quality=92, optimize=True)
    print(f"✓ Cover collage saved: {OUTPUT_PATH}")
    print(f"  Size: {canvas_w}x{canvas_h}")
    print(f"  File size: {OUTPUT_PATH.stat().st_size / 1024:.0f} KB")

if __name__ == "__main__":
    main()
