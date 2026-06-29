import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type { MotionSpec, SubjectSpec } from '../data/sceneSpecs';
import { palette, theme } from '../styles/palette';
import { mergeMotionStyles } from '../utils/motion';

type Props = {
  subject: SubjectSpec;
  motions: MotionSpec[];
};

const TextInside: React.FC<{ label?: string; color?: string; size?: number }> = ({ label, color = theme.darkText, size = 30 }) =>
  label ? (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        color,
        fontFamily: '"Microsoft YaHei", sans-serif',
        fontSize: size,
        fontWeight: 800,
        lineHeight: 1.15,
        padding: 18,
      }}
    >
      {label}
    </div>
  ) : null;

const Manual: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <svg viewBox="0 0 520 360" width="100%" height="100%" role="img" aria-label={label ?? 'Manual'}>
    <filter id="manualShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feDropShadow dx="0" dy="14" stdDeviation="10" floodColor="#020617" floodOpacity="0.28" />
    </filter>
    <g filter="url(#manualShadow)">
      <path d="M46 62c0-22 18-40 40-40h178c24 0 44 20 44 44v272H86c-22 0-40-18-40-40Z" fill={color} stroke="#0F172A" strokeWidth="10" />
      <path d="M474 62c0-22-18-40-40-40H304c-24 0-44 20-44 44v272h174c22 0 40-18 40-40Z" fill="#F8FAFC" stroke="#0F172A" strokeWidth="10" />
      <path d="M260 54v284" stroke="#0F172A" strokeWidth="8" strokeLinecap="round" opacity="0.42" />
      <path d="M96 92h142M96 132h112M96 216h126M96 256h86" stroke="#0F172A" strokeWidth="12" strokeLinecap="round" opacity="0.36" />
      <path d="M318 90h110M318 132h82M318 190h124M318 230h92" stroke="#0F172A" strokeWidth="12" strokeLinecap="round" opacity="0.32" />
      <rect x="92" y="158" width="126" height="44" rx="18" fill="#F8FAFC" stroke="#0F172A" strokeWidth="7" opacity="0.92" />
      <rect x="316" y="260" width="110" height="44" rx="18" fill={color} stroke="#0F172A" strokeWidth="7" />
      {label ? (
        <text x="155" y="190" textAnchor="middle" fill="#0F172A" fontFamily="Microsoft YaHei, sans-serif" fontSize="30" fontWeight="900">
          {label}
        </text>
      ) : null}
    </g>
  </svg>
);

const Human: React.FC<{ color: string }> = ({ color }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    <div style={{ position: 'absolute', left: '34%', top: '4%', width: '32%', height: '24%', borderRadius: '50%', background: '#FBCFE8', border: '7px solid #0F172A' }} />
    <div style={{ position: 'absolute', left: '23%', top: '30%', width: '54%', height: '52%', borderRadius: '42px 42px 24px 24px', background: color, border: '7px solid #0F172A' }} />
    <div style={{ position: 'absolute', left: '14%', top: '42%', width: '20%', height: '14%', borderRadius: 999, background: color, border: '6px solid #0F172A' }} />
    <div style={{ position: 'absolute', right: '14%', top: '42%', width: '20%', height: '14%', borderRadius: 999, background: color, border: '6px solid #0F172A' }} />
  </div>
);

const AiAssistant: React.FC<{ color: string }> = ({ color }) => (
  <svg viewBox="0 0 360 360" width="100%" height="100%" role="img" aria-label="AI assistant">
    <filter id="assistantShadow" x="-15%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="9" floodColor="#020617" floodOpacity="0.26" />
    </filter>
    <g filter="url(#assistantShadow)">
      <path d="M180 54V24" stroke="#0F172A" strokeWidth="10" strokeLinecap="round" />
      <circle cx="180" cy="22" r="18" fill="#FACC15" stroke="#0F172A" strokeWidth="8" />
      <rect x="62" y="68" width="236" height="184" rx="58" fill={color} stroke="#0F172A" strokeWidth="10" />
      <rect x="88" y="94" width="184" height="116" rx="38" fill="#E0F2FE" stroke="#0F172A" strokeWidth="7" opacity="0.95" />
      <circle cx="132" cy="144" r="16" fill="#0F172A" />
      <circle cx="220" cy="144" r="16" fill="#0F172A" />
      <circle cx="138" cy="138" r="5" fill="#F8FAFC" />
      <circle cx="226" cy="138" r="5" fill="#F8FAFC" />
      <path d="M146 176c22 16 48 16 70 0" fill="none" stroke="#0F172A" strokeWidth="9" strokeLinecap="round" />
      <rect x="94" y="236" width="52" height="54" rx="18" fill={color} stroke="#0F172A" strokeWidth="8" />
      <rect x="214" y="236" width="52" height="54" rx="18" fill={color} stroke="#0F172A" strokeWidth="8" />
      <rect x="132" y="248" width="96" height="70" rx="28" fill="#F8FAFC" stroke="#0F172A" strokeWidth="9" />
      <path d="M154 274h52M166 296h28" stroke="#0F172A" strokeWidth="8" strokeLinecap="round" opacity="0.45" />
      <circle cx="280" cy="84" r="14" fill="#4ADE80" stroke="#0F172A" strokeWidth="6" />
      <path d="M74 170h-22M308 170h-22" stroke="#0F172A" strokeWidth="10" strokeLinecap="round" />
    </g>
  </svg>
);

const MarkdownFile: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <svg viewBox="0 0 360 480" width="100%" height="100%" role="img" aria-label={label ?? 'Markdown file'}>
    <filter id="fileShadow" x="-10%" y="-8%" width="120%" height="125%">
      <feDropShadow dx="0" dy="14" stdDeviation="10" floodColor="#020617" floodOpacity="0.24" />
    </filter>
    <g filter="url(#fileShadow)">
      <path d="M44 22h228l84 84v330c0 24-20 44-44 44H44c-24 0-44-20-44-44V66c0-24 20-44 44-44Z" fill={color} stroke="#0F172A" strokeWidth="10" />
      <path d="M270 24v68c0 18 14 32 32 32h54Z" fill="#E2E8F0" stroke="#0F172A" strokeWidth="8" strokeLinejoin="round" />
      <rect x="28" y="56" width="202" height="58" rx="20" fill="#0F172A" />
      <text x="48" y="96" fill="#F8FAFC" fontFamily="JetBrains Mono, Fira Code, monospace" fontSize="30" fontWeight="900">
        {label ?? 'SKILL.md'}
      </text>
      <rect x="38" y="152" width="118" height="30" rx="15" fill="#22D3EE" stroke="#0F172A" strokeWidth="5" />
      <rect x="174" y="152" width="84" height="30" rx="15" fill="#FACC15" stroke="#0F172A" strokeWidth="5" />
      <path d="M44 220h230M44 260h278M44 300h204M44 354h250M44 394h158" stroke="#0F172A" strokeWidth="14" strokeLinecap="round" opacity="0.34" />
      <path d="M44 190h76" stroke="#0F172A" strokeWidth="10" strokeLinecap="round" opacity="0.58" />
      <path d="M74 222v78" stroke="#22D3EE" strokeWidth="9" strokeLinecap="round" opacity="0.9" />
      <path d="M72 354v42" stroke="#FACC15" strokeWidth="9" strokeLinecap="round" opacity="0.9" />
    </g>
  </svg>
);

const IndexCard: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <div style={{ position: 'absolute', inset: 0, borderRadius: 22, background: color, border: '7px solid #0F172A' }}>
    <TextInside label={label} size={28} />
  </div>
);

const PromptBubble: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <div style={{ position: 'absolute', inset: 0, borderRadius: 999, background: color, border: '7px solid #0F172A' }}>
    <div style={{ position: 'absolute', left: '14%', bottom: '-13%', width: '18%', height: '30%', transform: 'rotate(32deg)', background: color, borderLeft: '7px solid #0F172A', borderBottom: '7px solid #0F172A' }} />
    <TextInside label={label} size={26} />
  </div>
);

const WarningIcon: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <div style={{ position: 'absolute', inset: 0 }}>
    <div style={{ position: 'absolute', left: '13%', top: '5%', width: '74%', height: '74%', clipPath: 'polygon(50% 0, 100% 100%, 0 100%)', background: '#0F172A' }} />
    <div style={{ position: 'absolute', left: '19%', top: '12%', width: '62%', height: '60%', clipPath: 'polygon(50% 0, 100% 100%, 0 100%)', background: color }} />
    <div style={{ position: 'absolute', left: '47%', top: '31%', width: '6%', height: '23%', borderRadius: 999, background: '#0F172A' }} />
    <div style={{ position: 'absolute', left: '46%', top: '60%', width: '8%', height: '8%', borderRadius: '50%', background: '#0F172A' }} />
    <div
      style={{
        position: 'absolute',
        left: 0,
        right: 0,
        bottom: 0,
        textAlign: 'center',
        color: '#F8FAFC',
        fontSize: 26,
        fontWeight: 800,
        textShadow:
          '2px 0 0 #0F172A, -2px 0 0 #0F172A, 0 2px 0 #0F172A, 0 -2px 0 #0F172A, 2px 2px 0 #0F172A, -2px 2px 0 #0F172A, 2px -2px 0 #0F172A, -2px -2px 0 #0F172A',
      }}
    >
      {label}
    </div>
  </div>
);

const LibraryShelf: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <div style={{ position: 'absolute', inset: 0, borderRadius: 26, background: color, border: '8px solid #0F172A', padding: 28 }}>
    {[0, 1, 2].map((row) => (
      <div key={row} style={{ position: 'absolute', left: '7%', right: '7%', top: `${20 + row * 25}%`, height: '17%', borderBottom: '8px solid rgba(15,23,42,0.7)' }}>
        {[0, 1, 2, 3, 4].map((book) => (
          <div key={book} style={{ position: 'absolute', left: `${book * 18 + 3}%`, bottom: 0, width: '10%', height: `${54 + ((book + row) % 3) * 16}%`, borderRadius: '8px 8px 0 0', background: [palette.yellow, palette.green, palette.orange, palette.purple, palette.cyan][book], border: '4px solid #0F172A' }} />
        ))}
      </div>
    ))}
    <TextInside label={label} color="#F8FAFC" size={30} />
  </div>
);

const DataPacket: React.FC<{ color: string }> = ({ color }) => (
  <div style={{ position: 'absolute', inset: '10%', borderRadius: 20, background: color, border: '6px solid #0F172A' }}>
    <div style={{ position: 'absolute', inset: '22%', border: '5px solid rgba(15,23,42,0.5)', borderRadius: 14 }} />
  </div>
);

const Arrow: React.FC<{ color: string }> = ({ color }) => (
  <div style={{ position: 'absolute', left: 0, right: 0, top: '41%', height: '18%', background: color }}>
    <div style={{ position: 'absolute', right: '-1%', top: '-75%', width: '33%', height: '250%', clipPath: 'polygon(0 0, 100% 50%, 0 100%)', background: color }} />
  </div>
);

const AbstractShape: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <div style={{ position: 'absolute', inset: 0, borderRadius: 36, background: color, border: '8px solid #0F172A' }}>
    <div style={{ position: 'absolute', inset: '-12%', borderRadius: 52, border: '6px solid rgba(255,255,255,0.45)' }} />
    <TextInside label={label} />
  </div>
);

export const Subject: React.FC<Props> = ({ subject, motions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const color = palette[subject.colorToken];
  const subjectMotions = motions.filter((motion) => motion.targetId === subject.id);
  const motionStyle = mergeMotionStyles(frame, fps, subjectMotions);

  const content = (() => {
    switch (subject.type) {
      case 'human':
        return <Human color={color} />;
      case 'ai-assistant':
        return <AiAssistant color={color} />;
      case 'manual':
        return <Manual color={color} label={subject.label} />;
      case 'markdown-file':
        return <MarkdownFile color={color} label={subject.label} />;
      case 'index-card':
        return <IndexCard color={color} label={subject.label} />;
      case 'prompt-bubble':
        return <PromptBubble color={color} label={subject.label} />;
      case 'warning-icon':
        return <WarningIcon color={color} label={subject.label} />;
      case 'library-shelf':
        return <LibraryShelf color={color} label={subject.label} />;
      case 'data-packet':
        return <DataPacket color={color} />;
      case 'arrow':
        return <Arrow color={color} />;
      case 'abstract-shape':
      default:
        return <AbstractShape color={color} label={subject.label} />;
    }
  })();

  return (
    <div
      style={{
        position: 'absolute',
        left: `${subject.position.x}%`,
        top: `${subject.position.y}%`,
        width: subject.size.w,
        height: subject.size.h,
        transform: 'translate(-50%, -50%)',
        zIndex: 10,
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          transform: subject.rotation ? `rotate(${subject.rotation}deg)` : undefined,
          ...motionStyle,
        }}
      >
        {content}
      </div>
    </div>
  );
};
