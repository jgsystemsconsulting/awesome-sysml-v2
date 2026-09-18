# Context: maintenance-cadence-ack (P4)

## Context brief

- **Primary question**: What must change so contributing.md (or README) documents the repo's real maintenance cadence — weekly link scan, monthly freshness report, PR lint gates — as the plan, and where exactly does it go?
- **Success criteria**:
  - SC1: contributing.md current full section layout with line numbers (post-P7/P8: Inclusion criteria, Entry format, Local commands, Link check subsection).
  - SC2: The three automations' facts as they exist NOW post-P6/P7/P8 (weekly lychee cron + PR-time advisory + upsert report; monthly freshness with 24-month window; lint gates with pinned awesome-lint) — the documented cadence must match the AMENDED workflows, not the pre-P6/P7 ones.
  - SC3: Where a maintenance pointer belongs (contributing.md section vs README Contributing section) and the README's current Contributing section content.
  - SC4: Constraint: P4 is documentation-only; no workflow changes; the P6-fixed 24-month window and P7's upsert/labels are facts to describe, not re-litigate.
- **Out of scope**: workflow edits (all done in P6-P9); README entry content; new automations.
- **Budget**: 1 round; cap 3.
- **Workspace baseline**: HEAD b562394 (P7 landed; contributing.md now 40 lines with Link check subsection at 32+).

## Findings

Full graded claim table in the round log. 8 claims, verdict CONTEXT_COMPLETE, 0 conflicted/stale. Key facts (HEAD b562394):

- contributing.md (SC1): `## Inclusion criteria` (5), `## Entry format` (13), `## Local commands` (23) with the npx fence (27-30) and `### Link check` subsection (32-40). Heading style: `##` top-level, `###` subsection; terse imperative prose. 40 lines total.
- Amended automation facts (SC2): links.yml — weekly cron `0 18 * * 1` Monday, plus `pull_request` advisory check (`fail: false`, `::warning::`), issue step gated to non-PR AND exit!=0 (so the Link Checker Report upserts only when links break; clean weeks never touch it); stale.yml — monthly cron `0 6 1 * *` (06:00 UTC, day 1), 24-month window (cutoff + report strings), ALWAYS upserts the Freshness report issue (even clean months), scans only `github.com/owner/repo` URLs from README; lint.yml — PR/push gates running `npx awesome-lint@2.3.0` and the markdownlint action (blocking), local markdownlint is unpinned npx.
- README (SC3): `## Contributing` at 126-128 — one sentence delegating to contributing.md "for the inclusion criteria, entry format, and local lint commands".
- Constraints (SC4): markdownlint has only MD013 off; no heading-order constraints; no existing Maintenance/cadence text anywhere.
- Drift traps the spec must absorb (skeptic, config-sited): criterion 4 says "commit within 24 months" while freshness measures `pushed_at` (last push) — a Maintenance section must not equate them; Link report upserts only on failure vs Freshness always; freshness covers github.com URLs only; PR link check is advisory while lint is blocking; `## Maintenance` goes as a top-level sibling (not under `### Link check`); README's one-liner should gain "maintenance" in its list so the pointer stays complete.

## Synthesis

All four success criteria met (4/4); verdict CONTEXT_COMPLETE. SC1 corroborated by three independent reads; SC2 corroborated config-sited (cartographer + skeptic); SC3 corroborated (prospector + skeptic); SC4 corroborated. Single-source items: none material. The skeptic's drift traps are the spec's content requirements: describe the cadence exactly as the amended workflows behave (advisory vs blocking asymmetry, failure-only vs always upsert, github.com-only freshness scope, push-not-commit proxy), place `## Maintenance` as a top-level contributing.md sibling, and extend the README Contributing one-liner. Open questions: none.

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| contributing.md:5,13,23,32 | doc | cartographer, prospector, skeptic (layout; Link check subsection) |
| contributing.md:10 | doc | skeptic (criterion 4 commit wording) |
| contributing.md:27-30 | doc | prospector, skeptic (fence; unpinned markdownlint line 29) |
| .github/workflows/links.yml:11,13,29,47 | config | cartographer, skeptic (cron, PR trigger, fail:false, gated upsert) |
| .github/workflows/stale.yml:11,28,30,35,50 | config | cartographer, skeptic (monthly cron, 24-month strings, URL grep, always-upsert) |
| .github/workflows/lint.yml:10-13,29 | config | cartographer, skeptic (PR/push, awesome-lint@2.3.0) |
| README.md:126-128 | doc | prospector, skeptic (Contributing one-liner) |
| .markdownlint-cli2.jsonc:3 | config | prospector (MD013 off) |
