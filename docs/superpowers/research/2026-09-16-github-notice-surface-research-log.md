# Research round log: github-notice-surface

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| SC1 submission requirements (PR title, 4 PR reviews, 30-day age, unicorn comment, awesome-lint, duplicate check, slug, readme.md Contents) | R1 | R1 | Established | Multi primary: create-list.md, digger PR template, contributing.md |
| SC2 duplicate check: no v2-specific awesome list besides ours | R1 | R1 | Established | Digger GitHub search is primary; v1 sibling mycr0ft/awesome-sysml is not a duplicate |
| SC2 sibling: mycr0ft/awesome-sysml exists (5 stars, v1-focused) | R1 | R1 | Established | Digger GitHub search primary; relevant context, not a blocker |
| SC2 Awesome-MBSE-Engineer-Interview-QA unrelated | R1 | R1 | Established | Digger search primary; topic mismatch confirmed |
| SC3 pitfall: PRs temporarily disabled, ~89-90 open add-PRs backlog | R1 | R1 | Established | Skeptic primaries; current-state blocker for immediate submission |
| SC3 pitfall: AI-generated lists hard-rejected (#4093) | R1 | R1 | Established | Skeptic primary issue evidence |
| SC3 pitfall: low-effort immediate close, curation bar, no archived items, tight scope | R1 | R1 | Established | Skeptic primaries cluster |
| SC4 niche fit: no SysML/MBSE section on main readme; MBSE discovery via Gaphor/Open-MBEE hubs | R1 | R1 | Provisional | Skeptic secondary only; fit judgment the spec carries |
| Absence claims: no stars threshold, no personal-project rejection wording, no SysML decline precedent | R1 | R1 | Provisional | Named absences; closed-PR corpus gap noted |

## Round 1

Round 1 merged nine claim families across scout, digger, and skeptic sources. SC1 (submission requirements) and SC2 (duplicate check) are established on primary evidence. SC3 (pitfalls) is an established cluster: PRs are currently disabled with a large backlog, AI-generated lists are hard-rejected per issue 4093, and the curation bar is strict. Niche fit stays provisional because it rests on secondary sources and is a judgment the spec already carries. Three absence claims (stars threshold, personal-project wording, SysML decline precedent) stay provisional with the closed-PR corpus named as the gap. No claims were contradicted and no source rot was found. Verdict: RESEARCH_COMPLETE.

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| Submission requirements (30-day age, 4-PR review, unicorn, lint, slug, duplicate) (SC1) | scout, digger | EST | Resourced (Round 1) |
| Duplicate check: v1 sibling exists, no v2 duplicate (SC2) | digger | EST | Resourced (Round 1) |
| Pitfalls: PRs disabled, ~90 backlog, AI hard-reject, effort bar, curation bar (SC3) | skeptic | EST cluster | Resourced (Round 1) |
| Niche fit: no MBSE section on main readme; discovery lives in MBSE ecosystem | skeptic | PROV | Named (Round 1) |
| Absence claims: no stars gate, no personal-project wording, no SysML decline precedent | skeptic | PROV | Named (Round 1) |

Fixes applied: 0
Coverage: 3/3 criteria met
Validation: PASS

## Converged: Round 1

Track 3: diminishing-return halt. Predicate: brief-covered. All criteria met with ESTABLISHED decision-bearing claims; provisionals are absence claims and fit judgments, named in Synthesis.
Total rounds: 1  |  Total fixes: 0
Document is ready.
