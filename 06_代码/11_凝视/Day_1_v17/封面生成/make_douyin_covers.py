"""
生成抖音封面 — 3:4 竖版 + 4:3 横版
基于 Scarlatta 高清原图(1632 x 2912)
纯图无文字,B方案三角构图
"""

from PIL import Image
from pathlib import Path

# 配置
SOURCE = "/home/claude/scarlatta_hd.png"
OUTPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_video")

# 输出尺寸
PORTRAIT_W, PORTRAIT_H = 1200, 1600   # 3:4 竖版
LANDSCAPE_W, LANDSCAPE_H = 1600, 1200  # 4:3 横版


def make_portrait_cover():
    """
    3:4 竖版(1200 x 1600)
    
    原图 1632x2912 比例 0.560,目标 0.750(更宽更矮)
    需要:左右扩,或者上下裁
    
    策略:适度裁去顶部(红头巾)和底部(手腕红袖)
    保留:王冠 → 眼睛 → 面具 → 手指 → 部分斗篷
    水平方向居中或略偏右(让左侧手有完整呈现)
    """
    img = Image.open(SOURCE)
    W, H = img.size  # 1632 x 2912
    
    # 计算需要的裁剪
    # 目标比例 3:4 = 0.75
    # 原图 1632/2912 = 0.561,垂直方向太长
    # 保持原宽度 1632,需要的高度 = 1632 / 0.75 = 2176
    # 总共需要裁掉 2912 - 2176 = 736 像素
    
    target_h = int(W / 0.75)  # 2176
    crop_total = H - target_h  # 736
    
    # 裁剪策略:从顶部裁多一点(红头巾不是核心),底部少裁(手部很重要)
    # 顶部裁 60%,底部裁 40%
    crop_top = int(crop_total * 0.6)   # 442
    crop_bottom = int(crop_total * 0.4) # 294
    
    # 裁剪
    cropped = img.crop((0, crop_top, W, H - crop_bottom))
    print(f"3:4 竖版: 裁剪 {cropped.size}, 顶部裁 {crop_top}px, 底部裁 {crop_bottom}px")
    
    # 缩放到目标尺寸
    final = cropped.resize((PORTRAIT_W, PORTRAIT_H), Image.LANCZOS)
    
    output_path = OUTPUT_DIR / "凝视_抖音封面_3x4竖版.jpg"
    final.save(output_path, "JPEG", quality=95)
    print(f"✓ 已保存: {output_path.name} ({output_path.stat().st_size / 1024:.0f} KB)")
    return output_path


def make_landscape_cover():
    """
    4:3 横版(1600 x 1200)
    
    原图 1632x2912 比例 0.560,目标 1.333(横版)
    需要:大量裁剪上下,只保留中心三角区域
    
    B方案三角构图:
    - 顶部:略保留眉毛和上眼皮(让眼睛有"上方空间")
    - 底部:略保留手指压面具(三角的下顶点)
    - 中心焦点:眼睛 + 面具 + 手指
    
    估算:三角区域大概是 y 22% 到 y 60% 之间
    """
    img = Image.open(SOURCE)
    W, H = img.size  # 1632 x 2912
    
    # 目标比例 4:3 = 1.333
    # 保持原宽度 1632,需要的高度 = 1632 / 1.333 = 1224
    # 总共需要裁掉 2912 - 1224 = 1688 像素(很多!)
    
    target_h = int(W / 1.333)  # 1224
    crop_total = H - target_h  # 1688
    
    # 三角构图:核心区域中心点估算在 y = 42% 处(眼睛、面具、手指的视觉重心)
    # 把这个点放在裁剪后画面的中心
    center_y_ratio = 0.42
    target_center_y = H * center_y_ratio  # 1223 像素
    
    crop_top = int(target_center_y - target_h / 2)   # 611
    crop_bottom = H - (crop_top + target_h)          # 1077
    
    # 检查是否合理
    print(f"4:3 横版: 中心 y 比例 {center_y_ratio}")
    print(f"  裁剪范围: y {crop_top} 到 {crop_top + target_h}")
    print(f"  顶部裁 {crop_top}px, 底部裁 {crop_bottom}px")
    
    # 裁剪
    cropped = img.crop((0, crop_top, W, crop_top + target_h))
    print(f"  裁剪后尺寸: {cropped.size}")
    
    # 缩放到目标尺寸
    final = cropped.resize((LANDSCAPE_W, LANDSCAPE_H), Image.LANCZOS)
    
    output_path = OUTPUT_DIR / "凝视_抖音封面_4x3横版.jpg"
    final.save(output_path, "JPEG", quality=95)
    print(f"✓ 已保存: {output_path.name} ({output_path.stat().st_size / 1024:.0f} KB)")
    return output_path


def main():
    print("="*60)
    print("生成抖音封面")
    print("="*60)
    print()
    
    p1 = make_portrait_cover()
    print()
    p2 = make_landscape_cover()
    
    print()
    print("="*60)
    print("生成完成")
    print("="*60)


if __name__ == "__main__":
    main()
