# pr-lint-gate-surface (P8) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the PR lint gate one consistent contract: least-privilege permissions on lint.yml, `awesome-lint@2.3.0` pinned on all three live surfaces, and a markdownlint checkbox in the PR template.

**Architecture:** Three file edits, no new files, no new dependencies. lint.yml gains a top-level `permissions: contents: read` block between `on:` and `jobs:`, following the links.yml/stale.yml house pattern minus `issues: write`. The exact string `npx awesome-lint@2.3.0 README.md` replaces the unpinned command in lint.yml, contributing.md, and PULL_REQUEST_TEMPLATE.md, and the template gains a second checkbox. One commit lands all three files.

**Tech Stack:** GitHub Actions YAML, markdown, npx (npm), grep/diff/python for verification.

**Spec:** `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-pr-lint-gate-surface.md`

## Global Constraints

- Workspace baseline is HEAD `695dd1b`. All line numbers in the spec and this plan are HEAD-baseline values. Apply every edit by quoted content, never by line number, and re-anchor after each insertion.
- Exactly three files change: `.github/workflows/lint.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`. No other file changes.
- The pinned command string on every surface is exactly `npx awesome-lint@2.3.0 README.md`.
- The lint.yml permissions block is exactly `permissions:` plus `  contents: read`. No `issues: write`, no job-level override.
- `fetch-depth: 0` in the checkout step stays. The `awesome-lint` step name stays unchanged.
- The markdownlint line in contributing.md stays unpinned: `npx markdownlint-cli2 "README.md" "contributing.md"`. Only awesome-lint is pinned in this change.
- No task commits before Task 4. Nothing is pushed at any point in this plan.
- All commands run from the repo root `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2` under Git Bash (bash syntax such as process substitution is used in verification steps).

## Codebase context

Verified at HEAD 695dd1b (context gate, re-confirmed in the workspace before this plan was written):

- `.github/workflows/lint.yml` (33 lines): P9 pin comment block at lines 2-7; `on:` block at 9-13; no `permissions:` anywhere in the file; `jobs:` at 15; checkout at 19-21 with `fetch-depth: 0` (required by awesome-lint's repo-age check); setup-node at 22-24 with node-version 20; unpinned run line at 26 (`        run: npx awesome-lint README.md`); markdownlint step at 27-32 globbing README.md and contributing.md.
- `.github/PULL_REQUEST_TEMPLATE.md`: exactly 5 lines with a trailing newline; line 4 is ``- [ ] `npx awesome-lint README.md` passes locally``.
- `contributing.md` (30 lines): `## Local commands` heading at 23, prose at 25, bash fence 27-30 with unpinned `npx awesome-lint README.md` at 28 and `npx markdownlint-cli2 "README.md" "contributing.md"` at 29.
- Sibling permissions pattern (links.yml 14-16 and stale.yml 14-16): `permissions:` / `  contents: read` / `  issues: write`, with one blank line on each side. The lint job writes nothing, so `contents: read` alone is correct for lint.yml.
- `.markdownlint-cli2.jsonc` sets only `MD013: false`. The markdownlint globs do not cover the PR template, so template edits are not lint-constrained.
- Working tree at planning time: only untracked `docs/`; `.github/workflows/` contains exactly `links.yml`, `lint.yml`, `stale.yml`.

## Research

Decision-bearing sources (full graded table in `docs/superpowers/research/2026-09-16-pr-lint-gate-surface-research.md`):

- awesome-lint latest published version is 2.3.0 with `engines: node >=20`, matching CI's Node 20: https://registry.npmjs.org/awesome-lint
- `npx pkg@specifier` matches only that exact name and version and installs it into the npm cache: https://docs.npmjs.com/cli/v10/commands/npx (the lockfile contrast is sourced separately in the research companion's package-lock row)

Carried decision: pin `@2.3.0` at the top level rather than introduce a package.json plus lockfile subsystem. Transitive float is accepted and recorded as a documented limitation in the spec. Bump cadence for future maintenance: bump `@2.3.0` in all three files in one commit, on the same cadence as the P9 action SHA bumps, after confirming engines still satisfy Node 20. The version appears in exactly three live files, so a bump is a three-line diff.

---

### Task 1: Pre-flight gate

Read-only. Confirms the workspace still matches the spec's HEAD baseline before anything is edited. Any mismatch means the workspace drifted from the spec; stop and report instead of editing.

**Files:**
- Modify: none (verification only)

**Interfaces:**
- Consumes: nothing
- Produces: confirmation that the four before-surfaces quote-match the spec, which Tasks 2 through 4 rely on

**Model:** flash

- [ ] **Step 1: Verify HEAD**

Run: `git rev-parse --short HEAD`
Expected output: `695dd1b`
Any other value: STOP. Do not edit. Report the drift.

- [ ] **Step 2: Verify clean working tree**

Run: `git status --porcelain`
Expected output: exactly one line, `??  docs/` (untracked docs only). Any staged or modified entry (`M`, `A`, `D`): STOP.

- [ ] **Step 3: Quote-match the four before-surfaces**

Run each command and compare against the expected output.

```bash
grep -n 'run: npx awesome-lint README.md' .github/workflows/lint.yml
```
Expected: exactly one hit, `26:        run: npx awesome-lint README.md` (unpinned CI line).

```bash
grep -n 'permissions:' .github/workflows/lint.yml
```
Expected: no output, exit code 1 (no permissions block exists between `on:` and `jobs:`, or anywhere).

```bash
grep -n 'npx awesome-lint README.md' contributing.md
```
Expected: exactly one hit, `28:npx awesome-lint README.md` (unpinned runbook line).

```bash
grep -c '' .github/PULL_REQUEST_TEMPLATE.md && grep -n 'npx awesome-lint README.md' .github/PULL_REQUEST_TEMPLATE.md
```
Expected: first `5` (the template is 5 lines), then `4:- [ ] \`npx awesome-lint README.md\` passes locally` (unpinned checkbox line).

- [ ] **Step 4: Verify workflows dir is clean**

Run: `ls .github/workflows/`
Expected output: exactly `links.yml  lint.yml  stale.yml`

- [ ] **Step 5: Gate**

Done when: all four checks in Steps 1-4 returned the expected output. Any mismatch: STOP, report, do not start Task 2.

---

### Task 2: Apply the three-file edits

Four edits by exact string replacement. No commit in this task; the working tree stays dirty for Task 3 to verify.

**Files:**
- Modify: `.github/workflows/lint.yml` (two edits: permissions block, pinned run line)
- Modify: `contributing.md` (one edit: pinned fence line)
- Modify: `.github/PULL_REQUEST_TEMPLATE.md` (one edit: pin line 4, insert markdownlint checkbox after it)

**Interfaces:**
- Consumes: Task 1 gate passed
- Produces: the three edited files that Task 3 verifies and Task 4 stages and commits

**Model:** flash

- [ ] **Step 1: lint.yml, insert permissions block between `on:` and `jobs:`**

Replace this exact text:

```yaml
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
```

with this exact text (adds three lines: `permissions:`, `  contents: read`, and the blank line separating them from `jobs:`):

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

One blank line on each side of the block, matching the sibling workflow layout. No `issues: write`. No job-level override.

- [ ] **Step 2: lint.yml, pin the awesome-lint run line**

Replace this exact text:

```yaml
      - name: awesome-lint
        run: npx awesome-lint README.md
```

with this exact text (step name unchanged, six characters added to the run line):

```yaml
      - name: awesome-lint
        run: npx awesome-lint@2.3.0 README.md
```

`fetch-depth: 0` in the checkout step above stays as is.

- [ ] **Step 3: contributing.md, pin the fence line**

Replace this exact text (the two lines inside the bash fence):

```
npx awesome-lint README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

with this exact text (only the awesome-lint line changes; the markdownlint line stays unpinned):

```
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

Prose above the fence is untouched. MD013 is off, so fence-line length is not a lint concern.

- [ ] **Step 4: PULL_REQUEST_TEMPLATE.md, pin line 4 and insert the markdownlint checkbox after it**

Replace the full 5-line content with this exact 6-line content:

```
- [ ] Entry meets all five criteria in contributing.md
- [ ] Added to the correct section; alphabetical order kept
- [ ] `- [Name](URL) - Description.` format followed
- [ ] `npx awesome-lint@2.3.0 README.md` passes locally
- [ ] `npx markdownlint-cli2 "README.md" "contributing.md"` passes locally
- [ ] Commercial entries go in Commercial Tools only, with disclosure in the PR body
```

The new checkbox sits directly after the awesome-lint checkbox, mirroring the fence order in contributing.md, and embeds the exact contributing.md markdownlint command inside a code span with the same trailing wording ` passes locally`. The template is not covered by markdownlint globs, so the embedded quotes are lint-safe, and the code span renders correctly on GitHub. Preserve the trailing newline.

- [ ] **Step 5: Immediate sanity check**

Run: `grep -rn "npx awesome-lint" . --exclude-dir=.git --exclude-dir=docs --exclude-dir=.superpowers`
Expected: exactly three hits, one per file, every hit containing `@2.3.0` (match the three file paths and pinned content; line order and separator style may vary):

```
.github/PULL_REQUEST_TEMPLATE.md:4:- [ ] `npx awesome-lint@2.3.0 README.md` passes locally
.github/workflows/lint.yml:29:        run: npx awesome-lint@2.3.0 README.md
contributing.md:28:npx awesome-lint@2.3.0 README.md
```

(Path separator style may vary by platform. The lint.yml line number is 29 because Step 1 added three lines above it; match on content, not line number.)

Run: `grep -c 'permissions:' .github/workflows/lint.yml`
Expected output: `1`

Done when: all four edits applied exactly, the sanity grep shows three pinned hits and zero unpinned hits, and the permissions count is 1. Do NOT commit.

---

### Task 3: Verification battery

Read-only checks covering acceptance criteria 1 through 6 of the spec. No commit in this task.

**Files:**
- Modify: none (verification only)

**Interfaces:**
- Consumes: Task 2 edits present in the working tree
- Produces: the passing gate Task 4 requires before it commits

**Model:** flash

- [ ] **Step 1: YAML parses (AC1)**

Run: `python -c "import yaml; yaml.safe_load(open('.github/workflows/lint.yml'))"`
Expected: exit 0, no output. Requires PyYAML; if the import fails, run `python -m pip install pyyaml` and rerun.

- [ ] **Step 2: Pin coverage grep (AC2)**

Run: `grep -rn "npx awesome-lint" . --exclude-dir=.git --exclude-dir=docs --exclude-dir=.superpowers`
Expected: exactly three hits, one each in lint.yml, contributing.md, and PULL_REQUEST_TEMPLATE.md, all carrying `@2.3.0` (same output as Task 2 Step 5). The `.superpowers` exclusion matters: SDD scratch briefs quote the unpinned command and would false-fail the count.

Run: `grep -rn "npx awesome-lint README.md" . --exclude-dir=.git --exclude-dir=docs --exclude-dir=.superpowers`
Expected: no output, exit code 1. The unpinned string appears nowhere outside `docs/superpowers/` historical records, because the pinned form inserts `@2.3.0` before ` README.md` and no longer contains this substring.

- [ ] **Step 3: Byte-identical command strings (AC3)**

Run:

```bash
diff <(grep 'npx awesome-lint@2.3.0' .github/workflows/lint.yml | sed 's/^ *run: //') <(grep '^npx awesome-lint@2.3.0' contributing.md) && echo IDENTICAL
```

Expected output: `IDENTICAL`, exit 0. This strips the `run: ` prefix and indentation from the CI line and diffs it against the contributing.md fence line; both reduce to `npx awesome-lint@2.3.0 README.md`. The template code span contains the same string (already confirmed by the grep in Step 2).

- [ ] **Step 4: Template shape (AC4)**

Run: `grep -c '' .github/PULL_REQUEST_TEMPLATE.md`
Expected output: `6`

Run: `grep -n '^\- \[ \]' .github/PULL_REQUEST_TEMPLATE.md`
Expected output, in this order:

```
1:- [ ] Entry meets all five criteria in contributing.md
2:- [ ] Added to the correct section; alphabetical order kept
3:- [ ] `- [Name](URL) - Description.` format followed
4:- [ ] `npx awesome-lint@2.3.0 README.md` passes locally
5:- [ ] `npx markdownlint-cli2 "README.md" "contributing.md"` passes locally
6:- [ ] Commercial entries go in Commercial Tools only, with disclosure in the PR body
```

Both linter checkboxes present, awesome-lint before markdownlint, matching the fence order in contributing.md.

- [ ] **Step 5: Local lint run passes after the contributing.md edit (AC5)**

Run: `npx markdownlint-cli2 "README.md" "contributing.md"`
Expected: exit 0, no output. This lints the edited contributing.md (and README.md, unchanged). A cold npx cache downloads the package from the registry; network access is required on first run.

- [ ] **Step 6: Diff surface and untouched siblings (AC6)**

Run: `git diff --name-only`
Expected output: exactly these three paths, nothing else:

```
.github/PULL_REQUEST_TEMPLATE.md
.github/workflows/lint.yml
contributing.md
```

Run: `git diff --name-only | grep -cE 'links\.yml|stale\.yml'`
Expected output: `0` (grep prints 0 and exits 1 when nothing matched; both sibling workflows are untouched).

Done when: all six checks pass. If any check fails, fix Task 2's edit and rerun the battery before Task 4.

---

### Task 4: Single commit

Stages exactly the three changed files and commits with the exact plan message (see Step 3). Nothing is pushed.

**Files:**
- Stage: `.github/workflows/lint.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Consumes: Task 3 battery fully green
- Produces: one local commit containing exactly the three files

**Model:** flash

- [ ] **Step 1: Stage exactly the three files**

```bash
git add .github/workflows/lint.yml contributing.md .github/PULL_REQUEST_TEMPLATE.md
```

- [ ] **Step 2: Staging check**

Run: `git status --porcelain`
Expected output: three staged lines (`M  ` prefix) for exactly the three paths above, plus `??  docs/`. Nothing else.

- [ ] **Step 3: Commit with the exact message**

```bash
git commit -m "Add least-privilege lint permissions and pin awesome-lint 2.3.0"
```

The message is exact per this plan (the spec's acceptance criteria do not define a commit message): no conventional-commit prefix, no scope, no body. Do not push.

- [ ] **Step 4: Post-commit verification**

Run: `git log -1 --format=%s`
Expected output: `Add least-privilege lint permissions and pin awesome-lint 2.3.0`

Run: `git show --name-only --format= HEAD`
Expected output: exactly the three paths:

```
.github/PULL_REQUEST_TEMPLATE.md
.github/workflows/lint.yml
contributing.md
```

Run: `git status --porcelain`
Expected output: only `??  docs/`.

Run: `git status -sb`
Expected: the branch line shows ahead of its upstream by 1 commit (when upstream is tracked). Do NOT run `git push`; the push and PR open happen outside this plan.

Done when: the commit exists with the exact message and exactly three files, the working tree holds only untracked `docs/`, and nothing was pushed.

---

## Spec coverage map

| Acceptance criterion | Covered by |
|----------------------|------------|
| AC1 permissions block, YAML parses | Task 2 Step 1, Task 3 Step 1 |
| AC2 every live hit pinned, one per file | Task 2 Steps 2-5, Task 3 Step 2 |
| AC3 byte-identical command strings | Task 2 Steps 2-4, Task 3 Step 3 |
| AC4 template 6 lines, both checkboxes in order | Task 2 Step 4, Task 3 Step 4 |
| AC5 markdownlint passes locally | Task 3 Step 5 |
| AC6 diff is exactly three files, siblings untouched | Task 3 Step 6 |
| AC7 lint workflow passes on the PR | Verified by CI after the PR opens; outside this plan because nothing is pushed here |

Non-goal boundaries respected by this plan: links.yml and stale.yml are never edited, markdownlint-cli2 stays unpinned in contributing.md, README content untouched, no new linters, no lockfile subsystem.
