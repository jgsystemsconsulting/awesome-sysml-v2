# Models and Case Studies rename and PLEML entry Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the README section Example Models to Models and Case Studies (same TOC slot), add one entry (MBSE4U/PLEML), and sync docs/index.html, CHANGELOG.md, and the submission runbook in the same change.

**Architecture:** Pure text edit across four coordinated surfaces in one commit: README.md (tagline, TOC, H2, one alphabetical insert), docs/index.html (four shared description strings, hero, what-it-is, category row), CHANGELOG.md (two Unreleased bullets), and docs/superpowers/runbooks/awesome-submission.md (one differentiation sentence). No build system, no CI changes. Verification is grep-shaped because the acceptance criteria in the spec are grep-shaped. docs/ escapes lint.yml and lychee scopes, so the site sync rides in the same commit rather than relying on CI to catch drift.

**Tech Stack:** Markdown and static HTML edits. Git Bash on Windows. Lint via `npx awesome-lint@2.3.0` and `npx markdownlint-cli2`.

**Spec:** docs/superpowers/specs/2026-09-17-models-and-case-studies.md (the plan argues from the spec; executors read both)

## Global Constraints

- Baseline HEAD: `b3d842e8bfb84f3967ed7417cd6bae31e7ace8f1` (matches the context doc snapshot). If HEAD has moved, continue only if every baseline check below still matches; the content greps are the binding gate, not the hash.
- research: docs/superpowers/research/2026-09-17-models-and-case-studies-research.md (brief-covered; see Research section).
- Gate inputs: context doc docs/superpowers/context/2026-09-17-models-and-case-studies-context.md (CONTEXT_COMPLETE); spec review clean (FCL+ARL).
- Substitution rule: replace the lowercase token `example models` only inside the exact strings listed per task. No whole-file global replace of README entry lines. The nine existing entry lines stay byte-identical except for the PLEML insert.
- README must not gain any new H2 (total stays 13) and no H3 may appear inside the renamed section. No Projects section.
- `Systems-Modeling/SysML-v2-Release` stays under Official Implementations only; exactly one README hit after edits.
- contributing.md must not be modified by any task.
- Backlog items b-09 and b-13 stay open and untouched; both structured-use-cases entries stay; Flashlight stays under Migrating from SysML v1.
- Curation only: no entries beyond MBSE4U/PLEML, no automation for discovering model repos.
- Commit messages exact. Commit 0 (conditional, Task 1): `Add social card image and meta tags`. Final commit (Task 5): `Rename Example Models to Models and Case Studies and add PLEML`. One final commit for all four edited files so the README TOC+H2 pair and the docs/index.html category row land in the same commit (spec requirements 1 and 10).
- Nothing in this plan pushes to origin.
- Absence greps in verify steps: prefer `test "$(grep -c ... || true)" = "0"` so `set -e` shells do not abort on exit 1. Bare greps that expect no matches are documented as exit 1 only when run interactively without fail-fast.
- Commands are Git Bash on Windows. All paths relative to the repo root `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2`.
- Lint pins: `awesome-lint@2.3.0` and `markdownlint-cli2` (same versions as .github/workflows/lint.yml).

## Research

Gate: docs/superpowers/research/2026-09-17-models-and-case-studies-research.md (verdict: brief-covered).

- https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/docs/superpowers/research/2026-09-17-models-and-case-studies-research.md
- https://github.com/MBSE4U/PLEML (ESTABLISHED add: MBPLE examples, `PLEML.sysml` plus drone product-line `Examples/*.sysml`, last push 2026-06-14, not archived)
- https://github.com/airbus/apollo-11-sysml-v2 (baseline Apollo-class entry kept under the renamed section)
- https://github.com/Systems-Modeling/SysML-v2-Release (reject for re-listing here; already under Official Implementations)

Research decisions locked into the spec and honored by this plan: add PLEML only, keep all nine baseline entries, keep both structured-use-cases listings (b-13 open), no Case studies / Learning packs H3 split this pass, one H2, one alphabetical bucket.

## Codebase context

Live-checked at plan time against the pinned baseline (HEAD b3d842e):

- README.md:3 tagline, README.md:13 TOC line, README.md:76 `## Example Models`, nine entries at README.md:78-86 already alphabetical by link text. The section sits between `## Validation and Analysis` and `## Learning Resources` in both the TOC and the body.
- README lowercase `example models` baseline count is 2: the tagline (line 3) and the SYSMOD entry (line 83). Masterclass (79) and Book-examples (84) use capitalized `Example models` and are not matched by the lowercase grep. After the tagline edit and the PLEML insert the count stays 2 (SYSMOD + PLEML), which is exactly acceptance criterion 3.
- `grep -n "Example Models" README.md docs/index.html` baseline: README.md:13, README.md:76, docs/index.html:83. Nothing else.
- docs/index.html lowercase `example models` baseline count is 6: lines 8, 17, 23, 33 (shared description string), 60 (hero), 66 (what-it-is). Line 83 uses the capitalized label.
- docs/index.html is dirty in the working tree with an unrelated, self-contained social-card hunk (og:image sizes, twitter:card large, twitter:image), and docs/social-card.png plus docs/social-card.jpg are untracked. This is finished companion-site work that was never committed. Task 1 commits it first so the rename commit stays clean. The hunk does not overlap any string this plan edits.
- contributing.md binds entry format (one line, alpha by link text, one factual sentence) but names no section titles, so the rename needs no contributing.md edit (spec out-of-scope item).
- CHANGELOG.md Unreleased: Added holds three bullets ending `- Maintenance and contribution guidance: contributing guide, backlog, review records (P4).`; Changed holds three bullets ending `- Repository made public (P1).`; Fixed follows.
- docs/superpowers/runbooks/awesome-submission.md:53 holds the differentiation sentence; line 10 records a historical `gh repo view` description and stays.
- Lint config `.markdownlint-cli2.jsonc` disables only MD013; no section-name allowlist exists, so the rename cannot break lint.

## File structure

- README.md (modify): tagline, TOC line, H2, one inserted entry. Four hunks.
- docs/index.html (modify): four shared description strings, hero string, what-it-is string, category row (href fragment, label, blurb). Seven changed lines (numstat 7/7).
- CHANGELOG.md (modify): two appended bullets, one under Added, one under Changed.
- docs/superpowers/runbooks/awesome-submission.md (modify): one sentence in the line 53 differentiation step.
- No new files. No workflow changes. No contributing.md change.

---

## Task 1: Pre-flight gate and social-card split commit

**Files:** none modified by the rename. Commit 0 stages pre-existing companion-site leftovers only.

**Interfaces:**
- Consumes: the repo at the pinned baseline.
- Produces: a clean working tree for README.md, docs/index.html, CHANGELOG.md, contributing.md, and the runbook, so Tasks 2-5 diff output is exactly the rename. If any check fails, STOP and report the actual state; do not start Task 2.

**Model:** flash

- [ ] **Step 1: Verify HEAD and clean state of the untouched files**

Run:
```bash
git rev-parse HEAD
git status --porcelain README.md CHANGELOG.md contributing.md docs/superpowers/runbooks/awesome-submission.md
```
Expected: HEAD is `b3d842e8bfb84f3967ed7417cd6bae31e7ace8f1` (if different, proceed only if Steps 4-6 still match); porcelain output is empty for all four paths.

- [ ] **Step 2: Verify the docs/index.html dirty state is exactly the social-card hunk**

Run:
```bash
git status --porcelain docs/index.html docs/social-card.png docs/social-card.jpg
```
Expected, exactly three lines:
```
 M docs/index.html
?? docs/social-card.jpg
?? docs/social-card.png
```
If the output is empty instead (the social-card work was already committed elsewhere), skip Step 3. If it shows anything else, STOP and report.

- [ ] **Step 3: Commit the pre-existing social-card work (commit 0)**

Only if Step 2 showed the dirty state. Run:
```bash
git add docs/index.html docs/social-card.png docs/social-card.jpg
git commit -m "Add social card image and meta tags"
git status --porcelain docs/index.html docs/social-card.png docs/social-card.jpg
```
Expected: commit succeeds; the follow-up porcelain output is empty.

- [ ] **Step 4: Verify the Example Models surfaces at baseline**

Run:
```bash
grep -n "Example Models" README.md docs/index.html
```
Expected: exactly three lines, README.md:13 (TOC), README.md:76 (H2), docs/index.html:83 (category row).

- [ ] **Step 5: Verify lowercase and baseline counts**

Run:
```bash
grep -c "example models" README.md
grep -c "example models" docs/index.html
awk '/^## Example Models/{f=1;next} /^## /{f=0} f&&/^- \[/{n++} END{print n}' README.md
grep -c "MBSE4U/PLEML" README.md CHANGELOG.md
grep -c "curates tools, example models, and learning resources" docs/superpowers/runbooks/awesome-submission.md
```
Expected: `2` (tagline + SYSMOD), `6`, `9`, `0` and `0`, `1`.

- [ ] **Step 6: Verify Flashlight and both structured-use-cases entries are present before edits**

Run:
```bash
grep -c "Flashlight" README.md
grep -c "doug-rosenberg/structured-use-cases" README.md
grep -c "Open-MBEE/structured-use-cases" README.md
grep -n "SysML-v2-Release" README.md
```
Expected: `1`, `1`, `1`; exactly one SysML-v2-Release hit, under `## Official Implementations` (README.md:34).

Done when: all checks match and the working tree is clean for the four rename targets. Any mismatch: STOP, report the actual state, and await parent instruction.

## Task 2: README.md rename and PLEML insert

**Files:**
- Modify: `README.md` (lines 3, 13, 76, and one insert between 82 and 83)

**Interfaces:**
- Consumes: baseline state verified in Task 1.
- Produces: H2 `## Models and Case Studies`, TOC `- [Models and Case Studies](#models-and-case-studies)`, ten alphabetical entries. Task 3's category href fragment and Task 5's lint run depend on this task.

**Model:** flash (complete edits below; mechanical transcription)

- [ ] **Step 1: Edit the tagline (line 3)**

old_string:
```
A curated list of OMG SysML v2 tools, example models, and learning resources.
```
new_string:
```
A curated list of OMG SysML v2 tools, models and case studies, and learning resources.
```

- [ ] **Step 2: Edit the TOC line (line 13)**

old_string:
```
- [Example Models](#example-models)
```
new_string:
```
- [Models and Case Studies](#models-and-case-studies)
```

- [ ] **Step 3: Edit the H2 (line 76)**

old_string:
```
## Example Models
```
new_string:
```
## Models and Case Studies
```

- [ ] **Step 4: Insert the PLEML entry between its alphabetical neighbors**

Key on the two neighbor lines, not on line numbers. old_string:
```
- [MBSE4U/dont-panic-batmobile](https://github.com/MBSE4U/dont-panic-batmobile) - Batmobile example model from the Don't Panic beginners' guide to SysML v2.
- [MBSE4U/sysmod-sysmlv2](https://github.com/MBSE4U/sysmod-sysmlv2) - SYSMOD language extension for SysML v2 with example models.
```
new_string:
```
- [MBSE4U/dont-panic-batmobile](https://github.com/MBSE4U/dont-panic-batmobile) - Batmobile example model from the Don't Panic beginners' guide to SysML v2.
- [MBSE4U/PLEML](https://github.com/MBSE4U/PLEML) - MBPLE (model-based product line engineering) example models in SysML v2.
- [MBSE4U/sysmod-sysmlv2](https://github.com/MBSE4U/sysmod-sysmlv2) - SYSMOD language extension for SysML v2 with example models.
```

- [ ] **Step 5: Verify the README edits**

Run:
```bash
grep -n "Example Models" README.md; grep -n "#example-models" README.md
grep -c "example models" README.md
grep -c '^## Models and Case Studies$' README.md
grep -c '^## ' README.md
awk '/^## Models and Case Studies/{f=1;next} /^## /{f=0} f&&/^- \[/{n++} END{print n}' README.md
awk '/^## Models and Case Studies/{f=1;next} /^## Learning Resources/{f=0} f&&/^###/{print}' README.md
grep -cF -- '- [MBSE4U/PLEML](https://github.com/MBSE4U/PLEML) - MBPLE (model-based product line engineering) example models in SysML v2.' README.md
grep -A1 "MBSE4U/dont-panic-batmobile" README.md
grep -B1 "MBSE4U/sysmod-sysmlv2" README.md
grep -n "SysML-v2-Release" README.md
grep -n '^- \[' README.md | sed -n '6,8p'
git diff --numstat README.md
```
Expected, in order: both greps print nothing (exit 1, zero matches); `2` (SYSMOD + PLEML lines); `1`; `13` (no new H2); `10` entries; no H3 lines printed; `1` for the exact PLEML line; the line after dont-panic-batmobile is the PLEML line; the line before sysmod-sysmlv2 is the PLEML line; exactly one SysML-v2-Release hit (README.md:34); TOC lines 12-14 read Validation and Analysis, Models and Case Studies, Learning Resources; diff is `4	3` (four added lines: tagline, TOC, H2, PLEML; three removed).

No commit yet. The final commit in Task 5 keeps the TOC+H2 pair and the site sync in one commit (spec requirements 1 and 10).

## Task 3: docs/index.html sync

**Files:**
- Modify: `docs/index.html` (lines 8, 17, 23, 33, 60, 66, 83)

**Interfaces:**
- Consumes: Task 2's anchor `#models-and-case-studies`.
- Produces: the companion site pointing at the new anchor with updated copy. Acceptance criteria 2, 10, and 15 verify this task fully; AC 1's docs/index.html half is verified here and the README half in Task 2/5.

**Model:** flash (complete edits below; mechanical transcription)

- [ ] **Step 1: Replace the shared description string (four occurrences, lines 8, 17, 23, 33)**

Replace all occurrences of:
```
tooling, example models, and learning material
```
with:
```
tooling, models and case studies, and learning material
```
Exactly four occurrences exist (meta description, og:description, twitter:description, JSON-LD description). The line 66 string does not contain this substring (`learning resources`, not `learning material`), so a replace-all of the substring is safe.

- [ ] **Step 2: Edit the hero paragraph (line 60)**

old_string:
```
libraries, example models, and learning material
```
new_string:
```
libraries, models and case studies, and learning material
```

- [ ] **Step 3: Edit the what-it-is paragraph (line 66)**

old_string:
```
validation tooling, example models, learning resources
```
new_string:
```
validation tooling, models and case studies, learning resources
```

- [ ] **Step 4: Edit the category row (line 83)**

old_string (full line, 8-space indent):
```
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#example-models">Example Models</a></td><td>Working SysML v2 models to learn from and build on.</td></tr>
```
new_string (keep the absolute blob URL prefix; only the fragment, label, and blurb change):
```
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#models-and-case-studies">Models and Case Studies</a></td><td>Working SysML v2 models and case studies to learn from and build on.</td></tr>
```

- [ ] **Step 5: Verify the docs/index.html edits**

Run:
```bash
grep -n "example models" docs/index.html; grep -n "Example Models" docs/index.html; grep -n "#example-models" docs/index.html
grep -c 'tooling, models and case studies, and learning material' docs/index.html
grep -c 'libraries, models and case studies, and learning material' docs/index.html
grep -c 'validation tooling, models and case studies, learning resources' docs/index.html
grep -cF 'README.md#models-and-case-studies">Models and Case Studies</a></td><td>Working SysML v2 models and case studies to learn from and build on.</td></tr>' docs/index.html
git diff --numstat docs/index.html
```
Expected: the three greps print nothing (exit 1, zero matches); `4`; `1`; `1`; `1`; diff is `7	7` (seven changed lines: four shared description, hero, what-it-is, category row; none of the social-card lines from commit 0). If the numstat shows a whole-file rewrite (hundreds of lines), the editor wrote CRLF line endings: run `dos2unix docs/index.html` (or `sed -i 's/\r$//' docs/index.html`) and re-check.

No commit yet; Task 5 commits all four files together.

## Task 4: CHANGELOG.md and runbook sentence

**Files:**
- Modify: `CHANGELOG.md` (append one bullet under Added, one under Changed)
- Modify: `docs/superpowers/runbooks/awesome-submission.md` (line 53 differentiation sentence)

**Interfaces:**
- Consumes: baseline CHANGELOG Unreleased terminal bullets from Codebase context (re-confirm those exact strings before editing if the file may have drifted); runbook line 53 string.
- Produces: the two exact Unreleased bullets required by acceptance criterion 11 and the updated runbook sentence for criterion 13.

**Model:** flash (complete edits below; mechanical transcription)

- [ ] **Step 1: Append the Added bullet**

old_string:
```
- Maintenance and contribution guidance: contributing guide, backlog, review records (P4).

### Changed
```
new_string:
```
- Maintenance and contribution guidance: contributing guide, backlog, review records (P4).
- MBSE4U/PLEML SysML v2 model pack entry.

### Changed
```

- [ ] **Step 2: Append the Changed bullet**

old_string:
```
- Repository made public (P1).

### Fixed
```
new_string:
```
- Repository made public (P1).
- Example Models section renamed to Models and Case Studies.

### Fixed
```

- [ ] **Step 3: Edit the runbook differentiation sentence (line 53)**

old_string:
```
Awesome SysML V2 curates tools, example models, and learning resources for OMG SysML v2 specifically.
```
new_string:
```
Awesome SysML V2 curates tools, models and case studies, and learning resources for OMG SysML v2 specifically.
```
Line 10 (the historical `gh repo view` snapshot) stays byte-identical.

- [ ] **Step 4: Verify both files**

Run:
```bash
grep -A1 -- '- Maintenance and contribution guidance' CHANGELOG.md
grep -A1 -- '- Repository made public' CHANGELOG.md
grep -c "curates tools, models and case studies, and learning resources" docs/superpowers/runbooks/awesome-submission.md
grep -n "example models" docs/superpowers/runbooks/awesome-submission.md
git diff --numstat CHANGELOG.md docs/superpowers/runbooks/awesome-submission.md
```
Expected: the PLEML bullet is the line after the Added block end; the rename bullet is the line after the Changed block end; `1`; exactly one hit at line 10 (the historical snapshot, unchanged); diff is `2	0` for CHANGELOG.md and `1	1` for the runbook.

## Task 5: Full acceptance sweep and commit

**Files:** none modified (unless a sweep check fails and needs a fix). Commit covers the four rename files.

**Interfaces:**
- Consumes: Tasks 2-4 outputs.
- Produces: the single commit that satisfies spec requirements 1 (TOC+H2 same commit) and 10 (site row same change), plus the green lint run required by requirement 15.

**Model:** flash

- [ ] **Step 1: Run the acceptance sweep**

Run (absence checks use count wrappers so exit status stays 0 under `set -e`):
```bash
test "$(grep -c "Example Models" README.md docs/index.html || true)" = "0"
test "$(grep -c "#example-models" README.md docs/index.html || true)" = "0"
test "$(grep -c "example models" docs/index.html || true)" = "0"
test "$(grep -c "example models" README.md)" = "2"
sed -n '3p' README.md
test "$(grep -c '^## Models and Case Studies$' README.md)" = "1"
test "$(grep -cF -- '- [Models and Case Studies](#models-and-case-studies)' README.md)" = "1"
test "$(awk '/^## Models and Case Studies/{f=1;next} /^## /{f=0} f&&/^- \[/{n++} END{print n+0}' README.md)" = "10"
test "$(grep -cF -- '- [MBSE4U/PLEML](https://github.com/MBSE4U/PLEML) - MBPLE (model-based product line engineering) example models in SysML v2.' README.md)" = "1"
grep -A1 -- 'dont-panic-batmobile' README.md | grep -F 'MBSE4U/PLEML'
grep -B1 -- 'MBSE4U/sysmod-sysmlv2' README.md | grep -F 'MBSE4U/PLEML'
test "$(grep -c "SysML-v2-Release" README.md)" = "1"
test "$(grep -c "doug-rosenberg/structured-use-cases" README.md)" = "1"
test "$(grep -c "Open-MBEE/structured-use-cases" README.md)" = "1"
test "$(grep -c "Flashlight" README.md)" = "1"
test "$(grep -c '^## Projects' README.md || true)" = "0"
test -z "$(awk '/^## Models and Case Studies/{f=1;next} /^## Learning Resources/{f=0} f&&/^###/{print}' README.md)"
test -z "$(git diff --stat origin/main -- contributing.md 2>/dev/null || git diff --stat main -- contributing.md 2>/dev/null || true)"
test "$(grep -c "curates tools, models and case studies, and learning resources" docs/superpowers/runbooks/awesome-submission.md)" = "1"
test "$(grep -c "example models" docs/superpowers/runbooks/awesome-submission.md)" = "1"
test "$(grep -cF -- '- MBSE4U/PLEML SysML v2 model pack entry.' CHANGELOG.md)" = "1"
test "$(grep -cF -- '- Example Models section renamed to Models and Case Studies.' CHANGELOG.md)" = "1"
test "$(grep -cF 'README.md#models-and-case-studies">Models and Case Studies</a></td><td>Working SysML v2 models and case studies to learn from and build on.</td></tr>' docs/index.html)" = "1"
test "$(grep -c 'tooling, models and case studies, and learning material' docs/index.html)" = "4"
test "$(grep -c 'libraries, models and case studies, and learning material' docs/index.html)" = "1"
test "$(grep -c 'validation tooling, models and case studies, learning resources' docs/index.html)" = "1"
```
Expected: every `test` exits 0; neighbor greps each show the PLEML line; `sed -n '3p'` prints the new tagline; runbook still has exactly one residual `example models` (historical line 10). Covers AC 1-15 including AC6 exact PLEML, AC10 full category row, and AC15 positives.

- [ ] **Step 2: Run the lint gates**

Run:
```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```
Expected: both exit 0 with no error output (AC 14, spec requirement 15).

- [ ] **Step 3: Commit the four files (the single rename commit)**

Run:
```bash
git add README.md docs/index.html CHANGELOG.md docs/superpowers/runbooks/awesome-submission.md
git commit -m "Rename Example Models to Models and Case Studies and add PLEML"
```

- [ ] **Step 4: Verify the commit shape**

Run:
```bash
git show --stat HEAD
git status --porcelain README.md docs/index.html CHANGELOG.md docs/superpowers/runbooks/awesome-submission.md contributing.md
```
Expected: `git show --stat` lists exactly four files (README.md, docs/index.html, CHANGELOG.md, docs/superpowers/runbooks/awesome-submission.md) and no contributing.md; porcelain output is empty. Do not push; the parent owns the push.

Done when: the sweep is green, both lint commands exit 0, and the commit contains exactly the four files.
