# Template registries

Text layout and poster design are independent assets. Never use one shared
default or one combined rule table for both.

## Files

- Text: `模板库/文本模板/text-template-registry.json`
- Poster: `模板库/海报模板/poster-template-registry.json`
- Legacy compatibility only: `模板库/template-registry.json`

The legacy combined file is deprecated. New runs use
`workflow_guardrails.py template-plan`.

The current project defaults are `text-template-1` and `poster-template-1`.
Their portable baseline assets are bundled under the Skill's
`assets/text-template-1/` and `assets/poster-template-1/`; project registries
reference those assets directly. Template-one reusable course PSDs remain in
`课程预告ps/` and are not copied wholesale into the Skill.

## Status lifecycle

Every new template is added with `status: pending`. It becomes selectable only
after visual comparison and explicit user confirmation changes it to
`confirmed`. Disabled and pending templates cannot be used or made default.

Adding never changes the default. `set-default` is allowed only when the user
explicitly says that the named template should become the default.

## Text template model

Use IDs `text-template-1`, `text-template-2`, and so on. A confirmed distilled
template records:

- immutable source DOCX and SHA-256;
- executable DOCX template;
- machine-readable contract;
- reader-facing usage guide;
- generated sample DOCX;
- renderer type and notes.

One weekly document uses one text template. A request-level
`requested_text_template_id` overrides the text registry default for that run.
There are no per-course text-layout rules.

Commands:

```powershell
python scripts/workflow_guardrails.py text-template-add `
  --registry <text-registry.json> --id text-template-2 --name 文本模板二 `
  --source-docx <source.docx> --executable-template <template.docx> `
  --contract <contract.json> --usage-guide <guide.md> `
  --sample-docx <sample.docx>

python scripts/workflow_guardrails.py text-template-confirm `
  --registry <text-registry.json> --id text-template-2 --user-approved

python scripts/workflow_guardrails.py text-template-set-default `
  --registry <text-registry.json> --id text-template-2
```

## Poster template model

Use IDs `poster-template-1`, `poster-template-2`, and so on. Each poster
template has one or more PSD/PNG source locations and may have a layer contract.
A missing layer contract means the selected PSD must be inspected and mapped
before editing; it does not authorize blind layer-name guesses.

Poster selection order:

1. `requested_poster_template_id` on the current course;
2. highest-specificity persistent rule;
3. registry default.

After resolving the template ID, rank candidate assets within that template by
teacher, class, delivery, target title line count, source title structure,
smart-object canvas capacity, and objective/date-time safe area. Template
selection does not authorize using the first filename match when its geometry
is incompatible.

A poster layer contract should record `target_title_justification`,
`title_center_target_x_px`, `maximum_title_center_delta_px`,
`minimum_title_gap_px`, `fit_to_safe_bounds`, title `safe_bounds_px`,
`minimum_font_size_pt` as the fit search floor,
`minimum_line_glyph_height_px`, `minimum_fill_ratio`,
`decoration_top_px`, `minimum_decoration_gap_px`, the date/time block layer IDs or bounds,
`minimum_objective_time_gap_px`, objective canvas bounds, and a hash of the PSD
structure used to establish the contract. Refresh the contract when the PSD
hash or mapped layer type changes. When one template registry intentionally
covers heterogeneous historical PSD structures, keep its shared layer contract
unset and build a run-scoped contract from read-only inspection of every
selected PSD; do not reuse one file's layer IDs or center target blindly.
Readability is evaluated from rendered pixel bounds rather than nominal point
size because historical text layers may carry different transforms.

Rule weights are course title 4, class 2, delivery 1. Equal-specificity matches
that point to different templates are conflicts.

Commands:

```powershell
python scripts/workflow_guardrails.py poster-template-add `
  --registry <poster-registry.json> --id poster-template-2 `
  --name 海报模板二 --poster-source <folder-or-psd> `
  --layer-contract <optional-contract.json>

python scripts/workflow_guardrails.py poster-template-confirm `
  --registry <poster-registry.json> --id poster-template-2 --user-approved

python scripts/workflow_guardrails.py poster-template-assign `
  --registry <poster-registry.json> --id poster-template-2 `
  --course-title "<course>" --class-name "<optional class>" `
  --delivery live

python scripts/workflow_guardrails.py poster-template-set-default `
  --registry <poster-registry.json> --id poster-template-2
```

Use `--replace` only after the user explicitly changes an existing identical
assignment.

## Resolved evidence

The manifest records the ID, display name, registry revision, and
`selection_source` for the weekly text template and for every course poster.
Any change resets affected approval hashes. Re-run template planning after a
registry revision changes.
