---
date: 2026-09-15
project: awesome-sysml-v2
mode: light
rounds: 2
input_digest: e2daa39b08b9a8f6a391c90e55d6ed383d5adecaefb1dfe403ddac52b9df3b51
open_objections: []
---

# Work Packages: awesome-sysml-v2 (round 2, light)

Round 1 (2026-09-15) proposed P1-P5, none picked. Round 2 (2026-09-16) absorbed the RRL findings in
`docs/superpowers/reviews/2026-09-15-awesome-sysml-v2-findings.md` as P6-P9. No candidate matched a
prior package (different subsystem), so round-1 ids survive unchanged.

Convergence order: P9, P6, P8, P7, P1, P4, P2, P3, P5. Human fork X1 is attached to P5 and remains open.

## P9: actions-sha-pin-all-workflows

- **id**: P9
- **name**: actions-sha-pin-all-workflows
- **size**: S
- **status**: done
- **deps**: []
- **corroboration**: 2 (risk, cohesion)
- **promoted_ids**: []
- **absorbs**: RRL I4
- **problem**: All three workflows pin GitHub Actions by mutable major tags while scheduled jobs grant issues:write and pass GITHUB_TOKEN into third-party actions. checkout@v4, setup-node@v4, lychee-action@v2, create-issue-from-file@v5, and markdownlint-cli2-action@v24 share one supply-chain control plane; tag float is a single cross-workflow hygiene gap, not three product features.
- **evidence**:
  - `.github/workflows/lint.yml:L13-22` — "checkout@v4 ... setup-node@v4 ... markdownlint-cli2-action@v24"
  - `.github/workflows/links.yml:L23` — "token: ${{ secrets.GITHUB_TOKEN }}"
  - `.github/workflows/stale.yml:L8-16` — "permissions contents:read issues:write; checkout@v4"
- **in_scope**: Replace mutable major-tag Action refs in lint.yml, links.yml, and stale.yml with full-length commit SHAs for every uses: entry; brief in-repo comments documenting the pin upgrade path.
- **out_scope**: awesome-lint version pin and lint.yml permissions block (P8, coordinate to avoid double edits); behavioral fixes; lychee fail:false policy; CI expansion (b-10); CODEOWNERS/branch protection/org allowlists; Dependabot unless trivial.
- **why_now**: Orthogonal hygiene on the same three files the behavior packages edit; one pin pass avoids reworking each file three times, and behavioral PRs after it will not reintroduce tags.
- **first_prompt**: `/superpowers-process full sha-pin all actions in awesome-sysml-v2 workflows`
- **triage notes**: PASS, order 1.

## P6: freshness-job-truth

- **id**: P6
- **name**: freshness-job-truth
- **size**: M
- **status**: done
- **deps**: []
- **corroboration**: 3 (value, risk, cohesion)
- **promoted_ids**: []
- **absorbs**: RRL I3 + I1
- **problem**: The monthly freshness job cannot deliver a reliable report: set -euo pipefail plus curl -sf in command substitution aborts the whole step on the first dead or 403 GitHub entry before the empty-pushed skip runs, so maintainers get no issue at all. When the job does complete it enforces a 12-month cutoff while contributing.md criterion 4 allows 24 months, so automation flags policy-compliant entries.
- **evidence**:
  - `.github/workflows/stale.yml:L21-22` — "set -euo pipefail / cutoff=$(date -u -d \"12 months ago\" +%Y-%m-%dT%H:%M:%SZ)"
  - `.github/workflows/stale.yml:L30-31` — "pushed=$(curl -sf ...) / [ -n \"$pushed\" ] || continue"
  - `contributing.md:L10` — "4. Active maintenance (commit within 24 months) or foundational value (formal specs, canonical reference repos)."
- **in_scope**: Make per-repo API/curl failures non-fatal so the job always posts at least a partial report; one shared window (24 months per contributing.md) written identically in stale.yml cutoff math, report prose, and contributing.md; keep the create-or-update issue path, no new cron.
- **out_scope**: New crons or extra scanners (b-01, b-10); links/lychee (P7); lint.yml/PR template (P8); SHA pinning (P9); P4 doc narrative beyond the cutoff number; non-GitHub freshness; README entry curation.
- **why_now**: Silent monthly failure and the policy/automation mismatch bite on the next cron; must land before P4 so the written cadence matches working, policy-aligned automation.
- **first_prompt**: `/superpowers-process full fix freshness job resilience and sync 24-month cutoff`
- **triage notes**: NEEDS-FIX, corrected by triage and applied: merged deps [P4] was a dependency-direction error (P6 must precede P4, not follow it); P6 now has no deps and P4 carries deps [P6]. Grade after fix: PASS, order 2.

## P8: pr-lint-gate-surface

- **id**: P8
- **name**: pr-lint-gate-surface
- **size**: M
- **status**: done
- **deps**: []
- **corroboration**: 2 (value, cohesion)
- **promoted_ids**: []
- **absorbs**: RRL I5 + I6 + I7
- **problem**: First-time contributors hit one broken PR-gate contract: PULL_REQUEST_TEMPLATE asks only for awesome-lint while contributing.md and lint.yml also require markdownlint, so preventable red CI burns goodwill. The same lint workflow is the only job without a top-level permissions block and runs unpinned npx awesome-lint with no package.json or lockfile, so the PR gate fetches a mutable network executable.
- **evidence**:
  - `.github/PULL_REQUEST_TEMPLATE.md:L4` — "- [ ] `npx awesome-lint README.md` passes locally"
  - `contributing.md:L27-29` — "npx awesome-lint README.md / npx markdownlint-cli2 \"README.md\" \"contributing.md\""
  - `.github/workflows/lint.yml:L1-20` — "checkout@v4, setup-node@v4 node 20, run: npx awesome-lint README.md"; repo has no package.json or lockfile
- **in_scope**: Explicit permissions: contents: read on lint.yml; pin awesome-lint (versioned npx and/or minimal package.json+lockfile) consistent with contributing.md local commands; markdownlint checkbox on the PR template; keep contributing.md commands aligned with CI.
- **out_scope**: Repo-wide SHA pinning (P9, coordinate on the lint.yml header); new linter families (b-10); link checks (P7); freshness (P6); site/CoC/discoverability (P2/P5/P3).
- **why_now**: One PR-gate contract: permissions and pin without template/runbook alignment still fail contributors, and a template fix without pin leaves supply-chain drift on the same job. Pays off before the P1 public flip and P3 notice push.
- **first_prompt**: `/superpowers-process full align awesome-sysml-v2 pr lint gate`
- **triage notes**: PASS, order 3.

## P7: link-ops-no-spam-pr-path

- **id**: P7
- **name**: link-ops-no-spam-pr-path
- **size**: M
- **status**: done
- **deps**: [P9]
- **corroboration**: 3 (value, risk, cohesion)
- **promoted_ids**: []
- **absorbs**: RRL I2 + I8
- **problem**: Weekly link health leaks on both ends: links.yml always creates a new fixed-title Link Checker Report issue instead of the create-or-update pattern stale.yml already uses, so repeated failures spam the issue list (and the step depends on undefined in-repo labels, advisory a-06). Lychee runs only on cron/dispatch with fail:false while lint.yml PR/push never checks HTTP reachability though criterion 1 requires a stable reachable URL, so bad links merge green until Monday.
- **evidence**:
  - `.github/workflows/links.yml:L17-30` — "lychee-action@v2 fail: false; Create Issue From File ... title: Link Checker Report ... labels: report, broken-links"
  - `.github/workflows/stale.yml:L44-48` — "existing=$(gh issue list --state open --search \"Freshness report in:title\" ...) if [ -n \"$existing\" ]; then gh issue edit ..."
  - `contributing.md:L7` — "1. Stable, reachable URL pointing at the project itself."
  - `.github/workflows/lint.yml:L3-7` — "on: pull_request branches [main], push branches [main]"
- **in_scope**: Switch Link Checker Report to create-or-update single open issue (mirror the freshness pattern); ensure labels exist or stop depending on them (a-06); contributor-visible reachability path (PR-time lychee fail:false soft signal and/or documented local command); align the PR template link-check checkbox with the chosen path.
- **out_scope**: Hard-fail merge gate without an explicit product decision (a-04, see backlog b-12); extra scanners (b-01, b-10); freshness (P6); awesome-lint pin/permissions/markdownlint checkbox (P8); repo-wide pinning (P9); README content cleanup; P3.
- **why_now**: Complements P4's weekly-scan claim and protects list quality ahead of P3/awesome.re notice; sequenced after P9 so links.yml pins are stable before logic and label changes.
- **first_prompt**: `/superpowers-process full link report upsert and pr-time link check`
- **triage notes**: PASS, order 4.

## P1: make-repo-public

- **id**: P1
- **name**: make-repo-public
- **size**: S
- **status**: done
- **deps**: []
- **corroboration**: 3 (value, risk, cohesion)
- **promoted_ids**: []
- **problem**: The repo is private, so an awesome list cannot fulfill its purpose: GitHub search, stars, forks, topic pages, Google indexing, and the standard public github.io companion URL are all blocked. Description and topics already exist; visibility is the one missing switch every later public-facing package inherits.
- **evidence**:
  - `GITHUB METADATA: isPrivate` — "isPrivate: true. Repo is private: invisible to GitHub search, stars, forks, Google indexing; awesome lists are inherently public artifacts."
  - `README.md:L1` — "# Awesome SysML V2 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)"
- **in_scope**: Flip repository visibility to public when ready; confirm org/policy readiness; confirm description and topics survive the change; verify Actions still run under public defaults.
- **out_scope**: README entry curation; docs/ site authoring; new CI workflows; awesome.re submission and external promotion; community root meta files (P5).
- **why_now**: Blocks discoverability intent and every dependent public surface. No dependent package pays off while the repo is private.
- **first_prompt**: `/superpowers-process full make awesome-sysml-v2 public and verify metadata and actions`
- **triage notes**: Round 1 PASS. Round 2: unchanged; P9 (pins) now precedes it in the order.

## P4: maintenance-cadence-ack

- **id**: P4
- **name**: maintenance-cadence-ack
- **size**: S
- **status**: done
- **deps**: [P6]
- **corroboration**: 1 (value, round 1)
- **promoted_ids**: []
- **problem**: User asked whether a weekly scan is needed and wanted an ongoing maintenance plan. The repo already runs a weekly lychee link check and a monthly freshness report; the gap is writing that cadence down as the plan instead of inventing more automation.
- **evidence**:
  - `.github/workflows/links.yml` — weekly cron "0 18 * * 1", lychee link check, auto-creates issue on failure
  - `.github/workflows/stale.yml` — monthly cron "0 6 1 * *", freshness report issue
  - `.github/workflows/lint.yml` — awesome-lint + markdownlint on PR and push to main
- **in_scope**: Document the maintenance plan (weekly link scan, monthly freshness issue, PR lint gates) in contributing.md or README; answer the weekly-scan question: already covered by links.yml; one-line pointer to the cadence from the Contributing section.
- **out_scope**: New cron workflows; daily scans; editorial SLA tooling.
- **why_now**: Closes the cadence intent at near-zero cost by productizing automation already in tree. After round 2, it documents automation that P6 and P7 have first made truthful.
- **first_prompt**: `/superpowers-process full document awesome-sysml-v2 maintenance cadence`
- **triage notes**: Round 1 PASS. Round 2: deps now [P6] per dependency-direction fix; P4 documents the cadence only after P6 lands.

## P2: companion-docs-site

- **id**: P2
- **name**: companion-docs-site
- **size**: M
- **status**: done
- **deps**: [P1]
- **completion note**: Tasks 1-5 landed (commit de549d9). Task 6 (Pages enable, homepageUrl, live-200 check) pends the push to origin/main — tracked as backlog b-18.
- **corroboration**: 3 (value, risk, cohesion, round 1)
- **promoted_ids**: []
- **problem**: No docs/ GitHub Pages companion site exists and homepageUrl is empty, while the org standard for ten sibling JGS repos is easily navigable static HTML under docs/ with shared head/nav/masthead/site.css and homepageUrl pointed at the Pages URL.
- **evidence**:
  - `INTENT:1` — "A website to accompany the repo, easily navigable, matching the standard used for other JGS repos."
  - `ORG SITE STANDARD` — "Static hand-authored HTML in docs/ served by GitHub Pages at https://jgsystemsconsulting.github.io/<repo>/ ; repo homepageUrl set to that URL"
  - `GITHUB METADATA: homepageUrl` — "homepageUrl: empty"
- **in_scope**: docs/ static site to the JGS head/nav/masthead/site.css standard; README sections presented in navigable site form (README stays source of truth); Pages on; homepageUrl set; website-lifecycle review/update cycles going forward.
- **out_scope**: Rewriting the README entry corpus; custom app/backend; non-standard design system; visibility changes; community meta files; workflow cadence changes.
- **why_now**: Direct delivery of intent #1 and org parity; without Pages plus homepageUrl the repo stays README-only.
- **first_prompt**: `/superpowers-process full build awesome-sysml-v2 docs site to JGS standard and enable Pages`
- **triage notes**: Round 1 PASS, unchanged in round 2. Order 7.

## P3: github-notice-surface

- **id**: P3
- **name**: github-notice-surface
- **size**: S
- **status**: done
- **deps**: [P1, P2]
- **corroboration**: 1 (value, round 1)
- **promoted_ids**: []
- **problem**: Discoverability review is an explicit goal. Description and topics already exist, but the notice surface stays incomplete until public visibility, homepage, and a discoverability checklist are in place.
- **evidence**:
  - `INTENT:2` — "Review how to get the repo noticed on GitHub (discoverability)."
  - `GITHUB METADATA` — homepageUrl empty; description and topics set
- **in_scope**: Discoverability checklist (public + topics + description + awesome badge + homepage); awesome.re submission path; verify sibling-parity notice files landed (deferred to P5 for execution).
- **out_scope**: Paid promotion; social campaigns; list taxonomy changes.
- **why_now**: Converts the discoverability intent into a concrete, verifiable repo surface once visibility and site URL exist.
- **first_prompt**: `/superpowers-process full awesome-sysml-v2 discoverability checklist and awesome submission`
- **triage notes**: Round 1 PASS. Round 2: unchanged; P7's contributor-path work lands before it so new public traffic meets a working PR gate. Order 8.

## P5: community-root-meta

- **id**: P5
- **name**: community-root-meta
- **size**: M
- **status**: done
- **deps**: [P1]
- **corroboration**: 2 (risk, cohesion, round 1)
- **promoted_ids**: []
- **problem**: SECURITY.md and CODE_OF_CONDUCT.md are absent while LICENSE and contributing.md exist, and sibling parity also lists CITATION.cff and CHANGELOG.md. Once public, GitHub community and security tabs flag the gaps and there is no documented channel for malicious-link or conduct reports.
- **evidence**:
  - `REPO SURVEY` — "Missing vs sibling repos: docs/ site, CHANGELOG.md, CODE_OF_CONDUCT.md, SECURITY.md, CITATION.cff"
- **in_scope**: CODE_OF_CONDUCT.md and SECURITY.md at repo root in one pass; SECURITY.md reporting path appropriate to a link-curation repo (malicious or harmful entries, no app CVE theater); one-line pointers from README or contributing.md; CITATION.cff and CHANGELOG.md pending human fork X1.
- **out_scope**: docs/ site; visibility changes; workflow changes; README list rewrites.
- **why_now**: Cheap closed-loop fix so the first public snapshot is not missing baseline trust files; pairs with the visibility flip.
- **first_prompt**: `/superpowers-process full add awesome-sysml-v2 community root meta files`
- **triage notes**: Round 1 HOLD on fork X1 (risk excludes CITATION.cff/CHANGELOG.md; cohesion includes them). Round 2 merge and triage re-escalated X1 unchanged; still a human fork. Unrouted files fall back to backlog b-07/b-08. Order 9.
