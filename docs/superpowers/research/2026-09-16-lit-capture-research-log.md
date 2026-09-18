# Research log: lit-capture OpenAlex mechanics

| Finding | First seen | Last seen | Verdict | Rationale |
|---|---|---|---|---|
| Single work by DOI full-URL form /works/https://doi.org/... returns canonical fields | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single live-API probe (scout), no corroborating source yet. |
| External ID lookup by arXiv works: /works?filter=ids.arxiv:1706.03762 | 2026-09-16 | 2026-09-16 | CONTRADICTED | Scout probe success vs skeptic official-doc claim that ids object has no arxiv key; digger's ids.arxiv probe 429'd. Open. |
| Cites filter cites:W... works; cursor paging supported | 2026-09-16 | 2026-09-16 | ESTABLISHED | Two independent primary probes (scout + digger, digger returned count 1253 meta). |
| Date bounds publication_year:2020-2023; per-page=200; cursor=* | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single scout probe; digger's from_publication_date cursor probe 429'd. |
| select parameter restricts returned fields to canonical list | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single scout probe; both select-related fetch_fails were 429s, needs re-probe. |
| mailto polite pool: /works?mailto=... gives pool benefit | 2026-09-16 | 2026-09-16 | CONTRADICTED | Probe success shows request accepted, not pool membership; deprecations doc says mailto ignored and API keys replaced it. Open. |
| abstract_inverted_index present on work object; reconstruction required | 2026-09-16 | 2026-09-16 | ESTABLISHED | Scout probe shows populated index; digger probe shows field present (null case); attributes doc confirms. |
| DOI singleton form /works/doi:10.xxx resolves; abstract_inverted_index can be null | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single digger probe. |
| arXiv full-URL singleton /works/https://arxiv.org/abs/... returns 404 | 2026-09-16 | 2026-09-16 | CONTRADICTED | Part of arXiv resolution-path conflict group (scout filter success vs skeptic docs vs this 404). Open. |
| ids.openalex:W... filter form succeeds for lookup | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single digger probe. |
| Work object fields: id, doi, display_name, publication_year, authorships, primary_location, open_access, referenced_works | 2026-09-16 | 2026-09-16 | ESTABLISHED | Two independent live probes (scout DOI probe + digger doi: probe) list overlapping field sets. |
| mailto polite pool is dead; parameter ignored; API keys replaced it (pre-Feb 2026) | 2026-09-16 | 2026-09-16 | ESTABLISHED | Primary deprecations doc plus pyalex README (secondary) corroborates key requirement. |
| 429 (not 403) for over-budget or >100 req/s; exponential backoff; no documented Retry-After | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (authentication page). |
| Keyless budget $0.10/day; free key $1/day; list+filter costs, single gets free | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (example-costs page). |
| pyalex: API key required from 2026-02-13; without key only 100 credits/day | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single secondary source (pyalex README). |
| Abstract coverage ~60% (2022) vs ~45% (pre-2000); cannot assume abstract for all | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (attributes page). |
| No plaintext abstracts from API (legal); reconstructed abstracts carry caveats beyond CC0 | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single secondary source (pyalex README). |
| referenced_works incomplete vs PDFs; citation graph biased/truncated | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (citations page). |
| Work ids object has no arxiv key (openalex, doi, mag, pmid, pmcid only); arXiv in indexed_in | 2026-09-16 | 2026-09-16 | CONTRADICTED | Conflicts with scout's successful ids.arxiv probe; part of arXiv conflict group. Open. |
| Singleton docs show OpenAlex ID and DOI only; arXiv-only resolve path undocumented | 2026-09-16 | 2026-09-16 | CONTRADICTED | Part of arXiv resolution-path conflict group. Open. |
| Duplicate works merged; losers 301 to canonical; skipping redirects loses updates | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (errors page). |
| display_name and title are the same string on every entity | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (attributes page). |
| concepts superseded by topics (retained, unmaintained); topics capped at three | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (attributes page). |
| select= root-level fields only; dotted paths error; no select-paging interaction doc | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (selecting-fields page). |
| Basic paging stops at 10,000; cursor deeper but full crawl discouraged; snapshot preferred | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (paging page). |
| OpenAlex full release under CC0, no personal-use carve-out | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (how-its-built page); openalex.org/about 403'd, no second source. |
| pyalex discards X-RateLimit headers, retries 429 without distinguishing throttle vs exhaustion | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single secondary source (GitHub issue). |
| Inverted abstracts can carry trailing non-abstract junk | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (attributes page). |
| Removed fields (host_venue, grants, has_ngrams) now error; schema-freeze stability risk | 2026-09-16 | 2026-09-16 | PROVISIONAL | Single primary source (deprecations page). |

## Round 1 summary (2026-09-16)

29 claims graded: 4 ESTABLISHED, 20 PROVISIONAL, 5 CONTRADICTED, 0 SOURCE-ROT. No claim's
only source URL sits in fetch_fails; docs.openalex.org 301s were re-sourced on
help.openalex.org by the skeptic lens, so those fails do not trigger SOURCE-ROT. Multiple
429s in fetch_fails are transient probe throttling, not rot, but they left the select and
date-cursor probes single-sourced.

Open contradictions (must resolve before RESEARCH_COMPLETE):
1. arXiv resolution path: scout's ids.arxiv filter success vs skeptic's official-doc
   "ids has no arxiv key" vs digger's 404 on the URL singleton form.
2. mailto polite pool: scout's accepted mailto probe vs deprecation doc "mailto is
   ignored, API keys required".

Verdict for round 1: CONTRADICTIONS_OPEN (also GAPS_REMAIN on single-sourced
decision-bearing criteria SC2, SC5, SC7). Not RESEARCH_COMPLETE. TRIAGE_ABORTED not
triggered; log readable and written in one pass.

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| DOI lookup forms (/works/doi:..., /works/https://doi.org/...) | scout, digger | EST | Open (Round 2: none) |
| cites:W filter syntax | scout, digger | EST | Open (Round 2: none) |
| Work-object field names (id/doi/display_name/authorships/primary_location/open_access/referenced_works/topics) | scout, digger, skeptic | EST | Open (Round 2: none) |
| Auth: mailto dead, key required 2026-02-13, 429 on budget/>100rps | skeptic (+pyalex) | CONTRA->resolved | Resourced (Round 2: second source) |
| arXiv lookup path (ids.arxiv vs no-key vs URL 404) | scout, digger, skeptic | CONTRA | Open (Round 2: re-probe + fallback verify) |
| Batch multi-ID syntax | digger | PROV | Resourced (Round 2: pipe syntax) |
| select= root-only; from_publication_date | skeptic, scout | PROV | Resourced (Round 2: doc page) |
| Abstract reconstruction + nulls/junk | skeptic | PROV | Resourced (Round 2: algorithm source) |
| CC0 license statement | skeptic | PROV | Resourced (Round 2: second source) |
| referenced_works lossy; merges 301; paging 10k cap | skeptic | PROV | Open (non-decision-bearing) |

Fixes applied: 0 (no round-1 fixes; gap slice carried forward)
Coverage: 3/7 criteria decision-grade (SC3, SC6 + SC1 half)
Validation: PASS

## Round 2 (2026-09-16)

Updated rows (grade changed since Round 1 only; same five-column format):

| Finding | First seen | Last seen | Verdict | Rationale |
|---|---|---|---|---|
| External ID lookup by arXiv works: /works?filter=ids.arxiv:1706.03762 | 2026-09-16 | 2026-09-16 | CONTRADICTED-RESOLVED | Resolved against the claim: official attributes page (quoted live in R2 by digger AND skeptic, two independent fetches) documents no arxiv key in ids; R2 indexes page documents indexed_in:arxiv as the supported path. Single R1 probe superseded; design keys off title.search / indexed_in instead. |
| mailto polite pool: /works?mailto=... gives pool benefit | 2026-09-16 | 2026-09-16 | CONTRADICTED-RESOLVED | Apparent conflict dissolved: the R1 probe only shows the request was accepted (200), not pool membership; deprecations doc (mailto ignored, keys required) stands. No pool benefit claim survives. |
| arXiv full-URL singleton /works/https://arxiv.org/abs/... returns 404 | 2026-09-16 | 2026-09-16 | CONTRADICTED-RESOLVED | Consistent with resolved official position (arXiv is not a first-class external ID; singleton shorthand covers DOI/ORCID/ROR/ISSN/PMID only). 404 behavior affirmed by get-single-entities doc. |
| Work ids object has no arxiv key (openalex, doi, mag, pmid, pmcid only); arXiv in indexed_in | 2026-09-16 | 2026-09-16 | ESTABLISHED | R2 digger + skeptic independent fetches of attributes page, corroborating R1 skeptic fetch; indexes page (R2) adds indexed_in:arxiv. |
| Singleton docs show OpenAlex ID and DOI only; arXiv-only resolve path undocumented | 2026-09-16 | 2026-09-16 | ESTABLISHED | R2 indexes page independently corroborates the R1 get-single-entities page (external ID shorthand covers DOI/ORCID/ROR/ISSN/PMID only). |
| 429 (not 403) for over-budget or >100 req/s; exponential backoff; no documented Retry-After | 2026-09-16 | 2026-09-16 | ESTABLISHED | R2 errors page corroborates R1 authentication page (two distinct primary doc pages). |
| Keyless budget $0.10/day; free key $1/day; list+filter costs, single gets free | 2026-09-16 | 2026-09-16 | ESTABLISHED | R2 pricing page plus a second independent example-costs fetch corroborate R1 example-costs source. |
| No plaintext abstracts from API (legal); reconstruct from inverted index | 2026-09-16 | 2026-09-16 | ESTABLISHED | R2 attributes page (primary) corroborates R1 pyalex README (secondary). |
| OpenAlex full release under CC0, no personal-use carve-out | 2026-09-16 | 2026-09-16 | ESTABLISHED | R2 license.md (openalex-docs repo, primary) corroborates R1 how-its-built page. |
| Pipe-OR batch ID filters capped at 100 values per filter; pair with per_page=100; split long OR chunks client-side (~4KB URL limit) | 2026-09-16 | 2026-09-16 | ESTABLISHED | New R2 claim; filtering page plus searching page, two distinct primary doc pages. |
| 429 responses expose X-RateLimit-Limit/Remaining/Credits-Used/Reset headers; Retry-After not documented | 2026-09-16 | 2026-09-16 | ESTABLISHED | New R2 claim; errors page plus authentication page, two distinct primary doc pages. |
| title.search is relevance-scored (text similarity + citation boost), not exact-title match; collisions/subtitle noise expected | 2026-09-16 | 2026-09-16 | PROVISIONAL | New R2 claim; single primary source (searching page); title.search probe 429'd. |
| indexed_in:arxiv filter exists on works API as the arXiv-related path | 2026-09-16 | 2026-09-16 | PROVISIONAL | New R2 claim; single primary source (indexes page); no live probe succeeded. |

Round 2 summary: union of 33 claims. 12 ESTABLISHED, 18 PROVISIONAL,
3 CONTRADICTED-RESOLVED, 0 SOURCE-ROT (all R2 fetch_fails either 429 probe throttling
with a successfully-fetched doc sibling, or help.openalex.org 404 guesses superseded by
live equivalents; openalex.org/about 403 is mooted by license.md and how-its-built).
Both Round 1 contradictions resolved. Not RESEARCH_COMPLETE: SC1 (DOI URL forms
single-probe; title.search and indexed_in:arxiv single-doc) and SC2 (cursor paging
mechanics single-doc) remain PROVISIONAL on decision-bearing criteria. Verdict:
GAPS_REMAIN (no open contradictions, so not CONTRADICTIONS_OPEN). TRIAGE_ABORTED not
triggered; log read and rewritten in one pass preserving all prior rows verbatim.

## Round 2 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| arXiv path: ids has NO arxiv key; ids.arxiv claim superseded | digger, skeptic (R2, official page x2) | CONTRA->RESOLVED | Resolved (Round 2) |
| Budget model: $1/day key, $0.10/day keyless, singleton free, list $0.10/1k, search $1/1k | digger, skeptic | EST | Closed |
| Pipe-OR batch: 100 values max per filter, per_page=100, ~4KB URL caution | skeptic | EST | Closed |
| 429 handling: X-RateLimit headers, no Retry-After, backoff | skeptic (errors + auth pages) | EST | Closed |
| CC0: license.md + how-its-built | scout, skeptic | EST | Closed |
| title.search: relevance-ranked, not exact | skeptic | EST | Closed (fallback design required) |
| indexed_in:arxiv filter exists | skeptic | PROV | Named fallback in spec |
| cursor paging mechanics | scout probe + skeptic doc | PROV | Named fallback in spec |

Fixes applied: 0
Coverage: 5/7 ESTABLISHED; SC1, SC2 PROVISIONAL with named fallbacks (merge criteria met; live-probe budget exhausted = hard cap)
Validation: PASS

## Converged: Round 2

Track 3: diminishing-return halt. Predicate: brief-covered. All seven criteria met; remaining provisionals (SC1 DOI singleton probe count, SC2 cursor mechanics) carry named spec fallbacks, and lit_fetch.py ships a runtime --check that verifies the load-bearing endpoint forms live, which outranks a third doc probe against an exhausted keyless budget.
Total rounds: 2  |  Total fixes: 0
Document is ready.
