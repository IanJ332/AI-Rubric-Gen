# CS50x 2026 Rubric Benchmark Implementation Plan

Scope: Python **Cash, Readability, and DNA** from Problem Set 6. Completion means all three assignments run through the same generation entry point, using the existing 48 conditions across four assignments. This plan describes sources, input contracts, 15 candidate flaws, validation cases, and execution gates. Files, commands, and API requests in the plan are future implementation work.

## 1. Sources and use

| Source | Project use |
|---|---|
| User-provided *Harvard CS50x 2026 Assignments*, pp. 4–5 | Locate the three Python versions in Problem Set 6. Cash also has a C assignment in PSet 1 and Readability in PSet 2; verify edition and Python filenames when archiving. |
| [CS50x 2026 Problem Set 6](https://cs50.harvard.edu/x/psets/6/) and the three official assignment pages | Authority for requirements, terminology, input/output, and official tests. Archive each page with edition, retrieval time, and hash. |
| [Week 6 notes](https://cs50.harvard.edu/x/notes/6/) | Check Python teaching context. Examples aid researcher understanding and do not become grading criteria. |
| Check-in #2, pp. 2–3 | Establish four factors, five flaws per assignment, one formal generation per cell, and independent annotation by two researchers. |
| User-provided *CS500 Check-in 2 Research Dossier*, pp. 5–11 | Adopt recommendations on identical bytes per assignment, freezing flaws in advance, validating a single observable error, and recording valid alternatives and model versions. Follow Check-in #2 for rubric-text coverage. |

Read each official page's `Problem to Solve`, `Specification`, and `How to Test` first. For DNA also archive the official [2026 starter ZIP](https://cdn.cs50.net/2026/x/psets/6/dna.zip), verify its `dna.py`, `databases/`, and `sequences/`, and record SHA-256 hashes for the archive and files used. Retain Harvard attribution, source, change descriptions, and license links with course materials, and separately record any license or provenance notices included in the ZIP. Review applicable terms before public distribution. [CS50x license](https://cs50.harvard.edu/x/license/)

### Data package and prompt boundary

Follow [Mario's directory, fields, and validation](../data/assignments/mario-more/provenance.json). Reuse `load_generation_input` directly in the initial implementation.

| Planned path | Content and consumer |
|---|---|
| `data/assignments/<id>/source.html` | Original official page for provenance and human review. |
| `data/assignments/<id>/specification.txt` | Only course text given to the LLM; UTF-8, LF, preserving meaningful whitespace and punctuation. |
| `data/assignments/<id>/reference.py` | One team-authored Python example validated against official cases. Include frozen bytes under `spec-reference`. |
| `data/assignments/<id>/provenance.json` | Retain `assignment_id`, `publisher`, `requested_url`, `resolved_url`, `redirect_status`, `accessed_at_utc`, `edition`, `selection`, `license`, `reference_author`, `sha256`, and `requirements`. Add official check ID, extraction rule version, reference runtime environment, and DNA starter provenance. |
| `data/evaluation/<id>/flaws.json`, `evidence.json`, `fixtures/` | Five stable flaw IDs per assignment, requirement IDs, expected and incorrect behavior, case and evidence locations, status, and review records. Archive evidence from official and targeted cases and correct alternatives here. |

**Recommended text rule for freezing:** Extract official `Problem to Solve` and `Specification` into the prompt consistently for all four assignments. Use official `How to Test`, notes, installation steps, DNA ZIP, and custom cases for validation. Retain the official `longest_match` explanation in DNA's specification block. The current Mario development version includes test examples; if the team adopts this rule, rebuild Mario's `specification.txt` and hash using the same rule at formal freeze, retaining the original development snapshot and change record. Before the pilot, the team verifies that all four use the same extraction rule.

First accept each package's explicit CS50x 2026 edition label, actual redirect, and hashes, then compare extracted text paragraph by paragraph. Preserve headings, formulas, output literals, source symbols, and original conditions. The generation process reads only validated specifications and optional references; offline preflight checks other materials and manifest digests.

## 2. Assignment engineering tasks

### Cash

**Specification and reference.** Validate at the official path `sentimental-cash/cash.py`. The reference uses CS50 `get_float` to read dollars, repeatedly rejects negative values, and accepts zero. Convert valid amounts with at most two decimal places to integer cents and find the minimum number of 25, 10, 5, and 1 cent coins. The reference may use `divmod`, retaining each remainder, and prints an integer and newline on the last line. Grade behavior and accept other compliant strategies. The specification does not prescribe sub-cent rounding. [Official Cash specification and cases](https://cs50.harvard.edu/x/psets/6/cash/)

| Candidate flaw ID | Validation input and correct behavior | Distinguished error |
|---|---|---|
| `cash.negative-reprompt` | Input `-1`, `-0.25`, `0.50` in order; read three times and finally output `2\n`. | Accepting a negative, stopping on a negative, or allowing only one retry. |
| `cash.cents` | Calculate `0.29` as 29¢ and output `5\n`. | Directly truncating the binary floating-point product to 28¢ and outputting `4\n`. |
| `cash.minimum` | `0.50` outputs `2\n`. This case divides evenly with no penny remainder. | Using five 10¢ coins to reach the correct total without minimizing the count. |
| `cash.remainder` | Official `0.41` outputs `4\n`; a valid combination is 25+10+5+1. | Omitting the last 1¢ after the first three denominations and outputting `3\n`. |
| `cash.final-line` | The last line for `0.01` is `1\n`; earlier prompts are allowed. | Correct value but last line is `1 coin\n` or lacks a final newline. |

**Validation.** Use a `get_float` stub to test negative retry counts and valid zero. With the real CS50 library, also test nonnumeric input and a blank line followed by valid input, distinguishing library parsing from the program's nonnegative constraint. Run all official examples, including `0.15 → 2`, `1.60 → 7`, `23 → 92`, and `4.2 → 18`. Independently check custom cases with an integer minimum-coin calculation. Official check ID: `cs50/problems/2026/x/sentimental/cash`.

### Readability

**Specification and reference.** Validate at `sentimental-readability/readability.py`. Use CS50 `get_string`; count ASCII letters, space-delimited words, and `.`, `!`, `?`. With letters, words, and sentences `a, w, s`, calculate `L = 100*a/w`, `S = 100*s/w`, and index `0.0588*L - 0.296*S - 15.8`. Round to the nearest integer under the official rule and output `Grade X`, `Grade 16+`, or `Before Grade 1`. Accept character checks, regular expressions, or equivalent counting methods. [Official Readability specification and cases](https://cs50.harvard.edu/x/psets/6/readability/)

| Candidate flaw ID | Validation input, counts `(a,w,s)`, and expected output | Distinguished error |
|---|---|---|
| `readability.letters` | `Green birds fly high above lakes 1234567890.` → `(27,7,1)` → `Grade 3`. | Counting digits as letters produces `Grade 11`. Add a case with non-ASCII letters to check the range. |
| `readability.words` | `Don't stop looking around the garden.` → `(30,6,1)` → `Grade 9`. | Splitting `Don't` into two words produces `Grade 5`. |
| `readability.sentences` | `Bright stars! Silver moons? Lanterns shine.` → `(35,6,3)` → `Grade 4`. | Recognizing only periods produces `Grade 14`. |
| `readability.index` | `Bright stars shine above the lake.` → `(28,6,1)`, raw index approximately `6.7067`, output `Grade 7`. | Truncation gives `Grade 6`; omitting per-100-word normalization gives `Before Grade 1`. Group both under index calculation and rounding. |
| `readability.grade-labels` | `Small cats nap.` → `Before Grade 1`; `Extraordinary discoveries inspire curiosity.` → `Grade 16+`. | Printing numerical grades at the low or high end or using incorrect labels. |

**Validation.** Run all official input texts and outputs. Independently calculate counts, raw indices, and labels for synthetic cases by hand or exact rational arithmetic. Cover ASCII range, sentence punctuation, ordinary grades, and both ends of the scale. Before using rounding examples that cross a threshold, compare official wording, [the referenced PSet 2 description](https://cs50.harvard.edu/x/psets/2/readability/), and available 2026 Python checks; record both raw index and rounded grade. Use the above end cases away from thresholds as formal flaw cases. Keep empty input, consecutive spaces, and exact half-integer behavior as researcher notes until official evidence is clear. Official check ID: `cs50/problems/2026/x/sentimental/readability`.

### DNA

**Specification and reference.** Validate at `dna/dna.py`. Accept two file paths, CSV first and sequence text second; print an error for any other argument count. With the correct count, the official task permits assuming both files are valid. Read the CSV header and use fields after `name` to determine the STRs to compare. Compute the longest consecutive run for each field, exactly match all fields for one person, and print the name or `No match`. Start the reference from the official starter, record the origin of `longest_match`, and archive a runnable single-file reference. Accept functionally equivalent parsing and implementations. [Official DNA specification and cases](https://cs50.harvard.edu/x/psets/6/dna/)

The table uses `/` to separate CSV rows. Write real CSV and text files during implementation.

| Candidate flaw ID | Validation input and correct behavior | Distinguished error |
|---|---|---|
| `dna.arity` | Run with 0, 1, and 3 file arguments; each prints an error and exits. Verify the normal branch with 2 valid paths. | Incorrect counts cause an unhandled exception or continued argument access. The author chooses the error text. |
| `dna.csv-fields` | CSV `name,CG / Ada,2 / Bea,1`, text `CGCG`, output `Ada`. Also cover different column counts using the official small and large databases. | Hard-coding a set of STR columns or relying on a particular official database shape. |
| `dna.longest-run` | CSV `name,AC / Ada,3 / Bea,4`, text `ACACACGGAC`, output `Ada`. | Summing separated occurrences to get 4 and incorrectly reporting `Bea`. |
| `dna.exact-profile` | CSV `name,AC,GT / Bea,2,2 / Ada,2,1`, text `ACACGT`, output `Ada`. | Accepting the first row's partial match and incorrectly reporting `Bea`. |
| `dna.no-match` | CSV `name,AC,GT / Ada,1,2`, text `ACACGT`, output `No match`. | Silently exiting, printing the wrong message, or returning a person's name when no match exists. |

**Validation.** Use real files and subprocesses to check argument order, error branches, and standard output. Run the 20 official documented examples: four with the small database and sixteen with the large database. Retain evidence of at least one positive and one negative result, such as small database `1.txt → Bob` and `2.txt → No match`, and save status for all cases. The task does not require a particular CSV library, recovery from invalid files, or handling multiple exact matches. Official check ID: `cs50/problems/2026/x/dna`.

## 3. Reference and flaw acceptance

1. Freeze official sources before writing each reference. Record actual Python, CS50 library, and `check50` versions, commands, case IDs, expected values, and observed values. Run the matching `check50` from the original assignment directory; if environment or authentication limits this, retain the reason and local results for official examples, clearly distinguishing the two evidence types.
2. For each candidate, cite the official requirement subsection, then verify that the reference passes the targeted case and the incorrect behavior produces a different result. Prefer small variants or independently reproducible controls. Check raw output lines to prevent `strip()` hiding newlines or extra characters. Record derivations, inputs, and results for verbal examples too.
3. Review conceptual overlap. Distinguish Cash amount conversion, coin selection, and remainder with separate inputs. Use distinguishable CSVs for DNA consecutive counts, partial matches, and no match. If one error triggers several items, annotate affected behavior and scoring boundaries. Adjust definitions before freezing if evidence is insufficient.
4. Retain case evidence for one correct alternative per assignment: for example, successive change-making instead of `divmod` for Cash, character-range checks instead of a regular expression for Readability, and `csv.reader` instead of `DictReader` for DNA. Two researchers check official requirements, reference behavior, and five flaws per assignment, and sign a versioned list. Including Mario there are 20 items.

## 4. Generation engineering

### Unified entry point

- Reuse `Condition` and the four dimensions in `matrix.py`. Add a shared `build_prompt(condition, generation_input)` and migrate the existing Mario development smoke prompt assembly; the generation entry point accepts matrix conditions and covers any registered assignment. Suggested command: `python -m rubric_benchmark generate --mode dry-run --config config/experiment.toml --output <new-dir>`, optionally with `--assignment` for one assignment. Retain the existing `matrix` CLI.
- Freeze common English task instructions asking each criterion to state observable behavior or evidence, performance affecting points or levels, and concise feedback understandable to students. Require only constraints explicitly stated in the official specification and accept other compliant implementations. The body contains only that assignment's canonical spec, the cell's format block, and an optional example reference block. Assignment-specific information comes from the specification; flaw lists and synthetic cases remain on the evaluation side.
- The `points` candidate asks for maximum points per criterion, distinguishable partial credit, and a total, such as a fixed 100 points. The `levels` candidate asks for Meets / Partially Meets / Does Not Meet behavior descriptions under each criterion. Both formats share coverage scope. The team finalizes the total, level names, and exact wording before formal freeze. Record format adherence separately; annotate useful but format-deviating outputs under predetermined rules.
- Use a new request without history each time. The model slot only selects the configured deployment. Save `condition_id`, template version, spec/reference SHA-256, final prompt hash, and effective request parameters per cell. Save raw response, model and routing metadata, finish reason, usage, UTC time, errors, and attempt number. Implement isolated pilot/formal namespaces and recovery rules according to the [overall plan](IMPLEMENTATION_PLAN.md).

### Execution and failure handling

- `dry-run` first validates selected conditions and all required inputs, then outputs a manifest and per-cell `input.json` by `condition_id`. The manifest includes at least mode, version, condition IDs, and template and data hashes. Missing packages or references and hash mismatches identify the assignment and file and exit before any API call. Formal mode requires the complete matrix.
- Backend adapters handle authentication, parameter mapping, and raw response persistence. Record requested and returned models, provider-unsupported parameters, and effective values that cannot be verified. Separately record normal responses, empty responses, refusals, truncation, timeouts, format deviations, and model mismatches. Frozen rules determine retries. Retries use the original condition ID and a new attempt number.
- Persist raw output, hash, and attempt-completion record before publishing a cell result. On recovery, verify manifest and input hashes and skip accepted cells. Attempts with unknown send status enter a reconciliation state to avoid duplicate calls. Preflight and reports retain complete records for every cell to explain failures and missing data.
- The pilot may initially select two cells per model, one points and one levels, one spec-only and one spec-reference, representing all three assignments. Measure lengths with dry-run, include the longest input scenario, then freeze the six cells and budget. Manually verify correct use of all three assignment contents and effective truncation and format checks.

### Implementation order and gates

| Step | Deliverable | Acceptance |
|---|---|---|
| 1 · Freeze course inputs | Three HTML pages and specifications, provenance records, DNA ZIP archived as needed, and common extraction rule for four assignments | Titles, year, language, and official IDs agree. Source files, canonical text, and usable assets can be rechecked against records. |
| 2 · Validate references and evaluation packages | Three `reference.py` files, 15 flaws, evidence, and review records | Each assignment passes documented examples and targeted cases; five unique IDs each have observable evidence. All 20 items across four assignments pass two-person review. |
| 3 · Connect offline generation | Common prompt builder, dry-run, mock outputs, and actual run records | Twelve cells for each of three assignments, 36 total; 48 with Mario. Identical assignment, context, and format produce identical message bytes across models. Each of 24 context pairs changes only the reference block; each of 24 format pairs changes only the format block. |
| 4 · Verify isolation and persistence | Manifest, hash checks, leakage probes, provider mock, and failure records | Spec-only requests contain no reference. Generation still runs after removing the evaluation directory. A unique string placed in flaw and evidence files is absent from actual mock requests. Changing one input byte triggers hash failure. A full-matrix mock can generate and trace each result. |
| 5 · Pilot and formal freeze | Exact model IDs, run budget, raw drafts, codebook, and protocol sign-off | After team budget approval, run at most six live pilot calls under the overall plan, covering three deployments, both contexts and formats, and the measured longest input. Check returned deployments, truncation, and format, then freeze four assignments, templates, deployments, and codebook. Use a separate pilot directory. |
| 6 · Formal generation and evaluation | 48-cell result manifest, two independent annotations, adjudication, and descriptive results | At most one accepted rubric per cell; failures have separate statuses. Each researcher completes at most 240 flaw ratings and 48 implementation-bias judgments. Save both original judgments before calculating weighted Cohen’s κ, then adjudicate. |

## 5. Assessing rubric usefulness to teachers and students

Score the checks explicitly stated in the rubric. For Cash, a general requirement to “handle input correctly” can score 1; explicitly requiring repeated prompts after negative input until a nonnegative value is obtained can score 2. If no applicable criterion exists, score 0. Readability and DNA use the same standard; evidence may cite one rubric item or a combination of items.

Make one additional implementation-bias judgment per rubric. If it mandates `divmod` for Cash, a particular regular expression for Readability, or `DictReader` for DNA, record the offending criterion, official evidence, and a verifiable correct alternative. Handle explicitly required CS50 input functions according to the specification.

Report each rubric's mean coverage across five flaws (0–2), explicit coverage proportion (proportion scored 2), implementation bias, and results and missing data by experimental condition. Report examples should show teachers which criteria are actionable and which feedback explains the problem to students. A single rubric-text study provides evidence of coverage and scoring consistency. Actual grading accuracy, time savings, and student learning gains require later independent validation.
