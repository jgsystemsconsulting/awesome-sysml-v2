# ARL triage log: plan 2026-09-16-github-notice-surface

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Task 2 content order vs AC1 ordering (title/scope first, checklist, gates, steps, curation, alternatives) | R1 | R1 | FP | Verified in plan L123-186: block starts with title then Scope line then Sections A-E in AC1 order; no inconsistency exists |
| Hardcoded "as of 2026-09-16" cells stale if execution slips | R1 | R1 | Design | Dated snapshot is intentional; scope line says re-verify before acting and Task 2 Step 2 updates cells to live values |
| Section B quote/URL formatting ambiguity (inline vs Source line) | R1 | R1 | Advisory-skipped | Source URL sits on the line after each quote; AC5 satisfied; inline rewrite would touch four quotes for no functional gain |
| Task 4 expected output should show `?? docs/superpowers/` persisting alongside staged file | R1 | R1 | FP | Command greps `^A` only, so untracked siblings cannot appear; L289 expected text already says the rest stays untracked |
| Post-commit `git status` will still show `?? docs/superpowers/` for siblings | R1 | R1 | FP | L286-289 expected wording already states the rest of docs/superpowers/ stays untracked |
| grep for submit-now phrasing is case-sensitive | R1 | R1 | FP | Plan L215 uses `grep -Eic` (case-insensitive) for the submit-now check |

## Amendment note (spec-side, from plan FCL r1)

The spec's Gate 1 boundary note paraphrased the template's age item; corrected to verbatim "Has been around for at least 30 days" alongside the plan fix. Advisory-grade quote-accuracy fix; spec already converged Track 1 r1 — amendment recorded here for audit.

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Task 2 order consistency (title/scope → A-E) | saboteur, new_hire | MAJ (promoted) | FP | Verified: Task 2 block orders title/scope first, then A-E; matches AC1 (Round 1) |
| Stale as-of date if execution slips | saboteur | MAJ (promoted) | Design | Dated snapshot is the spec's stated design; runbook orders live re-verify (Round 1) |
| Section B quote/URL formatting ambiguity | new_hire | ADV | Advisory-skipped | AC5 governs; inline URLs already in block (Round 1) |

Fixes applied: 0
Inflation rate: 67% (2 of 3 findings FP/Design)
Validation: SKIP (docs-only)

## Converged: Round 1

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 1  |  Total fixes: 0
Document is ready.
