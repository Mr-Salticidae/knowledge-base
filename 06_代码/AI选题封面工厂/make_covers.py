# -*- coding: utf-8 -*-
"""
make_covers.py -- 按「对标·背景迭代」版式，把真实场景照片批量合成 960x600 大字封面。

版式来源：对标 65 张封面的量化结果（见 references/对标版式解析.md）
  · 画布 960x600（16:10，B 站封面）
  · 2-3 行超粗黑体，霓虹色 hero 行 + 白色 sub 行
  · 黑色厚描边 ≈ 0.075 × 字号（可读性的命根子）
  · 最长行撑到画面宽 84%，短行用字距（tracking）补齐
  · 文字块位置自动避开背景繁忙区

用法：
  python make_covers.py --topics topics.json --material 01_素材 --out 02_封面
  python make_covers.py --topics topics.json --material 01_素材 --out 02_封面 --variants 5
  python make_covers.py --topics topics.json --bg 某张图.jpg --out 02_封面   # 单图快速试排
"""
import argparse
import json
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ---------------------------------------------------------------- 常量

W, H = 960, 600          # 输出尺寸（16:10）
SS = 2                   # 超采样倍数，描边和曲线更顺滑
SIDE_MARGIN = 0.08       # 左右安全边距（占画面宽）
FILL_HERO = 0.84         # hero 行目标宽度占比
FILL_SUB = 0.72          # sub 行目标宽度占比
STROKE_RATIO = 0.075     # 描边宽度 / 字号

FONT_CANDIDATES = [
    (r"C:\Windows\Fonts\NotoSansSC-VF.ttf", "Black"),
    (r"C:\Windows\Fonts\msyhbd.ttc", None),
    (r"C:\Windows\Fonts\simhei.ttf", None),
    ("/usr/share/fonts/opentype/noto/NotoSansCJKsc-Black.otf", None),
]

# 霓虹色板，取自对标图逐像素采样
PALETTES = {
    "yellow":  {"hero": (250, 255, 0),   "sub": (255, 255, 255)},
    "green":   {"hero": (0, 255, 25),    "sub": (255, 255, 255)},
    "cyan":    {"hero": (26, 255, 235),  "sub": (255, 255, 255)},
    "magenta": {"hero": (255, 0, 192),   "sub": (255, 255, 255)},
    "red":     {"hero": (255, 20, 20),   "sub": (255, 255, 255)},
    "blue":    {"hero": (48, 160, 245),  "sub": (255, 255, 255)},
    "orange":  {"hero": (255, 156, 0),   "sub": (255, 255, 255)},
    # 反转版：hero 用白，sub 用霓虹（对标 7.x 那类）
    "green_inv": {"hero": (255, 255, 255), "sub": (0, 255, 25)},
}
STROKE_COLOR = (0, 0, 0)
BLOCK_COLOR = (255, 156, 0)   # 橙色底块（对标 1.x）

IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp")


# ---------------------------------------------------------------- 字体

_font_cache = {}


def load_font(size):
    """加载最粗的中文黑体。NotoSansSC 是可变字体，显式切到 Black 字重。"""
    size = max(8, int(size))
    if size in _font_cache:
        return _font_cache[size]
    last_err = None
    for path, variation in FONT_CANDIDATES:
        if not os.path.exists(path):
            continue
        try:
            f = ImageFont.truetype(path, size)
            if variation:
                try:
                    f.set_variation_by_name(variation)
                except Exception:
                    pass
            _font_cache[size] = f
            return f
        except Exception as e:      # noqa: BLE001
            last_err = e
    raise RuntimeError(
        "找不到可用的粗黑体。请安装 Noto Sans SC 或思源黑体 Heavy，"
        "或改 FONT_CANDIDATES。原始错误：%s" % last_err
    )


def text_width(text, font, track_px):
    """带字距的行宽。逐字累加，因为 Pillow 不支持 letter-spacing。"""
    if not text:
        return 0.0
    w = sum(font.getlength(ch) for ch in text)
    return w + track_px * (len(text) - 1)


def fit_font_size(text, target_w, lo=20, hi=400):
    """二分出让该行恰好达到 target_w 的字号（tracking=0）。"""
    if not text:
        return lo
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if text_width(text, load_font(mid), 0) <= target_w:
            lo = mid
        else:
            hi = mid - 1
    return lo


# ---------------------------------------------------------------- 背景

def load_background(path):
    """读图 → 等比缩放 → 居中裁到 16:10 → 放大到超采样尺寸。"""
    im = Image.open(path).convert("RGB")
    tw, th = W * SS, H * SS
    scale = max(tw / im.width, th / im.height)
    im = im.resize((max(tw, int(im.width * scale)), max(th, int(im.height * scale))),
                   Image.LANCZOS)
    x0 = (im.width - tw) // 2
    y0 = (im.height - th) // 2
    return im.crop((x0, y0, x0 + tw, y0 + th))


def busyness_profile(im):
    """逐行的『视觉繁忙度』：梯度能量 + 亮度方差。用来给文字块选干净的落点。"""
    g = np.asarray(im.convert("L").resize((240, 150), Image.LANCZOS)).astype(np.float32)
    gy, gx = np.gradient(g)
    energy = np.sqrt(gx ** 2 + gy ** 2).mean(axis=1)          # 每行梯度
    var = g.std(axis=1)                                        # 每行亮度起伏
    prof = energy / (energy.max() + 1e-6) + 0.5 * var / (var.max() + 1e-6)
    return prof, g


def pick_band(im, block_h_ratio, prefer=None):
    """
    在背景里滑窗找最干净的水平带，返回文字块顶部的 y 比例（0-1）。
    prefer: 'top' / 'center' / 'bottom' / None(自动)
    """
    prof, _ = busyness_profile(im)
    n = len(prof)
    win = max(1, int(block_h_ratio * n))
    if win >= n:
        return max(0.0, 0.5 - block_h_ratio / 2)

    cum = np.concatenate([[0.0], np.cumsum(prof)])
    scores = (cum[win:] - cum[:-win]) / win                    # 每个起点的平均繁忙度

    centers = (np.arange(len(scores)) + win / 2) / n
    if prefer == "top":
        scores = scores + np.abs(centers - 0.28) * 2.5
    elif prefer == "center":
        scores = scores + np.abs(centers - 0.50) * 2.5
    elif prefer == "bottom":
        scores = scores + np.abs(centers - 0.72) * 2.5
    else:
        # 自动：轻微惩罚贴边，避免文字顶到画面边缘
        scores = scores + np.abs(centers - 0.5) * 0.35

    best = int(np.argmin(scores))
    return best / n


def band_stats(gray_small, y0_ratio, h_ratio):
    """取该带的平均亮度与起伏，决定要不要压一层蒙版。"""
    n = gray_small.shape[0]
    a = int(y0_ratio * n)
    b = min(n, a + max(1, int(h_ratio * n)))
    seg = gray_small[a:b]
    if seg.size == 0:
        return 128.0, 0.0
    return float(seg.mean()), float(seg.std())


# ---------------------------------------------------------------- 排版

def layout_lines(lines, style):
    """
    算出每行的字号、字距、行宽、墨迹盒。

    规则（全部来自对标量化，见 references/对标版式解析.md）：
      1. 整块**共用一个基准字号**——对标 1.1 三行墨迹高都是 75px，层级靠
         颜色和行长拉开，不靠字号。基准 = 各行「撑到自己目标宽度」所需字号的
         **最小值**，这样最长的行刚好不溢出。
      2. sub 行可按 sub_scale 略缩（默认 0.92），维持一点主次。
      3. 多条 hero 行之间做两端对齐：短行加字距补到最宽行，字距封顶 0.22em。
      4. 最后硬夹一道：任何行都不许超出安全宽度。
    """
    usable = (1 - 2 * SIDE_MARGIN) * W
    sub_scale = style.get("sub_scale", 0.92)

    # --- 1. 基准字号 = 各行目标拟合值取最小 ---
    cand = []
    for ln in lines:
        role = ln.get("role", "sub")
        fill = ln.get("fill", style.get("fill_" + role,
                                        FILL_HERO if role == "hero" else FILL_SUB))
        size = fit_font_size(ln["text"], min(fill * W, usable))
        # sub 行按缩放折回基准坐标系再参与取最小
        cand.append(size / sub_scale if role == "sub" else size)
    base = max(12, int(min(cand)))

    plan = []
    for ln in lines:
        role = ln.get("role", "sub")
        size = int(base * sub_scale) if role == "sub" else base
        plan.append({"text": ln["text"], "role": role, "size": max(12, size)})

    # --- 2. 字距 ---
    base_track = style.get("tracking", 0.06)
    hero_w = [text_width(p["text"], load_font(p["size"]), 0)
              for p in plan if p["role"] == "hero"]
    widest_hero = max(hero_w) if hero_w else 0

    for p in plan:
        f = load_font(p["size"])
        raw = text_width(p["text"], f, 0)
        track = base_track * p["size"]
        # 只在 hero 行之间做两端对齐，sub 行保持自然宽度以拉出层级
        if (style.get("justify", True) and p["role"] == "hero"
                and len(p["text"]) > 1 and raw < widest_hero):
            need = (widest_hero - raw) / (len(p["text"]) - 1)
            track = max(track, min(need, 0.22 * p["size"]))

        # --- 3. 硬夹：先削字距，再削字号 ---
        n = max(1, len(p["text"]) - 1)
        if raw + track * n > usable:
            track = max(0.0, (usable - raw) / n)
        while text_width(p["text"], f, track) > usable and p["size"] > 12:
            p["size"] -= 2
            f = load_font(p["size"])
            raw = text_width(p["text"], f, 0)
            track = min(track, max(0.0, (usable - raw) / n))

        bbox = f.getbbox(p["text"]) if p["text"] else (0, 0, 0, 0)
        p["track"] = track
        p["w"] = text_width(p["text"], f, track)
        p["ink_top"] = bbox[1]                      # 墨迹顶相对绘制点的偏移
        p["ink"] = max(1, bbox[3] - bbox[1])        # 真实墨迹高，含拉丁下缘
    return plan


def draw_tracked(draw, x, y, text, font, fill, track, stroke_w=0, stroke_fill=None):
    """
    逐字绘制以支持字距。必须分两趟：先把所有字的描边画完，再画填充，
    否则后一个字的描边会啃掉前一个字的字面。
    """
    if stroke_w > 0:
        cx = x
        for ch in text:
            draw.text((cx, y), ch, font=font, fill=stroke_fill,
                      stroke_width=stroke_w, stroke_fill=stroke_fill, anchor="lt")
            cx += font.getlength(ch) + track
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=font, fill=fill, anchor="lt")
        cx += font.getlength(ch) + track


def soft_scrim(size, box, alpha, feather):
    """
    羽化的暗色带。不用硬边圆角矩形——对标全靠厚描边扛可读性，
    真需要压一层时也得是看不出边界的柔光，否则一眼廉价。
    """
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rectangle(box, fill=alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    layer.putalpha(mask)
    return layer


# ---------------------------------------------------------------- 合成

def compose(bg_path, topic, out_path, seed=None):
    style_name = topic.get("style", "yellow")
    palette = PALETTES.get(style_name, PALETTES["yellow"])
    style = topic.get("style_opts", {})
    deco = topic.get("deco", "auto")           # plain / scrim / block / auto
    align = topic.get("align", "center")       # center / left

    im = load_background(bg_path).convert("RGBA")
    plan = layout_lines(topic["lines"], style)

    gap = style.get("line_gap", 0.26)          # 行距 = gap × 该行字号（对标实测 0.26-0.55）
    heights = [p["ink"] for p in plan]
    gaps = [gap * p["size"] for p in plan[1:]]
    block_h = sum(heights) + sum(gaps)
    block_h_ratio = min(block_h / H, 0.92)

    y0r = topic.get("y")
    if y0r is None:
        y0r = pick_band(im, block_h_ratio, topic.get("pos"))
    y0r = min(max(y0r, 0.03), max(0.03, 1 - block_h_ratio - 0.03))

    _, gray = busyness_profile(im)
    mean_lum, std_lum = band_stats(gray, y0r, block_h_ratio)

    # ---- 装饰层 ----
    px = int(SIDE_MARGIN * W * SS)
    # auto 阈值调高：对标绝大多数图只靠厚描边扛，蒙版只在真的压不住时才出
    if deco == "scrim" or (deco == "auto" and (mean_lum > 196 or std_lum > 78)):
        pad = int(0.05 * W * SS)
        box = (-pad, int(y0r * H * SS) - pad,
               W * SS + pad, int((y0r + block_h_ratio) * H * SS) + pad)
        im = Image.alpha_composite(
            im, soft_scrim(im.size, box, 112, feather=0.035 * W * SS))
    elif mean_lum > 200:
        # 极亮背景：整块轻压一层，保住白字
        im = Image.alpha_composite(im, Image.new("RGBA", im.size, (0, 0, 0, 40)))

    txt = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(txt)

    y = y0r * H * SS
    for i, p in enumerate(plan):
        f = load_font(p["size"] * SS)
        track = p["track"] * SS
        w = text_width(p["text"], f, track)
        x = px if align == "left" else (W * SS - w) / 2

        color = palette[p["role"]]
        stroke_w = max(2, int(p["size"] * SS * STROKE_RATIO))

        # 橙色底块（对标 1.x）：只给 hero 行，字反白
        if deco == "block" and p["role"] == "hero":
            padx = int(0.12 * p["size"] * SS)
            pady = int(0.13 * p["size"] * SS)
            box = (max(int(0.02 * W * SS), int(x - padx)), int(y - pady),
                   min(int(0.98 * W * SS), int(x + w + padx)),
                   int(y + p["ink"] * SS + pady))
            blk = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(blk).rectangle(box, fill=BLOCK_COLOR + (255,))
            im = Image.alpha_composite(im, blk)
            color = (255, 255, 255)

        # 按实测墨迹盒回退绘制点，让 y 精确落在墨迹顶部，行距才视觉均匀
        y_draw = y - p["ink_top"] * SS
        draw_tracked(d, x, y_draw, p["text"], f, color, track,
                     stroke_w=stroke_w, stroke_fill=STROKE_COLOR)

        y += p["ink"] * SS + (gaps[i] * SS if i < len(gaps) else 0)

    # 柔和投影：从文字 alpha 派生，让字在杂乱照片上再拔一层
    if style.get("shadow", True):
        alpha = txt.split()[3].point(lambda v: int(v * 0.55))
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        sh.putalpha(alpha)
        sh = sh.filter(ImageFilter.GaussianBlur(6 * SS))
        im.alpha_composite(sh, (0, int(2 * SS)))

    im.alpha_composite(txt)

    out = im.convert("RGB").resize((W, H), Image.LANCZOS)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    out.save(out_path, quality=92, subsampling=0)
    return out_path


# ---------------------------------------------------------------- CLI

def collect_images(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(
        os.path.join(folder, f) for f in os.listdir(folder)
        if f.lower().endswith(IMG_EXT)
    )


def main():
    ap = argparse.ArgumentParser(description="批量合成 960x600 大字封面")
    ap.add_argument("--topics", required=True, help="topics.json 路径")
    ap.add_argument("--material", default="01_素材", help="素材根目录（下含 <topic_id>/ 子目录）")
    ap.add_argument("--out", default="02_封面", help="输出根目录")
    ap.add_argument("--variants", type=int, default=5, help="每个选题出几张背景变体")
    ap.add_argument("--bg", help="只用这一张背景快速试排（忽略 --material）")
    ap.add_argument("--only", help="只跑这个 topic id")
    ap.add_argument("--seed", type=int, default=20260909)
    args = ap.parse_args()

    with open(args.topics, encoding="utf-8") as fh:
        cfg = json.load(fh)
    topics = cfg["topics"] if isinstance(cfg, dict) else cfg

    made, skipped = 0, []
    for n, t in enumerate(topics, 1):
        tid = str(t.get("id") or t.get("slug") or n)
        if args.only and tid != args.only:
            continue

        if args.bg:
            bgs = [args.bg]
        else:
            bgs = collect_images(os.path.join(args.material, tid))
            if not bgs:
                bgs = collect_images(args.material)
        if not bgs:
            skipped.append((tid, "没有背景素材"))
            continue

        random.Random(args.seed + (hash(tid) % 9973)).shuffle(bgs)
        for i, bg in enumerate(bgs[: args.variants], 1):
            out = os.path.join(args.out, tid, "%s.%d.jpg" % (tid, i))
            try:
                compose(bg, t, out, seed=args.seed + i)
                made += 1
                print("  ok  %s  <-  %s" % (out, os.path.basename(bg)))
            except Exception as e:      # noqa: BLE001
                skipped.append((tid, "%s: %s" % (os.path.basename(bg), e)))

    print("\n合成完成：%d 张" % made)
    for tid, why in skipped:
        print("  跳过 %s — %s" % (tid, why), file=sys.stderr)


if __name__ == "__main__":
    main()
