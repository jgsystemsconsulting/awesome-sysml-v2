# Context: actions-sha-pin-all-workflows (P9)

## Context brief

- **Primary question**: What must change to SHA-pin every GitHub Actions `uses:` ref in this repository's three workflows, and what workspace facts constrain that change?
- **Sub-questions**:
  1. Exact inventory of every `uses:` ref (file:line, current mutable tag).
  2. Declared `permissions:` blocks per workflow (must not be touched by P9).
  3. Any other workflow files, reusable-workflow callers, or action metadata in the repo beyond the three known files?
  4. Conventions a maintainer-facing "pin upgrade path" comment must respect (file structure, comment placement, markdownlint scope).
- **Success criteria** (spec author needs):
  - SC1: Complete `uses:` inventory with file:line and tag for all three workflows (known from gate: 7 refs, see below) corroborated against the working tree.
  - SC2: Permission blocks of links.yml, lint.yml, stale.yml captured (lint.yml expected to have none — P8 owns adding it).
  - SC3: Confirmation that no other Actions references exist anywhere in the repo (no composite actions, no action.yml, no reusable workflow callers).
  - SC4: Where a pin-upgrade-path comment belongs in each file without altering step semantics.
- **Out of scope**: awesome-lint version pin and lint.yml permissions (P8); lychee behavior (P7); stale.yml curl/cutoff logic (P6); Dependabot/Renovate; README/content files.
- **Budget**: 1 round target; round cap 3.
- **Workspace baseline**: porcelain sha256 `0933b130d260f82993853e7b62552af5ff0dccda8cd3a8192496cf60092999d2`, HEAD `af077117bec632c636ec914ddb8af002e6e4bc4b` (informational).

## Findings

Full graded claim table lives in the round log (`2026-09-16-actions-sha-pin-all-workflows-context-log.md`). 27 claims: 14 corroborated, 13 single-source, 0 conflicted, 0 stale. Key claims:

- The complete `uses:` inventory is 7 refs across 3 files: stale.yml:16 checkout@v4; links.yml:16 checkout@v4, links.yml:19 lycheeverse/lychee-action@v2, links.yml:26 peter-evans/create-issue-from-file@v5; lint.yml:13 checkout@v4, lint.yml:16 actions/setup-node@v4, lint.yml:22 DavidAnson/markdownlint-cli2-action@v24. Matches the gate's independent pre-read grep exactly.
- Permissions: stale.yml:8-10 and links.yml:8-10 declare top-level `contents: read` + `issues: write`; lint.yml declares none (P8 owns adding it).
- No other Actions surface exists: no action.yml/action.yaml, no .github/actions, no workflow_call/workflow_run, no reusable callers (cartographer + prospector agree).
- No Dependabot/Renovate config exists; pins will freeze until manually bumped.
- The three workflow files contain zero `#` comments today; `uses:` lines are consistently indented (6-space dash, first-step position for checkout/setup-node).
- Boundary constraints from counter-evidence lens: P9 must not touch lint.yml's permissions block or `npx awesome-lint` line (P8 owns both); stale.yml's `issues: write` permission stays; no published doc claims tag-float behavior, so pinning contradicts nothing; PR template names no required check.

## Synthesis

All four success criteria are met (4/4). The uses: inventory (SC1) is the decision-bearing core: cartographer's per-file reads match the parent gate's independent grep line-for-line, so the inventory is treated as corroborated in substance; formally the per-file claims are single-lens and their single-source status is named here. SC2 permissions are corroborated (prospector+skeptic, cartographer). SC3 no-other-surfaces is corroborated (cartographer+prospector, independent searches). SC4 comment placement: no comment convention exists to follow (zero comments in all three files), so the plan should place one block comment per file under the `name:` line; single-source, named here. Open questions: none. Remaining single-sourced claims are boundary advisories (ubuntu-latest float, Dependabot absence, CI-vs-local markdownlint skew, a-11 Node pin) and are out of P9 scope or already routed (backlog b-12, b-15, b-16; P8 owns the npx/permissions boundary).

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| .github/workflows/stale.yml:3 | config | cartographer (triggers) |
| .github/workflows/stale.yml:8 | config/code | cartographer, prospector, skeptic (permissions) |
| .github/workflows/stale.yml:16 | config | cartographer (checkout@v4) |
| .github/workflows/links.yml:3 | config | cartographer (triggers) |
| .github/workflows/links.yml:8 | config | prospector (permissions) |
| .github/workflows/links.yml:16 | config | cartographer (checkout@v4) |
| .github/workflows/links.yml:19 | config | cartographer (lychee-action@v2) |
| .github/workflows/links.yml:26 | config | cartographer (create-issue-from-file@v5) |
| .github/workflows/lint.yml:1 | config/code | prospector, skeptic (no permissions block) |
| .github/workflows/lint.yml:3 | config | cartographer (triggers) |
| .github/workflows/lint.yml:11 | code | skeptic (ubuntu-latest) |
| .github/workflows/lint.yml:13 | config | cartographer, prospector (checkout@v4) |
| .github/workflows/lint.yml:16 | config | cartographer (setup-node@v4) |
| .github/workflows/lint.yml:20 | code | skeptic (npx awesome-lint, P8 boundary) |
| .github/workflows/lint.yml:22 | code | cartographer, skeptic (markdownlint-cli2-action@v24) |
| .github/workflows/lint.yml:24 | config | cartographer (globs) |
| contributing.md:1 | doc | prospector (no CI content) |
| contributing.md:25 | doc | skeptic (runbook intro) |
| contributing.md:29 | doc | skeptic (local markdownlint npx) |
| .github/PULL_REQUEST_TEMPLATE.md:4 | doc | skeptic (no required-check claims) |
| docs/superpowers/packages/2026-09-15-awesome-sysml-v2-packages.md:34 | doc | skeptic (P9 out_scope Dependabot) |
| docs/superpowers/packages/2026-09-15-awesome-sysml-v2-packages.md:76 | doc | skeptic (P8/P9 lint.yml coordination) |
| docs/superpowers/reviews/2026-09-15-awesome-sysml-v2-findings.md:66 | doc | skeptic (I4 control description) |
| docs/superpowers/reviews/2026-09-15-awesome-sysml-v2-findings.md:149 | doc | skeptic (a-11) |
| .github (dir) | config | prospector (no dependabot/renovate) |
| repo root | config | cartographer, prospector (no composite actions / reusable callers) |
| .github/workflows (dir) | config | prospector (zero comments) |
