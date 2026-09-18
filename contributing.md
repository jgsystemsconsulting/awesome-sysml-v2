# Contributing to Awesome SysML v2


**Lint is mandatory.** awesome-lint on README.md must pass on every push/PR to main. See [docs/MATURITY.md](docs/MATURITY.md).

Suggestions and pull requests are welcome. Every entry and every PR must meet the criteria below.

## Inclusion criteria

1. Stable, reachable URL pointing at the project itself.
2. Direct SysML v2 relevance; v1-only material is excluded except in Migrating.
3. One-line factual description, no marketing adjectives.
4. Active maintenance (commit within 24 months) or foundational value (formal specs, canonical reference repos).
5. Not a duplicate of an existing entry in the list.

## Entry format

One line per entry, exactly:

```markdown
- [Name](URL) - Description.
```

The name is the project or product proper name. The URL is canonical: repo root for GitHub projects, product page for commercial tools, no tracking parameters, no trailing slash on GitHub repo roots. The description is one factual sentence that starts uppercase and ends with a period; a short parenthetical is allowed after the first word, for example "(VS Code)". Entries are sorted alphabetically, case-insensitive, by link text within each section. Commercial products go in the Commercial Tools section only.

## Local commands

Run these from the repository root before opening a PR:

```bash
npx awesome-lint@2.3.0 README.md
npx markdownlint-cli2 "README.md" "contributing.md"
```

### Link check

`lychee` is a native binary, not an npm package. Install it once with your platform package manager (`scoop`, `winget`, or `choco` on Windows, `brew` on macOS, `pacman`, `zypper`, `snap`, or `apk` on Linux), then run from the repository root:

```bash
lychee README.md docs/index.html
```

Export `GITHUB_TOKEN` (for example `GITHUB_TOKEN=$(gh auth token)`) to avoid GitHub rate limiting on `github.com` links. Third-party sites sometimes return transient timeouts or 429s; retry before treating a failure as a broken link.

## Maintenance

Three workflows in `.github/workflows/` run on a fixed cadence. This section states what each does.

### Link scan (weekly)

`links.yml` runs lychee every Monday at 18:00 UTC, on every pull request, and on manual dispatch. It scans `README.md` and `docs/index.html` (the product surface). On pull requests, broken product-surface links fail the job and block merge. On the weekly schedule and manual dispatch, a nonzero run creates or updates the single open "Link Checker Report" issue; a clean run leaves that issue untouched.

### Freshness report (monthly)

`stale.yml` runs on the first day of each month at 06:00 UTC, or on manual dispatch. It collects the `github.com` repository URLs from README.md and lists repos with no push in the last 24 months. The report is advisory: an entry past the window can still be valid under the foundational-value exception (criterion 4). The "Freshness report" issue is refreshed on every run, including months with no stale entries. Criterion 4 speaks of a commit within 24 months; the report measures the repository's last push, which is usually but not always the same thing.

### Lint gates (every PR and push to main)

`lint.yml` runs `awesome-lint@2.3.0` on README.md, and `markdownlint` on README.md and contributing.md, on every pull request targeting main and every push to main. These gates block merge on failure. The local markdownlint command above installs an unpinned npx package and may differ from the version CI runs; the pinned `awesome-lint@2.3.0` matches CI exactly.
