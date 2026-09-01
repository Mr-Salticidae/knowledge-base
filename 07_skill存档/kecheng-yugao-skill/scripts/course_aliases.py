# -*- coding: utf-8 -*-
"""Persist and resolve user-confirmed historical course-title aliases."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from course_preview import normalize_title, read_json, write_json


def empty_registry() -> dict[str, Any]:
    return {"schema_version": 1, "revision": 1, "aliases": []}


def read_registry(path: Path) -> dict[str, Any]:
    data = read_json(path)
    if data.get("schema_version") != 1 or not isinstance(data.get("aliases"), list):
        raise ValueError("course alias registry must use schema_version 1")
    return data


def teacher_key(value: str | None) -> str | None:
    if not value:
        return None
    return normalize_title(value.removesuffix("老师"))


def init_command(args: argparse.Namespace) -> None:
    path = Path(args.registry)
    if path.exists():
        raise FileExistsError(path)
    write_json(path, empty_registry())
    print(path.resolve())


def add_command(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise ValueError("explicit user approval is required")
    path = Path(args.registry)
    data = read_registry(path)
    alias_key = normalize_title(args.alias)
    constraint = teacher_key(args.teacher)
    conflicts = [
        item
        for item in data["aliases"]
        if item["alias_key"] == alias_key
        and item.get("teacher_key") == constraint
        and normalize_title(item["canonical_title"])
        != normalize_title(args.canonical)
    ]
    if conflicts:
        raise ValueError("alias conflicts with an existing canonical title")
    duplicate = [
        item
        for item in data["aliases"]
        if item["alias_key"] == alias_key
        and item.get("teacher_key") == constraint
        and normalize_title(item["canonical_title"])
        == normalize_title(args.canonical)
    ]
    if duplicate:
        raise ValueError("alias is already registered")
    data["aliases"].append(
        {
            "alias_title": args.alias,
            "alias_key": alias_key,
            "canonical_title": args.canonical,
            "teacher": args.teacher,
            "teacher_key": constraint,
            "source": args.source,
            "confirmed_at_utc": datetime.now(timezone.utc).isoformat(),
        }
    )
    data["revision"] = int(data.get("revision", 0)) + 1
    write_json(path, data)
    print(path.resolve())


def resolve_command(args: argparse.Namespace) -> None:
    data = read_registry(Path(args.registry))
    alias_key = normalize_title(args.title)
    constraint = teacher_key(args.teacher)
    candidates = [item for item in data["aliases"] if item["alias_key"] == alias_key]
    if constraint:
        candidates = [
            item
            for item in candidates
            if item.get("teacher_key") in (None, constraint)
        ]
    canonical_keys = {normalize_title(item["canonical_title"]) for item in candidates}
    result = {
        "schema_version": 1,
        "title": args.title,
        "teacher": args.teacher,
        "status": "matched" if len(canonical_keys) == 1 else (
            "missing" if not candidates else "ambiguous"
        ),
        "candidates": candidates,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "matched":
        raise SystemExit(2)


def list_command(args: argparse.Namespace) -> None:
    print(json.dumps(read_registry(Path(args.registry)), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    command = sub.add_parser("init")
    command.add_argument("--registry", required=True)
    command.set_defaults(func=init_command)

    command = sub.add_parser("add")
    command.add_argument("--registry", required=True)
    command.add_argument("--alias", required=True)
    command.add_argument("--canonical", required=True)
    command.add_argument("--teacher")
    command.add_argument("--source", required=True)
    command.add_argument("--user-approved", action="store_true")
    command.set_defaults(func=add_command)

    command = sub.add_parser("resolve")
    command.add_argument("--registry", required=True)
    command.add_argument("--title", required=True)
    command.add_argument("--teacher")
    command.set_defaults(func=resolve_command)

    command = sub.add_parser("list")
    command.add_argument("--registry", required=True)
    command.set_defaults(func=list_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
