# -*- coding: utf-8 -*-
"""牧云人 — 无字纯净版 (壁纸 / 多图第2张)
仅去底部 'Z' 水印 + 等比裁切到小红书 3:4, 不加任何文字与压角。"""
import os
from PIL import Image

BASE = r"E:\AIGC工作站\46_牧云人_小红书封面"
SRC = BASE + r"\01_素材原图\牧云人_原图_928x1232.png"
OUT = BASE + r"\02_成品封面\牧云人_无字壁纸_v1.png"
TRIM_BOTTOM = 0.060        # 与封面一致, 裁掉底部 6% 去 'Z' 水印

W, H = 1080, 1440          # 小红书 3:4

im = Image.open(SRC).convert("RGB")
im = im.crop((0, 0, im.width, int(im.height * (1 - TRIM_BOTTOM))))
sw, sh = im.size
scale = max(W / sw, H / sh)
im = im.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
x0 = (im.width - W) // 2
y0 = (im.height - H) // 2
im = im.crop((x0, y0, x0 + W, y0 + H))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
im.save(OUT, quality=95)
im.resize((360, 480), Image.LANCZOS).save(BASE + r"\_脚本\preview_clean.jpg", quality=90)
print("saved", OUT, im.size)
