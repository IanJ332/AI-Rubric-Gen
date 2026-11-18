import json
import runpy
import sys
import types
from dataclasses import asdict
from pathlib import Path

import pytest

from rubric_benchmark.dataset import load_generation_input


ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = ROOT / "data" / "assignments"
EVALUATION = ROOT / "data" / "evaluation" / "mario-more" / "flaws.json"
REFERENCE = ASSIGNMENTS / "mario-more" / "reference.py"


def run_reference(monkeypatch, capsys, inputs):
    values = iter(inputs)
    calls = []

    def get_int(prompt):
        calls.append(prompt)
        return next(values)

    monkeypatch.setitem(sys.modules, "cs50", types.SimpleNamespace(get_int=get_int))
    runpy.run_path(str(REFERENCE), run_name="__main__")
    return capsys.readouterr().out, len(calls)


@pytest.mark.parametrize(
    ("inputs", "expected", "calls"),
    [
        ([1], "#  #\n", 1),
        ([2], " #  #\n##  ##\n", 1),
        ([8], "       #  #\n      ##  ##\n     ###  ###\n    ####  ####\n"
              "   #####  #####\n  ######  ######\n #######  #######\n########  ########\n", 1),
        ([-1, 0, 9, 2], " #  #\n##  ##\n", 4),
    ],
)
def test_official_examples(monkeypatch, capsys, inputs, expected, calls):
    assert run_reference(monkeypatch, capsys, inputs) == (expected, calls)


def test_flaw_evidence(monkeypatch, capsys):
    manifest = json.loads(EVALUATION.read_text())
    flaws = manifest["flaws"]
    provenance = json.loads((ASSIGNMENTS / "mario-more" / "provenance.json").read_text())
    assert manifest["assignment_id"] == "mario-more"
    assert len(flaws) == len({flaw["flaw_id"] for flaw in flaws}) == 5
    for flaw in flaws:
        assert flaw["requirement_id"] in provenance["requirements"]
        assert flaw["expected_behavior"] and flaw["incorrect_behavior"]
        assert flaw["status"] == "technically_validated_pending_human_review"
        inputs = [int(value) for value in flaw["test_input"].splitlines()]
        actual, calls = run_reference(monkeypatch, capsys, inputs)
        assert actual == flaw["expected_output"]
        if flaw["requirement_id"] == "height":
            assert calls == 2
            assert flaw["counterexample"] == "accepts 9 as height"
        else:
            assert actual != flaw["counterexample"]


def test_generation_isolation_and_reference_selection(tmp_path):
    import shutil

    shutil.copytree(ASSIGNMENTS / "mario-more", tmp_path / "mario-more")
    # Evaluation data is unavailable to this invocation.
    plain = load_generation_input(tmp_path, "mario-more", include_reference=False)
    with_reference = load_generation_input(tmp_path, "mario-more", include_reference=True)
    assert plain.specification == with_reference.specification
    assert plain.reference is None
    assert "from cs50 import get_int" in with_reference.reference
    assert "flaw_id" not in repr(asdict(with_reference))
    assert not (tmp_path / "evaluation").exists()


def test_rejects_modified_input_and_invalid_id(tmp_path):
    import shutil

    shutil.copytree(ASSIGNMENTS / "mario-more", tmp_path / "mario-more")
    (tmp_path / "mario-more" / "specification.txt").write_text("changed")
    with pytest.raises(ValueError, match="hash mismatch"):
        load_generation_input(tmp_path, "mario-more", include_reference=False)
    with pytest.raises(ValueError, match="invalid assignment ID"):
        load_generation_input(tmp_path, "../evaluation", include_reference=False)


def test_mock_smoke_preserves_outputs_and_isolates_evaluation(tmp_path):
    from rubric_benchmark.smoke import run_smoke

    calls = []

    def mock_model(prompt):
        calls.append(prompt)
        return "Criterion: follows assignment.\n"

    output = tmp_path / "development"
    run_smoke(ASSIGNMENTS, output, mock_model)
    assert len(calls) == 2
    first = json.loads((output / "1" / "input.json").read_text())
    second = json.loads((output / "2" / "input.json").read_text())
    assert first["reference"] is False and second["reference"] is True
    assert "Assign points" in first["prompt"]
    assert "performance levels" in second["prompt"]
    assert "from cs50 import get_int" not in first["prompt"]
    assert "from cs50 import get_int" in second["prompt"]
    assert all("flaw_id" not in prompt for prompt in calls)
    assert (output / "1" / "raw.txt").read_text() == "Criterion: follows assignment.\n"
    assert json.loads((output / "2" / "metadata.json").read_text())["status"] == "success"
    with pytest.raises(FileExistsError):
        run_smoke(ASSIGNMENTS, output, mock_model)


def test_mock_smoke_records_failure(tmp_path):
    from rubric_benchmark.smoke import run_smoke

    def broken_model(prompt):
        raise TimeoutError("private details")

    output = tmp_path / "development"
    run_smoke(ASSIGNMENTS, output, broken_model)
    record = json.loads((output / "1" / "metadata.json").read_text())
    assert record["status"] == "error"
    assert record["error"] == "TimeoutError"
    assert not (output / "1" / "raw.txt").exists()


def test_source_and_reference_hashes():
    import hashlib

    directory = ASSIGNMENTS / "mario-more"
    provenance = json.loads((directory / "provenance.json").read_text())
    for filename, expected in provenance["sha256"].items():
        assert hashlib.sha256((directory / filename).read_bytes()).hexdigest() == expected


def test_generation_does_not_read_evaluation_files(tmp_path, monkeypatch):
    import shutil

    shutil.copytree(ASSIGNMENTS / "mario-more", tmp_path / "assignments" / "mario-more")
    evaluation = tmp_path / "evaluation"
    evaluation.mkdir()
    (evaluation / "flaws.json").write_text("SECRET_FLAW_CANARY")
    (evaluation / "ratings.csv").write_text("SECRET_RATING_CANARY")
    original_text = Path.read_text
    original_bytes = Path.read_bytes

    def guarded_text(path, *args, **kwargs):
        assert evaluation not in path.parents
        return original_text(path, *args, **kwargs)

    def guarded_bytes(path):
        assert evaluation not in path.parents
        return original_bytes(path)

    monkeypatch.setattr(Path, "read_text", guarded_text)
    monkeypatch.setattr(Path, "read_bytes", guarded_bytes)
    result = load_generation_input(tmp_path / "assignments", "mario-more", include_reference=True)
    assert "SECRET_FLAW_CANARY" not in repr(result)
    assert "SECRET_RATING_CANARY" not in repr(result)
