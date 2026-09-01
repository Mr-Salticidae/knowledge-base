# Editable poster variants

Read this reference when a poster template has one PSD per teacher or when a user replaces a template with a more editable PSD.

## Register a teacher variant

1. Preserve the supplied PSD as an immutable source under
   `模板库/海报模板/<template-id>/teacher-variants/<老师姓名>/`.
2. Inspect canvas, recursive layers, every variable text layer, portrait smart
   object, icon slots, font PostScript names, bounds, and source text.
3. Record the exact teacher name, file hash, preview, inspection, expected text,
   layer IDs, and required fonts in the template contract.
4. Keep replaced PSDs as historical artifacts and mark them non-selectable.
5. Do not confirm the template or change the default until a real edited sample
   passes QA and the user approves it.

Resolve a poster by template ID and exact normalized teacher name. Never use
another teacher's variant as the course poster. If the teacher-specific PSD is
missing, stop unless the template contract contains a user-approved
base-derivation policy. With that policy, derive the new teacher PSD only from
the named immutable base, replace only the contracted portrait smart object and
teacher-name text, keep all locked regions unchanged, export a preview and audit,
then register the new variant. An opaque portrait still requires the configured
cutout preview and explicit confirmation before the variant may be created.

## Preserve editable text

- Verify the source text before every change.
- Use Action Manager text descriptors so `textStyleRange` and
  `paragraphStyleRange` survive content replacement.
- Never move an existing layer when the contract says positions are locked.
- Capture before/after text position, font, size, leading, tracking,
  justification, and bounds.
- For a single smart-object title with internal decoration, maximize rendered
  glyph bounds inside the registered safe rectangle and validate rendered
  pixels per line, horizontal fill, and glyph-to-decoration gap. Do not use
  nominal Photoshop point size as the only readability check because inherited
  transforms vary between PSDs.
- Retry from the immutable source after any failed fit or validation.

For templates with a fixed three-row display title, split the course title into
three semantic rows before editing. Change only each title row's font size to
make it visually full inside its original paper region. Preserve font family,
weight, color, effects, transform, alignment, and layer position. Lock every
non-title font size. If fixed-size text overflows, stop and revise the wording;
do not shrink or move it.

### Template 2 paper-strip title

Derive a poster-only title by removing every punctuation mark except `+` and
`-`. Preserve the original title in the manifest, Word, filenames, and reusable
PSD key. Center every visible title row on its contracted paper strip.

- Fewer than 8 visible alphanumeric/CJK characters: keep the cleaned title
  uninterrupted on the original middle green strip; hide, rather than delete,
  title rows and paper strips 1 and 3.
- 8 or more visible alphanumeric/CJK characters: split into three semantic rows
  and fit each row inside its original strip.

No title glyph may touch another title glyph or unrelated text. Preserve title
fonts and effects, keep all non-title font sizes locked, and record the ordered
visible title fragments for exact-title publication QA.

## Font preflight

Inspect the source PostScript font names and test them inside Photoshop before
editing. A cached PSD can display a missing font correctly until text changes;
after editing Photoshop may substitute another font. Treat missing fonts or
substitution as a hard stop. Record an official activation/download source in
the contract, activate all required weights, restart Photoshop, and repeat the
preflight.

## Software icons

Keep reusable transparent icons in the configured `software_icon_folder`
(currently `图标/`) and record filename, source URL, fetch date, and hash in its
source manifest. Match tool names to icons exactly. Place replacements only
inside the contracted icon slots. Generic colored squares, text initials, or
unrecorded web images do not satisfy the template.

For template 2, fewer than four tools use left-aligned, fixed-spacing icon/name
pairs. Hide unused original name and icon layers; never invent placeholder
tools. Because its software/date paper and border artwork is merged into the
large base image, reconstruct editable overlay bases when fewer than four tools
are used: preserve the paper's left/right caps and lower-right purple sticker,
compress the software paper to remove unused-slot space, and expand the
live/recorded panel leftward by the same width. Keep these overlays layered and
editable instead of flattening them.

Keep date, weekday, and time as separate editable text layers. Use one row when
it fits; otherwise center the date above a compact weekday/time row. Preserve
each text style and reject overlap or large dead space. A software-name
paragraph box may widen into the unused gap before the next slot only when its
anchor, layer position, font, and font size remain locked and the exported PNG
proves there is no clipping or overlap.
