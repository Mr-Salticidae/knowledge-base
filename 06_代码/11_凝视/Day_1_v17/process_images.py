"""
《凝视 The Gaze》系列图片后期处理脚本

功能:
1. 在每张图右下角添加极简署名(横向排版,字间距加大)
2. 自动适配深色/浅色背景(取右下角区域亮度判断)
3. 清除元数据(防止prompt泄露)
4. 输出网络发布版(长边1800px, JPG quality 90)
5. 保留原图不变

署名格式: MR. JUMPING SPIDER  ·  THE GAZE / 0X
"""

from PIL import Image, ImageDraw, ImageFont, ImageStat
import os
from pathlib import Path

# ==================== 配置参数 ====================

# 输入目录
INPUT_DIR = Path("/mnt/user-data/uploads")

# 输出目录
OUTPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_series")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 文件 → 角色编号映射(根据系列顺序)
# 顺序: 01 银面具 → 02 金发 → 03 赛博格 → 04 女巫 → 05 精灵 → 06 末代皇女
FILE_MAPPING = {
    "An_adult_female_female_semi-realistic_style_C_1121eea3": ("01", "SCARLATTA"),
    "Extreme_close-up_portrait_of_a_mature_woman_w_7778099f": ("02", "VESPER"),
    "Extreme_close-up_portrait_of_a_cybernetic_wom_9a6ee3da": ("03", "NULL-07"),
    "Extreme_close-up_portrait_of_a_mysterious_sor_ea1e3bd1": ("04", "MORGANA"),
    "Extreme_close-up_portrait_of_an_elven_huntres_0a2aa377": ("05", "SELENWE"),
    "Extreme_close-up_portrait_of_a_fallen_princes_0c11f5df": ("06", "VERITIA"),
}

# 字体路径
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf"

# 输出尺寸(长边)
TARGET_LONG_EDGE = 1800

# JPG质量
JPG_QUALITY = 90

# 署名内容模板
SIGNATURE_TEMPLATE = "MR. JUMPING SPIDER  ·  THE GAZE / {num}"

# 字间距(letter-spacing模拟,通过插入空格实现宽间距效果)
def add_letter_spacing(text, spacing=1):
    """在每个字符之间插入额外空格来模拟letter-spacing"""
    if spacing == 0:
        return text
    return (" " * spacing).join(text)

# ==================== 核心函数 ====================

def get_corner_brightness(img, corner_size_ratio=0.15):
    """获取右下角区域的平均亮度,用于决定字体颜色"""
    w, h = img.size
    corner_w = int(w * corner_size_ratio)
    corner_h = int(h * corner_size_ratio * 0.5)  # 只取扁平的下方区域

    # 提取右下角区域
    box = (w - corner_w, h - corner_h, w, h)
    corner = img.crop(box).convert("L")  # 转灰度
    stat = ImageStat.Stat(corner)
    return stat.mean[0]  # 0-255

def add_signature(img, signature_text):
    """
    在图片右下角添加署名
    统一用白色文字 + 微弱黑色阴影,保证所有背景下都可读
    保持极简克制的视觉效果
    """
    img = img.copy().convert("RGBA")
    w, h = img.size

    # 字号 = 长边的 1.3%
    long_edge = max(w, h)
    font_size = int(long_edge * 0.013)

    # 加载字体
    font = ImageFont.truetype(FONT_PATH, font_size)

    # 处理字间距
    text_with_spacing = add_letter_spacing(signature_text, spacing=1)

    # 测量文字尺寸
    bbox = font.getbbox(text_with_spacing)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 计算位置:右下角,边距为画面尺寸的一定比例
    margin_right = int(w * 0.04)
    margin_bottom = int(h * 0.025)

    x = w - text_w - margin_right
    y = h - text_h - margin_bottom - bbox[1]  # 减去bbox上偏移

    # 创建透明图层用于绘制文字
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # 第1层:微弱黑色阴影(给浅色背景下的可读性兜底)
    # 用偏移量极小的多次描边模拟微弱shadow,而不是用模糊(模糊会失去极简感)
    shadow_color = (0, 0, 0, 90)  # 黑色 35% 不透明度
    shadow_offsets = [(1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
    for dx, dy in shadow_offsets:
        draw.text((x + dx, y + dy), text_with_spacing, font=font, fill=shadow_color)

    # 第2层:主文字(白色,65% 不透明度)
    main_color = (255, 255, 255, 165)
    draw.text((x, y), text_with_spacing, font=font, fill=main_color)

    # 合并图层
    result = Image.alpha_composite(img, txt_layer)
    return result.convert("RGB")  # 转回RGB准备保存JPG

def resize_image(img, target_long_edge=TARGET_LONG_EDGE):
    """等比缩放到目标长边"""
    w, h = img.size
    long_edge = max(w, h)

    if long_edge <= target_long_edge:
        return img  # 已经够小

    scale = target_long_edge / long_edge
    new_w = int(w * scale)
    new_h = int(h * scale)
    return img.resize((new_w, new_h), Image.LANCZOS)

def process_image(input_path, output_path, char_num, char_name):
    """处理单张图片的完整流程"""
    print(f"  Processing: {char_num} - {char_name}")

    # 1. 打开图片
    img = Image.open(input_path)

    # 2. 缩放到网络版尺寸
    img = resize_image(img)

    # 3. 添加署名
    signature = SIGNATURE_TEMPLATE.format(num=char_num)
    img = add_signature(img, signature)

    # 4. 保存为JPG(自动剥离EXIF元数据)
    # PIL默认保存JPG时不会保留PNG的元数据,这一步天然清理
    img.save(output_path, "JPEG", quality=JPG_QUALITY, optimize=True)

    print(f"    ✓ Saved: {output_path.name} ({img.size[0]}x{img.size[1]})")

# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("《凝视 The Gaze》系列图片后期处理")
    print("=" * 60)

    # 找到所有匹配的输入文件
    all_inputs = list(INPUT_DIR.glob("*.png"))

    matched = []
    for input_file in all_inputs:
        for key, (num, name) in FILE_MAPPING.items():
            if key in input_file.name:
                matched.append((input_file, num, name))
                break

    matched.sort(key=lambda x: x[1])  # 按编号排序

    print(f"\n找到 {len(matched)} 张匹配的图片:\n")

    for input_path, num, name in matched:
        output_filename = f"the_gaze_{num}_{name.lower()}.jpg"
        output_path = OUTPUT_DIR / output_filename
        process_image(input_path, output_path, num, name)

    print(f"\n✓ 处理完成!所有图片已保存到: {OUTPUT_DIR}")
    print("\n输出文件列表:")
    for f in sorted(OUTPUT_DIR.glob("*.jpg")):
        size_kb = f.stat().st_size / 1024
        print(f"  - {f.name} ({size_kb:.0f} KB)")

if __name__ == "__main__":
    main()
