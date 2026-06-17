# -*- coding: utf-8 -*-
"""牧云人 — 小红书封面 代码排版 (优雅简约 / 诗意)"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = r"E:\AIGC工作站\46_牧云人_小红书封面"
SRC = BASE + r"\01_素材原图\牧云人_原图_928x1232.png"
OUT = BASE + r"\02_成品封面\牧云人_封面_v1.png"
TRIM_BOTTOM = 0.060        # 裁掉底部 6% 去除画面右下 "Z" 水印

W, H = 1080, 1440           # 小红书 3:4
SS = 2                      # 超采样倍数, 后期缩回 → 边缘更顺滑
w, h = W * SS, H * SS

FONTS = r"C:\Windows\Fonts"
f_song = lambda s: ImageFont.truetype(os.path.join(FONTS, "simsun.ttc"), s)
f_kai  = lambda s: ImageFont.truetype(os.path.join(FONTS, "simkai.ttf"), s)
f_lat  = lambda s: ImageFont.truetype(os.path.join(FONTS, "Dengl.ttf"), s)

INK   = (244, 246, 247)     # 雾白
INK2  = (228, 233, 236)
SHCOL = (10, 14, 20)        # 阴影深蓝灰

# ---------- 1. 底图: 先裁底部去水印, 再等比裁切到 3:4 ----------
im = Image.open(SRC).convert("RGB")
im = im.crop((0, 0, im.width, int(im.height * (1 - TRIM_BOTTOM))))
sw, sh = im.size
scale = max(w / sw, h / sh)
im = im.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
x0 = (im.width - w) // 2
y0 = (im.height - h) // 2
im = im.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")

# ---------- 2. 柔光压角 (只压左上 / 左下, 保留云朵与人物高光) ----------
def corner_scrim(cx, cy, rx, ry, amax):
    """以 (cx,cy) 为中心的椭圆衰减暗角"""
    layer = Image.new("L", (w, h), 0)
    px = layer.load()
    try:
        import numpy as np
        yy, xx = np.mgrid[0:h, 0:w]
        d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        a = np.clip(1 - d, 0, 1) ** 1.6 * amax
        layer = Image.fromarray(a.astype("uint8"), "L")
    except Exception:
        for yv in range(0, h, 2):
            for xv in range(0, w, 2):
                d = ((xv - cx) / rx) ** 2 + ((yv - cy) / ry) ** 2
                v = max(0.0, 1 - d) ** 1.6 * amax
                px[xv, yv] = int(v)
    return layer

scrim = Image.new("RGBA", (w, h), (18, 26, 36, 0))
m = corner_scrim(0, 0, 720 * SS / 1080 * 1080, 760, 118)        # 左上
m2 = corner_scrim(0, h, 760, 360, 96)                           # 左下
from PIL import ImageChops
mask = ImageChops.lighter(m, m2)
scrim.putalpha(mask)
im = Image.alpha_composite(im, scrim)

# ---------- 3. 文本层 (带柔和投影) ----------
txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(txt)

def vtext(x, y_start, chars, font, fill, step, ls=0):
    """竖排, 每字以 x 为水平中心, 逐字下落"""
    yy = y_start
    for ch in chars:
        if ch == " ":
            yy += step
            continue
        d.text((x, yy), ch, font=font, fill=fill, anchor="mm")
        yy += step

S = SS  # 缩写
# 主标题 牧云人 — 宋体, 竖排, 左上
hero = f_song(150 * S)
vtext(150 * S, 230 * S, "牧云人", hero, INK, step=185 * S)

# 细分隔线 (竖)
d.line([(232 * S, 150 * S), (232 * S, 660 * S)], fill=INK2 + (140,), width=2 * S)

# 副标题 楷体, 竖排, 标题右侧 (落款式, 略低起)
sub = f_kai(40 * S)
vtext(286 * S, 250 * S, "山中无岁月", sub, INK2, step=52 * S)
vtext(286 * S, 250 * S + 6 * 52 * S, "捧一朵云回家", sub, INK2, step=52 * S)

# 底部小标 — 英文 + 中文 (左下)
d.line([(72 * S, 1318 * S), (150 * S, 1318 * S)], fill=INK2 + (170,), width=2 * S)
lat = f_lat(27 * S)
def tracked(x, y, s, font, fill, tr):
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + tr
tracked(72 * S, 1338 * S, "THE CLOUD HERDER", lat, INK + (220,), 7 * S)
foot = f_kai(27 * S)
d.text((72 * S, 1384 * S), "牧云人 · 山间慢生活手记", font=foot, fill=INK2 + (190,))

# 柔和投影: 由文本 alpha 派生
alpha = txt.split()[3]
sh = Image.new("RGBA", (w, h), SHCOL + (0,))
sh.putalpha(alpha.point(lambda v: int(v * 0.6)))
sh = sh.filter(ImageFilter.GaussianBlur(5 * S))

base = im.copy()
base.alpha_composite(sh, (0, 3 * S))
base.alpha_composite(txt)

# ---------- 4. 缩回 + 导出 ----------
out = base.convert("RGB").resize((W, H), Image.LANCZOS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.save(OUT, quality=95)
out.resize((360, 480), Image.LANCZOS).save(
    BASE + r"\_脚本\preview.jpg", quality=90)
print("saved", OUT, out.size)
