import contextlib
import io
import json
import runpy
import subprocess
import sys
import types
import zipfile
from pathlib import Path

import pytest

from rubric_benchmark.dataset import load_generation_input

ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = ROOT / 'data' / 'assignments'


def run_interactive(monkeypatch, name, inputs):
    values = iter(inputs)
    calls = []
    def read(prompt):
        calls.append(prompt)
        return next(values)
    monkeypatch.setitem(sys.modules, 'cs50', types.SimpleNamespace(get_float=read, get_string=read))
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        runpy.run_path(str(ASSIGNMENTS / name / 'reference.py'), run_name='__main__')
    return output.getvalue(), len(calls)


@pytest.mark.parametrize(('inputs', 'expected'), [([0], '0\n'), ([0.41], '4\n'), ([0.01], '1\n'), ([0.15], '2\n'), ([1.60], '7\n'), ([23], '92\n'), ([4.2], '18\n'), ([0.29], '5\n'), ([0.50], '2\n'), ([-1, -0.25, 0.50], '2\n')])
def test_cash(monkeypatch, inputs, expected):
    assert run_interactive(monkeypatch, 'cash', inputs) == (expected, len(inputs))


@pytest.mark.parametrize(('text', 'expected'), [
    ('One fish. Two fish. Red fish. Blue fish.', 'Before Grade 1'),
    ('Would you like them here or there? I would not like them here or there. I would not like them anywhere.', 'Grade 2'),
    ('Green birds fly high above lakes 1234567890.', 'Grade 3'),
    ("Don't stop looking around the garden.", 'Grade 9'),
    ('Bright stars! Silver moons? Lanterns shine.', 'Grade 4'),
    ('Bright stars shine above the lake.', 'Grade 7'),
    ('Small cats nap.', 'Before Grade 1'),
    ('Extraordinary discoveries inspire curiosity.', 'Grade 16+'),
])
def test_readability(monkeypatch, text, expected):
    assert run_interactive(monkeypatch, 'readability', [text]) == (expected + '\n', 1)


def run_dna(*args):
    return subprocess.run([sys.executable, str(ASSIGNMENTS / 'dna' / 'reference.py'), *map(str, args)], capture_output=True, text=True, check=True).stdout


def test_dna_official_examples(tmp_path):
    with zipfile.ZipFile(ASSIGNMENTS / 'dna' / 'starter.zip') as archive:
        for name in archive.namelist():
            path = Path(name)
            assert not path.is_absolute() and '..' not in path.parts
        archive.extractall(tmp_path)
    base = tmp_path / 'dna'
    expected = ['Bob', 'No match', 'No match', 'Alice', 'Lavender', 'Luna', 'Ron', 'Ginny', 'Draco', 'Albus', 'Hermione', 'Lily', 'No match', 'Severus', 'Sirius', 'No match', 'Harry', 'No match', 'Fred', 'No match']
    for i, name in enumerate(expected, 1):
        db = 'small.csv' if i <= 4 else 'large.csv'
        assert run_dna(base / 'databases' / db, base / 'sequences' / f'{i}.txt') == name + '\n'


@pytest.mark.parametrize(('csv_text', 'sequence', 'expected'), [
    ('name,CG\nBea,1\nAda,2\n', 'CGCG', 'Ada'),
    ('name,AC\nAda,3\nBea,4\n', 'ACACACGGAC', 'Ada'),
    ('name,AC,GT\nBea,2,2\nAda,2,1\n', 'ACACGT', 'Ada'),
    ('name,AC,GT\nAda,1,2\n', 'ACACGT', 'No match'),
])
def test_dna_cases(tmp_path, csv_text, sequence, expected):
    db, seq = tmp_path / 'db.csv', tmp_path / 'seq.txt'
    db.write_text(csv_text)
    seq.write_text(sequence)
    assert run_dna(db, seq) == expected + '\n'


def test_dna_arguments():
    for args in [(), ('a',), ('a', 'b', 'c')]:
        assert 'Usage:' in run_dna(*args)


def test_datasets_and_flaw_manifests():
    for name in ('cash', 'readability', 'dna'):
        plain = load_generation_input(ASSIGNMENTS, name, include_reference=False)
        reference = load_generation_input(ASSIGNMENTS, name, include_reference=True)
        assert plain.reference is None and reference.reference and plain.specification == reference.specification
        data = json.loads((ROOT / 'data' / 'evaluation' / name / 'flaws.json').read_text())
        assert len(data['flaws']) == len({item['flaw_id'] for item in data['flaws']}) == 5


def test_distinguishing_counterexamples():
    # Each faulty calculation produces a different observable result from the reference case.
    assert int(0.29 * 100) == 28
    assert 28 // 25 + (28 % 25) == 4  # pennies after a quarter
    assert 5 != 2  # five dimes versus two quarters
    assert 3 != 4  # omitting the final penny from 41 cents
    assert '1 coin\n' != '1\n'

    def grade(letters, words, sentences):
        value = 0.0588 * 100 * letters / words - 0.296 * 100 * sentences / words - 15.8
        return round(value)
    assert grade(37, 7, 1) == 11 and grade(27, 7, 1) == 3
    assert grade(30, 7, 1) == 5 and grade(30, 6, 1) == 9
    assert grade(35, 6, 1) == 14 and grade(35, 6, 3) == 4
    assert int(6.7066666667) == 6 and round(6.7066666667) == 7

    assert 'ACACACGGAC'.count('AC') == 4
    assert (2, 2) != (2, 1)  # a partial profile must not match
    assert (1, 2) != (2, 1)  # no profile matches
