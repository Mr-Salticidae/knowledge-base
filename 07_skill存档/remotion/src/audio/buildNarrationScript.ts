import { sceneSpecs } from '../data/sceneSpecs';

export type NarrationScriptBuild = {
  text: string;
  sceneCount: number;
  beatCount: number;
  textLength: number;
};

export const buildNarrationScript = (): NarrationScriptBuild => {
  const sceneBlocks = sceneSpecs.map((scene, sceneIndex) => {
    const beats = scene.narrationBeats ?? [];
    const beatTexts = beats.map((beat) => beat.text);

    if (sceneIndex === 0 && beatTexts.length > 0) {
      return [`[calm] ${beatTexts[0]}`, ...beatTexts.slice(1)].join('\n\n');
    }

    return beatTexts.join('\n\n');
  });

  const text = sceneBlocks.filter(Boolean).join('\n\n[slight pause]\n\n');
  const beatCount = sceneSpecs.reduce((sum, scene) => sum + (scene.narrationBeats?.length ?? 0), 0);

  return {
    text,
    sceneCount: sceneSpecs.length,
    beatCount,
    textLength: text.length,
  };
};
