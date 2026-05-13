"""图 05/08 oref 五场景一致性长条"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/05_oref.png'
ROOT = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/方法A_oref/5场景一致性测试'
IMGS = [
    f'{ROOT}/雪夜窗下倚柱.png',
    f'{ROOT}/春樱树下侧脸仰望.png',
    f'{ROOT}/红叶古寺石阶.png',
    f'{ROOT}/灯笼夜行v2.png',
    f'{ROOT}/月下抚琴.png',
]
LABELS = ['雪夜', '春樱', '红叶', '灯笼', '月下']

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 6, total=9)
d = ImageDraw.Draw(c)

# eyebrow
f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'oref — Tier III · the apex', font=f_eb, fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(36)
d.text((100, 218), 'oref · 金字塔顶层', font=f_eb_cn, fill=C_INK_SOFT, anchor='la',
       stroke_width=0, stroke_fill=C_INK)

# ---- 中部主文 ----
f_main = font_han(38)
y_main = 290
draw_text(d, (W//2, y_main), '她的脸 = 她的生物身份', f_main,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
f_main_en = font_lora(24, italic=True, weight='medium')
d.text((W//2, y_main + 70), 'her face — her biometric identity',
       font=f_main_en, fill=C_GRAY, anchor='ma')

# ---- 5 张图横向排列：每张约 220×293 (3:4) ----
n = 5
gap = 8
total_w_avail = W - 100*2 - gap*(n-1)
cell_w = total_w_avail // n   # ≈ 209
cell_h = int(cell_w * 4 / 3)  # 278
y_strip = 460
x_start = 100

for i, p in enumerate(IMGS):
    x = x_start + i * (cell_w + gap)
    place_image(c, p, (x, y_strip, cell_w, cell_h), fit='cover')
    d.rectangle([x-1, y_strip-1, x+cell_w, y_strip+cell_h], outline=C_INK, width=1)
    # 场景标签
    f_lab = font_han(24)
    d.text((x + cell_w//2, y_strip + cell_h + 22), LABELS[i],
           font=f_lab, fill=C_INK_SOFT, anchor='ma')

# ---- 底部金句 ----
y_strip_end = y_strip + cell_h + 60
# 大金句
f_big = font_han(48)
y_big = y_strip_end + 80
draw_text(d, (W//2, y_big), '5 个完全不同的场景', f_big,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
# 暖橘点缀
f_em = font_han(48)
draw_text(d, (W//2, y_big + 76), '同一个人', f_em,
          fill=C_ACCENT, anchor='ma', heavy=False, stroke_width=0)

# 装饰玉兰
m = magnolia_brush(size=80, color=C_ACCENT, alpha=160)
c.alpha_composite(m, (90, 250))

# 装饰横线
ly = y_big + 195
d.line([(W//2 - 60, ly), (W//2 + 60, ly)], fill=C_INK_SOFT, width=1)
f_foot = font_lora(24, italic=True, weight='medium')
d.text((W//2, ly + 24), 'Five scenes. One face.',
       font=f_foot, fill=C_GRAY, anchor='ma')

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
