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
  <div style={{ position: 'absolute', inset: 0, borderRadius: 24, background: color, border: '8px solid rgba(15,23,42,0.65)' }}>
    <div style={{ position: 'absolute', left: '48%', top: 0, bottom: 0, width: 8, background: 'rgba(15,23,42,0.28)' }} />
    <div style={{ position: 'absolute', left: '12%', right: '56%', top: '22%', height: 12, borderRadius: 10, background: 'rgba(15,23,42,0.32)' }} />
    <div style={{ position: 'absolute', left: '56%', right: '12%', top: '36%', height: 12, borderRadius: 10, background: 'rgba(15,23,42,0.32)' }} />
    <div style={{ position: 'absolute', left: '56%', right: '20%', top: '52%', height: 12, borderRadius: 10, background: 'rgba(15,23,42,0.22)' }} />
    <TextInside label={label} />
  </div>
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
  <div style={{ position: 'absolute', inset: 0 }}>
    <div style={{ position: 'absolute', left: '13%', top: '12%', width: '74%', height: '62%', borderRadius: 44, background: color, border: '8px solid #0F172A' }} />
    <div style={{ position: 'absolute', left: '31%', top: '32%', width: '11%', height: '11%', borderRadius: '50%', background: '#0F172A' }} />
    <div style={{ position: 'absolute', right: '31%', top: '32%', width: '11%', height: '11%', borderRadius: '50%', background: '#0F172A' }} />
    <div style={{ position: 'absolute', left: '36%', top: '55%', width: '28%', height: '7%', borderRadius: 999, background: '#0F172A' }} />
    <div style={{ position: 'absolute', left: '47%', top: 0, width: '6%', height: '16%', background: '#0F172A' }} />
    <div style={{ position: 'absolute', left: '43%', top: '-6%', width: '14%', height: '14%', borderRadius: '50%', background: '#FACC15', border: '6px solid #0F172A' }} />
  </div>
);

const MarkdownFile: React.FC<{ color: string; label?: string }> = ({ color, label }) => (
  <div style={{ position: 'absolute', inset: 0, borderRadius: 22, background: color, border: '8px solid #0F172A', overflow: 'hidden' }}>
    <div style={{ height: '20%', background: '#0F172A', color: '#F8FAFC', display: 'flex', alignItems: 'center', paddingLeft: 30, fontSize: 30, fontWeight: 800 }}>{label}</div>
    {['---', 'name: skill', 'description: workflow', '---', '## Rules'].map((line, index) => (
      <div key={line} style={{ position: 'absolute', left: 34, right: 34, top: `${30 + index * 12}%`, height: 10, borderRadius: 999, background: index < 3 ? '#22D3EE' : '#94A3B8' }} />
    ))}
  </div>
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
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, textAlign: 'center', color: '#F8FAFC', fontSize: 26, fontWeight: 800 }}>{label}</div>
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
