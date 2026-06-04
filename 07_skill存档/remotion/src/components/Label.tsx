import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type { TextSpec } from '../data/sceneSpecs';
import { mergeMotionStyles } from '../utils/motion';
import { theme } from '../styles/palette';

type Props = {
  text: TextSpec;
};

const positionStyles: Record<TextSpec['position'], React.CSSProperties> = {
  top: { top: 118, left: '50%', transform: 'translateX(-50%)' },
  bottom: { bottom: 118, left: '50%', transform: 'translateX(-50%)' },
  center: { top: '50%', left: '50%', transform: 'translate(-50%, -50%)' },
  left: { left: 120, top: '50%', transform: 'translateY(-50%)' },
  right: { right: 120, top: '50%', transform: 'translateY(-50%)' },
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
        zIndex: 20,
        maxWidth: text.emphasis ? 1320 : 1120,
        padding: text.emphasis ? '22px 36px' : '16px 28px',
        borderRadius: 24,
        color: theme.text,
        background: text.emphasis ? 'rgba(15, 23, 42, 0.88)' : 'rgba(15, 23, 42, 0.78)',
        border: '1px solid rgba(255,255,255,0.16)',
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: text.emphasis ? 58 : 34,
        fontWeight: text.emphasis ? 800 : 650,
        lineHeight: 1.18,
        textAlign: 'center',
        whiteSpace: 'pre-wrap',
        ...positionStyles[text.position],
        ...motion,
      }}
    >
      {text.text}
    </div>
  );
};
