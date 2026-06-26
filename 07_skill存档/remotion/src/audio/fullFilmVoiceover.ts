export type FullFilmVoiceoverBeat = {
  id: string;
  section: 'intro' | 'teaching' | 'author-note' | 'outro';
  sceneId: string;
  caption: string;
  ttsText: string;
};

const beat = (
  id: string,
  section: FullFilmVoiceoverBeat['section'],
  sceneId: string,
  ttsText: string,
): FullFilmVoiceoverBeat => ({
  id,
  section,
  sceneId,
  caption: ttsText,
  ttsText,
});

// v3.1（2026-06-16 锁定）。母题：助产(maieutic)↔尸检(postmortem)，贯穿案例=真实双题复盘翻车。
// 字幕 = 口播（caption=ttsText 强制统一）。文稿源：production/full_film_2026-06-16_script_v3.1_locked.md
export const fullFilmVoiceoverBeats: FullFilmVoiceoverBeat[] = [
  // 段落 0 · 冷开场
  beat('intro_01_two_partners', 'intro', 'scene_00_two_partners', '我给我的创作，配了俩搭档：一个助产士，一个法医。'),
  beat('intro_02_midwife', 'intro', 'scene_00_two_partners', '创作之前，助产士帮我把脑子里那团乱麻，接生成一个清楚的想法。'),
  beat('intro_03_coroner', 'intro', 'scene_00_two_partners', '作品做完，法医给它来一次冷静的尸检，不许自我美化。'),
  beat('intro_04_whole_life', 'intro', 'scene_00_two_partners', '一头接生，一头验尸。我想给我做的每个东西，一个完整的一生。'),

  // 段落 1 · 它们是什么 = Skill
  beat('teaching_01_not_mystery', 'teaching', 'scene_01_what_is_skill', '这俩搭档，不是什么神秘 AI。说穿了，就是两份我写给 AI 的工作手册。'),
  beat('teaching_02_called_skill', 'teaching', 'scene_01_what_is_skill', '这种手册，有个名字，叫 Skill。'),

  // 段落 2 · 拆开法医（铁律 → 真实翻车 → 修复 → 形态）
  beat('teaching_03_investigate_coroner', 'teaching', 'scene_02_coroner_rule', '篇幅原因，我们先来调研一下法医。它只有一条铁律：先冻结事实，再写判断。'),
  beat('teaching_04_double_contest', 'teaching', 'scene_03_crash_case', '上个月我打了一场双题比赛，两道题的方案票数都靠前，但都没获奖。可我自己整理记录的时候，顺手就把它写成了“获奖图复盘”。'),
  beat('teaching_05_eleven_claims', 'teaching', 'scene_03_crash_case', 'AI 接着这份记录往下整合，真就当成获奖作品，给我分析出十一条“成功经验”。'),
  beat('teaching_06_not_won', 'teaching', 'scene_03_crash_case', '可它根本没获奖。我把我偏爱的方案，当成了获胜的方案。'),
  beat('teaching_07_freeze_first', 'teaching', 'scene_04_freeze_facts', '法医这份手册，逼 AI 动笔前，先在文档最顶上锁死一行事实：这东西到底获奖没有？这行填完，才准往下写。'),
  beat('teaching_08_payoff', 'teaching', 'scene_04_freeze_facts', '于是同一份记录，这次它先把我拦下来：先说清楚，它获奖了吗？那十一条自我表扬，从源头就没了。'),
  beat('teaching_09_markdown_form', 'teaching', 'scene_05_markdown_form', '说穿了，这手册就是个 Markdown 文件。开头写它什么时候被调用，正文写它要守的规矩，头一条就是：禁止把你偏爱的方案，写成获胜的方案。'),

  // 段落 3 · 三个误区
  beat('teaching_10_mistakes_intro', 'teaching', 'scene_06_three_mistakes', '用 Skill，最容易踩三个坑。'),
  beat('teaching_11_not_magic', 'teaching', 'scene_06_three_mistakes', '一，把它当魔法。它不让烂内容变好，只让流程变稳。'),
  beat('teaching_12_missing_files', 'teaching', 'scene_06_three_mistakes', '二，漏掉它引用的文件。点名的模板没带上，AI 照样抓瞎。'),
  beat('teaching_13_no_backup', 'teaching', 'scene_06_three_mistakes', '三，不存版本。调好的手册被随手一改覆盖，连备份都没有。'),

  // 段落 4 · 收束 · 一生
  beat('teaching_14_two_ends', 'teaching', 'scene_07_whole_life_close', '一个助产士，一个法医，一头一尾。中间那段创作，还是我自己来。'),
  beat('teaching_15_not_from_zero', 'teaching', 'scene_07_whole_life_close', '但有了这两份手册，我不再是每次从零开始，AI 也不再是转头就忘的临时工。'),
  beat('teaching_16_life_loop', 'teaching', 'scene_07_whole_life_close', '从一个念头出生，到一个作品落幕。这一回，有人替我认真对待了它的一生。'),

  // 段落 5 · 作者的话（压缩版）
  beat('author_01_cant_edit', 'author-note', 'scene_08_author_note', '一句私心：我自己不会剪辑，这条片子从画面、配音到剪辑，全是 AI 按 Skill 做的。'),
  beat('author_02_validate', 'author-note', 'scene_08_author_note', '我想验证的就是，只要把流程写清楚，不会剪辑的人，也能把想法变成作品。'),
  beat('author_03_open_source', 'author-note', 'scene_08_author_note', '代码会开源，欢迎一起来调试。'),
];

export const fullFilmVoiceoverText = fullFilmVoiceoverBeats.map((item) => item.ttsText).join('\n\n');

export const fullFilmVoiceover = {
  id: 'full_film_20260616_voiceover',
  audioPublicDir: 'audio/full_film_20260616',
  manifestPublicPath: 'audio/full_film_20260616/voiceover.manifest.json',
  source: 'fullFilmVoiceoverBeats',
  text: fullFilmVoiceoverText,
  beatCount: fullFilmVoiceoverBeats.length,
};
