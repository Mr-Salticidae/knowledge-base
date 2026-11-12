# -*- coding: utf-8 -*-
"""视频线索 → 抽帧 → 中文 OCR，捞取画面中叠加的文字/字幕/聊天记录。

用法:
    python video_frame_ocr.py --src <含 mp4 的目录> --out <输出 md> [--interval 4] [--workers 6]

说明: 很多剧本音视频线索是无声实拍，信息藏在画面文字或道具里。
本脚本只负责「画面文字」；语音台词另走 ASR；纯视觉信息需人工/多模态看图补足。
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"
import argparse
import re
import shutil
import subprocess
import tempfile
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image

MAXSIDE = 1600
MIN_CONF = 0.50
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


def ocr_frame(path):
    try:
        im = Image.open(path).convert("L")
        w, h = im.size
        scale = min(1.0, MAXSIDE / max(w, h))
        if scale < 1.0:
            im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        arr = np.repeat(np.array(im)[:, :, None], 3, axis=2)
        res, _ = _eng(arr)
        texts = []
        for box, txt, sc in (res or []):
            try:
                conf = float(sc)
            except (TypeError, ValueError):
                conf = 1.0
            t = str(txt).strip()
            if conf >= MIN_CONF and len(t) >= 2:
                texts.append((min(p[1] for p in box), min(p[0] for p in box), t))
        texts.sort()
        return str(path), " / ".join(t for _, _, t in texts), ""
    except Exception as e:
        return str(path), "", "%s: %s" % (type(e).__name__, str(e)[:80])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--interval", type=float, default=4.0, help="每 N 秒抽一帧")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    src = Path(args.src)
    vids = sorted(src.rglob("*.mp4"))
    tmp = Path(tempfile.mkdtemp(prefix="juben_frames_"))
    frames = []          # (video_rel, frame_path)
    print("videos=%d interval=%ss" % (len(vids), args.interval), flush=True)
    try:
        for i, v in enumerate(vids, 1):
            rel = v.relative_to(src)
            d = tmp / ("%03d" % i)
            d.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(v),
                            "-vf", "fps=1/%s" % args.interval, "-q:v", "4",
                            str(d / "f_%03d.jpg")], check=False, capture_output=True)
            fs = sorted(d.glob("*.jpg"))
            frames.extend([(str(rel), str(f)) for f in fs])
            print("  %2d/%d %-28s frames=%d" % (i, len(vids), v.name[:26], len(fs)), flush=True)

        t0 = time.time()
        results = {}
        with Pool(processes=args.workers, initializer=init_worker) as pool:
            for n, (p, text, err) in enumerate(pool.imap_unordered(ocr_frame, [f for _, f in frames], chunksize=2), 1):
                results[p] = (text, err)
                if n % 40 == 0 or n == len(frames):
                    print("  ocr %d/%d %.1fs" % (n, len(frames), time.time() - t0), flush=True)

        by_video, cur = {}, None
        for rel, fp in frames:
            if rel != cur:
                by_video.setdefault(rel, [])
                cur = rel
            text, err = results.get(fp, ("", "missing"))
            if text:
                idx = int(re.search(r"f_(\d+)", Path(fp).stem).group(1))
                by_video[rel].append((idx, text))

        parts = ["# 音视频线索 · 画面文字\n\n> 每 %g 秒抽一帧做中文 OCR；无声镜头或纯道具画面不会出现在下面，\n> 纯视觉信息（如「眼球泡在防腐液盒子里」）需回看视频。\n" % args.interval]
        for rel, rows in by_video.items():
            parts.append("\n---\n\n## %s\n\n" % rel)
            seen = set()
            uniq = []
            for idx, text in rows:
                if text in seen:
                    continue
                seen.add(text)
                uniq.append((idx, text))
            if not uniq:
                parts.append("*（未检出画面文字，线索为纯视觉内容）*\n")
            for idx, text in uniq:
                parts.append("- 第 %d 帧（约 %gs）：%s\n" % (idx, idx * args.interval, text))
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text("".join(parts), encoding="utf-8")
        print("WROTE", args.out, "DONE %.1fs" % (time.time() - t0), flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
