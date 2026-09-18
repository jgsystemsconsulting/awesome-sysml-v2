# Taste audit: Awesome SysML V2 landing (2026-09-18)

**Design read:** technical index landing for SysML v2 practitioners, minimal-technical light shell, Path S static docs/, family gold = awesome-archimate.

**Dials (from DESIGN, not SaaS baseline):** VARIANCE 4, MOTION 2, DENSITY 6.

## Verdict

Landing matches DESIGN contract composition and tokens. No should-fix visual redesign. Residual work is release-gate automation, CI product-surface coverage, distribution ledger channels, and optional acceptability assessment. Chrome nits already present (favicon, woff2 preload, 44px nav targets, no IE shim).

## Pre-flight (product-relevant only)

| Check | Result |
| --- | --- |
| CDN fonts | PASS (self-hosted Plex) |
| Em dashes in copy | PASS |
| "Hero" nav label | PASS (Top) |
| Dual full-list CTA labels | PASS (both "Open full list") |
| Evidence heading jargon | PASS (Status) |
| FAMILY.md / mirror-note maintainer tails | PASS (absent) |
| Sticky nav + section index + chips | PASS |
| Favicon | PASS |
| woff2 preload | PASS |
| Nav touch targets 44px | PASS |
| Dead IE shim | PASS (none) |
| One accent | PASS |
| Light shell | PASS |
| Support line ≤20 words | PASS (18 words) |
| Footer CC0 + licence enquiry + maintainer | PASS |
| Entry chip vs README curated count | PASS (75; gate green) |

## Should-fix

None on the landing visual surface. Ship as Path S router; remaining outcome-bar items are packages (truth gate already in tree as scripts/check_release.py; wire CI; harden links.yml; catalogue; assessment).

## Nits (optional, backlog only)

- n-01: og:image still points at social-card.png from the prior dark shell; regenerate optional later if share preview looks off-brand on light pages.
- n-02: contribute links use generic issues/new (no YAML templates yet); templates are a separate backlog if issue forms are wanted.
- n-03: dark `docs/site.css` removed; confirm nothing else linked it (landing is inline CSS only).

## Package feed

Feed package-loop: landing-truth-gate (gate exists; needs validate.yml + freeze docs), landing-visitor-copy (mostly done; hold only if residual jargon found), org-catalogue-entry, awesome-acceptability-assessment, link-check-product-surface, pin-validate-setup-python (if validate.yml added with setup-python).
