# -*- coding: utf-8 -*-
"""生成「对话」小红书知识卡片(3:4 双卡)。"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "2026-06-12_对话甲骨文二进制_原图.png")
FONTS = r"C:/Windows/Fonts"

W, H = 1080, 1440
MARGIN = 88

# 配色:全部从原图色域里取,克制
BG       = (244, 238, 230)   # 暖象牙
INK      = (47, 45, 42)      # 主墨
MUTED    = (140, 132, 121)   # 次级灰
HAIR     = (213, 203, 190)   # 细线
C_NARR   = (46, 139, 115)    # 叙事核心 · 青
C_STYLE  = (106, 111, 181)   # 风格基底 · 长春花
C_TRANS  = (198, 138, 51)    # 软过渡 · 金
C_NEG    = (191, 86, 56)     # 负面词 · 陶土红

def font(name, size, index=0):
    return ImageFont.truetype(os.path.join(FONTS, name), size, index=index)

# 字体
def msyh(s):   return font("msyh.ttc", s)
def msyhb(s):  return font("msyhbd.ttc", s)
def deng(s):   return font("Dengl.ttf", s)
def dengb(s):  return font("Dengb.ttf", s)
def mono(s):   return font("consola.ttf", s)
def monob(s):  return font("consolab.ttf", s)

def text_tracking(d, xy, s, fnt, fill, tracking=0, anchor_center=None):
    """带字距绘制;anchor_center=总宽度则居中。"""
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
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=radius, fill=255)
    im.putalpha(mask)
    return im

def place_image(canvas, box_w, top, radius=18, border=HAIR):
    src = Image.open(SRC).convert("RGB")
    ratio = src.size[1] / src.size[0]
    box_h = int(box_w * ratio)
    src = src.resize((box_w, box_h), Image.LANCZOS)
    src = rounded_img(src, radius)
    x = (W - box_w) // 2
    # 细边框
    bd = ImageDraw.Draw(canvas)
    bd.rounded_rectangle([x-1, top-1, x+box_w+1, top+box_h+1], radius=radius+1,
                         outline=border, width=2)
    canvas.paste(src, (x, top), src)
    return top + box_h

# ---------- 划线 prompt 渲染 ----------
def draw_annotated(d, segments, x0, y0, max_w, fnt, line_h, ul_dy=8, ul_w=4):
    """segments: [(text, color|None)]。逐词排版,同段同行连续下划线。"""
    space_w = d.textlength(" ", font=fnt)
    tokens = []  # (word, color, seg)
    for seg, (txt, col) in enumerate(segments):
        for wi, word in enumerate(txt.split(" ")):
            if word == "":
                continue
            tokens.append((word, col, seg))
    x, y = x0, y0
    prev = None  # (end_x, y, color, seg)
    for word, col, seg in tokens:
        ww = d.textlength(word, font=fnt)
        if x > x0 and x + ww > x0 + max_w:
            x = x0
            y += line_h
            prev = None
        # 段内同行:补上空格处的下划线
        if prev and prev[1] == y and prev[3] == seg and col is not None:
            d.line([(prev[0], y + fnt.size + ul_dy), (x, y + fnt.size + ul_dy)],
                   fill=col, width=ul_w)
        d.text((x, y), word, font=fnt, fill=INK)
        if col is not None:
            d.line([(x, y + fnt.size + ul_dy), (x + ww, y + fnt.size + ul_dy)],
                   fill=col, width=ul_w)
        prev = (x + ww, y, col, seg)
        x += ww + space_w
    return y + line_h

def series_tag(d, y, fsize=28, line_len=70):
    """系列刊头:两侧细线 + 居中系列名。"""
    label = "目标是成为 PROMPT 大师"
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

# ============================================================
# 卡片 1 · 封面
# ============================================================
def card_cover(path):
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)

    series_tag(d, 92)
    img_bottom = place_image(c, box_w=W - MARGIN*2, top=172, radius=20)

    # 主标题《对话》
    ty = img_bottom + 94
    title_f = msyhb(140)
    text_tracking(d, (0, ty), "《对话》", title_f, INK, tracking=10, anchor_center=W)

    # 四色短线(题意:四层)
    ly = ty + 196
    seg_w, gap = 84, 14
    total = seg_w*4 + gap*3
    sx = (W - total) // 2
    for col in (C_NARR, C_STYLE, C_TRANS, C_NEG):
        d.rounded_rectangle([sx, ly, sx+seg_w, ly+7], radius=3, fill=col)
        sx += seg_w + gap

    # 副标题
    sy = ly + 56
    text_tracking(d, (0, sy), "甲骨刻痕  ⟷  二进制", dengb(46), INK,
                  tracking=4, anchor_center=W)
    sy2 = sy + 74
    text_tracking(d, (0, sy2), "相隔三千年的同一个动作 —— 书写", deng(34), MUTED,
                  tracking=2, anchor_center=W)

    # 底注:留空,只保留一条克制的居中细线收尾
    d.line([(W//2-44, H-118), (W//2+44, H-118)], fill=HAIR, width=2)

    c.save(path, quality=95)
    print("saved", path)

# ============================================================
# 卡片 2 · prompt 四层拆解
# ============================================================
def card_breakdown(path):
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)

    series_tag(d, 64, fsize=24, line_len=56)
    # 标题
    d.text((MARGIN, 122), "《对话》· prompt 拆解", font=msyhb(50), fill=INK)
    d.text((MARGIN, 192), "四层标注 · 哪些动了,哪些没动", font=deng(30), fill=MUTED)

    # 小图
    img_bottom = place_image(c, box_w=520, top=252, radius=16)

    # 图例
    ly = img_bottom + 42
    legend = [("叙事核心 · 三轮没动", C_NARR), ("风格基底 · 整组置换", C_STYLE),
              ("软过渡 · 收尾关键", C_TRANS), ("负面词 · 逐版疫苗", C_NEG)]
    col_x = [MARGIN, W//2 + 10]
    lf = msyh(26)
    for i, (lab, col) in enumerate(legend):
        cx = col_x[i % 2]
        cy = ly + (i // 2) * 48
        d.line([(cx, cy+17), (cx+38, cy+17)], fill=col, width=6)
        d.text((cx+52, cy), lab, font=lf, fill=INK)

    # prompt
    pf = mono(21)
    py = ly + 116
    segments = [
        ("one continuous conceptual editorial illustration,", C_STYLE),
        (" a dialogue between two eras of writing,", C_NARR),
        (" on the left an ancient robed scribe carving oracle bone script into a turtle shell with a bone stylus,", C_NARR),
        (" on the right a modern figure typing on a keyboard with binary digits drifting above the monitor,", C_NARR),
        (" the two figures facing each other within the same shared room,", C_NARR),
        (" warm pastel terracotta tones on the left melting gradually into cool periwinkle and lavender tones on the right,", C_TRANS),
        (" soft gradient color transition with no hard dividing line,", C_TRANS),
        (" a cloud of glowing oracle characters and binary digits floating between them,", C_NARR),
        (" the glyph cloud gently bridging and blending the two color worlds,", C_TRANS),
        (" clean isometric perspective, flat color blocks, thin precise linework, controlled detail density, polished editorial article style, minimal background", C_STYLE),
        (" --no ", None),
        ("watermark, logo, blurry, low quality,", C_NEG),
        (" photorealistic, 3d render,", C_NEG),
        (" hard split line, frame border", C_NEG),
    ]
    end_y = draw_annotated(d, segments, MARGIN, py, W - MARGIN*2, pf, line_h=38, ul_dy=7, ul_w=3)

    # 底注心法
    d.line([(MARGIN, H-128), (W-MARGIN, H-128)], fill=HAIR, width=2)
    d.text((MARGIN, H-104), "心法", font=msyhb(28), fill=C_TRANS)
    d.text((MARGIN, H-62), "概念对但不美 → 冻结叙事核心,整组置换风格基底",
           font=msyh(28), fill=INK)

    c.save(path, quality=95)
    print("saved", path, "prompt_end_y=", end_y)

card_cover(os.path.join(HERE, "2026-06-12_对话_小红书卡片_01封面.png"))
card_breakdown(os.path.join(HERE, "2026-06-12_对话_小红书卡片_02拆解.png"))
