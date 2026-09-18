# Spec: companion-docs-site (P2, awesome-sysml-v2)

- Date: 2026-09-16
- Status: ready for plan
- Work package: P2 of the awesome-sysml-v2 packages plan
- Baseline: HEAD 4c68451 (P4 landed; contributing.md carries the Maintenance section)

## Problem statement

The repo is public and has no web landing page. `homepageUrl` is empty (live-checked this round), so the repo card shows no site link. The org's sibling repos each ship a hand-authored static site under `docs/`, served by GitHub Pages from `main:/docs`, following a shared family pattern: masthead strip, full head metadata (OG/Twitter/JSON-LD), anchor nav, dark CSS-var styling. awesome-sysml-v2 needs the same companion site so it matches the family and gives visitors a presentable entry point that links back into the README as the source of truth.

## Goals

1. Ship `docs/` as a static site: exactly `index.html`, `site.css`, `.nojekyll` (plus the pre-existing `docs/superpowers/` tree, which stays). Nothing else new.
2. Match the org family pattern: head inventory incl. OG/Twitter/JSON-LD, masthead strip `CLASSIFICATION: PUBLIC / LICENCE: MIT / DOC-ID: JGS-AWESOME-SYSML-V2 / REV: 1.0`, anchor nav, dark CSS-var styling.
3. Present the repo, not duplicate it: hero (name, badge, description), What it is, Category map (11 categories, one-line each, deep link to the GitHub README anchor), How to contribute, Maintenance cadence, Repository links using absolute blob URLs.
4. Enable GitHub Pages from `main:/docs` via the REST API; set `homepageUrl` to the Pages URL.
5. Keep README as source of truth. No entry lists on the site. No entry counts. No build system. No JavaScript dependencies.

## Non-goals

- Entry-list duplication on the site (README owns the lists).
- Live or hand-mirrored entry counts (drift trap; SE packs precedent).
- `og:image` generation; the head omits `og:image` rather than faking one (documented limitation).
- CoC/SECURITY files (P5), awesome-list submission (P3), workflow changes, README rewrites.
- Moving or gitignoring `docs/superpowers/` process trees (rejected mid-pipeline; accepted residual, see Limitations).

## Design

### File inventory (complete)

```
docs/
  index.html
  site.css
  .nojekyll
```

That is the whole package. No build step, no minifier, no JS, no fonts served locally (JetBrains Mono and Inter load from Google Fonts in the head, same as the sibling).

### index.html section structure

Single page, in this order, each with an anchor id:

1. Masthead strip (no anchor): `CLASSIFICATION: PUBLIC` | `LICENCE: MIT` | `DOC-ID: JGS-AWESOME-SYSML-V2` | `REV: 1.0`.
2. `<nav class="site">` anchor nav: What it is, Categories, Contribute, Maintenance, Links.
3. Hero: `Awesome SysML V2`, awesome.re badge (image src https://awesome.re/badge.svg linking to https://awesome.re), one-line description: "A curated list of SysML v2 resources: specifications, tools, libraries, example models, and learning material."
4. `#what` "What it is": two or three sentences. The repo is an awesome-style curated list for Systems Modeling Language v2. It collects specifications, official implementations, editor and tooling support, parsing SDKs, validation tooling, example models, learning resources, deployment artifacts, commercial tools, and v1 migration paths. Entries are maintained in the README; this site is a front door, not a mirror.
5. `#categories` "Category map": an HTML table, one row per category, two columns (Category, About). Each category name links to the corresponding GitHub README anchor (absolute blob URL). The About column is a qualitative one-liner, never a count. The 11 rows, fixed content:
   - Specifications and Standards -> https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#specifications-and-standards . "The normative documents: the OMG SysML v2 spec family, related OMG standards, and the OMG tools directory."
   - Official Implementations -> .../README.md#official-implementations . "Reference implementations of the SysML v2 standard: the pilot implementation, API services, clients, and releases."
   - Editors and Language Tooling -> .../README.md#editors-and-language-tooling . "IDEs, text-editor extensions, and language tooling for authoring SysML v2 textual models."
   - Modeling and Visualization -> .../README.md#modeling-and-visualization . "Tools for building models and rendering them: diagramming, visualization, and model-based environments."
   - Parsers, SDKs, and API Clients -> .../README.md#parsers-sdks-and-api-clients . "Libraries and SDKs for reading, writing, and scripting against SysML v2 from code."
   - Validation and Analysis -> .../README.md#validation-and-analysis . "Tooling for checking models: constraint checking, analysis, and verification support."
   - Example Models -> .../README.md#example-models . "Working SysML v2 models to learn from and build on."
   - Learning Resources -> .../README.md#learning-resources . "Tutorials, talks, courses, and documentation for getting up to speed on SysML v2."
   - Deployment and Containers -> .../README.md#deployment-and-containers . "Packaged and containerized distributions of SysML v2 tooling for quick setup."
   - Commercial Tools -> .../README.md#commercial-tools . "Vendor products with SysML v2 support, commercial licensing and all."
   - Migrating from SysML v1 -> .../README.md#migrating-from-sysml-v1 . "Guides and tooling for moving existing v1 models and practice to v2."
   (All URLs expand to the full `https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#<anchor>` form; abbreviated here for spec readability only.)
6. `#contribute` "How to contribute": short summary. PRs welcome; entry additions go through the README via a pull request; the process, entry format, and acceptance criteria live in contributing.md, linked as an absolute blob URL (https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md).
7. `#maintenance` "Maintenance cadence": short summary. The cadence (review cycles, link checking, entry curation) is documented in contributing.md; link the same absolute blob URL, straight to the maintenance heading: https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md#maintenance
8. `#links` "Repository links": list with these exact absolute URLs: README (https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md), contributing.md (https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md), repo root (https://github.com/jgsystemsconsulting/awesome-sysml-v2), issues (https://github.com/jgsystemsconsulting/awesome-sysml-v2/issues), this site's source directory (https://github.com/jgsystemsconsulting/awesome-sysml-v2/tree/main/docs). No relative repo-file links anywhere on the page (Pages-root 404 trap).
9. Footer: MIT licence line linking the blob LICENSE file (https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/LICENSE), plus a one-line note that the README is the source of truth for all entries.

### Head metadata (exact values)

- `<meta charset="utf-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, `<meta name="color-scheme" content="dark">`.
- Google Fonts link in the head (before site.css): `<link rel="preconnect" href="https://fonts.googleapis.com">`, `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`, and the family stylesheet for JetBrains Mono 400;700 and Inter 400;600 — same families as the sibling site.
- `<title>Awesome SysML V2 - JGS</title>`
- `<meta name="description" content="A curated list of Systems Modeling Language (SysML) v2 resources: specifications, implementations, tooling, example models, and learning material.">`
- `<link rel="canonical" href="https://jgsystemsconsulting.github.io/awesome-sysml-v2/">`
- OG: `og:type` website, `og:url` the Pages URL, `og:title` and `og:description` matching title/description above. `og:image` is omitted (limitation, see below). Twitter: `twitter:card` set to `summary`, plus `twitter:title` and `twitter:description` matching the OG values. No `twitter:image`.
- JSON-LD `SoftwareApplication`: name `Awesome SysML V2`, `applicationCategory` `DeveloperApplication`, `operatingSystem` `Web`, `url` https://github.com/jgsystemsconsulting/awesome-sysml-v2 (the software's home is the repo; the site canonical is the Pages URL — the split is intentional), `description` matching the meta description, `license` https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/LICENSE .

### site.css approach

Adapted from jgs-archi-skills/docs/site.css (60 lines), carried over nearly as-is:

- Carried over unchanged: CSS custom properties (`--ink`, `--line`, `--mute`, `--paper`), dark values, font stack (JetBrains Mono for code/strip, Inter for body, Google Fonts import), `.wrap` max-width 1200px, base body/link styling, masthead strip styling, nav rules.
- New, small: a minimal table rule set for the category map (border-collapse, row borders in `--line`, padding), since the sibling has no table. Nothing else added. Target is roughly 70 lines.

### Pages enablement and homepageUrl (exact commands)

```
gh api -X POST repos/jgsystemsconsulting/awesome-sysml-v2/pages -f "source[branch]=main" -f "source[path]=/docs"
gh repo edit jgsystemsconsulting/awesome-sysml-v2 --homepage https://jgsystemsconsulting.github.io/awesome-sysml-v2/
```

Run after the docs/ files are merged to main. If the POST returns 409 (Pages already configured), verify the existing config serves main:/docs and proceed.

## Verification steps

1. Files exist: `docs/index.html`, `docs/site.css`, `docs/.nojekyll`, and nothing else new under docs/ outside docs/superpowers/. `.nojekyll` is empty.
2. Head-element checks (HTML sanity, no YAML so no parse gate): index.html contains charset utf-8, the viewport and color-scheme metas, the Google Fonts links, the canonical URL, the masthead strip tokens `JGS-AWESOME-SYSML-V2` and `REV: 1.0`, all six section anchors (`id="top"` on the hero section, plus `id="what"`, `id="categories"`, `id="contribute"`, `id="maintenance"`, `id="links"`), a JSON-LD block, and exactly one `<style>`-free structure with site.css linked. No `og:image` tag present (intentional); no `<script>` tags other than the JSON-LD block (no JavaScript).
3. CSS-var check: site.css defines the `--ink`, `--line`, `--mute`, `--paper` custom properties and the `.wrap` rule.
4. No-duplication check: index.html contains no `<li>` entry lists from the README; the only table is the 11-row category map; no digits-only count strings.
5. No-relative-link check: `grep -nE 'href="(\./|\.\./)?(README|contributing)\.md'` on index.html returns nothing; every repo-file href starts with `https://github.com/jgsystemsconsulting/awesome-sysml-v2/`.
6. Pages POST returns success (or 409 with config confirmed). Then anonymous live check: `curl -s -o /dev/null -w "%{http_code}" https://jgsystemsconsulting.github.io/awesome-sysml-v2/` returns 200, and the body contains the masthead DOC-ID string.
7. homepageUrl check: `gh api repos/jgsystemsconsulting/awesome-sysml-v2 --jq .homepage` returns the Pages URL.
8. README.md and contributing.md are untouched by P2 (git diff shows no changes to either). homepageUrl is a repo setting, not a file edit.

## Sync policy

The site's category one-liners are qualitative; they carry no counts and no dates, so drift risk is minimal by construction. The only sync trigger is structural: if a README category is added, removed, or renamed, the category map must be updated in the same change that edits the README's Contents list. Review cadence: fold a site check into the next repo review loop after any README structural change; no scheduled re-render exists because there is no build step.

## Limitations

- No `og:image`: link previews fall back to text-only cards. Generating a 1200x630 image is out of scope (no build system, no binary assets); this is recorded rather than faked.
- `docs/superpowers/` process trees are committed and will be web-served under the Pages URL. They are already public in the repo; siblings gitignored theirs, ours are tracked, and moving them mid-pipeline is rejected. Accepted residual.
- `docs/` site files escape lint scopes (lint.yml globs README and contributing only) and lychee currently checks nothing: links.yml runs lychee with no file operands (backlog b-17), so it exits 2 before checking any URL. Anchor-drift detection is therefore manual until b-17 lands; the weekly crawl cannot be claimed as a mitigation. Accepted residual; manual verification above covers the initial state.

## Risks

- Anchor drift: if README category headings change slug, the site's deep links 404. Mitigated by the sync policy and manual anchor checks after README structural changes; lychee currently checks nothing (b-17), so it is not a mitigation until that lands.
- Pages POST ordering: enabling Pages before docs/ lands on main fails. Mitigated by sequencing (merge first, POST second).
- First Pages build latency: the live URL can lag the POST by a minute or two; verification step 6 may need one retry before declaring failure.

## Acceptance criteria

1. `docs/` contains exactly index.html, site.css, .nojekyll (plus the pre-existing docs/superpowers/ tree).
2. Acceptance criteria: index.html carries the masthead strip with DOC-ID JGS-AWESOME-SYSML-V2 and REV 1.0, anchor nav with all five targets, hero with badge and description, the What-it-is section, the 11-row category map with absolute blob deep links, contribute, maintenance, and repository-links sections, footer with the MIT licence blob link and the source-of-truth note, and the head metadata set defined above (charset, viewport, color-scheme, fonts links, title, description, canonical, OG without og:image, twitter:card summary with title/description, JSON-LD).
3. Pages live URL returns 200 anonymously and serves the masthead content.
4. homepageUrl is set to the Pages URL on the repo.
5. No entry-list duplication, no entry counts, no relative repo-file links anywhere on the site.
6. README.md and contributing.md are byte-identical to their pre-P2 state.

## Research

research: skipped (no-open-world-questions; replicates the org's own site pattern; Pages via platform API)

Gate inputs: context document at docs/superpowers/context/2026-09-16-companion-docs-site-context.md (verdict CONTEXT_COMPLETE, 13 claims, 0 conflicted); round log at docs/superpowers/research/2026-09-16-companion-docs-site-research-log.md. Sibling exemplars verified: jgs-archi-skills/docs (external site.css, 60 lines) and jgs-se-knowledge-packs/docs (inline variant). Repo state live-checked: public, homepageUrl empty.
