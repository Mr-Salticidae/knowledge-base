---
tags: [类型/平台工程]
---
# LibTV：CLI 跑的 Seedance 样片，补网页元数据后转正片

> 入档：2026-10-05
> 来源：《余温》单元剧 EP03（[[2026-10-05_余温_单元剧EP03瓦尔卡_LibTV样片到正片_阶段复盘_v1]]）。5 个 CLI 样片节点补完元数据后都出现了按钮，其中 4 条已转正片成功
> 适用：LibTV 画布，`star-video2.5-draft`（Seedance 2.5 样片模式），样片由 libtv CLI 提交

## 一句话

正片 = 一次普通的 `star-video2.5` 生成：参数同样片，加 `draft: false`、`draftTaskId: <样片的 providerTaskId>`，分辨率 1080p。网页"生成正片 1080P"按钮做的就是这件事。

CLI 跑的样片没有这个按钮，是因为缺网页端出片时自动写入的两份元数据。补上以后，按钮就会出现。

## 为什么缺

网页客户端拿到样片任务结果后，会写两样东西，CLI 都不写：

1. **节点数据** `data.seedanceDraft = {sourceTaskId, startTimeMs, createdAtMs, outputs:[{resultIndex, url, providerTaskId}]}`。
2. **节点附加数据（node payload）** `seedanceDraft = {version:1, detail:{taskId, model, status, params, result, startTimeMs, createdAtMs}}`。

鼠标悬停到视频上时，页面会读第 2 份详情，构造正片请求，再调算价接口。算价成功，按钮才渲染。

还有一个坑：CLI 任务的服务端参数里，参考视频是 `asset://` 地址，**没有时长**。前端算价读不到时长就报"无法读取视频时长"，被吞掉不显示，按钮照样不出来。

## 怎么补

前提：Chrome 登录 liblib.tv，账号和 CLI 是同一个；样片在 7 天有效期内。下面的代码在画布页的控制台里跑（或用 Claude in Chrome 的 javascript 工具），**只调页面自己的函数和自带登录态的接口客户端，不碰令牌**。

**第 0 步，拿页面模块上下文**。用 Turbopack 注册一个探针模块，再让运行时实例化它：

```js
TURBOPACK.push(['static/chunks/probe.js', 990001, e => { window.__tp = e }]);
TURBOPACK.push(['static/chunks/probe-rt.js', {otherChunks: [], runtimeModuleIds: [990001]}]);
```

下面用到的模块编号是 2026-10-05 前端版本的，站点更新后可能会变。变了就到 script 里搜导出名，找新编号。

| 模块 | 导出 |
| --- | --- |
| 383924 | `apiClient` |
| 185990 | `default.canvasTaskGenerationDetail`，即 `/api/canvas/task/generation/detail` |
| 824544 | `resolveSeedanceDraftDetail` |
| 756016 | `getSeedanceDraftOutputs`、`findSeedanceDraftOutput`、`buildSeedanceFinalRequest`、`isSeedanceDraftFinalAvailable` |
| 292830 | `getNodePayload`、`mutateNodePayload`、`parseNodePayload` |
| 299750 | `calculatePower` |
| 666809 | `applyCreateAlignedParams` |
| 334336 | `getRateLimitBenefitStatus` |

**第 1 步，取任务详情**。用页面的 `apiClient` 读 `generation/detail?task_id=<样片任务号>`，返回体里的 `detail` 是 JSON 字符串。要取的字段：
- `providerTaskId`：在 `task_result.videos[0]` 里，形如 `cgt-20261005000948-zdejb`；
- `start_time`；
- `task_power`：这条实际扣了多少分。

**第 2 步，写入 payload 详情，并补参考视频时长**：

```js
const e = window.__tp;
await e.i(824544).resolveSeedanceDraftDetail({projectUuid, nodeKey, taskId, startTimeMs, isCurrent: () => true});
await e.i(292830).mutateNodePayload(projectUuid, nodeKey, p => {
  const sd = p.seedanceDraft, prm = {...sd.detail.params};
  const fix = x => String(x?.url || '').startsWith('asset://') ? {...x, durationSec: 30, duration: 30} : x;  // 30 = 白模参考视频的实际秒数
  prm.mixedList = prm.mixedList.map(x => x.type === 'video' ? fix(x) : x);
  prm.videoListV2 = (prm.videoListV2 || []).map(fix);
  return {...p, seedanceDraft: {...sd, detail: {...sd.detail, params: prm}}};
});
```

**第 3 步，写节点数据**。`outputs` 用 `getSeedanceDraftOutputs(detail.task_result)` 算，算出来的 `url` 和节点视频地址一致。用 CLI 写：

```bash
libtv node <样片节点名> -u 'seedanceDraft={"sourceTaskId":"<任务号>","startTimeMs":<毫秒>,"createdAtMs":<毫秒>,"outputs":[{"resultIndex":0,"url":"<节点视频url>","providerTaskId":"cgt-…"}]}'
```

项目里有现成脚本：`{aigc-creative-archive}/…/EP03_瓦尔卡/样片转正片_补元数据.py`。

**第 4 步，验证**。不用挪画布找节点，在页面里按悬停逻辑原样跑一遍，能算出价就说明按钮会出来：

```js
const det = pm.parseNodePayload((await pm.getNodePayload(proj, nk)).payload).seedanceDraft.detail;
const o = m.getSeedanceDraftOutputs(det.result)[0];
const req = e.i(666809).applyCreateAlignedParams(m.buildSeedanceFinalRequest(det, o.providerTaskId, nk, proj, undefined), e.i(334336).getRateLimitBenefitStatus());
(await e.i(299750).calculatePower(req)).data.power   // 1080P 30 秒应为 6600
```

**第 5 步，出正片**。刷新画布，鼠标移到样片视频上，右上角出现「生成正片 1080P ⚡6600」，点它。

- 页面会新建一个「正片 1080P: <样片名>」节点。
- 约 20 分钟出片。CLI 有时要几分钟才同步到任务号，以网页节点和余额为准。
- 下载命令：`libtv download -n "正片 1080P: <样片名>" -o <目录> --without-ai-watermark --vip`。
- 节点名里有冒号，Windows 下文件会被改成 `_`，下载后要改名。

## 如何使用

- **最省事的是从源头避免**：要出正片的样片，直接在网页端跑。或者开着画布页再用 CLI 跑，看客户端会不会自己写元数据——这个办法还没验证。
- 已经用 CLI 跑完的样片，按上面 5 步补，一次补多条也可以。
- 价格：1080P 30 秒正片算价 6,600，**实扣 6,600**；样片算价 1,200，实扣 600。别拿样片的折扣推正片。

## 关联文档

- 来源复盘：[[2026-10-05_余温_单元剧EP03瓦尔卡_LibTV样片到正片_阶段复盘_v1]]
- LibTV 接入：[[Claude桌面版接入LibTV远程MCP_临时电脑环境与会话重连_v1]]
- 模型行为：[[Seedance2_5_行为规律_v1]]
- 浏览器侧操作的边界：[[浏览器插件自动化的能力边界_v1]]
