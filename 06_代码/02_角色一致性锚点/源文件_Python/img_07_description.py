"""图 07/08 描述词锁定 · 金字塔底层"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/07_description.png'
ROOT = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/方法C_反推'
IMGS = [
    f'{ROOT}/方法C_C1_寺庙石阶.png',
    f'{ROOT}/方法C_C2_茶室独饮.png',
    f'{ROOT}/方法C_C3_山顶云海.png',
    f'{ROOT}/方法C_C4_雨巷回眸.png',
]
LABELS = ['寺庙石阶', '茶室独饮', '山顶云海', '雨巷回眸']

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 8, total=9)
d = ImageDraw.Draw(c)

f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'description — Tier I · the base', font=f_eb,
       fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(36)
d.text((100, 218), '描述词锁定 · 金字塔底层', font=f_eb_cn, fill=C_INK_SOFT,
       anchor='la', stroke_width=0, stroke_fill=C_INK)

f_main = font_han(36)
y_main = 285
draw_text(d, (W//2, y_main), '她的装扮 = 她的 IP 标识', f_main,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
f_main_en = font_lora(24, italic=True, weight='medium')
d.text((W//2, y_main + 65), 'her wardrobe — her IP signature',
       font=f_main_en, fill=C_GRAY, anchor='ma')

# 2×2 网格
grid_y = 405
cell_w = 410
cell_h = 410
gap = 18
total_grid_w = cell_w*2 + gap
grid_x = (W - total_grid_w) // 2

for i, p in enumerate(IMGS):
    row, col = divmod(i, 2)
    x = grid_x + col * (cell_w + gap)
    y = grid_y + row * (cell_h + gap)
    place_image(c, p, (x, y, cell_w, cell_h), fit='cover')
    d.rectangle([x-1, y-1, x+cell_w, y+cell_h], outline=C_INK, width=1)
    f_lab = font_han(22)
    label_box_w, label_box_h = 124, 32
    lbx = x + cell_w - label_box_w - 8
    lby = y + cell_h - label_box_h - 8
    overlay = Image.new('RGBA', (label_box_w, label_box_h), (242, 235, 224, 230))
    c.alpha_composite(overlay, (lbx, lby))
    d2 = ImageDraw.Draw(c)
    d2.text((lbx + label_box_w//2, lby + label_box_h//2 + 1),
            LABELS[i], font=f_lab, fill=C_INK_SOFT, anchor='mm')

# 主金句段
y_quote = grid_y + cell_h*2 + gap + 35
f_q1 = font_han(28)
draw_text(d, (W//2, y_quote), '4 张人脸不同，但都"穿同款"', f_q1,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
f_q2 = font_han(26)
d.text((W//2, y_quote + 60), '— 这就是 IP 角色的真相',
       font=f_q2, fill=C_ACCENT, anchor='ma')

# 底部小字
f_foot = font_han(24)
d.text((W//2, y_quote + 130),
       '路飞认草帽，蜘蛛侠认蛛网',
       font=f_foot, fill=C_GRAY, anchor='ma')

# 装饰
m = magnolia_brush(size=70, color=C_ACCENT, alpha=160)
c.alpha_composite(m, (90, 250))

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
