"""
《凝视 The Gaze》视频生成 - 配置文件
集中管理所有素材路径、分镜数据、视觉参数
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List

# ==================== 路径配置 ====================

BASE_DIR = Path("/mnt/user-data/outputs/the_gaze_series")
OUTPUT_DIR = Path("/mnt/user-data/outputs/the_gaze_video")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 字体
# 主字体:Noto Sans CJK 系列(开源,Google+Adobe出品,大字号清晰度优秀)
FONT_EN = "/usr/share/fonts/opentype/noto/NotoSansCJK-Light.ttc"        # 主标题用
FONT_EN_INDEX = 2  # SC variant
FONT_EN_REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-DemiLight.ttc"  # 中等字号用
FONT_EN_REG_INDEX = 2
FONT_CN = "/usr/share/fonts/opentype/noto/NotoSerifCJK-ExtraLight.ttc"
FONT_CN_INDEX = 2  # SC variant for Chinese

# ==================== 角色数据 ====================

@dataclass
class Character:
    """单个角色的所有元数据"""
    num: str                    # 编号 "01" - "06"
    name_en: str                # 英文名 "SCARLATTA"
    name_cn: str                # 中文名 "斯卡拉塔"
    monologue_cn: str           # 中文独白
    monologue_en: str           # 英文独白
    image_path: Path            # 图片路径
    color_theme: str            # 主题色描述(用于设计)
    
CHARACTERS = [
    Character(
        num="01",
        name_en="SCARLATTA",
        name_cn="斯卡拉塔",
        monologue_cn="我用这副面具,看清了所有摘下面具的人。",
        monologue_en="Behind this mask, I see yours fall.",
        image_path=BASE_DIR / "the_gaze_01_scarlatta.jpg",
        color_theme="crimson_silver",
    ),
    Character(
        num="02",
        name_en="VESPER",
        name_cn="薇斯珀",
        monologue_cn="黄昏不属于白天,也不属于夜晚——我也是。",
        monologue_en="I belong to neither side of the dusk.",
        image_path=BASE_DIR / "the_gaze_02_vesper.jpg",
        color_theme="black_silver",
    ),
    Character(
        num="03",
        name_en="NULL-07",
        name_cn="诺尔·零柒",
        monologue_cn="警告,视觉模块异常,身份认证失败。",
        monologue_en="[WARN] visual_module: anomaly detected\n[ERROR] auth.verify(): identity not recognized",
        image_path=BASE_DIR / "the_gaze_03_null-07.jpg",
        color_theme="cyber_blue_orange",
    ),
    Character(
        num="04",
        name_en="MORGANA",
        name_cn="摩尔加娜",
        monologue_cn="你的命运我已经看完了——你想从哪一页开始反抗?",
        monologue_en="I've read your fate. Where shall we begin to defy it?",
        image_path=BASE_DIR / "the_gaze_04_morgana.jpg",
        color_theme="purple_gold",
    ),
    Character(
        num="05",
        name_en="SELENWE",
        name_cn="瑟兰薇",
        monologue_cn="这片森林记得每一个猎人的脚步——包括他们最后那一步。",
        monologue_en="The forest remembers every hunter's last step.",
        image_path=BASE_DIR / "the_gaze_05_selenwe.jpg",
        color_theme="forest_green_silver",
    ),
    Character(
        num="06",
        name_en="VERITIA",
        name_cn="薇瑞蒂亚",
        monologue_cn="王冠会碎,镜子会骗——但我相信,眼见为实。",
        monologue_en="Crowns crack. Mirrors lie. But I trust what I see.",
        image_path=BASE_DIR / "the_gaze_06_veritia.jpg",
        color_theme="dark_red_aged_gold",
    ),
]

CHARS_BY_NUM = {c.num: c for c in CHARACTERS}

# ==================== 视频规格 ====================

# 抖音/小红书短视频:9:16 竖版
DOUYIN_RESOLUTION = (1080, 1920)
DOUYIN_FPS = 30

# B站长视频:16:9 横版(更普遍)或者 9:16 (沉浸感)
# 既然作品集是竖版,B站也用竖版 1080x1920 更能保留细节
BILIBILI_RESOLUTION = (1080, 1920)
BILIBILI_FPS = 30

# 视频时长目标
DOUYIN_DURATION = 15.0
BILIBILI_DURATION = 75.0

# ==================== 颜色配置 ====================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (200, 200, 200)
GRAY_MID = (150, 150, 150)
GRAY_DARK = (80, 80, 80)
