---
tags: [类型/协作工具链, 主题/小红书, 主题/发布]
---
# 小红书笔记外链必带 xsec_token v1

> 入档:2026-06-20
> 来源:becoming-a-prompt-master 画廊第 3 期「小红书原帖」按钮点击无法跳转的排查
> 性质:平台发布操作坑(单次发现,但可直接当规则用)

---

## 一句话

往任何**站外页面**(画廊 / 网站 / 文档 / README)放小红书笔记链接时,**必须用带 `xsec_token` 的完整分享链接,或 App「分享 → 复制链接」得到的 `xhslink.com/o/xxx` 短链**;**绝不能用裁剪过的裸链** `https://www.xiaohongshu.com/discovery/item/{id}`——小红书强制校验 token,裸链会被拦截,点击跳转报「当前笔记无法浏览」或被甩到登录页。

## 三种链接

| 写法 | 能不能跳 |
|---|---|
| ✅ 完整分享链 `.../item/{id}?...&xsec_token=...&xsec_source=pc_share`(电脑端「分享」获得) | 能 |
| ✅ `http://xhslink.com/o/xxx`(App 分享 → 复制链接;token 内嵌,**最稳**) | 能 |
| ❌ 裸链 `https://www.xiaohongshu.com/discovery/item/{id}` | **不能** |

## 坑与规避

- **别为了"干净"截断链接**:归档 / 整理时手贱删掉 `?` 后面的参数,就把活链变成了死链。小红书链接的尾巴是功能性的,不是噪音。
- **token 有时效**:`xsec_token` 与部分 xhslink 短链可能过期失效。长期挂在**公开页面**的,优先用 App 复制的 xhslink 短链;失效就换新链重发。
- 自检:链接里有没有 `xsec_token=`?没有就是死链。

## 关联文档

- 平台发布:[[网易云音乐人发布SOP_v1]] · [[快手分发SOP_v1]] · [[小红书点赞与收藏陷阱]]
- 案例与配套 skill:`{AIGC工作站}/becoming-a-prompt-master`(画廊第 3 期外链修复);`prompt-master-series` 阶段 E 已写入此规则
