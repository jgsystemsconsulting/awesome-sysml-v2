# Research round log: pr-lint-gate-surface

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| awesome-lint dist-tags latest = 2.3.0 | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Registry primary (digger) corroborated by scout github package.json showing same version |
| awesome-lint 2.3.0 engines node >=20 | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Two primary sources agree: registry version endpoint and github package.json |
| awesome-lint actively maintained (commits through 2026-07, 2.3.0 in 2026-04, CI on node 20+24) | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Commits page plus main.yml workflow, two primary sources |
| npx pkg@specifier matches exact name+version only, installs to npm cache | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Both citations are docs.npmjs.com (npx and npm-exec), one doc family, counts as single primary |
| Top-level pin does not lock caret transitives (remark ^15) | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (skeptic package.json read) |
| Pin freezes FP fixes; FP classes exist (#204, #218, #224, v2.2.2 spell-check fix) | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Multiple primary GitHub issue and release URLs support the cluster |
| Upstream norm is unpinned npx awesome-lint + fetch-depth: 0 | r1 2026-09-16 | r1 2026-09-16 | ESTABLISHED | Two primary sources: awesome repo_linter.sh and awesome-lint readme |
| v2.0.0 required Node 20, coupling gate to runtime | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (release page) |
| Lockfile gives CI identical dependency trees | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Single primary source (npm docs) |
| No primary source on markdownlint double-lint collisions | r1 2026-09-16 | r1 2026-09-16 | PROVISIONAL | Absence claim with no source; unverifiable, treat as unconfirmed |

## Round 1

Merged 10 claims from digger, scout, and skeptic agents. SC1 is resolved: awesome-lint latest is 2.3.0 per the npm registry, corroborated by the GitHub package.json, and it requires Node >=20, so a pinned gate needs a Node 20+ runner. SC2 is provisionally resolved: npm docs state npx pkg@specifier matches an exact name and version and installs into the npm cache, but both citations come from one doc family, so the pin mechanics stay PROVISIONAL pending a second independent source. SC3 is supported by an established cluster of FP evidence (issues #204, #218, #224, and the v2.2.2 spell-check fix), which argues against pinning since pins freeze FP fixes; the upstream norm of unpinned npx with fetch-depth 0 is established from two primary sources. Single-source claims (caret transitives, v2.0.0 Node 20 break, lockfile CI guarantees, markdownlint collision absence) remain PROVISIONAL. Three fetch fails were recorded, none affecting claims 1 through 9. Decision-bearing coverage is met; verdict RESEARCH_COMPLETE.

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| awesome-lint latest = 2.3.0 (registry dist-tags) | digger | EST | Resourced (Round 1) |
| 2.3.0 engines node >=20; active project | digger, scout, skeptic | EST | Resourced (Round 1) |
| npx pkg@specifier: exact-match, cache install | scout, skeptic | EST | Resourced (Round 1) |
| Pin does not lock caret transitives; FP classes exist upstream | skeptic | PROV (named in Synthesis) | Resourced (Round 1) |
| Upstream norm unpinned + fetch-depth 0; lockfile guarantee | skeptic | PROV (named in Synthesis) | Resourced (Round 1) |

Fixes applied: 0
Coverage: 3/3 criteria met
Validation: PASS

## Converged: Round 1

Track 1: Merged verdict RESEARCH_COMPLETE.
Total rounds: 1  |  Total fixes: 0
Document is ready.
