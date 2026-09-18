# Awesome acceptability assessment: Awesome SysML V2

**Date:** 2026-09-18  
**Decision:** **no-go / wait** (do not open a sindresorhus/awesome PR now)  
**Assessor surface:** live upstream + this repository HEAD on feat/landing-archimate-parity

## Verdict

Do not open a pull request against sindresorhus/awesome. Re-assess on or after
**2026-10-15** when the 30-day maturity gate clears, and only if upstream intake
is open again and the list still passes awesome-lint on a clean public main.

## Live gates checked

| Gate | Result | Evidence |
| --- | --- | --- |
| 30-day maturity | **FAIL until 2026-10-15** | Repo `created_at` 2026-09-15T20:37:50Z; create-list.md: "Wait at least 30 days after creating a list before submitting it" |
| Upstream intake | **CLOSED** | sindresorhus/awesome description still includes: "Pull requests are temporarily disabled until I have a chance to catch up with the existing ones" (checked 2026-09-18; open_issues ~106) |
| AI-generated PR ban | **Process risk** | PR template: "Fully AI-generated pull requests are not accepted." Human maintainer must own curation claim and the eventual PR body. |
| Review-4-PRs requirement | **Not started** | PR template requires reviewing at least 4 open awesome PRs with substantive comments before submitting. |
| awesome-lint | **Environment-dependent** | CI runs `npx awesome-lint@2.3.0 README.md` on PR/push. Local agent run reported `awesome-github` repo detection noise; treat CI green on main as the bar after merge. |
| Differentiation | **PASS provisional** | List targets SysML v2 tooling/models/learning specifically; sister MagicGrid list is separate. Not a blockchain list. |
| List size / maturity signal | **WEAK** | 75 curated entries is solid content depth, but public stars/forks are still 0 as of assessment date; maturity is time-gated more than content-gated. |
| Product surface | **In progress this branch** | Path S landing + release gate + product-surface lychee land with this package drain. Prefer main green before any future submission. |

## Prerequisites before any future go-now

1. Calendar date ≥ 2026-10-15 (30 days after create).
2. sindresorhus/awesome description no longer says PRs are temporarily disabled (or an official issue states intake is open).
3. main has green lint, validate (check_release), and product-surface link checks.
4. Human maintainer re-reads create-list.md and the PR template the day of submit.
5. Human writes the PR body and entry description (objective theme description, not a tagline; title `Add SysML V2`; URL ends `#readme`).
6. Human completes the required reviews of at least four open awesome PRs.
7. Re-run this assessment; only flip DISTRIBUTION to a go-now note if every row above is PASS.

## Explicit non-actions

- No PR opened as part of this package.
- No README taxonomy rewrite solely for upstream cosmetics.
- No claim that the list is already "on awesome.re".

## Sources

- https://raw.githubusercontent.com/sindresorhus/awesome/main/create-list.md
- https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md
- https://api.github.com/repos/sindresorhus/awesome (description, 2026-09-18)
- https://api.github.com/repos/jgsystemsconsulting/awesome-sysml-v2 (created_at, 2026-09-18)
