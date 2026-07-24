---
tags: [类型/平台工程, 主题/字体]
---
# 导出运行时无系统字体回退律 · CJK 豆腐块 v1

> 入档:2026-07-24
> 来源:LastStand(Godot 4.7 FPS)Web 导出验证 —— 设置界面档位值中文全变豆腐块,桌面版一切正常
> 验证状态:✅ 已定位并修复(改字体回退后 Web 端中文恢复)
> 性质:导出/嵌入式运行时的字体坑,跨引擎通用(Godot Web/移动、任何 WASM/无系统字体沙箱)

---

## 一句话律

**桌面端会用操作系统字体自动补全字体里缺失的字形,导出到 Web/移动/嵌入式运行时后没有系统字体可借,凡是用「不含目标字形的字体」渲染的文本一律变豆腐块(□)。** 跨字体、跨语言的项目必须给每个「主力字体」显式挂 `fallbacks`,把桌面那份隐式 OS 回退**固化进导出**——桌面测不出来,只有到目标运行时才现形。

---

## 踩坑现场

LastStand 首次 Web 验证导出,进游戏 → 设置 → DISPLAY:

- **左侧标签**(显示模式 / 分辨率 / 垂直同步 / 帧率限制)—— 正常
- **右侧红框里的值**(窗口 / 全屏 / 无边框、关闭 / 启用、无限制……)—— 全是豆腐块 □□□□

桌面版这些值中文完全正常,只有 Web 出问题。

根因:值由 `CustomCycleButton` 用 `draw_string(font, …)` 绘制,其 `font` 硬编码为 **JetBrains Mono**(纯拉丁等宽,无 CJK 字形)。标签用的是 NotoSansSC(自带中文)所以没事。

**为什么桌面看不出来**:Godot 桌面端 TextServer 找不到字形时会**回退到操作系统字体**(Windows 有一大堆中文字体),悄悄把「窗口」画出来了。Web 导出的运行时**没有任何系统字体**可借,回退链一空,直接吐豆腐。这层 OS 回退是隐式的、不进包的,所以桌面自测**永远测不出这个 bug**。

---

## 修法:把隐式 OS 回退固化成显式 fallbacks

给每个可能用来画非本字符集文本的「主力字体」显式挂 fallback。LastStand 的做法——4 个拉丁 FontVariation(JBMono ×2、Oswald ×2)各加一条 NotoSansSC 回退:

```
[gd_resource type="FontVariation" load_steps=3 format=3]
[ext_resource type="FontFile" path="res://assets/fonts/JetBrainsMono-VF.ttf" id="1_ttf"]
[ext_resource type="FontFile" path="res://assets/fonts/NotoSansSC-VF.ttf" id="2_noto"]
[resource]
base_font = ExtResource("1_ttf")
fallbacks = Array[Font]([ExtResource("2_noto")])
variation_opentype = { "wght": 500 }
```

要点:

- **在拉丁字体上挂 CJK 回退**(而非反过来):拉丁字体负责数字/百分号的等宽观感,遇到中文自动落到 Noto,视觉设计不变。
- **一次改全局主力字体,不要逐控件修**:病在字体资源层,改 4 个 `.tres` 就覆盖了全游戏所有「拉丁字体画中文」的地方,比一个个界面补更稳。
- **零体积代价**:回退字体(NotoSansSC)本就因别处在用已打进包,`fallbacks` 只是加个引用,pck 只涨了 0.5KB。前提是回退字体已在导出资源里——若是新引入的大 CJK 字体,记得配子集控体积。

---

## 配套坑(同场次)

同一次 Godot Web 导出还踩了两个,一并记:

1. **headless `--export` 的 "configuration errors" 不吐细节** —— 命令行只报「因配置错误无法导出」,不说缺什么。我据此手搓猜了半天「preset 字段不全」,全错。**真相是编辑器 GUI 一打开就逐条红字点破**(此处是「目标平台需要 ETC2/ASTC 纹理压缩」)。教训:**卡在笼统配置错误时,别在 headless 里猜字段,开一次编辑器 GUI 是最快的诊断器**。参见 [[交付前实测证伪律_v1]] 的反面——我把「诊断不足」当成了「结论确定」。
2. **Web/Compatibility 渲染要求纹理 ETC2/ASTC 压缩** —— 项目需开 `textures/vram_compression/import_etc2_astc=true`,会给每张贴图再存一份 ETC2 变体(与桌面 s3tc 并存)。这是上面那条笼统报错的实际内容。

---

## 如何使用 / 判断

出现「桌面正常、导出后部分文字变豆腐块」时,先怀疑**字体缺字形 + 运行时无系统回退**,而不是编码/乱码:

- 症状特征:**同一界面有的文字正常、有的豆腐**——正常的那些用了含字形的字体,豆腐的用了缺字形的字体(常是等宽/标题类拉丁字体拿去画了中文)。
- 适用范围不止 Godot:任何「桌面/编辑器有系统字体兜底、目标端没有」的场景都会中招(WASM、嵌入式、精简容器、无 fontconfig 的 Linux 镜像)。
- 修的方向永远是「**把兜底显式化并打进产物**」,不是「换一种编码」。

---

## 关联文档

- 字形家族姊妹律:[[emoji字形版本兼容律_v1]](字形随平台/版本缺失)· [[CJK假斜体语言感知律_v1]](CJK 无真斜体)
- 所见非真相家族:[[Windows下编码与DPI的所见非真相]] —— 同样是「本机环境悄悄替你做了事,换环境就露馅」
- 诊断心法:[[交付前实测证伪律_v1]] · [[变通方案不等于故障点_v1]] —— headless 笼统报错别当定论,换更强工具复现
- 同线工程(LastStand→Toy):[[B站Toy同步事故复盘_版本指纹与外部cron兜底_v1]]
- 库外底料(裸路径):`E:\last-stand` commit `511184d`(字体回退)+ `9a46d7f`(Web preset)· `assets/fonts/font_*.tres`

---

## 版本

- v1(2026-07-24):首次入档,基于 LastStand Web 验证导出的豆腐块定位与修复。
