# GitHub Notice Surface (P3) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create `docs/superpowers/runbooks/awesome-submission.md`, a maintainer-facing discoverability checklist plus sindresorhus/awesome submission-readiness runbook, verified against live repo state, as the single new file of work package P3.

**Architecture:** One markdown deliverable in the `docs/superpowers/` process tree, sibling to `specs/`, `plans/`, `research/`, `context/`, `packages/`, `reviews/`. The checklist (Section A) and the three-gates runbook (Sections B through E) live in one file so the maintainer updates a single document as gates clear. No pointer to the file from README.md or contributing.md (spec Decision 3). All content is fixed by the spec; execution adds only live re-verification and one commit.

**Tech Stack:** Markdown, git, GitHub CLI (`gh`), `python ~/.zcode/scripts/prose_check.py`.

**Spec:** docs/superpowers/specs/2026-09-16-github-notice-surface.md

## Global Constraints

- Exactly one new repo file: `docs/superpowers/runbooks/awesome-submission.md`. No other file is created or modified.
- No commits before Task 4. Task 4 stages exactly the runbook file and commits with message exactly `Add awesome submission readiness runbook`. Nothing is pushed at any point (no `git push`).
- README.md, contributing.md, `.github/`, all workflows, and entry content are untouched (AC 3).
- The runbook contains no submit-now instruction and no promised dates. Gate 2 records "no promised reopen date". Guard step 9 ("Do not submit until steps 1 through 8 hold") is present (AC 4).
- Upstream requirements are quoted verbatim with a source URL next to each quote (AC 5).
- Zero em dashes anywhere in the new file. It must pass `python ~/.zcode/scripts/prose_check.py docs/superpowers/runbooks/awesome-submission.md` with no unexplained findings (AC 8).
- `docs/superpowers/` is currently fully UNTRACKED in this repo (`git status` shows a single `?? docs/superpowers/` entry). Task 4 tracks only the runbook file; every other path under `docs/superpowers/` stays untracked.
- All commands run from the repo root: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2` (in Git Bash: `/c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2`).
- Live-verification evidence is recorded in the execution run report returned to the parent, never in a new file (AC 3 forbids a second file).

## Codebase context

Verified live by the plan author against HEAD `de549d941b3801d3c0abaea853b9620b1f0ec984` ("Add companion docs site", committed 2026-09-16 16:36:30 +0100):

- 7 unpushed commits on the local branch relative to `origin/main` (`git log origin/main..HEAD --oneline | wc -l` = 7). backlog.md:24 tracks b-18, the push that unblocks Pages, homepageUrl, and the live-200 check.
- `git status --short` shows exactly `?? docs/superpowers/`; the whole tree is untracked. `docs/superpowers/runbooks/` does not exist yet. Existing siblings: `backlog.md`, `context/`, `packages/`, `plans/`, `research/`, `reviews/`, `specs/`.
- `gh repo view jgsystemsconsulting/awesome-sysml-v2 --json isPrivate,description,repositoryTopics,homepageUrl,createdAt`: `isPrivate` false; description `"A curated list of OMG SysML v2 tools, example models, and learning resources"`; topics `awesome, awesome-list, mbse, sysml, sysml-v2` (5); `homepageUrl` `""` (empty); `createdAt` `2026-09-15T20:37:50Z`.
- Workflows (`.github/workflows/`): `links.yml`, `lint.yml`, `stale.yml`; `gh workflow list` shows Links, Lint, Freshness report, all `active`. `lint.yml` line 29: `run: npx awesome-lint@2.3.0 README.md`.
- README.md line 1: `# Awesome SysML V2 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)`.
- `~/.zcode/scripts/prose_check.py` exists.

## Research

Carried ESTABLISHED from docs/superpowers/research/2026-09-16-github-notice-surface-research.md (all primary, retrieved 2026-09-16):

- https://raw.githubusercontent.com/sindresorhus/awesome/main/create-list.md (30-day age, review 4 PRs, unicorn comment, duplicate search)
- https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md (PR checklist verbatim: age, lint, slug, duplicate, effort, unmaintained; no-Awesome-in-title rule)
- https://raw.githubusercontent.com/sindresorhus/awesome/main/contributing.md (PR guidelines pointer)
- https://github.com/sindresorhus/awesome (PR intake temporarily disabled banner)
- https://github.com/sindresorhus/awesome/pulls?q=is%3Apr+is%3Aopen+add (~90 open add-PR backlog)
- https://github.com/sindresorhus/awesome/pull/4093 (AI-generated lists hard-reject)
- https://github.com/search?q=awesome+sysml&type=repositories (duplicate check: mycr0ft/awesome-sysml, v1-focused)
- https://github.com/topics/mbse (MBSE discovery concentration; alternative path)

---

### Task 1: Pre-flight gate and live re-verification

**Files:**
- None created or modified. Read-only checks; outputs recorded in the execution run report.

**Interfaces:**
- Consumes: nothing.
- Produces: the live-verified baseline values every later task and the runbook cells depend on (HEAD, unpushed count, isPrivate, description, topics, homepageUrl, workflow states, badge line, lint version). If any value diverges from the expected values below, Task 2 must use the live value and the divergence is named in the run report.

**Model:** flash

- [ ] **Step 1: Verify HEAD baseline**

Run: `git rev-parse HEAD && git log -1 --format=%s`
Expected: `de549d941b3801d3c0abaea853b9620b1f0ec984` and `Add companion docs site`.
If HEAD differs in any way: STOP. Report the actual HEAD and stop the run; the parent must re-baseline. Do not proceed on a moved baseline.

- [ ] **Step 2: Verify unpushed-commits baseline (b-18 state)**

Run: `git log origin/main..HEAD --oneline | wc -l`
Expected: `7`. If the count is not 7, the b-18 row in the runbook would be stale: STOP and report the actual count for the parent to re-baseline.

- [ ] **Step 3: Verify runbooks directory is absent**

Run: `test -d docs/superpowers/runbooks && echo EXISTS || echo ABSENT`
Expected: `ABSENT`.

- [ ] **Step 4: Live re-verify repo metadata with gh**

Run: `gh repo view jgsystemsconsulting/awesome-sysml-v2 --json isPrivate,description,repositoryTopics,homepageUrl,createdAt`
Expected: `isPrivate` `false`; description `"A curated list of OMG SysML v2 tools, example models, and learning resources"`; exactly 5 topics `awesome`, `awesome-list`, `mbse`, `sysml`, `sysml-v2`; `homepageUrl` `""`.

- [ ] **Step 5: Live re-verify workflows**

Run: `gh workflow list`
Expected: 3 rows, all `active`: Links, Lint, Freshness report.
Run: `grep -n "awesome-lint" .github/workflows/lint.yml`
Expected: a line matching `npx awesome-lint@2.3.0 README.md`.

- [ ] **Step 6: Live re-verify badge line**

Run: `head -1 README.md`
Expected: `# Awesome SysML V2 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)`

- [ ] **Step 7: Record the run report**

Record every actual output of Steps 1-6 in the execution run report (the final message to the parent), labeling each against its expected value. Do not write any file.

**Done when:** all six checks match the expected values (or divergences are reported and the run stopped per Step 1/2 rules); the run report lists each live value with its check; zero files created or modified.

---

### Task 2: Write the runbook

**Files:**
- Create: `docs/superpowers/runbooks/awesome-submission.md`

**Interfaces:**
- Consumes: the live baseline values from Task 1 (expected to match the snapshot values already written into the content below).
- Produces: the single deliverable file; Task 3 verifies it and Task 4 commits it.

**Model:** flash

- [ ] **Step 1: Create the directory**

Run: `mkdir -p docs/superpowers/runbooks`

- [ ] **Step 2: Write the file with exactly this content**

Use the Write tool (or an equivalent single write) so the content lands byte-for-byte. If Task 1 found a live divergence in description text, topics, badge line, lint version, or homepageUrl state, update only the affected cells to the live values before writing and name the change in the run report. If homepageUrl became non-empty, the b-18 row flips from Pending to Done with the live evidence; the Step 2 STOP rule in Task 1 makes this case unlikely.

````markdown
# Awesome Submission Runbook

Scope: discoverability checklist and sindresorhus/awesome submission-readiness record for this repo, snapshotted 2026-09-16 against HEAD de549d9. Every row and gate in this file is a dated snapshot, not a live fact. Re-verify against the repo and upstream before acting on anything here.

## Section A: Repo discoverability state (checklist)

| Item | Status as of 2026-09-16 | Evidence or blocker |
|---|---|---|
| Public visibility | Done | `gh repo view`: isPrivate false |
| Description set | Done | "A curated list of OMG SysML v2 tools, example models, and learning resources" (`gh repo view`) |
| Topics (5) | Done | awesome, awesome-list, mbse, sysml, sysml-v2 (`gh repo view`) |
| Awesome badge present | Done, badge chrome only | README.md line 1 links to awesome.re. The badge is decoration; it is not a sindresorhus listing. Listing means an entry in the sindresorhus/awesome readme.md Contents. |
| awesome-lint clean | Done, CI enforced | `.github/workflows/lint.yml` runs `awesome-lint@2.3.0` on README.md on every push to main and every PR to main |
| Companion site live and homepageUrl set | Pending | Blocked on b-18: 7 unpushed commits (HEAD de549d9) sit on the local branch; Pages, the repo homepage field, and a live-200 check wait for that push. `docs/superpowers/backlog.md:24` tracks b-18. |
| Listed in sindresorhus/awesome | Pending | Three gates, none in repo control. See Section B. |

## Section B: Submission gates (as of 2026-09-16)

### Gate 1: List age (open; clears by waiting)

Upstream requirement, quoted verbatim from create-list.md: "Wait at least 30 days after creating a list before submitting it, to give it a chance to mature"

Source: https://raw.githubusercontent.com/sindresorhus/awesome/main/create-list.md

This list was created 2026-09-15, so the earliest possible submission is on or after 2026-10-15. Note: the PR template's wording is "Has been around for at least 30 days", so the safe date is 2026-10-16 if the count is read strictly. If a 2026-10-15 submission draws an age objection, wait one day and resubmit.

### Gate 2: PR intake (blocked)

Upstream readme banner, quoted verbatim: "Pull requests are temporarily disabled until I have a chance to catch up with the existing ones"

Source: https://github.com/sindresorhus/awesome

Roughly 90 open add-PRs sit in the upstream backlog (retrieved 2026-09-16). No promised reopen date exists upstream. This runbook records no planned submission date. Recheck intake at https://github.com/sindresorhus/awesome before any submission attempt.

### Gate 3: Curation bar (blocked until the Section D claim is true)

Upstream hard-rejects AI-generated lists. From PR #4093, quoted verbatim: "AI generated lists are not accepted" and "There is no way for me to verify whether you just asked Claude to find more maps or you did it yourself"

Source: https://github.com/sindresorhus/awesome/pull/4093

The effort bar, quoted verbatim from pull_request_template.md: "If you have not put in considerable effort into your list, your pull request will be immediately closed"

Source: https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md

## Section C: Future PR steps (when all gates clear)

1. Confirm all three gates: date on or after 2026-10-15; intake reopened on sindresorhus/awesome; the Section D curation claim is true.
2. Review at least 4 other open PRs in sindresorhus/awesome.
3. Fork sindresorhus/awesome and create a branch.
4. Edit `readme.md`, Contents section: add the `Awesome SysML V2` entry under the fitting section. No SysML or MBSE section existed in the upstream Contents as of 2026-09-16 (provisional), so the maintainer picks the closest fit from the live Contents at submission time.
5. Title the PR exactly `Add SysML V2`. Upstream forbids the word Awesome in PR titles (pull_request_template.md bad example: `Add Awesome Swift`). The Contents entry name inside readme.md can still read `Awesome SysML V2`; only the PR title drops the word.
6. Complete the PR template checklist: list "has been around for at least 30 days"; reviewed at least 4 PRs; comment `unicorn` on your own PR; awesome-lint run and all reported issues fixed; repo slug in the lowercase `awesome-name-of-list` form (`awesome-sysml-v2`); not a duplicate.
7. For the not-duplicate item, include this differentiation sentence: "Unlike mycr0ft/awesome-sysml, which focuses on SysML v1, Awesome SysML V2 curates tools, example models, and learning resources for OMG SysML v2 specifically."
8. Hold the content bar: best-of curation only, no unmaintained, archived, or undocumented items, tight scope, and be ready to defend every entry in review.
9. Do not submit until steps 1 through 8 hold. This runbook records readiness; it does not schedule the submission.

## Section D: Curation statement

The submission is the maintainer's act. The build pipeline (specs, plans, research, and context rounds under `docs/superpowers/`) was tooling that assembled candidates; the claim upstream demands is personal curation by the human maintainer. Before any submission the maintainer must have personally read every entry, must be able to defend each inclusion, must drop any entry they cannot vouch for, and must write the PR text themselves. No AI-authored submission text.

## Section E: Alternative discovery paths

The list's value does not hinge on sindresorhus acceptance. MBSE discovery concentrates in the Systems-Modeling, Gaphor, and Open-MBEE ecosystem and on GitHub topics (https://github.com/topics/mbse), not the general awesome index. The repo already carries the mbse, sysml, and sysml-v2 topics. Community hubs, MBSE forums, and conference channels are viable regardless of the upstream outcome.
````

**Done when:** the file exists at `docs/superpowers/runbooks/awesome-submission.md` with all five `## Section` headings in order A, B, C, D, E; no other file changed (`git status --porcelain --untracked-files=all | grep -v '^?? docs/superpowers/'` prints nothing); `find docs/superpowers/runbooks -type f` lists exactly one file.

---

### Task 3: Verification

**Files:**
- Test (read-only): `docs/superpowers/runbooks/awesome-submission.md`

**Interfaces:**
- Consumes: the file from Task 2 and the run report values from Task 1.
- Produces: verified evidence for Task 4's commit and the parent's IVL step.

**Model:** flash

- [ ] **Step 1: Structure checks**

Run: `grep -n "^## Section" docs/superpowers/runbooks/awesome-submission.md`
Expected: exactly 5 lines, in order: Section A, Section B, Section C, Section D, Section E.
Run: `grep -c "^### Gate" docs/superpowers/runbooks/awesome-submission.md`
Expected: `3`.

- [ ] **Step 2: Content and quote checks (each grep must return the shown count)**

```bash
grep -c "Add SysML V2" docs/superpowers/runbooks/awesome-submission.md                 # expect 1 (step 5 title only)
grep -c "Add Awesome SysML V2" docs/superpowers/runbooks/awesome-submission.md         # expect 0
grep -Eic "submit now|submit today" docs/superpowers/runbooks/awesome-submission.md    # expect 0
grep -c "Wait at least 30 days after creating a list" docs/superpowers/runbooks/awesome-submission.md   # expect 1
grep -c "Pull requests are temporarily disabled until I have a chance to catch up with the existing ones" docs/superpowers/runbooks/awesome-submission.md   # expect 1
grep -c "AI generated lists are not accepted" docs/superpowers/runbooks/awesome-submission.md            # expect 1
grep -c "There is no way for me to verify whether you just asked Claude" docs/superpowers/runbooks/awesome-submission.md   # expect 1
grep -c "considerable effort into your list" docs/superpowers/runbooks/awesome-submission.md             # expect 1
grep -c "Unlike mycr0ft/awesome-sysml" docs/superpowers/runbooks/awesome-submission.md                   # expect 1
grep -c "Do not submit until steps 1 through 8" docs/superpowers/runbooks/awesome-submission.md          # expect 1
grep -c "| Listed in sindresorhus/awesome | Pending |" docs/superpowers/runbooks/awesome-submission.md   # expect 1
grep -c "badge chrome only" docs/superpowers/runbooks/awesome-submission.md             # expect 1
grep -c "b-18" docs/superpowers/runbooks/awesome-submission.md                          # expect >= 1
grep -ic "no promised reopen date" docs/superpowers/runbooks/awesome-submission.md      # expect 1 (content reads "No promised reopen date exists upstream.")
```

Note: `grep -c` exits 1 when the count is 0, so an expected-0 match is verified by reading the printed `0`, not the exit code.

- [ ] **Step 3: Source URLs present**

Run: `grep -c "^Source: https://" docs/superpowers/runbooks/awesome-submission.md`
Expected: `4` (create-list.md, awesome repo root, PR 4093, pull_request_template.md).

- [ ] **Step 4: Prose check**

Run: `python ~/.zcode/scripts/prose_check.py docs/superpowers/runbooks/awesome-submission.md`
Expected: no unexplained findings. Fix any finding in the runbook and rerun until clean. An em-dash finding is never acceptable: `grep -c "$(printf '\xe2\x80\x94')" docs/superpowers/runbooks/awesome-submission.md` must print `0`.

- [ ] **Step 5: Repo cleanliness**

Run: `git status --porcelain --untracked-files=all | grep -v '^?? docs/superpowers/' | wc -l`
Expected: `0` (no tracked file modified, nothing new outside `docs/superpowers/`).
Run: `find docs/superpowers/runbooks -type f | wc -l`
Expected: `1`.

**Done when:** every count matches its expected value; prose_check is clean; the cleanliness checks return the expected numbers. Any mismatch: fix the runbook (Task 2 content is the source of truth) and rerun Task 3 from Step 1. Do not commit in this task.

---

### Task 4: Commit the runbook

**Files:**
- Commit: `docs/superpowers/runbooks/awesome-submission.md` (staged and committed; the rest of `docs/superpowers/` stays untracked)

**Interfaces:**
- Consumes: the verified file from Task 3.
- Produces: the single P3 commit. Nothing pushed.

**Model:** flash

- [ ] **Step 1: Stage exactly the runbook**

```bash
git add docs/superpowers/runbooks/awesome-submission.md
git status --porcelain | grep '^A'
```

Expected: exactly one staged line, `A  docs/superpowers/runbooks/awesome-submission.md`.

- [ ] **Step 2: Commit**

```bash
git commit -m "Add awesome submission readiness runbook"
```

Expected: commit succeeds; no pre-commit hook output blocking it. If a hook fails, fix only the runbook file, restage, and recommit with the same message.

- [ ] **Step 3: Post-commit verification**

```bash
git log -1 --format=%s
git show --name-only --format="" HEAD | wc -l
git log origin/main..HEAD --oneline | wc -l
git status --porcelain --untracked-files=all | grep -v '^?? docs/superpowers/' | wc -l
```

Expected, in order: `Add awesome submission readiness runbook`; `1` (the commit touches exactly the runbook file); `8` (the 7 baseline unpushed commits plus this one; the runbook's "7 unpushed commits (HEAD de549d9)" row stays as written because it is the dated 2026-09-16 snapshot, and the scope line says to re-verify); `0` (nothing else modified; the rest of `docs/superpowers/` still untracked).
Confirm nothing was pushed: run `git status -sb` and verify the branch is ahead of origin by the count above with no upstream divergence, and that no `git push` was run in this plan.

**Done when:** the commit exists with the exact message, touches exactly `docs/superpowers/runbooks/awesome-submission.md`, the working tree is otherwise untouched, and nothing has been pushed. Report the commit hash in the run report.
