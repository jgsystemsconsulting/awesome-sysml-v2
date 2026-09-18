# ARL triage log: 2026-09-16-community-root-meta

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| CoC source unpinned (saboteur M1 L60 + new_hire M1 L56-65, 2 lenses, promoted CRITICAL) | R1 | R1 | Genuine | Spec demands CC 2.1 short-form verbatim but no stable URL publishes that text; no research gate. Fix: use full CC 2.1 from canonical URL with contact line filled |
| Security channel unverified (saboteur M2 L73) | R1 | R1 | Genuine | SECURITY.md points at private vulnerability reporting but repo setting never checked or enabled; no AC covers it |
| Scope AC1 outside docs/superpowers/ (A1) | R1 | R1 | Advisory-skipped | Cheap clarity fix: restrict AC1 scope to exclude pipeline docs appearing in git status |
| CoC contact mechanism wording (A2) | R1 | R1 | Advisory-skipped | Profile page is not a report mechanism; point conduct reports at GitHub issues with explicit instruction |
| Run-set accounting prose P2-through-P9 vs actual set incl. P3 (A3) | R1 | R1 | Advisory-skipped | Minor prose mismatch; restate done set accurately if touched, otherwise skip |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| CoC "2.1 short-form verbatim" unpinned: no stable short-form 2.1 template exists at a URL | saboteur, new_hire | CRITICAL (promoted) | Genuine | Fixed (Round 1): full CC 2.1 verbatim from canonical URL; implementer fetches and embeds |
| SECURITY.md report path (private vulnerability reporting) never enabled/verified | saboteur | MAJ | Genuine | Fixed (Round 1): design step + AC7 check/enable via gh api |
| AC1 git-status scope vs pipeline docs | saboteur | ADV | Advisory-skipped | Note added: scope outside docs/superpowers/ (Round 1) |
| CoC contact line is a page, not a mechanism | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: repo issue or profile instruction (Round 1) |
| Run-set accounting prose (P2-through-P9 vs actual set incl. P3) | auditor, saboteur | ADV | Advisory-skipped | Covered by spec's own run references; ledger records the done set (Round 1) |
| CC 2.1 section naming (Our Responsibilities vs Enforcement Responsibilities) | new_hire | ADV | Advisory-skipped | Moot with full-text verbatim decision (Round 1) |

Fixes applied: 2 genuine CRITICAL/MAJOR families + advisory folds
Inflation rate: 0% (0 findings triaged FP/Design)
Validation: SKIP (file creation at execute; canonical fetch by implementer)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed families (full-text CoC, security enablement) — AC2/Non-goals remnants found | saboteur, new_hire, auditor | - | Confirmed + 2 remnants fixed | Resolved by this change (Round 2) |
| AC2 still said "short form" | saboteur | MAJ | Genuine | Fixed (Round 2): full verbatim text |
| Non-goals still excluded full-length Covenant | saboteur | ADV | Genuine | Fixed (Round 2) |

Fixes applied: 2 (1 MAJOR remnant, 1 advisory remnant)
Inflation rate: n/a (remnants of the Round 1 fix, not new findings)
Validation: SKIP (docs-only)

## Converged: Round 3

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 3 (cap)  |  Total fixes: 9
Document is ready.
