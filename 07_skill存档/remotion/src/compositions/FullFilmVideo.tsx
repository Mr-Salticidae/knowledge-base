import React from 'react';
import { AbsoluteFill, Series } from 'remotion';
import { fullFilmVoiceoverTiming } from '../audio/generated/fullFilmVoiceoverTiming';
import { FullFilmVoiceoverAudio } from '../components/FullFilmVoiceoverAudio';
import { SceneRenderer } from '../components/SceneRenderer';
import { sceneSpecs, type NarrationBeat, type SceneSpec } from '../data/sceneSpecs';

export const FULL_FILM_FRAMES = fullFilmVoiceoverTiming.totalFrames;

const sceneById = new Map(sceneSpecs.map((scene) => [scene.id, scene]));

const timelineScenes = fullFilmVoiceoverTiming.beats.reduce<SceneSpec[]>((scenes, beat) => {
  const sourceScene = sceneById.get(beat.sceneId);

  if (!sourceScene) {
    return scenes;
  }

  const previousScene = scenes[scenes.length - 1];
  const localBeat: NarrationBeat = {
    id: beat.id,
    startFrame: previousScene?.id === beat.sceneId ? previousScene.durationInFrames : 0,
    durationInFrames: beat.durationInFrames,
    text: beat.caption,
  };

  if (previousScene?.id === beat.sceneId) {
    previousScene.durationInFrames += beat.durationInFrames;
    previousScene.narration += beat.caption;
    previousScene.narrationBeats = [...(previousScene.narrationBeats ?? []), localBeat];
    return scenes;
  }

  scenes.push({
    ...sourceScene,
    durationInFrames: beat.durationInFrames,
    narration: beat.caption,
    narrationBeats: [localBeat],
  });

  return scenes;
}, []);

const tailHoldFrames = Math.max(
  0,
  FULL_FILM_FRAMES - timelineScenes.reduce((sum, scene) => sum + scene.durationInFrames, 0),
);

export const FullFilmVideo: React.FC = () => (
  <AbsoluteFill style={{ background: '#0F172A' }}>
    <FullFilmVoiceoverAudio />
    <Series>
      {timelineScenes.map((scene, index) => (
        <Series.Sequence key={`${scene.id}-${index}`} durationInFrames={scene.durationInFrames}>
          <SceneRenderer scene={scene} />
        </Series.Sequence>
      ))}
      {tailHoldFrames > 0 ? (
        <Series.Sequence durationInFrames={tailHoldFrames}>
          <SceneRenderer scene={timelineScenes[timelineScenes.length - 1]} />
        </Series.Sequence>
      ) : null}
    </Series>
  </AbsoluteFill>
);
