# Triage log: 2026-09-16-lit-capture

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 W-id identity normalization undefined (URL vs bare W-id, 301 edge remap) | R1 | R1 | Genuine | Schema keeps OpenAlex `id` URL while filenames and edges use bare W-ids; merge remap never specified. Phantom nodes follow. |
| C2 Verb mutual exclusion contradicts --arxiv requiring --title | R1 | R1 | Genuine | L108 says one flag per invocation; L116 requires --title with --arxiv. Rule as written cannot be encoded. |
| C3 Duplicate-capture semantics for singleton verbs and inbox promotion undefined | R1 | R1 | Genuine | Batch verb skips existing; singleton and --inbox behavior on present records unstated, so seed and counts flip silently. |
| C4 Corpus known-ID set membership and DOI normalization undefined | R1 | R1 | Genuine | L129 relies on a set whose contents are never enumerated; first implementer cannot write the dedupe function. |
| C5 Inbox ref grammar sketch; arxiv: entries unresolvable | R1 | R1 | Genuine | arXiv path requires --title but the entry schema at L167 carries no title field, so those entries can never resolve. |
| M1 Findings filename inconsistent between corpus layout and skill | R1 | R1 | Genuine | L86 says findings/<slug>.md, L169 says findings/<year>-<slug>.md; pick one. |
| M2 API host and response envelope shapes unspecified | R1 | R1 | Genuine | Paths given hostless; singleton object vs list {results} shape unstated; implementer must guess parse logic. |
| M3 --inbox wholesale rewrite loses concurrent appends | R1 | R1 | FP | Inflation-FP: v1 is a single sequential agent workflow; no concurrent writer exists, and no failure path was shown. |
| M4 Exit 2 on missing corpus dir contradicts greenfield first use | R1 | R1 | Genuine | First capture into a fresh repo would exit 2 unless the write verb auto-creates the corpus dir; acceptance test implies it must. |
| A1 Abstract junk rule undefined | R1 | R1 | Advisory-skipped | Clarity only; test names the trailing-junk case, implementation can follow it. |
| A2 Batch missing-ID accounting | R1 | R1 | Advisory-skipped | Summary block already reports failed with reason; counting detail is clarity. |
| A3 Unparsable inbox refs | R1 | R1 | Advisory-skipped | Failures stay queued by the general rule; enough to implement. |
| A4 --status last-synced and --check exit codes | R1 | R1 | Advisory-skipped | Minor contract detail; exit-code table covers usage. |
| A5 --author/--year missing from common flags | R1 | R1 | Advisory-skipped | Table row shows them inline; cheap to clarify during implementation. |
| A6 fold() collision risk note | R1 | R1 | Advisory-skipped | Verification also checks surname and year when given; acceptable v1 risk. |
| A7 Keyless-warning multi-ID dead category | R1 | R1 | Advisory-skipped | Warning text is cosmetic; no failure path. |
| A8 Inbox rewrite ordering and idempotence | R1 | R1 | Advisory-skipped | Failures-stay-queued rule fixes content; ordering is minor. |
| A9 select= field list not enumerated | R1 | R1 | Advisory-skipped | Schema field names are listed; select list follows mechanically. |
| A10 150-ID acceptance fresh-dir pinning | R1 | R1 | Advisory-skipped | Acceptance detail the plan can pin. |
| A11 prose_check mechanism for embedded template | R1 | R1 | Advisory-skipped | Gate note at L197 already covers flag false positives. |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| W-id identity normalization + alias remap | saboteur, new_hire, auditor | CRIT | Genuine | Fixed (Round 1) |
| Verb exclusivity vs --arxiv --title | saboteur, new_hire | CRIT | Genuine | Fixed (Round 1) |
| Singleton/inbox skip-if-exists undefined | saboteur, auditor | CRIT | Genuine | Fixed (Round 1) |
| Inbox dedupe known-ID set undefined | new_hire, auditor | CRIT | Genuine | Fixed (Round 1) |
| Inbox ref grammar + unresolvable arxiv: form | new_hire, auditor | CRIT | Genuine | Fixed (Round 1) |
| Findings filename inconsistency | new_hire, auditor | MAJ | Genuine | Fixed (Round 1) |
| API host + response envelope unspecified | new_hire | MAJ | Genuine | Fixed (Round 1) |
| --inbox wholesale rewrite concurrency | saboteur | MAJ | FP | Wontfix (single-user CLI; rewrite ordering + idempotence specified instead) (Round 1) |
| Exit-2 missing-dir vs greenfield first use | saboteur | MAJ | Genuine | Fixed (Round 1) |
| 11 advisories (junk rule, batch accounting, unparseable refs, status/check exits, author/year flags, fold collisions, multi-ID warning category, inbox ordering, select= list, fresh-dir pinning, prose mechanism) | mixed | ADV | Genuine (cheap) | Fixed (Round 1) |

Fixes applied: 8 genuine + 11 advisory cleanups
Inflation rate: 11% (1 FP of 9 CRITICAL+MAJOR)
Validation: SKIP (prose document; no script)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| 6 fix clusters (identity/aliases, verb grammar, skip-if-exists, dedupe keys, inbox grammar, network/write/acceptance cleanups) | saboteur, new_hire, auditor | CRIT+MAJ | Genuine (confirmed) | Resolved by this change (18/18 verdicts) |

Fixes applied: 0 new (confirmation round)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (prose document; no script)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 9
Document is ready.
