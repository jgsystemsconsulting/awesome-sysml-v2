# Awesome Submission Runbook

Scope: discoverability checklist and sindresorhus/awesome submission-readiness record for this repo, snapshotted 2026-09-16 against HEAD de549d9. Every row and gate in this file is a dated snapshot, not a live fact. Re-verify against the repo and upstream before acting on anything here.

## Section A: Repo discoverability state (checklist)

| Item | Status as of 2026-09-16 | Evidence or blocker |
|---|---|---|
| Public visibility | Done | `gh repo view`: isPrivate false |
| Description set | Done | "A curated list of OMG SysML v2 tools, example models, and learning resources" (`gh repo view`) |
| Topics (5) | Done | awesome, awesome-list, mbse, sysml, sysml-v2 (`gh repo view`) |
| Awesome badge present | Done, badge chrome only | README.md line 1 links to awesome.re. The badge is decoration; it is not a sindresorhus listing. Listing means an entry in the sindresorhus/awesome readme.md Contents. |
| awesome-lint clean | Done, CI enforced | `.github/workflows/lint.yml` runs `awesome-lint@2.3.0` on README.md on every push to main and every PR to main |
| Companion site live and homepageUrl set | Pending | Blocked on b-18: 7 unpushed commits (HEAD de549d9) sit on the local branch; Pages, the repo homepage field, and a live-200 check wait for that push. `docs/superpowers/backlog.md:24` tracks b-18. |
| Listed in sindresorhus/awesome | Pending | Three gates, none in repo control. See Section B. |

## Section B: Submission gates (as of 2026-09-16)

### Gate 1: List age (open; clears by waiting)

Upstream requirement, quoted verbatim from create-list.md: "Wait at least 30 days after creating a list before submitting it, to give it a chance to mature"

Source: https://raw.githubusercontent.com/sindresorhus/awesome/main/create-list.md

This list was created 2026-09-15, so the earliest possible submission is on or after 2026-10-15. Note: the PR template's wording is "Has been around for at least 30 days", so the safe date is 2026-10-16 if the count is read strictly. If a 2026-10-15 submission draws an age objection, wait one day and resubmit.

### Gate 2: PR intake (blocked)

Upstream readme banner, quoted verbatim: "Pull requests are temporarily disabled until I have a chance to catch up with the existing ones"

Source: https://github.com/sindresorhus/awesome

Roughly 90 open add-PRs sit in the upstream backlog (retrieved 2026-09-16). No promised reopen date exists upstream. This runbook records no planned submission date. Recheck intake at https://github.com/sindresorhus/awesome before any submission attempt.

### Gate 3: Curation bar (blocked until the Section D claim is true)

Upstream hard-rejects AI-generated lists. From PR #4093, quoted verbatim: "AI generated lists are not accepted" and "There is no way for me to verify whether you just asked Claude to find more maps or you did it yourself"

Source: https://github.com/sindresorhus/awesome/pull/4093

The effort bar, quoted verbatim from pull_request_template.md: "If you have not put in considerable effort into your list, your pull request will be immediately closed"

Source: https://raw.githubusercontent.com/sindresorhus/awesome/main/pull_request_template.md

## Section C: Future PR steps (when all gates clear)

1. Confirm all three gates: date on or after 2026-10-15; intake reopened on sindresorhus/awesome; the Section D curation claim is true.
2. Review at least 4 other open PRs in sindresorhus/awesome.
3. Fork sindresorhus/awesome and create a branch.
4. Edit `readme.md`, Contents section: add the `Awesome SysML V2` entry under the fitting section. No SysML or MBSE section existed in the upstream Contents as of 2026-09-16 (provisional), so the maintainer picks the closest fit from the live Contents at submission time.
5. Title the PR exactly `Add SysML V2`. Upstream forbids the word Awesome in PR titles (pull_request_template.md bad example: `Add Awesome Swift`). The Contents entry name inside readme.md can still read `Awesome SysML V2`; only the PR title drops the word.
6. Complete the PR template checklist: list "has been around for at least 30 days"; reviewed at least 4 PRs; comment `unicorn` on your own PR; awesome-lint run and all reported issues fixed; repo slug in the lowercase `awesome-name-of-list` form (`awesome-sysml-v2`); not a duplicate.
7. For the not-duplicate item, include this differentiation sentence: "Unlike mycr0ft/awesome-sysml, which focuses on SysML v1, Awesome SysML V2 curates tools, example models, and learning resources for OMG SysML v2 specifically."
8. Hold the content bar: best-of curation only, no unmaintained, archived, or undocumented items, tight scope, and be ready to defend every entry in review.
9. Do not submit until steps 1 through 8 hold. This runbook records readiness; it does not schedule the submission.

## Section D: Curation statement

The submission is the maintainer's act. The build pipeline (specs, plans, research, and context rounds under `docs/superpowers/`) was tooling that assembled candidates; the claim upstream demands is personal curation by the human maintainer. Before any submission the maintainer must have personally read every entry, must be able to defend each inclusion, must drop any entry they cannot vouch for, and must write the PR text themselves. No AI-authored submission text.

## Section E: Alternative discovery paths

The list's value does not hinge on sindresorhus acceptance. MBSE discovery concentrates in the Systems-Modeling, Gaphor, and Open-MBEE ecosystem and on GitHub topics (https://github.com/topics/mbse), not the general awesome index. The repo already carries the mbse, sysml, and sysml-v2 topics. Community hubs, MBSE forums, and conference channels are viable regardless of the upstream outcome.
