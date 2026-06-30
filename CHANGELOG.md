# Changelog

## 2026-06-29 - Public Delivery Refresh

- Added this public changelog.
- Updated CI to current checkout/setup-python action majors.
- Replaced key-shaped documentation/test literals with runtime-assembled
  examples so public scanners do not flag synthetic fixture text as a leaked
  credential.
- Normalized scanner-blocking dash punctuation in public docs and examples.

## Current Status

- Runtime: Python package and CLI validator.
- Surfaces: reusable templates, examples, validation script, usage guide, and CI.
- Verification: pytest suite and public surface sweep.
