"""Best-effort demo -- not runtime-verified by author.

End-to-end demonstration of the consulting-template-kit validator using only
the package's public API: ``validate_paths`` and the ``Finding`` dataclass
(both exported from ``consulting_template_kit``).

Run from the repository root:

    python examples/demo_validate.py

It works without installing the package: the path bootstrap below mirrors
``scripts/validate_templates.py`` by adding ``src/`` to ``sys.path``.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

# Allow running straight from a clone, without `pip install -e .`.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from consulting_template_kit import Finding, validate_paths  # noqa: E402


def report(label: str, findings: list[Finding]) -> None:
    print(f"\n== {label} ==")
    if not findings:
        print("clean: no findings (exit code would be 0)")
        return
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.code}: {finding.message}")
    print(f"{len(findings)} finding(s) (exit code would be 1)")


def main() -> int:
    # 1. Validate the shipped templates and examples. These are kept clean,
    #    so this should report nothing.
    clean = validate_paths([ROOT / "templates", ROOT / "examples"])
    report("shipped templates + examples", clean)

    # 2. Validate a deliberately unsafe draft to show each finding code. The
    #    file has no bracketed placeholders, a client-data line, and a
    #    secret-shaped token line.
    fake_key = "sk-" + "abcdefghijklmnopqrstuvwx"
    bad_text = (
        "# Draft SOW\n"
        "\n"
        "Client Name: Acme Robotics\n"
        f"Token: {fake_key}\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        draft = Path(tmp) / "draft.md"
        draft.write_text(bad_text, encoding="utf-8")
        bad = validate_paths([draft])
        report("deliberately unsafe draft", bad)

    # The real CLI returns 1 when anything is flagged; this demo always exits 0
    # because finding problems in the unsafe sample is the expected outcome.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
