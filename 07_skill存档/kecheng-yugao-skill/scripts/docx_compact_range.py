#!/usr/bin/env python3
"""Compact spacer paragraphs in a render-identified paragraph range."""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document
from docx.shared import Pt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--start", required=True, type=int)
    parser.add_argument("--end", required=True, type=int)
    parser.add_argument("--size-pt", type=float, default=0.5)
    args = parser.parse_args()

    doc = Document(args.input)
    paragraphs = list(doc.paragraphs)
    if not (0 <= args.start < args.end <= len(paragraphs)):
        raise ValueError("invalid paragraph range")
    changed = 0
    for paragraph in paragraphs[args.start:args.end]:
        if paragraph.text.strip() or paragraph.paragraph_format.page_break_before:
            continue
        paragraph.paragraph_format.space_before = Pt(0)
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = Pt(args.size_pt)
        for run in paragraph.runs:
            run.font.size = Pt(args.size_pt)
        changed += 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(f"{output.resolve()}\ncompacted_spacers={changed}")


if __name__ == "__main__":
    main()
