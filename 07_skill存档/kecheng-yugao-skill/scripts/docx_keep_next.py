#!/usr/bin/env python3
"""Set keep-with-next on selected DOCX paragraphs after render QA."""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--indices", required=True, nargs="+", type=int)
    args = parser.parse_args()

    doc = Document(args.input)
    paragraphs = list(doc.paragraphs)
    for index in sorted(set(args.indices)):
        if index < 0 or index >= len(paragraphs) - 1:
            raise ValueError(f"paragraph index out of range: {index}")
        paragraphs[index].paragraph_format.keep_with_next = True

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output)
    print(output.resolve())


if __name__ == "__main__":
    main()
