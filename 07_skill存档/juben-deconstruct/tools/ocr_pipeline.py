# -*- coding: utf-8 -*-
"""Batch OCR for the scanned PDFs in 954虚拟游戏.
Reconstructs reading order: two-column A3 spreads are split at the gutter,
lines are re-grouped, and indented lines start a new paragraph.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import sys, io, json, time, math, argparse
import numpy as np
import pymupdf
from multiprocessing import Pool

# (abs pdf path, output md path, short label)
ROOT = r"C:\Users\12258\Downloads\954虚拟游戏"
OUT = r"C:\Users\12258\WorkBuddy\2026-11-12-18-07-45\954虚拟游戏_MD"

JOBS = [
    (ROOT + r"\剧本\剧本\6组织者.pdf",          OUT + r"\01_角色剧本\06_组织者手册.md",      "组织者手册"),
    (ROOT + r"\剧本\剧本\1李雨婷.pdf",          OUT + r"\01_角色剧本\01_李雨婷.md",          "李雨婷"),
    (ROOT + r"\剧本\剧本\2尹梦竹.pdf",          OUT + r"\01_角色剧本\02_尹梦竹.md",          "尹梦竹"),
    (ROOT + r"\剧本\剧本\3江白.pdf",            OUT + r"\01_角色剧本\03_江白.md",            "江白"),
    (ROOT + r"\剧本\剧本\4孙子楚.pdf",          OUT + r"\01_角色剧本\04_孙子楚.md",          "孙子楚"),
    (ROOT + r"\剧本\剧本\5于菲.pdf",            OUT + r"\01_角色剧本\05_于菲.md",            "于菲"),
    (ROOT + r"\剧本\剧本\7简清.pdf",            OUT + r"\01_角色剧本\07_简清.md",            "简清"),
    (ROOT + r"\剧本\线索卡.pdf",                OUT + r"\02_线索卡\线索卡_全套150页.md",      "线索卡"),
    (ROOT + r"\剧本\a4线索卡.pdf",              OUT + r"\02_线索卡\线索卡_A4打印版.md",       "A4线索卡"),
    (ROOT + r"\剧本\b5线索卡.pdf",              OUT + r"\02_线索卡\线索卡_B5打印版.md",       "B5线索卡"),
    (ROOT + r"\剧本\剧本\封皮.pdf",             OUT + r"\01_角色剧本\00_封皮.md",            "封皮"),
]

_engine = None
_docs = {}


def init_worker():
    """One ORT inference thread per process -> real multi-process scaling."""
    global _engine
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
    _engine = RapidOCR()


def to_lines(boxes, W, H):
    """Split into columns at a detected vertical gutter, then group lines."""
    if not boxes:
        return []
    # find widest empty vertical run in the central part of the page
    bins = 120
    occ = [0] * bins
    for b in boxes:
        x0, x1 = b["x0"], b["x1"]
        a = max(0, min(bins - 1, int(x0 / W * bins)))
        c = max(0, min(bins - 1, int(x1 / W * bins)))
        for i in range(a, c + 1):
            occ[i] = 1
    lo, hi = int(bins * 0.32), int(bins * 0.68)
    best_len, best_pos = 0, -1
    i = lo
    while i < hi:
        if occ[i] == 0:
            j = i
            while j < hi and occ[j] == 0:
                j += 1
            if j - i > best_len:
                best_len, best_pos = j - i, (i + j) / 2
            i = j
        else:
            i += 1
    gutter = None
    if best_len >= 4 and best_pos > 0:
        gx = best_pos / bins * W
        left = [b for b in boxes if (b["x0"] + b["x1"]) / 2 < gx]
        right = [b for b in boxes if (b["x0"] + b["x1"]) / 2 >= gx]
        if len(left) >= 3 and len(right) >= 3:
            gutter = gx
    groups = [boxes] if gutter is None else [
        [b for b in boxes if (b["x0"] + b["x1"]) / 2 < gutter],
        [b for b in boxes if (b["x0"] + b["x1"]) / 2 >= gutter],
    ]
    columns = []
    for g in groups:
        if not g:
            columns.append("")
            continue
        heights = sorted(b["y1"] - b["y0"] for b in g)
        mh = heights[len(heights) // 2] or 18
        tol = max(10, mh * 0.62)
        g = sorted(g, key=lambda b: (b["y0"] + b["y1"]) / 2)
        lines, cur, cur_y = [], [], None
        for b in g:
            cy = (b["y0"] + b["y1"]) / 2
            if cur_y is None or abs(cy - cur_y) <= tol:
                cur.append(b)
                cur_y = cy if cur_y is None else (cur_y * (len(cur) - 1) + cy) / len(cur)
            else:
                lines.append(cur)
                cur, cur_y = [b], cy
        if cur:
            lines.append(cur)
        # paragraph reconstruction: indented line starts new paragraph
        margin = min(b["x0"] for b in g)
        paras, buf = [], ""
        for ln in lines:
            ln = sorted(ln, key=lambda b: b["x0"])
            text = "".join(b["t"] for b in ln).strip()
            if not text:
                continue
            if min(b["x0"] for b in ln) - margin > max(14, mh * 0.55) and buf:
                paras.append(buf)
                buf = text
            else:
                buf += text
        if buf:
            paras.append(buf)
        columns.append("\n\n".join(paras))
    return columns


def process(task):
    path, pno, zoom = task
    global _engine
    try:
        if path not in _docs:
            _docs[path] = pymupdf.open(path)
        doc = _docs[path]
        page = doc[pno]
        pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom),
                              colorspace=pymupdf.csGRAY, alpha=False)
        g = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
        arr = np.repeat(g[:, :, None], 3, axis=2)
        res, _ = _engine(arr)
        boxes = []
        if res:
            for box, txt, score in res:
                try:
                    sc = float(score)
                except (TypeError, ValueError):
                    sc = 1.0
                if sc < 0.42 or not str(txt).strip():
                    continue
                xs = [p[0] for p in box]
                ys = [p[1] for p in box]
                boxes.append({"x0": min(xs), "x1": max(xs), "y0": min(ys),
                              "y1": max(ys), "t": str(txt).strip()})
        cols = to_lines(boxes, pix.width, pix.height)
        return (path, pno, cols, "")
    except Exception as e:
        return (path, pno, [], "%s: %s" % (type(e).__name__, e))


def zoom_for(page):
    r = page.rect
    return min(3.5, 1800.0 / max(r.width, r.height))


def write_md(path, m, results):
    os.makedirs(os.path.dirname(m["out"]), exist_ok=True)
    errs, nonempty = [], 0
    parts = ["# %s\n\n> 来源：`%s`\n> 共 %d 页，中文 OCR 自动识别（扫描件，可能有错字，重要内容请回看原 PDF）。\n"
             % (m["label"], os.path.relpath(path, ROOT).replace("\\", "/"), m["npages"])]
    plaintext = []
    for i in range(m["npages"]):
        cols, err = results.get(i, ([], "missing"))
        if err:
            errs.append("p%d %s" % (i + 1, err))
        parts.append("\n---\n\n## 第 %d 页\n" % (i + 1))
        if not cols or not any(c.strip() for c in cols):
            parts.append("\n*（本页未识别到文字 / 纯图片页）*\n")
        else:
            nonempty += 1
            if len(cols) == 2:
                parts.append("\n### 左页\n\n%s\n\n### 右页\n\n%s\n" % (cols[0] or "*(空)*", cols[1] or "*(空)*"))
                plaintext.append("[第%d页·左]\n%s\n[第%d页·右]\n%s" % (i + 1, cols[0], i + 1, cols[1]))
            else:
                parts.append("\n%s\n" % (cols[0] if cols else ""))
                plaintext.append("[第%d页]\n%s" % (i + 1, cols[0] if cols else ""))
    with open(m["out"], "w", encoding="utf-8") as f:
        f.write("".join(parts))
    raw = os.path.join(OUT, "_raw", os.path.splitext(os.path.basename(m["out"]))[0] + ".txt")
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    with open(raw, "w", encoding="utf-8") as f:
        f.write("\n\n".join(plaintext))
    print("WROTE %s  pages=%d with_text=%d errors=%d chars=%d" %
          (m["out"], m["npages"], nonempty, len(errs), sum(len(x) for x in plaintext)), flush=True)
    if errs:
        print("   ERR:", "; ".join(errs[:8]), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--only", default="")
    ap.add_argument("--skip-existing", action="store_true")
    args = ap.parse_args()

    jobs = [j for j in JOBS if not args.only or args.only in j[2]]
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    with Pool(processes=args.workers, initializer=init_worker) as pool:
        for path, outmd, label in jobs:
            if args.skip_existing and os.path.exists(outmd):
                print("SKIP %s" % label, flush=True)
                continue
            d = pymupdf.open(path)
            z = zoom_for(d[0])
            npages = len(d)
            d.close()
            m = {"out": outmd, "label": label, "npages": npages, "zoom": z}
            tasks = [(path, i, z) for i in range(npages)]
            print("START %s (%d pages)  elapsed=%.0fs" % (label, npages, time.time() - t0), flush=True)
            results = {}
            for n, (_, pno, cols, err) in enumerate(pool.imap_unordered(process, tasks, chunksize=1), 1):
                results[pno] = (cols, err)
                if n % 10 == 0 or n == npages:
                    print("   %s %d/%d  %.0fs" % (label, n, npages, time.time() - t0), flush=True)
            write_md(path, m, results)
    print("DONE %.1fs" % (time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
