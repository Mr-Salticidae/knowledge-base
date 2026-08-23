---
tags: [类型/档案]
---
# MiniMax H3 (Ref2VA) 行为规律

> 来源：项目 61《雨里旧信》MV 2026-08-23~24 本地部署实跑
> 环境：AutoDL RTX 5090 32GB · ComfyUI 0.33.0 · 开源权重 62.7GB（nvfp4 文本编码器）
> 适用：MiniMax H3 开源权重的 ComfyUI 路线（非 API）
> 注意：本档只写**实测**结论，每条都注明是怎么测出来的

---

## 一、开源权重路线值不值得走

值得，前提是你被会员门槛挡住了。项目 61 依次撞了三道墙：

| 路线 | 门槛 | 结果 |
|---|---|---|
| 即梦 Dreamina CLI | 需「高级」会员 | ❌ 充值不解决，是权限不是积分 |
| ElevenLabs Flows API | 需 Pro 套餐 | ❌ |
| 火山方舟 API | 充值 200 元 | ⚠️ 门槛可接受，但**不收含真人人脸的参考图** |
| **AutoDL 按小时租卡 + H3 开源权重** | **按小时付费** | ✅ |

三条 API 路线的共同问题是**能力握在别人手里，权限说变就变**。
开源权重 + 租卡的唯一变量是钱和时间，没有资格审查。

---

## 二、硬件：架构断崖，不是显存断崖

**24GB 的 Ada（4090）跑不动，32GB 的 Blackwell（5090）跑得动，差的不是那 8GB。**

H3 的文本编码器是 Qwen3-VL-32B。Blackwell 原生支持 nvfp4，编码器只要 14.6GB；
非 Blackwell 只能用 int8，同一个编码器要 25.3GB——**文本编码阶段就 OOM**。

| GPU | 量化 | 编码器 | 权重总量 | 结论 |
|---|---|---|---|---|
| RTX 5090 32GB | nvfp4 | 14.6GB | 62.7GB | ✅ 峰值 24.4GB，余 7.6GB |
| vGPU-48GB / PRO 6000 | int8 | 25.3GB | 73.4GB | ✅ 需 ≥40GB 显存 |
| RTX 4090 / 3090 24GB | int8 | 25.3GB | 73.4GB | ❌ 吃不到 nvfp4 |

所以选卡时**先看架构再看显存**。5090 还比 48GB 的 vGPU 便宜（¥2.78 vs ¥2.88/时）。

---

## 三、耗时：跟参考图张数强相关，这是排产的关键

官方对 `ref_image_size` 的说明里有一句：`'max'` … *"Reference tokens ride through
every sampling step, so 'max' can be several times slower."*
参考图 token 要跟着**每一步采样**走，所以耗时随参考图张数明显上升。

1344×768 · steps=20 · 不挂 turbo LoRA · `ref_image_size=max` 实测：

| 参考图张数 | 实测 | s/帧 |
|---|---|---|
| 1 张 | 124 帧 / 440s | **3.55** |
| 2 张 | 243 帧 / 1406s | **5.79** |
| 3 张 | 192 帧 / 1301s | **6.78** |
| 1 张 + `ref_image_size=match` | 124 帧 / 330s | **2.66** |

**排产必须按张数分桶估，不能用单一 s/帧。**
项目 61 一开始拿 3 张那镜的 6.78 去乘全片，把预算估成 ¥35.6；
按桶重算实际是 ¥25.7，差了 38%。

`match` 比 `max` 快约 25%（不是官方说的「several times」）。但注意：
**改 `ref_image_size` 会改变条件，出的是完全不同的构图，不只是画质差异**，
所以它不能当画质 A/B 用，也不适合在一批里混用。

---

## 四、帧数必须落在 17k+5 网格上

节点签名写死：`length` 的 `min=5, max=3600, step=17`。
合法帧数是 `17k+5`：22 / 39 / … / 124 / 141 / 158 / 175 / 192 / 209 / 226 / 243 …
（124 帧 ≈ 5s，官方标注训练区间约 124–362 帧。）

按秒排的分镜要先吸附到网格再算总时长：

```python
def snap_frames(seconds, fps=24):
    k = max(1, math.ceil((seconds * fps - 5) / 17))
    return 17 * k + 5
```

---

## 五、ComfyUI API 格式：两个会静默失败的坑

### 1. 嵌套 DynamicCombo 的键名是**点号链**

`SaveVideo` 的编码参数是层层嵌套的动态组合：

```
format = "mp4"  →  露出 codec  →  "h264"  →  露出 encoding  →  "re-encode"  →  露出 crf
```

API 格式里必须写成点号链，和 `ref_images.ref_image_0` 是同一套规则
（ComfyUI 的 `finalize_prefix()` 把前缀链用 `.` 连起来）：

```python
"inputs": {
    "video": ["15", 0],
    "filename_prefix": prefix,
    "format": "mp4",
    "format.codec": "h264",
    "format.codec.encoding": "re-encode",
    "format.codec.encoding.crf": 12.0,        # h264 范围 0-51
}
```

⚠️ **写成扁平的 `"codec"` / `"encoding"` / `"crf"` 不会报错，会被静默忽略**，
然后 codec 退回默认 `auto`（直通不重编码）。实测码率 **1.0 Mbps**，
雨这种高频细节直接压成糊块。改对之后同一镜 **6.9 Mbps**，S34 达 11.9 Mbps。

**所以「提交成功」不等于「参数生效」。** 凡是加了质量相关的参数，
先用极短探针（`--length 39 --steps 4 --turbo`，约 45 秒）验一次实际码率再开长跑。

### 2. 参考图是 Autogrow，序号即语义

`ref_images` 是 `io.Autogrow.Input`，前缀 `ref_image_`，`min=0, max=9`。
API 键为 `ref_images.ref_image_0`、`ref_images.ref_image_1`…

节点 docstring 明确：参考按 **图 → 视频 → 音频** 的固定顺序进入，
每类各自 1-based 编号，prompt 里用 `<Picture i>` / `<Video k>` / `<Audio j>` 引用。
**挂载顺序错了，模型会把「窗外景象」当成「角色身份」用。**

另有 `ref_videos`（Autogrow，max=3，收的是**图像帧序列**不是视频文件，24fps 下 2–15s）。

### 3. 缓存会救你

改了 `SaveVideo` 参数重跑同一镜，采样结果命中缓存，**1301s 的镜头只花 20s**
就重新出片。所以「参数写错了要重跑」的代价往往只有重编码，不是重采样。

---

## 六、Prompt：模型跟得住「像什么」，跟不住「怎么拍、发生什么」

这是项目 61 最大的一条。40 镜里前三个验证镜的表现高度一致：

> **调性、材质、年代、色彩——全对。**
> **构图、机位、动作——全错。**

### 1. 否定句几乎无效，越禁越突出

S17 要求「她手拿折着的信，但全程不看信」。原文 116 词，几乎全是否定：
`never lowers her head` / `never looks down at the letter` /
`does not read, unfold, lift or examine`，而 `letter` 出现 **5 次**。

**连改四版都失败**，每版她都在低头读信。反复提及反而把信推成了画面重点。

**有效解法不是把禁令写得更狠，是把冲突源头拿掉**——
第五版直接把镜头收到锁骨以上、手在画框之外，prompt 里一次都不提信。一次通过。

> 前一镜已是折信特写，靠剪辑说话就够了。
> **画面里不该出现的东西，连提都不要提。**

### 2. 把意图写成**可见的物理结果**

S34 要求「伞明显向女主一侧倾斜」（表达他在照顾她）。直接这么写，两版都没执行。

改成写这件事的**后果**：

> 她的头肩完全在伞下保持干燥，而他外侧的肩袖露在伞沿之外被淋透，
> 浅蓝布料那一块变成深色。

一次就对了，而且比原意图更好读——观众一眼看到湿透的肩膀。

**规律：模型渲染的是「看得见的东西」。抽象意图要翻译成可见的物理事实。**

### 3. 品类词会把模型带向错误的先验

S34 写 `a black oiled-paper umbrella`（黑色油纸伞）→ 出的是**灰白条纹纸伞**。
「油纸伞」把它带向了传统花纸伞的先验。

同一批里 S35 只写 `the same black umbrella` → **正确的纯黑伞**。

**解法：不写品类，写外观。** 改为
`a large plain black umbrella, its canopy a single flat matte black all over with no
stripes, no panels of any other colour, no pattern and no printing anywhere on it`。

### 4. 太短的 cam 等于没写

S30 的 `cam` 原本只有 `Medium shot, frontal, completely locked off with no movement`。
模型没有可抓的构图信息，**自己编了一条走廊**，门被推到侧面且很小。

改为写具体构图：门面与画框平行、门居中且占满画高、两侧只留窄边灰泥墙、
显式排除走廊/房间/窗/家具——门就出来了。

**描述详略要和你在意的程度成正比。你写得越短，模型自由度越大。**

### 5. ⚠️ 排除项写多了会削掉画面的成立条件

承上：为了赶走走廊，写了 `no corridor / no room / no window / no furniture`。
结果那一版**整个画面几乎全黑**——因为风格模板要求「恰好一处暖光源」，
而排除项把所有可能充当光源的东西都删干净了。

补回一束**画外**的低角度侧光（光源本身留在画框外，否则它又会画一扇窗），
并写明「门是画面里最亮的东西，从不处于黑暗中」，才恢复正常。

**删掉一个元素之前，先想清楚它在画面里还承担了什么功能。**

### 6. 跨镜必须一致的东西，只能写一处

S34/S35 是同机位冷暖对照，必须是同一把伞。两镜各写一遍描述，**必然漂**。
项目 61 的做法是在 shots.json 里加 `_shared` 段，镜头文本用 `{UMBRELLA}` 引用，
装配时替换并校验键存在——和「资产映射只写一份真源」同一个思路。

---

## 七、模板拼装类代码要对**生成结果**做自检

项目 61 在同一类 bug 上栽了两次，都是分支覆盖测不出来的：

1. `mem_char` 模式下 prompt 写「参考图中的这位女性」，而分镜写「画面里没有女性」
2. `has_ref = mode.endswith("_char")`——这是「有没有**角色**」，
   却被拿去控制「有没有**参考图**」的措辞。结果挂了场景资产但没人物的镜头，
   一边描述 `<Picture 1>` 是那扇门，一边连说两遍 `no reference assets`。
   **模型于是不把资产当权威、自己另编构图**（就是上面 S30 那条走廊的真正根因），
   影响 16 镜、占全片 40%。

**代码分支都覆盖了，语义却是矛盾的。** 修完加了一段全片自检：

```python
for x in shots:
    n = len(x.get("refs") or [])
    if n and "no reference assets" in x["prompt"]:  ...
    if not n and "<Picture 1>" in x["prompt"]:      ...
```

---

## 八、租卡运维

- **换区 = 数据全丢。** AutoDL 数据盘绑可用区不绑账号。项目 61 因余额耗尽自动关机、
  原区无资源只能换区，62.7GB 权重和已生成的成片全部作废，重下 110 分钟。
- **纪律：出一镜拉一镜**，别等全量跑完再导出。
- **国内机房到 GitHub 基本不可用**（实测直连 21 KB/s）。走 `gh-proxy.com` 镜像
  取 tarball（3827 KB/s）。**AutoDL 的 `/etc/network_turbo`「学术加速」实测 0 KB/s**，
  它会打印「设置成功」但把连接彻底掐死，开了比不开还慢。
- **pip 源要选同步快的不是选近的。** 清华源缺 ComfyUI master 要求的
  `comfyui-workflow-templates==0.11.44`，而 `pip install -r` 是先解析全部再安装，
  **一个包解析不到，整个 requirements 一个都装不上**。用阿里云（376 KB/s，版本齐全）。
- **Windows 的 OpenSSH 不支持 ControlMaster**（没有 unix socket）。防止刷连接数的办法是
  **把轮询循环写在远端**，一条 ssh 连接跑到底；绝不要本地 `for ...; do ssh ...; sleep 6; done`。
- **`pkill -f` 会匹配到自己的命令行**（远端 `bash -c` 的 cmdline 里就含那个串），
  表现为 ssh 退出码 255。pattern 要加方括号：`pkill -f "git-remote-htt[p]"`。

---

## 关联文档

- [[Seedance2_5_行为规律_v1]] —— 商业 API 路线的对应档案，prompt 规范与本文完全不通用
- [[可灵Kling3_0_行为规律]] —— 另一条视频模型路线的实测档案
- [[Eleven_v3_行为规律_v1]] —— ElevenLabs 平台行为
