#!/usr/bin/env python3
"""Set DOCX section margins for render-QA pagination repair."""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document
from docx.shared import Pt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--bottom-pt", type=float)
    args = parser.parse_args()

    doc = Document(args.input)
    for section in doc.sections:
        if args.bottom_pt is not None:
            section.bottom_margin = Pt(args.bottom_pt)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(output.resolve())


if __name__ == "__main__":
    main()
