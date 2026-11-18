import json
import subprocess
import sys
from collections import Counter
from itertools import product
from pathlib import Path

import pytest

from rubric_benchmark.matrix import load_matrix


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "experiment.toml"
EXPECTED_LEVELS = {
    "model": {"gpt": 16, "claude": 16, "gemini": 16},
    "assignment": {"mario-more": 12, "cash": 12, "readability": 12, "dna": 12},
    "reference_context": {"spec-only": 24, "spec-reference": 24},
    "rubric_format": {"points": 24, "levels": 24},
}


def test_formal_design_contains_every_expected_cell_once():
    conditions = load_matrix(CONFIG)
    assert len(conditions) == 48
    assert {condition.condition_id for condition in conditions} == {
        ".".join(levels) for levels in product(*EXPECTED_LEVELS.values())
    }
    for dimension, distribution in EXPECTED_LEVELS.items():
        assert Counter(getattr(condition, dimension) for condition in conditions) == distribution


def test_cli_emits_deterministic_matrix_without_credentials():
    command = [
        sys.executable, "-m", "rubric_benchmark", "matrix", "--config", str(CONFIG),
    ]
    first = subprocess.run(command, cwd=ROOT, env={}, capture_output=True, check=True)
    second = subprocess.run(command, cwd=ROOT, env={}, capture_output=True, check=True)
    assert first.stdout == second.stdout
    assert first.stderr == second.stderr == b""
    expected = load_matrix(CONFIG)
    rows = json.loads(first.stdout)
    assert len(rows) == 48
    assert [row["condition_id"] for row in rows] == [cell.condition_id for cell in expected]
    assert rows[0] == {
        "condition_id": "gpt.mario-more.spec-only.points",
        "model": "gpt",
        "assignment": "mario-more",
        "reference_context": "spec-only",
        "rubric_format": "points",
    }


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        ('model = ["gpt", "gpt"]', "duplicate levels"),
        ("model = []", "non-empty list"),
        ('model = "gpt"', "non-empty list"),
        ('model = ["gpt.with-dot"]', "lowercase alphanumeric IDs"),
        ("model = [17]", "lowercase alphanumeric IDs"),
        ('provider = ["gpt"]', "must contain exactly"),
        ('model = ["gpt"]\nextra = ["unknown"]', "must contain exactly"),
    ],
)
def test_rejects_invalid_dimensions(tmp_path, replacement, message):
    config = tmp_path / "invalid.toml"
    source = CONFIG.read_text(encoding="utf-8")
    config.write_text(
        source.replace('model = ["gpt", "claude", "gemini"]', replacement),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=message):
        load_matrix(config)


def test_cli_reports_invalid_toml_without_emitting_conditions(tmp_path):
    config = tmp_path / "invalid.toml"
    config.write_text("[dimensions", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "rubric_benchmark", "matrix", "--config", str(config)],
        cwd=ROOT, capture_output=True, text=True,
    )

    assert result.returncode == 2
    assert "error:" in result.stderr
    assert result.stdout == ""
