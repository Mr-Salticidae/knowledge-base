import React from 'react';
import { AbsoluteFill } from 'remotion';
import { COLORS, TYPE, FONT } from '../design-tokens';
import { fadeUp, fade } from '../helpers';

interface Props {
  frame: number;
  fps: number;
  code: string;
  caption?: string;
}

export const CodeCard: React.FC<Props> = ({ frame, fps, code, caption }) => (
  <AbsoluteFill style={{ background: COLORS.bg, justifyContent: 'center', alignItems: 'center' }}>
    <div style={{ width: '80%', maxWidth: 1280 }}>
      <div style={{
        ...fadeUp(frame, fps, 0),
        background: COLORS.surfaceHover,
        border: `1px solid ${COLORS.border}`,
        borderRadius: 12,
        padding: '48px 56px',
        fontFamily: FONT.mono,
        fontSize: TYPE.caption,
        color: COLORS.primary,
        lineHeight: 1.9,
        whiteSpace: 'pre' as const,
      }}>
        {code}
      </div>
      {caption && (
        <div style={{
          ...fade(frame, fps, 20),
          fontSize: TYPE.label,
          color: COLORS.secondary,
          fontFamily: FONT.sans,
          marginTop: 24,
          textAlign: 'center' as const,
        }}>
          {caption}
        </div>
      )}
    </div>
  </AbsoluteFill>
);
