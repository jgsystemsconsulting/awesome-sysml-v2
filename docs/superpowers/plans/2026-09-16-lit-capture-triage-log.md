| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| C1 fake_http replaces real http_get so retry/budget tests run against the fake | R1 | R1 | Genuine | test_retry_then_success asserts two attempts but fake get returns once; real retry/backoff/BudgetExhausted code never executes |
| C2 test_url_builders asserts raw SELECT_FIELDS suffix but urlencode encodes commas | R1 | R1 | Genuine | with_params uses urlencode; commas become %2C so endswith(SELECT_FIELDS) always fails against correct code |
| C3 test_status_never_before_index never writes edges before asserting edges=2 | R1 | R1 | Genuine | only write_record runs; edges.jsonl absent so verb_status prints 0/0 and the assertion fails |
| C4 tasks append implementation before the run-to-fail step expects AttributeErrors | R1 | R1 | Genuine | Step 4 expects FAIL on AttributeError after Step 1 already added the implementation; expected-output lines make red runs impossible |
| C5 boundary-ID recipe uses p.split('/') which breaks on Windows glob backslashes | R1 | R1 | Genuine | Windows glob returns backslash-joined paths; split('/') yields wrong stems and the recipe lists non-boundary endpoints |
| M1 malformed inbox loop never sets last_error but test asserts it | R1 | R1 | Genuine | verb_inbox malformed branch pops _ref and run.fail only; remaining[0]["last_error"] raises KeyError in test_inbox_triage_flow |
| M2 batch fetch of a 301-merged W-id never learns the alias or writes the canonical record | R1 | R1 | Genuine | by_id keys on response ids; merged id reported 404, no alias saved, re-runs fail identically against the spec's alias rule |
| M3 entry_key maps titleless arxiv entries to key "title:" so dedupe drops them silently | R1 | R1 | Genuine | arxiv kind falls to the title branch; all titleless entries collide on "title:" and the designed failure never fires |
| M4 verb_inbox except handler sets last_error but never calls run.fail | R1 | R1 | Genuine | hard inbox failures leave run.failed at 0 so main exits 0 on real errors |
| M5 verify step cmps $REPO/skills/lit-capture/lit_fetch.py which is never created | R1 | R1 | Genuine | Step 2 copies from $REPO/lit_fetch.py at repo root; the cmp path never exists so the check fails |
| M6 index regenerates only when a record was written; edge-only changes leave it stale | R1 | R1 | Genuine | promote_payload regenerates only if wrote but write_edges still unions edges on skip; spec requires regen after any successful write |
| M7 Task 4 Consumes lists load_aliases from Tasks 1-2 but it is produced in Task 4 | R1 | R1 | Genuine | load_aliases appears in Task 4 Produces; the Consumes credit misleads executors |
| A1 BudgetExhausted path sets last_error then raises before atomic_write persists it | R1 | R1 | Advisory-skipped | dead store in the abort path; cheap fix is dropping the assignment or a finally rewrite |
| A2 Tasks 4-7 extend CHECKS by prose only | R1 | R1 | Advisory-skipped | prose lists exact names, order, and count; full paste adds bulk without blocking |
| A3 "last-synced: 2" assertion matches only a leading year digit | R1 | R1 | Advisory-skipped | weak but passes; tighten with a full ISO match if touched |
| A4 expected status text "boundary=<same minus 1>" is wrong; boundary equals edge count | R1 | R1 | Advisory-skipped | with N refs, edges=N and boundary=N; one-line text fix |
| A5 verb_title doc claims True only when written but returns True on skip-if-exists | R1 | R1 | Advisory-skipped | reword to "present or written"; no behavior change |
| A6 interface text says BudgetExhausted propagates after queuing; rewrite never runs | R1 | R1 | Advisory-skipped | reword to "propagates without rewriting; original queue intact" |
| A7 coverage map omits the spec's Corpus layout section | R1 | R1 | Advisory-skipped | add one row mapping to Tasks 4 and 8 |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| C1 fake seam: tests replaced http_get, retry/budget never ran | saboteur, new_hire | CRIT | Genuine | Fixed: fake_urlopen under real http_get (Task 3 x4, Task 6 budget test) |
| C2 urlencode %2C vs raw SELECT_FIELDS assert | saboteur, new_hire | CRIT | Genuine | Fixed: parse_qs round-trip |
| C3 status test asserted edges without writing them | saboteur, new_hire | CRIT | Genuine | Fixed: write_edges before verb_status |
| C4 red-run steps expected impossible FAILs | saboteur, new_hire | CRIT | Genuine | Fixed (deviation): reworded expected output to truthful PASS + Global Constraints order note, instead of restructuring every task's step order; minimum change, same defect closed |
| C5 boundary recipe split('/') breaks on Windows | saboteur, auditor | CRIT | Genuine | Fixed: pathlib Path stem |
| M1 malformed inbox entry never set last_error | saboteur | MAJ | Genuine | Fixed |
| M2 batch 301-merged id false-404, alias never learned | saboteur | MAJ | Genuine | Fixed: resolve_alias match + alias learning + merge note |
| M3 titleless arxiv entries collided on "title:" key | saboteur | MAJ | Genuine | Fixed: distinct arxiv:<value> key |
| M4 inbox hard errors skipped run.fail (exit 0) | new_hire | MAJ | Genuine | Fixed |
| M5 Task 9 cmp used wrong script path | new_hire | MAJ | Genuine | Fixed |
| M6 index regen skipped edge-only changes | auditor | MAJ | Genuine | Fixed: promote_payload regenerates on edges change |
| M7 Task 4 Consumes mis-attributed load_aliases | new_hire, auditor | MAJ | Genuine | Fixed |
| A1 budget-abort mutated entry then raised before rewrite | saboteur | ADV | Genuine | Fixed: bare re-raise, queue untouched |
| A2 CHECKS arrays described not pasted | new_hire | ADV | Advisory-skipped | Skipped (counts + names stated; paste would bloat listings) |
| A3 weak timestamp assert | new_hire | ADV | Genuine | Fixed ("last-synced: 20") |
| A4 boundary=<same minus 1> wrong | auditor | ADV | Genuine | Fixed (same count wording) |
| A5 verb_title docstring return semantics | auditor | ADV | Genuine | Fixed |
| A6 verb_inbox budget wording | auditor | ADV | Genuine | Fixed (propagates without rewriting) |
| A7 coverage map missing Corpus layout row | auditor | ADV | Genuine | Fixed |

Fixes applied: 12 CRITICAL+MAJOR + 6 advisories (A2 skipped)
Inflation rate: 0% (0 of 12 CRITICAL+MAJOR triaged FP)
Validation: SKIP (plan document; listings executed at execute)

## Round 2 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| 10 fix clusters (fake_urlopen seam, budget-abort flow, parse_qs assert, status test counts, red-run rewording, pathlib recipe, verb_inbox error paths, verb_ids alias learning, promote_payload regen trigger, Consumes/cmp/acceptance/docstring/assert/coverage cleanups) | saboteur, new_hire, auditor | CRIT+MAJ | Genuine (confirmed) | Resolved by this change (30/30 verdicts) |

Fixes applied: 0 new (confirmation round)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (plan document; listings executed at execute)

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 18
Document is ready.
