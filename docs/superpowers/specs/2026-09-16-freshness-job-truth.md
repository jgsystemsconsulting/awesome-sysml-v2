# Freshness job truth (P6): non-fatal fetch, one 24-month window

- Date: 2026-09-16
- Package: P6 of the awesome-sysml-v2 work packages
- Absorbs: repo-review-loop findings I3 (fatal per-repo fetch) and I1 (window drift)
- Baseline: HEAD 1747fa6, workspace clean at gate time; line numbers below are current (post-P9)
- Constraints locked in the packages document; this spec fixes the remaining design decisions

## Problem statement

Two defects, one workflow file.

I3, the abort path. The monthly Freshness report job dies on the first per-repo GitHub API failure. stale.yml:27 sets `set -euo pipefail`. stale.yml:36 fetches inside command substitution:

```bash
pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty")
```

Any curl transport failure (404, 403 rate limit, timeout) or jq failure (non-JSON body, binary missing) makes the pipeline nonzero under pipefail. `set -e` then kills the step before stale.yml:37's `[ -n "$pushed" ] || continue` can run. One flaky repo means no report issue that month.

I1, the window drift. The workflow enforces 12 months while contributing.md criterion 4 (contributing.md:10) sets policy at 24 months: "Active maintenance (commit within 24 months) or foundational value (formal specs, canonical reference repos)." Three strings carry the wrong window: cutoff math (stale.yml:28), report header (stale.yml:30), footer threshold (stale.yml:44).

## Goals

- G1: The monthly job always finishes its report step and creates or updates the Freshness report issue, even when per-repo fetches fail. (A failure in the issue step itself remains fatal and is out of scope.)
- G2: Exactly one freshness window (24 months) appears in stale.yml, matching contributing.md criterion 4, in cutoff math, header, and footer.
- G3: The report states when repos were skipped, so a partial scan cannot read as a clean bill.
- G4: The report states its advisory nature, since criterion 4 is an OR and stale-but-foundational repos still belong in the list.

## Non-goals

- links.yml / lychee (P7). lint.yml / PR template (P8). Actions pins (P9, already landed).
- Non-GitHub URL freshness. README entry curation. P4 doc narrative beyond the cutoff number.
- Any change to: workflow name, cron, permissions block, checkout pin, URL grep charset, the cutoff comparison, the create-or-update issue upsert pattern, or the second step's script.
- The empty-grep property (zero URLs scanned still prints the clean `found=0` footer). The skip note covers API failures; a structurally empty URL list is a separate defect.
- Switching `pushed_at` to a commit-date API. The commit-vs-push drift is pre-existing and accepted (see Documented limitations).

## Codebase context

From the context gate (docs/superpowers/context/2026-09-16-freshness-job-truth-context.md, HEAD 1747fa6):

- Abort mechanism: stale.yml:27 `set -euo pipefail`; :28 cutoff `date -u -d "12 months ago"`; :30 header "over 12 months"; :36 `curl -sf ... | jq` fetch; :37 dead `[ -n "$pushed" ] || continue`; :44 footer "12-month threshold".
- Preservation surface: workflow name :1, cron :11, permissions :14-16, URL grep charset :34, issue upsert :50-55.
- Policy: contributing.md:10 criterion 4 already reads 24 months. PR template and README carry no month figures. markdownlint MD013 is off.
- House pattern for expected failure: links.yml:28 `fail: false` (this spec uses the shell-native `|| true` instead; no new workflow constructs).
- The 2026-09-15 findings doc cites pre-P9 line numbers (its stale.yml:21/22/30-31 are now 27/28/36-37). Match quoted text, not stale line numbers.

## Research

research: skipped (no-open-world-questions; all facts are repo-internal)

Track 3 halt at round 0, predicate no-open-world-questions: the fix is internal to stale.yml plus a window number that contributing.md already fixes. Round log: docs/superpowers/research/2026-09-16-freshness-job-truth-research-log.md. Context doc: docs/superpowers/context/2026-09-16-freshness-job-truth-context.md.

## Design

### D1. Non-fatal fetch: keep `-sf`, append `|| true` inside the substitution

Before (stale.yml:36):

```bash
pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty")
```

After:

```bash
pushed=$(curl -sf -H "Authorization: Bearer $GITHUB_TOKEN" "https://api.github.com/repos/$repo" | jq -r ".pushed_at // empty" || true)
```

Why this exact form:

- Under `set -o pipefail`, the pipeline's status is the rightmost nonzero. The substitution status is therefore nonzero for a curl transport failure (22 on HTTP error with `-f`; 6, 7, or 28 on network faults) and for a jq failure (exit 2 on a non-JSON body, 127 if jq is ever missing). `|| true` applies to the whole pipeline, drives the assignment status to 0, so `set -e` never fires and `$pushed` is empty on any failure.
- The pre-existing `[ -n "$pushed" ] || continue` already treats empty as skip. No new control flow; the change is one token.
- Keeping `-sf` means curl swallows HTTP error bodies itself, so jq normally sees nothing rather than an HTML page. The `|| true` still covers the residual jq paths (unexpected 200 body, missing binary).
- Verified with a local stub harness under `set -euo pipefail`: transport failure, HTML body, and 403 JSON without `pushed_at` all skip cleanly; a stale repo is still listed; the loop reaches the footer.

Rejected alternatives:

- Dropping `-f` only: absorbs transport errors through the empty-output path, but pipefail still aborts when jq meets a non-JSON 200 body. Does not meet the requirement.
- `if ! pushed=$(...); then continue; fi`: equivalent coverage, larger restructure of line 37 for no added benefit.
- `set +e` around the loop: too broad; masks real defects (typos, comparison errors) for the whole block.

### D2. Count skipped repos and say so in the report

A silent skip makes a rate-limited run print the same clean footer as a healthy one. The empty-grep gotcha already gives `found=0` one way to mislead; skips must not add another. Decision: count and note.

Before (stale.yml:37):

```bash
[ -n "$pushed" ] || continue
```

After:

```bash
[ -n "$pushed" ] || { skipped=$((skipped+1)); continue; }
```

Initialize `skipped=0` next to `found=0`, and insert this block after the `found` check, so the skip note is the last thing the report says:

```bash
if [ "$skipped" -gt 0 ]; then
  echo "Skipped $skipped repos whose GitHub API data was unavailable; the entry list above may be incomplete or empty." >> freshness-report.md
fi
```

Two implementation notes:

- Use `skipped=$((skipped+1))`, never `((skipped++))`. The arithmetic command form returns status 1 when the expression evaluates to 0, which kills the script under `set -e` on the first increment. The assignment form always returns 0.
- An empty `pushed_at` on a real 200 response would also count as a skip. GitHub repo objects always carry `pushed_at`, so the conflation is harmless and does not justify a second branch.

### D3. One window: 24 months, sourced from contributing.md

contributing.md criterion 4 is the canonical policy statement and already reads "commit within 24 months". It does not change. The three stale.yml strings are brought into compliance:

| Site | Before | After |
|---|---|---|
| :28 cutoff math | `date -u -d "12 months ago"` | `date -u -d "24 months ago"` |
| :30 header | "over 12 months" | "over 24 months" plus the D4 clause |
| :44 footer | "No entries exceeded the 12-month threshold." | "No entries exceeded the 24-month threshold." |

Window consistency greps: `grep -nE "12 months|12-month" .github/workflows/stale.yml` returns nothing; `grep -n "24 months" contributing.md` still matches criterion 4.

### D4. Header carries one advisory clause

Criterion 4 is an OR: a repo can be stale on the clock and still valid because it is a formal spec or a canonical reference. The report lists stale-but-foundational repos and must not read as a removal list. Decision: one sentence appended to the header line.

Before (stale.yml:30):

```bash
echo "Entries with no push in over 12 months (as of $(date -u +%Y-%m-%d)):"
```

After:

```bash
echo "Entries with no push in over 24 months (as of $(date -u +%Y-%m-%d)). Advisory only: entries meeting the foundational-value exception (contributing.md criterion 4) are still valid."
```

The clause lives once, in the header, where a reader starts. The footer stays factual and carries only the window number.

### Full after-state run block (step "Build freshness report")

```bash
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

Unchanged, in full: the P9 comment block, workflow name, `on` (cron plus workflow_dispatch), permissions, checkout pin, the "Create or update the issue" step, links.yml, lint.yml.

## Documented limitations (accepted, not fixed here)

- Policy says "commit within 24 months"; automation compares `pushed_at`. For most repos the two are close. The drift is pre-existing and out of scope.
- `pushed_at` moves on any default-branch push, including doc-only commits. It is a proxy, not a maintenance audit.
- The skip count merges transport failures and empty payloads. Separating them would put per-repo error strings into the report; not worth it until a real failure pattern demands it.

## Risks

- Systemic failure (expired token, API outage) now yields a report of zero entries plus a skip line instead of no report. That is the intended trade: an honest partial report beats a missing one. When every repo skips, the count equals the URL count and the report reads correctly: an empty entry list, the 24-month footer, then the skip note as the last line.
- `|| true` can mask a scripting defect such as a jq filter typo, converting it into a skip. Mitigation: the skip count surfaces it in the report; acceptance check 6 keeps the extracted script under basic lint.
- The bash arithmetic gotcha (`((x++))` under `set -e`) is a plausible implementer mistake. D2 fixes the exact form; acceptance check 6 exercises the increment.
- Line-number drift in the 2026-09-15 findings doc can send an implementer to the wrong lines. The quoted text in this spec is the source of truth.

## Acceptance criteria

1. Fatal-fetch fix: with the step-1 script body extracted and `curl` stubbed to fail (nonzero exit, empty output) for one repo and return valid JSON for the rest, the script exits 0 under `set -euo pipefail`, lists the stale repos, and appends the skip note with count 1. A second variant where the stub emits a non-JSON body must behave the same.
2. End-to-end intent: with at least one dead repo in README.md, a workflow_dispatch run completes both steps and the Freshness report issue is created or updated. Runner verification; the local harness in check 1 covers the mechanism.
3. Window consistency: all three window strings read 24 months; `grep -nE "12 months|12-month" .github/workflows/stale.yml` is empty; contributing.md criterion 4 is byte-identical to the current text.
4. Diff scope: `git diff` touches only `.github/workflows/stale.yml`, only inside the run block of the "Build freshness report" step. Workflow name, cron, permissions, checkout pin, grep charset, comparison, second step: no changed lines.
5. YAML parse: the workflow file loads as YAML (`python -c "import yaml; yaml.safe_load(open('.github/workflows/stale.yml'))"`, or actionlint if installed).
6. Shell sanity: `bash -n` on the extracted script body passes; if shellcheck is installed it reports no new findings; a one-line `bash -c 'set -euo pipefail; s=0; s=$((s+1)); echo ok'` run prints ok.
