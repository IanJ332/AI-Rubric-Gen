"""Load verified assignment inputs for rubric generation."""

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import re


@dataclass(frozen=True)
class GenerationInput:
    assignment_id: str
    specification: str
    reference: str | None


def load_generation_input(
    assignments_dir: Path, assignment_id: str, *, include_reference: bool
) -> GenerationInput:
    """Read only the specification and, when requested, the reference."""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", assignment_id):
        raise ValueError("invalid assignment ID")
    directory = assignments_dir / assignment_id
    provenance = json.loads((directory / "provenance.json").read_text(encoding="utf-8"))
    if provenance["assignment_id"] != assignment_id:
        raise ValueError("assignment ID does not match provenance")

    def read_verified(name: str) -> str:
        content = (directory / name).read_bytes()
        if sha256(content).hexdigest() != provenance["sha256"][name]:
            raise ValueError(f"hash mismatch: {name}")
        return content.decode("utf-8")

    specification = read_verified("specification.txt")
    reference = read_verified("reference.py") if include_reference else None
    return GenerationInput(assignment_id, specification, reference)
