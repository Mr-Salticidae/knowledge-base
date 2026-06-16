import React from 'react';
import { Audio, Sequence, staticFile } from 'remotion';
import { fullFilmVoiceoverTiming } from '../audio/generated/fullFilmVoiceoverTiming';

export const FullFilmVoiceoverAudio: React.FC = () => {
  // 还没生成真实 Eleven 音频时（provisional 估算 timing），静音预览，避免加载不存在的 mp3 导致渲染失败。
  if (!fullFilmVoiceoverTiming.hasGeneratedAudio) {
    return null;
  }

  return (
  <>
    {fullFilmVoiceoverTiming.beats.map((beat) => (
      <Sequence key={beat.id} from={beat.startFrame} durationInFrames={beat.durationInFrames}>
        <Audio src={staticFile(beat.audioSrc)} playbackRate={fullFilmVoiceoverTiming.playbackRate} />
      </Sequence>
    ))}
  </>
  );
};
