---
tags: [类型/平台工程]
---
# Claude 预览环境不派发滚动事件 · 滚动类功能无法行为验证

> 入档:2026-06-25 · 补充:2026-06-26(动画时钟冻结) · 2026-07-16(交互面板 rAF=0/Konva hit 图/合成双击)
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

## 补充(2026-06-26):预览还会「冻结动画时钟」,动效同样无法直接观测

给 taowhale 首页主图做流动动效时再次撞到同类边界,且更狠:**预览 iframe 会暂停渲染时钟**——

- **CSS 动画 / SMIL / `requestAnimationFrame` 全部不推进**:`@keyframes` 不走、SVG `<animate>` 不走、自己挂的 rAF 回调一帧都不跑(靠 rAF 设 CSS 变量的鼠标互动也因此「看不到」)。
- **设了内联值 `getComputedStyle` 也可能不回填**:页面进入冻结态后,`el.style.setProperty('--x', ...)` 再读 computed 拿不到新值(初次渲染的静态值才读得到)。
- 叠加旧结论:截图对持续 rAF 动画页**超时**——所以动效页**截图、computed 采样、肉眼**三条路在预览里都断了。

**替代验证法:不靠时钟自动走,手动把时钟推到指定时刻再采样**——

1. **CSS 动画 / WAAPI**:`el.getAnimations()[0]` 拿到动画对象,**直接写 `anim.currentTime = t`**,再 `getComputedStyle` 读被驱动的属性。例:验证流光位移 → 设 `currentTime` 到 0/25%/50%/75%,读 `background-position` 是否线性插值(证明会动)。
2. **SVG SMIL**:根 `<svg>.setCurrentTime(t)`,再读被动画属性的 `.animVal`。例:验证 `feTurbulence` 流动 → `setCurrentTime(0/5.5/11)` 读 `feTurbulence.baseFrequencyX.animVal` 是否随时间演化。
3. **静态合成预览**:动效的「单帧观感」可在本地用 Python/PIL 合成一帧(把遮罩 / 光层 / 位移近似画出来)肉眼看,判断强弱是否过曝/过碎——运动靠①②证明,观感靠合成图。
4. **真机最后一眼**:动效是否「好看 / 速度合适」终究要真机刷新确认;预览只能证明「接线对、会动」。

> 教训叠加:**预览能证明「结构对、会动(逐帧采样)」,但证明不了「观感对」**。动效类需求,把「逻辑/接线」验证(预览)与「观感/手感」验证(真机)分开,别指望在预览里调参数。

## 补充(2026-06-26):又一次验证 + 桌面侧新盲区(computer-use 遮蔽绿色 exe)

给 desk-pond 展示页做**滚动联动水波**(往下滚每隔一段荡开一圈)时第三次撞到本律:`scrollTo` 后 `scrollY` 变了但绑的 `scroll` 回调里的 rAF 一帧不跑,**触发链无法在预览里验证**;只能用 `eval` 手动跑一遍 `spawn()` 证明「元素创建 + `el.animate()` 在 running(`playState`)」——即「接线对、会动」,触发那一下留真机抽测。完全复用上面的分层验证法。

同期还撞到一个**不同工具的同类边界**:computer-use 截图会**遮蔽不在授权清单里的应用窗口**,而便携版 .exe(绿色程序、不在开始菜单)无法被 `request_access` 解析 → **运行中的桌面应用 UI 根本截不到**。所以桌面应用的「图标/界面观感」既不能 headless 验、也不能截图验,**只能靠离线合成预览(PIL 出真实尺寸图) + 用户真机肉眼终验**。

> 母题再确认:**「观感对」永远要真机/人眼终验**——无论拦路的是预览 iframe(冻结时钟)、还是 computer-use(遮蔽未授权窗口)。交付时把这条盲区**显式写出来**让用户终验,别默认没问题。

## 补充(2026-07-16):可交互 Browser 面板同样 rAF=0——Konva 全家(动画/hit 图/双击)连环失灵 + 无头 Chrome 退级法

给 LibreCanvas(Konva 画布应用)做验证时,在**可交互的 Browser 面板**(非预览 iframe,能点能截图那个)实测 `requestAnimationFrame` **每秒触发 0 次**(离屏渲染器按需出帧),引发三连:

- **Konva.Animation 一帧不跑**:视频卡逐帧重绘、呼吸辉光动效全部无法观测(逻辑正确也看不到动)。
- **Konva hit 图延迟绘制不执行**:`stage.getIntersection()` 全画布返回 null、hover/onClick 全部失灵——手动 `layer.drawHit()` 后立刻恢复。**派生收益:把产品逻辑里"依赖 hit 图"的判定改成几何包围盒,测试路障逼出了更稳的实现。**
- **合成事件两个坑**:Konva 9 默认听 mouse 事件,派发 PointerEvent 无效;`clickCount:2`(0ms 间隔)的机械双击不被认作 dblclick,**两次 click 间隔 ≥100ms 才触发**——"自动化测不出双击"是工具问题不是代码问题。

同机还撞到一个**独立环境坑**:VM 里用户真实 Chrome 的媒体管线全坏——任何来源(http/blob/data)的 video 都 readyState=0 超时,但 `canPlayType` 照样回答 "probably"。**canPlayType 会撒谎,它查的是解码器注册表不是管线健康。**

**退级验证法(已产线化,三层)**:
1. **逻辑层**:dev 构建暴露 `window.__lc = {stage, store}`(仅 `import.meta.env.DEV`),直接断言 store 状态与纯函数;
2. **交互层**:`puppeteer-core` 驱动本机已装 Chrome 无头实例(免下载浏览器)——**真 rAF、可信鼠标事件、page.mouse 拖拽**,Konva 动画采样(两次 shadowBlur 不等=在动)、吸附拖拽、双击(两次 click 加间隔)全部可端到端断言;
3. **观感层**:同一无头实例 `page.screenshot` 落盘,Read 进上下文人眼看(顺带产出 README 配图)。

> 母题第 N 次确认:环境限制清单每多一条,分层验证法就多一层退路——先判环境,再改代码。

## 选型建议

- 滚动监听优先 `document.addEventListener('scroll', fn, {capture:true, passive:true})` + rAF 节流 + `getBoundingClientRect` 判定——**跨滚动容器可靠**(window 滚动事件在容器化布局里也可能不冒到 window)。
- 别因为「预览里没高亮」就反复改代码:先确认是不是**环境不派发事件**(用上面的 probe 一测便知),否则会把好代码改坏。

## 教训(可复用)

- **「预览里没反应」≠「代码错」**。工具环境的能力边界本身要先验证。—— 又一例「所见非真相」:预览所见 ≠ 真机所见。
- 验证策略要**分层**:能行为验证就行为验证;不能,就退到「验证纯逻辑 + 信任标准 API + 真机抽测」。

## 关联文档

- [[双部署目标的base路径陷阱_根路径拼出双斜杠_v1]] —— 同期同站,「只在一个镜像现形」的另一类验证陷阱
- [[浏览器插件自动化的能力边界_v1]] —— 同样是「先认清自动化工具的能力边界」这一母题
- [[网页主图logo流动动效迭代_液态变形与碎裂问题_v1]] —— 本条「动画时钟冻结」补充的来源案例;其动效迭代与碎裂问题的完整复盘
- [[桌面应用打磨发布闭环复盘_工位池塘v0.5.0_v1]] —— 2026-06-26 补充的来源案例(滚动水波再验 + 桌面 exe 截图盲区)
- [[每日定时任务自动更新内容板块_首次自动化生产落地_v1]] —— 同族再验:preview_screenshot 超时,退级 DOM 快照 + inspect 完成验证
- [[BeatTapper卡点标记器说明]] —— 同族再验(2026-07-02):后台页 visibilityState=hidden 时 rAF 完全冻结,时间显示/回放动效无法行为验证;退级 preview_eval 驱动状态机 + 合成已知答案的测试音频断言算法精度
- [[2026-07-16_LibreCanvas开源画布_单日十版从立项到v1.4复盘_v1]] —— 2026-07-16 补充的来源案例;交互面板 rAF=0 三连坑 + puppeteer 无头 Chrome 三层退级法的完整项目背景
- [[2026-07-20_朱元璋K线人生_历史可视化迭代复盘_v1]] —— 2026-07-20 再验证：动画观感需结合逻辑检查、作者真机反馈、生产构建和线上探测分层收口。
- [[文档密集页两栏排版与对外截图脱敏_v1]] —— 正向复用:本篇的无头 Chrome 退级手段,反过来是**静态版式自检**的强项(不依赖滚动/动画时钟,一张 `--screenshot` 即可定性)
