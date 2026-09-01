import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import workflow_guardrails as guardrails


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


class FinalRunCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.run = self.root / "_course_preview_runs" / "2026-08-13"
        self.run.mkdir(parents=True)
        (self.run / "drafts").mkdir()
        (self.run / "drafts" / "draft.docx").write_bytes(b"draft")
        (self.run / "qa").mkdir()
        (self.run / "qa" / "preview.png").write_bytes(b"qa")
        self.poster = self.root / "8.13" / "poster.png"
        self.poster.parent.mkdir()
        self.poster.write_bytes(b"png")
        self.course_psd = self.root / "课程预告ps" / "课程A.psd"
        self.course_psd.parent.mkdir()
        self.course_psd.write_bytes(b"psd")
        self.weekly = self.root / "课程预告文本" / "8.10-8.14课程预告.docx"
        self.weekly.parent.mkdir()
        self.weekly.write_bytes(b"docx")
        self.manifest = self.run / "manifest-final.json"
        write_json(
            self.manifest,
            {
                "schema_version": 2,
                "root": str(self.root),
                "target_date": "2026-08-13",
                "weekly_document": {"canonical_path": str(self.weekly)},
                "completion": {
                    "status": "ready_for_delivery_check",
                    "poster_folder": str(self.poster.parent),
                },
                "courses": [
                    {
                        "course_key": "class|course-a",
                        "course_title": "课程A",
                        "poster_output_png": str(self.poster),
                        "poster_output_psd": str(self.course_psd),
                        "poster_qa": {
                            "full_poster_review": "passed",
                            "course_psd_title_match": True,
                        },
                    }
                ],
            },
        )
        self.baseline = self.run / "run-cleanup-baseline.json"
        write_json(
            self.baseline,
            {
                "schema_version": 1,
                "project_root": str(self.root),
                "run_dir": str(self.run),
                "baseline_files": [],
            },
        )
        self.report = self.root / "_course_preview_runs" / "_cleanup_reports" / "2026-08-13.json"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def args(self, approved: bool = True) -> argparse.Namespace:
        return argparse.Namespace(
            manifest=str(self.manifest),
            run_dir=str(self.run),
            baseline=str(self.baseline),
            out=str(self.report),
            user_approved=approved,
        )

    def test_requires_explicit_approval(self) -> None:
        with self.assertRaises(PermissionError):
            guardrails.final_run_cleanup(self.args(False))
        self.assertTrue(self.run.is_dir())

    def test_refuses_while_photoshop_is_running(self) -> None:
        with patch.object(guardrails, "validate_manifest", return_value=[]), patch.object(
            guardrails, "_windows_photoshop_running", return_value=True
        ):
            with self.assertRaisesRegex(RuntimeError, "Photoshop is still running"):
                guardrails.final_run_cleanup(self.args())
        self.assertTrue(self.run.is_dir())
        self.assertTrue(self.poster.is_file())

    def test_removes_entire_run_and_preserves_deliverables(self) -> None:
        with patch.object(guardrails, "validate_manifest", return_value=[]), patch.object(
            guardrails, "_windows_photoshop_running", return_value=False
        ), patch.object(guardrails, "_photoshop_temp_files", return_value=[]):
            guardrails.final_run_cleanup(self.args())
        self.assertFalse(self.run.exists())
        self.assertTrue(self.poster.is_file())
        self.assertTrue(self.course_psd.is_file())
        self.assertTrue(self.weekly.is_file())
        self.assertTrue(self.report.is_file())
        result = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "cleaned")
        self.assertGreater(result["run_deleted_count"], 0)

    def test_deletes_only_temp_files_absent_from_baseline(self) -> None:
        old_temp = self.root / "Photoshop Temp old"
        new_temp = self.root / "Photoshop Temp new"
        old_temp.write_bytes(b"old")
        new_temp.write_bytes(b"new")
        baseline = json.loads(self.baseline.read_text(encoding="utf-8"))
        baseline["baseline_files"] = [{"path": str(old_temp)}]
        write_json(self.baseline, baseline)
        with patch.object(guardrails, "validate_manifest", return_value=[]), patch.object(
            guardrails, "_windows_photoshop_running", return_value=False
        ), patch.object(
            guardrails, "_photoshop_temp_files", return_value=[old_temp, new_temp]
        ):
            guardrails.final_run_cleanup(self.args())
        self.assertTrue(old_temp.is_file())
        self.assertFalse(new_temp.exists())
        result = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertEqual(result["photoshop_temp_deleted_count"], 1)
        self.assertEqual(result["photoshop_temp_skipped"][0]["reason"], "present_before_run")


if __name__ == "__main__":
    unittest.main()
