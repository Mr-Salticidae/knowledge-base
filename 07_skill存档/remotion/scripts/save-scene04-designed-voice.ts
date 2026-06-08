import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scene04VoiceDescription } from '../src/audio/voiceDesign';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');
const envPath = path.join(projectRoot, '.env');
const selectedGeneratedVoiceId = process.env.ELEVENLABS_SELECTED_GENERATED_VOICE_ID?.trim() || '2UxEbGrUFQytPRKqCe66';
const voiceName = process.env.ELEVENLABS_NEW_VOICE_NAME?.trim() || 'Skill Explainer Creator CN';

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

const upsertEnvValue = (key: string, value: string) => {
  const lines = existsSync(envPath) ? readFileSync(envPath, 'utf8').split(/\r?\n/) : [];
  const nextLines = lines.filter((line, index) => !(index === lines.length - 1 && line === ''));
  const existingIndex = nextLines.findIndex((line) => line.startsWith(`${key}=`));

  if (existingIndex >= 0) {
    nextLines[existingIndex] = `${key}=${value}`;
  } else {
    nextLines.push(`${key}=${value}`);
  }

  writeFileSync(envPath, `${nextLines.join('\n')}\n`);
};

const main = async () => {
  loadLocalEnv();

  const apiKey = requiredEnv('ELEVENLABS_API_KEY');

  const response = await fetch('https://api.elevenlabs.io/v1/text-to-voice', {
    method: 'POST',
    headers: {
      'xi-api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      voice_name: voiceName,
      voice_description: scene04VoiceDescription,
      generated_voice_id: selectedGeneratedVoiceId,
      labels: {
        language: 'zh',
        use_case: 'aigc_explainer',
        project: 'skill_is_all_you_need',
      },
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`ElevenLabs create voice failed with status ${response.status}: ${errorText}`);
  }

  const result = (await response.json()) as { voice_id: string; name?: string; category?: string };

  if (!result.voice_id) {
    throw new Error('ElevenLabs create voice response did not include voice_id.');
  }

  upsertEnvValue('ELEVENLABS_VOICE_ID', result.voice_id);

  console.log(
    JSON.stringify(
      {
        status: 'done',
        voiceName,
        selectedGeneratedVoiceId,
        voiceId: result.voice_id,
        category: result.category,
        envUpdated: 'ELEVENLABS_VOICE_ID',
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
