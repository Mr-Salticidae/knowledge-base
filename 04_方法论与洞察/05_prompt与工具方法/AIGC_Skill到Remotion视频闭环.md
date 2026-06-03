---
tags: [类型/协作工具链, 主题/视频剪辑, 主题/工具方法]
---
# AIGC Skill 到 Remotion 视频闭环

> 入档:2026-06-03
> 来源:`{Downloads}/AIGC_Skill_Exploration_Recap.md`
> 性质:AIGC Skill 探索复盘 / Codex Skill / Remotion 视频生产流程

## 一句话

**Codex Skill + Remotion 可以形成“笔记 / 结构 → TSX → 预览 → 微调 → MP4”的视频生产闭环，但关键不在于安装 Skill 本身，而在于把复杂 Skill 拆成可控项目、用反馈模板持续微调。**

## 探索目标

这次探索的目标不是单纯调研 Skill，而是验证一个可复用流程:

```text
调研 Skill
→ 安装 / 注册 Skill
→ 调用 Skill 生成视频结构或 TSX
→ 接入最小 Remotion 项目
→ 预览与微调
→ build 成 mp4
→ 为后续蒙眼剪辑法模板库打底
```

长期目标是把 [[蒙眼剪辑法_方法论笔记]] 的“人判断，AI 执行”逻辑接入程序化视频渲染，让 AIGC 视频生产从手工剪辑扩展到模板化生成。

## Skill 筛选原则

调研阶段重点看四类信号:

- GitHub Star 和维护活跃度;
- 是否有清晰文档;
- 是否是单文件 `Skill.md`;
- 是否依赖复杂仓库、helpers、FFmpeg、Python 或其他环境。

初步结论:

| Skill / 项目 | 判断 |
|---|---|
| `video-use` | 依赖 ffmpeg / helpers / Python,不适合直接用辅助工具安装 |
| `remotion-best-practices` | 单文件 TSX / Skill.md,适合实操测试 |
| `Generative-Media-Skills/md-to-video` | 集合 Skill,高 Star,md → 视频逻辑可参考 |
| `claude-youtube` | 偏视频脚本生成,适合 B 站短视频改编 |

一句话规则:

> 新手阶段优先选单文件、依赖少、可被最小项目承接的 Skill。

## 安装工具的边界

这次制作了辅助安装工具 `CodexSkillInstaller`:

- 支持 `Skill.md` 文件一键注册;
- 可检测 / 安装 FFmpeg;
- 升级为 GUI 中文版;
- 后续可支持 FFmpeg 自动下载、路径加入 `PATH`;
- 打包 EXE,方便小白用户直接运行。

工具源码已作为代码资产收录到 [[CodexSkillInstaller说明]]。

但复盘结论很明确:

> 辅助工具只适合单文件 Skill.md 的安装，不适合把复杂仓库直接变成可用 Skill。

复杂仓库仍然需要额外处理依赖、项目结构和运行环境。不要把“能复制 Skill.md”误判成“整个工作流已可运行”。

## Windows 实操坑位

这次环境:

- Windows 10;
- Node.js v24;
- npm v11;
- Codex 客户端;
- B 站账号用于发布测试。

遇到的问题:

- PowerShell 执行策略阻止 `npm.ps1`;
- `npm install` 报 `EUNSUPPORTEDPROTOCOL catalog:`;
- `video-use` 依赖复杂,无法直接用辅助安装工具处理。

应对策略:

```text
用 CMD 跑 npm
新建最小 Remotion 项目
把 Skill 生成的 TSX 接入项目
保持配置和逻辑分离
```

Remotion 类 Skill 不要直接追求“一键生成完整项目”。更稳定的方式是:

```text
npx create-video@latest
→ 得到最小可运行项目
→ 把 Skill 产出的 TSX / scene / config 接进去
→ 用 Remotion 自身命令预览和 build
```

## 视频生成闭环

生成 `aigc-tutorial.mp4` 的流程可以抽象为:

```text
Skill
→ TSX
→ Remotion preview
→ 反馈微调
→ Remotion build
→ mp4
```

这个流程成立的前提是项目结构清楚:

- `scenes` 负责内容段落;
- `config` 负责文字、颜色、时长、布局参数;
- 组件负责视觉呈现;
- build 阶段只做渲染，不再临时改结构。

## 微调问题与修正方向

初版视频常见问题:

- Step 卡片被裁切;
- 布局没有落地到安全区;
- 内容抽象,缺少真实操作感;
- 结尾缺乏总结信息;
- 动画抢信息。

修正策略:

- 调整安全区、边距、卡片高度;
- 文案本地化、中文化;
- 增加操作演示卡片,例如终端命令淡入;
- 结尾加验证结论卡片;
- 动画克制,信息优先;
- 用反馈模板指导 Codex 微调 TSX。

一句话:

> Remotion 视频微调的核心不是“多做动画”，而是让信息稳定落地。

## 反馈模板的作用

Skill 生成的第一版通常只能算结构草稿。真正让它可发布的是反馈模板。

反馈重点应固定在:

1. 布局是否裁切;
2. 中文文案是否自然;
3. 是否有真实操作感;
4. 是否能看懂每一步;
5. 结尾是否有验证结论;
6. 动画是否服务信息。

这和 [[蒙眼剪辑法_方法论笔记]] 的逻辑一致:

```text
AI 先给结构
人类判断问题
再把判断翻译成可执行反馈
```

## 可复用流程

```text
1. 选单文件 Skill 或低依赖 Skill
2. 用 CodexSkillInstaller 注册
3. 新建最小 Remotion 项目
4. 调用 Skill 生成 TSX / scenes / config
5. 接入项目并预览
6. 用反馈模板微调布局、文案、操作感和结尾
7. build mp4
8. 记录可复用模板和坑位
```

## 后续建设方向

这次探索后，后续可以继续沉淀:

- 蒙眼剪辑法模板库;
- Remotion TSX 组件库;
- 中文教程视频模板;
- 操作演示卡片组件;
- 字幕 / 旁白 / 音频接入;
- B 站短视频发布模板;
- 多片种、多模板组合的生成体系。

## 如何使用

当要把一篇笔记或流程说明做成视频时，先判断:

1. 内容是否适合被拆成 3-6 个 scene?
2. 是否需要真实操作演示?
3. 是否可以先用最小 Remotion 项目承接?
4. Skill 负责生成结构，还是也要负责视觉实现?
5. 反馈模板是否足够具体到布局、文案和结尾?

如果答案成立，就走本闭环，而不是直接让 AI “生成一个完整视频”。

## 关联文档

- 视频剪辑方法:[[蒙眼剪辑法_方法论笔记]]
- 视频生成约束:[[图生视频_ForwardOnly原则]]
- 图文到视频工作流:[[图片占位到视频替换的工作流_v1]]
- LLM 规划工作流:[[方法论笔记_LLM-plan卡点工作流_v1]]
- Skill 安装工具:[[CodexSkillInstaller说明]]
- 代码资产入口:[[代码资产索引]]
- 原始笔记底料:`{Downloads}/AIGC_Skill_Exploration_Recap.md`
