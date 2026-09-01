# -*- coding: utf-8 -*-
"""Guardrails for templates, approvals, teacher assets, and poster outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image

from course_preview import (
    course_key_for,
    normalize_title,
    phase1_fingerprint,
    phase1_payload,
    read_json,
    validate_manifest,
    write_json,
)


REGISTRY_SCHEMA_VERSION = 1
SETTINGS_SCHEMA_VERSION = 1
TEXT_KIND = "text"
POSTER_KIND = "poster"
TEMPLATE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TEXT_TEMPLATE_ID_RE = re.compile(r"^text-template-\d+$")
POSTER_TEMPLATE_ID_RE = re.compile(r"^poster-template-\d+$")
DELIVERIES = {"live", "recorded"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def portable_path(root: Path, value: str | Path) -> str:
    path = Path(value).resolve()
    try:
        return str(path.relative_to(root.resolve()))
    except ValueError:
        return str(path)


def resolve_path(root: Path, value: str | Path | None) -> Path | None:
    if value in (None, ""):
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def require_file(path: Path, suffixes: set[str] | None = None) -> None:
    if not path.is_file():
        raise FileNotFoundError(path)
    if suffixes and path.suffix.lower() not in suffixes:
        raise ValueError(
            f"unsupported file type for {path}; expected {sorted(suffixes)}"
        )


def require_directory(path: Path) -> None:
    if not path.is_dir():
        raise NotADirectoryError(path)


def validate_template_id(template_id: str, kind: str) -> None:
    if not TEMPLATE_ID_RE.fullmatch(template_id):
        raise ValueError("template id must use lowercase letters, digits, and hyphens")
    expected = TEXT_TEMPLATE_ID_RE if kind == TEXT_KIND else POSTER_TEMPLATE_ID_RE
    if not expected.fullmatch(template_id):
        raise ValueError(f"{kind} template id has invalid prefix: {template_id}")


def read_typed_registry(path: Path, kind: str) -> dict[str, Any]:
    registry = read_json(path)
    if registry.get("schema_version") != REGISTRY_SCHEMA_VERSION:
        raise ValueError(f"{kind} registry schema_version must be 1")
    if registry.get("kind") != kind:
        raise ValueError(
            f"registry kind mismatch: expected {kind}, got {registry.get('kind')}"
        )
    if not isinstance(registry.get("templates"), dict) or not registry["templates"]:
        raise ValueError(f"{kind} registry has no templates")
    default_id = registry.get("default_template_id")
    if default_id not in registry["templates"]:
        raise ValueError(f"{kind} registry default is missing")
    return registry


def save_registry(path: Path, registry: dict[str, Any]) -> None:
    registry["revision"] = int(registry.get("revision", 0)) + 1
    write_json(path, registry)


def require_confirmed_template(
    registry: dict[str, Any], template_id: str
) -> dict[str, Any]:
    template = registry["templates"].get(template_id)
    if not template:
        raise ValueError(f"unknown template id: {template_id}")
    if not template.get("enabled", True):
        raise ValueError(f"template is disabled: {template_id}")
    if template.get("status") != "confirmed":
        raise ValueError(f"template has not been confirmed by the user: {template_id}")
    return template


def selection_record(
    registry: dict[str, Any],
    template_id: str,
    source: str,
) -> dict[str, Any]:
    template = require_confirmed_template(registry, template_id)
    return {
        "template_id": template_id,
        "display_name": template["display_name"],
        "selection_source": source,
        "registry_revision": registry["revision"],
    }


def text_template_add(args: argparse.Namespace) -> None:
    path = Path(args.registry)
    registry = read_typed_registry(path, TEXT_KIND)
    validate_template_id(args.id, TEXT_KIND)
    if args.id in registry["templates"]:
        raise ValueError(f"template already exists: {args.id}")
    root = Path(registry["project_root"])
    sources = {
        "source_docx": Path(args.source_docx),
        "executable_template": Path(args.executable_template),
        "contract": Path(args.contract),
        "usage_guide": Path(args.usage_guide),
        "sample_docx": Path(args.sample_docx),
    }
    require_file(sources["source_docx"], {".docx"})
    require_file(sources["executable_template"], {".docx"})
    require_file(sources["contract"], {".json", ".md"})
    require_file(sources["usage_guide"], {".md"})
    require_file(sources["sample_docx"], {".docx"})
    registry["templates"][args.id] = {
        "display_name": args.name,
        "enabled": True,
        "status": "pending",
        "renderer": "distilled-docx",
        "assets": {
            key: portable_path(root, value)
            for key, value in sources.items()
        },
        "source_sha256": sha256_file(sources["source_docx"]),
        "notes": args.notes or "",
    }
    save_registry(path, registry)
    print(json.dumps({
        "added": args.id,
        "status": "pending",
        "default_template_id": registry["default_template_id"],
        "revision": registry["revision"],
    }, ensure_ascii=False, indent=2))


def text_template_confirm(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise ValueError("explicit user approval is required")
    path = Path(args.registry)
    registry = read_typed_registry(path, TEXT_KIND)
    template = registry["templates"].get(args.id)
    if not template:
        raise ValueError(f"unknown template id: {args.id}")
    root = Path(registry["project_root"])
    source = resolve_path(root, template.get("assets", {}).get("source_docx"))
    if not source:
        raise ValueError("template source_docx is missing")
    require_file(source, {".docx"})
    if template.get("source_sha256") != sha256_file(source):
        raise ValueError("source DOCX changed after distillation")
    template["status"] = "confirmed"
    template["confirmed_at"] = datetime.now(timezone.utc).isoformat()
    save_registry(path, registry)
    print(json.dumps({
        "confirmed": args.id,
        "default_template_id": registry["default_template_id"],
        "revision": registry["revision"],
    }, ensure_ascii=False, indent=2))


def text_template_set_default(args: argparse.Namespace) -> None:
    path = Path(args.registry)
    registry = read_typed_registry(path, TEXT_KIND)
    require_confirmed_template(registry, args.id)
    registry["default_template_id"] = args.id
    save_registry(path, registry)
    print(json.dumps({
        "default_template_id": args.id,
        "revision": registry["revision"],
    }, ensure_ascii=False, indent=2))


def poster_template_add(args: argparse.Namespace) -> None:
    path = Path(args.registry)
    registry = read_typed_registry(path, POSTER_KIND)
    validate_template_id(args.id, POSTER_KIND)
    if args.id in registry["templates"]:
        raise ValueError(f"template already exists: {args.id}")
    root = Path(registry["project_root"])
    poster_sources = []
    for value in args.poster_source or []:
        resolved = resolve_path(root, value)
        assert resolved is not None
        if not resolved.exists():
            raise FileNotFoundError(resolved)
        poster_sources.append(portable_path(root, resolved))
    if not poster_sources:
        raise ValueError("at least one poster source is required")
    layer_contract = None
    if args.layer_contract:
        contract_path = Path(args.layer_contract)
        require_file(contract_path, {".json"})
        layer_contract = portable_path(root, contract_path)
    registry["templates"][args.id] = {
        "display_name": args.name,
        "enabled": True,
        "status": "pending",
        "assets": {
            "poster_sources": poster_sources,
            "layer_contract": layer_contract,
        },
        "notes": args.notes or "",
    }
    save_registry(path, registry)
    print(json.dumps({
        "added": args.id,
        "status": "pending",
        "default_template_id": registry["default_template_id"],
        "revision": registry["revision"],
    }, ensure_ascii=False, indent=2))


def poster_template_confirm(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise ValueError("explicit user approval is required")
    path = Path(args.registry)
    registry = read_typed_registry(path, POSTER_KIND)
    template = registry["templates"].get(args.id)
    if not template:
        raise ValueError(f"unknown template id: {args.id}")
    template["status"] = "confirmed"
    template["confirmed_at"] = datetime.now(timezone.utc).isoformat()
    save_registry(path, registry)
    print(json.dumps({
        "confirmed": args.id,
        "default_template_id": registry["default_template_id"],
        "revision": registry["revision"],
    }, ensure_ascii=False, indent=2))


def poster_template_set_default(args: argparse.Namespace) -> None:
    path = Path(args.registry)
    registry = read_typed_registry(path, POSTER_KIND)
    require_confirmed_template(registry, args.id)
    registry["default_template_id"] = args.id
    save_registry(path, registry)
    print(json.dumps({
        "default_template_id": args.id,
        "revision": registry["revision"],
    }, ensure_ascii=False, indent=2))


def poster_rule_matches(rule: dict[str, Any], course: dict[str, Any]) -> bool:
    match = rule["match"]
    if match.get("course_key") and match["course_key"] != normalize_title(
        course.get("course_title", "")
    ):
        return False
    if match.get("class_key") and match["class_key"] != normalize_title(
        course.get("class_name", "")
    ):
        return False
    if match.get("delivery") and match["delivery"] != course.get("delivery"):
        return False
    return True


def poster_rule_specificity(rule: dict[str, Any]) -> int:
    match = rule["match"]
    return (
        (4 if match.get("course_key") else 0)
        + (2 if match.get("class_key") else 0)
        + (1 if match.get("delivery") else 0)
    )


def resolve_poster_template(
    registry: dict[str, Any],
    course: dict[str, Any],
    explicit_id: str | None,
) -> dict[str, Any]:
    if explicit_id:
        return selection_record(registry, explicit_id, "explicit")
    matches = [
        rule
        for rule in registry.get("rules", [])
        if poster_rule_matches(rule, course)
    ]
    if matches:
        best = max(poster_rule_specificity(rule) for rule in matches)
        winners = [
            rule for rule in matches
            if poster_rule_specificity(rule) == best
        ]
        template_ids = {rule["template_id"] for rule in winners}
        if len(template_ids) != 1:
            raise ValueError(
                f"equal-specificity poster template conflict for "
                f"{course.get('course_title')}: {sorted(template_ids)}"
            )
        template_id = next(iter(template_ids))
        source = "rule:" + ",".join(rule["rule_id"] for rule in winners)
        return selection_record(registry, template_id, source)
    return selection_record(
        registry,
        registry["default_template_id"],
        "default",
    )


def poster_template_assign(args: argparse.Namespace) -> None:
    path = Path(args.registry)
    registry = read_typed_registry(path, POSTER_KIND)
    require_confirmed_template(registry, args.id)
    if not any((args.course_title, args.class_name, args.delivery)):
        raise ValueError("at least one selector is required")
    selector = {
        "course_title": args.course_title,
        "course_key": normalize_title(args.course_title or ""),
        "class_name": args.class_name,
        "class_key": normalize_title(args.class_name or ""),
        "delivery": args.delivery,
    }
    compact = {
        "course_key": selector["course_key"],
        "class_key": selector["class_key"],
        "delivery": selector["delivery"],
    }
    existing = [
        rule
        for rule in registry.get("rules", [])
        if {
            key: rule.get("match", {}).get(key)
            for key in compact
        } == compact
    ]
    if existing and not args.replace:
        raise ValueError("an identical selector exists; use --replace")
    if existing:
        registry["rules"] = [
            rule for rule in registry["rules"]
            if rule not in existing
        ]
    numbers = []
    for rule in registry.get("rules", []):
        match = re.fullmatch(r"rule-(\d+)", rule.get("rule_id", ""))
        if match:
            numbers.append(int(match.group(1)))
    rule = {
        "rule_id": f"rule-{max(numbers, default=0) + 1:04d}",
        "template_id": args.id,
        "match": selector,
    }
    registry.setdefault("rules", []).append(rule)
    save_registry(path, registry)
    print(json.dumps(rule, ensure_ascii=False, indent=2))


def registry_list(args: argparse.Namespace) -> None:
    registry = read_typed_registry(Path(args.registry), args.kind)
    print(json.dumps(registry, ensure_ascii=False, indent=2))


def separated_template_plan(args: argparse.Namespace) -> None:
    text_registry = read_typed_registry(Path(args.text_registry), TEXT_KIND)
    poster_registry = read_typed_registry(Path(args.poster_registry), POSTER_KIND)
    manifest = read_json(Path(args.manifest))
    previous = {
        "text": manifest.get("text_template_selection"),
        "poster": [
            course.get("poster_template_selection")
            for course in manifest.get("courses", [])
        ],
    }
    text_id = (
        manifest.get("requested_text_template_id")
        or text_registry["default_template_id"]
    )
    manifest["text_template_selection"] = selection_record(
        text_registry,
        text_id,
        "explicit" if manifest.get("requested_text_template_id") else "default",
    )
    manifest["document_template_id"] = text_id
    for course in manifest.get("courses", []):
        course["course_key"] = course.get("course_key") or course_key_for(course)
        resolved = resolve_poster_template(
            poster_registry,
            course,
            course.get("requested_poster_template_id"),
        )
        course["poster_template_selection"] = resolved
        course["template_selection"] = resolved  # compatibility with legacy helper
    current = {
        "text": manifest.get("text_template_selection"),
        "poster": [
            course.get("poster_template_selection")
            for course in manifest.get("courses", [])
        ],
    }
    if previous != current:
        approval = manifest.setdefault("approval", {})
        approval["phase1_status"] = "pending"
        approval["approved_at"] = None
        approval["phase1_content_hash"] = None
        approval["poster_status"] = "pending"
        approval["poster_approved_at"] = None
        approval["poster_content_hash"] = None
    write_json(Path(args.out), manifest)
    print(Path(args.out).resolve())


def read_settings(path: Path) -> dict[str, Any]:
    settings = read_json(path)
    if settings.get("schema_version") != SETTINGS_SCHEMA_VERSION:
        raise ValueError("project settings schema_version must be 1")
    if not settings.get("project_root"):
        raise ValueError("project_root is required in project settings")
    return settings


def settings_init(args: argparse.Namespace) -> None:
    path = Path(args.settings)
    if path.exists():
        raise ValueError(f"settings already exist: {path}")
    write_json(path, {
        "schema_version": SETTINGS_SCHEMA_VERSION,
        "revision": 1,
        "project_root": str(Path(args.root).resolve()),
        "teacher_asset_folder": None,
        "poster_psd_output_folder": None,
        "poster_psd_output_folders": {},
        "course_alias_registry": None,
    })
    print(path.resolve())


def teacher_folder_set(args: argparse.Namespace) -> None:
    path = Path(args.settings)
    settings = read_settings(path)
    root = Path(settings["project_root"])
    folder = resolve_path(root, args.folder)
    assert folder is not None
    require_directory(folder)
    settings["teacher_asset_folder"] = portable_path(root, folder)
    settings["revision"] = int(settings.get("revision", 0)) + 1
    write_json(path, settings)
    print(json.dumps({
        "teacher_asset_folder": settings["teacher_asset_folder"],
        "revision": settings["revision"],
    }, ensure_ascii=False, indent=2))


def poster_psd_folder_set(args: argparse.Namespace) -> None:
    path = Path(args.settings)
    settings = read_settings(path)
    root = Path(settings["project_root"]).resolve()
    folder = resolve_path(root, args.folder)
    assert folder is not None
    folder = folder.resolve()
    if folder == root:
        raise ValueError("poster PSD output folder cannot be the project root")
    if folder.exists() and not folder.is_dir():
        raise NotADirectoryError(folder)
    folder.mkdir(parents=True, exist_ok=True)
    portable = portable_path(root, folder)
    template_id = str(getattr(args, "template_id", "") or "").strip()
    if template_id:
        mappings = settings.setdefault("poster_psd_output_folders", {})
        if not isinstance(mappings, dict):
            raise ValueError("poster_psd_output_folders must be an object")
        mappings[template_id] = portable
    else:
        settings["poster_psd_output_folder"] = portable
    settings["revision"] = int(settings.get("revision", 0)) + 1
    write_json(path, settings)
    print(json.dumps({
        "template_id": template_id or None,
        "poster_psd_output_folder": portable,
        "revision": settings["revision"],
    }, ensure_ascii=False, indent=2))


def course_alias_registry_set(args: argparse.Namespace) -> None:
    path = Path(args.settings)
    settings = read_settings(path)
    root = Path(settings["project_root"]).resolve()
    registry = resolve_path(root, args.registry)
    assert registry is not None
    require_file(registry, {".json"})
    data = read_json(registry)
    if data.get("schema_version") != 1 or not isinstance(data.get("aliases"), list):
        raise ValueError("invalid course alias registry")
    settings["course_alias_registry"] = portable_path(root, registry)
    settings["revision"] = int(settings.get("revision", 0)) + 1
    write_json(path, settings)
    print(json.dumps({
        "course_alias_registry": settings["course_alias_registry"],
        "revision": settings["revision"],
    }, ensure_ascii=False, indent=2))


def configured_poster_psd_folder(
    settings: dict[str, Any], template_id: str | None = None
) -> Path:
    mappings = settings.get("poster_psd_output_folders") or {}
    if not isinstance(mappings, dict):
        raise ValueError("poster_psd_output_folders must be an object")
    value = mappings.get(template_id) if template_id else None
    if not value:
        value = settings.get("poster_psd_output_folder")
    if not value:
        raise ValueError(
            "poster_psd_output_folder is not configured; run poster-psd-folder-set"
        )
    root = Path(settings["project_root"]).resolve()
    folder = resolve_path(root, value)
    assert folder is not None
    folder = folder.resolve()
    if folder == root:
        raise ValueError("poster PSD output folder cannot be the project root")
    if folder.exists() and not folder.is_dir():
        raise NotADirectoryError(folder)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def safe_course_psd_stem(course_title: str) -> str:
    stem = unicodedata.normalize("NFKC", course_title).strip()
    stem = re.sub(r'[<>:"/\\|?*]+', " ", stem)
    stem = re.sub(r"\s+", " ", stem).strip(" .")
    if not stem:
        raise ValueError("course title cannot produce an empty PSD filename")
    return stem


def inspected_title_texts(path: Path) -> tuple[dict[str, Any], list[str]]:
    inspection = read_json(path)
    if inspection.get("schema_version") != 1:
        raise ValueError("title inspection must use schema_version 1")
    layers = inspection.get("layers")
    if not isinstance(layers, list):
        raise ValueError("title inspection is missing layers[]")
    texts = [
        str(layer.get("text", "")).strip()
        for layer in layers
        if layer.get("visible", True)
        and layer.get("kind") == "LayerKind.TEXT"
        and str(layer.get("text", "")).strip()
    ]
    if not texts:
        raise ValueError("title inspection has no visible text layer")
    return inspection, texts


def require_exact_inspected_course_title(
    inspection_path: Path,
    inspected_psd: Path,
    course_title: str,
) -> dict[str, Any]:
    inspection, texts = inspected_title_texts(inspection_path)
    inspected_source = Path(str(inspection.get("source_psd", ""))).resolve()
    if inspected_source != inspected_psd.resolve():
        raise ValueError(
            "title inspection source PSD does not match the selected course PSD"
        )
    target = normalize_title(course_title)
    exact = [text for text in texts if normalize_title(text) == target]
    match_type = "single_visible_text_layer"
    matched_text = exact[0] if len(exact) == 1 else None
    matched_layer_ids: list[int] | None = None
    if len(exact) != 1:
        fragments = inspection.get("title_fragments")
        if not isinstance(fragments, list) or len(fragments) < 2:
            raise ValueError(
                "selected PSD must contain one exact visible title text layer or "
                "an ordered title_fragments inspection for a multi-row title; "
                f"found single-layer matches {exact!r}"
            )
        if any(not isinstance(item, dict) or item.get("visible") is not True for item in fragments):
            raise ValueError("every inspected title fragment must be a visible layer")
        try:
            matched_layer_ids = [int(item["layer_id"]) for item in fragments]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("every inspected title fragment needs a numeric layer_id") from exc
        if len(set(matched_layer_ids)) != len(matched_layer_ids):
            raise ValueError("title fragment layer IDs must be unique")
        matched_text = "".join(str(item.get("text", "")) for item in fragments)
        if normalize_title(matched_text) != target:
            raise ValueError(
                "ordered visible title fragments do not exactly reconstruct the "
                f"course title: {matched_text!r}"
            )
        inspected_hash = str(inspection.get("source_sha256", "")).lower()
        actual_hash = sha256_file(inspected_psd)
        if inspected_hash != actual_hash:
            raise ValueError("multi-row title inspection PSD hash does not match the selected PSD")
        match_type = "ordered_visible_title_fragments"
    return {
        "inspection_file": str(inspection_path.resolve()),
        "inspected_psd": str(inspected_psd.resolve()),
        "course_title": course_title,
        "matched_text": matched_text,
        "matched_layer_ids": matched_layer_ids,
        "match_type": match_type,
        "normalized_title": target,
        "exact_match": True,
    }


def poster_psd_publish(args: argparse.Namespace) -> None:
    settings = read_settings(Path(args.settings))
    template_id = str(getattr(args, "template_id", "") or "").strip() or None
    output_folder = configured_poster_psd_folder(settings, template_id)
    source = Path(args.source_psd).resolve()
    poster = Path(args.poster_png).resolve()
    inspection_path = Path(args.title_inspection).resolve()
    course_title = str(args.course_title).strip()
    require_file(source, {".psd"})
    require_file(poster, {".png"})
    require_file(inspection_path, {".json"})
    if not course_title:
        raise ValueError("course title is required")

    existing_value = getattr(args, "existing_psd", None)
    if existing_value:
        destination = Path(existing_value).resolve()
        require_file(destination, {".psd"})
        try:
            destination.relative_to(output_folder)
        except ValueError as exc:
            raise ValueError(
                "existing course PSD must be inside poster_psd_output_folder"
            ) from exc
        title_match = require_exact_inspected_course_title(
            inspection_path, destination, course_title
        )
        source_hash = sha256_file(source)
        destination_hash = sha256_file(destination)
        status = "reused_existing_course_psd"
    else:
        title_match = require_exact_inspected_course_title(
            inspection_path, source, course_title
        )
        destination = (
            output_folder / f"{safe_course_psd_stem(course_title)}.psd"
        ).resolve()
        source_hash = sha256_file(source)
        if destination == source:
            destination_hash = source_hash
            status = "already_in_output_folder"
        elif destination.exists():
            if not destination.is_file():
                raise ValueError(f"PSD destination is not a file: {destination}")
            destination_hash = sha256_file(destination)
            if destination_hash != source_hash:
                raise FileExistsError(
                    "a PSD already occupies the canonical course filename; inspect "
                    "it and pass --existing-psd when it is the exact course PSD: "
                    f"{destination}"
                )
            status = "already_published_course_psd"
        else:
            shutil.copy2(source, destination)
            destination_hash = sha256_file(destination)
            if destination_hash != source_hash:
                destination.unlink(missing_ok=True)
                raise IOError("published course PSD hash verification failed")
            status = "published_new_course_psd"

    result = {
        "schema_version": 2,
        "status": status,
        "course_title": course_title,
        "source_psd": str(source),
        "final_poster_png": str(poster),
        "course_psd": str(destination),
        "published_psd": str(destination),
        "source_sha256": source_hash,
        "course_psd_sha256": destination_hash,
        "title_match": title_match,
        "settings_revision": settings.get("revision"),
        "template_id": template_id,
        "published_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if args.out:
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def poster_batch_preflight(args: argparse.Namespace) -> None:
    settings = read_settings(Path(args.settings))
    index = read_json(Path(args.poster_index))
    items_value = index.get("posters")
    if index.get("schema_version") != 1 or not isinstance(items_value, list):
        raise ValueError("poster index must use schema_version 1 and posters[]")
    if not items_value:
        raise ValueError("poster index contains no posters")
    items: list[dict[str, Any]] = []
    errors: list[str] = []
    title_to_psd: dict[str, Path] = {}
    psd_to_title: dict[Path, str] = {}
    for raw in items_value:
        course_title = str(raw.get("course_title", "")).strip()
        source = Path(str(raw.get("working_psd", ""))).resolve()
        poster = Path(str(raw.get("output_png", ""))).resolve()
        destination = Path(str(raw.get("output_psd", ""))).resolve()
        action = str(raw.get("psd_storage_action", ""))
        template_id = str(raw.get("template_id", "") or "").strip() or None
        output_folder = configured_poster_psd_folder(settings, template_id)
        item: dict[str, Any] = {
            "course_title": course_title,
            "poster_png": str(poster),
            "source_psd": str(source),
            "course_psd": str(destination),
            "psd_storage_action": action,
            "template_id": template_id,
            "poster_psd_output_folder": str(output_folder),
        }
        if not course_title:
            item["status"] = "missing_course_title"
            errors.append(str(raw.get("course_key") or raw))
        elif not poster.is_file() or poster.suffix.lower() != ".png" or poster.stat().st_size <= 0:
            item["status"] = "missing_poster_png"
            errors.append(str(poster))
        elif not source.is_file() or source.suffix.lower() != ".psd" or source.stat().st_size <= 0:
            item["status"] = "missing_working_psd"
            errors.append(str(source))
        else:
            source_hash = sha256_file(source)
            item["source_sha256"] = source_hash
            try:
                destination.relative_to(output_folder)
            except ValueError:
                item["status"] = "course_psd_outside_configured_folder"
                errors.append(str(destination))
            else:
                if raw.get("course_psd_title_match") not in {True, "passed"}:
                    item["status"] = "missing_exact_title_evidence"
                    errors.append(course_title)
                elif action == "reuse_existing":
                    if not destination.is_file() or destination.stat().st_size <= 0:
                        item["status"] = "missing_existing_course_psd"
                        errors.append(str(destination))
                    else:
                        item["status"] = "ready_reuse"
                        item["course_psd_sha256"] = sha256_file(destination)
                elif action == "publish_new":
                    expected = (
                        output_folder / f"{safe_course_psd_stem(course_title)}.psd"
                    ).resolve()
                    if destination != expected:
                        item["status"] = "noncanonical_new_course_psd_path"
                        errors.append(str(destination))
                    elif destination.exists():
                        item["status"] = "course_psd_already_exists_inspect_and_reuse"
                        errors.append(str(destination))
                    else:
                        item["status"] = "ready_publish_new"
                else:
                    item["status"] = "invalid_psd_storage_action"
                    errors.append(action or course_title)
        title_key = normalize_title(course_title)
        if title_key:
            prior_psd = title_to_psd.setdefault(title_key, destination)
            if prior_psd != destination:
                item["status"] = "one_course_maps_to_multiple_psds"
                errors.append(course_title)
            prior_title = psd_to_title.setdefault(destination, title_key)
            if prior_title != title_key:
                item["status"] = "one_psd_maps_to_multiple_courses"
                errors.append(str(destination))
        items.append(item)

    result = {
        "schema_version": 2,
        "valid": not errors and len(items) == len(items_value),
        "poster_count": len(items_value),
        "unique_course_psd_count": len(set(title_to_psd.values())),
        "items": items,
        "errors": errors,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if args.out:
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(2)


def poster_outputs_check(args: argparse.Namespace) -> None:
    settings = read_settings(Path(args.settings))
    cli_template_id = str(getattr(args, "template_id", "") or "").strip() or None
    psd_folder = configured_poster_psd_folder(settings, cli_template_id)
    poster_folder = Path(args.poster_folder).resolve()
    require_directory(poster_folder)
    posters = sorted(
        (path for path in poster_folder.iterdir() if path.suffix.lower() == ".png"),
        key=lambda path: path.name.casefold(),
    )
    if not posters:
        raise ValueError(f"no PNG posters found: {poster_folder}")

    manifest_value = getattr(args, "manifest", None)
    if manifest_value:
        manifest = read_json(Path(manifest_value))
        errors = validate_manifest(manifest, 2)
        expected_pngs: set[Path] = set()
        title_to_psd: dict[str, Path] = {}
        psd_to_title: dict[Path, str] = {}
        matched: list[dict[str, Any]] = []
        for course in manifest.get("courses") or []:
            label = course.get("course_key") or course.get("course_title")
            png_value = course.get("poster_output_png")
            psd_value = course.get("poster_output_psd")
            if not png_value or not psd_value:
                errors.append(f"{label}: poster output paths are missing")
                continue
            png = Path(png_value).resolve()
            psd = Path(psd_value).resolve()
            selection = course.get("poster_template_selection") or course.get("template_selection") or {}
            course_template_id = str(selection.get("template_id", "") or "").strip() or cli_template_id
            course_psd_folder = configured_poster_psd_folder(settings, course_template_id)
            expected_pngs.add(png)
            try:
                psd.relative_to(course_psd_folder)
            except ValueError:
                errors.append(
                    f"{label}: course PSD is outside configured folder for "
                    f"{course_template_id or 'legacy-default'}: {psd}"
                )
            if not png.is_file() or png.stat().st_size <= 0:
                errors.append(f"{label}: missing or empty PNG: {png}")
            if not psd.is_file() or psd.stat().st_size <= 0:
                errors.append(f"{label}: missing or empty course PSD: {psd}")
            title_key = normalize_title(str(course.get("course_title", "")))
            prior_psd = title_to_psd.setdefault(title_key, psd)
            if prior_psd != psd:
                errors.append(
                    f"{label}: one course title maps to multiple PSD files"
                )
            prior_title = psd_to_title.setdefault(psd, title_key)
            if prior_title != title_key:
                errors.append(
                    f"{label}: one course PSD maps to multiple course titles"
                )
            qa = course.get("poster_qa") or {}
            if qa.get("course_psd_title_match") not in {True, "passed"}:
                errors.append(f"{label}: exact internal course-title evidence is missing")
            matched.append({
                "course_key": label,
                "poster_png": str(png),
                "course_psd": str(psd),
                "course_psd_sha256": sha256_file(psd) if psd.is_file() else None,
                "template_id": course_template_id,
                "poster_psd_output_folder": str(course_psd_folder),
            })
        actual_png_set = {path.resolve() for path in posters}
        if actual_png_set != expected_pngs:
            missing_png = sorted(str(path) for path in expected_pngs - actual_png_set)
            extra_png = sorted(str(path) for path in actual_png_set - expected_pngs)
            if missing_png:
                errors.append("poster folder is missing manifest PNGs: " + " | ".join(missing_png))
            if extra_png:
                errors.append("poster folder has untracked PNGs: " + " | ".join(extra_png))
        result = {
            "schema_version": 2,
            "poster_folder": str(poster_folder),
            "poster_psd_output_folder": str(psd_folder),
            "png_count": len(posters),
            "course_mapping_count": len(matched),
            "unique_course_psd_count": len(set(title_to_psd.values())),
            "valid": not errors,
            "matched": matched,
            "errors": errors,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        if args.out:
            write_json(Path(args.out), result)
            print(Path(args.out).resolve())
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        if not result["valid"]:
            raise SystemExit(2)
        return

    matched: list[dict[str, Any]] = []
    missing: list[str] = []
    for poster in posters:
        psd = psd_folder / f"{poster.stem}.psd"
        if psd.is_file() and psd.stat().st_size > 0:
            matched.append({
                "poster_png": str(poster),
                "poster_psd": str(psd),
                "psd_sha256": sha256_file(psd),
            })
        else:
            missing.append(str(psd))

    result = {
        "schema_version": 1,
        "poster_folder": str(poster_folder),
        "poster_psd_output_folder": str(psd_folder),
        "png_count": len(posters),
        "matched_psd_count": len(matched),
        "valid": not missing and len(matched) == len(posters),
        "matched": matched,
        "missing_psd": missing,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    if args.out:
        write_json(Path(args.out), result)
        print(Path(args.out).resolve())
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(2)


def working_psd_cleanup(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise PermissionError(
            "working PSD cleanup requires explicit user approval"
        )
    manifest_path = Path(args.manifest).resolve()
    manifest = read_json(manifest_path)
    errors = validate_manifest(manifest, 2)
    if errors:
        raise ValueError("manifest validation failed: " + " | ".join(errors))
    completion = manifest.get("completion") or {}
    if completion.get("status") != "ready_for_delivery_check":
        raise ValueError(
            "manifest must be finalized before working PSD cleanup"
        )
    root = Path(manifest["root"]).resolve()
    target_date = str(manifest["target_date"])
    expected_run_dir = (root / "_course_preview_runs" / target_date).resolve()
    run_dir = Path(args.run_dir).resolve()
    if run_dir != expected_run_dir:
        raise ValueError(
            "cleanup run directory must exactly match "
            f"<project>/_course_preview_runs/{target_date}"
        )
    working_root = (run_dir / "working-psd").resolve()
    try:
        working_root.relative_to(run_dir)
    except ValueError as exc:
        raise ValueError("working PSD folder escapes the run directory") from exc
    output_report = Path(args.out).resolve()
    try:
        output_report.relative_to(working_root)
    except ValueError:
        pass
    else:
        raise ValueError("cleanup report cannot be written inside working-psd")

    for course in manifest.get("courses") or []:
        label = course.get("course_key") or course.get("course_title")
        for field, suffix in (
            ("poster_output_png", ".png"),
            ("poster_output_psd", ".psd"),
        ):
            value = course.get(field)
            if not value:
                raise ValueError(f"{label}: {field} is missing before cleanup")
            require_file(Path(value).resolve(), {suffix})
        qa = course.get("poster_qa") or {}
        if qa.get("full_poster_review") not in {True, "passed"}:
            raise ValueError(f"{label}: full poster review has not passed")
        if qa.get("course_psd_title_match") not in {True, "passed"}:
            raise ValueError(f"{label}: exact course PSD title match is missing")
        if qa.get("publish_status") not in {
            "reused_existing_course_psd",
            "published_new_course_psd",
            "already_published_course_psd",
            "already_in_output_folder",
        }:
            raise ValueError(f"{label}: course PSD storage is incomplete")

    candidates: list[Path] = []
    if working_root.exists():
        require_directory(working_root)
        candidates = sorted(
            (
                path.resolve()
                for path in working_root.rglob("*")
                if path.is_file() and path.suffix.lower() in {".psd", ".psb"}
            ),
            key=lambda path: str(path).casefold(),
        )
    deleted: list[dict[str, Any]] = []
    for path in candidates:
        try:
            path.relative_to(working_root)
        except ValueError as exc:
            raise ValueError(f"refusing to delete outside working-psd: {path}") from exc
        deleted.append({
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })
        path.unlink()

    if working_root.exists():
        directories = sorted(
            (path for path in working_root.rglob("*") if path.is_dir()),
            key=lambda path: len(path.parts),
            reverse=True,
        )
        for directory in directories:
            if not any(directory.iterdir()):
                directory.rmdir()

    result = {
        "schema_version": 1,
        "status": "cleaned" if deleted else "already_clean",
        "user_approved": True,
        "manifest": str(manifest_path),
        "run_dir": str(run_dir),
        "working_psd_folder": str(working_root),
        "deleted_count": len(deleted),
        "deleted_bytes": sum(item["bytes"] for item in deleted),
        "deleted": deleted,
        "cleaned_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(output_report, result)
    print(output_report)


def _safe_within(path: Path, parent: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(parent.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes its approved root: {resolved}") from exc
    if resolved == parent.resolve():
        raise ValueError(f"{label} cannot equal its approved root: {resolved}")
    return resolved


def _windows_photoshop_running() -> bool:
    if os.name != "nt":
        return False
    completed = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq Photoshop.exe", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        errors="replace",
        check=False,
    )
    return "photoshop.exe" in completed.stdout.casefold()


def _photoshop_temp_roots(root: Path) -> list[Path]:
    values = [Path(tempfile.gettempdir())]
    if os.name == "nt":
        values.append(Path(root.drive + "\\"))
    result: list[Path] = []
    for value in values:
        resolved = value.resolve()
        if resolved not in result:
            result.append(resolved)
    return result


def _photoshop_temp_files(root: Path) -> list[Path]:
    candidates: dict[str, Path] = {}
    for temp_root in _photoshop_temp_roots(root):
        if not temp_root.is_dir():
            continue
        for pattern in ("Photoshop Temp*", "~PST*.tmp"):
            for path in temp_root.glob(pattern):
                if path.is_file():
                    candidates[str(path.resolve()).casefold()] = path.resolve()
    return sorted(candidates.values(), key=lambda item: str(item).casefold())


def run_cleanup_baseline(args: argparse.Namespace) -> None:
    run_dir = Path(args.run_dir).resolve()
    root = Path(args.project_root).resolve()
    _safe_within(run_dir, root / "_course_preview_runs", "run directory")
    run_dir.mkdir(parents=True, exist_ok=True)
    output = Path(args.out).resolve()
    _safe_within(output, run_dir, "cleanup baseline report")
    files = [
        {
            "path": str(path),
            "bytes": path.stat().st_size,
            "mtime_ns": path.stat().st_mtime_ns,
            "sha256": sha256_file(path),
        }
        for path in _photoshop_temp_files(root)
    ]
    result = {
        "schema_version": 1,
        "project_root": str(root),
        "run_dir": str(run_dir),
        "photoshop_temp_roots": [str(path) for path in _photoshop_temp_roots(root)],
        "baseline_files": files,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    write_json(output, result)
    print(output)


def final_run_cleanup(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise PermissionError("final run cleanup requires explicit user approval")
    manifest_path = Path(args.manifest).resolve()
    manifest = read_json(manifest_path)
    errors = validate_manifest(manifest, 2)
    if errors:
        raise ValueError("manifest validation failed: " + " | ".join(errors))
    completion = manifest.get("completion") or {}
    if completion.get("status") not in {
        "ready_for_delivery_check",
        "delivery_checked",
        "complete",
    }:
        raise ValueError("manifest must be finalized before final run cleanup")
    root = Path(manifest["root"]).resolve()
    target_date = str(manifest["target_date"])
    expected_run_dir = (root / "_course_preview_runs" / target_date).resolve()
    run_dir = Path(args.run_dir).resolve()
    if run_dir != expected_run_dir:
        raise ValueError(
            "cleanup run directory must exactly match "
            f"<project>/_course_preview_runs/{target_date}"
        )
    _safe_within(run_dir, root / "_course_preview_runs", "run directory")
    baseline_path = Path(args.baseline).resolve()
    _safe_within(baseline_path, run_dir, "cleanup baseline report")
    baseline = read_json(baseline_path)
    if Path(baseline.get("project_root", "")).resolve() != root:
        raise ValueError("cleanup baseline project root does not match manifest")
    if Path(baseline.get("run_dir", "")).resolve() != run_dir:
        raise ValueError("cleanup baseline run directory does not match manifest")

    protected_files: list[dict[str, Any]] = []
    for course in manifest.get("courses") or []:
        label = course.get("course_key") or course.get("course_title")
        for field, suffix in (("poster_output_png", ".png"), ("poster_output_psd", ".psd")):
            value = course.get(field)
            if not value:
                raise ValueError(f"{label}: {field} is missing before cleanup")
            path = Path(value).resolve()
            require_file(path, {suffix})
            protected_files.append({"path": str(path), "sha256": sha256_file(path)})
        qa = course.get("poster_qa") or {}
        if qa.get("full_poster_review") not in {True, "passed"}:
            raise ValueError(f"{label}: full poster review has not passed")
        if qa.get("course_psd_title_match") not in {True, "passed"}:
            raise ValueError(f"{label}: exact course PSD title match is missing")

    weekly = manifest.get("weekly_document") or {}
    weekly_path = Path(
        weekly.get("canonical_path")
        or completion.get("final_weekly_document")
        or ""
    ).resolve()
    require_file(weekly_path, {".docx"})
    protected_files.append({"path": str(weekly_path), "sha256": sha256_file(weekly_path)})

    poster_folder = Path(completion.get("poster_folder") or "").resolve()
    if not poster_folder.is_dir():
        raise ValueError("final poster folder is missing before cleanup")
    expected_pngs = {Path(course["poster_output_png"]).resolve() for course in manifest["courses"]}
    actual_pngs = {path.resolve() for path in poster_folder.glob("*.png") if path.is_file()}
    if actual_pngs != expected_pngs:
        raise ValueError("final poster folder does not match the sealed manifest")

    if _windows_photoshop_running():
        raise RuntimeError("Photoshop is still running; close it before final run cleanup")

    baseline_paths = {
        str(Path(item["path"]).resolve()).casefold()
        for item in baseline.get("baseline_files") or []
    }
    temp_deleted: list[dict[str, Any]] = []
    temp_skipped: list[dict[str, Any]] = []
    for path in _photoshop_temp_files(root):
        key = str(path.resolve()).casefold()
        if key in baseline_paths:
            temp_skipped.append({"path": str(path), "reason": "present_before_run"})
            continue
        record = {
            "path": str(path),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        try:
            path.unlink()
            temp_deleted.append(record)
        except OSError as exc:
            temp_skipped.append({"path": str(path), "reason": str(exc)})

    run_deleted: list[dict[str, Any]] = []
    if run_dir.exists():
        require_directory(run_dir)
        for path in sorted(
            (item for item in run_dir.rglob("*") if item.is_file()),
            key=lambda item: str(item).casefold(),
        ):
            run_deleted.append({
                "path": str(path),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            })

    output_report = Path(args.out).resolve()
    _safe_within(output_report, root / "_course_preview_runs", "cleanup report")
    try:
        output_report.relative_to(run_dir)
    except ValueError:
        pass
    else:
        raise ValueError("final cleanup report must be outside the run directory")
    output_report.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "schema_version": 1,
        "status": "cleaned",
        "user_approved": True,
        "manifest": str(manifest_path),
        "run_dir": str(run_dir),
        "run_deleted_count": len(run_deleted),
        "run_deleted_bytes": sum(item["bytes"] for item in run_deleted),
        "run_deleted": run_deleted,
        "photoshop_temp_deleted_count": len(temp_deleted),
        "photoshop_temp_deleted_bytes": sum(item["bytes"] for item in temp_deleted),
        "photoshop_temp_deleted": temp_deleted,
        "photoshop_temp_skipped": temp_skipped,
        "protected_deliverables": protected_files,
        "cleaned_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    temporary_report = output_report.with_name(output_report.name + ".tmp")
    write_json(temporary_report, report)
    shutil.rmtree(run_dir)
    temporary_report.replace(output_report)
    for item in protected_files:
        path = Path(item["path"])
        require_file(path)
        if sha256_file(path) != item["sha256"]:
            raise RuntimeError(f"protected deliverable changed during cleanup: {path}")
    print(output_report)


def normalize_teacher(value: str) -> str:
    text = unicodedata.normalize("NFKC", value).strip().lower()
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"老师$", "", text)
    return text


def teacher_filename_matches(teacher: str, path: Path) -> bool:
    key = normalize_teacher(teacher)
    stem = normalize_teacher(path.stem)
    if not key or not stem.startswith(key):
        return False
    suffix = stem[len(key):]
    if suffix == "":
        return True
    return bool(re.fullmatch(r"(?:\d+|[_-].+|形象.+|新版.*)", suffix))


def alpha_audit(path: Path) -> dict[str, Any]:
    require_file(path, {".png"})
    with Image.open(path) as image:
        width, height = image.size
        rgba = image.convert("RGBA")
        alpha = rgba.getchannel("A")
        histogram = alpha.histogram()
        total = width * height
        transparent = sum(histogram[:255])
        fully_transparent = histogram[0]
        return {
            "file": str(path),
            "width": width,
            "height": height,
            "mode": image.mode,
            "has_alpha_channel": "A" in image.getbands(),
            "transparent_pixel_ratio": round(transparent / total, 6),
            "fully_transparent_pixel_ratio": round(
                fully_transparent / total,
                6,
            ),
            "requires_visual_background_check": True,
        }


def teacher_candidates(
    folder: Path,
    teacher: str,
) -> list[Path]:
    return sorted(
        path
        for path in folder.rglob("*.png")
        if "_原图备份" not in path.parts
        and teacher_filename_matches(teacher, path)
    )


def candidate_record(folder: Path, path: Path) -> dict[str, Any]:
    return {
        "file_name": path.name,
        "relative_path": str(path.relative_to(folder)),
        "alpha_audit": alpha_audit(path),
    }


def resolve_teacher_asset(
    folder: Path,
    course: dict[str, Any],
    settings_revision: int,
) -> dict[str, Any]:
    teacher = str(course.get("teacher") or "")
    explicit = course.get("requested_teacher_asset_filename")
    if not course.get("teacher_asset_required") and not explicit:
        return {
            "status": "not_required_existing_template",
            "file_name": None,
            "relative_path": None,
            "selection_source": "manifest_not_required",
            "settings_revision": settings_revision,
            "alpha_audit": None,
            "candidates": [],
        }
    if not str(course.get("teacher_asset_reason") or "").strip():
        raise ValueError(
            f"{teacher}: teacher_asset_reason is required when a portrait is required"
        )
    candidates = teacher_candidates(folder, teacher)
    records = [candidate_record(folder, path) for path in candidates]
    if explicit:
        exact = [path for path in candidates if path.name == explicit]
        if len(exact) != 1:
            raise ValueError(
                f"{teacher}: requested file name must identify exactly one PNG: "
                f"{explicit}"
            )
        chosen = exact[0]
        return {
            "status": "selected",
            "file_name": chosen.name,
            "relative_path": str(chosen.relative_to(folder)),
            "selection_source": "explicit_filename",
            "settings_revision": settings_revision,
            "alpha_audit": alpha_audit(chosen),
            "candidates": records,
        }
    if len(candidates) == 1:
        chosen = candidates[0]
        return {
            "status": "selected",
            "file_name": chosen.name,
            "relative_path": str(chosen.relative_to(folder)),
            "selection_source": "single_exact_teacher_match",
            "settings_revision": settings_revision,
            "alpha_audit": alpha_audit(chosen),
            "candidates": records,
        }
    if len(candidates) > 1:
        return {
            "status": "pending_user_filename",
            "file_name": None,
            "relative_path": None,
            "selection_source": "multiple_exact_teacher_matches",
            "settings_revision": settings_revision,
            "alpha_audit": None,
            "candidates": records,
        }
    return {
        "status": "missing",
        "file_name": None,
        "relative_path": None,
        "selection_source": "no_exact_teacher_match",
        "settings_revision": settings_revision,
        "alpha_audit": None,
        "candidates": [],
    }


def teacher_assets_plan(args: argparse.Namespace) -> None:
    settings = read_settings(Path(args.settings))
    folder_value = settings.get("teacher_asset_folder")
    if not folder_value:
        raise ValueError(
            "teacher asset folder is not configured; ask the user to provide it"
        )
    root = Path(settings["project_root"])
    folder = resolve_path(root, folder_value)
    assert folder is not None
    require_directory(folder)
    manifest = read_json(Path(args.manifest))
    previous = [
        course.get("teacher_asset_selection")
        for course in manifest.get("courses", [])
    ]
    for course in manifest.get("courses", []):
        course["teacher_asset_selection"] = resolve_teacher_asset(
            folder,
            course,
            int(settings.get("revision", 0)),
        )
    current = [
        course.get("teacher_asset_selection")
        for course in manifest.get("courses", [])
    ]
    if previous != current:
        approval = manifest.setdefault("approval", {})
        approval["poster_status"] = "pending"
        approval["poster_approved_at"] = None
        approval["poster_content_hash"] = None
    manifest["project_settings_revision"] = settings.get("revision")
    manifest["teacher_asset_folder"] = portable_path(root, folder)
    write_json(Path(args.out), manifest)
    print(Path(args.out).resolve())


def teacher_asset_select(args: argparse.Namespace) -> None:
    settings = read_settings(Path(args.settings))
    folder_value = settings.get("teacher_asset_folder")
    if not folder_value:
        raise ValueError("teacher asset folder is not configured")
    root = Path(settings["project_root"])
    folder = resolve_path(root, folder_value)
    assert folder is not None
    manifest = read_json(Path(args.manifest))
    teacher_key = normalize_teacher(args.teacher)
    changed = 0
    for course in manifest.get("courses", []):
        if normalize_teacher(str(course.get("teacher") or "")) != teacher_key:
            continue
        course["teacher_asset_required"] = True
        course["teacher_asset_reason"] = (
            course.get("teacher_asset_reason")
            or "user selected a replacement portrait"
        )
        course["requested_teacher_asset_filename"] = args.file_name
        course["teacher_asset_selection"] = resolve_teacher_asset(
            folder,
            course,
            int(settings.get("revision", 0)),
        )
        changed += 1
    if changed == 0:
        raise ValueError(f"teacher does not occur in manifest: {args.teacher}")
    approval = manifest.setdefault("approval", {})
    approval["poster_status"] = "pending"
    approval["poster_approved_at"] = None
    approval["poster_content_hash"] = None
    write_json(Path(args.out), manifest)
    print(json.dumps({
        "teacher": args.teacher,
        "file_name": args.file_name,
        "courses_updated": changed,
        "out": str(Path(args.out).resolve()),
    }, ensure_ascii=False, indent=2))


def teacher_asset_require(args: argparse.Namespace) -> None:
    manifest = read_json(Path(args.manifest))
    teacher_key = normalize_teacher(args.teacher)
    changed = 0
    for course in manifest.get("courses", []):
        if normalize_teacher(str(course.get("teacher") or "")) != teacher_key:
            continue
        course["teacher_asset_required"] = True
        course["teacher_asset_reason"] = args.reason
        course["requested_teacher_asset_filename"] = None
        course["teacher_asset_selection"] = None
        changed += 1
    if changed == 0:
        raise ValueError(f"teacher does not occur in manifest: {args.teacher}")
    approval = manifest.setdefault("approval", {})
    approval["poster_status"] = "pending"
    approval["poster_approved_at"] = None
    approval["poster_content_hash"] = None
    write_json(Path(args.out), manifest)
    print(json.dumps({
        "teacher": args.teacher,
        "reason": args.reason,
        "courses_updated": changed,
        "out": str(Path(args.out).resolve()),
    }, ensure_ascii=False, indent=2))


def alpha_audit_command(args: argparse.Namespace) -> None:
    print(json.dumps(
        alpha_audit(Path(args.image)),
        ensure_ascii=False,
        indent=2,
    ))


def cutout_commit(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise ValueError("explicit user approval is required before replacement")
    settings = read_settings(Path(args.settings))
    root = Path(settings["project_root"])
    folder_value = settings.get("teacher_asset_folder")
    if not folder_value:
        raise ValueError("teacher asset folder is not configured")
    folder = resolve_path(root, folder_value)
    assert folder is not None
    folder = folder.resolve()
    original = Path(args.original).resolve()
    processed = Path(args.processed).resolve()
    try:
        original.relative_to(folder)
    except ValueError as exc:
        raise ValueError("original must be inside the configured teacher folder") from exc
    require_file(original, {".png"})
    require_file(processed, {".png"})
    original_audit = alpha_audit(original)
    processed_audit = alpha_audit(processed)
    if (
        original_audit["width"],
        original_audit["height"],
    ) != (
        processed_audit["width"],
        processed_audit["height"],
    ):
        raise ValueError("processed cutout must preserve the original canvas size")
    if processed_audit["transparent_pixel_ratio"] <= 0:
        raise ValueError("processed PNG still has no transparent pixels")
    backup_dir = folder / "_原图备份"
    backup_dir.mkdir(parents=True, exist_ok=True)
    original_hash = sha256_file(original)
    backup = backup_dir / (
        f"{original.stem}_原图_{original_hash[:8]}{original.suffix.lower()}"
    )
    if not backup.exists():
        shutil.copy2(original, backup)
    temp_handle = tempfile.NamedTemporaryFile(
        prefix=f".{original.stem}_cutout_",
        suffix=".png",
        dir=original.parent,
        delete=False,
    )
    temp_path = Path(temp_handle.name)
    temp_handle.close()
    try:
        shutil.copy2(processed, temp_path)
        if sha256_file(temp_path) != sha256_file(processed):
            raise ValueError("temporary cutout copy failed hash verification")
        os.replace(temp_path, original)
    finally:
        if temp_path.exists():
            temp_path.unlink()
    print(json.dumps({
        "replaced": str(original),
        "backup": str(backup),
        "original_sha256": original_hash,
        "new_sha256": sha256_file(original),
        "alpha_audit": alpha_audit(original),
    }, ensure_ascii=False, indent=2))


def poster_payload(data: dict[str, Any]) -> dict[str, Any]:
    payload = phase1_payload(data)
    payload["courses"] = []
    for course in data.get("courses", []):
        payload["courses"].append({
            "class_name": course.get("class_name"),
            "course_title": course.get("course_title"),
            "teacher": course.get("teacher"),
            "delivery": course.get("delivery"),
            "time": course.get("time"),
            "details": course.get("details"),
            "poster_template_selection": (
                course.get("poster_template_selection")
                or course.get("template_selection")
            ),
            "teacher_asset_selection": course.get("teacher_asset_selection"),
        })
    payload["project_settings_revision"] = data.get("project_settings_revision")
    return payload


def poster_fingerprint(data: dict[str, Any]) -> str:
    raw = json.dumps(
        poster_payload(data),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def phase1_approve(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise ValueError("explicit user approval is required")
    manifest = read_json(Path(args.manifest))
    errors = validate_manifest(manifest, 1)
    if errors:
        raise ValueError("invalid Stage A manifest: " + "; ".join(errors))
    approval = manifest.setdefault("approval", {})
    approval["phase1_status"] = "approved"
    approval["approved_at"] = datetime.now(timezone.utc).isoformat()
    approval["phase1_content_hash"] = phase1_fingerprint(manifest)
    write_json(Path(args.out), manifest)
    print(json.dumps({
        "phase1_status": "approved",
        "phase1_content_hash": approval["phase1_content_hash"],
        "out": str(Path(args.out).resolve()),
    }, ensure_ascii=False, indent=2))


def approval_check(args: argparse.Namespace) -> None:
    manifest = read_json(Path(args.manifest))
    approval = manifest.get("approval", {})
    expected = approval.get("phase1_content_hash")
    actual = phase1_fingerprint(manifest)
    result = {
        "phase1_status": approval.get("phase1_status"),
        "stored_hash": expected,
        "actual_hash": actual,
        "valid": (
            approval.get("phase1_status") == "approved"
            and expected == actual
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(2)


def poster_approve(args: argparse.Namespace) -> None:
    if not args.user_approved:
        raise ValueError("explicit user approval is required")
    manifest = read_json(Path(args.manifest))
    errors = validate_manifest(manifest, 2)
    if errors:
        raise ValueError("invalid Stage B manifest: " + "; ".join(errors))
    unresolved = []
    for course in manifest.get("courses", []):
        selection = course.get("teacher_asset_selection")
        if not selection:
            unresolved.append(
                f"{course.get('teacher')}: teacher assets have not been planned"
            )
            continue
        if selection.get("status") not in {
            "selected",
            "not_required_existing_template",
        }:
            unresolved.append(
                f"{course.get('teacher')}: {selection.get('status')}"
            )
    if unresolved:
        raise ValueError("unresolved teacher assets: " + " | ".join(unresolved))
    approval = manifest.setdefault("approval", {})
    approval["poster_status"] = "approved"
    approval["poster_approved_at"] = datetime.now(timezone.utc).isoformat()
    approval["poster_content_hash"] = poster_fingerprint(manifest)
    write_json(Path(args.out), manifest)
    print(json.dumps({
        "poster_status": "approved",
        "poster_content_hash": approval["poster_content_hash"],
        "out": str(Path(args.out).resolve()),
    }, ensure_ascii=False, indent=2))


def poster_approval_check(args: argparse.Namespace) -> None:
    manifest = read_json(Path(args.manifest))
    approval = manifest.get("approval", {})
    expected = approval.get("poster_content_hash")
    actual = poster_fingerprint(manifest)
    result = {
        "poster_status": approval.get("poster_status"),
        "stored_hash": expected,
        "actual_hash": actual,
        "valid": (
            approval.get("poster_status") == "approved"
            and expected == actual
        ),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise SystemExit(2)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    cmd = sub.add_parser("registry-list")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--kind", required=True, choices=(TEXT_KIND, POSTER_KIND))
    cmd.set_defaults(func=registry_list)

    cmd = sub.add_parser("text-template-add")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.add_argument("--name", required=True)
    cmd.add_argument("--source-docx", required=True)
    cmd.add_argument("--executable-template", required=True)
    cmd.add_argument("--contract", required=True)
    cmd.add_argument("--usage-guide", required=True)
    cmd.add_argument("--sample-docx", required=True)
    cmd.add_argument("--notes")
    cmd.set_defaults(func=text_template_add)

    cmd = sub.add_parser("text-template-confirm")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=text_template_confirm)

    cmd = sub.add_parser("text-template-set-default")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.set_defaults(func=text_template_set_default)

    cmd = sub.add_parser("poster-template-add")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.add_argument("--name", required=True)
    cmd.add_argument("--poster-source", action="append")
    cmd.add_argument("--layer-contract")
    cmd.add_argument("--notes")
    cmd.set_defaults(func=poster_template_add)

    cmd = sub.add_parser("poster-template-confirm")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=poster_template_confirm)

    cmd = sub.add_parser("poster-template-set-default")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.set_defaults(func=poster_template_set_default)

    cmd = sub.add_parser("poster-template-assign")
    cmd.add_argument("--registry", required=True)
    cmd.add_argument("--id", required=True)
    cmd.add_argument("--course-title")
    cmd.add_argument("--class-name")
    cmd.add_argument("--delivery", choices=tuple(sorted(DELIVERIES)))
    cmd.add_argument("--replace", action="store_true")
    cmd.set_defaults(func=poster_template_assign)

    cmd = sub.add_parser("template-plan")
    cmd.add_argument("--text-registry", required=True)
    cmd.add_argument("--poster-registry", required=True)
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--out", required=True)
    cmd.set_defaults(func=separated_template_plan)

    cmd = sub.add_parser("settings-init")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--root", required=True)
    cmd.set_defaults(func=settings_init)

    cmd = sub.add_parser("teacher-folder-set")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--folder", required=True)
    cmd.set_defaults(func=teacher_folder_set)

    cmd = sub.add_parser("poster-psd-folder-set")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--folder", required=True)
    cmd.add_argument("--template-id")
    cmd.set_defaults(func=poster_psd_folder_set)

    cmd = sub.add_parser("course-alias-registry-set")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--registry", required=True)
    cmd.set_defaults(func=course_alias_registry_set)

    cmd = sub.add_parser("poster-psd-publish")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--source-psd", required=True)
    cmd.add_argument("--poster-png", required=True)
    cmd.add_argument("--course-title", required=True)
    cmd.add_argument("--template-id")
    cmd.add_argument("--title-inspection", required=True)
    cmd.add_argument("--existing-psd")
    cmd.add_argument("--out")
    cmd.set_defaults(func=poster_psd_publish)

    cmd = sub.add_parser("poster-batch-preflight")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--poster-index", required=True)
    cmd.add_argument("--out")
    cmd.set_defaults(func=poster_batch_preflight)

    cmd = sub.add_parser("poster-outputs-check")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--poster-folder", required=True)
    cmd.add_argument("--template-id")
    cmd.add_argument("--manifest")
    cmd.add_argument("--out")
    cmd.set_defaults(func=poster_outputs_check)

    cmd = sub.add_parser("working-psd-cleanup")
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--run-dir", required=True)
    cmd.add_argument("--out", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=working_psd_cleanup)

    cmd = sub.add_parser("run-cleanup-baseline")
    cmd.add_argument("--project-root", required=True)
    cmd.add_argument("--run-dir", required=True)
    cmd.add_argument("--out", required=True)
    cmd.set_defaults(func=run_cleanup_baseline)

    cmd = sub.add_parser("final-run-cleanup")
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--run-dir", required=True)
    cmd.add_argument("--baseline", required=True)
    cmd.add_argument("--out", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=final_run_cleanup)

    cmd = sub.add_parser("teacher-assets-plan")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--out", required=True)
    cmd.set_defaults(func=teacher_assets_plan)

    cmd = sub.add_parser("teacher-asset-select")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--teacher", required=True)
    cmd.add_argument("--file-name", required=True)
    cmd.add_argument("--out", required=True)
    cmd.set_defaults(func=teacher_asset_select)

    cmd = sub.add_parser("teacher-asset-require")
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--teacher", required=True)
    cmd.add_argument("--reason", required=True)
    cmd.add_argument("--out", required=True)
    cmd.set_defaults(func=teacher_asset_require)

    cmd = sub.add_parser("alpha-audit")
    cmd.add_argument("--image", required=True)
    cmd.set_defaults(func=alpha_audit_command)

    cmd = sub.add_parser("cutout-commit")
    cmd.add_argument("--settings", required=True)
    cmd.add_argument("--original", required=True)
    cmd.add_argument("--processed", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=cutout_commit)

    cmd = sub.add_parser("phase1-approve")
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--out", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=phase1_approve)

    cmd = sub.add_parser("approval-check")
    cmd.add_argument("--manifest", required=True)
    cmd.set_defaults(func=approval_check)

    cmd = sub.add_parser("poster-approve")
    cmd.add_argument("--manifest", required=True)
    cmd.add_argument("--out", required=True)
    cmd.add_argument("--user-approved", action="store_true")
    cmd.set_defaults(func=poster_approve)

    cmd = sub.add_parser("poster-approval-check")
    cmd.add_argument("--manifest", required=True)
    cmd.set_defaults(func=poster_approval_check)

    return result


def main() -> None:
    args = parser().parse_args()
    try:
        args.func(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
