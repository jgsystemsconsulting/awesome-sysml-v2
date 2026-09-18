# Spec: community root meta files (awesome-sysml-v2, P5)

Date: 2026-09-16
Topic: community-root-meta
Status: approved for planning (fork X1 resolved by controller ruling: all four files ship)

## Problem statement

The repo is public (P1) and hardening runs P2 through P9 are done, but the community trust surface is thinner than the sibling awesome lists it wants to sit beside. GitHub's community-standards panel flags four gaps: no code of conduct, no security policy, no citation metadata, no changelog. For a link-curation repo this matters more than for a code repo. Visitors deciding whether to trust the links, cite the list, or report a bad entry have no defined path for any of the three. Work package P5 closes the gap by shipping the four standard root files. The fork X1 question (ship a subset?) is settled: all four ship.

## Repository facts (in-stem, verified)

- Repo: `jgsystemsconsulting/awesome-sysml-v2`, public since P1, description set.
- `LICENSE` (MIT) exists at root.
- No `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, or `CHANGELOG.md` at root or in `.github/`. `.github/` holds only `PULL_REQUEST_TEMPLATE.md` and `workflows/`.
- No email contact is on file. Contact runs through GitHub (owner profile, issues, private vulnerability reporting).
- `.markdownlint-cli2.jsonc` disables only MD013. The lint workflow's markdownlint step globs `README.md` and `contributing.md` only.

## Goals

- Ship four files at the repo root, discovered by GitHub convention, with zero cross-link edits to README.md or contributing.md (P4 finalized those; no AC requires links).
- Each file uses its de facto standard format so GitHub and third-party tools parse it without custom code.
- The changelog records today's hardening runs honestly, under `[Unreleased]`, in consumer-facing terms.

## Non-goals

- No workflow changes. Adding `CHANGELOG.md` to the lint glob is a follow-up, not part of this package.
- No README or contributing.md changes, no entry content changes.
- No release, no git tag, no version bump.
- No email address and no separate enforcement email alias (contact runs through GitHub). The full-length Contributor Covenant 2.1 is in scope and ships verbatim.
- No `.github/CODE_OF_CONDUCT.md` / `.github/SECURITY.md` copies. Root only. GitHub surfaces root copies natively.

## Research

research: skipped (no-open-world-questions; standard file formats, no external fact to learn)

Gate logs:

- Research gate: `docs/superpowers/research/2026-09-16-community-root-meta-research-log.md`
- Context gate: `docs/superpowers/context/2026-09-16-community-root-meta-context-log.md`

## Design

### Inventory

Exactly four new files at the repo root. Nothing else changes.

| File | Rationale (one line) |
|---|---|
| `CODE_OF_CONDUCT.md` | Contributor Covenant is the form every sibling list uses; the short version fits a single-owner repo. |
| `SECURITY.md` | Gives GitHub's Security tab a real report path for hijacked links and repo issues, without pretending we ship an application. |
| `CITATION.cff` | The one file format GitHub turns directly into an "Cite this repository" box; entities without it get cited ad hoc or not at all. |
| `CHANGELOG.md` | Keep a Changelog is the convention consumers and auditors scan first; today's seven hardening runs deserve one honest summary entry. |

### CODE_OF_CONDUCT.md

Content outline:

1. `# Code of Conduct` heading, short intro: this project follows the Contributor Covenant, version 2.1 (full text).
2. The full Contributor Covenant 2.1 text, verbatim, fetched by the implementer from the canonical URL https://www.contributor-covenant.org/version/2/1/code_of_conduct/ and embedded in full. (Decision pinned: the full text, not a short form — no stable short-form 2.1 template exists at a pinned URL, and a verbatim claim needs a real source. The full text is the canonical artifact.)
3. The contact line filled in: conduct reports go to the repository owner via GitHub — open a GitHub issue on this repository, or contact the owner through the profile at https://github.com/jgsystemsconsulting. No literal `[INSERT CONTACT METHOD]` placeholder ships.
4. The standard follow-ups: complaints reviewed and investigated, confidentiality owed to reporters, maintainers acting in bad faith face consequences.
5. Attribution section: adapted from the Contributor Covenant, version 2.1, linking https://www.contributor-covenant.org/version/2/1/code_of_conduct/.

Decisions pinned: full Contributor Covenant 2.1 text from the canonical URL (a verbatim claim needs a real source; no stable 2.1 short-form template exists at a pinned URL). Contact runs through GitHub (repo issue or owner profile), because no email exists. If a real community forms and enforcement needs process, that process lands in a later package.

### SECURITY.md

Content outline:

1. `# Security Policy` heading.
2. Supported section: this repository is a curated list, not an application. The supported surface is this repository itself: its content, its workflows, and the links it lists. No supported-versions table exists and none gets invented, because there is no shipped product with releases.
3. Reporting section: use GitHub private vulnerability reporting (Security tab, "Report a vulnerability") on this repository. The setting is verified and, if disabled, enabled during execution (`gh api repos/jgsystemsconsulting/awesome-sysml-v2 --jq .private_vulnerability_reporting_enabled`; if false: `gh api -X PUT repos/jgsystemsconsulting/awesome-sysml-v2/private-vulnerability-reporting`). Two in-scope report types:
   - a listed link that has turned malicious, compromised, hijacked, or serves content materially different from its description;
   - a vulnerability in this repository itself (workflows, scripts, repository configuration).
   Both go through private reporting. Public issues are the wrong channel for either.
4. Response expectation: acknowledgment within 5 business days; removal or fix prioritized by exposure; a public note follows after remediation.
5. Out of scope: vulnerabilities inside the tools the list links to. Those belong to the linked projects' own security channels. This repo only acts on the entry.

This is the "no app-CVE theater" shape: the policy names a real supported surface (the list) and a real path (private vulnerability reporting), and declines everything else explicitly.

### CITATION.cff

Complete field set, pinned:

```yaml
cff-version: 1.2.0
message: "If you use this list in your work, please cite it using this metadata."
title: Awesome SysML V2
authors:
  - entity:
      name: "JG Systems Consulting Ltd"
license: MIT
repository-code: https://github.com/jgsystemsconsulting/awesome-sysml-v2
preferred-citation:
  type: generic
  title: "Awesome SysML V2"
  authors:
    - entity:
        name: "JG Systems Consulting Ltd"
  year: 2026
  repository-code: https://github.com/jgsystemsconsulting/awesome-sysml-v2
```

Decisions pinned: author is a CFF `entity`, matching the corporate owner. `license: MIT` is the SPDX identifier pointing at the existing root LICENSE file. `version` and `date-released` are deliberately omitted because no release exists; the changelog's `[Unreleased]` records the same reality. Add both fields in the commit that creates the first tagged release.

### CHANGELOG.md

Keep a Changelog 1.1.0 format. Content outline pinned to this skeleton:

```markdown
# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Companion documentation site for the list (P2).
- Link-report workflow: duplicate-report detection and advisory pull-request check (P7).
- Maintenance and contribution guidance: contributing guide, backlog, review records (P4).

### Changed

- All GitHub Actions pinned to full commit SHAs for supply-chain hardening (P9).
- Lint workflow runs least-privilege with a pinned awesome-lint version (P8).
- Repository made public (P1).

### Fixed

- Freshness check now reports link state accurately instead of masking failures (P6).
```

Decisions pinned: single `[Unreleased]` entry; no version header, because nothing shipped. Bullets are consumer-facing statements of observable repository change; no authorship claims, no effort claims, no dates inside bullets. P-numbers stay in the bullets as traceability to the repo's own specs; if they read as noise to outsiders, drop them in a follow-up edit, not now.

Lint ruling (the dispatched open decision): `CHANGELOG.md` is markdown, so it must pass the repo's own rule set. Pinned check: `npx markdownlint-cli2 CHANGELOG.md` runs clean against the existing `.markdownlint-cli2.jsonc` (MD013 off, defaults otherwise). The Keep a Changelog skeleton above passes: `# Changelog` satisfies MD041, headings and plain lists trip no default rules. The CI glob stays untouched (workflow changes are out of scope); wiring `CHANGELOG.md` into the lint workflow glob is the named follow-up.

`CITATION.cff` is not markdown. markdownlint does not apply to it. Its check is the YAML parse in the acceptance criteria.

## Risks

- **No contact endpoint.** Without email, conduct reports land via the owner's GitHub profile and security reports via private vulnerability reporting. Risk: reports sit unseen if the owner misses notifications. Mitigation: owner enables GitHub notifications and watches the Security tab. Accepted; revisit only if a real community forms.
- **CFF tooling variance.** Some citation tools render an entity author's name without the company suffix, and GitHub's citation box prefers files it can fully parse. The pinned field set is the CFF 1.2.0 mainstream shape; if a validator demands `version`/`date-released`, both arrive with the first release per the pinned decision above.
- **Changelog honesty.** The work summarized was produced by an AI-assisted pipeline across seven runs. The skeleton keeps every bullet to an observable repo change under `[Unreleased]`; it claims no release, no version, no human review that did not happen. The enforcement check is the skeleton itself: an executor may not add superlatives or version claims.
- **MD024 on the first real release.** The first release section will duplicate the `### Added`/`### Changed`/`### Fixed` headings under a new version header, which default markdownlint flags (MD024). Fix lands with that release: set `MD024: {siblings_only: true}` in `.markdownlint-cli2.jsonc` in the same commit. Out of scope today.
- **awesome-lint scope.** `awesome-lint` checks README.md only, so the new files cannot break the existing lint gate. No interaction risk.

## Acceptance criteria

1. Exactly four new files exist at the repo root: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CITATION.cff`, `CHANGELOG.md`. `git status` shows no other modified or added files.
2. `CODE_OF_CONDUCT.md` carries the full verbatim Contributor Covenant 2.1 text from https://www.contributor-covenant.org/version/2/1/code_of_conduct/, the "adapted from the Contributor Covenant, version 2.1" attribution with a working link, and its contact line points at the repo owner via GitHub with no unfilled placeholder.
3. `SECURITY.md` names GitHub private vulnerability reporting as the report path, scopes the supported surface to the repository and its link list, states the 5-business-day acknowledgment expectation, and contains no supported-versions table.
4. `CITATION.cff` parses as YAML (`python -c "import yaml; d=yaml.safe_load(open('CITATION.cff')); assert d['cff-version']=='1.2.0'; assert d['title']=='Awesome SysML V2'; assert d['license']=='MIT'; assert d['repository-code']=='https://github.com/jgsystemsconsulting/awesome-sysml-v2'; assert d['preferred-citation']['type']=='generic'"`).
5. `CHANGELOG.md` has a single `[Unreleased]` section with `Added`, `Changed`, `Fixed` groups covering all seven runs (P9, P6, P7, P8, P4, P2, P1) as sketched, and `npx markdownlint-cli2 CHANGELOG.md` exits clean with the existing config.
6. No changes to `README.md`, `contributing.md`, `.github/workflows/`, or any list entry content.
7. GitHub private vulnerability reporting is enabled on the repository (`gh api repos/jgsystemsconsulting/awesome-sysml-v2 --jq .private_vulnerability_reporting_enabled` prints `true` after execution), and the CoC text is the verbatim Contributor Covenant 2.1 from the canonical URL.

## Verification

- Criteria 1 through 3 and 6: read the diff. No tooling needed.
- Criterion 4: the pinned Python one-liner. No new dependency; PyYAML ships with the environment, and if it does not, `npx yaml-lint` or any YAML parser is an acceptable substitute for the parse step.
- Criterion 5: `npx markdownlint-cli2 CHANGELOG.md` from the repo root.
