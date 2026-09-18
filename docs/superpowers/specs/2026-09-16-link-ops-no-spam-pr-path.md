# Spec: link-ops-no-spam-pr-path (P7)

Date: 2026-09-16. Baseline: HEAD bf25772 (P8 landed). Work package P7 of the awesome-sysml-v2 packages plan. Absorbs RRL findings I2 and I8.

## Summary

Three changes across three files. The weekly Link Checker Report becomes a create-or-update issue following the stale.yml pattern, and the workflow creates its own labels so the report step has no undefined-label dependency. links.yml additionally triggers on `pull_request`, giving every PR a soft, visible link check that cannot create issues and cannot fail on forks. contributing.md documents a local lychee run, and the PR template gains one link-check checkbox. No hard merge gate is introduced. The weekly cron schedule is unchanged.

## Problem statement

- I2 (duplicate reports): the issue step (`.github/workflows/links.yml:30-36`) calls `peter-evans/create-issue-from-file` with the fixed title "Link Checker Report" and no dedupe. Every week with at least one unreachable link opens another issue. `create-issue-from-file` cannot dedupe by title (research: only an explicit `issue-number` input reuses an issue).
- I8 (no contributor-visible reachability check): inclusion criterion 1 in contributing.md requires a stable, reachable URL, but the only verification is a weekly cron after merge. A contributor learns about a dead link days after their PR merged.
- Label dependency: the issue step requests `labels: report, broken-links` (links.yml:36), but neither label is defined in the repo (GitHub labels live in settings). The first report create can fail on a missing label or lose the label.
- Ungated issue step: links.yml:31 gates only on `steps.lychee.outputs.exit_code != 0`. There is no `github.event_name` gate, so adding a `pull_request` trigger naively would attempt issue writes from PR runs and fail on forks, whose GITHUB_TOKEN is read-only.

## Goals

1. Exactly one open "Link Checker Report" issue at any time; weekly runs edit it in place.
2. Labels `report` and `broken-links` exist before the report step runs; the report issue carries both.
3. A PR-time link check that is visible (warning annotation plus step summary) but non-blocking, and safe on same-repo and fork PRs.
4. A documented local link check in contributing.md that does not imply an npm install (lychee is not an npm package).
5. A PR template checkbox aligned with the chosen check path.
6. Remove a third-party action from the supply-chain surface (`create-issue-from-file` is dropped).

## Non-goals

- Hard-fail merge gate (backlog item b-12; criterion 1 stays soft, decision a-04).
- Extra scanners or additional scan schedules; the weekly cron `0 18 * * 1` is untouched.
- Freshness reporting (P6, done), lint gate (P8, done), action SHA pins (P9, done).
- README entry content.
- Label taxonomy beyond the two labels this workflow already references.
- Concurrency groups (no modeled failure; see limitations).

## Codebase context

Facts at HEAD bf25772, all verified by the context round (verdict CONTEXT_COMPLETE):

- `.github/workflows/links.yml`: name line 1; P9 SHA-pin comment block 2-7; triggers `schedule: cron "0 18 * * 1"` plus `workflow_dispatch` (9-12); workflow permissions `contents: read`, `issues: write` (14-16); lychee step at 23-29 with `args: --no-progress`, `fail: false`, `token: GITHUB_TOKEN`; issue step 30-36 gated on `steps.lychee.outputs.exit_code != 0`, fixed title, `labels: report, broken-links`.
- `.github/workflows/stale.yml:50-59` holds the dedupe pattern to mirror: `gh issue list --state open --search "Freshness report in:title"` then `gh issue edit` or `gh issue create`.
- `contributing.md`: Local commands section at 23-30 with an npx fence (awesome-lint pinned at line 28, markdownlint at 29). A plain npx line for lychee would be wrong; lychee installs via platform package managers only.
- `.github/PULL_REQUEST_TEMPLATE.md`: 6 checkbox lines; the lint checkboxes sit at lines 4-5.
- No `.lycheeignore` or `lychee.toml` at repo root; nothing to migrate.
- P9 rule: any NEW `uses:` line would need full SHA plus version comment. This spec adds none; all new steps are `run:` steps.

Boundary: stale.yml and lint.yml are outside P7 and stay untouched.

## Design

### D1: weekly report upsert with explicit label creation

Replace the `Create Issue From File` step (links.yml:30-36) with a `gh` create-or-update block mirroring stale.yml:50-59, quoted for the actual title, plus a label-ensure step in front of it.

Before (links.yml:30-36):

```yaml
      - name: Create Issue From File
        if: steps.lychee.outputs.exit_code != 0
        uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5
        with:
          title: Link Checker Report
          content-filepath: ./lychee/out.md
          labels: report, broken-links
```

After:

```yaml
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

Decisions, fixed:

- Upsert mechanism: the stale.yml `gh` pattern. `create-issue-from-file` is removed; it cannot dedupe, and dropping it deletes one pinned third-party action.
- Search discipline: quoted phrase `"Link Checker Report" in:title`, not the bare unquoted form stale.yml uses. Bare multi-word searches match issue titles containing all words anywhere; the quoted phrase matches the exact phrase, which is as tight as `gh issue list --search` gets without post-filtering. Residual risk documented under limitations.
- Label fix: create labels explicitly, do not drop them. Rationale: acceptance requires the labels to exist, `report`/`broken-links` keep the single report issue filterable in the tracker, and the cost is two idempotent one-line commands. `|| true` tolerates the "already exists" error on every run after the first, so the step is idempotent under cron, dispatch, and concurrent runs. Label creation is gated to non-PR events because PR runs never touch the issue tracker.

### D2: PR-time check shape: one job, event-gated write steps

Add `pull_request:` to the triggers (links.yml:9-12) and keep a single job. The two write-capable steps get `github.event_name != 'pull_request'` gates. A new advisory step surfaces `exit_code` on PRs without failing the job.

Before (links.yml:9-12):

```yaml
on:
  schedule:
    - cron: "0 18 * * 1"
  workflow_dispatch:
```

After:

```yaml
on:
  schedule:
    - cron: "0 18 * * 1"
  workflow_dispatch:
  pull_request:
```

New step, placed immediately after the Link Checker step:

```yaml
      - name: Advisory broken-link warning
        if: github.event_name == 'pull_request' && steps.lychee.outputs.exit_code != 0
        run: |
          {
            echo "Lychee exit code: ${{ steps.lychee.outputs.exit_code }}."
            echo "Broken or unreachable links were found. This check is advisory and does not block merge; see the Link Checker step log for the URL list."
          } >> "$GITHUB_STEP_SUMMARY"
          echo "::warning::Lychee found unreachable links (exit code ${{ steps.lychee.outputs.exit_code }}); advisory only, see the Link Checker step log"
```

Decisions, fixed:

- One job, not two. Rejected alternative: a second PR-only job without `issues: write`. That shape is cleaner least-privilege but duplicates the lychee step, forces a job-level permissions refactor, and reduces risk by zero modeled failures: the event gate already makes PR runs issue-free, and GitHub forces a read-only GITHUB_TOKEN on fork PRs regardless of the declared workflow permissions. The single job is the shortest diff that cannot spam issues or fail forks.
- Softness kept: `fail: false` stays, so lychee findings never fail the job on any event. The PR signal is the `::warning::` annotation plus the step summary, both visible in the PR Checks tab. No branch protection or required check is added.
- Flake resilience made explicit: `--max-retries 3` is appended to the lychee args — the same value as lychee's documented default, stated explicitly so the retry floor survives any future default change (research: rate-limit and flake cluster). No other arg changes.
- Fork analysis: on fork PRs, checkout and lychee run with a read-only token (lychee uses it only for GitHub API rate-limit headroom); the label and issue steps are gated off; the advisory step only writes step-summary and annotation output. Fork PRs see a green check with a warning when links break, and no tracker writes.

### D3: local link check in contributing.md

Append a subsection after the existing Local commands fence (contributing.md:27-30). It is a separate fenced block with an explicit "not an npm package" sentence, so it cannot read as another npx line.

After line 30, insert:

````markdown

### Link check

`lychee` is a native binary, not an npm package. Install it once with your platform package manager (`scoop`, `winget`, or `choco` on Windows, `brew` on macOS, `pacman`, `zypper`, `snap`, or `apk` on Linux), then run from the repository root:

```bash
lychee README.md
```

Export `GITHUB_TOKEN` (for example `GITHUB_TOKEN=$(gh auth token)`) to avoid GitHub rate limiting on `github.com` links. Third-party sites sometimes return transient timeouts or 429s; retry before treating a failure as a broken link.
````

### D4: PR template checkbox

Insert one line after line 5 of `.github/PULL_REQUEST_TEMPLATE.md` (after the markdownlint checkbox, before the commercial line), matching the existing backticked-command style:

```markdown
- [ ] No new broken links: `lychee README.md` passes locally, or the Link check on this PR shows no new failures (advisory)
```

The wording offers both paths (local run or the PR check) and marks the check advisory, matching the non-blocking design.

### Exact after content for links.yml

Full file after the change, for plan verification:

```yaml
name: Links
# Action refs are pinned to full-length commit SHAs (supply-chain hardening,
# per GitHub's security-hardening guide). To bump an action, resolve its tag
# to a commit SHA, e.g.:
#   curl -s https://api.github.com/repos/<owner>/<repo>/commits/<tag>
# Use the "sha" field (the commit, not a tag object SHA; see annotated-tag
# note in the repo spec for P9), then update the version comment to match.

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
          args: --no-progress --max-retries 3
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

## Documented limitations

- Flaky external links: lychee treats 429 and transient timeouts as failures; a weekly report can list links that work. `--max-retries 3` reduces this; the report stays advisory, so a false positive never blocks anything.
- `in:title` search caveats: the quoted-phrase search matches any open issue whose title contains the phrase "Link Checker Report", including a human-opened issue with that phrase in its title; the upsert would edit it. Accepted residual risk for a single low-traffic tracker. Upgrade path if it ever bites: post-filter with `--json number,title` and `select(.title == "Link Checker Report")`.
- Closed reports reset: the search filters `--state open`. If a maintainer closes the report, the next failing week opens a fresh issue. Intentional: closed means acknowledged.
- Fork PRs: GitHub grants fork PR runs a read-only GITHUB_TOKEN regardless of declared workflow permissions, so the tracker writes are doubly unreachable; first-time contributors' PRs may additionally need maintainer approval before Actions run. The check result then appears once approved.
- PR runs declare `issues: write` at workflow level but no PR-path step uses it. GitHub downgrades the token to read-only on fork PRs; tightening to job-level permissions is the upgrade path, skipped here to keep one job.
- No concurrency group: a PR run and the weekly cron can overlap. Harmless, because PR runs never touch the issue and the weekly job is the only writer.
- Local version drift: contributing.md points at package managers rather than a pinned lychee version; output wording may differ slightly across versions. Acceptable for an advisory check.

## Risks

- Label ensure failure is silent (`|| true`): if label creation fails (for example a transient API error), the later `gh issue create --label` fails visibly and no issue is created; the next weekly run retries. No partial state.
- A maintainer-renamed or already-existing `report` or `broken-links` label keeps its existing color; `gh label create` does not overwrite. Harmless.
- One warning annotation per failing PR run: bounded noise, only when links actually break.
- Removing `create-issue-from-file` changes the report body source from the action's rendering to the same `lychee/out.md` file verbatim; body format is unchanged in practice since the action only uploaded that file.

## Acceptance criteria

1. Dedupe: two consecutive `workflow_dispatch` runs with at least one unreachable link leave exactly one open issue titled "Link Checker Report"; the second run edits the first issue's body and creates no second issue.
2. Labels: after any non-PR run, `report` and `broken-links` exist in repo settings, and the report issue carries both labels.
3. PR soft check: a PR that introduces a broken link shows the `::warning::` annotation and step-summary text; the check run is green; no issue is created or edited by any PR run (verify once on a same-repo PR and once on a fork PR).
4. Local command: contributing.md documents the per-platform install, `lychee README.md`, and the GITHUB_TOKEN note, with no line implying an npm install.
5. PR template: the link-check checkbox is present as line 6 of 7.
6. Diff scope: exactly `.github/workflows/links.yml`, `contributing.md`, `.github/PULL_REQUEST_TEMPLATE.md` change; stale.yml and lint.yml are untouched.
7. YAML parse: `python -c "import yaml; yaml.safe_load(open('.github/workflows/links.yml'))"` passes, and the cron `0 18 * * 1` is unchanged.
8. No hard gate: `fail: false` remains, no step fails the job on lychee findings on any event, and no branch protection or required check is added.
9. No new `uses:` lines; the only actions referenced remain the P9-pinned checkout and lychee-action.

## Research

Action contract, install paths, and pitfalls from the research round (retrieved 2026-09-16; verdicts ESTABLISHED):

- https://github.com/lycheeverse/lychee-action (action surface, soft-fail pattern)
- https://raw.githubusercontent.com/lycheeverse/lychee-action/master/action.yml (inputs `args`, `fail`, `output`, `token`; output `exit_code`)
- https://github.com/lycheeverse/lychee (CLI install via platform package managers, `GITHUB_TOKEN` rate-limit mitigation)
- https://github.com/peter-evans/create-issue-from-file (no title-based dedupe)
- https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests (title search semantics and pitfalls)
- https://github.com/lycheeverse/lychee-action/issues/134 (fail-new-links versus issues-for-later-links split)
- https://github.com/lycheeverse/lychee-action/issues/238 (contributor friction from PR link checks)
- https://raw.githubusercontent.com/lycheeverse/lychee/master/docs/TROUBLESHOOTING.md (rate-limit failure mode)
