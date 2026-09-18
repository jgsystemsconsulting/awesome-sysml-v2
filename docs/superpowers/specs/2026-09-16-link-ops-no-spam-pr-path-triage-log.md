# ARL triage log: 2026-09-16-link-ops-no-spam-pr-path

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| M1 edit path never restores labels (spec.md:L82-84) | R1 | R1 | Genuine | gh issue edit --body-file updates body only; AC2 requires report + broken-links labels, fix adds --add-label flags to edit branch and Exact-after block |
| M2 nested fence rendering broken in D3 block (spec.md:L143-154) | R1 | R1 | Genuine | Inner triple-backtick fence closes outer fence early; promoted from advisory to major because rendered example is the implementation reference; fix uses four-backtick outer fence |
| A2 paths filter limits link-check scan scope (saboteur) | R1 | R1 | Design | Full-repo scan is intentional for a link-check advisory; WONTFIX, filter would hide broken links outside filtered paths |
| A2 paths filter re-raised by auditor, same loc | R1 | R1 | Advisory-skipped | Duplicate of design row above; no fix needed, skipping avoids log bloat |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Edit path never restores labels on legacy label-less report issues | saboteur | MAJ | Genuine | Fixed (Round 1): --add-label on edit branch, mirrored in Exact-after |
| D3 nested fence renders split | saboteur, auditor | MAJ (promoted) | Genuine | Fixed (Round 1): four-backtick outer fence |
| Unfiltered pull_request trigger cost | saboteur | ADV | Design | Full-repo advisory scan intentional; soft gate unchanged (Round 1) |

Fixes applied: 2
Inflation rate: 25% (1 of 4 findings triaged Design)
Validation: SKIP (no associated script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (label restore x2, four-backtick fence) | saboteur, new_hire, auditor | - | Confirmed | Resolved by this change (Round 2) |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (no associated script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 2
Document is ready.
