import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { formalClipVoiceover, formalClipVoiceoverBeats } from '../src/audio/formalClipVoiceover';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const envPath = path.join(projectRoot, '.env');
const fps = 30;
const outputFormat = 'mp3_44100_128';
const audioDir = path.join(projectRoot, 'public', 'audio', 'formal_clip_20260608');
const manifestPath = path.join(audioDir, 'voiceover.manifest.json');
const timingPath = path.join(projectRoot, 'src', 'audio', 'generated', 'formalClipVoiceoverTiming.ts');

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

type GeneratedBeat = {
  id: string;
  sceneId: string;
  caption: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

const writeTimingFile = (beats: GeneratedBeat[], totalFrames: number) => {
  const content = `export type FormalClipVoiceoverTimingBeat = {
  id: string;
  sceneId: string;
  caption: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

export const formalClipVoiceoverTiming = {
  hasGeneratedAudio: true,
  fps: ${fps},
  totalFrames: ${totalFrames},
  beats: ${JSON.stringify(beats, null, 4)} satisfies FormalClipVoiceoverTimingBeat[],
};
`;

  writeFileSync(timingPath, content);
};

const main = async () => {
  loadLocalEnv();

  const apiKey = requiredEnv('ELEVENLABS_API_KEY');
  const voiceId = requiredEnv('ELEVENLABS_VOICE_ID');
  const modelId = process.env.ELEVENLABS_MODEL_ID?.trim() || 'eleven_v3';

  mkdirSync(audioDir, { recursive: true });

  const generatedBeats: GeneratedBeat[] = [];
  let startFrame = 0;

  for (const beat of formalClipVoiceoverBeats) {
    const fileName = `${beat.id}.mp3`;
    const filePath = path.join(audioDir, fileName);

    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=${outputFormat}`, {
      method: 'POST',
      headers: {
        'xi-api-key': apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: beat.ttsText,
        model_id: modelId,
        voice_settings: {
          stability: 0.52,
          similarity_boost: 0.75,
          style: 0.22,
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
    const durationInFrames = Math.max(45, Math.ceil(durationSeconds * fps) + 12);
    const audioSrc = `${formalClipVoiceover.audioPublicDir}/${fileName}`;

    generatedBeats.push({
      id: beat.id,
      sceneId: beat.sceneId,
      caption: beat.caption,
      audioSrc,
      startFrame,
      durationInFrames,
      durationSeconds,
    });

    startFrame += durationInFrames;
  }

  const tailHoldFrames = 30;
  const totalFrames = startFrame + tailHoldFrames;

  writeTimingFile(generatedBeats, totalFrames);
  writeFileSync(
    manifestPath,
    `${JSON.stringify(
      {
        provider: 'elevenlabs',
        modelId,
        voiceId,
        source: 'formalClipVoiceoverBeats',
        outputFormat,
        fps,
        totalFrames,
        tailHoldFrames,
        createdAt: new Date().toISOString(),
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
        modelId,
        manifestPath: formalClipVoiceover.manifestPublicPath,
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
