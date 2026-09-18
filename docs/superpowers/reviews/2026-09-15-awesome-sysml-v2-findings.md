---
date: 2026-09-15
project: awesome-sysml-v2
mode: light
rounds: 1
slice: []
input_digest: 781bed1188aa1f09322c40fc08d0d1ec37adda37def37537b054d006d9919f42
open_objections: []
---

# Repository findings: awesome-sysml-v2

Light-mode review, one round, four lenses (rot, defect, guard, operate) over the whole repository. Eleven raw issues merged to eight findings. Triage kept all eight, downgraded one from HIGH to MEDIUM, and escalated no conflicts. Every finding lives in the CI workflows and contributor-workflow surface; the README entry list itself came back clean.

## I1: freshness-window-mismatch

Severity: MEDIUM. Corroboration: 3 lenses (rot, defect, operate). Deps: I3.

contributing.md criterion 4 admits entries with a commit within 24 months (or foundational value), but the Freshness workflow computes its cutoff at 12 months and its report header says "no push in over 12 months", so the monthly automation flags policy-compliant entries as overdue. Maintainers acting on the report can nag or remove entries that still meet the written bar, and contributors have no single authoritative window when triaging stale items or defending a PR. The published policy and the only freshness job must share one cutoff.

Evidence:

- `contributing.md:10`: "4. Active maintenance (commit within 24 months) or foundational value (formal specs, canonical reference repos)."
- `.github/workflows/stale.yml:22-24`: `cutoff=$(date -u -d "12 months ago" +%Y-%m-%dT%H:%M:%SZ)` followed by the "Entries with no push in over 12 months" header echo.
- `.github/workflows/stale.yml:32-33`: `if [[ "$pushed" < "$cutoff" ]]; then` reporting line.
- `.github/workflows/stale.yml:37-38`: "No entries exceeded the 12-month threshold."

Blast radius: false-positive freshness entries drive churn on projects that still satisfy the inclusion rules, disputed removals and PR arguments, and eroded trust in the only automated debt signal this list has. The ambiguity grows with list size.

## I2: link-report-issue-spam

Severity: MEDIUM. Corroboration: 2 lenses (rot, defect). Deps: none.

The Links workflow soft-fails lychee (`fail: false`) and, on any nonzero `exit_code`, always runs create-issue-from-file with a fixed title and no lookup or edit of an existing open report, while the sibling Freshness workflow in the same repository already implements create-or-update against one canonical issue. On the weekly cron, every broken-link run opens another "Link Checker Report" issue, fragmenting link-rot debt instead of converging on one living ledger. Lychee also runs only on schedule or manual dispatch: the PR/push path (lint.yml) never checks HTTP reachability, so criterion 1's stable-URL bar has no merge-time enforcement.

Evidence:

- `.github/workflows/links.yml:24-30`: the Create Issue From File step with fixed title "Link Checker Report".
- `.github/workflows/links.yml:17-30`: Link Checker step with `fail: false`.
- `.github/workflows/links.yml:3-6`: `on:` limited to `schedule` and `workflow_dispatch`.
- `.github/workflows/stale.yml:44-48`: the create-or-update contrast in the Freshness workflow.
- `contributing.md:7`: "1. Stable, reachable URL pointing at the project itself."
- `.github/workflows/lint.yml:3-7`: PR/push triggers that never run lychee.

Blast radius: broken-link debt multiplies as same-titled duplicate issues, maintainers lose a single place to track link rot, close-out work duplicates, and the weekly signal becomes noise. Meanwhile unreachable URLs can merge with a green Lint check until the next Monday cron.

## I3: stale-curl-set-e-aborts

Severity: MEDIUM (downgraded from HIGH by triage; see rationale below). Corroboration: 1 lens (defect). Deps: none.

The Freshness workflow enables `set -euo pipefail` and then fetches each README GitHub repo with `curl -sf` inside a command substitution. `-f` makes curl exit non-zero on HTTP 404/403 (deleted, renamed, private, or rate-limited repos), and under `set -e` that aborts the whole step before the later `[ -n "$pushed" ] || continue` skip can run. One dead or unreachable GitHub entry therefore fails the "Build freshness report" step entirely, skips "Create or update the issue", and leaves maintainers with no monthly report even for the repos that did respond. The continue branch only covers an empty `pushed_at`, not transport/API failure, so the error path the script appears to handle is effectively dead.

Evidence:

- `.github/workflows/stale.yml:21`: `set -euo pipefail`
- `.github/workflows/stale.yml:30-31`: `pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty")` followed by `[ -n "$pushed" ] || continue`

Blast radius: any single bad GitHub URL in README.md turns the scheduled Freshness report into a red workflow with no issue body update; stale-but-still-reachable projects go unreported until the hard failure is fixed by hand.

Triage downgrade rationale: the defect lives in a scheduled monthly reporting job (stale.yml:5), not a production or onboarding path. The failure is loud in the Actions log, produces no data loss, and blocks only an advisory freshness report.

## I4: actions-not-sha-pinned

Severity: MEDIUM. Corroboration: 1 lens (guard). Deps: none.

All three workflows pin Actions by mutable major tags (`@v4`, `@v2`, `@v5`, `@v24`) rather than commit SHAs. Scheduled jobs in links.yml and stale.yml grant `issues: write` and pass `GITHUB_TOKEN` into third-party actions (`lycheeverse/lychee-action`, `peter-evans/create-issue-from-file`). A tag move or compromised publisher release would run attacker-controlled code on the runner with that token scope. Official `actions/*` tags share the same mutability class even if lower likelihood. SHA pinning (with an allowlist or a dependency bot) is the standard control for this supply-chain surface.

Evidence:

- `.github/workflows/links.yml:16-26`: checkout@v4, lychee-action@v2, create-issue-from-file@v5 in the `issues: write` job.
- `.github/workflows/links.yml:8-10`: `permissions: contents: read, issues: write`.
- `.github/workflows/lint.yml:13-22`: checkout@v4, setup-node@v4, markdownlint-cli2-action@v24.
- `.github/workflows/stale.yml:8-16`: same permission pair and checkout@v4.

Blast radius: a compromised action tag on a scheduled or dispatched run can use GITHUB_TOKEN to create or edit issues (spam, social-engineering issue bodies) and read repo contents. No `contents: write` exists today, so this is not a direct push-to-main path, but it is live CI code execution under the workflow identity.

## I5: npx-awesome-lint-unpinned

Severity: MEDIUM. Corroboration: 1 lens (guard). Deps: I6.

The lint workflow runs `npx awesome-lint README.md` with no package.json, lockfile, or version argument, so every push and pull_request to main resolves and executes whatever `awesome-lint` currently is on the npm registry. That is an unpinned, network-fetched executable on the PR critical path. Unlike Actions SHA pins, there is no in-repo lock to review when the tool changes, and a compromised or typosquat-adjacent publish would execute inside the lint job on ubuntu-latest for contributor PRs and main pushes.

Evidence:

- `.github/workflows/lint.yml:19-20`: `run: npx awesome-lint README.md` with no version constraint.
- Repo tree: no package.json or lockfile exists anywhere in the repository.

Blast radius: a registry-side compromise or hostile latest publish of awesome-lint yields arbitrary code execution on CI runners for all PRs and main pushes. Impact scales with whatever GITHUB_TOKEN permissions the lint job effectively receives (see I6) and any future secrets attached to that workflow.

## I6: lint-yml-no-permissions

Severity: MEDIUM. Corroboration: 1 lens (guard). Deps: I5.

lint.yml is the only workflow without a top-level `permissions:` block. links.yml and stale.yml already least-privilege to `contents: read` and `issues: write`. Lint only needs contents read (checkout) and should set `permissions: contents: read` explicitly so the job does not inherit a broader repository or organization default GITHUB_TOKEN policy. Missing explicit permissions on the PR-triggered workflow that also runs unpinned `npx` widens the trust boundary for that supply-chain path.

Evidence:

- `.github/workflows/lint.yml:1-12`: no `permissions:` key between `on:` and `jobs:`.
- `.github/workflows/links.yml:8-10` and `.github/workflows/stale.yml:8-10`: both set explicit `permissions:` blocks.

Blast radius: if repository or organization default token permissions are broader than read-only, the lint job (including unpinned npx and unpinned actions) silently receives excess scopes (issue write, package write, or worse) without any workflow-local signal. Explicit permissions cap the blast from a compromised lint dependency.

## I7: pr-checklist-omits-markdownlint

Severity: MEDIUM. Corroboration: 1 lens (operate). Deps: none.

The contributor runbook requires both awesome-lint and markdownlint-cli2 before opening a PR, and CI runs both on every PR to main, but the PR template checklist only asks for awesome-lint. New contributors following the template alone will skip markdownlint, hit a red Lint workflow they were never told to run, and bounce on a preventable CI failure during first-time onboarding.

Evidence:

- `contributing.md:27-30`: both `npx awesome-lint README.md` and `npx markdownlint-cli2 "README.md" "contributing.md"`.
- `.github/PULL_REQUEST_TEMPLATE.md:4`: only "`npx awesome-lint README.md` passes locally".
- `.github/workflows/lint.yml:19-26`: CI runs both tools.

Blast radius: first-time PRs fail CI after the author believed the template checklist was complete; review cycles burn on lint the runbook already knew about but the PR form did not surface.

## I8: link-health-no-contributor-path

Severity: MEDIUM. Corroboration: 1 lens (operate). Deps: none.

Criterion 1 requires a stable, reachable URL, yet the documented local commands and PR checklist never offer a link check, and the Links workflow runs only on weekly cron or manual dispatch with `fail: false` so the job stays green while optionally opening an issue. Contributors cannot verify the reachability bar before they open a PR, broken or mistyped entry URLs can merge with a green Lint check, and the only safety net is a non-blocking weekly report rather than a pre-merge signal on the list's actual product.

Evidence:

- `contributing.md:7`: "1. Stable, reachable URL pointing at the project itself."
- `contributing.md:27-30`: local commands contain no link checker.
- `.github/workflows/links.yml:3-6`: cron and workflow_dispatch triggers only.
- `.github/workflows/links.yml:17-25`: `fail: false` on the lychee step.
- `.github/PULL_REQUEST_TEMPLATE.md:4`: checklist has no link-check item.

Blast radius: bad URLs ship until the next Monday cron (or until someone remembers workflow_dispatch); readers hit dead links; maintainers rely on issue noise instead of PR-time failure; criterion 1 stays unenforceable by the people adding entries.

## Advisories

Below-the-findings-bar material left for a later packaging run to judge:

| Id | Title | Evidence |
|----|-------|----------|
| a-01 | Near-parallel structured-use-cases entries lack proven same-project identity | README.md:80,85 |
| a-02 | Syside split across listings is intentional open-core layering, not duplication | README.md:45-46,114 |
| a-03 | Cameo docs URL embeds 2026x path segment that may age | README.md:121 |
| a-04 | links.yml fail:false is a deliberate soft gate | .github/workflows/links.yml:22 |
| a-05 | No outstanding marker-comment debt in the repository; TOC anchors match all README sections | README.md:7-17,19-118 |
| a-06 | links.yml labels report, broken-links not defined in-repo; create-issue-from-file may fail on first use | .github/workflows/links.yml:30 |
| a-07 | Freshness gh issue search by title substring can attach to a non-bot issue titled similarly | .github/workflows/stale.yml:44 |
| a-08 | stale.yml URL injection mitigated by restrictive grep charset before curl/gh | .github/workflows/stale.yml:28-30 |
| a-09 | No committed secrets; only secrets.GITHUB_TOKEN references | .github/workflows/links.yml:23 |
| a-10 | Token scopes already limited to contents:read + issues:write | .github/workflows/stale.yml:8-10 |
| a-11 | Local runbook does not pin Node 20 that CI setup-node uses | .github/workflows/lint.yml:16-20; contributing.md:27-29 |
