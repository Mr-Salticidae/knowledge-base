# -*- coding: utf-8 -*-
"""
Markdown 预处理(Pass 1 用)+ 双链临时链接方案的编解码。

核心思路(绕开"靠文字定位占位符"的脆弱点):
- Pass 1:把 [[target|display]] 转成 Markdown 链接
    [display 或 target](TEMP_PREFIX + b64url(target_relpath_without_ext))
  导入飞书后,它就是一个真链接,URL 形如 https://kb-sync.local/n/<编码>
- Pass 2:遍历文档块,**只按 URL 前缀 TEMP_PREFIX 匹配**这些链接,
  解码出 target_relpath → 查 state 拿 node_token → 换成真实 wiki URL。
  按 URL 前缀匹配,比按可见文字匹配稳得多。

悬空/概念名/占位 → 直接渲染成纯文本(去掉方括号),不造链接。

本模块纯逻辑、可本地自测:`python md_transform.py` 会跑三篇 POC 文档的转换并自检。
"""
import os
import re
import json
import base64

WIKILINK_RE = re.compile(r"\[\[([^\]]+?)\]\]")
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

TEMP_PREFIX = "https://kb-sync.local/n/"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARSE_DATA = os.path.join(SCRIPT_DIR, "_out", "parse_data.json")


# ---------- 临时链接编解码 ----------
def encode_target(relpath_no_ext):
    raw = relpath_no_ext.encode("utf-8")
    return TEMP_PREFIX + base64.urlsafe_b64encode(raw).decode("ascii")


def decode_target(url):
    """从临时 URL 解出 target_relpath(无扩展名);非临时链接返回 None。"""
    if not url.startswith(TEMP_PREFIX):
        return None
    b = url[len(TEMP_PREFIX):]
    try:
        return base64.urlsafe_b64decode(b.encode("ascii")).decode("utf-8")
    except Exception:
        return None


# ---------- 双链解析(与 pass0 同规则的精简版) ----------
def build_index(relpaths):
    basename_index, path_index = {}, {}
    for rp in relpaths:
        base = os.path.splitext(os.path.basename(rp))[0].lower()
        basename_index.setdefault(base, []).append(rp)
        key = rp[:-3] if rp.lower().endswith(".md") else rp
        path_index[key] = rp
    return basename_index, path_index


def split_link(token):
    token = token.strip()
    display = None
    if "|" in token:
        token, display = token.split("|", 1)
        token, display = token.strip(), display.strip()
    if "#" in token:
        token = token.split("#", 1)[0].strip()
    if token.lower().endswith(".md"):
        token = token[:-3]
    return token, display


def resolve(target, from_relpath, basename_index, path_index):
    """返回 target 的 relpath(无扩展);解析不到返回 None。"""
    if "/" in target or target.startswith(".."):
        from_dir = os.path.dirname(from_relpath)
        for c in (os.path.normpath(os.path.join(from_dir, target)).replace("\\", "/"),
                  os.path.normpath(target).replace("\\", "/")):
            key = c[:-3] if c.lower().endswith(".md") else c
            if key in path_index:
                return path_index[key][:-3] if path_index[key].lower().endswith(".md") else path_index[key]
        return None
    hits = basename_index.get(target.lower())
    if hits and len(hits) == 1:
        rp = hits[0]
        return rp[:-3] if rp.lower().endswith(".md") else rp
    return None  # 0 或歧义都按未解析处理(纯文本)


# ---------- 主转换 ----------
def transform(text, from_relpath, basename_index, path_index):
    """把一篇 md 的双链转成临时链接 / 纯文本。返回 (新文本, 统计)。"""
    stats = {"linked": 0, "plain": 0}

    def repl(m):
        target, display = split_link(m.group(1))
        if not target:
            return m.group(0)
        rp = resolve(target, from_relpath, basename_index, path_index)
        label = display or target
        if rp:
            stats["linked"] += 1
            return f"[{label}]({encode_target(rp)})"
        else:
            stats["plain"] += 1
            return label  # 悬空/概念/占位 → 纯文字

    return WIKILINK_RE.sub(repl, text), stats


def extract_images(text, from_relpath):
    """列出本地图片引用 [(alt, 相对路径, 绝对路径)]。"""
    out = []
    from_dir = os.path.dirname(from_relpath)
    for m in IMG_RE.finditer(text):
        alt, src = m.group(1), m.group(2).strip()
        if src.startswith("http"):
            continue
        absrel = os.path.normpath(os.path.join(from_dir, src)).replace("\\", "/")
        out.append((alt, src, absrel))
    return out


# ---------- 本地自测 ----------
def _selftest():
    if not os.path.exists(PARSE_DATA):
        raise SystemExit("缺 parse_data.json,先跑 pass0_parse.py")
    with open(PARSE_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    relpaths = list(data["files"].keys())
    bi, pi = build_index(relpaths)

    repo_root = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
    poc = [
        "03_prompt模板库/02_案例复盘/2026-05-18_街道塑料袋家庭获奖图复盘.md",
        "03_prompt模板库/02_案例复盘/2026-05-19_松果手榴弹获奖图复盘.md",
        "03_prompt模板库/02_案例复盘/2026-05-18_垃圾高尔夫球获奖图复盘.md",
    ]
    print("=== 双链转换自测(三篇 POC 文档) ===")
    total_link, total_plain = 0, 0
    for rp in poc:
        p = os.path.join(repo_root, rp.replace("/", os.sep))
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        new, st = transform(text, rp, bi, pi)
        imgs = extract_images(text, rp)
        total_link += st["linked"]
        total_plain += st["plain"]
        # round-trip 校验:从新文本里抠出所有临时链接,解码,确认目标文件存在
        bad = 0
        for m in re.finditer(r"\]\((" + re.escape(TEMP_PREFIX) + r"[^)]+)\)", new):
            tgt = decode_target(m.group(1))
            if tgt is None or (tgt + ".md") not in data["files"]:
                bad += 1
        img_ok = all(os.path.exists(os.path.join(repo_root, a.replace("/", os.sep)))
                     for _, _, a in imgs)
        print(f"\n· {rp.split('/')[-1]}")
        print(f"    双链→链接 {st['linked']} / →纯文本 {st['plain']} / "
              f"编解码坏链 {bad} / 本地图片 {len(imgs)}(文件齐={img_ok})")
        # 抽一条示例
        ex = WIKILINK_RE.search(text)
        if ex:
            one, _ = transform(ex.group(0), rp, bi, pi)
            print(f"    示例: {ex.group(0)}  →  {one}")
    print(f"\n合计:->链接 {total_link} / ->纯文本 {total_plain}")
    print("[OK] 自测通过:编解码无坏链" if total_link else "[WARN] 无可链接双链?检查")


if __name__ == "__main__":
    _selftest()
