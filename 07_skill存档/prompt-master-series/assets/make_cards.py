# -*- coding: utf-8 -*-
"""《目标是成为 Prompt 大师》系列 · 小红书双卡生成器(参数化)。

用法:把下方 CONFIG 改成本期内容,然后 `python make_cards.py`。
依赖:pip install Pillow;字体走 Windows 自带(微软雅黑 / 等线 / Consolas)。
产物:<out_prefix>_封面卡.png、<out_prefix>_prompt拆解卡.png(均 3:4 / 1080×1440)。

检查:脚本会打印 prompt_end_y,必须 < 页脚线(约 1290);溢出就把 PF 或 LINE_H 调小。
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# CONFIG —— 每期只改这里
# ============================================================
CONFIG = {
    "src_image":  "对话_原图.png",                 # 原图(相对本脚本)
    "out_dir":    ".",                              # 输出目录
    "out_prefix": "对话",                           # 输出文件名前缀
    "series_label": "目标是成为 PROMPT 大师",        # 系列刊头(全系列固定)
    "title":      "《对话》",                        # 主标题
    "cover_sub1": "甲骨刻痕 ⟷ 二进制",               # 封面副标题(强)
    "cover_sub2": "相隔三千年的同一个动作 —— 书写",   # 封面副标题(弱)
    "bd_title":   "《对话》· prompt 拆解",           # 拆解卡标题
    "bd_sub":     "四层标注 · 哪些动了,哪些没动",     # 拆解卡副标题
    "legend": [                                      # 四层图例:(文案, 层key)
        ("叙事核心 · 三轮没动", "narr"),
        ("风格基底 · 整组置换", "style"),
        ("软过渡 · 收尾关键",   "trans"),
        ("负面词 · 逐版疫苗",   "neg"),
    ],
    # prompt 分段:(文本, 层key 或 None)。None=不划线(如 --no)
    "segments": [
        ("one continuous conceptual editorial illustration,", "style"),
        (" a dialogue between two eras of writing,", "narr"),
        (" on the left an ancient robed scribe carving oracle bone script into a turtle shell with a bone stylus,", "narr"),
        (" on the right a modern figure typing on a keyboard with binary digits drifting above the monitor,", "narr"),
        (" the two figures facing each other within the same shared room,", "narr"),
        (" warm pastel terracotta tones on the left melting gradually into cool periwinkle and lavender tones on the right,", "trans"),
        (" soft gradient color transition with no hard dividing line,", "trans"),
        (" a cloud of glowing oracle characters and binary digits floating between them,", "narr"),
        (" the glyph cloud gently bridging and blending the two color worlds,", "trans"),
        (" clean isometric perspective, flat color blocks, thin precise linework, controlled detail density, polished editorial article style, minimal background", "style"),
        (" --no ", None),
        ("watermark, logo, blurry, low quality,", "neg"),
        (" photorealistic, 3d render,", "neg"),
        (" hard split line, frame border", "neg"),
    ],
    "footer_tag":  "心法",
    "footer_line": "概念对但不美 → 冻结叙事核心,整组置换风格基底",
}

# ============================================================
# 设计系统(全系列固定,一般不动)
# ============================================================
W, H = 1080, 1440
MARGIN = 88
BG    = (244, 238, 230)   # 暖象牙
INK   = (47, 45, 42)      # 主墨
MUTED = (140, 132, 121)   # 次灰
HAIR  = (213, 203, 190)   # 细线
LAYERS = {
    "narr":  (46, 139, 115),    # 叙事核心 · 青
    "style": (106, 111, 181),   # 风格基底 · 长春花
    "trans": (198, 138, 51),    # 软过渡 · 金
    "neg":   (191, 86, 56),     # 负面词 · 陶土红
}
PF = 21       # prompt 字号
LINE_H = 38   # prompt 行高

FONTS = r"C:/Windows/Fonts"
def _f(name, size): return ImageFont.truetype(os.path.join(FONTS, name), size)
def msyh(s):  return _f("msyh.ttc", s)
def msyhb(s): return _f("msyhbd.ttc", s)
def deng(s):  return _f("Dengl.ttf", s)
def dengb(s): return _f("Dengb.ttf", s)
def mono(s):  return _f("consola.ttf", s)

def text_tracking(d, xy, s, fnt, fill, tracking=0, anchor_center=None):
    x, y = xy
    widths = [d.textlength(ch, font=fnt) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1) if s else 0
    if anchor_center is not None:
        x = (anchor_center - total) / 2
    for ch, wch in zip(s, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += wch + tracking
    return total

def rounded_img(im, radius):
    im = im.convert("RGBA")
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=radius, fill=255)
    im.putalpha(mask)
    return im

def place_image(canvas, src_path, box_w, top, radius=18):
    src = Image.open(src_path).convert("RGB")
    box_h = int(box_w * src.size[1] / src.size[0])
    src = rounded_img(src.resize((box_w, box_h), Image.LANCZOS), radius)
    x = (W - box_w) // 2
    ImageDraw.Draw(canvas).rounded_rectangle(
        [x-1, top-1, x+box_w+1, top+box_h+1], radius=radius+1, outline=HAIR, width=2)
    canvas.paste(src, (x, top), src)
    return top + box_h

def series_tag(d, label, y, fsize=28, line_len=70):
    f = deng(fsize)
    tracking = 6
    widths = [d.textlength(ch, font=f) for ch in label]
    tw = sum(widths) + tracking * (len(label) - 1)
    gap = 22
    block = line_len + gap + tw + gap + line_len
    x = (W - block) / 2
    cy = y + fsize * 0.62
    d.line([(x, cy), (x + line_len, cy)], fill=HAIR, width=2)
    tx = x + line_len + gap
    for ch, wch in zip(label, widths):
        d.text((tx, y), ch, font=f, fill=MUTED)
        tx += wch + tracking
    rx = x + line_len + gap + tw + gap
    d.line([(rx, cy), (rx + line_len, cy)], fill=HAIR, width=2)

def draw_annotated(d, segments, x0, y0, max_w, fnt, line_h, ul_dy=7, ul_w=3):
    space_w = d.textlength(" ", font=fnt)
    tokens = []
    for seg, (txt, key) in enumerate(segments):
        col = LAYERS.get(key) if key else None
        for word in txt.split(" "):
            if word:
                tokens.append((word, col, seg))
    x, y = x0, y0
    prev = None
    for word, col, seg in tokens:
        ww = d.textlength(word, font=fnt)
        if x > x0 and x + ww > x0 + max_w:
            x, y, prev = x0, y + line_h, None
        if prev and prev[1] == y and prev[3] == seg and col is not None:
            d.line([(prev[0], y + fnt.size + ul_dy), (x, y + fnt.size + ul_dy)], fill=col, width=ul_w)
        d.text((x, y), word, font=fnt, fill=INK)
        if col is not None:
            d.line([(x, y + fnt.size + ul_dy), (x + ww, y + fnt.size + ul_dy)], fill=col, width=ul_w)
        prev = (x + ww, y, col, seg)
        x += ww + space_w
    return y + line_h

# ============================================================
def card_cover(cfg, path):
    c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
    series_tag(d, cfg["series_label"], 92)
    img_bottom = place_image(c, cfg["_src"], W - MARGIN*2, 172, radius=20)
    ty = img_bottom + 94
    text_tracking(d, (0, ty), cfg["title"], msyhb(140), INK, tracking=10, anchor_center=W)
    ly = ty + 196
    seg_w, gap = 84, 14
    sx = (W - (seg_w*4 + gap*3)) // 2
    for key in ("narr", "style", "trans", "neg"):
        d.rounded_rectangle([sx, ly, sx+seg_w, ly+7], radius=3, fill=LAYERS[key]); sx += seg_w + gap
    sy = ly + 56
    text_tracking(d, (0, sy), cfg["cover_sub1"], dengb(46), INK, tracking=4, anchor_center=W)
    text_tracking(d, (0, sy+74), cfg["cover_sub2"], deng(34), MUTED, tracking=2, anchor_center=W)
    d.line([(W//2-44, H-118), (W//2+44, H-118)], fill=HAIR, width=2)
    c.save(path, quality=95); print("saved", path)

def card_breakdown(cfg, path):
    c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
    series_tag(d, cfg["series_label"], 64, fsize=24, line_len=56)
    d.text((MARGIN, 122), cfg["bd_title"], font=msyhb(50), fill=INK)
    d.text((MARGIN, 192), cfg["bd_sub"], font=deng(30), fill=MUTED)
    img_bottom = place_image(c, cfg["_src"], 520, 252, radius=16)
    ly = img_bottom + 42
    col_x = [MARGIN, W//2 + 10]; lf = msyh(26)
    for i, (lab, key) in enumerate(cfg["legend"]):
        cx, cy = col_x[i % 2], ly + (i // 2) * 48
        d.line([(cx, cy+17), (cx+38, cy+17)], fill=LAYERS[key], width=6)
        d.text((cx+52, cy), lab, font=lf, fill=INK)
    end_y = draw_annotated(d, cfg["segments"], MARGIN, ly + 116, W - MARGIN*2, mono(PF), LINE_H)
    d.line([(MARGIN, H-128), (W-MARGIN, H-128)], fill=HAIR, width=2)
    d.text((MARGIN, H-104), cfg["footer_tag"], font=msyhb(28), fill=LAYERS["trans"])
    d.text((MARGIN, H-62), cfg["footer_line"], font=msyh(28), fill=INK)
    c.save(path, quality=95); print("saved", path, "prompt_end_y=", end_y, "(需 < 1290)")

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    cfg = dict(CONFIG)
    cfg["_src"] = os.path.join(here, cfg["src_image"])
    out = os.path.join(here, cfg["out_dir"])
    os.makedirs(out, exist_ok=True)
    card_cover(cfg, os.path.join(out, f"{cfg['out_prefix']}_封面卡.png"))
    card_breakdown(cfg, os.path.join(out, f"{cfg['out_prefix']}_prompt拆解卡.png"))

if __name__ == "__main__":
    main()
