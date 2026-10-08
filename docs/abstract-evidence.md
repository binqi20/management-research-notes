# Optional PDF-derived abstract evidence

Use this only when the complete, visually verified abstract cannot match the
original text extraction because of layout or typography. Preserve the original
PDF, extracted text, frontmatter source paths and historical extraction stamps.
The default validator remains unchanged without the option. Book reviews with
no standalone abstract retain `**Abstract**` and `Not reported in paper`; they
need no alternative-evidence record.

## Prepare a local record

Inspect the original PDF and record the complete abstract boundaries. Review
both pages for continuations; exclude only verified non-abstract matter such as
acknowledgments or headers. Exact substring matching alone does not prove
completeness. Keep the record and any source-bearing files local.

Create a recipe JSON using one of these fixed extractors:

```json
{"name": "pdftotext-reading-order", "first_page": 1, "last_page": 2}
```

```json
{"name": "pymupdf-regions", "regions": [
  {"page": 1, "rect": [60, 340, 410, 495]},
  {"page": 2, "rect": [60, 70, 410, 98]}
]}
```

These coordinates are illustrative, not defaults. Pages are one-based; rectangles
use PyMuPDF page coordinates in points. Regions must be nonempty, within their
pages, nonoverlapping and ordered by page, top coordinate, then left coordinate.
For complex column layouts that cannot use this ordering, stop for source review.
The reading-order recipe needs Poppler's `pdftotext`; region recipes need Python
`PyMuPDF`. Neither is required for the default original-text check.

Supply a separate boundary-review JSON, written only after inspecting the PDF:

```json
{
  "complete": true,
  "reviewer": "<actual reviewer/context>",
  "source_location": "<PDF pages and abstract boundaries>",
  "rationale": "<why these spans comprise the whole abstract; excluded furniture>"
}
```

With the corrected abstract in a local candidate note, run:

```sh
python3 tools/abstract_evidence.py <candidate-note.md> \
  --recipe-json <recipe.json> --review-json <boundary-review.json> \
  --output <new-local-evidence.json>
python3 tools/validate_note.py <candidate-note.md> \
  --abstract-evidence <new-local-evidence.json>
```

The generator does not invent the review or overwrite an existing record. It
records schema `pdf-abstract-evidence-v1`, paper ID, unchanged source paths,
PDF/text byte hashes, abstract UTF-8 hash (as parsed by `parse_body_sections`),
actual extractor version, recipe, reproduced text hash and boundary review.
The validator reruns the fixed extractor on the actual PDF and verifies every
binding. It never runs commands supplied in JSON or trusts a supplied transcript.

## Matching and limits

The optional path joins U+00AD followed by an actual line break before whitespace
normalization and expands the seven Latin presentation ligatures `ﬀ ﬁ ﬂ ﬃ ﬄ ﬅ ﬆ`.
It then uses the existing whitespace normalization and tolerates word-internal
ASCII hyphens between letters, with exact substring comparison. Numeric signs
and range separators are preserved; the legacy hyphen-agnostic fallback is not
used on this optional path. It does not use fuzzy matching, delete arbitrary words,
alter numbers or change evidence-anchor/claims-quotation normalization.

Changed source files, extractor versions, reconstructed text, paper identity or
abstract bytes invalidate the record. Even a shorter matching excerpt requires
a new boundary review and evidence record. Supplying invalid evidence fails
closed even if the abstract happens to match the old extraction. A valid record
establishes reproducibility, not the truth of a reviewer's boundary judgment.

## Review and publication

Run the normal validation, numeric adjudication and fresh independent holistic
and claims reviews. Preserve the standard fitted source for both readers; retain
the PDF boundary review separately for parent adjudication. This path does not
change the fitter, schemas, original reader judgments or claims quote rules.

Add the local record's path and byte hash as `abstract_evidence` in the
[publication review](publication-readiness.md). The gate replays the check;
omitting the reference uses the original-text check and cannot silently waive
its failure. Publish only eligible notes after all other corrections and
authorizations are resolved. Full PDFs, extracted text and source-bearing
evidence remain local. A change to a protected frontmatter field still requires
its own exact authorization.
