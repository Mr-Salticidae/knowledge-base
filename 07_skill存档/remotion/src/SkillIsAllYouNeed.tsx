import React from 'react';
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from 'remotion';
import { CoverScene } from './scenes/CoverScene';
import { KnowledgeCard } from './scenes/KnowledgeCard';
import { CodeCard } from './scenes/CodeCard';
import { OutroScene } from './scenes/OutroScene';

// 场景帧偏移常量
const S = {
  cover:   { from: 0,    dur: 60  },  // 0–60    · 2s  · 封面
  s1:      { from: 60,   dur: 150 },  // 60–210  · 5s  · AI 每天失忆
  s2:      { from: 210,  dur: 150 },  // 210–360 · 5s  · 岗位手册比喻
  s3:      { from: 360,  dur: 150 },  // 360–510 · 5s  · Skill 是什么
  s4:      { from: 510,  dur: 150 },  // 510–660 · 5s  · 什么时候用
  s5:      { from: 660,  dur: 150 },  // 660–810 · 5s  · 旧方法的问题
  s6:      { from: 810,  dur: 210 },  // 810–1020 · 7s · SKILL_INDEX
  s7:      { from: 1020, dur: 210 },  // 1020–1230 · 7s · 三步上手
  s8:      { from: 1230, dur: 150 },  // 1230–1380 · 5s · 实测结果
  outro:   { from: 1380, dur: 120 },  // 1380–1500 · 4s · 结尾
};

export const TOTAL_FRAMES = 1500;

export const SkillIsAllYouNeed: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      {/* Scene 0 · 封面 */}
      <Sequence from={S.cover.from} durationInFrames={S.cover.dur}>
        <CoverScene frame={frame - S.cover.from} fps={fps} />
      </Sequence>

      {/* Scene 1 · AI 每天失忆 */}
      <Sequence from={S.s1.from} durationInFrames={S.s1.dur}>
        <KnowledgeCard
          frame={frame - S.s1.from} fps={fps}
          label="问题"
          title="你的 AI 每天都在失忆"
          body={[
            '每次开新对话，它就忘了你喜欢的格式、',
            '你反复强调的规则、上次踩过的坑。',
            '你得从头教。',
          ]}
          accentColor="cold"
        />
      </Sequence>

      {/* Scene 2 · 岗位手册比喻 */}
      <Sequence from={S.s2.from} durationInFrames={S.s2.dur}>
        <KnowledgeCard
          frame={frame - S.s2.from} fps={fps}
          label="比喻"
          title="Skill 就是它的岗位手册"
          body={[
            '你雇了一位助理，很聪明，但每次上班前都失忆了。',
            'Skill 就是你给它的那本手册——',
            '角色、规则、禁忌、输出格式，全部写死在里面。',
          ]}
          accentColor="cold"
        />
      </Sequence>

      {/* Scene 3 · Skill 是什么 */}
      <Sequence from={S.s3.from} durationInFrames={S.s3.dur}>
        <KnowledgeCard
          frame={frame - S.s3.from} fps={fps}
          label="概念"
          title="一个 .md 文件，三件事"
          body={[
            '① 角色说明 — 它在这个任务里是什么专家',
            '② 流程规则 — 遇到不同输入怎么处理',
            '③ 输出约束 — 交付什么格式，哪些话不能乱说',
          ]}
          accentColor="cold"
        />
      </Sequence>

      {/* Scene 4 · 什么时候用 */}
      <Sequence from={S.s4.from} durationInFrames={S.s4.dur}>
        <KnowledgeCard
          frame={frame - S.s4.from} fps={fps}
          label="判断"
          title="当你反复在教 AI 同一件事"
          body={[
            'Prompt 优化类 → 每次都要重新说规则',
            '工作流辅助类 → 固定步骤每次都一样',
            '工具语法类   → 不想每次查文档',
          ]}
          accentColor="warm"
        />
      </Sequence>

      {/* Scene 5 · 旧方法的问题 */}
      <Sequence from={S.s5.from} durationInFrames={S.s5.dur}>
        <KnowledgeCard
          frame={frame - S.s5.from} fps={fps}
          label="问题"
          title="装上去的 Skill 下次可能找不到"
          body={[
            'Cowork 每次启动都会生成一串随机编号（UUID）。',
            '安装路径跟着变，Skill 就失联了。',
            '就像把手册锁进了每天换地址的保险柜。',
          ]}
          accentColor="cold"
        />
      </Sequence>

      {/* Scene 6 · SKILL_INDEX 新方案 */}
      <Sequence from={S.s6.from} durationInFrames={S.s6.dur}>
        <KnowledgeCard
          frame={frame - S.s6.from} fps={fps}
          label="解法"
          title="把手册放在固定的地方"
          body={[
            '知识库的路径不会变。',
            'SKILL_INDEX.md 是所有 Skill 的目录——',
            '告诉 Claude 一次，它就知道去哪找、什么时候用哪本手册。',
            '',
            '只需要一句开场白，全部自动搞定。',
          ]}
          accentColor="warm"
        />
      </Sequence>

      {/* Scene 7 · 三步上手（代码） */}
      <Sequence from={S.s7.from} durationInFrames={S.s7.dur}>
        <CodeCard
          frame={frame - S.s7.from} fps={fps}
          code={`你好，我的知识库在 D:\\AIGC工作站\\知识库，
请先读取 SKILL_INDEX.md，
后续对话中自动判断何时调用哪个 skill。`}
          caption="每次新对话只需要这一句话"
        />
      </Sequence>

      {/* Scene 8 · 实测结果 */}
      <Sequence from={S.s8.from} durationInFrames={S.s8.dur}>
        <KnowledgeCard
          frame={frame - S.s8.from} fps={fps}
          label="实测"
          title="两次触发，两次成功 ⭐⭐"
          body={[
            '2026-06-04，设计虚拟形象的对话中，',
            'aigc-prompt-optimizer 和 aigc-postmortem',
            '均被自动识别并完整执行，无一遗漏。',
          ]}
          accentColor="warm"
        />
      </Sequence>

      {/* Scene 9 · 结尾 */}
      <Sequence from={S.outro.from} durationInFrames={S.outro.dur}>
        <OutroScene frame={frame - S.outro.from} fps={fps} />
      </Sequence>
    </AbsoluteFill>
  );
};
