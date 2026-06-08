import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scene04VoiceDescription, scene04VoicePreviewText } from '../src/audio/voiceDesign';
import { applyPronunciationFixes, pronunciationFixes } from '../src/audio/scene04Voiceover';

type VoicePreview = {
  audio_base_64?: string;
  audio_base64?: string;
  generated_voice_id: string;
  media_type?: string;
  duration_secs?: number;
};

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const envPath = path.join(projectRoot, '.env');
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
  const modelId = process.env.ELEVENLABS_TEXT_TO_VOICE_MODEL_ID?.trim() || 'eleven_ttv_v3';
  const previewDir = path.join(projectRoot, 'public', 'audio', 'scene_04', 'voice_design');

  mkdirSync(previewDir, { recursive: true });

  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-voice/design?output_format=${outputFormat}`, {
    method: 'POST',
    headers: {
      'xi-api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      voice_description: scene04VoiceDescription,
      model_id: modelId,
      text: applyPronunciationFixes(scene04VoicePreviewText),
      auto_generate_text: false,
      loudness: 0.35,
      guidance_scale: 5,
      ...(modelId === 'eleven_multilingual_ttv_v2' ? { quality: 0.6 } : {}),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`ElevenLabs voice design failed with status ${response.status}: ${errorText}`);
  }

  const result = (await response.json()) as { previews: VoicePreview[]; text: string };

  const previews = result.previews.map((preview, index) => {
    const audioBase64 = preview.audio_base_64 ?? preview.audio_base64;
    const fileName = `scene04_voice_candidate_${String(index + 1).padStart(2, '0')}.mp3`;

    if (audioBase64) {
      writeFileSync(path.join(previewDir, fileName), Buffer.from(audioBase64, 'base64'));
    }

    return {
      index: index + 1,
      generatedVoiceId: preview.generated_voice_id,
      previewPath: audioBase64 ? `public/audio/scene_04/voice_design/${fileName}` : undefined,
      mediaType: preview.media_type,
      durationSeconds: preview.duration_secs,
    };
  });

  const manifest = {
    provider: 'elevenlabs',
    modelId,
    outputFormat,
    createdAt: new Date().toISOString(),
    voiceDescription: scene04VoiceDescription,
    previewText: result.text,
    pronunciationFixes,
    previews,
    nextStep:
      'Listen to the preview mp3 files, choose one generatedVoiceId, then create/save that voice in ElevenLabs before using it as ELEVENLABS_VOICE_ID.',
  };

  writeFileSync(path.join(previewDir, 'scene04-voice-design.manifest.json'), `${JSON.stringify(manifest, null, 2)}\n`);

  console.log(JSON.stringify({ status: 'done', previewDir: 'public/audio/scene_04/voice_design', previews }, null, 2));
};

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
