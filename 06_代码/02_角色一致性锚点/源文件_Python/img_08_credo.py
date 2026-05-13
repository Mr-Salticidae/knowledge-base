"""图 08/08 灵魂金句收尾页"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/08_credo.png'

c = new_canvas()
d = ImageDraw.Draw(c)
apply_chrome(c, 9, total=9)
d = ImageDraw.Draw(c)

# eyebrow
f_eb = font_lora(28, italic=True, weight='medium')
d.text((100, 178), 'Final words — written at the eaves',
       font=f_eb, fill=C_ACCENT, anchor='la')
f_eb_cn = font_han(34)
d.text((100, 218), '写在最后', font=f_eb_cn, fill=C_INK_SOFT, anchor='la')

# 第一段：不要选方法 / 要叠方法
f_top = font_han(50)
y_t = 320
draw_text(d, (W//2, y_t), '不要选方法', f_top, fill=C_INK_SOFT, anchor='ma',
          heavy=False, stroke_width=0)
draw_text(d, (W//2, y_t + 72), '要叠方法', f_top, fill=C_ACCENT, anchor='ma',
          heavy=False, stroke_width=0)

# 第二段
f_mid = font_han(34)
y_m = y_t + 220
d.text((W//2, y_m), '不要找最稳的工具', font=f_mid, fill=C_INK_SOFT, anchor='ma')
d.text((W//2, y_m + 56), '要先想清楚你要锁什么', font=f_mid, fill=C_INK_SOFT, anchor='ma')

# 分隔线
ly = y_m + 130
d.line([(W//2 - 200, ly), (W//2 + 200, ly)], fill=C_INK_SOFT, width=1)

# 三层分类：脸 · 构图 · 签名
f_three = font_han(30)
y_three = ly + 40
parts = ['脸', '构图', '签名']
gap = 100
# 测量 + 居中布
total_w = sum(f_three.getbbox(t)[2] - f_three.getbbox(t)[0] for t in parts) + gap*2
xx = (W - total_w) // 2
for i, t in enumerate(parts):
    bbox = f_three.getbbox(t)
    w = bbox[2] - bbox[0]
    color = C_INK
    d.text((xx + w//2, y_three), t, font=f_three, fill=color, anchor='ma',
           stroke_width=0, stroke_fill=color)
    xx += w
    if i < 2:
        # 暖橘色 ·
        f_dot = font_han(32)
        d.text((xx + gap//2, y_three + 4), '·',
               font=f_dot, fill=C_ACCENT, anchor='ma')
        xx += gap

# 引用块：玉不琢
f_quo = font_han(34)
f_quo2 = font_han(30)
y_q = y_three + 120
draw_text(d, (W//2, y_q), '玉不琢，不成器', f_quo, fill=C_INK_SOFT, anchor='ma',
          heavy=False, stroke_width=0)
d.text((W//2, y_q + 70), '但雕琢之前，你得先知道',
       font=f_quo2, fill=C_GRAY, anchor='ma')
d.text((W//2, y_q + 110), '你要从这块玉里看见什么',
       font=f_quo2, fill=C_GRAY, anchor='ma')

# 引用左右两侧的小修饰
f_q_en = font_lora(32, italic=True, weight='medium')
d.text((W//2, y_q - 60),
       'Jade, unhewn, can never be a vessel —',
       font=f_q_en, fill=C_GRAY_2, anchor='ma')

# 最终：工具是术 / 知道自己要什么 / 是道
f_final = font_han(58)
y_f = y_q + 220
draw_text(d, (W//2, y_f), '工具是术', f_final, fill=C_INK_SOFT, anchor='ma',
          heavy=False, stroke_width=0)
draw_text(d, (W//2, y_f + 82), '知道自己要什么', f_final, fill=C_INK_SOFT, anchor='ma',
          heavy=False, stroke_width=0)
f_final2 = font_han(58)
draw_text(d, (W//2, y_f + 170), '是道', f_final2, fill=C_ACCENT, anchor='ma',
          heavy=False, stroke_width=0)

# 装饰：左下/右上 玉兰小簇
m1 = magnolia_silhouette(size=240, color=C_ACCENT, alpha=55)
c.alpha_composite(m1, (60, 720))
m2 = magnolia_brush(size=110, color=C_ACCENT, alpha=200)
c.alpha_composite(m2, (W - 180, 240))

# 印章和落款已在 chrome
c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT)
