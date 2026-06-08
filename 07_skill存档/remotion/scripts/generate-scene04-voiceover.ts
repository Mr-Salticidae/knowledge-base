import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { applyPronunciationFixes, pronunciationFixes, scene04AudioPublicDir, scene04VoiceoverBeats } from '../src/audio/scene04Voiceover';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const envPath = path.join(projectRoot, '.env');
const fps = 30;
const outputFormat = 'mp3_44100_128';

const loadLocalEnv = () => {
  if (!existsSync(envPath)) {
    return;
  }

  const lines = readFileSync(envPath, 'utf8').split(/\r?\n/);

  for (const line of lines) {
    const trimmed = line.trim();

    if (!trimmed || trimmed.startsWith('#')) {
      continue;
    }

    const separatorIndex = trimmed.indexOf('=');

    if (separatorIndex === -1) {
      continue;
    }

    const key = trimmed.slice(0, separatorIndex).trim();
    const rawValue = trimmed.slice(separatorIndex + 1).trim();
    const value = rawValue.replace(/^["']|["']$/g, '');

    if (key && process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
};

const requiredEnv = (name: string) => {
  const value = process.env[name]?.trim();

  if (!value) {
    throw new Error(`${name} is required. Configure it in the environment or local .env file.`);
  }

  return value;
};

const durationSecondsFor = (filePath: string) => {
  const output = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filePath], {
    encoding: 'utf8',
  }).trim();
  const duration = Number(output);

  if (!Number.isFinite(duration) || duration <= 0) {
    throw new Error(`Unable to read duration for ${filePath}`);
  }

  return duration;
};

const writeTimingFile = (params: {
  beats: Array<{
    id: string;
    text: string;
    audioSrc: string;
    startFrame: number;
    durationInFrames: number;
    durationSeconds: number;
  }>;
  totalFrames: number;
}) => {
  const timingPath = path.join(projectRoot, 'src', 'audio', 'generated', 'scene04VoiceoverTiming.ts');
  const content = `export type Scene04VoiceoverTimingBeat = {
  id: string;
  text: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

export const scene04VoiceoverTiming = {
  hasGeneratedAudio: true,
  fps: ${fps},
  totalFrames: ${params.totalFrames},
  beats: ${JSON.stringify(params.beats, null, 4)} satisfies Scene04VoiceoverTimingBeat[],
};
`;

  writeFileSync(timingPath, content);
};

const main = async () => {
  loadLocalEnv();

  const apiKey = requiredEnv('ELEVENLABS_API_KEY');
  const voiceId = requiredEnv('ELEVENLABS_VOICE_ID');
  const modelId = process.env.ELEVENLABS_MODEL_ID?.trim() || 'eleven_v3';
  const audioDir = path.join(projectRoot, 'public', scene04AudioPublicDir);
  const manifestPath = path.join(audioDir, 'scene04-voiceover.manifest.json');

  mkdirSync(audioDir, { recursive: true });

  const generatedBeats = [];
  let startFrame = 0;

  for (const [index, beat] of scene04VoiceoverBeats.entries()) {
    const fileName = `${beat.id}.mp3`;
    const filePath = path.join(audioDir, fileName);
    const ttsText = applyPronunciationFixes(beat.ttsText);
    const previousText = scene04VoiceoverBeats[index - 1] ? applyPronunciationFixes(scene04VoiceoverBeats[index - 1].ttsText) : undefined;
    const nextText = scene04VoiceoverBeats[index + 1] ? applyPronunciationFixes(scene04VoiceoverBeats[index + 1].ttsText) : undefined;
    const continuityText =
      modelId === 'eleven_v3'
        ? {}
        : {
            previous_text: previousText,
            next_text: nextText,
          };

    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=${outputFormat}`, {
      method: 'POST',
      headers: {
        'xi-api-key': apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: ttsText,
        model_id: modelId,
        ...continuityText,
        voice_settings: {
          stability: 0.5,
          similarity_boost: 0.75,
          style: 0.35,
          use_speaker_boost: true,
        },
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`ElevenLabs TTS failed for ${beat.id} with status ${response.status}: ${errorText}`);
    }

    writeFileSync(filePath, Buffer.from(await response.arrayBuffer()));

    const durationSeconds = durationSecondsFor(filePath);
    const durationInFrames = Math.max(18, Math.ceil(durationSeconds * fps) + 8);

    generatedBeats.push({
      id: beat.id,
      text: beat.text,
      audioSrc: `${scene04AudioPublicDir}/${fileName}`,
      startFrame,
      durationInFrames,
      durationSeconds,
    });

    startFrame += durationInFrames;
  }

  const totalFrames = startFrame;

  writeTimingFile({ beats: generatedBeats, totalFrames });
  writeFileSync(
    manifestPath,
    `${JSON.stringify(
      {
        provider: 'elevenlabs',
        modelId,
        voiceId,
      outputFormat,
      fps,
      totalFrames,
      createdAt: new Date().toISOString(),
      pronunciationFixes,
      beats: generatedBeats,
      },
      null,
      2,
    )}\n`,
  );

  console.log(
    JSON.stringify(
      {
        status: 'done',
        provider: 'elevenlabs',
        modelId,
        manifestPath: `${scene04AudioPublicDir}/scene04-voiceover.manifest.json`,
        totalFrames,
        beats: generatedBeats,
      },
      null,
      2,
    ),
  );
};

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
