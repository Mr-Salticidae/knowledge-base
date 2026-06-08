import { Composition } from 'remotion';
import { ExplainerVideo, TOTAL_FRAMES } from './compositions/ExplainerVideo';
import { FormalClip20260608, FORMAL_CLIP_20260608_FRAMES } from './compositions/FormalClip20260608';
import { FullFilmVideo, FULL_FILM_FRAMES } from './compositions/FullFilmVideo';
import { Scene04MotionTest, SCENE_04_MOTION_TEST_FRAMES } from './compositions/Scene04MotionTest';
import { Scene05MotionTest, SCENE_05_MOTION_TEST_FRAMES } from './compositions/Scene05MotionTest';

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
      id="SkillIsAllYouNeedFullFilm"
      component={FullFilmVideo}
      durationInFrames={FULL_FILM_FRAMES}
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
    <Composition
      id="Scene05MotionTest"
      component={Scene05MotionTest}
      durationInFrames={SCENE_05_MOTION_TEST_FRAMES}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="FormalClip20260608"
      component={FormalClip20260608}
      durationInFrames={FORMAL_CLIP_20260608_FRAMES}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
