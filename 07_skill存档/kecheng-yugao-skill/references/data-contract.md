# Manifest data contract (schema version 2)

Use one JSON manifest per target date. Preserve evidence; do not replace
unknowns with plausible guesses.

## Top-level fields

- `schema_version`: exactly `2`.
- `target_date`: ISO date.
- `root`: absolute project root.
- `period`: start, end, filename, and optional existing document.
- `weekly_document`:
  - `canonical_path`: absolute path to the only formal DOCX for the range;
  - `mode`: `create` or `update`;
  - `source_document`: the single existing weekly DOCX, or null;
  - `source_is_legacy_name`: whether the one existing source has a suffix;
  - `working_path`: run-directory DOCX used for Stage A/Stage B edits;
  - `backup_root`: run-directory backup location;
  - `same_week_candidates`: resolve-time filename, size, and SHA-256 snapshot;
  - `publication_status`, `published_sha256`, and publication report after the
    approved final DOCX is atomically published.
- `requested_text_template_id`: optional one-run override.
- `text_template_selection`: resolved ID, display name, source, revision.
- `document_template_id`: compatibility copy of the resolved text template ID.
- `project_settings_revision`: set after portrait planning.
- `teacher_asset_folder`: configured folder relative to the project when
  possible.
- `poster_psd_output_folder`: user-configured final PSD folder, relative to the
  project when possible.
- `poster_psd_output_folders`: optional poster-template-ID to final PSD folder
  mapping. It takes precedence over the legacy single-folder setting; the
  current `poster-template-2` mapping is `课程预告ps第二版`.
- `course_alias_registry`: configured confirmed-alias registry and revision.
- `approval`:
  - `phase1_status`: `pending` or `approved`;
  - `approved_at`;
  - `phase1_content_hash`;
  - `poster_status`, `poster_approved_at`, `poster_content_hash` for optional
    high-risk portrait/template confirmation evidence.
- `courses`: non-empty list.

## Course fields

Required in Stage A:

- `course_key`: stable normalized class + course identifier
- `class_name`
- `schedule_title`: verbatim visible title
- `course_title`: normalized display title
- `teacher`
- `delivery`: `live` or `recorded`
- `schedule_source`
- `schedule_evidence`
- `schedule_cell_locator`: target month/week/date cell within the source image
- `schedule_entry_index`: 1-based top-to-bottom index of this course block in
  the class's target-date cell
- `schedule_entry_count`: total number of distinct course blocks found in that
  target-date cell; every course from the same class/source repeats this count
- `schedule_cell_color`: visible color description for this specific block
- `schedule_legend_evidence`: verbatim or faithful transcription of the current
  schedule image's live/recorded legend; required for legend-based decisions
- `delivery_evidence_source`: `schedule_legend`, `explicit_schedule_label`, or
  `user_confirmation`
- `delivery_evidence`: the exact legend/color/label or user instruction that
  proves the selected `delivery`
- `confidence`: use `confirmed` when sources agree; use `user_confirmed` only
  when the user explicitly resolves an ambiguity
- `overrides`: explicit user changes with old/new delivery and time, evidence,
  timestamp, and whether both fields were confirmed
- `requested_poster_template_id`: optional
- `poster_template_selection`

Required before Stage B output:

- `time`
- `details.tools`: list, possibly empty when source explicitly has none
- `details.homework`: list, possibly empty
- `details.objectives`: non-empty list
- `details.source_document`
- `details.sources`: field-level evidence for `tools`, `homework`, and
  `objectives`; each entry records source type, path, matched title, and
  confirmation status
- `details.alias_resolution`: canonical/matched title and confirmation evidence
  when an alias rather than an exact title was used

Portrait fields:

- `teacher_asset_required`: true whenever the selected PSD has a visible person
  slot; false only when no person slot exists
- `teacher_asset_reason`: required when the boolean is true
- `requested_teacher_asset_filename`: exact filename supplied by the user
- `teacher_asset_selection`:
  - `status`: `not_required_no_portrait_slot`, `selected`,
    `pending_user_filename`, or `missing`;
  - `file_name`, `relative_path`, `selection_source`;
  - `settings_revision`;
  - `alpha_audit`;
  - all candidates with full filenames and relative paths.

Poster output fields, required before completion:

- `poster_working_psd`: temporary dated-run PSD modified or reconstructed for
  this poster; it may be absent on disk after explicit user acceptance and a
  recorded working-PSD cleanup;
- `poster_output_png`: final PNG in the dated poster folder;
- `poster_output_psd` / `poster_course_psd`: the reusable exact-title course PSD
  in the selected template's resolved output folder; its filename is the exact
  display course title with only Windows-invalid filename characters sanitized,
  and it need not share the dated PNG filename stem;
- `poster_psd_storage_status`: `reused_existing_course_psd`,
  `published_new_course_psd`, `already_published_course_psd`, or
  `already_in_output_folder`;
- `poster_source_type`: `editable_psd` or `flattened_date_slot`;
- `poster_editability_grade`: `A` for fully editable, `B` for a compliant
  layered date/time fallback; `C` is invalid;
- `poster_candidate_evidence`: candidate score, title line/canvas compatibility,
  teacher/delivery match, and rejected candidates with reasons;
- `poster_qa`: full-poster review, changed-region crop review, title canvas
  bounds, title paragraph justification, title center target/actual/delta,
  title safe bounds, rendered glyph height per line, title fill ratio,
  title-to-internal-decoration gap, title-to-lower-block gap,
  objective/date-time safe-area bounds, editability
  grade, exact internal course-title evidence, and course-PSD storage/hash
  status.

## Approval fingerprints

The Stage A fingerprint covers the visible basic course data and resolved text/
poster template choices. Portrait choices and detailed copy belong to the later
poster fingerprint, so selecting a portrait does not invalidate an already
approved basic DOCX.

Before Stage B, `approval-check` must match. Before a high-risk poster operation
whose choices were explicitly approved, `poster-approval-check` must match.
Changing fingerprinted fields requires new approval.

## Validation invariants

- no duplicate class + normalized course title;
- `course_key` values are unique and stable;
- no empty teacher, delivery, evidence, or confidence;
- for every class target-date cell, `schedule_entry_count` is consistent
  and the recorded indices are exactly `1..schedule_entry_count`; a missing,
  repeated, or out-of-range index is invalid;
- delivery evidence comes only from the current schedule legend, an explicit
  schedule label, or user confirmation; title wording and historical copy are
  prohibited as Stage A delivery sources;
- one weekly text template;
- one resolved poster template per course;
- live and recorded are never inferred from teacher or time;
- a delivery override records an independently verified time;
- a one-course semantic diff contains no unrelated changes;
- Stage B requires explicit time and at least one objective;
- required portrait assets must resolve to exactly one PNG;
- historical sources and generated outputs use different paths.
- one date range has exactly one formal DOCX in `课程预告文本/`, and its name is
  exactly `<start M.D>-<end M.D>课程预告.docx`;
- Stage A/Stage B drafts, approval copies, QA files, and backups are outside the
  final text folder and inside the dated run directory;
- no final weekly filename has `_基础信息`, `_待确认`, `_DRAFT`, `_FINAL`,
  `_new`, `_v2`, or another version suffix;
- a same-date rerun replaces the target date block by stable course keys and
  does not duplicate it;
- every final PNG maps to one non-empty reusable PSD whose inspected internal
  title exactly matches the normalized course title;
- one normalized course title maps to one PSD, while multiple class rows for
  that same title may share it; one PSD never maps to different course titles;
- every final PNG stem contains its manifest class, course title, teacher,
  target `M.D`, and the `直播` marker when delivery is live;
- every grade-A title has an enforced horizontal-alignment guard whose absolute
  center delta is within the registered template tolerance;
- every fitted grade-A title passes its rendered per-line glyph-height and
  minimum-fill guards, stays inside the registered inner title safe bounds, and
  preserves the registered minimum gap above internal decoration artwork;
- no final PSD publish overwrites an existing course PSD without explicit
  replacement approval;
- course count equals final PNG count; unique course PSD count may be lower when
  the same course appears in multiple classes.
- every poster has editability grade A or B and a passing objective safe-area
  check.
- final run cleanup occurs only after explicit user acceptance, requires a
  pre-run Photoshop-temp baseline, removes only the exact dated run directory
  plus baseline-diff Photoshop temp files, requires Photoshop to be closed, and
  verifies protected deliverable hashes afterward;
- no deliverable changes after the post-cleanup manifest, poster-output, and
  delivery checks; any change invalidates those results and requires a rerun.
