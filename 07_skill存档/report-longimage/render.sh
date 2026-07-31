#!/usr/bin/env bash
# 报告长图渲染 —— headless Chrome 两趟截图
#
# 用法:  bash render.sh <input.html> <output.png> [逻辑宽度=1120] [缩放=2]
#
# 为什么必须两趟:Chrome 的 --screenshot 只截 --window-size 那么大的视口,
# 内容更长就被直接切掉。所以第一趟用 --dump-dom 读页面自报的 scrollHeight,
# 第二趟才按精确高度截。页面里必须有这一行(母版已内置):
#     <script>document.title = "H" + document.documentElement.scrollHeight;</script>
#
# 注意:本脚本在 Git Bash 下跑。Windows 的 scp/ssh 在自动化会话里不可靠,Chrome 无此问题。

set -euo pipefail

IN="${1:?用法: bash render.sh <input.html> <output.png> [宽度] [缩放]}"
OUT="${2:?用法: bash render.sh <input.html> <output.png> [宽度] [缩放]}"
W="${3:-1120}"
SCALE="${4:-2}"

# ---- 定位 Chrome ----
# ⚠ 这里必须用 if,不能写成 [ -f "$p" ] && CHROME=.. && break —— set -e 下
#   循环体最后一条命令返回非 0 会直接终止脚本(找不到第一个候选就静默退出)。
CHROME=""
for p in \
  "/c/Program Files/Google/Chrome/Application/chrome.exe" \
  "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
  "/c/Program Files/Microsoft/Edge/Application/msedge.exe" \
  "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  "google-chrome" "chromium"
do
  if [ -f "$p" ]; then CHROME="$p"; break; fi
  if command -v "$p" >/dev/null 2>&1; then CHROME="$p"; break; fi
done
if [ -z "$CHROME" ]; then echo "✗ 找不到 Chrome/Edge,请手动改本脚本里的路径" >&2; exit 1; fi

# ---- file:// URL 需要绝对路径(Git Bash 下用 pwd -W 拿 Windows 盘符路径) ----
abspath() {
  local d b
  d="$(cd "$(dirname "$1")" && { pwd -W 2>/dev/null || pwd; })"
  b="$(basename "$1")"
  printf '%s/%s' "$d" "$b"
}
ABS_IN="$(abspath "$IN")"
ABS_OUT="$(abspath "$OUT")"
URL="file:///${ABS_IN#/}"

COMMON=(--headless --disable-gpu --no-sandbox --hide-scrollbars --virtual-time-budget=3000)

# ---- 第一趟:量高度 ----
H=$("$CHROME" "${COMMON[@]}" --window-size="$W",2000 --dump-dom "$URL" 2>/dev/null \
    | grep -o "<title>H[0-9]*</title>" | grep -o "[0-9]*" | head -1)

if [ -z "$H" ]; then
  echo "✗ 没读到页面高度。检查 HTML 末尾是否有:" >&2
  echo '    <script>document.title = "H" + document.documentElement.scrollHeight;</script>' >&2
  exit 1
fi
echo "① 量得内容高度 ${H}px"

# ---- 第二趟:按精确高度截 ----
"$CHROME" "${COMMON[@]}" \
  --force-device-scale-factor="$SCALE" \
  --window-size="$W","$H" \
  --screenshot="$ABS_OUT" "$URL" 2>&1 | tail -1

echo "② 出图 ${W}x${H} @${SCALE}x → $OUT"
echo
echo "⚠ 别跳过验收:必须裁头/中/尾三段回看,缩略图看不出字体回退和漏改的文案。"
echo "   python -c \"from PIL import Image;im=Image.open(r'$OUT');print(im.size);im.crop((0,0,im.size[0],1300)).save('_c1.png');im.crop((0,im.size[1]-900,im.size[0],im.size[1])).save('_c2.png')\""
