# Context: companion-docs-site (P2)

## Context brief

- **Primary question**: What exactly must the docs/ companion site contain and look like to match the JGS org standard, how is Pages enabled and homepageUrl wired, and what README content maps to which site sections?
- **Success criteria**:
  - SC1: The org site standard, concretely: structure of a sibling repo's docs/ site (jgs-archi-skills/docs/index.html + site.css + masthead + anchor nav + head metadata incl. OG/Twitter/JSON-LD + classification strip) — enough detail to replicate the pattern.
  - SC2: awesome-sysml-v2 README content inventory: title, description, badge, Contents list (11 sections), all section headings, entry counts, Contributing section — the site's content map.
  - SC3: Pages mechanics: how Pages is enabled for this repo (gh api pages endpoint, source branch/path), current Pages state, and the homepageUrl wiring command.
  - SC4: Constraint: README stays source of truth; the site presents (not duplicates) it; single index.html + site.css per the standard; no build system.
- **Out of scope**: CoC/SECURITY files (P5); awesome submission (P3); workflow changes; README rewrites.
- **Budget**: 1 round; cap 3.
- **Workspace baseline**: HEAD 4c68451 (P4 landed; contributing.md has the Maintenance section).

## Findings

Full graded claim table in the round log. 13 merged claims, verdict CONTEXT_COMPLETE, 0 conflicted. Key facts:

- Org site pattern (SC1, corroborated): head inventory per sibling index.html — charset utf-8, viewport, `color-scheme: dark`, title/description, canonical to the Pages URL, OG tags (type/url/title/description/image 1200x630), Twitter summary_large_image, JSON-LD SoftwareApplication; masthead strip `CLASSIFICATION: PUBLIC / LICENCE: MIT / DOC-ID: <REPO> / REV: <n>`; anchor nav `<nav class="site">` with in-page links; site.css ~60 lines of CSS vars (ink/line/mute/paper, JetBrains Mono + Inter, `.wrap` max-width 1200px), dark drafting aesthetic. Family variance: archi uses external site.css, SE packs inline styles — the strip and layout tokens are the family constants.
- README inventory (SC2, corroborated): 12 `##` headings (Contents, 11 categories, Contributing), badge on line 1, 9-10 entries per category, Contributing delegates to contributing.md.
- Pages mechanics (SC3, corroborated): NEITHER sibling uses a Pages workflow — Pages is Settings/API-based (docs/ on main). Enable via `gh api -X POST repos/<o>/<r>/pages -f "source[branch]=main" -f "source[path]=/docs"`; homepageUrl via `gh repo edit --homepage <url>`.
- Source-of-truth pattern (SC4, corroborated): archi's own companion-site spec decided "no second copy of the hub" — the site presents and links to the blob README rather than re-rendering entries.
- Drift/publish traps (skeptic, config-sited): (1) hand-mirrored counts go stale (SE packs needed a truth gate after drift) — avoid live counts or date-stamp them; (2) relative `contributing.md` links 404 on the Pages root — siblings use absolute github blob URLs for repo files; (3) both siblings ship `docs/.nojekyll` — awesome must too; (4) `docs/superpowers/` process trees are committed in awesome (siblings gitignored theirs) — once Pages serves docs/, the process artifacts are web-served (already public in the repo since P1; accepted residual, documented); (5) lint globs cover README+contributing only — docs/ site files get no CI checks; (6) lychee args have no path allowlist, so site files enter the weekly crawl scope (relates to backlog b-17); (7) P1 spec text records isPrivate true as a dated fact — parent live-checked this round: isPrivate false, homepageUrl empty.

## Synthesis

All four success criteria met (4/4); verdict CONTEXT_COMPLETE. SC1 corroborated across two sibling fetches by two lenses; SC2 corroborated (cartographer + skeptic README reads); SC3's answer is itself the finding — Settings/API-based Pages, no workflow — corroborated by absence-of-workflow evidence in both siblings; SC4 corroborated with the archi no-second-copy precedent. Single-source items: install-prompt delegation detail (archi-only), SE inline-style variance — family variance, named here. The stale isPrivate fact in the P1 spec is a dated record of its gate time, superseded by the live check (false now); noted, not an error. Design constraints locked for the spec: single index.html + site.css + .nojekyll under docs/; masthead strip and head metadata per family pattern with DOC-ID JGS-AWESOME-SYSML-V2; anchor nav; site presents overview + category map with deep links to the GitHub README anchors (no entry-list duplication, no live counts); absolute blob URLs for repo files; Pages enabled from main:/docs via API; homepageUrl set to the Pages URL. Open questions: none.

## Evidence index

| Loc | Kind | Cited by |
|-----|------|----------|
| jgs-archi-skills/docs/index.html:5-27 | doc | cartographer (head inventory) |
| jgs-archi-skills/docs/index.html:31-36 | doc | cartographer, prospector (masthead strip) |
| jgs-archi-skills/docs/index.html:38-52 | doc | cartographer (anchor nav) |
| jgs-archi-skills/docs/index.html:184 | code | skeptic (blob-URL pattern) |
| jgs-archi-skills/docs/site.css:1-60 | code | cartographer, prospector (layout tokens) |
| jgs-archi-skills/docs/.nojekyll | config | skeptic (.nojekyll marker) |
| jgs-se-knowledge-packs/docs/index.html:124 | code | prospector (masthead family variant) |
| jgs-archi-skills/.github/workflows/ | config | cartographer, prospector (no Pages workflow) |
| jgs-archi-skills/.gitignore:22 | config | skeptic (docs/superpowers gitignored in sibling) |
| jgs-se-knowledge-packs/docs/superpowers/specs/2026-09-16-landing-catalogue-count-truth.md:7,16 | doc | skeptic (count-drift precedent) |
| jgs-archi-skills/docs/superpowers/specs/2026-09-02-companion-site-guide-design.md:59 | doc | skeptic (no-second-copy precedent) |
| README.md:1,5-126,126-129 | doc | cartographer, skeptic (inventory) |
| .github/workflows/lint.yml:33 | config | skeptic (lint globs exclude docs/) |
| .github/workflows/links.yml:28 | config | skeptic (lychee crawl scope) |
| live gh check (parent, this round) | config | parent (isPrivate false, homepageUrl empty) |
