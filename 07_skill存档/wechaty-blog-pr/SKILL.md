---
name: wechaty-blog-pr
description: Submit a technical blog post to the Wechaty Contributor Program via GitHub Pull Request. Use when the user wants to publish a Wechaty-related blog to wechaty/jekyll in exchange for a Contributor Token. 触发词：投 Wechaty 博客、给 wechaty 提 PR、换 PadLocal Token、Wechaty Contributor Program。
---

# Wechaty 博客 PR 提交

## When to Use

- User has written a Wechaty-related technical blog and wants to submit it to the Wechaty Contributor Program.
- Goal is to obtain a free Wechaty Contributor Token (e.g., PadLocal puppet token) by publishing a blog post.

## Important Correction

The target repository is **https://github.com/wechaty/jekyll**, not `wechaty/wechaty.js.org`. The old name `wechaty.js.org` now redirects to `wechaty/jekyll`. Always fork and PR against `wechaty/jekyll`.

## Workflow

### 1. Verify or Create Fork

Check if the user already has a fork:

```bash
gh repo view <username>/jekyll --json name,parent
```

If not, fork it:

```bash
gh repo fork wechaty/jekyll --clone=false --default-branch-only
```

### 2. Clone and Branch

```bash
git clone https://github.com/<username>/jekyll.git
cd jekyll
git remote add upstream https://github.com/wechaty/jekyll.git
git fetch upstream
git checkout -b <branch-name> upstream/main
```

Branch name convention: `blog-<short-topic>`.

### 3. Add Blog Post

Place the Markdown file in `jekyll/_posts/` with filename:

```
YYYY-MM-DD-<lowercase-hyphenated-title>.md
```

Example:

```bash
cp /path/to/blog-post.md jekyll/_posts/2026-08-10-wechaty-llm-wechat-group-feedback-collector.md
```

Front matter requirements:

```yaml
---
title: "Post Title"
author: <GitHub username>
date: YYYY-MM-DD
categories: tutorial
tags:
  - wechaty
  - <other-tags>
image: /assets/YYYY/MM-<slug>/<image-file>
---
```

### 4. Add Assets (Optional)

Place images in:

```
jekyll/assets/YYYY/MM-<slug>/
```

- SVG is accepted by the site; PNG/WebP are also fine.
- If using `scripts/fit-image.sh`, ImageMagick must be installed.
- Keep images under 1MB.

### 5. Add or Update Contributor Profile

Create `jekyll/_contributors/<GitHub-username>.md`:

```markdown
---
name: <display-name>
site: https://github.com/<username>
avatar: https://avatars.githubusercontent.com/u/<user-id>?v=4
bio: <short bio>
github: <username>
---

<short bio or contact info>
```

The GitHub user ID can be retrieved via:

```bash
gh api users/<username> --jq '.avatar_url'
```

### 6. Commit and Push

```bash
git add jekyll/_posts/ jekyll/_contributors/ jekyll/assets/YYYY/MM-<slug>/
git commit -m "Add blog: <Post Title>"
git push origin <branch-name>
```

### 7. Create Pull Request

```bash
gh pr create --repo wechaty/jekyll \
  --base main \
  --head <username>:<branch-name> \
  --title "Add blog: <Post Title>" \
  --body "<brief description>"
```

### 8. Sign CLA

After creating the PR, the CLAassistant bot will comment with a link. The user must sign the Contributor License Agreement before the PR can be merged.

## Common Pitfalls

1. **Wrong repo**: `wechaty/wechaty.js.org` is outdated; use `wechaty/jekyll`.
2. **Default branch**: Use `main`, not `master`.
3. **Git ref bug on Windows**: If `git fetch upstream` reports success but `upstream/main` does not exist, manually create the ref directory and file, or create the branch from the commit hash returned by `git ls-remote upstream main`.
4. **Filename case**: Blog post filenames must be lowercase English letters, numbers, and hyphens only.
5. **SVG conversion**: The site accepts SVG directly. Do not block the workflow trying to convert SVG to PNG if conversion tools are not readily available.

## After Merge

Wechaty maintainers will issue a Contributor Token (typically valid for up to one year). The user can then add it to their bot's `.env` file and start the bot.
