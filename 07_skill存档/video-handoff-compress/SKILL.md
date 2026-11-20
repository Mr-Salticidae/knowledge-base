---
name: video-handoff-compress
description: 手机录制视频的取片、压缩与回传交付工作流。当用户说「压缩手机里新录的视频」「传回手机，我要在手机端上传」「视频太大不好传」「上传前压一下」「把成品推到手机」，或源片是 HDR / 杜比视界 / HLG / HEVC 10bit 转发后发灰发暗、打不开时触发。含三层分离（色彩 / 兼容 / 体积）、先定目标体积再倒推码率、adb 取片与回传双校验。触发词：手机视频、压缩视频、传回手机、上传前压、HDR 发灰、杜比视界、视频太大、adb pull、adb push。
---

# Video Handoff · 手机视频压缩与回传交付

> **核心立场**：这不是「压一下」，是**三层分离 + 体积先定**。
> 色彩层（HDR→SDR）、兼容层（HEVC→H.264）、体积层（码率）各管一件事；体积是人的约束，必须由人先定，技术在后倒推。

## 何时使用

- 用户拿手机录了一段视频，要压小、要传、要在手机端上传
- 源是 HDR / 杜比视界 / HLG / HEVC 10bit，转发后发灰发暗或打不开
- 需要把本机成品推回手机供 App 上传

**不适用**：剪辑创作、封面、字幕、发布策略（走对应 skill）。已知目标体积的二次转码仍可用第 3–4 步。

---

## 五步流程

### 0 · 先问目标体积（不可跳过）

给 2–3 个可选项让人挑（如 180 MB / 120 MB / 100 MB），写清各自代价。**不要先压一版再问**——码率、分辨率、编码全由它倒推，选错整遍重来。用户已明确说过体积则跳过。

> 真实教训：先按 6 Mbps 压出约 700 MB 的方案，跑了十分钟被一句「还是太大」叫停，中间产物全废。

### 1 · 取片与验明正身

```bash
export PATH="$PATH:/c/Users/.../Android/Sdk/platform-tools"   # adb 不在 PATH 时补
export MSYS2_ARG_CONV_EXCL='*'   # 关键：否则 Git Bash 把 /sdcard/... 转成 Windows 路径，adb 找不到
adb devices -l
adb pull "/sdcard/DCIM/Camera/<源>.mp4" "<源>.mp4"
```

`ffprobe` 至少看清：`codec_name / pix_fmt / color_transfer / color_space / color_primaries / bit_rate / width / height / r_frame_rate` + 旋转元数据 + 音轨。**别凭文件名猜规格**（带 `DOLBY` 不等于 4K；本次实测是 1080p，省掉缩放）。

### 2 · 色调映射先试帧

HDR 源转发前**必须**映射到 SDR BT.709，否则微信 / Windows 播放器 / 投屏整体发灰发暗。出 3 秒试片、抽一帧肉眼比两条链路：

| 链路 | 滤镜 | 本机实测 |
| --- | --- | --- |
| GPU ⭐ | `libplacebo=tonemapping=auto:colorspace=bt709:color_primaries=bt709:color_trc=bt709:format=yuv420p` | 单遍约 5 分钟 |
| CPU | `zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p` | 两遍编码 10 分钟未完 |

画质接近时按速度选；有独显优先 GPU 单遍。**滤镜跑通不等于颜色对，必须看帧。**

### 3 · 按目标体积倒推码率，单遍直出

`码率 ≈ 目标体积(MB) × 8 × 1024 / 时长(秒) − 音轨码率`

```bash
ffmpeg -y -i "$IN" \
  -vf "libplacebo=tonemapping=auto:colorspace=bt709:color_primaries=bt709:color_trc=bt709:format=yuv420p" \
  -c:v libx264 -preset medium -b:v 1400k -maxrate 2000k -bufsize 4000k \
  -profile:v high -level 4.1 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ac 2 -movflags +faststart "$OUT"
```

参考锚点：15:26 竖屏人像讲解（背景静止）→ 1.4 Mbps → 169 MB。**换题材（运动 / 游戏实录 / 特效）先试帧，别套码率。**

### 4 · 回传手机与双校验

```bash
adb push "C:/.../成品.mp4" "/sdcard/Download/成品.mp4"   # Download：各类上传入口的文件选择器都可见
adb shell stat -c %s "/sdcard/Download/成品.mp4"          # 字节数与本机比对
adb shell toybox md5sum "/sdcard/Download/成品.mp4"       # MD5 与本机比对
adb shell "am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/Download/成品.mp4"
```

本地路径写 `C:/...` 风格，别用 `/c/...`（配合 `MSYS2_ARG_CONV_EXCL='*'`）。推送后告诉用户**手机上的确切路径**，别只说「传好了」。

---

## 验收清单

- [ ] 目标体积由用户确认过，成品落在 ±10% 内
- [ ] `ffprobe` 时长与源一帧不差；分辨率 / 帧率 / 旋转方向正确
- [ ] 色彩层：输出 BT.709 / SDR，抽帧肤色正常不发灰
- [ ] 兼容层：H.264 High + yuv420p + AAC，通用播放器可播
- [ ] 抽前 / 中 / 后 3 帧肉眼验：无块状瑕疵、无死黑过曝、方向正立
- [ ] 手机端字节数 + MD5 双一致
- [ ] 原片与本机源文件未删除
- [ ] 交付时附一句：要更小就从源重出，不拿成品二次压缩

## 红线

- ❌ 不问体积就开压
- ❌ HDR 源不做色调映射直接转发
- ❌ 拿成品二次压缩求更小（从源重出）
- ❌ 删除手机原片或本机源文件——破坏性操作，须明确确认
- ❌ 只信参数清单就交付：**内容能用清单验收，呈现必须肉眼验收**
- ❌ 交付时不给手机上的确切路径

## 关联

- 方法论：[[手机HDR视频交付_三层分离与体积先定_v1]] · [[Mac素材包到Windows的两个坑_zip文件名编码与HEVC解码_v1]] · [[图表交付的确定性_坐标绘制胜过自动布局_v1]]
- 私有剧本库：`<工作区>/juben-dm-lab`（本次讲解视频对应 `cases/954-虚拟游戏/10_过本单.md`）
