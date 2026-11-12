# -*- coding: utf-8 -*-
"""The script PDFs are saddle-stitch 2-up scans: sheet k holds printed page k
on one side and printed page (2S+1-k) on the other. Rebuild the true reading order.

For sheet k (1-based):
  front page k        -> right half when k is odd,  left half when k is even
  back  page 2S+1-k   -> left  half when k is odd,  right half when k is even
Reading order = front 1..S, then back S+1..2S  (i.e. k = S..1 on the back half).
"""
import os, re, shutil

OUT = r"C:\Users\12258\WorkBuddy\2026-11-12-18-07-45\954虚拟游戏_MD"
RAW = OUT + r"\_raw"
BACKUP = RAW + r"\扫描页序备份"
os.makedirs(BACKUP, exist_ok=True)

DOCS = [
    ("00_封皮", "01_角色剧本/00_封皮.md", "封皮", 7, False),
    ("01_李雨婷", "01_角色剧本/01_李雨婷.md", "李雨婷", 12, True),
    ("02_尹梦竹", "01_角色剧本/02_尹梦竹.md", "尹梦竹", 12, True),
    ("03_江白", "01_角色剧本/03_江白.md", "江白", 12, True),
    ("04_孙子楚", "01_角色剧本/04_孙子楚.md", "孙子楚", 12, True),
    ("05_于菲", "01_角色剧本/05_于菲.md", "于菲", 12, True),
    ("06_组织者手册", "01_角色剧本/06_组织者手册.md", "组织者手册", 16, True),
    ("07_简清", "01_角色剧本/07_简清.md", "简清", 12, True),
]

MARK = re.compile(r"(?m)^\[(第(\d+)页(?:·(左|右))?)\]\s*$")
FOOTNUM = re.compile(r"^\s*(\d{1,2})\s*$")


def parse(name):
    text = open(os.path.join(RAW, name + ".txt"), encoding="utf-8").read()
    parts = MARK.split(text)
    # parts: [pre, tag, k, side, body, tag, k, side, body, ...]
    spreads = {}
    for i in range(1, len(parts), 4):
        tag, k, side, body = parts[i], int(parts[i + 1]), parts[i + 2], parts[i + 3]
        spreads.setdefault(k, {"left": "", "right": "", "single": ""})
        lines = [ln.rstrip() for ln in body.strip().splitlines()]
        # drop bare page-number footers and OCR watermark noise
        lines = [ln for ln in lines if ln.strip() and not FOOTNUM.match(ln)
                 and ln.strip() not in ("米花剧本", "花剧本", "米花")]
        clean = "\n\n".join(lines)
        if side == "左":
            spreads[k]["left"] = clean
        elif side == "右":
            spreads[k]["right"] = clean
        else:
            spreads[k]["single"] = clean
    return spreads


def get(spreads, k, side):
    s = spreads.get(k, {})
    v = s.get(side, "")
    if not v and s.get("single"):
        v = s["single"]
        s["single"] = ""   # consume once
    return v


for name, relmd, label, S, do_reorder in DOCS:
    spreads = parse(name)
    mdpath = os.path.join(OUT, relmd)
    if os.path.exists(mdpath):
        shutil.copy2(mdpath, os.path.join(BACKUP, os.path.basename(mdpath)))
    src = open(mdpath, encoding="utf-8").read()
    srcnote = re.search(r"> 来源：`([^`]+)`", src)
    source = srcnote.group(1) if srcnote else relmd

    if not do_reorder:
        continue

    order = []
    for k in range(1, S + 1):
        side = "right" if k % 2 else "left"
        order.append((k, k, side))
    for k in range(S, 0, -1):
        side = "left" if k % 2 else "right"
        order.append((2 * S + 1 - k, k, side))

    parts = ["# %s\n\n> 来源：`%s`\n"
             "> 原文件为骑马订 2-up 扫描（%d 张 A3 拼版 = %d 个印刷页），"
             "已按**印刷页 1→%d 的正确阅读顺序**重排。\n"
             "> 中文 OCR 自动识别（扫描件，可能有错字，重要内容请回看原 PDF）。\n"
             % (label, source, S, 2 * S, 2 * S)]
    plain = []
    empty = 0
    for pageno, k, side in order:
        body = get(spreads, k, side)
        cn = "左半页" if side == "left" else "右半页"
        parts.append("\n---\n\n## 印刷页 %d  ·  扫描第 %d 页%s\n\n" % (pageno, k, cn))
        if body.strip():
            parts.append(body + "\n")
            plain.append("[印刷页 %d]\n%s" % (pageno, body))
        else:
            parts.append("*（空白页 / 无文字）*\n")
            empty += 1
    open(mdpath, "w", encoding="utf-8").write("".join(parts))
    open(os.path.join(RAW, name + "_阅读顺序.txt"), "w", encoding="utf-8").write("\n\n".join(plain))
    print("REORDERED %-12s sheets=%d pages=%d empty=%d chars=%d" %
          (label, S, 2 * S, empty, sum(len(x) for x in plain)), flush=True)
