# Research round log: actions-sha-pin-all-workflows

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Full-length commit SHA is the only immutable release method | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Scout and skeptic both cite the same docs.github.com security-hardening page; same-document sourcing is not independent, so effectively a single primary doc. |
| Refs API resolves tags/<tag> format | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (scout, GitHub REST docs); supporting claim. |
| Commits API accepts tag names | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (scout, GitHub REST docs); supporting claim. |
| checkout v4 -> 11d5960a326750d5838078e36cf38b85af677262, lightweight tag | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Digger (commits endpoint) and skeptic (refs/tags endpoint) are independent retrieval paths over the primary api.github.com data; both agree. Decision-bearing (SC1/SC2). |
| setup-node v4 -> 49933ea5288caeca8642d1e84afbd3f7d6820020 | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Digger only for the SHA value; skeptic's refs check on this action was reported in one grouped claim and did not independently confirm the hash. Decision-bearing. |
| lychee-action v2 -> e7477775783ea5526144ba13e8db5eec57747ce8 | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Digger only for the SHA value; skeptic's refs check grouped with two other actions, no independent hash confirmation. Decision-bearing. |
| create-issue-from-file v5 -> e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Digger only for the SHA value; skeptic's refs check grouped, no independent hash confirmation. Decision-bearing. |
| markdownlint-cli2-action v24 -> 21c1be1b93ad9ed58fa840aacc3f279cde2a72ff (peeled; annotated tag object 28a7e8bdb81fd8ad675883de92c758ab78e0ce10) | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Digger (commits endpoint) and skeptic (annotated-tag peel via refs API) independently agree on the peeled commit. Decision-bearing (SC1/SC2). |
| markdownlint v24 tag is annotated (object.type=tag) | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (skeptic, refs API); supporting claim. |
| setup-node/lychee/create-issue-from-file v-tags are lightweight | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Skeptic single grouped check against refs API; grouped reporting weakens per-action attribution. Supporting claim. |
| tj-actions Mar 2025 tag-retarget attack; hash-pinned consumers unaffected | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single secondary source (wiz.io). |
| Attackers rewrote existing tags | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single secondary source (wiz.io). |
| reviewdog to tj-actions attack chain; full SHA pin as mitigation | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single secondary source (unit42). |
| CISA remediation pins a specific commit | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (cisa.gov). |
| Dependabot will not create alerts for SHA-pinned actions | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (docs.github.com). |
| Maintenance burden dissent | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single secondary source (stepsecurity). |
| Renovate disables bare-SHA pins without version comment | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (docs.renovatebot.com). |
| Annotated tags are checksummed objects | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (git-scm). |
| Enterprise policy can mandate SHA pins | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (docs.github.com). |
| Immutable Actions roadmap closed not planned | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (github/roadmap#592). |
| Pin is point-in-time; automerge drift risk | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (securitylab). |
| No 2025-2026 compromise of the five target actions found | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Absence claim by skeptic with no direct source; absence of evidence only. |
| No primary source on whether uses: rejects vs peels annotated tag-object SHAs | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Absence claim, no direct source; remains an open question for synthesis. |
| setup-node v4 -> 49933ea5288caeca8642d1e84afbd3f7d6820020 | r1 2026-09-16 | r2 2026-09-16 | ESTABLISHED | 3 independent primary retrieval paths — commits API, refs API, releases page; SHAs match. |
| lychee-action v2 -> e7477775783ea5526144ba13e8db5eec57747ce8 | r1 2026-09-16 | r2 2026-09-16 | ESTABLISHED | 3 independent primary retrieval paths — commits API, refs API, releases page; SHAs match. |
| create-issue-from-file v5 -> e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd | r1 2026-09-16 | r2 2026-09-16 | ESTABLISHED | 3 independent primary retrieval paths — commits API, refs API, releases page; SHAs match. |

## Round 1

Round 1 retrieved all five target SHA resolutions plus the supporting pitfall landscape, so nominal coverage is complete (SC1-SC3 addressed). Grade quality is uneven: only checkout v4 and markdownlint-cli2-action v24 reach ESTABLISHED, because the digger's commits-endpoint lookup and the skeptic's refs/tags-endpoint lookup independently agreed on those two. For setup-node, lychee-action, and create-issue-from-file, only the digger confirmed the hash; the skeptic's refs checks for those three arrived as one grouped claim and cannot serve as per-action corroboration, leaving three decision-bearing SHAs PROVISIONAL. The immutability claim is likewise PROVISIONAL because scout and skeptic cited the identical docs.github.com page, which the rules treat as a single source. The 8 fetch_fails were skeptic URL probes referencing none of claims 1-21, so no SOURCE-ROT rows. Two absence claims (no recent compromise of the target actions; no primary doc on uses: handling of annotated tag-object SHAs) stay PROVISIONAL and should be framed as open questions unless a later round finds direct evidence. Next round should re-verify the three uncorroborated hashes via independent refs/tags lookups; absent that, the synthesis must present them as single-source values.

## Round 2

The round-1 gap slice was the three single-source SHA claims (setup-node v4, lychee-action v2, create-issue-from-file v5). A wave of three lenses ran: the scout honestly reported zero new findings, the digger re-resolved each tag through the refs API, and the skeptic pulled each action's releases page. Each of the three claims gained two new independent primary sources whose SHAs match the round-1 digger values exactly, giving three independent primary retrieval paths (commits API, refs API, releases page) per claim; all three re-grade ESTABLISHED. No CONTRADICTED or SOURCE-ROT rows exist, no fetch_fails touch any claim, and every decision-bearing SHA claim (checkout v4, markdownlint-cli2 v24, setup-node v4, lychee-action v2, create-issue-from-file v5) is now ESTABLISHED, so the verdict is RESEARCH_COMPLETE rather than CONTRADICTIONS_OPEN or GAPS_REMAIN. No TRIAGE_ABORTED condition arose: the log read and wrote cleanly. The two absence claims remain PROVISIONAL by nature and are handed to synthesis as open questions, which the rules permit under RESEARCH_COMPLETE.

## Round 2 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| setup-node v4 → 49933ea5288caeca8642d1e84afbd3f7d6820020 | digger, skeptic | EST | Resourced (Round 2) |
| lychee-action v2 → e7477775783ea5526144ba13e8db5eec57747ce8 | digger, skeptic | EST | Resourced (Round 2) |
| create-issue-from-file v5 → e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd | digger, skeptic | EST | Resourced (Round 2) |
| Landscape/method (scout) | scout | - | Honest zero (Round 2) |

Fixes applied: 0
Coverage: 3/3 criteria met
Validation: PASS

## Converged: Round 2

Track 1: Merged verdict RESEARCH_COMPLETE.
Total rounds: 2  |  Total fixes: 0
Document is ready.
