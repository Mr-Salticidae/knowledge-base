---
tags: [类型/平台工程]
---
# Claude 预览环境不派发滚动事件 · 滚动类功能无法行为验证

> 入档:2026-06-25
> 来源:给蛛网之上首页做左侧浮动版块索引(滚动高亮当前版块),想在 Claude Preview 里验证 scroll-spy
> 状态:确认是预览环境硬限制(非代码 bug),已找到可靠替代验证法

## 一句话总结

Claude Preview 的预览 iframe **根本不向页面派发 `scroll` 事件**——`window` / `document`、冒泡 / 捕获**全部 0 次**,连 `IntersectionObserver` 回调也 **0 次**,**即便 `window.scrollY` 确实发生了变化**(`scrollIntoView` / `scrollTo` 能滚,但不触发事件)。所以一切「**滚动时才发生**」的逻辑(scroll-spy 高亮、滚动懒加载、滚动动画、无限加载)在预览里**无法行为验证**。另外预览**截图对持续 rAF 动画页(如 canvas 粒子背景)会超时**。

## 实测证据

- 自挂 `window.addEventListener('scroll', probe)` → `scrollTo(2000)` 后 `scrollY` 变了,但 `probe` 触发 **0 次**。
- 自挂 `IntersectionObserver` observe 一个 section → 大幅滚动后回调 **0 次**。
- 捕获阶段 `document.addEventListener('scroll', fn, {capture:true})` → 同样 **0 次**。
- 结论:不是监听挂错位置/相位,是这个环境的滚动**根本不走事件派发**。

## 替代验证法(绕过环境限制)

1. **验证「判定公式」而非「触发」**:把"当前版块"的计算抽成纯函数,用 `eval` **在多个已知滚动位置手动调用它**,逐一比对返回值是否正确。
   - 例:`scrollIntoView(各 section)` 后调用 `compute()`,确认返回「首页/可玩/视觉系统/skill存档…」逐一对。触发器在真机必然生效,公式对了就够。
2. **DOM 状态验证替代截图**:`naturalWidth>0 && complete` 验图片真加载、`getBoundingClientRect` 验布局不重叠、`getComputedStyle` 验样式值——比截图可靠且不超时。
3. **真机最后一眼**:滚动高亮这类「触发依赖」的,留一句话请用户在真实浏览器扫一眼确认。标准 API(capture 阶段 document scroll)在所有真实浏览器必然工作。

## 选型建议

- 滚动监听优先 `document.addEventListener('scroll', fn, {capture:true, passive:true})` + rAF 节流 + `getBoundingClientRect` 判定——**跨滚动容器可靠**(window 滚动事件在容器化布局里也可能不冒到 window)。
- 别因为「预览里没高亮」就反复改代码:先确认是不是**环境不派发事件**(用上面的 probe 一测便知),否则会把好代码改坏。

## 教训(可复用)

- **「预览里没反应」≠「代码错」**。工具环境的能力边界本身要先验证。—— 又一例「所见非真相」:预览所见 ≠ 真机所见。
- 验证策略要**分层**:能行为验证就行为验证;不能,就退到「验证纯逻辑 + 信任标准 API + 真机抽测」。

## 关联文档

- [[双部署目标的base路径陷阱_根路径拼出双斜杠_v1]] —— 同期同站,「只在一个镜像现形」的另一类验证陷阱
- [[浏览器插件自动化的能力边界_v1]] —— 同样是「先认清自动化工具的能力边界」这一母题
