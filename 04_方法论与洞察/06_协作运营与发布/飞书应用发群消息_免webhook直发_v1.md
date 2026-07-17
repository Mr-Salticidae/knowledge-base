---
tags: [类型/协作工具链]
---
# 飞书应用发群消息：免 webhook 直发

> 入档：2026-07-17
> 来源：首次让飞书智能体（自建应用"小桁"）把开源项目盘点文档发进「蛛网文化传播」群，一次通
> 验证状态：⚠️首次（单租户单群验证；链路四步全部真机走通）

---

## 一句话

**自建应用发群消息不用另建 webhook 机器人：只要 bot 已在群、应用有 IM 权限，tenant token 直接 `POST /im/v1/messages` 就发出去了；chat_id 也不用问人——`GET /im/v1/chats` 列出 bot 所在的群，表里就有。**

## 背景：链路里缺的最后一步

此前"小桁"链路只覆盖到**建文档拿链接**（pb-arena 的 feishu-doc-sync CLI，见 [[feishu-doc-publish/SKILL.md]]），"把链接发到群里"一直是人肉粘贴。这次的诉求是全托管：整理 → 发布文档 → **机器人自己发群**。CLI 不支持发消息，于是直接裸调 IM API 补上最后一步。

## 链路四步（全部零依赖，Node ≥18 原生 fetch）

```text
1. POST /auth/v3/tenant_access_token/internal   # app_id + app_secret 换 tenant token
2. GET  /im/v1/chats                            # 列 bot 所在群 → 验证"在群"并拿 chat_id
3. （建文档）feishu-doc-sync CLI 发布 md → 拿回 docx 链接
4. POST /im/v1/messages?receive_id_type=chat_id # 把摘要+链接发进群
```

第 4 步请求体（**注意 content 是"JSON 字符串"不是对象**，双重序列化是最容易踩的坑）：

```js
const r = await fetch('https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + tenantToken },
  body: JSON.stringify({
    receive_id: 'oc_xxxx',                       // GET /im/v1/chats 里的 chat_id
    msg_type: 'text',
    content: JSON.stringify({ text: '……' })      // ← 内层再 stringify 一次
  })
});
// r.code === 0 且返回 message_id 即成
```

本租户实值：群「蛛网文化传播」chat_id = `oc_f60819a8e42b213035b12154cdffe43b`；应用凭据在 `~/.feishu/config.json`（app_id `cli_aac04681d3399be8`，secret 不落库）。

## 要点与坑

| 要点 | 说明 |
| --- | --- |
| 读探测先行 | 先 `GET /im/v1/chats`（只读）确认权限可用 + bot 在群 + 拿 chat_id，再进有副作用的发消息。别带着未验证的权限假设直接 POST |
| content 双重序列化 | `content` 字段的值是 JSON **字符串**（`JSON.stringify({text})`），直接传对象报参数错误 |
| receive_id_type | 发群用 `chat_id`（oc_ 开头）；query 参数别漏，漏了 receive_id 解析不了 |
| 文档档位与群发的配合 | 文档默认「互联网可阅读(只读)」（见 [[飞书应用文档授用户编辑权_唯open_id可靠_v1]] 附带节），群成员点链接即读，**不需要逐人授权**——群发链路能一次通，一半功劳在分享档位早已放开 |
| 前置条件（跟应用走） | ① bot 已被拉进目标群；② 应用开通 IM 发消息权限。本应用两者此前已具备，换新应用/新群才需重配 |

## 举一反三

- 与「open_id 从 wiki 空间成员表读」（[[飞书应用文档授用户编辑权_唯open_id可靠_v1]]）同构的一条：**应用自己"能看见"的资源列表，就是最近的 id 字典**。要给 X 发东西先要 X 的 id 时，别先想申请通讯录/管理权限，先想"bot 已经在哪些群/空间/文档里"——列表接口里往往直接带着 id。
- "CLI 不支持"不等于"链路断了"：CLI 只是对 API 的一层薄封装，缺的动作用同一份凭据裸调 API 即可补齐，不必等工具升级。
- 机器人全托管发布的通用四拍：**换 token → 读探测（验权限+拿 id）→ 产出物落位 → 副作用动作**。任何"生成内容并送达某处"的自动化都能套。

## 关联文档

- 同应用文档授权与分享档位（本档链路的前半段）：[[飞书应用文档授用户编辑权_唯open_id可靠_v1]]
- 封装文档发布段的 skill（发群是其未覆盖的延伸，见本档）：[[feishu-doc-publish/SKILL.md]]
- 读探测先行的同族心法：[[交付前实测证伪律_v1]]
- 本档对外白话版（「进阶：让助理直接发群」一节）：`08_对外分发/让AI助理一句话发飞书文档_零依赖CLI链路搭建_同好版.md`
