"""Validate factor levels and enumerate conditions from a TOML file."""

import re
import tomllib
from dataclasses import dataclass
from itertools import product
from pathlib import Path


DIMENSIONS = ("model", "assignment", "reference_context", "rubric_format")
LEVEL_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


@dataclass(frozen=True)
class Condition:
    model: str
    assignment: str
    reference_context: str
    rubric_format: str

    @property
    def condition_id(self) -> str:
        return ".".join(
            (self.model, self.assignment, self.reference_context, self.rubric_format)
        )


def load_matrix(path: Path) -> list[Condition]:
    with path.open("rb") as config_file:
        dimensions = tomllib.load(config_file).get("dimensions")

    if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
        raise ValueError(f"[dimensions] must contain exactly: {', '.join(DIMENSIONS)}")

    level_lists = []
    for dimension in DIMENSIONS:
        levels = dimensions[dimension]
        if not isinstance(levels, list) or not levels:
            raise ValueError(f"{dimension} must be a non-empty list")
        if any(
            not isinstance(level, str) or not LEVEL_ID.fullmatch(level)
            for level in levels
        ):
            raise ValueError(
                f"{dimension} must use lowercase alphanumeric IDs with optional hyphens"
            )
        if len(set(levels)) != len(levels):
            raise ValueError(f"{dimension} contains duplicate levels")
        level_lists.append(levels)

    return [Condition(*levels) for levels in product(*level_lists)]
