# GPT-6 Astra 推理档位怎么选，额度为什么没了

> 写给用 Codex 跑 GPT-6 Astra、看着额度往下掉一脸懵的你。所有数字来自 OpenAI 官方文档、OpenAI 工程师的公开发言和 Artificial Analysis 的公开数据，截至 2026 年 9 月 9 日。文末附来源。

## 先说结论

1. 推理档位确实影响额度，但它只是官方列出的**六个因子之一**。另外两个同量级的项，很多人一个字都没听过：**Fast 模式按 2.5 倍扣**，**上下文每一回合都要重发**。
2. 档位排序里真正不划算的是 **Max**，不是 Extra High。两者在公开基准上分数持平，Max 贵四成。
3. Ultra 不是「更聪明的档位」，是「Max 推理 + 自动拉子代理分工」。任务拆不开就别开，开了就是纯多付。

下面把每一条讲清楚。

---

## 一、推理档位到底是什么

先解释两个词。

- **Codex**：OpenAI 的编码代理，能在你的电脑里读文件、改代码、跑命令。它和网页版 ChatGPT 聊天是两个产品。
- **推理档位**（reasoning effort）：你允许模型在给答案之前「想多久」。OpenAI 官方文档的原话是：**同一个模型，不同的推理 token 预算**。模型没换，换的是它被允许花多少思考量。

Codex 界面上的六个选项，对应关系如下。

| 界面上的名字 | 官方说明 |
|---|---|
| Light（命令行里叫 Low） | 快速回答，轻量推理 |
| Medium（默认） | 速度与深度平衡，日常任务 |
| High | 复杂问题用更深的推理 |
| Extra High | 比 High 更深 |
| Max | 给单个任务更多思考时间 |
| Ultra | **最大推理 + 自动把任务派给子代理** |

注意最后一行。前五个是同一个模型的不同思考预算，Ultra 是一个**模式**，后面单独讲。

另外两条官方细节：

- 推理过程你看不到，但**按输出 token 计费**。这是它贵的根本原因，下一节讲。
- 一个会话里可以中途改档位，上下文不丢。但只在普通单代理模式下可以，Ultra 模式下不能改。

---

## 二、额度是怎么扣的

OpenAI 在订阅套餐里按「积分」扣额度，积分按 token 数算。官方原话：**你的提示词、文件、聊天历史、工具结果、模型的回复，全都消耗 token。**

GPT-6 Astra 的扣分率如下（单位：积分 / 每百万 token）。

| 类型 | 积分 |
|---|---|
| 输入 | 250 |
| 缓存输入（重复发送、命中缓存的部分） | 25 |
| **输出，包括看不见的推理** | **1250** |

看这三个数的比例就明白了：**输出是输入的 5 倍，是缓存输入的 50 倍**。推理 token 走输出，所以档位越高越贵，这一点没错。

但官方紧接着说了一句很多科普文不引的话：**模型选择、上下文、推理、工具调用、检索、缓存，全都影响消耗，光看提示词长度估不准。** 六个因子。

其中三个和你的日常操作直接相关：

**1. Fast 模式，2.5 倍。** 官方原文：Fast mode applies a 2.5x multiplier to Astra's Standard rate。它只让模型快 1.5 倍左右，代价是每一个 token 都按 2.5 倍扣。作为对比，在公开基准上从 Medium 升到 High 成本只多约一成。**一个 Fast 开关，抵三档推理。**

**2. 上下文，每一回合都重发。** Codex 这类代理每次调用工具都是一次完整请求，整段对话历史、读过的文件、工具输出都会随每一回合重新发送。命中缓存的部分按 1/10 计，但没缓存的新内容按全价。一个跑了两百回合、上下文几十万 token 的长会话，输入侧的累计消耗可以超过推理侧。

**3. 推理档位。** 就是上一节讲的。

再补三条你可能关心的：

- **网页版 ChatGPT 聊天和 Codex 的额度是分开的。** 5 小时限额的范围是「ChatGPT Work 和 Codex」这两个代理类产品，普通聊天单独计量。所以查资料、问问题去网页版聊，别在 Codex 里聊。
- **Pro 的额度是 Plus 的 5 倍或 20 倍**，对应 100 美元和 200 美元两档。官方原话。
- Plus 用 Astra 的额度，官方只给了一个估计区间：**每 5 小时约 5 到 45 条本地消息**，按任务重量浮动。周上限没公布。

---

## 三、各档位值不值：看数据

OpenAI 工程师 Tibo Sottiaux 在 2026 年 9 月 7 日的原话：

> GPT-6 Astra 开 low 的表现，好于上一代 GPT-5.6 Sol 开 high。如果你之前在 Sol 上用 high 用得很满意，建议在 Astra 上降到 low 或 medium。

第三方评测机构 Artificial Analysis 对 GPT-6 Astra 五个档位的公开数据：

| 档位 | 智能指数 | 每个任务成本 |
|---|---|---|
| Low | 46 | $0.82 |
| Medium | 50 | $1.54 |
| High | 51 | $1.72 |
| Extra High | 53 | $2.31 |
| Max | 53 | $3.26 |

三个观察：

- **Low 到 Medium 涨 4 分，Medium 到 High 只涨 1 分。** Medium 是性价比拐点，这也是官方默认值。
- **Extra High 到 Max 分数一样，成本多四成。** 另一个版本的指数是 54 对 55，跑完的输出 token 从 3000 万涨到 4900 万。
- 官方文档对两档的定位也不同：Extra High 给「深度研究、异步工作流、需要很长 rollout 的代理任务」，且明确写了「只在你的评测证明有收益时用」；Max 给「单个最难的任务」。

网上流传一种说法：「Extra High 很尴尬，任务够难就直接 Max，一轮解决反而省」。这个推论的前提是 Max 一轮做对的概率明显高于 Extra High。**数据不支持这个前提。** 按成本效率排，尴尬的是 Max。

---

## 四、Ultra 是什么，什么时候用

官方定义一句话：**Ultra 使用最大推理，并让模型主动把合适的工作派给子代理。**

拆开看：

- 主代理跑在 Max 档。所以 Ultra 至少和 Max 一样聪明，说它「不是更聪明只是更贵」不准确。
- 主代理会把任务拆成几块，同时开几个子代理并行做，最后汇总。**每个子代理各自消耗自己的模型调用和工具调用**，官方原话是「子代理工作流比同等单代理消耗更多 token」。
- 官方给的适用场景：**读密集、能拆开的任务**。探索代码库、跑测试、分诊问题、总结文档。
- 官方明确警告：**写密集的并行会冲突。** 几个子代理同时改同一批文件，合并成本可能高于收益。

一个公开样本：有 Pro 20x 用户在 GitHub 上报告，用 Astra Ultra 做一个 SwiftUI 加载动画的重构，跑了 1 小时 11 分，3 个子代理，**消耗了周额度的三成**。

所以判断标准只有一条：**你这个任务能不能拆成几块互不打架的活。** 能拆，Ultra 有价值。不能拆，比如你在一个文件里顺着改、每一步依赖上一步，开 Ultra 就是给几个子代理付薪水让它们等着。

另外，「额度快重置了拿 Ultra + Fast 清仓」这个用法，是 Max 推理 × 子代理数 × 2.5 倍，是目前能选出的最贵组合。清仓当然可以，但别把它当成 Ultra 的正确用法。

---

## 五、额度体检卡

额度掉得快，按这个顺序自查：

1. **Fast 开了吗？** 先关。2.5 倍。
2. **一个会话跑了多久？** 上下文每回合重发。一个任务一个新会话，别把大日志、大 JSON 整段贴进对话。
3. **档位高于任务需要吗？** 日常 Medium，困难调试 High，长 rollout 的代理任务 Extra High，Max 极少用。
4. **Ultra 用在能拆的任务上了吗？** 不能拆就关。

前两条是大多数科普文不讲的，也是最容易立刻见效的。

---

## 六、按套餐给的建议

**Plus（20 美元）**

- 查资料、问问题去网页版 ChatGPT，那边额度分开算。
- Codex 里 Medium 常驻，Fast 关掉。
- 遇到确实难的调试，临时切 High，做完切回来。
- 一个任务一个会话。

**Pro（100 / 200 美元）**

- 官方和 Tibo 的建议都是 Medium 起步。想常驻 High 也行，但要知道这是偏好不是必要。
- 先规划后执行的习惯值得保留：规划阶段用 Extra High 或 Max，出了方案切回 Medium 或 High 执行。同一会话里切档位，上下文不丢。
- Ultra 留给能拆的大任务：跑全量测试、扫一遍代码库找问题、批量迁移互不依赖的模块。
- Fast 只在你真的在等它、时间比额度贵的时候开。

---

## 七、哪些还没证实

诚实起见，列一下这篇里没有直接核实的部分：

- Plus 的 Astra 精确额度，官方只给估计区间。
- 有报道说 Astra 在 Codex 订阅侧免除了 27.2 万 token 以上的长上下文加价（API 侧仍是输入 2 倍、输出 1.5 倍），引用的是企业版费率卡，原页面没能打开。
- Ultra 的真实消耗只有一例社区报告，没有官方账单结构说明。
- Artificial Analysis 的两版指数数字不同，这里只取相对关系。
- 本文没有自测任何档位的真实消耗，全部为公开数据。

---

## 来源

- OpenAI 推理指南：https://developers.openai.com/api/docs/guides/reasoning
- GPT-6 Astra 模型页：https://developers.openai.com/api/docs/models/gpt-6-astra
- ChatGPT Learn 定价页：https://learn.chatgpt.com/docs/pricing
- ChatGPT Learn Fast 模式：https://learn.chatgpt.com/docs/agent-configuration/speed
- ChatGPT Learn 子代理：https://learn.chatgpt.com/docs/agent-configuration/subagents
- ChatGPT Learn 模型页：https://learn.chatgpt.com/docs/models
- Tibo Sottiaux 原推：https://x.com/thsottiaux/status/2096688770523467947
- Artificial Analysis GPT-6 Astra 页：https://artificialanalysis.ai/models/releases/gpt-6-astra
- openai/codex issue #43029：https://github.com/openai/codex/issues/43029
- 9to5Mac 报道 Plus 恢复 5 小时限额：https://9to5mac.com/2026/08/24/openai-restores-5-hour-codex-and-work-limits-for-chatgpt-plus-users/
