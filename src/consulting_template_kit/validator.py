from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import re
import sys


SECRET_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password|bearer)\b"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"(?i)\b(stripe|paypal|venmo|zelle|routing number|account number)\b"),
]

PRIVATE_DATA_PATTERNS = [
    re.compile(r"\b\d{3}[-.) ]?\d{3}[- ]?\d{4}\b"),
    re.compile(r"(?i)\b(client|customer)\s+(name|email|address|phone)\s*:\s*[^\[]"),
    re.compile(r"(?i)\b\d{3}-\d{2}-\d{4}\b"),
]


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    code: str
    message: str


def iter_markdown(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.suffix.lower() == ".md":
            files.append(path)
    return files


def validate_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text(encoding="utf-8")
    if "[" not in text or "]" not in text:
        findings.append(Finding(path, 1, "placeholder", "template should include bracketed placeholders"))
    for idx, line in enumerate(text.splitlines(), start=1):
        for pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(path, idx, "secret-shape", "remove secret or payment-account wording"))
        for pattern in PRIVATE_DATA_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(path, idx, "private-data", "replace personal or customer data with placeholders"))
    return findings


def validate_paths(paths: list[str | Path]) -> list[Finding]:
    markdown = iter_markdown([Path(p) for p in paths])
    findings: list[Finding] = []
    for path in markdown:
        findings.extend(validate_file(path))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate public-safe consulting templates.")
    parser.add_argument("paths", nargs="+", help="Markdown files or directories to validate")
    args = parser.parse_args(argv)
    findings = validate_paths(args.paths)
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.code}: {finding.message}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
