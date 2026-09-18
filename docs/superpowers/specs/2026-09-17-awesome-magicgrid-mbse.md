# Design spec: awesome-magicgrid-mbse

Date: 2026-09-17. Author: sp-spec-author (superpowers step 1). Status: ready for planning.

## Goal

Create and publish `awesome-magicgrid-mbse`, a curated awesome list for the MagicGrid MBSE methodology, as a standalone public repository under `jgsystemsconsulting`. Execution creates the repo at `C:\Users\gower\OneDrive\Documents\GitHub\awesome-magicgrid-mbse`; nothing outside the spec is written now.

MagicGrid is the MBSE methodology from No Magic, now part of Dassault Systemes (CATIA Magic, Cameo Systems Modeler). It is a grid-based methodology; its canonical structure is taken from official MagicGrid material at seed time. The list collects material about that method: official resources, the Book of Knowledge, papers and case studies, videos and talks, training, example models, tool support, and brief pointers to peer methodologies. The sister list awesome-sysml-v2 owns the SysML v2 language and its tooling; this list owns the method applied with it.

Version one ships as one cut: seeded README with 40+ verified entries, lint and link-check automation, community meta files, docs site, and publication after all local checks pass.

## Non-goals

- No generic SysML language material; awesome-sysml-v2 already covers it.
- No generic MBSE content beyond the MagicGrid method and named peer methodologies.
- No CSS or JavaScript "magic grid" layout libraries, at any quality level.
- No hosting of Book of Knowledge PDFs or any other copyrighted material.
- No awesome.re submission and no social card generation in v1.
- No coverage of OOSEM, Harmony-SE, SYSMOD, or Arcadia/Capella beyond short pointer entries.

## Research

Research gate: `docs/superpowers/research/2026-09-17-awesome-magicgrid-mbse-research.md` (this session). Findings the spec relies on:

- No public MagicGrid list exists. GitHub "MagicGrid" results are CSS/JS grid libraries and stubs, with one real MBSE hit (`matthieugourssies/sysml-magicgrid-vccs`). The gap is real.
- Roughly 40 to 70 linkable items are reachable, with a high-signal core of 35 to 50. Strongest buckets: videos (15 to 40), academic papers (15 to 30), official pages (8 to 15), training (5 to 15).
- The method lives in vendor training, docs, and papers; the top-level CATIA Magic pages scraped in the research scan mention it zero times. Guessed deep doc URLs 404 and old `nomagic.com` paths return 403, so links must be verified, never constructed.
- MagicGrid is vendor methodology branding. Standard awesome-list posture applies: descriptive use plus a disclaimer. Cited sources used by this spec:
  - https://www.3ds.com/products/catia/catia-magic
  - https://docs.nomagic.com/
  - https://www.3ds.com/edu/catia-magic-training/mbse-sysml-v2-and-magicgrid
  - https://doi.org/10.1002/j.2334-5837.2017.00350.x (MBSE Grid origin paper, 2017)
  - https://doi.org/10.1002/inst.12429 (V&V with MagicGrid, INSIGHT 2023)

Decision recorded in the research file and confirmed by the user: build standalone now, cross-linked with awesome-sysml-v2; fold into a public awesome-mbse later only if that repo goes public (it is currently private).

## Codebase context

The template is this repository, awesome-sysml-v2, read in full this session. Facts the port depends on:

- Root files: README.md, contributing.md, .markdownlint-cli2.jsonc (sets MD013 line-length off), CHANGELOG.md, CITATION.cff, CODE_OF_CONDUCT.md, SECURITY.md, LICENSE (CC0 1.0 Universal), docs/ (index.html, site.css, social-card.jpg, social-card.png, .nojekyll), and three workflows under .github/workflows/.
- README pattern: awesome badge, one-paragraph intro, Contents TOC, 11 content sections plus Contributing, entries in `- [Name](URL) - Description.` format, sorted alphabetically by link text, one factual sentence per entry.
- contributing.md: five inclusion criteria, exact entry format, pinned local commands (`npx awesome-lint@2.3.0 README.md`, `npx markdownlint-cli2`, native `lychee` binary), and a maintenance section describing the three workflows.
- lint.yml: awesome-lint plus markdownlint on every PR and push to main, Node 20, actions pinned to full commit SHAs. links.yml: weekly lychee scan (Monday 18:00 UTC), advisory, report issue on failure. stale.yml: monthly 24-month freshness report, advisory. All three reference only README.md and contributing.md by path; none mentions the repo name.
- docs/index.html: static single page, dark scheme, canonical under `https://jgsystemsconsulting.github.io/awesome-sysml-v2/`, category map table, JSON-LD block, og and twitter meta.
- Inconsistency to avoid copying: CITATION.cff and the docs footer say MIT while LICENSE is CC0 1.0. The new repo writes CC0 in all three places. Fixing the template repo itself is out of scope here.

## Locked decisions

These came from the conversation and are fixed. The spec does not reopen them.

| Decision | Value |
|---|---|
| Repo name | `awesome-magicgrid-mbse` (disambiguates from CSS/JS magic-grid libraries; matches vendor spelling) |
| Layout | Standalone repo, created at execution time, public under `jgsystemsconsulting` |
| Scope in | Official resources, books, papers and case studies, videos and talks, training, example models, tool support, brief peer-methodology pointers |
| Scope out | Generic SysML, generic MBSE, CSS/JS grid libraries, BoK PDF hosting |
| Style | Mirrors awesome-sysml-v2: README with badge and TOC, contributing.md, awesome-lint plus markdownlint CI, weekly lychee, stale report, community files, docs site |
| Cross-links | Both directions between the two repos |
| Disclaimer | Not affiliated with Dassault Systemes or No Magic; trademark note; legitimate links only |
| Seed size | 40+ verified links; section minimums below sum to 45 |
| Publication | Gated on lint, markdownlint, and lychee passing locally first |

## Repo structure

Everything below is created fresh in the new repo at execution time.

```text
awesome-magicgrid-mbse/
├── .github/
│   └── workflows/
│       ├── lint.yml        # copied verbatim
│       ├── links.yml       # adapted: lychee accept set
│       └── stale.yml       # copied verbatim
├── docs/
│   ├── .nojekyll           # copied, empty; keeps Pages from running Jekyll
│   ├── index.html          # adapted from template
│   └── site.css            # copied verbatim
├── .markdownlint-cli2.jsonc  # copied verbatim
├── CHANGELOG.md            # fresh
├── CITATION.cff            # fresh
├── CODE_OF_CONDUCT.md      # adapted
├── LICENSE                 # CC0 1.0 Universal, copied
├── README.md               # fresh
├── SECURITY.md             # copied verbatim
└── contributing.md         # adapted
```

No social-card files in v1; see the docs site plan and the later-work section.

## README plan

Header and intro: `# Awesome MagicGrid MBSE` with the awesome.re badge. One intro paragraph: "A curated list of resources for the MagicGrid MBSE methodology: official material, the Book of Knowledge, papers and case studies, talks, training, example models, and tool support. For SysML v2 language and tooling, see the sister list [awesome-sysml-v2](https://github.com/jgsystemsconsulting/awesome-sysml-v2)."

Disclaimer blockquote directly under the intro, verbatim:

> This list is maintained independently. It is not affiliated with, endorsed by, or sponsored by Dassault Systemes or No Magic. MagicGrid is a methodology brand of No Magic, now part of Dassault Systemes. Every entry links to a legitimate public source; this list does not host copies of the MagicGrid Book of Knowledge or other copyrighted material.

Then Contents TOC and nine content sections. Section minimums:

| Section | Minimum entries | Contents |
|---|---|---|
| Official Resources | 4 | docs.nomagic.com hub, 3DS training catalog, the official MagicGrid course pages |
| Books and Formal Publications | 2 | BoK via Goodreads or publisher page, edition-2 material as verified |
| Papers and Case Studies | 12 | INCOSE, Wiley, Springer, ACM papers with DOIs, from the research scan and OpenAlex follow-ups |
| Training and Courses | 4 | partner courses and seminars beyond the official catalog |
| Videos and Talks | 10 | the seven YouTube URLs from the research scan plus vendor channel and INCOSE talks |
| Example Models | 2 | public MagicGrid sample models, starting with `sysml-magicgrid-vccs` |
| Tool Support | 3 | CATIA Magic product family, Cameo Systems Modeler, related vendor product pages |
| Community | 3 | INCOSE venues, LinkedIn practitioner circles, durable forums if any verify |
| Related Methodologies | 5 | one-line pointers each for OOSEM, Harmony-SE, SYSMOD, Arcadia/Capella, plus the sister list |

Minimum sum: 45 entries, five above the 40-entry floor. Entry format, sorting, and the one-sentence factual description rule match the template exactly. Each URL appears in exactly one content section; the intro cross-link is not a content entry. Descriptions name vendor affiliation where an author or presenter is No Magic or Dassault staff, so readers can weigh the source (the same affiliation-naming rule is a contributing criterion, so future PRs stay governed). The README ends with a Contributing section linking contributing.md, mirroring the template.

## Skeleton port plan

| File | Action | Changes from template |
|---|---|---|
| .github/workflows/lint.yml | Copy, strip comment | Drop the header comment that cites "the repo spec for P9" (that document does not ship); body stays verbatim |
| .github/workflows/links.yml | Adapt | Drop the same P9 header comment; add `--accept '200,204,301,308,403'` to the lychee args so CI matches the local gate. Weekly and PR scans stay advisory on exit code only; the CHANGELOG 403 allowlist is enforced at the local publication gate, not by the report issue |
| .github/workflows/stale.yml | Copy, strip comment | Drop the P9 header comment; body stays verbatim (the grep reads README.md generically) |
| docs/site.css | Copy verbatim | None |
| docs/.nojekyll | Copy verbatim | None; empty file, keeps Pages from running Jekyll |
| .markdownlint-cli2.jsonc | Copy verbatim | None; MD013 off, the markdownlint gate needs it |
| LICENSE | Copy | None; CC0 1.0 Universal |
| contributing.md | Adapt | Keep structure (criteria, entry format, local commands, maintenance). Rename the H1 from "Contributing to Awesome SysML v2" to "Contributing to Awesome MagicGrid MBSE". Rewrite criteria for MagicGrid scope: method relevance required, generic SysML and generic MBSE excluded, CSS/JS grid layout libraries excluded explicitly, registration-walled links allowed only when they are the canonical source (for example official training), each URL appears in at most one content section (the intro sister-list cross-link is exempt, mirroring the README plan), and descriptions name vendor affiliation where the author or presenter is No Magic or Dassault staff. Keep the template's five-criterion order with criterion 4 as the 24-month freshness rule carrying the foundational-value exception, so stale.yml's criterion-4 reference stays valid. The local-commands section rewrites the lychee line to `lychee --accept '200,204,301,308,403' README.md`, matching the publication gate |
| CODE_OF_CONDUCT.md | Adapt | Contact and profile URL references only; the template has no repo-name string |
| SECURITY.md | Copy verbatim | None; the template has no repo-name strings |
| CITATION.cff | Fresh | Title "Awesome MagicGrid MBSE", author JG Systems Consulting Ltd, `license: CC0-1.0`, repository-code set to the final URL before publication |
| CHANGELOG.md | Fresh | 1.0.0 entry: initial public release, 45+ entries, clean lychee run recorded |
| docs/index.html | Adapt | See docs site plan |
| README.md | Fresh | Intro, disclaimer, TOC, nine sections per README plan |

Before copying the workflows, confirm with a grep that they still contain no `awesome-sysml-v2` string (true this session). If the template gains repo-specific strings before execution, adapt those lines instead.

## Content seeding plan

Sourcing order: URLs already in the research file first, then expansion passes (OpenAlex body mentions of MagicGrid, the vendor YouTube channel, INCOSE proceedings search, partner training catalogs). Every entry passes the seed-time verification rule before it lands in the README:

- Accepted: HTTP 200; 301 or 308 that lands on the right page (confirm the final URL still matches the intended resource; lychee status alone is not enough); 403 only when the URL is the canonical vendor source known to block bots.
- Rejected: 404, repeated timeouts, parked or squatted domains, dead DOIs (DOI resolution checked, not assumed).
- Method: local `lychee --accept '200,204,301,308,403' README.md` with `GITHUB_TOKEN` exported for the zero-broken gate. Separately extract every 403 (a second lychee pass without 403 in the accept set, or `--format json` / verbose output grepped for status 403), diff that set against the CHANGELOG accepted-403 list, and fail if any 403 is off-list. The 403 accept applies only to bot-blocked canonical URLs (DOIs resolving to Wiley, named vendor pages) on that list. Manual checks cover URLs lychee cannot classify and redirect landing pages. The clean run output is noted in the CHANGELOG 1.0.0 entry.

Bucket-specific rules:

- Books: link Goodreads, publisher, or library catalog pages. Never link or host BoK PDFs, and never link aggregator pirate copies.
- Papers: DOI links are canonical and stable even when paywalled. Descriptions state what the paper covers so readers judge the click.
- Official and tools: link only pages verified reachable in this session's research or at seed time. Never construct deep documentation paths.
- Related Methodologies: one entry per peer methodology, one factual sentence, linked to its canonical description page or paper. These are pointers, not coverage.

## Automation plan

Copy the three workflows after stripping the header comment that cites "the repo spec for P9". lint.yml and stale.yml bodies stay verbatim. links.yml body takes one adaptation: the lychee args gain `--accept '200,204,301,308,403'` so the weekly and PR scans match the local zero-broken gate. The CHANGELOG 403 allowlist is enforced only at the local publication gate (step 4); accepted 403s exit zero under that accept set, so the weekly report issue does not surface 403 drift. Nothing else needs renaming because the workflows reference only README.md and contributing.md, use relative paths, and pin actions by commit SHA.

- lint.yml gates every PR and push to main: `awesome-lint@2.3.0` on README.md, markdownlint on README.md and contributing.md, Node 20. First push must pass.
- links.yml runs lychee weekly (Monday 18:00 UTC) and on PRs, advisory only, opening or updating a "Link Checker Report" issue on failure.
- stale.yml publishes a monthly freshness report of README GitHub repos with no push in 24 months, advisory only, with the foundational-value exception from contributing.md.

One nuance for the local lint gate: awesome-lint has repo-aware checks that need a git repository and, for full repo-info checks, a GitHub remote. The publication plan orders `git init` before the local checks and treats remaining repo-info warnings as resolved once the remote exists and CI lint passes on first push.

## Docs site plan

Adapt docs/index.html; copy site.css verbatim.

- Replace every identity string: title "Awesome MagicGrid MBSE - JGS", description, canonical URL `https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/`, og and twitter meta, JSON-LD name, URL, description, and license link.
- Masthead: `DOC-ID: JGS-AWESOME-MAGICGRID-MBSE`, `LICENCE: CC0` (the template says MIT; do not copy that).
- Body rewrite: every visible prose block in the template page (hero, what-it-is, contribute, maintenance sections) is rewritten with MagicGrid content; swapping identity strings alone is not enough, and no SysML v2 prose ships.
- Category map table: one row per content section, each linking to the corresponding README anchor in the new repo.
- Repository links section: README, contributing.md, repo root, issues, docs/ source.
- Footer: "CC0 Licence" linking the new repo LICENSE.
- v1 omits og:image and twitter:image tags and does not copy social-card.jpg or social-card.png. Restore both when a MagicGrid-branded card is generated (later work).

Pages publishes from the main branch, /docs directory, enabled after the first push (publication plan).

## Cross-linking plan

- New repo README: intro sentence linking awesome-sysml-v2 (README plan above) plus a Related Methodologies entry for the sister list.
- awesome-sysml-v2 README: one line under the intro paragraph, no new section and no TOC change: "For the MagicGrid MBSE methodology, see the sister list [awesome-magicgrid-mbse](https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse)."
- The template edit goes through that repo's normal flow; its lint gates run on push to main and must pass. Change is one line, so risk is low.

## Publication plan

Steps 1 through 4 are the local gate. Steps 5 through 10 run only after the gate is clean.

1. Build the full skeleton and seeded README (45+ entries under section minimums).
2. `git init`, branch main, initial commit.
3. Local checks from the repo root with `GITHUB_TOKEN=$(gh auth token)` exported: `npx awesome-lint@2.3.0 README.md`, `npx markdownlint-cli2 "README.md" "contributing.md"`, `lychee --accept '200,204,301,308,403' README.md` (same accept set as the seeding method).
4. Fix findings and rerun until clean. Lychee must report zero broken links under that accept set. Separately extract every 403 (second lychee pass without 403 in the accept set, or `--format json` / verbose output grepped for status 403), diff that set against the CHANGELOG accepted-403 list, and fail the gate if any 403 is off-list. Do not rely on the accept-set run's default output for the allowlist diff: accepted 403s are reported as OK and exit zero.
5. `gh repo create jgsystemsconsulting/awesome-magicgrid-mbse --public --source . --remote origin --push`.
6. Confirm the lint workflow is green on the first push to main; this closes out any repo-info warning from step 3.
7. Enable Pages from main /docs (`gh api` or repo settings), confirm the site serves at the canonical URL.
8. Set the homepage: `gh repo edit --homepage "https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/"`.
9. Add topics for search disambiguation against CSS/JS magic-grid libraries: `mbse`, `sysml`, `magicgrid`, `awesome-list` (repeat `--add-topic` per topic).
10. Apply the one-line cross-link edit in awesome-sysml-v2 and push through its normal gates.

Note for prose checkers: the `--` tokens in steps 5, 8, and 9 are command-line flags inside code spans, not prose dashes; they stay.

## Acceptance criteria

- `awesome-lint@2.3.0` passes on README.md; repo-info checks green once the remote exists and CI has run.
- `markdownlint-cli2` passes on README.md and contributing.md.
- Lychee on the seeded README reports zero broken links under the documented accept set; accepted 403s are listed in the CHANGELOG.
- 40+ verified entries; every section meets its minimum (sum 45); every entry passed the seed-time verification rule.
- README carries the disclaimer: no affiliation, trademark note, no copyrighted-material hosting.
- Descriptions name vendor affiliation for No Magic or Dassault staff authors and presenters where applicable.
- Cross-links present in both directions: new README to awesome-sysml-v2, awesome-sysml-v2 README to the new repo.
- CI lint workflow green on first push to main.
- Pages live at `https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/`; repo homepage field set; topics set.
- No CSS/JS magic-grid layout library appears anywhere in the list, and contributing.md excludes them explicitly.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Vendor link rot: guessed doc paths 404, old nomagic.com paths 403 | Link only URLs verified in the research scan or at seed time; prefer top-level hubs (3ds.com product pages, docs.nomagic.com root); never construct documentation paths; weekly lychee catches non-403 drift, and the local publication gate catches 403 drift against the CHANGELOG allowlist |
| Paywalled papers dominate the papers bucket | Accepted: DOIs are canonical and stable; descriptions carry enough context to judge before clicking; the videos bucket keeps the list usable without subscriptions |
| Name collision with CSS/JS magic-grid libraries | Repo name already disambiguates; explicit exclusion criterion in contributing.md; topics `mbse` and `sysml` fix search intent |
| Single-vendor gravity reads as marketing | Disclaimer at the top; one-sentence factual descriptions with vendor affiliation named; Related Methodologies gives independent breadth |
| Copyright exposure from BoK material | Link Goodreads or publisher pages only; contributing.md forbids hosting and pirate-aggregator links |
| Maintenance load with few organic community PRs | Advisory stale report with the foundational-value exception; the weekly lychee scan automates the highest-chore task |
| awesome-lint repo-aware checks fail before a remote exists | Publication order: `git init` before local lint; remaining repo-info warnings close when CI lint passes after push |

## Version one scope and later work

Must-have in v1: the full repo structure, 45+ verified entries, three workflows, community files with consistent CC0, adapted docs site, both cross-links, publication after the local gate, Pages and homepage set.

Deferred, in rough priority order:

1. Social card generation for MagicGrid, then restore og:image and twitter:image in docs/index.html.
2. awesome.re submission, once the list has public history and a clean CI record.
3. Grow the papers bucket past 12 via OpenAlex body-mention culling.
4. Curate non-English tutorial series (Korean CATIA Magic and MagicGrid videos exist) if they verify.
5. Revisit folding into a public awesome-mbse if `jgsystemsconsulting/awesome-mbse` goes public; until then the standalone repo stands.
