# scene_05 正式小片段实验生产包

## 目标

- 场景:`scene_05_markdown_structure`
- 命题:Skill 的物理形态通常是一个 Markdown 文件,由触发条件和工作规则组成。
- 工作流:Midjourney 生成关键视觉锚 -> Seedance 2.0 生成图内机制运动 -> Remotion 叠字幕和时间线。

## 本轮归档

Midjourney 主图:

```text
07_skill存档/remotion/public/assets/scene_05/mj_markdown_structure_key_visual.png
```

来源:

```text
C:\Users\Administrator\Downloads\mr_jumping_spider_premium_flat-vector_educational_explainer_i_44a127e2-77be-476a-adae-774574136e5d_1.png
```

Seedance 2.0 视频:

```text
07_skill存档/remotion/public/assets/scene_05/seedance_markdown_structure_motion.mp4
```

来源:

```text
C:\Users\Administrator\Downloads\jimeng-2026-06-08-8492- as the first frame and visual style ref....mp4
```

Remotion 输出:

```text
07_skill存档/remotion/out/scene05-motion-test.mp4
```

## 本轮分析

### 成立点

- Midjourney 主图的优点是关系干净:一个 `SKILL.md` 文件被上下层结构包围,箭头明确表达调用与回流。
- Seedance 输出最有效的部分在中段:`TRIGGER` 和 `WORKFLOW RULES` 被拆成两个功能层,这正好补上 Remotion 原生图形较难表现的结构分离过程。
- Remotion 包装后,字幕和外框保持统一,这一段可以和 `scene_04` 的视觉语言并列。

### 需要避开的点

- Seedance 视频开头主体靠近画面上缘,直接当片段开场会显得残缺。
- 制作时已用 MJ 静态图做开场视觉锚,再从 Seedance 有效段切入。
- Seedance 有效段结束后会留空,制作时已淡回 MJ 主图兜底。

### 制作结论

`scene_05` 适合作为第二个正式小片段验证:它证明了同一条工作流可以从"压缩成 Skill"迁移到"Skill 文件结构"。下一步可以继续测试 `scene_06_skill_index`,看图书馆索引隐喻是否也能用 MJ + Seedance 形成稳定机制动画。

## Midjourney Prompt

```text
premium flat-vector educational explainer illustration, a clean markdown document labeled SKILL.md in the center, the document is visibly split into two structured sections: a small top YAML header card labeled TRIGGER and a larger body card labeled WORKFLOW RULES, arrows show the YAML section deciding when to call the skill and the body section guiding how to execute the work, simple geometric UI cards, thick dark ink outlines, warm off-white paper background, restrained science explainer style, clear cause-and-effect composition, enough clean empty space at the bottom for subtitles, no photorealism, no anime, no realistic human faces, no 3D realism, no cinematic lighting, no tiny unreadable paragraphs, no logo, no watermark --ar 16:9 --style raw
```

保存目标:

```text
07_skill存档/remotion/public/assets/scene_05/mj_markdown_structure_key_visual.png
```

选择标准:

- `SKILL.md` 必须是第一眼能读出的主体。
- `TRIGGER` 和 `WORKFLOW RULES` 必须分别代表顶部触发区和正文规则区。
- 下方必须有稳定留白,便于 Remotion 字幕叠加。
- 优先选概念关系最清楚的一张,不是单张最炫的一张。

## Seedance 2.0 Prompt

上传素材:

```text
@Image1 = 选中的 Midjourney 主图
```

生成时长:5s

```text
@Image1 as the first frame and visual style reference. Create a 5-second premium flat-vector educational explainer animation based on @Image1. Keep the same warm off-white paper texture, thick dark ink outlines, simple geometric UI cards, SKILL.md document, TRIGGER header card, and WORKFLOW RULES body card. 0-1s: the SKILL.md document settles in the center with a subtle paper bounce; the camera stays mostly locked with a very slow push-in. 1-2.5s: the top YAML/TRIGGER header gently lifts upward and becomes a separate small card, while a thin arrow points from TRIGGER to a small call-decision icon. 2.5-4s: the lower WORKFLOW RULES body expands downward into stacked rule cards, with two or three clean line blocks appearing in sequence. 4-5s: the TRIGGER card and WORKFLOW RULES cards reconnect visually to the SKILL.md file, forming a stable two-layer structure. Leave the bottom area clean for Remotion subtitles. Style: premium editorial flat-vector science explainer, restrained motion, calm intelligent tone, no photorealism, no anime, no 3D realism, no realistic human faces, no extra text beyond SKILL.md, TRIGGER, WORKFLOW RULES, no logo, no watermark.
```

保存目标:

```text
07_skill存档/remotion/public/assets/scene_05/seedance_markdown_structure_motion.mp4
```

验收标准:

- 运动必须解释结构关系,不是只做镜头推拉。
- `TRIGGER` 和 `WORKFLOW RULES` 的分层关系必须清楚。
- 末帧要稳定,方便 Remotion 接字幕和转场。
- 不要新增人物、复杂背景、额外品牌字样或水印。
