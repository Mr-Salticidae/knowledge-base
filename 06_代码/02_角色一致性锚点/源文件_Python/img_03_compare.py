"""图 03/08 失败组对比：A 组（无 personalize）vs B 组（有 personalize）"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/03_compare.png'
ROOT = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/失败组'
A = [f'{ROOT}/A组_1.png', f'{ROOT}/A组_3.png', f'{ROOT}/A组_5.png']
B = [f'{ROOT}/B组_1.png', f'{ROOT}/B组_3.png', f'{ROOT}/B组_5.png']

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 4, total=9)
d = ImageDraw.Draw(c)

# eyebrow
f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'Side-by-side comparison', font=f_eb, fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(34)
d.text((100, 215), '账号级锚点 · 一秒看出差异', font=f_eb_cn, fill=C_INK_SOFT, anchor='la')

# ---- 对称布局：左右两列以画面中线对称 ----
mid_x = W // 2
cell_w = 290        # 每张图宽
inner_gap = 80      # 中线两侧的间隙总宽
# 左列右端 = mid_x - inner_gap/2
left_x = mid_x - inner_gap // 2 - cell_w   # 291
right_x = mid_x + inner_gap // 2            # 661
# 整体水平外边距：W - (right_x + cell_w) == left_x ⇒ 1242 - 951 = 291 ✓ 对称

# 中央分隔线（柔细）
d.line([(mid_x, 280), (mid_x, 1320)], fill=C_INK_SOFT, width=1)

# 列标题（柔灰，不加粗）
f_col = font_han(36)
d.text((left_x + cell_w//2, 290), '不开 personalize',
       font=f_col, fill=C_INK_SOFT, anchor='ma')
d.text((right_x + cell_w//2, 290), '开 personalize',
       font=f_col, fill=C_INK_SOFT, anchor='ma')
f_col_en = font_lora(22, italic=True, weight='medium')
d.text((left_x + cell_w//2, 340), 'training set defaults',
       font=f_col_en, fill=C_GRAY, anchor='ma')
d.text((right_x + cell_w//2, 340), 'my own taste, learned',
       font=f_col_en, fill=C_GRAY, anchor='ma')

# 6 张缩图：每列 3 张，cell_w=290，cell_h 为 3:4 = 387
start_y = 380
cell_h = 290  # 改为正方近似 3:3 让纵向更紧凑
gap_y = 12

# 计算总高，确保不超出 1310
# 3 张 + 2 间隙 = 3*cell_h + 2*gap_y
total_h = 3 * cell_h + 2 * gap_y  # = 894
# start_y + total_h ≤ 1310 ⇒ start_y ≤ 416；目前 380 ✓

for i, p in enumerate(A):
    y = start_y + i * (cell_h + gap_y)
    place_image(c, p, (left_x, y, cell_w, cell_h), fit='cover')
    d.rectangle([left_x-1, y-1, left_x + cell_w, y + cell_h],
                outline=C_INK_SOFT, width=1)

for i, p in enumerate(B):
    y = start_y + i * (cell_h + gap_y)
    place_image(c, p, (right_x, y, cell_w, cell_h), fit='cover')
    d.rectangle([right_x-1, y-1, right_x + cell_w, y + cell_h],
                outline=C_INK_SOFT, width=1)

# 列底注（紧贴图组下方，对称居中到列中点）
note_y = start_y + total_h + 30  # ≈ 1304
f_note = font_han(24)
d.text((left_x + cell_w//2, note_y), '"复古东方美人"',
       font=f_note, fill=C_GRAY, anchor='ma')
d.text((left_x + cell_w//2, note_y + 32), '训练集里的旧想象',
       font=f_note, fill=C_GRAY, anchor='ma')
d.text((right_x + cell_w//2, note_y), '"当代东方审美"',
       font=f_note, fill=C_GRAY, anchor='ma')
d.text((right_x + cell_w//2, note_y + 32), '我的 personalize 学到的',
       font=f_note, fill=C_GRAY, anchor='ma')

# 底部金句（细宋体）
f_bottom = font_han(34)
d.text((W//2, note_y + 110), '但 — 都不是同一个人',
       font=f_bottom, fill=C_INK_SOFT, anchor='ma')

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT,
      'left=', left_x, 'right=', right_x,
      'left_to_mid=', mid_x - (left_x + cell_w),
      'right_to_mid=', right_x - mid_x)
