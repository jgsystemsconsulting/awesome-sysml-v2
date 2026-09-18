# Backlog: awesome-sysml-v2

One project per repository. Rows are never deleted; every transition is a status change.

| id | title | source | status | evidence |
|----|-------|--------|--------|----------|
| b-01 | Add extra weekly/daily link or content scanner beyond links.yml | triage round 1 2026-09-15 (kills) | needs-info | .github/workflows/links.yml weekly cron 0 18 * * 1 |
| b-02 | Add monthly freshness automation | triage round 1 2026-09-15 (kills) | needs-info | .github/workflows/stale.yml monthly cron 0 6 1 * * |
| b-03 | TODO/FIXME cleanup drive | triage round 1 2026-09-15 (kills) | needs-info | repo survey: no TODO/FIXME/HACK hits |
| b-04 | Split homepageUrl-only vs docs/-only packages | triage round 1 2026-09-15 (kills) | needs-info | org site standard: docs/ + homepageUrl is one Pages surface |
| b-05 | Per-file packages for CoC/SECURITY/CITATION/CHANGELOG | triage round 1 2026-09-15 (kills) | needs-info | repo survey missing-files list |
| b-06 | Mega package site+public+meta+maintenance | triage round 1 2026-09-15 (kills) | needs-info | spans docs/, GitHub settings, root meta, .github/workflows |
| b-07 | CHANGELOG.md as standalone work (if X1 resolves it out of P5) | triage round 1 2026-09-15 (kills) | done | CHANGELOG.md present at repo root |
| b-08 | CITATION.cff as standalone work (if X1 resolves it out of P5) | triage round 1 2026-09-15 (kills) | done | CITATION.cff present; license CC0-1.0 |
| b-09 | README structural rewrite | triage round 1 2026-09-15 (kills) | open | README has badge, TOC, ~70 entries; already lint-clean |
| b-10 | Expand CI beyond awesome-lint/markdownlint | triage round 1 2026-09-15 (kills); reaffirmed needs-info round 2 | needs-info | .github/workflows/lint.yml gates PR and push to main |
| b-11 | awesome.re submission path (if P3 drops it) | triage round 1 2026-09-15 (P3 out_scope) | open | intent:2 discoverability review |
| b-12 | Decide lychee gate policy: keep weekly soft gate (a-04) or flip PR path to hard fail | triage round 2 2026-09-16 (advisory a-04) | promoted | promoted into 2026-09-18 P2 link-check-product-surface (outcome bar hard-fail on product surface) |
| b-13 | Near-parallel structured-use-cases entries lack proven same-project identity | triage round 2 2026-09-16 (advisory a-01) | needs-info | README.md:80,85 |
| b-14 | Verify Cameo docs URL 2026x path segment will not age out | triage round 2 2026-09-16 (advisory a-03) | open | README.md:121 |
| b-15 | Pin Node 20 in local runbook to match CI setup-node | triage round 2 2026-09-16 (advisory a-11) | open | .github/workflows/lint.yml:L16-20; contributing.md:27-29 |
| b-16 | Record-only advisories a-02 (Syside layering), a-05 (no marker debt), a-06 (labels, absorbed by P7), a-07 (title search, mitigated), a-08 (injection mitigated), a-09/a-10 (secrets/scopes clean) | triage round 2 2026-09-16 (kills) | needs-info | findings doc 2026-09-15 advisories table |
| b-17 | links.yml lychee args lack file operands: args override replaced the action's default globs, so lychee exits 2 (missing inputs) and the weekly job reports a config error, not broken links | final review P4 2026-09-16 | done | fixed in commit b3d842e: args now end with README.md |
| b-18 | After push: enable Pages (main:/docs via gh api POST), set homepageUrl to https://jgsystemsconsulting.github.io/awesome-sysml-v2/, verify live URL 200 — P2 Task 6, deferred until origin/main carries de549d9 | P2 run 2026-09-16 | done | gh pages status built; homepageUrl set; DISTRIBUTION Pages row submitted 2026-09-16 |
| b-19 | og:image social-card regen for light Path S shell (optional) | taste n-01 2026-09-18 | open | docs/superpowers/reviews/2026-09-18-landing-taste.md n-01 |
| lit-capture-1 | Consider filter=title.search for --title/--arxiv resolution (scoped, title-only search) instead of generic search= | lit-capture | open | docs/superpowers/plans/2026-09-16-lit-capture-fcl-triage-log.md Round 1 row 3; spec --title verb row |
| lit-cap-2 | Reconsider x-ratelimit-remaining=0 abort guard: shared-IP keyless users locked out while API serves 200s | lit-capture | open | docs/superpowers/specs/2026-09-16-lit-capture-fcl-triage-log.md Round 1 rows C2/C4; jgs-lit-memory lit_fetch.py http_get |
| lit-cap-3 | verb_inbox should check x-ratelimit-remaining between entries like verb_ids does (budget stop currently multi-chunk only) | lit-capture | open | jgs-lit-memory lit_fetch.py verb_inbox |
| lit-cap-4 | BudgetExhausted is unreachable dead code; verb_inbox docstring describes an impossible re-raise | lit-capture | open | jgs-lit-memory lit_fetch.py BudgetExhausted, verb_inbox docstring, main handler |
| lit-cap-5 | corpus_keys has no direct offline check (only indirect coverage via inbox triage flow) | lit-capture | open | jgs-lit-memory test_lit_fetch.py |
| awesome-magicgrid-mbse-1 | Intro sister href dropped for double-link vs plan count-2 grep | awesome-magicgrid-mbse | open | docs/superpowers/plans/2026-09-17-awesome-magicgrid-mbse-ivl-triage-log.md (M1 Design) |
| awesome-magicgrid-mbse-2 | Book catalog hosts flaky under lychee (Goodreads 202, Amazon 503, Open Library timeout) | awesome-magicgrid-mbse | open | docs/superpowers/plans/2026-09-17-awesome-magicgrid-mbse-ivl-triage-log.md (C1) |
| awesome-magicgrid-mbse-3 | INCOSE OOSEM portal allowlisted 403 outside brief vendor/DOI class | awesome-magicgrid-mbse | open | C:/Users/gower/OneDrive/Documents/GitHub/awesome-magicgrid-mbse/CHANGELOG.md Accepted 403 |
| awesome-magicgrid-mbse-4 | Extra GitHub topic awesome required by awesome-lint beyond named four | awesome-magicgrid-mbse | open | gh repo topics on jgsystemsconsulting/awesome-magicgrid-mbse |
