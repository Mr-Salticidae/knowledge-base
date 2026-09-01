# -*- coding: utf-8 -*-
"""Compare two manifests by stable course identity and reject unrelated edits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from course_preview import course_key_for, read_json, write_json


COURSE_FIELDS = (
    "class_name",
    "schedule_title",
    "course_title",
    "teacher",
    "delivery",
    "time",
    "requested_poster_template_id",
    "poster_template_selection",
)
TOP_FIELDS = (
    "target_date",
    "period",
    "requested_text_template_id",
    "text_template_selection",
)


def keyed_courses(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for course in manifest.get("courses") or []:
        key = str(course.get("course_key") or course_key_for(course))
        if key in result:
            raise ValueError(f"duplicate course key: {key}")
        result[key] = course
    return result


def semantic_diff(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    top_changes = [
        {"field": field, "before": before.get(field), "after": after.get(field)}
        for field in TOP_FIELDS
        if before.get(field) != after.get(field)
    ]
    old_courses = keyed_courses(before)
    new_courses = keyed_courses(after)
    all_keys = sorted(set(old_courses) | set(new_courses))
    course_changes: list[dict[str, Any]] = []
    for key in all_keys:
        if key not in old_courses:
            course_changes.append({"course_key": key, "change": "added"})
            continue
        if key not in new_courses:
            course_changes.append({"course_key": key, "change": "removed"})
            continue
        fields = [
            {
                "field": field,
                "before": old_courses[key].get(field),
                "after": new_courses[key].get(field),
            }
            for field in COURSE_FIELDS
            if old_courses[key].get(field) != new_courses[key].get(field)
        ]
        if fields:
            course_changes.append(
                {"course_key": key, "change": "modified", "fields": fields}
            )
    return {
        "schema_version": 1,
        "top_level_changes": top_changes,
        "course_changes": course_changes,
        "changed_course_keys": [item["course_key"] for item in course_changes],
    }


def delivery_override_is_confirmed(course: dict[str, Any]) -> bool:
    for override in course.get("overrides") or []:
        if override.get("field") != "delivery":
            continue
        required = (
            "old_delivery",
            "new_delivery",
            "old_time",
            "new_time",
            "evidence",
        )
        if override.get("time_confirmed") and all(
            override.get(field) not in (None, "") for field in required
        ):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", required=True)
    parser.add_argument("--after", required=True)
    parser.add_argument("--expect-only", action="append", default=[])
    parser.add_argument("--require-delivery-time-review", action="store_true")
    parser.add_argument("--out")
    args = parser.parse_args()

    before = read_json(Path(args.before))
    after = read_json(Path(args.after))
    result = semantic_diff(before, after)
    errors: list[str] = []

    if args.expect_only:
        allowed = set(args.expect_only)
        unrelated = sorted(set(result["changed_course_keys"]) - allowed)
        if result["top_level_changes"]:
            errors.append("unexpected top-level manifest changes")
        if unrelated:
            errors.append("unrequested course changes: " + ", ".join(unrelated))
        missing = sorted(allowed - set(result["changed_course_keys"]))
        if missing:
            errors.append("expected course did not change: " + ", ".join(missing))

    if args.require_delivery_time_review:
        new_courses = keyed_courses(after)
        for change in result["course_changes"]:
            if change.get("change") != "modified":
                continue
            if any(field["field"] == "delivery" for field in change.get("fields", [])):
                course = new_courses[change["course_key"]]
                if not delivery_override_is_confirmed(course):
                    errors.append(
                        f"delivery change lacks confirmed old/new time: {change['course_key']}"
                    )

    result["valid"] = not errors
    result["errors"] = errors
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
