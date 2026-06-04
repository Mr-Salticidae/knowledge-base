import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS, TYPE, FONT, SPACING } from '../design-tokens';
import { fadeUp, fadeLeft, fade } from '../helpers';

interface Props {
  frame: number;
  fps: number;
  label?: string;
  title: string;
  body: string[];   // 每个元素一行，支持逐行入场
  accentColor?: 'cold' | 'warm';
}

export const KnowledgeCard: React.FC<Props> = ({
  frame, fps, label, title, body, accentColor = 'cold',
}) => {
  const color = accentColor === 'warm' ? COLORS.warm : COLORS.accent;

  return (
    <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
      <div style={{
        background: COLORS.surface,
        border: `1px solid ${COLORS.border}`,
        borderLeft: `3px solid ${color}`,
        borderRadius: 16,
        padding: SPACING.cardPadding,
        maxWidth: 1280,
        width: '80%',
      }}>
        {/* 标签 */}
        {label && (
          <div style={{
            ...fade(frame, fps, 0),
            fontSize: TYPE.label,
            color,
            fontFamily: FONT.mono,
            marginBottom: 24,
            letterSpacing: '2px',
            textTransform: 'uppercase' as const,
          }}>
            {label}
          </div>
        )}

        {/* 主标题 */}
        <div style={{
          ...fadeUp(frame, fps, 6),
          fontSize: TYPE.h2,
          color: COLORS.primary,
          fontFamily: FONT.sans,
          fontWeight: 600,
          lineHeight: 1.3,
          marginBottom: 36,
        }}>
          {title}
        </div>

        {/* 正文，逐行入场 */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {body.map((line, i) => (
            <div key={i} style={{
              ...fadeLeft(frame, fps, 16 + i * 8),
              fontSize: TYPE.body,
              color: COLORS.secondary,
              fontFamily: FONT.sans,
              lineHeight: SPACING.lineHeight,
            }}>
              {line}
            </div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
