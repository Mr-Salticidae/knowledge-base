---
tags: [类型/prompt模板]
---
# MJ V7/V8 审核避雷词表

> 首次沉淀:2026-05-01(02 教程基准图实测触发)
> 入档:2026-05-02
> 主线作品来源:`02_角色一致性锚点/02_角色卡.md`

---

## 一句话总结

**MJ 审核会拦截"真实风格人像 + 年轻女性"的特定组合**——记下 7 大类雷词 + 1 个过审神器。

---

## 如何使用

写人像 prompt 之前 sanity check:
1. 是否含"young / girl / age 数字"等年龄敏感词?
2. 是否含"parted lips / wet / moisture / cherry lips"等被算作"暗示性"的词?
3. 是否含"translucent skin"等触发"透视"语义的词?
4. 是否包了 "fashion editorial / artistic portraiture / vogue editorial" 等过审神器?

**防被拦原则**:把 prompt 包装成"时尚 / 艺术摄影"语境,描述焦点放在**衣物、氛围、光线、构图**而不是身体。

---

## 7 大类雷词 + 安全替代

| 类别 | 雷词 | 安全替代 |
|---|---|---|
| **人物指代** | `girl`, `teen`, `young girl` | `woman`, `lady`, `subject` |
| **年龄** | `around 20 years old`, `young` | 不写年龄 / `youthful` |
| **嘴唇** | `parted lips`, `cherry lips`, `lips slightly open`, `pouty lips` | `soft lips`, `pale rose lips` |
| **皮肤** | `translucent skin`, `wet skin`, `glossy skin`, `bare skin` | `luminous skin`, `porcelain skin`, `fair skin` |
| **眼神** | `wet eyes`, `moisture`, `tearful` | `dewy gaze`, `contemplative gaze`, `misty gaze` |
| **身体** | `slim waist`, `curves`, 任何具体体型描述 | 完全不写体型 |
| **氛围词** | `seductive`, `sensual`, `intimate`, `vulnerable` | `aloof`, `ethereal`, `melancholic`, `literary` |

---

## 过审神器(加在 prompt 末尾)

```
fashion editorial, vogue style, artistic portraiture,
museum quality, cinematic still, fine art photography
```

**作用**:把图归类到"时尚/艺术摄影",而不是"真人照片"。**实测过审率显著提升**。

---

## 实测案例(02 基准图触发与修复)

### V1(被拦截)
```
a young east asian girl, around 20 years old,
porcelain pale skin with translucent quality,
melancholic gaze with subtle moisture,
cherry-shaped lips with matte nude-pink color, slightly parted,
...
```
报错:`Sorry! The AI Moderator is unsure about this prompt.`

触发雷词:
- `young...girl, around 20 years old`(年龄+girl)
- `lips slightly parted`(微张唇)
- `melancholic gaze with subtle moisture`(湿润眼神)
- `translucent (skin)`(透视语义)
- `cherry-shaped lips`(性化暗示组合)

### V2(过审 + 加强版)
```
fashion editorial portrait of an east asian woman,
luminous porcelain fair skin,
contemplative melancholic gaze,
soft pale rose lips with matte finish,
...
artistic portraiture, vogue china editorial style
```
全部雷词替换 + 末尾加过审神器 = 通过 ✅

---

## 一个 east asian woman 隐藏调参

不要写 `chinese girl`,**用 `east asian woman`**。

理由:`chinese girl` 在 MJ 训练集里关联到"网红甜妹脸 / 老照片东方美人",而 `east asian woman` 关联到"现代摄影下的东方面孔",**质感更高**。

这是个写在公开教程里都没人讲的隐藏调参,跳蛛先生今日实测验证。

---

## 金句段落(可直接用于内容创作)

> *"MJ 审核给你的不是'要不要写'的限制,而是'换个语境怎么写'的训练。先用艺术语境过审,再用场景层次找回灵魂——避雷和惊艳可以同时拥有。"*

> *"我让 MJ 画'裸粉唇',它画出来了。我再让它描述这张图,它说这是'红唇'。同一个 AI,写作时和阅读时,是两种语言。"*

---

## 关联文档

- 关联模板:[[角色锁定段_檐下28岁成熟版]](待写,完整成熟版 prompt 模板)
- 应用案例:`{AIGC工作站}/02_角色一致性锚点\02_角色卡.md`(V1→V2→V3 完整迭代)
- 关联方法论:AI 写作语言 vs 阅读语言(待重新沉淀) · [[AI甜妹脸vs复古东方美人]]
- 隐形雷区:[[负面词计入prompt浓度_v1]](`--no` 里的人体/脸词照样推高浓度,会反噬过审)
- 配套基础句:[[MUJI极简插画基础句]](插画风格的避雷扩展)
