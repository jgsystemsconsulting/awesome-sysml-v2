# Research: OpenAlex API mechanics for lit_fetch.py

## Research brief

**Primary question.** What are the exact OpenAlex REST API mechanics needed for `lit_fetch.py` (Python, stdlib only) to fetch scholarly work metadata by DOI and arXiv ID, batch-retrieve, filter by citing works, and emit normalized JSON records plus citation edges for the `.lit/` directory format?

**Context.** Spec: lit-capture (jgs-lit-memory skill repo). `lit_fetch.py` is the only component that talks to OpenAlex. Everything downstream (capture skill, triage, `.lit/` SKILL.md contract) consumes its normalized output: `papers/*.json` (OpenAlex work schema plus local flags) and `graph/edges.jsonl` (`{source, target}` where source cites target, both OpenAlex IDs).

**Sub-questions.**
1. Work lookup by DOI: exact URL form(s) that resolve.
2. Work lookup by arXiv identifier: does OpenAlex resolve arXiv IDs/URLs as external IDs? Exact form, and known gaps.
3. Batch retrieval of many works in one request (filter syntax for ID sets) and cursor paging for large result sets.
4. Filter for "papers citing work W" (`cites:W...` style) and date bounds (`from_publication_date`).
5. Polite pool and rate limits: `mailto` parameter, requests/second, daily cap.
6. `abstract_inverted_index`: format and reconstruction algorithm.
7. Canonical field names on the work object: id, doi, title/display_name, publication_date, authorships, referenced_works, cited_by_count, topics, open_access, primary_location; is there a cap on `referenced_works`?
8. License status for redistributing OpenAlex metadata (CC0?) and expected attribution norms.
9. `select=` parameter to slim payloads; interaction with filters.

**Success criteria.** The spec author can write `lit_fetch.py`'s interface and the `.lit/` record schema without guessing:
- SC1: verified URL forms for DOI and arXiv-ID lookup (each demonstrated by at least one live or documented example).
- SC2: verified batch + paging mechanics sufficient for a 500-work pack.
- SC3: verified citing-works filter syntax.
- SC4: verified rate-limit numbers and polite-pool requirement.
- SC5: verified abstract reconstruction algorithm (or documented absence).
- SC6: confirmed field names verbatim from the works-object reference.
- SC7: license status confirmed with primary-source URL.

**Out of scope.** Semantic Scholar and arXiv APIs; pack publishing/export; capture-skill design; hooks and cron.

**Budget.** Target 1 round, cap 3 (superpowers full tier).

## Findings

Round 1 pool: 29 claims, 4 ESTABLISHED, 20 PROVISIONAL, 5 CONTRADICTED, 0 SOURCE-ROT. Full grading in `2026-09-16-lit-capture-research-log.md`; raw pool in `2026-09-16-lit-capture-merged-round1.json`.

Load-bearing findings so far (with distinct source counts):

1. **Auth model changed (Feb 2026): the mailto polite pool is dead.** Official deprecations page: "The mailto parameter is ignored." API key required from 2026-02-13 (pyalex README concurs); over-budget or >100 req/s returns 429 with exponential-backoff guidance. Keyless budget is tiny (~100 credits/day framing); list+filter requests cost credits, single-entity gets are free. (1 primary + 1 secondary)
2. **DOI lookup forms verified by live probes from two lenses:** `/works/doi:10.1038/nature12373` and `/works/https://doi.org/10.7717/peerj.4375` both resolve and return full work objects. (2 primary probes)
3. **Citing-works filter verified by live probes from two lenses:** `filter=cites:W2741809807` returns results (meta count 1253 observed). (2 primary probes)
4. **Abstract reality:** `abstract_inverted_index` is the only abstract form (plaintext withheld for legal reasons); it is null on a large fraction of works (~45-60% coverage depending on year) and can carry trailing non-abstract junk. Reconstruction = place each word at its index positions, join. (1 primary + 1 secondary, multiple pages)
5. **referenced_works is lossy, not capped:** shorter than the printed reference list (unknown targets dropped, non-DOI refs fail match). Graph must be documented as biased, not authoritative. (1 primary)
6. **Field naming:** `display_name` and `title` are the same value; `topics` supersedes deprecated `concepts`; `host_venue`/`grants`/`has_ngrams` now hard-error (removed fields). `select=` accepts root-level fields only. (1 primary, help.openalex.org attributes + deprecations + selecting-fields pages)
7. **Merges:** duplicate works 301 to canonical; clients must follow redirects. (1 primary)
8. **Paging:** basic paging hard-stops at 10,000 results; cursor paging goes deeper; bulk full-dataset crawls officially discouraged (irrelevant at 500-work scale). (1 primary)
9. **License:** official help page states the full release is CC0 with no personal-use carve-out; but reconstructed abstract text carries legal caveats beyond bare CC0 metadata (plaintext is withheld upstream for that reason). (1 primary + 1 secondary)

## Synthesis

Final per-criterion status after Round 2 (grading in the round log):

- **SC1 (DOI + arXiv lookup): PROVISIONAL, fallbacks named.** DOI singleton forms (`/works/doi:10.xxx`, `/works/https://doi.org/...`) each carry one live probe success plus official-doc corroboration that DOI is the canonical external ID; the arXiv contradiction is RESOLVED: the official work-object attributes page (fetched independently twice in Round 2) lists no `arxiv` key in `ids`, so the Round 1 `ids.arxiv` probe claim is superseded. arXiv-only papers resolve via `title.search` (relevance-ranked, so results must be verified against authors/year client-side) or, better, via a user-supplied DOI. `lit_fetch.py --check` verifies the DOI forms live on first run, closing the probe-count gap at runtime.
- **SC2 (batch + paging): PROVISIONAL on cursor mechanics only, fallback named.** Batch retrieval is ESTABLISHED: pipe-OR filters take up to 100 values with `per-page=100`, and ~4KB URL-length caution documented. Cursor paging (`cursor=*`, `meta.next_cursor`, 10,000 basic-paging stop) rests on one probe success + one doc page; fallback is the standard next-cursor loop, runtime-checked by `--check`.
- **SC3 (cites filter): ESTABLISHED** (two independent live probes).
- **SC4 (rate limits/auth/budget): ESTABLISHED.** mailto dead (deprecations page, 2026-08-12); key required from 2026-02-13; 429 fires on daily budget exhaustion or >100 req/s; response exposes X-RateLimit-Limit/Remaining/Credits-Used/Reset, no Retry-After; budgets $1/day with free key, $0.10/day keyless, reset midnight UTC; singleton GETs free, list+filter $0.10/1k, search $1/1k.
- **SC5 (abstract handling): ESTABLISHED.** Only `abstract_inverted_index` exists (plaintext withheld upstream for legal reasons); it is null on ~40-55% of works and can carry trailing non-abstract junk; reconstruction is the standard position-based join. The spec treats abstracts as optional field, never load-bearing.
- **SC6 (field names): ESTABLISHED.** `id`, `doi`, `display_name` (= `title`), `publication_date`/`publication_year`, `authorships`, `primary_location`, `open_access`, `referenced_works`, `cited_by_count`, `topics` (supersedes `concepts`); removed fields (`host_venue`, `grants`, `has_ngrams`) hard-error; `select=` accepts root-level fields only. Works merge with 301 to canonical IDs; client follows redirects.
- **SC7 (license): ESTABLISHED.** CC0 with no personal-use carve-out (help center how-its-built + official docs repo license.md); sole stated exception is the MAG snapshot (ODC-BY). OpenAlex recommends care on reconstructed abstracts since plaintext is withheld upstream for legal reasons: local reconstruction for personal corpus use is fine; public pack redistribution of reconstructed abstracts is the named risk surface for the future pack-export feature (out of v1 scope).

Undated sources on decision-bearing claims (DOI forms, cites filter, fields, rate limits) were probed or fetched live on 2026-09-16 (retrieved_at on every claim in the round log).

## Sources

| URL | Class | Note |
|---|---|---|
| https://help.openalex.org/api/deprecations/ | primary | mailto ignored; removed fields hard-error (2026-08-12) |
| https://help.openalex.org/api/authentication/ | primary | key required 2026-02-13; 100 req/s; dual 429 triggers |
| https://help.openalex.org/access/example-costs/ | primary | singleton free; list $0.10/1k; search $1/1k; $1/$0.10 daily |
| https://help.openalex.org/access/pricing/ | primary | free daily budget, UTC reset |
| https://help.openalex.org/api/errors/ | primary | 429 semantics; X-RateLimit headers; 301 merges |
| https://help.openalex.org/api/filtering/ | primary | pipe-OR 100-value cap; per_page=100 |
| https://help.openalex.org/api/searching/ | primary | title.search relevance ranking; 4KB URL caution |
| https://help.openalex.org/api/selecting-fields/ | primary | select= root-level only |
| https://help.openalex.org/api/paging/ | primary | cursor vs basic; 10k stop; no bulk crawls |
| https://help.openalex.org/api/get-single-entities/ | primary | canonical external IDs; DOI canonical for works |
| https://help.openalex.org/data/works/attributes/ | primary | ids keys; abstracts inverted + coverage; display_name=title; topics>concepts |
| https://help.openalex.org/data/works/citations/ | primary | referenced_works lossy vs PDF reference lists |
| https://help.openalex.org/data/indexes/ | primary | indexed_in:arxiv filter |
| https://help.openalex.org/data/how-its-built | primary | CC0, no carve-outs |
| https://raw.githubusercontent.com/ourresearch/openalex-docs/main/license.md | primary | CC0 statement; MAG snapshot ODC-BY exception |
| https://raw.githubusercontent.com/J535D165/pyalex/master/README.md | secondary | key-required date corroboration; plaintext-abstract caveat |
| https://github.com/J535D165/pyalex/issues/100 | secondary | prior-art 429 handling gap |
| https://api.openalex.org/works/doi:10.1038/nature12373 | primary | live probe: doi: singleton form, abstract null case |
| https://api.openalex.org/works/https://doi.org/10.7717/peerj.4375 | primary | live probe: full-DOI-URL singleton form |
| https://api.openalex.org/works?filter=cites:W2741809807 | primary | live probe x2 lenses: cites filter |
| https://api.openalex.org/works?filter=ids.openalex:W2741809807 | primary | live probe: ID filter form |
| https://api.openalex.org/works?filter=publication_year:2020-2023&per-page=200&cursor=* | primary | live probe: paging forms |
