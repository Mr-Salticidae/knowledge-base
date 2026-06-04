import { Composition } from 'remotion';
import { ExplainerVideo, TOTAL_FRAMES } from './compositions/ExplainerVideo';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="SkillIsAllYouNeed"
      component={ExplainerVideo}
      durationInFrames={TOTAL_FRAMES}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
