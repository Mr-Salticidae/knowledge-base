import React from 'react';
import { AbsoluteFill, Series } from 'remotion';
import { sceneSpecs, TOTAL_FRAMES } from '../data/sceneSpecs';
import { SceneRenderer } from '../components/SceneRenderer';
import { VoiceoverAudio } from '../components/VoiceoverAudio';

export { TOTAL_FRAMES };

export const ExplainerVideo: React.FC = () => (
  <AbsoluteFill style={{ background: '#0F172A' }}>
    <VoiceoverAudio />
    <Series>
      {sceneSpecs.map((scene) => (
        <Series.Sequence key={scene.id} durationInFrames={scene.durationInFrames}>
          <SceneRenderer scene={scene} />
        </Series.Sequence>
      ))}
    </Series>
  </AbsoluteFill>
);
