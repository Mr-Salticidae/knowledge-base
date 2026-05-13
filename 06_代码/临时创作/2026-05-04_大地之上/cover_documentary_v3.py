"""
《大地之上》封面 v3 · NOROI 式电影海报
参考:《NOROI: The Curse》(2005) 伪纪录片海报

设计语法:
- 上方 78%:纯净照片(零 HUD,零文字,零暗角)
- 下方 22%:纯黑实心条(锐利横切)
- 黑条上:大字中文标题 + 小字英文副标
- 标题字体:风化/缺损效果,模拟"刷上去,经过岁月"
- 副标字体:衬线斜体,小,在标题正下方居中
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/mr_jumping_spider_cinematic_still_ultra_wide_establishing_sho_9c654027-54aa-4e33-acfe-9e7b6af9a7bf_2.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/00_封面_大地之上_v3.png"

MING_FONT       = "/sessions/tender-admiring-galileo/.local/share/fonts/uming.ttc"
SERIF_LATIN     = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_LATIN_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_LATIN_ITAL = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"

img = Image.open(SRC).convert("RGB")
W_orig, H_orig = img.size

# ---- 关键比例 ----
BAR_RATIO   = 0.22   # 黑条占总高度
PHOTO_RATIO = 1.0 - BAR_RATIO  # 照片占的高度

# 海报最终尺寸保持 9:16 风格(原图本身就是 9:16 左右,我们直接用)
W = W_orig
H = H_orig

# ---- Step 1: 准备照片区域(裁剪以保持照片比例,不被压扁) ----
photo_h = int(H * PHOTO_RATIO)
bar_h = H - photo_h

# 照片纵横比保留,从原图按比例裁
photo_aspect_target = W / photo_h  # 目标的宽高比
photo_aspect_orig   = W_orig / H_orig

if photo_aspect_orig > photo_aspect_target:
    # 原图更宽 → 上下裁
    new_h_orig = int(W_orig / photo_aspect_target)
    crop_top = (H_orig - new_h_orig) // 2
    photo_crop = img.crop((0, crop_top, W_orig, crop_top + new_h_orig))
else:
    # 原图更高 → 左右裁
    new_w_orig = int(H_orig * photo_aspect_target)
    crop_left = (W_orig - new_w_orig) // 2
    photo_crop = img.crop((crop_left, 0, crop_left + new_w_orig, H_orig))

photo = photo_crop.resize((W, photo_h), Image.LANCZOS)

# 极轻调色(微提对比,加一点点 grain)
photo_arr = np.asarray(photo, dtype=np.float32) / 255.0
mid = 0.5
photo_arr = mid + (photo_arr - mid) * 1.04
rng = np.random.RandomState(2027)
grain = (rng.rand(photo_h, W) - 0.5) * 0.018
photo_arr = np.clip(photo_arr + grain[..., None], 0, 1)
photo_arr = np.clip(photo_arr * 255, 0, 255).astype(np.uint8)
photo = Image.fromarray(photo_arr)

# ---- Step 2: 拼装最终画布(照片 + 纯黑条) ----
canvas = Image.new("RGB", (W, H), (0, 0, 0))
canvas.paste(photo, (0, 0))
# 黑条已经是默认黑色,无需画

canvas = canvas.convert("RGBA")

# ---- Step 3: 黑条上的标题(风化效果) ----

# 字号:中文标题占黑条高度 ~ 50%
title_size = int(bar_h * 0.50)
title_font = ImageFont.truetype(MING_FONT, title_size)

# 中文字间距:0.18x 字宽(海报感的拉开)
title_text = "大地之上"
char_spacing = int(title_size * 0.18)

# 计算总宽
chars = list(title_text)
char_widths = []
for ch in chars:
    bb = title_font.getbbox(ch)
    char_widths.append(bb[2] - bb[0])
total_title_w = sum(char_widths) + char_spacing * (len(chars) - 1)

# 居中起点
title_x = (W - total_title_w) // 2
# Y 坐标:在黑条内偏上
title_y = photo_h + int(bar_h * 0.18)

# ---- 风化效果:渲染到独立 mask,然后做 erosion + noise ----
mask_pad = title_size  # 留白防止裁切
mask_w = total_title_w + mask_pad * 2
mask_h = title_size + mask_pad * 2
title_mask = Image.new("L", (mask_w, mask_h), 0)
mdraw = ImageDraw.Draw(title_mask)

cur_x = mask_pad
for ch, cw in zip(chars, char_widths):
    bb = title_font.getbbox(ch)
    mdraw.text((cur_x - bb[0], mask_pad - bb[1]), ch, font=title_font, fill=255)
    cur_x += cw + char_spacing

# 应用风化:随机像素点 alpha 归零(模拟掉漆)
mask_arr = np.asarray(title_mask, dtype=np.float32)
rng2 = np.random.RandomState(123)

# 1. 整体性"破损斑"——大块缺失
big_holes = rng2.rand(mask_h, mask_w) < 0.003  # 0.3% 像素是大洞中心
# 把大洞扩散到 3-6 像素直径
big_holes_img = Image.fromarray((big_holes * 255).astype(np.uint8))
big_holes_img = big_holes_img.filter(ImageFilter.GaussianBlur(radius=2))
big_holes_dilated = np.asarray(big_holes_img) > 80

mask_arr[big_holes_dilated] = 0

# 2. 细密斑点——模拟漆面颗粒
fine_noise = rng2.rand(mask_h, mask_w)
mask_arr = mask_arr * (0.85 + fine_noise * 0.15)

# 3. 边缘轻度抖动(像手刷)
mask_arr = np.clip(mask_arr, 0, 255).astype(np.uint8)
title_mask = Image.fromarray(mask_arr)

# ---- 把 mask 渲染成奶白色文字 ----
title_layer = Image.new("RGBA", (mask_w, mask_h), (0, 0, 0, 0))
TITLE_COLOR = (235, 230, 215)
title_arr = np.zeros((mask_h, mask_w, 4), dtype=np.uint8)
title_arr[..., 0] = TITLE_COLOR[0]
title_arr[..., 1] = TITLE_COLOR[1]
title_arr[..., 2] = TITLE_COLOR[2]
title_arr[..., 3] = mask_arr
title_layer = Image.fromarray(title_arr)

# 贴到 canvas
paste_x = title_x - mask_pad
paste_y = title_y - mask_pad
canvas.paste(title_layer, (paste_x, paste_y), title_layer)

# ---- Step 4: 副标(衬线斜体,小,居中) ----
sub_text = "RECOVERED  FOOTAGE"
sub_size = int(bar_h * 0.13)
sub_font = ImageFont.truetype(SERIF_LATIN_ITAL, sub_size)

# 字距 +20%
sub_spacing = int(sub_size * 0.15)
sub_chars = list(sub_text)
sub_char_widths = []
for ch in sub_chars:
    bb = sub_font.getbbox(ch)
    sub_char_widths.append(bb[2] - bb[0])
total_sub_w = sum(sub_char_widths) + sub_spacing * (len(sub_chars) - 1)
sub_x = (W - total_sub_w) // 2
sub_y = title_y + title_size + int(bar_h * 0.10)

sub_draw = ImageDraw.Draw(canvas)
cur_x = sub_x
for ch, cw in zip(sub_chars, sub_char_widths):
    bb = sub_font.getbbox(ch)
    sub_draw.text((cur_x - bb[0], sub_y), ch, font=sub_font, fill=(220, 215, 200, 240))
    cur_x += cw + sub_spacing

# ---- Step 5: 黑条右下角小标识(类似 NOROI 那个 logo) ----
mark_font = ImageFont.truetype(SERIF_LATIN_BOLD, int(bar_h * 0.06))
mark_text = "EP.01"
bb = mark_font.getbbox(mark_text)
mark_x = W - int(W * 0.04) - (bb[2] - bb[0])
mark_y = H - int(bar_h * 0.13) - (bb[3] - bb[1])
sub_draw.text((mark_x, mark_y), mark_text, font=mark_font, fill=(180, 175, 160, 220))

# 输出
canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")
print(f"输出: {W}x{H}, 照片 {photo_h}px, 黑条 {bar_h}px")
