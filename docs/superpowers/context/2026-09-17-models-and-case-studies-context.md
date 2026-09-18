# Context: Models and Case Studies section

## Context brief

**Primary question:** What must change in this workspace to rename and expand the README Example Models section into a curated Models and Case Studies list, without inventing a separate Projects category?

**Sub-questions:**
1. Where is the Example Models section defined (README TOC, heading, entries)?
2. Which companion-site surfaces hard-code the old section name or anchor?
3. What inclusion and entry-format rules in contributing.md bind any new model entries?
4. Are there existing specs, backlog items, or site copy that constrain rename vs expand?
5. What alphabetical-order and duplicate rules apply to the current nine model entries?

**Success criteria (design work needs):**
1. Exact file:line locations for TOC link, H2 heading, and every current Example Models entry.
2. Exact locations of companion docs site text that names Example Models or `#example-models`.
3. Contributing criteria and entry format that new model entries must satisfy (verbatim rules).
4. Whether section rename requires contributing.md or only README + docs/index.html.
5. Known open backlog items that touch this section (b-09, b-13) and their evidence paths.
6. Whether awesome-lint / markdownlint impose section-name or structure constraints visible in-repo.

**Out of scope:**
- Implementing the README edit in this context document.
- Full GitHub search for new external model repos (research-loop).
- Creating a top-level Projects section.
- GitHub Pages settings or CI workflow changes unrelated to section text.

**Budget:** 1-2 rounds, ~12 tool calls per lens.

**Workspace baseline:**
- porcelain sha256: `d3ffb3baaf3dd1aae7ec1f146885a3b3d6dfac4db13dc03240e8b4e04415beeb`
- HEAD (informational): `b3d842e8bfb84f3967ed7417cd6bae31e7ace8f1`
- Date: 2026-09-17

## Findings

1. **TOC and H2 own `#example-models`.** README.md:13 TOC `- [Example Models](#example-models)`; README.md:76 `## Example Models`. Rename must change both link text and slug together (GitHub heading anchors).
2. **Nine live entries at README.md:78-86**, already alphabetical by link text (airbus … sensmetry).
3. **Live companion site hardcodes the category.** docs/index.html:83 links `README.md#example-models` with label `Example Models` and blurb "Working SysML v2 models to learn from and build on."
4. **Companion-site sync policy (historical spec).** docs/superpowers/specs/2026-09-16-companion-docs-site.md:106 requires the category map update in the same change as a README category rename. Spec also notes docs/ is outside lint.yml/lychee scopes (:112), so CI will not catch a README-only rename.
5. **contributing.md does not name section titles.** Inclusion criteria :5-11 and entry format :15-21 (one-line form, alpha by link text, commercial-only Commercial Tools) bind every new model row. Label rename alone does not require contributing.md edits.
6. **Lint has no section-name allowlist.** `.markdownlint-cli2.jsonc` only disables MD013; lint.yml runs `awesome-lint@2.3.0` on README.md and markdownlint on README + contributing.
7. **Backlog overlap.** b-09 open README structural rewrite (backlog.md:15). b-13 needs-info on near-parallel structured-use-cases at README:80 and :85 (backlog.md:19).
8. **Boundary:** Flashlight starter model sits under Migrating (README.md:122), not Example Models. Cross-section move is out of this rename unless scoped.
9. **Soft copy:** CHANGELOG Keep a Changelog Unreleased (CHANGELOG.md:5-7). awesome-submission runbook differentiation sentence still says "example models" (docs/superpowers/runbooks/awesome-submission.md:53). PR template checks correct section + alpha (.github/PULL_REQUEST_TEMPLATE.md).

## Synthesis

Rename is a three-surface edit: README TOC + H2 (+ entries), docs/index.html category row (label, href anchor, optional blurb), and optional tagline/runbook/CHANGELOG wording. contributing.md stays as the criteria source and does not need a section-title rewrite. No automated section-name gate exists; same-change site sync is mandatory because docs/ escapes CI. Expand means alphabetical inserts under the renamed H2, each meeting contributing criteria 1-5. Do not open a second top-level Projects section. Leave b-13 open unless this work proves same-project identity; do not thrash a full b-09 rewrite beyond this section. Decision-bearing live-site claim is CORROBORATED; most path claims are SINGLE-SOURCE doc facts (expected for a markdown list repo).

## Evidence index

| loc | kind |
|-----|------|
| README.md:13 | doc |
| README.md:76 | doc |
| README.md:78-86 | doc |
| README.md:80 | doc |
| README.md:85 | doc |
| README.md:122 | doc |
| docs/index.html:83 | code |
| contributing.md:5-11 | doc |
| contributing.md:15-21 | doc |
| docs/superpowers/backlog.md:15 | doc |
| docs/superpowers/backlog.md:19 | doc |
| docs/superpowers/specs/2026-09-16-companion-docs-site.md:56 | doc |
| docs/superpowers/specs/2026-09-16-companion-docs-site.md:106 | doc |
| docs/superpowers/specs/2026-09-16-companion-docs-site.md:112 | doc |
| docs/superpowers/plans/2026-09-16-companion-docs-site.md:187 | doc |
| docs/superpowers/runbooks/awesome-submission.md:53 | doc |
| .markdownlint-cli2.jsonc:1-5 | config |
| .github/workflows/lint.yml:28 | config |
| .github/PULL_REQUEST_TEMPLATE.md:2 | doc |
| CHANGELOG.md:5-7 | doc |
