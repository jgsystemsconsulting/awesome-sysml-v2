# Companion docs site (P2) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship docs/ as a hand-authored static companion site (index.html, site.css, .nojekyll), enable GitHub Pages from main:/docs, and set homepageUrl, without touching README.md or contributing.md.

**Architecture:** A single static page in the JGS org family pattern: masthead strip, anchor nav, hero, five anchored sections, footer, with dark CSS-var styling adapted from the jgs-archi-skills sibling. The site presents the repo and deep links into the GitHub README using absolute blob URLs; the README stays the source of truth. Pages is enabled through the REST API only after the site files are committed to main.

**Tech Stack:** Static HTML and CSS only. No build system, no JavaScript, no locally served fonts (JetBrains Mono and Inter load from Google Fonts in the head). GitHub CLI (gh) for Pages enablement and repo settings.

**Spec:** docs/superpowers/specs/2026-09-16-companion-docs-site.md (the plan argues from the spec; executors read both)

## Global Constraints

- Baseline: HEAD 4c68451. No task commits before Task 5. Nothing in this plan pushes to origin.
- research: skipped (no-open-world-questions; replicates the org's own site pattern; Pages via platform API)
- Gate inputs: context document docs/superpowers/context/2026-09-16-companion-docs-site-context.md (verdict CONTEXT_COMPLETE, 13 claims, 0 conflicted); round log docs/superpowers/research/2026-09-16-companion-docs-site-research-log.md.
- The file inventory is complete and closed: docs/index.html, docs/site.css, docs/.nojekyll. Nothing else new under docs/ outside the pre-existing docs/superpowers/ tree.
- No build step, no minifier, no JavaScript, no locally served fonts, no og:image, no twitter:image.
- No entry lists on the site, no entry counts, no digits-only count strings. The only table is the 11-row category map.
- No relative repo-file links anywhere on the page. Every repo-file href is an absolute URL under https://github.com/jgsystemsconsulting/awesome-sysml-v2/.
- Masthead strip tokens exact: CLASSIFICATION: PUBLIC | LICENCE: MIT | DOC-ID: JGS-AWESOME-SYSML-V2 | REV: 1.0.
- README.md and contributing.md must stay byte-identical to their pre-P2 state (spec verification step 8, AC6).
- Commit message exact: `Add companion docs site` (one commit, Task 5).
- Sync policy (spec, no task needed): the category one-liners carry no counts and no dates, so the only sync trigger is structural. If a README category is added, removed, or renamed, update the site's category map in the same change that edits the README's Contents list.
- Commands are Git Bash on Windows. All paths are relative to the repo root C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2.

## Codebase context

Live-checked at plan time against the pinned baseline:

- Local main is at 4c6845142ec40df8bf2f0760de9ae0aac80f0282 and is ahead 6 of origin/main (af07711). The push is the parent's job; this plan never pushes.
- docs/ exists on disk and contains only docs/superpowers/ (specs, plans, context, research, reviews, packages, backlog.md). Nothing under docs/ is tracked at HEAD or on origin/main; git status reports `?? docs/`. The dispatch assumption that docs/superpowers/ is already tracked does not match this state, so Task 5 stages only the three site files and leaves docs/superpowers/ untracked.
- README.md line 1: `# Awesome SysML V2 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)`. Thirteen `##` headings: Contents, the 11 categories in spec order, Contributing (line 126).
- contributing.md line 42: `## Maintenance`.
- .github/workflows/ contains exactly links.yml, lint.yml, stale.yml. Workflow changes are a spec non-goal.
- Styling tokens come from the sibling jgs-archi-skills/docs/site.css (fetched live via `gh api repos/jgsystemsconsulting/jgs-archi-skills/contents/docs/site.css`): the --ink/--line/--mute/--paper families with dark values, JetBrains Mono for headings and strips, Inter for body, `.wrap` at max-width 1200px, the masthead and nav.site rules, and the sibling's table.data rule set, trimmed to what this page uses.

## File structure

- docs/index.html (create): the whole page. Head metadata set, masthead, anchor nav, hero, #what, #categories (11-row table), #contribute, #maintenance, #links, footer.
- docs/site.css (create): dark CSS-var styling. Family tokens carried over from the sibling, plus a small table rule set.
- docs/.nojekyll (create): empty marker file so Pages serves docs/ as-is.

---

## Task 1: Pre-flight gate

**Files:** none modified. Read-only checks only.

**Interfaces:**
- Consumes: the repo at HEAD.
- Produces: the green-light baseline every later task assumes. If any check fails, STOP and report the actual state; do not start Task 2.

**Model:** flash

- [ ] **Step 1: Verify HEAD is the pinned baseline**

Run:
```bash
git rev-parse HEAD
```
Expected: `4c6845142ec40df8bf2f0760de9ae0aac80f0282`.

- [ ] **Step 2: Verify docs/ holds only the process tree**

Run:
```bash
find docs -maxdepth 1 -mindepth 1
```
Expected: exactly `docs/superpowers` and nothing else (site files absent).

- [ ] **Step 3: Verify README.md and contributing.md are at the expected state and clean**

Run:
```bash
head -1 README.md
grep -c '^## ' README.md
grep -n '^## Maintenance' contributing.md
git status --porcelain README.md contributing.md
```
Expected: line 1 is `# Awesome SysML V2 [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)`; heading count is 13; the Maintenance heading is at contributing.md:42; porcelain output is empty.

- [ ] **Step 4: Verify the workflows dir is unchanged**

Run:
```bash
ls .github/workflows
git status --porcelain .github/
```
Expected: exactly `links.yml`, `lint.yml`, `stale.yml`; porcelain output is empty.

Done when: all four checks match. Any mismatch: STOP, report the actual state, and await parent instruction.

## Task 2: Create docs/index.html

**Files:**
- Create: `docs/index.html`

**Interfaces:**
- Consumes: nothing.
- Produces: the complete page that Tasks 3-4 build on. Section anchors: `id="top"` on the hero, plus `id="what"`, `id="categories"`, `id="contribute"`, `id="maintenance"`, `id="links"`. CSS classes used (each must exist in Task 3's site.css): `wrap`, `masthead`, `site` on the nav, `hero`, `badge`, `shead`, `lead`, `data` on the table, `foot-note`.

**Model:** flash (complete content below; this is a transcription task)

- [ ] **Step 1: Write the file with exactly this content**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<title>Awesome SysML V2 - JGS</title>
<meta name="description" content="A curated list of Systems Modeling Language (SysML) v2 resources: specifications, implementations, tooling, example models, and learning material.">
<link rel="canonical" href="https://jgsystemsconsulting.github.io/awesome-sysml-v2/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="site.css">
<meta property="og:type" content="website">
<meta property="og:url" content="https://jgsystemsconsulting.github.io/awesome-sysml-v2/">
<meta property="og:title" content="Awesome SysML V2 - JGS">
<meta property="og:description" content="A curated list of Systems Modeling Language (SysML) v2 resources: specifications, implementations, tooling, example models, and learning material.">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="Awesome SysML V2 - JGS">
<meta name="twitter:description" content="A curated list of Systems Modeling Language (SysML) v2 resources: specifications, implementations, tooling, example models, and learning material.">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Awesome SysML V2",
  "applicationCategory": "DeveloperApplication",
  "operatingSystem": "Web",
  "url": "https://github.com/jgsystemsconsulting/awesome-sysml-v2",
  "description": "A curated list of Systems Modeling Language (SysML) v2 resources: specifications, implementations, tooling, example models, and learning material.",
  "license": "https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/LICENSE"
}
</script>
</head>
<body>
<div class="masthead">
  <div class="wrap">
    <span>CLASSIFICATION: PUBLIC</span>
    <span>LICENCE: MIT</span>
    <span>DOC-ID: JGS-AWESOME-SYSML-V2</span>
    <span>REV: 1.0</span>
  </div>
</div>
<nav class="site">
  <div class="wrap">
    <a href="#what">What it is</a>
    <a href="#categories">Categories</a>
    <a href="#contribute">Contribute</a>
    <a href="#maintenance">Maintenance</a>
    <a href="#links">Links</a>
  </div>
</nav>
<section class="hero" id="top">
  <div class="wrap">
    <a class="badge" href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
    <h1>Awesome SysML V2</h1>
    <p>A curated list of SysML v2 resources: specifications, tools, libraries, example models, and learning material.</p>
  </div>
</section>
<section id="what">
  <div class="wrap">
    <div class="shead"><h2>What it is</h2></div>
    <p class="lead">Awesome SysML V2 is an awesome-style curated list for the Systems Modeling Language v2. It collects specifications, official implementations, editor and tooling support, parsing SDKs, validation tooling, example models, learning resources, deployment artifacts, commercial tools, and v1 migration paths. Entries are maintained in the <a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md">README</a>; this site is a front door, not a mirror.</p>
  </div>
</section>
<section id="categories">
  <div class="wrap">
    <div class="shead"><h2>Category map</h2></div>
    <table class="data">
      <thead>
        <tr><th scope="col">Category</th><th scope="col">About</th></tr>
      </thead>
      <tbody>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#specifications-and-standards">Specifications and Standards</a></td><td>The normative documents: the OMG SysML v2 spec family, related OMG standards, and the OMG tools directory.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#official-implementations">Official Implementations</a></td><td>Reference implementations of the SysML v2 standard: the pilot implementation, API services, clients, and releases.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#editors-and-language-tooling">Editors and Language Tooling</a></td><td>IDEs, text-editor extensions, and language tooling for authoring SysML v2 textual models.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#modeling-and-visualization">Modeling and Visualization</a></td><td>Tools for building models and rendering them: diagramming, visualization, and model-based environments.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#parsers-sdks-and-api-clients">Parsers, SDKs, and API Clients</a></td><td>Libraries and SDKs for reading, writing, and scripting against SysML v2 from code.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#validation-and-analysis">Validation and Analysis</a></td><td>Tooling for checking models: constraint checking, analysis, and verification support.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#example-models">Example Models</a></td><td>Working SysML v2 models to learn from and build on.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#learning-resources">Learning Resources</a></td><td>Tutorials, talks, courses, and documentation for getting up to speed on SysML v2.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#deployment-and-containers">Deployment and Containers</a></td><td>Packaged and containerized distributions of SysML v2 tooling for quick setup.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#commercial-tools">Commercial Tools</a></td><td>Vendor products with SysML v2 support, commercial licensing and all.</td></tr>
        <tr><td><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md#migrating-from-sysml-v1">Migrating from SysML v1</a></td><td>Guides and tooling for moving existing v1 models and practice to v2.</td></tr>
      </tbody>
    </table>
  </div>
</section>
<section id="contribute">
  <div class="wrap">
    <div class="shead"><h2>How to contribute</h2></div>
    <p class="lead">Pull requests are welcome. Entry additions go through the <a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md">README</a> via a pull request; the process, entry format, and acceptance criteria live in <a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md">contributing.md</a>.</p>
  </div>
</section>
<section id="maintenance">
  <div class="wrap">
    <div class="shead"><h2>Maintenance cadence</h2></div>
    <p class="lead">Review cycles, link checking, and entry curation run on the cadence documented in <a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md#maintenance">contributing.md</a>.</p>
  </div>
</section>
<section id="links">
  <div class="wrap">
    <div class="shead"><h2>Repository links</h2></div>
    <ul>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md">README</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md">contributing.md</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2">Repository root</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/issues">Issues</a></li>
      <li><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/tree/main/docs">Site source (docs/)</a></li>
    </ul>
  </div>
</section>
<footer>
  <div class="wrap">
    <p class="foot-note"><a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/LICENSE">MIT Licence</a>. The <a href="https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md">README</a> is the source of truth for all entries.</p>
  </div>
</footer>
</body>
</html>
```

- [ ] **Step 2: Spot-check the file landed intact**

Run:
```bash
wc -l docs/index.html
grep -c '<tr>' docs/index.html
grep -c 'id="top"' docs/index.html
```
Expected: exactly 118 lines (the transcription is fixed content); 12 table rows; 1 hero anchor. The full battery runs in Task 4.

Done when: docs/index.html exists with the exact content above and the three spot checks pass. Do not commit; Task 5 owns the single commit.

## Task 3: Create docs/site.css and docs/.nojekyll

**Files:**
- Create: `docs/site.css`
- Create: `docs/.nojekyll`

**Interfaces:**
- Consumes: the class inventory from Task 2 (wrap, masthead, site, hero, badge, shead, lead, data, foot-note).
- Produces: styles for every class Task 2 uses, and the CSS custom properties `--ink`, `--line`, `--mute`, `--paper` that Task 4 checks.

**Model:** flash (complete content below)

- [ ] **Step 1: Write docs/site.css with exactly this content**

Adapted from jgs-archi-skills/docs/site.css: family tokens carried over, rules trimmed to what this page uses, and the sibling's table.data rule set kept for the category map.

```css
/* Copyright (c) 2026 JG Systems Consulting Ltd. Source: https://github.com/jgsystemsconsulting/awesome-sysml-v2. See LICENSE. */
/* SPDX-License-Identifier: MIT */
:root{
  --ink:#0a0a0b; --ink-2:#111113; --ink-3:#16171a;
  --line:#2a2d33; --line-2:#3a3e46;
  --mute:#6b7078; --mute-2:#8b9099;
  --text:#c7ccd3; --text-hi:#e8ebf0;
  --paper:#f4f2ec; --paper-ink:#0a0a0b;
  --mono:'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace;
  --sans:'Inter',ui-sans-serif,system-ui,sans-serif;
  --pad-x:clamp(24px,4vw,80px); --pad-section:clamp(48px,6vw,96px);
}
*{box-sizing:border-box;margin:0;padding:0;}
html{background:var(--ink);}
body{background:var(--ink);color:var(--mute-2);font:400 16px/1.7 var(--sans);-webkit-font-smoothing:antialiased;}
.wrap{max-width:1200px;margin:0 auto;padding:0 var(--pad-x);}
a{color:var(--text-hi);text-decoration:none;border-bottom:1px solid var(--line-2);}
a:hover{border-color:var(--paper);}
:focus-visible{outline:2px solid var(--paper);outline-offset:2px;}
h1,h2,h3{color:var(--text-hi);font-family:var(--mono);font-weight:700;letter-spacing:-0.02em;}
.masthead{border-bottom:1px solid var(--line);}
.masthead .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1.5rem;padding-top:14px;padding-bottom:14px;}
.masthead span{font:700 .625rem/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--mute);}
nav.site{border-bottom:1px solid var(--line);}
nav.site .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:.75rem 1.5rem;padding-top:12px;padding-bottom:12px;}
nav.site a{font:700 .6875rem/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;border:0;color:var(--mute-2);}
nav.site a:hover{color:var(--text-hi);}
.hero{padding:var(--pad-section) 0;border-bottom:1px solid var(--line);}
.hero h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.05;margin-bottom:1.25rem;}
.hero p{max-width:62ch;font-size:1.0625rem;color:var(--text);}
.hero .badge{display:inline-block;border-bottom:0;margin-bottom:1.5rem;}
.hero .badge img{display:block;}
section{padding:var(--pad-section) 0;border-bottom:1px solid var(--line);}
.shead{margin-bottom:2rem;}
.shead h2{font-size:clamp(1.4rem,3vw,2rem);}
.lead{max-width:70ch;color:var(--text);}
section ul{list-style:none;max-width:70ch;padding:0;}
section li{padding:.3rem 0;}
table.data{width:100%;border-collapse:collapse;font-size:.9375rem;}
table.data th,table.data td{text-align:left;vertical-align:top;padding:14px 16px;border-bottom:1px solid var(--line);}
table.data th{font:700 .6875rem/1.4 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--mute);background:var(--ink-3);}
table.data td{color:var(--text);}
footer{padding:var(--pad-section) 0;}
.foot-note{font:400 .8125rem/1.6 var(--mono);color:var(--mute);}
@media (max-width:860px){
  table.data{display:block;overflow:auto;}
}
```

- [ ] **Step 2: Create the empty .nojekyll marker**

Run:
```bash
printf '' > docs/.nojekyll
wc -c docs/.nojekyll
```
Expected: `0 docs/.nojekyll`.

- [ ] **Step 3: Spot-check the CSS vars and the .wrap rule**

Run:
```bash
grep -c -- '--ink:' docs/site.css
grep -c -- '--line:' docs/site.css
grep -c -- '--mute:' docs/site.css
grep -c -- '--paper:' docs/site.css
grep -c '^\.wrap{' docs/site.css
```
Expected: `1` for each of the four CSS vars; the anchored `^\.wrap{` count is also `1` (the base rule; the `.masthead .wrap{` and `nav.site .wrap{` descendant selectors do not match the line anchor).

Done when: both files exist, .nojekyll is empty, and the five spot checks each return 1. Do not commit.

## Task 4: Local verification battery (spec verification steps 1-5)

**Files:** none modified. Read-only checks over the three files from Tasks 2-3.

**Interfaces:**
- Consumes: docs/index.html, docs/site.css, docs/.nojekyll as written by Tasks 2-3.
- Produces: nothing. This is the gate before the Task 5 commit. On any failing check: fix the file, rerun the whole battery. Do not weaken a check to make it pass.

**Model:** flash

Run every check from the repo root. Expected values are in the comments.

- [ ] **Step 1: File inventory (spec step 1)**

```bash
find docs -maxdepth 1 -mindepth 1
```
Expected: exactly `docs/.nojekyll`, `docs/index.html`, `docs/site.css`, `docs/superpowers`. Nothing else new outside docs/superpowers/.

```bash
wc -c docs/.nojekyll
```
Expected: 0.

- [ ] **Step 2: Head-element checks (spec step 2)**

```bash
grep -c '<meta charset="utf-8">' docs/index.html                                         # 1
grep -c '<meta name="viewport" content="width=device-width, initial-scale=1">' docs/index.html  # 1
grep -c '<meta name="color-scheme" content="dark">' docs/index.html                      # 1
grep -c 'rel="preconnect" href="https://fonts.googleapis.com"' docs/index.html           # 1
grep -c 'rel="preconnect" href="https://fonts.gstatic.com" crossorigin' docs/index.html  # 1
grep -c 'family=JetBrains+Mono:wght@400;700' docs/index.html                             # 1
grep -c 'rel="canonical" href="https://jgsystemsconsulting.github.io/awesome-sysml-v2/"' docs/index.html  # 1
grep -c 'JGS-AWESOME-SYSML-V2' docs/index.html                                           # 1 (masthead strip)
grep -c 'REV: 1.0' docs/index.html                                                       # 1
grep -c 'id="top"' docs/index.html                                                       # 1
grep -c 'id="what"' docs/index.html                                                      # 1
grep -c 'id="categories"' docs/index.html                                                # 1
grep -c 'id="contribute"' docs/index.html                                                # 1
grep -c 'id="maintenance"' docs/index.html                                               # 1
grep -c 'id="links"' docs/index.html                                                     # 1
grep -c 'application/ld+json' docs/index.html                                            # 1
grep -c '<link rel="stylesheet" href="site.css">' docs/index.html                        # 1
grep -c '<style' docs/index.html                                                         # 0
grep -ci 'og:image' docs/index.html                                                      # 0
grep -ci 'twitter:image' docs/index.html                                                 # 0
grep -c '<script' docs/index.html                                                        # 1 (the JSON-LD block only)
```

- [ ] **Step 3: CSS-var check (spec step 3)**

```bash
grep -c -- '--ink:' docs/site.css     # 1
grep -c -- '--line:' docs/site.css    # 1
grep -c -- '--mute:' docs/site.css    # 1
grep -c -- '--paper:' docs/site.css   # 1
grep -c '^\.wrap{' docs/site.css      # 1
```

- [ ] **Step 4: No-duplication check (spec step 4)**

```bash
grep -c '<table' docs/index.html      # 1 (the category map only)
grep -c '<tr>' docs/index.html        # 12 (1 header row + 11 category rows)
grep -c '<li>' docs/index.html        # 5 (the repository links list only)
grep -cE '(^|[^v0-9])[0-9]+ (entries|tools|libraries|resources|models|categories)' docs/index.html  # 0
```

The no-counts regex excludes digits preceded by `v` so the mandated phrases "SysML v2 resources" and "SysML v1 models" do not false-positive; a real count like "12 tools" still matches.

- [ ] **Step 5: No-relative-link check (spec step 5)**

```bash
grep -nE 'href="(\./|\.\./)?(README|contributing)\.md' docs/index.html
```
Expected: no output (grep exit code 1).

Then list every href and confirm each is on the allowlist: the anchor targets #what, #categories, #contribute, #maintenance, #links; the canonical Pages URL; fonts.googleapis.com, fonts.gstatic.com, and the Google Fonts css2 URL; site.css; https://awesome.re; and github.com URLs under https://github.com/jgsystemsconsulting/awesome-sysml-v2/.

```bash
grep -oE 'href="[^"]*"' docs/index.html | sort -u
```

Done when: every expected value matches. This battery must pass before Task 5 runs.

## Task 5: Single commit

**Files:** none new. Stages exactly docs/index.html, docs/site.css, docs/.nojekyll.

**Interfaces:**
- Consumes: the three verified files from Tasks 2-4.
- Produces: one local commit `Add companion docs site` on main carrying exactly the three site files. docs/superpowers/ stays out of the commit: it is untracked at this baseline (nothing under docs/ has ever been committed locally or on origin), and the dispatch instructs that it is not part of this commit. Keep it that way.

**Model:** flash

- [ ] **Step 1: Stage exactly the three site files**

```bash
git add docs/index.html docs/site.css docs/.nojekyll
git status --porcelain
```
Expected: three `A ` lines (docs/.nojekyll, docs/index.html, docs/site.css) plus the untracked `?? docs/superpowers/`. Nothing from docs/superpowers/ is staged.

- [ ] **Step 2: Commit**

```bash
git commit -m "Add companion docs site"
```

- [ ] **Step 3: Post-commit verification**

```bash
git log -1 --pretty=%s                                      # Add companion docs site
git show --stat --oneline HEAD                              # exactly 3 files changed
git diff 4c68451 HEAD --stat -- README.md contributing.md   # empty output (spec step 8)
git status --porcelain                                      # only ?? docs/superpowers/
```

Done when: HEAD carries the exact message and exactly the three files, and README.md and contributing.md show no diff against the baseline.

## Task 6: Pages enablement and homepageUrl (BLOCKED until push)

**Files:** none in the repo. Platform API calls only.

**Interfaces:**
- Consumes: Task 5's commit, which must be on origin/main first. This plan cannot push; the Pages build serves from REMOTE main, so enabling Pages before the push would serve a docs/ that does not exist there.
- Produces: Pages serving main:/docs, homepageUrl set to https://jgsystemsconsulting.github.io/awesome-sysml-v2/, and a live URL that returns 200 anonymously (spec verification steps 6-7, AC3, AC4).
- Ordering resolution: the executing agent checks the Step 1 precondition. If the commit is not yet on origin/main, the agent STOPS and reports `DONE (Tasks 1-5); Task 6 deferred to the push step`. Only if the commit is already on origin/main (the parent has pushed) does the agent run Steps 2-6. The executing agent never pushes.

**Model:** standard (external API responses, 409 handling, live-check retry judgment)

- [ ] **Step 1: Precondition gate**

```bash
git fetch origin main
git merge-base --is-ancestor HEAD origin/main && echo PUSHED
```
Expected: prints `PUSHED`. If it does not, STOP: report Tasks 1-5 done and Task 6 deferred to the push step.

- [ ] **Step 2: Enable Pages from main:/docs**

```bash
gh api -X POST repos/jgsystemsconsulting/awesome-sysml-v2/pages -f "source[branch]=main" -f "source[path]=/docs"
```
On success (201): proceed. On 409 (Pages already configured): verify the existing config serves main:/docs, then proceed:
```bash
gh api repos/jgsystemsconsulting/awesome-sysml-v2/pages --jq '{branch: .source.branch, path: .source.path, status: .status}'
```
Expected: branch `main`, path `/docs`. Any other failure: report and stop.

- [ ] **Step 3: Set homepageUrl**

```bash
gh repo edit jgsystemsconsulting/awesome-sysml-v2 --homepage https://jgsystemsconsulting.github.io/awesome-sysml-v2/
```

- [ ] **Step 4: Anonymous live check (spec step 6) with one retry**

```bash
curl -s -o /dev/null -w "%{http_code}" https://jgsystemsconsulting.github.io/awesome-sysml-v2/
```
Expected: 200. The first Pages build can lag the POST by a minute or two. If the code is not 200: wait 60 seconds and retry once. Still not 200 after that single retry: report the failure; do not loop.

- [ ] **Step 5: Body serves the masthead (spec step 6)**

```bash
curl -s https://jgsystemsconsulting.github.io/awesome-sysml-v2/ | grep -c 'JGS-AWESOME-SYSML-V2'
```
Expected: 1 or more.

- [ ] **Step 6: homepageUrl check (spec step 7)**

```bash
gh api repos/jgsystemsconsulting/awesome-sysml-v2 --jq .homepage
```
Expected: `https://jgsystemsconsulting.github.io/awesome-sysml-v2/`.

Done when: Pages is configured for main:/docs (fresh 201 or verified 409), the live URL returned 200 with the masthead DOC-ID in the body, and .homepage returns the Pages URL.
