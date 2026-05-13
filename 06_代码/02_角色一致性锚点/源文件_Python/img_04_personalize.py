"""图 04/08 账号级锚点：personalize × moodboard 双柱（多层阴影 + 边缘羽化）"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/04_personalize.png'
SRC_P = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/账号级锚点/personalize_2257points.png'
SRC_M = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/账号级锚点/moodboard_清冷古风.png'

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 5, total=9)
d = ImageDraw.Draw(c)

# eyebrow
f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'Account-level anchor — Tier I', font=f_eb, fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(34)
d.text((100, 215), '账号级锚点 · 第一层金字塔', font=f_eb_cn, fill=C_INK_SOFT, anchor='la')

# 主标
f_main = font_han(48)
draw_text(d, (W//2, 280), '不是一条腿，是两条腿', f_main, fill=C_INK_SOFT,
          anchor='ma', heavy=False, stroke_width=0)
f_main_en = font_lora(24, italic=True, weight='medium')
d.text((W//2, 348), 'personalize × moodboard',
       font=f_main_en, fill=C_GRAY, anchor='ma')

# 双柱
mid_x = W // 2
cell_w = 480
gap = 60
left_x = mid_x - gap//2 - cell_w
right_x = mid_x + gap // 2

d.line([(mid_x, 410), (mid_x, 1390)], fill=C_GRAY_2, width=1)

# 列名
f_col = font_lora(46, italic=True, weight='semibold')
d.text((left_x + cell_w//2, 425), 'personalize', font=f_col,
       fill=C_INK_SOFT, anchor='ma')
d.text((right_x + cell_w//2, 425), 'moodboard', font=f_col,
       fill=C_INK_SOFT, anchor='ma')
f_col_cn = font_han(24)
d.text((left_x + cell_w//2, 480), '矫正 · 中西方审美偏差',
       font=f_col_cn, fill=C_ACCENT, anchor='ma')
d.text((right_x + cell_w//2, 480), '矫正 · 个体审美差异性',
       font=f_col_cn, fill=C_ACCENT, anchor='ma')

# ===== 卡片：多层柔影 + 边缘羽化 =====
def card_with_padding(src_path, max_w, max_h, pad=14, bg=C_HIGH):
    src = Image.open(src_path).convert('RGBA')
    sw, sh = src.size
    inner_w = max_w - pad*2
    inner_h = max_h - pad*2
    ratio = min(inner_w / sw, inner_h / sh)
    nw, nh = int(sw * ratio), int(sh * ratio)
    src = src.resize((nw, nh), Image.LANCZOS)
    card = Image.new('RGBA', (nw + pad*2, nh + pad*2), bg + (255,))
    card.alpha_composite(src, (pad, pad))
    # 边缘羽化（关键：让卡片边软掉）
    card = soften_edges(card, radius=2)
    return card

def composite_card_soft(canvas, card, cx, cy):
    """多层阴影 + 卡片合成"""
    cw, ch = card.size
    px = cx - cw // 2
    py = cy - ch // 2
    # 多层柔影
    sh_img, pad = soft_shadow_layered(cw, ch,
        layers=[(8, 28, 1, 2),    # 接触阴影：极柔
                (35, 18, 3, 8),   # 中层柔影
                (90, 14, 6, 18)]) # 远层环境阴影：大羽化
    canvas.alpha_composite(sh_img, (px - pad, py - pad))
    canvas.alpha_composite(card, (px, py))
    return (px, py, cw, ch)

card_max_w = 460
card_max_h = 320
card_y = 535 + card_max_h // 2

card_p = card_with_padding(SRC_P, card_max_w, card_max_h, pad=12, bg=C_HIGH)
composite_card_soft(c, card_p, left_x + cell_w // 2, card_y)

card_m = card_with_padding(SRC_M, card_max_w, card_max_h, pad=18, bg=C_HIGH)
composite_card_soft(c, card_m, right_x + cell_w // 2, card_y)

# 大数字
f_num = font_lora(120, weight='semibold')
y_num = 945
d.text((left_x + cell_w//2, y_num), '2257', font=f_num,
       fill=C_INK_SOFT, anchor='mt')
d.text((right_x + cell_w//2, y_num), '8', font=f_num,
       fill=C_INK_SOFT, anchor='mt')
f_num_lbl = font_lora(22, italic=True, weight='medium')
d.text((left_x + cell_w//2, y_num + 130), 'data points',
       font=f_num_lbl, fill=C_GRAY, anchor='mt')
d.text((right_x + cell_w//2, y_num + 130), 'reference images',
       font=f_num_lbl, fill=C_GRAY, anchor='mt')

# 短句
f_phrase = font_han(22)
d.text((left_x + cell_w//2, 1130),
       '— 让 AI 学会"我属于谁"', font=f_phrase, fill=C_GRAY, anchor='ma')
d.text((right_x + cell_w//2, 1130),
       '— 告诉 AI"这就是我要的感觉"', font=f_phrase, fill=C_GRAY, anchor='ma')

# 底部金句
f_b1 = font_han(34)
y_b = 1450
draw_text(d, (W//2, y_b), 'personalize 锁审美方向', f_b1, fill=C_GRAY, anchor='ma')
draw_text(d, (W//2, y_b + 50), 'moodboard 锁审美质感', f_b1, fill=C_GRAY, anchor='ma')

m = magnolia_brush(size=70, color=C_ACCENT, alpha=160)
c.alpha_composite(m, (90, 250))

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
