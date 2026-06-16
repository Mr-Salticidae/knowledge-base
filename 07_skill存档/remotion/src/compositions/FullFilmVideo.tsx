import React from 'react';
import { AbsoluteFill, Series } from 'remotion';
import {
  FULL_FILM_FRAMES,
  fullFilmTimeline,
  fullFilmTimelineTailFrames,
} from '../audio/deriveFullFilmTimeline';
import { FullFilmBgmAudio } from '../components/FullFilmBgmAudio';
import { FullFilmVoiceoverAudio } from '../components/FullFilmVoiceoverAudio';
import { SceneRenderer } from '../components/SceneRenderer';

export { FULL_FILM_FRAMES };

export const FullFilmVideo: React.FC = () => (
  <AbsoluteFill style={{ background: '#0F172A' }}>
    <FullFilmBgmAudio />
    <FullFilmVoiceoverAudio />
    <Series>
      {fullFilmTimeline.map((scene, index) => (
        <Series.Sequence key={`${scene.id}-${index}`} durationInFrames={scene.durationInFrames}>
          <SceneRenderer scene={scene} />
        </Series.Sequence>
      ))}
      {fullFilmTimelineTailFrames > 0 ? (
        <Series.Sequence durationInFrames={fullFilmTimelineTailFrames}>
          <SceneRenderer scene={fullFilmTimeline[fullFilmTimeline.length - 1]} />
        </Series.Sequence>
      ) : null}
    </Series>
  </AbsoluteFill>
);
