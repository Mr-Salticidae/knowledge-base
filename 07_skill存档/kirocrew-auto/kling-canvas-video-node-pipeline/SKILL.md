---
name: auto/kling-canvas-video-node-pipeline
description: Generate a video shot in Kling web canvas via playwright-cli, download the blob, build a contact sheet and BGM review cut
triggers: kling canvas, playwright-cli video node, tiptap prompt fill, output.mp4 blob download, 主体库, 可灵画布, video node, 画布取视频, 配乐审片
source: auto
session_key: dashboard:chat-14-1792321418
created_at: 2026-10-20T04:18:00+00:00
version: 2
---

## When to use
Generating segments on the Kling web canvas through a persistent `playwright-cli -s=kling` window (user logs in once), one video node per segment, with local blockout video + reference images + a long prompt. The dashboard panel can't upload local files and doesn't share login. 生成 costs credits: click it only after the user confirms.

## Steps
1. Create node: double-click blank canvas, or click an existing node (panel keeps last params).
2. Upload refs in fixed order: `+` -> 本地上传 -> `playwright-cli -s=kling upload <img...> <blockout.mp4>`. They number 图片1/2.../视频1 by order. Poll ~20s, verify via `document.body.innerText.match(/(图片|视频|主体)\d/g)`.
3. Params: click the param pill, exact-match duration, 16:9, 1 条, 原声关, click empty canvas. Deselecting MAY reset params: reopen the node and read back `[textLen, params, refs]` before generating.
4. Prompt: editor is `.tiptap.ProseMirror`. Copy the one-line prompt to an ASCII scratch path first (CJK path reads/args fail), then click editor, Control+A, Backspace, `keyboard.insertText`. Read back `innerText()`.
5. Consistency via 主体库: one face image drifts to a generic 甜妹 face. Build a 主体 once (best face cover + 3 ffmpeg crops front/side/low-head from an approved film), attach it, @-mention it (Shift+Digit2). Keep negatives: no round face, no bangs, no big eyes, no skin smoothing, weak catchlights.
6. Generate: button label includes cost (match /324.*生成/). Check `kling account -q` before/after.
7. Fetch: wait until 创作中 disappears, open clip, scrape `performance.getEntriesByType('resource')` for `output.mp4` URL, download with the helper.
8. Review: contact sheet 1 frame/sec + BGM review cut (slice Cover master by global start/end, 0.15s fades, trim to length). Keep silent original.

## Gotchas
- Long single passes (30s/6 shots) reorder shots and pull far figures into foreground; split into short clips and stitch.
- After an interrupted turn or backend error, re-query 创作中/video count before re-clicking 生成 -- re-clicking double-charges.
- Use `--raw run-code` for exact JSON. Credits may expire monthly; warn before big runs.
- Keep reusable per-segment helpers (fill-prompt, download, contact-sheet, bgm-review).
