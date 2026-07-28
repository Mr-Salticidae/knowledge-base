# -*- coding: utf-8 -*-
"""衔风 — 小红书作品封面 (高调冷白底 · 深墨题跋式)
底图是高调近白背景 + 人物暗部,故走"深冷墨宋体竖排 + 白柔光晕托字 + 绯红细线 + 朱砂印、不压暗角"
(参照 48_梦游困境 / 46_牧云人 题跋母版,配色随底图明暗反转,不套暗调封面的浅色标题)。
文字全部进左侧纯净留白,不压脸、不压发丝高光。
用法: py make_cover.py   依赖: pip install Pillow (numpy 可选)
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "01_原图", "原图_衔风.png")
OUT = os.path.join(BASE, "02_成品", "衔风_小红书封面.png")

HERO = "衔风"           # 竖排主标(深墨,进左侧冷白留白)
SUB = "偏不肯下"        # 楷体钩子句(米白,进左下黑衣暗部)
SEAL = "風"             # 朱砂闲章

W, H = 1080, 1440       # 3:4 小红书竖版
SS = 2
w, h = W * SS, H * SS

FONTS = r"C:\Windows\Fonts"
f_song = lambda s: ImageFont.truetype(os.path.join(FONTS, "simsun.ttc"), s)
f_kai = lambda s: ImageFont.truetype(os.path.join(FONTS, "simkai.ttf"), s)

INK = (34, 40, 54)          # 深冷墨
INK2 = (74, 80, 96)         # 题跋次级墨
RED = (168, 40, 44)         # 绯红,呼应发带与格纹
HALO = (255, 255, 255)      # 白柔光晕(高调底托字用)

# —— cover-fit 到 3:4 ——
im = Image.open(SRC).convert("RGB")
sw, sh = im.size
scale = max(w / sw, h / sh)
im = im.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
x0 = (im.width - w) // 2
y0 = (im.height - h) // 2
im = im.crop((x0, y0, x0 + w, y0 + h)).convert("RGBA")

txt = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(txt)
S = SS


def vtext(x, y_start, chars, font, fill, step):
    yy = y_start
    for ch in chars:
        d.text((x, yy), ch, font=font, fill=fill, anchor="mm")
        yy += step


# 主标 竖排宋体 · 左侧冷白留白(深墨 + 白柔光晕)
vtext(116 * S, 408 * S, HERO, f_song(124 * S), INK, step=152 * S)
# 绯红细竖线(与主标同高)
d.line([(192 * S, 336 * S), (192 * S, 632 * S)], fill=RED + (150,), width=2 * S)

# 白柔光晕托字(高调底防糊)
alpha = txt.split()[3]
halo = Image.new("RGBA", (w, h), HALO + (0,))
halo.putalpha(alpha.point(lambda v: int(v * 0.78)))
halo = halo.filter(ImageFilter.GaussianBlur(7 * S))

base = im.copy()
base.alpha_composite(halo)
base.alpha_composite(txt)

# 钩子句 竖排楷体 · 左下黑衣暗部(米白 + 极淡暗投影,避免深字压深衣糊掉)
sub = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d2 = ImageDraw.Draw(sub)
f_sub = f_kai(38 * S)
yy = 916 * S
for ch in SUB:
    d2.text((116 * S, yy), ch, font=f_sub, fill=(246, 242, 236, 236), anchor="mm")
    yy += 62 * S
shadow = Image.new("RGBA", (w, h), (10, 12, 18, 0))
shadow.putalpha(sub.split()[3].point(lambda v: int(v * 0.5)))
shadow = shadow.filter(ImageFilter.GaussianBlur(8 * S))
base.alpha_composite(shadow)
base.alpha_composite(sub)

# 朱砂印(左下暗部)
seal = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ds = ImageDraw.Draw(seal)
sx, sy, ss_ = 92 * S, 1266 * S, 62 * S
ds.rounded_rectangle([sx, sy, sx + ss_, sy + ss_], radius=5 * S, fill=RED + (228,))
ds.text((sx + ss_ * 0.5, sy + ss_ * 0.52), SEAL, font=f_kai(40 * S),
        fill=(252, 246, 240, 255), anchor="mm")
base.alpha_composite(seal)

out = base.convert("RGB").resize((W, H), Image.LANCZOS)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
out.save(OUT, quality=95)
out.resize((360, 480), Image.LANCZOS).save(os.path.join(BASE, "preview.jpg"), quality=90)
print("saved", OUT, out.size)
