# Independent claims verification

**Pass:** claims-v1. **Rubric provenance:** v3 from v0.70.0.

You are a fresh independent reader. You did not extract, augment, repair or
holistically audit this note. Your only analytical input is this prompt. Read
the complete note and supplied PDF text; do not consult other notes, reports,
repair histories or external sources. Return evidence, not rewritten prose.

## Task and coverage

List **every atomic checkable claim** in Hypotheses / Propositions, Data &
Measures and Key Findings, including hypotheses, measures, samples, controls,
results, numbers, units, formulas, study attribution and robustness qualifiers.
In the six legacy fields (Research Question, Mechanism Process, Theoretical
Contribution, Practical Implication, Limitations, Future Research), list every
direction word, prescription and generalizability target. Do not sample claims
or stop after finding an error. Read every target field and inventory its clauses
before checking them. Split compound claims when their support differs; repeat a
verbatim note clause in multiple rows if necessary to check distinct components.
Use `scope` for a checkable claim that fits none of the more specific types.

Before checking evidence, make an ordered inventory through the end of every
sentence. Relative clauses, parenthetical qualifications, comparisons and
attributions are claims too. Do not omit a clause because the preceding main
clause already has a row. A shorter `note_clause` must retain the words that
make the claim checkable: actor, action, object, unit and qualifier as relevant.

**Semantic check before SUPPORTED.** Quotation membership is a separate, later
check; a matching phrase is not sufficient evidence. For every claim:

1. Read the complete source sentence or table region, including column headers,
   row labels, unit labels, totals and relevant footnotes. For each reported
   quantity check the value and the unit separately, with separate rows if
   needed. A row label names what was observed; it does not by itself establish
   what unit the table counted.
2. For a direction, write in `note` who or what acts on whom, or what increases
   or decreases relative to what. Compare that mapping with the exact note
   clause. Shared nouns or a plausible recommendation do not establish direction.
3. For a formula, write the ordered operations in `note`, including the index
   over which each sum or average is taken. Compare the source's operation order
   and grouping with the note's; matching variable names cannot establish an
   equivalent formula.
4. For a claim applying across cases, tests, studies, stages or cycles, enumerate
   the relevant members and check the claim against each, including the final
   member. A process description may have an endpoint that differs from earlier
   transitions. A true statement elsewhere in the field does not cancel an
   overgeneralized statement.
5. For attribution or prescription, check the complete asserted action and its
   actor and status: a warning, proposal, recommendation and an already-applied
   requirement are different claims. Check the relative clause as well as the
   main recommendation.
6. Actively look for source text that limits or conflicts with the claim before
   accepting it. If the claim and source differ, record UNVERIFIED or
   CONTRADICTED rather than explaining the difference away as broadly accurate.

Choose a source fragment that bears the relevant evidence, not merely a generic
noun or a phrase such as “the first author” or “the results.” Its surrounding
context must support the whole atomic claim. If multiple separated fragments
are needed, use multiple rows with the same note clause and explain how each
bears on it; never stitch the fragments into a fabricated quotation. After
checking, compare the rows with the initial inventory to detect omitted tails
or qualifiers. Missing coverage is an incomplete pass, not tacit support.

For each claim, provide a verbatim source fragment of at most 25 whitespace-
separated words and one of:

- `SUPPORTED`: the fragment and its context support this exact claim, including
  unit, direction, study and scope. Numeric presence alone is insufficient.
- `UNVERIFIED`: the supplied source does not establish the claim, or the source
  is ambiguous or missing. State what remains unverified. Use an empty fragment
  only when no relevant fragment exists; never fabricate evidence of absence.
- `CONTRADICTED`: an affirmative source statement conflicts with the claim;
  quote that conflicting fragment and name the conflict.

Check aggregation step by step, not by similar terminology. Check each test in
“all,” “every,” “across all” or “robust to” claims. Preserve the study and outcome
attached to each sample, control, threshold and result. Distinguish descriptive
findings from recommendations; do not invent a practitioner audience or a
generalizability target. Resolve direction words by identifying both actors.

Known pdftotext artifacts include `=` rendered as `5`, minus rendered as `2`,
`<` rendered as `,`, and two-column line splices. Read the surrounding layout;
do not treat a zero-hit phrase search as proof of absence. Quote a short
contiguous fragment from the supplied text, preserving its artifacts. A fragment
may span whitespace or a line wrap, but must not silently remove an intervening
column or join separate passages. Explain the surrounding evidence in `note`.

The shared input preamble may use the holistic rubric's word PARTIAL for possible
truncation. This pass has no PARTIAL status: use UNVERIFIED for that uncertainty,
identifying the possibly missing evidence. Do not guess from prior knowledge.
Legitimate “Not reported in paper” sentinels are not invented substantive claims;
describe them only if a checkable claim remains. Empty coverage is not a completed
claims pass and requires parent review.

**Verify the note against the paper, not the paper against your own analysis.**
If the note faithfully repeats an internally inconsistent statistic in the
paper, that is not a source contradiction. Mark the faithful claim SUPPORTED
and explain the paper-internal inconsistency in `note`; the parent records it
separately. A clearly implied design characterization can be supported by the
reported methods even when the paper does not use the note's exact terminology.

**Mechanical quotation check before submission.** Extract the note body and
the PDF-text block separately from this prompt. The PDF-text block begins after
`## PDF text (the source of truth)`; neither the note body nor the task text is
source evidence. Use a local script to verify that each `note_clause` is an exact
substring of the note body and each nonempty `source_fragment`, after collapsing
whitespace, is a substring of that PDF-text block. Use only this prompt and your
own output for this check; do not read tools, external texts or other artifacts.
Check the 25-word limit too. Do not substitute synonyms, normalize printed math
glyphs, remove intervening columns, or copy a note clause as evidence unless it
also occurs in the PDF block. Shorten an overlong or spliced quote to a genuinely
contiguous fragment and explain its context in `note`. If you cannot locate
support, use UNVERIFIED with an empty fragment. Never make a claim SUPPORTED
merely to complete the inventory. These checks establish quotation membership,
not semantic support; read the surrounding passage to judge the claim.

## Output format — strict JSON

Return only one JSON object, without fences or commentary. No extra keys.
The parent supplies the exact provenance values in this prompt; use them
without changing hashes. The parent verifies the actual model from runtime
metadata. `generated_at` is the UTC completion time in ISO 8601 form.

```json
{
  "provenance": {
    "paper_id": "the paper id supplied by the parent",
    "note_sha256": "SHA-256 of the full raw note text supplied by the parent",
    "text_sha256": "SHA-256 of source loaded with errors=replace, supplied by the parent",
    "rubric_version": "v3",
    "auditor_model": "the runtime-verified reader model supplied by the parent",
    "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
    "dispatch_mode": "codex-independent-agent",
    "input_mode": "standard-fitted",
    "pass": "claims-v1"
  },
  "claims": [
    {
      "field": "data_measures",
      "note_clause": "an exact contiguous substring of the note body",
      "claim_type": "number",
      "status": "SUPPORTED",
      "source_fragment": "an exact contiguous supporting or conflicting fragment, at most 25 words",
      "note": "Explain the match, limitation or conflict, including the study and referent."
    }
  ]
}
```

`field` is one of `research_question`, `mechanism_process`,
`theoretical_contribution`, `practical_implication`, `limitations`,
`future_research`, `hypotheses`, `data_measures`, `key_findings`; only use fields
present in this note. `claim_type` is exactly one of `number`, `unit`, `direction`,
`formula`, `robustness`, `attribution`, `prescription`, `scope`. Every row has all
six string-valued keys shown above. Preserve note spelling and punctuation in
`note_clause`; paraphrases are not verbatim. Coverage and semantic support are
reviewed by the parent, not inferred from valid JSON.

## Parent assembly contract

The claims reader is separate from the holistic reader and from every writer.
Use a different OpenAI model when runtime metadata verifies that it is available;
otherwise record the same-model, separate-context fallback in the ledger. Both
readers receive identical fitted source text through the audit tool's prompt
modes. Run `check_numbers.py` first; adjudicate each zero-hit token against raw
lines before dispatch. Neither numeric matches nor reader agreement prove truth.

Before assembly, the parent checks every reader disagreement and every UNVERIFIED
or CONTRADICTED claim against the raw source (two-channel verification), records
the disposition and raw lines in the batch ledger, and checks inventory coverage.
Assemble every report in the wave before making any repair. A parent-confirmed
contradiction is repair-class; a repaired note receives fresh readers again.
Layer-2 field verdicts remain the official gate. A passing report alone does not
waive these ledger and adjudication requirements. The staged retrospective pass
uses the reader count selected by the recorded calibration decision rule.
