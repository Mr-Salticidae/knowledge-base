import { sceneSpecs } from '../data/sceneSpecs';
import { createVideo } from './RemotionSkill';

export const runRemotionSkillExample = async () =>
  createVideo({
    sceneSpecs,
    callExistingSkills: ['ai-short-film-breakdown', 'aigc-prompt-optimizer', 'blind-editing-workflow'],
    outputPath: 'out/skill-is-all-you-need.mp4',
    dryRun: true,
    style: {
      visualLanguage: 'in-a-nutshell-inspired',
      palette: 'vivid-controlled',
      motionPreset: 'snappy',
      assetMode: 'placeholder',
    },
  });
