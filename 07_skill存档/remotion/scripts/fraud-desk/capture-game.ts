import { chromium } from 'playwright';
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, readdirSync, renameSync, rmSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..', '..');
const ffmpeg = path.join(projectRoot, 'node_modules', '@remotion', 'compositor-win32-x64-msvc', 'ffmpeg.exe');

const GAME_URL = process.env.GAME_URL || 'http://localhost:5273/index.html';
const CASE_Q = process.env.CASE_Q || 'actually real';     // ?case= substring
const RULE = process.env.RULE || 'scam';                  // which button to click (scam=诈骗)
const outDir = path.join(projectRoot, 'public', 'fraud-desk', 'capture');
const rawDir = path.join(outDir, '_raw');
const outMp4 = path.join(outDir, 'pilot.mp4');

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

const main = async () => {
  mkdirSync(rawDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  // Playwright video records at CSS viewport size and IGNORES deviceScaleFactor.
  // So record at 540x960 (mobile CSS, exact 9:16) and upscale 2x with lanczos below.
  const context = await browser.newContext({
    viewport: { width: 540, height: 960 },
    deviceScaleFactor: 1,
    locale: 'zh-CN',
    recordVideo: { dir: rawDir, size: { width: 540, height: 960 } },
  });
  // force Chinese before the app boots
  await context.addInitScript(() => {
    try { localStorage.setItem('fd_lang', 'zh'); } catch (e) {}
  });
  const page = await context.newPage();

  const url = `${GAME_URL}?case=${encodeURIComponent(CASE_Q)}`;
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => (document as any).fonts?.ready).catch(() => {});
  await sleep(600);

  // intro -> start the shift (drawRound reads ?case=)
  await page.click('#startBtn');
  await page.waitForSelector('#caseScreen:not(.hidden)', { timeout: 5000 });
  await sleep(400);

  // —— hold on the case page so the SMS is readable (hook + setup narration ~14s) ——
  await sleep(13500);

  // —— rule it (deliberately wrong: scam on a real alert) -> verdict ——
  await page.click(`#caseActions button[data-choice="${RULE}"]`);
  await page.waitForSelector('#verdictBox .verdict', { timeout: 5000 }).catch(() => {});
  await sleep(700);

  // —— hold on the verdict (turn + reversal + CTA narration ~26s) ——
  await sleep(26000);

  await context.close();   // video flushes to disk on close
  await browser.close();

  // move/convert the recorded webm -> pilot.mp4
  const webm = readdirSync(rawDir).find((f) => f.endsWith('.webm'));
  if (!webm) throw new Error('no webm recorded');
  const webmPath = path.join(rawDir, webm);
  const ff = existsSync(ffmpeg) ? ffmpeg : 'ffmpeg';
  execFileSync(ff, ['-y', '-i', webmPath, '-vf', 'scale=1080:1920:flags=lanczos', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-an', outMp4], { stdio: 'inherit' });
  rmSync(rawDir, { recursive: true, force: true });

  const dur = execFileSync(ff.replace('ffmpeg', 'ffprobe'), ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', outMp4], { encoding: 'utf8' }).trim();
  console.log(JSON.stringify({ status: 'done', outMp4: 'fraud-desk/capture/pilot.mp4', durationSec: Number(dur) }, null, 2));
};

main().catch((e) => { console.error(e instanceof Error ? e.message : String(e)); process.exit(1); });
