# -*- coding: utf-8 -*-
"""Validate the final DOCX, PNG posters, and reusable course PSD mappings."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from docx import Document

from course_preview import (
    normalize_title,
    poster_filename_contract_errors,
    read_json,
    validate_manifest,
    write_json,
)
from weekly_document import check_weekly_document


def poster_qa_valid(course: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    grade = course.get("poster_editability_grade")
    if grade not in {"A", "B"}:
        errors.append(f"invalid poster editability grade: {grade!r}")
    qa = course.get("poster_qa")
    if not isinstance(qa, dict):
        return errors + ["poster_qa is missing"]
    if qa.get("full_poster_review") not in {"passed", True}:
        errors.append("full poster review has not passed")
    horizontal = qa.get("title_horizontal_alignment")
    if isinstance(horizontal, dict):
        if horizontal.get("valid") not in {True, "passed"}:
            errors.append("title horizontal alignment check has not passed")
    elif grade == "A":
        errors.append("title horizontal alignment evidence is missing")
    safe = qa.get("objective_safe_area")
    if isinstance(safe, dict):
        if safe.get("valid") not in {True, "passed"}:
            errors.append("objective safe-area check has not passed")
    elif grade == "A":
        errors.append("objective safe-area evidence is missing")
    if qa.get("publish_status") not in {
        "reused_existing_course_psd",
        "published_new_course_psd",
        "already_published_course_psd",
        "already_in_output_folder",
    }:
        errors.append("course PSD storage status is not complete")
    if qa.get("course_psd_title_match") not in {True, "passed"}:
        errors.append("exact internal course-title evidence is missing")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--docx", required=True)
    parser.add_argument("--poster-folder", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()

    manifest = read_json(Path(args.manifest))
    errors = validate_manifest(manifest, 2)
    document_path = Path(args.docx).resolve()
    period = manifest.get("period") or {}
    try:
        weekly_check = check_weekly_document(
            Path(manifest["root"]),
            date.fromisoformat(str(period["start"])),
            date.fromisoformat(str(period["end"])),
            expected_docx=document_path,
        )
        errors.extend(
            f"weekly document: {item}" for item in weekly_check["errors"]
        )
    except Exception as exc:
        weekly_check = {"valid": False, "same_week_docx_count": None}
        errors.append(f"weekly document check failed: {exc}")
    document = Document(document_path)
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs]
    document_key = normalize_title("\n".join(paragraphs))
    poster_folder = Path(args.poster_folder).resolve()
    actual_pngs = sorted(poster_folder.glob("*.png"))
    expected_pngs: set[Path] = set()
    expected_psds: set[Path] = set()
    title_to_psd: dict[str, Path] = {}
    psd_to_title: dict[Path, str] = {}

    for course in manifest.get("courses") or []:
        label = course.get("course_key") or course.get("course_title")
        for field in ("class_name", "course_title", "teacher"):
            value = str(course.get(field, ""))
            if normalize_title(value) not in document_key:
                errors.append(f"{label}: DOCX is missing {field}={value}")
        if course.get("delivery") == "live":
            matching_rows = [
                text
                for text in paragraphs
                if normalize_title(str(course.get("course_title")))
                in normalize_title(text)
            ]
            if not any("直播" in row for row in matching_rows):
                errors.append(f"{label}: live marker is missing from DOCX")
        for objective in course.get("details", {}).get("objectives") or []:
            if normalize_title(str(objective)) not in document_key:
                errors.append(f"{label}: DOCX is missing objective={objective}")

        png_value = course.get("poster_output_png")
        psd_value = course.get("poster_output_psd")
        if not png_value or not psd_value:
            errors.append(f"{label}: poster output paths are missing")
            continue
        png = Path(png_value).resolve()
        psd = Path(psd_value).resolve()
        expected_pngs.add(png)
        expected_psds.add(psd)
        if not png.is_file() or png.stat().st_size <= 0:
            errors.append(f"{label}: missing or empty PNG: {png}")
        if not psd.is_file() or psd.stat().st_size <= 0:
            errors.append(f"{label}: missing or empty PSD: {psd}")
        title_key = normalize_title(str(course.get("course_title", "")))
        prior_psd = title_to_psd.setdefault(title_key, psd)
        if prior_psd != psd:
            errors.append(f"{label}: one course title maps to multiple PSD files")
        prior_title = psd_to_title.setdefault(psd, title_key)
        if prior_title != title_key:
            errors.append(f"{label}: one PSD maps to multiple course titles")
        errors.extend(
            f"{label}: {item}"
            for item in poster_filename_contract_errors(
                course, png, manifest["target_date"]
            )
        )
        errors.extend(f"{label}: {item}" for item in poster_qa_valid(course))

    actual_png_set = {path.resolve() for path in actual_pngs}
    if actual_png_set != expected_pngs:
        missing = sorted(str(path) for path in expected_pngs - actual_png_set)
        extra = sorted(str(path) for path in actual_png_set - expected_pngs)
        if missing:
            errors.append("poster folder is missing manifest PNGs: " + " | ".join(missing))
        if extra:
            errors.append("poster folder has untracked PNGs: " + " | ".join(extra))

    course_count = len(manifest.get("courses") or [])
    if course_count != len(expected_pngs):
        errors.append("course/PNG counts are not one-to-one")
    if not expected_psds and course_count:
        errors.append("no reusable course PSDs are mapped")

    result = {
        "schema_version": 1,
        "valid": not errors,
        "course_count": course_count,
        "poster_png_count": len(actual_pngs),
        "unique_course_psd_count": len(expected_psds),
        "available_course_psd_count": sum(path.is_file() for path in expected_psds),
        "weekly_document_valid": weekly_check["valid"],
        "same_week_docx_count": weekly_check["same_week_docx_count"],
        "errors": errors,
    }
    if args.out:
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
