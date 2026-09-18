# ARL triage log: 2026-09-16-companion-docs-site

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| Lychee mitigation claim false (L110) | R1 | R1 | Genuine | Backlog b-17 records lychee exits 2 with no operands, so the claimed weekly crawl checks nothing |
| AC2/verification coverage incomplete (L121) | R1 | R1 | Genuine | Hero, What-it-is, Repository links, footer, and nav anchor targets are unchecked by the verification section |
| Relative-link grep too narrow (L97) | R1 | R1 | Advisory-skipped | Cheap widening: assert all repo-file hrefs absolute so ./ variants cannot evade |
| Goal 1 "Nothing else" vs AC1 carve-out (L14) | R1 | R1 | Advisory-skipped | One-line consistency fix: repeat the docs/superpowers carve-out in Goal 1 |
| Maintenance link slug unstated (L63) | R1 | R1 | Advisory-skipped | Write the full blob URL ending contributing.md#maintenance |
| JSON-LD url vs og:url/canonical mixed identity (L74) | R1 | R1 | Advisory-skipped | State rationale or unify: JSON-LD url is the repo home, canonical is the site |
| Repository-links URLs unspelled (L64) | R1 | R1 | Advisory-skipped | List the five URLs: README blob, contributing blob, repo root, issues, docs tree |
| Google Fonts link unpinned (L39-80) | R1 | R1 | Advisory-skipped | Add href, weights, and placement to the head inventory |
| site.css carry-over wording contradiction (L77-82) | R1 | R1 | Advisory-skipped | Sibling is 81 lines with table.data and table rules are new; fix wording to tokens/base copy only |
| Badge img src unstated (L47) | R1 | R1 | Advisory-skipped | Pin src to https://awesome.re/badge.svg |
| Viewport and twitter card fields unpinned (L69-73) | R1 | R1 | Advisory-skipped | Pin viewport content string and state twitter:title/description present |
| Category one-liners overclaim README content (L50-51) | R1 | R1 | Advisory-skipped | "tracked change proposals" absent and "vendor implementations" should be reference implementations |
| Dark styling and no-JS unchecked (L94-100) | R1 | R1 | Advisory-skipped | Add CSS-var presence check and no-script-tag grep to verification |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Lychee mitigation false (b-17: checks nothing until fixed) | auditor | MAJ | Genuine | Fixed (Round 1): Limitations + Risks state manual anchor checks until b-17 |
| AC2/verification omit hero/what/links/footer/nav checks | auditor | MAJ | Genuine | Fixed (Round 1): AC2 enumerates all sections; verification step 2 checks all anchors |
| Category one-liners overclaim README content | auditor | ADV | Genuine | Fixed as cheap advisory: two one-liners reworded (Round 1) |
| Table CSS carried-vs-new contradiction | auditor, new_hire | ADV | Genuine | Fixed as cheap advisory (Round 1) |
| Relative-link grep too narrow | saboteur | ADV | Genuine | Fixed as cheap advisory: anchored pattern (Round 1) |
| Google Fonts link unpinned; viewport/twitter exactness | new_hire | ADV | Genuine | Fixed as cheap advisory: head inventory extended (Round 1) |
| site.css carry-over wording (60 lines false) | new_hire, auditor | ADV | Genuine | Fixed as cheap advisory (Round 1) |
| Maintenance + repo-links URLs unstated | saboteur, new_hire | ADV | Genuine | Fixed as cheap advisory: full URLs written (Round 1) |
| Badge img src; JSON-LD url rationale; Goal 1 carve-out; dark/no-JS checks | saboteur, new_hire, auditor | ADV | Genuine | Fixed as cheap advisories (Round 1) |

Fixes applied: 2 genuine MAJOR + 9 advisory items
Inflation rate: 0% (0 findings triaged FP/Design)
Validation: SKIP (build-time checks run at execute)

## Round 3 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Round-1 fixed locs (re-confirmed) | saboteur, new_hire, auditor | - | Confirmed | Resolved (Round 2) |
| Duplicate step number 7 | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: renumbered to 8 (Round 3) |
| id="top" placement undefined; five-vs-six count | saboteur | ADV | Advisory-skipped | Fixed as cheap advisory: id on hero, six anchors (Round 3) |

Fixes applied: 2 (advisories)
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: SKIP (build-time checks run at execute)

## Converged: Round 3

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 3  |  Total fixes: 9
Document is ready.
