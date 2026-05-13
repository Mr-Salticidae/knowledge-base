"""封面 A 案：我让 MJ 画粉樱，它给了我白玉兰"""
import sys
sys.path.insert(0, '/sessions/practical-eloquent-hopper/mnt/outputs')
from design_kit import *

OUT = '/sessions/practical-eloquent-hopper/mnt/outputs/01_cover_A.png'
SRC = '/sessions/practical-eloquent-hopper/mnt/02_角色一致性锚点/素材图/方法A_oref/5场景一致性测试/春樱树下侧脸仰望.png'

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
# ---- 主标题 ----
f_title = font_han(108)
title_y = 215
draw_text(d, (W//2, title_y), '我让 MJ 画粉樱', f_title,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)
draw_text(d, (W//2, title_y + 124), '它给了我白玉兰', f_title,
          fill=C_INK_SOFT, anchor='ma', heavy=False, stroke_width=0)

# ---- 主图 620×827 (3:4) ----
img_w, img_h = 620, 827
img_x = (W - img_w) // 2
img_y = 525
place_image(c, SRC, (img_x, img_y, img_w, img_h), fit='cover')
d.rectangle([img_x-2, img_y-2, img_x+img_w+1, img_y+img_h+1],
            outline=C_INK, width=1)
img_bottom = img_y + img_h  # 1352

# ---- 副标 ----
f_subtitle = font_han(38)
f_subtitle_en = font_lora(28, italic=True, weight='medium')
sub_y_en = img_bottom + 32   # 1384
sub_y_cn = sub_y_en + 44      # 1428
d.text((W//2, sub_y_en),
       'oref · seed · description — three layers of one face',
       font=f_subtitle_en, fill=C_GRAY_2, anchor='ma')
d.text((W//2, sub_y_cn), '审美锚点 02 · 角色一致性的金字塔',
       font=f_subtitle, fill=C_GRAY, anchor='ma')

# 装饰横线
line_y = sub_y_cn + 60   # 1488
d.line([(W//2 - 70, line_y), (W//2 + 70, line_y)], fill=C_ACCENT, width=2)

# ---- 装饰玉兰 ----
m = magnolia_brush(size=110, color=C_ACCENT, alpha=200)
c.alpha_composite(m, (88, 165))
draw_falling_leaf(c, (img_x + 14, img_y + img_h - 60), size=36, rot=18)
draw_falling_leaf(c, (img_x + img_w - 50, img_y + 24), size=32, rot=-25)

# ---- 底部：左侧落款 / 右侧印章，最底部 ----
s = stamp(text='跳蛛先生 · 檐下', scale=1.4)
stamp_y = H - s.height - 38     # 印章下沉到最底
c.alpha_composite(s, (W - s.width - 90, stamp_y))

f_foot = font_lora(22, italic=True, weight='regular')
d.text((100, H - 60), 'Spider Mr. — under the eaves',
       font=f_foot, fill=C_GRAY, anchor='la')

c = add_grain(c, intensity=3)
c.convert('RGB').save(OUT, quality=95, dpi=(DPI, DPI))
print('saved:', OUT, 'img_bottom=', img_bottom, 'stamp_y=', stamp_y)
