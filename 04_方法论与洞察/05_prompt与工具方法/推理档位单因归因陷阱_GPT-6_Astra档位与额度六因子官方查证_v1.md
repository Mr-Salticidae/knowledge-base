---
tags: [类型/协作工具链, 主题/模型选型, 主题/查证与核查, 工具/Codex]
---
# 推理档位单因归因陷阱：GPT-6 Astra 档位与额度六因子官方查证 · v1

> 入档：2026-09-09
> 触发：跳蛛先生转来一篇热传的 GPT-6 Astra「推理等级怎么选」科普文（作者是 Pro 20x 用户，两个号额度烧光），直觉「他在错误归因」，要求从技术层评估并查证
> 验证状态：⚠️ **首次**（OpenAI 官方文档 + Tibo 原推 + Artificial Analysis 分档数据交叉核对；Ultra 实耗只有一例 GitHub issue，未自测）
> 性质：AI 编码工具的**成本机制档案** + **归因纠偏案例**（含我自己被官方数据纠正的三处）
> 对外版：`08_对外分发/GPT-6_Astra推理档位怎么选_额度为什么没了_同好版.md`（飞书云文档见文末）

---

## 一句话律

**推理档位是额度六因子之一，不是唯一因子。** 把「额度没了」单归到档位，会漏掉 Fast 2.5 倍和上下文体积这两个同量级项，并在 xhigh 与 max 的取舍上给出与实测数据相反的建议。

---

## 事实冻结（官方口径，2026-09-09 核）

### 推理档位（reasoning effort）

- API 支持 `low / medium / high / xhigh / max` 五档；GPT-6 Astra **不支持 `none`**（传了返 HTTP 400）。
- 官方推理指南原话：**the same model with different reasoning token budgets**；并说模型会 reason adaptively，简单任务少用、复杂任务多用。
- **推理 token 按输出 token 计费**，不可见但占上下文窗口。
- 会话中途可用 `configuration_update` 改档位，**仅限标准单代理模式**（即 Ultra 下不可改）。
- 官方对各档定位：low「高效推理、延迟略增」/ medium「质量与可靠性并重」（默认）/ high「困难推理、复杂调试、深度规划」/ xhigh「深度研究、异步工作流、需要很长 rollout 的 agent 任务，**只在 evals 证明有收益时用**」/ max「最复杂任务的最大推理」。

### Codex / ChatGPT 界面命名

| 界面档位 | API 值 | 官方说明 |
|---|---|---|
| Light（CLI 里叫 Low） | low | Fast responses with lighter reasoning |
| Medium（默认） | medium | Balances speed and reasoning depth for everyday tasks |
| High | high | Greater reasoning depth for complex problems |
| Extra High | xhigh | Extra high reasoning depth for complex problems |
| Max | max | more time to reason about a single task |
| Ultra | 非档位，是模式 | **Maximum reasoning with automatic task delegation** |

### Ultra

- 官方定义：**Ultra uses maximum reasoning and lets ChatGPT proactively delegate suitable work to subagents.** 即 max 推理 + 自动派发子代理。不是并行采样，是任务分解编排。
- 子代理**各自做自己的模型和工具调用**，因此 subagent workflows consume more tokens than comparable single-agent runs；未显式配置时子代理继承父代理设置。
- 官方适用场景：**读密集、可拆分**的任务（探索、测试、分诊、总结）；**写密集并行会冲突**，官方明确警告。
- Ultra 仅对 eligible accounts and supported models 开放。
- 实耗样本（GitHub openai/codex #43029）：Pro 20x 用户，Astra Ultra 跑一个 SwiftUI 加载指示器重构，1 小时 11 分，3 个子代理，**消耗周额度约 30%**。无官方回复。

### 额度怎么扣（learn.chatgpt.com/docs/pricing）

- 订阅侧按 **token 积分** 计：输入 / 缓存输入 / 输出三类。官方原话：**Your prompt, files, chat history, tool results, and ChatGPT's response all use tokens.**

| 模型 | 输入 | 缓存输入 | 输出（含推理） |
|---|---|---|---|
| GPT-6 Astra | 250 | 25 | 1250 |
| GPT-5.6 Sol | 100 | 10 | 500 |
| GPT-5.6 Terra | 50 | 5 | 300 |
| GPT-5.6 Luna | 5 | 0.5 | 30 |

（单位：积分 / 百万 token）

- 官方列出的消耗因子：**Model choice, context, reasoning, tool use, retrieval, and caching all affect usage, so prompt length alone isn't a reliable estimate.** 六个因子。
- **Fast 模式：Astra 按 Standard 的 2.5 倍计**（订阅侧）。API 侧另有 Priority processing 2 倍。
- Pro 是 Plus 的 **5 倍或 20 倍**（官方定价页原文 Pro 5x or 20x higher rate limits than Plus）。
- **ChatGPT Work 和 Codex 共用额度**；2026-08-24 Tibo 宣布 Plus 恢复 5 小时限额时，范围是「ChatGPT Work 和 Codex」，**普通聊天单独计量**。
- Plus 的 Astra 额度官方只给估计区间：每 5 小时约 5 到 45 条本地消息，按任务权重浮动；周上限未公布。
- Astra 在 Codex 订阅侧**免除 272K 长上下文加价**（二手报道引用企业版费率卡；API 侧保留 2 倍输入 / 1.5 倍输出）。

### Tibo 原推（2026-09-07）

> To calibrate you all on which reasoning effort to use for Astra, know that GPT-6 Astra on low performs better than GPT-5.6 Sol on high. If you were using high reasoning efforts with Sol and were happy, I suggest you move down to low or medium for Astra.

### Artificial Analysis 分档数据（GPT-6 Astra 发布页）

| 档位 | 智能指数 | 每任务成本 |
|---|---|---|
| low | 46 | $0.82 |
| medium | 50 | $1.54 |
| high | 51 | $1.72 |
| xhigh | 53 | $2.31 |
| max | 53 | $3.26 |

另一版本指数（paddo.dev 转引）：low 49 / medium 52 / high 53 / xhigh 54 / max 55，跑完指数的输出 token 分别为 5.4M / 12M / 19M / 30M / 49M。两版排序一致：**xhigh 到 max 分数持平或 +1，成本多四到六成，token 多六成。**

---

## 文章裁决表

| 文章说法 | 裁决 | 依据 |
|---|---|---|
| 档位＝同一模型不同思考预算，不是模型档位 | ✅ 对 | 官方原话 same model with different reasoning token budgets |
| Ultra＝「成立专项工作组」 | ✅ 对 | 官方定义 maximum reasoning + automatic task delegation |
| Plus 用户聊天走 ChatGPT 不走 Codex，额度分开 | ✅ 对 | 5h 限额范围＝Work + Codex，普通聊天单独计 |
| Pro 是 Plus 的 5 倍 / 20 倍 | ✅ 对 | 官方定价页 |
| 引 Tibo「Astra low 优于 Sol high」 | ✅ 对 | 原推核实 |
| 「最高出计划、降到高执行」 | ✅ 流程可行 | configuration_update 单代理模式下可中途改档，上下文延续 |
| **额度烧快＝推理档位太高** | ❌ **单因归因** | 官方六因子；作者自己的样本（测试 + 演示 + 全栈重构 + Fast）被工作量与倍率混淆 |
| **Fast 只是「拉满」的姿势** | ❌ **漏掉倍率项** | Fast 2.5 倍；基准任务上 medium→high 成本差仅约一成，Fast 一个开关顶三档 |
| **「极高没意义，直接最高」** | ❌ **与数据相反** | xhigh 53 vs max 53，成本 $2.31 vs $3.26；官方把 xhigh 定位给长 rollout agent 任务；「max 一轮解决更省」的前提（max 一轮成功率明显高于 xhigh）无数据支持 |
| Pro 用户「高」常驻 | 🟡 与官方建议相反 | Tibo 建议降到 low/medium；Codex 提示指南推荐 medium；作者自认心理因素 |
| Ultra「不是更聪明只是更贵」 | 🟡 半对 | Ultra 内含 max，至少和 max 一样聪明；Sol Ultra 在 Terminal-Bench 2.1 上 +3.1 个百分点（88.8→91.9）；**该不该用取决于任务可不可拆**，作者的顺序写密集 Vibe Coding 确实不适合，但理由错了 |
| Ultra 只在额度快重置时清仓用 | 🟡 浪费用法 | 官方适用场景是可拆分的读密集任务；清仓＝max × 子代理数 × Fast 2.5，是最贵组合 |
| 大号被风控是 OpenAI「莫名其妙」 | ❓ 未核实 | 两个 Pro 号同机高强度自动化是常见触发条件，但无证据 |

用 [[伪机制解释识别_四层拆解法_v1]] 的四层看：**现象✅（额度确实烧得快）/ 机制✅（同模型不同预算是官方口径）/ 根因❌（六因子讲成单因子）/ 药方🟡（档位匹配任务对，xhigh→max 反向）**。这是四层框架第三次复用，形态与前两次不同：前两次是「机制编数字」，这次机制层是对的，错在根因层的**遗漏**而非捏造。

---

## 我自己被纠正的三处（诚实记录）

上一轮凭经验给出的评估，有三处被官方文档推翻，一并留档，防止下次再犯：

1. **「推理档位只是二阶变量，上下文重发才是主因」→ 撤回。** 推理 token 按输出计费，Astra 输出费率是未缓存输入的 5 倍、缓存输入的 50 倍；max 的输出 token 约为 medium 的 4 倍。推理档位是**一阶**变量。正确表述：推理与上下文**同为一阶**，短会话推理主导，长会话上下文主导。
2. **「档位是训练出来的策略，不是同一段计算跑久一点」→ 撤回。** 官方口径就是 same model, different reasoning token budgets。文章的比喻是对的，我加的修饰是多余的。
3. **「Ultra 可能是并行采样，若是则更聪明」→ 撤回。** 官方定义是任务派发编排。文章的「工作组」比喻准确。

教训：**对成本机制的判断，先查费率表再下结论**。凭「agent 循环每回合重发上下文」这个正确的机制，推出「上下文主导」这个错误的量级，是因为没查输出与输入的费率比。机制对不等于量级对。

---

## 可复用：额度体检四问

额度掉得快，按顺序问：

1. **开 Fast 了吗？** 2.5 倍，先关。
2. **会话多长、上下文多大？** 每回合重发全部上下文，缓存也按 1/10 计；大日志、大 JSON 整段吐进对话是常见肥源。一个任务一个会话。
3. **档位高于任务需要吗？** 官方默认 medium；Astra low 已优于 Sol high。日常 medium，困难调试 high，长 rollout 的 agent 任务 xhigh，max 极少。
4. **Ultra 用在可拆分的读密集任务上了吗？** 探索、测试、分诊、总结可拆；顺序写代码不可拆，开了就是纯多付。

前两问是文章漏掉的，后两问文章讲了但第三问的档位排序要修正（xhigh 不是鸡肋，max 才是）。

---

## 举一反三：单因归因的识别信号

- **官方列了 N 个因子，文章只讲 1 个。** 先找官方的因子清单，再看文章覆盖率。
- **作者自身样本被工作量混淆。** 「我两个号烧光了」的工作内容是测试 + 演示 + 全栈重构，换任何档位都省不了多少。
- **「一轮解决更省」这类推论依赖未验证前提。** 前提是高档一轮成功率显著更高，数据显示 xhigh 与 max 持平。
- **比喻准确不等于建议正确。** 文章的两个比喻（思考预算、工作组）都对，建议层仍可以反向。

---

## 未核实 / 边界

- 风控原因无公开信息。
- Plus 的 Astra 精确额度未公布，只有估计区间。
- 272K 长上下文加价在 Codex 订阅侧免除：二手报道引企业版费率卡，原页面 403，未直接核实。
- Ultra 实耗只有一例社区报告，无官方账单结构说明。
- Artificial Analysis 两版指数数字不同（46 vs 49 等），系指数版本差异，只取相对关系。
- 本篇未自测任何档位的真实消耗，全部为官方与第三方公开数据。

---

## 资料来源

- OpenAI Reasoning guide：https://developers.openai.com/api/docs/guides/reasoning
- GPT-6 Astra 模型页：https://developers.openai.com/api/docs/models/gpt-6-astra
- ChatGPT Learn · Pricing：https://learn.chatgpt.com/docs/pricing
- ChatGPT Learn · Speed / Fast mode：https://learn.chatgpt.com/docs/agent-configuration/speed
- ChatGPT Learn · Subagents：https://learn.chatgpt.com/docs/agent-configuration/subagents
- ChatGPT Learn · Models：https://learn.chatgpt.com/docs/models
- Tibo Sottiaux 原推：https://x.com/thsottiaux/status/2096688770523467947
- Artificial Analysis · GPT-6 Astra 发布页：https://artificialanalysis.ai/models/releases/gpt-6-astra
- paddo.dev 分档数据转引：https://paddo.dev/blog/gpt-6-astra-critical-generally-available/
- openai/codex issue #43029：https://github.com/openai/codex/issues/43029
- 9to5Mac · Plus 恢复 5 小时限额：https://9to5mac.com/2026/08/24/openai-restores-5-hour-codex-and-work-limits-for-chatgpt-plus-users/
- MindStudio · GPT-5.6 Ultra：https://www.mindstudio.ai/blog/what-is-gpt-5-6-ultra-mode-multi-agent-coordination
- Lookonchain · Codex 免长上下文加价：https://m.lookonchain.com/feeds/71419
- codexusage.dev · Astra 额度：https://www.codexusage.dev/limits/astra
- kingy.ai · Codex 档位说明：https://kingy.ai/news/openai-codex-reasoning-levels-low-medium-high-extra-high/

---

## 关联文档

- ⭐ [[伪机制解释识别_四层拆解法_v1]] —— 四层框架**第三次复用**：现象✅ / 机制✅ / 根因❌（遗漏型而非捏造型）/ 药方🟡；新增形态「机制对、根因漏」
- ⭐ [[模型排名科学性律_五层评估框架与AA拆解_v1]] —— 本篇用 Artificial Analysis 分档数据时遵循「榜单用来 narrowing」：只取 xhigh≈max 的相对关系，不拿绝对分选模型
- [[Claude_Opus_4.8行为实测]] —— 同族「模型版本行为档案」：那篇记 Claude 侧 effort 分级与 Fast 降价，本篇记 OpenAI 侧的档位结构与 2.5 倍 Fast
- [[2026-07-28_Ultra模式个人作品集网站_从附件到部署闭环复盘_v1]] —— Ultra 的实战面「放大闭环密度、不替代判断」与本篇「派发不等于更聪明、任务可拆才值」互为印证
- [[任务书接AI辅助填写_模型只产草稿与思考额度陷阱_v1]] —— 同族「思考型模型额度陷阱」：那篇是 API 侧千问的思考 token 账单，本篇是订阅侧的六因子
- [[复盘事实先行原则]] —— 本篇先冻结官方事实再裁决文章，我自己被纠正的三处单列
- [[交付前实测证伪律_v1]] —— 上一轮凭机制推量级的结论被费率表证伪：机制对不等于量级对，查证要在交付前
- [[新模型试跑_硬锁清单先行_v1]] —— 同属「新模型上手先过清单」：那篇是出图硬锁，本篇是额度体检四问
- 对外版（裸路径，不进图谱）：`08_对外分发/GPT-6_Astra推理档位怎么选_额度为什么没了_同好版.md`；飞书云文档（组织内可读）：https://ncnnb044q88x.feishu.cn/docx/S7yrdMKZjo290Exqae9cjeMunTc

---

## 版本

- v1 · 2026-09-09 · 首次沉淀（官方文档 + Tibo 原推 + AA 数据交叉；含自我纠偏三处）

升级触发：
- 自测任一档位的真实消耗（同任务跑 medium / high / xhigh / max 记 token）后补实测节
- Ultra 官方账单结构公布，或积累 3 例以上实耗样本
- OpenAI 调整 Fast 倍率或档位定义
