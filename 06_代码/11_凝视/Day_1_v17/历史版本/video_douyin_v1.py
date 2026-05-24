"""
《凝视 The Gaze》抖音15秒版 - MVP
先跑通 pipeline:6张图轮播 + 入场字幕 + 收尾字幕
特效暂时简单,后续迭代加强
"""

import sys
sys.path.insert(0, "{运行环境}")

from moviepy import (
    ImageClip, TextClip, CompositeVideoClip, concatenate_videoclips,
    ColorClip, AudioFileClip
)
from moviepy.video.fx import FadeIn, FadeOut, CrossFadeIn, CrossFadeOut, Resize
from PIL import Image
import numpy as np
from pathlib import Path

from video_config import (
    CHARACTERS, BASE_DIR, OUTPUT_DIR, FONT_EN, FONT_CN,
    DOUYIN_RESOLUTION, DOUYIN_FPS, DOUYIN_DURATION,
    BLACK, WHITE, GRAY_LIGHT
)

# ==================== 配置 ====================

W, H = DOUYIN_RESOLUTION  # 1080 x 1920
FPS = DOUYIN_FPS
TOTAL_DURATION = DOUYIN_DURATION  # 15s

# 时间分配
TIME_OPENING = 1.5      # 开场字幕
TIME_PER_CHAR = 1.8     # 每个角色展示时长
TIME_ENDING = 2.7       # 收尾字幕

# 验算: 1.5 + 6*1.8 + 2.7 = 15.0 ✓

OUTPUT_FILE = OUTPUT_DIR / "douyin_15s_mvp.mp4"

# ==================== 工具函数 ====================

def fit_image_to_canvas(image_path, canvas_size):
    """
    把图片等比缩放并居中裁剪到目标画布尺寸
    确保画面铺满,人脸居中
    """
    img = Image.open(image_path)
    iw, ih = img.size
    cw, ch = canvas_size
    
    # 计算缩放比例,使图片完全覆盖画布
    scale = max(cw / iw, ch / ih)
    new_w = int(iw * scale)
    new_h = int(ih * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    
    # 居中裁剪
    left = (new_w - cw) // 2
    # 顶部稍微往下一点,确保眼睛在视觉中心(约画面上1/3)
    top = max(0, (new_h - ch) // 2 - int(ch * 0.05))
    top = min(top, new_h - ch)  # 防止超出
    
    img = img.crop((left, top, left + cw, top + ch))
    return np.array(img)

def make_image_clip(image_path, duration, ken_burns=True):
    """
    创建一个图片clip,带ken burns效果(轻微推进)
    """
    img_array = fit_image_to_canvas(image_path, (W, H))
    clip = ImageClip(img_array, duration=duration)
    
    if ken_burns:
        # 从1.0缓慢放大到1.06
        clip = clip.with_effects([Resize(lambda t: 1.0 + 0.06 * (t / duration))])
    
    return clip

def make_text_clip(text, font_size, color, duration, font=FONT_EN):
    """创建一个文字clip"""
    return TextClip(
        text=text,
        font=font,
        font_size=font_size,
        color=color,
        size=(W, None),
        method='caption',
        text_align='center',
        duration=duration,
    )

# ==================== 镜头构建 ====================

def build_opening():
    """开场:1.5秒 黑屏 + 一行字 'THIS TIME, WHO IS WATCHING?'"""
    bg = ColorClip(size=(W, H), color=BLACK, duration=TIME_OPENING)
    
    # 主标题(英文)
    title = make_text_clip(
        "THIS TIME,\nWHO IS WATCHING?",
        font_size=72,
        color="white",
        duration=TIME_OPENING,
    ).with_position('center')
    
    # 加渐入渐出效果
    title = title.with_effects([FadeIn(0.3), FadeOut(0.3)])
    
    return CompositeVideoClip([bg, title], size=(W, H))

def build_character_shot(char, duration):
    """
    单个角色的镜头:
    - 图片(带ken burns)
    - 角色英文名(右下角小字)
    """
    img_clip = make_image_clip(char.image_path, duration)
    
    # 右下角的角色名
    name_clip = make_text_clip(
        char.name_en,
        font_size=36,
        color="white",
        duration=duration,
    ).with_position((W * 0.55, H * 0.92)).with_opacity(0.7)
    
    # 编号
    num_clip = make_text_clip(
        f"0{char.num[-1]} / 06",
        font_size=24,
        color="white",
        duration=duration,
    ).with_position((W * 0.55, H * 0.95)).with_opacity(0.5)
    
    composite = CompositeVideoClip([img_clip, name_clip, num_clip], size=(W, H))
    
    # 加快速渐入渐出做转场
    composite = composite.with_effects([CrossFadeIn(0.2), CrossFadeOut(0.2)])
    
    return composite

def build_ending():
    """收尾:黑屏 + 'SIX EYES. ONE DIRECTION.'"""
    bg = ColorClip(size=(W, H), color=BLACK, duration=TIME_ENDING)
    
    main_text = make_text_clip(
        "SIX EYES.\nONE DIRECTION.",
        font_size=84,
        color="white",
        duration=TIME_ENDING,
    ).with_position('center')
    main_text = main_text.with_effects([FadeIn(0.4), FadeOut(0.4)])
    
    # 底部署名
    sig = make_text_clip(
        "THE GAZE  ·  MR. JUMPING SPIDER",
        font_size=28,
        color="white",
        duration=TIME_ENDING,
    ).with_position(('center', H * 0.92)).with_opacity(0.5)
    sig = sig.with_effects([FadeIn(0.6), FadeOut(0.4)])
    
    return CompositeVideoClip([bg, main_text, sig], size=(W, H))

# ==================== 主流程 ====================

def main():
    print("=" * 60)
    print("《凝视 The Gaze》抖音15秒视频 - MVP构建")
    print("=" * 60)
    
    print("\n构建镜头序列...")
    
    # 1. 开场
    print("  [1] 开场字幕")
    opening = build_opening()
    
    # 2. 6张角色镜头 (按色彩节奏顺序)
    char_clips = []
    for i, char in enumerate(CHARACTERS):
        print(f"  [{i+2}] 角色 {char.num} - {char.name_en}")
        clip = build_character_shot(char, TIME_PER_CHAR)
        char_clips.append(clip)
    
    # 3. 收尾
    print(f"  [{len(CHARACTERS)+2}] 收尾字幕")
    ending = build_ending()
    
    # 4. 拼接
    print("\n拼接视频...")
    all_clips = [opening] + char_clips + [ending]
    final = concatenate_videoclips(all_clips, method="compose")
    
    print(f"\n视频总时长: {final.duration:.1f}s (目标: {TOTAL_DURATION}s)")
    print(f"分辨率: {W}x{H} @ {FPS}fps")
    
    # 5. 渲染
    print(f"\n开始渲染到: {OUTPUT_FILE}")
    final.write_videofile(
        str(OUTPUT_FILE),
        fps=FPS,
        codec='libx264',
        audio=False,  # MVP暂不加音频
        preset='medium',
        threads=4,
        logger=None,  # 减少日志输出
    )
    
    file_size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)
    print(f"\n✓ 渲染完成: {OUTPUT_FILE}")
    print(f"  文件大小: {file_size_mb:.1f} MB")

if __name__ == "__main__":
    main()
