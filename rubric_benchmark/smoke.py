"""Small development-only smoke path with an injected model callable."""

from datetime import datetime, timezone
import json
from pathlib import Path

from .dataset import load_generation_input


def build_smoke_prompt(assignments_dir: Path, assignment_id: str, *,
                       include_reference: bool, rubric_format: str) -> str:
    """Build a development prompt from verified assignment inputs."""
    assignment = load_generation_input(
        assignments_dir, assignment_id, include_reference=include_reference
    )
    instruction = (
        "Create an actionable grading rubric. Accept all implementations "
        "that satisfy the assignment requirements. "
    )
    if rubric_format == "points":
        instruction += "Assign points to each criterion."
    elif rubric_format == "levels":
        instruction += "Provide performance levels for each criterion."
    else:
        raise ValueError("unsupported rubric format")
    prompt = instruction + "\n\n" + assignment.specification
    if assignment.reference is not None:
        prompt += "\n\nExample reference implementation:\n" + assignment.reference
    return prompt


def run_smoke(assignments_dir: Path, output_dir: Path, generate, *,
              assignment_id: str = "mario-more",
              conditions=((False, "points"), (True, "levels"))) -> None:
    """Exercise two complementary conditions using the supplied model callable."""
    output_dir.mkdir(parents=True, exist_ok=False)
    for index, (include_reference, rubric_format) in enumerate(conditions, 1):
        prompt = build_smoke_prompt(assignments_dir, assignment_id,
                                    include_reference=include_reference,
                                    rubric_format=rubric_format)

        condition_dir = output_dir / str(index)
        condition_dir.mkdir()
        (condition_dir / "input.json").write_text(
            json.dumps({"format": rubric_format, "reference": include_reference,
                        "prompt": prompt}, indent=2) + "\n", encoding="utf-8"
        )
        try:
            response = generate(prompt)
            if not isinstance(response, str):
                raise TypeError("model response must be text")
            (condition_dir / "raw.txt").write_text(response, encoding="utf-8")
            status = "success" if response.strip() else "empty_response"
            error = None
        except Exception as exc:
            status = "error"
            error = type(exc).__name__
        (condition_dir / "metadata.json").write_text(
            json.dumps({"mode": "development", "status": status, "error": error,
                        "timestamp": datetime.now(timezone.utc).isoformat()},
                       indent=2) + "\n", encoding="utf-8"
        )
