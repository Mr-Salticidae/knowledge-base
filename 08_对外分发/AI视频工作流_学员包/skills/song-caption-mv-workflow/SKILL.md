---
name: song-caption-mv-workflow
description: AI 歌曲 MV 与字幕自动化工作流。用于 Suno/AI 音乐作品的 MV 制作、无字版导出、歌曲字幕识别、哼唱过滤、Demucs 人声分离、WhisperX 词级对齐、中英双语 SRT 生成和剪映后期交付。当用户说“给这首歌做 MV”“歌词卡点不准”“导出无文字版”“生成 SRT”“歌曲字幕识别”“哼唱太多识别不准”“用 Demucs/WhisperX 跑字幕”时触发。
---

# Song Caption MV Workflow

## 角色定位

你是 AI 音乐 MV 制作与字幕自动化协作 agent。目标不是替代创作者审美，而是把以下重复环节做成可验证流程：

- 音乐作品归档
- 抽象/具象 MV 画面组织
- 无文字 MP4 导出
- 歌曲字幕识别与清洗
- Demucs 人声分离
- WhisperX 词级对齐
- 中英双语 SRT 交付
- 剪映/Premiere 手调前的预处理

核心原则：**视频画面和字幕解耦，字幕卡点用工具给锚点，最终由人耳校对。**

---

## 适用场景

使用本 Skill 当用户需要：

- 把 Suno / AI 音乐做成 MV
- 歌曲里有 humming、beatbox、多语言 hook、含混唱腔
- 旧字幕卡点严重不准
- 需要导出无文字版 MP4，后续在剪映手调字幕
- 需要英文 SRT、中文意译 SRT、双语字幕
- 想验证 Demucs + WhisperX 是否比 Whisper 更准

不适用：

- 普通说话/播客字幕：直接 WhisperX 或普通转写即可
- 纯人工剪辑审美判断：本 Skill 只负责生成可审核素材和时间锚点
- 要求 100% 自动准确歌词：AI 歌曲尤其多语言和哼唱仍需要人工校对

---

## 最小输入

必须收集：

```text
[ ] 音频路径
[ ] 目标视频比例（默认 16:9）
[ ] 图片/视频素材目录
[ ] 是否需要无字版 MP4
[ ] 是否已有人工调整过的歌词 SRT
[ ] 是否需要中文意译 SRT
```

可选：

```text
[ ] 目标歌词文本
[ ] 片尾字幕
[ ] 字体偏好
[ ] 是否使用 GPU
[ ] 是否需要 Demucs 人声分离
```

---

## 工作流

### 1. 归档与素材确认

在项目目录下建立清晰结构：

```text
01_音频/
02_视频/
04_素材_出图/
07_输出/
08_发布/
```

确认音频、歌词、图片是否存在。不要在素材不完整时直接渲染 final。

### 2. MV 画面版本

推荐先做三版：

1. `preview_540p.mp4`：粗看节奏
2. `no_text_1080p.mp4`：无字母版，给剪映/Premiere 加字幕
3. `final_1080p.mp4`：如果字幕和片尾已确定，再烘焙文字

歌曲类 MV 默认不要把歌词早早烘焙进视频。先把画面和字幕解耦。

### 3. 电影感基础处理

如果用户要求电影质感，可加：

- 上下黑边（letterbox）
- 轻微 Ken Burns
- 微抖动 / 呼吸式缩放
- 暗角
- 胶片颗粒
- 冷调或统一色彩 tint

中文黑幕字幕优先使用稳定宋体/思源宋体/Noto Serif SC。若本机无字体，明确告知用户下载，不要假装用了。

### 4. 字幕识别路线选择

按复杂度选择：

#### 路线 A：已有人工 SRT

优先级最高。保留用户时间码，只做：

- 翻译
- 排序修复
- 编码修复
- 多语言标注

不要重新识别覆盖人工时间轴。

#### 路线 B：清晰演唱 / 普通歌曲

直接跑 WhisperX：

```powershell
whisperx audio.wav --model large-v3-turbo --device cuda --compute_type float16 --language en --output_format all
```

CPU 可用 `--device cpu --compute_type int8`，但速度慢。

#### 路线 C：哼唱 / beatbox / 多语言 hook / 伴奏干扰

先 Demucs 分离人声：

```powershell
python -m demucs --two-stems vocals -n htdemucs -d cuda -o output_dir audio.wav
```

再跑 WhisperX：

```powershell
whisperx vocals.wav --model large-v3-turbo --device cuda --compute_type float16 --language en --vad_method silero --output_format all
```

然后从 `vocals.json` 的 `word_segments` 生成短语级 SRT。

### 5. 哼唱过滤规则

删除或不显示：

- `Hum`
- `Hmm`
- `Mmm`
- `Ah`
- `Oh`
- `[humming ...]`
- 只有拟声、没有语义的长段

保留：

- `Stay alive`
- `one small light`
- `still breathing`
- `we're still here`
- 多语言 “活下去” hook

### 6. 短语级 SRT 重组

不要直接使用 WhisperX 默认长句 SRT。优先读取 JSON 里的 `word_segments`，按短语组合：

```text
Stay alive, vive, ikite, sarajwo
Reste en vie, hayatta kal, zinda raho
we're still here
one small light
still breathing
```

每条字幕建议 1-5 秒。过短会闪，过长会压住画面节奏。

### 7. 中文意译 SRT

如果已有用户手调英文 SRT：

1. 保留原时间码
2. 只替换文本
3. 按时间排序
4. 多语言 hook 标注语言
5. 以艺术性优先，不逐字硬译

示例：

```text
one small light
→ 一粒微光

Stay alive, vive, ikite, sarajwo
→ 活下去。英语 / 西语 / 日语 / 韩语

Reste en vie, hayatta kal, zinda raho
→ 活下去。法语 / 土耳其语 / 印地语、乌尔都语
```

---

## 验收清单

视频：

```text
[ ] 时长正确
[ ] 分辨率正确
[ ] 音频未截断
[ ] 片尾黑幕时间足够
[ ] 字幕没有被提前烘焙到无字版里
[ ] 黑边、抖动、颗粒不过度
```

字幕：

```text
[ ] SRT 编号连续
[ ] 时间码升序
[ ] 无重叠或明显倒序
[ ] 哼唱段已删除或有意保留
[ ] 多语言 hook 已标注语言
[ ] 中文翻译以意译为主
```

技术：

```text
[ ] `torch.cuda.is_available()` 为 True（如使用 GPU）
[ ] Demucs 输出 `vocals.wav`
[ ] WhisperX 输出 `json/srt/vtt/txt`
[ ] 从 `word_segments` 重组过短语级 SRT
```

---

## 已验证案例

详见 [[2026-06-07_Stay_alive_AI音乐公益MV复盘]] 与 [references/stay-alive-case-notes.md](references/stay-alive-case-notes.md)。
