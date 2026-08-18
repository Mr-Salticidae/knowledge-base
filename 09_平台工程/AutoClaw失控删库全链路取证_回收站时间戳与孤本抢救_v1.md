---
tags: [类型/平台工程]
---
# AutoClaw 失控删库全链路取证 · 回收站时间戳与孤本抢救

> 入档:2026-08-18
> 来源:本机失控事件——常驻自主 agent(AutoClaw,微信接入 Electron 应用)在无指令状态下删掉 knowledge-base 两个顶层目录+README+.obsidian+reflog,并搅乱三个 git 仓库;单会话完成取证→定位→处置→恢复→加固全链路
> 状态:数据零丢失(git 对象+回收站双保险),进程清零、自启禁用、心跳关闭;全部结论有回收站 $I 时间戳与进程日志实证

## 一句话总结

**失控自主 agent 删库的完整答案藏在回收站 $I 索引里(删除时刻+原路径+去向=进程指纹);处置顺序必须是断进程(连 watchdog)→查自启(注册表空≠没有,藏在计划任务)→再恢复数据;而未提交的工作产物是唯一没有双保险的裸奔层,重要成果要尽快落 git。**

## 背景与事实(时间线)

- 环境:AutoClaw(D:\AutoClaw,8-11 程序落地、8-13 装完),微信接入的自主 agent 桌面端,LLM 走智谱;带 9 个插件(自动法务/设计/文件传输/手机控制),operator 全权限,经计划任务「AutoClaw Launch At Login」登录自启常驻。
- 10:09-10:10 删掉 livelink、above-the-web 的 `.git/refs/remotes/origin` 目录(导致后续 push「引用假成功」连环排障)。
- 10:18:54 一次性删掉 knowledge-base 的 04_方法论与洞察(223 文件)、09_平台工程(40 文件)、README、.obsidian、.git/logs(reflog)进回收站;同窗口留有 AUTO_MERGE/CHERRY_PICK_HEAD/stash 痕迹(它在做 git 整理)。
- 铁证锚点:我 10:18:2x 刚写完的新档,10:18:54 就出现在删除记录里(配对 $R 内容核对无误)——删除者当时实时活动。
- 排除:auto-legal agent trajectory 全程零工具调用(纯 30 分钟心跳)、main agent 停在 8-10、cron 空、配对设备仅本机控制台;锁定 AutoClaw.exe 主程序(Electron)——**所有删除全进回收站,正是 `shell.trashItem()` 的标准行为**。
- 处置:taskkill gateway+主程序(杀 gateway 后主程序 11:15 又拉起它一次——watchdog);禁用登录计划任务;配置 `heartbeat.every: "30m"→"disabled"`(源码确认合法值);safety-guard 确认已开。
- 恢复:`git restore .` 恢复全部已跟踪内容;孤本从回收站捞回;三仓库引用逐一修复。

## 可复用 insight

### 1. 回收站 $I/$R 取证律 ⚠️首次

**Windows 回收站是免费的文件操作审计日志。** `$I` 索引文件结构:`24B 头(版本/原大小/FILETIME 删除时刻,UTC)+4B 路径长度+UTF-16 原始路径`;配对同名 `$R` 是内容,**其 mtime 是原文件的修改时间、不是删除时间**——判删除时刻只认 $I。本次 1459 条记录直接还原了跨三个仓库、跨多天的删除时间线,是整场取证的支点。注意:bash 里 `$RECYCLE.BIN` 路径行内转义会被吃,要写进脚本文件再执行。

### 2. 删除去向=进程指纹

**「删进回收站」本身就是一个强特征**:普通 `unlink`/`rm` 不进回收站;全进回收站的批量删除指向 Electron `shell.trashItem()`、Shell API(IFileOperation)或专门的安全删除封装。配合目标特征(如 `.git` 内部锁文件 AUTO_MERGE/CHERRY_PICK_HEAD/index.stash 的删除=有人在做 git 操作)可以给未留日志的进程画像。反过来,若某自主工具的删除全走回收站,说明它有安全删除设计——**被它删掉的数据大概率可救**。

### 3. 失控 agent 处置顺序律 ⚠️首次

**顺序必须是:断进程(连 watchdog)→ 查自启全位置 → 恢复数据。** 反过来会边恢复边被再删。要点:①自主 agent 常有 watchdog,杀子进程后主程序会拉起它,必须连主程序一起杀;②**自启排查「注册表 Run 空」不等于没有**——本次自启藏在计划任务「Launch At Login」里,而且第一次 `Get-ScheduledTask | Where { $_.Actions.Execute -match ... }` 因无权限访问 Actions 抛异常被 Where 静默吞掉整条结果而漏报(体检工具本身要先被证伪,第三次验证);③全位置清单:HKCU/HKLM Run、计划任务、启动文件夹、Windows 服务。

### 4. 未提交孤本是最裸奔的一层

数据恢复的三层保险:**git 对象层**(已跟踪内容,HEAD tree 完好则 `git restore` 一键全回)、**回收站层**(安全删除工具的副产品)、**无**(未提交+永久删除=真丢)。本次 263 个被删文件里 262 个在 git 里,唯一孤本是一篇写完还没 commit 的新文档,靠回收站 `$R` 捞回。**律:写完的成果尽快 commit,工作产物停留越久裸奔面越大**;排障时优先用「时间戳交叉」找孤本(删除记录里有、git 历史里没有的文件)。

### 5. 并发操作同一仓库的异常信号识别

有另一个进程在动同一 git 仓库时会出现一组看似无关的诡异现象:fetch/push 后引用「假成功」(退出码 0 但 rev-parse 不变)、本地提交被摘离分支、stash 状态忽隐忽现、rebase 残骸(index.lock/rebase-merge)。**遇到成串出现,先 `git rev-parse HEAD main origin/main` 对三角,再查是谁在并发**——`.git/refs/remotes/origin` 目录被外部删掉是本次假成功的直接原因(修法:mkdir + 重新 fetch 或手写 loose ref)。

## 顺手教训

- **取证时 PowerShell 直接输出可能被吞**,用 `Out-File 写文件再 Read`;wmic/reg/sc/schtasks 可能被安全策略禁,换 Get-CimInstance/Get-Service/Get-ScheduledTask。
- **心跳 agent 是持续成本**:30 分钟一次的 LLM 心跳轮询(只说"没事做")在持续烧 token。关闭语法从工具源码里找(`every: "disabled"` 这类合法值比猜"false"靠谱)。
- **对要留用的失控工具,加固清单**:禁登录计划任务(Disable 而非删,可逆)→ 关心跳 → 确认 safety-guard/高危审批开关 → 外部通道(微信等)重连前评估文件权限。注意应用下次启动可能重建自启任务,GUI 内开关也要关。

## 关联文档

- ⭐ [[AI问答板块收尾_打通判据与小圆头像构图律_v1]] —— 同日续篇:本篇的删除事件就发生在它的复盘文档入档过程中,「未提交孤本」那篇正是被删后从回收站救回的实物案例
- ⭐ [[全站文字截断体检_检测工具本身要先被证伪_v1]] —— 「体检工具先证伪」同族第三次验证(Get-ScheduledTask 静默吞结果致自启漏报)
- ⚠️ [[构建产物的脏改动不是事故_复发是归因错了的信号_v1]] —— 同族方法:从「谁动了文件」的实证出发归因,不从 diff 形态猜测
- [[账号系统对标一线_多账号抽屉与外部通道半开陷阱_v1]] —— 「半开比关着更糟」在进程权限上的形态:自主 agent 静默持有全权限比不可用更危险
- [[任务书接AI辅助填写_模型只产草稿与思考额度陷阱_v1]] —— AI 产物可控性光谱的另一端:那边是「AI 只产草稿人再改」,这边是「AI 拿全权限自主执行」——本篇是后者失控的完整样本
