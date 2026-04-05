# Repository Agent Instructions

## Scope
These instructions apply to the entire repository unless overridden by a deeper `AGENTS.md`.

## Project Layout
- Root HTML entry points: `index.html`, `password.html`
- Root JS behavior: `password.js`
- Root CSS styles: `password.css`
- Python tests live in `tests/`

## Test Guidance
- Use `pytest` style tests.
- Keep tests deterministic and free of network calls.
- Prefer fixtures/helpers over repeated logic.

## Change Policy
- Keep edits minimal and focused to the task.
- When introducing new configuration files, include concise inline comments.
- Only modify files explicitly requested by the user.
- If you identify extra fixes, put suggestions in comments where possible; when comments are not supported, add a companion file named `codex_fixed_<original_filename>`.
