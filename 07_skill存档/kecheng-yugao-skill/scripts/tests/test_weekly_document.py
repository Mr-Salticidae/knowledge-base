from __future__ import annotations

import json
import sys
import tempfile
import unittest
import zipfile
from argparse import Namespace
from datetime import date
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from weekly_document import (  # noqa: E402
    check_weekly_document,
    publish_weekly_document,
    resolve_weekly_document,
)
from course_preview import init_manifest  # noqa: E402


START = date(2026, 8, 3)
END = date(2026, 8, 7)
CANONICAL = "8.3-8.7课程预告.docx"


def make_docx(path: Path, marker: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("word/document.xml", f"<document>{marker}</document>")


class WeeklyDocumentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.docs = self.root / "课程预告文本"
        self.docs.mkdir()
        self.run = self.root / "_course_preview_runs" / "2026-08-07"
        self.source = self.run / "drafts" / "stage-b-complete.docx"
        make_docx(self.source, "new")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_plan(self, plan: dict) -> Path:
        path = self.run / "weekly-document-plan.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return path

    def test_create_and_publish_canonical(self) -> None:
        plan = resolve_weekly_document(self.root, self.run, START, END)
        self.assertEqual(plan["mode"], "create")
        result = publish_weekly_document(self.write_plan(plan), self.source)
        self.assertEqual(result["same_week_docx_count"], 1)
        self.assertTrue((self.docs / CANONICAL).is_file())
        self.assertTrue(check_weekly_document(self.root, START, END)["valid"])

    def test_update_canonical_creates_backup(self) -> None:
        make_docx(self.docs / CANONICAL, "old")
        plan = resolve_weekly_document(self.root, self.run, START, END)
        self.assertEqual(plan["mode"], "update")
        result = publish_weekly_document(self.write_plan(plan), self.source)
        backup = Path(result["backup_folder"]) / CANONICAL
        self.assertTrue(backup.is_file())
        self.assertEqual(len(list(self.docs.glob("8.3-8.7课程预告*.docx"))), 1)

    def test_single_legacy_name_is_consolidated(self) -> None:
        legacy = self.docs / "8.3-8.7课程预告_8.7完整预告_FINAL.docx"
        make_docx(legacy, "legacy")
        plan = resolve_weekly_document(self.root, self.run, START, END)
        self.assertTrue(plan["source_is_legacy_name"])
        result = publish_weekly_document(self.write_plan(plan), self.source)
        self.assertFalse(legacy.exists())
        self.assertTrue((self.docs / CANONICAL).is_file())
        self.assertEqual(result["archived_legacy_paths"], [str(legacy.resolve())])

    def test_multiple_same_week_files_are_a_conflict(self) -> None:
        make_docx(self.docs / CANONICAL, "one")
        make_docx(self.docs / "8.3-8.7课程预告_DRAFT.docx", "two")
        plan = resolve_weekly_document(self.root, self.run, START, END)
        self.assertEqual(plan["status"], "conflict")
        self.assertEqual(len(plan["same_week_candidates"]), 2)

    def test_init_manifest_uses_default_weekly_folder(self) -> None:
        existing = self.docs / CANONICAL
        make_docx(existing, "old")
        output = self.run / "manifest.json"
        init_manifest(
            Namespace(
                date="2026-08-07",
                root=str(self.root),
                docs=None,
                run_dir=str(self.run),
                out=str(output),
            )
        )
        manifest = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(manifest["weekly_document"]["mode"], "update")
        self.assertEqual(
            manifest["weekly_document"]["source_document"], str(existing.resolve())
        )
        self.assertEqual(len(manifest["weekly_document"]["same_week_candidates"]), 1)

    def test_init_manifest_rejects_multiple_default_weekly_files(self) -> None:
        make_docx(self.docs / CANONICAL, "one")
        make_docx(self.docs / "8.3-8.7课程预告_FINAL.docx", "two")
        with self.assertRaisesRegex(ValueError, "multiple course-preview DOCX"):
            init_manifest(
                Namespace(
                    date="2026-08-07",
                    root=str(self.root),
                    docs=None,
                    run_dir=str(self.run),
                    out=str(self.run / "manifest.json"),
                )
            )


if __name__ == "__main__":
    unittest.main()
