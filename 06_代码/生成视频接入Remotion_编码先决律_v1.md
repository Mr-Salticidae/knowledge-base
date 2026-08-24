---
tags: [类型/代码, 主题/图生视频, 主题/Remotion]
---

# 生成视频接入 Remotion 编码先决律 · v1

> 入档:2026-08-24 | 来源:《擦干净》动态化阶段(v3 渲染崩溃根因)
> 关联案例:[[2026-08-24_擦干净_从素材到动态化制片_全链路复盘_v1]]

## 一句话律

**生成式视频工具(即梦/Seedance 等)的输出若为 h264 High profile 或内嵌音频流,接入 Remotion 剪辑工程必报 `PIPELINE_ERROR_DECODE`;接入前必须重编码为 baseline profile + yuv420p + 去音频流 + ASCII 文件名。**

## 原理

- Remotion 用 Chromium 播放 `<Video>`,Chromium 对 h264 High profile 的解码支持在打包环境不稳定(尤其带 AAC 音频流的 mp4),失败报 Code 3 解码错误
- 文件名含中文时 staticFile 走 URL 编码,增加二次故障面
- 视频内嵌音频流与工程混音层(Remotion Audio)重复,且是解码失败的常见诱因

## 操作规则

1. 下载生成视频后**先 `ffprobe` 预检**:`codec_name / profile / pix_fmt / 音频流`
2. 统一标准化:
   ```
   ffmpeg -i in.mp4 -an -c:v libx264 -profile:v baseline -level 3.0 -pix_fmt yuv420p -r 24 -crf 20 -preset fast out.mp4
   ```
3. 文件名 ASCII 化(如 s31.mp4)
4. 视频素材一律不带音频(混音由工程声音层负责)
5. **验收以渲染为准**:Remotion Studio 手动预览正常 ≠ 渲染正常,必须跑一帧 render still 或主线性 render 首段验证

## 反例/边界

- 若项目在所有视频已标准化的前提下仍出现解码错误,优先检查:像素格式(必须 yuv420p)、帧率异常、文件下载不完整
- Chromium 不支持硬解的场合(某些 Linux 打包镜像)同样适用本律;桌面 Windows + Chrome 也受此约束(实测命中)
