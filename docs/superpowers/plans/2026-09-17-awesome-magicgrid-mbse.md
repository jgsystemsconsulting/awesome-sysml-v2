# Awesome MagicGrid MBSE Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and publish `awesome-magicgrid-mbse`, a standalone public awesome list for the MagicGrid MBSE methodology under `jgsystemsconsulting`, seeded with 45+ verified entries, full lint and link automation, community meta files, a docs site, and both cross-links with awesome-sysml-v2.

**Architecture:** New sibling repo at `C:\Users\gower\OneDrive\Documents\GitHub\awesome-magicgrid-mbse`, ported from the awesome-sysml-v2 template. Verbatim copies where the template is repo-agnostic; adaptations where it is not (workflows lose their P9 header comment, links.yml gains a lychee accept set, contributing.md and docs/index.html get full MagicGrid rewrites, docs/site.css loses its MIT/template header, CITATION.cff and CHANGELOG.md are fresh with consistent CC0). Content seeding follows the spec's seed-time verification rule with a separate 403 extraction pass diffed against a CHANGELOG allowlist. Publication is gated on a clean local run of awesome-lint, markdownlint-cli2, and lychee before `gh repo create`.

**Tech Stack:** Markdown, static HTML, GitHub Actions (Node 20, actions pinned to full commit SHAs), `npx awesome-lint@2.3.0`, `npx markdownlint-cli2`, native `lychee` binary, `gh` CLI, Git Bash on Windows.

**Spec:** docs/superpowers/specs/2026-09-17-awesome-magicgrid-mbse.md (the plan argues from the spec; executors read both)

## Global Constraints

- New repo path: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-magicgrid-mbse` (Git Bash: `/c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse`). Template path: `/c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2`. The target directory must not exist before Task 1; if it exists, STOP and report.
- License is CC0 1.0 Universal in LICENSE, CITATION.cff (`license: CC0-1.0`), and the docs site (masthead `LICENCE: CC0`, footer "CC0 Licence"). Template MIT identity strings are never shipped: strip the MIT SPDX and awesome-sysml-v2 Source URL from the `docs/site.css` header on copy, and never copy CITATION.cff or docs/index.html MIT strings.
- No social-card files in v1: do not copy `social-card.jpg` or `social-card.png`, and do not write `og:image` or `twitter:image` tags in docs/index.html.
- Workflow copies must not contain the string `P9` or `repo spec`; the header comment citing "the repo spec for P9" is stripped from all three workflows.
- `links.yml` and the local gate use the same lychee accept set: `--accept '200,204,301,308,403'`. The 403 allowlist is enforced only by the local publication gate (Task 7), never by the advisory CI report.
- Entry format everywhere: `- [Name](URL) - One factual sentence.` starting uppercase, ending with a period, sorted alphabetically case-insensitive by link text within each section. Each URL appears in at most one content section; the intro's sister-list cross-link is not a content entry and is exempt.
- Descriptions name the vendor affiliation (No Magic or Dassault Systemes) wherever the author, presenter, or publisher is vendor staff, as confirmed by the resource page itself or the research file.
- Never link or host Book of Knowledge PDFs or pirate aggregator copies. Books link Goodreads, publisher, or library catalog pages only. Never construct deep documentation paths; link only URLs verified in the research scan or at seed time.
- No CSS or JavaScript magic-grid layout library appears anywhere in the repo. contributing.md excludes them explicitly.
- Tool pins: `awesome-lint@2.3.0`, `markdownlint-cli2` (npx, matching lint.yml), Node 20 in CI, action SHAs copied verbatim from the template. `gh` must be authenticated (`gh auth status`).
- Context gate: `context: ad-hoc (template inventory in spec + live tree)`. No separate context file; spec section "Codebase context" plus the live-tree checks recorded below are the context.
- The template repo awesome-sysml-v2 is modified exactly once, by Task 9, with one inserted line. Every other task writes only inside the new repo.
- Commands are Git Bash on Windows. `set -e` behavior: absence checks use count wrappers so exit 1 cannot abort a script block.
- Commit messages are given per task. Only the new repo gets commits from Tasks 1 through 8; Task 9 commits and pushes in awesome-sysml-v2 per the spec's publication step 10.

## Research

Gate: `docs/superpowers/research/2026-09-17-awesome-magicgrid-mbse-research.md` (verdict: gap is real, 40-70 linkable items reachable, core high-signal set 35-50). Key URLs the spec and this plan rely on:

- https://www.3ds.com/products/catia/catia-magic
- https://www.3ds.com/products/catia/no-magic
- https://www.3ds.com/products/catia/no-magic/cameo-systems-modeler
- https://docs.nomagic.com/
- https://www.3ds.com/edu/catia-magic-training
- https://www.3ds.com/edu/catia-magic-training/mbse-sysml-v2-and-magicgrid
- https://doi.org/10.1002/j.2334-5837.2017.00350.x (MBSE Grid origin paper, 2017)
- https://doi.org/10.1002/inst.12429 (V&V with MagicGrid, INSIGHT 2023)
- https://www.goodreads.com/book/show/56720281-magicgrid-book-of-knowledge
- https://github.com/matthieugourssies/sysml-magicgrid-vccs (the one real MBSE hit among GitHub MagicGrid results; the rest are CSS/JS grid libraries and stubs)

Research findings honored by this plan: guessed deep doc URLs 404 and old `nomagic.com` paths return 403, so links are verified, never constructed; top-level CATIA Magic marketing pages mention MagicGrid zero times, so the method lives in training, docs, and papers; standard awesome-list trademark posture (descriptive use plus disclaimer); standalone build now, fold into a public awesome-mbse later only if that repo goes public.

## Codebase context

Live-checked at plan time against the template tree (2026-09-17):

- `.github/workflows/lint.yml`, `links.yml`, `stale.yml`: each has a 6-line header comment block (lines 2-7) ending with the phrase `repo spec for P9`. Bodies below the comment are repo-agnostic. A grep confirms none of the three workflows contains the string `awesome-sysml-v2`, so the bodies can ship verbatim after the comment strip. Pinned SHAs: checkout `11d5960a326750d5838078e36cf38b85af677262` (v4), setup-node `49933ea5288caeca8642d1e84afbd3f7d6820020` (v4), markdownlint-cli2-action `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff` (v24), lychee-action `e7477775783ea5526144ba13e8db5eec57747ce8` (v2). links.yml lychee args line: `args: --no-progress --max-retries 3 README.md`.
- `.markdownlint-cli2.jsonc`: `{"config": {"MD013": false}}`. Needed by the markdownlint gate.
- `LICENSE`: CC0 1.0 Universal full text. `SECURITY.md`: no repo-name strings (verified). `CODE_OF_CONDUCT.md`: Contributor Covenant 2.1, contact is "repository owner through the profile at https://github.com/jgsystemsconsulting", no repo-name string (verified). Both can ship verbatim per the spec's skeleton table (CODE_OF_CONDUCT is labeled adapt but its only contact/profile reference is already correct).
- `CITATION.cff`: template says `license: MIT`, inconsistent with the CC0 LICENSE. The new repo writes CC0-1.0; fixing the template itself is out of scope.
- `contributing.md`: five numbered criteria, criterion 4 is the 24-month freshness rule with the foundational-value exception (stale.yml references "criterion 4" in its report text, so the new file must keep the exception in criterion 4). Local commands pin `npx awesome-lint@2.3.0 README.md` and `npx markdownlint-cli2 "README.md" "contributing.md"`; lychee is a native binary with per-platform install guidance. Entry format paragraph ends "Commercial products go in the Commercial Tools section only."
- `docs/index.html`: 123 lines, dark scheme, canonical `https://jgsystemsconsulting.github.io/awesome-sysml-v2/`, masthead with `LICENCE: MIT` and `DOC-ID: JGS-AWESOME-SYSML-V2`, JSON-LD SoftwareApplication block, og:image and twitter:image pointing at social-card.png, 11-row category table, footer "MIT Licence". `docs/site.css` (2845 bytes) is CSS-body-agnostic but its first two comment lines cite `awesome-sysml-v2` and `SPDX-License-Identifier: MIT`, so the copy must strip or rewrite those two lines (body stays). `docs/.nojekyll` is empty.
- Template README ends with `## Contributing` and one sentence linking contributing.md; 13 H2 sections total. The new README mirrors that ending.
- Template working tree: `docs/index.html`, `docs/social-card.jpg`, `docs/social-card.png` may be dirty from prior companion-site work. Task 9 touches only `README.md` and pre-checks it is clean.

## File structure

Everything below is inside the new repo unless stated. Verbatim copies keep template bytes; adaptations are full rewrites supplied in this plan.

- `.github/workflows/lint.yml` (copy, strip lines 2-7)
- `.github/workflows/links.yml` (copy, strip lines 2-7, one args change)
- `.github/workflows/stale.yml` (copy, strip lines 2-7)
- `.markdownlint-cli2.jsonc`, `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md` (verbatim copies)
- `docs/.nojekyll` (empty), `docs/site.css` (copy body; strip MIT SPDX and awesome-sysml-v2 Source header lines)
- `docs/index.html` (full rewrite, supplied)
- `CITATION.cff` (fresh, supplied), `CHANGELOG.md` (fresh, supplied; accepted-403 list filled in Task 7)
- `contributing.md` (full adaptation, supplied)
- `README.md` (fresh; scaffolding supplied in Task 5, entries seeded and verified in Task 5)

---

## Task 1: Repo scaffold, git init, verbatim copies

**Files:**
- Create: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-magicgrid-mbse\` tree with `.markdownlint-cli2.jsonc`, `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `docs/.nojekyll`, adapted `docs/site.css`

**Interfaces:**
- Produces: the repo root with git on branch `main`, all verbatim copies in place. Tasks 2-7 write the remaining files into this tree. This task starts the spec's publication steps 1-2 (skeleton plus `git init`, branch main); the binding order the spec requires, `git init` before the local lint run, is preserved because Tasks 1-5 build and Task 7 lints.

**Model:** flash (mechanical copies with exact commands)

- [ ] **Step 1: Guard and create the repo directory with git**

Run:
```bash
TPL="/c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2"
NEW="/c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse"
test ! -e "$NEW" || { echo "STOP: target already exists"; exit 1; }
test -d "$TPL/.git" || { echo "STOP: template not found"; exit 1; }
mkdir -p "$NEW/.github/workflows" "$NEW/docs"
cd "$NEW" && git init -b main
```
Expected: `Initialized empty Git repository` on branch main.

- [ ] **Step 2: Copy the verbatim files**

Run:
```bash
TPL="/c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2"
NEW="/c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse"
cp "$TPL/.markdownlint-cli2.jsonc" "$NEW/.markdownlint-cli2.jsonc"
cp "$TPL/LICENSE" "$NEW/LICENSE"
cp "$TPL/SECURITY.md" "$NEW/SECURITY.md"
cp "$TPL/CODE_OF_CONDUCT.md" "$NEW/CODE_OF_CONDUCT.md"
cp "$TPL/docs/.nojekyll" "$NEW/docs/.nojekyll"
cp "$TPL/docs/site.css" "$NEW/docs/site.css"
# Rewrite the two-line MIT/template header to CC0; keep CSS body from line 3.
python -c "from pathlib import Path; p=Path(r\"C:/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse/docs/site.css\"); lines=p.read_text(encoding=\"utf-8\").splitlines(True); body=lines[2:] if len(lines)>=2 else lines; hdr=[\"/* Copyright (c) 2026 JG Systems Consulting Ltd. See LICENSE (CC0-1.0). */\n\", \"/* SPDX-License-Identifier: CC0-1.0 */\n\"]; p.write_text(\"\".join(hdr+body), encoding=\"utf-8\"); print(\"site.css header rewritten to CC0\")"
```

- [ ] **Step 3: Verify the copies and the MIT/CC0 split**

Run:
```bash
NEW="/c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse"
cd "$NEW"
ls -la . docs
grep -c "CC0 1.0 Universal" LICENSE
diff "$NEW/.markdownlint-cli2.jsonc" "/c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2/.markdownlint-cli2.jsonc" && echo cfg-ok
tail -n +3 docs/site.css > /tmp/new-css-body
tail -n +3 /c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2/docs/site.css > /tmp/tpl-css-body
diff /tmp/new-css-body /tmp/tpl-css-body && echo css-body-ok
grep -n "SPDX-License-Identifier" docs/site.css
grep -n "awesome-sysml-v2" docs/site.css && echo "FAIL: template URL remains" || echo css-header-ok
wc -c docs/.nojekyll
grep -rn "MIT" LICENSE docs/site.css || echo "no MIT strings in LICENSE or site.css"
```
Expected: LICENSE contains CC0 1.0 Universal; cfg-ok; css-body-ok; site.css SPDX line is CC0-1.0; css-header-ok (no awesome-sysml-v2); `.nojekyll` is 0 bytes; MIT grep prints `no MIT strings in LICENSE or site.css`.

- [ ] **Step 4: Commit**

Run:
```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git add -A
git commit -m "Scaffold repo with template files and CC0 site.css header"
```

Done when: five files copied byte-identical (markdownlint config, LICENSE, SECURITY.md, CODE_OF_CONDUCT.md, docs/.nojekyll), docs/site.css copied with CC0 header rewrite (body byte-identical from line 3), git initialized on main, one commit.

## Task 2: Workflows port (strip P9 comment, links.yml accept set)

**Files:**
- Create: `.github/workflows/lint.yml`
- Create: `.github/workflows/links.yml`
- Create: `.github/workflows/stale.yml`

**Interfaces:**
- Produces: three workflows with no `P9`/`repo spec` strings, all action SHAs identical to the template, and links.yml lychee args `--no-progress --max-retries 3 --accept '200,204,301,308,403' README.md`. Task 7's local gate and Task 8's CI green check depend on these exact files. contributing.md's maintenance section (Task 4) describes these three workflows.

**Model:** flash (complete file bodies below; mechanical transcription)

- [ ] **Step 1: Write `.github/workflows/lint.yml` (template minus the comment block)**

```yaml
name: Lint

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4
        with:
          node-version: 20
      - name: awesome-lint
        run: npx awesome-lint@2.3.0 README.md
      - name: markdownlint
        uses: DavidAnson/markdownlint-cli2-action@21c1be1b93ad9ed58fa840aacc3f279cde2a72ff # v24
        with:
          globs: |
            README.md
            contributing.md
```

- [ ] **Step 2: Write `.github/workflows/links.yml` (comment stripped, accept set added)**

```yaml
name: Links

on:
  schedule:
    - cron: "0 18 * * 1"
  workflow_dispatch:
  pull_request:

permissions:
  contents: read
  issues: write

jobs:
  linkChecker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
      - name: Link Checker
        id: lychee
        uses: lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2
        with:
          args: --no-progress --max-retries 3 --accept '200,204,301,308,403' README.md
          fail: false
          token: ${{ secrets.GITHUB_TOKEN }}
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

The only body change from the template is the args line: `--accept '200,204,301,308,403'` inserted so the weekly and PR scans match the local zero-broken gate. Weekly and PR scans stay advisory on exit code only.

- [ ] **Step 3: Write `.github/workflows/stale.yml` (template minus the comment block)**

```yaml
name: Freshness report

on:
  schedule:
    - cron: "0 6 1 * *"
  workflow_dispatch:

permissions:
  contents: read
  issues: write

jobs:
  freshness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
      - name: Build freshness report
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
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
      - name: Create or update the issue
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          existing=$(gh issue list --state open --search "Freshness report in:title" --json number --jq ".[0].number // empty")
          if [ -n "$existing" ]; then
            gh issue edit "$existing" --body-file freshness-report.md
          else
            gh issue create --title "Freshness report" --body-file freshness-report.md
          fi
```

- [ ] **Step 4: Verify the workflow port**

Run:
```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
grep -rn "P9\|repo spec" .github/workflows/ || echo "no P9/repo-spec strings"
grep -rn "awesome-sysml-v2" .github/workflows/ || echo "no template repo strings"
test "$(grep -c "11d5960a326750d5838078e36cf38b85af677262" .github/workflows/*.yml | awk -F: '{s+=$2} END{print s}')" = "3"
grep -n "accept" .github/workflows/links.yml
grep -c "accept" .github/workflows/lint.yml .github/workflows/stale.yml || true
git diff --stat 2>/dev/null; git status --porcelain
```
Expected: no `P9` or `repo spec` matches; no `awesome-sysml-v2` matches; checkout SHA appears once in each of the three files (3 total); the accept string appears once, in links.yml only; status shows the three new files.

- [ ] **Step 5: Commit**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git add .github/workflows
git commit -m "Port lint, links, and stale workflows with lychee accept set"
```

## Task 3: CITATION.cff, CHANGELOG.md, community file check

**Files:**
- Create: `CITATION.cff` (fresh)
- Create: `CHANGELOG.md` (fresh; accepted-403 subsection is appended by Task 7, not here)

**Interfaces:**
- Produces: citation metadata with `license: CC0-1.0` and `repository-code` set to the final URL `https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse`; a 1.0.0 changelog that Task 7 extends with the accepted-403 list and the recorded clean lychee run. CODE_OF_CONDUCT.md and SECURITY.md were already copied in Task 1.

**Model:** flash (complete file bodies below)

- [ ] **Step 1: Write `CITATION.cff`**

```yaml
cff-version: 1.2.0
message: "If you use this list in your work, please cite it using this metadata."
title: Awesome MagicGrid MBSE
authors:
  - entity:
      name: "JG Systems Consulting Ltd"
license: CC0-1.0
repository-code: https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse
preferred-citation:
  type: generic
  title: "Awesome MagicGrid MBSE"
  authors:
    - entity:
        name: "JG Systems Consulting Ltd"
  year: 2026
  repository-code: https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse
```

- [ ] **Step 2: Write `CHANGELOG.md`**

The date is set to the execution date, not hard-coded. Task 7 appends the Accepted-403 subsection and a clean-run bullet under Added.

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - EXEC_DATE

### Added

- Initial public release: curated list for the MagicGrid MBSE methodology with 45+ verified entries across nine sections.
- Lint gate (awesome-lint, markdownlint) on every pull request and push to main.
- Weekly lychee link scan and monthly freshness report, both advisory.
- Companion documentation site under docs/, published with GitHub Pages.
```

Run to stamp the date:
```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
sed -i "s/EXEC_DATE/$(date +%F)/" CHANGELOG.md
grep -n "^## \[1.0.0\]" CHANGELOG.md
```
Expected: one line, `## [1.0.0] - 2026-09-17` (or the actual execution date).

- [ ] **Step 3: Verify CC0 consistency across the repo so far**

Run:
```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
grep -n "license" CITATION.cff
grep -rn "MIT" CITATION.cff CHANGELOG.md LICENSE CODE_OF_CONDUCT.md SECURITY.md || echo "no MIT strings anywhere"
grep -c "CC0" LICENSE CITATION.cff
```
Expected: `license: CC0-1.0`; the MIT grep exits nonzero; LICENSE and CITATION.cff both reference CC0.

- [ ] **Step 4: Commit**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git add CITATION.cff CHANGELOG.md
git commit -m "Add citation metadata and changelog with CC0 licensing"
```

## Task 4: contributing.md adapted for MagicGrid

**Files:**
- Create: `contributing.md`

**Interfaces:**
- Produces: the contribution guide referenced by README's Contributing section (Task 5) and quoted by stale.yml's criterion-4 mention. The five-criterion order matches the template with criterion 4 as the freshness rule carrying the foundational-value exception. The lychee line matches the Task 7 gate exactly.

**Model:** flash (complete file body below)

- [ ] **Step 1: Write `contributing.md`**

```markdown
# Contributing to Awesome MagicGrid MBSE

Suggestions and pull requests are welcome. Every entry and every PR must meet the criteria below.

## Inclusion criteria

1. Stable, reachable URL pointing at the resource itself.
2. Direct MagicGrid methodology relevance: official material, the Book of Knowledge, papers and case studies, talks, training, example models, or tool support for applying the method. Generic SysML language material is excluded (the sister list awesome-sysml-v2 covers it), generic MBSE content beyond the method and named peer methodologies is excluded, and CSS or JavaScript "magic grid" layout libraries are excluded at any quality level. Peer methodologies (OOSEM, Harmony-SE, SYSMOD, Arcadia/Capella) appear only as one-line pointers under Related Methodologies.
3. One-line factual description, no marketing adjectives. When the author or presenter is No Magic or Dassault Systemes staff, the description names that affiliation so readers can weigh the source.
4. Active maintenance (commit within 24 months) or foundational value (the MBSE Grid origin paper, the MagicGrid Book of Knowledge, canonical vendor pages).
5. Not a duplicate of an existing entry, and each URL appears in at most one content section. The intro's sister-list cross-link is not a content entry and is exempt.

Registration-walled links are allowed only when the walled page is the canonical source, for example official vendor training. Never link or host copies of the MagicGrid Book of Knowledge PDF or other copyrighted material; link the Goodreads, publisher, or library catalog page instead.

## Entry format

One line per entry, exactly:

```markdown
- [Name](URL) - Description.
```

The name is the resource or product proper name. The URL is canonical: repo root for GitHub projects, product page for commercial tools, no tracking parameters, no trailing slash on GitHub repo roots. The description is one factual sentence that starts uppercase and ends with a period; a short parenthetical is allowed after the first word, for example "(INCOSE 2024)". Entries are sorted alphabetically, case-insensitive, by link text within each section. Commercial products go in the Tool Support section only.

## Local commands

Run these from the repository root before opening a PR:

```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

### Link check

`lychee` is a native binary, not an npm package. Install it once with your platform package manager (`scoop`, `winget`, or `choco` on Windows, `brew` on macOS, `pacman`, `zypper`, `snap`, or `apk` on Linux), then run from the repository root:

```bash
lychee --accept '200,204,301,308,403' README.md
```

Export `GITHUB_TOKEN` (for example `GITHUB_TOKEN=$(gh auth token)`) to avoid GitHub rate limiting on `github.com` links. Third-party sites sometimes return transient timeouts or 429s; retry before treating a failure as a broken link. A 403 is accepted only for canonical vendor sources known to block bots, for example DOIs resolving to Wiley; the accepted set is listed in CHANGELOG.md and enforced at the publication gate.

## Maintenance

Three workflows in `.github/workflows/` run on a fixed cadence. This section states what each does.

### Link scan (weekly)

`links.yml` runs lychee every Monday at 18:00 UTC, on every pull request, and on manual dispatch, with the accept set `200,204,301,308,403` matching the local command above. The check is advisory: a PR with broken links gets a warning but is never blocked by it. The "Link Checker Report" issue is created or updated only when the check exits nonzero; a clean run leaves that issue untouched. The accepted-403 allowlist in CHANGELOG.md is enforced by the publication gate, not by this workflow.

### Freshness report (monthly)

`stale.yml` runs on the first day of each month at 06:00 UTC, or on manual dispatch. It collects the `github.com` repository URLs from README.md and lists repos with no push in the last 24 months. The report is advisory: an entry past the window can still be valid under the foundational-value exception (criterion 4). The "Freshness report" issue is refreshed on every run, including months with no stale entries. Criterion 4 speaks of a commit within 24 months; the report measures the repository's last push, which is usually but not always the same thing.

### Lint gates (every PR and push to main)

`lint.yml` runs `awesome-lint@2.3.0` on README.md, and `markdownlint` on README.md and contributing.md, on every pull request targeting main and every push to main. These gates block merge on failure. The local markdownlint command above installs an unpinned npx package and may differ from the version CI runs; the pinned `awesome-lint@2.3.0` matches CI exactly.
```

- [ ] **Step 2: Verify the adaptation**

Run:
```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
head -1 contributing.md
grep -c "^## " contributing.md
grep -n "criterion 4\|criterion 4)" contributing.md | head -3
grep -n "magic grid" contributing.md
grep -n "lychee --accept '200,204,301,308,403' README.md" contributing.md
grep -n "Tool Support section only" contributing.md
grep -c "sister list" contributing.md
```
Expected: H1 is `# Contributing to Awesome MagicGrid MBSE`; four H2 sections (Inclusion criteria, Entry format, Local commands, Maintenance) plus three H3 under Maintenance, total `^## ` count 4; criterion 4 carries the foundational-value exception; the explicit magic-grid exclusion line exists; the lychee line matches the gate; the Tool Support sentence replaced the template's Commercial Tools sentence; the sister-list mention exists in criterion 2 (grep count 1).

- [ ] **Step 3: Commit**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git add contributing.md
git commit -m "Add MagicGrid contribution guide"
```

## Task 5: README seeding with seed-time verification

**Files:**
- Create: `README.md` (scaffolding below, then entries)

**Interfaces:**
- Produces: the seeded README with nine content sections meeting the spec minimums (sum 45), the verbatim disclaimer, both cross-link surfaces in the new repo (intro sentence plus the Related Methodologies sister-list entry), and a working list of accepted 403 URLs handed to Task 7. Tasks 6 (docs site anchors), 7 (lint and lychee gates), and 8 (publication) consume this.

**Model:** deep (content-heavy, verification judgment, multi-pass expansion)

- [ ] **Step 1: Write the README scaffolding**

Fixed text, verbatim from the spec. Entries are inserted under each H2 in the steps that follow.

```markdown
# Awesome MagicGrid MBSE [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of resources for the MagicGrid MBSE methodology: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support. For SysML v2 language and tooling, see the sister list [awesome-sysml-v2](https://github.com/jgsystemsconsulting/awesome-sysml-v2).

> This list is maintained independently. It is not affiliated with, endorsed by, or sponsored by Dassault Systemes or No Magic. MagicGrid is a methodology brand of No Magic, now part of Dassault Systemes. Every entry links to a legitimate public source; this list does not host copies of the MagicGrid Book of Knowledge or other copyrighted material.

## Contents

- [Official Resources](#official-resources)
- [Books and Formal Publications](#books-and-formal-publications)
- [Papers and Case Studies](#papers-and-case-studies)
- [Training and Courses](#training-and-courses)
- [Videos and Talks](#videos-and-talks)
- [Example Models](#example-models)
- [Tool Support](#tool-support)
- [Community](#community)
- [Related Methodologies](#related-methodologies)

## Official Resources

## Books and Formal Publications

## Papers and Case Studies

## Training and Courses

## Videos and Talks

## Example Models

## Tool Support

## Community

## Related Methodologies

## Contributing

See [contributing.md](contributing.md) for the inclusion criteria, entry format, local lint commands, and maintenance cadence.
```

The disclaimer blockquote is byte-identical to the spec; do not reword it. The intro cross-link and the Related Methodologies sister-list entry are the two new-repo cross-link surfaces; the intro line is not a content entry.

- [ ] **Step 2: Verify every candidate URL before it lands (seed-time rule)**

For each URL from the candidate tables below and every expansion find, run:

```bash
url="PASTE_URL"
code=$(curl -sSL -o /dev/null -w '%{http_code}' --max-time 30 "$url"); echo "$code $url"
```

Accept: `200`; `301` or `308` only when the landing page matches the intended resource, checked with `curl -sSL -o /dev/null -w '%{url_effective}' "$url"` and a manual look at the final page (lychee status alone is not enough); `403` only when the URL is the canonical vendor source known to block bots (DOIs resolving to Wiley, named vendor pages), in which case record it in `~/magicgrid-403-accepted.txt`, one bare URL per line, for the Task 7 allowlist. Before any seed URL is checked, run `touch ~/magicgrid-403-accepted.txt` so Task 7 always has a readable allowlist file even when zero 403s occur. Reject: `404`, repeated timeouts (retry once before rejecting), parked or squatted domains, dead DOIs (verify resolution with `curl -sI "https://doi.org/..."` showing a Location header). For GitHub repo candidates, also confirm the repo is MBSE-related and not a CSS/JS grid library: language or description must show modeling content, and `curl -s "https://api.github.com/repos/OWNER/REPO" | grep -E '"description"|"language"'` must not indicate a web layout library.

- [ ] **Step 3: Seed Official Resources (minimum 4)**

Candidates from the research scan, each verified per Step 2 before landing:

```markdown
- [CATIA Magic product family](https://www.3ds.com/products/catia/catia-magic) - Dassault Systemes product page for the CATIA Magic modeling family that implements MagicGrid.
- [Cameo Systems Modeler](https://www.3ds.com/products/catia/no-magic/cameo-systems-modeler) - Dassault Systemes page for the Cameo Systems Modeler modeling environment.
- [docs.nomagic.com](https://docs.nomagic.com/) - Vendor documentation hub for CATIA Magic and Cameo products.
- [MBSE with SysML V2 and MagicGrid course](https://www.3ds.com/edu/catia-magic-training/mbse-sysml-v2-and-magicgrid) - Official Dassault Systemes three-day course on MBSE with SysML v2 and MagicGrid.
```

Note: CATIA Magic product family and Cameo Systems Modeler are also listed under Tool Support candidates below. The one-URL-per-section rule means each goes in exactly one section; put the product family and Cameo page under Tool Support and keep Official Resources to the docs hub, training catalog, and course pages. Keep Official Resources to docs hub, training catalog, and course pages only (product family and Cameo go under Tool Support). Required Official set after the Tool Support move: (1) docs.nomagic.com, (2) the MagicGrid course page, (3) the plain training catalog `https://www.3ds.com/edu/catia-magic-training` if it verifies, (4) a second official course page findable by browsing the catalog (never by guessing its path), or another verified top-level official hub. If fewer than 4 Official entries verify after those fallbacks, STOP and report; do not invent paths. Sort by link text before finishing.

- [ ] **Step 4: Seed Books and Formal Publications (minimum 2)**

```markdown
- [MagicGrid Book of Knowledge](https://www.goodreads.com/book/show/56720281-magicgrid-book-of-knowledge) - The MagicGrid Book of Knowledge by No Magic methodology staff (Aiste Aleksandraviciene et al.), Vitae Litera, 2018.
```

Second entry: edition-2 material only as verified. Search for a publisher, library catalog, or vendor page for the BoK second edition; if none verifies, substitute another verified formal publication about the method (for example a verified OpenAlex hit with a monograph or chapter DOI). Never link a PDF of the BoK or any aggregator copy. If fewer than 2 Books entries verify, STOP and report.

- [ ] **Step 5: Seed Papers and Case Studies (minimum 12)**

Ten candidate DOIs from the research scan; verify each per Step 2 (DOI resolution, then final status):

```markdown
- [Architecture meta-model for MagicGrid (2024)](https://doi.org/10.1002/iis2.13284) - INCOSE 2024 paper proposing an architecture meta-model for the MagicGrid framework.
- [Extending MagicGrid for virtual prototyping (2024)](https://doi.org/10.1145/3652620.3686249) - ACM 2024 paper on extending MagicGrid for virtual prototyping.
- [Flight-control requirements case study (2024)](https://doi.org/10.1007/978-981-97-0550-4_3) - Springer 2024 case study applying MagicGrid to flight-control requirements.
- [Mainstream MBSE methodologies survey (2022)](https://doi.org/10.3233/faia220529) - 2022 survey comparing mainstream MBSE methodologies including MagicGrid.
- [MBSE Grid origin paper (2017)](https://doi.org/10.1002/j.2334-5837.2017.00350.x) - INCOSE 2017 paper introducing MBSE Grid, the precursor to MagicGrid, by No Magic methodology staff.
- [Space remote-sensing case study (2020)](https://doi.org/10.1007/978-981-33-4102-9_35) - Springer 2020 case study applying MagicGrid to a space remote-sensing system.
- [SysML v1 vs v2 in MagicGrid scope (2024)](https://doi.org/10.1002/iis2.13257) - INCOSE 2024 paper comparing SysML v1 and v2 use within MagicGrid scope.
- [SysML v2 solution architecture with MagicGrid (2025)](https://doi.org/10.1002/iis2.70000) - INCOSE 2025 paper on a SysML v2 solution architecture using MagicGrid.
- [Towards a Common SE Methodology (2020)](https://doi.org/10.1002/j.2334-5837.2020.00713.x) - INCOSE 2020 paper toward a common systems engineering methodology grounded in MBSE Grid.
- [V&V using MagicGrid (2023)](https://doi.org/10.1002/inst.12429) - INSIGHT 2023 article on verification and validation with MagicGrid.
```

Affiliation clauses: the origin paper's No Magic attribution is supported by the research file; for every other entry, name a vendor affiliation in the description only if the paper's landing page confirms it, and leave it out otherwise. Expansion to reach 12: query OpenAlex and verify hits per Step 2.

```bash
curl -s "https://api.openalex.org/works?filter=title.search:MagicGrid&per-page=100" | jq -r '.results[] | .title + " " + (.doi // "no-doi")'
curl -s "https://api.openalex.org/works?filter=fulltext.search:MagicGrid&per-page=100&sort=publication_date:desc" | jq -r '.results[] | .title + " " + (.doi // "no-doi")'
```

Cull to MagicGrid-relevant works, keep DOI-bearing ones, verify, and add the best until the section holds at least 12. If fewer than 12 pass verification after both queries and a second retry pass, STOP and report the actual count; do not pad with weak entries.

- [ ] **Step 6: Seed Training and Courses (minimum 4)**

Partner courses and seminars beyond the official catalog (the official catalog and course pages live under Official Resources). Verify each candidate per Step 2 before landing. Candidates to check: MBSE4U training pages that mention MagicGrid (start at `https://www.mbse4u.com/` and browse, never guess deep paths), university or partner seminar pages for "SysML Made Simple with MagicGrid" style seminars (the research file records one full seminar video, so the delivering organization likely has a course page), and any partner listing on the 3DS training catalog page. Expansion searches: `curl -s "https://api.openalex.org/works?filter=fulltext.search:MagicGrid"` is not a training source; use web search for `MagicGrid training course` and `MagicGrid seminar` and verify each hit. If fewer than 4 verify, STOP and report; do not fill with vendor marketing pages already used elsewhere.

- [ ] **Step 7: Seed Videos and Talks (minimum 10)**

Seven candidate URLs from the research scan, verified per Step 2 (`youtu.be` short links redirect; confirm the final YouTube page is the intended talk):

```markdown
- [BoK Edition 2 overview](https://youtu.be/FzrzzSS4GvM) - Video walkthrough of the MagicGrid Book of Knowledge second edition.
- [Conceptual subsystems](https://youtu.be/UzNZhFSGtjw) - Talk on conceptual subsystem decomposition in MagicGrid.
- [Hypermodeling with MagicGrid](https://youtu.be/0ctdRBGiBk0) - Demo of hypermodeling applied with the MagicGrid method.
- [MagicGrid methodology walkthrough](https://youtu.be/todMOBqirAA) - Walkthrough of the MagicGrid SysML methodology.
- [Method of ellipses? No: MoEs and traceability](https://youtu.be/CsF2nKbO0KY) - Talk on methods of execution and traceability in MagicGrid.
```

Correction before writing: the fifth line's link text must be factual. Use `- [MoEs and traceability](https://youtu.be/CsF2nKbO0KY) - Talk on methods of execution (MoEs) and traceability in MagicGrid.`

```markdown
- [Radar sample model](https://youtu.be/JtWZQM-yamk) - Demo building a radar sample model with MagicGrid.
- [SysML Made Simple with MagicGrid seminar](https://youtu.be/xFGFA8H7Yd0) - Full seminar on SysML with MagicGrid by No Magic methodology staff (Morkevicius et al.).
```

For each video, confirm the channel at seed time by visiting the watch page; when the channel is the official No Magic, CATIA Magic, or Dassault Systemes channel, the description names that affiliation. Three more entries to reach 10: browse the vendor channel's uploads for MagicGrid-titled videos and INCOSE proceedings channels for MagicGrid talks; verify each URL per Step 2 and write factual one-sentence descriptions with channel affiliation where confirmed. If fewer than 10 verify, STOP and report.

- [ ] **Step 8: Seed Example Models (minimum 2)**

```markdown
- [sysml-magicgrid-vccs](https://github.com/matthieugourssies/sysml-magicgrid-vccs) - Public MagicGrid sample model for a vehicle cruise control system built with SysML.
```

Second entry: find one more public MagicGrid sample model. Search GitHub repositories for `MagicGrid` and inspect candidates with the Step 2 GitHub check (must be an MBSE model repo, not a CSS/JS grid library; Cameo project samples and student repos are the expected surface per the research file). Verify the repo URL per Step 2. If no second model verifies, STOP and report.

- [ ] **Step 9: Seed Tool Support (minimum 3)**

```markdown
- [CATIA Magic](https://www.3ds.com/products/catia/catia-magic) - Dassault Systemes product family (CATIA Magic Grid, Grid DX, and Cloud) implementing the MagicGrid methodology.
- [Cameo Systems Modeler](https://www.3ds.com/products/catia/no-magic/cameo-systems-modeler) - Dassault Systemes modeling environment for SysML with MagicGrid support.
- [No Magic](https://www.3ds.com/products/catia/no-magic) - Dassault Systemes hub page for the No Magic product line including Cameo and MagicDraw.
```

Product naming: confirm the exact family member names on the 3ds.com page at seed time and keep the description factual; if the family breakdown in the description does not match the page, simplify to "Dassault Systemes product page for the CATIA Magic modeling family." None of these three URLs may appear in another section.

- [ ] **Step 10: Seed Community (minimum 3)**

Candidates, each verified per Step 2: the INCOSE MBSE Working Group page (browse from `https://www.incose.org/`), the INCOSE International Symposium program page mentioning MagicGrid tracks, and the vendor community surface (CATIA Magic community or forum page reachable from the 3ds.com product pages). LinkedIn practitioner circles are acceptable only if the URL returns 200 or is canonical vendor material; LinkedIn commonly blocks bots with non-403 codes, so prefer INCOSE and vendor community pages that verify. One factual sentence per entry; name vendor affiliation where the community space is run by No Magic or Dassault. If fewer than 3 verify, STOP and report.

- [ ] **Step 11: Seed Related Methodologies (exactly 5)**

One entry per peer methodology plus the sister list, one factual sentence each, linked to a canonical description page or paper verified per Step 2. Candidates (verify, never assume):

```markdown
- [Awesome SysML v2](https://github.com/jgsystemsconsulting/awesome-sysml-v2) - Sister list covering the SysML v2 language and its tooling.
- [Capella (Arcadia)](https://www.eclipse.org/capella/) - Open source implementation of the Arcadia method, a peer MBSE methodology.
- [Harmony-SE](https://www.ibm.com/products/rational-rhapsody) - IBM Rational Rhapsody family page, home of the Harmony-SE (Harmony for Systems Engineering) method; replace with the canonical Harmony-SE description page if a better one verifies.
- [OOSEM](https://www.incose.org/) - INCOSE portal; locate and use the OOSEM working group or description page as the entry URL instead of the bare portal if it verifies.
- [SYSMOD](https://github.com/MBSE4U/sysmod) - SYSMOD methodology materials from MBSE4U; replace with the canonical SYSMOD description page if a better one verifies.
```

For OOSEM, Harmony-SE, and SYSMOD, browse from the named candidate or search for the methodology's canonical page, verify it, and link the most specific stable page found (working group page, method whitepaper, or maintained project page). Bare portals are last resorts. These are pointers, not coverage; no section growth.

- [ ] **Step 12: Sort, count, and verify the seeded README**

Sort each section alphabetically by link text (case-insensitive), then run:

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
declare -A mins=( ["Official Resources"]=4 ["Books and Formal Publications"]=2 ["Papers and Case Studies"]=12 ["Training and Courses"]=4 ["Videos and Talks"]=10 ["Example Models"]=2 ["Tool Support"]=3 ["Community"]=3 ["Related Methodologies"]=5 )
total=0
for s in "Official Resources" "Books and Formal Publications" "Papers and Case Studies" "Training and Courses" "Videos and Talks" "Example Models" "Tool Support" "Community" "Related Methodologies"; do
  n=$(awk -v sec="## $s" '$0==sec{f=1;next} /^## /{f=0} f&&/^- \[/{c++} END{print c+0}' README.md)
  printf '%s: %s (min %s)\n' "$s" "$n" "${mins[$s]}"
  test "$n" -ge "${mins[$s]}" || { echo "FAIL: $s below minimum"; exit 1; }
  total=$((total+n))
done
echo "total: $total"
test "$total" -ge 45 || { echo "FAIL: total below 45"; exit 1; }
```
Expected: every section at or above its minimum; total at least 45.

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
for s in "Official Resources" "Books and Formal Publications" "Papers and Case Studies" "Training and Courses" "Videos and Talks" "Example Models" "Tool Support" "Community" "Related Methodologies"; do
  awk -v sec="## $s" '$0==sec{f=1;next} /^## /{f=0} f' README.md | grep -oE 'https?://[^) ]+' | sed "s|^|$s\t|"
done | cut -f2 | sort | uniq -d
grep -c "not affiliated with, endorsed by, or sponsored by Dassault Systemes or No Magic" README.md
grep -c "awesome-sysml-v2" README.md
grep -inE 'npmjs|magic[- ]?grid.*(css|layout)' README.md || echo "no CSS/JS grid library hits"
```
Expected: the duplicate-URL check prints nothing (each URL in at most one content section; the intro cross-link sits outside the nine sections); disclaimer present once; `awesome-sysml-v2` appears exactly twice (intro plus Related Methodologies entry); no grid library hits.

- [ ] **Step 13: Commit**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git add README.md
git commit -m "Seed README with verified MagicGrid entries across nine sections"
```

Keep `~/magicgrid-403-accepted.txt` (created in Step 2); Task 7 consumes it.

## Task 6: docs/index.html full rewrite

**Files:**
- Create: `docs/index.html`

**Interfaces:**
- Consumes: README section anchors from Task 5 (nine H2s, GitHub slugification as listed below) and the canonical URL from the spec. Task 8 publishes this from Pages.

**Model:** flash (complete file body below)

- [ ] **Step 1: Write `docs/index.html`**

Full rewrite. No SysML v2 prose anywhere; identity strings, masthead license, category table, and footer all point at the new repo; no og:image or twitter:image tags; no social-card files.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Awesome MagicGrid MBSE - JGS</title>
<meta name="description" content="A curated list of MagicGrid MBSE methodology resources: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support.">
<link rel="canonical" href="https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="site.css">
<meta property="og:type" content="website">
<meta property="og:url" content="https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/">
<meta property="og:title" content="Awesome MagicGrid MBSE - JGS">
<meta property="og:description" content="A curated list of MagicGrid MBSE methodology resources: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support.">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Awesome MagicGrid MBSE - JGS">
<meta name="twitter:description" content="A curated list of MagicGrid MBSE methodology resources: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support.">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Awesome MagicGrid MBSE",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web",
  "url": "https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse",
  "description": "A curated list of MagicGrid MBSE methodology resources: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support.",
  "license": "https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/LICENSE"
}
</script>
</head>
<body>
<div class="masthead">
  <div class="wrap">
    <span>CLASSIFICATION: PUBLIC</span>
    <span>LICENCE: CC0</span>
    <span>DOC-ID: JGS-AWESOME-MAGICGRID-MBSE</span>
    <span>REV: 1.0</span>
  </div>
</div>
<nav class="site">
  <div class="wrap">
    <a href="#what">What it is</a>
    <a href="#categories">Categories</a>
    <a href="#contribute">Contribute</a>
    <a href="#maintenance">Maintenance</a>
    <a href="#links">Links</a>
  </div>
</nav>
<section class="hero" id="top">
  <div class="wrap">
    <a class="badge" href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
    <h1>Awesome MagicGrid MBSE</h1>
    <p>A curated list of MagicGrid methodology resources: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support.</p>
  </div>
</section>
<section id="what">
  <div class="wrap">
    <div class="shead"><h2>What it is</h2></div>
    <p class="lead">Awesome MagicGrid MBSE is an awesome-style curated list for the MagicGrid methodology, the grid-based MBSE method from No Magic, now part of Dassault Systemes. It collects official material, the Book of Knowledge, papers and case studies, talks, training, example models, tool support, and brief pointers to peer methodologies. For the SysML v2 language and its tooling, see the sister list <a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2">awesome-sysml-v2</a>. Entries are maintained in the <a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md">README</a>; this site is a front door, not a mirror.</p>
  </div>
</section>
<section id="categories">
  <div class="wrap">
    <div class="shead"><h2>Category map</h2></div>
    <table class="data">
      <thead>
        <tr><th scope="col">Category</th><th scope="col">About</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#official-resources">Official Resources</a></td><td>Vendor documentation hub, training catalog, and official MagicGrid course pages.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#books-and-formal-publications">Books and Formal Publications</a></td><td>The MagicGrid Book of Knowledge and other formal publications about the method.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#papers-and-case-studies">Papers and Case Studies</a></td><td>INCOSE, Wiley, Springer, and ACM papers with DOIs, from the origin paper to current case studies.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#training-and-courses">Training and Courses</a></td><td>Partner courses and seminars beyond the official catalog.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#videos-and-talks">Videos and Talks</a></td><td>Vendor walkthroughs, seminars, and conference talks on applying MagicGrid.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#example-models">Example Models</a></td><td>Public MagicGrid sample models to learn from and build on.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#tool-support">Tool Support</a></td><td>CATIA Magic and Cameo Systems Modeler, the tools that implement the method.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#community">Community</a></td><td>INCOSE venues and practitioner circles around the method.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md#related-methodologies">Related Methodologies</a></td><td>One-line pointers to peer methodologies and the sister list.</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section id="contribute">
  <div class="wrap">
    <div class="shead"><h2>How to contribute</h2></div>
    <p class="lead">Pull requests are welcome. Entry additions go through the <a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md">README</a> via a pull request; the process, entry format, and acceptance criteria live in <a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/contributing.md">contributing.md</a>.</p>
  </div>
</section>
<section id="maintenance">
  <div class="wrap">
    <div class="shead"><h2>Maintenance cadence</h2></div>
    <p class="lead">Review cycles, link checking, and entry curation run on the cadence documented in <a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/contributing.md#maintenance">contributing.md</a>.</p>
  </div>
</section>
<section id="links">
  <div class="wrap">
    <div class="shead"><h2>Repository links</h2></div>
    <ul>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md">README</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/contributing.md">contributing.md</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse">Repository root</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/issues">Issues</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/tree/main/docs">Site source (docs/)</a></li>
    </ul>
  </div>
</section>
<footer>
  <div class="wrap">
    <p class="foot-note"><a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/LICENSE">CC0 Licence</a>. The <a href="https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse/blob/main/README.md">README</a> is the source of truth for all entries.</p>
  </div>
</footer>
</body>
</html>
```

- [ ] **Step 2: Verify the rewrite**

Run:
```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
grep -c "SysML v2" docs/index.html
grep -c "awesome-sysml-v2" docs/index.html
grep -c "MIT" docs/index.html || echo "no MIT strings"
grep -c "og:image\|twitter:image" docs/index.html || echo "no image meta tags"
grep -c "DOC-ID: JGS-AWESOME-MAGICGRID-MBSE" docs/index.html
grep -c "CC0" docs/index.html
grep -oE 'README.md#[a-z-]+' docs/index.html | sort
ls docs
```
Expected: `SysML v2` appears once (the sister-list sentence in What it is) and never as prose about the SysML language; `awesome-sysml-v2` appears once (the same link); no MIT strings; no og:image or twitter:image tags; DOC-ID present; CC0 present twice (masthead and footer); nine README anchors matching the nine sections (`#official-resources`, `#books-and-formal-publications`, `#papers-and-case-studies`, `#training-and-courses`, `#videos-and-talks`, `#example-models`, `#tool-support`, `#community`, `#related-methodologies`); docs contains only `.nojekyll`, `index.html`, `site.css` (no social-card files).

- [ ] **Step 3: Commit**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git add docs/index.html
git commit -m "Add MagicGrid docs site"
```

## Task 7: Local publication gate (lint, markdownlint, lychee, 403 allowlist)

**Files:**
- Modify: `CHANGELOG.md` (append clean-run bullet and Accepted-403 subsection)

**Interfaces:**
- Consumes: the full skeleton and seeded README from Tasks 1-6, and `~/magicgrid-403-accepted.txt` from Task 5.
- Produces: a clean local gate. Task 8 runs only after every check here exits 0. The CHANGELOG accepted-403 list and clean-run note required by the spec's acceptance criteria land here.

**Model:** deep (gate debugging, 403 diff, judgment on link failures)

- [ ] **Step 1: Confirm the working tree is committed and on main**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
git status --porcelain
git branch --show-current
```
Expected: porcelain output empty; branch is main.

- [ ] **Step 2: Run the lint gates**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
export GITHUB_TOKEN=$(gh auth token)
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```
Expected: both exit 0. awesome-lint may emit repo-info warnings about the missing GitHub remote; per the spec, that is expected before publication and resolves after Task 8's push when CI lint runs green. Any error (as opposed to repo-info warning) must be fixed and the command rerun.

- [ ] **Step 3: Run the zero-broken lychee gate**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
export GITHUB_TOKEN=$(gh auth token)
lychee --accept '200,204,301,308,403' --no-progress --max-retries 3 README.md
echo "exit: $?"
```
Expected: exit 0, zero broken links under the accept set. Save the run summary for the CHANGELOG note: `lychee --accept '200,204,301,308,403' --no-progress --max-retries 3 README.md 2>&1 | tail -20 > ~/magicgrid-lychee-summary.txt`.

- [ ] **Step 4: Extract every 403 with a second pass and diff against the allowlist**

The accept-set run above reports accepted 403s as OK and exits zero, so it cannot be used for the diff. Run a probe without 403 in the accept set:

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
export GITHUB_TOKEN=$(gh auth token)
lychee --accept '200,204,301,308' --no-progress --max-retries 3 --format json README.md > lychee-403-probe.json || true
jq -r '.fail_map[][]?.url // empty' lychee-403-probe.json | grep -iE '^https?://' | sort -u > seen-failed.txt
jq -r '.fail_map[][]?.error // empty' lychee-403-probe.json | grep -c "403" || true
```

If the `fail_map` path yields nothing while the Step 3 run showed warnings, inspect `lychee-403-probe.json` directly (`jq 'keys' lychee-403-probe.json`, then drill into the failures key) and adapt the jq path; alternatively rerun without `--format json` and grep the plain output for `403`. The goal is the set of URLs that fail with 403 and nothing else. Then:

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
# URLs that failed the probe for reasons other than 403 must be empty after 403 filtering;
# inspect the error strings to confirm every probe failure is a 403:
jq -r '.fail_map[][]? | .url + " :: " + (.error // "")' lychee-403-probe.json
# Build the accepted allowlist from the Task 5 records:
sed 's#^https\?://#https://#' ~/magicgrid-403-accepted.txt | sort -u > allowlist-403.txt
# Off-list 403s (seen but not allowlisted) fail the gate:
comm -13 allowlist-403.txt seen-failed.txt
echo "off-list count: $(comm -13 allowlist-403.txt seen-failed.txt | wc -l)"
```

Gate rule: the probe's failure set must contain only 403 errors (no 404s, no timeouts; the accept-set run in Step 3 already proved everything else passes), and `comm -13` must print nothing. A URL that 403s during the probe but is absent from `allowlist-403.txt` either gets added to Task 5's records with the canonical-vendor justification (then rerun from Step 3) or the entry is removed from the README (then rerun Task 5 Step 12 and this task). A URL in the allowlist that no longer 403s is harmless here; note it for a later cleanup, it is not a gate failure.

- [ ] **Step 5: Record the accepted-403 list and clean run in CHANGELOG.md**

Append under the existing 1.0.0 entry. If the allowlist is empty, write the none line as shown; otherwise one backticked URL per line, exactly matching `allowlist-403.txt`:

```markdown
- Clean lychee run recorded at seed time: zero broken links under the accept set `200,204,301,308,403`.

### Accepted 403 links (canonical, bot-blocked)

- (none; every seeded link returned 200, a verified redirect, or a non-403 status)
```

Or, with accepted URLs:

```markdown
- Clean lychee run recorded at seed time: zero broken links under the accept set `200,204,301,308,403`.

### Accepted 403 links (canonical, bot-blocked)

- `https://doi.org/10.1002/inst.12429`
```

(the URL list is illustrative of format; write the actual `allowlist-403.txt` contents). Then delete the probe artifacts:

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
rm -f lychee-403-probe.json seen-failed.txt allowlist-403.txt
npx markdownlint-cli2 "README.md" "contributing.md" && echo md-ok
git add CHANGELOG.md
git commit -m "Record clean lychee run and accepted 403 allowlist"
```
Expected: markdownlint still exits 0; one commit.

- [ ] **Step 6: Re-run the full gate end to end**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
export GITHUB_TOKEN=$(gh auth token)
npx awesome-lint@2.3.0 README.md && npx markdownlint-cli2 "README.md" "contributing.md" && lychee --accept '200,204,301,308,403' --no-progress --max-retries 3 README.md && echo "LOCAL GATE CLEAN"
```
Expected: `LOCAL GATE CLEAN`. Any failure: fix, commit the fix, rerun this step. Do not proceed to Task 8 until this prints the marker.

## Task 8: Publication (repo create, CI, Pages, homepage, topics)

**Files:** none modified in the new repo. External state changes only.

**Interfaces:**
- Consumes: the clean Task 7 gate on branch main with all commits.
- Produces: the public repo, green CI, the live Pages site, the homepage field, and the four topics. Task 10's sweep verifies all of it.

**Model:** standard (external failure modes; commands fully specified, judgment needed on retries)

- [ ] **Step 1: Create the public repo and push**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
gh repo create jgsystemsconsulting/awesome-magicgrid-mbse --public --source . --remote origin --push
git remote -v
git log --oneline origin/main | head -5
```
Expected: repo created, origin set, all commits pushed to main.

- [ ] **Step 2: Confirm the lint workflow is green on the first push**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
sleep 20
gh run list --repo jgsystemsconsulting/awesome-magicgrid-mbse --workflow lint.yml --limit 1
```
Poll until the run completes:
```bash
run_id=$(gh run list --repo jgsystemsconsulting/awesome-magicgrid-mbse --workflow lint.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$run_id" --repo jgsystemsconsulting/awesome-magicgrid-mbse --exit-status
```
Expected: completed with conclusion success. This closes out any awesome-lint repo-info warning from Task 7. If it fails, read the log with `gh run view "$run_id" --log-failed`, fix, commit, push, and re-watch.

- [ ] **Step 3: Enable Pages from main /docs**

```bash
gh api --method POST repos/jgsystemsconsulting/awesome-magicgrid-mbse/pages --input - <<'EOF'
{"source":{"branch":"main","path":"/docs"}}
EOF
gh api repos/jgsystemsconsulting/awesome-magicgrid-mbse/pages --jq '.status + " " + .html_url'
```
Expected: the POST returns 201 (409 with a "already exists" message means Pages is already on; verify its source matches main//docs and continue). Status may read `building` first.

- [ ] **Step 4: Confirm the site serves at the canonical URL**

```bash
for i in 1 2 3 4 5 6 7 8 9 10; do
  code=$(curl -s -o /dev/null -w '%{http_code}' https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/)
  echo "attempt $i: $code"
  [ "$code" = "200" ] && break
  sleep 30
done
```
Expected: 200 within ten attempts. If still building after ten, report and retry later; do not fail the task on propagation delay.

- [ ] **Step 5: Set the homepage and topics**

```bash
gh repo edit jgsystemsconsulting/awesome-magicgrid-mbse --homepage "https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/"
gh repo edit jgsystemsconsulting/awesome-magicgrid-mbse --add-topic mbse --add-topic sysml --add-topic magicgrid --add-topic awesome-list
gh repo view jgsystemsconsulting/awesome-magicgrid-mbse --json homepage,repositoryTopics --jq '.homepage, [.repositoryTopics[].name]'
```
Expected: homepage set to the canonical URL; topics list `mbse`, `sysml`, `magicgrid`, `awesome-list`. The `mbse` and `sysml` topics fix search intent against the CSS/JS magic-grid libraries per the spec.

## Task 9: Cross-link edit in awesome-sysml-v2

**Files:**
- Modify: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\README.md` (one inserted line under the intro paragraph)

**Interfaces:**
- Consumes: the published repo URL from Task 8.
- Produces: the reverse cross-link required by the spec. This is the only edit to the template repo.

**Model:** flash (one-line insert with exact strings)

- [ ] **Step 1: Pre-check the template working tree**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2
git branch --show-current
git status --porcelain README.md
sed -n '3p' README.md
```
Expected: branch main; README.md clean; line 3 is `A curated list of OMG SysML v2 tools, models and case studies, and learning resources.` If README.md is dirty or line 3 differs, STOP and report.

- [ ] **Step 2: Insert the cross-link line directly under the intro paragraph**

old_string:
```
A curated list of OMG SysML v2 tools, models and case studies, and learning resources.
```
new_string:
```
A curated list of OMG SysML v2 tools, models and case studies, and learning resources.
For the MagicGrid MBSE methodology, see the sister list [awesome-magicgrid-mbse](https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse).
```

No new section, no TOC change (the template TOC is unaffected).

- [ ] **Step 3: Verify and lint**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2
grep -n "awesome-magicgrid-mbse" README.md
git diff --numstat README.md
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md"
```
Expected: one hit at line 4; numstat `1	0` (one insertion, zero deletions); both lint commands exit 0.

- [ ] **Step 4: Commit and push through the normal gates**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2
git add README.md
git commit -m "Add sister list cross-link to awesome-magicgrid-mbse"
git push origin main
```
Then confirm CI lint green on the push:
```bash
sleep 20
run_id=$(gh run list --repo jgsystemsconsulting/awesome-sysml-v2 --workflow lint.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$run_id" --repo jgsystemsconsulting/awesome-sysml-v2 --exit-status
```
Expected: success. Do not touch any other template file.

## Task 10: Acceptance sweep

**Files:** none modified unless a check fails and needs a fix.

**Interfaces:**
- Consumes: Tasks 1-9 complete.
- Produces: the evidence that every spec acceptance criterion holds.

**Model:** standard (cross-repo sweep with remote checks)

- [ ] **Step 1: Run the local sweep in the new repo**

```bash
cd /c/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse
export GITHUB_TOKEN=$(gh auth token)
npx awesome-lint@2.3.0 README.md && echo AC-lint-ok
npx markdownlint-cli2 "README.md" "contributing.md" && echo AC-md-ok
lychee --accept '200,204,301,308,403' --no-progress --max-retries 3 README.md && echo AC-lychee-ok
grep -c "not affiliated with, endorsed by, or sponsored by Dassault Systemes or No Magic" README.md
grep -c "does not host copies of the MagicGrid Book of Knowledge" README.md
grep -n "### Accepted 403 links" CHANGELOG.md
grep -n "Clean lychee run recorded" CHANGELOG.md
grep -c "awesome-sysml-v2" README.md
test "$(grep -icE 'npmjs' README.md || true)" = "0" && echo AC-no-css-libs
grep -cn "magic grid.*layout librar\|CSS or JavaScript" contributing.md
```
Expected: three lint/link markers; disclaimer present (two greps each 1); CHANGELOG has the accepted-403 heading and the clean-run line; sister-list count 2; no npm hits; contributing.md carries the explicit exclusion. No Magic/Dassault affiliation naming inside descriptions was enforced at seed time (Task 5 Steps 5-10) and is re-checked by reading the nine sections; there is no reliable grep for it.

- [ ] **Step 2: Run the remote sweep**

```bash
gh run list --repo jgsystemsconsulting/awesome-magicgrid-mbse --workflow lint.yml --limit 1 --json conclusion --jq '.[0].conclusion'
curl -s -o /dev/null -w '%{http_code}\n' https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/
gh repo view jgsystemsconsulting/awesome-magicgrid-mbse --json homepage,repositoryTopics,isPrivate --jq '.isPrivate, .homepage, [.repositoryTopics[].name]'
grep -c "awesome-magicgrid-mbse" /c/Users/gower/OneDrive/Documents/GitHub/awesome-sysml-v2/README.md
```
Expected: `success`; `200`; repo public with the canonical homepage and the four topics; template README contains the cross-link (once). Cross-link in the other direction was verified in Task 5 Step 12 (count 2 in the new README).

- [ ] **Step 3: Report**

If every check matches, the plan is complete. Any mismatch: fix in the owning task's file, rerun that task's verification, then rerun this sweep.

## Acceptance mapping

| Spec acceptance criterion | Where verified |
|---|---|
| awesome-lint@2.3.0 passes; repo-info green after remote + CI | Task 7 Step 2, Task 8 Step 2, Task 10 Step 1 |
| markdownlint-cli2 passes on README.md and contributing.md | Task 7 Step 2, Task 10 Step 1 |
| Lychee zero broken under documented accept set; 403s in CHANGELOG | Task 7 Steps 3-5, Task 10 Step 1 |
| 40+ entries, section minimums sum 45, seed-time verification | Task 5 Steps 2-12 |
| Disclaimer: no affiliation, trademark note, no copyrighted hosting | Task 5 Step 1 (verbatim), Task 10 Step 1 |
| Vendor affiliation named in descriptions | Task 5 Steps 5-10, Task 4 criterion 3 |
| Cross-links both directions | Task 5 Steps 1 and 11, Task 9, Task 10 |
| CI lint green on first push to main | Task 8 Step 2 |
| Pages live, homepage set, topics set | Task 8 Steps 3-5, Task 10 Step 2 |
| No CSS/JS magic-grid library; explicit exclusion in contributing.md | Task 5 Step 12, Task 4 Step 2, Task 10 Step 1 |

Non-goals respected by construction: no generic SysML or MBSE sections (scope rule in contributing.md criterion 2), no CSS/JS grid libraries (exclusion + sweep greps), no BoK PDF hosting (Books rule in Task 5 Step 4), no awesome.re submission, no social cards (Task 6 omits image tags and files), peer methodologies as pointers only (Task 5 Step 11 caps the section at five).
