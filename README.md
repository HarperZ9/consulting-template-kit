# consulting-template-kit

Public-safe templates for small consulting, documentation, and software-service work.

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
- `scripts/validate_templates.py`

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

## Boundaries

These files are not legal, accounting, tax, or compliance advice. They are
starter documents for scoping, communication, and operational hygiene.

Do not publish filled versions that contain client names, payment details,
private rates, addresses, or signed terms.
