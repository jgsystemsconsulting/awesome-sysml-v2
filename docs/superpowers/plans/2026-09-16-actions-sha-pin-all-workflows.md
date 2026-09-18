# Actions SHA Pin All Workflows Implementation Plan (P9)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace all seven mutable tag refs in the repository's three GitHub Actions workflows with research-verified full-length commit SHA pins, each with a version comment, plus one upgrade-path comment block per file.

**Architecture:** Pure text edits to three YAML files with zero behavior change: the same actions run at the same versions, only the ref spelling changes. A pre-flight commits-API re-check guards against tag drift before any edit is made. Within each file, ref edits come first, then the comment block insert, matching the spec's stated order. All edits land in one commit covering only the three workflow files.

**Tech Stack:** GitHub Actions YAML, curl plus jq (python json fallback), grep, PyYAML for parse checks, git.

**Spec:** C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-actions-sha-pin-all-workflows.md

## Global Constraints

- Touch only `.github/workflows/lint.yml`, `.github/workflows/links.yml`, `.github/workflows/stale.yml`. No other file.
- Forbidden edits (work-package boundaries): lint.yml permissions block and its `npx awesome-lint` line (P8 owns both); lychee arguments, triggers, or report handling (P7); stale.yml cutoff or curl logic (P6); README or content files; Dependabot or Renovate config (backlog).
- No changes to triggers, permissions, step order, `with:` inputs, env blocks, runner labels, or run scripts. Only the seven `uses:` lines change, plus the added comment blocks.
- Pins are the exact 40-hex SHAs from the pin table below. Never re-derive a SHA; copy from the table. Full length only, never short.
- Version comments are the bare resolved tag: `# v4`, `# v2`, `# v5`, `# v24`. No dates, no prose suffixes.
- The upgrade-path comment block is the verbatim 6 lines given in Task 2, inserted directly under each file's `name:` line and followed by one blank line.
- Single commit at the end, staging only the three workflow files. No intermediate commits.
- Workspace baseline at plan time: HEAD `af077117bec632c636ec914ddb8af002e6e4bc4b`, `.github/workflows/` clean.
- Line-number expectations in checks below are post-insert (each file gains 6 lines above the first `uses:` line: the six comment lines; the blank line after `name:` already exists and is kept).

## Research

SHAs verified 2026-09-16 through at least two independent primary paths per action (GitHub commits API, git refs API, releases pages). Key sources:

- https://api.github.com/repos/actions/checkout/commits/v4 (commits-API resolution, the method of record for all five actions)
- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions (pinning to a full-length commit SHA is currently the only way to use an action as an immutable release)
- https://docs.renovatebot.com/modules/manager/github-actions/ (a bare SHA without a version comment is disabled by default; basis for the `# vX` comments)
- https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066 (tag-retarget attack this pin defends against)
- https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-github-action-cve-2025-30066 (CISA remediation pins a specific commit)

Full graded claim table: `docs/superpowers/research/2026-09-16-actions-sha-pin-all-workflows-research.md`.

## Codebase context

From `docs/superpowers/context/2026-09-16-actions-sha-pin-all-workflows-context.md`: the seven-ref inventory below is corroborated by two independent reads (gate grep plus per-file cartographer reads) and matches the working tree at plan time. Permissions are `contents: read` plus `issues: write` at stale.yml:8-10 and links.yml:8-10; lint.yml declares none (P8 territory). No other Actions surface exists anywhere (no action.yml, no composite actions, no reusable-workflow callers), so seven refs is the complete set. All three files contain zero comments today, so the under-`name:` block placement sets the convention. `uses:` lines use the 6-space dash form for the checkout and setup-node steps, and the 8-space form for named steps.

## Pin table (source of truth)

Pre-insert line numbers, copied from the spec:

| File:line | Current ref | Pinned replacement (40-hex SHA) | Tag type |
|---|---|---|---|
| stale.yml:16 | `actions/checkout@v4` | `11d5960a326750d5838078e36cf38b85af677262` | lightweight |
| links.yml:16 | `actions/checkout@v4` | `11d5960a326750d5838078e36cf38b85af677262` | lightweight |
| links.yml:19 | `lycheeverse/lychee-action@v2` | `e7477775783ea5526144ba13e8db5eec57747ce8` | lightweight |
| links.yml:26 | `peter-evans/create-issue-from-file@v5` | `e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd` | lightweight |
| lint.yml:13 | `actions/checkout@v4` | `11d5960a326750d5838078e36cf38b85af677262` | lightweight |
| lint.yml:16 | `actions/setup-node@v4` | `49933ea5288caeca8642d1e84afbd3f7d6820020` | lightweight |
| lint.yml:22 | `DavidAnson/markdownlint-cli2-action@v24` | `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff` | annotated |

The markdownlint-cli2-action v24 tag is annotated: tag object SHA `28a7e8bdb81fd8ad675883de92c758ab78e0ce10`, peeled commit `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff`. Pin the peeled commit. Never substitute the tag object SHA.

---

### Task 1: Pre-flight tag-drift gate and working-tree baseline

**Files:**
- None modified (read-only gate)

**Interfaces:**
- Consumes: pin table above, working tree
- Produces: confirmation that all five live tag-to-SHA resolutions equal the pin table, and that the seven current refs match the baseline. Tasks 2-4 must not start until this gate passes.

**Model:** flash

- [ ] **Step 1: Confirm the workflows directory is clean and the tree matches the plan baseline**

```bash
git status --porcelain -- .github/workflows/
git rev-parse HEAD
```

Expected: no porcelain output, and HEAD equals `af077117bec632c636ec914ddb8af002e6e4bc4b`. Any porcelain output means uncommitted workflow changes exist; stop and resolve before proceeding. A different HEAD means the tree drifted since plan time: re-derive every line-number expectation against the current tree before proceeding.

- [ ] **Step 2: Baseline the seven current refs**

```bash
grep -n "^      - uses: actions/checkout@v4" .github/workflows/stale.yml .github/workflows/links.yml .github/workflows/lint.yml
grep -n "^        uses: lycheeverse/lychee-action@v2" .github/workflows/links.yml
grep -n "^        uses: peter-evans/create-issue-from-file@v5" .github/workflows/links.yml
grep -n "^      - uses: actions/setup-node@v4" .github/workflows/lint.yml
grep -n "^        uses: DavidAnson/markdownlint-cli2-action@v24" .github/workflows/lint.yml
```

Expected hits, exactly one per pattern: stale.yml:16, links.yml:16, lint.yml:13; links.yml:19; links.yml:26; lint.yml:16; lint.yml:22. Any mismatch between the working tree and the pin table's "Current ref" column stops work.

- [ ] **Step 3: Re-run the commits-API check for all five actions**

```bash
curl -s https://api.github.com/repos/actions/checkout/commits/v4 | jq -r .sha
curl -s https://api.github.com/repos/actions/setup-node/commits/v4 | jq -r .sha
curl -s https://api.github.com/repos/lycheeverse/lychee-action/commits/v2 | jq -r .sha
curl -s https://api.github.com/repos/peter-evans/create-issue-from-file/commits/v5 | jq -r .sha
curl -s https://api.github.com/repos/DavidAnson/markdownlint-cli2-action/commits/v24 | jq -r .sha
```

If jq is unavailable, use this form instead for each URL:

```bash
curl -s <url> | python -c "import json,sys; print(json.load(sys.stdin)['sha'])"
```

Expected outputs, in order, an exact match with the pin table:

1. `11d5960a326750d5838078e36cf38b85af677262` (checkout v4)
2. `49933ea5288caeca8642d1e84afbd3f7d6820020` (setup-node v4)
3. `e7477775783ea5526144ba13e8db5eec57747ce8` (lychee-action v2)
4. `e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd` (create-issue-from-file v5)
5. `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff` (markdownlint-cli2-action v24)

The commits API returns the commit SHA in `.sha` even for the annotated v24 tag, so the same comparison is valid for all five. These calls are unauthenticated and subject to GitHub's 60-per-hour rate limit; a rate-limited response prints `null` (or a JSON error message) instead of a SHA. Treat any `null` or message payload as a failed fetch and retry after the limit window — do not treat it as a tag mismatch.

- [ ] **Step 4: Compare and gate**

If any of the five live SHAs differs from the pin table, STOP before any edit. Report the action, the live SHA, and the spec SHA. Do not silently pin a newer commit; stop and report — a mismatch requires spec revision and re-approval before any pin change. Only a five-for-five exact match clears the gate.

**Done when:** Step 1 shows a clean workflows directory, Step 2 shows all seven baseline hits at the expected lines, and Step 3 matches the pin table on all five actions.

---

### Task 2: Pin stale.yml (1 ref + upgrade-path block)

**Files:**
- Modify: `.github/workflows/stale.yml`

**Interfaces:**
- Consumes: pin table rows for stale.yml, gate clearance from Task 1
- Produces: pinned stale.yml consumed by the Task 5 acceptance sweep

**Model:** flash

- [ ] **Step 1: Ref edit (stale.yml line 16, pre-insert)**

Old, exact:

```yaml
      - uses: actions/checkout@v4
```

New, exact:

```yaml
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
```

- [ ] **Step 2: Insert the upgrade-path comment block**

Old, exact (top of file):

```yaml
name: Freshness report

on:
```

New, exact (block verbatim from the spec, followed by one blank line):

```yaml
name: Freshness report
# Action refs are pinned to full-length commit SHAs (supply-chain hardening,
# per GitHub's security-hardening guide). To bump an action, resolve its tag
# to a commit SHA, e.g.:
#   curl -s https://api.github.com/repos/<owner>/<repo>/commits/<tag>
# Use the "sha" field (the commit, not a tag object SHA; see annotated-tag
# note in the repo spec for P9), then update the version comment to match.

on:
```

- [ ] **Step 3: Verify the file**

```bash
grep -n "^      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4" .github/workflows/stale.yml
grep -n "@v[0-9]" .github/workflows/stale.yml || echo "OK: no mutable tag refs remain"
python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/stale.yml
git diff -- .github/workflows/stale.yml
```

Expected: first grep returns exactly one hit at line 22; the mutable-tag grep reports OK; YAML parse exits 0; diff shows only the one `-`/`+` uses: pair plus the 6 added comment lines. Permissions block, cron, and the run scripts are untouched.

**Done when:** all three checks pass and the diff shape matches.

---

### Task 3: Pin links.yml (3 refs + upgrade-path block)

**Files:**
- Modify: `.github/workflows/links.yml`

**Interfaces:**
- Consumes: pin table rows for links.yml, gate clearance from Task 1
- Produces: pinned links.yml consumed by the Task 5 acceptance sweep

**Model:** flash

- [ ] **Step 1: Ref edits (pre-insert lines 16, 19, 26)**

Line 16, old exact:

```yaml
      - uses: actions/checkout@v4
```

Line 16, new exact:

```yaml
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
```

Line 19, old exact:

```yaml
        uses: lycheeverse/lychee-action@v2
```

Line 19, new exact:

```yaml
        uses: lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2
```

Line 26, old exact:

```yaml
        uses: peter-evans/create-issue-from-file@v5
```

Line 26, new exact:

```yaml
        uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5
```

- [ ] **Step 2: Insert the upgrade-path comment block**

Old, exact (top of file):

```yaml
name: Links

on:
```

New, exact (same verbatim block as Task 2 Step 2, followed by one blank line):

```yaml
name: Links
# Action refs are pinned to full-length commit SHAs (supply-chain hardening,
# per GitHub's security-hardening guide). To bump an action, resolve its tag
# to a commit SHA, e.g.:
#   curl -s https://api.github.com/repos/<owner>/<repo>/commits/<tag>
# Use the "sha" field (the commit, not a tag object SHA; see annotated-tag
# note in the repo spec for P9), then update the version comment to match.

on:
```

- [ ] **Step 3: Verify the file**

```bash
grep -n "^      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4" .github/workflows/links.yml
grep -n "^        uses: lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2" .github/workflows/links.yml
grep -n "^        uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5" .github/workflows/links.yml
grep -n "@v[0-9]" .github/workflows/links.yml || echo "OK: no mutable tag refs remain"
python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/links.yml
grep -n "args: --no-progress" .github/workflows/links.yml
```

Expected: three pin hits at lines 22, 25, 32; the mutable-tag grep reports OK; YAML parse exits 0; the boundary grep shows `args: --no-progress` still present at line 27 with content unchanged (P7 boundary).

**Done when:** all checks pass and `git diff -- .github/workflows/links.yml` shows only the three `-`/`+` uses: pairs plus the 6 added comment lines.

---

### Task 4: Pin lint.yml (3 refs + upgrade-path block)

**Files:**
- Modify: `.github/workflows/lint.yml`

**Interfaces:**
- Consumes: pin table rows for lint.yml, gate clearance from Task 1
- Produces: pinned lint.yml consumed by the Task 5 acceptance sweep

**Model:** flash

- [ ] **Step 1: Ref edits (pre-insert lines 13, 16, 22)**

Line 13, old exact:

```yaml
      - uses: actions/checkout@v4
```

Line 13, new exact:

```yaml
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
```

Line 16, old exact:

```yaml
      - uses: actions/setup-node@v4
```

Line 16, new exact:

```yaml
      - uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4
```

Line 22, old exact (this is the annotated tag; pin the peeled commit from the pin table):

```yaml
        uses: DavidAnson/markdownlint-cli2-action@v24
```

Line 22, new exact:

```yaml
        uses: DavidAnson/markdownlint-cli2-action@21c1be1b93ad9ed58fa840aacc3f279cde2a72ff # v24
```

- [ ] **Step 2: Insert the upgrade-path comment block**

Old, exact (top of file):

```yaml
name: Lint

on:
```

New, exact (same verbatim block as Task 2 Step 2, followed by one blank line):

```yaml
name: Lint
# Action refs are pinned to full-length commit SHAs (supply-chain hardening,
# per GitHub's security-hardening guide). To bump an action, resolve its tag
# to a commit SHA, e.g.:
#   curl -s https://api.github.com/repos/<owner>/<repo>/commits/<tag>
# Use the "sha" field (the commit, not a tag object SHA; see annotated-tag
# note in the repo spec for P9), then update the version comment to match.

on:
```

- [ ] **Step 3: Verify the file**

```bash
grep -n "^      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4" .github/workflows/lint.yml
grep -n "^      - uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4" .github/workflows/lint.yml
grep -n "^        uses: DavidAnson/markdownlint-cli2-action@21c1be1b93ad9ed58fa840aacc3f279cde2a72ff # v24" .github/workflows/lint.yml
grep -n "@v[0-9]" .github/workflows/lint.yml || echo "OK: no mutable tag refs remain"
python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/lint.yml
grep -n "npx awesome-lint README.md" .github/workflows/lint.yml
grep -c "permissions:" .github/workflows/lint.yml || echo "OK: no permissions block (P8 owns adding it)"
```

Expected: three pin hits at lines 19, 22, 28; the mutable-tag grep reports OK; YAML parse exits 0; `npx awesome-lint README.md` still present at line 26 unchanged; the permissions grep reports 0 matches (P8 owns adding it, not P9).

**Done when:** all checks pass and `git diff -- .github/workflows/lint.yml` shows only the three `-`/`+` uses: pairs plus the 6 added comment lines.

---

### Task 5: Acceptance sweep and single commit

**Files:**
- Commit: `.github/workflows/lint.yml`, `.github/workflows/links.yml`, `.github/workflows/stale.yml`

**Interfaces:**
- Consumes: the three pinned files from Tasks 2-4
- Produces: one commit containing only the three workflow files, passing all six spec acceptance criteria

**Model:** flash

- [ ] **Step 1: Acceptance criteria 1 and 2: seven exact pins, version comments, zero mutable tags**

```bash
grep -rn "uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4" .github/workflows/
grep -rn "uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4" .github/workflows/
grep -rn "uses: lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2" .github/workflows/
grep -rn "uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5" .github/workflows/
grep -rn "uses: DavidAnson/markdownlint-cli2-action@21c1be1b93ad9ed58fa840aacc3f279cde2a72ff # v24" .github/workflows/
grep -rn "@v[0-9]" .github/workflows/ || echo "OK: no mutable tag refs remain"
```

Expected: checkout pin hits in exactly three files (lint.yml, links.yml, stale.yml), one hit each; the other four patterns hit exactly once each in their file; the final grep finds no `@v[0-9]` anywhere under `.github/workflows/`.

- [ ] **Step 2: Acceptance criteria 3 and 6: verbatim upgrade-path block in all three files**

```bash
python - <<'EOF'
block = '''# Action refs are pinned to full-length commit SHAs (supply-chain hardening,
# per GitHub's security-hardening guide). To bump an action, resolve its tag
# to a commit SHA, e.g.:
#   curl -s https://api.github.com/repos/<owner>/<repo>/commits/<tag>
# Use the "sha" field (the commit, not a tag object SHA; see annotated-tag
# note in the repo spec for P9), then update the version comment to match.
'''
for f in ['.github/workflows/lint.yml', '.github/workflows/links.yml', '.github/workflows/stale.yml']:
    assert block in open(f, encoding='utf-8').read(), f
print('OK: verbatim upgrade-path block present in all three files')
EOF
```

Expected: the OK line prints. This also covers criterion 6: the commits-API method and the annotated-tag warning are documented in the repo.

- [ ] **Step 3: Acceptance criterion 4: diff scope and boundaries**

```bash
git diff --name-only
git diff --numstat
git diff
grep -n "npx awesome-lint README.md" .github/workflows/lint.yml
grep -c "permissions:" .github/workflows/lint.yml || echo "OK: no permissions block (P8 owns adding it)"
grep -n "issues: write" .github/workflows/links.yml .github/workflows/stale.yml
grep -n "args: --no-progress" .github/workflows/links.yml
grep -n "12 months ago" .github/workflows/stale.yml
```

Expected: `--name-only` lists exactly the three workflow files; `--numstat` shows lint.yml `9 3`, links.yml `9 3`, stale.yml `7 1` (7 rewritten uses: lines appear as delete/add pairs, 18 pure comment-line insertions); the full diff contains only the seven `-`/`+` uses: pairs and the three 6-line comment insertions; all boundary greps confirm P6/P7/P8 territory is untouched, with `grep -n "12 months ago" .github/workflows/stale.yml` expected to return exactly one hit at post-insert line 28.

- [ ] **Step 4: Acceptance criterion 5: YAML parse and indentation**

```bash
python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/lint.yml
python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/links.yml
python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/stale.yml
```

Expected: all three exit 0. Indentation is already proven by the `^`-anchored greps in Tasks 2-4 (6-space dash form for checkout and setup-node, 8-space form for named steps).

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/lint.yml .github/workflows/links.yml .github/workflows/stale.yml
git commit -m "Pin GitHub Actions to full-length commit SHAs"
```

- [ ] **Step 6: Post-commit verification**

```bash
git show --stat HEAD
git status --porcelain -- .github/workflows/
```

Expected: HEAD shows exactly the three workflow files and no others; the porcelain check returns no output.

**Done when:** every check in Steps 1-4 and 6 passes and the commit from Step 5 exists containing only the three workflow files. Any failure at any step stops work for diagnosis before commit.
