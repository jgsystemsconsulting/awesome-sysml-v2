# Context: link-ops-no-spam-pr-path (P7)

## Context brief

- **Primary question**: What must change so the weekly Link Checker Report dedupes into one issue (create-or-update, like the Freshness report), undefined labels are handled, a contributor-visible link check exists (PR-time soft signal and/or documented local command), and the PR template carries a link-check checkbox — and what workspace facts constrain that change?
- **Success criteria**:
  - SC1: links.yml current full content (HEAD bf25772; post-P9 pins) with exact line numbers: triggers, permissions, lychee step (args/fail/token/output), create-issue-from-file step.
  - SC2: The Freshness create-or-update pattern in stale.yml (the dedupe pattern to mirror) quoted.
  - SC3: contributing.md current local-commands section (post-P8 pinned line) and PR template current 6 lines (post-P8) — the insert points for the local link-check command and the link-check checkbox.
  - SC4: Boundary: stale.yml/lint.yml outside P7; whether any issue labels exist in the repo (report, broken-links were referenced by links.yml but never defined).
- **Out of scope**: hard-fail merge gate (a-04, backlog b-12); freshness (done P6); lint gate (done P8); README entries.
- **Budget**: 1 round; cap 3.
- **Workspace baseline**: HEAD bf25772 (P8 landed).

## Findings

Full graded claim table in the round log. 12 claims: verdict CONTEXT_COMPLETE, 0 conflicted, 0 stale. Key facts (HEAD bf25772):

- links.yml (SC1): name line 1, P9 pin block 2-7, `on:` cron "0 18 * * 1" + workflow_dispatch (9-12), permissions contents:read + issues:write (14-16), lychee step (args `--no-progress`, `fail: false`, token GITHUB_TOKEN), create-issue-from-file step gated `if: steps.lychee.outputs.exit_code != 0` with fixed title "Link Checker Report" and `labels: report, broken-links`.
- Dedupe pattern to mirror (SC2): stale.yml:50-59 — `gh issue list --state open --search "Freshness report in:title"` → edit or create.
- Runbook + template (SC3): contributing.md fence 27-30 (line 28 pinned awesome-lint, 29 unpinned markdownlint); PR template 6 lines post-P8 (pinned awesome-lint + markdownlint checkboxes at 4-5).
- Labels (SC4): `report`/`broken-links` referenced by links.yml but defined nowhere in-repo (GitHub labels live in settings); first create can fail on a missing label or silently drop it.
- Design constraints surfaced by the skeptic lens (all config/code-sited): (1) the issue step has no `event_name` gate — adding a `pull_request` trigger without gating would spam the report issue from PRs and fail on forks lacking issues:write; (2) no concurrency group — cron and PR runs can double up; (3) the `in:title` substring search can hijack a user issue with a similar title — quoted-phrase search or exact-match discipline needed; (4) lychee is not an npm package — the local command cannot live as a plain npx line in the same fence as awesome-lint; it needs a per-platform install note (research SC2: scoop/winget/choco/brew/...); (5) GITHUB_TOKEN is already wired into the lychee step (github links OK); (6) P9 pins force SHA+#tag on any NEW `uses:` lines; (7) `issues: write` is excess scope for a soft PR-time check.

## Synthesis

All four success criteria met (4/4); verdict CONTEXT_COMPLETE. SC1/SC2/SC4 corroborated with config/code sites from at least two lenses; SC3 doc-as-artifact surfaces were read independently by three lenses with matching quotes — named here per the Track 1 rule. No conflicts, no stale. The design constraints above are the spec's raw material: the PR-time check must be soft and issue-free (separate job without issues:write, or a hard event gate on the issue step), the weekly report dedupes via the stale.yml pattern with a quoted-phrase search, labels get created explicitly or dropped from the step, and the local command documents the platform install path plus GITHUB_TOKEN.

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| .github/workflows/links.yml:1 | config | cartographer (name) |
| .github/workflows/links.yml:2-7 | config | cartographer, prospector (P9 block) |
| .github/workflows/links.yml:9-12 | config | cartographer, skeptic (triggers) |
| .github/workflows/links.yml:14-16 | config | cartographer, skeptic (permissions) |
| .github/workflows/links.yml:26 | config | prospector, skeptic (lychee args/fail/token) |
| .github/workflows/links.yml:30-31 | config | skeptic (exit_code gate, no event gate) |
| .github/workflows/links.yml:36 | config | cartographer, skeptic (labels) |
| .github/workflows/stale.yml:50-59 | config/code | cartographer, prospector, skeptic (upsert pattern) |
| contributing.md:27-30 | doc | cartographer, prospector, skeptic (fence; lychee-not-npx constraint) |
| .github/PULL_REQUEST_TEMPLATE.md:1-6 | doc | cartographer, prospector, skeptic (6 checkboxes) |
| docs/superpowers/specs/2026-09-16-actions-sha-pin-all-workflows.md:36 | doc | skeptic (P7 boundary) |
| docs/superpowers/research/2026-09-16-link-ops-no-spam-pr-path-research.md:20 | doc | skeptic (dedupe mechanism) |
| repo root | config | prospector (no .lycheeignore/lychee.toml) |
