# Context: github-notice-surface (P3)

## Context brief

- **Primary question**: What is the repo's current discoverability state after P1/P2/P4 landed, and what exactly must P3 produce — the discoverability checklist verification plus the awesome-re submission-readiness runbook (requirements, current gate status, and the maintainer's submission steps)?
- **Success criteria**:
  - SC1: Live repo metadata state (visibility, description, topics, homepageUrl incl. b-18 pending state, workflow states) — the checklist's verification baseline.
  - SC2: contributing.md and README current Contributing text (P4 landed the Maintenance section) — where the submission-readiness note belongs.
  - SC3: The awesome-re submission requirements as established by the research round (30-day age gate: list created 2026-09-15, earliest submission ~2026-10-15; PR intake currently disabled; AI-curation sensitivity) — carried into the runbook.
  - SC4: Where the runbook lives (contributing.md is contributor-facing; a maintainer-facing submission runbook may belong elsewhere — sibling precedent?) and P3's file scope.
- **Out of scope**: workflow changes; entry content; site changes (P2 done); spam tactics.
- **Budget**: 1 round; cap 3.
- **Workspace baseline**: HEAD b562394 + P4 landed... verify actual HEAD (P4 commit 467126a + fix 4c68451).

## Findings

Full graded claim table in the round log. 8 merged families, verdict CONTEXT_COMPLETE, 0 conflicted/stale. Key facts:

- Live baseline (SC1, parent gh check): isPrivate **false**; description and the five topics intact; **homepageUrl still empty** (b-18 pending the push — Pages, homepage, and live-200 are NOT done); workflows Links/Lint/Freshness report all active; **7 unpushed commits** (1747fa6..de549d9); docs/ holds index.html, site.css, superpowers/.
- contributing.md (SC2): 57 lines, ends with `## Maintenance` (P4); PR template at .github/ with entry + lint checklist; README Contributing at 126-128.
- Submission gates (SC3, ESTABLISHED, carried from the research companion): 30-day list-age minimum (list created 2026-09-15 → earliest submission ~2026-10-15); upstream PR intake **temporarily disabled** with ~90 open backlog; **AI-generated lists hard-rejected** (maintainer must claim personal curation); effort/curation bars (best-of, no unmaintained items, tight scope).
- Placement (SC4): no MAINTAINERS.md exists; maintainer process lives in the docs/superpowers/ tree (specs/plans/research) — the submission runbook belongs there, not in contributor-facing contributing.md.
- Checklist reality (skeptic constraints): the discoverability checklist must mark homepage/Pages as pending (b-18), separate badge chrome from sindresorhus listing, note the v1 sibling (mycr0ft/awesome-sysml) without overclaiming uniqueness, and state that the list's value does not depend on sindresorhus acceptance (MBSE community hubs are the alternative path).

## Synthesis

All four success criteria met (4/4); verdict CONTEXT_COMPLETE. SC1 settled by the parent's live gh check this round (not lens prose); SC2/SC4 corroborated across lenses; SC3 carried ESTABLISHED from the research round. Single-source items: placement precedent (no sibling runbook exists — this repo creates its own), named in Synthesis. Design constraints locked for the spec: P3 delivers (1) a verified discoverability checklist with honest pending markers (homepage = pending b-18), and (2) a maintainer-facing submission-readiness runbook in the docs/superpowers/ process tree containing the ESTABLISHED requirements, the three gates with their dates/status, the exact future PR steps (title, target file, checklist items), and the curation-claim note — explicitly NOT a submit-now instruction. No workflow changes; contributing.md and README untouched unless the spec argues a one-line pointer (it should not — the runbook is maintainer-facing). Open questions: none.

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| live gh repo view (parent, this round) | config | parent (SC1 baseline: public, topics, homepageUrl empty, workflows active) |
| git log --oneline -8 | config | parent (7 unpushed commits) |
| docs/ tree | config | parent (index.html, site.css, superpowers/) |
| contributing.md:42 | doc | cartographer, prospector, skeptic (Maintenance section; no submission text) |
| .github/PULL_REQUEST_TEMPLATE.md:1 | doc | cartographer (contributor checklist) |
| README.md:126-128 | doc | prosp, skeptic (Contributing one-liner) |
| docs/superpowers/research/2026-09-16-github-notice-surface-research.md:21-29 | doc | cart, prosp, skeptic (ESTABLISHED gates) |
| docs/superpowers/packages/2026-09-15-awesome-sysml-v2-packages.md:149,175-179 | doc | skeptic (P2 done w/ b-18 pending; P3 wording) |
| docs/superpowers/backlog.md:24 | doc | skeptic (b-18 open) |
| docs/index.html:9,54 | code | skeptic (canonical/badge forward references) |
| README.md:1 | doc | skeptic (badge chrome) |
| docs/superpowers tree inventory | doc | prospector (runbook placement; no MAINTAINERS.md) |
