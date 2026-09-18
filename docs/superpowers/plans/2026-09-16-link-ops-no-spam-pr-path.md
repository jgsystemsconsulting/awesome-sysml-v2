# Link Ops No-Spam PR Path (P7) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the weekly Link Checker Report into a create-or-update issue that creates its own labels, add a soft PR-time link check to links.yml, document the local lychee run in contributing.md, and add one link-check checkbox to the PR template.

**Architecture:** Three files change. links.yml gains a `pull_request` trigger; the two tracker-writing steps get `github.event_name != 'pull_request'` gates; the `peter-evans/create-issue-from-file` step is replaced by a label-ensure step plus a `gh` create-or-update step mirroring the stale.yml upsert pattern; a new advisory step surfaces lychee findings on PRs as a `::warning::` annotation plus a step summary. contributing.md gains a Link check subsection and the PR template gains one checkbox. Single job kept; `fail: false` stays; no new `uses:` lines; cron unchanged.

**Tech Stack:** GitHub Actions workflow YAML, `gh` CLI run steps, lychee via the P9-pinned lycheeverse/lychee-action, Git Bash on Windows for verification, Python `yaml` for parse checks.

**Spec:** C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-link-ops-no-spam-pr-path.md

## Global Constraints

- Baseline: HEAD bf25772. All work sits on top of it. Nothing is pushed at any point in this plan.
- No task commits before Task 5. Task 5 is the only commit and stages exactly three files: `.github/workflows/links.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`.
- Commit message, exact: `Deduplicate link reports and add advisory PR link check`
- Diff scope: exactly those three files. stale.yml and lint.yml are outside P7 and must not change.
- No new `uses:` lines. The only actions referenced remain the P9 pins `actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4` and `lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2`.
- Cron `0 18 * * 1` is unchanged. `fail: false` stays. No branch protection or required check is introduced.
- Repo files use LF line endings (verified via `git ls-files --eol`); keep LF in every edit.
- Every command block below runs from the repo root `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2`.

## Codebase context

Facts verified at HEAD bf25772; they match the context round (verdict CONTEXT_COMPLETE).

- `.github/workflows/links.yml` (36 content lines): name at line 1; P9 SHA-pin comment block at 2-7; triggers at 9-12 are `schedule` (cron `"0 18 * * 1"`) plus `workflow_dispatch`, no `pull_request`; permissions `contents: read` and `issues: write` at 14-16; checkout at 22; Link Checker step at 23-29 with `args: --no-progress`, `fail: false`, `token: ${{ secrets.GITHUB_TOKEN }}`; `Create Issue From File` step at 30-36 gated only on `steps.lychee.outputs.exit_code != 0`, fixed title `Link Checker Report`, `labels: report, broken-links`.
- `.github/workflows/stale.yml:50-59` holds the upsert pattern this plan mirrors: `gh issue list --state open --search ... in:title` then `gh issue edit` or `gh issue create`. stale.yml itself is not modified.
- `contributing.md` (30 lines): Local commands section at 23-30; npx fence at 27-30 with `npx awesome-lint@2.3.0 README.md` at 28 and `npx markdownlint-cli2 "README.md" "contributing.md"` at 29.
- `.github/PULL_REQUEST_TEMPLATE.md`: exactly 6 checkbox lines, LF, trailing newline; awesome-lint checkbox at line 4, markdownlint at line 5, commercial at line 6.
- Labels `report` and `broken-links` are referenced by links.yml but defined nowhere in the repo (GitHub labels live in settings); the new label-ensure step creates them idempotently with `|| true`.
- No `.lycheeignore` or `lychee.toml` at the repo root; nothing to migrate.

## Research

Research round retrieved 2026-09-16, verdicts ESTABLISHED; full table in `docs/superpowers/research/2026-09-16-link-ops-no-spam-pr-path-research.md`. Decision-bearing sources:

- https://raw.githubusercontent.com/lycheeverse/lychee-action/master/action.yml (inputs `args`, `fail`, `output`, `token`; single output `exit_code`)
- https://github.com/lycheeverse/lychee (per-platform install: scoop/winget/choco, brew, pacman/zypper/snap/apk; no npm package; GITHUB_TOKEN rate-limit mitigation)
- https://github.com/peter-evans/create-issue-from-file (documents the `issue-number` input as the only reuse path; the title-dedupe limitation framing is the spec's, per its problem statement and the research companion)
- https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests (title search semantics; quoted-phrase discipline)
- https://github.com/lycheeverse/lychee-action/issues/238 (contributor friction from PR link checks; keeps the PR check advisory)

---

### Task 1: Pre-flight gate

**Description:** Confirm the workspace still sits at the spec baseline before any edit. Abort and report if any check mismatches.

**Files:** none modified. Reads `.github/workflows/links.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`.

**Interfaces:**
- Consumes: nothing.
- Produces: confirmation that HEAD is bf25772 and the before-content matches the spec's quoted before-lines, so the exact old_strings in Tasks 2 and 3 will match.

**Model:** flash

- [ ] **Step 1: Verify HEAD**

Run:

```bash
git rev-parse HEAD
```

Expected: `bf25772dccffa23620c37aa14bba6aee2a81556f`.

- [ ] **Step 2: Quote-match the before-lines**

Run:

```bash
sed -n '9,12p' .github/workflows/links.yml
```

Expected output, exactly:

```yaml
on:
  schedule:
    - cron: "0 18 * * 1"
  workflow_dispatch:
```

Run:

```bash
sed -n '30,36p' .github/workflows/links.yml
```

Expected output, exactly:

```yaml
      - name: Create Issue From File
        if: steps.lychee.outputs.exit_code != 0
        uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5
        with:
          title: Link Checker Report
          content-filepath: ./lychee/out.md
          labels: report, broken-links
```

Run:

```bash
sed -n '23,30p' contributing.md
```

Expected output, exactly:

````markdown
## Local commands

Run these from the repository root before opening a PR:

```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```
````

Run:

```bash
grep -c '' .github/PULL_REQUEST_TEMPLATE.md
sed -n '5p;6p' .github/PULL_REQUEST_TEMPLATE.md
```

Expected: `6` lines, line 5 is the markdownlint checkbox, line 6 is the commercial checkbox.

- [ ] **Step 3: Confirm the workflows directory is clean**

Run:

```bash
git status --porcelain .github/workflows/
```

Expected: no output.

**Done when:** HEAD is bf25772; all four quote-matches reproduce the spec's before-lines; `git status --porcelain .github/workflows/` is empty.

---

### Task 2: links.yml edits (trigger, retries, advisory step, label ensure, upsert)

**Description:** Apply the four spec edits to `.github/workflows/links.yml` as whole-block replacements with exact old/new strings, so the file ends matching the spec's Exact-after block.

**Files:**
- Modify: `.github/workflows/links.yml`

**Interfaces:**
- Consumes: Task 1's confirmation that the before-content matches.
- Produces: links.yml with `pull_request` trigger at line 13, `args: --no-progress --max-retries 3`, steps in order: checkout, Link Checker, Advisory broken-link warning, Ensure issue labels exist, Create or update the report issue. Task 4's expected step-name list depends on these exact five entries.

**Model:** flash

- [ ] **Step 1: Add the `pull_request` trigger (spec D2, links.yml 9-12)**

Edit `.github/workflows/links.yml`. Old string:

```yaml
on:
  schedule:
    - cron: "0 18 * * 1"
  workflow_dispatch:
```

New string:

```yaml
on:
  schedule:
    - cron: "0 18 * * 1"
  workflow_dispatch:
  pull_request:
```

Verify:

```bash
sed -n '9,13p' .github/workflows/links.yml
```

Expected: the five lines above, with `  pull_request:` as line 13.

- [ ] **Step 2: Append `--max-retries 3` to the lychee args (spec D2)**

Edit `.github/workflows/links.yml`. Old string:

```yaml
        args: --no-progress
```

New string:

```yaml
        args: --no-progress --max-retries 3
```

Verify:

```bash
grep -F -n -- '--max-retries 3' .github/workflows/links.yml
```

Expected: one hit on the args line (line 28 after the Task 2 Step 1 trigger insertion shifted the file by one line).

- [ ] **Step 3: Replace the create-issue-from-file step with the advisory, label-ensure, and upsert steps (spec D1 and D2, links.yml 30-36)**

Edit `.github/workflows/links.yml`. Old string:

```yaml
      - name: Create Issue From File
        if: steps.lychee.outputs.exit_code != 0
        uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5
        with:
          title: Link Checker Report
          content-filepath: ./lychee/out.md
          labels: report, broken-links
```

New string:

```yaml
      - name: Advisory broken-link warning
        if: github.event_name == 'pull_request' && steps.lychee.outputs.exit_code != 0
        run: |
          {
            echo "Lychee exit code: ${{ steps.lychee.outputs.exit_code }}."
            echo "Broken or unreachable links were found. This check is advisory and does not block merge; see the Link Checker step log for the URL list."
          } >> "$GITHUB_STEP_SUMMARY"
          echo "::warning::Lychee found unreachable links (exit code ${{ steps.lychee.outputs.exit_code }}); advisory only, see the Link Checker step log"
      - name: Ensure issue labels exist
        if: github.event_name != 'pull_request'
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh label create report --color 1D76DB || true
          gh label create broken-links --color D93F0B || true
      - name: Create or update the report issue
        if: github.event_name != 'pull_request' && steps.lychee.outputs.exit_code != 0
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          existing=$(gh issue list --state open --search '"Link Checker Report" in:title' --json number --jq ".[0].number // empty")
          if [ -n "$existing" ]; then
            gh issue edit "$existing" --body-file lychee/out.md --add-label report --add-label broken-links
          else
            gh issue create --title "Link Checker Report" --body-file lychee/out.md --label report --label broken-links
          fi
```

Verify the step sequence:

```bash
grep -n '      - name:' .github/workflows/links.yml
```

Expected, in order: `Link Checker`, `Advisory broken-link warning`, `Ensure issue labels exist`, `Create or update the report issue`.

- [ ] **Step 4: Compare against the spec's Exact-after block**

Run `git diff .github/workflows/links.yml` and confirm the added content is character-identical to the spec section "Exact after content for links.yml": same triggers, same args, same four step bodies, same permissions, same pins and comments. Do not commit.

**Done when:** the three edits are applied; the step sequence matches; the diff shows no other change to the file; working tree still has uncommitted changes only.

---

### Task 3: contributing.md Link check subsection and PR template checkbox

**Description:** Insert the D3 subsection after the Local commands fence in contributing.md (after line 30) and the D4 checkbox after line 5 of the PR template.

**Files:**
- Modify: `contributing.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Consumes: Task 1's confirmation of the before-content.
- Produces: contributing.md with a `### Link check` subsection containing "not an npm package" and the `lychee README.md` fence; the template at 7 lines with the link-check checkbox at line 6. Task 4 asserts on both.

**Model:** flash

- [ ] **Step 1: Insert the Link check subsection (spec D3)**

Edit `contributing.md`. Old string:

````markdown
```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```
````

New string (old fence, then blank line, then the new subsection; the leading blank line separates it from the Local commands fence):

````markdown
```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

### Link check

`lychee` is a native binary, not an npm package. Install it once with your platform package manager (`scoop`, `winget`, or `choco` on Windows, `brew` on macOS, `pacman`, `zypper`, `snap`, or `apk` on Linux), then run from the repository root:

```bash
lychee README.md
```

Export `GITHUB_TOKEN` (for example `GITHUB_TOKEN=$(gh auth token)`) to avoid GitHub rate limiting on `github.com` links. Third-party sites sometimes return transient timeouts or 429s; retry before treating a failure as a broken link.
````

Verify:

```bash
tail -n 14 contributing.md
```

Expected: the new subsection exactly as written above.

- [ ] **Step 2: Insert the link-check checkbox (spec D4)**

Edit `.github/PULL_REQUEST_TEMPLATE.md`. Old string:

```markdown
- [ ] `npx markdownlint-cli2 "README.md" "contributing.md"` passes locally
- [ ] Commercial entries go in Commercial Tools only, with disclosure in the PR body
```

New string:

```markdown
- [ ] `npx markdownlint-cli2 "README.md" "contributing.md"` passes locally
- [ ] No new broken links: `lychee README.md` passes locally, or the Link check on this PR shows no new failures (advisory)
- [ ] Commercial entries go in Commercial Tools only, with disclosure in the PR body
```

Verify:

```bash
grep -c '' .github/PULL_REQUEST_TEMPLATE.md
sed -n '5p;6p;7p' .github/PULL_REQUEST_TEMPLATE.md
```

Expected: `7` lines; line 5 markdownlint checkbox, line 6 the new link-check checkbox, line 7 commercial checkbox. Do not commit.

**Done when:** both inserts are in place; contributing.md is 40 lines with the subsection after the existing fence; the template is 7 lines with the checkbox at line 6; working tree still uncommitted.

---

### Task 4: Verification battery

**Description:** Run the full local verification: YAML parse, grep asserts, step structure, run-block syntax, doc and template checks, diff scope, boundary files.

**Files:** none modified. Reads the three modified files.

**Interfaces:**
- Consumes: Task 2 and Task 3 outputs.
- Produces: a passing verification record. Deferred: AC1 (dedupe across two consecutive `workflow_dispatch` runs) and AC3 (PR and fork runtime behavior) are runner-side behaviors; they are verified on GitHub after push, not in this plan. Every local check below covers the remaining acceptance criteria statically.

**Model:** standard

- [ ] **Step 1: YAML parse and cron unchanged (AC7)**

Run:

```bash
python -c "import yaml; yaml.safe_load(open('.github/workflows/links.yml')); print('YAML OK')"
grep -n 'cron: "0 18 \* \* 1"' .github/workflows/links.yml
```

Expected: `YAML OK`, and the cron line still at line 11.

- [ ] **Step 2: Grep asserts (AC1 mechanism, AC2, AC3, AC8, AC9)**

Run:

```bash
grep -F -n '  pull_request:' .github/workflows/links.yml
grep -F -n -- '--max-retries 3' .github/workflows/links.yml
grep -F -n '"Link Checker Report" in:title' .github/workflows/links.yml
grep -F -n -- '--add-label' .github/workflows/links.yml
grep -F -n '::warning::' .github/workflows/links.yml
grep -F -n 'fail: false' .github/workflows/links.yml
grep -c -F "github.event_name != 'pull_request'" .github/workflows/links.yml
grep -c -F "github.event_name == 'pull_request'" .github/workflows/links.yml
grep -c -F 'create-issue-from-file' .github/workflows/links.yml || echo "OK: create-issue-from-file absent"
grep -c -F 'uses:' .github/workflows/links.yml
```

Expected: `pull_request:` at line 13; `--max-retries 3` at line 28; one quoted-phrase search hit inside the upsert step; two `--add-label` hits (report and broken-links on the edit line); one `::warning::` line; event-gate counts `2` then `1`; the create-issue-from-file count grep prints `0` then, exiting nonzero, the `OK: create-issue-from-file absent` fallback; the `uses:` count is `2` (checkout and lychee-action only, no new pins).

- [ ] **Step 3: Step structure and run-block syntax**

Run:

```bash
python - <<'EOF'
import yaml, subprocess, os, re
wf = yaml.safe_load(open('.github/workflows/links.yml'))
steps = wf['jobs']['linkChecker']['steps']
names = [s.get('name', s.get('uses', '<unnamed>')) for s in steps]
expected = ['actions/checkout@11d5960a326750d5838078e36cf38b85af677262', 'Link Checker',
            'Advisory broken-link warning', 'Ensure issue labels exist',
            'Create or update the report issue']
assert names == expected, names
run_blocks = [(s['name'], s['run']) for s in steps if 'run' in s]
assert len(run_blocks) == 3, run_blocks
for name, body in run_blocks:
    stripped = re.sub(r'\$\{\{.*?\}\}', 'GH_EXPR', body)
    with open('run_block_check.sh', 'w', newline='\n') as f:
        f.write(stripped)
    r = subprocess.run(['bash', '-n', 'run_block_check.sh'])
    assert r.returncode == 0, 'bash -n failed for step: ' + name
    os.remove('run_block_check.sh')
print('structure OK; run blocks OK:', [n for n, _ in run_blocks])
EOF
```

Expected: `structure OK; run blocks OK: ['Advisory broken-link warning', 'Ensure issue labels exist', 'Create or update the report issue']` and no leftover `run_block_check.sh`. The `re.sub` strips GitHub `${{ ... }}` expressions before `bash -n`, because those are substituted by the runner before bash ever parses the script and are not valid bash on their own.

- [ ] **Step 4: Docs and template checks (AC4, AC5)**

Run:

```bash
grep -F -n 'not an npm package' contributing.md
grep -F -n 'lychee README.md' contributing.md
grep -c '' .github/PULL_REQUEST_TEMPLATE.md
sed -n '6p' .github/PULL_REQUEST_TEMPLATE.md
```

Expected: one `not an npm package` hit; one `lychee README.md` hit inside the bash fence; `7` template lines; line 6 is `- [ ] No new broken links: \`lychee README.md\` passes locally, or the Link check on this PR shows no new failures (advisory)`.

- [ ] **Step 5: Diff scope and boundary (AC6)**

Run:

```bash
git diff --name-only
git diff --exit-code -- .github/workflows/stale.yml .github/workflows/lint.yml && echo "boundary OK: stale.yml and lint.yml untouched"
```

Expected: the first command lists exactly `.github/workflows/links.yml`, `.github/PULL_REQUEST_TEMPLATE.md`, `contributing.md`; the second prints `boundary OK: stale.yml and lint.yml untouched`.

**Done when:** every command in Steps 1-5 returns the expected output. Any mismatch: fix the offending file (re-apply the exact new string from Task 2 or 3) and rerun the failed step; do not proceed to Task 5 with a red check.

---

### Task 5: Single commit

**Description:** Stage exactly the three changed files and create the single commit with the exact message. Nothing is pushed.

**Files:**
- Commit: `.github/workflows/links.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Consumes: Task 4's green battery.
- Produces: one commit on top of bf25772 containing exactly the three files, ready for the parent's step 4/5.

**Model:** flash

- [ ] **Step 1: Stage the three files**

Run:

```bash
git status --porcelain
git add .github/workflows/links.yml contributing.md .github/PULL_REQUEST_TEMPLATE.md
git diff --cached --name-only
```

Expected: pre-add status lists only the three modified files; the cached diff lists exactly the same three.

- [ ] **Step 2: Commit**

Run:

```bash
git commit -m "Deduplicate link reports and add advisory PR link check"
```

Expected: commit created on top of bf25772 with that exact subject.

- [ ] **Step 3: Post-commit verification**

Run:

```bash
git status --porcelain
git log --oneline -2
git show --name-only --format= HEAD
```

Expected: clean working tree (no output from the first command); `HEAD` is the new commit with parent bf25772; `git show` lists exactly `.github/PULL_REQUEST_TEMPLATE.md`, `.github/workflows/links.yml`, `contributing.md`.

**Done when:** one commit, exact message, exactly three files, clean tree, nothing pushed.
