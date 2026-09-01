---
name: kecheng-yugao-skill
description: 自动制作指定日期的课程预告文本和课程预告海报，并管理课表提取、Word 模板、PSD 模板、教师形象、软件图标、审批节点及运行残留清理。当用户给出的文字包含“课程预告”“课程预告文本”或“课程预告海报”中的任一短语时，自动使用本 Skill；也用于调整相应模板、默认模板、课程信息、教师形象或海报成品。
---

# Kecheng-Yugao-Skill

Produce one date-specific course preview through controlled stages. This is a
user-invoked production skill, not a recurring operating-system automation.

## Read before acting

For every dated production run, read:

1. [references/decision-rules.md](references/decision-rules.md)
2. [references/data-contract.md](references/data-contract.md)
3. [references/template-registry.md](references/template-registry.md)
4. [references/weekly-document.md](references/weekly-document.md)

Additionally read:

- [使用说明书.md](使用说明书.md) when the user asks how to install, configure,
  invoke, or operate this skill;
- [references/text-template-workflow.md](references/text-template-workflow.md)
  when a DOCX style is added, extracted, compared, or changed;
- [references/teacher-assets.md](references/teacher-assets.md) when a teacher is
  new, the portrait is being replaced, or a portrait background is opaque;
- [references/photoshop-posters.md](references/photoshop-posters.md) before
  inspecting or editing a PSD;
- [references/editable-poster-variants.md](references/editable-poster-variants.md)
  when one template has teacher-specific PSDs, a new PSD replaces an older
  source, or only title font sizes may change.

Use the `documents` workflow for DOCX extraction, rendering, and visual QA.
Use Photoshop itself for PSD inspection/editing. Use the image-editing workflow
for background removal; do not simulate cutouts by deleting a rectangular
background.

## Project locations

Require:

- `课表/`: all schedule images;
- `课程预告文本/`: historical course-copy DOCX files and exactly one canonical
  formal DOCX per weekly range;
- `课程预告ps/` and `课程预告海报/`: historical PSD/PNG sources;
- `课程预告ps第二版/`: reusable PSD destination for `poster-template-2`;
  template-specific destinations come from `poster_psd_output_folders`, and
  existing files remain immutable;
- `模板库/文本模板/text-template-registry.json`;
- `模板库/海报模板/poster-template-registry.json`;
- `模板库/课程别名/course-aliases.json`;
- `模板库/项目设置/project-settings.json`;
- `图标/`: transparent software icons plus their source manifest.

Store all DOCX drafts, approval copies, QA renders, backups, run evidence, and
working PSDs in `_course_preview_runs/YYYY-MM-DD/`.
Store final posters in `<M.D>/` at the project root. Keep only one reusable PSD
per exact normalized course title in the resolved template-specific PSD output
folder; a final PNG
maps to that course PSD and does not require a same-stem PSD. Never overwrite a
historical DOCX, PSD, poster, or an existing course PSD without explicit
replacement approval.

The only formal weekly DOCX is
`课程预告文本/<start M.D>-<Friday M.D>课程预告.docx`. Never publish files with
`_基础信息`, `_待确认`, `_DRAFT`, `_FINAL`, `new`, or version-number suffixes to
`课程预告文本/`. Update the canonical weekly DOCX through the safe publication
workflow; keep its previous version in the run backup folder.

Use these run subfolders so drafts and evidence do not mix with deliverables:

```text
_course_preview_runs/YYYY-MM-DD/
├─ drafts/
├─ backups/
├─ schedule-evidence/
├─ inspections/
├─ measurements/
├─ failed-qa/
├─ working-psd/
└─ qa/
```

Use the bundled workspace Python. The deterministic helpers are:

```powershell
python scripts/course_preview.py --help
python scripts/workflow_guardrails.py --help
python scripts/manifest_semantic_diff.py --help
python scripts/course_aliases.py --help
python scripts/docx_layout_guard.py --help
python scripts/weekly_document.py --help
python scripts/manifest_finalize.py --help
python scripts/delivery_check.py --help
powershell -ExecutionPolicy Bypass -File scripts/photoshop_run_job.ps1 -JobPath <job.json>
```

On Windows, read/write JSON as UTF-8 explicitly. Invoke Photoshop edits through
`photoshop_run_job.ps1`; do not pass long Chinese text directly through a
PowerShell command line.

## Stage 0 — resolve configuration

1. Parse the date explicitly supplied by the user.
2. Initialize a schema-v2 manifest.
3. Resolve the canonical weekly DOCX before reading or generating content:

   ```powershell
   python scripts/weekly_document.py resolve `
     --project-root <root> --run-dir <run-dir> `
     --period-start <YYYY-MM-DD> --period-end <YYYY-MM-DD> `
     --out <weekly-document-plan.json>
   ```

   If no same-week document exists, create from the selected template. If one
   exists, copy it to `drafts/weekly-working.docx` and update that working copy.
   If multiple same-week files exist, stop; never pick one by suffix or modified
   time. A single legacy suffixed file may be used as the update source and is
   consolidated to the canonical filename only during backed-up publication.
4. Give every course a stable `course_key` derived from normalized class and
   title. Treat the manifest as the single source of truth; never patch a DOCX
   by paragraph number after a course changes.
5. Resolve text and poster templates from their separate registries:

   ```powershell
   python scripts/workflow_guardrails.py template-plan `
     --text-registry <text-template-registry.json> `
     --poster-registry <poster-template-registry.json> `
     --manifest <manifest.json> --out <resolved.json>
   ```

6. Use one text template for the entire weekly DOCX. Poster templates may vary
   per course.
7. Do not infer a teacher-portrait folder. Read `teacher_asset_folder`; if it is
   empty, ask which folder is authoritative and persist it with
   `teacher-folder-set`. Once configured, every poster that contains a person
   slot must replace the template person with the matching PNG from that
   folder. Use only the isolated person subject: no source-image background may
   remain. The current project setting is `人物`.
8. Resolve the PSD destination from `poster_psd_output_folders` using the
   selected poster template ID, then fall back to legacy
   `poster_psd_output_folder` only when that template has no mapping. If neither
   exists, ask the user and persist it with `poster-psd-folder-set`. The current
   `poster-template-2` destination is `课程预告ps第二版`.
9. Read `course_alias_registry`. If absent, initialize it with
   `course_aliases.py init` and persist it with `course-alias-registry-set`.
10. Capture a Photoshop-temporary-file baseline before Photoshop is first
    opened. Keep it inside the run directory:

    ```powershell
    python scripts/workflow_guardrails.py run-cleanup-baseline `
      --project-root <root> --run-dir <run-dir> `
      --out <run-dir/run-cleanup-baseline.json>
    ```

    This baseline is required for safe post-acceptance cleanup. It prevents the
    skill from deleting a Photoshop temporary file that existed before the run.

## Stage A — collect and deliver basic information

1. Open every schedule image in `课表/`, read that image's own delivery legend,
   and inspect the target date. Never reuse another schedule's color mapping.
2. For each class, use two passes on the complete target-date cell: first count
   all distinct course blocks without transcribing them; then scan top to bottom
   again and transcribe block `1..N`. Save a target-cell crop in
   `schedule-evidence/` whenever practical so the count can be visually audited.
   Enumerate every distinct course block before recording any result. If the
   cell contains `N` blocks, create exactly `N` manifest courses with
   `schedule_entry_index=1..N` and the same `schedule_entry_count=N`. Record
   `schedule_cell_locator`, each block's color, the legend text, and a crop or
   precise evidence note. Finding one course never ends the scan. If a class has
   no course block that day, omit it.
3. Resolve each course's `delivery` only from that schedule's legend/cell
   encoding, an explicit live/recorded label printed in the schedule, or an
   explicit user confirmation. Record `delivery_evidence_source` and
   `delivery_evidence`. Course-title words (including `直播`, `直播间`, or
   `直播贴片`), historical Word copy, teacher, and time are never delivery
   evidence. If the legend or block color is unreadable, stop for confirmation.
4. Resolve the teacher by exact normalized title from historical DOCX copy.
   Poster/PSD filenames may corroborate but may not override a conflicting text
   source.
5. Run `course_preview.py validate --phase 1` before building the draft. It must
   reject a class whose extracted indices do not cover every value from `1` to
   `schedule_entry_count`; do not bypass this as a visual judgment.
6. Build only:
   `班级名称 + 日期 + 课程名称 + 讲师名称 + （直播/录播）`.
   Live rows follow the selected text template; in text template one they are
   red and bold. Do not include details yet.
7. Group all same-class courses under one class heading. Keep every enumerated
   course as its own row/block; do not collapse the list to one course per class.
   Keep the heading with
   the following row/block.
8. Save the Stage A file only under `<run-dir>/drafts/`; never place an approval
   draft in `课程预告文本/`.
9. Render every DOCX page and compare it with the selected text template. Try
   the packaged renderer first; on Windows, Microsoft Word PDF export plus PDF
   page rendering is the fallback when LibreOffice is unavailable. Reject
   repeated headings, orphan headings, detached time/notification lines, and
   nearly empty spill pages. PDF extraction may lose a leading emoji; detect
   detached lines from their semantic time/notification text as well.
10. Present the run-directory draft, template choices, source uncertainties, and omitted
   classes. Then stop.
11. After explicit user approval, bind the exact Stage A content:

   ```powershell
   python scripts/workflow_guardrails.py phase1-approve `
     --manifest <resolved.json> --out <approved.json> --user-approved
   ```

   If date, course, teacher, delivery, time, or template selection later
   changes, the fingerprint no longer matches and approval must be obtained
   again.
12. When the user changes one course, regenerate the affected output from the
   manifest and run `manifest_semantic_diff.py`. Show the complete before/after
   delivery and time. Assert that no unrequested course changed. A delivery
   change never silently supplies a new time.

## Stage B — append detailed introductions

1. Continue only when `approval-check` succeeds.
2. Build/refresh the historical catalog and match each course:

   ```powershell
   python scripts/course_preview.py catalog --docs <课程预告文本> --out <catalog.json>
   python scripts/course_preview.py match --catalog <catalog.json> --title "<course title>"
   ```

3. Accept only a unique exact normalized match, a previously confirmed alias,
   or a candidate explicitly confirmed by the user. Persist confirmed aliases
   with the canonical title and evidence so the same ambiguity is not asked
   again.
4. Copy source-backed tools, optional homework, and objectives. Record evidence
   per field; do not represent a poster-sourced objective as though the entire
   detail block came from a DOCX. Replace old
   dates/times with the target date and current confirmed time.
5. A live course must have an explicit time. Never infer `19:30` from the word
   “直播”.
6. Append details using the selected text template. Group repeated class
   courses, keep headings with their blocks, and use compact spacing to avoid a
   final page containing only one carried-over objective.
7. Render every page, run `docx_layout_guard.py` on the exported PDF, and
   visually inspect the result before posters. Reject a nearly empty spill
   page, a page beginning with a detached notification/time/objective, or a
   class heading separated from its first course row.
8. Publish the QA-approved working DOCX to the canonical weekly filename:

   ```powershell
   python scripts/weekly_document.py publish `
     --plan <weekly-document-plan.json> `
     --source-docx <qa-approved-working.docx> `
     --out <weekly-document-publish.json>
   ```

   Publication backs up the existing weekly file inside the run directory,
   uses an atomic replacement, and consolidates one legacy suffixed filename.
   It must leave exactly one same-week DOCX in `课程预告文本/`.

For `text-template-1`, the legacy helper may build the DOCX. For a distilled
newer template, follow its executable template, contract, and usage guide with
the documents workflow; do not send it through the legacy hard-coded renderer.

## Stage C — select portraits and produce posters

Read [references/photoshop-posters.md](references/photoshop-posters.md) before
starting this stage. Also read
[references/editable-poster-variants.md](references/editable-poster-variants.md)
for teacher-specific or multi-row templates, and
[references/teacher-assets.md](references/teacher-assets.md) whenever portrait
selection or background removal is involved.

1. Inspect candidate PSD title smart objects after Stage B and match the exact
   normalized internal course title; never select by filename or substring.
   Score candidates by title structure, canvas, teacher, delivery, objective
   safe area, and target line count. Record rejected candidates. Zero matches
   permits one new course PSD after QA, one match is reused, and multiple
   matches stop the run.
2. Inspect the selected parent PSD and title smart object read-only. For a
   teacher-variant template, require the exact teacher variant and preflight its
   contracted fonts. A missing variant stops unless the contract contains an
   explicit user-approved base-derivation policy.
3. Record whether a visible person slot requires a teacher asset. Generic
   person slots set `teacher_asset_required=true`; an exact contracted teacher
   variant satisfies that requirement unless its portrait is explicitly being
   replaced. Use `teacher-assets-plan` for required assets. Zero or ambiguous
   matches stop; opaque portraits follow the preview, approval, and backup
   procedure. Set `teacher_asset_required=false` only for
   `not_required_no_portrait_slot`.
4. Edit only a dated working copy through a UTF-8 job passed to
   `photoshop_run_job.ps1`. Keep `source_expected_*` separate from `target_*`,
   change only contracted roles, and preserve every locked font, effect, mask,
   transform, layer position, and unrelated pixel. Apply all title, objective,
   icon, date/time, and template-specific geometry rules from the two poster
   references and the selected template contract. Re-inspect the saved PSD;
   outer-poster QA alone is insufficient.
5. Export and inspect the full-size PNG. Its manifest-derived stem must contain
   class, course title, teacher, target `M.D`, and `直播` for live courses. Its
   visible teacher, title, date, time, objectives, and delivery must match the
   manifest.
6. Keep a layered working PSD. Record `editability_grade=A` for the fully
   editable result or `B` only for the compliant same-design date/time fallback
   defined in the Photoshop reference. Never deliver grade C, and retain run
   evidence until the user accepts the outputs.
7. Preflight the complete poster index, then reuse or publish exactly one
   canonical exact-title course PSD through `poster-psd-publish`. Multi-layer
   titles must use the ordered `title_fragments` inspection contract described
   in the poster reference; never fake a single title layer.
8. Finalize poster fields, then run `delivery_check.py`,
   `poster-outputs-check --manifest <final-manifest.json>`, and
   `weekly_document.py check`. Course count must equal PNG count and every
   course must map to one non-empty reusable PSD. These are the final
   write-dependent checks; any later deliverable write invalidates all three.
9. Present the Word and PNG outputs for acceptance. Only after the user
   explicitly confirms they are usable, close Photoshop and run:

    ```powershell
    python scripts/workflow_guardrails.py final-run-cleanup `
      --manifest <final-manifest.json> --run-dir <run-dir> `
      --baseline <run-dir/run-cleanup-baseline.json> `
      --out <project>/_course_preview_runs/_cleanup_reports/<date>.json `
      --user-approved
    ```

   The cleanup must verify sealed deliverables, require the exact dated run and
   recorded temporary-file baseline, refuse while Photoshop is open, preserve
   its external report, and verify protected output hashes afterward. Use the
   legacy `working-psd-cleanup` only when the user explicitly asks to retain the
   rest of the run evidence.

## Template behavior

- Text IDs: `text-template-1`, `text-template-2`, …
- Poster IDs: `poster-template-1`, `poster-template-2`, …
- The current project defaults are `text-template-1` and
  `poster-template-1`. Template one assets are bundled under
  `assets/text-template-1/` and `assets/poster-template-1/`.
- Adding a template never makes it the default.
- Change a default only after the user explicitly asks.
- A course poster resolves in this order: request-level explicit choice,
  persistent exact rule, poster default.
- “Use the newest template” is not a rule. Equal-specificity conflicts stop.
- A new DOCX style remains `pending` until the user sees the generated sample
  and usage guide and explicitly confirms it.

## Hard stops

Stop rather than guess when:

- a class's target-date cell has not completed the two-pass count/transcription
  audit, or its recorded indices do not equal exactly `1..schedule_entry_count`;
- delivery lacks current-schedule legend/label evidence or explicit user
  confirmation, or relies on a course-title word such as `直播间`;
- a schedule cell or delivery color cannot be read;
- teacher sources conflict;
- details have tied/fuzzy candidates;
- a live time or required objective is missing;
- a delivery override lacks a separately verified time;
- a requested one-course change modifies any other course;
- the user has not approved Stage A;
- a requested text/poster template is missing, disabled, or still pending;
- portrait selection has zero or multiple unresolved candidates;
- a required portrait is opaque and the cutout is not yet confirmed;
- two files have the same selectable portrait filename;
- the PSD lacks an editable target or uses an unresolved linked smart object;
- a teacher-variant template lacks the exact teacher PSD;
- a contracted Photoshop font is missing or substituted;
- a position-locked template moves a layer, changes a non-title font size, or
  cannot fill its title regions by title-size adjustment alone;
- a required software icon is missing, generic, or lacks a recorded source;
- exact style preservation is requested but only a flattened image is
  available;
- an operation would overwrite historical source material.
- multiple DOCX files cover the same weekly range;
- a Stage A/Stage B draft would be written to `课程预告文本/`;
- the formal weekly DOCX name is not exactly
  `<start M.D>-<Friday M.D>课程预告.docx`;
- a title exceeds the source title's smart-object overflow allowance or fails
  the template horizontal-alignment, rendered readability, internal-decoration,
  or outer spacing guard;
- an objective enters the date/time safe area or exceeds the poster canvas;
- a fallback PSD would have `editability_grade=C`;
- any final PNG lacks a reusable exact-title course PSD mapping;
- a course title matches multiple PSDs, or one PSD maps to multiple course titles;
- an existing course PSD's teacher, objectives, portrait, or poster template no
  longer matches the requested poster and the user has not approved replacement;
- a final filename does not semantically identify its manifest course, or the
  final folder contains an untracked alias/temporary PNG.
- final run cleanup is requested before explicit user acceptance, lacks a
  matching temporary-file baseline, points outside the exact dated run folder,
  runs while Photoshop is open, or occurs before deliverables and visual QA are
  complete.

## Completion report

Report:

- target date and weekly document range;
- each included class's target-date course-block count and confirmation that
  all indices `1..N` were recorded;
- each course's delivery evidence source and the current schedule legend/color
  or user confirmation used;
- included and omitted classes;
- selected text template and each poster template with selection source;
- Stage A run-directory draft and the single canonical weekly DOCX path;
- final poster folder/count and configured PSD folder/unique reusable course PSD count;
- each poster's source type, editability grade, and rejected fallback reason;
- portrait files used and whether a cutout replacement was committed;
- whether the dated run directory and run-created Photoshop temporary files
  were retained pending acceptance or removed after acceptance, including the
  cleanup report and protected-output verification;
- unresolved items and the evidence needed to resolve them.
