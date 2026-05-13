"""图 06/08 seed · 金字塔中层"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/06_seed.png'
ROOT = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/方法B_seed'
IMGS = [
    f'{ROOT}/方法B_微调1_表情.png',
    f'{ROOT}/方法B_微调2_服装.png',
    f'{ROOT}/方法B_微调3_光线.png',
    f'{ROOT}/方法B_微调4_视线.png',
]
LABELS = ['微调表情', '微调服装', '微调光线', '微调视线']

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 7, total=9)
d = ImageDraw.Draw(c)

f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'seed — Tier II · the middle', font=f_eb,
       fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(36)
d.text((100, 218), 'seed · 金字塔中层', font=f_eb_cn, fill=C_INK_SOFT, anchor='la',
       stroke_width=0, stroke_fill=C_INK)

f_main = font_han(36)
y_main = 285
draw_text(d, (W//2, y_main), '她的构图 = 同一帧的不同瞬间', f_main,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
f_main_en = font_lora(24, italic=True, weight='medium')
d.text((W//2, y_main + 65), 'her composition — moments within one frame',
       font=f_main_en, fill=C_GRAY, anchor='ma')

# 2×2 网格 (缩小 4 张图)
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

# 数据：94% / 11% — 紧凑放在网格下
y_data = grid_y + cell_h*2 + gap + 40
f_pct = font_lora(70, weight='semibold')
f_pct_pc = font_lora(40, weight='bold')
f_pct_lbl = font_han(22)

# 左
xL = W//2 - 200
d.text((xL, y_data), '94', font=f_pct, fill=C_INK_SOFT, anchor='mm',
       stroke_width=0, stroke_fill=C_INK)
d.text((xL + 70, y_data - 6), '%', font=f_pct_pc, fill=C_INK_SOFT, anchor='lm')
d.text((xL + 10, y_data + 60), '构图相似', font=f_pct_lbl, fill=C_GRAY, anchor='ma')

# 右
xR = W//2 + 200
d.text((xR, y_data), '11', font=f_pct, fill=C_ACCENT, anchor='mm',
       stroke_width=0, stroke_fill=C_ACCENT)
d.text((xR + 60, y_data - 6), '%', font=f_pct_pc, fill=C_ACCENT, anchor='lm')
d.text((xR + 10, y_data + 60), '微调执行', font=f_pct_lbl, fill=C_GRAY, anchor='ma')

d.line([(W//2, y_data - 38), (W//2, y_data + 38)], fill=C_INK_SOFT, width=1)

# 底部金句
f_bot = font_han(28)
d.text((W//2, y_data + 130),
       'seed 不让你"微调"，seed 让你"复刻"',
       font=f_bot, fill=C_INK_SOFT, anchor='ma',
       stroke_width=0, stroke_fill=C_INK)

# 装饰玉兰
m = magnolia_brush(size=70, color=C_ACCENT, alpha=160)
c.alpha_composite(m, (90, 250))

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
