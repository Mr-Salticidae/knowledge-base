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
        maxWidth: '72%',
        padding: text.emphasis ? '16px 34px' : '14px 30px',
        borderRadius: 999,
        color: theme.text,
        background: text.emphasis ? 'rgba(15, 23, 42, 0.84)' : 'rgba(15, 23, 42, 0.76)',
        border: '1px solid rgba(255,255,255,0.16)',
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: text.emphasis ? 40 : 32,
        fontWeight: text.emphasis ? 800 : 650,
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
