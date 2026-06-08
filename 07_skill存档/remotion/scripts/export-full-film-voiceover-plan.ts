import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { sceneSpecs } from '../src/data/sceneSpecs';
import { fullFilmVoiceoverBeats } from '../src/audio/fullFilmVoiceover';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const outputDir = path.join(projectRoot, 'production');
const outputPath = path.join(outputDir, 'full_film_2026-06-09_voiceover_plan.md');

const sceneIds = new Set(sceneSpecs.map((scene) => scene.id));
const missingSceneIds = fullFilmVoiceoverBeats.filter((beat) => !sceneIds.has(beat.sceneId));

if (missingSceneIds.length > 0) {
  throw new Error(`Voiceover beats reference missing scenes: ${missingSceneIds.map((beat) => `${beat.id}->${beat.sceneId}`).join(', ')}`);
}

const sectionCounts = fullFilmVoiceoverBeats.reduce<Record<string, number>>((counts, beat) => {
  counts[beat.section] = (counts[beat.section] ?? 0) + 1;
  return counts;
}, {});

const rows = fullFilmVoiceoverBeats
  .map((beat, index) => `| ${index + 1} | ${beat.section} | ${beat.sceneId} | ${beat.id} | ${beat.caption.replace(/\|/g, '/')} |`)
  .join('\n');

const content = `# Skill Is All You Need · Full Film Voiceover Plan

Generated: 2026-06-09

## Summary

- Total beats: ${fullFilmVoiceoverBeats.length}
- Sections: ${Object.entries(sectionCounts)
  .map(([section, count]) => `${section}=${count}`)
  .join(', ')}
- Scene binding: passed
- Audio generation command: \`npm.cmd run generate:full-film-voiceover\`

## Required Environment

\`\`\`text
ELEVENLABS_API_KEY=<your key>
ELEVENLABS_VOICE_ID=<selected voice id>
ELEVENLABS_MODEL_ID=eleven_v3
\`\`\`

## Beats

| # | section | sceneId | beatId | caption |
|---:|---|---|---|---|
${rows}
`;

mkdirSync(outputDir, { recursive: true });
writeFileSync(outputPath, content);

console.log(
  JSON.stringify(
    {
      status: 'done',
      outputPath: 'production/full_film_2026-06-09_voiceover_plan.md',
      beatCount: fullFilmVoiceoverBeats.length,
      sectionCounts,
    },
    null,
    2,
  ),
);
