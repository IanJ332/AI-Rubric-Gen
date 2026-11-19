# AI-Rubric-Gen

Research into generating grading rubrics from CS50x 2026 assignment materials and evaluating whether they cover predefined programming flaws. Data packages are provided for Mario More, Cash, Readability, and DNA.

## Generate rubrics

Requires Python 3.13 or later, valid OpenAI API credentials, and an API deployment supporting `gpt-6-luna` and `high` reasoning effort. Set `OPENAI_API_KEY` securely in your local environment. Do not put the key in the repository or chat.

```sh
python -m rubric_benchmark.luna_run --output runs/luna-high-01
```

The command creates separate spec-only, point-based requests for the four assignments. `runs/luna-high-01/raw_data/<assignment>/` stores inputs, requests, responses, and rubrics; `manifest.json` stores status, model identity, and hashes. The output directory must be new. Generation provides no tools, personal skills, or conversation history to the model; the evaluation flaw lists are also excluded from the prompt. See [generation isolation rules](docs/GENERATION_ISOLATION.md).

**Current limitations:** The end-to-end API requests above have not been verified with real credentials; support for the model ID or parameters is not guaranteed. The generator currently supports only these four archived assignments. New course materials must first be packaged in the `data/assignments/<assignment>/` format and the generation entry point adjusted. After generation, a scoring report must still be written using the course specifications and flaw lists in `data/evaluation`; there is currently no automated scoring report command.

You can tell an agent:

> Use this repository's isolated generation track to generate a point-based rubric for each of Mario More, Cash, Readability, and DNA. Save each raw input and output, then score each item against the official specifications and flaw lists and generate a report. Identify missing, vague, or course-inconsistent criteria and record model identity and verification limitations. Do not use personal skills, configuration, or previously generated rubrics as scoring evidence.

## Research and local verification

```sh
python -m rubric_benchmark matrix --config config/experiment.toml
python -m pip install -e '.[test]'
python -m pytest -q
```

The matrix command lists 48 experimental conditions without calling a model. Each assignment includes the official specification, a reference implementation, and separate evaluation flaw records; researchers must still review the flaws. The reference implementations require the CS50 Python library. Run outputs are excluded by `.gitignore` to avoid pushing generated rubrics and personal data to the remote.

[Implementation plan](docs/IMPLEMENTATION_PLAN.md) · [Detailed plan for three assignments](docs/CS50X_REMAINING_ASSIGNMENTS_PLAN.md) · [Validation record](docs/THREE_ASSIGNMENTS_VALIDATION.md) · [Requirements traceability](docs/REQUIREMENTS_TRACEABILITY.md)
