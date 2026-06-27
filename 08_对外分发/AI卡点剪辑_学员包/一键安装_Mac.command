#!/bin/bash
# AI 卡点剪辑 · Mac 一键安装
# 双击运行。如果双击没反应,见 02_安装_照着做一遍.md 里的 Mac 说明。

cd "$(dirname "$0")" || exit 1

echo ""
echo "============================================================"
echo "            AI 卡点剪辑 · Mac 一键安装"
echo "============================================================"
echo ""
echo "这个脚本会帮你自动装好三样东西:"
echo "   1) Claude Code   —— 你的 AI 剪辑助理"
echo "   2) FFmpeg        —— 真正干剪辑活的引擎"
echo "   3) Python        —— AI 写的剪辑代码靠它运行"
echo "然后把\"剪辑技能说明书\"放到正确的位置。"
echo ""
echo "全程你只需要等待。中途可能让你输入开机密码(输入时屏幕不显示,是正常的)。"
echo "------------------------------------------------------------"
echo ""
read -r -p "准备好了就按回车开始..." _

# ---------- 第 0 步:确保有 Homebrew(Mac 上的软件管家) ----------
echo ""
echo "[检查] 正在确认是否已安装 Homebrew(Mac 软件管家)..."
if ! command -v brew >/dev/null 2>&1; then
    echo "    没找到 Homebrew,正在为你安装(这一步可能要几分钟)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # 让当前窗口立刻能用 brew(Apple 芯片和 Intel 芯片路径不同,都试一下)
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

# ---------- 第 1-3 步:装三件套 ----------
echo ""
echo "============================================================"
echo "[1/4] 安装 FFmpeg(剪辑引擎)和 Python(运行剪辑代码)"
echo "============================================================"
brew install ffmpeg python || echo "    [提示] 这一步若报\"already installed\"说明已装好,可忽略。"

echo ""
echo "============================================================"
echo "[2/4] 安装 Claude Code(AI 剪辑助理)"
echo "============================================================"
brew install --cask claude-code || echo "    [提示] 若报已安装可忽略;若失败,02 教程里有备用办法。"

# ---------- 第 4 步:安装技能说明书 ----------
echo ""
echo "============================================================"
echo "[3/4] 安装\"剪辑技能说明书\""
echo "============================================================"
SKILL_SRC="$(pwd)/skills/blind-editing-workflow"
SKILL_DST="$HOME/.claude/skills/blind-editing-workflow"
if [ ! -f "$SKILL_SRC/SKILL.md" ]; then
    echo "    [!] 没在脚本旁边找到 skills 文件夹。"
    echo "        请确认你是把整个文件夹解压后,在里面双击本脚本的。"
else
    mkdir -p "$HOME/.claude/skills"
    rm -rf "$SKILL_DST"
    cp -R "$SKILL_SRC" "$SKILL_DST"
    echo "    OK,技能已装到:$SKILL_DST"
fi

# ---------- 收尾 ----------
echo ""
echo "============================================================"
echo "                     安装基本完成 ✅"
echo "============================================================"
echo ""
echo "还差最后一步:让 AI 助理认识你(登录,只需做一次)"
echo ""
echo "   1) 关掉这个窗口"
echo "   2) 打开\"终端\"(在\"启动台\"里搜 终端 / Terminal)"
echo "   3) 输入下面这行,按回车:"
echo ""
echo "         claude"
echo ""
echo "   4) 它会自动打开浏览器让你登录,按提示完成即可。"
echo "      (需要 Claude 的会员账号,详见 02 安装教程)"
echo ""
echo "之后想做片子,就照着 03_第一支片子_完整走一遍.md 来。"
echo ""
read -r -p "按回车关闭本窗口..." _
