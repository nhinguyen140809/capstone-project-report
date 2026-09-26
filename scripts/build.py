"""Compile the report with latexmk. Works on Windows, macOS and Linux with no extra Python packages.

    python scripts/build.py            build once, producing main.pdf at the repo root
    python scripts/build.py watch      rebuild on every file save, press Ctrl+C to stop
    python scripts/build.py clean      remove build/ and main.pdf

Build settings (engine, output directories, biber) live in .latexmkrc; this script only calls latexmk.
Options the script does not recognize are passed through to latexmk, e.g. `python scripts/build.py build -g`
to force a full rebuild.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"
PDF = ROOT / "main.pdf"
LOG = BUILD_DIR / "main.log"


def check_tools() -> None:
    missing = [tool for tool in ("latexmk", "perl") if shutil.which(tool) is None]
    if missing:
        sys.exit(
            f"Could not find {', '.join(missing)} in PATH. "
            "See the 'Install compiler' section in README.md."
        )


def print_errors() -> None:
    """Print error lines such as `chapters/x/goals.tex:12: ...` with the offending code, faster than reading the full log."""
    if not LOG.exists():
        return
    lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    error_line = re.compile(
        r"^(?:[A-Za-z]:)?[^:\s]+:\d+: |^! "
        # .latexmkrc enables $warnings_as_errors, so these warnings also fail the build
        r"|Warning: (Reference|Citation) .* undefined|multiply defined|Missing character"
    )
    errors = []
    for i, line in enumerate(lines):
        if error_line.search(line):
            errors.append(line)
            # Right after an error, TeX prints the offending code on a line starting with `l.<line number>`
            errors += [f"    {ctx}" for ctx in lines[i + 1 : i + 4] if ctx.startswith("l.")][:1]
    if errors:
        print("\nErrors in build/main.log:", file=sys.stderr)
        for line in errors[:20]:
            print(f"  {line}", file=sys.stderr)


def latexmk(extra: list[str]) -> int:
    check_tools()
    result = subprocess.run(["latexmk", *extra], cwd=ROOT)
    return result.returncode


def build(extra: list[str]) -> int:
    code = latexmk(extra)
    if code == 0:
        print(f"\nPDF: {PDF.relative_to(ROOT).as_posix()}")
    else:
        print_errors()
    return code


def watch(extra: list[str]) -> int:
    # -pvc: watch source files and rebuild on change. -view=none: do not open a PDF viewer.
    try:
        return latexmk(["-pvc", "-view=none", *extra])
    except KeyboardInterrupt:
        return 0


def clean(_: list[str]) -> int:
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    for f in (PDF, PDF.with_suffix(".synctex.gz")):
        f.unlink(missing_ok=True)
    print("Removed build/ and main.pdf")
    return 0


def main() -> int:
    # Windows consoles fall back to cp1252 when output is piped; force UTF-8 so non-ASCII text in the log prints correctly.
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")
    commands = {"build": build, "watch": watch, "clean": clean}
    parser = argparse.ArgumentParser(description="Compile the report with latexmk.")
    parser.add_argument("command", nargs="?", default="build", choices=commands)
    args, extra = parser.parse_known_args()
    return commands[args.command](extra)


if __name__ == "__main__":
    sys.exit(main())
