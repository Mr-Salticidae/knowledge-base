# -*- coding: utf-8 -*-
"""
contact_sheet.py -- 把批量出的封面拼成审图大图，供人工一眼挑。

20 个选题 × 5 张变体 = 100 张图，一张张点开看是不现实的。
这个脚本按选题分组拼成若干张 contact sheet，每格左上角标 id.序号，
挑中哪个直接报编号。

用法：
  python contact_sheet.py --covers 02_封面 --out 03_审图
  python contact_sheet.py --covers 02_封面 --out 03_审图 --cols 5 --rows 4
"""
import argparse
import os

from PIL import Image, ImageDraw, ImageFont

CELL_W = 384                       # 每格宽（960 的 40%）
LABEL_H = 26
PAD = 10
BG = (24, 24, 26)
FG = (235, 235, 235)
IMG_EXT = (".jpg", ".jpeg", ".png")

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def load_font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:      # noqa: BLE001
                pass
    return ImageFont.load_default()


def collect(covers):
    """covers/<topic_id>/<file> → [(label, path), ...]，也吃平铺目录。"""
    items = []
    for root, _dirs, files in os.walk(covers):
        for f in sorted(files):
            if not f.lower().endswith(IMG_EXT):
                continue
            path = os.path.join(root, f)
            items.append((os.path.splitext(f)[0], path))
    return items


def build(items, out_path, cols, rows, title=None):
    cell_h = int(CELL_W * 600 / 960)
    gw = CELL_W + PAD
    gh = cell_h + LABEL_H + PAD
    head = 40 if title else 0
    sheet = Image.new("RGB", (cols * gw + PAD, rows * gh + PAD + head), BG)
    d = ImageDraw.Draw(sheet)
    if title:
        d.text((PAD, PAD + 4), title, font=load_font(20), fill=FG)

    f = load_font(16)
    for i, (label, path) in enumerate(items):
        r, c = divmod(i, cols)
        x = PAD + c * gw
        y = PAD + head + r * gh
        try:
            im = Image.open(path).convert("RGB").resize((CELL_W, cell_h), Image.LANCZOS)
        except Exception:      # noqa: BLE001
            continue
        sheet.paste(im, (x, y))
        d.text((x + 2, y + cell_h + 4), label, font=f, fill=FG)
    sheet.save(out_path, quality=90)
    return out_path


def main():
    ap = argparse.ArgumentParser(description="拼封面审图大图")
    ap.add_argument("--covers", default="02_封面")
    ap.add_argument("--out", default="03_审图")
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--rows", type=int, default=4)
    args = ap.parse_args()

    items = collect(args.covers)
    if not items:
        print("在 %s 下没找到封面。" % args.covers)
        return
    os.makedirs(args.out, exist_ok=True)

    per = args.cols * args.rows
    made = []
    for n, i in enumerate(range(0, len(items), per), 1):
        chunk = items[i:i + per]
        rows = min(args.rows, -(-len(chunk) // args.cols))
        p = os.path.join(args.out, "审图_%02d.jpg" % n)
        build(chunk, p, args.cols, rows, title="封面审图 %d / 共 %d 张" %
              (n, len(items)))
        made.append(p)
        print("  ok  %s  (%d 格)" % (p, len(chunk)))
    print("\n生成 %d 张审图大图。" % len(made))


if __name__ == "__main__":
    main()
