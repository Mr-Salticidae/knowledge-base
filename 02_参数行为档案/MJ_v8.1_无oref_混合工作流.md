---
tags: [类型/档案]
---
# MJ v8.1 无 oref/cref · 混合工作流

> 入档：2026-05-12（D2 晚间）
> 触发：「拾色」女主形象试跑时，需要在 v8.1 美学和角色一致性之间做 trade-off
> 关联：[[角色一致性金字塔]] / [[MJ_v8.2_行为档案_v1]]（v8.2 已实测 --preview 通道，质感再上一档，oref 支持情况未测）

---

## 一句话

**v8.1 美学优于 v7，但 v8.1 没有 cref/oref 功能。** 解法不是二选一，是**按镜头需要分工**：

- 必须锁脸的镜头 → v7 + oref
- 无人物 / 局部 / 远景 → v8.1 美学最大化

---

## 如何使用

写一支多镜头作品（MV / 海报组 / 系列封面）前，**先把所有镜头按"是否需要清晰看到她的脸"分成 A/B/C 三类**：

| 类别 | 定义 | 工具 |
|---|---|---|
| **A · 必须锁脸** | 脸是主体（特写 / 半身正面 / 看表情） | **v7 + oref --ow 100** |
| **B · 半锁脸** | 半身侧背 / 远景轮廓 | **v7 + oref --ow 50-70** |
| **C · 无需锁脸** | 道具 / 局部 / 场景 / 远景 / 手部 / 黑场 | **v8.1**（美学最大化 + 无 reference）|

**典型分布**：16 镜作品里 A 类约 25% / B 类约 25% / C 类约 50%。

C 类占一半 → **整片综合美学接近 v8.1 全片**，只有"她的脸"的镜头损失 v7 的美学差。

---

## v7 vs v8.1 实测对比（拾色 D2）

### v8.1 出图特点

- ✅ 真实质感更强（皮肤 / 织物 / 光影）
- ✅ photographic realism 关键词响应更准
- ✅ Hasselblad / Kodak Portra 等胶片关键词改变质感
- ✅ 长 prompt 解读更精准
- ❌ **没有 cref / oref / character reference 功能**
- ❌ 每次 seed 不同，脸会漂移

### v8.1 inset frame 双层结构稳定执行（2026-05-14 实测）

**发现来源**：异界气象台 minitest 第一节·深海第七断层 prompt 测试（A-v3 组）

prompt 写入：
```
... ultra wide top-down satellite view of an unknown ocean region as the main image, a smaller inset square frame in the upper right corner showing a cross-section diagram of an underwater trench ...
```

**结果**：MJ V8.1 在 4 张抽卡中**全部稳定召出**"主图 + 右上角子图"的标准排版——主图是俯瞰场景，子图小窗口里是 cross-section / radar scan / topographic 等技术示意图。

**关键能力**：
- "inset frame" / "inset square frame in the upper right corner" 指令稳定执行
- 子图内容可由 prompt 后续描述指定（cross-section / radar / topographic / scope view 等）
- 子图与主图视觉风格保持一致（同色温、同质感），不会出现"现代 UI 子图"违和

**应用场景**：
- 央视气象图主图 + 雷达扫描子图（异界气象台 minitest 实测）
- 监控录像 + 监控目标特写子图
- 仪表盘 + 单一仪表读数子图
- 任何"档案/纪录片/报告"语境的复合信息呈现

**注意事项**：
- 子图位置（upper right / upper left / lower right ...）按 prompt 指令稳定执行
- "smaller inset square frame" 比 "small picture-in-picture" 更精准——前者 MJ 理解为"嵌入边框小窗口"，后者可能被理解为"另一张完整画面叠加"

---

### v8.1 inset frame 子图内容偏离 prompt 的常见模式（2026-05-14 实测追加）

第一节验证过双层叠加（inset frame）100% 稳定召出，但**子图具体内容**的执行有偏差：

| prompt 写 | 实际跑出 |
|---|---|
| `cross-section diagram of an underwater trench` | ✅ 较准确（剖面图） |
| `radar scan view with grid scale` | ✅ 准确（带刻度的雷达扫描） |
| `thermal radar visualization with cold color heat map` | ⚠️ 偏离 —— 出"温度热点 / 异常事件型景观"，不是"等温线图" |
| `geological topographic chart` | （未测试） |

**规律推测**：MJ 训练数据里 "radar" / "cross-section" 等"二维可视化技术"图示丰富，但 "thermal heat map" 这类"色彩映射数据可视化"训练样本较少，倾向用"光点 / 红色热区"代替等温线。

**应对**：想要"等温线图"风格，prompt 写得更直接：`topographic isotherm contour map with concentric temperature rings` 而非 `thermal heat map`。

但子图偏离不一定是坏事——异界气象台第三节 A-v2_u0 跑出的"红色温度热点"反而和字幕"-89℃ 温度回升"互锁，是 happy accident。

---

### v8.1 材质属性形容词弱权重（2026-05-14 实测）

prompt 写：
```
snowflakes have a faint metallic sheen catching the dim ambient light
```

期望：雪花有金属光泽（暗示"金属味的雪"诗意）。

实际：4 张抽卡**全部跑出普通雾雪**，没有任何金属感。

**规律**：MJ V8.1 对"具体材质属性形容词"（metallic sheen / glossy / wet / translucent / iridescent 作为形容词修饰名词时）执行不稳定——它把这些当弱权重 modifier 处理，优先级低于主体形态描述。

**应对**：把材质属性**做成视觉元素本身**：

| ❌ 弱（形容词模式） | ✅ 强（视觉元素模式） |
|---|---|
| `snowflakes with metallic sheen` | `tiny metallic silver shards mixed with snow particles` |
| `glossy black armor` | `pitch black armor reflecting bright highlights` |
| `wet skin` | `skin with visible water droplets on the surface` |
| `iridescent feathers` | `feathers with rainbow color gradient like oil on water` |

---

### v8.1 数量约束 "single / one" 执行不稳定（2026-05-14 实测）

prompt 写：
```
a single tall thin mechanical figure silhouette barely visible
```

实际：4 张抽卡里有 **2 张跑出了 2-3 个剪影**，"single" 数量约束执行率约 50%。

**规律**：MJ 对"数量词"的执行受 prompt 整体语境干扰。如果 prompt 后续描述了"scattered" / "in the distance" 等空间分布词，"single" 会被忽略。

**应对**：双重约束 + 强否定：
- 写 `a single ... and no other figures anywhere in the entire frame`
- 或者 `exactly one ... only one, nothing else moving in the frame`

**注意**：本节恰好需要"几个剪影"而非"一个"（brief 要求"几个机械生命体的剪影"），所以这次的"数量约束失败"反而符合 brief。**是否需要严格 single 看具体需求**。

---

### v8.1 "closing transmission/shot" 自动召出 letterbox + 双频道结构（2026-05-14 实测）

**发现来源**：异界气象台 minitest 收尾·总览图 v2/v3 测试

**问题**：v3 prompt **没写** letterbox，但 4 张全部跑出了 letterbox + 双弧线结构；v2 prompt 写了 `prominent black letterbox bars`，但跑出的 4 张里 3 张是**双 letterbox 双弧线**而非期望的"单 letterbox 单弧线"。

**规律**：MJ V8.1 把 `closing transmission` / `closing shot` 关联到了**"电视信号即将关机的双频道残影 / 录像带切换瞬间"**——这是训练数据里电视档案影像的典型视觉特征。

**应用调整**：
- 想要 closing 镜头的"单频道"视觉，要在 prompt 里**显式排除**：`single continuous frame, no signal interruption, no double horizontal split`
- 想要"双频道分裂感"反而是 happy accident——直接写 `closing transmission` 就能稳定召出

---

### v8.1 双重约束尺寸技巧：稳定锁标记点大小（2026-05-14 实测）

**发现来源**：异界气象台 minitest 收尾·总览图 12 张抽卡

**正例**：prompt 写
```
three small bright white circular markers ... about 2 percent of the frame width each
```
**12 张全部稳定召出清晰、大小合适的白色圆点**——MJ 把"形容词（small bright）+ 量化（about 2%）"作为强双重约束执行。

**模板**：
- `[形容词描述] [object], about X percent of the frame [width/height] each`
- 比单独写 "small markers" 或 "tiny dots" 稳定得多

**对比反例**：第三节 prompt 写 `tiny dark dots barely visible`——只用形容词，MJ 把"废墟"画得比 prompt 要求更显眼。

**回流到"材质属性形容词弱权重"小节作为对比正例**：单形容词权重弱，但**形容词 + 量化数值**权重强。

---

### v8.1 雷达扫描召唤静态而非动态（2026-05-14 实测）

**发现来源**：异界气象台 minitest 收尾·总览图 v3 测试

**问题**：prompt 写 `a sweeping radar scan line ... sweeping clockwise`，期望是"动态扫描线"。实际 4 张跑出**静态雷达光带 + 同心圆脉冲**——没有"运动"概念。

**规律**：MJ 是图像生成模型，**所有"运动 / 扫描 / 旋转"等动态词都被翻译成静态呈现**。

**应用调整**：
- 不在 prompt 里期望"动态"
- "扫描动作"由后期 MoviePy/AE 实现——MJ 出"扫描线已经定格的某一帧"作为基底
- prompt 写 `radar scan line frozen at moment of sweeping` 比 `sweeping radar scan line` 更准确（前者承认是静态帧）

---

### v8.1 sref 跨色温场景强度阈值（2026-05-14 实测）

**发现来源**：异界气象台 minitest 第一节·B-v1 镜头测试

**问题**：使用 sref 基准图（navy 色调）+ prompt 写 "deep saturated purple"，期望出紫色场景。

| sw 值 | 实际输出 | 评价 |
|---|---|---|
| 100 | 完全 navy，紫色被吃掉 | ❌ |
| 60 | teal 青绿（navy 和紫色折中产物） | ❌ 仍不达标 |
| **40-50（推测）** | 应能出现 deep purple 主导 | 待验证 |

**结论**：sref 跨色温压制能力很强。当目标色温和 sref 色温**显著不同**时（如 navy → purple、navy → magenta、teal → red），**sw 必须降到 40-50**，否则 prompt 的色温描述会被洗掉。

**判断阈值**：
- 同色温微调（如 navy → 深 navy）：sw 100
- 邻色温（如 navy → cyan）：sw 70-80
- 跨色温（如 navy → purple/red/green）：sw 40-50
- 想完全脱离 sref 色温：不挂 sref，纯 prompt

---

### v8.1 sref 工作流变化（2026-05-14 实测）

**Web 端 v8.1 的 sref 已从"数字 ID"改为"图片挂载"**：

- ❌ 旧（v7 时代）：prompt 末尾写 `--sref 5692463053 --sw 100`，数字 ID 可跨会话/项目复用
- ✅ 新（v8.1 web 端）：点击 prompt 输入框旁的"加图"按钮上传/挂载参考图，UI 显示为图片缩略图挂载状态
- ✅ `--sw 100` 等强度属性照常生效（写在 prompt 文本里）
- ⚠️ 无法直接获取 sref 数字 ID（UI 隐藏了 ID 字段）

**对知识库的影响**：

- 旧 sref 档案命名约定 `sref_<数字ID>_<描述>.md` 不再适用于 v8.1 web 端工作流
- 新约定：`sref_<项目>_<图片名>.md`，文件内挂图片路径（相对/绝对都可），而非 ID
- 旧档案（如 `sref_5692463053_navy现代极简.md`）仍适用于 v7 + oref 或 discord 端工作流

**对项目工作流的影响**：

- sref 母本图片必须**保留为本地图片** + **路径稳定**（移动/删除原图 = sref 失效，每次都要重新挂）
- 跨项目复用 sref → 把图片复制到新项目目录，在新项目里重新挂载
- 用 MJ Web 端做风格统一项目时，**先固定 sref 母本图片的存储位置再开始批量出图**——避免中途搬家

### v7 + oref 出图特点

- ✅ oref 锁脸一致性 ≈ 85%（跑 8 张里 7 张能保住主气质）
- ✅ 美学比 v8.1 弱 10-15%（但仍可用）
- ⚠️ 部分图唇色偏深 / 神态偏锐利（v7 默认偏好）
- ⚠️ `--ow` 不是越高越好：100 锁得死但缺活气，50-70 留 moodboard 调味空间

---

## 风险预案（如果 v7 + oref 不达标）

```
Step 1：v7 + oref 跑 1-2 个 A 类镜头测试
   ↓
   评估"她"的气质保留度 vs 主基准图
   ↓
   ├─ ≥ 80% → 走 v7 + oref（主推）
   ├─ 60-80% → v7 + oref + 后期换脸补正
   └─ < 60% → 切换 libtv + nano-banana（节点工具）
       ↓
       nano 接管所有 A/B 类（角色一致性）
       v8.1 仍管 C 类（美学最大化）
```

**Cowork 推荐顺序**：
1. v7 + oref（首试）
2. libtv + nano-banana（备用）
3. v8.1 全跑 + FaceFusion / InsightFace 后期换脸（兜底）

---

## 「拾色」实战配置

| 镜号 | 内容 | 类别 | 工具 |
|---|---|---|---|
| S01 | 雨打邮局门外 | C | v8.1 |
| S02 | 邮局内景空镜 | C | v8.1 |
| S03 | 推门背影 | B | v7+oref ow50 |
| S04 | 取信特写 | A | v7+oref ow100 |
| S05 | 信封特写 | C | v8.1 |
| S06 | 看信表情 | A | v7+oref ow100 |
| S07 | 撑伞远景 | B | v7+oref ow70 |
| S08 | 室内换装暗示 | A | v7+oref ow100 |
| S09 | 抽屉题眼 | C | v8.1 |
| S10-S11 | 闪回手部 | C | v8.1 |
| S12 | 弄堂行走 | B | v7+oref ow60 |
| S13 | 邮局复入 | B | v7+oref ow70 |
| S14 | 邮局远景 | C | v8.1 |
| S15 | 直视镜头 | A | v7+oref ow100 |
| S16 | 黑场 | C | v8.1 |

**统计**：A 类 4 / B 类 4 / C 类 8。

---

## 「封面抽卡场景」的行为规律（异界气象台 minitest v2 实测沉淀）

> 入档时间：2026-05-14（运营经理 + Cowork 双方确认）
> 触发：异界气象台 minitest 封面 v2，32 张 MJ 实测（首轮 24 + 横屏补抽 8）
> 关联：[[入场票框架_v1.1迭代待办暂存]] 补丁 2/3/6/7

封面属于"无 cref/oref"的子场景，但有独有的行为规律，与 A/B/C 三类角色场景不完全重叠。

### 规律 1 · 五重反字幕约束（100% 有效率）

封面 prompt 必须包含：`no text, no labels, no logos, no subtitles, no banners`。

**理由**：MJ V8.1 在没有强压制时，会按"它理解的央视/纪录片画面"自带生成红条字幕条——对封面是污染。32 张实测 100% 无字幕，验证有效。

**适用范围**：任何"自带制式画面"的素材（央视格式、新闻联播、动物世界、气象预报、纪录片）都需要这条防御。

### 规律 2 · 主体尺寸召唤词「单一 > 群体」（封面专属）

| 召唤词 | 实测主体压倒感 |
|---|---|
| 单一主体（colossal / towering / monolithic）+ 形容词激进 | **4-5 分** |
| 群体（massive / countless / horde）| 2-3 分 |

**实测数据**：
- B-v1（`massive whales` 群体）→ 鲸群被画太小，主体感 2-3 分
- B-v2（`colossal whale` 单一）→ 主体压倒感 5 分
- A 系列（`towering tower` 单一）→ 4-5 分

**操作指南**：封面 prompt 优先用"单一主体 + 形容词激进"。如必须做群体，每个个体单独 prompt，避免依赖群体词。

### 规律 3 · sref 强度的「视频 - 封面」差分

| 场景 | 推荐 sw |
|---|---|
| 视频内画面（追求广角连贯感） | 80 |
| 封面（追求主体冲出框） | **40-50** |

**理由**：封面追求"主体压倒"而非"风格一致"。sw 50 同色家族验证一致性 4.7、主体压倒感 4.6——封面默认值。sw 40 适用于跨色家族。

### 规律 4 · 所有目标比例必须 MJ 原生抽卡（流程层）

**禁止**：从 9:16 抽卡通过 PIL 扩展 / 裁剪 / 翻转得到 16:9 / 4:3。

**实测对比**：
- PIL 画布扩展 16:9 左留白质量 = **1 分**（色块 + 噪点）
- MJ 原生重抽 16:9 左留白质量 = **5 分**（真实雾天 + 海面层次）

**操作指南**：每个目标比例（9:16 / 3:4 / 16:9 / 4:3）必须独立 MJ prompt，第一轮就抽出来。

### 规律 5 · sw 不是主体形态杠杆，prompt 文本才是

**反例**：异界气象台 C-v1 用 `monolithic mechanical lifeforms` + sw 40，4 张全部跑成"弯腰前行的人类剪影"。**降 sw 不能纠正歧义**。

**修复**：必须改 prompt 文本——`weathered ancient industrial machinery, no glow, no neon, no humanoid form` 类显式排除。

**操作指南**：当 MJ 跑出"概念歧义"时（如"机械生命"→"人形"），优先调 prompt 文本，而非调 sw。

---

## 关联文档

- 顶层方法论:[[角色一致性金字塔]](oref/seed/personalize/sref 4 层)
- 账号级地基:[[personalize与moodboard分工]]
- IP 应用案例:[[檐下IP 视觉系统]](V4 基准图修复案例)
- 对照参数:[[ow_行为规律]] · [[seed_行为规律]]
- 封面抽卡触发本节的源头：`20_异界气象台_minitest/02_视觉/封面_v2/sref调试日志_v2.md`
