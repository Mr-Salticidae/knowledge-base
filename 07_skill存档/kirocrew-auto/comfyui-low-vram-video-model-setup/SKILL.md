---
name: auto/comfyui-low-vram-video-model-setup
description: Install a new ComfyUI model (clone portable, upgrade core, download weights, verify) headlessly via HTTP API and smoke test, debugging mismatches from the official template
triggers: ComfyUI local setup, 8GB VRAM, GGUF quantization, BlockSwap, HuggingFace weight download, extra_model_paths.yaml, 装新ComfyUI模型, 便携版升级, text encoder维度不对
source: auto
session_key: dashboard:chat-13-1792279878
created_at: 2026-10-14T20:17:00+00:00
version: 2
---

## When to use
Setting up an open-weight model in ComfyUI on Windows when VRAM is below the official minimum or the model needs a newer core. Confirm facts, protect the working env, use a community low-VRAM recipe, verify weights, then prove it with a boot self-test plus (image models) a real smoke image.

## Steps
1. Confirm via web, not memory: license, official HF repo (beware fakes), real checkpoint, min ComfyUI version, and the EXACT text encoder + VAE (generation N often differs from N-1).
2. Probe host: `nvidia-smi --query-gpu=name,memory.total --format=csv`, RAM, disk, arch (NVFP4 needs RTX50). Probe existing ComfyUI version, custom_nodes, yaml.
3. Never upgrade a working env in place: robocopy the portable to a new dir, upgrade the copy with `update/update.py` (needs `.git`).
4. After core upgrade re-run `pip install -r requirements.txt -i https://pypi.org/simple` to fix stale deps.
5. Recipe: GGUF/INT8 DiT + BlockSwap + quantized text encoder + community sweet-spot resolution/frames/steps. Watch quant quirks (dim not divisible by 256 -> Q4_0/Q5_1).
6. `git clone --depth 1` nodes into custom_nodes; install reqs with embedded python.exe.
7. List exact filenames/sizes with `HfApi().model_info(repo, files_metadata=True)` before pulling GB.
8. Weights on a roomy drive via a dedicated `extra_model_paths.yaml`. CJK paths: ASCII `-File` script with `[char]0x....`, results to a file. Resumable download via mirror. 401 or ~150-byte 'Access restricted' = gated; find a re-upload.
9. Boot test: `--lowvram --listen 127.0.0.1 --port <p> --disable-auto-launch` in background, logs, wait ~45s, grep for IMPORT FAILED/Traceback, low-VRAM state, paths. If a watchdog says stalled, check the port/API before relaunching.
10. `/object_info` must list your filenames; then a `/prompt` smoke image, poll `/history`. Leave OOM-prone video smoke tests to a human pass.
11. Some nodes ignore the yaml (grep `folder_paths`/`models_dir`); restart after adding weights.
12. Write a launcher .bat + deploy manual.

## Gotchas
- `mat1 and mat2 shapes cannot be multiplied` at txt_in = WRONG text encoder file (e.g. Qwen3 vs Qwen3-VL). Copy CLIP type, sampler and encoder name from the official template JSON in `comfyui_workflow_templates_json/templates/`; don't guess.
- aria2 `-i` input files mangle CJK paths (errorCode=18): pass `-d`/`-o` as argv, one file per call, one process only.
- `-like '*name*'` process checks match your own shell.
- hf_hub_download may throw LocalEntryNotFoundError while curl works; use a resumable downloader. Verify size and no `.aria2` file.
