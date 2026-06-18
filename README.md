# Consulting Template Kit

> Public-safe consulting & technical-writing templates: document kits and process scaffolds.

[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![version](https://img.shields.io/badge/version-0.1.0-informational.svg)
[![CI](https://github.com/HarperZ9/consulting-template-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/HarperZ9/consulting-template-kit/actions/workflows/ci.yml)
![deps: none](https://img.shields.io/badge/deps-none-success.svg)
[![part of: AI-accountability toolkit](https://img.shields.io/badge/part_of-AI--accountability_toolkit-7a5cff.svg)](https://harperz9.github.io)

The kit is intentionally plain: statement of work, engagement letter, invoice,
proposal email, project brief, and technical-writing cover letter templates.
It includes a validator that catches common release mistakes before a template
is reused or published.

## What Is Included

- `templates/engagement-letter.md`
- `templates/statement-of-work.md`
- `templates/invoice.md`
- `templates/proposal-email.md`
- `templates/technical-writing-cover-letter.md`
- `templates/project-brief.md`
- `examples/example-project-brief.md`
- `src/consulting_template_kit/validator.py` (the installable package and `ctk-validate` console script)
- `scripts/validate_templates.py` (no-install wrapper around the package)

## Quick Start

```powershell
python -m pip install -e .
python scripts/validate_templates.py templates examples
```

The validator flags:

- secret-shaped text
- private contact placeholders that should remain generic
- payment-account wording
- suspicious personal/customer data patterns
- templates without bracketed placeholders

## Use

Copy a template, replace bracketed placeholders, and run the validator against
the finished draft before sending it.

```powershell
ctk-validate templates examples
```

A clean run prints nothing and exits `0`; findings are printed one per line and
exit `1`. See [USAGE.md](USAGE.md) for the full command-line reference, the
finding codes, the Python API, and worked examples.

## Boundaries

These files are not legal, accounting, tax, or compliance advice. They are
starter documents for scoping, communication, and operational hygiene.

Do not publish filled versions that contain client names, payment details,
private rates, addresses, or signed terms.

---
**Zain Dana Harper** — small tools with explicit edges.
[Portfolio](https://harperz9.github.io) · [HarperZ9](https://github.com/HarperZ9)
<sub>Built with Claude Code; reviewed, tested, and owned by me.</sub>
