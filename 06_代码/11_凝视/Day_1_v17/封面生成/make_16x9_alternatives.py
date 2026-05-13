"""
B站封面 16:9 — 两个改进版本对比
A: 优化虚化版(模糊更强 + 边缘羽化)
B: 纯裁剪版(横向裁剪,主体居中,无 padding)
"""

from PIL import Image, ImageFilter, ImageEnhance
from pathlib import Path

SOURCE = "/home/claude/scarlatta_hd.png"
OUTPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_video")


def make_blur_v2():
    """优化的虚化版:更强模糊 + 边缘暗化"""
    img = Image.open(SOURCE)
    W, H = img.size
    
    canvas_w, canvas_h = 1280, 720
    
    # 背景:横向放大并模糊
    # 不用宽度撑满,而用 高度撑满 让背景更抽象(不会有清晰的轮廓)
    scale_to_fill_height = canvas_h / H * 1.3  # 1.3 倍是为了有足够"溢出"的内容
    bg_w = int(W * scale_to_fill_height)
    bg_h = int(H * scale_to_fill_height)
    bg_resized = img.resize((bg_w, bg_h), Image.LANCZOS)
    
    # 居中裁剪到 canvas 大小
    crop_x = (bg_w - canvas_w) // 2
    crop_y = (bg_h - canvas_h) // 2
    bg_cropped = bg_resized.crop((crop_x, crop_y, crop_x + canvas_w, crop_y + canvas_h))
    
    # 强模糊
    bg_blurred = bg_cropped.filter(ImageFilter.GaussianBlur(radius=60))
    bg_dimmed = ImageEnhance.Brightness(bg_blurred).enhance(0.55)
    
    # 主体(4:3 区域)
    target_h_43 = int(W / (4/3))
    center_y = int(H * 0.42)
    crop_top_43 = center_y - target_h_43 // 2
    cropped_43 = img.crop((0, crop_top_43, W, crop_top_43 + target_h_43))
    
    new_h = 720
    new_w = int(720 * 1632 / 1224)  # 960
    fg = cropped_43.resize((new_w, new_h), Image.LANCZOS)
    
    # 给主体加一点轻微的羽化边缘(让边界过渡更柔)
    # 创建一个左右渐变的 alpha 蒙版
    feather_width = 30
    fg_with_alpha = fg.convert("RGBA")
    pixels = fg_with_alpha.load()
    fw, fh = fg_with_alpha.size
    for x in range(feather_width):
        alpha = int(255 * x / feather_width)
        for y in range(fh):
            r, g, b, _ = pixels[x, y]
            pixels[x, y] = (r, g, b, alpha)
            r, g, b, _ = pixels[fw - 1 - x, y]
            pixels[fw - 1 - x, y] = (r, g, b, alpha)
    
    # 合成
    canvas = bg_dimmed.convert("RGBA")
    paste_x = (canvas_w - new_w) // 2
    canvas.paste(fg_with_alpha, (paste_x, 0), fg_with_alpha)
    canvas = canvas.convert("RGB")
    
    output_path = OUTPUT_DIR / "凝视_B站封面_16x9_虚化优化版.jpg"
    canvas.save(output_path, "JPEG", quality=95)
    print(f"✓ 虚化优化版: {output_path.name}")
    return output_path


def make_crop_v2():
    """
    纯裁剪版,不留黑边
    
    思路:横向裁剪到 16:9,但选择最佳裁剪位置
    原图 1632x2912,16:9 需要 1632x918
    选择中心 y 让构图最美
    """
    img = Image.open(SOURCE)
    W, H = img.size
    
    target_h = int(W / (16/9))  # 918
    
    # 关键:选择哪个 y 中心
    # 0.30 = 眼睛中心(完整眼睛 + 王冠)
    # 0.35 = 眼睛 + 部分面具
    # 0.42 = 面具中心(之前的版本,导致眼睛偏右上)
    # 0.38 = 折中(面具+一只完整眼睛+部分王冠)
    
    # 新选择: 0.35 — 让眼睛在视觉中心,面具延展到下半部分
    center_y_ratio = 0.35
    center_y = int(H * center_y_ratio)
    crop_top = center_y - target_h // 2
    crop_top = max(0, min(crop_top, H - target_h))
    
    cropped = img.crop((0, crop_top, W, crop_top + target_h))
    print(f"  裁剪范围: y {crop_top}-{crop_top + target_h}, 中心 y 比例 {center_y_ratio}")
    
    final = cropped.resize((1280, 720), Image.LANCZOS)
    
    output_path = OUTPUT_DIR / "凝视_B站封面_16x9_纯裁剪版.jpg"
    final.save(output_path, "JPEG", quality=95)
    print(f"✓ 纯裁剪版: {output_path.name}")
    return output_path


if __name__ == "__main__":
    make_blur_v2()
    make_crop_v2()
