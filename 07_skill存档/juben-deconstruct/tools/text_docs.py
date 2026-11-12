# -*- coding: utf-8 -*-
"""Convert the text-layer PDF / DOCX / TXT sources into Markdown."""
import os, re, subprocess, sys
from docx import Document

ROOT = r"C:\Users\12258\Downloads\954虚拟游戏"
OUT = r"C:\Users\12258\WorkBuddy\2026-11-12-18-07-45\954虚拟游戏_MD"

os.makedirs(OUT + r"\03_开本资料", exist_ok=True)
os.makedirs(OUT + r"\04_线索总表", exist_ok=True)

# ---------- 1. 线索列表 PDF (has a real text layer) ----------
pdf = ROOT + r"\6人虚拟游戏\虚拟游戏线索列表.pdf"
raw = subprocess.check_output(["pdftotext", "-raw", pdf, "-"]).decode("utf-8", "replace")
pages = raw.split("\f")

CN = r"[\u4e00-\u9fff\u3000-\u303f‘’“”…，、；：？！（）《》]"
LISTY = re.compile(r"^(\d+[.\s]|20\d\d[.\-/]|\d{3,4}\s|[A-Za-z]{1,3}\d)")
HEADERS = ("虚拟世界线索", "现实世界线索", "其他线索")


def merge_lines(lines):
    """Join soft-wrapped Chinese lines, keep list-like / tabular lines separate."""
    out = []
    for ln in lines:
        ln = ln.rstrip()
        if not ln:
            continue
        if not out:
            out.append(ln)
            continue
        prev = out[-1]
        new_para = bool(LISTY.match(ln)) or bool(re.match(r"^第[一二三四五六七八九十]", ln))
        tabular = (" " in ln.strip()) or (" " in prev)
        prev_ends_open = (not re.search(r"[。！？：；]$", prev)
                          and bool(re.search(r"[\u4e00-\u9fff，、]$", prev)))
        next_starts_cn = bool(re.match(r"^[\u4e00-\u9fff‘’“「]", ln))
        if new_para or tabular or not prev_ends_open or not next_starts_cn:
            out.append(ln)
        else:
            out[-1] = prev + ln
    return out


sections, cur_section = [], None
for pi, page in enumerate(pages, 1):
    lines = [l.strip() for l in page.splitlines()]
    lines = [l for l in lines if l]
    if not lines:
        continue
    i = 0
    while i < len(lines):
        l = lines[i]
        if l in HEADERS:
            cur_section = l
            sections.append(("__HEADER__", pi, "", "", [l]))
            i += 1
            continue
        if l in ("编号 内容", "编号", "内容"):
            i += 1
            continue
        if re.fullmatch(r"\d{1,3}", l):
            num = l
            loc = lines[i + 1] if i + 1 < len(lines) else ""
            i += 2
            body = []
            while i < len(lines) and not re.fullmatch(r"\d{1,3}", lines[i]) \
                    and lines[i] not in HEADERS:
                body.append(lines[i])
                i += 1
            sections.append((cur_section, pi, num, loc, merge_lines(body)))
        else:
            sections.append((cur_section, pi, "", "", [l]))
            i += 1

md = ["# 虚拟游戏 · 线索总表\n",
      "> 来源：`6人虚拟游戏/虚拟游戏线索列表.pdf`（WPS 表格生成，含文字层，非 OCR）\n",
      "> 与 `开本资料/虚拟游戏售后资料/虚拟游戏线索列表.pdf` 内容完全相同（MD5 一致），已去重。\n",
      "> 按「编号 / 地点 / 内容」整理，保留原分行与措辞。\n"]
for sec, pi, num, loc, body in sections:
    if sec == "__HEADER__":
        md.append("\n---\n\n# %s\n" % body[0])
        continue
    if num:
        md.append("\n## 线索 %s · %s\n\n" % (num, loc))
    else:
        md.append("\n")
    md.append("\n".join(body) + "\n")
open(OUT + r"\04_线索总表\虚拟游戏线索列表.md", "w", encoding="utf-8").write("".join(md))

# ---------- 2. DOCX ----------
doc = Document(ROOT + r"\6人虚拟游戏\搜证补充说明.docx")
dmd = ["# 搜证补充说明\n",
       "> 来源：`6人虚拟游戏/搜证补充说明.docx`（与售后资料副本 MD5 一致，已去重）\n\n"]
for p in doc.paragraphs:
    t = p.text.strip()
    if t:
        dmd.append(t + "\n\n")
for ti, t in enumerate(doc.tables, 1):
    dmd.append("\n## 表格 %d\n\n" % ti)
    for ri, row in enumerate(t.rows):
        cells = [c.text.strip().replace("\n", " / ") for c in row.cells]
        dmd.append("| " + " | ".join(cells) + " |\n")
        if ri == 0:
            dmd.append("| " + " | ".join(["---"] * len(cells)) + " |\n")
    dmd.append("\n")
open(OUT + r"\03_开本资料\搜证补充说明.md", "w", encoding="utf-8").write("".join(dmd))

# ---------- 3. TXT ----------
txt = open(ROOT + r"\开本资料\虚拟游戏售后资料\勘误.txt", encoding="utf-8", errors="replace").read()
tmd = ["# 勘误 / 开本注意事项（官方售后）\n",
       "> 来源：`开本资料/虚拟游戏售后资料/勘误.txt`\n\n", "```text\n", txt.strip(), "\n```\n",
       "\n## 结构化要点\n\n",
       "| 项目 | 内容 |\n| --- | --- |\n",
       "| 凶手卡 | 发给 **简清**、**尹梦竹** |\n",
       "| 侦探卡 | 其余角色 |\n",
       "| 空信封 | 徐光 |\n",
       "| 开场前 | 把身份卡和规则放入角色对应信封 |\n",
       "| 第一轮搜证开始后 | 线索 32（205 药品室）与线索 33（后院）直接作为**公开线索**发放 |\n",
       "| BGM | 歌单搜「虚拟游戏BGM」；《Remember Me》用作看本 BGM，另两首用于结局 |\n"]
open(OUT + r"\03_开本资料\勘误与开本注意事项.md", "w", encoding="utf-8").write("".join(tmd))

print("OK: clue-list / docx / txt -> markdown")
print("clue sections:", len(sections))
