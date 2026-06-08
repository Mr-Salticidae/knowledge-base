import React from 'react';
import { AbsoluteFill, Audio, Easing, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { scene04VoiceoverTiming } from '../audio/generated/scene04VoiceoverTiming';
import { SCENE_04_SEEDANCE_MOTION_PATH } from '../data/sceneAssets';
import { theme } from '../styles/palette';

export const SCENE_04_MOTION_TEST_FRAMES = scene04VoiceoverTiming.totalFrames;

const clamp = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};

const Caption: React.FC<{ frame: number }> = ({ frame }) => {
  const active =
    scene04VoiceoverTiming.beats.find((beat) => frame >= beat.startFrame && frame < beat.startFrame + beat.durationInFrames) ??
    scene04VoiceoverTiming.beats[scene04VoiceoverTiming.beats.length - 1];
  const localFrame = frame - active.startFrame;
  const opacity = interpolate(localFrame, [0, 12, Math.max(20, active.durationInFrames - 14), active.durationInFrames], [0, 1, 1, 0], clamp);
  const y = interpolate(localFrame, [0, 12], [18, 0], clamp);

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        bottom: 58,
        transform: `translateX(-50%) translateY(${y}px)`,
        width: 760,
        padding: '18px 34px',
        borderRadius: 28,
        border: `6px solid ${theme.border}`,
        background: '#FFFFFF',
        boxShadow: '12px 12px 0 rgba(24, 35, 58, 0.14)',
        color: theme.darkText,
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: 42,
        fontWeight: 900,
        lineHeight: 1.2,
        textAlign: 'center',
        opacity,
        zIndex: 20,
      }}
    >
      {active.text}
    </div>
  );
};

export const Scene04MotionTest: React.FC = () => {
  const frame = useCurrentFrame();
  const intro = interpolate(frame, [0, 24], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const videoScale = interpolate(frame, [0, SCENE_04_MOTION_TEST_FRAMES], [0.985, 1.015], clamp);
  const videoY = interpolate(frame, [0, SCENE_04_MOTION_TEST_FRAMES], [4, -4], clamp);
  const glow = interpolate(frame, [8, 40, 88, 118], [0, 1, 1, 0], clamp);

  return (
    <AbsoluteFill style={{ background: '#FFF2C7', overflow: 'hidden' }}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundImage:
            'linear-gradient(rgba(24,35,58,0.05) 2px, transparent 2px), linear-gradient(90deg, rgba(24,35,58,0.05) 2px, transparent 2px)',
          backgroundSize: '96px 96px',
        }}
      />
      <div
        style={{
          position: 'absolute',
          right: -170,
          top: -140,
          width: 520,
          height: 280,
          borderRadius: '50%',
          background: 'rgba(65,182,230,0.22)',
          border: '7px solid rgba(24,35,58,0.08)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -190,
          bottom: -150,
          width: 560,
          height: 280,
          borderRadius: '50%',
          background: 'rgba(255,216,77,0.34)',
          border: '7px solid rgba(24,35,58,0.08)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: '50%',
          top: '45%',
          width: 1210,
          height: 682,
          transform: `translate(-50%, -50%) translateY(${videoY}px) scale(${videoScale})`,
          opacity: intro,
          transformOrigin: 'center center',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: -16,
            borderRadius: 38,
            background: `rgba(255, 216, 77, ${0.2 * glow})`,
            filter: 'blur(16px)',
          }}
        />
        <OffthreadVideo
          src={staticFile(SCENE_04_SEEDANCE_MOTION_PATH)}
          muted
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            borderRadius: 34,
            border: `7px solid ${theme.border}`,
            boxShadow: '16px 16px 0 rgba(24, 35, 58, 0.14)',
            background: '#FFFFFF',
          }}
        />
      </div>
      <div
        style={{
          position: 'absolute',
          left: 92,
          top: 72,
          padding: '14px 24px',
          borderRadius: 24,
          border: `5px solid ${theme.border}`,
          background: '#FFFFFF',
          color: theme.darkText,
          fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
          fontSize: 28,
          fontWeight: 900,
          boxShadow: '9px 9px 0 rgba(24, 35, 58, 0.12)',
          opacity: intro,
        }}
      >
        scene_04 / motion test
      </div>
      <Caption frame={frame} />
      {scene04VoiceoverTiming.hasGeneratedAudio
        ? scene04VoiceoverTiming.beats.map((beat) => (
            <Sequence key={beat.id} from={beat.startFrame} durationInFrames={beat.durationInFrames}>
              <Audio src={staticFile(beat.audioSrc)} />
            </Sequence>
          ))
        : null}
    </AbsoluteFill>
  );
};
