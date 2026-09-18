# Spec: github-notice-surface (P3)

Date: 2026-09-16
Parent: docs/superpowers/packages/2026-09-15-awesome-sysml-v2-packages.md (P3)
Gates: context COMPLETE (SC1 live-verified by parent; SC2/SC4 corroborated; SC3 carried ESTABLISHED), research COMPLETE (SC1/SC2/SC3 established from primary sources)

## Problem statement

Discoverability of this repo was implicit. The description and five topics were set during P1, the badge went up in P2, and nothing records that state against a checklist, so nobody can tell at a glance what is done and what still blocks discovery. Submission to sindresorhus/awesome was folklore until the research round pulled the primary sources, and that research found three gates the repo does not control: a 30-day list-age minimum (list created 2026-09-15, so earliest possible submission on or after 2026-10-15), upstream PR intake temporarily disabled with roughly 90 open add-PRs in the backlog and no promised reopen date, and a hard rejection of AI-generated lists that puts the curation claim on the human maintainer. Without a written record, these requirements live only in a research companion and will be re-derived or guessed wrong at submission time, for example by submitting while intake is closed or by letting tooling speak where the maintainer must.

P3 turns both into durable documents: a checklist verified against live state with honest pending markers, and a maintainer-facing submission-readiness runbook that carries the requirements, the gate status, the exact future PR steps, the curation claim, and the alternative discovery path.

## Goals

1. One new file, `docs/superpowers/runbooks/awesome-submission.md`, that holds the verified discoverability checklist and the awesome-re submission-readiness runbook.
2. Checklist rows carry evidence for done items and named blockers for pending items, verified against live repo state as of 2026-09-16.
3. The runbook records the three gates with their dates and status, quotes the upstream requirements verbatim with source URLs, and fixes the exact future PR steps.
4. The curation note states plainly that the submission is the maintainer's act and that this pipeline was tooling.
5. Zero churn elsewhere: no workflow changes, no README or contributing.md changes, no entry content changes.

## Non-goals (hard)

- Submitting the list now. All three gates block it. The runbook contains no submit-now instruction.
- Promised dates. Gate 2 has no promised reopen date and the runbook records no planned submission date.
- Workflow changes.
- Changes to contributing.md or README.md, including pointer lines. See the pointer decision below.
- Entry content, site content, spam or promotion tactics.

## Design

### Decision 1: one deliverable file, checklist inside the runbook

P3 creates exactly one file: `docs/superpowers/runbooks/awesome-submission.md` (new `runbooks/` directory under `docs/superpowers/`, sibling to `specs/`, `plans/`, `research/`, `context/`, `packages/`, `reviews/`). The discoverability checklist is the first content section of that file, not a second file. Two files for one maintainer audience doubles the drift surface for no gain; the spec artifacts under `docs/superpowers/specs/` are process-tree ephemera, and the checklist must live somewhere the maintainer will update as gates clear.

### Decision 2: content of the two deliverables

#### Section A: Repo discoverability state (checklist)

Table with columns: Item / Status as of 2026-09-16 / Evidence or blocker. Rows:

| Item | Status | Evidence or blocker |
|---|---|---|
| Public visibility | Done | `gh repo view`: isPrivate false |
| Description set | Done | "A curated list of OMG SysML v2 tools, example models, and learning resources" (`gh repo view`) |
| Topics (5) | Done | awesome, awesome-list, mbse, sysml, sysml-v2 (`gh repo view`) |
| Awesome badge present | Done, badge chrome only | README.md line 1 links to awesome.re. The badge is decoration; it is not a sindresorhus listing. Listing means an entry in sindresorhus/awesome readme.md Contents. |
| awesome-lint clean | Done, CI enforced | `.github/workflows/lint.yml` runs `awesome-lint@2.3.0` on README.md on every push to main and every PR to main |
| Companion site live and homepageUrl set | Pending | Blocked on b-18: 7 unpushed commits (HEAD de549d9) sit on the local branch; Pages, the repo homepage field, and a live-200 check wait for that push. backlog.md:24 tracks b-18. |
| Listed in sindresorhus/awesome | Pending | Three gates, none in repo control. See Section B. |

Every done row names its evidence source. Every pending row names its blocker. The badge row separates badge chrome from listing so the checklist cannot be read as "we are on awesome already".

#### Section B: Submission gates (as of 2026-09-16)

Three subsections, each with status, the verbatim upstream requirement, and its source URL.

1. Gate 1, list age. Upstream: "Wait at least 30 days after creating a list before submitting it, to give it a chance to mature" (create-list.md). This list was created 2026-09-15, so the earliest possible submission is on or after 2026-10-15. Status: open; clears by waiting.
2. Gate 2, PR intake. Upstream readme banner: "Pull requests are temporarily disabled until I have a chance to catch up with the existing ones", with roughly 90 open add-PRs in the backlog (retrieved 2026-09-16). No promised reopen date exists upstream. Status: blocked; must be rechecked at https://github.com/sindresorhus/awesome before any submission.
3. Gate 3, curation bar. Upstream hard-rejects AI-generated lists: "AI generated lists are not accepted"; "There is no way for me to verify whether you just asked Claude to find more maps or you did it yourself" (PR #4093). The effort bar: "If you have not put in considerable effort into your list, your pull request will be immediately closed" (pull_request_template.md). Status: blocked until the maintainer can truthfully make the personal curation claim in Section D.

#### Section C: Future PR steps (when all gates clear)

Numbered steps, exact enough to execute without re-research:

1. Confirm all three gates: date on or after 2026-10-15; intake reopened on sindresorhus/awesome; the Section D curation claim is true.
2. Review at least 4 other open PRs in sindresorhus/awesome.
3. Fork sindresorhus/awesome and create a branch.
4. Edit `readme.md`, Contents section: add the `Awesome SysML V2` entry under the fitting section. No SysML or MBSE section existed in the upstream Contents as of 2026-09-16 (provisional), so the maintainer picks the closest fit from the live Contents at submission time.
5. Title the PR exactly `Add SysML V2`. Upstream forbids the word Awesome in PR titles (pull_request_template.md bad example: `Add Awesome Swift`). The Contents entry name inside readme.md can still read `Awesome SysML V2`; only the PR title drops the word.
6. Complete the PR template checklist: the list "has been around for at least 30 days"; reviewed at least 4 PRs; comment `unicorn` on your own PR; awesome-lint run and all reported issues fixed; repo slug in the lowercase `awesome-name-of-list` form (`awesome-sysml-v2`); not a duplicate.
7. For the not-duplicate item, include this differentiation sentence: "Unlike mycr0ft/awesome-sysml, which focuses on SysML v1, Awesome SysML V2 curates tools, example models, and learning resources for OMG SysML v2 specifically."
8. Hold the content bar: best-of curation only, no unmaintained, archived, or undocumented items, tight scope, and be ready to defend every entry in review.
9. Do not submit until steps 1 through 8 hold. This runbook records readiness; it does not schedule the submission.

#### Section D: Curation statement

Fixed content: the submission is the maintainer's act. The build pipeline (specs, plans, research, context rounds under `docs/superpowers/`) was tooling that assembled candidates; the claim upstream demands is personal curation by the human maintainer. Before any submission the maintainer must have personally read every entry, must be able to defend each inclusion, must drop any entry they cannot vouch for, and must write the PR text themselves. No AI-authored submission text.

#### Section E: Alternative discovery paths

Fixed content: the list's value does not hinge on sindresorhus acceptance. MBSE discovery concentrates in the Systems-Modeling, Gaphor, and Open-MBEE ecosystem and on GitHub topics (github.com/topics/mbse), not the general awesome index. The repo already carries the mbse, sysml, and sysml-v2 topics. Community hubs, MBSE forums, and conference channels are viable regardless of the upstream outcome.

### Decision 3: no pointer to the runbook anywhere else

Default confirmed: none. Reasons: contributing.md and the README Contributing line are contributor-facing; this runbook is maintainer process, and the context round found that maintainer process lives in `docs/superpowers/` (no MAINTAINERS.md exists; the tree holds specs, plans, packages, backlog, and the packages document already indexes P3, so the tree self-indexes). A pointer in contributor files would also cross the locked out-of-scope ban on README and contributing.md changes. If a maintainer-facing index is ever wanted, a later work package can add it in the process tree.

## Documented limitations

- The checklist is a snapshot dated 2026-09-16. It goes stale the moment the b-18 push lands or upstream changes its rules. The runbook tells the maintainer to re-verify live state rather than trust old rows.
- The niche-fit claim (no SysML section upstream) is provisional. The section choice is deferred to submission time for that reason.
- Absence claims from research are provisional: no documented minimum-star gate and no personal-project rejection wording were found. Absence of a rule is not a rule.
- The runbook does not decide the submission. The maintainer does.

## Risks

- Gate drift: intake may reopen or requirements may change before 2026-10-15. Mitigation: quotes are dated, and step 1 of Section C mandates a live recheck of all three gates.
- Wrong Contents section risks a decline or an awkward review. Mitigation: the choice is deferred to the maintainer at submission time against the live Contents.
- Overclaiming against the v1 sibling (mycr0ft/awesome-sysml) would be both wrong and a rejection risk. Mitigation: the differentiation sentence is fixed in Section C, step 7, and states scope, not uniqueness.
- Stale pending markers being read as current fact. Mitigation: every row carries the as-of date via the section header, and pending rows name their blockers.

## Acceptance criteria

1. `docs/superpowers/runbooks/awesome-submission.md` exists and contains, in order: a title and scope line, the discoverability checklist table (requirement / status as of 2026-09-16 / gate or done), the three-gates section with dates and verbatim quotes, the future PR steps, the curation statement, and the alternative-paths section.
2. Every checklist row shows evidence for done or a named blocker for pending; the homepage/Pages row names b-18 and the unpushed commits; the badge row separates badge chrome from sindresorhus listing; rows reflect live state re-verified at execution time (not copied blind from this spec).
3. `git status` after execution shows exactly one new file; README.md, contributing.md, `.github/`, and workflows are untouched.
4. The runbook contains no submit-now instruction and no promised dates: gate 2 records "no promised reopen date", and the guard step ("do not submit until steps 1 through 8 hold") is present.
5. Upstream requirements are quoted verbatim with source URLs next to each quote.
6. The curation statement says the submission is the maintainer's act and that this pipeline was tooling.
7. The not-duplicate step contains the v1 sibling differentiation sentence from Section C, step 7.
8. The file passes `python ~/.zcode/scripts/prose_check.py` with no unexplained findings (zero em dashes, no Tier-1 slop vocabulary).

## Codebase context

Verified live 2026-09-16 against HEAD de549d9 ("Add companion docs site"). 7 unpushed commits on the local branch relative to origin/main (jgsystemsconsulting/awesome-sysml-v2). `gh repo view`: public, description set, five topics, homepageUrl empty. Three workflows active: links.yml, lint.yml, stale.yml. README.md line 1 carries the Awesome badge. contributing.md ends in the Maintenance section (P4) with a lint-gates subsection; a contributor PR template lives at `.github/PULL_REQUEST_TEMPLATE.md`. `docs/superpowers/` holds backlog.md plus context/, packages/, plans/, research/, reviews/, specs/; no `runbooks/` directory exists yet, and P3 creates it.

## Research

Carried ESTABLISHED from docs/superpowers/research/2026-09-16-github-notice-surface-research.md (retrieved 2026-09-16, all primary):

- https://raw.githubusercontent.com/sindresorhus/awesome/main/create-list.md (30-day age, duplicate search)
- https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md (PR checklist verbatim: review 4 PRs, unicorn comment, age, lint, slug, duplicate, effort, unmaintained; no-Awesome-in-title rule)
- https://github.com/sindresorhus/awesome (PRs temporarily disabled banner)
- https://github.com/sindresorhus/awesome/pull/4093 (AI-generated lists hard-reject)
- https://github.com/search?q=awesome+sysml&type=repositories (duplicate check: mycr0ft/awesome-sysml, v1-focused)
- https://github.com/topics/mbse (MBSE discovery concentration; alternative path)
