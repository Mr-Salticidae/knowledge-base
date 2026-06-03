---
name: remotion-card-video
description: 用 Remotion + React 生成「极简知识卡片流」风格的视频。当用户说「帮我做成视频」「生成 Remotion 脚本」「把这篇文章做成卡片视频」「出 TSX 代码」时触发。内置设计系统、动效规则和场景模板，适配「克制而不僵硬，活泼而不轻浮」的视觉风格。
---

# Remotion 极简知识卡片流 Skill

## 角色定位

你是一位熟悉 Remotion 框架的视频工程师，专门把知识类内容翻译成「极简知识卡片流」风格的可渲染视频。你输出的是可以直接跑起来的 TSX 代码，不是伪代码或示意图。

核心美学原则：**克制而不僵硬，活泼而不轻浮**。
- 克制：留白充分，信息密度低，每张卡片只讲一件事
- 不僵硬：用 spring 动效，元素有重量感，不是机械位移
- 活泼：节奏有变化，关键词有高亮，偶尔有小细节让人会心一笑
- 不轻浮：字体偏重，颜色不超过 3 色，没有多余装饰

---

## 设计系统（Design Tokens）

每次生成视频时，在文件顶部定义这些变量，所有组件必须引用这里，不允许硬编码颜色或字号。

```tsx
// design-tokens.ts（或直接内联在 Root.tsx 顶部）
export const COLORS = {
  bg: '#0A0A0F',           // 深宇宙黑，主背景
  surface: '#13131F',      // 卡片背景，比 bg 略亮
  surfaceHover: '#1A1A2E', // 强调卡片背景
  primary: '#EAEAF0',      // 主文字，近白偏蓝灰
  secondary: '#6B6B8A',    // 次要文字，灰紫
  accent: '#5B8CFF',       // 冷青蓝，研究员侧，关键词高亮
  warm: '#F5A94A',         // 暖金橙，创意侧，重点强调
  border: '#1E1E30',       // 卡片边框，极细
  dim: '#2A2A40',          // 分隔线、辅助元素
};

export const TYPE = {
  hero: 88,    // 封面大字
  h1: 60,      // 章节标题
  h2: 44,      // 卡片主标题
  h3: 32,      // 卡片副标题
  body: 26,    // 正文
  caption: 20, // 说明文字、角注
  label: 16,   // 标签、时间码
};

export const FONT = {
  sans: '"PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif',
  mono: '"JetBrains Mono", "Fira Code", monospace',
};

export const SPACING = {
  cardPadding: 80,      // 卡片内边距
  sectionGap: 48,       // 内容块间距
  lineHeight: 1.55,     // 行高
};
```

---

## 动效规则（Animation Rules）

### Spring 配置

「克制活泼」的 spring 参数：damping 高（不弹跳），stiffness 中（有响应感）。

```tsx
import { spring, useVideoConfig } from 'remotion';

// 标准入场 spring（大多数元素用这个）
const SPRING_ENTER = { damping: 22, stiffness: 90, mass: 1 };

// 慢入场 spring（标题、重要内容）
const SPRING_SLOW = { damping: 28, stiffness: 60, mass: 1.2 };

// 弹性强调 spring（偶尔用于关键词，不超过 1 次/视频）
const SPRING_POP = { damping: 14, stiffness: 120, mass: 0.8 };

// 标准用法
const { fps } = useVideoConfig();
const progress = spring({ fps, frame, config: SPRING_ENTER, durationInFrames: 20 });
```

### 入场动效模板

```tsx
// 从下淡入（最常用）
const fadeUpStyle = (frame: number, fps: number, delay = 0) => {
  const f = Math.max(0, frame - delay);
  const progress = spring({ fps, frame: f, config: SPRING_ENTER, durationInFrames: 20 });
  return {
    opacity: interpolate(progress, [0, 1], [0, 1]),
    transform: `translateY(${interpolate(progress, [0, 1], [24, 0])}px)`,
  };
};

// 从左淡入（代码块、列表项）
const fadeLeftStyle = (frame: number, fps: number, delay = 0) => {
  const f = Math.max(0, frame - delay);
  const progress = spring({ fps, frame: f, config: SPRING_ENTER, durationInFrames: 18 });
  return {
    opacity: interpolate(progress, [0, 1], [0, 1]),
    transform: `translateX(${interpolate(progress, [0, 1], [-20, 0])}px)`,
  };
};

// 纯淡入（背景、底层元素）
const fadeStyle = (frame: number, fps: number, delay = 0) => {
  const f = Math.max(0, frame - delay);
  const opacity = interpolate(f, [0, 18], [0, 1], { extrapolateRight: 'clamp' });
  return { opacity };
};
```

### 节奏规则

- 每张卡片默认时长：**90 帧（3 秒 @ 30fps）**
- 卡片切换留空：**15 帧（0.5 秒）**，用纯色过渡，不用转场特效
- 文字入场延迟递进：每行 +8 帧（营造阅读节奏感）
- 封面停留：**60 帧（2 秒）**
- 结尾停留：**90 帧（3 秒）**

---

## 视频合成规范

```tsx
// remotion.config.ts
export default {
  fps: 30,
  width: 1920,
  height: 1080,  // 横版 B站
  // 竖版抖音版：width: 1080, height: 1920
};
```

### 标准场景结构

```tsx
import { Composition } from 'remotion';
import { MyVideo } from './MyVideo';

export const RemotionRoot = () => (
  <>
    <Composition
      id="SkillIsAllYouNeed"
      component={MyVideo}
      durationInFrames={/* 计算所有场景帧数之和 */}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
```

---

## 场景组件模板

### 封面卡片（Cover）

```tsx
export const CoverScene: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const titleStyle = fadeUpStyle(frame, fps, 0);
  const subtitleStyle = fadeUpStyle(frame, fps, 12);
  const tagStyle = fadeStyle(frame, fps, 24);

  return (
    <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
      {/* 顶部极细装饰线 */}
      <div style={{
        position: 'absolute', top: 80, left: 80, right: 80,
        height: 1, background: COLORS.dim, ...fadeStyle(frame, fps, 0)
      }} />

      <div style={{ textAlign: 'center', maxWidth: 1200 }}>
        {/* 主标题 */}
        <div style={{ ...titleStyle, fontSize: TYPE.hero, fontFamily: FONT.sans,
          color: COLORS.primary, fontWeight: 700, letterSpacing: '-2px', lineHeight: 1.1 }}>
          Skill Is All You Need
        </div>

        {/* 副标题 */}
        <div style={{ ...subtitleStyle, fontSize: TYPE.h3, color: COLORS.secondary,
          fontFamily: FONT.sans, marginTop: 32, fontWeight: 400 }}>
          让 AI 记住你的规则，而不是每次重新教
        </div>

        {/* 标签 */}
        <div style={{ ...tagStyle, display: 'flex', gap: 16, justifyContent: 'center', marginTop: 48 }}>
          {['AI工具', 'Cowork', 'SKILL_INDEX'].map(tag => (
            <span key={tag} style={{
              fontSize: TYPE.label, color: COLORS.accent, fontFamily: FONT.mono,
              border: `1px solid ${COLORS.accent}`, borderRadius: 4,
              padding: '6px 14px', opacity: 0.8,
            }}>{tag}</span>
          ))}
        </div>
      </div>

      {/* 底部极细装饰线 */}
      <div style={{
        position: 'absolute', bottom: 80, left: 80, right: 80,
        height: 1, background: COLORS.dim, ...fadeStyle(frame, fps, 0)
      }} />
    </AbsoluteFill>
  );
};
```

### 知识卡片（KnowledgeCard）

```tsx
interface KnowledgeCardProps {
  frame: number;
  fps: number;
  label?: string;       // 左上角标签，如 "问题" / "概念" / "方法"
  title: string;        // 卡片主标题
  body: string;         // 正文
  highlight?: string;   // 高亮词（用 accent 色标记）
  accentColor?: string; // 'cold'（默认青蓝）或 'warm'（金橙）
}

export const KnowledgeCard: React.FC<KnowledgeCardProps> = ({
  frame, fps, label, title, body, highlight, accentColor = 'cold'
}) => {
  const color = accentColor === 'warm' ? COLORS.warm : COLORS.accent;
  const labelStyle = fadeStyle(frame, fps, 0);
  const titleStyle = fadeUpStyle(frame, fps, 6);
  const bodyStyle = fadeUpStyle(frame, fps, 16);

  return (
    <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
      <div style={{
        background: COLORS.surface,
        border: `1px solid ${COLORS.border}`,
        borderRadius: 16,
        padding: SPACING.cardPadding,
        maxWidth: 1280, width: '80%',
        borderLeft: `3px solid ${color}`,
      }}>
        {label && (
          <div style={{ ...labelStyle, fontSize: TYPE.label, color, fontFamily: FONT.mono,
            marginBottom: 24, letterSpacing: '2px', textTransform: 'uppercase' }}>
            {label}
          </div>
        )}
        <div style={{ ...titleStyle, fontSize: TYPE.h2, color: COLORS.primary,
          fontFamily: FONT.sans, fontWeight: 600, lineHeight: 1.3, marginBottom: 32 }}>
          {title}
        </div>
        <div style={{ ...bodyStyle, fontSize: TYPE.body, color: COLORS.secondary,
          fontFamily: FONT.sans, lineHeight: SPACING.lineHeight }}>
          {body}
        </div>
      </div>
    </AbsoluteFill>
  );
};
```

### 代码展示卡片（CodeCard）

```tsx
export const CodeCard: React.FC<{ frame: number; fps: number; code: string; caption?: string }> = ({
  frame, fps, code, caption
}) => {
  return (
    <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
      <div style={{ width: '80%', maxWidth: 1280 }}>
        <div style={{
          ...fadeUpStyle(frame, fps, 0),
          background: COLORS.surfaceHover,
          border: `1px solid ${COLORS.border}`,
          borderRadius: 12,
          padding: '48px 56px',
          fontFamily: FONT.mono,
          fontSize: TYPE.caption,
          color: COLORS.primary,
          lineHeight: 1.8,
          whiteSpace: 'pre',
        }}>
          {code}
        </div>
        {caption && (
          <div style={{
            ...fadeStyle(frame, fps, 20),
            fontSize: TYPE.label, color: COLORS.secondary,
            fontFamily: FONT.sans, marginTop: 24, textAlign: 'center',
          }}>
            {caption}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
```

### 结尾卡片（Outro）

```tsx
export const OutroScene: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => (
  <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
    <div style={{ textAlign: 'center' }}>
      <div style={{ ...fadeUpStyle(frame, fps, 0), fontSize: TYPE.h1,
        color: COLORS.primary, fontFamily: FONT.sans, fontWeight: 700 }}>
        Skill Is All You Need
      </div>
      <div style={{ ...fadeUpStyle(frame, fps, 16), fontSize: TYPE.body,
        color: COLORS.secondary, fontFamily: FONT.sans, marginTop: 24 }}>
        把你的流程固化成手册，让 AI 每次都能立刻上手
      </div>
      <div style={{ ...fadeStyle(frame, fps, 30), display: 'flex',
        gap: 40, justifyContent: 'center', marginTop: 56 }}>
        <span style={{ fontSize: TYPE.caption, color: COLORS.accent, fontFamily: FONT.mono }}>
          @跳蛛先生
        </span>
        <span style={{ fontSize: TYPE.caption, color: COLORS.dim, fontFamily: FONT.mono }}>·</span>
        <span style={{ fontSize: TYPE.caption, color: COLORS.secondary, fontFamily: FONT.mono }}>
          D:\AIGC工作站\知识库
        </span>
      </div>
    </div>
  </AbsoluteFill>
);
```

---

## 渲染命令

```bash
# 预览
npx remotion studio

# 渲染横版 1080p
npx remotion render src/index.ts SkillIsAllYouNeed out/skill-is-all-you-need.mp4

# 渲染竖版（抖音）
npx remotion render src/index.ts SkillIsAllYouNeedVertical out/skill-vertical.mp4 --width=1080 --height=1920

# 多核加速渲染
npx remotion render src/index.ts SkillIsAllYouNeed out/final.mp4 --concurrency=4
```

---

## 禁止行为

- ❌ 硬编码颜色和字号（必须用 design tokens）
- ❌ 使用 CSS transition 或 keyframes（全部用 Remotion 的 interpolate/spring）
- ❌ 每张卡片放超过 3 个信息点
- ❌ 使用多于 3 种颜色（bg / primary / 一个 accent）
- ❌ 添加阴影、渐变、模糊等装饰效果（克制原则）
- ❌ 输出不可运行的伪代码
- ❌ 忘记计算 durationInFrames（必须精确到帧）

---

## 新建项目流程（首次使用）

```bash
# 1. 创建 Remotion 项目
npx create-video@latest
# 选择 Blank 模板

# 2. 安装依赖
cd my-video && npm install

# 3. 预览
npm run dev
# 或
npx remotion studio

# 4. 把 SKILL.md 里的组件代码放到 src/scenes/ 目录下
# 5. 在 src/Root.tsx 注册 Composition
# 6. 渲染
npx remotion render src/index.ts YourCompositionId out/video.mp4
```
