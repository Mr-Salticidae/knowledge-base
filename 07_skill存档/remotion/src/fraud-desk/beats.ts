// Pilot timing for《反诈柜台》short. Durations measured from ElevenLabs output
// (scripts/fraud-desk/generate-voiceover.ts → voiceover.timing.json). 字幕 = 逐字口播.
export const FPS = 30;
export const WIDTH = 1080;
export const HEIGHT = 1920;

// Raw capture: case page appears ~2.0s, verdict ~16.0s. Trim so comp t≈0 = case
// page and the verdict reveal (~comp t14) lands on the "turn" narration (b3).
export const VIDEO_TRIM_FRAMES = 58;

export type Beat = {
  id: string;
  section: 'hook' | 'setup' | 'turn' | 'reversal' | 'cta';
  text: string;
  startFrame: number;
  durationInFrames: number;
};

export const beats: Beat[] = [
  { id: 'b1_hook', section: 'hook', text: '凌晨一点，你妈收到条短信：银行卡刚在境外被刷了六千八，让她马上冻结。', startFrame: 0, durationInFrames: 241 },
  { id: 'b2_setup', section: 'setup', text: '九五开头的号，金额吓人，口气紧急。第一反应——诈骗，拦掉。', startFrame: 241, durationInFrames: 181 },
  { id: 'b3_turn', section: 'turn', text: '但它没让你点链接、没要验证码、没让你把钱转去安全账户。它只让你打自己卡背面的电话。', startFrame: 422, durationInFrames: 259 },
  { id: 'b4_reversal', section: 'reversal', text: '这条，是真的。真银行的盗刷预警就长这样。你把它当骗局拦了，你妈下次就再也不信预警——这才是骗子最想要的。', startFrame: 681, durationInFrames: 332 },
  { id: 'b5_cta', section: 'cta', text: '真预警把主动权还给你，骗局想自己攥着。关注，练出反诈直觉。', startFrame: 1013, durationInFrames: 202 },
];

export const TOTAL_FRAMES = beats.reduce((n, b) => Math.max(n, b.startFrame + b.durationInFrames), 0);

export type CaptionPage = { text: string; from: number; to: number; section: Beat['section'] };

// One short clause per "page" (TikTok-style swap). Even sub-timing within each beat.
export const buildCaptionPages = (): CaptionPage[] => {
  const pages: CaptionPage[] = [];
  for (const b of beats) {
    const clauses = b.text.split(/[，。、！？：—]/).map((s) => s.trim()).filter(Boolean);
    const per = b.durationInFrames / clauses.length;
    clauses.forEach((c, i) => {
      pages.push({
        text: c,
        from: Math.round(b.startFrame + i * per),
        to: Math.round(b.startFrame + (i + 1) * per),
        section: b.section,
      });
    });
  }
  return pages;
};
