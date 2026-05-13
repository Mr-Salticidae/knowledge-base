"""设计工具模块 — 9 张轮播图统一调性"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math, random
import numpy as np

# 画布
W, H = 1242, 1656
DPI = 300

# 配色
C_BG       = (242, 235, 224)
C_BG_2     = (168, 179, 191)
C_HIGH     = (250, 248, 242)
C_ACCENT   = (201, 124,  93)
C_INK      = ( 44,  44,  44)
C_INK_SOFT = ( 70,  70,  70)
C_GRAY     = ( 90,  90,  90)
C_GRAY_2   = (140, 140, 140)

# 字体路径
F_HAN_REG = '/sessions/practical-eloquent-hopper/.local/lib/python3.10/site-packages/mplfonts/fonts/SourceHanSerifSC-Regular.otf'
F_HAN_NTSF = '/sessions/practical-eloquent-hopper/.local/lib/python3.10/site-packages/mplfonts/fonts/NotoSerifCJKsc-Regular.otf'
F_LORA_VAR = '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'
F_LORA_IT_VAR = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'

def font_han(size, heavy=False):
    path = F_HAN_NTSF if heavy else F_HAN_REG
    return ImageFont.truetype(path, size)

def font_lora(size, italic=False, weight='regular'):
    path = F_LORA_IT_VAR if italic else F_LORA_VAR
    f = ImageFont.truetype(path, size)
    try:
        wmap = {'regular': 400, 'medium': 500, 'semibold': 600, 'bold': 700}
        f.set_variation_by_axes([wmap.get(weight, 400)])
    except Exception:
        pass
    return f

def draw_text(draw, xy, text, font, fill=C_INK, anchor='la',
              heavy=False, stroke_width=0, stroke_fill=None,
              align='left', spacing=4):
    if heavy and stroke_width == 0:
        stroke_width = max(1, int(font.size * 0.012))
        stroke_fill = stroke_fill or fill
    draw.text(xy, text, font=font, fill=fill, anchor=anchor,
              stroke_width=stroke_width, stroke_fill=stroke_fill,
              align=align, spacing=spacing)

def text_size(font, text, stroke_width=0):
    bbox = font.getbbox(text, stroke_width=stroke_width)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def magnolia_brush(size=120, color=C_ACCENT, alpha=180):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    petal_color = color + (alpha,)
    for k in range(5):
        ang = math.radians(-90 + k * 72)
        pw, ph = size * 0.34, size * 0.50
        ox = cx + math.cos(ang) * size * 0.20
        oy = cy + math.sin(ang) * size * 0.20
        petal = Image.new('RGBA', (int(pw * 1.5), int(ph * 1.5)), (0, 0, 0, 0))
        pd = ImageDraw.Draw(petal)
        pd.ellipse([petal.size[0]//2 - pw/2, petal.size[1]//2 - ph/2,
                    petal.size[0]//2 + pw/2, petal.size[1]//2 + ph/2],
                   outline=petal_color, width=max(2, int(size*0.018)))
        petal = petal.rotate(math.degrees(ang) + 90, resample=Image.BICUBIC)
        img.alpha_composite(petal, (int(ox - petal.size[0]//2), int(oy - petal.size[1]//2)))
    rr = int(size * 0.06)
    d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=color + (alpha,))
    return img

def magnolia_silhouette(size=300, color=C_ACCENT, alpha=70):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    cx, cy = size // 2, size // 2
    fill = color + (alpha,)
    for k in range(5):
        ang = math.radians(-90 + k * 72 + random.uniform(-4, 4))
        pw, ph = size * 0.40, size * 0.62
        ox = cx + math.cos(ang) * size * 0.18
        oy = cy + math.sin(ang) * size * 0.18
        petal = Image.new('RGBA', (int(pw * 1.6), int(ph * 1.6)), (0, 0, 0, 0))
        pd = ImageDraw.Draw(petal)
        pd.ellipse([petal.size[0]//2 - pw/2, petal.size[1]//2 - ph/2,
                    petal.size[0]//2 + pw/2, petal.size[1]//2 + ph/2],
                   fill=fill)
        petal = petal.rotate(math.degrees(ang) + 90, resample=Image.BICUBIC)
        img.alpha_composite(petal, (int(ox - petal.size[0]//2), int(oy - petal.size[1]//2)))
    img = img.filter(ImageFilter.GaussianBlur(radius=size*0.012))
    return img

def stamp(text='跳蛛先生 · 檐下', scale=1.0):
    w = int(220 * scale)
    h = int(85 * scale)
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    sr = (180, 80, 60, 230)
    pad = 7
    d.rectangle([pad, pad, w - pad, h - pad], outline=sr, width=int(3 * scale))
    f = font_han(int(28 * scale))
    d.text((w//2, h//2), text, font=f, fill=sr, anchor='mm')
    return img

def draw_falling_leaf(canvas, xy, size=80, rot=0):
    leaf = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(leaf)
    d.polygon([(size//2, 4),
               (size - 6, size//2),
               (size//2, size - 4),
               (6, size//2)], fill=C_ACCENT + (200,))
    d.line([(size//2, 4), (size//2, size - 4)], fill=C_INK + (130,), width=2)
    leaf = leaf.rotate(rot, resample=Image.BICUBIC)
    canvas.alpha_composite(leaf, xy)

def new_canvas(bg=C_BG):
    return Image.new('RGBA', (W, H), bg + (255,))

def add_grain(img, intensity=3):
    arr = np.array(img.convert('RGB')).astype('int16')
    noise = np.random.randint(-intensity, intensity + 1, arr.shape, dtype='int16')
    arr = np.clip(arr + noise, 0, 255).astype('uint8')
    return Image.fromarray(arr).convert('RGBA')

def soft_shadow(box_w, box_h, blur=24, alpha=60):
    img = Image.new('RGBA', (box_w + blur*2, box_h + blur*2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([blur, blur, blur+box_w, blur+box_h], fill=(0, 0, 0, alpha))
    img = img.filter(ImageFilter.GaussianBlur(blur))
    return img

def apply_chrome(canvas, num, total=8):
    """统一应用顶栏、章节标记、印章、落款"""
    d = ImageDraw.Draw(canvas)
    f_vol_en = font_lora(28, italic=True, weight='medium')
    en_txt = 'VOL.02   //   AESTHETIC ANCHOR   //   '
    d.text((100, 90), en_txt, font=f_vol_en, fill=C_GRAY, anchor='la')
    en_w = f_vol_en.getbbox(en_txt)[2]
    f_vol_cn = font_han(26)
    d.text((100 + en_w, 94), '檐下', font=f_vol_cn, fill=C_GRAY, anchor='la')
    d.line([(100, 138), (W - 100, 138)], fill=C_INK, width=1)
    # 章节标记：小字 italic，与 VOL 同行右端，呼应文学感
    f_chap = font_lora(30, italic=True, weight='medium')
    d.text((W - 100, 96), f'No. {num:02d} of {total:02d}',
           font=f_chap, fill=C_GRAY, anchor='ra')
    s = stamp(scale=1.0)
    canvas.alpha_composite(s, (W - s.width - 60, H - s.height - 50))
    f_foot = font_lora(22, italic=True, weight='regular')
    d.text((100, H - 78), 'Spider Mr. — under the eaves',
           font=f_foot, fill=C_GRAY, anchor='la')
    return canvas

def place_image(canvas, src_path, box, fit='contain'):
    src = Image.open(src_path).convert('RGBA')
    bx, by, bw, bh = box
    sw, sh = src.size
    if fit == 'contain':
        ratio = min(bw / sw, bh / sh)
    else:
        ratio = max(bw / sw, bh / sh)
    nw, nh = int(sw * ratio), int(sh * ratio)
    src = src.resize((nw, nh), Image.LANCZOS)
    if fit == 'cover':
        left = (nw - bw) // 2
        top = (nh - bh) // 2
        src = src.crop((left, top, left + bw, top + bh))
        nw, nh = bw, bh
    px = bx + (bw - nw) // 2
    py = by + (bh - nh) // 2
    sh_img = soft_shadow(nw, nh, blur=20, alpha=50)
    canvas.alpha_composite(sh_img, (px - 20, py - 12))
    canvas.alpha_composite(src, (px, py))
    return (px, py, nw, nh)


def soft_shadow_layered(box_w, box_h, layers=None, pad=None):
    """多层柔影：每层 (blur, alpha, dx, dy)。返回带 padding 的 RGBA + 推荐贴附偏移"""
    if layers is None:
        # 近层接触阴影 + 远层环境阴影
        layers = [(10, 35, 1, 3), (60, 22, 4, 12)]
    max_blur = max(l[0] for l in layers)
    max_d = max(max(abs(l[2]), abs(l[3])) for l in layers)
    if pad is None:
        pad = max_blur + max_d + 8
    img = Image.new('RGBA', (box_w + pad*2, box_h + pad*2), (0, 0, 0, 0))
    for blur, alpha, dx, dy in layers:
        layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rectangle([pad + dx, pad + dy,
                      pad + dx + box_w, pad + dy + box_h],
                     fill=(0, 0, 0, alpha))
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img.alpha_composite(layer)
    return img, pad


def soften_edges(rgba, radius=2):
    """对 RGBA 图做边缘 alpha 羽化（让卡片边自然过渡）"""
    if rgba.mode != 'RGBA':
        rgba = rgba.convert('RGBA')
    r, g, b, a = rgba.split()
    a = a.filter(ImageFilter.GaussianBlur(radius))
    return Image.merge('RGBA', (r, g, b, a))
