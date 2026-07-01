# -*- coding: utf-8 -*-
"""
断裂网格杂志海报 · 一键生成器（学员版）
========================================
把你的一张竖构图图片，排成杂志感海报：整张图被切进断裂网格、缝隙露底色，
配标题、正文、署名和一枚虹彩玻璃装饰。

【怎么用】三选一：
  1) 把图片拖到「把图片拖到我身上_Windows.bat」上（最省事）；
  2) 把这个 .py 和图片放同一个文件夹，双击运行，会自动挑文件夹里第一张图；
  3) 双击运行后，按提示把图片路径粘进去。
成品会存在原图旁边，文件名加「_海报」。

【只需要改下面这一段】↓↓↓
"""

# ============ 改这里就够了 ============
TITLE   = "STATIC / BLOOM"          # 大标题（英文更像杂志；中文也行）
BODY    = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
           "eiusmod tempor incididunt ut labore et dolore magna aliqua. "
           "Risus commodo viverra maecenas accumsan lacus vel facilisis.")  # 正文，随便写多长，自动换行
AUTHOR  = "your name"               # 署名
DATE    = "Jul 2026"                # 日期
NUMBER  = "N°01"                    # 右上角小编号
THEME   = "暗"                      # "暗" = 墨绿暗调 ；"亮" = 奶粉亮调
# ====================================


# ---------- 下面不用看也能用 ----------
import sys, os, subprocess, math

# 自动安装 Pillow（第一次运行会联网装，装好后就不再装）
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
except ImportError:
    print("正在为你自动安装图像库 Pillow，请稍候……")
    subprocess.call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

W, H = 1080, 1440
LIME = (190, 240, 44)
MAG  = (232, 30, 140)

THEMES = {
    "暗": dict(BG_TL=(60, 68, 46), BG_BR=(20, 26, 17), INK=(236, 238, 230),
              BODY=(198, 204, 186), CRED=(206, 208, 196), EDGE=(12, 16, 10), VIG=0.12),
    "亮": dict(BG_TL=(240, 226, 224), BG_BR=(214, 196, 199), INK=(36, 32, 38),
              BODY=(96, 88, 92), CRED=(72, 66, 70), EDGE=(150, 138, 140), VIG=0.04),
}

def find_font(cands, size):
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FBOLD = [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\Arialbd.ttf",
         "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
         "/Library/Fonts/Arial Bold.ttf"]
FREG  = [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\Arial.ttf",
         "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]

def gradient(size, c1, c2):
    w, h = size
    base = Image.new("RGB", size, c1); top = Image.new("RGB", size, c2)
    mask = Image.new("L", size); md = mask.load(); maxd = w + h
    for y in range(h):
        for x in range(w):
            md[x, y] = int(255 * (x + y) / maxd)
    return Image.composite(top, base, mask)

def cover(img, tw, th, bias_y=0.28):
    iw, ih = img.size
    s = max(tw / iw, th / ih)
    nw, nh = int(math.ceil(iw * s)), int(math.ceil(ih * s))
    im = img.resize((nw, nh), Image.LANCZOS)
    return im.crop((int((nw-tw)*0.5), int((nh-th)*bias_y),
                    int((nw-tw)*0.5)+tw, int((nh-th)*bias_y)+th))

def wrap(draw, text, fnt, max_w):
    """把一段文字按宽度自动折行"""
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines[:6]

def _prism(layer, cx0, cy0, angle, length, width, colors):
    a = math.radians(angle); dx, dy = math.cos(a), math.sin(a); px, py = -dy, dx
    L, Wd = length/2, width/2
    pts = [(cx0+dx*L, cy0+dy*L), (cx0+dx*L*0.55+px*Wd, cy0+dy*L*0.55+py*Wd),
           (cx0-dx*L*0.55+px*Wd, cy0-dy*L*0.55+py*Wd), (cx0-dx*L, cy0-dy*L),
           (cx0-dx*L*0.55-px*Wd, cy0-dy*L*0.55-py*Wd), (cx0+dx*L*0.55-px*Wd, cy0+dy*L*0.55-py*Wd)]
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

def build(src_path):
    T = THEMES.get(THEME, THEMES["暗"])
    canvas = gradient((W, H), T["BG_TL"], T["BG_BR"])
    vig = Image.new("L", (W, H), 0); ImageDraw.Draw(vig).ellipse(
        [-W*0.3, -H*0.2, W*1.3, H*1.2], fill=40)
    vig = vig.filter(ImageFilter.GaussianBlur(200))
    canvas = Image.composite(canvas, Image.new("RGB", (W, H), (0, 0, 0)),
             ImageChops.invert(vig).point(lambda p: 255 - int(p*T["VIG"]))).convert("RGB")
    draw = ImageDraw.Draw(canvas)

    ML, MR = 138, W - 130
    title_f = find_font(FBOLD, 46); body_f = find_font(FREG, 21)
    cred_f = find_font(FREG, 22); tag_f = find_font(FBOLD, 16)

    ty = 150
    draw.text((ML, ty), TITLE, font=title_f, fill=T["INK"])
    tb = draw.textbbox((ML, ty), TITLE, font=title_f)
    draw.rectangle([ML, tb[3]+12, ML+92, tb[3]+16], fill=MAG)

    by = tb[3] + 34
    for ln in wrap(draw, BODY, body_f, MR - ML):
        draw.text((ML, by), ln, font=body_f, fill=T["BODY"]); by += 30

    gx, gy = ML, by + 34
    gw, gh = MR - ML, H - (by + 34) - 168
    cg, rg = 16, 16
    colW = (gw - 2*cg) / 3.0
    cx = [gx, gx + colW + cg, gx + 2*(colW + cg)]; wideW = 2*colW + cg
    usable = gh - 3*rg; bh = [usable*f for f in (0.19, 0.19, 0.19, 0.43)]
    band_y = []; yy = gy
    for h in bh: band_y.append(yy); yy += h + rg
    tiles = [(cx[c], band_y[0], colW, bh[0]) for c in range(3)]
    tiles += [(cx[0], band_y[1], wideW, bh[1]), (cx[2], band_y[1], colW, bh[1])]
    tiles += [(cx[0], band_y[2], wideW, bh[2]), (cx[2], band_y[2], colW, bh[2])]
    tiles += [(cx[c], band_y[3], colW, bh[3]) for c in range(3)]

    src = Image.open(src_path).convert("RGB")
    grid_img = cover(src, int(round(gw)), int(round(gh)))

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(shadow)
    for (tx, tyy, tw, th) in tiles:
        sd.rectangle([int(tx)+6, int(tyy)+8, int(tx+tw)+6, int(tyy+th)+8], fill=(0, 0, 0, 80))
    canvas.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0),
                 shadow.filter(ImageFilter.GaussianBlur(9)).split()[3].point(lambda p: int(p*0.5)))
    draw = ImageDraw.Draw(canvas)

    for (tx, tyy, tw, th) in tiles:
        sx, sy = int(round(tx-gx)), int(round(tyy-gy))
        itw, ith = int(round(tw)), int(round(th))
        canvas.paste(grid_img.crop((sx, sy, sx+itw, sy+ith)), (int(round(tx)), int(round(tyy))))
        draw.rectangle([int(round(tx)), int(round(tyy)),
                        int(round(tx+tw))-1, int(round(tyy+th))-1], outline=T["EDGE"], width=1)

    cyu = H - 128
    for i, line in enumerate([f"create · {DATE}", "", "create by", AUTHOR]):
        draw.text((ML, cyu + i*26 + (14 if i >= 2 else 0)), line, font=cred_f, fill=T["CRED"])
    draw.text((MR - 54, 150), NUMBER, font=tag_f, fill=LIME)

    orn = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ocx, ocy = W - 118, H - 132
    ImageDraw.Draw(glow).ellipse([ocx-170, ocy-170, ocx+170, ocy+170], fill=(140, 225, 130, 55))
    orn = Image.alpha_composite(orn, glow.filter(ImageFilter.GaussianBlur(70)))
    _prism(orn, ocx, ocy, 62, 430, 116, [(120,235,150),(120,215,245),(240,244,250),(232,60,150)])
    _prism(orn, ocx, ocy, -28, 340, 92, [(120,215,245),(240,244,250),(150,235,150),(232,60,150)])
    canvas = Image.alpha_composite(canvas.convert("RGBA"), orn).convert("RGB")

    out = os.path.splitext(src_path)[0] + "_海报.png"
    canvas.save(out, quality=95)
    return out

def pick_image():
    exts = (".jpg", ".jpeg", ".png", ".webp", ".bmp")
    # 1) 拖拽 / 命令行传入
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        return sys.argv[1]
    # 2) 脚本同目录里第一张图（排除自己生成的 _海报.png）
    here = os.path.dirname(os.path.abspath(__file__))
    imgs = [os.path.join(here, f) for f in os.listdir(here)
            if f.lower().endswith(exts) and not f.lower().endswith("_海报.png")]
    if imgs:
        return sorted(imgs, key=os.path.getmtime, reverse=True)[0]
    # 3) 手动粘路径
    p = input("把图片文件拖进这个窗口，或粘贴图片完整路径，然后回车：\n").strip().strip('"')
    return p if os.path.isfile(p) else None

if __name__ == "__main__":
    try:
        src = pick_image()
        if not src:
            print("没找到图片。把图片和这个脚本放一起，或拖到 .bat 上再试。")
        else:
            print("正在生成，用图：", src)
            out = build(src)
            print("\n[完成] 成品已存到：\n", out)
    except Exception as e:
        print("\n[出错] ", e)
        print("常见原因：图片路径含特殊字符 / 图片损坏。把图片换个简单英文名再试。")
    input("\n按回车键关闭窗口。")
