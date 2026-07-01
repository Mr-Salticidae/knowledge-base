# -*- coding: utf-8 -*-
"""
断裂网格杂志海报 · 母版脚本（内核开发版）
================================================
把「一张竖构图英雄图」排成杂志感海报：整张图被切进一组断裂的 3 列网格，
缝隙露出底色，读起来是「一整张被切开」而非九宫格缩略图。
配左上标题 / 正文块、左下署名、右下虹彩玻璃装饰。

核心机制（这份脚本的价值点，见 04_方法论与洞察/05_prompt与工具方法/断裂网格杂志海报排版工作流_v1.md）：
  整张原图按 cover 缩放铺满「整个网格区域」，每个格子只显示它覆盖到的那一块，
  缝隙保持底色 → 视觉上是一张连续图被网格切开。

改这里就能复用：SRC / OUT / 顶部 CONFIG 文案与配色。
学员一键版见 08_对外分发/断裂网格海报_一键生成_学员版/
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import math, os

# ========== 改这里 ==========
SRC   = r"C:\Users\Administrator\Downloads\你的英雄图.png"   # 原图（竖构图最佳）
OUT   = r"C:\Users\Administrator\Downloads\海报成品.png"
TITLE = "STATIC / BLOOM"
BODY  = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do",
    "eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis",
    "ipsum suspendisse ultrices gravida. Risus commodo viverra",
    "maecenas accumsan lacus vel facilisis.",
]
CRED  = ["create 01", "Jul 2026", "", "create by", "mr.spider"]
TAG   = "N°01"
# 配色（暗调，脱胎自图1的绿、拉向源图灰调；霓虹取自源图）
BG_TL = (60, 68, 46)      # 底色渐变 左上
BG_BR = (20, 26, 17)      # 底色渐变 右下
INK   = (236, 238, 230)   # 标题白
BODY_C= (198, 204, 186)   # 正文
CRED_C= (206, 208, 196)   # 署名
LIME  = (190, 240, 44)    # 霓虹绿点缀
MAG   = (232, 30, 140)    # 品红点缀
W, H  = 1080, 1440
# ============================

def font(paths, size):
    """按候选列表找字体，找不到退回 PIL 默认（保证不崩）"""
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FBOLD = [r"C:\Windows\Fonts\arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
FREG  = [r"C:\Windows\Fonts\arial.ttf",   "/System/Library/Fonts/Supplemental/Arial.ttf"]

def gradient(size, c1, c2):
    w, h = size
    base = Image.new("RGB", size, c1); top = Image.new("RGB", size, c2)
    mask = Image.new("L", size); md = mask.load(); maxd = w + h
    for y in range(h):
        for x in range(w):
            md[x, y] = int(255 * (x + y) / maxd)
    return Image.composite(top, base, mask)

def cover(img, tw, th, bias_y=0.5):
    """等比放大到盖满 tw×th 再裁；bias_y<0.5 偏上裁（留住头部）"""
    iw, ih = img.size
    s = max(tw / iw, th / ih)
    nw, nh = int(math.ceil(iw * s)), int(math.ceil(ih * s))
    im = img.resize((nw, nh), Image.LANCZOS)
    offx = int((nw - tw) * 0.5); offy = int((nh - th) * bias_y)
    return im.crop((offx, offy, offx + tw, offy + th))

def build():
    canvas = gradient((W, H), BG_TL, BG_BR)
    # 柔暗角
    vig = Image.new("L", (W, H), 0); vd = ImageDraw.Draw(vig)
    vd.ellipse([-W*0.3, -H*0.2, W*1.3, H*1.2], fill=40)
    vig = vig.filter(ImageFilter.GaussianBlur(200))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    canvas = Image.composite(canvas, dark,
                             ImageChops.invert(vig).point(lambda p: 255 - int(p*0.12))).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    ML, MR = 138, W - 130
    title_f = font(FBOLD, 46); body_f = font(FREG, 21)
    cred_f = font(FREG, 22); tag_f = font(FBOLD, 16)

    # 标题 + 品红短横
    ty = 150
    draw.text((ML, ty), TITLE, font=title_f, fill=INK)
    tb = draw.textbbox((ML, ty), TITLE, font=title_f)
    draw.rectangle([ML, tb[3] + 12, ML + 92, tb[3] + 16], fill=MAG)
    # 正文
    by = tb[3] + 34
    for ln in BODY:
        draw.text((ML, by), ln, font=body_f, fill=BODY_C); by += 30

    # ---- 断裂网格 ----
    gx, gy = ML, by + 34
    gw, gh = MR - ML, H - (by + 34) - 168
    cg, rg = 16, 16
    colW = (gw - 2*cg) / 3.0
    cx = [gx, gx + colW + cg, gx + 2*(colW + cg)]
    wideW = 2*colW + cg
    usable = gh - 3*rg
    bh = [usable*f for f in (0.19, 0.19, 0.19, 0.43)]
    band_y = []; yy = gy
    for h in bh:
        band_y.append(yy); yy += h + rg
    tiles = []
    for c in range(3): tiles.append((cx[c], band_y[0], colW, bh[0]))      # 顶排三格
    tiles += [(cx[0], band_y[1], wideW, bh[1]), (cx[2], band_y[1], colW, bh[1])]  # 宽+窄
    tiles += [(cx[0], band_y[2], wideW, bh[2]), (cx[2], band_y[2], colW, bh[2])]  # 宽+窄
    for c in range(3): tiles.append((cx[c], band_y[3], colW, bh[3]))      # 底排三高格

    src = Image.open(SRC).convert("RGB")
    grid_img = cover(src, int(round(gw)), int(round(gh)), bias_y=0.28)

    # 格子柔影
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    for (tx, tyy, tw, th) in tiles:
        sd.rectangle([int(tx)+6, int(tyy)+8, int(tx+tw)+6, int(tyy+th)+8], fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    canvas.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0),
                 shadow.split()[3].point(lambda p: int(p*0.55)))
    draw = ImageDraw.Draw(canvas)

    # 逐格贴同一张连续图的对应切片
    for (tx, tyy, tw, th) in tiles:
        sx, sy = int(round(tx - gx)), int(round(tyy - gy))
        itw, ith = int(round(tw)), int(round(th))
        canvas.paste(grid_img.crop((sx, sy, sx + itw, sy + ith)), (int(round(tx)), int(round(tyy))))
        draw.rectangle([int(round(tx)), int(round(tyy)),
                        int(round(tx+tw))-1, int(round(tyy+th))-1], outline=(12, 16, 10), width=1)

    # 署名（左下）
    cyu = H - 128
    for i, line in enumerate(CRED):
        draw.text((ML, cyu + i*26 + (14 if i >= 3 else 0)), line, font=cred_f, fill=CRED_C)
    draw.text((MR - 54, 150), TAG, font=tag_f, fill=LIME)

    # 虹彩玻璃装饰（右下，呼应图1的水晶十字）
    orn = crystal()
    canvas = Image.alpha_composite(canvas.convert("RGBA"), orn).convert("RGB")
    canvas.save(OUT, quality=95)
    print("saved:", OUT, canvas.size)

def _prism(layer, cx0, cy0, angle, length, width, colors):
    a = math.radians(angle); dx, dy = math.cos(a), math.sin(a); px, py = -dy, dx
    L, Wd = length/2, width/2
    pts = [(cx0+dx*L, cy0+dy*L),
           (cx0+dx*L*0.55+px*Wd, cy0+dy*L*0.55+py*Wd),
           (cx0-dx*L*0.55+px*Wd, cy0-dy*L*0.55+py*Wd),
           (cx0-dx*L, cy0-dy*L),
           (cx0-dx*L*0.55-px*Wd, cy0-dy*L*0.55-py*Wd),
           (cx0+dx*L*0.55-px*Wd, cy0+dy*L*0.55-py*Wd)]
    d = ImageDraw.Draw(layer); n = 60
    for i in range(n):
        t = i/(n-1); seg = t*(len(colors)-1); k = min(int(seg), len(colors)-2); f = seg-k
        c0, c1 = colors[k], colors[k+1]
        col = tuple(int(c0[j]+(c1[j]-c0[j])*f) for j in range(3)) + (235,)
        t0 = t-0.5; cxk = cx0+dx*t0*length; cyk = cy0+dy*t0*length
        wt = max(Wd*(1-abs(t0)*1.1), 1)
        d.line([(cxk+px*wt, cyk+py*wt), (cxk-px*wt, cyk-py*wt)], fill=col, width=int(length/n)+2)
    d.line([pts[0], pts[3]], fill=(255, 255, 255, 210), width=2)
    d.polygon(pts, outline=(255, 255, 255, 170))

def crystal():
    orn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    ocx, ocy = W - 118, H - 132
    gd.ellipse([ocx-170, ocy-170, ocx+170, ocy+170], fill=(140, 225, 130, 55))
    orn = Image.alpha_composite(orn, glow.filter(ImageFilter.GaussianBlur(70)))
    irid  = [(120, 235, 150), (120, 215, 245), (240, 244, 250), (232, 60, 150)]
    irid2 = [(120, 215, 245), (240, 244, 250), (150, 235, 150), (232, 60, 150)]
    _prism(orn, ocx, ocy, 62, 430, 116, irid)
    _prism(orn, ocx, ocy, -28, 340, 92, irid2)
    return orn

if __name__ == "__main__":
    build()
