# -*- coding: utf-8 -*-
"""衔风 — 无字纯净版 (3:4)
与封面同一 cover-fit 口径,只是不叠任何文字,作小红书多图第 2 张 / 壁纸钩子。
用法: py make_clean.py
"""
import os
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "01_原图", "原图_衔风.png")
OUT = os.path.join(BASE, "02_成品", "衔风_无字版.png")

W, H = 1080, 1440

im = Image.open(SRC).convert("RGB")
sw, sh = im.size
scale = max(W / sw, H / sh)
im = im.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
x0 = (im.width - W) // 2
y0 = (im.height - H) // 2
im = im.crop((x0, y0, x0 + W, y0 + H))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT, quality=95)
print("saved", OUT, im.size)
