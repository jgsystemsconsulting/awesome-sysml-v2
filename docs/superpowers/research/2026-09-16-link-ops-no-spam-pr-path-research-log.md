# Research round log: link-ops-no-spam-pr-path

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| lychee-action official; inputs args/fail/output/token/lycheeVersion; output exit_code; fail controls workflow failure (SC1) | R1 | R1 | ESTABLISHED | Two primary fetches of action.yml plus README in the same repo; primary plus corroborating |
| Soft-fail plus issue-creation pattern `if: steps.lychee.outputs.exit_code != 0` documented (SC1) | R1 | R1 | ESTABLISHED | README primary plus local repo fact: links.yml already uses this pattern |
| lychee current release lychee-v0.24.2; action default lycheeVersion v0.24.2 (supporting) | R1 | R1 | PROVISIONAL | Single primary (releases page); version moves, recheck at install time |
| Local install methods per platform: scoop/winget/choco/brew/pacman; no npm (SC2) | R1 | R1 | PROVISIONAL | Single primary (lychee README); no second source fetched |
| Rate limits: unauth 60/h; Actions GITHUB_TOKEN 1000/repo/h; mitigation GITHUB_TOKEN env or --github-token (SC3) | R1 | R1 | ESTABLISHED | docs.github.com plus lychee README plus TROUBLESHOOTING, independent primaries |
| 429 not in default accept; --accept 429 pattern; timeout and transient flake issues #2053 #2027 action#138 (SC3) | R1 | R1 | ESTABLISHED | Multiple primary issue threads plus docs |
| create-issue-from-file cannot dedupe by title, only issue-number input; naive gh title search has in:title/phrase pitfalls (SC3) | R1 | R1 | ESTABLISHED | Action README primary plus docs.github search semantics |
| cron plus issue is the official sample pattern; PR-link-check friction documented (action#238; #134 fail-only-new-links split) (SC3) | R1 | R1 | ESTABLISHED | Primary issues in the action and lychee repos |
| Absence: no primary source on create-issue-from-file concurrent double-create behavior | R1 | R1 | GAP-NOTE | Recorded source gap, not a graded claim |

## Round 1

Scout and skeptic runs merged without contradictions. The SC1 cluster (action inputs, exit_code output, fail input, soft-fail issue pattern) is established from two independent primary fetches plus a local repo fact, so the workflow contract is safe to build on. The SC3 pitfalls cluster is established across docs.github.com, the lychee README, TROUBLESHOOTING, and primary issue threads: rate limits, 429 acceptance, transient flakes, issue-dedup limits, and the cron-plus-issue sample pattern. Two items stay provisional. The pinned version v0.24.2 rests on one releases page and should be rechecked at install time. The SC2 local-install method list rests on the lychee README alone; a second source would confirm the no-npm claim. One recorded gap: no primary source covers whether create-issue-from-file can double-create issues under concurrent runs. Four fetch fails were logged (lychee.cli.rs 404 twice, rust-lang 404, two issue-comment gaps); none affects claims 1 through 8.

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| Action contract: inputs/exit_code/fail (SC1) | scout, digger | EST | Resourced (Round 1) |
| Local install per platform, no npm (SC2) | digger | EST (single primary, named) | Resourced (Round 1) |
| Rate limits + token mitigation; 429/timeouts; dedupe limits; friction dissent (SC3) | skeptic | EST cluster | Resourced (Round 1) |
| Absence: concurrent double-create docs | skeptic | PROV | Named (Round 1) |

Fixes applied: 0
Coverage: 3/3 criteria met
Validation: PASS

## Converged: Round 1

Track 3: diminishing-return halt. Predicate: brief-covered. All criteria met; remaining provisionals are absence claims and single-primary install docs, named in Synthesis.
Total rounds: 1  |  Total fixes: 0
Document is ready.
