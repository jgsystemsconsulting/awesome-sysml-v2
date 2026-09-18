# Community Root Meta Files Implementation Plan (awesome-sysml-v2, P5)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the four community-standard root files (`CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, `CHANGELOG.md`) in exactly one commit, and enable GitHub private vulnerability reporting on the repository.

**Architecture:** Four new files at the repo root, each in its de facto standard format so GitHub and third-party tools parse it with no custom code: Contributor Covenant 2.1 verbatim, a security policy shaped for a link-curation repo, CFF 1.2.0 citation metadata, and a Keep a Changelog 1.1.0 skeleton under a single `[Unreleased]`. No existing file is edited. The commit lands once, in Task 5, after all checks pass; nothing is pushed.

**Tech Stack:** Markdown, YAML (CFF 1.2.0), git, `gh` CLI, `markdownlint-cli2` (existing repo config), Python with PyYAML, curl.

**Spec:** `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-community-root-meta.md`

## Research

research: skipped (no-open-world-questions; standard file formats, no external fact to learn)

Round 0 gate logs: `docs/superpowers/research/2026-09-16-community-root-meta-research-log.md` and `docs/superpowers/context/2026-09-16-community-root-meta-context-log.md`.

## Global Constraints

- Baseline commit for every task: `ccc0acc5aa90c18d1131f18e16a6b57529bab0e9`. Exactly one commit lands, in Task 5, with message exactly `Add community root meta files`. Nothing is ever pushed.
- Create exactly four files at the repo root: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, `CHANGELOG.md`. Root only; no `.github/` copies.
- No edits to `README.md`, `contributing.md`, `.github/workflows/`, or any list entry content. No commits before Task 5.
- `CODE_OF_CONDUCT.md`: full Contributor Covenant 2.1 verbatim from the canonical URL, one contact-line substitution, and no literal `INSERT` placeholder anywhere in the file.
- `CITATION.cff`: the spec's pinned YAML block, byte-exact, plus a trailing newline.
- `CHANGELOG.md`: the spec's pinned Keep a Changelog skeleton, byte-exact, single `[Unreleased]` section, plus a trailing newline.
- Working-tree note: untracked `docs/superpowers/**` pipeline artifacts pre-exist at the baseline commit. Every `git status` check in this plan is scoped to exclude them.
- All commands run from the repo root: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2` (Git Bash path: `/c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2`).

---

### Task 1: Pre-flight gate

**Files:**
- None created or modified. Read-only checks only.

**Interfaces:**
- Consumes: nothing.
- Produces: verified baseline facts consumed by Tasks 2 through 5 (HEAD hash, clean state of the four target paths, reachable canonical URL, PyYAML availability).

**Model:** flash

- [ ] **Step 1: Verify HEAD is the pinned baseline**

Run: `git rev-parse HEAD`
Expected output, exactly: `ccc0acc5aa90c18d1131f18e16a6b57529bab0e9`
If the hash differs, STOP and report. Do not plan around a moved baseline.

- [ ] **Step 2: Verify none of the four target files exist**

```bash
for f in CODE_OF_CONDUCT.md SECURITY.md CITATION.cff CHANGELOG.md; do test ! -e "$f" || echo "EXISTS: $f"; done; echo "absence-check-done"
```
Expected output: only `absence-check-done`. Any `EXISTS:` line is a STOP.

- [ ] **Step 3: Verify README, contributing guide, and .github are clean**

Run: `git status --porcelain README.md contributing.md .github`
Expected output: empty.

- [ ] **Step 4: Verify the working tree carries only the known pipeline artifacts**

Run: `git status --porcelain | grep -v '^?? docs/'`
Expected output: empty. This pins the dirty-state baseline that Task 3's scoped status check relies on.

- [ ] **Step 5: Verify the canonical CoC URL is reachable**

Run: `curl -s -o /dev/null -w "%{http_code}" https://www.contributor-covenant.org/version/2/1/code_of_conduct/`
Expected output: `200`

- [ ] **Step 6: Verify PyYAML is available for the Task 3 parse check**

Run: `python -c "import yaml; print('yaml-ok')"`
Expected output: `yaml-ok`. If this fails, note it: Task 3 Step 4 falls back to any YAML parser (for example `npx yaml-lint CITATION.cff`), per the spec's verification section.

**Done when:** all six checks print their expected output and no file was touched.

---

### Task 2: Create the four root files

**Files:**
- Create: `CODE_OF_CONDUCT.md`
- Create: `SECURITY.md`
- Create: `CITATION.cff`
- Create: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1's verified baseline.
- Produces: the four files, with these pinned anchor strings that Task 3 greps for: `# Code of Conduct`, `## Our Pledge`, `through GitHub: open an issue on this repository`, `adapted from the [Contributor Covenant][homepage], version 2.1`, `private vulnerability reporting`, `5 business days`, `cff-version: 1.2.0`, and the seven `(P<n>)` changelog bullets.

**Model:** flash

**Verified source facts (checked 2026-09-15, so the executor does not re-derive them):** the canonical page `https://www.contributor-covenant.org/version/2/1/code_of_conduct/` returns 200, and the same site serves the document as raw markdown at `https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md`. That markdown's body contains exactly one `INSERT` occurrence, the enforcement contact line. Its attribution footer already reads "adapted from the [Contributor Covenant][homepage], version 2.1", linking `https://www.contributor-covenant.org/version/2/1/code_of_conduct.html`, which 301-redirects to the live page; keep that footer byte for byte, and do not "fix" the link. Full heading inventory of the document: `# Contributor Covenant Code of Conduct`, `## Our Pledge`, `## Our Standards`, `## Enforcement Responsibilities`, `## Scope`, `## Enforcement`, `## Enforcement Guidelines`, `### 1. Correction`, `### 2. Warning`, `### 3. Temporary Ban`, `### 4. Permanent Ban`, `## Attribution`, followed by the link-reference definitions.

- [ ] **Step 1: Fetch the canonical CC 2.1 markdown**

```bash
curl -s https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md -o /tmp/cc21.md
grep -c 'INSERT' /tmp/cc21.md
grep -c '^+++' /tmp/cc21.md
grep -qxF '## Our Pledge' /tmp/cc21.md && echo "source-ok"
```
Expected: `1`, then `0`, then `source-ok`. One `INSERT` is correct at this point; it is the contact placeholder that Step 3 replaces.

Fallback, only if the site variant fails to fetch: `curl -s https://raw.githubusercontent.com/EthicalSource/contributor_covenant/release/content/version/2/1/code_of_conduct.md -o /tmp/cc21.md`. That copy carries a 5-line `+++` front matter block (which contains a second `INSERT`), so the expected greps there are `2` for `^+++` and `2` for `INSERT`. The awk in Step 2 skips everything above `## Our Pledge` either way; the Task 3 checks on the finished file are the real gate.

- [ ] **Step 2: Assemble CODE_OF_CONDUCT.md**

```bash
awk '/^## Our Pledge$/{found=1} found{print}' /tmp/cc21.md > /tmp/cc21_body.md
{
  printf '# Code of Conduct\n\n'
  printf 'This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/), version 2.1. The full text follows.\n\n'
  cat /tmp/cc21_body.md
} > CODE_OF_CONDUCT.md
```
This replaces the source's own top-level heading with ours and keeps the body from `## Our Pledge` through the link-reference definitions byte for byte. The intro line carries the spec's attribution link; the verbatim footer keeps its own.

- [ ] **Step 3: Fill the contact line (the only text edit)**

The source sentence, verbatim:
`Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement at [INSERT CONTACT METHOD]. All complaints will be reviewed and investigated promptly and fairly.`

Apply exactly this replacement:

```bash
python - <<'EOF'
from pathlib import Path
# newline="" below disables universal-newline translation: keep the file LF on Windows.
p = Path("CODE_OF_CONDUCT.md")
t = p.read_text(encoding="utf-8", newline="")
old = "at [INSERT CONTACT METHOD]. All complaints"
new = "through GitHub: open an issue on this repository, or contact the repository owner through the profile at https://github.com/jgsystemsconsulting. All complaints"
assert t.count(old) == 1, "anchor not found exactly once"
p.write_text(t.replace(old, new), encoding="utf-8", newline="")
EOF
```

Resulting sentence: `Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to the community leaders responsible for enforcement through GitHub: open an issue on this repository, or contact the repository owner through the profile at https://github.com/jgsystemsconsulting. All complaints will be reviewed and investigated promptly and fairly.`

- [ ] **Step 4: Smoke-check the assembled CoC**

```bash
grep -c 'INSERT' CODE_OF_CONDUCT.md
grep -c '^+++' CODE_OF_CONDUCT.md
```
Expected: `0`, then `0`. The full battery runs in Task 3.

- [ ] **Step 5: Create SECURITY.md**

Create `SECURITY.md` with exactly this content, ending with a single trailing newline:

```markdown
# Security Policy

## Supported

This repository is a curated list, not an application. The supported surface is this repository itself: its content, its workflows, and the links it lists. There is no supported-versions table because there is no shipped product with releases.

## Reporting a vulnerability

Use GitHub private vulnerability reporting on this repository: open the Security tab and choose "Report a vulnerability". Do not open a public issue for a security report.

Two report types are in scope:

- A listed link that has turned malicious, compromised, hijacked, or serves content materially different from its description.
- A vulnerability in this repository itself (workflows, scripts, repository configuration).

## Response expectations

Reports are acknowledged within 5 business days. Removal or fix is prioritized by exposure, and a public note follows after remediation.

## Out of scope

Vulnerabilities inside the tools the list links to. Those belong to the linked projects' own security channels; this repository only acts on the entry.
```

Quick check:

```bash
grep -qF "private vulnerability reporting" SECURITY.md && echo "sec-ok"
```
Expected: `sec-ok`. The enabling of the setting itself is Task 4; the file only names the path.

- [ ] **Step 6: Create CITATION.cff**

Create `CITATION.cff` with exactly this content, byte-exact per the spec, ending with a single trailing newline:

```yaml
cff-version: 1.2.0
message: "If you use this list in your work, please cite it using this metadata."
title: Awesome SysML V2
authors:
  - entity:
      name: "JG Systems Consulting Ltd"
license: MIT
repository-code: https://github.com/jgsystemsconsulting/awesome-sysml-v2
preferred-citation:
  type: generic
  title: "Awesome SysML V2"
  authors:
    - entity:
        name: "JG Systems Consulting Ltd"
  year: 2026
  repository-code: https://github.com/jgsystemsconsulting/awesome-sysml-v2
```

Quick parse smoke (the full assertion set runs in Task 3):

```bash
python -c "import yaml; d=yaml.safe_load(open('CITATION.cff')); assert d['cff-version']=='1.2.0'; print('cff-ok')"
```
Expected: `cff-ok`. Note for the executor: `version` and `date-released` are deliberately absent because no release exists; do not add them.

- [ ] **Step 7: Create CHANGELOG.md**

Create `CHANGELOG.md` with exactly this content, byte-exact per the spec, ending with a single trailing newline:

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Companion documentation site for the list (P2).
- Link-report workflow: duplicate-report detection and advisory pull-request check (P7).
- Maintenance and contribution guidance: contributing guide, backlog, review records (P4).

### Changed

- All GitHub Actions pinned to full commit SHAs for supply-chain hardening (P9).
- Lint workflow runs least-privilege with a pinned awesome-lint version (P8).
- Repository made public (P1).

### Fixed

- Freshness check now reports link state accurately instead of masking failures (P6).
```

Lint it with the repo's own config (`.markdownlint-cli2.jsonc` disables only MD013; markdownlint-cli2 auto-discovers it):

```bash
npx markdownlint-cli2 CHANGELOG.md && echo "CHANGELOG-LINT-OK"
```
Expected: `CHANGELOG-LINT-OK`, exit 0. Do not add bullets, do not add a version header, do not add dates inside bullets: the spec pins the skeleton as the honesty enforcement.

- [ ] **Step 8: Confirm exactly four untracked files beyond the pipeline artifacts**

Run: `git status --porcelain | grep -v '^?? docs/'`
Expected output, exactly these four lines and nothing else:

```text
?? CHANGELOG.md
?? CITATION.cff
?? CODE_OF_CONDUCT.md
?? SECURITY.md
```

**Done when:** all four files exist with the pinned content, both CoC smoke greps print `0`, `sec-ok` and `cff-ok` and `CHANGELOG-LINT-OK` printed, and the scoped status shows only the four new files. No commit in this task.

---

### Task 3: Verification battery (AC1 through AC6)

**Files:**
- None modified. Checks only. A failure here means fixing the file named in the failed check, then re-running the battery.

**Interfaces:**
- Consumes: Task 2's four files and pinned anchor strings.
- Produces: a passing AC1-AC6 record that Task 5's commit gate relies on.

**Model:** flash

- [ ] **Step 1: AC1, exactly four new files and a scoped-clean status**

```bash
ls CODE_OF_CONDUCT.md SECURITY.md CITATION.cff CHANGELOG.md
git status --porcelain | grep -Ev '^\?\? (docs/|CODE_OF_CONDUCT\.md|SECURITY\.md|CITATION\.cff|CHANGELOG\.md)'
```
Expected: `ls` lists exactly the four files; the `grep` prints nothing. Any other line (a modification, an addition, a stray file) fails AC1.

- [ ] **Step 2: AC2 and AC7 (text half), CoC is the verbatim 2.1 document with filled contact and attribution**

```bash
grep -c 'INSERT' CODE_OF_CONDUCT.md
grep -c '^+++' CODE_OF_CONDUCT.md
grep -c '^# Code of Conduct$' CODE_OF_CONDUCT.md
for h in "## Our Pledge" "## Our Standards" "## Enforcement Responsibilities" "## Scope" "## Enforcement" "## Enforcement Guidelines" "### 1. Correction" "### 2. Warning" "### 3. Temporary Ban" "### 4. Permanent Ban" "## Attribution"; do grep -qxF "$h" CODE_OF_CONDUCT.md || echo "MISSING: $h"; done; echo "heading-check-done"
grep -qF 'adapted from the [Contributor Covenant][homepage], version 2.1' CODE_OF_CONDUCT.md || echo "FAIL: attribution"
grep -qF 'through GitHub: open an issue on this repository' CODE_OF_CONDUCT.md || echo "FAIL: contact"
grep -qF 'https://github.com/jgsystemsconsulting' CODE_OF_CONDUCT.md || echo "FAIL: profile link"
grep -qxF '[translations]: https://www.contributor-covenant.org/translations' CODE_OF_CONDUCT.md || echo "FAIL: tail truncated"
```
Expected: `0`, `0`, `1`, then only `heading-check-done` (no `MISSING:` lines), then no `FAIL:` lines. The attribution grep proves the verbatim 2.1 footer survived; its `.html` link 301-redirects to the live canonical page, which AC2 accepts as a working link.

- [ ] **Step 3: AC3, SECURITY.md names the real path and scope**

```bash
grep -qF "private vulnerability reporting" SECURITY.md || echo "FAIL: report path"
grep -qF "Report a vulnerability" SECURITY.md || echo "FAIL: tab path"
grep -qF "5 business days" SECURITY.md || echo "FAIL: acknowledgment"
grep -qF "supported surface" SECURITY.md || echo "FAIL: supported scope"
grep -q '^|' SECURITY.md && echo "FAIL: table found"
echo "security-checks-done"
```
Expected: only `security-checks-done`. The `^|` grep proves no supported-versions markdown table shipped.

- [ ] **Step 4: AC4, CITATION.cff parses with the pinned assertions**

Run (spec-pinned command, verbatim):
`python -c "import yaml; d=yaml.safe_load(open('CITATION.cff')); assert d['cff-version']=='1.2.0'; assert d['title']=='Awesome SysML V2'; assert d['license']=='MIT'; assert d['repository-code']=='https://github.com/jgsystemsconsulting/awesome-sysml-v2'; assert d['preferred-citation']['type']=='generic'"`
Expected: exit 0, no output. If PyYAML is missing (Task 1 Step 6 flagged it), substitute any YAML parser for the parse step, for example `npx yaml-lint CITATION.cff`, and eyeball the five asserted fields.

- [ ] **Step 5: AC5, single Unreleased section, full run coverage, clean lint**

```bash
test "$(grep -c '^## \[' CHANGELOG.md)" = "1" || echo "FAIL: section count"
for p in P9 P6 P7 P8 P4 P2 P1; do grep -qF "($p)" CHANGELOG.md || echo "FAIL: missing $p"; done; echo "coverage-check-done"
npx markdownlint-cli2 CHANGELOG.md && echo "CHANGELOG-LINT-OK"
```
Expected: no `FAIL:` lines, only `coverage-check-done`, then `CHANGELOG-LINT-OK` with exit 0. The seven P-numbers cover all seven hardening runs (P9, P6, P7, P8, P4, P2, P1).

- [ ] **Step 6: AC6, nothing else touched**

```bash
git status --porcelain README.md contributing.md .github
git diff --stat
```
Expected: both empty. Combined with Step 1's scoped status, this proves no cross-links, no workflow edits, no entry changes.

**Done when:** every step prints its expected output. AC1 through AC6 all hold.

---

### Task 4: Enable private vulnerability reporting (AC7)

**Files:**
- None in the repo. This is a GitHub repository-settings change via the `gh` CLI.

**Interfaces:**
- Consumes: authenticated `gh` CLI with admin rights on `jgsystemsconsulting/awesome-sysml-v2`.
- Produces: `private_vulnerability_reporting_enabled == true` on the repository, the state AC7 asserts and SECURITY.md's report path depends on.

**Model:** flash

- [ ] **Step 1: Check the current setting**

Run: `gh api repos/jgsystemsconsulting/awesome-sysml-v2 --jq .private_vulnerability_reporting_enabled`
If it prints `true`, the setting is already on; skip Step 2.

- [ ] **Step 2: Enable it if false**

Run: `gh api -X PUT repos/jgsystemsconsulting/awesome-sysml-v2/private-vulnerability-reporting`

- [ ] **Step 3: Re-check**

Run: `gh api repos/jgsystemsconsulting/awesome-sysml-v2 --jq .private_vulnerability_reporting_enabled`
Expected output: `true`

**Done when:** the check prints `true`. If `gh` is unauthenticated or the PUT is forbidden, STOP and report instead of claiming AC7.

---

### Task 5: Single commit, nothing pushed

**Files:**
- Commit exactly: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, `CHANGELOG.md` (all new, all `A`).

**Interfaces:**
- Consumes: Task 3's passing battery and Task 4's `true`.
- Produces: commit `Add community root meta files` on top of `ccc0acc5aa90c18d1131f18e16a6b57529bab0e9`, parent of the next package's baseline.

**Model:** flash

- [ ] **Step 1: Stage exactly the four files**

```bash
git add CODE_OF_CONDUCT.md SECURITY.md CITATION.cff CHANGELOG.md
git diff --cached --name-status
```
Expected: exactly four lines, each starting with `A`, one per file, nothing else.

- [ ] **Step 2: Commit with the exact message**

```bash
git commit -m "Add community root meta files"
```

- [ ] **Step 3: Post-commit verification**

```bash
git log -1 --format=%s
git show --name-status --format="" HEAD
git rev-parse HEAD~1
git status --porcelain | grep -v '^?? docs/'
```
Expected: the subject is exactly `Add community root meta files`; `git show` lists exactly four `A` lines; `HEAD~1` is `ccc0acc5aa90c18d1131f18e16a6b57529bab0e9`; the scoped status is empty.

- [ ] **Step 4: Do not push**

Run no `git push` command of any kind. The package ends at the local commit. Confirm the commit is local-only by leaving the remote alone; the parent pipeline decides when anything ships.

**Done when:** Step 3's four checks all pass and no push happened.

---

## Self-review record

Spec coverage: AC1 is Task 3 Step 1 (existence and scoped status); AC2 is Task 2 Steps 1-3 plus Task 3 Step 2; AC3 is Task 2 Step 5 plus Task 3 Step 3; AC4 is Task 2 Step 6 plus Task 3 Step 4; AC5 is Task 2 Step 7 plus Task 3 Step 5; AC6 is Task 3 Steps 1 and 6; AC7 is Task 4. Non-goals are enforced by the Task 3 Step 6 checks and by Task 2 having no commit. Every file's full content or a complete fetch-and-substitute recipe appears in Task 2; no placeholders. Anchor strings, file names, the baseline hash, and the commit message are identical across tasks.
