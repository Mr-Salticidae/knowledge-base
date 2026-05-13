"""图 02/08 痛点开篇：每一张都是另一个人 — 用 4 张失败图拼图体现"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/02_pain.png'
ROOT = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/失败组'
# 用 B 组 4 张：每张都很美，但都不是同一个人 → 痛点
IMGS = [
    f'{ROOT}/B组_1.png',
    f'{ROOT}/B组_2.png',
    f'{ROOT}/B组_3.png',
    f'{ROOT}/B组_4.png',
]
# 假名标签，强化"每张是不同的人"
LABELS = ['是她？', '是她？', '是她？', '还是她？']

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 3, total=9)
d = ImageDraw.Draw(c)

# eyebrow
f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'The pain point — opening', font=f_eb, fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(34)
d.text((100, 215), '你的 AI 画的"她"', font=f_eb_cn, fill=C_INK_SOFT, anchor='la')

# ---- 中央痛点大字 ----
f_main = font_han(68)
y_main = 290
draw_text(d, (W//2, y_main), '每一张都很美', f_main, fill=C_GRAY,
          anchor='ma', heavy=False, stroke_width=0)
draw_text(d, (W//2, y_main + 80), '但每一张都是另一个人', f_main, fill=C_INK_SOFT,
          anchor='ma', heavy=False, stroke_width=0)

# ---- 2×2 网格：4 张失败图 ----
grid_y = 480
cell_w = 410
cell_h = 410
gap = 18
total_grid_w = cell_w*2 + gap
grid_x = (W - total_grid_w) // 2

# 朱砂色（与印章同源），用作"不一致"的标识色
RED = (180, 80, 60)

for i, p in enumerate(IMGS):
    row, col = divmod(i, 2)
    x = grid_x + col * (cell_w + gap)
    y = grid_y + row * (cell_h + gap)
    place_image(c, p, (x, y, cell_w, cell_h), fit='cover')
    # 朱砂细边（强化"问题"感，但不刺眼）
    d.rectangle([x-2, y-2, x+cell_w+1, y+cell_h+1], outline=RED, width=2)

    # 在每张图右上角加"虚线小圆"+假名标签，暗示"这是不同的人"
    label = LABELS[i]
    f_lab = font_han(24)
    # 半透明白底标签
    label_box_w, label_box_h = 130, 38
    lbx = x + cell_w - label_box_w - 10
    lby = y + 10
    overlay = Image.new('RGBA', (label_box_w, label_box_h), (250, 248, 242, 230))
    c.alpha_composite(overlay, (lbx, lby))
    # 边框朱砂
    dd = ImageDraw.Draw(c)
    dd.rectangle([lbx, lby, lbx + label_box_w - 1, lby + label_box_h - 1],
                 outline=RED, width=1)
    dd.text((lbx + label_box_w//2, lby + label_box_h//2 + 1),
            label, font=f_lab, fill=RED, anchor='mm')

# ---- 中央叠加："？" 大问号（朱砂半透） ----
# 用一个大 ? 透明叠在网格中央，强化困惑感
qx, qy = W//2, grid_y + cell_h + gap//2
# 简单方式：用 Lora 大问号
f_q = font_lora(180, italic=True, weight='semibold')
qmark_overlay = Image.new('RGBA', (220, 240), (0, 0, 0, 0))
qd = ImageDraw.Draw(qmark_overlay)
qd.text((110, 120), '?', font=f_q, fill=RED + (140,), anchor='mm')
# 加柔影
qmark_overlay = qmark_overlay.filter(ImageFilter.GaussianBlur(radius=1))
c.alpha_composite(qmark_overlay, (qx - 110, qy - 120))

# ---- 底部金句 ----
y_bottom = grid_y + cell_h*2 + gap + 50
f_bottom = font_han(40)
draw_text(d, (W//2, y_bottom), '想做一个 IP 角色？', f_bottom,
          fill=C_GRAY, anchor='ma')
draw_text(d, (W//2, y_bottom + 60), '——你连"她"是谁，都没锁住', f_bottom,
          fill=C_INK_SOFT, anchor='ma')

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
