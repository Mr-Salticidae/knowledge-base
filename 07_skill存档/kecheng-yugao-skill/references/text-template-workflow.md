# Extracting a text template from a DOCX

Use this workflow whenever the user provides a new course-preview DOCX style.
The latest supplied file does not automatically become active or default.

## Required outputs

For `text-template-N`, preserve or create:

1. untouched source DOCX;
2. executable DOCX template;
3. contract JSON/Markdown;
4. generated sample DOCX;
5. rendered comparison images/PDF;
6. reader-facing usage guide;
7. source SHA-256 and pending registry entry.

## Distillation procedure

1. Copy the supplied DOCX into `模板库/文本模板/text-template-N/` without
   modifying it.
2. Use the documents workflow to inspect document structure, styles, direct run
   formatting, section/page settings, tables, headers/footers, numbering, and
   embedded objects.
3. Render all pages. The Word style name alone is not proof of visible
   formatting because direct formatting may override it.
4. Identify four semantic examples:
   - recorded summary;
   - live summary;
   - recorded detail;
   - live detail.
5. Replace example values with placeholders or content controls while retaining
   paragraph/run/table structure. Do not duplicate a live row to represent a
   recorded row when its visual rules differ.
6. Write a contract that maps manifest fields to document positions and records
   repetition, optional blocks, conditional live/recorded formatting, spacing,
   page breaks, and missing-field behavior.
7. Generate a sample containing at least one live and one recorded course.
8. Render source and sample and compare every page.
9. Run the PDF layout guard. It must reject a nearly empty final spill page, a
   class heading separated from its first course row, and a page beginning with
   a detached notification, time, or objective continuation.
10. Register it as `pending`; show the user the sample and usage guide.
11. Only after explicit confirmation run `text-template-confirm`. Changing the
    source file after distillation invalidates confirmation.

## What counts as a valid course-preview format

A valid format must make these meanings unambiguous:

- class heading;
- target date;
- course title;
- teacher;
- delivery state, with a defined live visual treatment;
- time location;
- course detail boundary;
- tools field;
- optional homework behavior;
- non-empty objectives;
- order and spacing of repeated course blocks.

The supplied DOCX must contain or explicitly define both live and recorded
behavior. If it shows only one, ask the user to provide the missing example or
approve a clearly described derived rule.

## Usage guide shown to the user

The guide must say, in plain language:

- which visible block becomes a class heading, summary, and detail;
- which data fills each placeholder;
- how live differs from recorded;
- how multiple classes repeat;
- what happens when tools/homework are empty;
- what fields cause a hard stop;
- how to request this template for one run;
- how to make it the text default.

The guide and rendered sample are the user's review surface. Do not ask the user
to validate raw JSON or WordprocessingML.

## Separation from weekly deliverables

Source examples, distilled templates, generated samples, rendered comparisons,
and template approval files stay in the template library or the dated run
directory. They must never be saved as weekly variants in `课程预告文本/`.

Every text template, regardless of style revision, publishes through the same
weekly-document rule: one date range, one canonical formal DOCX, with drafts and
backups outside the final folder.
