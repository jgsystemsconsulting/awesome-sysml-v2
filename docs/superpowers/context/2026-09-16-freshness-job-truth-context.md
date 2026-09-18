# Context: freshness-job-truth (P6)

## Context brief

- **Primary question**: What must change so the monthly freshness job always produces a report (per-repo API failures non-fatal) and enforces exactly one freshness window shared with contributing.md criterion 4 (24 months), and what workspace facts constrain that change?
- **Sub-questions**:
  1. Exact current curl/jq/continue logic in stale.yml under `set -euo pipefail` (the abort path: `curl -sf` in command substitution; the `[ -n "$pushed" ] || continue` skip that never sees transport failures).
  2. Complete inventory of "12 months" strings in stale.yml (cutoff date math, report header echo, threshold footer line) that must sync to the chosen window.
  3. contributing.md criterion 4 exact wording (24 months or foundational value) and how a synced window should be phrased there.
  4. What must be preserved: create-or-update Freshness report issue pattern, cron, permissions, workflow name, grep URL extraction, the rest of the run script.
- **Success criteria**:
  - SC1: The abort mechanism is located and quoted (set -euo pipefail + curl -sf in command substitution; skipped continue path).
  - SC2: Every "12 months"-window string in stale.yml is inventoried with line numbers (expected: cutoff math, report header, footer threshold line).
  - SC3: contributing.md criterion 4 quoted exactly; any other freshness-policy mentions in the repo found (README, PR template, docs/).
  - SC4: Preservation surface inventoried (issue upsert block, cron, permissions, workflow name, URL grep charset).
- **Out of scope**: links.yml/lychee (P7); lint.yml (P8); Actions pins (done, P9); README entry content; new workflows.
- **Budget**: 1 round target; cap 3.
- **Workspace baseline**: porcelain sha256 recorded at gate time; HEAD `1747fa6d4f5d7c89dbe25884e2456da0098751f5` (P9 landed; stale.yml line numbers shifted +6 from the P9 comment block).

## Findings

Full graded claim table in the round log. 20 claims: 11 corroborated, 9 single-source, 0 conflicted, 0 stale. Key facts (current line numbers, HEAD 1747fa6, post-P9 +6 shift):

- Abort mechanism (SC1, corroborated x3 lenses): stale.yml:27 `set -euo pipefail`; stale.yml:36 `pushed=$(curl -sf ... | jq -r ".pushed_at // empty")` — curl -sf in command substitution makes any transport failure (404/403, rate limit, non-JSON) abort the step before stale.yml:37 `[ -n "$pushed" ] || continue` can run. pipefail couples curl AND jq: softening curl alone still aborts on jq/non-JSON.
- 12-month window strings (SC2, corroborated): stale.yml:28 cutoff math, stale.yml:30 issue header ("Entries with no push in over 12 months"), stale.yml:44 footer ("No entries exceeded the 12-month threshold.") — three strings, footer window-bearing.
- Policy (SC3, corroborated x3): contributing.md:10 criterion 4 — "Active maintenance (commit within 24 months) or foundational value (formal specs, canonical reference repos)." PR template and README state no month figures. Known policy nuances for the spec to settle: (a) criterion 4 is "24 months OR foundational value" — the report is advisory and will still list stale-but-foundational repos; (b) policy says commit, automation compares pushed_at — semantic drift is pre-existing and accepted.
- Preservation surface (SC4, corroborated): issue upsert stale.yml:50-55 (gh issue list/edit/create "Freshness report"), cron stale.yml:11, permissions stale.yml:13-16, workflow name stale.yml:1, URL grep charset stale.yml:34.
- Reuse: links.yml `fail: false` is the house expected-failure pattern; markdownlint MD013 false (no line-length cap) for contributing.md edits.
- Gotchas: empty URL grep yields found=0 + clean footer (looks like a full scan); the 2026-09-15 findings doc cites stale.yml line numbers that predate the P9 +6 shift (its stale.yml:21/22/30-31 are now 27/28/36-37).

## Synthesis

All four success criteria met (4/4). The decision-bearing claims (abort mechanism, the three window strings, criterion 4, preservation surface) are each corroborated by at least two lenses with code/config sites. Single-source items, named here: README URL-flow observation, commit-vs-pushed_at drift note, empty-grep footer note, findings-doc stale line-number note, links fail:false analog, MD013 config, workflow name — all boundary or advisory observations, none decision-bearing. The triage's three residual items resolve as: criterion-4 single-siting framed above (it is the only policy statement; three lenses read it independently); commit-vs-pushed_at is a pre-existing accepted nuance for the spec to carry as a documented limitation, not an evidence gap; findings-doc line drift is a dated-record property, noted for the implementer. Open questions: none blocking. Workspace baseline at gate time: HEAD 1747fa6.

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| .github/workflows/stale.yml:1 | code | prospector (workflow name) |
| .github/workflows/stale.yml:9-16 | config | cartographer (triggers, permissions) |
| .github/workflows/stale.yml:11 | code/config | prospector, skeptic (cron) |
| .github/workflows/stale.yml:16 | code | prospector (issues: write) |
| .github/workflows/stale.yml:27 | code/config | cartographer, prospector, skeptic (set -euo pipefail) |
| .github/workflows/stale.yml:28 | code/config | cartographer, prospector, skeptic (12-month cutoff) |
| .github/workflows/stale.yml:30 | code/config | cartographer, prospector, skeptic (12-month header) |
| .github/workflows/stale.yml:33 | code | skeptic (found=0) |
| .github/workflows/stale.yml:34 | code/config | cartographer, prospector (URL grep charset) |
| .github/workflows/stale.yml:36 | code | cartographer, prospector, skeptic (curl -sf fetch) |
| .github/workflows/stale.yml:37 | code/config | cartographer, skeptic (dead continue) |
| .github/workflows/stale.yml:38 | code/config | cartographer, prospector (cutoff comparison) |
| .github/workflows/stale.yml:44 | code | prospector, skeptic (12-month footer) |
| .github/workflows/stale.yml:50-55 | code/config | cartographer, prospector, skeptic (issue upsert) |
| .github/workflows/links.yml:28 | code | prospector (fail: false) |
| .github/workflows/lint.yml | (P8 boundary) | - |
| contributing.md:10 | doc | cartographer, prospector, skeptic (criterion 4) |
| .github/PULL_REQUEST_TEMPLATE.md:1 | doc | cartographer, skeptic (no months) |
| README.md:21-49 | doc | cartographer (URLs, no window text) |
| .markdownlint-cli2.jsonc:3 | config | prospector (MD013 false) |
| docs/superpowers/reviews/2026-09-15-awesome-sysml-v2-findings.md:55 | doc | skeptic (stale line refs) |
