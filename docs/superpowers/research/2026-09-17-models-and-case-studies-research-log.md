# Research log: models-and-case-studies

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| SysML-v2-Release ships official sysml/ and kerml/ example models | R1 | R1 | ESTABLISHED | scout+digger primary same URL; parent gh api confirms live |
| SysML-v2-Release already listed under Official Implementations; re-list is cross-section duplicate | R1 | R1 | ESTABLISHED | README Official Implementations + Release description of sample models |
| Nine baseline Example Models entries are real model packs with .sysml | R1 | R1 | ESTABLISHED | digger primary repo pages + existing list URLs |
| MBSE4U/PLEML is MBPLE SysML v2 example models (drone product line .sysml) | R1 | R1 | ESTABLISHED | scout primary + parent gh api tree (Examples/*.sysml, PLEML.sysml); stars 9, pushed 2026-06-14, not archived |
| MBSE4U/goodSysMLv2 has no .sysml model files; reject as model entry | R1 | R1 | PROVISIONAL | single scout; parent did not re-tree |
| MBSE4U/SysMLv2JupyterBook is tutorials not model pack; reject | R1 | R1 | PROVISIONAL | single scout |
| sysml.org lists no extra model-repo directory | R1 | R1 | PROVISIONAL | digger only; skeptic fetch failed same host |
| Case studies subhead would be thin (Apollo sparse; most are learning packs) | R1 | R1 | PROVISIONAL | skeptic reading of nine blurbs |
| doug-rosenberg and Open-MBEE structured-use-cases are both non-fork, same description text | R1 | R1 | ESTABLISHED | parent gh api: fork=false both; distinct pushed_at and tip commits; b-13 still open |
| Upstream awesome bar: no unmaintained/archived/undocumented | R1 | R1 | PROVISIONAL | runbook secondary |
| mycr0ft/awesome-sysml is v1; false-positive mine | R1 | R1 | PROVISIONAL | runbook secondary |
| Broad guessed model-repo names mostly 404 | R1 | R1 | PROVISIONAL | parent gh api probe list |

## Round 1 Summary

| Claim | Lenses | Grade | Action |
|-------|--------|-------|--------|
| Release has samples but already listed Official | scout, digger, skeptic, parent gh | EST | Do not re-add under Models |
| Baseline nine are real model packs | digger | EST | Keep under renamed section |
| PLEML net-new candidate | scout + parent gh | EST | Add if meets contributing |
| goodSysML / Jupyter reject | scout | PROV | Do not add |
| Case-studies H3 premature | skeptic | PROV | Single H2 only |
| structured-use-cases dual rows | digger, skeptic, parent gh | EST identity facts; b-13 open | Keep both; do not resolve identity this pass |
| sysml.org empty of packs | digger | PROV | No OMG dump |

Fixes applied: 0 (parent gh api filled PLEML + fork facts after rcl-triage spawn failed)
Coverage: 5/5 criteria met for decision support
Validation: PASS with named provisionals

## Converged: Round 1

Track 3: diminishing-return halt. Predicate: brief-covered.
Every success criterion has a usable claim. Decision-bearing add/reject calls are ESTABLISHED (Release no-relist, baseline keep, PLEML add). Remaining provisionals are rejects and thin-subhead guidance. Further web rounds blocked by earlier WebFetch failures and empty search API; parent gh filled the gap. `rcl-triage` spawn failed (`model-not-found` GLM-5.2); parent wrote this log.
Total rounds: 1  |  Total fixes: 0
Document is ready.
