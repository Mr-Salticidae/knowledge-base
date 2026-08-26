---
tags: [类型/平台工程, 主题/LLM接入, 主题/凭据管理, 来源/DeepSeekHarness, 主题/agnes]
---
# agnes接入DeepSeekHarness_双节点实测与思考方言

> 首次记录：2026-08-26
> 来源：本地 DeepSeek Harness（E:\deepseek-harness）接入 Agnes AI（agnes-ai.com），沿用 [[DSH接入第三方OpenAI兼容提供商_providers声明与凭据热重载断档_v1]] 的标准流程，新增 4 个文本模型。
> 状态：headless 端到端验证通过（agent 链路真实对话成功）；Web 服务已重启加载新 provider。

---

## 事实记录（不可修改区）

- 项目：DeepSeek Harness 本地部署，DSH_HOME = `E:/deepseek-harness/.dsh-home`
- 接入提供商：**Agnes AI**（agnes-ai），OpenAI 兼容，`apiKeyEnv: AGNES_API_KEY`
- baseURL：`https://apihub.agnes-ai.com/v1`（国际站；国内站 `https://apihub.agnes-ai.cn/v1` 实测同一 key 同样可用、模型列表一致）
- 接入模型（实测 `/v1/models` 全量 9 个）：
  - 文本 4 个：`agnes-2.0-flash` / `agnes-2.5-flash` / `agnes-2.5-pro` / `agnes-2.5-pro-alpha`
  - 图像 2 个：`agnes-image-2.0-flash` / `agnes-image-2.1-flash`
  - 视频 3 个：`agnes-video-v2.0` / `agnes-video-2.5` / `agnes-video-2.5-flash`
- 配置要点：`compat.thinkingFormat: deepseek`（实测返回 `reasoning_content`，DeepSeek 方言思考流）
- 验证方式：curl 直连（models 200 + chat completion 真实返回）+ `dsh --profile headless` 全链路 agent 调用（返回「确认」）+ Web 服务重启（healthz 200）
- 数据来源：agnes 官方 wiki（agnes-25-flash 规格）、agnese 平台 /v1/models 实测、curl 实测、headless 实测

---

## 一句话总结

agnes 是标准的 OpenAI 兼容 hand-declared route——配置结构与 LongCat 完全同构，唯一必须注意两点：**它默认开启思考且输出 DeepSeek 方言的 `reasoning_content`，必须声明 `compat.thinkingFormat: deepseek`**；**官方宣传的「1M 上下文」是错的，官方 wiki 写 512K 上下文 / 65.5K 最大输出**（营销文与官方文档打架时以 wiki 为准）。

---

## 核心律

### 1. 双节点域名实测 key 通用，选 .com 或 .cn 均可

`apihub.agnes-ai.com`（国际）与 `apihub.agnes-ai.cn`（国内）用**同一个 key** 实测都返回 200，`/v1/models` 模型列表完全一致（9 个）。官方称「国内站和国际站账号不互通」但实测 key 两边通用（可能共享后端）。大陆网络访问 .cn 延迟更低，.com 是官方文档主地址——二者可随时切换。

### 2. agnes 默认开启思考，输出 DeepSeek 方言 reasoning_content

curl 实测 `agnes-2.5-flash` 响应体里带 `reasoning_content` 字段（思考流），且 `max_tokens` 会被思考 token 先吃掉（实测 32 token 全部被 reasoning 占用，`text_tokens: 0`，`finish_reason: "length"`）。这决定了：
- `compat.thinkingFormat: deepseek` **必须声明**，否则 DSH 会把思考内容当正文
- `maxTokens` 声明要给足余量（官方最大输出 65.5K，但其中包含思考 token）

### 3. 上下文窗口以官方 wiki 为准，营销文会吹牛

agnese 多篇营销文称「标配 1,000,000 Token (1M)」，但官方 wiki（agnes-25-flash）写 **Context window 512K / Maximum output 65.5K**。配置里用 524288 / 65536。判据：**spec 类数字优先信官方文档（wiki/docs），不信营销号与聚合站**。

### 4. 图像/视频模型不进 providers 声明

agnes 的图像（agnes-image-2.x）与视频（agnes-video-*）是**独立端点类型**（`supported_endpoint_types` 非 openai），不是 `/chat/completions` 能调的对象——与既有律 [[OpenAI兼容止于对话端点_多提供商视频接口分流与真key首测_v1]] 一致：**OpenAI 兼容止于对话端点**。文本模型进 `providers`，图像/视频要打包成 skill 用各自端点调。

### 5. --patch 不能覆盖 agent-default-model

`dsh --patch <file>` 的 patch 文件是 **loader entry patch 数组**（`@deepseek-ai/cordis-plugin-include` 的 PatchOptions，作用于插件加载树），**不是用户 settings 覆盖**——拿它改 `agent-default-model` 会报 `must be a top-level YAML array of loader patch entries`。headless 验证默认模型要**临时改 settings.yaml 的 `agent-default-model` 再恢复**。

---

## 踩坑记录

### ⚠️ 坑 1：--patch 覆盖默认模型报错（本次现形）

**现象**：`dsh --profile headless --patch ./tmp.yml "..."` 报 `overlay ... must be a top-level YAML array of loader patch entries`。
**根因**：patch 文件格式是插件加载层的 PatchOptions（数组），不是普通 YAML 配置覆盖。
**处置**：临时 Edit `settings.yaml` 的 `agent-default-model` → headless 验证 → 改回 longcat。配置文件在 headless 每次启动时重新读取，无需重启。

### ⚠️ 坑 2：营销文上下文窗口虚标（复核确认）

**现象**：多篇推文称 agnes-2.5-flash 上下文 1M。
**根因**：营销文夸大；官方 wiki 明写 512K / 65.5K。
**处置**：按官方 wiki 配置 524288 / 65536。

### ⚠️ 坑 3：max_tokens 被思考 token 吃满

**现象**：`max_tokens: 32` 时返回 `finish_reason: "length"`、`reasoning_tokens: 32`、`text_tokens: 0`，正文为空。
**根因**：agnes 默认开启思考，输出预算先给 reasoning。
**处置**：max_tokens 给足余量；测试连通性时加大 max_tokens（如 128+）再断言正文。

---

## 配置模板（本次落地）

### settings.yaml（providers 声明）

```yaml
    agnes:
      displayName: Agnes
      apiKeyEnv: AGNES_API_KEY
      api: openai-completions
      baseURL: https://apihub.agnes-ai.com/v1
      compat:
        thinkingFormat: deepseek
      models:
        - id: agnes-2.0-flash
          name: Agnes 2.0 Flash
          contextWindow: 524288
          maxTokens: 65536
          input: [ text, image ]
        - id: agnes-2.5-flash
          name: Agnes 2.5 Flash
          contextWindow: 524288
          maxTokens: 65536
          input: [ text, image ]
        - id: agnes-2.5-pro
          name: Agnes 2.5 Pro
          contextWindow: 524288
          maxTokens: 65536
          input: [ text, image ]
        - id: agnes-2.5-pro-alpha
          name: Agnes 2.5 Pro Alpha
          contextWindow: 524288
          maxTokens: 65536
          input: [ text, image ]
```

### .credentials.yaml

```yaml
AGNES_API_KEY: sk-...
```

---

## 端点速查

| 提供商 | baseURL | 文本模型 | 上下文 | 输出 | 思考流 | 备注 |
|---|---|---|---|---|---|---|
| Agnes 国际站 | `https://apihub.agnes-ai.com/v1` | agnes-2.0-flash / 2.5-flash / 2.5-pro / 2.5-pro-alpha | 512K | 65.5K | ✅ 默认开启，DeepSeek 方言 | 2.5-flash 当前免费 |
| Agnes 国内站 | `https://apihub.agnes-ai.cn/v1` | 同上（实测模型列表一致） | 512K | 65.5K | ✅ | 大陆访问延迟更低 |
| 图像 | 同上，模型名换 agnes-image-2.0/2.1-flash | — | — | — | — | 独立端点类型，需 skill 封装 |
| 视频 | 同上，模型名换 agnes-video-v2.0 / 2.5 / 2.5-flash | — | — | — | — | 同上 |

> 关联：[[DSH接入第三方OpenAI兼容提供商_providers声明与凭据热重载断档_v1]]（标准流程）、[[OpenAI兼容止于对话端点_多提供商视频接口分流与真key首测_v1]]（图像/视频分流）
