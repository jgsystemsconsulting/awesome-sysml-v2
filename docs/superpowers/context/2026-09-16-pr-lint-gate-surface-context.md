# Context: pr-lint-gate-surface (P8)

## Context brief

- **Primary question**: What must change so the PR lint gate is one consistent contract — explicit least-privilege permissions on lint.yml, a pinned awesome-lint version in CI and the local runbook, and a PR template checklist that names both required linters — and what workspace facts constrain that change?
- **Success criteria**:
  - SC1: lint.yml current full content post-P9 (pins landed; line numbers shifted +0 relative to P9 since lint.yml gained the 7-line comment block) — exact lines for the `uses:` steps, the npx line, and where the `permissions:` block must sit (between `on:` and `jobs:`).
  - SC2: PULL_REQUEST_TEMPLATE.md exact current checklist lines.
  - SC3: contributing.md local-commands section exact content (the two npx commands) and the PR-opening instructions.
  - SC4: Boundary confirmation: links.yml and stale.yml are P7/P6 territory (P6 landed; links.yml untouched); .markdownlint-cli2.jsonc config that constrains contributing.md edits (MD013 off).
- **Out of scope**: links.yml/lychee (P7); stale.yml (done, P6); SHA pins (done, P9); README content.
- **Budget**: 1 round; cap 3.
- **Workspace baseline**: HEAD 695dd1b (P6 landed).

## Findings

Full graded claim table in the round log. 13 claims: 7 corroborated, 6 single-source, 0 conflicted, 0 stale. Key facts (HEAD 695dd1b):

- lint.yml (SC1): P9 pin comment block lines 2-7; `on:` 9-13; **no permissions block** between `on:` and `jobs:` (insertion slot is line 14, before `jobs:` at 15); jobs 15-32 with checkout pin at 20-21 (`fetch-depth: 0` present, required by awesome-lint's repo-age check), npx line at 26 (`run: npx awesome-lint README.md`, unpinned), markdownlint step globs README.md + contributing.md at 30.
- PR template (SC2): 5 lines; line 4 is `- [ ] \`npx awesome-lint README.md\` passes locally` — carrying the UNPINNED command.
- contributing.md (SC3): "## Local commands" at 23, prose at 25, bash fence 27-30 with unpinned `npx awesome-lint README.md` (28) and `npx markdownlint-cli2 "README.md" "contributing.md"` (29).
- Three live unpinned `npx awesome-lint` surfaces (skeptic inventory): lint.yml:26, contributing.md:28, PULL_REQUEST_TEMPLATE.md:4. A pin that lands on only two of three leaves the contract split.
- Permissions house pattern: `permissions:\n  contents: read\n  issues: write` — links.yml:14-16, stale.yml:14-16. lint.yml needs `contents: read` only (no issue write in the lint job).
- Boundaries (SC4): links.yml/stale.yml outside P8 (P6 done, P7 next); .markdownlint-cli2.jsonc sets only MD013 false; markdownlint globs do not cover the PR template, so template edits are not lint-constrained.
- Collisions: P7 will also edit the PR template (link-check checkbox); P8 lands first in the queue. Packages-doc line refs predate the P9 shift.

## Synthesis

All four success criteria met (4/4). SC1 is corroborated (cartographer + skeptic + prospector on lint.yml sites, code/config). SC4 corroborated. SC2/SC3 are graded SINGLE-SOURCE by the evidence-kind rule, but the single source IS the artifact under review (a .md file cannot carry a code site); three lenses read each independently and quotes matched, so they are treated as corroborated in substance — named here per the Track 1 rule. No conflicts, no stale. Open questions: none. Design-relevant catches the spec must absorb: (1) the PR template's line 4 command is a third live unpinned surface and must be pinned together with CI and contributing.md; (2) the permissions block for lint.yml is `contents: read` only, inserted at line 14 following the sibling pattern; (3) contributing.md stays the runbook source of truth, byte-aligned with the CI pin; (4) P7 owns a later PR-template edit — no conflict, different lines.

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| .github/workflows/lint.yml:1-7 | config | cartographer, prospector (name + P9 block) |
| .github/workflows/lint.yml:9 | code | skeptic (on: block) |
| .github/workflows/lint.yml:20-21 | code | skeptic (checkout pin, fetch-depth: 0) |
| .github/workflows/lint.yml:26 | code | prospector, skeptic (unpinned npx) |
| .github/workflows/lint.yml:30 | code | skeptic (markdownlint globs) |
| .github/PULL_REQUEST_TEMPLATE.md:1-5 | doc | cartographer, prospector, skeptic (checklist; line 4 command) |
| contributing.md:23-30 | doc | cartographer, prospector, skeptic (local commands; line 28 command) |
| .github/workflows/links.yml:14-16 | config | prospector, skeptic (permissions pattern) |
| .github/workflows/stale.yml:14-16 | config | prospector (permissions pattern) |
| .markdownlint-cli2.jsonc:1-5 | config | cartographer, prospector (MD013 false) |
| docs/superpowers/packages/2026-09-15-awesome-sysml-v2-packages.md:74,97 | doc | skeptic (stale refs; P7 collision) |
| docs/superpowers/research/2026-09-16-pr-lint-gate-surface-research.md:33 | doc | skeptic (pin decision wording) |
