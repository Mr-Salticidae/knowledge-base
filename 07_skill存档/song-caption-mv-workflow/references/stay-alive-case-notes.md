# Stay alive Case Notes

> 案例日期：2026-06-07
> 项目：`D:\AIGC工作站\38_Stay alive`

## 已验证链路

```text
Suno song
→ MJ V8.1 abstract surreal images
→ no-text MP4
→ Demucs vocals stem
→ WhisperX large-v3-turbo on CUDA
→ word-level JSON
→ phrase-level SRT
→ user hand-adjusted SRT
→ Chinese artistic translation SRT
```

## 本机环境

- GPU：NVIDIA GeForce RTX 4060 Ti
- CUDA driver：`nvidia-smi` 显示 CUDA 13.2
- PyTorch：`2.8.0+cu128`
- WhisperX：`3.8.6`
- Demucs：`4.0.1`
- 字体：`C:\Windows\Fonts\NotoSerifSC-VF.ttf`

## 关键经验

- CPU 版 PyTorch 会让 Demucs/WhisperX 很慢；需要安装 CUDA 版 PyTorch。
- 安装 CUDA PyTorch 后可能把 Pillow 升到 MoviePy 不兼容版本，需回退到 `<12.0`。
- WhisperX 默认 SRT 可能是长段；真正有用的是 JSON 里的 `word_segments`。
- 哼唱类歌曲不要把 `Hum/Mmm` 当歌词显示，除非创作者明确要做拟声字幕。
- 最终发布版仍需要人工审美精修：本案最终 MV 由用户手动调整文字大小、位置，并添加片头标题、作者信息后导出；本 Skill 的目标是把作品推进到高质量可精修状态，而不是承诺完全无人参与的一键成片。

