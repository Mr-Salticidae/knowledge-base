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
import manifest_finalize


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def title_inspection(path: Path, psd: Path, title: str) -> None:
    write_json(
        path,
        {
            "schema_version": 1,
            "source_psd": str(psd.resolve()),
            "layers": [
                {
                    "kind": "LayerKind.TEXT",
                    "visible": True,
                    "text": title,
                }
            ],
        },
    )


class CoursePsdStorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.output = self.root / "课程预告ps"
        self.output.mkdir()
        self.settings = self.root / "settings.json"
        write_json(
            self.settings,
            {
                "schema_version": 1,
                "revision": 1,
                "project_root": str(self.root),
                "poster_psd_output_folder": "课程预告ps",
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_template_specific_output_folder_overrides_legacy_default(self) -> None:
        second = self.root / "课程预告ps第二版"
        settings = json.loads(self.settings.read_text(encoding="utf-8"))
        settings["poster_psd_output_folders"] = {
            "poster-template-2": "课程预告ps第二版"
        }
        write_json(self.settings, settings)
        resolved = guardrails.configured_poster_psd_folder(
            settings, "poster-template-2"
        )
        self.assertEqual(resolved, second)
        self.assertTrue(second.is_dir())

    def test_course_filename_is_sanitized_from_exact_course_title(self) -> None:
        self.assertEqual(
            guardrails.safe_course_psd_stem("课程：A/B？"),
            "课程 A B",
        )

    def publish_args(
        self,
        source: Path,
        poster: Path,
        inspection: Path,
        title: str,
        existing: Path | None = None,
    ) -> argparse.Namespace:
        return argparse.Namespace(
            settings=str(self.settings),
            source_psd=str(source),
            poster_png=str(poster),
            course_title=title,
            title_inspection=str(inspection),
            existing_psd=str(existing) if existing else None,
            out=str(self.root / "publish.json"),
        )

    def test_new_course_publishes_one_stable_psd(self) -> None:
        source = self.root / "working.psd"
        poster = self.root / "dated-poster.png"
        inspection = self.root / "title.json"
        source.write_bytes(b"working-psd")
        poster.write_bytes(b"png")
        title_inspection(inspection, source, "课程A")

        guardrails.poster_psd_publish(
            self.publish_args(source, poster, inspection, "课程A")
        )

        destination = self.output / "课程A.psd"
        self.assertEqual(destination.read_bytes(), b"working-psd")
        result = json.loads((self.root / "publish.json").read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "published_new_course_psd")
        self.assertEqual(Path(result["course_psd"]), destination)

    def test_existing_exact_title_psd_is_reused_without_copy(self) -> None:
        source = self.root / "working.psd"
        poster = self.root / "dated-poster.png"
        existing = self.output / "旧日期课程A.psd"
        inspection = self.root / "title.json"
        source.write_bytes(b"current-working")
        poster.write_bytes(b"png")
        existing.write_bytes(b"canonical-course")
        title_inspection(inspection, existing, "课程A")

        guardrails.poster_psd_publish(
            self.publish_args(source, poster, inspection, "课程A", existing)
        )

        self.assertEqual(existing.read_bytes(), b"canonical-course")
        self.assertFalse((self.output / "课程A.psd").exists())
        result = json.loads((self.root / "publish.json").read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "reused_existing_course_psd")

    def test_cleanup_removes_only_run_working_psd_files(self) -> None:
        target_date = "2026-08-11"
        run_dir = self.root / "_course_preview_runs" / target_date
        working = run_dir / "working-psd"
        working.mkdir(parents=True)
        (working / "one.psd").write_bytes(b"one")
        nested = working / "nested"
        nested.mkdir()
        (nested / "two.psb").write_bytes(b"two")
        (working / "keep-audit.json").write_text("{}", encoding="utf-8")
        poster = self.root / "8.11" / "poster.png"
        poster.parent.mkdir()
        poster.write_bytes(b"png")
        course_psd = self.output / "课程A.psd"
        course_psd.write_bytes(b"course")
        manifest = run_dir / "manifest-final.json"
        write_json(
            manifest,
            {
                "schema_version": 2,
                "root": str(self.root),
                "target_date": target_date,
                "completion": {"status": "ready_for_delivery_check"},
                "courses": [
                    {
                        "course_key": "class|course-a",
                        "course_title": "课程A",
                        "poster_output_png": str(poster),
                        "poster_output_psd": str(course_psd),
                        "poster_qa": {
                            "full_poster_review": "passed",
                            "course_psd_title_match": True,
                            "publish_status": "reused_existing_course_psd",
                        },
                    }
                ],
            },
        )
        report = run_dir / "working-psd-cleanup.json"
        args = argparse.Namespace(
            manifest=str(manifest),
            run_dir=str(run_dir),
            out=str(report),
            user_approved=True,
        )

        with patch.object(guardrails, "validate_manifest", return_value=[]):
            guardrails.working_psd_cleanup(args)

        self.assertFalse((working / "one.psd").exists())
        self.assertFalse((nested / "two.psb").exists())
        self.assertTrue((working / "keep-audit.json").is_file())
        self.assertTrue(poster.is_file())
        self.assertTrue(course_psd.is_file())
        result = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(result["deleted_count"], 2)

    def test_two_class_rows_for_same_course_share_one_psd(self) -> None:
        poster_folder = self.root / "8.11"
        poster_folder.mkdir()
        first_png = poster_folder / "班级一 课程A.png"
        second_png = poster_folder / "班级二 课程A.png"
        first_png.write_bytes(b"one")
        second_png.write_bytes(b"two")
        course_psd = self.output / "课程A.psd"
        course_psd.write_bytes(b"course")
        manifest = self.root / "manifest.json"
        write_json(
            manifest,
            {
                "schema_version": 2,
                "courses": [
                    {
                        "course_key": "class-1|course-a",
                        "course_title": "课程A",
                        "poster_output_png": str(first_png),
                        "poster_output_psd": str(course_psd),
                        "poster_qa": {"course_psd_title_match": True},
                    },
                    {
                        "course_key": "class-2|course-a",
                        "course_title": "课程A",
                        "poster_output_png": str(second_png),
                        "poster_output_psd": str(course_psd),
                        "poster_qa": {"course_psd_title_match": True},
                    },
                ],
            },
        )
        report = self.root / "outputs-check.json"
        args = argparse.Namespace(
            settings=str(self.settings),
            poster_folder=str(poster_folder),
            manifest=str(manifest),
            out=str(report),
        )

        with patch.object(guardrails, "validate_manifest", return_value=[]):
            guardrails.poster_outputs_check(args)

        result = json.loads(report.read_text(encoding="utf-8"))
        self.assertTrue(result["valid"])
        self.assertEqual(result["png_count"], 2)
        self.assertEqual(result["unique_course_psd_count"], 1)

    def test_manifest_finalize_allows_different_course_psd_stem(self) -> None:
        working = self.root / "班级 8.11 课程A 老师.psd"
        png = self.root / "班级 8.11 课程A 老师.png"
        course_psd = self.output / "课程A.psd"
        audit = self.root / "audit.json"
        working.write_bytes(b"working")
        png.write_bytes(b"png")
        course_psd.write_bytes(b"course")
        write_json(
            audit,
            {
                "changes": {
                    "layout_guard": {"actual_gap_px": 20, "minimum_gap_px": 20},
                    "title_horizontal_alignment": {
                        "enforced": True,
                        "actual_center_delta_px": 0,
                        "maximum_center_delta_px": 15,
                    },
                    "objective_safe_area_guard": {
                        "skipped": False,
                        "vertical_overlap_px": 0,
                        "actual_horizontal_gap_px": 20,
                        "minimum_horizontal_gap_px": 20,
                    },
                }
            },
        )
        source_manifest = self.root / "source-manifest.json"
        write_json(
            source_manifest,
            {
                "schema_version": 2,
                "target_date": "2026-08-11",
                "courses": [
                    {
                        "course_key": "class|course-a",
                        "class_name": "班级",
                        "course_title": "课程A",
                        "teacher": "老师",
                        "delivery": "recorded",
                    }
                ],
            },
        )
        index = self.root / "poster-index.json"
        write_json(
            index,
            {
                "schema_version": 1,
                "posters": [
                    {
                        "course_key": "class|course-a",
                        "working_psd": str(working),
                        "output_png": str(png),
                        "output_psd": str(course_psd),
                        "editability_grade": "A",
                        "source_type": "editable_psd",
                        "audit_file": str(audit),
                        "full_poster_review": "passed",
                        "changed_region_review": "passed",
                        "publish_status": "reused_existing_course_psd",
                        "course_psd_title_match": True,
                        "published_sha256": "hash",
                    }
                ],
            },
        )
        final_manifest = self.root / "manifest-final.json"
        argv = [
            "manifest_finalize.py",
            "--manifest",
            str(source_manifest),
            "--poster-index",
            str(index),
            "--out",
            str(final_manifest),
        ]

        with patch.object(sys, "argv", argv):
            manifest_finalize.main()

        result = json.loads(final_manifest.read_text(encoding="utf-8"))
        course = result["courses"][0]
        self.assertEqual(Path(course["poster_output_psd"]), course_psd)
        self.assertNotEqual(png.stem, course_psd.stem)
        self.assertTrue(course["poster_qa"]["course_psd_title_match"])


if __name__ == "__main__":
    unittest.main()
