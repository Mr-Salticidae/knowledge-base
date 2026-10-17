# MiniMax H3 本地图生视频工作流 · 本机部署手册

> 本机 RTX 4060 Ti 8GB / 32GB RAM / Windows。480×864 低显存档。
> 搭建日期 2026-10-15。模型为 **开源权重**(H3 Community License,**商用需单独授权**,Comfy 是官方唯一转售方)。

## 一句话

H3 是 33B omni-modal 视频+音频模型,i2v 走 **FL2VA** checkpoint。8GB 跑得起来靠四层叠加:
**W4A8/GGUF 低比特量化 + BlockSwap 逐块换入换出 + 4B 小文本编码器(替 32B)+ 压分辨率到 480×864**。
真·本地推理,生成在本机;720p+ 成片需云端 regenerate(本地上限 768p,8GB 实测稳定 480×864)。

## 关键事实(核实于 2026-10,社区源)

- 本地基础分辨率 768p;8GB 实测甜点 **480×864 / 158 帧(~6.6s@24fps)/ 20 步 Euler/Simple**。25 步在 8GB 上不稳。
- NVFP4(11.9GB)**仅 Blackwell/RTX 50 系**;4060 Ti 是 Ada,用 **W4A8/GGUF**,不是 NVFP4。
- H3 隐藏层宽 2688,不被 256 整除 → **用不了 K-quant**(Q4_K_M 那种),只能经典 Q4_0/Q5_1/Q3mix 或 W4A8。
- 一条 clip 本地 5–10 分钟。

## 目录与组件

- ComfyUI 便携版(空壳,0.35.0):`C:\ComfyUI-H3\ComfyUI_windows_portable\`
- 权重库(D 盘,省 C 盘):`D:\AIGC工作站\99_工具\minimax_h3_tool\models\`
- `extra_model_paths.yaml`(C 盘 ComfyUI 内)指向 D 盘库。**例外:ClipProj 节点只读 `models_dir\clip_projections`(C 盘),该文件须放 C 盘。**

### 自定义节点(custom_nodes,4 个,全部已验加载成功)

| 节点 | 来源 | 作用 |
|---|---|---|
| ComfyUI-GGUF | city96/ComfyUI-GGUF | GGUF 量化加载 |
| ComfyUI-H3-Multishot | jlucasmcrell/ComfyUI-H3-Multishot | **补 `minimax_h3` 架构**(不然 GGUF 报 Unexpected architecture 拒载) |
| ComfyUI-ClipProj | nicolab28/ComfyUI-ClipProj | 4B 小编码器投影(省显存);**必须用 `-v3-mlp`,旧版报 KeyError 'W'** |
| ComfyUI-Spectrum-MiniMax-H3 | xmarre/ComfyUI-Spectrum-MiniMax-H3 | 采样加速(可选) |

### 权重(4 个,B/8GB 配方)

| 文件 | repo | 大小 | 去向 |
|---|---|---|---|
| minimax_h3_fl2va_pruned_w4a8_mixed.safetensors | starsfriday/MiniMax-H3-w4a8 | 12.5GB | diffusion_models |
| qwen3vl_4b_int8_convrot.safetensors | Stick9190/qwen3vl_4b_int8_convrot | 5.4GB | text_encoders |
| minimax_h3_video_vae_int8_convrot.safetensors | Kijai/MiniMax-H3-experimental | 3.2GB | vae |
| mmh3-4b-ClipProj-v3-mlp.safetensors | NicoLab28/ClipProj-MiniMax-H3 | 0.5GB | clip_projections(**C 盘**) |

## 启动

双击 `run_h3_8gb.bat`(或)：
```
cd /d C:\ComfyUI-H3\ComfyUI_windows_portable
python_embeded\python.exe -s ComfyUI\main.py --lowvram --fp16-vae --listen 127.0.0.1 --port 8188
```
浏览器开 http://127.0.0.1:8188 → 导入 `workflows\MiniMax_H3_FL2V_8GB_VRAM.json`。

## i2v 用法

- 两个 LoadImage 节点填首帧/尾帧(纯 i2v 可首尾用同一张或只给首帧)。
- 分辨率先用 **480×864,length 158,steps 20,Euler,Simple**。
- 产出落 `outputs\`。

## 下载踩坑(本机特有,务必记住)

1. **CJK 路径坑**:aria2 的 `-i` 输入文件被存成 ASCII,把 `AIGC工作站`/`99_工具` 编码成 `AIGC???`,报 `errorCode=18 Invalid argument` 建目录失败。
   **解法:不用 `-i`,直接把 Unicode 路径作为 `-d`/`-o` 参数传给 aria2c**(PowerShell 以 UTF-16 传参,aria2 收到正确路径)。
2. **hf-mirror 慢且重定向不稳**;**huggingface.co 原站 + aria2 `-x8 -s8`** 反而更快更稳(实测 ~9MB/s)。
3. aria2 加 `--file-allocation=none --auto-file-renaming=false --continue=true`;断点续传可靠。
4. **勿多开 aria2 抢同一文件**(会互相清理导致"下完即空")。单进程逐文件。

## 自检验证(2026-10-15 已通过)

ComfyUI 启动日志应见:
- `[H3] taught ComfyUI-GGUF the 'minimax_h3' architecture`
- `[ClipProj] graph watch installed`
- 4 节点 Import times 全部无 FAILED
- `comfy_kitchen backend eager/cuda available`,capabilities 含 `w4a8_int8_linear`(W4A8 算子就位)
- `Set vram state to: LOW_VRAM` + `async weight offloading`

## 待办(搭建完成时)

- [ ] 跑一条 480×864 i2v 冒烟测试,确认不 OOM、出 mp4
- [ ] 商用前确认 H3 Community License 授权(SeeBay 等参赛/商用片相关)


---

## 增强版工作流 (v2 · 2026-10-15)

跑通 480x864 基础档后加的三个增强。原始工作流备份在 `workflows\MiniMax_H3_FL2V_8GB_VRAM.base.json`。

### 1. 尾帧开关 (workflow 内)
- 新增本地小节点 `ComfyUI-H3-TailSwitch`（`custom_nodes\ComfyUI-H3-TailSwitch\__init__.py`，零依赖）。
- 节点名 **H3 Tail-Frame Switch**，接在首/尾 LoadImage 与 H3 节点之间。
- `use_tail` 关(默认)=复用首帧喂进 last_frame（纯 i2v 开放式运动，没尾帧时用这个）；开=用真尾帧。
- 这样 `MiniMaxH3ImageToVideo.last_frame` 这个必填口永远有合法输入，不会报缺输入。

### 2. 补帧 / 插帧 (workflow 内)
- 装 `ComfyUI-Frame-Interpolation`(Fannovel16)，依赖 opencv-contrib-python 已装(走官方 PyPI，清华镜像对该 wheel 403)。
- 新增 **RIFE_VFI** 节点接在 `VAEDecode -> CreateVideo` 之间。
- 8GB 配置：`ckpt=rife49.pth / multiplier=2 / fast_mode=on / ensemble=off / scale_factor=1.0 / dtype=float16 / clear_cache_after_n_frames=4 / torch_compile=off`。
- **关键**：multiplier=2 把 24->48fps，所以 **CreateVideo 的 fps 已同步改成 48**（否则播放会被放慢）。首次用 RIFE 会自动下 rife49 权重(~50MB)。
- triton 缺失无害(只有 torch_compile=on 才用，已关)。

### 3. 超分 (离线 CLI，不进 workflow)
- 脚本 `upscale_video.py`。**刻意放到图外**：8GB 逐帧超分在 ComfyUI 里几乎必 OOM；且 GAN 超分会抹平颗粒/柔焦，作者历史偏好是定稿默认原版、超分慎用。
- 用法：`python_embeded\python.exe upscale_video.py 输入.mp4 --scale 2`
- 流程：拆帧 -> realesrgan-ncnn-vulkan 逐帧放大(零推理显存) -> ffmpeg 重组(保留原音频/原帧率)。
- realesrgan-ncnn-vulkan 便携 exe 已装到 `bin\`(含 x4plus / x4plus-anime / animevideov3 模型)，脚本自动检测；缺失时打印一键下载命令。
- 已端到端实测通过(2026-10-15)：640x480 -> x4 -> 2560x1920，帧率/音频保留。x4plus 模型按 x4 出，`--scale` 走模型原生倍数。
- 建议：定稿前先出 5s 原版/超分对比片盲看再决定是否整片超分。

### 自检验证 (2026-10-15)
- CI 自检全绿：TailSwitch 0.0s 加载、Frame-Interpolation 0.4s 加载、H3 架构补丁仍生效、ClipProj 完好。
- workflow JSON link 完整性校验通过：无悬空 link，node8.last_frame<-TailSwitch、node15.images<-RIFE(fps=48)、RIFE.frames<-VAEDecode。
