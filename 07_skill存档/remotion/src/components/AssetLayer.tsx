import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, staticFile, useCurrentFrame } from 'remotion';
import type { SceneAsset } from '../skills/RemotionSkill';

type Props = {
  assets: SceneAsset[];
};

const isRenderable = (asset: SceneAsset) =>
  (asset.status === 'linked' || asset.status === 'verified') &&
  Boolean(asset.filePath ?? asset.expectedPath) &&
  (asset.binding === 'background-image' || asset.binding === 'foreground-image' || asset.binding === 'video-insert');

const sourceFor = (asset: SceneAsset) => staticFile(asset.filePath ?? asset.expectedPath ?? '');

export const AssetLayer: React.FC<Props> = ({ assets }) => {
  const frame = useCurrentFrame();
  const renderableAssets = assets.filter(isRenderable);

  if (renderableAssets.length === 0) {
    return null;
  }

  return (
    <AbsoluteFill style={{ zIndex: 8, pointerEvents: 'none' }}>
      {renderableAssets.map((asset) => {
        if (asset.timeRange && (frame < asset.timeRange.startFrame || frame > asset.timeRange.endFrame)) {
          return null;
        }

        const commonStyle: React.CSSProperties =
          asset.binding === 'background-image'
            ? {
                position: 'absolute',
                inset: 0,
                width: '100%',
                height: '100%',
                objectFit: 'cover',
              }
            : {
                position: 'absolute',
                left: '50%',
                top: '47%',
                width: 1120,
                height: 630,
                transform: 'translate(-50%, -50%)',
                objectFit: 'contain',
                borderRadius: 30,
                border: '6px solid rgba(24, 35, 58, 0.86)',
                boxShadow: '14px 14px 0 rgba(24, 35, 58, 0.14)',
                background: '#FFFFFF',
              };

        if (asset.kind === 'video' || asset.binding === 'video-insert') {
          return <OffthreadVideo key={asset.id} src={sourceFor(asset)} muted style={commonStyle} />;
        }

        return <Img key={asset.id} src={sourceFor(asset)} style={commonStyle} />;
      })}
    </AbsoluteFill>
  );
};
