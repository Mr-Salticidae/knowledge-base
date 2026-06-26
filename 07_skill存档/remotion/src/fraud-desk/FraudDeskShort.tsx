import {
  AbsoluteFill,
  Audio,
  interpolate,
  OffthreadVideo,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { beats, buildCaptionPages, TOTAL_FRAMES, VIDEO_TRIM_FRAMES } from './beats';

export const FRAUD_DESK_SHORT_FRAMES = TOTAL_FRAMES;

const CJK = '"Microsoft YaHei", "Microsoft YaHei UI", "SimHei", "Noto Sans CJK SC", sans-serif';
const pages = buildCaptionPages();

const Caption: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const page = pages.find((p) => frame >= p.from && frame < p.to);
  if (!page) return null;
  const t = frame - page.from;
  const pop = spring({ frame: t, fps, config: { damping: 16, stiffness: 150, mass: 0.6 } });
  const y = interpolate(pop, [0, 1], [34, 0]);
  const op = interpolate(pop, [0, 1], [0, 1]);
  const hot = page.section === 'reversal' || page.section === 'cta';
  const big = page.text.length <= 9;
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 360 }}>
      <div
        style={{
          maxWidth: 940,
          textAlign: 'center',
          transform: `translateY(${y}px)`,
          opacity: op,
          fontFamily: CJK,
          fontWeight: 800,
          fontSize: big ? 96 : 76,
          lineHeight: 1.28,
          letterSpacing: 1,
          color: hot ? '#ffe9a8' : '#ffffff',
          textShadow: '0 6px 30px rgba(0,0,0,0.85), 0 2px 8px rgba(0,0,0,0.95)',
          padding: '0 10px',
        }}
      >
        {page.text}
      </div>
    </AbsoluteFill>
  );
};

const HookKicker: React.FC<{ frame: number }> = ({ frame }) => {
  // small label top-left for the first ~2.5s
  const op = interpolate(frame, [0, 8, 70, 80], [0, 1, 1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <div
      style={{
        position: 'absolute',
        top: 150,
        left: 60,
        opacity: op,
        fontFamily: CJK,
        fontWeight: 800,
        fontSize: 40,
        color: '#fff',
        background: 'rgba(193,42,42,0.92)',
        padding: '12px 22px',
        borderRadius: 8,
        textShadow: '0 2px 8px rgba(0,0,0,0.6)',
      }}
    >
      真实案例 · 你也会判错
    </div>
  );
};

const FollowPill: React.FC<{ frame: number; fps: number }> = ({ frame, fps }) => {
  const start = beats.find((b) => b.section === 'cta')!.startFrame;
  if (frame < start) return null;
  const pop = spring({ frame: frame - start, fps, config: { damping: 14, stiffness: 120 } });
  const s = interpolate(pop, [0, 1], [0.7, 1]);
  const op = interpolate(pop, [0, 1], [0, 1]);
  return (
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 180,
        display: 'flex',
        justifyContent: 'center',
        opacity: op,
        transform: `scale(${s})`,
      }}
    >
      <div
        style={{
          fontFamily: CJK,
          fontWeight: 800,
          fontSize: 46,
          color: '#1a140c',
          background: '#ffd24a',
          padding: '18px 40px',
          borderRadius: 999,
          boxShadow: '0 10px 30px rgba(0,0,0,0.45)',
        }}
      >
        ＋ 关注 · 练出反诈直觉
      </div>
    </div>
  );
};

export const FraudDeskShort: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = interpolate(frame, [0, TOTAL_FRAMES], [1.02, 1.08]);
  const fadeIn = interpolate(frame, [0, 8], [0, 1], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{ backgroundColor: '#efe7d6' }}>
      <AbsoluteFill style={{ opacity: fadeIn }}>
        <OffthreadVideo
          src={staticFile('fraud-desk/capture/pilot.mp4')}
          trimBefore={VIDEO_TRIM_FRAMES}
          style={{ width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${scale})` }}
        />
      </AbsoluteFill>

      {beats.map((b) => (
        <Sequence key={b.id} from={b.startFrame} durationInFrames={b.durationInFrames}>
          <Audio src={staticFile(`fraud-desk/audio/${b.id}.mp3`)} />
        </Sequence>
      ))}

      {/* readability scrim — bottom-weighted */}
      <AbsoluteFill
        style={{
          background:
            'linear-gradient(to top, rgba(18,14,8,0.88) 0%, rgba(18,14,8,0.66) 20%, rgba(18,14,8,0.0) 46%)',
        }}
      />

      <Caption frame={frame} fps={fps} />
      <HookKicker frame={frame} />
      <FollowPill frame={frame} fps={fps} />

      {/* watermark */}
      <div
        style={{
          position: 'absolute',
          top: 56,
          right: 40,
          fontFamily: CJK,
          fontWeight: 700,
          fontSize: 30,
          color: 'rgba(255,255,255,0.92)',
          textShadow: '0 2px 8px rgba(0,0,0,0.7)',
          letterSpacing: 1,
        }}
      >
        反诈柜台 · The Fraud Desk
      </div>
    </AbsoluteFill>
  );
};
