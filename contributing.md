# Contributing to Awesome SysML v2

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
lychee README.md
```

Export `GITHUB_TOKEN` (for example `GITHUB_TOKEN=$(gh auth token)`) to avoid GitHub rate limiting on `github.com` links. Third-party sites sometimes return transient timeouts or 429s; retry before treating a failure as a broken link.
