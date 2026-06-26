---
tags: [类型/协作工具链, 工具/Remotion, 工具/ElevenLabs, 工具/Whisper, 平台/抖音, 平台/B站, 平台/快手]
---
# 短视频批量分发方案 · 蒙眼剪辑法 × Remotion × 抖音/B站/快手 (v1)

> 入档:2026-06-26
> 触发项目:《反诈柜台 The Fraud Desk》(单文件 HTML/JS 反诈 web 游戏,314 案件,竖屏手机界面)
> 性质:**方案书 / 可复用 SOP**。以反诈柜台为首个落地样例,但管线对任何"有结构化数据 + 网页/图文素材"的项目通用。
> 一句话:**把蒙眼剪辑法从"单片精修"升级为"母版 + 批量",用 Remotion 把 314 个案件程序化批量出竖屏短视频,一稿母版过审、代码批量分发抖音/B站/快手。**

---

## 零、为什么是这套组合(战略判断)

1. **图文流量天花板低,视频是增量入口**。小红书图文已就绪(见 [[小红书导流话术合规红线_扣1领资料_v1]] 同项目),但抖音/B站/快手是视频平台,图文几乎没有自然流量。要拿这三个平台的量,必须出视频。
2. **反诈题材 + 314 案件 = 程序化批量的完美场景**。每个案件本身就是一条 15–30 秒短视频的天然脚本(一条诈骗/真消息 → 审 → 判 → 揭红旗)。内容是结构化数据,不是需要逐条手工创意的素材——这正是 Remotion `dataset-render` 最擅长的形态。
3. **已有 Remotion 实战基建可直接复用**。本人已跑通 Eleven 分段旁白 → 真实 duration 反推 timing → Suno 取段 → 全片字幕 BGM(见 [[2026-06-09_Remotion全片音频字幕BGM复盘]] / [[2026-06-08_Remotion_MJ_Seedance混合动画闭环复盘]])。本方案**不重教基础**,只在已验证管线上加三块新能力。
4. **反诈受众与短视频下沉人群高度重叠**。快手/抖音的中老年、下沉用户正是诈骗高危人群,"转给爸妈"的传播场景天然成立,公益属性也利于平台推荐。

---

## 一、蒙眼剪辑法 v4:从"单片精修"到"母版 + 批量"

蒙眼剪辑法的内核不变(见 [[蒙眼剪辑法_方法论笔记]]):**AI 看不见视频,所以人做感性判断、AI 做精确执行;配置与逻辑分离;音频先行;字幕=逐字口播。** 批量化只是把"人的判断"放在不同的位置:

| | 单片模式(凝视/Skill 全片) | 批量模式(反诈柜台 314 条) |
|---|---|---|
| 人审核的对象 | 每一条成片,迭代到 v17 | **一个竖屏母版模板**(1 条样片审到满意) |
| AI 执行 | 按反馈逐条改代码 | 母版过审后,**314 条 `renderMedia` 批量出片** |
| 感性判断密度 | 高(每条都看) | 前移、集中(只在母版 + 抽检若干条) |
| 风险 | 慢 | 母版有缺陷会被放大 314 倍 → **母版必须审狠** |

> **关键洞察(v4 新增)**:批量化没有违背蒙眼剪辑法,而是把"人不可见但必须判断"的成本**前移并复用**——人把一条母版看到极致,模板内的变量位(案件文本、录屏、旁白)交给数据驱动。代价是:母版阶段的反馈必须比单片更苛刻,因为它会被复制 N 次。

**两条铁律照搬,不打折**(已在全片复盘二次验证):
- **音频先行**:先定稿每条案件的旁白文稿 → TTS 生成 → 读真实 duration → `calculateMetadata` 反推帧数。绝不手数帧。
- **字幕=逐字口播**:短视频字幕首先是听觉校验层。本方案用 Whisper 对**实际 TTS 音频**转写生成逐词字幕——天然满足"字幕=口播",还顺带拿到 TikTok 蹦字效果。技术英文名词留画面、不进 TTS。

---

## 二、技术管线:四块拼装,每块有现成代码

整体数据流(faceless 五层管线的反诈柜台版):

```text
案件数据(314 条,已在 script.js LIBRARY)
  → 旁白文稿(LLM 按案件生成 3-4 句钩子+判读)
  → TTS 中文配音(Eleven / Fish Audio)→ narration.wav + 真实 duration
  → Whisper 逐词转写 → captions.json(逐词时间戳)
  → Playwright 录屏(竖屏游戏操作)→ recording.mp4
  → Remotion 母版 Composition(props=案件)→ renderMedia 批量
  → out/{caseId}.mp4(1080×1920 母版,三平台共用)
```

合成结构固定三层(从下到上):

```text
┌─────────────────────────────────────┐
│  顶层  <Audio> 旁白 + 低音量 BGM(Suno 取段)│
│  中层  TikTok 逐词字幕(安全带内,蹦字高亮)   │
│  底层  <OffthreadVideo> 游戏竖屏录屏 / 卡片背景 │
└─────────────────────────────────────┘
```

### 2.1 竖屏母版 Composition(新能力①:9:16)

竖屏只是把尺寸换成 1080×1920;关键是 `calculateMetadata` 按音频反推时长——这正是已验证的"音频先行"在批量场景的落地:

```tsx
<Composition
  id="FraudDeskShort"
  component={FraudDeskShort}
  fps={30}
  width={1080}
  height={1920}
  defaultProps={{ caseId: '001' }}
  calculateMetadata={async ({ props }) => {
    const dur = await getAudioDuration(`audio/${props.caseId}.wav`); // 真实音频长度
    return { durationInFrames: Math.ceil(dur * 30), props };
  }}
/>
```

### 2.2 游戏素材:Playwright 录屏 → OffthreadVideo(新能力②)

游戏是 localhost 单文件网页,**不重写进 React**(成本高),而是 Playwright 脚本化录"审案→盖章"这段操作,产出干净竖屏 webm,再喂 Remotion。一个脚本配不同案件数据 = 一批确定性录屏(无真人鼠标抖动):

```js
const context = await browser.newContext({
  viewport: { width: 1080, height: 1920 },
  recordVideo: { dir: 'recordings/', size: { width: 1080, height: 1920 } },
});
const page = await context.newPage();
await page.goto('http://localhost:5273');
await page.click('#startBtn');
// …脚本化走到目标案件,点"诈骗/属实",停在判定页
await context.close();   // close 时才落盘 webm → ffmpeg 转 mp4
```

Remotion 里用 `<OffthreadVideo>`(渲染期 FFmpeg 外部抽帧,比 `<Video>` 准):

```tsx
<OffthreadVideo src={staticFile(`rec/${caseId}.mp4`)}
  trimBefore={30} style={{ width: 1080, height: 1920 }} />
```

> 为什么不直接 Playwright 录全片:浏览器录制的时长/FPS 不稳定、看机器性能。正确分工 = **Playwright 只录"游戏操作"素材,整片合成交给 Remotion 逐帧渲染**。这与蒙眼剪辑法"AI 用代码精确执行"一脉相承。

### 2.3 配音 + 逐词字幕(新能力③:Whisper TikTok 蹦字)

沿用已有 Eleven 管线;新增 `@remotion/install-whisper-cpp` + `@remotion/captions`:

```ts
// 1) 对实际 TTS 音频转写,逐词时间戳
const { transcription } = await transcribe({
  inputPath: 'narration.wav',  // 16kHz WAV
  whisperPath: './whisper.cpp', model: 'medium',   // 中文用 medium/large
  tokenLevelTimestamps: true,
});
const { captions } = toCaptions({ whisperCppOutput: transcription }); // 注意:convertToCaptions 已废弃

// 2) 切页 + 逐词高亮(TikTok 风格)
const { pages } = createTikTokStyleCaptions({
  captions, combineTokensWithinMilliseconds: 1000,  // 小=逐字蹦,大=整句一页
});
```

最省事起点:**clone 官方 TikTok 模板做底座**(内置 Whisper 自动安装 + `node sub.mjs <video>` 一键转写 + `<TikTokPage>` 逐词组件),把 `WHISPER_MODEL` 改中文即可,不要从零搭字幕。

### 2.4 批量:bundle 一次 + dataset-render 串行(新能力③:规模)

```ts
const serveUrl = await bundle({ entryPoint: './src/index.ts' });   // 打包一次
for (const c of cases) {                                            // 串行,勿并发
  const comp = await selectComposition({ serveUrl, id: 'FraudDeskShort', inputProps: c });
  await renderMedia({ composition: comp, serveUrl, codec: 'h264',
    outputLocation: `out/${c.id}.mp4`, inputProps: c });
}
```

> 官方明确:**不要并发渲染多条**(资源竞争);串行循环,单条内用 `--concurrency` 吃满 CPU。Windows 下 `--props` 必须传文件名,不能内联 JSON(shell 吃引号)。

**链接附录(均已核实可访问)**
- dataset 批量渲染 https://www.remotion.dev/docs/dataset-render ·calculateMetadata https://www.remotion.dev/docs/calculate-metadata
- TikTok 字幕模板 https://github.com/remotion-dev/template-tiktok ·toCaptions https://www.remotion.dev/docs/install-whisper-cpp/to-captions ·createTikTokStyleCaptions https://www.remotion.dev/docs/captions/create-tiktok-style-captions
- OffthreadVideo https://www.remotion.dev/docs/offthreadvideo ·Playwright 录像 https://playwright.dev/docs/videos
- 参考管线:claude-video-kit(中文 TTS,音频反推时长)https://github.com/runesleo/claude-video-kit ·ClawVid(TTS-first)https://github.com/neur0map/clawvid

---

## 三、单条视频的"成片公式"(短视频留存硬规律落地)

有数据支撑的硬规律(来源:OpusClip 完播率复盘、TikTok 安全区/3 秒规则指南):

- **时长 20–34 秒**完播率最高(21–34s 平均 62%,60s+ 掉到 48%)。反诈柜台单案例做成 **22–30 秒**。
- **前 3 秒痛点钩子**留住 80–90% 观众;痛点型钩子比泛开场多 23% 留存。反诈题材天生适合("这条短信能让你倾家荡产")。
- **字幕全程在屏**:带字幕留存高 12%,60–70% 用户静音看。字幕不是可选项。
- **每 3–5 秒一次画面变化 / pattern interrupt**;录屏要勤切镜、配蹦字。
- **结论/反转前置**:前 15 秒给"答案"留存高 20%——别把"这是诈骗"全憋到最后。
- **竖屏安全区**:字幕和关键动作留中央安全带,避开顶部/底部平台 UI(点赞、文案、进度条)遮挡。
- **CTA 放后段**(payoff 之后),别在前 3 秒打断钩子。

**反诈柜台 30 秒母版分镜(模板,变量位用 `{}`)**:

```text
0.0–3.0s  钩子   黑底大字 + 旁白:"{这条 95 开头的短信,让她三分钟转走 8 万}"
                 ↓ 画面闪现案件短信(障眼)
3.0–8.0s  入场   游戏录屏:案件物证页推入,倒计时跳动,旁白读关键句
8.0–18s   审读   录屏:逐条划过红旗/障眼点,逐词字幕同步高亮("链接域名差一个字")
18–24s    判决   录屏:盖章瞬间(FRAUD/属实)+ 反转旁白("它其实是真的——你刚误伤了客户")
24–30s    收尾   信任/止损数字 + CTA:"{关注,练成反诈肌肉记忆}" + 小站水印
```

---

## 四、平台分发 playbook(抖音/B站/快手差异)

**同一条 1080×1920 母版三平台通用**,差异只在**封面 / 标题 / 标签 / 时长取舍 / 调性文案**——这些都是发布层参数,不需要重渲染。

| 维度 | 抖音 | B站 | 快手 |
|---|---|---|---|
| 核心指标 | 完播 + 互动,推荐流为王 | 标题点击 + 弹幕 + 三连,可沉淀 | 关注 + 私域,老铁文化 |
| 最佳时长 | 22–30s,越短越易完播 | 可 60–90s,知识区容忍长 | 20–35s,接地气 |
| 标题调性 | 痛点钩子党("我把它改到能骗过你") | 知识党+悬念("用代码做了个会骗你的反诈游戏") | 大白话("爸妈千万别信这条短信") |
| 标签 | 话题挑战 #反诈 #vibecoding | 分区=科技/编程,合集归档 | #反诈 #老铁 接地气词 |
| 链接 | 简介不放链接(限流),引导主页 | 简介可放小站链接 | 引导关注私域,家人转发 |
| 内容微调 | 钩子更狠、节奏更快 | 可加"怎么做的"技术钩子 | 真实感、家人口吻 |

**统一动作**:① 三平台都用同一母版 MP4;② 各自做 1 张竖屏封面(可用 Remotion 抽帧或单独 Composition);③ 标题/标签按上表换;④ 评论区自己先发一条"我是怎么用 AI 把它做难的"引导讨论(**禁"扣1领资料"导流话术**,见 [[小红书导流话术合规红线_扣1领资料_v1]],三平台同理会限流)。

**首发顺序建议**:快手/抖音先发(受众=反诈高危 + 传播快),B站做"技术 + 公益"长尾沉淀和合集。

---

## 五、《反诈柜台》首批落地执行(具体可做)

1. **选题**:从 314 案件挑 **10 条最反直觉的**做首批——优先"障眼真消息"(真盗刷预警/真验证码)与"隐形诈骗"(安全账户/一字差域名),因为反转最强、最适合做 hook。每条一支视频。
2. **搭母版**:独立工程在 `fraud-desk-demo/_video/`(与游戏同仓),竖屏 `FraudDeskShort` Composition + 三层结构;可参考官方 TikTok 模板做逐词字幕升级。
3. **跑通 1 条 pilot**:先把 1 条案件从"文稿→Eleven→Whisper→Playwright 录屏→母版渲染"全链路跑通,**人审到满意**(这是蒙眼剪辑法的关键判断点)。
4. **母版审核清单**(人必须看的):
   - 前 3 秒钩子能不能在静音下看懂?
   - 逐词字幕是否=实际口播?有无技术名词被 TTS 误读?
   - 字幕/关键动作有没有越出竖屏安全带?
   - 反转点(payoff)是否在 18s 前给出?
   - BGM 是否取段而非整首铺底、音量是否压在旁白之下?
5. **母版过审 → 批量**:把 10 条(再 314 条)交给 `renderMedia` 循环出片,抽检 3–5 条。
6. **发布**:按第四节 playbook 三平台分发。

---

## 六、复用 checklist

```text
[ ] 1. 数据 → 文稿:每个条目生成 3-4 句(钩子 + 判读 + 反转 + CTA)
[ ] 2. 配音先行:Eleven/Fish 中文 TTS → 读真实 duration
[ ] 3. 逐词字幕:Whisper 转写实际音频(token 级)→ captions.json
[ ] 4. 素材:Playwright 竖屏录屏 → ffmpeg 转 mp4 → OffthreadVideo
[ ] 5. 母版:9:16 Composition + calculateMetadata 按音频反推 + 三层结构
[ ] 6. 人审母版(用第五节审核清单,审狠——它会被复制 N 倍)
[ ] 7. 批量:bundle 一次 + dataset-render 串行循环
[ ] 8. 分发:同母版 + 各平台换封面/标题/标签(第四节表)
```

---

## 七、风险与合规

- **反诈题材边界**:演示诈骗话术要点到为止,**不把完整可复制的诈骗操作流程演全**(平台对"教骗术"敏感);落点始终是"如何识别/防范"。强调公益、未用真实人名品牌(沿用游戏 footer 口径)。
- **导流合规**:三平台均禁"扣1/私信领源码"式导流,易判广告限流。用评论区自然分享代替。见 [[小红书导流话术合规红线_扣1领资料_v1]]。
- **批量同质化限流**:母版若千篇一律,平台会判搬运/批量号限流。对策:母版预留足够变量位(不同案件文本/录屏/钩子/封面),且**不要 314 条一天发完**,按节奏放。
- **音乐版权**:BGM 用 Suno 自生成取段(见 [[Suno配乐制作分享]]),不用平台外热门曲。
- **水印**:小站水印放安全区内、不挡字幕;抖音简介不放外链以免限流。

---

## 关联文档

- [[蒙眼剪辑法_方法论笔记]](v4 是其批量化延伸)
- [[2026-06-09_Remotion全片音频字幕BGM复盘]] / [[2026-06-08_Remotion_MJ_Seedance混合动画闭环复盘]] / [[Remotion正式小片段实验工作流防偏移]]
- [[图片占位到视频替换的工作流_v1]] / [[Suno配乐制作分享]] / [[方法论笔记_Suno两阶段工作流_v1]]
- [[小红书导流话术合规红线_扣1领资料_v1]](同项目发布合规)

---

*v1 (2026-06-26):反诈柜台短视频分发触发,整合蒙眼剪辑法母本 + 国际 Remotion 短视频自动化管线(官方 TikTok 模板 / Whisper 逐词字幕 / OffthreadVideo 录屏 / dataset-render 批量 / OpusClip 留存数据)。落地路径已给,待 pilot 验证后回填实测数据。*
