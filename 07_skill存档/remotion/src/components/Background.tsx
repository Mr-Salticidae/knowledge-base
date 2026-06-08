import React from 'react';
import { AbsoluteFill } from 'remotion';
import type { BackgroundType, LayoutType } from '../data/sceneSpecs';
import { theme } from '../styles/palette';

type Props = {
  type: BackgroundType;
  layout: LayoutType;
};

const backgrounds: Record<BackgroundType, string> = {
  space: '#DFF6FF',
  body: '#E6FFF1',
  data: '#E9F6FF',
  city: '#EDE7FF',
  abstract: '#FFF1C9',
  plain: '#FFF7E6',
  library: '#FFE8AD',
  workspace: '#F6FBF4',
};

export const Background: React.FC<Props> = ({ type, layout }) => {
  return (
    <AbsoluteFill style={{ background: backgrounds[type], overflow: 'hidden' }}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'linear-gradient(rgba(24,35,58,0.055) 2px, transparent 2px), linear-gradient(90deg, rgba(24,35,58,0.055) 2px, transparent 2px)',
          backgroundSize: '96px 96px',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: 110,
          right: 110,
          top: 96,
          bottom: 120,
          border: `5px solid ${theme.border}`,
          borderRadius: 34,
          opacity: 0.1,
        }}
      />
      {(layout === 'network-map' || type === 'data') && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage:
              'radial-gradient(circle, rgba(24,35,58,0.18) 0 6px, transparent 7px), linear-gradient(rgba(24,35,58,0.08) 2px, transparent 2px), linear-gradient(90deg, rgba(24,35,58,0.08) 2px, transparent 2px)',
            backgroundSize: '160px 160px, 80px 80px, 80px 80px',
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
            border: `7px dashed rgba(24,35,58,0.2)`,
          }}
        />
      )}
      <div
        style={{
          position: 'absolute',
          left: -180,
          bottom: -150,
          width: 560,
          height: 280,
          borderRadius: '50%',
          background: 'rgba(255,216,77,0.36)',
          border: '7px solid rgba(24,35,58,0.09)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: -210,
          top: -170,
          width: 620,
          height: 320,
          borderRadius: '50%',
          background: 'rgba(65,182,230,0.28)',
          border: '7px solid rgba(24,35,58,0.08)',
        }}
      />
    </AbsoluteFill>
  );
};
