---
tags: [类型/平台工程]
---
# reduced-motion 本机陷阱 · 动效降级纯淡入而非跳过

> 入档:2026-07-24
> 来源:蛛网之上首页「滚动渐现」动效上线后作者本机毫无变化的排查与修复(above-the-web `src/pages/index.astro`)
> 性质:⚠️ 二次踩坑升律。第一次见 [[网页主图logo流动动效迭代_液态变形与碎裂问题_v1]](2026-06-26,当时用 `!important` 定向豁免收场);本次给出更通用的「降级而非禁用」模式,单独立档。

## 一句话律

**Windows 关了「动画效果」的机器,所有浏览器都会全局上报 `prefers-reduced-motion: reduce`;网页动效对它的正确响应是「降级为纯淡入」,不是「整体跳过」——纯透明度渐变没有位移,不触发运动不适,规范允许。**

对本机开发者的推论:**你自己的机器就是 reduce 机时,凡是"严格尊重 reduce=跳过动画"的实现,你自测永远看不到效果**,会误判"改动没生效"。

## 原理

- Windows「动画效果」开关(设置 → 轻松使用/辅助功能 → 显示)对应系统参数 `SPI_GETCLIENTAREAANIMATION`。它是**系统级**的:一关,本机所有浏览器(含 headless Chrome)都向所有网页上报 `prefers-reduced-motion: reduce`。
- 这个偏好针对的是**位移/缩放/视差等"运动"**引发的前庭不适。纯 opacity 渐变不含运动,业界公认安全——所以"reduce=完全禁动画"是过度执行,正解是**降级阶梯**:
  1. 常规环境 → 完整动效(淡入 + 位移);
  2. reduce → 纯淡入(只动 opacity);
  3. 无 JS / 爬虫 → 不隐藏任何内容,全量静态可见(渐进增强底线)。

## 事故现场(两次)

| 次序 | 项目 | 现象 | 当时修法 |
|---|---|---|---|
| ① 2026-06-26 | 鲸海拾贝首页 logo 光效 | "太淡 + 看不到" | 氛围光效用 `!important` 从 reduce 定向豁免 |
| ② 2026-07-24 | 蛛网之上首页滚动渐现 | "我没有感觉到变化诶" | reduce 下降级纯淡入(本篇正解) |

两次的共同根因都不在代码,在**本机是 reduce 机**。第二次先查了部署、缓存、脚本执行,最后才用 PowerShell 查系统开关定性——下次遇到"动效本机看不到",**第一步就查这个**:

```powershell
$sig = '[DllImport("user32.dll")] public static extern bool SystemParametersInfo(uint uiAction, uint uiParam, ref bool pvParam, uint fWinIni);'
$t = Add-Type -MemberDefinition $sig -Name SPI -Namespace Win32 -PassThru
$anim = $false; [Win32.SPI]::SystemParametersInfo(0x1042, 0, [ref]$anim, 0) | Out-Null
"动画效果开启: $anim"   # False = 本机是 reduce 机
```

## 可复用成品:滚动渐现的完整实现模式

进入视口才淡入上移、同批错峰,四条硬要求全部满足(渐进增强 / reduce 降级 / 不抢 hover / 与筛选共存):

```css
/* 隐藏态只在 JS 挂上 html.rv-on 后生效 —— 无 JS / 爬虫全量可见 */
html.rv-on .rv { opacity: 0; }
html.rv-on .rv.rv-in { animation: rv-in .65s cubic-bezier(.2,.7,.3,1) both; }
@keyframes rv-in { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }
/* reduce:降级纯淡入,不是跳过 */
@media (prefers-reduced-motion: reduce) {
  html.rv-on .rv.rv-in { animation: rv-fade .5s ease both; }
}
@keyframes rv-fade { from { opacity: 0; } to { opacity: 1; } }
```

```js
if ('IntersectionObserver' in window) {          // 只守 IO,不守 reduce(reduce 交给 CSS 降级)
  const els = [...document.querySelectorAll('.sec-head, .card, /* … */')];
  document.documentElement.classList.add('rv-on');
  const settle = (el) => { el.classList.remove('rv','rv-in'); el.style.animationDelay = ''; };
  els.forEach((el) => { el.classList.add('rv');
    el.addEventListener('animationend', () => settle(el), { once: true }); });
  const io = new IntersectionObserver((entries) => {
    let batch = 0;
    for (const en of entries) {
      if (!en.isIntersecting) continue;
      io.unobserve(en.target);
      const delay = Math.min(batch++ * 70, 350);          // 同批错峰
      en.target.style.animationDelay = delay + 'ms';
      en.target.classList.add('rv-in');
      setTimeout(() => settle(en.target), delay + 900);   // animationend 兜底
    }
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
  els.forEach((el) => io.observe(el));
}
```

设计要点(为什么这么写):

- **动画用 keyframes 而非 transition**:卡片自身往往已有 `transition: transform …` 的 hover 动效,渐现若也走 transition 会互相覆盖。
- **动画结束即摘类(settle)**:`animation … both` 的填充态会一直压住 transform,不摘类的话 hover 上浮从此失灵。`animationend` + 超时双保险(动画中途被 `display:none` 打断时 animationend 不触发)。
- **隐藏态挂在 `html.rv-on` 之下**:JS 没跑,类就不存在,内容不会被藏起——SEO / 无障碍 / 弱网的底线。
- **与筛选类功能天然兼容**:被筛选藏起的元素 IO 不触发,重新展示后进入视口照常渐现。

## 验证方法(headless Chrome 三坑)

1. **不加参数的 headless 测到的就是本机真实路径**:本机是 reduce 机时,headless 也上报 reduce——第一次看到"没触发"别急着断定代码坏了,先想想在测哪条路径。
2. **强制关 reduce 的参数是** `--blink-settings=prefersReducedMotion=false`。注意 `--force-prefers-reduced-motion` 只能强制**开**,给它拼 `=no-preference` 无效(实测仍是 reduce)。
3. **统计口径两坑**:
   - `--virtual-time-budget` 会把虚拟时间快进——动画早已放完、settle 早已摘类,元素既不在"待触发"也不带 `rv-in`,数错口径会误判"没生效"(其实是"已生效并清理完毕",要数**被还原成原始 class** 的元素);
   - 构建器(如 Astro)会把 `<style>` 抽进外部 `/_astro/*.css`——**grep 线上 HTML 验证 CSS 关键字会永远 0 命中**,要先从 HTML 里摘出样式表 URL 再 curl 那个文件。

## 举一反三

- 任何"效果类"改动上线后作者说"没变化",排查顺序:**① 本机偏好/环境开关 → ② 缓存 → ③ 部署产物 → ④ 代码**。第①步最便宜,却最容易被跳到最后。
- reduce 降级阶梯可迁移到一切动效:视差 → 静态、轮播自动播放 → 手动、骨架屏脉冲 → 静态占位。原则一致:**去掉运动,保留信息层级的过渡**。

## 关联文档

- [[网页主图logo流动动效迭代_液态变形与碎裂问题_v1]] —— 同根因第一次现形(logo 光效"看不到");其「`!important` 定向豁免」适合轻微氛围光,本篇「纯淡入降级」适合内容渐现,两法并存按场景选
- [[Claude预览环境不派发滚动事件_滚动类功能无法行为验证_v1]] —— 同族验证陷阱:预览环境不派发 scroll/IO;本篇的 headless Chrome + 强制关 reduce + 高视口 dump,是滚动渐现类功能的又一条可行验证退级路
- [[双部署目标的base路径陷阱_根路径拼出双斜杠_v1]] —— 同站同族:「验证方式选错会误判部署失败」(那篇是只在一个镜像现形,本篇是 grep HTML 验 CSS 永远 0 命中)
- [[09_平台工程索引]] —— 平台工程区入口
