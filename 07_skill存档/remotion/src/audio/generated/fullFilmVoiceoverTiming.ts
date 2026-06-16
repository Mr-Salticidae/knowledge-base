export type FullFilmVoiceoverTimingBeat = {
  id: string;
  section: string;
  sceneId: string;
  caption: string;
  audioSrc: string;
  startFrame: number;
  durationInFrames: number;
  durationSeconds: number;
};

// PROVISIONAL（估算 timing，无真实音频）。由 scripts/estimate-full-film-timing.ts 生成。
// 真实音频生成后会被 scripts/generate-full-film-voiceover.ts 覆盖（hasGeneratedAudio=true）。
export const fullFilmVoiceoverTiming = {
  hasGeneratedAudio: false,
  fps: 30,
  playbackRate: 1.05,
  totalFrames: 4627,
  beats: [
    {
        "id": "intro_01_two_partners",
        "section": "intro",
        "sceneId": "scene_00_two_partners",
        "caption": "我给我的创作，配了俩搭档：一个助产士，一个法医。",
        "audioSrc": "audio/full_film_20260616/intro_01_two_partners.mp3",
        "startFrame": 0,
        "durationInFrames": 151,
        "durationSeconds": 4.86
    },
    {
        "id": "intro_02_midwife",
        "section": "intro",
        "sceneId": "scene_00_two_partners",
        "caption": "创作之前，助产士帮我把脑子里那团乱麻，接生成一个清楚的想法。",
        "audioSrc": "audio/full_film_20260616/intro_02_midwife.mp3",
        "startFrame": 151,
        "durationInFrames": 184,
        "durationSeconds": 6
    },
    {
        "id": "intro_03_coroner",
        "section": "intro",
        "sceneId": "scene_00_two_partners",
        "caption": "作品做完，法医给它来一次冷静的尸检，不许自我美化。",
        "audioSrc": "audio/full_film_20260616/intro_03_coroner.mp3",
        "startFrame": 335,
        "durationInFrames": 157,
        "durationSeconds": 5.05
    },
    {
        "id": "intro_04_whole_life",
        "section": "intro",
        "sceneId": "scene_00_two_partners",
        "caption": "一头接生，一头验尸。我想给我做的每个东西，一个完整的一生。",
        "audioSrc": "audio/full_film_20260616/intro_04_whole_life.mp3",
        "startFrame": 492,
        "durationInFrames": 178,
        "durationSeconds": 5.81
    },
    {
        "id": "teaching_01_not_mystery",
        "section": "teaching",
        "sceneId": "scene_01_what_is_skill",
        "caption": "这俩搭档，不是什么神秘 AI。说穿了，就是两份我写给 AI 的工作手册。",
        "audioSrc": "audio/full_film_20260616/teaching_01_not_mystery.mp3",
        "startFrame": 670,
        "durationInFrames": 200,
        "durationSeconds": 6.57
    },
    {
        "id": "teaching_02_called_skill",
        "section": "teaching",
        "sceneId": "scene_01_what_is_skill",
        "caption": "这种手册，有个名字，叫 Skill。",
        "audioSrc": "audio/full_film_20260616/teaching_02_called_skill.mp3",
        "startFrame": 870,
        "durationInFrames": 113,
        "durationSeconds": 3.53
    },
    {
        "id": "teaching_03_investigate_coroner",
        "section": "teaching",
        "sceneId": "scene_02_coroner_rule",
        "caption": "篇幅原因，我们先来调研一下法医。它只有一条铁律：先冻结事实，再写判断。",
        "audioSrc": "audio/full_film_20260616/teaching_03_investigate_coroner.mp3",
        "startFrame": 983,
        "durationInFrames": 211,
        "durationSeconds": 6.95
    },
    {
        "id": "teaching_04_double_contest",
        "section": "teaching",
        "sceneId": "scene_03_crash_case",
        "caption": "上个月我打了一场双题比赛，两道题的方案票数都靠前，但都没获奖。可我自己整理记录的时候，顺手就把它写成了“获奖图复盘”。",
        "audioSrc": "audio/full_film_20260616/teaching_04_double_contest.mp3",
        "startFrame": 1194,
        "durationInFrames": 341,
        "durationSeconds": 11.51
    },
    {
        "id": "teaching_05_eleven_claims",
        "section": "teaching",
        "sceneId": "scene_03_crash_case",
        "caption": "AI 接着这份记录往下整合，真就当成获奖作品，给我分析出十一条“成功经验”。",
        "audioSrc": "audio/full_film_20260616/teaching_05_eleven_claims.mp3",
        "startFrame": 1535,
        "durationInFrames": 222,
        "durationSeconds": 7.33
    },
    {
        "id": "teaching_06_not_won",
        "section": "teaching",
        "sceneId": "scene_03_crash_case",
        "caption": "可它根本没获奖。我把我偏爱的方案，当成了获胜的方案。",
        "audioSrc": "audio/full_film_20260616/teaching_06_not_won.mp3",
        "startFrame": 1757,
        "durationInFrames": 162,
        "durationSeconds": 5.24
    },
    {
        "id": "teaching_07_freeze_first",
        "section": "teaching",
        "sceneId": "scene_04_freeze_facts",
        "caption": "法医这份手册，逼 AI 动笔前，先在文档最顶上锁死一行事实：这东西到底获奖没有？这行填完，才准往下写。",
        "audioSrc": "audio/full_film_20260616/teaching_07_freeze_first.mp3",
        "startFrame": 1919,
        "durationInFrames": 287,
        "durationSeconds": 9.61
    },
    {
        "id": "teaching_08_payoff",
        "section": "teaching",
        "sceneId": "scene_04_freeze_facts",
        "caption": "于是同一份记录，这次它先把我拦下来：先说清楚，它获奖了吗？那十一条自我表扬，从源头就没了。",
        "audioSrc": "audio/full_film_20260616/teaching_08_payoff.mp3",
        "startFrame": 2206,
        "durationInFrames": 265,
        "durationSeconds": 8.85
    },
    {
        "id": "teaching_09_markdown_form",
        "section": "teaching",
        "sceneId": "scene_05_markdown_form",
        "caption": "说穿了，这手册就是个 Markdown 文件。开头写它什么时候被调用，正文写它要守的规矩，头一条就是：禁止把你偏爱的方案，写成获胜的方案。",
        "audioSrc": "audio/full_film_20260616/teaching_09_markdown_form.mp3",
        "startFrame": 2471,
        "durationInFrames": 385,
        "durationSeconds": 13.03
    },
    {
        "id": "teaching_10_mistakes_intro",
        "section": "teaching",
        "sceneId": "scene_06_three_mistakes",
        "caption": "用 Skill，最容易踩三个坑。",
        "audioSrc": "audio/full_film_20260616/teaching_10_mistakes_intro.mp3",
        "startFrame": 2856,
        "durationInFrames": 102,
        "durationSeconds": 3.15
    },
    {
        "id": "teaching_11_not_magic",
        "section": "teaching",
        "sceneId": "scene_06_three_mistakes",
        "caption": "一，把它当魔法。它不让烂内容变好，只让流程变稳。",
        "audioSrc": "audio/full_film_20260616/teaching_11_not_magic.mp3",
        "startFrame": 2958,
        "durationInFrames": 151,
        "durationSeconds": 4.86
    },
    {
        "id": "teaching_12_missing_files",
        "section": "teaching",
        "sceneId": "scene_06_three_mistakes",
        "caption": "二，漏掉它引用的文件。点名的模板没带上，AI 照样抓瞎。",
        "audioSrc": "audio/full_film_20260616/teaching_12_missing_files.mp3",
        "startFrame": 3109,
        "durationInFrames": 168,
        "durationSeconds": 5.43
    },
    {
        "id": "teaching_13_no_backup",
        "section": "teaching",
        "sceneId": "scene_06_three_mistakes",
        "caption": "三，不存版本。调好的手册被随手一改覆盖，连备份都没有。",
        "audioSrc": "audio/full_film_20260616/teaching_13_no_backup.mp3",
        "startFrame": 3277,
        "durationInFrames": 168,
        "durationSeconds": 5.43
    },
    {
        "id": "teaching_14_two_ends",
        "section": "teaching",
        "sceneId": "scene_07_whole_life_close",
        "caption": "一个助产士，一个法医，一头一尾。中间那段创作，还是我自己来。",
        "audioSrc": "audio/full_film_20260616/teaching_14_two_ends.mp3",
        "startFrame": 3445,
        "durationInFrames": 184,
        "durationSeconds": 6
    },
    {
        "id": "teaching_15_not_from_zero",
        "section": "teaching",
        "sceneId": "scene_07_whole_life_close",
        "caption": "但有了这两份手册，我不再是每次从零开始，AI 也不再是转头就忘的临时工。",
        "audioSrc": "audio/full_film_20260616/teaching_15_not_from_zero.mp3",
        "startFrame": 3629,
        "durationInFrames": 211,
        "durationSeconds": 6.95
    },
    {
        "id": "teaching_16_life_loop",
        "section": "teaching",
        "sceneId": "scene_07_whole_life_close",
        "caption": "从一个念头出生，到一个作品落幕。这一回，有人替我认真对待了它的一生。",
        "audioSrc": "audio/full_film_20260616/teaching_16_life_loop.mp3",
        "startFrame": 3840,
        "durationInFrames": 206,
        "durationSeconds": 6.76
    },
    {
        "id": "author_01_cant_edit",
        "section": "author-note",
        "sceneId": "scene_08_author_note",
        "caption": "一句私心：我自己不会剪辑，这条片子从画面、配音到剪辑，全是 AI 按 Skill 做的。",
        "audioSrc": "audio/full_film_20260616/author_01_cant_edit.mp3",
        "startFrame": 4046,
        "durationInFrames": 238,
        "durationSeconds": 7.9
    },
    {
        "id": "author_02_validate",
        "section": "author-note",
        "sceneId": "scene_08_author_note",
        "caption": "我想验证的就是，只要把流程写清楚，不会剪辑的人，也能把想法变成作品。",
        "audioSrc": "audio/full_film_20260616/author_02_validate.mp3",
        "startFrame": 4284,
        "durationInFrames": 206,
        "durationSeconds": 6.76
    },
    {
        "id": "author_03_open_source",
        "section": "author-note",
        "sceneId": "scene_08_author_note",
        "caption": "代码会开源，欢迎一起来调。",
        "audioSrc": "audio/full_film_20260616/author_03_open_source.mp3",
        "startFrame": 4490,
        "durationInFrames": 92,
        "durationSeconds": 2.77
    }
] satisfies FullFilmVoiceoverTimingBeat[],
};
