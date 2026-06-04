import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS, TYPE, FONT } from '../design-tokens';
import { fadeUp, fade } from '../helpers';

interface Props { frame: number; fps: number; }

const TAGS = ['AI工具', 'Cowork', 'SKILL_INDEX'];

export const CoverScene: React.FC<Props> = ({ frame, fps }) => (
  <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
    {/* 顶部装饰线 */}
    <div style={{
      position: 'absolute', top: 80, left: 80, right: 80,
      height: 1, background: COLORS.dim, ...fade(frame, fps, 0),
    }} />

    <div style={{ textAlign: 'center', maxWidth: 1200 }}>
      {/* 主标题 */}
      <div style={{
        ...fadeUp(frame, fps, 0),
        fontSize: TYPE.hero,
        fontFamily: FONT.sans,
        color: COLORS.primary,
        fontWeight: 700,
        letterSpacing: '-2px',
        lineHeight: 1.1,
      }}>
        Skill Is All You Need
      </div>

      {/* 副标题 */}
      <div style={{
        ...fadeUp(frame, fps, 12),
        fontSize: TYPE.h3,
        color: COLORS.secondary,
        fontFamily: FONT.sans,
        marginTop: 32,
        fontWeight: 400,
      }}>
        让 AI 记住你的规则，而不是每次重新教
      </div>

      {/* 标签 */}
      <div style={{
        ...fade(frame, fps, 24),
        display: 'flex',
        gap: 16,
        justifyContent: 'center',
        marginTop: 48,
      }}>
        {TAGS.map(tag => (
          <span key={tag} style={{
            fontSize: TYPE.label,
            color: COLORS.accent,
            fontFamily: FONT.mono,
            border: `1px solid ${COLORS.accent}`,
            borderRadius: 4,
            padding: '6px 14px',
            opacity: 0.8,
          }}>
            {tag}
          </span>
        ))}
      </div>
    </div>

    {/* 底部装饰线 */}
    <div style={{
      position: 'absolute', bottom: 80, left: 80, right: 80,
      height: 1, background: COLORS.dim, ...fade(frame, fps, 0),
    }} />
  </AbsoluteFill>
);
