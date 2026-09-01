# -*- coding: utf-8 -*-
"""Detect common pagination regressions in a rendered course-preview PDF."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import fitz
except ImportError:  # Bundled workspace Python normally provides pypdf.
    fitz = None
    from pypdf import PdfReader

from course_preview import normalize_title, read_json, write_json


DETACHED_PREFIXES = (
    "🙌",
    "👉",
    "课程目标",
    "作业布置",
    "授课老师",
    "所需工具",
)
DETACHED_CONTAINS = ("直播预告通知", "录播课程已更新")
DETACHED_TIME_PATTERN = re.compile(
    r"^\d{1,2}\s*月\s*\d{1,2}\s*(?:日|号)?\s+\d{1,2}\s*[:：]\s*\d{2}"
)


def is_detached_page_start(line: str) -> bool:
    """Recognize detached block lines even when PDF extraction loses emoji."""
    # Word/PDF extraction may replace the leading hand/bell glyph with U+FFFD
    # or omit it entirely. Strip only known extraction noise, then inspect the
    # semantic line content as well as the original marker.
    cleaned = line.lstrip("\ufeff\ufffd\ufe0f\u200d ?")
    return (
        line.startswith(DETACHED_PREFIXES)
        or cleaned.startswith(DETACHED_PREFIXES)
        or any(marker in cleaned for marker in DETACHED_CONTAINS)
        or bool(DETACHED_TIME_PATTERN.match(cleaned))
    )


def meaningful_lines(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", line).strip() for line in text.splitlines() if line.strip()]


def extract_pages(pdf_path: Path) -> list[str]:
    if fitz is not None:
        document = fitz.open(pdf_path)
        try:
            return [page.get_text("text") for page in document]
        finally:
            document.close()
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return [
        text.encode("utf-16", "surrogatepass").decode("utf-16", "replace")
        for text in pages
    ]


def analyze(pdf_path: Path, manifest: dict[str, Any], stage: str, min_last_chars: int) -> dict[str, Any]:
    pages = extract_pages(pdf_path)
    errors: list[dict[str, Any]] = []
    metrics = []

    for index, text in enumerate(pages):
        lines = meaningful_lines(text)
        compact_chars = len(re.sub(r"\s+", "", text))
        metrics.append(
            {
                "page": index + 1,
                "non_whitespace_chars": compact_chars,
                "first_line": lines[0] if lines else "",
                "last_line": lines[-1] if lines else "",
            }
        )
        if index > 0 and lines and is_detached_page_start(lines[0]):
            errors.append(
                {
                    "type": "detached_page_start",
                    "page": index + 1,
                    "text": lines[0],
                }
            )

    if len(pages) > 1 and metrics[-1]["non_whitespace_chars"] < min_last_chars:
        errors.append(
            {
                "type": "nearly_empty_final_page",
                "page": len(pages),
                "non_whitespace_chars": metrics[-1]["non_whitespace_chars"],
                "minimum": min_last_chars,
            }
        )

    expected_occurrences = 1 if stage == "a" else 2
    all_text_key = normalize_title("\n".join(pages))
    target_classes = {
        normalize_title(str(course.get("class_name", "")))
        for course in manifest.get("courses") or []
    }
    for course in manifest.get("courses") or []:
        title = str(course.get("course_title", ""))
        count = all_text_key.count(normalize_title(title))
        if count < expected_occurrences:
            errors.append(
                {
                    "type": "missing_course_occurrence",
                    "course_key": course.get("course_key"),
                    "title": title,
                    "found": count,
                    "minimum": expected_occurrences,
                }
            )

    for index, text in enumerate(pages[:-1]):
        lines = meaningful_lines(text)
        if not lines:
            continue
        last_key = normalize_title(lines[-1])
        if last_key in target_classes:
            errors.append(
                {
                    "type": "orphan_class_heading",
                    "page": index + 1,
                    "text": lines[-1],
                }
            )

    return {
        "schema_version": 1,
        "pdf": str(pdf_path.resolve()),
        "stage": stage,
        "page_count": len(pages),
        "page_metrics": metrics,
        "valid": not errors,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--stage", required=True, choices=("a", "b"))
    parser.add_argument("--min-last-page-chars", type=int, default=80)
    parser.add_argument("--out")
    args = parser.parse_args()

    result = analyze(
        Path(args.pdf),
        read_json(Path(args.manifest)),
        args.stage,
        args.min_last_page_chars,
    )
    if args.out:
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
