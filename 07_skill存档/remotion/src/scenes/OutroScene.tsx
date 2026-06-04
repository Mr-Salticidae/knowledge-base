import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS, TYPE, FONT } from '../design-tokens';
import { fadeUp, fade } from '../helpers';

interface Props { frame: number; fps: number; }

export const OutroScene: React.FC<Props> = ({ frame, fps }) => (
  <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
    <div style={{ textAlign: 'center' }}>
      <div style={{
        ...fadeUp(frame, fps, 0),
        fontSize: TYPE.h1,
        color: COLORS.primary,
        fontFamily: FONT.sans,
        fontWeight: 700,
        letterSpacing: '-1px',
      }}>
        Skill Is All You Need
      </div>

      <div style={{
        ...fadeUp(frame, fps, 16),
        fontSize: TYPE.body,
        color: COLORS.secondary,
        fontFamily: FONT.sans,
        marginTop: 28,
        lineHeight: 1.6,
      }}>
        把你的流程固化成手册，让 AI 每次都能立刻上手
      </div>

      <div style={{
        ...fade(frame, fps, 30),
        display: 'flex',
        gap: 32,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 56,
      }}>
        <span style={{ fontSize: TYPE.caption, color: COLORS.accent, fontFamily: FONT.mono }}>
          @跳蛛先生
        </span>
        <span style={{ fontSize: TYPE.caption, color: COLORS.dim, fontFamily: FONT.mono }}>·</span>
        <span style={{ fontSize: TYPE.caption, color: COLORS.secondary, fontFamily: FONT.mono }}>
          AIGC工作站 · 知识库
        </span>
      </div>
    </div>
  </AbsoluteFill>
);
