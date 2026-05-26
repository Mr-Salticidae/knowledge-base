"""Convert liblib.tv exported videos to widely playable MP4 files.

Default output:
- H.264 video
- yuv420p pixel format
- 1920x1080 max size
- 24 fps
- AAC audio when audio exists
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import imageio_ffmpeg


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def probe(ffmpeg: str, input_path: Path) -> dict:
    ffprobe = str(Path(ffmpeg).with_name("ffprobe.exe"))
    if not Path(ffprobe).exists():
        return {}
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-show_format",
            str(input_path),
        ]
    )
    return json.loads(result.stdout)


def has_audio(meta: dict) -> bool:
    return any(stream.get("codec_type") == "audio" for stream in meta.get("streams", []))


def build_output_path(input_path: Path, output: str | None) -> Path:
    if output:
        return Path(output)
    return input_path.with_name(f"{input_path.stem}_h264_1080p.mp4")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert liblib.tv HEVC/high-fps MP4 exports to compatible H.264 MP4."
    )
    parser.add_argument("input", help="Input video path, e.g. path\\to\\input.mp4")
    parser.add_argument("-o", "--output", help="Output MP4 path. Defaults beside input.")
    parser.add_argument("--fps", type=int, default=24, help="Output frame rate. Default: 24")
    parser.add_argument(
        "--height",
        type=int,
        default=1080,
        help="Max output height while preserving aspect ratio. Default: 1080",
    )
    parser.add_argument(
        "--crf",
        type=int,
        default=18,
        help="H.264 quality. Lower is higher quality. Default: 18",
    )
    parser.add_argument(
        "--preset",
        default="medium",
        choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow"],
        help="Encoding speed/size tradeoff. Default: medium",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file does not exist: {input_path}")

    output_path = build_output_path(input_path, args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    meta = probe(ffmpeg, input_path)
    audio_args = ["-an"]
    if has_audio(meta):
        audio_args = ["-c:a", "aac", "-b:a", "192k"]

    scale_filter = (
        f"fps={args.fps},"
        f"scale=-2:'min({args.height},ih)':force_original_aspect_ratio=decrease"
    )

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(input_path),
        "-vf",
        scale_filter,
        "-c:v",
        "libx264",
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        *audio_args,
        str(output_path),
    ]

    print("Converting:")
    print(f"  input : {input_path}")
    print(f"  output: {output_path}")
    print(f"  ffmpeg: {ffmpeg}")
    completed = run(command)
    if completed.stderr:
        print(completed.stderr[-1200:])
    print("Done.")


if __name__ == "__main__":
    main()
