"""
《大地之上》封面 v2 · 监控/HUD 美学(伪纪录片真正的样子)

设计转向:
- ❌ 撤掉中央大字标题(那是文艺杂志的玩法)
- ✅ 摄像机 HUD:REC 指示灯 + 时间码 + 帧号 + 通道号
- ✅ 取景框角标(四角"L"形 register marks)
- ✅ 等宽字体(像监控录像/相机 OSD)
- ✅ 标题缩成小字,塞到左下角作为"档案条"
- ✅ 微 VHS 扫描线
- ✅ 整体气质:这一帧是从 30 分钟录像里截出来的,而不是设计师做的封面
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SRC = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/mr_jumping_spider_cinematic_still_ultra_wide_establishing_sho_9c654027-54aa-4e33-acfe-9e7b6af9a7bf_2.png"
DST = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图/00_封面_大地之上_v2.png"

MONO_FONT      = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_BOLD      = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MING_FONT      = "/sessions/tender-admiring-galileo/.local/share/fonts/uming.ttc"  # 中文宋体

img = Image.open(SRC).convert("RGB")
W, H = img.size
print(f"封面尺寸: {W}x{H}")

# Step 1: 极轻调色 + VHS 噪点 + 微暗角
arr = np.asarray(img, dtype=np.float32) / 255.0
mid = 0.5
arr = mid + (arr - mid) * 1.04
rng = np.random.RandomState(2027)
noise = (rng.rand(H, W) - 0.5) * 0.02
arr = np.clip(arr + noise[..., None], 0, 1)

# 微 VHS 扫描线(每隔几行略暗一点)
scanline_rows = np.arange(H) % 3 == 0
arr[scanline_rows] *= 0.97

# 暗角
yy, xx = np.meshgrid(np.linspace(-1, 1, H), np.linspace(-1, 1, W), indexing="ij")
radius = np.sqrt(xx ** 2 + yy ** 2)
vignette = 1.0 - np.clip((radius - 0.5) * 0.22, 0, 0.22)
arr *= vignette[..., None]

arr = np.clip(arr * 255, 0, 255).astype(np.uint8)
canvas = Image.fromarray(arr).convert("RGBA")

# ============ HUD 层 ============
hud = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(hud)

# 文字色:HUD 通常是淡白/淡黄,这里跟着画面调走 — 暖白略带绿
HUD_WHITE = (235, 230, 210, 235)
HUD_DIM   = (200, 195, 175, 180)
REC_RED   = (220, 50, 40, 245)

# ---- 左上:REC 指示 + 时间码 ----
# 红点
rec_x, rec_y = int(W * 0.05), int(H * 0.045)
rec_r = int(H * 0.008)
draw.ellipse([(rec_x - rec_r, rec_y - rec_r), (rec_x + rec_r, rec_y + rec_r)], fill=REC_RED)

# REC 文字
rec_font = ImageFont.truetype(MONO_BOLD, int(H / 60))
draw.text((rec_x + rec_r + int(H * 0.012), rec_y - int(H * 0.012)), "REC", font=rec_font, fill=HUD_WHITE)

# 时间码
tc_font = ImageFont.truetype(MONO_FONT, int(H / 55))
tc_x = rec_x + int(W * 0.10)
tc_y = rec_y - int(H * 0.012)
draw.text((tc_x, tc_y), "14:12:03:18", font=tc_font, fill=HUD_WHITE)

# 时间码下:DATE
date_font = ImageFont.truetype(MONO_FONT, int(H / 75))
draw.text((tc_x, tc_y + int(H * 0.028)), "2027.04.27", font=date_font, fill=HUD_DIM)

# ---- 右上:CAM ID + FILE ----
right_pad = int(W * 0.05)
cam_font = ImageFont.truetype(MONO_BOLD, int(H / 60))
cam_text = "CAM-04"
bb = cam_font.getbbox(cam_text)
draw.text((W - right_pad - (bb[2] - bb[0]), rec_y - int(H * 0.012)), cam_text, font=cam_font, fill=HUD_WHITE)

file_font = ImageFont.truetype(MONO_FONT, int(H / 75))
file_text = "FILE: 0427-A"
bb = file_font.getbbox(file_text)
draw.text((W - right_pad - (bb[2] - bb[0]), rec_y + int(H * 0.016)), file_text, font=file_font, fill=HUD_DIM)

depth_text = "DEPTH: UNCONFIRMED"
bb = file_font.getbbox(depth_text)
draw.text((W - right_pad - (bb[2] - bb[0]), rec_y + int(H * 0.034)), depth_text, font=file_font, fill=HUD_DIM)

# ---- 四角:取景框角标(L 形 register marks) ----
def corner_brackets(draw, x, y, size, thick, color, corner):
    """corner: 'tl', 'tr', 'bl', 'br'"""
    if corner == 'tl':
        # 横
        draw.rectangle([(x, y), (x + size, y + thick)], fill=color)
        # 竖
        draw.rectangle([(x, y), (x + thick, y + size)], fill=color)
    elif corner == 'tr':
        draw.rectangle([(x - size, y), (x, y + thick)], fill=color)
        draw.rectangle([(x - thick, y), (x, y + size)], fill=color)
    elif corner == 'bl':
        draw.rectangle([(x, y - thick), (x + size, y)], fill=color)
        draw.rectangle([(x, y - size), (x + thick, y)], fill=color)
    elif corner == 'br':
        draw.rectangle([(x - size, y - thick), (x, y)], fill=color)
        draw.rectangle([(x - thick, y - size), (x, y)], fill=color)

bracket_size = int(H * 0.025)
bracket_thick = max(2, int(H * 0.0025))
bracket_inset = int(H * 0.02)
bracket_color = (235, 230, 210, 200)

corner_brackets(draw, bracket_inset, bracket_inset, bracket_size, bracket_thick, bracket_color, 'tl')
corner_brackets(draw, W - bracket_inset, bracket_inset, bracket_size, bracket_thick, bracket_color, 'tr')
corner_brackets(draw, bracket_inset, H - bracket_inset, bracket_size, bracket_thick, bracket_color, 'bl')
corner_brackets(draw, W - bracket_inset, H - bracket_inset, bracket_size, bracket_thick, bracket_color, 'br')

# ---- 中央十字准星(很轻,几乎看不见,但增加监控感) ----
cx, cy = W // 2, H // 2
cross_len = int(H * 0.008)
cross_thick = 1
draw.line([(cx - cross_len, cy), (cx + cross_len, cy)], fill=(235, 230, 210, 110), width=cross_thick)
draw.line([(cx, cy - cross_len), (cx, cy + cross_len)], fill=(235, 230, 210, 110), width=cross_thick)

# ---- 左下:档案条(标题塞这里) ----
# 一道半透明黑条 + 等宽字体 + 中英标题
bar_h = int(H * 0.06)
bar_y = H - bar_h - int(H * 0.05)

# 半透明黑条
bar_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bdraw = ImageDraw.Draw(bar_layer)
bar_x_start = int(W * 0.05)
bar_x_end   = int(W * 0.55)
bdraw.rectangle([(bar_x_start, bar_y), (bar_x_end, bar_y + bar_h)], fill=(0, 0, 0, 110))

# 黑条上的红色细线(分隔)
bdraw.rectangle([(bar_x_start, bar_y), (bar_x_start + 4, bar_y + bar_h)], fill=(220, 50, 40, 220))

# 文字
title_font_en = ImageFont.truetype(MONO_BOLD, int(H / 50))
title_font_cn = ImageFont.truetype(MING_FONT, int(H / 35))

# 中文标题
cn_x = bar_x_start + int(W * 0.025)
cn_y = bar_y + int(bar_h * 0.10)
bdraw.text((cn_x, cn_y), "大地之上", font=title_font_cn, fill=(245, 240, 225, 240))

# 英文副标
en_text = "ON  LAND  ABOVE   ·   EP. 01"
en_font = ImageFont.truetype(MONO_FONT, int(H / 80))
en_y = bar_y + int(bar_h * 0.65)
bdraw.text((cn_x, en_y), en_text, font=en_font, fill=(210, 205, 190, 200))

# ---- 右下:警示语 ----
warn_font = ImageFont.truetype(MONO_BOLD, int(H / 75))
warn_text = "RESTRICTED  ·  DO NOT REDISTRIBUTE"
bb = warn_font.getbbox(warn_text)
warn_x = W - right_pad - (bb[2] - bb[0])
warn_y = H - int(H * 0.05) - int(H / 75)
bdraw.text((warn_x, warn_y), warn_text, font=warn_font, fill=(220, 50, 40, 200))

# ---- 上面再加一道顶部的 RECOVERED FOOTAGE 标识带 ----
# 顶部超细黑条
top_bar_h = int(H * 0.018)
top_y = 0
bdraw.rectangle([(0, top_y), (W, top_y + top_bar_h)], fill=(0, 0, 0, 130))
top_text = "▮  R E C O V E R E D    F O O T A G E    ·    A R C H I V E   2 0 2 7  ▮"
top_font = ImageFont.truetype(MONO_BOLD, int(H / 90))
bb = top_font.getbbox(top_text)
top_text_w = bb[2] - bb[0]
top_text_x = (W - top_text_w) // 2
top_text_y = top_y + (top_bar_h - (bb[3] - bb[1])) // 2 - bb[1]
bdraw.text((top_text_x, top_text_y), top_text, font=top_font, fill=HUD_WHITE)

# 合成
canvas = Image.alpha_composite(canvas, bar_layer)
canvas = Image.alpha_composite(canvas, hud)

# 输出
canvas.convert("RGB").save(DST, optimize=True)
print(f"[OK] {DST}")
