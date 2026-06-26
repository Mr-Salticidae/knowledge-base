import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');
const envPath = path.join(projectRoot, '.env');

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

const main = async () => {
  loadLocalEnv();
  const apiKey = process.env.ELEVENLABS_API_KEY?.trim();
  if (!apiKey) throw new Error('no ELEVENLABS_API_KEY');
  const res = await fetch('https://api.elevenlabs.io/v2/voices?page_size=100', {
    headers: { 'xi-api-key': apiKey },
  });
  if (!res.ok) throw new Error(`voices list failed ${res.status}: ${await res.text()}`);
  const data = (await res.json()) as any;
  const voices = (data.voices ?? []).map((v: any) => ({
    id: v.voice_id,
    name: v.name,
    gender: v.labels?.gender,
    accent: v.labels?.accent,
    age: v.labels?.age,
    desc: v.labels?.description ?? v.labels?.descriptive,
    lang: v.fine_tuning?.language ?? v.verified_languages?.map((x: any) => x.language).join(',') ?? '',
    category: v.category,
  }));
  console.log('TOTAL', voices.length);
  for (const v of voices) console.log(JSON.stringify(v));
};

main().catch((e) => {
  console.error(e instanceof Error ? e.message : String(e));
  process.exit(1);
});
