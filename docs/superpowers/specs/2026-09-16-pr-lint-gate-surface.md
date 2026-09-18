# Design spec: pr-lint-gate-surface (P8)

Date: 2026-09-16
Workspace baseline: HEAD 695dd1b
Absorbs: repo-review-loop findings I5, I6, I7

## Problem statement

The PR lint gate is one workflow with three inconsistent surfaces, and the repo review loop flagged each as a finding:

- I5: `.github/workflows/lint.yml` has no explicit `permissions:` block. Every other workflow in the repo (links.yml, stale.yml) declares least-privilege permissions at top level; lint.yml inherits default token scopes instead.
- I6: `npx awesome-lint README.md` appears unpinned on three live surfaces: lint.yml line 26, contributing.md line 28, and `.github/PULL_REQUEST_TEMPLATE.md` line 4. A pin that lands on only two of the three splits the contract between CI, the local runbook, and the contributor checklist.
- I7: the PR template checklist names only awesome-lint. CI also runs markdownlint (pinned action, v24), so contributors get no reminder to run the second required linter, and the template's embedded awesome-lint command drifts from contributing.md whenever either changes.

One change fixes all three: explicit `contents: read` permissions on lint.yml, one exact awesome-lint version (`@2.3.0`) on all three surfaces, and a second checkbox in the template.

## Goals

1. lint.yml declares `permissions: contents: read` at top level, matching the links.yml/stale.yml house pattern minus `issues: write`, which the lint job does not need.
2. All three `npx awesome-lint` surfaces carry the exact same pinned command: `npx awesome-lint@2.3.0 README.md`. CI, contributing.md, and the PR template are byte-identical on this string.
3. PULL_REQUEST_TEMPLATE.md gains a markdownlint checkbox worded like the awesome-lint one.
4. contributing.md stays the runbook source of truth for awesome-lint: its pinned command matches CI byte-for-byte. (The markdownlint pair intentionally differs in form — CI runs the pinned action, the runbook the npx command; see design section 2.)

## Non-goals

- Repo-wide Actions SHA pinning (P9, done).
- New linters of any kind.
- Link checks (P7) and the link-check checkbox P7 will later add to the template (different lines, no conflict; P8 lands first).
- stale.yml changes (P6, done); site, CoC, discoverability (P2/P5/P3); README content.
- A package.json plus lockfile subsystem to lock transitive dependencies (see limitations).
- Pinning `markdownlint-cli2` in contributing.md. Only awesome-lint is in scope; the CI side is already pinned (markdownlint-cli2-action SHA, v24).

## Codebase context

Facts verified at HEAD 695dd1b (context gate):

- lint.yml: P9 pin comment block lines 2 to 7; `on:` block lines 9 to 13; no `permissions:` between `on:` and `jobs:` (insertion slot is line 14, before `jobs:` at 15); checkout at lines 19 to 21 with `fetch-depth: 0`, which awesome-lint's repo-age check requires and which must stay; unpinned npx run line at 26; markdownlint step globs README.md and contributing.md at lines 27 to 32.
- PULL_REQUEST_TEMPLATE.md: 5 lines; line 4 is a checkbox embedding the unpinned command inside a code span, followed by "passes locally".
- contributing.md: "## Local commands" heading at line 23, prose at 25, bash fence at 27 to 30 with the two npx commands at 28 and 29.
- Sibling permissions pattern (`permissions:` / `  contents: read` / `  issues: write`) at links.yml 14 to 16 and stale.yml 14 to 16. The lint job writes nothing, so `contents: read` alone is sufficient.
- `.markdownlint-cli2.jsonc` sets only `MD013: false`; markdownlint globs do not cover the PR template, so template edits are not lint-constrained.

## Research

Decision-bearing lines, full graded table in the research gate document:

- awesome-lint latest published version is 2.3.0, engines node >=20, matching CI's Node 20: https://registry.npmjs.org/awesome-lint
- `npx pkg@specifier` matches only that exact name and version and installs it into the npm cache without consulting a lockfile: https://docs.npmjs.com/cli/v10/commands/npx

Carried decision: pin `awesome-lint@2.3.0` at the top level in CI and in all documented local commands. A package.json plus lockfile variant would lock the transitive tree but adds a maintenance surface the packages document did not request; the top-level pin is accepted with the transitive-float limitation recorded below.

## Design

Three files change. No other file changes. All cited line numbers are HEAD-baseline (695dd1b); apply edits by quoted content, not by line number, and re-anchor after each insertion.

### 1. lint.yml: permissions block

Insert between the `on:` block and `jobs:`, with one blank line on each side, matching the sibling workflow layout.

Before (lines 9 to 15):

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
```

After:

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
```

The insertion adds three lines total: the blank-line-separated pair `permissions:` and `  contents: read`. No `issues: write`, no job-level override. Post-edit, the P9 comment block (2 to 7) and the `on:` block (9 to 13) keep their positions; `jobs:` moves to line 18 and the npx run line moves from 26 to 29. `fetch-depth: 0` stays as is.

### 2. The one pinned command string

All three surfaces use exactly:

```
npx awesome-lint@2.3.0 README.md
```

Embedded forms per surface:

- CI run line (lint.yml): `run: npx awesome-lint@2.3.0 README.md`
- contributing.md fence line: `npx awesome-lint@2.3.0 README.md`
- PR template checkbox: `- [ ] ` + backtick code span `npx awesome-lint@2.3.0 README.md` + ` passes locally`

The CI run line and the contributing.md line are byte-identical after stripping the `run: ` prefix and indentation. The template checkbox embeds the same string inside a code span and keeps the existing trailing wording ` passes locally`. On the dispatch question of divergence: CI and contributing.md do not diverge on the awesome-lint command. The markdownlint pair (CI action versus local `npx markdownlint-cli2 "README.md" "contributing.md"`) is a pre-existing, intentional surface difference (an action is not a shell command) and stays unchanged.

### 3. lint.yml: pinned run line

Before (lines 25 to 26):

```yaml
      - name: awesome-lint
        run: npx awesome-lint README.md
```

After:

```yaml
      - name: awesome-lint
        run: npx awesome-lint@2.3.0 README.md
```

Step name unchanged.

### 4. contributing.md: pinned fence line

Before (lines 27 to 30):

```bash
npx awesome-lint README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

After:

```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

Only the awesome-lint line changes. The markdownlint line stays unpinned (non-goal). Prose above the fence is untouched; MD013 is off, so fence-line length is not a lint concern.

### 5. PULL_REQUEST_TEMPLATE.md: pin plus second checkbox

Before (5 lines):

```
- [ ] Entry meets all five criteria in contributing.md
- [ ] Added to the correct section; alphabetical order kept
- [ ] `- [Name](URL) - Description.` format followed
- [ ] `npx awesome-lint README.md` passes locally
- [ ] Commercial entries go in Commercial Tools only, with disclosure in the PR body
```

After (6 lines):

```
- [ ] Entry meets all five criteria in contributing.md
- [ ] Added to the correct section; alphabetical order kept
- [ ] `- [Name](URL) - Description.` format followed
- [ ] `npx awesome-lint@2.3.0 README.md` passes locally
- [ ] `npx markdownlint-cli2 "README.md" "contributing.md"` passes locally
- [ ] Commercial entries go in Commercial Tools only, with disclosure in the PR body
```

The new checkbox sits directly after the awesome-lint checkbox, mirroring the fence order in contributing.md (awesome-lint, then markdownlint), and embeds the exact contributing.md markdownlint command inside a code span. The template is not covered by markdownlint globs, so the embedded quotes are lint-safe; the code span renders correctly on GitHub.

### Pin bump cadence

Bump `@2.3.0` in all three files in one commit, on the same cadence as the P9 action SHA bumps: check npm dist-tags, confirm engines still satisfy Node 20, update three lines. The version appears in exactly three live files, so a bump is a three-line diff.

## Documented limitations

- Transitive float: a top-level npx pin does not lock caret transitive dependencies (for example remark ^15), so cold-cache runs can still resolve newer transitives. Accepted; this is the cost of avoiding a lockfile subsystem in a repo that has none.
- Upstream-norm divergence: awesome-lint's own README recipe and sindresorhus/awesome's repo linter run `npx awesome-lint` unpinned (with `fetch-depth: 0`). This repo pins deliberately for supply-chain consistency with the P9 hardening and accepts divergence from upstream examples. `fetch-depth: 0` stays because awesome-lint's repo-age check requires it.
- Frozen false-positive fixes: the pin freezes the stream of lint false-positive fixes upstream ships (for example the v2.2.2 spell-check fix, sourced in the research companion's Sources table: https://github.com/sindresorhus/awesome-lint/releases/tag/v2.2.2). Fixes arrive only when the pin is bumped; the bump cadence above covers this.

## Risks

- YAML breakage from the insertion: low. The block is two plain mappings between blank lines. Mitigated by the parse check in the acceptance criteria.
- contributing.md lint regression: low. The edit adds six characters inside an existing bash fence and MD013 is off.
- Version skew after a partial bump: the acceptance criterion that every live `npx awesome-lint` hit carries `@2.3.0` makes a partial bump grep-detectable.
- npx cache versus registry: npx resolves the exact version from the registry on a cold cache and reuses the identical version warm. No drift class exists for the pinned top-level package.

## Acceptance criteria

1. lint.yml contains a top-level `permissions:` block with exactly `contents: read`, positioned between the `on:` block and `jobs:`; no other permission key appears. YAML parses (`python -c "import yaml; yaml.safe_load(open('.github/workflows/lint.yml'))"` exits 0).
2. `npx awesome-lint README.md` without `@2.3.0` appears nowhere in the repo outside `docs/superpowers/` historical records. Verified with `grep -rn "npx awesome-lint" . --exclude-dir=.git --exclude-dir=docs`: every hit contains `@2.3.0`, exactly one hit per file (lint.yml, contributing.md, PULL_REQUEST_TEMPLATE.md).
3. The three command strings are byte-identical: the lint.yml run line equals the contributing.md fence line after removing the `run: ` prefix, and the template code span equals both.
4. PULL_REQUEST_TEMPLATE.md carries both checkboxes (pinned awesome-lint, markdownlint) in the order shown above, 6 lines total.
5. `npx markdownlint-cli2 "README.md" "contributing.md"` passes after the contributing.md edit.
6. The diff against the base commit (file names only) lists exactly `.github/workflows/lint.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`. links.yml and stale.yml are untouched.
7. The lint workflow passes on the PR that lands this change (it triggers on pull_request to main).
