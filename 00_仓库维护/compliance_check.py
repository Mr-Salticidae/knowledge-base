#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库外来提交合规校验脚本

用途：在 PR 时（或本地手动）扫描知识库提交中常见的合规偏离，作为人工审核的
自动化前置关卡。检查项对应《外来提交PR审核清单》的可脚本化部分：

  1. 他机绝对路径污染（最高优先级，本次最痛点）
     - 判定收紧为：**索引/登记类文档**（*索引.md / SKILL_INDEX.md / README / AGENTS / CLAUDE）
       里出现「非作者机器」的绝对路径（C:\\Users\\<非 Administrator>、/home/、/Users/）。
     - 作者本人机器（C:\\Users\\Administrator）出现在复盘/档案类文档里，是合法的
       「库外裸路径」，不误报。
     - skill verbatim 归档（使用说明书等）允许保留，按文件名白名单排除。
  2. 索引表格列语义错位（启发式）
     - 索引表中「类型」列填入过长用途描述（> 30 字且含用途动词）→ 提示复核。
  3. frontmatter 单一颜色轴 + 双链带 .md
     - 跳过 README（颜色规范总表，天然罗列全部类型）与 skill 存档目录。

用法：
  python compliance_check.py            # 扫描全库
  python compliance_check.py --diff    # 仅扫描最近一次 commit 的变更（供 CI 用）

退出码：0 = 通过（或仅有提示）；1 = 发现他机路径污染（error 级，告警）。
"""

import os
import re
import sys
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 作者本人机器用户名（本机为 Administrator，出现这类路径视为合法库外裸路径）
AUTHOR_USERS = {'Administrator'}

# 索引/登记类文档关键字（这些文档里的路径必须指向库内，是污染高发区）
INDEX_KEYWORDS = ['索引.md', 'SKILL_INDEX.md', 'README.md', 'AGENTS.md', 'CLAUDE.md']

# 允许保留他机路径的文件（skill verbatim 归档内容，记录来源真实性）
ALLOWED_FOREIGN_FILES = ['使用说明书.md', '本机Skill部署与调用手册.md']

# 允许出现绝对路径的文档类型（复盘/档案类，库外产物用裸路径是规范允许的）
# 这类文件里出现 C:\Users\Administrator 是合法的，不检查


def get_all_md_files(root, only_diff=False):
    if not only_diff:
        files = []
        for dirpath, dirnames, filenames in os.walk(root):
            if '.git' in dirpath:
                continue
            for fn in filenames:
                if fn.endswith('.md'):
                    files.append(os.path.relpath(os.path.join(dirpath, fn), root))
        return files
    try:
        out = subprocess.check_output(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            cwd=root, text=True
        )
        return [f.strip() for f in out.splitlines() if f.strip().endswith('.md')]
    except Exception:
        return get_all_md_files(root, only_diff=False)


def is_index_file(relpath):
    return any(k in relpath for k in INDEX_KEYWORDS)


def is_allowed_foreign_file(relpath):
    return any(k in relpath for k in ALLOWED_FOREIGN_FILES)


def extract_foreign_user(path_text):
    """若路径含「非作者机器」的绝对路径，返回用户名；否则 None。"""
    # Windows: C:\Users\<name> 或 C:/Users/<name>
    m = re.search(r'[A-Za-z]:[\\/]Users[\\/]([^\\/\s]*)', path_text)
    if m:
        name = m.group(1).strip('`"')
        if name and name not in AUTHOR_USERS:
            return name
    # Linux/macOS: /home/<name> 或 /Users/<name>
    m = re.search(r'/(?:home|Users)/([^/\s]+)', path_text)
    if m:
        name = m.group(1).strip('`"')
        if name and name not in AUTHOR_USERS:
            return name
    return None


def check_foreign_paths(files):
    """检查一：他机绝对路径污染（仅索引/登记类文档，且非作者机器）。"""
    issues = []
    for relpath in files:
        if not is_index_file(relpath):
            continue
        if is_allowed_foreign_file(relpath):
            continue
        full = os.path.join(REPO_ROOT, relpath)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue
        for i, line in enumerate(lines, 1):
            user = extract_foreign_user(line)
            if user:
                issues.append(('error', relpath, i,
                               f'他机绝对路径(C:\\Users\\{user} 等)，应改为库内 E:\\knowledge-base\\ 路径'))
    return issues


def check_index_column_semantics(files):
    """检查二：索引表格列数不一致（列错位的可确定性信号，提示级）。

    注：「类型列填成用途描述」这类语义错位无法可靠脚本化（需理解表头语义，
    启发式必然误报），故保留在人工清单，脚本只查「行内列数 ≠ 表头列数」
    这种确定性错位。
    """
    issues = []
    for relpath in files:
        if not is_index_file(relpath):
            continue
        full = os.path.join(REPO_ROOT, relpath)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue
        header_cols = None
        for i, line in enumerate(lines, 1):
            if not line.lstrip().startswith('|'):
                continue
            # 跳过表格分隔行 |---|---|
            if re.match(r'^\s*\|[\s:\-|]+\|\s*$', line):
                continue
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if header_cols is None:
                header_cols = len(cells)
                continue
            if len(cells) != header_cols:
                issues.append(('warn', relpath, i,
                               f'表格列数({len(cells)})与表头({header_cols})不一致'))
    return issues


def check_frontmatter_and_links(files):
    """检查三：frontmatter 单一颜色轴 + 双链带 .md（跳过 README 与 skill 存档）。"""
    issues = []
    for relpath in files:
        # 跳过 README（颜色规范总表）与 skill 存档目录
        if relpath.endswith('README.md'):
            continue
        if '07_skill存档' in relpath:
            continue
        full = os.path.join(REPO_ROOT, relpath)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        # 单一颜色轴：仅检查 frontmatter 块内
        fm = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if fm:
            type_tags = re.findall(r'类型/([^,\s\]]+)', fm.group(1))
            if len(type_tags) > 1:
                issues.append(('warn', relpath, 0,
                               f'frontmatter 多类型轴({type_tags})，违反单一颜色轴'))
        # 双链带 .md（排除 SKILL.md 惯例）
        for m in re.finditer(r'\[\[([^\]]+\.md)\]\]', content):
            target = m.group(1)
            if 'SKILL.md' in target or 'skill' in target.lower():
                continue
            issues.append(('warn', relpath, 0, f'双链带 .md 后缀: {target}'))
    return issues


def main():
    only_diff = '--diff' in sys.argv
    full_mode = '--full' in sys.argv
    files = get_all_md_files(REPO_ROOT, only_diff=only_diff)

    if only_diff and not files:
        print('[compliance] 本次提交无 md 变更，跳过。')
        return 0
    print(f'[compliance] 检查 {len(files)} 个文件…')

    # 默认只跑确定性检查（他机路径污染）；--full 追加提示级诊断
    all_issues = []
    all_issues += check_foreign_paths(files)
    if full_mode:
        all_issues += check_index_column_semantics(files)
        all_issues += check_frontmatter_and_links(files)

    if not all_issues:
        print('[compliance] ✅ 未发现合规偏离。')
        return 0

    errors = [x for x in all_issues if x[0] == 'error']
    warns = [x for x in all_issues if x[0] == 'warn']

    print(f'[compliance] 发现 {len(errors)} 项违规 / {len(warns)} 项提示：\n')
    for sev, relpath, lineno, detail in all_issues:
        tag = '❌' if sev == 'error' else '⚠️ '
        print(f'  {tag} {relpath}:{lineno}  {detail}')

    if errors:
        print('\n[compliance] ❌ 检测到他机路径污染，需修正后再合并。')
        return 1
    print('\n[compliance] ⚠️ 仅有提示级偏离，请人工复核《外来提交PR审核清单》。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
