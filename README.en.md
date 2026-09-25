# Mr. Jumping Spider · Creative Knowledge Base

[简体中文](README.md) · **English** · [日本語](README.ja.md) · [한국어](README.ko.md) · [繁體中文](README.zh-TW.md)

> A long-term archive of reusable creative assets.
> Started 2026-05-02 · Design principles: **Less is more · Update as you use · No filler**

> [!NOTE]
> This page is a translated overview. The notes themselves are written in Simplified Chinese; the [Chinese README](README.md) and the folder indexes are the canonical, continuously updated maps.
> This page is intentionally a stable guide. It explains what is here and where to start, and does not mirror every new note. Last synced: 2026-09-25.

This is the public AIGC methodology knowledge base of 跳蛛先生 / Mr. Jumping Spider. It records reusable insights from AI image, video and music creation, character consistency, retrospectives, and human–AI collaboration workflows.

It is written for:

- people making AI images, videos or music;
- people studying where tools like Midjourney, Suno, Kling, Seedance and Claude work well together, and where they don't;
- people who manage creative methodology in Obsidian;
- anyone interested in a "creator judges, AI executes" workflow.

What is published here is **methodology and code samples, not an asset pack**. Paths such as `{AIGC工作站}` or `项目工作区/` that appear in the notes are placeholders for the author's local workspace. They record where something came from; you do not need the same folders.

The showcase website [Above the Web (蛛网之上)](https://tiaozhuxiansheng.com) is built from this repository (Chinese only).

---

## What this is

After each creative exploration, the **findings that carry an insight** are distilled here as long-term, reusable assets.

It is an **insight archive, not an output archive**. Images, audio and video usually do not live in this repository. What lives here is "what I learned".

The repository is an **Obsidian vault** (config in `.obsidian/`). Notes link to each other with `[[wikilinks]]`, so you can click through them, or see how the ideas connect in Obsidian's graph view.

---

## Reading it without Chinese

- **Browser translation** works well on GitHub for the prose. File names and links stay in Chinese.
- **LLM translation**: most notes are self-contained, so you can paste a whole note into an LLM and ask for a translation.
- **Prompts**: many of the Midjourney prompts inside the notes are written in English and can be used as-is. Prompts for Chinese-first tools (Kling, Jimeng, etc.) are usually in Chinese.
- **Note anatomy**: most notes open with `一句话总结` (one-line summary), include `如何使用` (how to use), and end with `关联文档` (related documents).

### Glossary of recurring terms

These words appear in file names all the time:

| Term | Meaning |
|---|---|
| 律 | law / rule: a distilled regularity, usually phrased as one sentence |
| 原则 / 法 / 公式 | principle / method / formula |
| 复盘 | retrospective / post-mortem of a real project or competition entry |
| 档案 | profile / dossier (e.g. how a model or `--sref` code behaves) |
| 行为规律 | behavior patterns of a tool or parameter, from hands-on tests |
| 基础句 | base phrase: a reusable prompt block |
| 索引 | index: the entry page of a folder |
| 方法论 / 洞察 | methodology / insight |
| 假说 | hypothesis: not yet confirmed |
| 获奖图 / 冠军 | award-winning image / champion entry (mostly from prompt battles) |
| 学员版 / 公开版 / 同好版 | student / public / fellow-creator edition of a public-facing piece |
| 对外分发 | public distribution: standalone pieces meant to be shared |
| `_v1`, `_v2` … | version of the note |

### Markers

| Marker | Meaning |
|---|---|
| ⭐ | hub note: referenced from many places, an entry-level methodology |
| ⭐⭐ / ⭐⭐⭐ | confirmed in two / three independent cases (⭐⭐⭐ = treated as an iron rule) |
| ✓✓ / ✓✓✓ | verified twice / three times |
| ⚠️首次 | first observation: single case, not yet re-verified |
| ✅首验 | first validation passed |
| 🚧 | work in progress |

---

## How to use this knowledge base

1. **On GitHub**, start from the knowledge map below. Every folder links to its index, which lists everything in it.
2. **In Obsidian**, clone the repository and open the folder as a vault. [README.md](README.md) is the entry map (MOC). Press `Ctrl+G` for the graph view.
3. **Follow the links.** The `关联文档` (related documents) section at the bottom of each note is a doorway to the next idea.

---

## Knowledge map

Organized by folder, mirroring the [Chinese README](README.md). Each folder links to its index, which lists everything in it; only a few entry points are shown here.

### 01 · sref profiles → [index](01_sref档案/01_sref档案索引.md)

One "temperament profile" per Midjourney `--sref` code.

- ⭐ [sref编号独立律_v1](04_方法论与洞察/01_角色一致性与视觉签名/sref编号独立律_v1.md): every sref code is an independent photographer. When you hit a wall, change the signature before you change the tool.

### 02 · Parameter & model behavior → [index](02_参数行为档案/02_参数行为档案索引.md)

How specific model versions and parameters actually behave: Midjourney (`--ow`, `--seed`, multi-sref, v8.1 / v8.2 / niji), Kling, Seedance, Suno, ElevenLabs, and platforms such as Flova.

- [MJ_v8.2_行为档案_v1](02_参数行为档案/MJ_v8.2_行为档案_v1.md): Midjourney v8.2 behavior profile
- [可灵Kling3_0_行为规律_v1](02_参数行为档案/可灵Kling3_0_行为规律_v1.md): Kling 3.0 image-to-video, four iron rules and three red lines
- [Suno_v5.5_行为规律_v1](02_参数行为档案/Suno_v5.5_行为规律_v1.md): Suno v5.5 for soundtracks

### 03 · Prompt template library → [index](03_prompt模板库/03_prompt模板库索引.md)

Reusable base phrases, a moderation-safe vocabulary list, process specs, and retrospectives of award-winning images from prompt battles, including entries that lost.

- ⭐ [OVA怀旧基础句_v1](03_prompt模板库/01_prompt模板/OVA怀旧基础句_v1.md): base phrase for late-1980s Japanese OVA nostalgia (verified three times)
- ⭐⭐⭐ [东方美人五官堆叠基础句_v1](03_prompt模板库/01_prompt模板/东方美人五官堆叠基础句_v1.md): facial-feature stacking block for East Asian beauty portraits

### 04 · Methodology & insights → [index](04_方法论与洞察/04_方法论与洞察索引.md)

Higher-level insights and AI behavior phenomena, in eight sub-areas.

**01 Character consistency & visual signatures**: the thickest thread, from top-level methodology down to parameter tests.

- ⭐ [角色一致性金字塔_v1](04_方法论与洞察/01_角色一致性与视觉签名/角色一致性金字塔_v1.md): the Character Consistency Pyramid, a 4-layer model (sref / oref–seed–descriptors / personalize–moodboard)

**02 Style, aesthetics & image rules**

- [AI甜妹脸vs复古东方美人_v1](04_方法论与洞察/02_风格审美与画面律/AI甜妹脸vs复古东方美人_v1.md): the "sweet AI face" vs. retro East Asian beauty; personalize switches between the two tracks
- [主体不看镜头律_v1](04_方法论与洞察/02_风格审美与画面律/主体不看镜头律_v1.md): in intimate or immersive themes, the subject does not look at the camera

**03 Surrealism & breaking out of saturated ("red ocean") themes**

- ⭐ [超现实主题的冷热两种处理路径_v1](04_方法论与洞察/03_超现实与主题破局/超现实主题的冷热两种处理路径_v1.md): the cold and warm paths for surreal themes
- ⭐ [红海主题的三条破局路径_v1](04_方法论与洞察/03_超现实与主题破局/红海主题的三条破局路径_v1.md): three ways out of a saturated theme: concept, visual spectacle, scarce medium

**04 Video, film & sound**: image-to-video, the "blindfold editing" method (AI drafts the edit, a human reviews it), sound design, TTS quality checks, and full-pipeline retrospectives of short films and MVs.

- [蒙眼剪辑法_方法论笔记_v1](04_方法论与洞察/04_视频影像与声音/蒙眼剪辑法_方法论笔记_v1.md): the blindfold editing method
- [图生视频_ForwardOnly原则_v1](04_方法论与洞察/04_视频影像与声音/图生视频_ForwardOnly原则_v1.md): the forward-only principle for image-to-video
- ⭐⭐ [跨镜道具锁定律_资产图优于形容词_v1](04_方法论与洞察/04_视频影像与声音/跨镜道具锁定律_资产图优于形容词_v1.md): a prop that appears in two or more shots needs its own reference image, not adjectives

**05 Prompt & tool methods**

- ⭐ [生成式vs编辑式工具选择律_v1](04_方法论与洞察/05_prompt与工具方法/生成式vs编辑式工具选择律_v1.md): to change one spot, use an editing model; to create a whole image, use a generative one
- ⭐⭐ [指定对象与气质描述_生成路径分岔律_v1](04_方法论与洞察/05_prompt与工具方法/指定对象与气质描述_生成路径分岔律_v1.md): does the audience need to *recognize* the named work or character? If yes, only cloning / image-to-image preserves it
- ⭐ [标签相同不等于行为相同_第三方代跑平台律_v1](04_方法论与洞察/05_prompt与工具方法/标签相同不等于行为相同_第三方代跑平台律_v1.md): the same model name on a third-party platform is not the same capability. Check the channel, don't trust your eyes.

**06 Collaboration, operations & publishing**: working with Claude Code, Codex, GPT and other tools; delivery discipline; and the voting psychology of peer-voted prompt battles.

- ⭐⭐⭐ [可行性生死线前置律_移植先探一票否决约束_v1](04_方法论与洞察/06_协作运营与发布/可行性生死线前置律_移植先探一票否决约束_v1.md): when porting or switching platforms, probe the one constraint that can veto the whole project first
- ⭐⭐ [开工前先对基线律_v1](04_方法论与洞察/06_协作运营与发布/开工前先对基线律_v1.md): check the baseline (`git fetch`) before writing the first line
- ⭐ [交付前实测证伪律_v1](04_方法论与洞察/06_协作运营与发布/交付前实测证伪律_v1.md): before delivering, write a minimal probe that tries to falsify the solution
- ⭐ [入场票框架_v1](04_方法论与洞察/06_协作运营与发布/入场票框架_v1.md): what makes a "good work": a recognizable concept × an entry ticket

**07 AI theory & creative philosophy**

- ⭐ [压缩保留簇丢弃孤例_v1](04_方法论与洞察/07_AI理论与创作哲学/压缩保留簇丢弃孤例_v1.md): what survives in a model is decided by cluster density, not by "niche vs. mainstream"
- [低频退化与频率定律_v1](04_方法论与洞察/07_AI理论与创作哲学/低频退化与频率定律_v1.md): models understand the *statistical distribution* of language

**08 General-interest research**: classic experiments from social psychology and behavioral science, plus fact-checks of viral AI claims.

- [复印机实验_安慰剂式理由与无意识顺从_v1](04_方法论与洞察/08_通识与趣味研究/复印机实验_安慰剂式理由与无意识顺从_v1.md): Langer's 1978 photocopier experiment on "placebic" reasons
- [AI心理测量实验PsAIch_角色扮演不是内心独白_v1](04_方法论与洞察/08_通识与趣味研究/AI心理测量实验PsAIch_角色扮演不是内心独白_v1.md): the PsAIch study. A role-play is not an inner monologue.

### 05 · Visual systems → [index](05_视觉系统/05_视觉系统索引.md)

- ⭐ [檐下IP_视觉系统_v1](05_视觉系统/檐下IP_视觉系统_v1.md): "Under the Eaves", a classical-style girl IP (seal, typeface, layout)
- ⭐ [R-07_IP_视觉系统_v1](05_视觉系统/R-07_IP_视觉系统_v1.md): R-07, a forgotten robot singing in the ruins

### 06 · Code → [index](06_代码/代码资产索引.md)

Python scripts, cover-layout templates, an MV production pipeline, a beat-tapping web tool and more.

### 07 · Skill archive → [index](07_skill存档/07_skill存档索引.md)

Tested agent skills archived verbatim with version history. How they are mounted and used: [SKILL_INDEX](07_skill存档/SKILL_INDEX.md).

### 08 · Public-facing pieces → [index](08_对外分发/08_对外分发索引.md)

Standalone articles and tutorials for students and readers. They have no wikilinks and can be shared as-is.

### 09 · Platform engineering → [index](09_平台工程/09_平台工程索引.md)

Engineering methods, architecture patterns and pitfalls from building the showcase site and other content platforms: static sites with accounts, deployment, CI, networking.

---

## Directory structure

```
knowledge-base/
├── 00_仓库维护/            repository maintenance: writing conventions, PR checklist, compliance script
├── 01_sref档案/            one file per Midjourney sref code: its "temperament"
├── 02_参数行为档案/         parameter & model behavior profiles (ow / seed / multi-sref / models)
├── 03_prompt模板库/         reusable prompt blocks + retrospectives
│   ├── 01_prompt模板/       base phrases / moderation-safe words / video prompt templates
│   ├── 02_案例复盘/         award-winning images / competition themes / case retrospectives
│   └── 03_流程规范/         asset prep / handoff documents / process specs
├── 04_方法论与洞察/         higher-level insights + AI behavior phenomena
│   ├── 01_角色一致性与视觉签名/   character consistency & visual signatures
│   ├── 02_风格审美与画面律/       style, aesthetics & image rules
│   ├── 03_超现实与主题破局/       surrealism & breaking out of themes
│   ├── 04_视频影像与声音/         video, film & sound
│   ├── 05_prompt与工具方法/       prompt & tool methods
│   ├── 06_协作运营与发布/         collaboration, operations & publishing
│   ├── 07_AI理论与创作哲学/       AI theory & creative philosophy
│   └── 08_通识与趣味研究/         general-interest research
├── 05_视觉系统/             IP-level visual systems
├── 06_代码/                 runnable code assets (cover templates / MV tools / video pipelines)
├── 07_skill存档/            tested skills, archived verbatim with versions
├── 08_对外分发/             standalone public-facing pieces, ready to share
├── 09_平台工程/             engineering for the showcase site and content platforms
├── README.md               the Chinese navigation page
└── README.<lang>.md        translated overviews (this page)
```

---

## Five core rules

1. **No insight, no note.** Not every exploration has to be written down.
2. **Update before you create.** Check whether an existing note can take the new content first.
3. **Every note has a "how to use" and a "related documents" section.** The first makes it a tool; the second keeps it from being an island in the graph.
4. **Reference the source work, don't copy it.**
5. **Register in one place.** Full lists live in each folder's index; the README only navigates and lists hub notes. No dated changelogs: git history is the changelog.

---

## Contributing

Pull requests are welcome. Every PR runs an automated compliance check that looks for absolute paths from other machines, misaligned index columns, and wikilink / frontmatter issues. Foreign paths fail the check and the rest are hints; either way it is a pre-review warning, not a merge gate. Maintainers then review with the [PR review checklist](00_仓库维护/外来提交PR审核清单.md) (Chinese).

New notes follow the [writing conventions](00_仓库维护/知识库写作规范.md) (Chinese): file naming, a single `类型/…` tag in the frontmatter, a `关联文档` section, and registration in the folder index.

---

## License

This knowledge base is licensed under [CC BY-NC 4.0](LICENSE.md) (Attribution-NonCommercial). Please keep the author and repository link when quoting or adapting it. Suggested attribution:

> 跳蛛先生 / Mr. Jumping Spider, 《跳蛛先生 · 创作知识库》

Files under `06_代码/` are workflow examples and study references. They may contain project-specific paths or assumptions and are not guaranteed to run as-is in another environment.
