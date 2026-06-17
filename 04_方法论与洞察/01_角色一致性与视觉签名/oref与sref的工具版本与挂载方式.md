---
tags: [类型/参数行为]
---
# oref / sref 的工具版本与挂载方式(MJ 实操约束)

> 沉淀:2026-06-17(项目 47 霜见,实操确认)
> 验证状态:⭐ 用户实操确认
> 适用:Midjourney 角色一致性工作流

---

## 三条硬约束

1. **oref 仅支持 v7**
   omni-reference(oref 锁脸)只在 `--v 7` 可用,**v8.1 不支持 oref**。要锁脸 → 整张切 v7。

2. **v7 没有 hd 模式**
   `--hd` 是 v8.1 的能力,v7 不能用。v7 出图 prompt 不要带 `--hd`。

3. **sref / oref 经 UI 点击挂载,不写进 prompt**
   在编辑器里**点击图片**把它设为 style reference(sref)或 character/omni reference(oref),权重也在 UI 调。
   **不要**在 prompt 正文写 `--sref <url>` / `--oref <url>`。

---

## 对 prompt 正文的影响

挂载交给 UI 后,prompt 正文只保留**描述 + 基础参数**:

```
[画面描述...] --ar 3:4 --v 7 --style raw --no text, watermark, logo, blurry
```

- 锁脸(oref-on):`--v 7`,UI 挂 oref(+ sref),无 hd。
- 不锁脸(oref-off / 仅 sref):可留 v8.1 + `--raw --hd`,sref 仍经 UI 挂(或按当前界面支持写法)。

## 决策速查

| 需求 | 版本 | 挂载 | 参数尾 |
|---|---|---|---|
| 锁脸(oref) | v7 | UI 点图挂 oref(+sref) | `--v 7 --style raw`,无 hd |
| 仅风格(sref) | v8.1 可 | UI 点图挂 sref | `--raw --hd` 可用 |

---

## 关联文档

- [[oref高方差律]](oref 高方差,抽卡+验收)
- [[角色一致性金字塔]] · [[sref纯净性原则]] · [[sref编号独立律]]
- 避雷:[[负面词计入prompt浓度_v1]]
