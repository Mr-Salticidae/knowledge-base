import { Composition } from 'remotion';
import { ExplainerVideo, TOTAL_FRAMES } from './compositions/ExplainerVideo';
import { Scene04MotionTest, SCENE_04_MOTION_TEST_FRAMES } from './compositions/Scene04MotionTest';

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
    <Composition
      id="Scene04MotionTest"
      component={Scene04MotionTest}
      durationInFrames={SCENE_04_MOTION_TEST_FRAMES}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
