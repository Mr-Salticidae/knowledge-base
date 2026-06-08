import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildNarrationScript } from '../src/audio/buildNarrationScript';
import { buildTtsManifest } from '../src/audio/ttsManifest';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const envPath = path.join(projectRoot, '.env');
const audioDir = path.join(projectRoot, 'public', 'audio');
const audioPath = path.join(audioDir, 'voiceover.mp3');
const manifestPath = path.join(audioDir, 'voiceover.manifest.json');
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

const main = async () => {
  loadLocalEnv();

  const apiKey = requiredEnv('ELEVENLABS_API_KEY');
  const voiceId = requiredEnv('ELEVENLABS_VOICE_ID');
  const modelId = process.env.ELEVENLABS_MODEL_ID?.trim() || 'eleven_v3';
  const script = buildNarrationScript();

  mkdirSync(audioDir, { recursive: true });

  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=${outputFormat}`, {
    method: 'POST',
    headers: {
      'xi-api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text: script.text,
      model_id: modelId,
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75,
        style: 0.25,
        use_speaker_boost: true,
      },
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`ElevenLabs TTS failed with status ${response.status}: ${errorText}`);
  }

  const audio = Buffer.from(await response.arrayBuffer());
  writeFileSync(audioPath, audio);

  const manifest = buildTtsManifest({
    modelId,
    voiceId,
    audioPath: 'public/audio/voiceover.mp3',
    sceneCount: script.sceneCount,
    beatCount: script.beatCount,
    textLength: script.textLength,
    outputFormat,
  });

  writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

  console.log(
    JSON.stringify(
      {
        status: 'done',
        provider: manifest.provider,
        modelId: manifest.modelId,
        audioPath: manifest.audioPath,
        manifestPath: 'public/audio/voiceover.manifest.json',
        sceneCount: manifest.sceneCount,
        beatCount: manifest.beatCount,
        textLength: manifest.textLength,
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
