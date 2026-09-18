# Spec: Rename Example Models to Models and Case Studies, expand the curated list

Date: 2026-09-17
Status: authored (Superpowers step 1)
Gates: context COMPLETE, research brief-covered (see Research below)
Implementation: to follow in this pipeline; this spec is the edit contract.

## Problem

The README section named Example Models (TOC line 13, H2 line 76) undersells what the list now carries. Apollo-class domain models such as airbus/apollo-11-sysml-v2 sit in a bucket labeled as examples, which reads as tutorial material. Researchers looking for real SysML v2 model packs scan past it. The companion site (docs/index.html) hardcodes the same label and the `#example-models` anchor, so a README-only rename would leave the live site pointing at a dead anchor. docs/ sits outside lint.yml and lychee scopes, so CI would not catch the drift.

The section is also one net-new entry away from being a genuinely useful research list. MBSE4U/PLEML (MBPLE example models, ESTABLISHED by research) belongs in it. Nothing else found by research clears the bar this pass.

## Goal

One curated bucket, renamed Models and Case Studies, same TOC slot, holding the existing nine entries plus MBSE4U/PLEML. Companion site updated in the same change. Descriptor copy that says "example models" updated to match. No Projects section, no subhead split, no bulk additions.

## Approach

Rename in place across four coordinated surfaces in one change: (1) README.md tagline, TOC, H2, and one new entry; (2) docs/index.html category row plus the six descriptor strings listed under Exact edits; (3) CHANGELOG.md Unreleased bullets; (4) the awesome-submission runbook differentiation sentence. Substitution rule: only replace the lowercase token "example models" inside the Exact edits table cells for README tagline, docs/index.html descriptors, and the runbook differentiation sentence. Do not run a whole-file global replace on README.md entry lines. Entry description lines stay byte-identical except for the new PLEML insert. Those lines may use "Example models" or "example models" as factual repo content; do not rewrite them to satisfy a grep count.

## In scope

- README.md: tagline (line 3), TOC line (13), H2 (76), one new entry inserted in lines 78-86.
- docs/index.html: category row (line 83), meta description, og:description, twitter:description, JSON-LD description (lines 8, 17, 23, 33), hero paragraph (60), what-it-is paragraph (66).
- CHANGELOG.md: two Unreleased bullets (Added, Changed).
- docs/superpowers/runbooks/awesome-submission.md: differentiation sentence (line 53).

## Out of scope

- A top-level Projects section or any new README category.
- H3 subheads (Case studies / Learning packs) inside the renamed section. Research found the case-study side too thin to carry its own sort bucket; revisit when more domain case studies exist.
- Re-listing Systems-Modeling/SysML-v2-Release here. It stays under Official Implementations only; samples inside it are a cross-section duplicate.
- Moving Flashlight out of Migrating from SysML v1.
- Editing contributing.md. It names no section titles; its criteria and format bind new entries unchanged.
- Editing historical gate docs: the 2026-09-16 specs and plans, context and research logs, and this change's own context/research docs.
- Changing the GitHub repo description via gh api. It still reads "A curated list of OMG SysML v2 tools, example models, and learning resources" server-side; that string is not a file in this repo and is an optional follow-up after this change ships.
- Backlog edits. b-09 (README structural rewrite) and b-13 (structured-use-cases identity) stay as they are.
- Automated GitHub crawling or bulk model-pack additions.

## Exact edits

Line numbers are pre-edit positions; match on the exact strings, not line numbers.

### README.md

| Loc | Before | After |
|-----|--------|-------|
| 3 | A curated list of OMG SysML v2 tools, example models, and learning resources. | A curated list of OMG SysML v2 tools, models and case studies, and learning resources. |
| 13 | `- [Example Models](#example-models)` | `- [Models and Case Studies](#models-and-case-studies)` |
| 76 | `## Example Models` | `## Models and Case Studies` |
| insert between neighbors | (none) | Insert the PLEML line immediately after the dont-panic-batmobile entry and immediately before the sysmod-sysmlv2 entry: `- [MBSE4U/PLEML](https://github.com/MBSE4U/PLEML) - MBPLE (model-based product line engineering) example models in SysML v2.` |

Anchor derivation: GitHub slugifies the heading to `models-and-case-studies` (lowercase, spaces to hyphens). Link text and slug change together in the same commit.

Sort check for the insert: case-insensitive by link text, `mbse4u/dont-panic-batmobile` < `mbse4u/pleml` < `mbse4u/sysmod-sysmlv2`. Key the insert on those two neighbor lines, not on a line number.

### docs/index.html

| Loc | Change |
|-----|--------|
| 8, 17, 23, 33 | In the shared description string, `tooling, example models, and learning material` becomes `tooling, models and case studies, and learning material`. Same replacement in all four spots (meta description, og:description, twitter:description, JSON-LD). |
| 60 | `libraries, example models, and learning material` becomes `libraries, models and case studies, and learning material`. |
| 66 | `validation tooling, example models, learning resources` becomes `validation tooling, models and case studies, learning resources`. |
| 83 | Label text `Example Models` becomes `Models and Case Studies`. Full href Before: `https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#example-models`. Full href After: `https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#models-and-case-studies`. Keep the absolute blob URL prefix; change only the fragment. Blurb `Working SysML v2 models to learn from and build on.` becomes `Working SysML v2 models and case studies to learn from and build on.` |

### CHANGELOG.md

Append to Unreleased, keeping Keep a Changelog section order:

- Added, after the existing three bullets: `- MBSE4U/PLEML SysML v2 model pack entry.`
- Changed, after the existing three bullets: `- Example Models section renamed to Models and Case Studies.`

### docs/superpowers/runbooks/awesome-submission.md

Line 53, inside the quoted differentiation sentence: `curates tools, example models, and learning resources` becomes `curates tools, models and case studies, and learning resources`. Nothing else in the runbook changes; line 10 records a historical step and stays.

## Normative requirements

1. The README H2 shall read exactly `## Models and Case Studies`, and the TOC line shall read exactly `- [Models and Case Studies](#models-and-case-studies)`. Both must change in the same commit.
2. The renamed section shall contain exactly ten entries: the nine existing lines byte-identical, plus the PLEML line exactly as specified above, in the position specified above.
3. Entries shall stay sorted alphabetically, case-insensitive, by link text, per contributing.md.
4. README must not gain a Projects section or any other new H2. The renamed section keeps its TOC slot between Validation and Analysis and Learning Resources.
5. No H3 headings may appear inside the renamed section in this change.
6. Systems-Modeling/SysML-v2-Release must not be listed under Models and Case Studies. `grep -n "SysML-v2-Release" README.md` shall show exactly one hit, under Official Implementations.
7. Both structured-use-cases entries (doug-rosenberg and Open-MBEE) shall remain. Provenance stays open as backlog item b-13.
8. The Flashlight starter model line shall stay under Migrating from SysML v1.
9. contributing.md must not be modified in this change.
10. The docs/index.html category row must be updated in the same change as the README rename: label, full absolute href (fragment only), and blurb as specified under Exact edits. Same-change sync is mandatory because no CI job covers docs/.
11. After edits, the lowercase phrase "example models" must not remain in the README tagline, section heading, TOC, or anywhere in docs/index.html. It may remain only inside entry descriptions that use that exact lowercase spelling, including the new PLEML line. Pre-edit baseline: SYSMOD (README) uses lowercase; Masterclass and Book-examples use capitalized "Example models". Do not rewrite the Masterclass or Book-examples lines.
12. The changelog bullets shall be added under the existing Added and Changed subsections of Unreleased with the exact text specified.
13. The runbook differentiation sentence shall be updated as specified under Exact edits (MUST).
14. Curation only. This change shall add no entries beyond MBSE4U/PLEML and shall introduce no automation for discovering model repos.
15. After all edits, `npx awesome-lint@2.3.0 README.md` and `npx markdownlint-cli2 "README.md" "contributing.md"` must pass from the repository root.

## Acceptance criteria

Each item is checkable from the repository root after implementation.

1. `grep -n "Example Models" README.md docs/index.html` returns zero lines, and `grep -n "#example-models" README.md docs/index.html` returns zero lines.
2. `grep -n "example models" docs/index.html` returns zero lines.
3. `grep -c "example models" README.md` returns exactly 2 (case-sensitive): the SYSMOD entry description and the PLEML entry description. Masterclass and Book-examples keep capitalized "Example models" and are not counted by that grep.
4. README line 3 reads: `A curated list of OMG SysML v2 tools, models and case studies, and learning resources.`
5. README TOC contains `- [Models and Case Studies](#models-and-case-studies)` in the position between the Validation and Analysis and Learning Resources TOC lines, and the H2 `## Models and Case Studies` appears exactly once.
6. The renamed section holds exactly 10 list entries; the PLEML line matches the exact string in Exact edits and sits directly between the dont-panic-batmobile and sysmod-sysmlv2 lines; the other nine lines are unchanged against the pre-edit diff.
7. `grep -n "SysML-v2-Release" README.md` returns exactly one line, inside Official Implementations.
8. Both structured-use-cases lines and the Flashlight line are present and unchanged.
9. README has no `## Projects` heading and no H3 between `## Models and Case Studies` and `## Learning Resources`.
10. docs/index.html category row uses the full absolute href `https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#models-and-case-studies`, label `Models and Case Studies`, and blurb `Working SysML v2 models and case studies to learn from and build on.`
11. CHANGELOG Unreleased Added contains the exact bullet `- MBSE4U/PLEML SysML v2 model pack entry.` and Changed contains the exact bullet `- Example Models section renamed to Models and Case Studies.`
12. `git diff origin/main -- contributing.md` (or the PR base if different) is empty.
13. The runbook line 53 sentence contains `curates tools, models and case studies, and learning resources`.
14. Both local lint commands from requirement 15 exit 0.
15. docs/index.html contains each of these exact post-edit substrings at least once: `tooling, models and case studies, and learning material`; `libraries, models and case studies, and learning material`; `validation tooling, models and case studies, learning resources`.

## Codebase context

From the context gate (docs/superpowers/context/2026-09-17-models-and-case-studies-context.md, CONTEXT_COMPLETE): the section is defined at README.md:13 (TOC) and README.md:76 (H2) with nine entries at 78-86, already alphabetical by link text. docs/index.html:83 is the one live-site surface that hardcodes the label and anchor. The companion-site spec (docs/superpowers/specs/2026-09-16-companion-docs-site.md:106) requires the category map to move in the same change as a README category rename, and notes docs/ escapes lint.yml and lychee scopes. contributing.md binds entry format and inclusion criteria (one line, alpha by link text, one factual sentence, no duplicates, active or foundational) but names no section titles, so the rename needs no contributing.md edit. Lint has no section-name allowlist. Backlog neighbors: b-09 (README structural rewrite, open; this change must not thrash it) and b-13 (structured-use-cases identity, needs-info; stays open). The PR template already checks correct-section placement and alphabetical order.

## Research

Gate: docs/superpowers/research/2026-09-17-models-and-case-studies-research.md (brief-covered).

- https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/docs/superpowers/research/2026-09-17-models-and-case-studies-research.md
- https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/docs/superpowers/context/2026-09-17-models-and-case-studies-context.md
- https://github.com/MBSE4U/PLEML (ESTABLISHED add: MBPLE examples, `PLEML.sysml` plus drone product-line `Examples/*.sysml`, pushed 2026-06-14, not archived)
- https://github.com/airbus/apollo-11-sysml-v2 (baseline Apollo-class entry kept under the renamed section)
- https://github.com/Systems-Modeling/SysML-v2-Release (reject for re-listing here; already under Official Implementations)

Research decisions locked into this spec: add PLEML only; keep all nine baseline entries; keep both structured-use-cases listings (b-13 open); no Case studies / Learning packs H3 split this pass; one H2, one alphabetical bucket.
