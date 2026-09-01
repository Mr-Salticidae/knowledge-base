# Teacher portrait assets

## Configure the authoritative folder

Never infer the folder from a name such as `卡通`. If project settings are
empty, ask the user to identify the folder, then record it:

```powershell
python scripts/workflow_guardrails.py teacher-folder-set `
  --settings <project-settings.json> --folder <user-specified-folder>
```

Only PNG files are selectable. Report matching JPG/ZIP files as unsupported
rather than silently converting them.

## Decide whether a portrait is needed

Inspect the chosen PSD first. For a generic PSD with a visible person slot,
require a portrait from the configured authoritative folder. A contracted
teacher-specific PSD variant is different: its exact teacher match satisfies
the portrait requirement, and its built-in person remains unless the user
explicitly requests a replacement. Never use a different teacher's variant as
the course poster. When the template contract records a user-approved
base-derivation policy, a missing variant may be generated from the named base
using this portrait workflow, but only the allowed portrait and teacher-name
layers may change and the result must pass QA before registration.

For a generic PSD, record the requirement:

```powershell
python scripts/workflow_guardrails.py teacher-asset-require `
  --manifest <manifest.json> --teacher "<teacher>" `
  --reason "poster has a person slot; authoritative portrait required" `
  --out <manifest.json>
```

Then plan candidates. An unneeded course is limited to a poster design with no
visible person slot and records `not_required_no_portrait_slot`.

## Name matching and multiple images

Match the teacher name without a trailing “老师”. Valid examples include
`卡卡.png`, `卡卡1.png`, `卡卡_半身.png`, and `卡卡形象二.png`.

- zero matches: stop and request a PNG;
- one unique match: select it and show the filename;
- multiple matches: show every full filename and relative path, then ask the
  user to reply with the exact filename;
- duplicate identical filenames in subfolders: stop and ask the user to rename
  them uniquely because a filename alone cannot identify one.

Record an explicit selection:

```powershell
python scripts/workflow_guardrails.py teacher-asset-select `
  --settings <project-settings.json> --manifest <manifest.json> `
  --teacher "<teacher>" --file-name "<exact filename.png>" `
  --out <manifest.json>
```

## Transparency audit

Run `alpha-audit`, but treat its output as a screening signal only. A PNG may
have an alpha channel while still containing a solid rectangular background.
Inspect the image on checkerboard, white, and dark backgrounds.

The placed smart object or raster layer must contain only the person subject.
Do not carry any original photo background, generated backdrop, floor, wall,
frame, or rectangular matte into the final poster.

## Background removal and confirmation

When the background is not transparent:

1. Use the image-editing workflow to isolate only the person.
2. Preserve identity, face, hair, clothing, pose, proportions, and canvas size.
   Do not beautify, redraw, add accessories, or alter the pose.
3. Save a temporary PNG outside the authoritative reference filename.
4. Show the cutout on checkerboard, white, and dark backgrounds. Inspect hair,
   fingers, clothing edges, holes, and residual color spill.
5. Ask the user for explicit confirmation.
6. After approval only, commit it:

   ```powershell
   python scripts/workflow_guardrails.py cutout-commit `
     --settings <project-settings.json> `
     --original <reference.png> --processed <approved-cutout.png> `
     --user-approved
   ```

The helper preserves canvas size, requires real transparent pixels, creates a
recoverable copy in `_原图备份/`, verifies hashes, and atomically replaces the
original filename. Never delete the backup automatically.
