from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"


def execute(script: str, args: list[str]) -> None:
    command = [sys.executable, str(SCRIPTS / script), *args]
    subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Skill Harvester command runner"
    )
    parser.add_argument(
        "command",
        choices=["collect", "analyze", "consolidate", "build-readme", "all"],
    )
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    optional_limit = ["--limit", str(args.limit)] if args.limit else []

    if args.command == "collect":
        execute("collect_skills.py", optional_limit)
    elif args.command == "analyze":
        execute("analyze_skills.py", optional_limit)
    elif args.command == "consolidate":
        execute("consolidate_skills.py", optional_limit)
    elif args.command == "build-readme":
        execute("build_readme.py", [])
    else:
        execute("collect_skills.py", optional_limit)
        execute("analyze_skills.py", optional_limit)
        execute("consolidate_skills.py", optional_limit)
        execute("build_readme.py", [])
