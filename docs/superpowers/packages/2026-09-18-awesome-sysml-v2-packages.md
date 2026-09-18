---
date: 2026-09-18
project: awesome-sysml-v2
mode: light
rounds: 1
input_digest: 6f431235a29552908be66fb00a9b98a2e88f9553c383280e32f6b832e257081c
open_objections: []
---

# Work packages: awesome-sysml-v2 (2026-09-18, light mode, round 1)

First package-loop run against the Path S landing bar (awesome-archimate parity).
Prior 2026-09-15 packages are all done. Taste audit found no should-fix on the
landing visual surface. Lens wave found 5 remaining candidates; merge union left
5 packages; triage graded all 5 PASS with zero critical defects.

Dependency order: P1, P3, P2, P5, P4. P3 may land in the same change as P1
(setup-python pin on the new validate.yml). landing-visitor-copy is not packaged
(already clean per taste audit).

## P1: landing-truth-gate

| Field | Value |
|---|---|
| id | P1 |
| name | landing-truth-gate |
| size | M |
| deps | none |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full landing truth gate` |

**Problem.** scripts/check_release.py already encodes the Path S landing truth
gate (chips vs RELEASE-INFO/README, eleven section anchors) and passes locally,
but no workflow runs it on PR/push and the truth triad is not documented as a
frozen product contract. Chip or heading drift can merge green while CI stays
green.

**Evidence.**

- scripts/check_release.py landing truth gate block and PASS print
- no .github/workflows/validate.yml (only lint/links/stale)
- awesome-archimate validate.yml runs python scripts/check_release.py
- docs/index.html chips: version 0.1.0, sweep 2026-09, entries 75
- taste review residual: wire CI; harden links.yml; catalogue; assessment

**In scope.** Add .github/workflows/validate.yml (SHA-pinned checkout,
contents:read, run scripts/check_release.py on pull_request and push to main
plus workflow_dispatch, fail on nonzero). Freeze truth triad as product contract
(document chip/RELEASE-INFO/README source mapping). Minimal gate fixes only on
false fail. Match archimate validate surface. Hand setup-python SHA pin to P3
in the same change when the job adds Python.

**Out of scope.** Landing visual or visitor-copy rewrite; lychee policy (P2);
org catalogue (P4); acceptability assessment (P5); GitHub Releases tagging;
branch-protection admin outside the workflow file.

**Why now.** Gate file is half of outcome-bar item 3; without CI every later
product-surface change can ship untrue chips. Precedes pin, catalogue, and
assessment claims that the router is trustworthy.

**Triage notes.** PASS, order 1, size M.

## P3: pin-validate-setup-python

| Field | Value |
|---|---|
| id | P3 |
| name | pin-validate-setup-python |
| size | S |
| deps | P1 |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full pin validate setup python` |

**Problem.** Existing workflows are full-length SHA-pinned. When P1 adds
validate.yml with a Python runner, a mutable setup-python@v5 tag would reopen
the P9 supply-chain hole. awesome-archimate already pins
actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.

**Evidence.**

- lint.yml pin-policy comment and setup-node full SHA
- links.yml checkout and lychee-action full SHAs
- archimate validate.yml setup-python full SHA # v5
- P9 actions-sha-pin-all-workflows status done

**In scope.** Ensure every uses: entry in validate.yml is full-length SHA-pinned
with a version comment matching sibling workflows; pin setup-python when present;
Python 3.12 parity with archimate. Same PR as P1 or tiny follow-on.

**Out of scope.** Creating validate.yml (P1); re-pinning lint/links/stale;
Dependabot; gate script content; lychee.

**Why now.** Pays the moment P1 introduces the workflow; tiny fix keeps P9
parity on the only new Action this bar adds.

**Triage notes.** PASS, order 2, size S.

## P2: link-check-product-surface

| Field | Value |
|---|---|
| id | P2 |
| name | link-check-product-surface |
| size | S |
| deps | P1 |
| status | done |
| promoted_ids | [b-12] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full landing link check coverage` |

**Problem.** links.yml lychee scopes only README.md with fail: false, so PR
broken-link findings are advisory and docs/index.html product-surface hrefs are
never scanned. Broken landing CTAs and section anchors can merge green.
awesome-archimate already scopes README.md + docs/index.html with
--include-fragments=anchor-only and fails the PR job on lychee nonzero exit.
Outcome bar item 6 chooses hard-fail for the product surface (promotes b-12).

**Evidence.**

- .github/workflows/links.yml args README.md only; fail: false; advisory PR step
- docs/index.html Open full list CTA and eleven README section anchors
- backlog b-12 lychee hard-fail needs-info
- archimate links.yml product-surface fail step

**In scope.** Add docs/index.html to lychee args with fragment parity
(--include-fragments=anchor-only). On pull_request, fail the job when lychee
exit_code != 0. Keep schedule/workflow_dispatch create-or-update issue path.
Align contributing.md / PR template if they still describe advisory-only link
checks. Preserve fail: false on the lychee action step if an explicit PR fail
step owns blocking (archimate pattern).

**Out of scope.** Full-repo crawl of docs/superpowers; chip/anchor assertions
(P1); landing copy redesign; freshness/stale.yml; validate.yml; sindresorhus.

**Why now.** Landing is the public router; unscoped advisory-only link CI lets
dead CTAs ship while README-only advisory greenwashes the PR.

**Triage notes.** PASS, order 3, size S. b-12 promoted into this package.

## P5: awesome-acceptability-assessment

| Field | Value |
|---|---|
| id | P5 |
| name | awesome-acceptability-assessment |
| size | S |
| deps | P1, P3 |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full awesome acceptability assessment` |

**Problem.** DISTRIBUTION.md defers sindresorhus/awesome with acceptability
unassessed. The 2026-09-16 runbook is a dated snapshot (age gate, intake closed,
curation claim), not a live go/no-go. Outcome bar item 9 wants assessment only;
do not open the awesome PR unless the assessment is an explicit go-now.

**Evidence.**

- docs/DISTRIBUTION.md sindresorhus row deferred, unassessed
- docs/superpowers/runbooks/awesome-submission.md snapshot header and gates
- backlog b-11 open awesome.re path

**In scope.** Re-verify age, intake banner, awesome-lint, curation/effort bar,
and differentiation. Write a dated go/no-go/wait assessment. Update
DISTRIBUTION.md notes with decision date. Refresh runbook snapshot headers.
Explicit no-PR default unless go-now.

**Out of scope.** Opening the sindresorhus/awesome PR before go-now; bulk README
rewrite; org catalogue; CI workflow changes; landing redesign.

**Why now.** Closes outcome bar item 9 without forcing a premature upstream PR;
independent of catalogue once public surfaces are stable.

**Triage notes.** PASS, order 4, size S.

## P4: org-catalogue-entry

| Field | Value |
|---|---|
| id | P4 |
| name | org-catalogue-entry |
| size | S |
| deps | P1, P2, P3 |
| status | done |
| promoted_ids | [] |
| corroboration | 3 (value, risk, cohesion) |
| first_prompt | `/superpowers-process full org catalogue entry` |

**Problem.** DISTRIBUTION.md lists the labs.jgsystemsconsulting.com org
catalogue as planned. jgsystemsconsulting-website data/products.yml has
awesome-archimate but not awesome-sysml-v2, so the public list stays off the
org product surface after Path S lands.

**Evidence.**

- docs/DISTRIBUTION.md org catalogue row planned
- GitHub Pages landing row already submitted
- labs products.yml awesome-archimate entry; no awesome-sysml-v2
- landing canonical https://jgsystemsconsulting.github.io/awesome-sysml-v2/

**In scope.** Add awesome-sysml-v2 entry to products.yml (name, url, page, blurb,
tier, featured, order) beside other awesome spokes. Point page at the live
Pages URL. Regenerate labs docs/index.html products section if that is the
repo's render path. Flip DISTRIBUTION.md org catalogue row to submitted with
date and evidence. Leave a clean labs branch ready to merge.

**Out of scope.** Labs site redesign; sindresorhus PR; community directory
posts; landing HTML redesign inside this repo beyond ledger status; GitHub
Releases.

**Why now.** Next named org channel after the landing router is trustworthy
(P1 gate, P2 product-surface links, P3 pin).

**Triage notes.** PASS, order 5, size S.

## Killed / not packaged

- landing-visitor-copy: taste audit PASS; Top/Status/Open full list; no Hero,
  FAMILY.md, or mirror-note jargon; chrome nits already present.
- Path S visual shell + DESIGN_BRIEF/DESIGN: already written this session.
- og:image social-card regen: optional nit n-01 / b-19 only.
- Re-pin lint/links/stale: P9 done.
- GitHub Releases v0.1.0: after package drain on main.
