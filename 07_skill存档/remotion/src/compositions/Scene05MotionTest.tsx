import React from 'react';
import { AbsoluteFill, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { SCENE_05_MJ_KEY_VISUAL_PATH, SCENE_05_SEEDANCE_MOTION_PATH } from '../data/sceneAssets';
import { theme } from '../styles/palette';

export const SCENE_05_MOTION_TEST_FRAMES = 210;

const VIDEO_START_FRAME = 30;
const VIDEO_SOURCE_START_FRAME = 30;
const VIDEO_DURATION_FRAMES = 150;

const clamp = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};

const captionBeats = [
  { id: 'markdown_file', text: 'Skill 先是一份可读的 Markdown', startFrame: 0, durationInFrames: 70 },
  { id: 'trigger_layer', text: '触发条件决定：什么时候调用', startFrame: 70, durationInFrames: 70 },
  { id: 'workflow_layer', text: '工作规则决定：怎么把事做完', startFrame: 140, durationInFrames: 70 },
];

const Caption: React.FC<{ frame: number }> = ({ frame }) => {
  const active = captionBeats.find((beat) => frame >= beat.startFrame && frame < beat.startFrame + beat.durationInFrames) ?? captionBeats[captionBeats.length - 1];
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
        width: 900,
        padding: '18px 34px',
        borderRadius: 28,
        border: `6px solid ${theme.border}`,
        background: '#FFFFFF',
        boxShadow: '12px 12px 0 rgba(24, 35, 58, 0.14)',
        color: theme.darkText,
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: 40,
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

export const Scene05MotionTest: React.FC = () => {
  const frame = useCurrentFrame();
  const intro = interpolate(frame, [0, 24], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const staticOpacity = interpolate(frame, [0, 24, VIDEO_START_FRAME, VIDEO_START_FRAME + 18], [0, 1, 1, 0], clamp);
  const finalStaticOpacity = interpolate(frame, [VIDEO_START_FRAME + VIDEO_DURATION_FRAMES - 18, VIDEO_START_FRAME + VIDEO_DURATION_FRAMES], [0, 1], clamp);
  const videoOpacity = interpolate(frame, [VIDEO_START_FRAME, VIDEO_START_FRAME + 18], [0, 1], clamp);
  const videoScale = interpolate(frame, [0, SCENE_05_MOTION_TEST_FRAMES], [0.99, 1.018], clamp);
  const videoY = interpolate(frame, [0, SCENE_05_MOTION_TEST_FRAMES], [4, -4], clamp);
  const glow = interpolate(frame, [12, 52, 150, 188], [0, 1, 1, 0], clamp);

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
          right: -160,
          top: -130,
          width: 500,
          height: 270,
          borderRadius: '50%',
          background: 'rgba(65,182,230,0.2)',
          border: '7px solid rgba(24,35,58,0.08)',
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: -180,
          bottom: -150,
          width: 540,
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
            background: `rgba(255, 216, 77, ${0.18 * glow})`,
            filter: 'blur(16px)',
          }}
        />
        <Img
          src={staticFile(SCENE_05_MJ_KEY_VISUAL_PATH)}
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
            opacity: staticOpacity,
          }}
        />
        <Sequence from={VIDEO_START_FRAME} durationInFrames={VIDEO_DURATION_FRAMES}>
          <OffthreadVideo
            src={staticFile(SCENE_05_SEEDANCE_MOTION_PATH)}
            startFrom={VIDEO_SOURCE_START_FRAME}
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
              opacity: videoOpacity,
            }}
          />
        </Sequence>
        <Img
          src={staticFile(SCENE_05_MJ_KEY_VISUAL_PATH)}
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
            opacity: finalStaticOpacity,
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
        scene_05 / motion test
      </div>
      <Caption frame={frame} />
    </AbsoluteFill>
  );
};
