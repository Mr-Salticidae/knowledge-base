# -*- coding: utf-8 -*-
"""
Pass 0:本地知识库解析器(零风险,不碰飞书)

职责:
1. 扫描仓库所有 .md(排除 node_modules / .git / .obsidian / .claude)
2. 解析 frontmatter(tags)、首个 # 标题、双链 [[...]]
3. 建立 basename 索引,解析每条双链为:已解析 / 悬空 / 歧义
4. 把目录树映射成飞书 Wiki 节点树预览
5. 产出:
   - feishu_sync/_out/report.md        人类可读迁移报告
   - feishu_sync/_out/parse_data.json  机器可读(供 Pass 1/2 复用)
   - feishu_sync/_out/node_tree.txt     节点树预览

用法:python 06_代码/feishu_sync/pass0_parse.py
"""
import os
import re
import json
from collections import defaultdict

# ---- 配置 ----
# 仓库根:本脚本位于 06_代码/feishu_sync/,上两级即仓库根
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUT_DIR = os.path.join(SCRIPT_DIR, "_out")

# 技术垃圾目录(任一路径段命中即跳过)
EXCLUDE_DIRS = {".git", "node_modules", ".obsidian", ".claude", "_out", "__pycache__"}

# 迁移范围排除:不进飞书的顶层目录(skill 存档是工具源码,且是全部同名冲突来源)
SCOPE_EXCLUDE_TOP = {"07_skill存档"}

# 字面占位词:出现在文档里是「描述双链格式」的示范,不是真链接
PLACEHOLDER_TARGETS = {"文件名", "双链", "name", "their-name", "标题"}

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TAGS_RE = re.compile(r"tags:\s*\[(.*?)\]")


def rel(path):
    return os.path.relpath(path, REPO_ROOT).replace("\\", "/")


def walk_md():
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        # 原地裁剪排除目录
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        # 范围排除:跳过顶层不进飞书的目录
        rp_dir = rel(dirpath)
        top = rp_dir.split("/", 1)[0]
        if top in SCOPE_EXCLUDE_TOP:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.lower().endswith(".md"):
                yield os.path.join(dirpath, fn)


def parse_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    # 标题
    m = H1_RE.search(text)
    title = m.group(1).strip() if m else os.path.splitext(os.path.basename(path))[0]
    # tags
    tags = []
    fm = FRONTMATTER_RE.search(text)
    if fm:
        tm = TAGS_RE.search(fm.group(1))
        if tm:
            tags = [t.strip().strip('"\'' ) for t in tm.group(1).split(",") if t.strip()]
    # 所有标题(供概念链接分类)
    headings = [h.strip() for h in HEADING_RE.findall(text)]
    # 双链原始 token
    raw_links = WIKILINK_RE.findall(text)
    return {"title": title, "tags": tags, "raw_links": raw_links, "headings": headings}


def split_link(token):
    """拆 [[target|display#anchor]] -> (target_no_ext, display, anchor)"""
    token = token.strip()
    display = None
    anchor = None
    if "|" in token:
        token, display = token.split("|", 1)
        token, display = token.strip(), display.strip()
    if "#" in token:
        token, anchor = token.split("#", 1)
        token, anchor = token.strip(), anchor.strip()
    if token.lower().endswith(".md"):
        token = token[:-3]
    return token, display, anchor


def resolve_link(target, from_relpath, basename_index, path_index):
    """返回 (status, resolved_relpath_or_None)
    status: resolved / dangling / ambiguous"""
    if "/" in target or target.startswith(".."):
        # 当作路径:相对当前文件目录,再相对仓库根
        from_dir = os.path.dirname(from_relpath)
        candidates = [
            os.path.normpath(os.path.join(from_dir, target)).replace("\\", "/"),
            os.path.normpath(target).replace("\\", "/"),
        ]
        for c in candidates:
            key = c[:-3] if c.lower().endswith(".md") else c
            if key in path_index:
                return "resolved", path_index[key]
        return "dangling", None
    # 按 basename 解析
    hits = basename_index.get(target.lower())
    if not hits:
        return "dangling", None
    if len(hits) == 1:
        return "resolved", hits[0]
    return "ambiguous", hits  # 多个候选


def main():
    files = sorted(walk_md(), key=rel)
    parsed = {}
    basename_index = defaultdict(list)  # basename(lower) -> [relpath]
    path_index = {}                      # relpath_without_ext -> relpath

    all_headings = []  # 全库标题列表(小写),用于概念链接子串判定
    for p in files:
        rp = rel(p)
        base = os.path.splitext(os.path.basename(p))[0]
        basename_index[base.lower()].append(rp)
        path_index[rp[:-3] if rp.lower().endswith(".md") else rp] = rp
        parsed[rp] = parse_file(p)
        for h in parsed[rp]["headings"]:
            all_headings.append(h.lower())

    # 解析双链
    link_records = []  # 每条双链一条记录
    stats = {"resolved": 0, "dangling": 0, "ambiguous": 0, "total": 0}
    dangling_detail = defaultdict(list)   # target -> [来源文件]
    ambiguous_detail = []

    for rp, info in parsed.items():
        outlinks = []
        for raw in info["raw_links"]:
            target, display, anchor = split_link(raw)
            if not target:
                continue
            status, resolved = resolve_link(target, rp, basename_index, path_index)
            stats["total"] += 1
            stats[status] += 1
            rec = {"from": rp, "raw": raw, "target": target,
                   "display": display, "anchor": anchor,
                   "status": status, "to": resolved}
            link_records.append(rec)
            outlinks.append(rec)
            if status == "dangling":
                dangling_detail[target].append(rp)
            elif status == "ambiguous":
                ambiguous_detail.append(rec)
        info["outlinks"] = outlinks

    # 给悬空目标分类:占位 / 概念名 / 真缺失
    # 概念名 = 目标文本作为子串出现在某个标题里(标题常带「6. xxx ⭐」前后缀)
    heading_blob = "\n".join(all_headings)

    def classify(target):
        if target in PLACEHOLDER_TARGETS:
            return "占位"
        t = target.lower().strip()
        # 路径型目标(含 /)不当概念名
        if "/" not in t and len(t) >= 4 and t in heading_blob:
            return "概念名"
        return "真缺失"

    dangling_classified = {}
    for target in dangling_detail:
        dangling_classified[target] = classify(target)

    # basename 冲突(同名文件,会导致双链歧义)
    collisions = {b: v for b, v in basename_index.items() if len(v) > 1}

    # 目录树 -> 节点树预览
    tree = build_tree(files)

    os.makedirs(OUT_DIR, exist_ok=True)
    write_json(parsed, stats, link_records, collisions)
    write_report(files, parsed, stats, dangling_detail, ambiguous_detail,
                 collisions, dangling_classified)
    write_tree(tree)
    write_cleanup_csv(dangling_detail, dangling_classified)

    # 悬空分类计数(按出现次数)
    cat_count = defaultdict(int)
    for target, srcs in dangling_detail.items():
        cat_count[dangling_classified[target]] += len(srcs)

    # 控制台摘要(关键数字用 ASCII 标签,避免 Windows 终端 cp936 乱码)
    print("=" * 50)
    print(f"repo root : {REPO_ROOT}")
    print(f"docs      : {len(files)}  (excl. 07_skill archive)")
    print(f"wikilinks : {stats['total']}")
    print(f"  resolved: {stats['resolved']}")
    print(f"  dangling: {stats['dangling']}  "
          f"[real-missing={cat_count['真缺失']} "
          f"concept={cat_count['概念名']} placeholder={cat_count['占位']}]")
    print(f"  ambiguous:{stats['ambiguous']}")
    print(f"collisions: {len(collisions)}")
    print("=" * 50)
    print("out -> 06_代码/feishu_sync/_out/  (report.md / dangling_cleanup.csv / "
          "node_tree.txt / parse_data.json)")


def build_tree(files):
    root = {}
    for p in files:
        parts = rel(p).split("/")
        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node.setdefault("__files__", []).append(parts[-1])
    return root


def write_tree(tree, path=None):
    lines = []

    def rec(node, depth):
        for key in sorted(k for k in node if k != "__files__"):
            lines.append("  " * depth + "📁 " + key)
            rec(node[key], depth + 1)
        for fn in sorted(node.get("__files__", [])):
            lines.append("  " * depth + "📄 " + fn)

    rec(tree, 0)
    with open(os.path.join(OUT_DIR, "node_tree.txt"), "w", encoding="utf-8") as f:
        f.write("飞书 Wiki 节点树预览(📁=分组节点 / 📄=文档节点)\n\n")
        f.write("\n".join(lines))


def write_json(parsed, stats, link_records, collisions):
    data = {"stats": stats,
            "files": parsed,
            "links": link_records,
            "collisions": collisions}
    with open(os.path.join(OUT_DIR, "parse_data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_cleanup_csv(dangling_detail, dangling_classified):
    """导出悬空双链清理清单(可用 Excel/飞书表格打开手动修)"""
    import csv
    rows = []
    for target, srcs in dangling_detail.items():
        rows.append((dangling_classified[target], len(srcs), target,
                     " ; ".join(sorted(set(srcs)))))
    # 排序:真缺失优先,再按被引次数降序
    order = {"真缺失": 0, "概念名": 1, "占位": 2}
    rows.sort(key=lambda r: (order.get(r[0], 9), -r[1]))
    path = os.path.join(OUT_DIR, "dangling_cleanup.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["类型", "被引次数", "悬空目标", "来源文件(全部)"])
        w.writerows(rows)


def write_report(files, parsed, stats, dangling_detail, ambiguous_detail,
                 collisions, dangling_classified):
    # 分类计数
    cat = defaultdict(int)
    for t in dangling_detail:
        cat[dangling_classified[t]] += len(dangling_detail[t])
    L = []
    L.append("# Pass 0 解析报告 · 飞书迁移前体检\n")
    L.append("> 范围:已排除 `07_skill存档`(工具源码)与 node_modules\n")
    L.append(f"- 文档总数:**{len(files)}**")
    L.append(f"- 双链总数:**{stats['total']}**")
    L.append(f"  - ✅ 已解析:**{stats['resolved']}** "
             f"({pct(stats['resolved'], stats['total'])})")
    L.append(f"  - ❌ 悬空:**{stats['dangling']}** "
             f"({pct(stats['dangling'], stats['total'])}) — 指向不存在的目标,迁移后会是死链")
    L.append(f"  - ⚠️ 歧义:**{stats['ambiguous']}** — 同名文件多个候选,需人工指定")
    L.append(f"- 同名文件冲突:**{len(collisions)}** 组\n")

    L.append("## ❌ 悬空双链分类\n")
    L.append(f"- 🔴 **真缺失**(指向从不存在的文件,该修):**{cat['真缺失']}** 处")
    L.append(f"- 🟡 **概念名**(其实是别处的小标题,非独立文件):**{cat['概念名']}** 处")
    L.append(f"- ⚪ **占位**(文档里描述双链格式的示范文本,应忽略):**{cat['占位']}** 处")
    L.append("\n👉 完整清理清单见 **`dangling_cleanup.csv`**"
             "(Excel/飞书表格可直接打开,按类型+被引次数排好序)\n")
    L.append("### 真缺失 Top 50(按目标聚合)\n")
    L.append("迁移前建议先在本地修掉这些,否则飞书里会变成死链文字。\n")
    real_missing = {t: s for t, s in dangling_detail.items()
                    if dangling_classified[t] == "真缺失"}
    if real_missing:
        ranked = sorted(real_missing.items(), key=lambda kv: -len(kv[1]))
        L.append("| 目标(找不到) | 被引用次数 | 来源示例 |")
        L.append("|---|---|---|")
        for target, srcs in ranked[:50]:
            sample = srcs[0].split("/")[-1]
            L.append(f"| `{target}` | {len(srcs)} | {sample} |")
        if len(ranked) > 50:
            L.append(f"\n> 还有 {len(ranked) - 50} 个真缺失目标未列出,详见 CSV")
    else:
        L.append("_无真缺失,全部能解析或属概念名/占位 🎉_")

    L.append("\n## ⚠️ 歧义双链(同名多候选)\n")
    if ambiguous_detail:
        L.append("| 来源 | 双链 | 候选 |")
        L.append("|---|---|---|")
        for rec in ambiguous_detail[:30]:
            cands = " / ".join(rec["to"]) if isinstance(rec["to"], list) else rec["to"]
            L.append(f"| {rec['from'].split('/')[-1]} | `{rec['target']}` | {cands} |")
    else:
        L.append("_无_")

    L.append("\n## 同名文件冲突\n")
    if collisions:
        L.append("以下文件名重复,双链按 basename 解析时会歧义:\n")
        for b, v in sorted(collisions.items()):
            L.append(f"- `{b}`:")
            for x in v:
                L.append(f"  - {x}")
    else:
        L.append("_无_")

    with open(os.path.join(OUT_DIR, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def pct(a, b):
    return f"{(100.0 * a / b):.1f}%" if b else "0%"


if __name__ == "__main__":
    main()
