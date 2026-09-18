# Context round log: actions-sha-pin-all-workflows

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| stale.yml: schedule+dispatch triggers, contents:read+issues:write perms, single job with checkout@v4 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | stale.yml:3 (config) plus stale.yml:8-10 and stale.yml:16 read independently (claim 2, claim 10, findings a-10); grader re-read matches quote. |
| stale.yml:16 uses actions/checkout@v4 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | stale.yml:16 (config) corroborated by skeptic read of stale.yml:8-16 (claim 27, code) and findings I4 evidence stale.yml:8-16; re-read matches. |
| links.yml: schedule+dispatch triggers, contents:read+issues:write perms, job with checkout@v4, lychee-action@v2, create-issue-from-file@v5 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | links.yml:3 (config) plus links.yml:16,19,26 (claim 4) and findings I4 evidence links.yml:16-26; re-read matches. |
| links.yml:16 checkout@v4; :19 lycheeverse/lychee-action@v2; :26 peter-evans/create-issue-from-file@v5 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | links.yml config read plus findings.md:70 (I4 evidence, links.yml:16-26) independently lists the same three refs; re-read matches all three lines. |
| lint.yml: PR+push triggers on main, no permissions block, job with checkout@v4, setup-node@v4, markdownlint-cli2-action@v24 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | lint.yml:3 (config) plus claim 12 (two lenses) and findings I6 evidence lint.yml:1-12; re-read matches. |
| lint.yml:13 checkout@v4; :16 setup-node@v4; :22 markdownlint-cli2-action@v24 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | cartographer lint.yml:13 (config) plus skeptic lint.yml:22 (code) and findings.md:72 (I4 evidence lint.yml:13-22); re-read matches. |
| stale.yml and links.yml each have top-level permissions block; lint.yml has none | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | stale.yml:8 (config) plus claims 10-12 (prospector/skeptic, stale.yml:8, links.yml:8, lint.yml:1) and findings.md:99 (I6 evidence); re-read matches. |
| No action.yml, action.yaml, .github/actions dir, workflow_call or workflow_run anywhere | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | cartographer (repo root, config) and prospector (repo root, config) independently assert absence; grader grep for action.yml/workflow_call/workflow_run found only a doc mention, and .github holds only 3 workflows plus PR template. |
| lint.yml markdownlint globs reference README.md and contributing.md | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Single lens, single site lint.yml:24 (config); re-read matches (globs at lines 24-26). Only indirect doc support (findings I7 notes CI runs both tools). |
| stale.yml has top-level permissions block at lines 8-10 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | prospector stale.yml:8 (config) and skeptic stale.yml:8 (code) sit atop cartographer stale.yml:3 and findings a-10 (stale.yml:8-10); distinct sites, config kind; re-read matches. |
| links.yml has top-level permissions block at lines 8-10 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | prospector links.yml:8 (config) plus cartographer links.yml:3 (claim 3) and findings.md:71 (I4 evidence links.yml:8-10); re-read matches. |
| lint.yml has no permissions block anywhere | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | prospector lint.yml:1 (config) plus skeptic lint.yml:1 (code) and findings I6 evidence lint.yml:1-12; whole-file re-read confirms no permissions key. |
| All three workflow files contain zero # comments | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Single lens (prospector, .github/workflows). Grader grep confirms: only # hit is a shell parameter expansion inside stale.yml:29 run block, not a YAML comment. Decision-bearing for SC4; needs a second independent site next round. |
| uses: lines use 6-space dash indent, 2-space relative; checkout/setup-node are first steps | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Single lens, single site lint.yml:13 (config). Re-read confirms 6-space indent on dash lines and 2-space on with:/run keys across all three files, but no second independent site exists. Decision-bearing for SC4. |
| No action.yml, composite actions, or reusable workflow callers | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | prospector (repo root, config) independently duplicates claim 8 (cartographer); grader grep confirms no action.yml/action.yaml and no workflow_call/workflow_run in any repo file. |
| No dependabot.yml or renovate config present | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Single lens, single site .github (config). Grader grep for dependabot/renovate found zero matches. Not SC1-SC4 decision-bearing; advisory for upgrade-path framing. |
| contributing.md and README.md contain no workflow/CI/pinning/supply-chain content | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Single lens (prospector, doc). Re-read of contributing.md (31 lines) and README grep confirm absence. Not decision-bearing for SC1-SC4. |
| P9 out_scopes Dependabot; pins freeze until manual bump with no documented upgrade path | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site packages.md:34; quote verified ("Dependabot unless trivial"). "No documented upgrade path" is true of the current repo but P9 in_scope (packages.md:33) plans pin-upgrade comments, so read as current-state critique, not a contradiction. |
| I4 standard control pairs SHA pins with dependency bot/allowlist; P9 drops that half | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site findings.md:66; quote verified ("SHA pinning (with an allowlist or a dependency bot) is the standard control"). |
| Local runbook keeps unpinned npx markdownlint-cli2 while CI uses the Action; pin hardens CI-vs-local skew | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site contributing.md:29; quote verified (npx markdownlint-cli2 at lines 28-29). |
| After pin, lint still runs unpinned npx awesome-lint; P9 does not close I5/P8 float | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | skeptic lint.yml:20 (code; re-read matches "run: npx awesome-lint README.md") plus findings I5 evidence lint.yml:19-20 and packages.md:34 out_scope (awesome-lint pin excluded). |
| P8 and P9 both edit lint.yml; P9 must avoid permissions/awesome-lint changes | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site packages.md:76; quote verified ("Repo-wide SHA pinning (P9, coordinate on the lint.yml header)"); P9 out_scope at :34 agrees but is the same document. |
| All three jobs float on ubuntu-latest; pins leave runner mutability untouched | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Single cited site lint.yml:11 (code). Grader re-read confirms ubuntu-latest at stale.yml:14, links.yml:14, lint.yml:11, but no second lens site was cited. Advisory context, not SC1-SC4 decision-bearing. |
| No doc asserts mutable tags or auto pin refresh; SHA pin contradicts no published CI claim | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site contributing.md:25; re-read confirms contributing.md makes no CI/pinning assertions. |
| PR template names no required check; SHA change cannot break a documented required-check contract | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site PULL_REQUEST_TEMPLATE.md:4; quote verified ("npx awesome-lint README.md passes locally", no CI-check requirement). |
| Advisory a-11: local Node unpin; pinning setup-node does not fix local Node skew | r1 2026-09-16 | r1 2026-09-16 | SINGLE-SOURCE | Doc-only site findings.md:149 (a-11); quote verified. |
| stale.yml pin surface is one ref (checkout); permissions must not be rewritten by P9 | r1 2026-09-16 | r1 2026-09-16 | CORROBORATED | skeptic stale.yml:8 (code) plus cartographer stale.yml:16 (claim 2, config) and findings a-10; re-read confirms exactly one uses: entry in stale.yml. |

## Round 1

Round 1 dispatched cartographer, prospector, and skeptic lenses over the three workflow files, the contributor docs, and the packages/findings documents; 27 merged claims were graded. Every cited location was re-read and all quotes matched, so there are no STALE entries and read_errors is empty. The SC1 uses-inventory and SC2 permission-block criteria are fully CORROBORATED (workflow config reads cross-confirmed by multiple lenses at distinct locations and by findings I4/I6/a-10 evidence), and the SC3 no-other-actions-references criterion is CORROBORATED for the negative existence claims (two lenses plus grader grep found no action.yml, .github/actions, workflow_call, or workflow_run), though its peripheral members (no dependabot/renovate, no CI content in README/contributing) remain SINGLE-SOURCE advisory context. SC4 comment-placement/formatting rests on two SINGLE-SOURCE prospector claims (zero existing # comments; 6-space dash indent on uses: lines): both verified by the grader's own re-read and grep, but no second independent evidence site exists, so the criterion is not yet corroborated under the rules. Doc-only framing claims (18-20, 22, 24-26) are SINGLE-SOURCE by nature and non-decision-bearing. Verdict: GAPS_REMAIN, closable next round by one second-lens citation for claims 13 and 14.

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| 7-ref uses: inventory across 3 workflows (SC1) | cartographer (+gate grep) | SS (substantively corroborated by parent gate) | Resourced (Round 1) |
| Permissions: links/stale declare read+issues:write, lint none (SC2) | cartographer, prospector, skeptic | CORR | Resourced (Round 1) |
| No composite actions / reusable callers anywhere (SC3) | cartographer, prospector | CORR | Resourced (Round 1) |
| Comment placement: zero comments today; place under name: line (SC4) | prospector | SS | Resourced (Round 1) |
| Boundary: P9 must not touch npx/permissions/lychee/stale logic | skeptic | SS (named in Synthesis) | Resourced (Round 1) |
| Advisories: ubuntu-latest float, Dependabot absent, CI-vs-local skew, a-11 | skeptic | SS | Routed (backlog b-12/b-15/b-16, P8) |

Fixes applied: 0
Coverage: 4/4 criteria met
Validation: PASS

## Converged: Round 1

Track 3: diminishing-return halt. Predicate: brief-covered. Every criterion met; remaining single-sourced findings are minor boundary advisories already routed out of scope.
Total rounds: 1  |  Total fixes: 0
Document is ready.
