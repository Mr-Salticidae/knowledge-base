# Canonical weekly DOCX workflow

## Invariant

For one resolved weekly range, `课程预告文本/` contains exactly one formal
document named:

```text
<start M.D>-<end M.D>课程预告.docx
```

“One document” is scoped to the same weekly range. Other historical weeks and
non-weekly source documents remain untouched.

Never publish stage/version suffixes such as `_基础信息`, `_待确认`, `_DRAFT`,
`_FINAL`, `_new`, `_v2`, or `_补全`. Drafts are review surfaces, not formal
weekly documents.

## Resolve

Resolve the weekly document before Stage A:

```powershell
python scripts/weekly_document.py resolve `
  --project-root <root> --run-dir <run-dir> `
  --period-start <YYYY-MM-DD> --period-end <YYYY-MM-DD> `
  --out <weekly-document-plan.json>
```

- Zero candidates: `create`; build the working copy from the selected template.
- One canonical candidate: `update`; copy it to
  `<run-dir>/drafts/weekly-working.docx`.
- One legacy suffixed candidate: `update`; use it as the working-copy source.
  Safe publication backs it up and consolidates it to the canonical name.
- More than one candidate: hard stop. Do not choose by `_FINAL`, suffix, file
  size, or modified time. The user must identify the authoritative document.

Record the plan in the manifest and do not rescan opportunistically midway
through the run. Publication rechecks the candidate snapshot and stops if the
folder changed.

## Edit

Keep all files before final publication under the run directory:

```text
<run-dir>/
├─ drafts/
│  ├─ weekly-working.docx
│  ├─ stage-a-basic.docx
│  └─ stage-b-complete.docx
├─ backups/weekly-document/
└─ qa/
```

For an existing weekly document, update the target-date section in the working
copy. Identify content from the manifest (`target_date`, `course_key`, class),
not a fixed paragraph number. Rebuilding the weekly document from the manifest
is preferred when reliable date-section replacement is unavailable. A rerun
for the same target date must replace that date's content and must not append a
second copy.

Stage A stops with a draft from `drafts/`; it does not publish to
`课程预告文本/`. Stage B continues from the same working document and is the
only text stage that may publish the formal weekly DOCX after complete render
and visual QA.

## Publish

Publish only a QA-approved run-directory DOCX:

```powershell
python scripts/weekly_document.py publish `
  --plan <weekly-document-plan.json> `
  --source-docx <qa-approved-working.docx> `
  --out <weekly-document-publish.json>
```

The publisher:

1. verifies the DOCX package;
2. verifies that the same-week candidate snapshot has not changed;
3. backs up the current formal/legacy weekly document under the run directory;
4. copies and validates a temporary DOCX in the destination directory;
5. atomically replaces the canonical weekly document;
6. removes a single legacy suffixed source only after its backup exists;
7. verifies that one canonical same-week DOCX remains.

Do not use the publisher to replace unrelated historical source documents.

## Final check

Run immediately before handoff:

```powershell
python scripts/weekly_document.py check `
  --project-root <root> `
  --period-start <YYYY-MM-DD> --period-end <YYYY-MM-DD> `
  --expected-docx <canonical.docx> `
  --out <weekly-document-check.json>
```

Completion requires:

- same-week DOCX count equals one;
- that file uses the exact canonical name;
- it is a valid, non-empty DOCX package;
- no unfinished publication file remains;
- `delivery_check.py` reports `weekly_document_valid=true`.

Any later DOCX replacement, rename, addition, or deletion invalidates the final
checks and requires the weekly check and full delivery sequence to run again.

## Historical catalog hygiene

The course-detail catalog may read canonical weekly documents and non-weekly
source documents. Skip versioned weekly files. Otherwise one course can appear
as multiple exact matches solely because approval/final drafts were indexed.
