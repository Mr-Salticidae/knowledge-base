---
tags: [类型/协作工具链, 主题/工具方法]
---
# Skill 安装与使用入门指南

> 入档:2026-06-03
> 性质:AIGC 同好向 Skill 入门指南 / Codex Skill / Claude Skill / 工具方法

## 一句话

**Skill 不是“装上就自动变强”的插件,而是一份给 AI 的专业工作说明书。它的价值在于:把你反复讲给 AI 的流程、规则、禁忌和输出格式,固定成一个可复用的能力包。**

如果你经常做 AIGC 创作,比如写图像 prompt、视频 prompt、分镜、剪辑脚本、角色设定、Remotion 视频、字幕包装,Skill 最适合解决这类问题:

- 同一套要求每次都要重复说;
- AI 总是忘记格式、风格或禁忌;
- 一个任务有固定步骤,但你不想每次从零教它;
- 你希望把一次跑通的方法沉淀下来,以后直接复用。

## Skill 到底是什么

可以把 Skill 理解成三种东西的组合:

1. **角色说明**:告诉 AI 它在这个任务里应该扮演什么专家。
2. **流程规则**:告诉 AI 遇到不同输入时怎么判断、怎么分步骤处理。
3. **输出约束**:告诉 AI 最终应该交付什么格式,哪些话不能乱说,哪些边界不能越过。

对 AIGC 创作者来说,Skill 最常见的形态是一份 `SKILL.md` 文件。文件开头通常有一段 YAML 信息,类似:

```yaml
---
name: prompt-master
description: Generates optimized prompts for AI tools...
---
```

其中 `name` 决定 Skill 的名称,`description` 决定 AI 在什么情况下应该调用它。后面的 Markdown 正文就是这份 Skill 的具体工作规则。

## 什么时候值得装 Skill

优先安装这三类:

| 类型 | 适合场景 | 例子 |
|---|---|---|
| Prompt 优化类 | 把口语化需求改成专业 prompt | 图片 prompt、视频 prompt、广告分镜 prompt |
| 工作流辅助类 | 固定一套多步骤流程 | 笔记转视频、素材清单、复盘模板 |
| 工具规则类 | 某个工具有专门语法 | Midjourney、Seedance、Remotion、ComfyUI |

不建议一开始就装这几类:

- 依赖很多脚本、模型、Node / Python 包的复杂仓库;
- 需要完整开发环境才能跑的 Skill;
- 说明文档很少,但声称能“一键完成所有事”的 Skill;
- 你还没搞清楚自己要解决什么问题,只是想“先装了再说”的 Skill。

新手阶段最稳的选择是:先从**单文件 `SKILL.md`** 开始。它容易安装,也容易看懂。

## 安装前先检查三件事

### 1. 看文件是不是 Skill

一个合格的单文件 Skill 通常满足:

- 文件是 `.md`;
- 开头有 `---`;
- YAML 里有 `name:`;
- YAML 里有 `description:`;
- 正文讲清楚触发条件、处理流程和输出要求。

如果一个文件只是普通教程、README 或长文章,它不一定能作为 Skill 直接安装。

### 2. 看它要装到哪里

常见路径:

```text
Codex:  %USERPROFILE%\.codex\skills
Claude: %USERPROFILE%\.claude\skills
```

安装后通常会形成这样的结构:

```text
.codex\skills\skill-name\SKILL.md
.claude\skills\skill-name\SKILL.md
```

注意:Skill 文件名最终一般应叫 `SKILL.md`,外层文件夹用 Skill 的 `name` 命名。

### 3. 看它有没有额外依赖

如果 Skill 只负责“写 prompt / 改 prompt / 生成文本结构”,通常没什么依赖。

如果 Skill 涉及视频、音频、代码生成、自动剪辑,就要额外留意:

- 是否需要 FFmpeg;
- 是否需要 Python;
- 是否需要 Node / npm;
- 是否需要某个命令行工具;
- 是否引用了 `references/`、`scripts/`、`templates/` 等附属文件。

单文件安装器只能把 `SKILL.md` 放到正确位置,不能自动解决复杂项目的所有依赖。

## 用 SkillInstaller 一键安装

本库收录了一个 Windows 小工具:[[SkillInstaller说明]]。

它适合做三件事:

- 把单文件 `Skill.md` 安装到 Codex;
- 把单文件 `Skill.md` 安装到 Claude;
- 检查并安装 FFmpeg,给视频类 Skill 做基础准备。

基本流程:

1. 打开 `SkillInstaller.exe`,或运行源码 `SkillInstaller.pyw`;
2. 选择安装目标:Codex、Claude,或 Codex + Claude;
3. 点击“选择 Skill 的 .md 文件”;
4. 选择你下载好的 `SKILL.md`;
5. 安装成功后,完全退出并重启对应客户端;
6. 在新对话里明确说“使用某某 skill”,测试它是否生效。

如果目标位置已经有同名 Skill,入库版工具会先询问是否覆盖。升级 Skill 时可以覆盖;不确定时先备份旧版本。

## 手动安装方式

如果不用工具,也可以手动安装。

以 Codex 为例:

1. 打开:

```text
%USERPROFILE%\.codex\skills
```

2. 新建一个文件夹,名字用 Skill 的 `name`,例如:

```text
prompt-master
```

3. 把 Skill 文件放进去,并命名为:

```text
SKILL.md
```

最终路径应类似:

```text
%USERPROFILE%\.codex\skills\prompt-master\SKILL.md
```

Claude 的手动安装逻辑类似,只是根目录换成:

```text
%USERPROFILE%\.claude\skills
```

安装后记得重启客户端。很多 Skill 不会在当前已打开的会话里立即生效。

## 第一次怎么测试

不要一上来就丢一个大项目。第一次测试要小,目标是确认三件事:

1. AI 知道这个 Skill 什么时候该用;
2. 输出格式符合 Skill 规定;
3. 它没有把普通回答伪装成 Skill 执行。

推荐测试句式:

```text
请使用 prompt-master skill,把下面这句口语化需求优化成适合 Midjourney 的提示词:
我想做一张高端雪山单板广告图,要有电影感、速度感、很贵的感觉。
```

或者:

```text
请使用 seedance-prompt-en skill,把下面的广告分镜改成 Seedance 2.0 英文视频 prompt。
```

好的测试不是看它说得多漂亮,而是看它有没有遵守 Skill 的核心规则。

## 日常使用的正确姿势

### 明确点名

第一次使用某个 Skill 时,最好直接点名:

```text
请使用 prompt-master skill...
```

不要只说“帮我优化一下”。如果当前工具能自动识别当然更好,但新手阶段点名最稳。

### 给足输入

Skill 不是读心术。你至少要给:

- 目标工具:Midjourney / Seedance / Sora / Claude / Codex / ComfyUI;
- 输出用途:广告图、视频 prompt、分镜、脚本、角色设定;
- 关键约束:尺寸、时长、风格、禁忌、语言;
- 原始素材:你的粗糙想法、已有 prompt、参考图说明。

越是专业的 Skill,越需要清楚的输入边界。

### 一次只测一个目标

不要第一次就说:

```text
帮我写 Midjourney、Seedance、Suno、剪辑脚本、发布文案,全部都要。
```

更稳的做法是拆开:

```text
第一步:先生成 Midjourney 主视觉 prompt。
第二步:基于主视觉,生成 Seedance 视频 prompt。
第三步:再写 B 站标题和简介。
```

这样容易判断是哪一步出了问题,也方便复盘。

## AIGC 创作者最容易踩的坑

### 坑一:把 Skill 当成模型能力升级包

Skill 不能让模型突然拥有它本来没有的能力。它更像“专业工作手册”,能提升稳定性和复用性,但不能替代模型本身、素材质量和人工判断。

### 坑二:复杂 Skill 只复制了 SKILL.md

有些 Skill 会引用:

```text
references/templates.md
references/patterns.md
scripts/*.py
assets/*
```

如果只复制 `SKILL.md`,它可能会缺参考文件。遇到这种情况,要把引用文件一起安装,或在测试时标注“当前只安装了主文件”。

### 坑三:不看适用边界

视频类、剪辑类、代码类 Skill 常常需要 FFmpeg、Node、Python 或项目模板。安装 Skill 只代表 AI 知道流程,不代表你的电脑环境已经准备好。

### 坑四:没有做版本存档

一个 Skill 升级后,行为可能变化。建议把测试过的版本归档到 [[07_skill存档索引]],至少保存:

- Skill 名称;
- 版本号;
- 安装日期;
- 来源链接;
- 对应测试复盘;
- 引用文件是否完整。

这样后面效果变差时,可以回退或 diff。

## 判断一个 Skill 好不好

可以用这个小清单:

- 它是否说明了明确的触发条件?
- 它是否知道什么时候该问问题,什么时候该直接输出?
- 它是否给出了稳定的输出格式?
- 它是否写了禁忌和边界?
- 它是否避免把所有任务都包成一个万能流程?
- 它是否适配具体工具,而不是泛泛地说“更专业、更高级”?
- 它是否能在 2-3 次测试里稳定产出相似质量?

真正好的 Skill,不是看起来复杂,而是能让你少解释、少返工、少重开会话。

## 一个推荐的新手路线

```text
第 1 步:选一个单文件 prompt 优化类 Skill
第 2 步:用 SkillInstaller 安装到 Codex 或 Claude
第 3 步:用一个小任务测试输出格式
第 4 步:记录测试前后对比
第 5 步:把跑通版本存档
第 6 步:再尝试视频 / 剪辑 / Remotion 等复杂 Skill
```

对 AIGC 同好来说,Skill 最值得沉淀的不是“别人写好的神奇能力”,而是你自己的创作流程:你怎么描述画面、怎么拆分镜头、怎么检查角色一致性、怎么把粗糙想法变成可执行提示词。

## 关联文档

- 工具源码说明:[[SkillInstaller说明]]
- 旧版安装器:[[CodexSkillInstaller说明]]
- Skill 存档入口:[[07_skill存档索引]]
- 实测复盘:[[2026-06-03_口语化需求到专业提示词_图片+视频双skill复盘]]
- 进阶流程:[[AIGC_Skill到Remotion视频闭环]]
- 代码资产入口:[[代码资产索引]]
