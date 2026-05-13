"""
《凝视 The Gaze》Day 2 - VERITIA 184 秒独白剧场 · 配置文件

时间线(15 段分镜,基于跳蛛先生人耳确认的 BGM 卡点 18s/100-110s/166s):

  PROLOGUE (静默铺垫,0-15s)
    01  0.0  -  3.0s   字幕      VERITIA / 06 / 06
    02  3.0  -  9.0s   Nano A1   王座厅广角(她坐其上)
    03  9.0  - 15.0s   Seed V-01 王座戏(听见远处声响,微微抬眼)

  第一幕:傀儡(15-50s)— 18s 情绪爆发
    04  15.0 - 22.0s   Nano A2   案桌签诏(她签别人写的诏书)    字幕"王冠会碎"18s 浮现
    05  22.0 - 32.0s   Nano A3   戴冠歪斜(王冠特写,镶嵌松脱)
    06  32.0 - 50.0s   Seed V-02 傀儡座位漫长等待

  第二幕:看见(50-100s)— 第一波 climax
    07  50.0 - 65.0s   Nano A4   抬眼望画外
    08  65.0 - 85.0s   Nano A5   镜中王朝崩塌(镜面映出真相)    字幕"镜子会骗"70s 浮现
    09  85.0 -100.0s   Nano A6   紧闭的嘴 + 锐利的眼

  幕间:脆弱(100-110s)— 能量回落
    10 100.0 -110.0s   Nano A7   合眼瞬间(她的瞬间脆弱)

  第三幕:反抗(110-166s)— 第二波 climax
    11 110.0 -122.0s   Nano V-02 王冠破碎(已生成)
    12 122.0 -145.0s   Seed V-03 玻璃裂纹蔓延                 字幕"但我相信,眼见为实"130s 浮现
    13 145.0 -166.0s   Nano V-04 玻璃末帧凝视(已生成)

  余韵 + 收尾(166-184s)
    14 166.0 -180.0s   Nano V-05 残破空王座
    15 180.0 -184.0s   字幕      THE GAZE / 凝视
"""

import platform
from pathlib import Path
from dataclasses import dataclass


# ============================================================
# 版本号
# ============================================================

VERSION = "v0"


# ============================================================
# 路径
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_STATIC = PROJECT_ROOT / "Day_2_素材"
ASSETS_VIDEO = PROJECT_ROOT / "Day_2_视频段"
ASSETS_BGM = PROJECT_ROOT / "Day_2_BGM"
OUTPUT_DIR = PROJECT_ROOT / "Day_2_输出"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

VERITIA_DIR = PROJECT_ROOT / "Veritia"
PLACEHOLDER_HALFBODY = VERITIA_DIR / "半身像.png"
PLACEHOLDER_FULLBODY = VERITIA_DIR / "全身像.png"


# ============================================================
# 字体
# ============================================================

def _resolve_fonts():
    sys_name = platform.system()

    if sys_name == "Windows":
        candidates = [
            (r"C:\Windows\Fonts\msyh.ttc", 0, r"C:\Windows\Fonts\msyh.ttc", 0,
             r"C:\Windows\Fonts\msyh.ttc", 0),
            (r"C:\Windows\Fonts\msyhl.ttc", 0, r"C:\Windows\Fonts\msyhl.ttc", 0,
             r"C:\Windows\Fonts\msyh.ttc", 0),
            (r"C:\Windows\Fonts\simhei.ttf", 0, r"C:\Windows\Fonts\simhei.ttf", 0,
             r"C:\Windows\Fonts\simsun.ttc", 0),
        ]
    elif sys_name == "Darwin":
        candidates = [
            ("/System/Library/Fonts/PingFang.ttc", 0, "/System/Library/Fonts/PingFang.ttc", 1,
             "/System/Library/Fonts/PingFang.ttc", 0),
        ]
    else:
        candidates = [
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Light.ttc", 2,
             "/usr/share/fonts/opentype/noto/NotoSansCJK-DemiLight.ttc", 2,
             "/usr/share/fonts/opentype/noto/NotoSerifCJK-ExtraLight.ttc", 2),
            ("/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 0,
             "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 0,
             "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf", 0),
        ]

    for cand in candidates:
        if Path(cand[0]).exists():
            return cand

    raise RuntimeError(f"找不到中文字体 ({sys_name})。")


(FONT_EN, FONT_EN_INDEX,
 FONT_EN_REG, FONT_EN_REG_INDEX,
 FONT_CN, FONT_CN_INDEX) = _resolve_fonts()


# ============================================================
# 视频规格
# ============================================================

RESOLUTION = (1080, 1920)
FPS = 30
TOTAL_DURATION = 184.000     # 跟随 Crown_Crack_Silence.wav 的精确时长


# ============================================================
# 分镜时间线(15 段)
# ============================================================

@dataclass
class Shot:
    idx: int
    start: float
    end: float
    kind: str              # 'title' | 'ai_video' | 'static_image'
    asset: object
    desc: str
    placeholder: object = None

    @property
    def duration(self) -> float:
        return self.end - self.start


SHOTS = [
    # PROLOGUE — 静默铺垫
    Shot(1,  0.0,   3.0,   'title',        None,
         "开场字幕 VERITIA / 06 / 06"),
    Shot(2,  3.0,   9.0,   'static_image', ASSETS_STATIC / "Veritia_A1_王座厅广角.png",
         "A1 王座厅广角(她坐其上)"),
    Shot(3,  9.0,   15.0,  'ai_video',     ASSETS_VIDEO / "V-01_王座戏.mp4",
         "V-01 王座戏(听见远处声响,微微抬眼)",
         placeholder=PLACEHOLDER_HALFBODY),

    # 第一幕:傀儡 — 18s 卡点情绪爆发
    Shot(4,  15.0,  22.0,  'static_image', ASSETS_STATIC / "Veritia_A2_案桌签诏.png",
         "A2 案桌签诏(她签别人写的诏书)"),
    Shot(5,  22.0,  32.0,  'static_image', ASSETS_STATIC / "Veritia_A3_戴冠歪斜.png",
         "A3 戴冠歪斜(王冠特写,镶嵌松脱)"),
    Shot(6,  32.0,  50.0,  'ai_video',     ASSETS_VIDEO / "V-02_傀儡座位.mp4",
         "V-02 傀儡座位漫长等待 Seedance",
         placeholder=ASSETS_STATIC / "Veritia_A1_王座厅广角.png"),

    # 第二幕:看见 — 第一波 climax
    Shot(7,  50.0,  65.0,  'static_image', ASSETS_STATIC / "Veritia_A4_抬眼望画外.png",
         "A4 抬眼望画外"),
    Shot(8,  65.0,  85.0,  'static_image', ASSETS_STATIC / "Veritia_A5_镜中王朝崩塌.png",
         "A5 镜中王朝崩塌"),
    Shot(9,  85.0,  100.0, 'static_image', ASSETS_STATIC / "Veritia_A6_紧闭的嘴.png",
         "A6 紧闭的嘴 + 锐利的眼"),

    # 幕间:脆弱 — 100-110s 能量回落
    Shot(10, 100.0, 110.0, 'static_image', ASSETS_STATIC / "Veritia_A7_合眼瞬间.png",
         "A7 合眼瞬间(她的瞬间脆弱)"),

    # 第三幕:反抗 — 第二波 climax
    Shot(11, 110.0, 122.0, 'static_image', ASSETS_STATIC / "Veritia_V-02_王冠破碎.png",
         "V-02 王冠破碎"),
    Shot(12, 122.0, 145.0, 'ai_video',     ASSETS_VIDEO / "V-03_玻璃蔓延.mp4",
         "V-03 玻璃裂纹蔓延 Seedance",
         placeholder=ASSETS_STATIC / "Veritia_V-03_玻璃起手帧.png"),
    Shot(13, 145.0, 166.0, 'static_image', ASSETS_STATIC / "Veritia_V-04_玻璃末帧.png",
         "V-04 玻璃末帧凝视"),

    # 余韵 + 收尾
    Shot(14, 166.0, 180.0, 'static_image', ASSETS_STATIC / "Veritia_V-05_残破空王座.png",
         "V-05 残破空王座(余韵段)"),
    Shot(15, 180.0, 184.0, 'title',        None,
         "收尾字幕 THE GAZE / 凝视"),
]


# ============================================================
# 字幕计划(对应跳蛛先生人耳卡点)
# ============================================================

@dataclass
class Subtitle:
    text: str
    fade_in_at: float
    fade_in_duration: float
    hold_until: float
    fade_out_duration: float
    style: str = 'monologue'

    @property
    def total_duration(self) -> float:
        return (self.hold_until + self.fade_out_duration) - self.fade_in_at


SUBTITLES = [
    # 开场字幕
    Subtitle(
        text="VERITIA\n06 / 06",
        fade_in_at=0.4, fade_in_duration=0.6,
        hold_until=2.4, fade_out_duration=0.4,
        style='opening',
    ),
    # "王冠会碎" 18s 卡点(跳蛛先生人耳确认的情绪爆发点)
    # 17s 开始淡入,18s 完全显示,持续到 30s
    Subtitle(
        text="王冠会碎\nCrowns crack.",
        fade_in_at=17.0, fade_in_duration=1.0,
        hold_until=30.0, fade_out_duration=1.0,
        style='monologue',
    ),
    # "镜子会骗" 70s 浮现(第二幕中段,镜中真相镜头)
    Subtitle(
        text="镜子会骗\nMirrors lie.",
        fade_in_at=69.0, fade_in_duration=1.0,
        hold_until=83.0, fade_out_duration=1.0,
        style='monologue',
    ),
    # "但我相信,眼见为实" 130s 浮现(第三幕反抗段)
    Subtitle(
        text="但我相信,眼见为实\nBut I trust what I see.",
        fade_in_at=128.0, fade_in_duration=1.0,
        hold_until=158.0, fade_out_duration=2.0,
        style='monologue',
    ),
    # 收尾字幕
    Subtitle(
        text="THE GAZE\n凝视",
        fade_in_at=180.4, fade_in_duration=0.6,
        hold_until=183.0, fade_out_duration=1.0,
        style='ending',
    ),
]


# ============================================================
# 视觉参数
# ============================================================

KEN_BURNS_ZOOM = 0.06
GLITCH_DURATION = 0.08
GLITCH_OFFSET = 6

FONT_SIZE_OPENING = 96
FONT_SIZE_MONOLOGUE = 76
FONT_SIZE_MONOLOGUE_EN = 42
FONT_SIZE_ENDING = 88

LETTER_SPACING_OPENING = 4
LETTER_SPACING_MONOLOGUE = 2
LETTER_SPACING_ENDING = 3


# ============================================================
# BGM + 环境声
# ============================================================

# Suno v3 prompt 出的第一首,184.04s,选定为 Day 2 BGM
BGM_FILE = ASSETS_BGM / "Crown_Crack_Silence.wav"
ENV_SOUND_OPENING = ASSETS_BGM / "env_opening_dynasty_echo.wav"
ENV_SOUND_GLASS_CRACK = ASSETS_BGM / "env_glass_crack.wav"
ENV_SOUND_GLASS_BREAK = ASSETS_BGM / "env_glass_break.wav"
ENV_SOUND_ENDING = ASSETS_BGM / "env_ending_residual.wav"


# ============================================================
# 输出
# ============================================================

OUTPUT_NO_AUDIO = OUTPUT_DIR / f"凝视_Day2_{VERSION}_无音频.mp4"
OUTPUT_WITH_BGM = OUTPUT_DIR / f"凝视_Day2_{VERSION}_含BGM.mp4"
