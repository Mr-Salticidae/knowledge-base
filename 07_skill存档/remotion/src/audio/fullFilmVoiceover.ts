export type FullFilmVoiceoverBeat = {
  id: string;
  section: 'intro' | 'teaching' | 'author-note' | 'outro';
  sceneId: string;
  caption: string;
  ttsText: string;
};

const captionFrom = (text: string) => text.replace(/\[[^\]]+\]\s*/g, '').trim();

const beat = (
  id: string,
  section: FullFilmVoiceoverBeat['section'],
  sceneId: string,
  ttsText: string,
): FullFilmVoiceoverBeat => ({
  id,
  section,
  sceneId,
  caption: captionFrom(ttsText),
  ttsText,
});

export const fullFilmVoiceoverBeats: FullFilmVoiceoverBeat[] = [
  beat(
    'intro_01_same_ai_forgets',
    'intro',
    'scene_00_intro_question',
    '[curious] 同一个 AI，昨天刚教会它你的偏好，今天换个新对话，它又像第一次见你一样。',
  ),
  beat(
    'intro_02_repeat_process',
    'intro',
    'scene_00_intro_question',
    '你明明已经总结过流程，但每次开工，还是要重新解释一遍。',
  ),
  beat(
    'intro_03_should_remember',
    'intro',
    'scene_00_intro_question',
    '如果 AI 真的能帮我们工作，那它不该只会回答问题。',
  ),
  beat(
    'intro_04_skill_promise',
    'intro',
    'scene_00_intro_question',
    '[slight pause] 它应该记住流程，调用工具，并且稳定复现一套做事方法。这就是这期视频要讲的东西：Skill。',
  ),
  beat('teaching_01_skill_word', 'teaching', 'scene_01_hook', '[calm] 你可能听过一个很酷的词：Skill。'),
  beat('teaching_02_plugin_misread', 'teaching', 'scene_01_hook', '很多人以为它是神秘插件。'),
  beat('teaching_03_not_magic', 'teaching', 'scene_01_hook', '但真正有用的地方，不在神秘感。'),
  beat('teaching_04_smart_assistant', 'teaching', 'scene_02_forgetful_assistant', '想象你雇了一位聪明的 AI 助理。'),
  beat('teaching_05_fast_execution', 'teaching', 'scene_02_forgetful_assistant', '它理解很快，执行也很快。'),
  beat('teaching_06_forgets_every_time', 'teaching', 'scene_02_forgetful_assistant', '但每次新对话前，它都会失忆。'),
  beat('teaching_07_manual_metaphor', 'teaching', 'scene_03_skill_as_manual', 'Skill 更像一本岗位手册。'),
  beat('teaching_08_role_workflow_rules', 'teaching', 'scene_03_skill_as_manual', '它把角色、流程和规则写清楚。'),
  beat('teaching_09_repeatable_work', 'teaching', 'scene_03_skill_as_manual', '下次 AI 接手，就不用从头教。'),
  beat('teaching_10_repeated_instruction', 'teaching', 'scene_04_repeat_to_skill', '反复教同一件事，先别急着加 prompt。'),
  beat('teaching_11_patterns_emerge', 'teaching', 'scene_04_repeat_to_skill', '重复的格式、流程和避坑，就是模式。'),
  beat('teaching_12_compress_to_skill', 'teaching', 'scene_04_repeat_to_skill', '把模式压缩成手册，它就变成 Skill。'),
  beat('teaching_13_markdown_file', 'teaching', 'scene_05_markdown_structure', '它通常就是一个 Markdown 文件。'),
  beat('teaching_14_yaml_trigger', 'teaching', 'scene_05_markdown_structure', '前面写触发条件：什么时候调用。'),
  beat('teaching_15_body_rules', 'teaching', 'scene_05_markdown_structure', '正文写工作规则：怎么执行。'),
  beat('teaching_16_index_metaphor', 'teaching', 'scene_06_skill_index', 'SKILL_INDEX 像图书馆索引。'),
  beat('teaching_17_where_to_find', 'teaching', 'scene_06_skill_index', '它告诉 AI：有哪些手册、放在哪里。'),
  beat('teaching_18_when_to_use', 'teaching', 'scene_06_skill_index', '也告诉 AI：什么时候取哪一本。'),
  beat('teaching_19_not_magic', 'teaching', 'scene_07_common_mistakes', '第一个误区：把 Skill 当魔法。'),
  beat('teaching_20_missing_files', 'teaching', 'scene_07_common_mistakes', '第二个误区：漏掉引用文件。'),
  beat('teaching_21_no_backup', 'teaching', 'scene_07_common_mistakes', '第三个误区：没有版本存档。'),
  beat('teaching_22_not_the_end', 'teaching', 'scene_08_ending_system', '最后，Skill 不是终点。'),
  beat('teaching_23_personal_system', 'teaching', 'scene_08_ending_system', '它让工作流变成个人系统。'),
  beat('teaching_24_skill_library', 'teaching', 'scene_08_ending_system', '手册越多，能力库越完整。'),
  beat('author_01_thanks', 'author-note', 'author_01_loop_closed', '[warm] 感谢你看到这里。'),
  beat('author_02_loop_closed', 'author-note', 'author_01_loop_closed', '如果你喜欢这期视频，那么这条链路就顺利完成了闭环。'),
  beat(
    'author_03_ai_made_this',
    'author-note',
    'author_02_ai_made_this',
    '这条视频，除了文稿的核心，以及我现在说的这些话以外，全部是 AI 制作的。',
  ),
  beat(
    'author_04_assets',
    'author-note',
    'author_02_ai_made_this',
    '包括但不限于：图片、动画、配音、配乐，以及剪辑。',
  ),
  beat('author_05_goal', 'author-note', 'author_03_motivation', '这也是我追求的目标。'),
  beat(
    'author_06_cant_edit',
    'author-note',
    'author_03_motivation',
    '我有很多稀奇古怪的想法，但是苦于不会剪辑，无法表达。',
  ),
  beat('author_07_project_reason', 'author-note', 'author_03_motivation', '所以我做了这个项目。'),
  beat(
    'author_08_not_showoff',
    'author-note',
    'author_03_motivation',
    '它不是为了炫技，而是为了把不会剪辑的人，也接入视频表达。',
  ),
  beat(
    'author_09_stack',
    'author-note',
    'author_04_stack',
    '技术栈其实很简单：Midjourney，Seedance，Eleven，Remotion，Suno，还有 Codex。',
  ),
  beat('author_10_roles_hint', 'author-note', 'author_04_stack', '你大体可以猜到它们各自的分工。'),
  beat(
    'author_11_tool_roles',
    'author-note',
    'author_04_stack',
    'Midjourney 负责建立视觉锚点。Seedance 负责让图里的机制动起来。Eleven 负责把文稿变成声音。Suno 负责让情绪有一条底层轨道。Remotion 负责时间线、字幕和最终合成。',
  ),
  beat('author_12_codex_conductor', 'author-note', 'author_05_codex_conductor', '[confident] 而 Codex，是总指挥。'),
  beat(
    'author_13_skill_process',
    'author-note',
    'author_05_codex_conductor',
    '一切由 Skill 充当标准流程。Codex 引导众多 AI 工具各司其职。',
  ),
  beat(
    'author_14_industrialize',
    'author-note',
    'author_06_industrialization',
    '理论上，只要把 prompt 调优到足够稳定，就可以把任意文稿，工业化地、自动化地，生产成任意风格的视频。',
  ),
  beat('author_15_need_you', 'author-note', 'author_06_industrialization', '而这个调优过程，需要各位的参与。'),
  beat('author_16_limited', 'author-note', 'author_06_industrialization', '我的能力有限，只能抛砖引玉。'),
  beat('author_17_personal_view', 'author-note', 'author_07_open_source', '[slight pause] 最后，我想记录一些个人看法。'),
  beat('author_18_can_close', 'author-note', 'author_07_open_source', '不感兴趣的话，现在可以酌情关闭视频了。'),
  beat('author_19_question', 'author-note', 'author_07_open_source', '有朋友问我：这个项目这么有价值，还要坚持开源吗？'),
  beat('author_20_open_source', 'author-note', 'author_07_open_source', '[firm] 我的回答是：开源。而且是一定要开源。'),
  beat('author_21_face', 'author-note', 'author_07_open_source', '就要狠狠打字节的脸。'),
  beat(
    'author_22_final_statement',
    'author-note',
    'author_07_open_source',
    '因为，正如群星必须回归轨道，“无产阶级”的铡刀也终将落下。',
  ),
  beat('outro_01_title', 'outro', 'author_08_final_words', '[calm] Skill Is All You Need。'),
  beat('outro_02_method', 'outro', 'author_08_final_words', '把流程写成手册，把手册交给 AI，把想法变成作品。'),
  beat('outro_03_credit', 'outro', 'author_08_final_words', '作者：跳蛛先生。'),
];

export const fullFilmVoiceoverText = fullFilmVoiceoverBeats.map((item) => item.ttsText).join('\n\n');

export const fullFilmVoiceover = {
  id: 'full_film_20260609_voiceover',
  audioPublicDir: 'audio/full_film_20260609',
  manifestPublicPath: 'audio/full_film_20260609/voiceover.manifest.json',
  source: 'fullFilmVoiceoverBeats',
  text: fullFilmVoiceoverText,
  beatCount: fullFilmVoiceoverBeats.length,
};
