# -*- coding: utf-8 -*-
"""Merge a validated poster index and audit evidence into a final manifest."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from course_preview import (
    course_key_for,
    poster_filename_contract_errors,
    read_json,
    write_json,
)


def course_map(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for course in manifest.get("courses") or []:
        key = str(course.get("course_key") or course_key_for(course))
        course["course_key"] = key
        if key in result:
            raise ValueError(f"duplicate course key: {key}")
        result[key] = course
    return result


def require_output(path_value: str, suffix: str) -> Path:
    path = Path(path_value).resolve()
    if path.suffix.lower() != suffix or not path.is_file() or path.stat().st_size <= 0:
        raise ValueError(f"missing or invalid {suffix} output: {path}")
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--poster-index", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    manifest = read_json(Path(args.manifest))
    courses = course_map(manifest)
    index = read_json(Path(args.poster_index))
    items = index.get("posters")
    if index.get("schema_version") != 1 or not isinstance(items, list):
        raise ValueError("poster index must use schema_version 1 and posters[]")
    seen: set[str] = set()

    for item in items:
        key = str(item.get("course_key") or "")
        if key not in courses:
            raise ValueError(f"poster index has unknown course_key: {key}")
        if key in seen:
            raise ValueError(f"poster index duplicates course_key: {key}")
        seen.add(key)
        working = require_output(item["working_psd"], ".psd")
        png = require_output(item["output_png"], ".png")
        published = require_output(item["output_psd"], ".psd")
        if working.stem != png.stem:
            raise ValueError(f"working PSD/final PNG stems differ for {key}")
        filename_errors = poster_filename_contract_errors(
            courses[key], png, manifest["target_date"]
        )
        if filename_errors:
            raise ValueError(
                f"poster filename contract failed for {key}: "
                + " | ".join(filename_errors)
            )

        grade = item.get("editability_grade")
        source_type = item.get("source_type")
        if grade not in {"A", "B"}:
            raise ValueError(f"invalid editability grade for {key}: {grade}")
        if source_type not in {"editable_psd", "flattened_date_slot"}:
            raise ValueError(f"invalid poster source type for {key}: {source_type}")
        if grade == "B" and item.get("base_verification") not in {"passed", True}:
            raise ValueError(f"grade B poster lacks exact-base verification: {key}")
        storage_status = item.get("publish_status")
        if storage_status not in {
            "reused_existing_course_psd",
            "published_new_course_psd",
            "already_published_course_psd",
            "already_in_output_folder",
        }:
            raise ValueError(
                f"invalid course PSD storage status for {key}: {storage_status}"
            )
        title_match = item.get("course_psd_title_match")
        if title_match not in {True, "passed"}:
            raise ValueError(
                f"course PSD lacks exact internal title evidence for {key}"
            )

        audit_path = Path(item["audit_file"]).resolve()
        audit = read_json(audit_path)
        changes = audit.get("changes", {})
        title_guard = changes.get("layout_guard")
        horizontal_guard = changes.get("title_horizontal_alignment")
        safe_guard = changes.get("objective_safe_area_guard")
        if grade == "A":
            if not isinstance(title_guard, dict):
                raise ValueError(f"title layout guard missing for {key}")
            if title_guard.get("actual_gap_px", -1) < title_guard.get("minimum_gap_px", 20):
                raise ValueError(f"title gap failed for {key}")
            if not isinstance(horizontal_guard, dict) or not horizontal_guard.get("enforced"):
                raise ValueError(f"title horizontal alignment guard missing/not enforced for {key}")
            actual_delta = abs(float(horizontal_guard.get("actual_center_delta_px", 1e9)))
            maximum_delta = float(horizontal_guard.get("maximum_center_delta_px", -1))
            horizontal_valid = maximum_delta >= 0 and actual_delta <= maximum_delta
            if not horizontal_valid:
                raise ValueError(f"title horizontal alignment failed for {key}")
            if not isinstance(safe_guard, dict) or safe_guard.get("skipped"):
                raise ValueError(f"objective safe-area guard missing/skipped for {key}")
            safe_valid = (
                safe_guard.get("vertical_overlap_px", 0) <= 0
                or safe_guard.get("actual_horizontal_gap_px", -1)
                >= safe_guard.get("minimum_horizontal_gap_px", 20)
            )
            if not safe_valid:
                raise ValueError(f"objective safe-area guard failed for {key}")
        else:
            horizontal_valid = True
            safe_valid = True

        course = courses[key]
        course.update(
            {
                "poster_working_psd": str(working),
                "poster_output_png": str(png),
                "poster_output_psd": str(published),
                "poster_course_psd": str(published),
                "poster_psd_storage_status": storage_status,
                "poster_source_type": source_type,
                "poster_editability_grade": grade,
                "poster_candidate_evidence": item.get("candidate_evidence", {}),
                "poster_qa": {
                    "audit_file": str(audit_path),
                    "full_poster_review": item.get("full_poster_review"),
                    "changed_region_review": item.get("changed_region_review"),
                    "title_layout_guard": title_guard,
                    "title_horizontal_alignment": {
                        "valid": horizontal_valid,
                        "evidence": horizontal_guard,
                    },
                    "objective_safe_area": {
                        "valid": safe_valid,
                        "evidence": safe_guard,
                    },
                    "editability_grade": grade,
                    "publish_status": storage_status,
                    "published_sha256": item.get("published_sha256"),
                    "course_psd_title_match": True,
                    "course_psd_title_evidence": item.get(
                        "course_psd_title_evidence"
                    ),
                },
            }
        )

    missing = sorted(set(courses) - seen)
    if missing:
        raise ValueError("poster index is missing courses: " + ", ".join(missing))
    manifest["completion"] = {
        "poster_index": str(Path(args.poster_index).resolve()),
        "status": "ready_for_delivery_check",
    }
    write_json(Path(args.out), manifest)
    print(Path(args.out).resolve())


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
