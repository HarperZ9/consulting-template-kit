# Usage Guide

`consulting-template-kit` is a set of plain Markdown consulting / technical-writing
templates plus a small validator that catches common release mistakes (leaked
secrets, payment-account wording, private contact data, missing placeholders)
before a filled template is reused or published.

This guide covers the real, current public surface: the `ctk-validate` console
script, the `scripts/validate_templates.py` wrapper, and the Python API
(`consulting_template_kit.validator`).

## Install

```powershell
python -m pip install -e .
```

This installs the package from `src/` and registers the `ctk-validate` console
script (declared in `pyproject.toml` under `[project.scripts]`). Requires
Python 3.9+ and has no third-party dependencies.

## Command-line usage

The validator accepts one or more Markdown files or directories. Directories
are searched recursively for `*.md` files.

### Console script

```powershell
ctk-validate templates examples
```

### Module / wrapper script (no install required)

```powershell
python scripts/validate_templates.py templates examples
```

Both forms call the same `consulting_template_kit.validator:main` entry point.
The wrapper script injects `src/` onto `sys.path`, so it works straight from a
clone without `pip install`.

### Exit codes and output

- Exit code `0` and **no output** when nothing is flagged.
- Exit code `1` and one line per finding when problems are found.

Each finding line has the form:

```
<path>:<line>: <code>: <message>
```

The validator reports these codes:

| Code | When it fires |
| --- | --- |
| `placeholder` | The file contains no `[` and `]` bracketed placeholders (always reported at line 1). |
| `secret-shape` | A line matches secret/payment wording: `api_key`, `secret`, `token`, `password`, `bearer`, an `sk-...` key, or `stripe`/`paypal`/`venmo`/`zelle`/`routing number`/`account number`. |
| `private-data` | A line matches a phone-number pattern, an SSN-shaped pattern, or `client`/`customer` followed by `name`/`email`/`address`/`phone`. |

## Worked examples

### 1. Validate the shipped templates (clean pass)

```powershell
ctk-validate templates examples
```

Expected output (the shipped templates are kept clean, so there is none):

```
```

Exit code: `0`.

### 2. Catch a leaked secret and a missing placeholder

Given a file `draft.md`:

```markdown
# Draft SOW

Client Name: Acme Robotics
Token: <redacted API key>
```

Run:

```powershell
ctk-validate draft.md
```

Expected output (illustrative -- paths shown as `draft.md`; the validator prints
the path exactly as you passed it):

```
draft.md:1: placeholder: template should include bracketed placeholders
draft.md:3: private-data: replace personal or customer data with placeholders
draft.md:4: secret-shape: remove secret or payment-account wording
draft.md:4: secret-shape: remove secret or payment-account wording
```

Exit code: `1`. (Line 4 matches the `token` keyword. A real key-shaped value is
also flagged, but examples should not publish key-shaped strings.)

### 3. Validate a single directory

```powershell
ctk-validate templates
```

Validates every `*.md` under `templates/` recursively. Expected output: none,
exit code `0`.

### 4. Use the Python API directly

```python
from pathlib import Path
from consulting_template_kit.validator import validate_paths

findings = validate_paths([Path("templates"), Path("examples")])
for f in findings:
    print(f.code, f.path, f.line, f.message)

print("clean" if not findings else f"{len(findings)} finding(s)")
```

`validate_paths(paths)` accepts a list of `str` or `Path` entries and returns a
list of frozen `Finding` dataclasses with fields `path`, `line`, `code`, and
`message`. On the shipped templates it returns an empty list:

```
clean
```

`Finding` and `validate_paths` are the package's exported API
(`consulting_template_kit.__all__`).

## Recommended workflow

Copy a template from `templates/`, replace the bracketed placeholders with your
own content, and run the validator against the finished draft before sending or
publishing it:

```powershell
ctk-validate path/to/your-draft.md
```

A clean exit (code `0`, no output) means none of the leak heuristics fired. The
validator is a pre-publication safety net, not a guarantee -- review filled
documents by hand as well.
