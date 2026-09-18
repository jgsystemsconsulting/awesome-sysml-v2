# Research: pr-lint-gate-surface (P8)

## Research brief

- **Primary question**: What exact awesome-lint version should the CI and documented local command pin to, and what are the pinning mechanics and pitfalls for `npx package@version` in GitHub Actions?
- **Sub-questions**:
  1. Current latest published awesome-lint version on the npm registry (and its publish date/maintenance status).
  2. Exact pin mechanics: does `npx awesome-lint@X.Y.Z` resolve reproducibly without a lockfile; node version compatibility (CI runs Node 20).
  3. Pitfalls: npx cache behavior, awesome-lint project health, any known breaking changes across majors.
- **Success criteria**:
  - SC1: The chosen awesome-lint version is sourced from the npm registry (primary).
  - SC2: Pin mechanics for `npx pkg@version` stated from a primary/official source (npm docs).
  - SC3: Pitfalls surfaced (maintenance status, npx semantics).
- **Out of scope**: whether to pin (decided, P8); Actions SHA pins (P9, done); Renovate/Dependabot (backlog).
- **Budget**: 1 round target; cap 3.

## Findings

Decision-bearing (retrieved 2026-09-16):

- **awesome-lint latest published version: 2.3.0** (npm registry dist-tags, primary). engines: node >=20. ESTABLISHED.
- **Pin mechanics**: `npx pkg@specifier` matches only the exact name+version and installs the package into the npm cache, which is added to PATH (npm CLI docs, primary). No lockfile is consulted for `npx pkg@ver`; a package.json+lockfile approach is the only variant that locks the transitive tree (npm lockfile docs: CI "guaranteed to install exactly the same dependencies"). ESTABLISHED.

Supporting:

- awesome-lint is actively maintained: commits through 2026-07, 2.3.0 released 2026-04, upstream CI matrix tests Node 20 and 24 (skeptic + scout, primary repo sources). ESTABLISHED.
- Upstream norm is actually UNPINNED `npx awesome-lint` with `fetch-depth: 0` (needed for repo-age checks) in both awesome-lint's README recipe and sindresorhus/awesome's own repo linter (primary). PROVISIONAL as a single claim but dual-sourced.
- Pitfalls (SC3, primary issue/release sources): pinning freezes false-positive fixes that keep shipping (v2.2.2 "Fix false-positives in spell-check rule"; #218 .NET casing FP); known GHA-vs-local mismatch classes (#204 non-reproducible GHA errors, closed not-planned; #224 CLI-vs-PR inconsistency); a top-level pin does not lock caret transitives (remark ^15), so cold-cache runs can still vary; v2.0.0 broke on Node (requires >=20).
- No evidence found for markdownlint double-lint rule collisions (absence claim, PROVISIONAL).

## Synthesis

SC1: version 2.3.0 resolved from the registry primary; distinct sources: registry (digger) + repo package.json (scout) corroborate the version line and its node requirement. SC2: pin mechanics from npm's own CLI docs; the lockfile-guarantee doc is the same family (docs.npmjs.com), so graded single-doc-primary and named here. SC3: pitfall cluster multi-sourced across issue/release/repo primaries. Design consequence for the spec: pin the top-level package with an exact version (`npx awesome-lint@2.3.0` in CI and contributing.md) rather than introducing a package.json+lockfile subsystem into a repo that has none — the lockfile variant locks transitives but adds a maintenance surface the packages document did not request; the transitive-float risk is accepted and recorded as a documented limitation with the same bump cadence as the P9 SHA pins. The upstream fetch-depth: 0 requirement is already satisfied (lint.yml checks out with fetch-depth: 0). Open questions: none blocking. PROVISIONAL claims (upstream-norm note, absence of double-lint collisions) named here and non-decision-bearing.

## Sources

| URL | Class | Used for |
|-----|-------|----------|
| https://registry.npmjs.org/awesome-lint | primary | dist-tags latest 2.3.0 |
| https://registry.npmjs.org/awesome-lint/2.3.0 | primary | engines node >=20 |
| https://docs.npmjs.com/cli/v10/commands/npx | primary | npx exact-match + cache semantics |
| https://docs.npmjs.com/cli/v10/commands/npm-exec | primary | npx cache install behavior |
| https://docs.npmjs.com/cli/v9/configuring-npm/package-lock-json | primary | lockfile reproducibility guarantee |
| https://github.com/sindresorhus/awesome-lint/blob/main/package.json | primary | engines; caret transitive example |
| https://github.com/sindresorhus/awesome-lint/blob/main/.github/workflows/main.yml | primary | node 20/24 CI matrix |
| https://github.com/sindresorhus/awesome-lint | primary | project surface; CLI requires node + git |
| https://github.com/sindresorhus/awesome-lint/commits/main/ | primary | maintenance activity 2026-07 |
| https://github.com/sindresorhus/awesome-lint/releases/tag/v2.2.2 | primary | FP-fix release |
| https://github.com/sindresorhus/awesome-lint/releases/tag/v2.0.0 | primary | Node 20 breaking major |
| https://github.com/sindresorhus/awesome-lint/issues/204 | primary | non-reproducible GHA errors |
| https://github.com/sindresorhus/awesome-lint/issues/218 | primary | spell-check FP |
| https://github.com/sindresorhus/awesome-lint/issues/224 | primary | CLI-vs-PR mismatch |
| https://github.com/sindresorhus/awesome-lint/blob/main/readme.md | primary | unpinned recipe + fetch-depth |
| https://github.com/sindresorhus/awesome/blob/main/.github/workflows/repo_linter.sh | primary | upstream unpinned norm |
