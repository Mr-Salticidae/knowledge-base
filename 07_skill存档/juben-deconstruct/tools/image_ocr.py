# -*- coding: utf-8 -*-
"""OCR standalone JPG/PNG images into one Markdown file per group."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import glob
from PIL import Image
import numpy as np
import rapidocr_onnxruntime.utils as ru
from onnxruntime import SessionOptions

class SO(SessionOptions):
    def __init__(self):
        super().__init__()
        self.intra_op_num_threads = 1
        self.inter_op_num_threads = 1
ru.SessionOptions = SO
from rapidocr_onnxruntime import RapidOCR

ROOT = r"C:\Users\12258\Downloads\954虚拟游戏\6人虚拟游戏"
OUT = r"C:\Users\12258\WorkBuddy\2026-11-12-18-07-45\954虚拟游戏_MD\06_图片资料"
os.makedirs(OUT, exist_ok=True)
engine = RapidOCR()

GROUPS = [
    ("测评问卷", sorted(glob.glob(ROOT + r"\测评\*.jpg")), "测评"),
    ("结局解析", sorted(glob.glob(ROOT + r"\结局解析\*.jpg")), "结局解析"),
    ("海报与人物图", sorted(glob.glob(ROOT + r"\海报人物图\*.*")), "海报人物图"),
]

MAXSIDE = 2000

for title, files, fname in GROUPS:
    parts = ["# %s · 图片 OCR\n\n> 来源：`6人虚拟游戏/%s/`\n> 自动中文 OCR，仅供检索；海报类以图为主，文字可能不完整。\n"
             % (title, fname)]
    for f in files:
        try:
            im = Image.open(f).convert("RGB")
            w, h = im.size
            scale = min(1.0, MAXSIDE / max(w, h))
            if scale < 1.0:
                im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
            arr = np.array(im)
            res, _ = engine(arr)
            lines = []
            if res:
                items = []
                for box, txt, sc in res:
                    try:
                        conf = float(sc)
                    except (TypeError, ValueError):
                        conf = 1.0
                    if conf < 0.45:
                        continue
                    ys = [p[1] for p in box]
                    xs = [p[0] for p in box]
                    items.append((min(ys), min(xs), str(txt).strip()))
                for _, _, t in sorted(items):
                    if t:
                        lines.append(t)
            parts.append("\n---\n\n## %s\n\n- 原图：`%s`（%d×%d）\n\n" %
                         (os.path.basename(f), fname + "/" + os.path.basename(f), w, h))
            parts.append("\n".join(lines) if lines else "*（未识别到文字 / 纯图）*")
            parts.append("\n")
            print("OK", os.path.basename(f), w, h, "lines", len(lines), flush=True)
        except Exception as e:
            parts.append("\n---\n\n## %s\n\n*OCR 失败：%s*\n" % (os.path.basename(f), e))
            print("FAIL", f, e, flush=True)
    open(os.path.join(OUT, fname + ".md"), "w", encoding="utf-8").write("".join(parts))
    print("WROTE", fname + ".md", flush=True)
