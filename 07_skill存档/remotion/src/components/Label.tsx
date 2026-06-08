import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type { TextSpec } from '../data/sceneSpecs';
import { mergeMotionStyles } from '../utils/motion';
import { theme } from '../styles/palette';

type Props = {
  text: TextSpec;
};

export const Label: React.FC<Props> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const motion = mergeMotionStyles(frame, fps, [
    { targetId: text.id, type: 'fade-in', startFrame: text.delayFrames ?? 8, durationFrames: 24 },
  ]);

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        bottom: 56,
        transform: 'translateX(-50%)',
        zIndex: 20,
        maxWidth: '68%',
        padding: text.emphasis ? '18px 34px' : '16px 32px',
        borderRadius: 28,
        color: theme.darkText,
        background: text.emphasis ? '#FFFFFF' : theme.paper,
        border: `6px solid ${theme.border}`,
        boxShadow: '12px 12px 0 rgba(24, 35, 58, 0.14)',
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: text.emphasis ? 42 : 34,
        fontWeight: text.emphasis ? 900 : 750,
        lineHeight: 1.25,
        textAlign: 'center',
        whiteSpace: 'normal',
        ...motion,
      }}
    >
      {text.text}
    </div>
  );
};
