import React from 'react';
import { AbsoluteFill } from 'remotion';
import type { BackgroundType, LayoutType } from '../data/sceneSpecs';

type Props = {
  type: BackgroundType;
  layout: LayoutType;
};

const backgrounds: Record<BackgroundType, string> = {
  space: 'linear-gradient(135deg, #111827 0%, #172554 54%, #312E81 100%)',
  body: 'linear-gradient(135deg, #0F172A 0%, #164E63 100%)',
  data: 'linear-gradient(135deg, #0F172A 0%, #1E293B 58%, #0E7490 100%)',
  city: 'linear-gradient(135deg, #1E293B 0%, #334155 100%)',
  abstract: 'linear-gradient(135deg, #581C87 0%, #0F766E 100%)',
  plain: 'linear-gradient(135deg, #E0F2FE 0%, #F8FAFC 100%)',
  library: 'linear-gradient(135deg, #422006 0%, #7C2D12 48%, #172554 100%)',
  workspace: 'linear-gradient(135deg, #F8FAFC 0%, #DBEAFE 100%)',
};

export const Background: React.FC<Props> = ({ type, layout }) => {
  const isLight = type === 'plain' || type === 'workspace';

  return (
    <AbsoluteFill style={{ background: backgrounds[type], overflow: 'hidden' }}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: isLight
            ? 'radial-gradient(circle at 20% 20%, rgba(14, 165, 233, 0.18), transparent 28%), radial-gradient(circle at 84% 76%, rgba(250, 204, 21, 0.16), transparent 30%)'
            : 'radial-gradient(circle at 18% 16%, rgba(255,255,255,0.14), transparent 26%), radial-gradient(circle at 76% 70%, rgba(34, 211, 238, 0.18), transparent 32%)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 96,
          right: 96,
          top: 90,
          bottom: 90,
          border: `2px solid ${isLight ? 'rgba(15, 23, 42, 0.12)' : 'rgba(255,255,255,0.12)'}`,
          borderRadius: 36,
        }}
      />
      {(layout === 'network-map' || type === 'data') && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage:
              'linear-gradient(rgba(255,255,255,0.07) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.07) 1px, transparent 1px)',
            backgroundSize: '88px 88px',
          }}
        />
      )}
      {layout === 'circular-system' && (
        <div
          style={{
            position: 'absolute',
            left: '24%',
            top: '17%',
            width: '52%',
            height: '66%',
            borderRadius: '50%',
            border: `4px dashed ${isLight ? 'rgba(15, 23, 42, 0.16)' : 'rgba(255,255,255,0.18)'}`,
          }}
        />
      )}
    </AbsoluteFill>
  );
};
