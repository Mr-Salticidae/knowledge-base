import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { sceneAssets } from '../data/sceneAssets';
import type { SceneSpec } from '../data/sceneSpecs';
import { AssetLayer } from './AssetLayer';
import { Background } from './Background';
import { Label } from './Label';
import { NarrationCaption } from './NarrationCaption';
import { Subject } from './Subject';

type Props = {
  scene: SceneSpec;
};

export const SceneRenderer: React.FC<Props> = ({ scene }) => {
  const frame = useCurrentFrame();
  const assets = sceneAssets.filter((asset) => asset.sceneId === scene.id);
  const hasLinkedPrimaryAsset = assets.some(
    (asset) =>
      (asset.status === 'linked' || asset.status === 'verified') &&
      (asset.binding === 'foreground-image' || asset.binding === 'video-insert') &&
      (!asset.timeRange || (frame >= asset.timeRange.startFrame && frame <= asset.timeRange.endFrame))
  );

  return (
    <AbsoluteFill>
      <Background type={scene.background} layout={scene.layout} />
      <AssetLayer assets={assets} />
      {!hasLinkedPrimaryAsset &&
        scene.subjects.map((subject) => (
          <Subject key={subject.id} subject={subject} motions={scene.motion} />
        ))}
      {scene.narrationBeats?.length ? <NarrationCaption beats={scene.narrationBeats} fallbackTexts={scene.texts} /> : scene.texts.map((text) => <Label key={text.id} text={text} />)}
    </AbsoluteFill>
  );
};
