# Photoshop poster workflow

## Capability boundary

PSD files can be used when desktop Photoshop is installed and its native
automation interface is available. Photoshop must perform the PSD operation;
general image libraries do not preserve all smart objects, masks, layer effects,
fonts, and transforms.

PSD automation is template-structure dependent. A script that works on one PSD
must not be assumed safe for all files in `课程预告ps/`.

## Candidate selection

Treat the exact normalized course title as the reusable PSD key. Search only
after the detailed course copy is approved. Inspect internal title smart
objects instead of trusting filenames or substring matches. Zero matches means
one new canonical course PSD may be published after QA, one match is reused,
and multiple matches are a hard stop.

Before editing, score candidate compatibility by target line count, source title
structure, smart-object canvas, teacher, delivery, and objective safe area.
Record every rejected candidate and its reason.

## Read-only inspection

Run `photoshop_inspect.ps1` on the exact selected source. It opens the file,
enumerates recursive layers and bounds, closes without saving, and optionally
writes JSON. Then run `photoshop_inspect_smartobject.ps1` on the title smart
object to record the actual text, text bounds, paragraph justification, and text
position. A filename that names the desired course is not evidence that its
internal smart object contains that course.

Inspection does not prove whether a smart object is embedded or linked. Check
the Layers panel and Photoshop warnings for link icons/missing assets. An
unresolved linked object is a hard stop.

## Layer contract

Before editing, map these semantic roles to exact layer IDs/paths:

- course title;
- date;
- time;
- objectives;
- live/recorded label;
- teacher portrait;
- teacher shadow or other dependent visual;
- export canvas.

Record whether each role is direct text, an embedded smart object, or unsupported.
If the actual layer ID/type/bounds differs from the contract, stop and refresh
the contract. Do not fall back to name-only guessing.

## Safe editing

1. Copy the selected PSD to the dated run folder.
2. Open the copy with Photoshop.
3. Change text content while retaining font, size, color, spacing, transform,
   alignment, effects, and layer position.
4. For an embedded title smart object, edit only the internal text content,
   save the smart object, and verify the parent transform did not move.
5. Replace a teacher smart-object payload only with the confirmed PNG. Preserve
   the parent transform, masks, effects, and clipping relationships.
6. Update a dependent teacher shadow from the same confirmed portrait or keep
   the existing shadow only when it still matches.
7. Saving the temporary working PSD is mandatory. Export the PNG from the same
   working document and never save over the reusable course PSD.
8. Inspect the complete poster and changed-region crops. Search the configured
   PSD folder by inspecting title smart objects. Reuse one exact normalized
   internal-title match without publishing the working PSD. Only when no course
   PSD exists, publish one canonical `<course title>.psd` in the selected poster
   template's configured PSD folder. The filename is derived only from the
   manifest course title, with Windows-invalid filename characters sanitized;
   it must not contain class, date, teacher, delivery, or a version suffix. The
   course PSD does not need the same filename stem as the dated PNG.

Drive edits with a UTF-8 JSON job through `photoshop_run_job.ps1`. The job must
separate source expectations from target values. Use names such as
`source_expected_date` and `target_date`; do not overload an `ExpectedDate`
argument whose direction is unclear. On Windows PowerShell, always use explicit
UTF-8 reads and the standard `-ExecutionPolicy Bypass` launcher.

Every editable-PSD job must carry the template's explicit
`target_title_justification`, `title_center_target_x_px`, and
`maximum_title_center_delta_px`. Set `center_title_horizontally=true` when the
contract declares a centered title. If positions are locked, do not move any
layer.

When a target text layer contains multiple character or paragraph styles, do
not replace it with a plain `textItem.contents` assignment. Inspect and retain
its `textStyleRange` and `paragraphStyleRange`, extend terminal ranges to the
new content length, and re-inspect the result.

For title smart objects, preserve intentional line breaks and record the source
title's existing overflow allowance. Reject a replacement that extends farther
outside the smart-object canvas than the source title. After the smart object is saved,
measure the parent title bounds and its gap to the next lower content block.
The template contract controls the gap; use 20 px when no stricter value is
defined. A failed geometry guard is a hard stop, not a visual preference.

The smart-object canvas guard is not a typography guard. For a title layout
with an internal underline, arrow, paper strip, or other decoration, register
the title's inner `safe_bounds_px`, `decoration_top_px`, and
`minimum_decoration_gap_px`. Maximize the rendered title inside the safe bounds,
then require both `actual_line_glyph_height_px >=
minimum_line_glyph_height_px` and `decoration_top_px - title.bottom >=
minimum_decoration_gap_px`. Use rendered pixel bounds for readability; a
Photoshop `textItem.size` value can differ across historical PSDs because of
text transforms and must not be the sole small-text guard. The point-size floor
is only the search floor for the fit operation. Also enforce the template's
line-count-specific maximum point size; do not keep enlarging a short title to
fill every available pixel. For template 1 the maximums are 78 pt (one line),
64 pt (two lines), and 52 pt (three lines). Normalize replacement title
characters to the registered white base color and hide the contracted legacy
accent-overlay layer when present. A fixed yellow accent created for the donor
title can otherwise overlap unrelated characters after the replacement title
reflows. Record both the final character-color range and accent-overlay
visibility in the poster audit. Long mixed CJK/Latin titles may
use semantic line breaks, but must still pass the pixel-height and decoration
gap guards from an unchanged source.

When template 1 declares `fit_to_safe_bounds`, maximize the title inside its
registered `safe_bounds_px`, align the rendered glyph bottom to the safe-area
bottom, and enforce `minimum_fill_ratio` in addition to the glyph-height and
decoration-gap guards. If any required measurement is absent, stop and register
it from a known-good source before batch generation.

Horizontal alignment is a separate mandatory guard. The poster template
contract must define the target paragraph justification, target visual center
for the rendered title bounds, and allowed center delta. For a centered title:

```text
title_center_x = (title_bounds.left + title_bounds.right) / 2
abs(title_center_x - title_center_target_x_px)
  <= maximum_title_center_delta_px
```

Use the smart-object canvas midpoint only when the registered template declares
that midpoint as its title center; asymmetric designs may declare a different
target. For an unregistered centered template, measure and register a known-good
source. A newly edited title may be auto-centered only inside its title smart
object; do not move unrelated parent design elements. The 2026-08-05 template-1
run uses a 938 px smart-object canvas, midpoint 469 px, and 15 px maximum delta.

Measure the objective block after replacement. Let `time_block_left` be the
leftmost bound of the date, time, and status layers. Require:

```text
objective.right + minimum_objective_time_gap_px <= time_block_left
objective.bottom <= objective_bottom_limit_px <= canvas.bottom
```

Use the template contract gap; default to 20 px. Register the lowest visually
safe objective baseline separately from the raw canvas edge so that text cannot
be hidden by the inner frame, border, or footer artwork. If the guard fails,
return to the unchanged source, insert semantic line breaks, and rerun. When the
full wording requires an additional line, a job may apply a measured
`objective_translate_y_px` to the objective text layer only and must also set
`objective_bottom_limit_px`; record the before/after bounds in the audit. Do not
move or resize unrelated design elements to hide the failure.

## Flattened-only fallback

- Only date/time differs and an exact same-design source exists: a pixel-slot
  transplant may be considered. Save a layered PSD containing at least the
  untouched historical poster base and a separate date/time replacement layer,
  then inspect seams at 100%.
- Title, objectives, status, or teacher differs: stop and request an editable
  PSD, or get explicit permission for an approximate rebuild.

A flattened final PNG converted to a one-layer PSD does not satisfy the normal
editable-output requirement. For a past run where the layered source was not
saved, reconstruct the PSD from the recorded base, donor, and slot audit when
those inputs still exist.

Record editability as:

- `A`: title, date, time, status, objectives, and required portrait remain
  editable in the final PSD;
- `B`: exact same-design flattened base plus a separate, editable date/time
  replacement layer, used only when those are the sole visible changes;
- `C`: one-layer final image or an approximate rebuild without the required
  editability. Do not deliver grade C.

Before using grade B, verify that the historical base visibly matches title,
teacher, delivery, objectives, dimensions, and every class-specific element.

## Reusable course PSD publication

Preflight the complete poster index before publishing any PSD. Every course
must map to one exact normalized internal-title PSD. If it already exists,
record `reuse_existing` and do not copy another file. Otherwise publish one
canonical `<course title>.psd` to the selected template's configured folder
only after the working title inspection and poster QA pass. Sanitize only
Windows-invalid filename characters; never add class, date, teacher, delivery,
version, or temporary aliases.

For a title intentionally split across visible text layers, record ordered
`title_fragments` containing layer ID, visible state, and text. Reconstruct the
poster-only cleaned title without added or missing characters, record the exact
manifest title and punctuation-cleaning rule, and bind the inspection to the
saved PSD SHA-256. Never invent a fake single-title layer for publication.

```powershell
python scripts/workflow_guardrails.py poster-psd-publish `
  --settings <project-settings.json> `
  --source-psd <working.psd> --poster-png <final.png> `
  --course-title "<course title>" `
  --template-id "<poster-template-id>" `
  --title-inspection <working-title-inspection.json> `
  [--existing-psd <exact-title-existing.psd>]
```

## Photoshop automation retry

If Photoshop exposes a transient COM/JavaScript call failure before any output
is written, release the COM object and retry the isolated operation once. Do
not retry after a partial write; remove only the just-created run outputs and
restart from the unchanged source. A second failure is a hard stop.

## Visual QA

Inspect the full poster and 100% crops around all changed regions. Confirm:

- no missing fonts or smart-object warnings;
- no clipped/overflowing Chinese text;
- preserved mixed text styles and intended line breaks;
- readable rendered title size at 100%, including the registered minimum glyph
  height per line and minimum horizontal fill;
- no title glyph, outline, or shadow touches/crosses an internal underline,
  arrow, strip edge, or other registered decoration;
- title paragraph justification and rendered horizontal center match the
  registered template contract;
- title-to-lower-block spacing passes the recorded geometry guard;
- portrait edges and shadow are clean;
- title, teacher, date, time, objectives, and delivery match the manifest;
- output dimensions/color mode match the source;
- filename is derived from the manifest and contains class, course title,
  teacher, target `M.D`, and `直播` when applicable. Generic or temporary names
  such as `c.png`, `final.png`, or `new.png` are invalid.

Run `poster-outputs-check --manifest <final-manifest.json>` after course-PSD
planning/publication. Final delivery is incomplete when a PNG lacks one
reusable exact-title course PSD mapping, when one title maps to multiple PSDs,
or when one PSD maps to different titles.

Run `manifest_finalize.py`, `poster-outputs-check`, and `delivery_check.py`
before requesting acceptance. Capture `run-cleanup-baseline` before the first
Photoshop operation. After the user explicitly accepts the Word and PNG
outputs, close Photoshop and run `final-run-cleanup --user-approved` for the
exact dated run. The cleanup removes the run directory and only Photoshop temp
files created after the baseline, writes its report outside the run directory,
and verifies protected output hashes. Do not mutate the DOCX, dated PNG folder
or reusable course PSD files after cleanup.

Also run `weekly_document.py check` on the canonical weekly DOCX. Course count
must equal PNG count, and every course must map to one non-empty reusable PSD;
multiple class rows with the same exact course title may share that PSD. These
are the last write-dependent checks. A later rename, addition, replacement, or
deletion invalidates them and requires all three delivery checks to run again.

Final cleanup must first verify the sealed Word, PNG, and reusable course PSD
outputs; require the exact dated run directory and matching cleanup baseline;
and refuse while Photoshop is open. It deletes the dated run evidence and may
delete only `Photoshop Temp*` and `~PST*.tmp` files created after the baseline.
It must never delete formal Word files, final PNGs, reusable course PSDs,
template assets, teacher assets, icons, Skill files, or pre-existing temporary
files. Preserve the cleanup report outside the run directory and verify the
protected output hashes after deletion. Use `working-psd-cleanup` only when the
user explicitly asks to retain the remaining run evidence.

Preflight all course-title mappings and publication destinations before the
first copy. This avoids duplicate course PSDs and a half-published batch.
