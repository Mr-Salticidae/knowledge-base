import React from 'react';
import { Audio, Sequence, staticFile } from 'remotion';
import { fullFilmVoiceoverTiming } from '../audio/generated/fullFilmVoiceoverTiming';

export const FullFilmVoiceoverAudio: React.FC = () => (
  <>
    {fullFilmVoiceoverTiming.beats.map((beat) => (
      <Sequence key={beat.id} from={beat.startFrame} durationInFrames={beat.durationInFrames}>
        <Audio src={staticFile(beat.audioSrc)} playbackRate={fullFilmVoiceoverTiming.playbackRate} />
      </Sequence>
    ))}
  </>
);
