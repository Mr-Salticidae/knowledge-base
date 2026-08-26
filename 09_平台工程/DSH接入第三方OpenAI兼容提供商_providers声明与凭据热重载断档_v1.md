---
tags: [类型/平台工程, 主题/LLM接入, 主题/凭据管理, 来源/DeepSeekHarness]
---
# DSH接入第三方OpenAI兼容提供商_providers声明与凭据热重载断档

> 首次记录：2026-08-25
> 来源：本地 DeepSeek Harness（@deepseek-ai/dsh v0.1.0-rc.6，E:\deepseek-harness）接入 LongCat 与阿里云百炼 Token Plan 两家第三方提供商。
> 状态：两家均端到端验证通过（headless 全链路 + curl 直连）；Web 服务凭据热重载问题已定位并给出重启解法。

---

## 事实记录（不可修改区）

- 项目：DeepSeek Harness 本地部署，DSH_HOME = `E:/deepseek-harness/.dsh-home`
- 接入提供商：
  - **LongCat**（美团）：`https://api.longcat.chat/openai`，模型 `LongCat-2.0`（1M 上下文 / 128K 输出），思维链模型
  - **百炼 Token Plan 个人版**（阿里云）：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，模型 `qwen3.8-max`（1M 上下文 / 128K 输出，2.4T MoE / 95B 激活），思维链模型
- 配置文件：`settings.yaml`（`llm-pi-ai.providers` 命名空间）+ `.credentials.yaml`（凭据键值对）
- 验证方式：curl 直连 API（模型列表 / 对话补全 / 参数兼容性）+ `dsh --profile headless` 全链路 agent 调用
- 数据来源：dsh-llm-pi-ai README、dsh-credentials-local README、阿里云百炼官方文档、curl 实测

---

## 一句话总结

DSH 的 `llm-pi-ai` 插件用一份 `providers` dict 声明任意 OpenAI 兼容提供商——**端点、协议、模型目录全靠 YAML 配置而非代码**，但凭据写入 `.credentials.yaml` 后 **Web 进程的环境快照不会热更新**，必须重启才能让新 key 生效。

---

## 核心律

### 1. providers 是 dict，models 列表整体替换目录

`llm-pi-ai.providers` 下每个键是一个路由名（如 `longcat`、`bailian`），值是该路由的完整 provider 声明。**catalog route**（pi-ai 内置已知的，如 openai/deepseek）继承端点与模型目录；**hand-declared route**（pi-ai 不认识的，如 longcat/bailian）必须自填 `api` + `baseURL` + `models`。

`models` 列表 **替换** 而非扩展该路由的内置目录——声明了 `models` 就必须列出所有要用模型，哪怕只列 `id` 一个字段也够。`modelOverrides` 则是原地修改单个 catalog 模型而不替换整表。

### 2. apiKeyEnv 是凭据引用名，不是凭据本身

`apiKeyEnv: LONGCAT_API_KEY` 是一个**引用**——运行时由 `dsh-credentials-local` 插件从 `.credentials.yaml`（或环境变量）按此名解析。**密钥不进 settings.yaml**，只进 `.credentials.yaml`，键名 = `apiKeyEnv` 的值。省略 `apiKeyEnv` 则走 pi-ai 的环境变量 ambient discovery。

### 3. 凭据文件热重载 ≠ Web 进程环境快照热更新

`dsh-credentials-local` 支持文件热重载（外部编辑 `.credentials.yaml` 会触发 `credentials/updated` 事件）。但 **Web 进程在启动时冻结了一份环境快照**，启动后写入的新凭据**不会进入该进程的环境层**——headless 每次启动都重新读，所以 headless 测试通过 ≠ Web UI 能用。**写入新凭据后必须重启 Web 服务**。

> 判据：headless 测试通过但 Web UI 报 `API key is invalid (AUTH)` → 99% 是 Web 进程在凭据写入前已启动。

### 4. 推理参数兼容性要逐家实测，不能假设

同样是「OpenAI 兼容」端点，对推理控制参数的支持天差地别：

| 提供商 | `thinking:{type}` | `reasoning_effort` | `temperature` 等常规参数 | 默认思维链 |
|---|---|---|---|---|
| LongCat | ✅ 接受（DeepSeek 方言） | ✅ 接受 | ✅ | 默认开启 |
| 百炼 Token Plan | ❌ 拒绝（报 InvalidApiKey） | ❌ 拒绝 | ✅ | 默认开启，无法关闭 |

**百炼的参数拒绝错误会伪装成 `Invalid API-key provided`**——实际是参数不支持，但错误信息指向认证失败，极具误导性。判据：同一个 key 裸请求成功、带额外参数失败 → 是参数问题不是 key 问题。

### 5. compat.thinkingFormat 决定推理参数的线上拼写

对 hand-declared route，pi-ai 无法从 URL 推断推理方言，需手动声明 `compat.thinkingFormat`：
- `deepseek`：`off` → `thinking:{type:"disabled"}`，effort 档位 → `thinking:{type:"enabled"}` + 对应 spelling
- 不声明：走 OpenAI 方言，`off` → 什么都不发（provider 默认行为），effort → `reasoning_effort` 字段

选错方言 = 参数被静默忽略或报错。**选哪个方言要 curl 实测**：先裸请求确认 key 有效，再逐个测 `thinking` / `reasoning_effort` 参数，最后测 `off`（关闭思维链）是否真正生效。

---

## 踩坑记录

### ⚠️ 坑 1：Web 进程凭据快照断档（首次现形）

**现象**：headless 端到端测试百炼成功返回"确认"，但 Web UI（MemoraX Code）运行报 `API key is invalid (AUTH)`。

**根因**：Web 服务进程在 `.credentials.yaml` 写入 `BAILIAN_API_KEY` **之前**已启动。`dsh-credentials-local` 虽然热重载文件，但 Web 进程的环境快照层（`env` source）在启动时冻结，新写入的凭据只更新了 `file` 层，而 `env` 层优先级更高——但 `env` 层里没有这个 key，`file` 层有，按理 `file` 应该 win。**实际问题更微妙**：Web 进程的 settings 命名空间缓存可能未刷新，或 pi-ai adapter 的 provider 注册在启动时已完成。

**判据**：`headless 通过 + Web 失败 = 重启 Web`。重启后凭据重新加载，问题消失。

**处置**：找到并终止占用 3080 端口的 node 进程，重新 `dsh web` 启动。Windows 下 `netstat -ano | grep :3080` 找 PID（注意 TIME_WAIT 残留不是 LISTENING），或直接 `taskkill /PID <pid> /F`。

### ⚠️ 坑 2：百炼参数拒绝伪装成 InvalidApiKey（首次现形）

**现象**：百炼裸请求成功，带 `thinking:{enabled:false}` / `reasoning_effort:"low"` / `enable_thinking:false` 等任何额外参数都返回 `{"error":{"code":"invalid_api_key","message":"Invalid API-key provided"}}`。

**根因**：百炼 Token Plan 的 OpenAI 兼容端点**不支持推理控制参数**，但错误信息不报「参数不支持」而报「API key 无效」。连续高频请求也会触发同样的伪装错误（实为限流）。

**判据**：同一 key 裸请求成功 + 带参数失败 → 参数问题，不是 key 问题。**永远先 curl 裸请求确认 key 有效**，再测参数兼容性。

**处置**：百炼配置中**不声明 `reasoningEfforts`**，交由模型默认启用思维链。LongCat 则实测支持 `thinking:{type}` 全形式，声明 `compat.thinkingFormat: deepseek` + `reasoningEfforts: {off:, low:low, medium:medium, high:high}`。

### ⚠️ 坑 3：百炼 models 列表端点返回 InvalidApiKey（首次现形）

**现象**：`GET /compatible-mode/v1/models` 返回 `{"code":"InvalidApiKey"}`，但 `POST /chat/completions` 正常工作。

**根因**：百炼 Token Plan 的 `/models` 端点鉴权方式与 `/chat/completions` 不同（可能不支持 Token Plan key，或端点本身未开放）。

**处置**：不依赖 `/models` 拉列表，手动从官方文档查模型规格填入 `models` 声明。

### ⚠️ 坑 4：工作区路径 ENOENT（DSH 记忆残留）

**现象**：DSH Web 启动后报 `ENOENT: no such file or directory`，无法打开工作区。

**根因**：DSH 记住了上次的工作区路径（如 `E:\deepseek-harness\lab\擦干净`），但该目录已被重命名/删除（实际名为 `擦干净一站式`）。DSH 启动时尝试打开上次路径，找不到就报错。

**处置**：创建缺失目录，或在 DSH UI 中重新选择工作区。

---

## 配置模板

### settings.yaml（providers 声明）

```yaml
llm-pi-ai:
  providers:
    longcat:
      displayName: LongCat
      apiKeyEnv: LONGCAT_API_KEY
      api: openai-completions
      baseURL: https://api.longcat.chat/openai
      compat:
        thinkingFormat: deepseek
      models:
        - id: LongCat-2.0
          name: LongCat-2.0
          contextWindow: 1048576
          maxTokens: 131072
          reasoningEfforts:
            off:
            low: low
            medium: medium
            high: high
    bailian:
      displayName: 百炼
      apiKeyEnv: BAILIAN_API_KEY
      api: openai-completions
      baseURL: https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
      models:
        - id: qwen3.8-max
          name: Qwen-3.8-Max
          contextWindow: 1000000
          maxTokens: 131072
```

### .credentials.yaml（凭据键值对）

```yaml
DEEPSEEK_API_KEY: sk-...
LONGCAT_API_KEY: ak_...
BAILIAN_API_KEY: sk-sp-...
```

> 格式约束：纯 YAML mapping，键必须是 POSIX identifier（字母+数字+下划线），值为非空字符串。注释会随条目删除而移除。

---

## 接入新提供商的标准流程

1. **curl 裸请求确认 key 有效**：`POST {baseURL}/chat/completions`，带最小 messages + max_tokens
2. **curl 测参数兼容性**：逐个测 `thinking:{type:"disabled"}` / `reasoning_effort` / `temperature`，观察哪些被接受、哪些被拒绝
3. **curl 测模型列表端点**：`GET {baseURL}/models`，失败则从官方文档手动查模型规格
4. **写入 .credentials.yaml**：`{CREDENTIAL_REF}: {key}`，键名自取（POSIX identifier）
5. **写入 settings.yaml**：`llm-pi-ai.providers.{route}` 声明，含 `apiKeyEnv` / `api` / `baseURL` / `models`，按参数兼容性决定是否声明 `compat.thinkingFormat` 和 `reasoningEfforts`
6. **headless 验证**：临时把 `agent-default-model` 切到新提供商，跑 `dsh --profile headless "只回复：确认"`
7. **重启 Web 服务**：headless 通过后，**必须重启 Web 进程**让凭据快照刷新
8. **Web UI 验证**：浏览器打开 127.0.0.1:3080，切 provider + model，发一条消息确认

---

## 端点速查

| 提供商 | baseURL | 模型 | 上下文 | 输出 | 思维链 | 推理参数控制 |
|---|---|---|---|---|---|---|
| LongCat | `https://api.longcat.chat/openai` | LongCat-2.0 | 1M | 128K | ✅ 默认开启 | ✅ `thinking:{type}` 全形式 |
| 百炼 Token Plan | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | qwen3.8-max | 1M | 128K | ✅ 默认开启 | ❌ 不支持，错误伪装成 InvalidApiKey |
| 百炼 Anthropic 兼容 | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic` | — | — | — | — | Anthropic 协议，DSH 未接入 |

> 百炼 Token Plan 的 API Key 以 `sk-sp-` 开头，与百炼通用 API Key（`sk-` 开头）格式不同，两者不可混用，必须配套使用各自的 Base URL。
