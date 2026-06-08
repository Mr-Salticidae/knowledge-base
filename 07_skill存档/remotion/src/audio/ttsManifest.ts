export type TtsManifest = {
  provider: 'elevenlabs';
  modelId: string;
  voiceId: string;
  audioPath: string;
  source: 'sceneSpecs.narrationBeats';
  sceneCount: number;
  beatCount: number;
  createdAt: string;
  textLength: number;
  outputFormat: string;
  durationSeconds?: number;
};

export const buildTtsManifest = (params: Omit<TtsManifest, 'provider' | 'source' | 'createdAt'>): TtsManifest => ({
  provider: 'elevenlabs',
  source: 'sceneSpecs.narrationBeats',
  createdAt: new Date().toISOString(),
  ...params,
});
