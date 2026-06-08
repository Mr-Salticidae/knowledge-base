import React from 'react';
import { AbsoluteFill } from 'remotion';
import type { SceneSpec } from '../data/sceneSpecs';
import { Background } from './Background';
import { Label } from './Label';
import { NarrationCaption } from './NarrationCaption';
import { Subject } from './Subject';

type Props = {
  scene: SceneSpec;
};

export const SceneRenderer: React.FC<Props> = ({ scene }) => (
  <AbsoluteFill>
    <Background type={scene.background} layout={scene.layout} />
    {scene.subjects.map((subject) => (
      <Subject key={subject.id} subject={subject} motions={scene.motion} />
    ))}
    {scene.narrationBeats?.length ? <NarrationCaption beats={scene.narrationBeats} fallbackTexts={scene.texts} /> : scene.texts.map((text) => <Label key={text.id} text={text} />)}
  </AbsoluteFill>
);
