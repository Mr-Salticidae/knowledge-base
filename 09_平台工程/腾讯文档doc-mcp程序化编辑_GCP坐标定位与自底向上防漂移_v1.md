---
tags: [类型/平台工程, 主题/腾讯文档]
---
# 腾讯文档 doc-mcp 程序化编辑 · GCP 坐标定位与自底向上防漂移

> 入档：2026-09-08
> 来源：《屏幕录制标准》v1.1→v1.2 全程程序化更新（version 10→26，5 组改动 + 变更记录插行 + 三行删除），零手工介入编辑器，三次全量回读校验
> 状态：产线验证可用

## 一句话总结

**腾讯文档 doc-mcp 的编辑不是"改文档"是"改坐标"：find 拿 GCP 坐标 → replace_text / insert_text 精确落刀，多处修改自底向上排序防坐标漂移，表格行号 0-based，每刀之后 find 复验。这套流程与钉钉 dws 块级编辑同构（见 [[dws块级插入_index语义陷阱与倒序插入法_v1]]），但坐标系从 block id 换成了全文 UTF-16 字符偏移——没有稳定锚点，排序与复验就是全部的安全网。**

## 操作要点（实测 tencent-docs-plugin 5.5.3）

1. **入口**：`python tencentdocs.py tdoc_call doc-mcp <tool> '<json>'`；调用任何工具前 `tdoc_schema <service> <tool>` 查参数定义，严禁凭记忆拼参
2. **定位**：`find` 按文本拿 range（begin/end，UTF-16 坐标），表格内文本同样可定位；`resolve_document_structure` 传 idx 拿单块结构（表格给 table_id、行列数、每格坐标）
3. **防漂移**：多处编辑**自底向上**（坐标降序）执行——每刀只作废变点之后的坐标，降序保证所有待改坐标落刀时仍有效；升序改则每刀之后都要重新 find
4. **表格**：`insert_rows` / `delete_table_row` 行号 **0-based**（⚠️ delete_table_row 工具描述写「1-based」是错的，以参数 schema 为准；散文描述与 schema 冲突时信 schema）。破坏性操作先删一行 → 回读 `get_table_info` 验证语义 → 再批量。`insert_rows` 支持 cells 三元组（insert_index / offset / cross_pos）插入即填内容，一次调用完成
5. **追加**：`insert_text` 可落在表格单元格内指定位置，返回 `last_index` 供链式追加
6. **校验**：`replace_text` 的 end 少算 1 字符会留残字（本次「发挥挥」事故），**每刀之后 find 目标文本复验**；收尾 `get_content` 全量回读——回包是双层 JSON：`result.content[0].text` 再 `json.loads` 取 `content` 字段
7. **变更管理**：规范类文档改内容必须同步登记版本行 + 变更记录表（新行插表头之下保持新→旧排序），对外公告与文档口径同轮收口，不留两个真相源

## 边界

- GCP 坐标含结构占位（段落结束符、表格、图片等），**不能按肉眼字符数手算**，必须 find / resolve_document_structure 取
- `paragraph_id` 不跨 editor 实例，本轮拿到本轮用，重开文档必须重新解析
- 本篇是「内容级编辑」（改字、插行）；块级结构大改（钉钉 adoc 场景）仍走 [[dws块级插入_index语义陷阱与倒序插入法_v1]] 那套

相关：[[2026-09-08_WorkBuddy录屏公告与录制标准v1.2_协作复盘_v1]]（本篇的实战出处）、[[录屏假光标被打回_画出来的不算操作与输入送达四处假信号_v1]]（同域：教程录屏的另一半坑）

---

## 关联文档

- [[2026-09-08_WorkBuddy录屏公告与录制标准v1.2_协作复盘_v1]] —— 实战出处与协作层规律
- [[dws块级插入_index语义陷阱与倒序插入法_v1]] —— 同族坐标防漂移（钉钉侧）
- [[录屏假光标被打回_画出来的不算操作与输入送达四处假信号_v1]] —— 教程录屏域
- [[钉钉知识库交付_格式白名单与终版回填闭环_v1]] —— 在线文档交付闭环的另一形态
