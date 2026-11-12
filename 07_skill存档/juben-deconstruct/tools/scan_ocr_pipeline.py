# -*- coding: utf-8 -*-
"""扫描图资料包 → Markdown 通用流水线。

适用于纯 JPG/PNG 扫描件（角色剧本、组织者手册、线索卡、地图等），
按目录自动分组、按文件名中的数字排页序、按 y 坐标聚类还原正文段落。

用法:
    python scan_ocr_pipeline.py --src <dir> --out <dir> [--workers 6] [--only 组织者手册]
    JUBEN_SRC / JUBEN_OUT 环境变量可替代 --src / --out

依赖: pillow, numpy, onnxruntime, rapidocr_onnxruntime
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import argparse
import re
import time
from pathlib import Path
from multiprocessing import Pool

import numpy as np
from PIL import Image

MAXSIDE = 2000           # 缩放到长边 2000px，精度/速度平衡点
MIN_CONF = 0.45          # 低于此置信度的文本框丢弃
GROUP_SPLIT_TOL = 0.60   # 行聚类容差 = 中位字高 × 该系数
PARA_GAP = 2.2           # 段落间隔 = 中位字高 × 该系数

_eng = None


def init_worker():
    global _eng
    os.environ["OMP_NUM_THREADS"] = "1"
    import rapidocr_onnxruntime.utils as ru
    from onnxruntime import SessionOptions

    class SO(SessionOptions):
        def __init__(self):
            super().__init__()
            self.intra_op_num_threads = 1
            self.inter_op_num_threads = 1

    ru.SessionOptions = SO
    from rapidocr_onnxruntime import RapidOCR
    _eng = RapidOCR()


def num_key(path):
    """图像 (100).jpg → 100；无数字时退回到文件名。保证自然页序。"""
    m = re.findall(r"(\d+)", Path(path).stem)
    return (int(m[-1]) if m else 10**9, Path(path).stem)


def layout(items):
    """把 OCR 文本框按 y 聚类成行、行内按 x 排序，再按行距切段落。"""
    if not items:
        return ""
    heights = [ymax - ymin for ymin, ymax, _, _ in items]
    med = sorted(heights)[len(heights) // 2] or 14
    tol = med * GROUP_SPLIT_TOL
    items = sorted(items, key=lambda it: (it[0], it[2]))
    rows, cur, anchor = [], [], None
    for it in items:
        if anchor is None or abs(it[0] - anchor) <= tol:
            cur.append(it)
            anchor = it[0] if anchor is None else (anchor * (len(cur) - 1) + it[0]) / len(cur)
        else:
            rows.append(cur)
            cur, anchor = [it], it[0]
    if cur:
        rows.append(cur)

    out, prev_bottom = [], None
    for row in rows:
        row.sort(key=lambda it: it[2])
        line, prev_right = "", None
        for ymin, ymax, xmin, txt in row:
            if not txt:
                continue
            if line and prev_right is not None and xmin - prev_right > med * 1.2:
                line += "  "
            line += txt
            prev_right = max(prev_right or 0, xmin + len(txt) * med * 0.6)
        top = min(it[0] for it in row)
        bottom = max(it[1] for it in row)
        if prev_bottom is not None and top - prev_bottom > med * PARA_GAP:
            out.append("")
        out.append(line.strip())
        prev_bottom = bottom
    return "\n".join(out).strip()


def ocr_one(path):
    try:
        im = Image.open(path).convert("L")
        w, h = im.size
        scale = min(1.0, MAXSIDE / max(w, h))
        if scale < 1.0:
            im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        arr = np.repeat(np.array(im)[:, :, None], 3, axis=2)
        res, _ = _eng(arr)
        items = []
        for box, txt, sc in (res or []):
            try:
                conf = float(sc)
            except (TypeError, ValueError):
                conf = 1.0
            if conf < MIN_CONF:
                continue
            ys, xs = [p[1] for p in box], [p[0] for p in box]
            items.append((min(ys), max(ys), min(xs), str(txt).strip()))
        return str(path), layout(items), len(items), ""
    except Exception as e:
        return str(path), "", 0, "%s: %s" % (type(e).__name__, str(e)[:120])


def discover(src):
    """返回 {组名: [图片路径...]}。组名按资料包目录语义生成。"""
    src = Path(src)
    groups = {}
    for p in sorted(src.rglob("*")):
        if p.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        rel = p.relative_to(src)
        parts = rel.parts
        if parts[0].startswith("窗边的女人音视频") or "音视频" in parts[0]:
            continue
        if len(parts) == 1:
            group = "地图与散页"
        elif parts[0] == "人物剧本" and len(parts) == 2:
            group = "人物剧本·前言"
        elif parts[0] == "人物剧本":
            group = "人物剧本·" + parts[1]
        else:
            group = parts[0]
        groups.setdefault(group, []).append(p)
    return {k: sorted(v, key=num_key) for k, v in groups.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=os.environ.get("JUBEN_SRC", ""))
    ap.add_argument("--out", default=os.environ.get("JUBEN_OUT", ""))
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", default="", help="只跑组名包含该字符串的分组")
    args = ap.parse_args()
    if not args.src or not args.out:
        raise SystemExit("需要 --src / --out 或 JUBEN_SRC / JUBEN_OUT")

    groups = discover(args.src)
    if args.only:
        groups = {k: v for k, v in groups.items() if args.only in k}
    tasks = [(str(p), g) for g, ps in groups.items() for p in ps]
    print("groups=%d pages=%d workers=%d" % (len(groups), len(tasks), args.workers), flush=True)

    out = Path(args.out)
    (out / "_raw").mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    results = {}
    with Pool(processes=args.workers, initializer=init_worker) as pool:
        for n, (path, text, nbox, err) in enumerate(pool.imap_unordered(ocr_one, [t[0] for t in tasks], chunksize=1), 1):
            results[path] = (text, nbox, err)
            if n % 10 == 0 or n == len(tasks):
                print("  %d/%d  %.1fs" % (n, len(tasks), time.time() - t0), flush=True)

    for g, ps in groups.items():
        safe = re.sub(r"[\\/:*?\"<>|]", "_", g)
        parts = ["# %s\n\n> 共 %d 页 · 扫描图中文 OCR 自动识别，可能有错字，关键判定请回看原图。\n" % (g, len(ps))]
        plain, errs, nonempty = [], [], 0
        for i, p in enumerate(ps, 1):
            text, nbox, err = results.get(str(p), ("", 0, "missing"))
            if err:
                errs.append("p%d %s" % (i, err))
            parts.append("\n---\n\n## 第 %d 页\n\n" % i)
            if text:
                parts.append(text + "\n")
                plain.append("[第%d页]\n%s" % (i, text))
                nonempty += 1
            else:
                parts.append("*（本页未识别到文字 / 纯图片页）*\n")
        (out / (safe + ".md")).write_text("".join(parts), encoding="utf-8")
        (out / "_raw" / (safe + ".txt")).write_text("\n\n".join(plain), encoding="utf-8")
        print("WROTE %s pages=%d with_text=%d errors=%d" % (safe, len(ps), nonempty, len(errs)), flush=True)
        if errs:
            print("   ERR:", "; ".join(errs[:5]), flush=True)
    print("DONE %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
