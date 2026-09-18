# maintenance-cadence-ack (P4) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Document the repo's three maintenance automations (weekly link scan, monthly freshness report, PR lint gates) in contributing.md and extend the README Contributing one-liner, changing no workflow and no behavior.

**Architecture:** Documentation-only change to two existing files. A top-level `## Maintenance` section is appended verbatim to the end of contributing.md, after the `### Link check` subsection. The README `## Contributing` body at line 128 is replaced with an extended one-liner that adds "maintenance cadence" to the pointer list. One commit at the end lands both files; nothing is pushed.

**Tech Stack:** Markdown; `npx markdownlint-cli2` and `npx awesome-lint@2.3.0` for verification; git for the single commit.

**Spec:** C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-maintenance-cadence-ack.md

**Research log:** docs/superpowers/research/2026-09-16-maintenance-cadence-ack-research-log.md

research: skipped (no-open-world-questions; documents the repo's own automation)

## Global Constraints

- Documentation-only: no file under `.github/workflows/` is added, modified, or deleted; no other repo behavior changes.
- Baseline: HEAD must be b562394 (full SHA b562394e4da6d35c8e8a805c658957c99154bf19) before Task 1 starts.
- The contributing.md section text is transcribed verbatim from the spec (block in Task 2). No rewording, no added or dropped sentences.
- The README change is exactly the one-line replacement given in Task 2.
- Exactly one commit, in Task 4 only, staging exactly `contributing.md` and `README.md`, with message exactly `Document maintenance cadence in contributing.md`. No task before Task 4 commits. Nothing is pushed.
- `.markdownlint-cli2.jsonc` disables only MD013, so the long lines in the new section lint clean. Keep them as written; do not wrap.
- All commands run from the repository root: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2`.

## Codebase context

From the context gate (`C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\context\2026-09-16-maintenance-cadence-ack-context.md`, verdict CONTEXT_COMPLETE, 8/8 claims), re-verified against the working tree at HEAD b562394:

- contributing.md is 40 lines: `## Inclusion criteria` (line 5), `## Entry format` (13), `## Local commands` (23) with the npx fence (27-30) and `### Link check` (32-40). Line 40 is the `GITHUB_TOKEN` rate-limit sentence and the file ends with a newline. Heading style is `##` top level and `###` subsection; no heading-order lint constraints.
- README.md `## Contributing` is lines 126-128; line 128 is the single body sentence delegating to contributing.md.
- Automation facts live in `.github/workflows/links.yml` (cron `0 18 * * 1`, advisory PR run with `fail: false`, issue upsert gated to broken-link runs only), `.github/workflows/stale.yml` (cron `0 6 1 * *`, 24-month window on `pushed_at`, github.com-only URL grep, unconditional issue upsert), and `.github/workflows/lint.yml` (PR and push gates on main, `awesome-lint@2.3.0` plus markdownlint, both blocking).
- Git status at baseline shows only the untracked `docs/` pipeline artifacts; tracked files are clean.

---

### Task 1: Pre-flight gate

**Files:**
- Read only: `contributing.md`, `README.md`, `.github/workflows/`

**Model:** flash

Verify the workspace matches the spec's baseline before touching anything. If any check below fails, stop and report BLOCKED; do not apply edits on a drifted baseline.

- [ ] **Step 1: Verify HEAD**

Run: `git rev-parse HEAD`
Expected: `b562394e4da6d35c8e8a805c658957c99154bf19`

- [ ] **Step 2: Verify tracked tree is clean**

Run: `git status --porcelain`
Expected output, exactly one line: `?? docs/`
Any `M `, `A `, `D `, or other tracked-file entry is a failure.

- [ ] **Step 3: Verify contributing.md shape**

Run: `wc -l contributing.md`
Expected: `40 contributing.md`

Run: `grep -n "^### Link check$" contributing.md`
Expected: `32:### Link check`

Run: `sed -n '40p' contributing.md`
Expected: the line starting `Export \`GITHUB_TOKEN\` (for example \`GITHUB_TOKEN=$(gh auth token)\`)` and ending `retry before treating a failure as a broken link.`

- [ ] **Step 4: Verify README Contributing section**

Run: `grep -n "^## Contributing$" README.md`
Expected: `126:## Contributing`

Run: `sed -n '126,128p' README.md`
Expected output, three lines:

```
## Contributing

See [contributing.md](contributing.md) for the inclusion criteria, entry format, and local lint commands.
```

- [ ] **Step 5: Verify workflows are untouched**

Run: `ls .github/workflows/`
Expected, exactly: `links.yml  lint.yml  stale.yml`

Run: `git diff --exit-code -- .github/workflows && git status --porcelain .github/workflows`
Expected: no output, exit 0.

**Done when:** all five steps produced the expected output. Any mismatch stops the plan.

---

### Task 2: Apply the contributing.md section and the README one-liner

**Files:**
- Modify: `contributing.md` (append after line 40; file grows from 40 to 56 lines)
- Modify: `README.md:128` (one-line replacement)

**Model:** flash

- [ ] **Step 1: Append the Maintenance section to contributing.md**

The file ends with a newline on line 40. Append one blank line, then the 15-line block below, exactly as written. Run this from the repository root; the quoted heredoc keeps every backtick and quote literal:

```bash
cat >> contributing.md <<'EOF'

## Maintenance

Three automated workflows keep the list current. They live in `.github/workflows/` and need no manual upkeep; this section describes what each one does so contributors and maintainers can tell automation from neglect.

### Link scan (weekly)

`links.yml` checks the links in every Markdown, HTML, and reStructuredText file in the repository every Monday at 18:00 UTC, on every pull request, and on manual dispatch. The check is advisory: a PR with broken links gets a warning but is never blocked by it. The "Link Checker Report" issue is created or updated only when links actually break; a week with no broken links leaves that issue untouched.

### Freshness report (monthly)

`stale.yml` runs on the first day of each month at 06:00 UTC, or on manual dispatch. It collects the `github.com` repository URLs from README.md and lists repos with no push in the last 24 months. The report is advisory: an entry past the window can still be valid under the foundational-value exception (criterion 4). The "Freshness report" issue is refreshed on every run, including months with no stale entries. Criterion 4 speaks of a commit within 24 months; the report measures the repository's last push, which is usually but not always the same thing.

### Lint gates (every PR and push to main)

`lint.yml` runs `awesome-lint@2.3.0` on README.md, and `markdownlint` on README.md and contributing.md, on every pull request targeting main and every push to main. These gates block merge on failure. The local markdownlint command above installs an unpinned npx package and may differ from the version CI runs; the pinned `awesome-lint@2.3.0` matches CI exactly.
EOF
```

Verify the append:

Run: `wc -l contributing.md`
Expected: `56 contributing.md`

- [ ] **Step 2: Replace the README one-liner**

Old line 128, exact:

```
See [contributing.md](contributing.md) for the inclusion criteria, entry format, and local lint commands.
```

New line 128, exact:

```
See [contributing.md](contributing.md) for the inclusion criteria, entry format, local lint commands, and maintenance cadence.
```

Use a text edit that replaces only that line; no other README byte changes.

Verify:

Run: `grep -n "maintenance cadence" README.md`
Expected: `128:See [contributing.md](contributing.md) for the inclusion criteria, entry format, local lint commands, and maintenance cadence.`

Run: `grep -c "entry format, and local lint commands" README.md`
Expected: `0` (old phrasing gone; exit code 1 is the success signal here)

- [ ] **Step 3: Spot-check the new section layout**

Run: `grep -n "^## Maintenance$\|^### Link scan (weekly)$\|^### Freshness report (monthly)$\|^### Lint gates (every PR and push to main)$" contributing.md`
Expected output, four lines in this order:

```
42:## Maintenance
46:### Link scan (weekly)
50:### Freshness report (monthly)
54:### Lint gates (every PR and push to main)
```

**Done when:** contributing.md is 56 lines with the four new headings at 42, 46, 50, 54, and README line 128 matches the new text exactly.

---

### Task 3: Verification (pre-commit)

**Files:**
- Read only: `contributing.md`, `README.md`

**Model:** flash

No edits in this task. Every command must exit 0 (or print the expected output) before Task 4 runs.

- [ ] **Step 1: Run the local lints**

Run: `npx markdownlint-cli2 "README.md" "contributing.md"`
Expected: exit 0, no findings.

Run: `npx awesome-lint@2.3.0 README.md`
Expected: exit 0, no findings.

- [ ] **Step 2: Assert section content and ordering**

```bash
test "$(grep -n '^### Link check$' contributing.md | cut -d: -f1)" -lt "$(grep -n '^## Maintenance$' contributing.md | cut -d: -f1)" && echo ORDER-OK
grep -q 'every Monday at 18:00 UTC' contributing.md && echo LINKS-CRON-OK
grep -q 'gets a warning but is never blocked by it' contributing.md && echo LINKS-ADVISORY-OK
grep -q 'created or updated only when links actually break' contributing.md && echo LINKS-UPSERT-GATE-OK
grep -q 'first day of each month at 06:00 UTC' contributing.md && echo STALE-CRON-OK
grep -q 'github.com` repository URLs from README.md' contributing.md && echo STALE-SCOPE-OK
grep -q 'no push in the last 24 months' contributing.md && echo STALE-WINDOW-OK
grep -q 'refreshed on every run, including months with no stale entries' contributing.md && echo STALE-ALWAYS-UPSERT-OK
grep -q "the report measures the repository's last push" contributing.md && echo PUSH-VS-COMMIT-OK
grep -q 'awesome-lint@2.3.0` on README.md' contributing.md && echo LINT-PIN-OK
grep -q 'These gates block merge on failure' contributing.md && echo LINT-BLOCKING-OK
grep -q 'installs an unpinned npx package' contributing.md && echo LOCAL-MDLINT-DIVERGENCE-OK
```

Expected output, twelve lines:

```
ORDER-OK
LINKS-CRON-OK
LINKS-ADVISORY-OK
LINKS-UPSERT-GATE-OK
STALE-CRON-OK
STALE-SCOPE-OK
STALE-WINDOW-OK
STALE-ALWAYS-UPSERT-OK
PUSH-VS-COMMIT-OK
LINT-PIN-OK
LINT-BLOCKING-OK
LOCAL-MDLINT-DIVERGENCE-OK
```

Also confirm the three subsection headings each appear exactly once:

Run: `grep -c "^### Link scan (weekly)$" contributing.md && grep -c "^### Freshness report (monthly)$" contributing.md && grep -c "^### Lint gates (every PR and push to main)$" contributing.md`
Expected: `1`, `1`, `1` on three lines.

- [ ] **Step 3: Assert the diff scope**

Run: `git diff --name-only`
Expected output, exactly two lines:

```
README.md
contributing.md
```

Run: `git diff --name-only | diff - <(printf 'README.md\ncontributing.md\n') && echo DIFF-SCOPE-OK`
Expected: `DIFF-SCOPE-OK` (no other lines).

Run: `git diff --exit-code -- .github/workflows && echo WORKFLOWS-CLEAN`
Expected: `WORKFLOWS-CLEAN`.

**Done when:** both lints exit 0, all twelve content assertions print, heading counts are 1/1/1, the diff names exactly README.md and contributing.md, and `.github/workflows/` shows no diff.

---

### Task 4: Single commit

**Files:**
- Stage and commit: `contributing.md`, `README.md`

**Model:** flash

- [ ] **Step 1: Stage exactly the two files**

```bash
git add contributing.md README.md
git status --porcelain
```

Expected output, exactly three lines:

```
M  README.md
M  contributing.md
?? docs/
```

`docs/` is the untracked superpowers pipeline artifacts directory and stays uncommitted. Any other staged path is a failure; unstage it with `git restore --staged <path>` before committing.

- [ ] **Step 2: Commit**

```bash
git commit -m "Document maintenance cadence in contributing.md"
```

- [ ] **Step 3: Post-commit verification**

Run: `git log -1 --pretty=%s`
Expected: `Document maintenance cadence in contributing.md`

Run: `git show --stat --pretty=format:"" HEAD`
Expected: exactly two file rows, `contributing.md` and `README.md`, nothing else.

Run: `git status --porcelain`
Expected: `?? docs/` only.

Run: `git status -sb`
Expected: first line shows the branch ahead of its upstream by 1 (for example `## main...origin/main [ahead 1]`). If no upstream is configured, this prints the bare branch line; that also passes. The plan contains no push command and none may be run.

**Done when:** HEAD carries the exact message with exactly the two files staged in it, the tracked tree is clean apart from untracked `docs/`, and the commit has not been pushed.

---

## Self-review record

- Spec coverage: AC1 maps to Task 2 Step 1 (verbatim block) and Task 3 Step 2 (twelve assertions cover placement, both crons, advisory vs blocking asymmetry, failure-only vs always upsert, github.com scope, 24-month push-based window, foundational-value exception text, lint pin, and the commit-versus-push sentence). AC2 maps to Task 2 Step 2 and its two greps. AC3 and AC4 map to Task 3 Step 1. AC5 maps to Task 3 Step 3 and Task 4 Steps 1 and 3. Non-goals are enforced by the diff-scope and workflows-clean checks.
- Placeholder scan: every edit step carries the exact bytes; every verification step carries the exact command and expected output. None found.
- Consistency: the commit message, heading strings, and grep patterns are identical across Tasks 2, 3, and 4.
