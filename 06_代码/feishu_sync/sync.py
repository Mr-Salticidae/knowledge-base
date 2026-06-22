# -*- coding: utf-8 -*-
"""
飞书知识库同步编排器(Pass 1 建树+上正文 / Pass 2 回填双链),幂等。

用法:
  python sync.py --poc            只同步三篇袋走行动复盘(POC,验证全链路)
  python sync.py                  全量(POC 跑通后再用)
  python sync.py --backfill-only  只跑 Pass 2 回填(已建好节点时)
  python sync.py --dry-run        只打印计划,不调飞书

幂等:state(feishu_sync_state.json)记 relpath→{hash,node_token,doc_token}。
重跑时内容 hash 未变且已有 node_token 的文档跳过;变了则更新正文。
本地为主,改完重跑即可刷新飞书镜像。
"""
import os
import sys
import json
import time
import hashlib
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
PARSE_DATA = os.path.join(SCRIPT_DIR, "_out", "parse_data.json")
STATE_PATH = os.path.join(SCRIPT_DIR, "feishu_sync_state.json")

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import md_transform as MT

POC_DOCS = [
    "03_prompt模板库/02_案例复盘/2026-05-18_街道塑料袋家庭获奖图复盘.md",
    "03_prompt模板库/02_案例复盘/2026-05-19_松果手榴弹获奖图复盘.md",
    "03_prompt模板库/02_案例复盘/2026-05-18_垃圾高尔夫球获奖图复盘.md",
]


def log(m): print(m, flush=True)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load_json(p, default):
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# ---------- 目录节点(分组占位) ----------
def ensure_dir_node(wiki, reldir, state, dry):
    """确保 reldir 及其所有上级在 wiki 里有分组节点,返回其 node_token。"""
    if reldir in ("", "."):
        return None  # 空间根
    if reldir in state["dirs"]:
        return state["dirs"][reldir]
    parent = ensure_dir_node(wiki, os.path.dirname(reldir).replace("\\", "/"),
                             state, dry)
    title = os.path.basename(reldir)
    if dry:
        log(f"  [dry] 建目录节点: {reldir}")
        tok = f"DRY_DIR_{reldir}"
    else:
        node = wiki.create_node(parent_node_token=parent, title=title)
        tok = node["node_token"]
        log(f"  + 目录节点 {reldir} -> {tok}")
    state["dirs"][reldir] = tok
    save_state(state)
    return tok


# ---------- 单篇文档:Pass 1 ----------
def sync_doc(wiki, relpath, files_meta, state, bi, pi, dry):
    abspath = os.path.join(REPO_ROOT, relpath.replace("/", os.sep))
    with open(abspath, "r", encoding="utf-8") as f:
        raw = f.read()
    h = sha(raw)
    prev = state["files"].get(relpath)
    if prev and prev.get("hash") == h and prev.get("node_token"):
        log(f"= 跳过(未变) {relpath.split('/')[-1]}")
        return
    new_text, st = MT.transform(raw, relpath, bi, pi)
    imgs = MT.extract_images(raw, relpath)
    # 内容变更:先删旧节点再重建(避免重复)
    if prev and not dry and prev.get("doc_token"):
        wiki.delete_doc(prev["doc_token"])
        log(f"  ~ 变更,删旧节点 {relpath.split('/')[-1]}")
    parent = ensure_dir_node(wiki, os.path.dirname(relpath).replace("\\", "/"),
                             state, dry)
    title = files_meta.get(relpath, {}).get("title") or \
        os.path.splitext(os.path.basename(relpath))[0]
    if dry:
        log(f"  [dry] 上正文 {title}  (双链->链接{st['linked']} 图{len(imgs)})")
        state["files"][relpath] = {"hash": h, "node_token": f"DRY_{relpath}",
                                   "doc_token": f"DRYDOC_{relpath}"}
        save_state(state)
        return

    # 上传 -> 导入 -> 轮询 -> 挂入 wiki
    fname = os.path.splitext(os.path.basename(relpath))[0] + ".md"
    mount = state.get("import_folder_token")
    if not mount:
        mount = wiki.app_root_folder()
        state["import_folder_token"] = mount
        save_state(state)
    file_token = wiki.upload_media_for_import(fname, new_text.encode("utf-8"))
    ticket = wiki.create_import_task(file_token, fname, mount)
    docx_token, _ = wiki.poll_import(ticket)
    node_token = wiki.move_doc_to_wiki(docx_token, parent_wiki_token=parent)
    state["files"][relpath] = {"hash": h, "node_token": node_token,
                               "doc_token": docx_token, "linked": st["linked"]}
    save_state(state)
    log(f"+ 上墙 {title} -> node={node_token}")
    if imgs:
        img_abs = [os.path.join(REPO_ROOT, a.replace("/", os.sep))
                   for _, _, a in imgs]
        done = wiki.embed_images(docx_token, img_abs)
        log(f"    + 嵌入图片 {done}/{len(imgs)}")
    colored = wiki.colorize_layer_blocks(docx_token)
    if colored:
        log(f"    + 四层标注上色 {colored} 条")


# ---------- Pass 2:回填双链 ----------
def backfill(wiki, relpath, state, dry):
    meta = state["files"].get(relpath)
    if not meta or not meta.get("doc_token"):
        return 0
    doc_id = meta["doc_token"]
    if dry:
        log(f"  [dry] 回填 {relpath.split('/')[-1]}")
        return 0
    blocks = wiki.list_blocks(doc_id)
    fixed = 0
    for b in blocks:
        # 块类型无关:找出该块里承载 elements 的字段(text/headingN/bullet/ordered/quote/...)
        container = None
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(v.get("elements"), list):
                container = v
                break
        elements = container.get("elements") if container else None
        if not elements:
            continue
        changed = False
        for el in elements:
            tr = el.get("text_run")
            if not tr:
                continue
            link = (tr.get("text_element_style") or {}).get("link")
            url = link.get("url") if link else None
            if not url:
                continue
            # Feishu 可能对 link.url 做了百分号编码,解码后再判前缀
            target = MT.decode_target(_url_unescape(url))
            if target is None:
                continue
            tgt_meta = state["files"].get(target + ".md")
            if tgt_meta and tgt_meta.get("node_token"):
                real = wiki.wiki_url(tgt_meta["node_token"])
                # Feishu 存储时会自行编码,这里写明文 URL
                tr["text_element_style"]["link"]["url"] = real
                changed = True
            else:
                # 目标未同步(POC 子集外):降级为纯文本(去链接)
                tr.get("text_element_style", {}).pop("link", None)
                changed = True
        if changed:
            wiki.patch_block_elements(doc_id, b["block_id"], elements)
            fixed += 1
    log(f"~ 回填 {relpath.split('/')[-1]}: 改 {fixed} 块")
    return fixed


def _url_escape(u):
    from urllib.parse import quote
    return quote(u, safe="")


def _url_unescape(u):
    from urllib.parse import unquote
    return unquote(u)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--poc", action="store_true")
    ap.add_argument("--backfill-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data = load_json(PARSE_DATA, None)
    if not data:
        raise SystemExit("缺 parse_data.json,先跑 pass0_parse.py")
    files_meta = data["files"]
    relpaths = list(files_meta.keys())
    bi, pi = MT.build_index(relpaths)

    targets = POC_DOCS if args.poc else relpaths
    log(f"同步范围: {len(targets)} 篇  {'(POC)' if args.poc else '(全量)'}"
        f"{'  [dry-run]' if args.dry_run else ''}")

    state = load_json(STATE_PATH, {"version": 1, "dirs": {}, "files": {}})

    wiki = None
    if not args.dry_run:
        from feishu_wiki import FeishuWiki
        wiki = FeishuWiki()
        if not wiki.space_id:
            raise SystemExit("feishu_config.json 缺 target_space_id(成员加成功后填)")
        state.setdefault("space_id", wiki.space_id)

    failures = []
    if not args.backfill_only:
        log(f"\n--- Pass 1: 建树 + 上正文 ({len(targets)}) ---")
        for n, rp in enumerate(targets, 1):
            try:
                sync_doc(wiki, rp, files_meta, state, bi, pi, args.dry_run)
            except Exception as e:
                failures.append((rp, "pass1", str(e)))
                log(f"  ✗ [{n}/{len(targets)}] 跳过(出错) {rp.split('/')[-1]}: {e}")

    log("\n--- Pass 2: 回填双链 ---")
    total = 0
    for rp in targets:
        try:
            total += backfill(wiki, rp, state, args.dry_run) if wiki else 0
            if args.dry_run:
                backfill(None, rp, state, True)
        except Exception as e:
            failures.append((rp, "pass2", str(e)))
            log(f"  ✗ 回填出错 {rp.split('/')[-1]}: {e}")

    log(f"\n完成。回填改块合计 {total}。成功 {len(state['files'])} 篇,"
        f"失败 {len(failures)} 篇。state -> {os.path.basename(STATE_PATH)}")
    if failures:
        log("失败清单(重跑可续传):")
        for rp, ph, err in failures:
            log(f"  - [{ph}] {rp}: {err[:80]}")


if __name__ == "__main__":
    main()
