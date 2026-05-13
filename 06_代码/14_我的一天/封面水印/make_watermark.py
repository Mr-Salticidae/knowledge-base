# -*- coding: utf-8 -*-
"""
我的一天 · MY DAY — 封面水印批处理
=====================================

为 5 张系列图加细 serif 文学风格水印。
视觉语言与 11_凝视 footer 对齐 — "跳蛛先生"作品集的统一签名标识。

水印结构(右下角内缩 4.5%,右对齐):
    我 的 一 天   M Y   D A Y
    01 / 05    跳蛛先生

设计准则
--------
- 字体: 中文 SourceHanSerifSC-ExtraLight + 英文 DejaVuSans-ExtraLight
- 颜色: 暖灰白 (228, 224, 214) @ 65% 不透明度
- 字号: 主行长边 1.85% / 副行 1.3%
- 字间距: 中文+2 空格 / 英文大写+2 空格 / 数字+1 空格
- 编号: 01/05 阿拉伯前导零(早期试过 I/V + MMXXVI 被否,理由"不明觉厉")
- 渲染: supersample 2x + LANCZOS

Usage
-----
    python make_watermark.py
    python make_watermark.py --src DIR --dst DIR --font-cn PATH --font-en PATH
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SERIES_TITLE_CN = "我的一天"
SERIES_TITLE_EN = "MY DAY"
AUTHOR_CN = "跳蛛先生"
TOTAL = 5

FILE_MAPPING = {
    "6979eb7b": (1, "做游戏"),
    "5b9904a6": (2, "打游戏"),
    "93206c09": (3, "读书"),
    "f3d9f450": (4, "听音乐"),
    "0bedd499": (5, "看电影"),
}

WM_INSET_RATIO = 0.045
WM_LINE1_RATIO = 0.0185
WM_LINE2_RATIO = 0.013
WM_COLOR = (228, 224, 214)
WM_OPACITY = 165
WM_LINE_GAP_RATIO = 1.5
SPACING_CN = 2
SPACING_EN_TITLE = 2
SPACING_EN_FOOT = 1

DEFAULT_SRC = Path(r"D:\小红书运营\临时创作\2026-05-09_我的一天")
DEFAULT_DST = Path(r"D:\小红书运营\14_我的一天\成品图")
DEFAULT_FONT_CN = Path(r"D:\小红书运营\字体\SourceHanSerifSC-ExtraLight.otf")
DEFAULT_FONT_EN = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf")


@dataclass
class Job:
    src: Path
    dst: Path
    index: int
    theme: str

    @property
    def num_label(self) -> str:
        return f"{self.index:02d} / {TOTAL:02d}"


def spaced(text: str, n: int = 1) -> str:
    return (" " * n).join(text)


def discover_jobs(src_dir: Path, dst_dir: Path) -> list[Job]:
    jobs: list[Job] = []
    for png in src_dir.glob("*.png"):
        for tag, (idx, theme) in FILE_MAPPING.items():
            if tag in png.name:
                out = dst_dir / f"{idx:02d}_{theme}.png"
                jobs.append(Job(src=png, dst=out, index=idx, theme=theme))
                break
        else:
            print(f"[skip] 未识别: {png.name}")
    jobs.sort(key=lambda j: j.index)
    return jobs


def render_watermark(img, job, font_cn_path, font_en_path, *, supersample=2):
    base = img.convert("RGBA")
    W, H = base.size
    long_edge = max(W, H)
    SS = supersample

    inset = int(long_edge * WM_INSET_RATIO * SS)
    fz1 = int(long_edge * WM_LINE1_RATIO * SS)
    fz2 = int(long_edge * WM_LINE2_RATIO * SS)
    color = WM_COLOR + (WM_OPACITY,)

    overlay = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_cn1 = ImageFont.truetype(str(font_cn_path), fz1)
    f_en1 = ImageFont.truetype(str(font_en_path), fz1)
    f_cn2 = ImageFont.truetype(str(font_cn_path), fz2)
    f_en2 = ImageFont.truetype(str(font_en_path), fz2)

    right_x = W * SS - inset
    bottom_y = H * SS - inset

    # Line 2: 01/05  跳蛛先生
    parts2 = [
        (spaced(AUTHOR_CN, SPACING_CN), f_cn2),
        ("    ", f_en2),
        (spaced(job.num_label, SPACING_EN_FOOT), f_en2),
    ]
    cursor = right_x
    for txt, fn in parts2:
        bbox = draw.textbbox((0, 0), txt, font=fn)
        w = bbox[2] - bbox[0]
        draw.text((cursor, bottom_y), txt, font=fn, fill=color, anchor="rd")
        cursor -= w

    # Line 1: 我的一天 MY DAY
    line2_h = draw.textbbox((0, 0), "Ag我", font=f_cn2)[3]
    gap = int(line2_h * WM_LINE_GAP_RATIO)
    y1 = bottom_y - line2_h - gap

    parts1 = [
        (spaced(SERIES_TITLE_EN, SPACING_EN_TITLE), f_en1),
        ("    ", f_en1),
        (spaced(SERIES_TITLE_CN, SPACING_CN), f_cn1),
    ]
    cursor = right_x
    for txt, fn in parts1:
        bbox = draw.textbbox((0, 0), txt, font=fn)
        w = bbox[2] - bbox[0]
        draw.text((cursor, y1), txt, font=fn, fill=color, anchor="rd")
        cursor -= w

    overlay = overlay.resize((W, H), Image.LANCZOS)
    return Image.alpha_composite(base, overlay)


def process(jobs, font_cn, font_en):
    if not Path(font_cn).exists():
        raise FileNotFoundError(f"中文字体不存在: {font_cn}")
    if not Path(font_en).exists():
        raise FileNotFoundError(f"英文字体不存在: {font_en}")
    for job in jobs:
        job.dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(job.src) as im:
            out = render_watermark(im, job, font_cn, font_en)
            out.save(job.dst, "PNG", optimize=True)
        print(f"[ok] {job.index:02d} {job.theme}  ->  {job.dst.name}")


def main():
    ap = argparse.ArgumentParser(description="我的一天 · 封面水印批处理")
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC)
    ap.add_argument("--dst", type=Path, default=DEFAULT_DST)
    ap.add_argument("--font-cn", type=Path, default=DEFAULT_FONT_CN)
    ap.add_argument("--font-en", type=Path, default=DEFAULT_FONT_EN)
    args = ap.parse_args()

    jobs = discover_jobs(args.src, args.dst)
    if not jobs:
        print(f"未在 {args.src} 找到匹配的原图。")
        return
    print(f"待处理: {len(jobs)} 张  ->  {args.dst}")
    process(jobs, args.font_cn, args.font_en)
    print("完成。")


if __name__ == "__main__":
    main()
