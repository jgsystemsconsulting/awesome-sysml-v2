# Research: github-notice-surface (P3)

## Research brief

- **Primary question**: What does submitting this list to sindresorhus/awesome require, and what does a complete discoverability checklist for the repo look like?
- **Sub-questions**:
  1. sindresorhus/awesome submission rules: contributing guidelines for adding a new list (README requirements, awesome-lint, PR process, acceptance criteria).
  2. Whether an "Awesome SysML"-adjacent list already exists upstream (duplicate check).
  3. Any discoverability checklist items beyond the obvious (topics, description, social preview).
- **Success criteria**:
  - SC1: The upstream submission requirements from the primary source (sindresorhus/awesome contributing guide).
  - SC2: Duplicate-list check result (existing SysML/MBSE lists in the awesome ecosystem).
  - SC3: Pitfalls/decline reasons surfaced (common PR rejection reasons).
- **Out of scope**: whether to submit (P3 decides the path; the user executes); spam/promotion tactics.
- **Budget**: 1 round target; cap 3.

## Findings

Decision-bearing (retrieved 2026-09-16):

- **Submission requirements (SC1, ESTABLISHED)**: sindresorhus/awesome new-list submissions require — a PR titled `Add <Name of List>` to the readme.md Contents section; the list to have existed ≥30 days ("Wait at least 30 days after creating a list before submitting it, to give it a chance to mature"); reviewing at least 4 other open PRs; commenting `unicorn` on your own PR; running awesome-lint and fixing reported issues; the repo slug in lowercase `awesome-name-of-list` form; not a duplicate. Sources: create-list.md, pull_request_template.md, contributing.md (all primary).
- **Duplicate check (SC2, ESTABLISHED)**: `mycr0ft/awesome-sysml` exists (5 stars, v1-focused). No v2-specific awesome list exists besides this repo. An unrelated Awesome-MBSE-Interview-QA repo also exists. GitHub search + topics pages, primary.
- **Pitfalls (SC3, ESTABLISHED cluster)**: sindresorhus/awesome has **temporarily disabled pull requests** ("Pull requests are temporarily disabled until I have a chance to catch up") with ~89-90 open add-PRs backlog. **AI-generated lists are hard-rejected** (PR #4093: "AI generated lists are not accepted"; "There is no way for me to verify whether you just asked Claude to find more maps"). Low-effort submissions are immediately closed ("If you have not put in considerable effort into your list, your pull request will be immediately closed"). Content bar: curation of the best, not everything; no unmaintained/archived/undocumented items; tight scope.
- **Niche fit (PROVISIONAL)**: the main awesome readme has no SysML/MBSE/systems-engineering section; MBSE discovery concentrates on the Systems-Modeling/Gaphor/Open-MBEE ecosystem and GitHub topics, not the general awesome index.
- Absence claims (PROVISIONAL): no documented minimum-star gate; no personal-project rejection wording; no SysML-scope decline precedent found.

## Synthesis

SC1/SC2/SC3 established from primary sources. Consequence for P3's design: the awesome-re submission is a **dated readiness path, not an immediate act** — three gates stand outside our control (30-day list age: earliest ~2026-10-15; PR intake currently disabled; the AI-curation sensitivity requires the human maintainer to demonstrate personal curation). The checklist therefore records the requirements, their current status, and the exact future PR steps, and defers the submission act to the maintainer once the age gate opens and intake resumes. Fit note: an alternative discovery path (MBSE community hubs, GitHub topics) is viable regardless of the sindresorhus outcome. Provisional items (stars gate folklore, niche-fit judgment) are named and non-blocking. Sources:

| URL | Class | Used for |
|-----|-------|----------|
| https://raw.githubusercontent.com/sindresorhus/awesome/main/create-list.md | primary | 30-day age, review-4-PRs, unicorn, duplicate search |
| https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md | primary | PR checklist verbatim (age, lint, slug, duplicate, effort, unmaintained) |
| https://raw.githubusercontent.com/sindresorhus/awesome/main/contributing.md | primary | PR guidelines pointer |
| https://github.com/sindresorhus/awesome | primary | PRs temporarily disabled banner |
| https://github.com/sindresorhus/awesome/pulls?q=is%3Apr+is%3Aopen+add | primary | ~89-90 open add-PR backlog |
| https://github.com/sindresorhus/awesome/pull/4093 | primary | AI-generated lists hard-reject |
| https://github.com/search?q=awesome+sysml&type=repositories | primary | duplicate check |
| https://github.com/search?q=awesome+mbse&type=repositories | primary | duplicate check |
| https://github.com/topics/mbse | secondary | MBSE discovery concentration |
