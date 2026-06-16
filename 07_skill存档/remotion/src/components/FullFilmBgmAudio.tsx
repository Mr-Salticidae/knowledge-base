import React from 'react';
import { Audio, interpolate, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { fullFilmVoiceoverTiming } from '../audio/generated/fullFilmVoiceoverTiming';

const FULL_FILM_FRAMES = fullFilmVoiceoverTiming.totalFrames;
const AUTHOR_NOTE_START_FRAME =
  fullFilmVoiceoverTiming.beats.find((beat) => beat.id === 'author_01_cant_edit')?.startFrame ?? 3000;
const CROSSFADE_FRAMES = 90;
const OPEN_BENCH_START_FRAME = 300;
const NIGHT_WORKSHOP_START_FRAME = 150;
const OPEN_BENCH_VOLUME = 0.1;
const NIGHT_WORKSHOP_VOLUME = 0.13;

export const FullFilmBgmAudio: React.FC = () => {
  const frame = useCurrentFrame();
  const crossfadeStart = AUTHOR_NOTE_START_FRAME - CROSSFADE_FRAMES;
  const crossfadeEnd = AUTHOR_NOTE_START_FRAME + CROSSFADE_FRAMES;

  const openBenchVolume = interpolate(
    frame,
    [0, 60, crossfadeStart, crossfadeEnd],
    [0, OPEN_BENCH_VOLUME, OPEN_BENCH_VOLUME, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' },
  );

  const nightWorkshopVolume = interpolate(
    frame,
    [crossfadeStart, crossfadeEnd, FULL_FILM_FRAMES - 120, FULL_FILM_FRAMES],
    [0, NIGHT_WORKSHOP_VOLUME, NIGHT_WORKSHOP_VOLUME, 0],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' },
  );

  return (
    <>
      <Audio
        src={staticFile('audio/suno/open-bench.mp3')}
        volume={openBenchVolume}
        startFrom={OPEN_BENCH_START_FRAME}
        endAt={OPEN_BENCH_START_FRAME + crossfadeEnd}
      />
      <Sequence from={crossfadeStart}>
        <Audio
          src={staticFile('audio/suno/night-workshop-manifesto.mp3')}
          volume={nightWorkshopVolume}
          startFrom={NIGHT_WORKSHOP_START_FRAME}
        />
      </Sequence>
    </>
  );
};
