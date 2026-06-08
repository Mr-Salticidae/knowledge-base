import React from 'react';
import { AbsoluteFill, Audio, Easing, Img, interpolate, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { formalClipVoiceoverTiming } from '../audio/generated/formalClipVoiceoverTiming';
import {
  FORMAL_CLIP_01_AI_FORGETS_MJ_PATH,
  FORMAL_CLIP_01_AI_FORGETS_SEEDANCE_PATH,
  FORMAL_CLIP_04_SKILL_INDEX_MJ_PATH,
  FORMAL_CLIP_04_SKILL_INDEX_SEEDANCE_PATH,
  FORMAL_CLIP_05_TOOL_LOOP_MJ_PATH,
  FORMAL_CLIP_05_TOOL_LOOP_SEEDANCE_PATH,
  SCENE_04_MJ_KEY_VISUAL_PATH,
  SCENE_04_SEEDANCE_MOTION_PATH,
  SCENE_05_MJ_KEY_VISUAL_PATH,
  SCENE_05_SEEDANCE_MOTION_PATH,
} from '../data/sceneAssets';
import { theme } from '../styles/palette';

const FPS = 30;

type ClipScene = {
  id: string;
  label: string;
  videoPath: string;
  fallbackImagePath?: string;
  startFrom?: number;
  sourceDurationInFrames: number;
};

export const formalClipScenes: ClipScene[] = [
  {
    id: 'ai_forgets',
    label: '01 / AI 会忘记',
    videoPath: FORMAL_CLIP_01_AI_FORGETS_SEEDANCE_PATH,
    fallbackImagePath: FORMAL_CLIP_01_AI_FORGETS_MJ_PATH,
    sourceDurationInFrames: 150,
  },
  {
    id: 'compress_to_skill',
    label: '02 / 压缩成 Skill',
    videoPath: SCENE_04_SEEDANCE_MOTION_PATH,
    fallbackImagePath: SCENE_04_MJ_KEY_VISUAL_PATH,
    sourceDurationInFrames: 120,
  },
  {
    id: 'markdown_structure',
    label: '03 / SKILL.md',
    videoPath: SCENE_05_SEEDANCE_MOTION_PATH,
    fallbackImagePath: SCENE_05_MJ_KEY_VISUAL_PATH,
    startFrom: 30,
    sourceDurationInFrames: 150,
  },
  {
    id: 'skill_index',
    label: '04 / SKILL_INDEX',
    videoPath: FORMAL_CLIP_04_SKILL_INDEX_SEEDANCE_PATH,
    fallbackImagePath: FORMAL_CLIP_04_SKILL_INDEX_MJ_PATH,
    sourceDurationInFrames: 150,
  },
  {
    id: 'tool_loop',
    label: '05 / 工具闭环',
    videoPath: FORMAL_CLIP_05_TOOL_LOOP_SEEDANCE_PATH,
    fallbackImagePath: FORMAL_CLIP_05_TOOL_LOOP_MJ_PATH,
    sourceDurationInFrames: 150,
  },
];

export const FORMAL_CLIP_20260608_FRAMES = formalClipVoiceoverTiming.totalFrames;

const clamp = {
  extrapolateLeft: 'clamp' as const,
  extrapolateRight: 'clamp' as const,
};

const Caption: React.FC<{ text: string; frame: number; durationInFrames: number }> = ({ text, frame, durationInFrames }) => {
  const opacity = interpolate(frame, [0, 14, Math.max(18, durationInFrames - 16), durationInFrames], [0, 1, 1, 0], clamp);
  const y = interpolate(frame, [0, 14], [18, 0], clamp);

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        bottom: 46,
        transform: `translateX(-50%) translateY(${y}px)`,
        width: 1480,
        minHeight: 96,
        padding: '16px 40px',
        borderRadius: 24,
        border: `6px solid ${theme.border}`,
        background: '#FFFFFF',
        boxShadow: '12px 12px 0 rgba(24, 35, 58, 0.14)',
        color: theme.darkText,
        fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
        fontSize: 32,
        fontWeight: 900,
        lineHeight: 1.28,
        textAlign: 'center',
        opacity,
        zIndex: 20,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {text}
    </div>
  );
};

const SceneShell: React.FC<{ scene: ClipScene; beat: (typeof formalClipVoiceoverTiming.beats)[number] }> = ({ scene, beat }) => {
  const frame = useCurrentFrame();
  const durationInFrames = beat.durationInFrames;
  const intro = interpolate(frame, [0, 22], [0, 1], {
    ...clamp,
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });
  const videoScale = interpolate(frame, [0, durationInFrames], [0.988, 1.012], clamp);
  const videoY = interpolate(frame, [0, durationInFrames], [5, -5], clamp);
  const fallbackStart = Math.max(0, scene.sourceDurationInFrames - 18);
  const fallbackOpacity = scene.fallbackImagePath ? interpolate(frame, [fallbackStart, scene.sourceDurationInFrames], [0, 1], clamp) : 0;

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
          left: '50%',
          top: '45%',
          width: 1210,
          height: 682,
          transform: `translate(-50%, -50%) translateY(${videoY}px) scale(${videoScale})`,
          opacity: intro,
          transformOrigin: 'center center',
        }}
      >
        <OffthreadVideo
          src={staticFile(scene.videoPath)}
          startFrom={scene.startFrom ?? 0}
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
        {scene.fallbackImagePath ? (
          <Img
            src={staticFile(scene.fallbackImagePath)}
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
              opacity: fallbackOpacity,
            }}
          />
        ) : null}
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
        {scene.label}
      </div>
      <div
        style={{
          position: 'absolute',
          right: 92,
          top: 78,
          color: theme.mutedText,
          fontFamily: '"JetBrains Mono", "Cascadia Mono", monospace',
          fontSize: 22,
          fontWeight: 800,
          opacity: intro,
        }}
      >
        {Math.round((frame / FPS) * 10) / 10}s
      </div>
      <Caption text={beat.caption} frame={frame} durationInFrames={durationInFrames} />
      <Audio src={staticFile(beat.audioSrc)} />
    </AbsoluteFill>
  );
};

export const FormalClip20260608: React.FC = () => (
  <AbsoluteFill style={{ background: '#FFF2C7' }}>
    {formalClipVoiceoverTiming.beats.map((beat) => {
      const scene = formalClipScenes.find((item) => item.id === beat.sceneId);

      if (!scene) {
        return null;
      }

      return (
        <Sequence key={beat.id} from={beat.startFrame} durationInFrames={beat.durationInFrames}>
          <SceneShell scene={scene} beat={beat} />
        </Sequence>
      );
    })}
  </AbsoluteFill>
);
