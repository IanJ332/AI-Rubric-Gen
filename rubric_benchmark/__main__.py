"""Offline command-line interface."""

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .matrix import load_matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="Enumerate rubric benchmark conditions")
    subcommands = parser.add_subparsers(dest="command", required=True)
    matrix_command = subcommands.add_parser("matrix", help="Print the condition matrix as JSON")
    matrix_command.add_argument("--config", required=True, type=Path, help="Experiment TOML file")
    args = parser.parse_args()

    try:
        conditions = load_matrix(args.config)
    except (OSError, ValueError) as error:
        matrix_command.error(str(error))

    records = [
        {"condition_id": condition.condition_id, **asdict(condition)}
        for condition in conditions
    ]
    print(json.dumps(records, indent=2))


if __name__ == "__main__":
    main()
