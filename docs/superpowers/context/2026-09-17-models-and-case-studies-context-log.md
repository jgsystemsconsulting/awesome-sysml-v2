# Context log: models-and-case-studies

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| README TOC Example Models at :13 | R1 | R1 | SINGLE-SOURCE | Two lenses, same loc; doc-only restatement, not independent |
| H2 Example Models at :76 | R1 | R1 | SINGLE-SOURCE | Same pair, doc-only |
| Nine entries README:78-86 | R1 | R1 | SINGLE-SOURCE | Same pair, doc-only |
| docs/index.html:83 hardcodes label and #example-models | R1 | R1 | CORROBORATED | cart+prosp doc + skeptic code site on live HTML |
| companion-docs-site spec:56 and plan:187 hardcode Example Models | R1 | R1 | SINGLE-SOURCE | Historical plan/spec docs; not live site |
| contributing inclusion criteria :5-11 | R1 | R1 | SINGLE-SOURCE | Multi-lens, one file, doc-only |
| contributing entry format + alpha sort :15-21 | R1 | R1 | SINGLE-SOURCE | Multi-lens, doc-only |
| b-09 open README structural rewrite backlog:15 | R1 | R1 | SINGLE-SOURCE | Multi-lens, one row |
| b-13 structured-use-cases needs-info backlog:19 + README:80,85 | R1 | R1 | CORROBORATED | backlog row + two live README entry sites |
| markdownlint only MD013 off; no section-name rules | R1 | R1 | CORROBORATED | config file + lint.yml + contributing local commands |
| Companion sync policy: same-change category map on rename | R1 | R1 | SINGLE-SOURCE | specs:106 only |
| docs/ outside lint/lychee; rename can ship green CI with dead site links | R1 | R1 | SINGLE-SOURCE | specs:112 only |
| contributing.md never names section titles; label rename need not edit it | R1 | R1 | SINGLE-SOURCE | skeptic; full-file scan agrees |
| CHANGELOG Keep a Changelog soft for list edits | R1 | R1 | SINGLE-SOURCE | CHANGELOG.md:5 |
| Flashlight starter under Migrating README:122 | R1 | R1 | SINGLE-SOURCE | boundary risk |
| awesome-submission runbook hardcodes "example models" | R1 | R1 | SINGLE-SOURCE | runbooks:53 |
| PR template section + alpha checklist | R1 | R1 | SINGLE-SOURCE | PULL_REQUEST_TEMPLATE |
| Current nine link texts sort A-S case-insensitive | R1 | R1 | SINGLE-SOURCE | README:78-86 order |

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| TOC/H2/entries locations | cart, prosp | SS | Use as edit targets |
| Live site #example-models | cart, prosp, skeptic | CORR | Must retarget with README |
| Contributing criteria/format | cart, prosp, skeptic | SS | Bind new entries; no section-title edit required |
| b-09 / b-13 | cart, prosp, skeptic | CORR/SS | Note overlap; leave b-13 open |
| Lint has no section-name gate | cart, prosp, skeptic | CORR | Manual site sync required |
| Sync policy + docs outside lint | skeptic | SS | Same-change README+index.html required |
| Flashlight / runbook / CHANGELOG soft | skeptic | SS | Boundary + optional copy updates |

Fixes applied: 0
Coverage: 6/6 criteria met
Validation: PASS (parent triage; ctx-triage spawn failed model-not-found GLM-5.2)

## Converged: Round 1

Track 1: Merged verdict CONTEXT_COMPLETE.
Every success criterion located. Decision-bearing claims for rename targets are CORROBORATED or named SINGLE-SOURCE. No CONFLICTED or STALE. Parent wrote triage after `ctx-triage` spawn failure (`model-not-found` for GLM-5.2).
Total rounds: 1  |  Total fixes: 0
Document is ready.
