# -*- coding: utf-8 -*-
"""过本单配图 · A4 横版关系图样板（《草台班子》实跑版，换本只改两处）

用法：
    python relation_a4.py --out 10_人物关系图.html --title "本名 · 六人关系图"

换本：
    1. 改 P（每人 = 名字 / 位置·演谁 / 真身 / 列 / 行）
    2. 改 build() 里的横杆与关系词（夫妻 / 情侣 / 父女 …）
    A4 横版 297x210mm，viewBox 单位 = mm。
"""
import argparse
import io
import os

W, H = 297, 210

CW, CH = 64, 38          # 卡片尺寸
X1, X2, X3 = 66, 148.5, 231
Y1, Y2 = 68, 143         # 两行卡片的中心 y

INK, GREY, FAINT = "#111", "#6a6a6a", "#9a9a9a"
ACC = "#8b1a1a"
FONT = "'Source Han Sans SC','Noto Sans SC','Microsoft YaHei',sans-serif"

# key: (名, 位置·演谁, 真身, 列, 行)
P = {
    "chang":  ("常长",   "大哥 · 演县令", "县令",  X1, Y1, True),
    "bao":    ("常包包", "二姐 · 演乞丐", "皇帝",  X2, Y1, False),
    "an":     ("常安全", "三弟 · 演捕快", "侍卫",  X3, Y1, False),
    "xiao":   ("常晓晓", "女儿 · 演师爷", "总管",  X1, Y2, False),
    "jiang":  ("蒋文明", "女婿 · 演老板", "状元",  X2, Y2, False),
    "li":     ("姜离",   "弟媳 · 演状师", "太后",  X3, Y2, False),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def txt(x, y, s, size, fill=INK, w="400", anchor="middle", ls="0.4"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{w}" fill="{fill}" font-family="{FONT}" '
            f'letter-spacing="{ls}">{esc(s)}</text>')


def card(key):
    name, pos, body, x, y, star = P[key]
    l, t = x - CW / 2, y - CH / 2
    s = [f'<rect x="{l:.1f}" y="{t:.1f}" width="{CW}" height="{CH}" rx="2.6" '
         f'fill="#fff" stroke="{INK}" stroke-width="1.0"/>']
    s.append(txt(x, y - 5.4, name, 14, INK, "700", ls="1.4"))
    s.append(txt(x, y + 4.2, pos, 7.2, GREY))
    s.append(f'<line x1="{l+7:.1f}" y1="{y+9.2:.1f}" x2="{l+CW-7:.1f}" y2="{y+9.2:.1f}" '
             f'stroke="#e4e4e4" stroke-width="0.4"/>')
    s.append(txt(l + 8, y + 15.4, "真身", 6.2, FAINT, "400", "start", "0.6"))
    s.append(txt(l + 23.6, y + 15.6, body, 8.0, INK, "700", "start", "1.2"))
    if star:
        s.append(txt(l + CW - 9, y + 15.2, "★", 7.0, ACC, "700", "end", "0"))
    return "".join(s)


def pill(x, y, s, size=7.4):
    w = len(s) * size + 7.5
    return "".join([
        f'<rect x="{x-w/2:.1f}" y="{y-3.9:.1f}" width="{w:.1f}" height="7.9" rx="3.9" '
        f'fill="#fff" stroke="#dcdcdc" stroke-width="0.45"/>',
        txt(x, y + 2.6, s, size, INK, "700", "middle", "0.6"),
    ])


def build():
    g = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'width="{W}mm" height="{H}mm">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']

    # ---- 页眉 ----
    g.append(txt(20, 19, "草台班子 · 六人关系图", 9.8, INK, "700", "start", "1.0"))
    g.append(txt(20, 26.4, "三兄妹一排，各自带来一个人；角色是随便分的",
                 6.4, GREY, "400", "start", "0.4"))
    g.append(txt(W - 20, 19, "三行读法：名字 ／ 位置·演谁 ／ 真身", 6.2, FAINT, "400", "end"))
    g.append(txt(W - 20, 26.4, "第六幕大戏前不许说", 6.2, ACC, "700", "end"))

    # ---- 兄妹横杆 ----
    g.append(f'<line x1="{X1}" y1="39" x2="{X3}" y2="39" stroke="{INK}" stroke-width="1.0"/>')
    for x in (X1, X2, X3):
        g.append(f'<line x1="{x}" y1="39" x2="{x}" y2="{Y1-CH/2}" stroke="{INK}" stroke-width="1.0"/>')
    g.append(txt(X2, 35.4, "一母同胞 · 兄妹", 6.8, INK, "700", "middle", "1.4"))

    # ---- 三对竖线 + 关系牌 ----
    for x, word in ((X1, "父女"), (X2, "夫妻"), (X3, "情侣")):
        g.append(f'<line x1="{x}" y1="{Y1+CH/2}" x2="{x}" y2="{Y2-CH/2}" '
                 f'stroke="{INK}" stroke-width="1.0"/>')
        g.append(pill(x, (Y1 + CH / 2 + Y2 - CH / 2) / 2, word))

    # ---- 闺蜜虚线（晓晓 ⇄ 姜离，走卡片下方）----
    g.append(f'<path d="M{X1},{Y2+CH/2} V176 H{X3} V{Y2+CH/2}" fill="none" '
             f'stroke="#9a9a9a" stroke-width="0.85" stroke-dasharray="3.2 2.6"/>')
    g.append(pill(X2, 176, "闺蜜", 6.8))

    # ---- 卡片 ----
    for k in P:
        g.append(card(k))

    # ---- 页脚 ----
    g.append(f'<line x1="20" y1="186" x2="{W-20}" y2="186" stroke="#ddd" stroke-width="0.4"/>')
    g.append(txt(20, 192.4, "叔侄：常安全 与 常晓晓（差一辈，岁数差不多）",
                 5.6, "#5a5a5a", "400", "start", "0.2"))
    g.append(txt(W - 20, 192.4, "★ 县令是全场唯一没反转的人", 5.6, ACC, "700", "end", "0.2"))
    g.append(txt(20, 198.4, "姜离既是常安全的女友，也是常晓晓的闺蜜——六人里唯一双重关系",
                 5.6, "#5a5a5a", "400", "start", "0.2"))
    g.append(txt(20, 204.4, "真身全称：皇帝 ／ 新科武状元 ／ 御前带刀侍卫 ／ 大内总管 ／ 皇太后",
                 5.4, FAINT, "400", "start", "0.2"))
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
    ap.add_argument("--out", default="relation_a4.html")
    ap.add_argument("--title", default="六人关系图")
    args = ap.parse_args()
    out = os.path.abspath(args.out)
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(HTML.format(w=W, h=H, svg=build(), title=args.title))
    print("written:", out)
