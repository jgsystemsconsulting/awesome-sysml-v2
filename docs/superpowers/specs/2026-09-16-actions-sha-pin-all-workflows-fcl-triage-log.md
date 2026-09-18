# FCL triage log: 2026-09-16-actions-sha-pin-all-workflows

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| M1: Spec cites nonexistent CISA alert AA25-079A and attributes tag-rewrite and SHA-only-survival claims to it | R1 | R1 | Genuine | CISA's March 2025 tj-actions alert (already in the Research list) carries no AA ID; the attribution is fabricated. Fix covers the same-paragraph advisories: attribute the mechanism to wiz.io/Unit42, add the Unit42 URL to Research, and hedge "only SHA-pinned consumers were unaffected" to match wiz.io's in-window caveat. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| CISA alert AA25-079A does not exist; attribution fabricated | skeptic | MAJ | Genuine | Fixed (Round 1) |

Fixes applied: 1
Inflation rate: 0% (0 of 1 CRITICAL+MAJOR findings triaged FP/Recurring/Design)
Validation: SKIP (no associated script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| L9 CISA identifier + attribution (confirmation wave) | skeptic, source, correspondent | - | Confirmed | Resolved by this change (Round 2) |
| Research-list Unit42 URL (confirmation wave) | skeptic, source, correspondent | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 1
Document is ready.
