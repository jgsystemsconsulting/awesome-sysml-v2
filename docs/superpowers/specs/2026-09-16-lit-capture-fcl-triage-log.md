| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 spec:L20 key-mandate date and mailto-ignored conflated onto one primary | 2026-09-16 | 2026-09-16 | Genuine | mailto-ignored is on the deprecations page; the 2026-02-13 key date rests on the authentication page plus a secondary. Split the cites and soften "key is expected". |
| C2 spec:L43 pricing split and X-RateLimit-Credits-Used header names | 2026-09-16 | 2026-09-16 | FP | Spec wording matches the research synthesis SC4 (graded ESTABLISHED, quoted from the errors and example-costs pages) verbatim. A fresh fetch omitting a header name does not contradict a recorded primary quote. |
| C3 spec:L55-56 license cite bundles CC0 and abstract caveat under license.md | 2026-09-16 | 2026-09-16 | Advisory-skipped | Both facts are primary-verified in the research (license.md for CC0, attributes page for the caveat). Only the cite grouping is loose; no factual error. |
| C4 spec:L137 "Never read Retry-After (OpenAlex does not send it)" | 2026-09-16 | 2026-09-16 | Genuine | Live 429 observed with Retry-After: 39154. The spec overgeneralized "not documented" into "not sent". Honor the header when present. |
| M1 spec:L47 /works/https://doi.org/... resolves | 2026-09-16 | 2026-09-16 | FP | The research Sources table records a live probe of that exact URL succeeding on 2026-09-16. A documented primary probe stands even though the get-single-entities page shows no example. |
| M2 spec:L50-51 4 KB URL limit cited to filtering page | 2026-09-16 | 2026-09-16 | Genuine | The 4 KB caution lives on the searching page per the research Sources table; the filtering page covers the 100-value pipe-OR cap. One-line cite move. |
| M3 spec:L114 arXiv DOI alias GET /works/doi:10.48550/arXiv.<id> | 2026-09-16 | 2026-09-16 | Genuine | The alias appears in no source and no research claim, and a live probe returned 404. The --arxiv verb depends on it, so it is load-bearing. Drop the alias or replace with title verify plus known DOI. |
| A1 spec:L52 "null on roughly 40 to 55 percent" | 2026-09-16 | 2026-09-16 | FP | Matches the research synthesis SC5 (ESTABLISHED: null on roughly 40 to 55 percent of works). The finding's per-year framing does not contradict the graded range. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| L20 key-mandate date + mailto cite conflation | skeptic, source, correspondent | CRIT | Genuine | Fixed (Round 1) |
| L43 pricing split + Credits-Used header name | source, correspondent | CRIT | FP | Wontfix (matches recorded primary quotes) (Round 1) |
| L55-56 license cite grouping | skeptic, source | CRIT | Advisory-skipped | Skipped (facts primary-verified; grouping only) (Round 1) |
| L137 Retry-After never-read claim | skeptic | CRIT | Genuine | Fixed (Round 1) |
| L47 https-DOI-URL form resolves | source | MAJ | FP | Wontfix (live probe recorded in research Sources) (Round 1) |
| L50-51 4 KB limit cite placement | skeptic | MAJ | Genuine | Fixed (Round 1) |
| L114 arXiv DOI alias verb | skeptic | MAJ | Genuine | Fixed (Round 1) |
| L52 abstract null-rate framing | skeptic | ADV | FP | Skipped (matches research synthesis) (Round 1) |

Fixes applied: 4
Inflation rate: 50% (4 of 8 CRITICAL+MAJOR triaged FP or Advisory-skipped)
Validation: SKIP (prose document; no script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| L19-20/L43 auth date + cite split | skeptic, source, correspondent | CRIT | Genuine (confirmed) | Resolved by this change |
| L50-57 batch cite placement | skeptic, source, correspondent | MAJ | Genuine (confirmed) | Resolved by this change |
| L137 Retry-After honor-when-present | skeptic, source, correspondent | CRIT | Genuine (confirmed) | Resolved by this change |
| L114 arXiv alias removal cluster | skeptic, source, correspondent | MAJ | Genuine (confirmed after L177 remnant fix) | Resolved by this change |

Fixes applied: 5 (4 from Round 1 carried, plus L177 five-to-four remnant)
Inflation rate: n/a (confirmation wave; no new findings)
Validation: SKIP (prose document; no script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 5
Document is ready.
