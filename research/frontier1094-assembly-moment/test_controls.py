#!/usr/bin/env python3
"""Confirm the positive fixture passes and the three semantic controls reject."""

import subprocess
import sys
from pathlib import Path

CHECKER = Path(__file__).resolve().parent / "check_moment.py"


def run(args):
    return subprocess.run(
        [sys.executable, "-B", str(CHECKER), *args],
        cwd=Path(__file__).resolve().parents[2],
        text=True,
        capture_output=True,
    )


def main():
    fixture = run(["--fixture"])
    if fixture.returncode != 0:
        print(fixture.stdout)
        print(fixture.stderr)
        raise SystemExit("positive fixture did not pass")
    assembly = run([])
    if assembly.returncode != 0 or "PASS_FRONTIER1094_ASSEMBLY_MOMENT" not in assembly.stdout:
        print(assembly.stdout)
        print(assembly.stderr)
        raise SystemExit("assembly check did not pass")
    for name in ("perturbed-nr", "larger-a", "tampered-hash"):
        outcome = run(["--control", name])
        if outcome.returncode != 1:
            print(outcome.stdout)
            print(outcome.stderr)
            raise SystemExit(f"control {name} exited {outcome.returncode}, expected 1")
    print("PASS_MOMENT_CONTROLS fixture=0 assembly=0 perturbed-nr=1 larger-a=1 tampered-hash=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
