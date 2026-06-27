#!/bin/bash
# AI 视频工作流 · Mac 一键安装
# 双击运行。如果双击没反应,见 02_安装_照着做一遍.md 里的 Mac 说明。

cd "$(dirname "$0")" || exit 1

echo ""
echo "============================================================"
echo "            AI 视频工作流 · Mac 一键安装"
echo "============================================================"
echo ""
echo "这个脚本会帮你自动装好地基:"
echo "   1) Claude Code   —— 你的 AI 总指挥"
echo "   2) Node.js       —— 剪辑台 Remotion 的运行底座"
echo "   3) FFmpeg        —— 处理音视频的引擎"
echo "   4) Python        —— 跑字幕等技术活要用"
echo "然后把整支\"技能乐队\"放到正确的位置。"
echo ""
echo "(画师/配音/作曲那几位是网上的在线服务,不在这里装,"
echo " 注册办法见 02_安装_照着做一遍.md 的 B 部分。)"
echo ""
echo "全程你只需要等待。中途可能让你输入开机密码(输入时屏幕不显示,正常)。"
echo "------------------------------------------------------------"
echo ""
read -r -p "准备好了就按回车开始..." _

# ---------- 第 0 步:确保有 Homebrew(Mac 软件管家) ----------
echo ""
echo "[检查] 正在确认是否已安装 Homebrew(Mac 软件管家)..."
if ! command -v brew >/dev/null 2>&1; then
    echo "    没找到 Homebrew,正在为你安装(可能要几分钟)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if [ -x /opt/homebrew/bin/brew ]; then eval "$(/opt/homebrew/bin/brew shellenv)"; fi
    if [ -x /usr/local/bin/brew ]; then eval "$(/usr/local/bin/brew shellenv)"; fi
fi
if ! command -v brew >/dev/null 2>&1; then
    echo ""
    echo "[!] Homebrew 还是没装上(可能网络问题)。"
    echo "    请把这句话发给帮你的朋友,或打开 02 安装教程看手动办法。"
    echo ""
    read -r -p "按回车关闭..." _
    exit 1
fi
echo "    OK,Homebrew 可用。"

# ---------- 装四件套 ----------
echo ""
echo "============================================================"
echo "[1/3] 安装 Node.js / FFmpeg / Python"
echo "============================================================"
brew install node ffmpeg python || echo "    [提示] 报\"already installed\"说明已装好,可忽略。"

echo ""
echo "============================================================"
echo "[2/3] 安装 Claude Code(AI 总指挥)"
echo "============================================================"
brew install --cask claude-code || echo "    [提示] 报已安装可忽略;若失败,02 教程里有备用办法。"

# ---------- 装整支技能乐队 ----------
echo ""
echo "============================================================"
echo "[3/3] 安装整支\"技能乐队\""
echo "============================================================"
SKILL_SRC="$(pwd)/skills"
SKILL_DST="$HOME/.claude/skills"
if [ ! -d "$SKILL_SRC" ]; then
    echo "    [!] 没在脚本旁边找到 skills 文件夹。"
    echo "        请确认你是把整个文件夹解压后,在里面双击本脚本的。"
else
    mkdir -p "$SKILL_DST"
    count=0
    for s in "$SKILL_SRC"/*/; do
        [ -d "$s" ] || continue
        name="$(basename "$s")"
        rm -rf "$SKILL_DST/$name"
        cp -R "$s" "$SKILL_DST/$name"
        count=$((count+1))
        echo "    已装技能:$name"
    done
    echo "    ---- 共安装 $count 个技能到:$SKILL_DST"
fi

# ---------- 收尾 ----------
echo ""
echo "============================================================"
echo "                     地基安装基本完成 ✅"
echo "============================================================"
echo ""
echo "还差两件事:"
echo ""
echo "【一】让总指挥认识你(登录,只需做一次)"
echo "   1) 关掉这个窗口"
echo "   2) 打开\"终端\"(在\"启动台\"里搜 终端 / Terminal)"
echo "   3) 输入下面这行,按回车:"
echo ""
echo "         claude"
echo ""
echo "   4) 它会自动打开浏览器让你登录,按提示完成即可。"
echo "      (需要 Claude 会员账号,详见 02 安装教程)"
echo ""
echo "【二】注册 AI 工具账号(配音 / 作曲 / 画师)"
echo "   见 02_安装_照着做一遍.md 的 B 部分。新手先备齐\"核心三件套\"即可。"
echo ""
echo "之后想做片子,照着 03_第一支片子_完整走一遍.md 来。"
echo ""
read -r -p "按回车关闭本窗口..." _
