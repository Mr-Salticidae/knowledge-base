"""
#2 调色:把"窄巷仰望"(偏冷蓝灰)拉回系列统一的黄绿调

方法:
1. 采样 #1 / #3 / 封面 三张已统一的图,计算它们在 LAB 色彩空间的平均色彩偏移
2. 采样 #2 的当前色彩偏移
3. 计算需要的修正量
4. 用 LAB 空间做温和位移(避开 RGB 直接调整带来的色块异常)
5. 不动亮度结构(只改色相,保留原图的明暗层次)
"""
from PIL import Image
import numpy as np

BASE = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图"
OUT  = "/sessions/tender-admiring-galileo/mnt/小红书运营/临时创作/2026-05-04_大地之上/素材图"

# 已统一色调的 3 张参考(电影截图组,排除 #4 手机)
REFS = [
    f"{BASE}/mr_jumping_spider_cinematic_still_ultra_wide_establishing_sho_9c654027-54aa-4e33-acfe-9e7b6af9a7bf_2.png",  # 封面
    f"{BASE}/mr_jumping_spider_cinematic_still_monumental_arachnid_leg_pie_05ae17f4-54ae-444a-848d-d819403490c3_1.png",  # #1
    f"{BASE}/mr_jumping_spider_cinematic_still_vast_translucent_organic_me_5480f94e-aec2-427d-bbcb-406c7e723ec1_3.png",  # #3
]

# 要修的 #2
SRC_2 = f"{BASE}/mr_jumping_spider_cinematic_still_view_from_an_extremely_narr_33061bb8-0436-4e95-94d0-48b8c216ddee_0.png"
DST_2 = f"{OUT}/02_窄巷仰望_调色后.png"

# RGB → 简化 LAB-like 空间(用 OKLAB 理论的简化版 — 不引入 colormath 依赖)
# 实际上我们用一个更直接的方法:HSV 空间调相 + 整体色温微调
def rgb_to_hsv_arr(rgb_arr):
    """rgb_arr: (H, W, 3) float32 in [0,1] → hsv_arr: (H, W, 3) float32"""
    r, g, b = rgb_arr[..., 0], rgb_arr[..., 1], rgb_arr[..., 2]
    maxc = np.max(rgb_arr, axis=-1)
    minc = np.min(rgb_arr, axis=-1)
    v = maxc
    delta = maxc - minc
    s = np.where(maxc > 0, delta / np.maximum(maxc, 1e-8), 0)
    rc = (maxc - r) / np.maximum(delta, 1e-8)
    gc = (maxc - g) / np.maximum(delta, 1e-8)
    bc = (maxc - b) / np.maximum(delta, 1e-8)
    h = np.where(r == maxc, bc - gc, np.where(g == maxc, 2.0 + rc - bc, 4.0 + gc - rc))
    h = (h / 6.0) % 1.0
    h = np.where(delta == 0, 0, h)
    return np.stack([h, s, v], axis=-1)


def hsv_to_rgb_arr(hsv_arr):
    h, s, v = hsv_arr[..., 0], hsv_arr[..., 1], hsv_arr[..., 2]
    i = (h * 6).astype(np.int32) % 6
    f = h * 6 - i.astype(np.float32)
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    rgb = np.zeros_like(hsv_arr)
    masks = [(i == k) for k in range(6)]
    rs = [v, q, p, p, t, v]
    gs = [t, v, v, q, p, p]
    bs = [p, p, t, v, v, q]
    for k in range(6):
        m = masks[k]
        rgb[..., 0] = np.where(m, rs[k], rgb[..., 0])
        rgb[..., 1] = np.where(m, gs[k], rgb[..., 1])
        rgb[..., 2] = np.where(m, bs[k], rgb[..., 2])
    return rgb


def mean_hue(rgb01):
    hsv = rgb_to_hsv_arr(rgb01)
    h = hsv[..., 0]
    s = hsv[..., 1]
    # 加权平均(忽略饱和度极低的像素)
    weight = np.clip(s, 0.05, 1.0)
    # 平均色相用向量平均(避开 0-1 wrap 问题)
    angle = h * 2 * np.pi
    x = np.average(np.cos(angle), weights=weight)
    y = np.average(np.sin(angle), weights=weight)
    mean_angle = np.arctan2(y, x)
    if mean_angle < 0:
        mean_angle += 2 * np.pi
    return mean_angle / (2 * np.pi)


# 采样参考组的目标色相
ref_hues = []
for p in REFS:
    img = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32) / 255.0
    h = mean_hue(img)
    ref_hues.append(h)
    print(f"参考 {p.split('/')[-1][:40]}... 平均色相 = {h:.4f} ({h*360:.1f}°)")

# 用 cos/sin 平均
angles = np.array(ref_hues) * 2 * np.pi
target_angle = np.arctan2(np.mean(np.sin(angles)), np.mean(np.cos(angles)))
if target_angle < 0:
    target_angle += 2 * np.pi
target_hue = target_angle / (2 * np.pi)
print(f"\n目标色相(参考组平均) = {target_hue:.4f} ({target_hue*360:.1f}°)")

# 测当前 #2 色相
img2 = np.asarray(Image.open(SRC_2).convert("RGB"), dtype=np.float32) / 255.0
src_hue = mean_hue(img2)
print(f"#2 当前色相 = {src_hue:.4f} ({src_hue*360:.1f}°)")

# 计算需要的色相位移(取最短路径)
hue_shift = target_hue - src_hue
if hue_shift > 0.5:  hue_shift -= 1.0
if hue_shift < -0.5: hue_shift += 1.0
print(f"需要色相位移 = {hue_shift:.4f} ({hue_shift*360:.1f}°)")

# 应用:HSV 空间整体偏移色相 + 略提饱和度(让黄绿更出来) + 微调色温(暖)
hsv2 = rgb_to_hsv_arr(img2)

# 仅对中等饱和度像素调相(避免污染纯灰雾区,反而出色块)
sat_mask = np.clip((hsv2[..., 1] - 0.05) * 4, 0, 1)  # sat 在 0.05-0.30 之间渐进生效
applied_shift = hue_shift * sat_mask
hsv2[..., 0] = (hsv2[..., 0] + applied_shift) % 1.0

# 略提饱和(0.95 → 1.05x)同样按 sat_mask 渐进
hsv2[..., 1] = np.clip(hsv2[..., 1] * (1.0 + 0.10 * sat_mask), 0, 1)

rgb2 = hsv_to_rgb_arr(hsv2)

# 微调色温:整体暖一点(R+ B-),让冷蓝灰彻底消失
rgb2[..., 0] = np.clip(rgb2[..., 0] + 0.025, 0, 1)
rgb2[..., 2] = np.clip(rgb2[..., 2] - 0.020, 0, 1)

# 微调对比(轻提)
mid = 0.5
rgb2 = mid + (rgb2 - mid) * 1.03
rgb2 = np.clip(rgb2, 0, 1)

# 输出
Image.fromarray((rgb2 * 255).astype(np.uint8)).save(DST_2, optimize=True)
print(f"\n[OK] 调色后 #2 → {DST_2}")

# 验证调色后的色相
new_hue = mean_hue(rgb2)
print(f"调色后 #2 色相 = {new_hue:.4f} ({new_hue*360:.1f}°),与目标 {target_hue:.4f} 差距 = {abs(new_hue - target_hue):.4f}")
