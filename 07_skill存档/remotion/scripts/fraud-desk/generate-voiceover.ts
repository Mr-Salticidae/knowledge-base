import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');
const envPath = path.join(projectRoot, '.env');
const fps = 30;
const outputFormat = 'mp3_44100_128';
const audioDir = path.join(projectRoot, 'public', 'fraud-desk', 'audio');
const timingPath = path.join(audioDir, 'voiceover.timing.json');
const bundledFfprobe = path.join(projectRoot, 'node_modules', '@remotion', 'compositor-win32-x64-msvc', 'ffprobe.exe');

// Jason Chen - Deep, Magnetic and Calm (beijing mandarin). Override via env if desired.
const DEFAULT_VOICE = 'DowyQ68vDpgFYdWVGjc3';

// 字幕 = 逐字口播(caption 与 ttsText 完全一致,不写情绪控制标签)
const beats = [
  { id: 'b1_hook',     section: 'hook',     text: '凌晨一点，你妈收到条短信：银行卡刚在境外被刷了六千八，让她马上冻结。' },
  { id: 'b2_setup',    section: 'setup',    text: '九五开头的号，金额吓人，口气紧急。第一反应——诈骗，拦掉。' },
  { id: 'b3_turn',     section: 'turn',     text: '但它没让你点链接、没要验证码、没让你把钱转去安全账户。它只让你打自己卡背面的电话。' },
  { id: 'b4_reversal', section: 'reversal', text: '这条，是真的。真银行的盗刷预警就长这样。你把它当骗局拦了，你妈下次就再也不信预警——这才是骗子最想要的。' },
  { id: 'b5_cta',      section: 'cta',      text: '真预警把主动权还给你，骗局想自己攥着。关注，练出反诈直觉。' },
];

const loadLocalEnv = () => {
  if (!existsSync(envPath)) return;
  for (const line of readFileSync(envPath, 'utf8').split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const i = t.indexOf('=');
    if (i === -1) continue;
    const k = t.slice(0, i).trim();
    const v = t.slice(i + 1).trim().replace(/^["']|["']$/g, '');
    if (k && process.env[k] === undefined) process.env[k] = v;
  }
};

const durationSecondsFor = (filePath: string) => {
  const cmd = existsSync(bundledFfprobe) ? bundledFfprobe : 'ffprobe';
  const out = execFileSync(cmd, ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filePath], { encoding: 'utf8' }).trim();
  const d = Number(out);
  if (!Number.isFinite(d) || d <= 0) throw new Error(`bad duration for ${filePath}`);
  return d;
};

const main = async () => {
  loadLocalEnv();
  const apiKey = process.env.ELEVENLABS_API_KEY?.trim();
  if (!apiKey) throw new Error('ELEVENLABS_API_KEY missing');
  const voiceId = process.env.FRAUD_VOICE_ID?.trim() || DEFAULT_VOICE;
  const modelId = process.env.FRAUD_MODEL_ID?.trim() || 'eleven_multilingual_v2';
  const force = process.env.FORCE === '1';

  mkdirSync(audioDir, { recursive: true });

  let startFrame = 0;
  const out: any[] = [];
  for (const b of beats) {
    const file = path.join(audioDir, `${b.id}.mp3`);
    if (force || !existsSync(file)) {
      const res = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=${outputFormat}`, {
        method: 'POST',
        headers: { 'xi-api-key': apiKey, 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: b.text,
          model_id: modelId,
          voice_settings: { stability: 0.55, similarity_boost: 0.8, style: 0.2, use_speaker_boost: true },
        }),
      });
      if (!res.ok) throw new Error(`TTS ${b.id} failed ${res.status}: ${await res.text()}`);
      writeFileSync(file, Buffer.from(await res.arrayBuffer()));
    }
    const durationSeconds = durationSecondsFor(file);
    const durationInFrames = Math.ceil(durationSeconds * fps);
    out.push({ id: b.id, section: b.section, caption: b.text, audioSrc: `fraud-desk/audio/${b.id}.mp3`, startFrame, durationInFrames, durationSeconds });
    startFrame += durationInFrames;
  }

  const totalFrames = startFrame;
  writeFileSync(timingPath, JSON.stringify({ provider: 'elevenlabs', modelId, voiceId, fps, totalFrames, totalSeconds: +(totalFrames / fps).toFixed(2), beats: out }, null, 2));
  console.log(JSON.stringify({ status: 'done', voiceId, modelId, totalSeconds: +(totalFrames / fps).toFixed(2), beats: out.map((b) => ({ id: b.id, sec: +b.durationSeconds.toFixed(2) })) }, null, 2));
};

main().catch((e) => { console.error(e instanceof Error ? e.message : String(e)); process.exit(1); });
