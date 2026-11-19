# Cash, Readability, and DNA Local Validation Record

2026-11-18. See each assignment's `provenance.json` for official source and reference implementation hashes. The three specification texts were extracted from Problem to Solve and Specification; the original HTML was retained. The official DNA starter.zip was used for testing, with its hash and URL recorded. The project authored the reference implementations; the DNA reference independently implements the longest consecutive match algorithm.

Ran `/tmp/cs500-audit-ebooks/ci-venv/bin/python -m pytest -q`: 46 passed. After adding counterexample calculation checks, ran `.../python -m pytest -q tests/test_remaining_assignments.py`: 26 passed. Cash and Readability interaction tests used CS50 input stubs. All 20 official examples in the DNA starter test data passed; tests also covered argument count, dynamic STRs, longest consecutive runs, exact matching, and no match.

Correct behavior for the 15 candidate flaws was run or checked in `tests/test_remaining_assignments.py`. Some numerical counterexamples were independently calculated; single-flaw programs had not yet been constructed for every item, nor had independence of the flaws been established. The list therefore retains the `reference_case_passed_counterexample_pending_independent_validation` status pending further validation and researcher review.

Official check50, interaction with the real CS50 library, and GPT-6 Luna generation calls were not run at this stage. This session did not provide an interface or credentials for selecting that model, so the model and thinking effort could not be verified; local mock tests cannot replace a real-model smoke test. Readability rounding boundaries, empty input, and unusual whitespace require separate verification against the official specification and checks.

## Additional validation on 2026-11-18

Generated 15 single-point code variants in a temporary directory, each using one text replacement in the corresponding reference implementation. Ran `python data/evaluation/mutation/run_mutations.py` and saved results in `data/evaluation/mutation/results.json`. Each reference passed all five input sets for its assignment, and each variant failed its corresponding test set. The DNA header case originally placed the correct match first, allowing the hard-coded-field variant to pass incorrectly; Bea was moved before Ada to expose the incorrect match.

The five columns in each row below follow that assignment's `flaws.json` order. `X` means the variant caused that case to fail; `.` means it passed. The matrix shows that each variant is distinguished by its own case and also shows overlap among cases; it does not prove that all possible flaw implementations are independent.

```text
cash.reference          .....
cash.negative-reprompt  X....
cash.cents              .X...
cash.minimum            XXXX.
cash.remainder          .X.XX
cash.final-line         XXXXX
readability.reference   .....
readability.letters     X....
readability.words       .X...
readability.sentences   ..X..
readability.index       XXXX.
readability.grade-labels ....X
dna.reference           .....
dna.arity               X....
dna.csv-fields          .X.XX
dna.longest-run         ..X..
dna.exact-profile       ...X.
dna.no-match            ....X
```

The Cash minimum-coin variant affected other amount results, and the final-line format variant changed every output; Readability truncation can affect multiple numerical grades; fixed DNA fields also affect match and no-match cases. These observations do not make the flaw definitions mutually exclusive. Researchers must decide scoring boundaries before the formal freeze.

Installed `cs50 9.5.0` and `check50 3.5.0` in `/tmp/cs50-verification-env`. With the real CS50 library, Cash received `foo`, a blank line, `-1`, and `0.41` and ultimately printed 4; Readability printed `Before Grade 1` for the official One fish example. Using `check50 --local --no-download-checks --no-install-dependencies` with the temporary environment's `bin` first on PATH, the official checks passed: Cash 10/10, Readability 10/10, DNA 29/29. The first Cash run did not set PATH, so the checks used system Python without CS50 and nine checks failed. All passed when rerun with the correct PATH.

These automated checks do not replace independent researcher review. See `data/evaluation/mutation/results.json` for each process's output and exit status. Earlier Luna smoke outputs and their scores were deleted.
