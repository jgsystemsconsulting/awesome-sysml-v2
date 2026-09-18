# Freshness Job Truth (P6) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the monthly Freshness report job survive per-repo GitHub API failures (non-fatal fetch, counted skips, honest skip note) and enforce exactly one freshness window, 24 months, matching contributing.md criterion 4.

**Architecture:** One file changes: `.github/workflows/stale.yml`. The run block of the "Build freshness report" step is replaced wholesale with the spec's after-state: `|| true` on the curl/jq pipeline (D1), a `skipped` counter plus a skip note emitted last (D2), 24-month strings in cutoff, header, and footer (D3), and one advisory clause in the header (D4). Verification runs the extracted script body in a temp dir against a stubbed `curl`, then checks window greps, YAML parse, and diff scope. One commit lands at the end.

**Tech Stack:** GitHub Actions workflow YAML, bash (`set -euo pipefail`), curl, jq, GNU date, Python (yaml.safe_load) or actionlint, git.

**Spec:** C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-freshness-job-truth.md

## Global Constraints

- Baseline commit: `1747fa6` (full hash `1747fa6d4f5d7c89dbe25884e2456da0098751f5`). If HEAD differs, stop and report before touching anything.
- The only file any task may modify is `.github/workflows/stale.yml`.
- No task may touch `links.yml`, `lint.yml`, `README.md`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`, or any other file. `contributing.md` stays byte-identical: `git diff --exit-code -- contributing.md` must pass after every task.
- No commit before Task 4. Exactly one commit, staging exactly `.github/workflows/stale.yml`.
- Commit message, exact string: `Make freshness job failures non-fatal and sync 24-month window`. This plan never pushes.
- Within stale.yml, unchanged surfaces: workflow name (`name: Freshness report`), the P9 pin comment block (lines 2-7), `on:` (cron `0 6 1 * *` plus `workflow_dispatch`), the `permissions:` block, the checkout pin (`actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4`), the URL grep charset (`https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+`), the cutoff comparison (`[[ "$pushed" < "$cutoff" ]]`), and the entire second step ("Create or update the issue").
- The freshness window is 24 months, sourced from contributing.md:10 criterion 4. contributing.md is the policy source and never changes in this plan.
- Match quoted text, never line numbers. The 2026-09-15 findings doc cites pre-P9 line numbers that have drifted; the quoted strings in this plan and the spec are the source of truth.
- Task 3 scratch files (extracted script, curl stub, fixture README) live only under `mktemp -d` directories. Nothing from Tasks 1-3 is committed, staged, or added to the repo.

## Codebase context

From docs/superpowers/context/2026-09-16-freshness-job-truth-context.md (HEAD 1747fa6, verified at plan time):

- Abort mechanism: `set -euo pipefail` opens the run block; the fetch `pushed=$(curl -sf ... | jq -r ".pushed_at // empty")` sits in command substitution. Under pipefail, any curl transport failure (exit 22 with `-f`, or 6/7/28 on network faults) or jq failure (exit 2 on non-JSON) is nonzero, and `set -e` kills the step before the `[ -n "$pushed" ] || continue` skip line can run. One flaky repo means no report that month.
- Window drift: three strings carry 12 months (cutoff math, report header, footer threshold) while contributing.md:10 criterion 4 already reads "commit within 24 months".
- Policy shape: criterion 4 is an OR. Stale-but-foundational repos (formal specs, canonical references) stay valid, so the report must read as advisory.
- House pattern for expected failure: links.yml uses `fail: false`. This spec uses the shell-native `|| true` instead; no new workflow constructs.
- Current stale.yml run block (verified verbatim at HEAD 1747fa6): `set -euo pipefail` at line 27, 12-month cutoff at line 28, 12-month header echo at line 30, `found=0` at line 33, curl fetch at line 36, `[ -n "$pushed" ] || continue` at line 37, 12-month footer at line 44. Re-verify by quote, not by number.

## Research

research: skipped (no-open-world-questions; all facts are repo-internal)

Track 3 halt at round 0, predicate no-open-world-questions: the fix is internal to stale.yml plus a window number that contributing.md already fixes. Round log: docs/superpowers/research/2026-09-16-freshness-job-truth-research-log.md. Context doc: docs/superpowers/context/2026-09-16-freshness-job-truth-context.md.

---

### Task 1: Pre-flight gate

**Files:**
- Read only: `.github/workflows/stale.yml`, `contributing.md`. No edits in this task.

**Interfaces:**
- Consumes: nothing.
- Produces: confirmation that the workspace matches the spec baseline, so Task 2's old_string is guaranteed to match.

**Model:** flash

- [ ] **Step 1: Verify HEAD is the baseline commit**

Run from the repo root (`C:/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2`):

```bash
[ "$(git rev-parse HEAD)" = "1747fa6d4f5d7c89dbe25884e2456da0098751f5" ] && echo "HEAD OK" || echo "HEAD MOVED: $(git rev-parse HEAD)"
```

Expected: `HEAD OK`. If HEAD moved, stop the whole plan and report; do not edit on a drifted baseline.

- [ ] **Step 2: Verify no tracked modifications in the blast-radius paths**

```bash
git status --porcelain -- .github/workflows README.md contributing.md
```

Expected: empty output. (`git status --porcelain` overall may show untracked `?? docs/`; that is the superpowers docs tree and is expected.)

- [ ] **Step 3: Quote-match the before-lines in stale.yml**

This is a quote-match, deliberately not a line-number match (line-drift gotcha in the spec's Risk section):

```bash
for s in \
  'set -euo pipefail' \
  'cutoff=$(date -u -d "12 months ago" +%Y-%m-%dT%H:%M:%SZ)' \
  'echo "Entries with no push in over 12 months (as of $(date -u +%Y-%m-%d)):"' \
  'pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty")' \
  '[ -n "$pushed" ] || continue' \
  'echo "No entries exceeded the 12-month threshold." >> freshness-report.md' \
; do grep -Fq "$s" .github/workflows/stale.yml || { echo "MISSING: $s"; exit 1; }; done && echo "BEFORE-LINES OK"
```

Expected: `BEFORE-LINES OK`. Any `MISSING:` line means the file drifted from the spec; stop and report.

- [ ] **Step 4: Confirm the policy source is already at 24 months**

```bash
grep -n "commit within 24 months" contributing.md
```

Expected: exactly one hit, on contributing.md criterion 4 (currently line 10).

- [ ] **Step 5: Confirm the workflows directory contains only the three known files**

```bash
ls .github/workflows/
```

Expected exactly: `links.yml`, `lint.yml`, `stale.yml`. Any fourth file is out of baseline; stop and report.

Done when: HEAD OK, clean status on the blast-radius paths, all six before-lines quote-matched, criterion 4 confirmed at 24 months, workflows dir matches baseline.

### Task 2: Apply the run-block edits to stale.yml

**Files:**
- Modify: `.github/workflows/stale.yml`, the run block of the "Build freshness report" step (the block between the `run: |` line and the `- name: Create or update the issue` line). Current content spans lines 27-45; verify by quote, not line number.

**Interfaces:**
- Consumes: Task 1's confirmation that the old block matches verbatim.
- Produces: stale.yml whose "Build freshness report" run block equals the spec's after-state exactly. Task 3 and Task 4 verify and commit that file.

**Model:** flash

- [ ] **Step 1: Replace the run block with the spec's after-state**

Using the Edit tool, replace the entire block below (the old block, YAML-indented exactly as in the file, from `set -euo pipefail` through the `fi` that closes the `found` check) with the new block beneath it. This is one single edit; do not edit line by line.

Old block (exact current content, 10-space YAML indent for block body):

```yaml
          set -euo pipefail
          cutoff=$(date -u -d "12 months ago" +%Y-%m-%dT%H:%M:%SZ)
          {
            echo "Entries with no push in over 12 months (as of $(date -u +%Y-%m-%d)):"
            echo
          } > freshness-report.md
          found=0
          for url in $(grep -oE "https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+" README.md | sort -u); do
            repo=$(printf '%s' "${url#https://github.com/}" | cut -d/ -f1-2)
            pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty")
            [ -n "$pushed" ] || continue
            if [[ "$pushed" < "$cutoff" ]]; then
              echo "- [$repo]($url) - last push $pushed" >> freshness-report.md
              found=1
            fi
          done
          if [ "$found" -eq 0 ]; then
            echo "No entries exceeded the 12-month threshold." >> freshness-report.md
          fi
```

New block (the spec's after-state, same indentation; this is the only content the file may gain):

```yaml
          set -euo pipefail
          cutoff=$(date -u -d "24 months ago" +%Y-%m-%dT%H:%M:%SZ)
          {
            echo "Entries with no push in over 24 months (as of $(date -u +%Y-%m-%d)). Advisory only: entries meeting the foundational-value exception (contributing.md criterion 4) are still valid."
            echo
          } > freshness-report.md
          found=0
          skipped=0
          for url in $(grep -oE "https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+" README.md | sort -u); do
            repo=$(printf '%s' "${url#https://github.com/}" | cut -d/ -f1-2)
            pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty" || true)
            [ -n "$pushed" ] || { skipped=$((skipped+1)); continue; }
            if [[ "$pushed" < "$cutoff" ]]; then
              echo "- [$repo]($url) - last push $pushed" >> freshness-report.md
              found=1
            fi
          done
          if [ "$found" -eq 0 ]; then
            echo "No entries exceeded the 24-month threshold." >> freshness-report.md
          fi
          if [ "$skipped" -gt 0 ]; then
            echo "Skipped $skipped repos whose GitHub API data was unavailable; the entry list above may be incomplete or empty." >> freshness-report.md
          fi
```

Design decisions baked into this block, from the spec (do not deviate):

- D1: `|| true` applies to the whole `curl | jq` pipeline inside the substitution, so `set -e` never fires; `-sf` stays. The increment form is `skipped=$((skipped+1))`, never `((skipped++))`, because the arithmetic command form returns status 1 when the expression is 0 and would kill the script under `set -e` on the first increment.
- D2: `skipped=0` sits next to `found=0`; the skip-note `if` block comes after the `found` check so the note is the last thing the report says.
- D3: exactly three window strings, all 24: cutoff `"24 months ago"`, header "over 24 months", footer "24-month threshold".
- D4: the advisory clause lives once, appended to the header line. The footer stays factual.

- [ ] **Step 2: Edit-time sanity greps**

```bash
grep -nE "12 months|12-month" .github/workflows/stale.yml && echo "FAIL: 12-month strings remain" || echo "NO 12-MONTH STRINGS"
grep -cE "24 months|24-month" .github/workflows/stale.yml
grep -nF 'skipped=$((skipped+1))' .github/workflows/stale.yml
```

Expected: first command prints `NO 12-MONTH STRINGS`; second prints `3`; third shows the skip-increment line inside the run block.

- [ ] **Step 3: Confirm diff touches only stale.yml**

```bash
git diff --name-only
```

Expected output, exactly one line: `.github/workflows/stale.yml`

Done when: the run block equals the spec's after-state verbatim, no 12-month strings remain anywhere in stale.yml, exactly three 24-month strings exist, and the diff names only stale.yml.

### Task 3: Behavioral and scope verification

**Files:**
- Read only: `.github/workflows/stale.yml`, `contributing.md`. All artifacts go to a `mktemp -d` scratch dir; nothing is written into the repo.

**Interfaces:**
- Consumes: Task 2's edited stale.yml.
- Produces: recorded pass/fail for spec acceptance checks 1, 3, 4, 5, 6 (check 2 is runner-side, noted in Task 4 as post-merge manual verification).
- AC1 merge note: the spec's two failure variants (transport failure; non-JSON body) are exercised together in one mixed scan asserting a skip count of 2 — same mechanism, both failure classes covered.
- AC6 note: the shellcheck clause of acceptance check 6 is intentionally dropped (shellcheck is not guaranteed on the executor); `bash -n` and the arithmetic one-liner carry the check.

**Model:** standard

- [ ] **Step 1: Extract the run-block body and run bash -n on it**

Requires `jq` on PATH (the real one; the runner image has it, and Git Bash environments typically do too). If `command -v jq` fails, install jq locally before continuing; nothing is committed.

```bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRATCH="$(mktemp -d)"
command -v jq >/dev/null || { echo "jq is required"; exit 1; }
awk '/^      - name: Create or update the issue$/ { exit }
     /^        run: \|$/ { if (!seen) { seen=1; next } }
     seen { print }' \
  "$REPO_ROOT/.github/workflows/stale.yml" | sed 's/^          //' > "$SCRATCH/stale-run-body.sh"
[ "$(head -n 1 "$SCRATCH/stale-run-body.sh")" = "set -euo pipefail" ]
[ "$(tail -n 1 "$SCRATCH/stale-run-body.sh")" = "fi" ]
[ "$(wc -l < "$SCRATCH/stale-run-body.sh")" -eq 23 ]
bash -n "$SCRATCH/stale-run-body.sh" && echo "BASH -N OK"
echo "SCRATCH=$SCRATCH"
```

Expected: `BASH -N OK`, and the body is exactly 23 lines (the spec's after-state). The name-line rule sits FIRST and `exit`s, so extraction can never re-arm on the second step's `run: |` (an earlier draft reset `seen` there and swept the issue-step body in, producing 29 lines). Keep the `SCRATCH` path for the next steps; if running the steps in separate shells, recreate the extraction first — but note that Steps 2 and 3 below are self-contained and rebuild their own scratch dirs.

- [ ] **Step 2: Stub curl and run the mixed-failure scan (acceptance check 1)**

The stub makes one repo fail with a nonzero exit and empty output (transport failure through pipefail), one repo return a non-JSON body (jq failure through pipefail), one repo stale since 2020, one repo fresh.

```bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRATCH="$(mktemp -d)"
awk '/^      - name: Create or update the issue$/ { exit }
     /^        run: \|$/ { if (!seen) { seen=1; next } }
     seen { print }' \
  "$REPO_ROOT/.github/workflows/stale.yml" | sed 's/^          //' > "$SCRATCH/stale-run-body.sh"
mkdir -p "$SCRATCH/bin"
cat > "$SCRATCH/bin/curl" <<'EOF'
#!/usr/bin/env bash
url="${*: -1}"
case "$url" in
  */example/dead-repo)  exit 7 ;;
  */example/html-repo)  printf '<html>service unavailable</html>'; exit 0 ;;
  */example/stale-repo) printf '{"pushed_at":"2020-01-01T00:00:00Z"}'; exit 0 ;;
  *)                    printf '{"pushed_at":"2099-01-01T00:00:00Z"}'; exit 0 ;;
esac
EOF
chmod +x "$SCRATCH/bin/curl"
cat > "$SCRATCH/README.md" <<'EOF'
- [Dead Repo](https://github.com/example/dead-repo) - Test fixture.
- [Html Repo](https://github.com/example/html-repo) - Test fixture.
- [Stale Repo](https://github.com/example/stale-repo) - Test fixture.
- [Fresh Repo](https://github.com/example/fresh-repo) - Test fixture.
EOF
cd "$SCRATCH"
PATH="$SCRATCH/bin:$PATH" GITHUB_TOKEN=test-token \
  bash -c 'set -euo pipefail; source ./stale-run-body.sh'
echo "EXIT 0 UNDER SET -EUO PIPEFAIL"
grep -F -- "- [example/stale-repo](https://github.com/example/stale-repo) - last push 2020-01-01T00:00:00Z" freshness-report.md
grep -q "fresh-repo" freshness-report.md && { echo "FAIL: fresh repo listed"; exit 1; }
grep -q "24-month threshold" freshness-report.md && { echo "FAIL: footer printed despite found=1"; exit 1; }
grep -q "over 24 months" freshness-report.md
grep -q "Advisory only" freshness-report.md
[ "$(tail -n 1 freshness-report.md)" = "Skipped 2 repos whose GitHub API data was unavailable; the entry list above may be incomplete or empty." ]
echo "MIXED SCAN ASSERTIONS OK"
```

Expected: the script exits 0 despite one dead repo and one non-JSON repo; the stale repo is listed with its 2020 push date; the fresh repo is absent; the footer is suppressed because `found=1`; the header carries "over 24 months" and the advisory clause; the skip note with count 2 is the last line. This also proves the `skipped=$((skipped+1))` increment survives `set -e` twice.

- [ ] **Step 3: Run the all-skip variant (spec risk scenario: footer, then skip note last)**

```bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRATCH="$(mktemp -d)"
awk '/^      - name: Create or update the issue$/ { exit }
     /^        run: \|$/ { if (!seen) { seen=1; next } }
     seen { print }' \
  "$REPO_ROOT/.github/workflows/stale.yml" | sed 's/^          //' > "$SCRATCH/stale-run-body.sh"
mkdir -p "$SCRATCH/bin"
cat > "$SCRATCH/bin/curl" <<'EOF'
#!/usr/bin/env bash
url="${*: -1}"
case "$url" in
  *) exit 7 ;;
esac
EOF
chmod +x "$SCRATCH/bin/curl"
cat > "$SCRATCH/README.md" <<'EOF'
- [Dead Repo](https://github.com/example/dead-repo) - Test fixture.
- [Html Repo](https://github.com/example/html-repo) - Test fixture.
EOF
cd "$SCRATCH"
PATH="$SCRATCH/bin:$PATH" GITHUB_TOKEN=test-token \
  bash -c 'set -euo pipefail; source ./stale-run-body.sh'
grep -q "No entries exceeded the 24-month threshold." freshness-report.md
[ "$(tail -n 1 freshness-report.md)" = "Skipped 2 repos whose GitHub API data was unavailable; the entry list above may be incomplete or empty." ]
echo "ALL-SKIP ASSERTIONS OK"
```

Expected: exit 0; the 24-month footer prints (found=0); the skip note with count 2 is still the last line. When every repo skips, the report reads correctly: empty entry list, footer, skip note last.

- [ ] **Step 4: Arithmetic sanity line (acceptance check 6)**

```bash
bash -c 'set -euo pipefail; s=0; s=$((s+1)); echo ok'
```

Expected output: `ok`

- [ ] **Step 5: YAML parse (acceptance check 5)**

Run from the repo root:

```bash
if command -v actionlint >/dev/null 2>&1; then
  actionlint .github/workflows/stale.yml && echo "ACTIONLINT OK"
elif python -c "import yaml" 2>/dev/null; then
  python -c "import yaml; yaml.safe_load(open('.github/workflows/stale.yml')); print('YAML OK')"
else
  python -m pip install pyyaml
  python -c "import yaml; yaml.safe_load(open('.github/workflows/stale.yml')); print('YAML OK')"
fi
```

Expected: `ACTIONLINT OK` or `YAML OK` with no parse errors.

- [ ] **Step 6: Window consistency greps (acceptance check 3)**

Run from the repo root:

```bash
grep -nE "12 months|12-month" .github/workflows/stale.yml && echo "FAIL" || echo "NO 12-MONTH STRINGS"
grep -n "24 months" contributing.md
[ "$(grep -cE "24 months|24-month" .github/workflows/stale.yml)" = "3" ] && echo "THREE 24-MONTH STRINGS"
```

Expected: `NO 12-MONTH STRINGS`; the contributing.md hit is criterion 4, unchanged; exactly three 24-month strings in stale.yml (cutoff, header, footer).

- [ ] **Step 7: Diff scope check (acceptance check 4)**

Run from the repo root:

```bash
git diff --name-only
git diff --exit-code -- contributing.md README.md .github/workflows/links.yml .github/workflows/lint.yml && echo "FORBIDDEN FILES UNTOUCHED"
git diff -U0 .github/workflows/stale.yml | grep -E '^[+-][^+-]'
```

Expected for the third command, exactly these 5 removed and 9 added lines (in any pairing order; `-U0` shows them with a leading `-` or `+` plus the file's own indentation):

Removed:

```text
-          cutoff=$(date -u -d "12 months ago" +%Y-%m-%dT%H:%M:%SZ)
-            echo "Entries with no push in over 12 months (as of $(date -u +%Y-%m-%d)):"
-            pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty")
-            [ -n "$pushed" ] || continue
-            echo "No entries exceeded the 12-month threshold." >> freshness-report.md
```

Added:

```text
+          cutoff=$(date -u -d "24 months ago" +%Y-%m-%dT%H:%M:%SZ)
+            echo "Entries with no push in over 24 months (as of $(date -u +%Y-%m-%d)). Advisory only: entries meeting the foundational-value exception (contributing.md criterion 4) are still valid."
+          skipped=0
+            pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty" || true)
+            [ -n "$pushed" ] || { skipped=$((skipped+1)); continue; }
+            echo "No entries exceeded the 24-month threshold." >> freshness-report.md
+          if [ "$skipped" -gt 0 ]; then
+            echo "Skipped $skipped repos whose GitHub API data was unavailable; the entry list above may be incomplete or empty." >> freshness-report.md
+          fi
```

Expected for the first command: only `.github/workflows/stale.yml`. Expected for the second: `FORBIDDEN FILES UNTOUCHED`.

Done when: bash -n passes on the 23-line extracted body; the mixed scan exits 0 with the stale repo listed, the fresh repo absent, and the skip note (count 2) as the last line; the all-skip variant shows footer then skip note last; the arithmetic sanity line prints ok; YAML parse passes; no 12-month strings remain and exactly three 24-month strings exist; the diff is stale.yml only, with exactly the 5 removed and 9 added lines above; contributing.md is byte-identical.

### Task 4: Commit

**Files:**
- Commit: `.github/workflows/stale.yml` (the only staged file).

**Interfaces:**
- Consumes: Task 3's full verification pass.
- Produces: one commit on the current branch. No push.

**Model:** flash

- [ ] **Step 1: Stage exactly stale.yml**

Run from the repo root:

```bash
git status --porcelain
git add .github/workflows/stale.yml
git diff --cached --name-only
```

Expected: the staged list is exactly `.github/workflows/stale.yml`. Untracked `docs/` must remain untracked; if anything else appears staged, unstage it before proceeding.

- [ ] **Step 2: Commit with the exact message**

```bash
git commit -m "Make freshness job failures non-fatal and sync 24-month window"
```

- [ ] **Step 3: Post-commit verification**

```bash
git show --stat HEAD
git show HEAD --name-only --format=""
git status --porcelain
```

Expected: HEAD's stat shows one file changed, `9 insertions(+)`, `5 deletions(-)`, all in `.github/workflows/stale.yml`; the name-only list is exactly that one file; working tree afterwards shows only untracked `docs/`.

Post-merge, manual, not a task in this plan (spec acceptance check 2): trigger the workflow via `workflow_dispatch` on GitHub and confirm both steps complete and the Freshness report issue is created or updated.

Done when: exactly one commit exists with the exact message, staging and committed content are stale.yml only, and the working tree is back to baseline plus untracked `docs/`.
