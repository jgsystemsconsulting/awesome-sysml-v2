# Research: link-ops-no-spam-pr-path (P7)

## Research brief

- **Primary question**: How should the repo add a PR-time lychee link check (soft, visible) and a documented local link check, and de-duplicate the weekly Link Checker Report issue — using official lychee-action behavior?
- **Sub-questions**:
  1. lycheeverse/lychee-action v2: official inputs (args, fail, output, token), outputs (exit_code), behavior on pull_request events, recommended PR usage.
  2. lychee CLI: install methods for local contributors (primary install section), exit-code semantics, token/rate-limit flags.
  3. Pitfalls: rate limiting on shared runners, flaky third-party URLs, soft-fail patterns, issue-report formats.
- **Success criteria**: SC1 lychee-action inputs/outputs from the action's own README (primary). SC2 local install path from lychee's primary docs. SC3 pitfalls surfaced.
- **Out of scope**: whether to add a PR check (decided, P7); freshness job (done, P6); lint gate (done, P8).
- **Budget**: 1 round target; cap 3.

## Findings

Decision-bearing (retrieved 2026-09-16):

- **Action contract (SC1, ESTABLISHED)**: lycheeverse/lychee-action exposes inputs `args`, `fail`, `output`, `token`, `lycheeVersion` (default pins lychee v0.24.2), and a single output `exit_code` ("The exit code returned from Lychee"). The `fail` input controls whether a nonzero lychee exit fails the workflow; the documented soft-fail + issue pattern is `if: steps.lychee.outputs.exit_code != 0`. Corroborated by scout + digger independent fetches of action.yml and README.
- **Local install (SC2, ESTABLISHED)**: lychee distributes per-platform via package managers — scoop/winget/choco (Windows), brew/port (macOS), pacman/zypper/snap/apk (Linux); there is no npm/pip package. Current release lychee-v0.24.2. Single primary (lychee README install section, digger), named here.
- **Pitfalls (SC3, ESTABLISHED cluster)**: GitHub rate limits are aggressive (60/h unauthenticated; Actions GITHUB_TOKEN 1,000/repo/h); lychee's documented mitigation is the `GITHUB_TOKEN` env var or `--github-token`. 429 is not in lychee's default accepted statuses (`--accept '200..=204, 429'` pattern exists); transient timeouts and GitHub-URL flakes have open issues (#2053, #2027, action#138). `peter-evans/create-issue-from-file` cannot dedupe by title (only an explicit `issue-number` input), so the repo's gh list/edit/create upsert pattern is the correct dedupe mechanism; naive title search carries `in:title`/phrase pitfalls. The action's own sample is cron + issue creation; contributor-friction concerns for PR link checks are documented upstream (action#238), with the credible split being "fail PRs only for newly introduced broken links; issues for links that die later" (action#134).

## Synthesis

SC1 sources: action.yml (digger) + README (scout) — independent fetches, same primary repo, both list the same inputs/outputs; corroborated. SC2: single primary (lychee install docs), named here as provisional-grade but decision-sufficient (the spec only needs one documented local path per platform family). SC3: multi-source primary cluster. Open items named and non-blocking: no primary source on create-issue-from-file concurrent double-create (absence claim); publish-date fields absent from registry-style endpoints (n/a here). Design consequences for the spec: (1) the PR-time check stays SOFT (exit_code surfaced, no hard merge gate) per a-04 and the upstream friction evidence; (2) the local runbook command documents the platform package-manager install plus `GITHUB_TOKEN` for GitHub links; (3) the weekly report dedupes via the stale.yml create-or-update pattern; (4) flake mitigation uses `--max-retries` and keeps `fail: false`. Sources table:

| URL | Class | Used for |
|-----|-------|----------|
| https://github.com/lycheeverse/lychee-action | primary | action surface |
| https://raw.githubusercontent.com/lycheeverse/lychee-action/master/action.yml | primary | inputs/outputs contract |
| https://github.com/lycheeverse/lychee-action/blob/master/README.md | primary | fail input, soft-fail pattern, cache mitigation |
| https://github.com/lycheeverse/lychee | primary | CLI README: token env, rate flags, install methods |
| https://github.com/lycheeverse/lychee/releases/latest | primary | current release lychee-v0.24.2 |
| https://raw.githubusercontent.com/lycheeverse/lychee/master/docs/TROUBLESHOOTING.md | primary | rate-limit failure mode |
| https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api | primary | rate-limit numbers |
| https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests | primary | title search pitfalls |
| https://github.com/lycheeverse/lychee-action/issues/138 | primary | GitHub URL flake |
| https://github.com/lycheeverse/lychee-action/issues/238 | primary | contributor friction |
| https://github.com/lycheeverse/lychee-action/issues/134 | primary | fail-new-links split |
| https://github.com/lycheeverse/lychee/issues/2053 | primary | transient timeout flake |
| https://github.com/lycheeverse/lychee/issues/2027 | primary | backoff bug |
| https://github.com/peter-evans/create-issue-from-file | primary | no title dedupe |
| https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066 | secondary | (context: tag-retarget risk class) |
