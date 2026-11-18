# CS 500 rubric benchmark implementation plan

Audit date: November 18, 2026 (America/Chicago)  
Companion evidence: [Requirements traceability](REQUIREMENTS_TRACEABILITY.md) · [Validation report](VALIDATION_REPORT.md)

## 1. Executive summary

The Check-in #2 design meets the visible structural requirements of CS 500 Format 4. It benchmarks rubric drafting for introductory Python, names three model families, and crosses four factors under a common protocol. It still needs three selected model instances, frozen materials and controls, a formal run, independent coding, and an evidence-based computing-education interpretation. The separate Canvas final-project rubric and deadline remain unverified.

The local scaffold enumerates 48 cells and validates TOML factor lists with Python 3.13. A file-based runner, assignment dataset, annotation workflow, and analysis are specified below for later phases. Each formal cell has one intended rubric, yielding at most 240 flaw judgments per researcher and 480 initial judgments overall when both researchers complete the full grid. Operational retries stay within a cell.

## 2. Research objective

Measure how often rubric drafts give a grader actionable criteria for predefined, specification-grounded programming flaws. Compare the drafts across selected model deployments, tasks, reference context, and requested rubric format. Identify common omissions, vague criteria, and restrictions that would penalize valid alternative implementations.

The educational use case is instructor review of rubric drafts. Strong explicit coverage could identify material worth retaining, while missing, vague, or overly prescriptive criteria point to review and revision needs. This study measures rubric text against selected flaws. Claims about grading accuracy, student-code rankings, time savings, fairness in actual grades, and learning outcomes require separate evidence. Without verified prevalence data, call the items “predefined” or “pedagogically plausible” flaws when reporting findings.

## 3. Source audit

The four PDFs are evidence for this engineering plan. The pasted request defines the scope of this pass. Use the sources in the following order for the decisions they govern.

| ID | Source and extent read | Authority and relevant evidence |
| --- | --- | --- |
| S1 | *Project Information (CS 500 PAG)*, PDF pp. 1–4 | Course authority. General expectations on p. 1 and Format 4 on p. 3. Later rubrics are mentioned on p. 1. Other formats have their own requirements. |
| S2 | *Evaluating the Coverage of AI-Generated Grading Rubrics for Introductory Python Assignments*, PDF pp. 1–4 | Current Check-in #2. RQ and task on pp. 1–2, factors and generation on p. 2, checklist and human coding on pp. 2–3, metrics and progress on p. 3, works cited and an unpopulated budget section on p. 4. |
| S3 | *CS500_Checkin2_Research_Dossier*, PDF pp. 1–18 | Historical audit and methodology options. Course audit pp. 2–4, design and controls pp. 4–7, assignments pp. 7–8, evaluation pp. 8–11, literature pp. 11–13, workload and alternatives pp. 13–15, proposed meeting and readiness checks pp. 15–17, citation marker index pp. 17–18. |
| S4 | *Harvard CS50x 2026 Assignments*, PDF pp. 1–7 | Discovery guide. Week 6 entries on pp. 4–5 and version note on p. 7. Harvard course submission instructions on pp. 6–7 address a separate course. |

### Conflicts and dispositions

| Topic | Resolution |
| --- | --- |
| Four versus five flaws | S3 pp. 13–14 estimates 16 flaws and 192 judgments per researcher. S2 pp. 2–3 specifies five per task, 20 definitions, and 240 judgments per researcher. Use S2. Its p. 3 “20-point flaw checklist” refers to the 20 definitions. Each rubric has five scores on a 0–2 scale. |
| Repetition and assignment choice | S3 pp. 6–8 and 14 proposes alternative tasks and repeat designs. S2 pp. 1–2 selects the four named tasks and one initial rubric per cell. |
| Mutants and grading discrimination | S3 pp. 8–11 proposes controlled mutants and optional rubric application. S2 pp. 1, 3 specifies rubric-text coding and permits an illustrative example or test to validate a flaw. Use targeted behavioral validation for the dataset. Full mutants, grading students' code, and ranking analyses remain outside the core study. |
| Level-based wording | S2 p. 2 names the factor “level-based” but its procedure also describes asking for criteria “related to points.” Freeze an analytic rubric with criterion-specific performance levels as the proposed implementation. The research team must approve the exact descriptors and any scale or point total before formal collection. |
| Bias unit | S2 p. 3 defines a flag per rubric. The pasted request also asks for a flag in the annotation schema. Store one independently assessed rubric-level value per rater, then project it into flat flaw-row exports with equality validation. Count each rubric once. |
| Cash and DNA specifics | S2's flaw categories and S3's examples guide selection. Check each final definition against the official task. Cash requires the minimum coin count rather than a particular greedy or rounding implementation. DNA assumes valid files with two arguments, provides a repeat-count helper, and does not mandate a specific parser. Failure to handle missing files and failure to use the suggested parser lack support as primary flaws. |
| Approval and course documents | The user reports instructor permission for AI in this research and development, resolving S3's historical open question for this pass. The separate CS 500 syllabus, calendar, Check-in #2 Outline, and final-project rubric were unavailable. S3's account of the outline and earlier October 20 date is secondary evidence. |
| Source quality | S3 contains unresolved internal source markers and a reused citation number [19] for distinct papers on p. 17. Treat its literature mapping as a lead. Verify primary publications before citing substantive findings in the course report. |

### Official external sources

Accessed November 18, 2026 (America/Chicago). Playwright HTTP requests observed `302` for each dated URL and `200` for its unversioned target. Each target page title identified CS50x 2026. These URLs can serve a later edition, so retain a snapshot and hash for formal work. The source boundary for prompts is a recorded selection of assignment sections. Phase 2 determines and freezes that selection before piloting.

| Source | Dated URL → observed target | Verified assignment behavior and boundaries |
| --- | --- | --- |
| Problem Set 6 | [2026 index](https://cs50.harvard.edu/x/2026/psets/6/) → [index](https://cs50.harvard.edu/x/psets/6/) | Python set. The index links two Mario variants and the Cash/Credit choice, plus Readability and DNA. This benchmark samples four tasks. |
| Mario — More Comfortable | [2026 task](https://cs50.harvard.edu/x/2026/psets/6/mario/more/) → [Mario specification](https://cs50.harvard.edu/x/psets/6/mario/more/#specification) | `sentimental-mario-more/mario.py`. Use CS50's `get_int`, re-prompt outside 1–8, and print mirrored half-pyramids with at least one loop. Rows grow in width, the left shape is padded to align at the bottom-left, the gap has two spaces, and rows end without trailing spaces. No particular loop type is specified. |
| Cash | [2026 task](https://cs50.harvard.edu/x/2026/psets/6/cash/) → [Cash specification](https://cs50.harvard.edu/x/psets/6/cash/#specification) | `sentimental-cash/cash.py`. Read dollars via `get_float`, re-prompt until nonnegative, and find the minimum number of 25¢, 10¢, 5¢, and 1¢ coins. The last line is the integer count followed by a newline. Validate cent-sensitive behavior with specified inputs. The page gives no mandatory conversion technique or general sub-cent rounding rule. |
| Readability | [2026 task](https://cs50.harvard.edu/x/2026/psets/6/readability/) → [Readability specification](https://cs50.harvard.edu/x/psets/6/readability/#specification) | `sentimental-readability/readability.py`. Use `get_string` and count ASCII letters, space-delimited words, and sentence terminators `.`, `!`, or `?`. Use Coleman–Liau `0.0588 * L - 0.296 * S - 15.8` with letters and sentences per 100 words. Output the nearest grade as `Grade X`, with the prescribed `Grade 16+` and `Before Grade 1` boundary labels. Freeze boundary fixtures consistent with the official examples. Avoid asserting an unsupported tie or empty-text policy. |
| DNA | [2026 task](https://cs50.harvard.edu/x/2026/psets/6/dna/) → [DNA specification](https://cs50.harvard.edu/x/psets/6/dna/#specification) | `dna/dna.py`. Require CSV then sequence-text filename arguments and print an error for an incorrect argument count. Read the CSV and text. Derive STR fields from the header and find the longest consecutive run for each. Print the exact matching profile's name or `No match`. Assume valid files and at most one exact match. CS50 provides the `longest_match` helper and 2026 distribution archive. The task is a text/CSV matching exercise. |

The public university listing confirms Fall 2026 section PAG and Katie Cunningham. Illinois Canvas redirected to institutional sign-in. Final deliverable format, grading rubric, and project deadline could not be checked there. Track them as course verification items while continuing the local work. [Illinois Course Explorer](https://courses.illinois.edu/schedule/2026/fall/CS/500), [Illinois Canvas](https://canvas.illinois.edu/)

## 4. Official requirement alignment

| S1 requirement | Evidence and completion gate |
| --- | --- |
| Identify a programming-education task (p. 3) | S2 pp. 1–2 defines rubric drafting for introductory Python and the actionable-coverage question. |
| Systematically test at least three models (p. 3) | S2 p. 2 identifies three families. Select and record one actual model deployment per family, then account for all 48 cells and verify actual outputs from all three deployments. |
| At least four dimensions under consistent documented conditions, with a rationale (p. 3) | S2 p. 2 identifies all four and why each is included. Publish the frozen condition manifest, documented controls, intended differences, and any provider-specific exceptions. |
| Checkpoint #1 task and success measures considered (p. 3) | S2 documents the task and measures. Evidence of what was delivered at Checkpoint #1 is unavailable. |
| Checkpoint #2 conditions identified, introduction written, rest of report planned (pp. 1, 3) | S2 pp. 1–4 contains the introduction, factor table, and substantive sections. Verify any separate outline, Canvas deliverable details, and filing history against course records if available. |
| Education implications and appropriate team scope (pp. 1, 3) | Have the two researchers interpret observed outcomes for instructor drafting and review. Preserve the five-flaw workload and verify any section-specific scope expectations if the final rubric becomes available. |

S1 gives no Format 4 requirement for think-aloud participants, a Guzdial Chart, preregistration, or Format 1's $1,000 cap. Optional design improvements remain engineering decisions. See the [traceability matrix](REQUIREMENTS_TRACEABILITY.md) for the source, status, and evidence of each requirement.

## 5. Confirmed experimental design

| Dimension | Levels | Research rationale | Conditions per level |
| --- | --- | --- | --- |
| Model | GPT, Claude, Gemini | Compare selected deployments from three families | 16 |
| Assignment | Mario — More Comfortable, Cash, Readability, DNA | Sample distinct introductory Python requirements while holding language and course source constant | 12 |
| Reference context | Specification only, specification plus reference implementation | Explore whether an implementation example improves coverage or induces restrictions | 24 |
| Rubric format | Point-based, level-based | Explore differences in explicitness caused by requesting different scoring structures | 24 |

The Cartesian product is `3 × 4 × 2 × 2 = 48`. Each assignment appears in 12 rubrics and contributes five fixed flaws. The design produces 60 judgments per assignment per researcher with complete data. The 240 flaw scores per researcher are nested within rubrics and repeatedly use the same assignment flaw sets. Neither multiple scores nor two raters provide replicate generations. Describe observed deployments and tasks. Provider, model version, and some model defaults may travel together. Assignment identity bundles several task features. Assess isolated model-family effects, complexity effects, and run-to-run variance only in a different design with suitable evidence.

Use independent 0/1/2 coding with per-flaw justification and an implementation-bias assessment per rubric. Calculate per-rubric mean and explicit rate from five adjudicated flaw scores. Report initial inter-rater agreement before adjudication. Leave the one-generation design in place. A second output per cell would give 96 rubrics and 480 judgments per researcher. Three outputs per cell would give 144 rubrics and 720 judgments per researcher. Those options trade rater time for information about variability and require a separately approved research decision.

## 6. System architecture

Use a Python 3.13 command-line package. TOML defines the experiment, versioned text and JSON capture the dataset and run evidence, and CSV is the interchange format for two human coders. Keep source and run files on local disk for generation. Copy closed, checksummed bundles to team storage for preservation. One operator and bounded worker threads are sufficient. Use `argparse`, `tomllib`, `dataclasses`, `json`, `csv`, `hashlib`, and Pytest. Add one HTTP client with mock transport if needed. Use a single pinned plotting dependency if a figure cannot be produced by the existing stack. A database, dashboard, queue service, and agent framework have no required role.

Generation receives a typed assignment input consisting of the approved specification and optional reference. Evaluation alone reads the flaw manifests and generated rubric text. An offline protocol verifier reads and hashes evaluation materials. The generation runner receives only their frozen digests. Analysis reads locked evaluation exports and the run outcome inventory. Reviewers need readable intermediate artifacts and documented commands.

## 7. Repository file tree

The tree combines the current scaffold and planned additions. Entries marked `[now]` exist. Each dataset entry denotes a repeatable layout for all four assignments.

```text
README.md                                      [now]
.gitignore                                     [now]
.github/workflows/offline.yml                  [now]
pyproject.toml                                 [now]
config/experiment.toml                         [now]
docs/
  IMPLEMENTATION_PLAN.md                       [now]
  REQUIREMENTS_TRACEABILITY.md                 [now]
  VALIDATION_REPORT.md                         [now]
  CODING_GUIDE.md
data/
  assignments/<assignment>/
    provenance.json
    source.html
    specification.md
    reference.py
  evaluation/<assignment>/
    flaws.json
    evidence.json
    fixtures/
prompts/
  system.txt
  task.txt
  format/{points,levels}.txt
rubric_benchmark/
  __init__.py                                  [now]
  __main__.py                                  [now]
  matrix.py                                    [now]
  dataset.py
  prompts.py
  providers.py
  runner.py
  annotations.py
  analysis.py
tests/
  test_matrix.py                               [now]
  test_dataset.py
  test_prompts.py
  test_runner.py
  test_annotations.py
  test_analysis.py
runs/<pilot-or-formal>/<run_id>/                local, archived after close
  manifest.json
  cells/<condition_id>/
    input.json
    attempts/<attempt_id>/
    outcome.json
  annotation/
  analysis/
  checksums.sha256
```

If a source snapshot includes materials with different provenance or redistribution terms, preserve it in the private study bundle and keep its source/hash record. Preserve Harvard attribution and license notices for snapshots and adapted text. Record reference authorship and applicable starter-code terms. Keep student submissions out of the formal dataset. [CS50x license](https://cs50.harvard.edu/x/license/)

## 8. Module responsibilities

| Module | Responsibility |
| --- | --- |
| `matrix.py` and `__main__.py` | Typed condition records, TOML validation, deterministic enumeration, and CLI dispatch. In formal preflight validate exact declared levels and the full 48-cell contract as well as model bindings. |
| `dataset.py` | Verify provenance and source files by hash. Expose an allowlisted generation reader and a separate evaluation reader. The generation interface accepts no flaw data, file tree bundles, check logs, or codebook. |
| `prompts.py` | Assemble common text from frozen files. Emit canonical system and user text and their hash. Present a reference as an example and protect valid alternatives consistently across contexts. |
| `providers.py` | Translate this small shared contract into chosen endpoint calls. Record endpoint-specific parameters, versions and raw response bytes. Return a normalized completion or reason code. |
| `runner.py` | Preflight, mode/manifest handling, deterministic scheduling, retry policy, attempts, final outcomes, resumption, and provenance. |
| `annotations.py` | Prepare blinded rating packages, validate and lock independent submissions, produce disagreement views and accept hashed consensus records. |
| `analysis.py` | Join run and rating artifacts by stable keys, summarize outcomes, calculate agreement, and emit deterministic tables and figures. |

## 9. Data schemas and interfaces

| Record and grain | Required content and constraints |
| --- | --- |
| Experiment TOML | Current `[dimensions]` lists. Add schema version; per-family exact model ID, vendor/endpoint, API protocol/version, supported/requested parameters and known defaults, allowed served model/route identifiers, and credential variable name. Add dataset and prompt versions, seeded execution order and limits, failure policy version, and an annotation/analysis protocol version. No secret values. |
| Condition | `model`, `assignment`, `reference_context`, `rubric_format`, and dotted `condition_id`, e.g. `gpt.mario-more.spec-only.points`. The factor slugs exclude periods. A condition ID identifies a design cell across runs. Use `experiment_id = run_id + "/" + condition_id` to identify one cell in one run. |
| Assignment provenance | `assignment_id`, publisher, accessed UTC timestamp with audit date, requested and resolved URLs, redirect status, page label and official check ID, selected headings, extraction rules, source SHA-256 and rendered-spec SHA-256, reference author/origin/license/hash, runtime and fixture/test provenance. Include assignment-scoped stable requirement IDs and source anchors. |
| Flaw and evidence | Stable `flaw_id` such as `mario-more.gap`, linked `requirement_id`, novice mistake, expected behavior, distinguishing input or case ID, observed failure or independently worked example, rationale, verification method, status (`proposed` or `verified`), first and second reviewer IDs, dates and evidence references. Evidence describes the exact requirement boundary and checks for overlap. Reserve IDs for their original definitions. |
| Run manifest | Unique UTC-date-plus-random-suffix `run_id`, mode, created time, frozen source commit and clean-tree preflight result, Python/OS/locked dependencies, dataset and evaluation hashes, canonical config and prompt bundle SHA-256, all 48 expected IDs and planned execution order for formal mode. Leave the run manifest frozen and attach later manifests, including the locked annotation key-map hash, to its hash. |
| Attempt | `experiment_id`, monotonic attempt ID, start/end UTC, request and prompt hash, effective request body without auth, endpoint, requested and returned model, served route or explicit unknown, vendor request/response IDs, transport/HTTP state, finish reason, usage, raw body path, byte hash, retry reason and next action. Distinguish provider-reported parameters, explicit requests, defaults, unsupported settings, and unknown effective values. |
| Cell outcome | One terminal outcome per closed cell. Record `accepted`, `failed`, or `excluded`, reason code, attempt link if applicable, decision timestamp and actor for manual resolutions, text extraction version and hash, and format-conformance flag when text exists. Rebuild the run inventory from outcomes. `pending` and `ambiguous` are work states requiring resolution before closure. |
| Initial flaw rating | Locked import stores `experiment_id`, `flaw_id`, pseudonymous `rater_id`, integer `coverage_score` in 0–2, `evidence` (criterion locator or reason for absence), and `annotation_timestamp` in UTC as ISO 8601. The primary key is the first three fields. A rater-facing CSV uses a blind rubric ID that maps to `experiment_id` at import. |
| Initial implementation bias | One record per `(experiment_id, rater_id)` with `implementation_bias_flag` (true/false), evidence and timestamp. True requires a criterion, a spec comparison, and an explanation of a valid alternative the rule would penalize. Repeat the flag in a flat flaw-row export only if every joined row agrees. |
| Adjudication | Final flaw values keyed by `(experiment_id, flaw_id)` and final bias values keyed by `experiment_id`, with links to both locked inputs, consensus justification for changes/disagreements, codebook version, closure timestamp, and explicit unresolved state when needed. Equal initial judgments may carry forward deterministically. Never replace an initial submission with consensus. |

Planned interfaces: `build_prompt(condition, generation_input) -> Prompt`, `generate(prompt, model_settings) -> Completion`, and `analyze(inventory, locked_ratings, consensus) -> outputs`. Type the shared fields and validate each file or endpoint boundary. Keep vendor payloads in the provider module. Read TOML and build the complete matrix before any call so invalid selections fail early.

### Prompt construction and provider choice

Use fresh, stateless text requests with no conversations, tools, search, or other model outputs. Assign a common instructor-facing role, a fixed specification block, a format instruction and, for the reference condition only, a delimited reference block. State in the common instruction that criteria should allow alternative approaches that meet the specification. The reference block presents one example. Both formats ask for actionable assignment-grounded criteria at the same scope. The point version requests point allocations per criterion. The level version requests anchored performance levels per criterion. Establish both definitions and avoid carrying point language into the level condition unless the team explicitly adopts it.

Use the official material according to a single extraction policy across tasks. Proposed default: include Problem to Solve, Specification, and task-specific input assumptions or permitted starter material required to understand the spec. Archive the complete official page and its examples. If retaining examples or hints in the prompt, select by a general rule independent of flaw IDs and retain the identical selection in both contexts. Avoid extra invitations aimed at specific checklist items, researcher comments, mutation evidence, and copy-paste from the dossier. Natural overlap between genuine spec language and flaw categories is expected. Test isolation through source allowlisting, canary data, and paired prompt diffs.

Direct vendor APIs are the default recommendation for provenance, subject to credential access and model availability. Before provider selection, verify the exact snapshot ID, structured capabilities, request controls, effective defaults, finish statuses, response metadata and cost for each endpoint. OpenAI Responses, Claude Messages and Gemini generateContent have different request envelopes and output-limit/finish semantics. Use a generous pilot-tested output budget per deployment and record what it counts. Leave unsupported sampling parameters unset and declare differences. Matching temperature numbers alone cannot establish comparable sampling. [OpenAI Responses](https://developers.openai.com/api/reference/resources/responses/methods/create), [Claude Messages](https://platform.claude.com/docs/en/api/messages), [Gemini generateContent](https://aistudio.google.com/api-reference/generate-content)

OpenRouter can reduce adapter work when a fixed endpoint exists. Pin one provider endpoint per selected model, disable fallbacks, require parameter support, and verify returned route/model metadata. A fixed route can still expose a mutable model alias. Kie.ai documents vendor-specific protocols and live model lists, including a separate OpenAI-compatible Gemini chat endpoint. Compatibility covers request shape. Snapshot identity, transformation and route guarantees need independent confirmation. Choose a different documented endpoint before freeze if essential metadata is insufficient. If only a mutable alias is feasible, record the known limits, constrain timing, and characterize results as observed deployments with alias uncertainty, subject to researcher agreement. [OpenRouter routing](https://openrouter.ai/docs/guides/routing/provider-selection), [Kie.ai protocol overview](https://docs.kie.ai/ai-agent/overview), [Kie.ai Gemini endpoint example](https://docs.kie.ai/market/gemini/gemini-3-pro)

## 10. Benchmark execution workflow

1. **Enumerate and dry-run.** Run `python -m rubric_benchmark matrix --config config/experiment.toml` today. Implement an offline `dry-run` command that resolves all 48 formal inputs, shows intended routes and settings, compares prompt pairs, and writes or displays a manifest preview without creating accepted outcomes.
2. **Mock and pilot.** Simulate each adapter with saved fixtures. Proposed live pilot is at most six requests across three model slots and both levels of each text factor, plus practice rubrics for calibration. Select cells in advance and include the longest input. Freeze a cost cap with the two researchers before any live request. Use distinct mode directories, run IDs, and deduplication keys. Pilot rubrics can calibrate the codebook only. Their ratings and outputs stay outside formal results.
3. **Freeze and schedule.** Approve the dataset, checklist, codebook, prompts, model bindings, parameter exceptions, execution order, cost and failure policy in a hashed protocol. Require a clean checkout at the frozen code commit, ignoring generated run and cache files. The offline preflight verifies both the generation input bundle and the evaluation/codebook bundle. Pass the latter to the generation runner only as hash identifiers. Construct the formal directory from this snapshot. Keep a seeded interleaved order across models and conditions over a short collection window. Record actual order and timestamp for each attempt.
4. **Dispatch and persist.** Use one coordinator with a process-level exclusive lock per run on a local filesystem and a bounded pool. Recommended starting limit is two in flight total and one per provider. Use one worker per cell and persist the started attempt and sanitized request before dispatch. Save raw response bytes, including malformed success bodies and error bodies where returned, before parsing. Use same-directory temporary staging, flush/fsync, and atomic no-clobber publication for immutable files. After raw bytes are durable, publish an attempt completion record containing the raw hash, sanitized metadata and normalized finish or error reason. Include HTTP status where available, timestamps, response IDs and model/route evidence. Publish a terminal outcome only after the verified attempt record is durable. Preserve headers on an allowlist. Record transport errors even when no response body exists.
5. **Retry conservatively.** Pilot-tune explicit connect and read timeouts, a total request budget, and a small retry cap (proposed up to three attempts total). Disable hidden SDK retries. Auto-retry only a documented pre-generation rejection such as a retryable 429, or a confirmed pre-send failure. Honor `Retry-After` up to a frozen wait budget and use bounded backoff with jitter. Treat ambiguous read timeouts, lost responses, and potentially accepted 5xx as indeterminate. Reconcile using a request ID or documented endpoint idempotency where available. Persist and adjudicate ambiguity before sending again. Exclude responses for unapproved routes or model versions and hold subsequent calls pending review. Record credential, invalid-request, and parameter failures explicitly.
6. **Accept a single rubric.** Accept the first complete usable response from the declared deployment and apply the frozen text-extraction rule. Keep substantive rubrics with a wrong requested format as observed outputs and flag the deviation. Freeze examples distinguishing a rateable rubric from refusal, empty content or truncation. Archive every attempt. Exclude ineligible content with a reason and no automatic quality reroll. Do not repair a rubric with another model or replace text based on coverage. Report adherence separately and, if predeclared, show complete-case sensitivity for format-adherent outputs.
7. **Resume and close.** Before resume, use the offline verifier to check the clean frozen code checkout, immutable manifest, inputs and evaluation hashes. The generation runner verifies its own allowlisted input hashes. Reuse an on-disk response only when its published attempt completion record and referenced bytes verify and its recorded metadata support the outcome. Raw bytes without that record are insufficient. Treat unfinished attempts as ambiguous and preserve them without automatic re-dispatch. Accepted cells are skipped and mismatched bytes or duplicate terminal records stop the run for investigation. Append retries under new attempt IDs. Require a disposition for all 48 cells, report each missing/excluded reason, and hash the closed inventory. An accounted-for failure is still missing data.
8. **Evaluate and analyze.** Export locked rubric text via stable blind IDs. Automated packet preparation keeps model, context and transport metadata out of the packets and avoids printing the key map. Raters receive the assignment, specification and frozen flaws. Seal the map until both initial submissions lock. Record any earlier exposure from running the study and any condition clues in the rubric body. Then compute agreement, adjudicate, run analysis and archive artifacts.

## 11. Sub-agent delegation strategy

The lead engineer owns source precedence, schemas, integration and acceptance. Delegate read-only source or architecture review when the cross-check can improve a gate. Keep each implementation phase with one owner for shared paths. The second researcher independently validates Phase 2 evidence and performs their own Phase 5 ratings. A sub-agent cannot substitute for a human rater.

The agent environment did not expose a selectable Luna model. A separate read-only reviewer checked the actual draft and scaffold for Format 4, matrix arithmetic, Check-in #2 fidelity, generation/evaluation isolation, reproducibility and resume behavior, scope, and test acceptance. Findings and corrections are recorded in the [validation report](VALIDATION_REPORT.md).

## 12. Implementation phases

Apply the requested loop at every gate: **Plan → Implement → Test → Inspect Evidence → Review → Fix → Regression Test → Accept**. Before starting a phase identify an owner and verifier from the two researchers. At the gate, inspect the artifacts and underlying test output, document corrections in the validation ledger, and rerun the targeted checks and the offline suite. Record acceptance or a specific blocker and keep evidence from failures as well as successes.

| Phase and scope | Inputs and dependencies | Tasks and outputs | Tests and acceptance | Failure and recovery | Evidence to preserve |
| --- | --- | --- | --- | --- | --- |
| **0. Source audit and research protocol** | Four PDFs, local and GitHub repository, official public specs | Audit source authority, record conflicts and open items, define protocol and freeze checklist | All hard requirements and current decisions mapped, sources page-checked, unverified course items explicitly marked | If sources conflict, prefer S1 then S2. Retrieve additional course evidence through authorized access if available and record any impact before affected work | PDF page ranges/hashes, source access/redirect log, matrix, review and decisions |
| **1. Repository foundation** | Accepted source design and baseline Git tree | Set up Python, TOML, CLI, immutable condition record, Pytest and basic CI. Current scaffold is local | Exact Cartesian product and expected marginal counts, same CLI JSON with an empty environment, invalid config exits nonzero. Verify hosted CI when available | Fix config/validation or environment, rerun CLI and full offline tests on unchanged protocol | Code diff, Python/Pytest versions, CLI hash, distribution counts, local and hosted results when available |
| **2. Assignment dataset** | Phase 0 source decisions, stable IDs from Phase 1 | Snapshot and hash four specs, establish extraction rules, author and vet one reference per task, build five requirement-linked flaw definitions each with evidence. Review correct-alternative reasoning | Four recorded 2026 sources, references pass documented official cases and targeted checks, 20 unique flaws with five per task, dual review of every definition | Quarantine mismatched snapshots or questionable evidence. Replace an overlapping or out-of-spec candidate before freeze, retest the reference and rerun the manifest gate | Original snapshots, attribution, hashes, test inputs and outputs, versions, reviewer sign-offs and rejected candidates |
| **3. Prompt and model pipeline** | Accepted dataset, candidate deployments, credentials only for authorized pilot | Freeze template candidates, implement adapters, isolated dry-run, attempt storage and resume. Develop codebook with practice rubrics. Run mocked scenarios and an approved budgeted pilot | Full offline mock run completes, crashes resume with no duplicate acceptance, provider mismatch quarantines, prompts pass paired diffs and leakage tests, pilot proves the selected request and metadata contract. Confirm exact final settings and codebook after pilot | Resolve mismatches offline, revise pilot versions with rationale, repeat affected pilot cases only within authorization. A provider that cannot meet frozen constraints stays out of formal runs | Prompt and request hashes, mock logs, pilot-only raw data and cost, provider capability matrix, practice calibration and approved freeze |
| **4. Formal benchmark execution** | Accepted Phase 3 and signed protocol freeze, authorized formal run | Create fresh formal namespace and issue one intended generation per cell. Reconcile failures and preserve every attempt and outcome | 48 unique terminal dispositions and at most one accepted rubric each, each accepted response verified by hash and deployment. Verify coverage of three models for course execution and quantify failures | Resume only on identical manifest. For uncertain attempts reconcile or close as missing. If a frozen condition changes, halt and document a new protocol or incomplete original run | Frozen configs, execution order, raw bodies, recovery and failure ledger, closed inventory and checksums |
| **5. Human evaluation** | Closed formal inventory, verified evaluation dataset, frozen codebook | Export two separate packets, validate independently locked imports, calculate pre-adjudication agreement, adjudicate with provenance | Target 240 initial flaw ratings per rater, 480 total, plus 48 bias decisions per rater. If some rubrics are unavailable, reconcile eligible, received, paired and missing counts and keep the shortfall visible. Adjudication keeps initial hashes unchanged | Return invalid or missing records to the originating rater before unblinding. Preserve revisions and actual missing reasons. Record unresolved disagreements rather than averaging them away | Blind key map sealed until both submissions lock, both locked inputs, timestamps, agreement and disagreement outputs, consensus log |
| **6. Analysis and research outputs** | Phase 5 accepted or documented incompleteness, closed inventory and formal data only | Implement deterministic summaries, tables, figures and reproducibility instructions. Researchers connect measured gaps and bias to instructional use | Hand fixtures pass. A clean offline rerun from the archived data reproduces every final number, including missingness counts and denominators. Verify student-authored interpretation against the data | Isolate mismatched joins, denominators, contamination or drift. Correct code under version control and regenerate all dependent figures/tables with the same preserved inputs | Analysis commands, dependency snapshot, hashes, tables, figures and claim-to-evidence mapping |

### Phase 2 validation starting points

These are requirement groups and fixture ideas, pending independent verification and exact flaw definitions. Create no formal rubric before the checklist freezes. Prefer one independently distinguishing observable behavior per flaw. A validated reference plus a discriminating test or independently checked input/output example supplies evidence for the checklist. Runtime mutants are optional validation aids.

| Task | Requirement anchors and suggested distinguishing examples |
| --- | --- |
| Mario | Validate range and re-prompting with 0 then 1 and 9 then 8. Verify row count and growth at 1, 2, and 8. Compare leading alignment, the gap, and trailing whitespace with exact strings. Treat separate whitespace flaws as distinct only if each can fail independently. |
| Cash | Exercise a negative input followed by a valid amount and test zero. Official decimal and integer cases such as `0.41 → 4` and `23 → 92` distinguish unit/count errors. Use cases with remainders and multiple denominations to distinguish candidate logic flaws. Check the exact last-line format separately from its numeric value. |
| Readability | Derive cases for letters, words and ending punctuation, scaled Coleman–Liau calculation plus grade rounding, and boundary rendering. Use the official examples for both boundary outputs and at least one intermediate grade. Verify raw and rounded boundary behavior before fixing fixtures near cutoffs. |
| DNA | Exercise wrong argument count, datasets with varying valid headers, a case where separated repeat occurrences differ from the longest consecutive run, exact matching against a partial-match distractor, and an official no-match case. Preserve the provided helper's provenance. |

Use the official local examples and available correctness tests on team-authored references, recording the 2026 test identifier, test/tool version, command and result. If `check50` cannot be used, record the constraint and run the documented official cases locally. Passing those cases supports validation within the tested domain. The rubric audit checks requirement legitimacy, so any correct alternative used to justify a bias flag must respect explicit constraints such as Mario's use of a loop.

## 13. Testing and validation strategy

| Check | Procedure and expected result |
| --- | --- |
| Matrix cardinality and margins | Compare all IDs to an independently specified product. Require 48 unique IDs, 16 per model, 12 per assignment, 24 per context and 24 per format. Repeat the real CLI with an empty environment and compare bytes. Reject duplicate, empty, missing, extra, invalid and malformed factors. |
| Flaw manifest and behavioral validation | Load four manifests and reject unknown requirement anchors, duplicates, wrong assignment links, unverified entries, and missing evidence. Require five verified definitions per assignment, 20 total. Exercise reference and distinguishing fixture expectations with the same frozen spec. |
| Prompt isolation | Plant unique literals in flaws, codebook and validation evidence and prove they never reach provider payloads. Run with the evaluation directory absent. Require equal canonical messages for the same non-model conditions across model slots. Compare all 24 matched pairs for each text factor: contexts differ only by the approved reference block and formats only by the format block. |
| Provider compatibility | Inject mocked normal, refusal, truncated, empty, malformed, wrong-model, missing-route, 429, invalid-auth and timeout responses. Check effective payload, retry boundaries, persisted raw bytes and metadata, and exact state transitions. A full mocked run with valid outputs yields 48 accepted cells. |
| Reconstructability and corruption | Rebuild the matrix and prompts from the frozen spec/reference, config, template bytes and render version. Verify identical per-cell hashes. Change a single input byte or raw response, then verify preflight/resume or analysis rejects it. Change the flaw manifest and verify offline preflight blocks resume. Exercise the generation worker with only the approved digest and the evaluation directory absent. Reject an altered executable working tree or different commit. |
| Resume and durability | Kill a mock runner after the start marker, after raw publication but before attempt completion, after attempt completion but before cell outcome, and after terminal publication. Resume with the same manifest. Verify the first two incomplete states are ambiguous without re-dispatch. Recover a completed attempt without another provider call and skip accepted cells. Prove old files are byte-identical. A concurrent coordinator must fail before dispatch. |
| Failure accounting | Force a never-generated, failed, refused, truncated and format-deviating example in independent fixtures. Ensure the first four carry explicit missing reasons and the last remains rateable if the text meets the frozen usability rule. A retry uses the same experiment ID. No result or score is fabricated. |
| Secret isolation | Run offline with no credentials. Inject fake keys into the adapter environment and mocked errors, including an echoed key in a raw response. Assert the marker is confined to the outgoing auth header and the quarantined original if echoed. Scan normal logs, artifacts, exports and tracked files for absence. Test environment-name validation and missing-key preflight. |
| Ratings and independence | For 48 accepted fixtures require 240 rows per rater and 480 dual-rater initial rows. Require 48 separate bias decisions per rater. Reject duplicate, cross-assignment, invalid-score or unlabeled blank rows. Remove one rubric and verify the inventory shows five unavailable ratings per rater and one unavailable bias decision. Keep initial file hashes unchanged during adjudication. |
| Statistics | For coverage `[0, 1, 2, 2, 0]`, expect mean `1.0` and explicit rate `0.4`. With 1 true bias flag among 2 assessed rubrics expect `0.5` even if joined into ten flaw rows. For paired coverage `[0,1,2,2]` versus `[0,2,1,2]`, expect two exact agreements of four and linear weighted kappa `3/7`. For identical constant ratings report kappa as undefined when expected disagreement is zero. |
| Scope and release | Ensure pilot IDs cannot join formal exports or analysis. Regenerate deterministic tables and figures twice from the archived formal bundle. Verify all expected cells, usable rubrics, received/paired ratings, and scored denominators can be traced to individual records. Hosted CI uses only the offline suite. |

### Analysis and coding decisions to freeze

- **Coverage.** Score 0 for no applicable criterion, 1 for broad or indirect coverage, and 2 for an explicit actionable check. As in S2 p. 3, general correctness can score 1 for a behavior-changing flaw. A vague criterion unrelated to the flaw scores 0. Use coding-guide examples for borderline cases and multiple clauses that jointly address a flaw. Require raters to read the same frozen rubric text without further model assistance.
- **Agreement.** Recommend linear-weighted Cohen's kappa across paired initial flaw judgments, with disagreement weight `abs(i-j)/2`. Compute observed weighted disagreement from the joint 3×3 counts and expected disagreement from independent empirical marginals. Report `1 - D_observed / D_expected`, exact agreement, paired count, marginals and disagreement table before adjudication. Mark undefined cases explicitly. For the stated fixture `D_observed=0.25` and `D_expected=0.4375`. For the binary bias flag report independent agreement counts and any separately predeclared coefficient. Agreement is descriptive for this grouped sample.
- **Primary summaries.** For each rubric with five final scores, report `sum(scores)/5` and `count(score == 2)/5`. Compute unweighted means of those rubric-level values by level of each of the four dimensions. Report bias as flagged divided by assessed rubrics. Include expected cells, eligible outputs and denominator for each metric. Use complete rubrics for primary coverage summaries and report missing/invalid ratings and unresolved consensus separately. Do not encode missing as 0. A zero eligible denominator yields an unavailable result. A complete negative outcome is valid data.
- **Interpretation.** Present coverage, format adherence, and bias with representative evidence and denominator counts. Show composition if missing cells unbalance the grid. The data support comparisons among these drafts and a discussion of what instructors might check. Avoid p-values, claims of reliable model rankings, causal complexity labels, and actual grader- or student-outcome claims under this design.

## 14. Reproducibility and data integrity

Record source URLs, edition labels and hashes on acquisition. Freeze data, prompts, run plan, settings, codebook, analysis rules, and code commit with an SHA-256 inventory of exact UTF-8/byte artifacts and stable canonical JSON for derived IDs/hashes. Archive snapshots, reference evidence, generated inputs, attempts, accepted text and exclusion logs, locked rater files, consensus and analysis commands. Preserve dependency versions, Python/OS, and execution order. Protect blind mappings and individual rater workspaces during collection. Keep credentials in runtime environment variables and out of requests saved to disk, URL query strings, logs, exports and Git. If a raw provider response echoes a credential or contains other sensitive material, quarantine the original in restricted storage, preserve its hash and record the disposition without printing the secret. An operational or shareable derivative uses a clearly marked scrubbed copy. Exclude quarantined originals from normal logs and exports.

A reproduction starts from a named code commit, the same dependency and input bundle, and a verified hash inventory. Rebuild prompts offline for manifest verification, replay extraction from preserved responses, reimport locked ratings, and regenerate tables and figures. Reissuing the calls is a new run. Model sampling and serving-version changes mean identical historical API output cannot be guaranteed. Store a verified second copy of the closed evidence bundle and test restoration before final submission.

## 15. Risks and mitigations

| Risk | Control and residual limitation |
| --- | --- |
| Checklist or reference leakage | Allowlisted input, no shared prompt-workspace reads, canary tests and full paired diffs. Natural spec/checklist overlap is expected. Inspect comments in reference code for evaluation-only hints. |
| Overfitting to implementation | Keep the example warning common across conditions, record permissible alternatives, and assess bias at rubric level. Explicit spec constraints remain valid. |
| Validity of five preselected flaws | Require precise anchors, observed or independently derived failing behavior, dual review and pre-freeze approval. Record emergent flaws separately for possible future research. |
| Model routing and time drift | Fixed requested IDs/endpoints and reported served metadata, seed and timestamps, interleaved order, documented alias/default gaps. Stop on unapproved changes. |
| Noncompliant or missing outputs | Preserve raw responses, record eligibility by rule, count missingness by condition and level, and stop any attempt to fill failed cells with undeclared substitutes. |
| Rater workload and agreement | Two people each assess up to 240 flaw judgments and 48 bias flags. Use pilot timing to schedule independent batches and reserve adjudication time. Lock originals and expose agreement uncertainty. |
| Overinterpretation | Purposeful assignment sample and one generation per cell. Report observed rubric properties and limitations. |
| Course details and schedule | Public Format 4 baseline is verified. Record official rubric, deadline and deliverable expectations when accessible and log any material change. |
| Citation and redistribution | Preserve source attribution and licenses, distinguish copied from adapted material, and retain only approved materials in any shared release. |

## 16. Open decisions

| Decision | Proposed default and owner | Resolve by |
| --- | --- | --- |
| Exact model snapshots, provider routes, versions, controls, cost and budget | Both researchers choose after a documented capability check and set pilot/formal cost caps. Prefer independently identifiable snapshots and direct APIs if practical. | Before live pilot for pilot settings and before freeze for formal settings |
| Level anchors, common rubric scope and point totals | Both researchers approve analytic levels, point allocations and comparable criterion scope given the Check-in wording ambiguity. | Phase 3 |
| Source extraction, distribution context, reference authors and exact flaw list | Dataset owner drafts and second researcher validates. Decide which official examples are in the prompt and preserve single canonical copies. | Phase 2 before Phase 3 pilot |
| Blinding/order, weighting and missing-data rules | Both researchers sign the coding and analysis protocol. Default to blind IDs, independently shuffled packets, linear weighted kappa, complete rubric denominators and explicit missingness. | Phase 3 calibration before formal collection |
| Failure/metadata policy | Both researchers approve eligibility examples, timeout/retry limits, unknown-alias handling and restart conditions. Record whether any discovered noncompliance is a planned sensitivity view. | Before Phase 4 |
| Canvas rubric and deliverable deadline | Obtain from course materials through the team when accessible. Requirements inferred from public listings are insufficient for final submission verification. | Before final deliverable planning is closed |

## 17. Acceptance criteria

- **This pass.** Four supplied sources reviewed with page citations and conflicts, four official assignment specifications verified with dates and redirects, repository audited, three requested plan files present, critical review recorded, and the offline scaffold verified against the 48-cell grid.
- **Formal-start gate.** Both researchers sign the hash-identified protocol. Four vetted assignment packages, three resolved deployments, 20 independently verified flaws, versioned prompts and codebook, approved operational and analysis rules, and an isolated pilot with acceptable evidence are ready. The complete mock path passes with no live credential needed in CI.
- **Research completion gate.** Every formal cell is accounted for. Each accepted record retains original bytes, metadata and lineage. Both rating sets are independently locked and complete for available rubrics or documented as incomplete. Agreement uses paired initial ratings. Consensus and all reported results reproduce from the preserved bundle. Computing-education discussion is tied to measured coverage and restrictions.

## 18. Recommended implementation order

Phase 0 and the offline subset of Phase 1 are complete locally. Continue with Phase 2. Freeze one end-to-end assignment package first, starting with Mario — More Comfortable. Have the second researcher verify the exact spec extraction, reference behavior and five candidate flaw definitions. Apply the validated layout to Cash, Readability and DNA. Build Phase 3 against those inputs, secure a bounded pilot, and freeze the full protocol. Then proceed in order through formal generation, independent evaluation and descriptive analysis. Course rubric verification can proceed as access becomes available.

## Phase 2 update — Mario development package

The Mario source snapshot, selected assignment text, provenance hashes, example reference, five requirement-linked flaw records, and generation-only dataset loader are implemented. The loader verifies the selected specification and reference hashes, accepts validated assignment IDs, and reads no evaluation files. The two-condition development smoke helper accepts an injected model callable and stores prompt, raw text and status separately. Its mock checks cover reference inclusion and both requested formats. This helper is diagnostic and does not implement the formal runner, provider metadata contract, or automatic rubric quality evaluation.

The five Mario flaws have technical example evidence and await independent human review before the formal protocol freezes. Cash, Readability and DNA packages remain outstanding. A direct sub-agent request specifying Luna and medium effort completed independent QA. The resolved runtime model and effort were not exposed, so its exact configuration remains unverified. See the validation report for findings. The source snapshot retains Harvard's attribution and CC BY-NC-SA license reference. The official `check50` suite and CS50 library integration remain to be exercised in an environment that has them.

The research team's staged development roadmap is Luna independent sub-agent QA, selective Terra/Sol compatibility testing, Terra cross-platform research, an AI preliminary report grounded in recorded evidence, and final human review. These steps remain diagnostic or proposed until executed. The GPT/Claude/Gemini formal conditions and independent human coding remain the research protocol.
