"""图 02. 檐下，她是谁 — 角色卡（基于真实角色设定）"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/02_protagonist.png'
SRC = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/基准图.png'

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 2, total=9)
d = ImageDraw.Draw(c)

# eyebrow
f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'The protagonist — character sheet',
       font=f_eb, fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(34)
d.text((100, 215), '写在前面 · 角色卡',
       font=f_eb_cn, fill=C_INK_SOFT, anchor='la')

# 主标：檐下 + 是谁
# 用大字"檐下"作为名号，下面跟"，是谁。"
f_name = font_han(110)
y_name = 285
draw_text(d, (W//2, y_name), '檐下，是谁。', f_name, fill=C_INK_SOFT,
          anchor='ma', heavy=False, stroke_width=0)

# 副标
f_sub_en = font_lora(28, italic=True, weight='medium')
d.text((W//2, y_name + 130), 'Meet her, before we lose her.',
       font=f_sub_en, fill=C_GRAY, anchor='ma')

# ---- 主图：基准图（卡片化 + 柔阴影） ----
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
    return soften_edges(card, radius=2)

def composite_card_soft(canvas, card, cx, cy):
    cw, ch = card.size
    px = cx - cw // 2
    py = cy - ch // 2
    sh_img, pad = soft_shadow_layered(cw, ch,
        layers=[(8, 28, 1, 2), (35, 18, 3, 8), (90, 14, 6, 18)])
    canvas.alpha_composite(sh_img, (px - pad, py - pad))
    canvas.alpha_composite(card, (px, py))
    return px, py, cw, ch

img_w, img_h = 540, 720
img_x_center = 350  # 左侧
img_y = 530
card = card_with_padding(SRC, img_w, img_h, pad=14, bg=C_HIGH)
px, py, cw, ch = composite_card_soft(c, card, img_x_center, img_y + card.height // 2)

# ---- 右侧 6 个真实角色卡标签 ----
# 格式："字 · 描述" + 英文注
labels = [
    ('名',  '檐下',     'eaves — under the cold roof'),
    ('脸',  '鹅蛋瓷白', 'oval face, porcelain skin'),
    ('眼',  '杏仁丹凤', 'almond-shaped, downturned'),
    ('唇',  '裸粉樱桃', 'matte nude-pink cherry'),
    ('簪',  '白玉兰',   'magnolia — IP signature'),
    ('衣',  '烟白汉服', 'ming hanfu, ink-wash ivory'),
]

label_x = px + cw + 50
y_start = py + 5
gap_y = 110

f_lab_key = font_lora(22, italic=True, weight='semibold')
f_lab_cn  = font_han(34)
f_lab_en  = font_lora(18, italic=True, weight='medium')

for i, (key, cn, en) in enumerate(labels):
    yt = y_start + i * gap_y
    # 暖橘小竖线作为分隔
    d.line([(label_x, yt + 6), (label_x, yt + 65)], fill=C_ACCENT, width=2)
    # 一字key
    d.text((label_x + 16, yt), key + '.', font=f_lab_key, fill=C_ACCENT, anchor='la')
    # 中文描述
    d.text((label_x + 16, yt + 26), cn, font=f_lab_cn, fill=C_INK_SOFT, anchor='la')
    # 英文注释
    d.text((label_x + 16, yt + 72), en, font=f_lab_en, fill=C_GRAY, anchor='la')

# ---- 底部 footnote：玉兰 IP 实测说明 ----
foot_y = py + ch + 50
# 上方一条短装饰线
d.line([(W//2 - 60, foot_y - 16), (W//2 + 60, foot_y - 16)],
       fill=C_GRAY_2, width=1)

f_foot_cn = font_han(24)
f_foot_em = font_han(26)
d.text((W//2, foot_y + 6),
       '— 玉兰，是 AI 在 personalize 训练里"投票"选出的视觉签名',
       font=f_foot_cn, fill=C_GRAY, anchor='ma')
draw_text(d, (W//2, foot_y + 50),
       '从此她叫「檐下」', f_foot_em, fill=C_INK_SOFT, anchor='ma')

# 装饰玉兰（强化"玉兰即签名"）
m1 = magnolia_brush(size=68, color=C_ACCENT, alpha=170)
c.alpha_composite(m1, (90, 250))
m2 = magnolia_silhouette(size=180, color=C_ACCENT, alpha=45)
c.alpha_composite(m2, (W - 220, 1180))

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
