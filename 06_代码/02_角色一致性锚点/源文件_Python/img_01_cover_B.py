"""封面 B 案：oref · seed · 描述词 / 不是三选一 / 是三层金字塔"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/01_cover_B.png'
SRC = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/方法A_oref/5场景一致性测试/灯笼夜行v2.png'

c = new_canvas()
d = ImageDraw.Draw(c)

# ---- 顶部 VOL ----
f_vol_en = font_lora(28, italic=True, weight='medium')
en_txt = 'VOL.02   //   AESTHETIC ANCHOR   //   '
d.text((100, 90), en_txt, font=f_vol_en, fill=C_GRAY, anchor='la')
en_w = f_vol_en.getbbox(en_txt)[2]
f_top_cn = font_han(26)
d.text((100 + en_w, 94), '檐下 · 跳蛛先生 · 角色一致性的金字塔', font=f_top_cn, fill=C_GRAY, anchor='la')
d.line([(100, 138), (W - 100, 138)], fill=C_INK_SOFT, width=1)

# ---- 主标顶 eyebrow：oref · seed · 描述词（中英混排） ----
# 用统一的字号和位置，把混排做正
f_brow = font_han(46)
f_brow_en = font_lora(46, weight='semibold')
y_brow = 200
# 准备文字测量后水平居中
parts = [('oref', f_brow_en),
         (' · ', f_brow_en),
         ('seed', f_brow_en),
         (' · ', f_brow_en),
         ('描述词', f_brow)]
total_w = sum(p[1].getbbox(p[0])[2] - p[1].getbbox(p[0])[0] for p in parts)
x = (W - total_w) // 2
for txt, ff in parts:
    bbox = ff.getbbox(txt)
    d.text((x, y_brow), txt, font=ff, fill=C_ACCENT, anchor='la')
    x += bbox[2] - bbox[0]

# ---- 主标 ----
f_t = font_han(96)
y1 = 290
y2 = y1 + 118
draw_text(d, (W//2, y1), '不是三选一', f_t,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
# 中央装饰小线
d.line([(W//2 - 24, y1 + 122), (W//2 + 24, y1 + 122)],
       fill=C_ACCENT, width=2)
draw_text(d, (W//2, y2), '是三层金字塔', f_t,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)

# ---- 主图 ----
img_w, img_h = 600, 800
img_x = (W - img_w) // 2
img_y = 615
place_image(c, SRC, (img_x, img_y, img_w, img_h), fit='cover')
d.rectangle([img_x-2, img_y-2, img_x+img_w+1, img_y+img_h+1],
            outline=C_INK, width=1)
img_bottom = img_y + img_h  # 1415

# ---- 副标 ----
f_sub = font_han(32)
f_sub_en = font_lora(24, italic=True, weight='medium')
d.text((W//2, img_bottom + 28), 'A pyramid of character consistency',
       font=f_sub_en, fill=C_GRAY_2, anchor='ma')
d.text((W//2, img_bottom + 64), '审美锚点 02 · 三种方法的真实分工',
       font=f_sub, fill=C_GRAY, anchor='ma')

# ---- 装饰 ----
m = magnolia_brush(size=98, color=C_ACCENT, alpha=200)
c.alpha_composite(m, (88, 175))
draw_falling_leaf(c, (img_x + 14, img_y + img_h - 56), size=34, rot=18)
draw_falling_leaf(c, (img_x + img_w - 46, img_y + 22), size=28, rot=-25)

# ---- 底部：印章靠最右下 / 落款最左下 ----
s = stamp(text='跳蛛先生 · 檐下', scale=1.35)
c.alpha_composite(s, (W - s.width - 80, H - s.height - 28))

f_foot = font_lora(22, italic=True, weight='regular')
d.text((100, H - 50), 'Spider Mr. — under the eaves',
       font=f_foot, fill=C_GRAY, anchor='la')

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
