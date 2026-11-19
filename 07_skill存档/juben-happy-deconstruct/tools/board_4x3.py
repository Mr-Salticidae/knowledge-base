# -*- coding: utf-8 -*-
"""现场白板 · 4:3 横幅样板（《草台班子》实跑版，换本只改两处）

用法：
    python board_4x3.py --out 09_白板现场版_4x3.html --title "本名 · 白板现场版"

换本：
    1. 改 NODES（六个框：先写表层身份，真身放在 body，第五幕才补）
    2. 改 edges()（每支箭头 = 一条 line + 一个名词 label；标签放在自己那条线上方）
    3. 打印：chrome --headless --print-to-pdf   （不要用 paint-order="stroke" 描边，见 SKILL.md 雷区）
"""
import argparse
import io
import os

W, H = 280, 210          # 4:3

BOX_W, BOX_H = 48, 30
NODES = {
    "qigai":     dict(cn="乞丐", body="皇帝", x=76,  y=50),
    "zhuangshi": dict(cn="状师", body="太后", x=204, y=50),
    "xianling":  dict(cn="县令", body="县令", x=76,  y=108),
    "laoban":    dict(cn="老板", body="状元", x=204, y=108),
    "bukuai":    dict(cn="捕快", body="侍卫", x=76,  y=166),
    "shiye":     dict(cn="师爷", body="总管", x=204, y=166),
}

INK = "#111"
GREY = "#8e8e8e"
FONT = "'Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(n):
    d = NODES[n]
    x, y = d["x"] - BOX_W / 2, d["y"] - BOX_H / 2
    return "".join([
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{BOX_W}" height="{BOX_H}" rx="2.6" '
        f'fill="#fff" stroke="{INK}" stroke-width="1.05"/>',
        f'<text x="{d["x"]}" y="{d["y"]+1.0:.1f}" text-anchor="middle" font-size="12.8" '
        f'font-weight="700" fill="{INK}" font-family="{FONT}" letter-spacing="0.8">'
        f'{esc(d["cn"])}</text>',
        f'<text x="{d["x"]}" y="{d["y"]+11.4:.1f}" text-anchor="middle" font-size="7.0" '
        f'fill="{GREY}" font-family="{FONT}" letter-spacing="1.6">'
        f'{esc(d["body"])}</text>',
    ])


def label(x, y, txt, size=7.6, anchor="middle", fill=INK, bold=True):
    w = "700" if bold else "400"
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{w}" fill="{fill}" font-family="{FONT}" '
            f'letter-spacing="0.4">{esc(txt)}</text>')


def line(x1, y1, x2, y2, width=0.95):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{INK}" stroke-width="{width}" stroke-linecap="round" '
            f'marker-end="url(#ar)"/>')


def edges():
    s = []
    L, R = 76, 204
    LT, RT = L + BOX_W / 2, R - BOX_W / 2      # 100 / 180
    MID = (LT + RT) / 2                        # 140

    # 1 乞丐 → 县令（竖，盐）
    s.append(line(L, 65, L, 92.6))
    s.append(label(L + 5.8, 80, "盐", anchor="start"))

    # 2 捕快 → 县令（竖，502）
    s.append(line(L, 151, L, 123.4))
    s.append(label(L + 5.8, 139, "502", anchor="start"))

    # 3 乞丐 ⇄ 状师（横，上下两条各挂一个词）
    s.append(line(LT, 42, RT, 42))             # 乞丐 → 状师：包子
    s.append(line(RT, 58, LT, 58))             # 状师 → 乞丐：苦瓜汁
    s.append(label(MID, 38.4, "包子"))
    s.append(label(MID, 54.6, "苦瓜汁"))

    # 4 县令 → 老板（横，榴莲壳）
    s.append(line(LT, 108, RT, 108))
    s.append(label(MID, 104.2, "榴莲壳"))

    # 5 老板 → 捕快（斜，香蕉）
    s.append(line(180, 118.9, 100, 155.1))
    s.append(label(170, 148, "香蕉"))

    # 6 捕快 ⇄ 师爷（横，上下两条）
    s.append(line(LT, 158.5, RT, 158.5))       # 捕快 → 师爷：胡椒粉
    s.append(line(RT, 173.5, LT, 173.5))       # 师爷 → 捕快：辣根
    s.append(label(MID, 155.2, "胡椒粉"))
    s.append(label(MID, 170.2, "辣根"))
    return "".join(s)


def build():
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}mm" height="{H}mm">',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="5.8" markerHeight="5.8" orient="auto-start-reverse">'
         f'<path d="M1,1.1 L9.3,5 L1,8.9 z" fill="{INK}"/></marker></defs>',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']

    # 顶栏
    g.append(label(13, 18, "草台班子", size=10.5, anchor="start"))
    g.append(label(W - 13, 18, "白板 · 现场版", size=6.6, anchor="end",
                   bold=False, fill=GREY))
    g.append(label(13, 26.6, "先六个框  →  问出一个连一条  →  第五幕补灰字",
                   size=5.2, anchor="start", bold=False, fill="#8a8a8a"))

    g.append(edges())
    for n in NODES:
        g.append(box(n))

    # 底栏
    g.append(f'<line x1="13" y1="193" x2="{W-13}" y2="193" '
             f'stroke="#dedede" stroke-width="0.45"/>')
    g.append(label(13, 199.4, "箭头指向受害者；同段两支＝互相加害",
                   size=5.8, anchor="start", bold=False, fill="#5a5a5a"))
    g.append(label(W - 13, 199.4, "灰字＝第五幕才补",
                   size=5.8, anchor="end", bold=False, fill="#5a5a5a"))
    g.append('</svg>')
    return "".join(g)


HTML = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{ size: {w}mm {h}mm; margin: 0; }}
  html, body {{ margin:0; padding:0; background:#fff; }}
  .page {{ width:{w}mm; height:{h}mm; background:#fff; overflow:hidden; }}
  .page svg {{ width:100%; height:100%; display:block; }}
  @media screen {{ body {{ padding:14px; background:#e9edef; }}
    .page {{ margin:0 auto; box-shadow:0 3px 18px rgba(0,0,0,.16); }} }}
</style></head>
<body><div class="page">{svg}</div></body></html>
"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="board_4x3.html")
    ap.add_argument("--title", default="白板现场版（4:3）")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(HTML.format(w=W, h=H, svg=build(), title=args.title))
    print("written:", out)
