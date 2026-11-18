# CS 500 benchmark validation report

Audit date: November 18, 2026 (America/Chicago)  
Scope: source audit, implementation plan, traceability and offline matrix scaffold

**PASS** means verified for the listed scope. **FAIL** means an attempted check failed. **BLOCKED** means required access or capability was unavailable. **NOT RUN** means execution belongs to a later phase or was outside this pass.

## Source and repository verification

| Status | Verification item | Actual evidence |
| --- | --- | --- |
| PASS | Read all four PDFs | Extracted and read all 33 PDF pages with page numbers. Rendered all pages to check for content missed by extraction. The [plan's source audit](IMPLEMENTATION_PLAN.md#3-source-audit) records source roles, precedence, and conflicts. |
| PASS | Git baseline and live GitHub tree | Local `HEAD` and the local `origin/main` ref pointed to `40c729b2f1424a6f63c4ba35b5767e3e3f70bd24`. The checkout was clean before edits and `git ls-files` listed only `README.md`. An initial `gh api` connection attempt failed. A read-only GitHub connector request for `contents?ref=main` succeeded and showed only `README.md`, with blob `38aca5d8ff988e0966c908f666a8b5e96590e97b`, matching the local baseline. [GitHub repository](https://github.com/IanJ332/AI-Rubric-Gen/tree/main) |
| PASS | CS50x 2026 PSet 6 and four tasks | Direct HTTP requests on November 18 showed a `302` from each dated URL to the matching versionless path and a `200` with the 2026 title. Read each official requirement section and available examples. [Problem Set 6](https://cs50.harvard.edu/x/psets/6/) |
| PASS | Illinois course listing | The Fall 2026 Course Explorer page lists section PAG, Program Edu in Age of GenAI, with Katie Cunningham. [Illinois Course Explorer](https://courses.illinois.edu/schedule/2026/fall/CS/500) |
| BLOCKED | Final-project rubric, official deadline and private Canvas materials | Illinois Canvas redirected to institutional sign-in. The four local PDFs omit the separate rubric, calendar, syllabus and Check-in #2 Outline. S1 is the verified source for Format 4. [Illinois Canvas](https://canvas.illinois.edu/) |
| PASS | Model provider documentation comparison | Primary docs show different native envelopes and routing limitations. OpenRouter documents provider restrictions, fallback and parameter behavior. Kie.ai documents protocol and endpoint differences. This verifies the design constraints from documentation. [OpenAI](https://developers.openai.com/api/reference/resources/responses/methods/create), [Claude](https://platform.claude.com/docs/en/api/messages), [Gemini](https://aistudio.google.com/api-reference/generate-content), [OpenRouter](https://openrouter.ai/docs/guides/routing/provider-selection), [Kie.ai](https://docs.kie.ai/ai-agent/overview) |

### Source fingerprints

These are hashes of local PDFs, for disambiguation. Publication dates and filenames alone do not lock an experiment input.

| Source | Pages | SHA-256 |
| --- | ---: | --- |
| S1 · Project Information | 4 | `0a1bc66508e5af4252bbe7b94b1a6d811134f3c57cfca375d656c6cd0c6abf08` |
| S2 · Current Check-in #2 | 4 | `7f2f6a4bae0bd7c0ae559dcb20c8e3fa8217aea327b225cb09dfbe941b326eb9` |
| S3 · Research Dossier | 18 | `bc9e2f6a263a7e5bdc750f7dcb10070557aa0943f93f571b88c4b9e99ec9531a` |
| S4 · CS50x 2026 Assignment Guide | 7 | `4a93577b9222bfa197bb7264c9c90f45bd837c13401eb39acb029f8159de6949` |

The task pages list the following official correctness test IDs. Their presence was **PASS**. Running those tests is **NOT RUN**, pending references.

| Assignment | Verified check50 identifier |
| --- | --- |
| [Mario More](https://cs50.harvard.edu/x/psets/6/mario/more/#correctness) | `cs50/problems/2026/x/sentimental/mario/more` |
| [Cash](https://cs50.harvard.edu/x/psets/6/cash/#correctness) | `cs50/problems/2026/x/sentimental/cash` |
| [Readability](https://cs50.harvard.edu/x/psets/6/readability/#correctness) | `cs50/problems/2026/x/sentimental/readability` |
| [DNA](https://cs50.harvard.edu/x/psets/6/dna/#correctness) | `cs50/problems/2026/x/dna` |

## Architecture and methodology review

| Status | Item | Finding and disposition |
| --- | --- | --- |
| PASS | Visible Format 4 requirements mapped | The task, three family slots, four factors and their rationales agree with S1 p. 3 and S2 pp. 1–2. Testing three deployed models, documenting executed controls and drawing educational implications await the benchmark. |
| PASS | Check-in design has precedence | Corrected the historical 16-flaw/192-judgment proposal to 20 flaws/240 judgments per researcher. The four selected assignments, one intended rubric per cell, no formal prior-submission use, independent ordinal coding and weighted agreement follow S2. |
| PASS | Bias grain and format ambiguity surfaced | The plan applies one bias flag per rubric per assessor and carries that value into any flat flaw-row export. Analytic level definitions and any total points remain decisions for freeze. |
| PASS | Generation and evaluation boundary in design | Only frozen spec and optional reference enter prompt construction. Evaluation reads the flaw manifest and checked raw-text derivative. Canary and pair-diff tests are specified for Phase 3. |
| PASS | Resume and reproducibility specified on paper | Version and route mismatches, uncertain network outcomes, accepted-cell skips, atomic publication and raw-byte verification have explicit rules. Reconstruction uses the recorded decisions and data. Operational tests remain pending. |
| PASS | Scope proportional to two researchers | File-based Python, one coordinator, bounded concurrency and two separate rating packets. No infrastructure or dataset implementation beyond the offline scaffold. |
| BLOCKED | Luna Medium | Luna was absent from the selectable collaboration models. Named Luna review could not run. |

### Independent critical review and corrections

**PASS.** A separate read-only sub-agent, using the available inherited model, reviewed the written plan, traceability and local scaffold. It checked the exact condition margins and rating counts by executing the CLI and independently calculated weighted kappa for the fixture. Its results were 48 unique cells, 240 ratings per rater, 480 combined and `κ = 3/7`. The reviewer confirmed the file-based scope and Check-in #2 alignment.

| Priority | Finding | Correction in the final plan |
| --- | --- | --- |
| P1 | Body bytes alone could trigger incorrect acceptance after a crash. | Publish attempt completion only after the raw byte hash and metadata are durable. Treat premature interruption as ambiguous and distinguish it from a completed attempt awaiting outcome publication. |
| P1 | A generation check required evaluation files to be absent while resume also needed to detect flaw-list changes. | Assign evaluation verification to the offline preflight and pass only hashes to the runner. Add tests for preflight rejection on mutation and isolated generation. |
| P2 | A two-person team could see model/context labels through the runner or blind map. | Strip metadata from packets, seal the map until both originals lock and disclose any actual exposure. |
| P2 | A Git commit plus dirty-tree status cannot reconstruct executable changes. | Require the clean frozen commit for formal execution and resume. Add mismatch rejection as a gate. |
| P2 | Raw provider bodies may exceptionally echo credentials. | Preserve restricted originals and hashes with marked scrubbed derivatives. Test the boundary using a mock echoed key. |
| P3 | The Readability audit did not list exact labels. | Added `Grade X`, `Grade 16+` and `Before Grade 1`. |

These corrections update the plan and its acceptance checks. Runner and annotation behavior remain **NOT RUN**.

## Actual checks and limits

The package and its test extra installed in a fresh temporary virtual environment. Python 3.13.9 and Pytest 8.4.2 were used. Direct sandboxed PyPI installation initially failed with `No matching distribution found`. An approved network-enabled install against PyPI succeeded. The tested repository was the local working tree.

```text
$ python -m pip install -e '.[test]'
Successfully installed ... pytest-8.4.2 rubric-benchmark-0.1.0
$ python -m pytest -q -rA
..........                                                               [100%]
10 passed in 0.26s
```

| Status | Verification item | Observed result |
| --- | --- | --- |
| FAIL | First dependency download attempt | Sandboxed pip returned no matching distribution. Retried with an approved PyPI install into a temporary environment. |
| PASS | Editable install and offline Pytest suite | Ten passing cases. Exact grid, credential-free repeated CLI, seven config-error cases and one CLI parse-error case. |
| PASS | Real CLI and independent distribution check | 48 JSON records and 48 unique IDs. Per-model counts `16/16/16`, per-assignment `12/12/12/12`, per-context `24/24`, per-format `24/24`. CLI SHA-256 `a9149376f1848b656bab0744ae7e1f09170e41b5cfb06b519e7bf64fa824869d` for the current config and output serialization. |
| PASS | Credential isolation at scaffold boundary | The CLI emitted identical bytes in subprocesses with empty environments. Git ignore checks confirmed `.env`, `.env.local`, and a local `runs/formal/` path are ignored. The workflow passes no model credentials. Adapter artifact redaction remains untested. |
| PASS | Planned calculations independently checked | From 48 cells, `48 × 5 = 240` flaw score slots per rater and `240 × 2 = 480` overall. Independently verified the coverage fixture and rational kappa calculation `D_observed = 1/4`, `D_expected = 7/16`, `κ = 3/7`. This is fixture arithmetic. |
| PASS | CI workflow parsed and commands exercised locally | Parsed the YAML and checked triggers, read-only repository permissions, and install/test commands. Ran the equivalent install and tests in a local fresh environment. |
| PASS | Deliverable structure and final regression | Checked Markdown tables, local links and anchors, all 18 plan sections, phases 0–6, and 42 unique traceability IDs. Confirmed all six independent-review corrections and reran the suite with ten passes. |
| NOT RUN | Hosted GitHub Actions | Workflow exists locally. This pass made no commit or push. |
| NOT RUN | Frozen dataset, reference behavior and 20 flaw definitions | Official task requirements are verified. Snapshots, vetted code, fixture evidence and independent reviewer sign-offs are Phase 2 work. |
| NOT RUN | Prompt isolation, provider compatibility, raw integrity, retries and resume | Tests and expected outcomes are specified. No adapters, prompts, or runner exist yet. |
| NOT RUN | Live pilot and 48 formal requests | No model endpoint calls, costs, rubric outputs or observed model performance. |
| NOT RUN | Human ratings, implementation-bias frequency and inter-rater agreement | No rater data exist. Planned target counts and statistics fixture arithmetic are recorded above. |
| NOT RUN | Analysis package and archive restoration | Reproduction gates are defined. No final tables, figures or research findings exist. |

## Remaining risks and readiness

Ready to start Phase 2 with a local, tested matrix scaffold. Before formal generation the team needs four frozen assignment packages with independently verified flaws, exact model deployments and parameter rules, a tested runner, a documented pilot and a frozen codebook. Campus course deliverables and deadline remain unverified. The milestone-based plan can proceed from the available course requirements.

## Phase 2 Mario development update

| Status | Item | Evidence |
| --- | --- | --- |
| PASS | Official Mario source snapshot | Retrieved the 2026 dated URL and preserved the HTML, selected text, requested/resolved URLs, access timestamp, license link and SHA-256 hashes in `data/assignments/mario-more/provenance.json`. |
| PASS | Reference cases | Automated tests run the example reference with a stub for CS50's `get_int`. They verify exact output at heights 1, 2 and 8 and re-prompting for -1, 0 and 9. The stub supplies integers and does not test CS50 library handling of nonnumeric input. |
| PASS | Five flaw records | Each record links to an official requirement, expected and incorrect behavior, distinguishing example and automated evidence. All are technically validated and pending human review. |
| PASS | Generation input isolation | The loader reads an allowlisted specification and optional reference, verifies hashes, and rejects invalid IDs. Tests run without evaluation files and with guarded flaw and rating canaries present. |
| PASS | Mock smoke tests | Two complementary mock conditions exercise point/spec-only and level/spec-plus-reference construction, raw text preservation, status metadata, failure recording and no-overwrite behavior. Mock output is diagnostic and carries no research findings. |
| BLOCKED | Luna 6 Medium independent sub-agent QA | The orchestration interface does not expose Luna as a selectable model. No Luna sub-agent was launched. The earlier reference to API credentials was mistaken and irrelevant to sub-agent availability. Mock testing was performed by the main agent. |
| NOT RUN | Official check50 and real CS50 library integration | No check50 or CS50 runtime was used. The local tests use a controlled input stub. |
| NOT RUN | Independent human review and formal benchmark | The Mario records await researcher review. Other assignment packages, formal model calls, human coding, and analysis remain future work. |

The final local regression command `/tmp/cs500-audit-ebooks/ci-venv/bin/python -m pytest -q` reported **21 passed in 0.72s**. The existing matrix CLI independently emitted 48 conditions. `git diff --check` passed. The added mock smoke helper validates nonempty text only. Point allocations, level anchors, real model metadata, and provider response semantics require live integration and later validation.

## Correction — independent sub-agent smoke testing

Luna was requested as a local independent QA sub-agent. The local orchestration interface lists model overrides `gpt-6.2-sol`, `gpt-6.2-astra`, `gpt-6.1-terra`, `gpt-6.1-sol`, and `gpt-6-astra`, with medium among the supported reasoning efforts. It does not list Luna or a named-agent selector. No substitute was launched for this request, and no benchmark API credentials are relevant to this availability check.

| Status | Verification | Evidence |
| --- | --- | --- |
| BLOCKED | Luna 6 Medium independent QA | Exact requested model is unavailable in the exposed sub-agent configuration. No Luna report or independent execution exists. |
| PASS | Main-agent regression | Re-ran the existing offline suite. `21 passed in 0.63s`. Matrix CLI produced 48 records and 48 unique condition IDs. These are main-agent checks. |
| NOT RUN | Independent review of source, flaw independence, isolation and smoke helper | Existing automated coverage is documented above. A separate Luna verification remains outstanding. |
| NOT RUN | Official check50 | No check50 execution was performed in this correction. |

The existing example evidence checks each counterexample against expected output, but does not establish that each flaw is independent of the others. The input stub also leaves actual CS50 library input behavior unverified. The Mario layout is a preliminary template for later packages, subject to the requested independent review and research-team validation.

## Sub-agent selection diagnostic

A direct local `spawn_agent` call accepted `model="gpt-6-luna"` and `reasoning_effort="medium"` and returned `/root/luna_mario_qa`. The agent completed independent read-only checks and a follow-up test run. The interface returned no backend rejection, but it also exposed no resolved model or reasoning metadata to the parent or agent. The actual runtime model and effort therefore remain unverified. This supersedes the earlier conclusion that direct selection was unavailable.

The sub-agent independently verified the source hashes, inspected the requirements, reference, flaw records and loader, exercised mock smoke output, and checked the matrix margins. It subsequently ran the existing virtual environment's test suite with **21 passed in 0.44s**. It found that flaw independence lacks executable pairwise evidence, and that the development smoke helper checks only nonempty output rather than provider or rubric-format validity. The agent did not run official check50 or CS50 library integration. No benchmark implementation was changed during this diagnostic.
