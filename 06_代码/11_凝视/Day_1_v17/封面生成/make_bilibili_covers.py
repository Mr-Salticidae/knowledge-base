"""
生成 B 站封面
- 16:9 主封面(1280 x 720)
- 4:3 横版(800 x 600)
基于 Scarlatta 高清原图
纯图无文字
"""

from PIL import Image
from pathlib import Path

SOURCE = "{运行环境}/scarlatta_hd.png"
OUTPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_video")


def make_16x9_tight():
    """
    16:9 紧凑版 — 直接裁剪到 1632x918,只保留中央带
    特点: 极致贴脸,眼睛+面具横贯,冲击力最大
    """
    img = Image.open(SOURCE)
    W, H = img.size  # 1632 x 2912
    
    target_h = int(W / (16/9))  # 918
    
    # 中心点 y = 0.42(和 4:3 相同的核心区域中心)
    center_y = int(H * 0.42)
    crop_top = center_y - target_h // 2
    crop_bottom = crop_top + target_h
    
    cropped = img.crop((0, crop_top, W, crop_bottom))
    
    # 缩放到 1280x720
    final = cropped.resize((1280, 720), Image.LANCZOS)
    
    output_path = OUTPUT_DIR / "凝视_B站封面_16x9_紧凑版.jpg"
    final.save(output_path, "JPEG", quality=95)
    print(f"✓ 16:9 紧凑版: {output_path.name} ({output_path.stat().st_size // 1024} KB)")
    return output_path


def make_16x9_breathing():
    """
    16:9 呼吸版 — 左右扩展画布,加深色背景作为呼吸空间
    特点: 主体居中,左右黑色 padding,更像电影海报
    
    思路:
    1. 取原图核心三角区域(类似 4:3 横版的裁剪)
    2. 在 1280x720 画布上居中放置
    3. 左右留黑作为电影感边框
    """
    img = Image.open(SOURCE)
    W, H = img.size
    
    # 先做 4:3 裁剪(我们之前的逻辑)
    target_h_43 = int(W / (4/3))  # 1224
    center_y = int(H * 0.42)
    crop_top = center_y - target_h_43 // 2
    crop_bottom = crop_top + target_h_43
    cropped_43 = img.crop((0, crop_top, W, crop_bottom))  # 1632 x 1224
    
    # 缩放,使其能放入 1280x720 画布
    # 我们想让人脸主体占据 720 高度的 100%(满高放置)
    # 1632 x 1224 → 缩到 height=720,width = 720 * 1632/1224 = 960
    new_h = 720
    new_w = int(720 * 1632 / 1224)  # 960
    cropped_43_scaled = cropped_43.resize((new_w, new_h), Image.LANCZOS)
    
    # 创建黑色背景画布
    canvas = Image.new("RGB", (1280, 720), (0, 0, 0))
    
    # 居中放置
    paste_x = (1280 - new_w) // 2  # 160
    paste_y = 0
    canvas.paste(cropped_43_scaled, (paste_x, paste_y))
    
    output_path = OUTPUT_DIR / "凝视_B站封面_16x9_呼吸版.jpg"
    canvas.save(output_path, "JPEG", quality=95)
    print(f"✓ 16:9 呼吸版: {output_path.name} ({output_path.stat().st_size // 1024} KB)")
    return output_path


def make_4x3_for_bilibili():
    """
    4:3 (800 x 600) - B站后台备用封面尺寸
    复用之前抖音的 4:3 构图,只是缩小尺寸
    """
    img = Image.open(SOURCE)
    W, H = img.size
    
    target_h = int(W / (4/3))  # 1224
    center_y = int(H * 0.42)
    crop_top = center_y - target_h // 2
    crop_bottom = crop_top + target_h
    
    cropped = img.crop((0, crop_top, W, crop_bottom))
    final = cropped.resize((800, 600), Image.LANCZOS)
    
    output_path = OUTPUT_DIR / "凝视_B站封面_4x3.jpg"
    final.save(output_path, "JPEG", quality=95)
    print(f"✓ 4:3 横版: {output_path.name} ({output_path.stat().st_size // 1024} KB)")
    return output_path


def main():
    print("="*60)
    print("生成 B 站封面")
    print("="*60)
    print()
    
    make_16x9_tight()
    make_16x9_breathing()
    make_4x3_for_bilibili()
    
    print()
    print("="*60)
    print("生成完成")
    print("="*60)


if __name__ == "__main__":
    main()
