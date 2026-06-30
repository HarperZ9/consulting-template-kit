from pathlib import Path

from consulting_template_kit.validator import validate_paths


def test_templates_pass_public_gate() -> None:
    findings = validate_paths([Path("templates"), Path("examples")])
    assert findings == []


def test_secret_shaped_text_is_flagged(tmp_path: Path) -> None:
    sample = tmp_path / "bad.md"
    fake_key = "sk-" + "abcdefghijklmnopqrstuvwxyz"
    sample.write_text(f"# Bad\n\nToken: {fake_key}\n", encoding="utf-8")
    findings = validate_paths([sample])
    assert any(finding.code == "secret-shape" for finding in findings)


def test_phone_number_is_flagged(tmp_path: Path) -> None:
    sample = tmp_path / "bad.md"
    sample.write_text("# Bad\n\nCall [Name] at 206-555-0199.\n", encoding="utf-8")
    findings = validate_paths([sample])
    assert any(finding.code == "private-data" for finding in findings)
