# Decision rules

## Source authority

- Schedule image: authority for whether a class meets, visible course title,
  class identity, and live/recorded color or legend.
- Historical course-copy DOCX: authority for teacher attribution and course
  details.
- Poster/PSD filename and visible content: corroboration and template matching;
  not authority when it conflicts with the DOCX.
- Configured teacher portrait folder: authority only for which user-provided PNG
  may replace an image. A filename is not evidence that the course teacher is
  correct.
- Template registries: authority for template IDs, defaults, status, rules, and
  asset locations.

## Date and weekly file

- Use the date supplied by the user, not the system date.
- Resolve the weekly document before Stage A. For one date range, the final
  folder must contain exactly one formal DOCX named
  `<period start M.D>-<period end M.D>课程预告.docx`.
- If no matching weekly DOCX exists, create the canonical file. If exactly one
  exists, update that weekly document through a run-directory working copy.
- If two or more matching weekly DOCX files exist, stop and report every full
  path. Never choose by suffix, modification time, or words such as `FINAL`.
- Re-running the same target date replaces that date's course section by stable
  course keys; it must not append a duplicate date section.
- Drafts, approval copies, QA renders, and backups belong only under
  `_course_preview_runs/YYYY-MM-DD/`. The final folder must not contain weekly
  variants such as `_基础信息`, `_待确认`, `_DRAFT`, `_FINAL`, `_new`, or `_v2`.
- When the only existing weekly file has a legacy suffix, it may be consolidated
  to the canonical name only during backed-up atomic publication.
- If no weekly range contains the target, use
  `<target M.D>-<Friday M.D>课程预告.docx`.
- A weekend date is allowed only when the schedule visibly contains a weekend
  course or the user explicitly instructs it.

## Title matching

Normalize Unicode width, whitespace, punctuation, quote marks, and capitalization.
Do not silently correct the schedule. Preserve the verbatim title separately.

Use an exact normalized title match for teacher/detail extraction. A fuzzy match
is a candidate list, never automatic evidence. Equal or conflicting candidates
require user confirmation.

## Delivery and time

Read each schedule image's own legend before interpreting its cells. Color
mappings are local to the image: green, pink, orange, or another color may mean
live in different schedules. Never carry a color mapping from one class image
to another.

Use a two-pass scan: pass one counts course blocks only; pass two transcribes
them from top to bottom. Preserve a target-cell crop in `schedule-evidence/`
when practical. Record the expected block count and a 1-based index for each
course. The class extraction is invalid unless its indices equal exactly
`1..expected count`. A shared class heading in Word does not merge its courses.

Read delivery only from the current schedule's legend/cell encoding, an explicit
schedule label, or explicit user confirmation. Store the block color, legend
text, evidence source, and evidence statement. Do not infer delivery from course
history, time, teacher, common practice, or words in the course title. In
particular, `直播间`, `直播贴片`, and a bare occurrence of `直播` inside a title
are not proof of a live class.

Historical DOCX delivery is supplementary catalog metadata only. Parse it only
from explicit markers such as `直播预告通知`, `录播课程已更新`, or a standalone
`（直播）`; when no explicit marker exists, store `unknown` rather than defaulting
to recorded. Historical delivery never overrides Stage A schedule evidence.

The time must come from the schedule, current trusted copy, or user confirmation.
Do not carry an old time into the new date merely because the course title
matches.

Treat delivery and time as a coupled review unit but as separate facts. If a
user changes `live` to `recorded` or the reverse, show both old and proposed new
values. A delivery-only instruction does not authorize inventing a new time.

## Course changes and semantic diff

Identify a course by normalized class plus normalized course title, never by a
DOCX paragraph index. Apply changes to the manifest, regenerate outputs, and
compare the before/after manifests. A one-course request must produce a diff for
exactly that course; any other changed course is a hard stop. Reset the Stage A
approval fingerprint whenever an approved field changes.

## Confirmed aliases and field evidence

A fuzzy historical match remains a hard stop until confirmed. After explicit
confirmation, persist an alias mapping with canonical title, matched title,
teacher constraint, source, and confirmation timestamp. Reuse it only when the
constraints still match.

Record provenance separately for tools, homework, and objectives. A field
borrowed from an exact-title/teacher poster must retain poster provenance and
must not be described as DOCX-sourced. Conflicting field sources require user
confirmation.

## Template selection

Text and poster templates have separate registries and defaults. Adding a new
template does not make it default.

An explicitly named template applies only where the user scopes it. Persistent
course/class/delivery rules apply after explicit choices. Default applies last.
Never interpret “latest” or highest template number as an automatic choice.

## Portrait decision

First inspect the chosen PSD:

- matching teacher already present and no replacement requested: portrait asset
  is not required;
- new/different teacher or explicit replacement: portrait asset is required;
- teacher identity cannot be determined: stop and ask rather than replacing.

Select only PNG files from the user-configured folder. One match may be selected
automatically. Multiple matches require the exact filename. Identical filenames
in different subfolders are ambiguous and must be renamed before use.

An alpha channel alone does not prove the background is removed. Inspect the
pixels visually. Replacing the reference file after cutout always requires an
approved preview and a recoverable backup.

## Output safety

- Copy source DOCX/PSD before modification.
- A source path may never equal an output path.
- Never edit a formal weekly DOCX in place. Back up the current weekly document
  in the run directory, validate a temporary DOCX, and use atomic replacement
  to publish the canonical filename. Historical PSD and poster sources must not
  be overwritten. The configured PSD output folder may also contain historical
  sources; reuse one exact-title PSD per course instead of publishing a dated
  copy for every poster.
- Stage A and Stage B working DOCX files must remain in the run directory. Only
  the approved, detailed, validated document may be published to
  `课程预告文本/`.
- Save one temporary working PSD for every generated poster in the dated run
  folder. Keep it through visual QA and user acceptance; it is not a permanent
  deliverable.
- Identify reusable course PSDs by exact normalized text read from the title
  smart object. Filenames and substring matches are only search hints. Zero
  exact matches allows one new course PSD; one exact match is reused without
  publishing another; multiple exact matches stop for deduplication.
- Resolve the reusable PSD folder by selected poster template ID. For template
  two use `课程预告ps第二版`; do not mix it with legacy/template-one PSDs in
  `课程预告ps`. Name every reusable PSD from the exact manifest course title,
  sanitizing only characters Windows forbids in filenames. Never add class,
  date, teacher, delivery, template number, or version suffix.
- Completion requires every final PNG to map to a non-empty reusable course PSD
  in the configured output folder. Multiple PNGs for the same exact course title
  may share that PSD. Different course titles may not share one PSD.
- If an existing course PSD differs in teacher, objectives, portrait, or poster
  template, stop. Because the storage rule permits only one PSD per course,
  replacement requires explicit user approval and a recoverable backup.
- Exported poster content and filename must agree with the final manifest. The
  stem must contain class, course title, teacher, target `M.D`, and `直播` for a
  live course; temporary aliases such as `c.png` are invalid.
- Treat the final manifest, poster-output check, and delivery check as a sealed
  handoff set. Any later rename, replacement, addition, or deletion invalidates
  the checks and requires the entire final sequence to run again.
- Capture a Photoshop temporary-file baseline before the first Photoshop
  operation. After the user explicitly accepts the Word and PNG outputs, close
  Photoshop and delete the exact dated run directory in full: drafts, backups,
  schedule evidence, inspections, QA renders, failed attempts and working PSDs.
  Record paths, sizes and hashes in a cleanup report outside the run directory.
- Photoshop residue cleanup is a baseline difference, never a broad Temp-folder
  purge. Delete only root-level/user-temp files named `Photoshop Temp*` or
  `~PST*.tmp` that were absent from the run baseline. Preserve every pre-existing
  temporary file and refuse cleanup while Photoshop is running.
- Never include reusable course PSDs, final PNGs, formal Word files, template
  assets, teacher assets, icons, Skill files or any other path outside the exact
  run directory and the baseline-diff Photoshop temp set.
- The sealed handoff also requires a weekly-document check: exactly one matching
  weekly DOCX, exact canonical filename, valid DOCX package, and expected hash.
- If a PSD is linked, missing a required editable layer, or structurally
  different from its contract, stop before editing.

## Layout regression rules

- Group repeated courses under one class heading in both Stage A and Stage B;
  do not repeat the heading for each course in the same class.
- Keep each class heading with the next course row/block. Render every DOCX
  page and reject an orphan heading or a nearly empty final page caused by a
  single objective spilling over.
- Reject a page that begins with a notification, time, topic, teacher, tool,
  homework, or objective line detached from its class/course heading. PDF text
  extraction may replace or omit a leading emoji, so use semantic time and
  notification patterns instead of relying only on the glyph.
- Preserve explicit line breaks when the replacement title needs them. Record
  the source title's existing smart-object overflow allowance and reject any
  replacement that exceeds it.
- Inspect the title smart object's actual text, paragraph justification, and
  rendered bounds; a matching PSD filename is not proof of matching internal
  content. Require an explicit template target justification and horizontal
  center target. Reject a grade-A title whose absolute center delta exceeds the
  configured tolerance.
- Record the title block bounds and the next lower content block. A template
  contract should define a minimum gap; the default guard is 20 px. Reject an
  overlap or a smaller gap before publishing.
- Before replacing mixed-style objective text, inspect text and paragraph style
  ranges. Preserve and extend terminal ranges, then inspect the result again.
- Treat the date/time block as a protected poster safe area. Require the
  objective text's right edge plus the contract gap to stay left of the
  date/time block, and require its bottom edge to remain inside the canvas.
- Grade poster PSD editability: `A` fully editable, `B` compliant layered
  date/time fallback, `C` flattened or insufficient. Grade C is not deliverable.

## Batch publication and reuse

Before copying any new course PSD, preflight the whole batch for working-source
existence, final PNG existence, exact internal title evidence, unique
course-title-to-PSD mappings, and destination conflicts. Publish only titles
with zero existing matches. A partial publish is an incomplete run and must be
reported as such.

## Historical text catalog hygiene

Only canonical weekly filenames are eligible historical course-copy sources.
Skip legacy weekly variants with suffixes such as `_FINAL`, `_new`, or `_v2` so
that multiple versions of the same course cannot create false exact matches.
