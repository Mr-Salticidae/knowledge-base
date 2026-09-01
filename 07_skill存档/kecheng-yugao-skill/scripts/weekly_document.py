# -*- coding: utf-8 -*-
"""Resolve, safely publish, and validate the single canonical weekly DOCX."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def canonical_filename(start: date, end: date) -> str:
    return f"{start.month}.{start.day}-{end.month}.{end.day}课程预告.docx"


def weekly_candidates(docs: Path, start: date, end: date) -> list[Path]:
    stem = Path(canonical_filename(start, end)).stem
    return sorted(
        path.resolve()
        for path in docs.glob(f"{stem}*.docx")
        if path.is_file()
    )


def candidate_record(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.resolve()),
        "name": path.name,
        "size": path.stat().st_size,
        "sha256": sha256(path),
    }


def validate_docx(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.is_file() or path.stat().st_size <= 0:
        return [f"missing or empty DOCX: {path}"]
    if path.suffix.lower() != ".docx":
        errors.append(f"file must end in .docx: {path}")
        return errors
    try:
        with zipfile.ZipFile(path) as archive:
            names = set(archive.namelist())
            if "word/document.xml" not in names:
                errors.append("DOCX is missing word/document.xml")
            if "[Content_Types].xml" not in names:
                errors.append("DOCX is missing [Content_Types].xml")
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"DOCX package is invalid: {exc}")
    return errors


def resolve_weekly_document(
    project_root: Path, run_dir: Path, start: date, end: date
) -> dict[str, Any]:
    root = project_root.resolve()
    docs = (root / "课程预告文本").resolve()
    canonical = docs / canonical_filename(start, end)
    candidates = weekly_candidates(docs, start, end) if docs.is_dir() else []
    status = "ready" if len(candidates) <= 1 else "conflict"
    source = candidates[0] if len(candidates) == 1 else None
    return {
        "schema_version": 1,
        "status": status,
        "project_root": str(root),
        "period_start": start.isoformat(),
        "period_end": end.isoformat(),
        "canonical_filename": canonical.name,
        "canonical_path": str(canonical),
        "mode": "update" if source else "create",
        "source_document": str(source) if source else None,
        "source_is_legacy_name": bool(source and source != canonical),
        "same_week_candidates": [candidate_record(path) for path in candidates],
        "working_path": str((run_dir.resolve() / "drafts" / "weekly-working.docx")),
        "backup_root": str((run_dir.resolve() / "backups" / "weekly-document")),
        "errors": (
            []
            if status == "ready"
            else [
                "multiple same-week DOCX files exist; select the authoritative document before updating: "
                + " | ".join(path.name for path in candidates)
            ]
        ),
    }


def current_snapshot(plan: dict[str, Any]) -> list[dict[str, Any]]:
    canonical = Path(plan["canonical_path"])
    start = parse_iso_date(plan["period_start"])
    end = parse_iso_date(plan["period_end"])
    return [candidate_record(path) for path in weekly_candidates(canonical.parent, start, end)]


def check_weekly_document(
    project_root: Path,
    start: date,
    end: date,
    expected_docx: Path | None = None,
    expected_sha256: str | None = None,
) -> dict[str, Any]:
    root = project_root.resolve()
    docs = (root / "课程预告文本").resolve()
    canonical = docs / canonical_filename(start, end)
    candidates = weekly_candidates(docs, start, end) if docs.is_dir() else []
    errors: list[str] = []
    if len(candidates) != 1:
        errors.append(
            f"same-week DOCX count must be 1, found {len(candidates)}: "
            + " | ".join(path.name for path in candidates)
        )
    elif candidates[0] != canonical:
        errors.append(f"weekly DOCX must use canonical name: {canonical.name}")
    if expected_docx and expected_docx.resolve() != canonical:
        errors.append(f"delivery DOCX path is not canonical: {expected_docx.resolve()}")
    if canonical.exists():
        docx_errors = validate_docx(canonical)
        errors.extend(docx_errors)
        actual_hash = sha256(canonical) if not docx_errors else None
        if expected_sha256 and actual_hash != expected_sha256:
            errors.append("canonical DOCX SHA-256 does not match the expected value")
    else:
        actual_hash = None
        errors.append(f"canonical weekly DOCX is missing: {canonical}")
    publishing_artifacts = sorted(docs.glob(f".{canonical.stem}.publishing-*.docx")) if docs.is_dir() else []
    if publishing_artifacts:
        errors.append(
            "unfinished publication artifacts exist: "
            + " | ".join(path.name for path in publishing_artifacts)
        )
    return {
        "schema_version": 1,
        "valid": not errors,
        "period_start": start.isoformat(),
        "period_end": end.isoformat(),
        "canonical_path": str(canonical),
        "same_week_docx_count": len(candidates),
        "same_week_candidates": [str(path) for path in candidates],
        "canonical_sha256": actual_hash,
        "temporary_publication_files": [str(path.resolve()) for path in publishing_artifacts],
        "errors": errors,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def publish_weekly_document(plan_path: Path, source_docx: Path) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("status") != "ready":
        raise RuntimeError("weekly-document plan is not ready")
    source = source_docx.resolve()
    errors = validate_docx(source)
    if errors:
        raise RuntimeError("; ".join(errors))
    canonical = Path(plan["canonical_path"]).resolve()
    if source == canonical:
        raise RuntimeError("publish from the QA-approved working copy, not the live canonical DOCX")
    expected_snapshot = plan.get("same_week_candidates") or []
    actual_snapshot = current_snapshot(plan)
    if expected_snapshot != actual_snapshot:
        raise RuntimeError("same-week DOCX state changed after resolve; resolve again before publishing")

    canonical.parent.mkdir(parents=True, exist_ok=True)
    backup_root = Path(plan["backup_root"]).resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup_dir = backup_root / timestamp
    backup_dir.mkdir(parents=True, exist_ok=False)
    existing_paths = [Path(item["path"]).resolve() for item in expected_snapshot]
    for existing in existing_paths:
        shutil.copy2(existing, backup_dir / existing.name)

    with tempfile.NamedTemporaryFile(
        dir=canonical.parent,
        prefix=f".{canonical.stem}.publishing-",
        suffix=".docx",
        delete=False,
    ) as handle:
        temp_path = Path(handle.name)
    try:
        shutil.copy2(source, temp_path)
        temp_errors = validate_docx(temp_path)
        if temp_errors:
            raise RuntimeError("; ".join(temp_errors))
        os.replace(temp_path, canonical)
    finally:
        if temp_path.exists():
            temp_path.unlink()

    archived_legacy: list[str] = []
    for existing in existing_paths:
        if existing != canonical and existing.exists():
            existing.unlink()
            archived_legacy.append(str(existing))

    check = check_weekly_document(
        Path(plan["project_root"]),
        parse_iso_date(plan["period_start"]),
        parse_iso_date(plan["period_end"]),
        expected_docx=canonical,
        expected_sha256=sha256(canonical),
    )
    if not check["valid"]:
        raise RuntimeError("post-publication weekly DOCX check failed: " + " | ".join(check["errors"]))
    return {
        "schema_version": 1,
        "status": "published",
        "mode": plan["mode"],
        "canonical_path": str(canonical),
        "canonical_sha256": sha256(canonical),
        "backup_folder": str(backup_dir),
        "archived_legacy_paths": archived_legacy,
        "same_week_docx_count": check["same_week_docx_count"],
        "published_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    command = sub.add_parser("resolve")
    command.add_argument("--project-root", required=True)
    command.add_argument("--run-dir", required=True)
    command.add_argument("--period-start", required=True)
    command.add_argument("--period-end", required=True)
    command.add_argument("--out", required=True)

    command = sub.add_parser("publish")
    command.add_argument("--plan", required=True)
    command.add_argument("--source-docx", required=True)
    command.add_argument("--out", required=True)

    command = sub.add_parser("check")
    command.add_argument("--project-root", required=True)
    command.add_argument("--period-start", required=True)
    command.add_argument("--period-end", required=True)
    command.add_argument("--expected-docx")
    command.add_argument("--expected-sha256")
    command.add_argument("--out")

    args = parser.parse_args()
    if args.command == "resolve":
        result = resolve_weekly_document(
            Path(args.project_root),
            Path(args.run_dir),
            parse_iso_date(args.period_start),
            parse_iso_date(args.period_end),
        )
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
        if result["status"] != "ready":
            raise SystemExit(2)
    elif args.command == "publish":
        result = publish_weekly_document(Path(args.plan), Path(args.source_docx))
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
    else:
        result = check_weekly_document(
            Path(args.project_root),
            parse_iso_date(args.period_start),
            parse_iso_date(args.period_end),
            Path(args.expected_docx) if args.expected_docx else None,
            args.expected_sha256,
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
