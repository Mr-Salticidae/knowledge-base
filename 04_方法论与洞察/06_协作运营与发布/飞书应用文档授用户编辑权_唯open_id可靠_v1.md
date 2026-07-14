---
tags: [类型/协作工具链]
---
# 飞书应用文档授用户编辑权：唯 open_id 可靠

> 入档：2026-07-14
> 来源：给 pb-arena 进展文档（自建应用发布的飞书 docx）加"作者本人可编辑"权限时，连撞三堵墙、白折腾数小时后拿到的可靠解
> 验证状态：⭐⭐ 反直觉——既有笔记 / skill / 官方式做法（手机号授权）在本租户**证伪**，换 open_id 一次即成

---

## 一句话

**把"应用发布的飞书文档"授予某人编辑权，别信手机号 / 邮箱那套；唯一稳的是拿到此人 open_id，按 `member_type=openid` 授 `full_access`。而 open_id 不用申请通讯录权限——直接读该应用的 wiki 知识空间成员表就有。**

## 背景：为什么会卡

飞书自建应用用导入接口（md → docx）生成的文档**归应用所有**，作者本人打开自己的文档只有只读权，必须显式把作者加为协作者才能编辑。既有做法（见 skill `feishu-doc-publish` 与对外版）教的是：配 `owner_mobile` → 调通讯录接口把手机号换成 open_id → 授权。**这条在本租户（蛛网文化传播 / 应用"蛛网之上" `cli_aab2776096f81cca`）走不通。**

## 三堵墙（都别再撞了）

| 路子 | 结果 | 根因 |
| --- | --- | --- |
| 手机号 → open_id（`/contact/v3/users/batch_get_id`，tenant token） | `99991672 权限不足` | `contact:user.id:readonly` 这条权限只给「**用户身份**」；应用用的是「**应用身份**」(tenant token)，拿不到。**发版、管理员审核都没用**——身份类型不对，不是没生效 |
| 邮箱直接授权（`member_type=email`） | `1063001 Invalid parameter` | 该协作者接口不认 email 成员类型（至少本租户如此），换 edit/full_access 都一样 |
| 文档「邀请协作者」里搜人 | 搜名字/手机号/邮箱都只出**群聊**、搜不到本人 | 单人组织 + 应用拥有的文档，个人账号在协作者搜索里不可见 |

> 教训：官方文档里「支持」不等于「你这个应用的这个身份能用」。权限管理页每条权限右边标的是「用户身份」还是「应用身份」——**看清这个再动手**，能省几小时。

## 可靠做法：从 wiki 空间成员表取 open_id

只要该应用是某个 **wiki 知识空间**的可访问方（本例应用同时是知识库空间的管理员），空间成员表里就直接带着人的 open_id，且这个读取**不需要通讯录权限**。

```bash
# 1. 读空间成员，拿到用户 open_id（member_role=admin 的那个人）
GET /open-apis/wiki/v2/spaces/<space_id>/members
#   → members[].member_type=openid, member_id=ou_xxxx

# 2. 按 open_id 授权（应用有云文档权限即可，无需通讯录权限）
POST /open-apis/drive/v1/permissions/<doc_token>/members?type=docx&need_notification=false
     { "member_type": "openid", "member_id": "ou_xxxx", "perm": "full_access" }

# 3. 核验：协作者列表里出现 openid=ou_xxxx perm=full_access 即成
GET /open-apis/drive/v1/permissions/<doc_token>/members?type=docx
```

拿到 open_id 后写进 `~/.feishu/config.json` 的 `owner_open_id`，以后每次发布自动授权，**永久绕开手机号/邮箱这套坑**。工具解析优先级：`owner_open_id` > `owner_email` > `owner_mobile`。

## 附带：链接分享默认改互联网只读

同批需求里把分享档位默认从「组织内可阅读」提到「**互联网可阅读（只读）**」：`PATCH /drive/v2/permissions/<doc>/public` 传 `{"link_share_entity":"anyone_readable"}`。要私密时退回 `tenant_readable`。放开到互联网属扩大对外暴露，操作前要跟本人说清含义。

## 举一反三

- 任何"机器人/应用替你生成、但你要能编辑"的飞书文档，都用 open_id 授权，别绕通讯录。
- 拿不到 open_id 时，先想"这个人在不在我应用能读的某个 wiki 空间 / 群 / 文档协作者表里"——成员表往往就是最近的 open_id 来源。
- 更普适的一条：**接口报"权限不足"先分清 tenant / user 身份**，很多"开了权限还是不行"都是身份类型错配，不是没发版。

## 关联文档

- 同族能力边界（本次又一次印证插件/自动化"最后一公里必须人来"）：[[浏览器插件自动化的能力边界_v1]]
- 本律纠正的对外白话版（其"手机号授权"步骤已按本文修订）：`08_对外分发/让AI助理一句话发飞书文档_零依赖CLI链路搭建_同好版.md`
- 封装此链路的 skill：[[feishu-doc-publish/SKILL.md]]
- 协作核查心法（别把"官方说支持"当已验证）：[[Claude完成报告核查心法]] · [[交付前实测证伪律_v1]]
