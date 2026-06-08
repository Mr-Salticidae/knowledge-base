import React from 'react';
import { Audio, staticFile } from 'remotion';

export const VoiceoverAudio: React.FC = () => <Audio src={staticFile('audio/voiceover.mp3')} />;
