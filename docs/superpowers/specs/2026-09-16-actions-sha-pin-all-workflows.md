# Spec: actions-sha-pin-all-workflows (P9)

Date: 2026-09-16
Scope: `.github/workflows/lint.yml`, `.github/workflows/links.yml`, `.github/workflows/stale.yml`
Status: approved work package P9 of the awesome-sysml-v2 hardening series

## Problem statement

All seven `uses:` refs in the repository's three GitHub Actions workflows point at mutable major-version tags (`@v4`, `@v2`, `@v5`, `@v24`). A tag is a pointer the action's owner can retarget at any commit. The tj-actions/changed-files compromise of March 2025 worked exactly this way: attackers rewrote existing version tags, and wiz.io reports that customers using a hash-pinned version of the action were not impacted (wiz.io and Unit42 incident reports; CISA notice for CVE-2025-30066). GitHub's own security-hardening guide states that pinning to a full-length commit SHA is currently the only way to use an action as an immutable release.

This repository publishes link and freshness reports that open issues with `GITHUB_TOKEN`, so a compromised action could write attacker-controlled content into repo issues. Replacing tag refs with SHAs removes the retarget attack surface at zero behavioral cost.

Inventory (verified against the working tree, matches the context gate line for line):

| File:line | Current ref | Replacement SHA (research-verified 2026-09-16) | Tag type |
|---|---|---|---|
| stale.yml:16 | `actions/checkout@v4` | `11d5960a326750d5838078e36cf38b85af677262` | lightweight |
| links.yml:16 | `actions/checkout@v4` | `11d5960a326750d5838078e36cf38b85af677262` | lightweight |
| links.yml:19 | `lycheeverse/lychee-action@v2` | `e7477775783ea5526144ba13e8db5eec57747ce8` | lightweight |
| links.yml:26 | `peter-evans/create-issue-from-file@v5` | `e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd` | lightweight |
| lint.yml:13 | `actions/checkout@v4` | `11d5960a326750d5838078e36cf38b85af677262` | lightweight |
| lint.yml:16 | `actions/setup-node@v4` | `49933ea5288caeca8642d1e84afbd3f7d6820020` | lightweight |
| lint.yml:22 | `DavidAnson/markdownlint-cli2-action@v24` | `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff` | annotated |

Each SHA was resolved through at least two independent primary paths (GitHub commits API, git refs API, releases pages). See Research for URLs.

## Goals

- Replace all seven mutable tag refs with full-length (40-hex) commit SHAs, using the verified values above.
- Keep behavior identical: each job runs the same action at the same version; only the ref spelling changes.
- Add a version comment on every pinned line and one upgrade-path comment block per file, so maintainers can bump pins without re-deriving the method.

## Non-goals

- lint.yml `permissions:` block and the `npx awesome-lint` invocation (P8 owns both).
- lychee arguments, triggers, or report handling (P7).
- stale.yml cutoff or curl logic (P6).
- Dependabot or Renovate configuration, and any automation for bumping pins (backlog).
- README or content file changes.
- Any change to job semantics, step order, `with:` inputs, triggers, or env blocks.

## Design

### Pin format

Every pinned line takes the form:

```yaml
<indent>- uses: <owner>/<repo>@<full-40-hex-sha> # <resolved-tag>
```

Decisions, both fixed by this spec:

1. **Full-length SHA, never short.** GitHub's hardening guidance specifies the full 40-character commit SHA; short SHAs do not give immutability guarantees.
2. **Version comment is the bare resolved tag: `# v4`, `# v2`, `# v5`, `# v24`.** Rationale: the verified fact is "tag X pointed at SHA Y on 2026-09-16", so the comment records exactly that tag. Renovate's github-actions manager treats a bare-SHA ref with no version comment as disabled by default (docs.renovatebot.com); a `# vX` version comment satisfies its convention, so a future Renovate enablement can propose digest updates, and until then the comment gives human readers the version at a glance. The repo has no Renovate or Dependabot config today, so bot compatibility is a bonus, not a requirement. No `(repo pinned on YYYY-MM-DD)` suffix or similar: unverified niceties cost characters and invite drift. One tag, one comment, done.

### Upgrade-path comment

Each of the three files gets the same 6-line block comment, inserted directly under line 1 (`name: ...`) followed by one blank line. Exact text, verbatim:

```yaml
# Action refs are pinned to full-length commit SHAs (supply-chain hardening,
# per GitHub's security-hardening guide). To bump an action, resolve its tag
# to a commit SHA, e.g.:
#   curl -s https://api.github.com/repos/<owner>/<repo>/commits/<tag>
# Use the "sha" field (the commit, not a tag object SHA; see annotated-tag
# note in the repo spec for P9), then update the version comment to match.
```

This documents the commits-API resolution method the research validated as the method of record (`https://api.github.com/repos/<owner>/<repo>/commits/<tag>` returns the commit SHA directly), and it warns about the one trap in the method: for annotated tags the refs API surfaces the tag object first, and the pinned value must be the peeled commit.

### Per-file edits

Apply the ref edits before inserting the comment block; cited line numbers are pre-insert.

**stale.yml** (1 ref + comment block):

- Line 16: `      - uses: actions/checkout@v4` becomes `      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4`
- Insert the upgrade-path comment block after line 1 (`name: Freshness report`).

**links.yml** (3 refs + comment block):

- Line 16: `      - uses: actions/checkout@v4` becomes `      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4`
- Line 19: `        uses: lycheeverse/lychee-action@v2` becomes `        uses: lycheeverse/lychee-action@e7477775783ea5526144ba13e8db5eec57747ce8 # v2`
- Line 26: `        uses: peter-evans/create-issue-from-file@v5` becomes `        uses: peter-evans/create-issue-from-file@e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd # v5`
- Insert the upgrade-path comment block after line 1 (`name: Links`).

**lint.yml** (3 refs + comment block):

- Line 13: `      - uses: actions/checkout@v4` becomes `      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4`
- Line 16: `      - uses: actions/setup-node@v4` becomes `      - uses: actions/setup-node@49933ea5288caeca8642d1e84afbd3f7d6820020 # v4`
- Line 22: `        uses: DavidAnson/markdownlint-cli2-action@v24` becomes `        uses: DavidAnson/markdownlint-cli2-action@21c1be1b93ad9ed58fa840aacc3f279cde2a72ff # v24`
- Insert the upgrade-path comment block after line 1 (`name: Lint`).

Comment placement is safe because YAML comments are legal anywhere at top level, and all three files currently contain zero comments (context finding), so no convention is violated. Total diff: 7 modified lines, 18 added lines (six comment lines per file; the blank line after `name:` already exists and is kept), 0 removed lines.

## Behavior invariant

Before and after, each workflow resolves to the same action code: `checkout@v4` and `checkout@<sha>` are the same commit today because the verified SHA is what the tag points to. No step, input, trigger, permission, runner, or env value changes. A reviewer confirms this by checking that the diff touches only the seven `uses:` lines and the comment blocks.

## Risks

1. **Annotated tag pitfall (real, hits exactly one of the five).** `DavidAnson/markdownlint-cli2-action@v24` is an annotated tag: tag object SHA `28a7e8bdb81fd8ad675883de92c758ab78e0ce10`, peeled commit `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff`. Pinning the tag object SHA is wrong (and the research found no source stating whether `uses:` would even accept it; the question is moot because the spec pins the peeled commit, correct under either reading). Mitigation: the implementer copies SHAs from this spec's table and never re-derives them (Risk 3's pre-commit re-check is verification only, not re-derivation); verification greps for the exact strings.
2. **Pins freeze.** No Dependabot or Renovate exists in the repo (context finding), so SHAs stay fixed until a maintainer bumps them manually, including for security fixes. This is the accepted cost of pinning (stepsecurity.io names the same dissent). Mitigation is the in-repo upgrade-path comment; automation is explicit backlog, not P9.
3. **Point-in-time values.** Major tags move. The SHAs here are verified as of 2026-09-16; if implementation runs later, a tag may have advanced and "same version" would no longer hold against the live tag. Mitigation: implementation re-runs the commits-API check for each of the five actions before committing, and accepts only a match with this spec's table; a mismatch stops work and reports back rather than silently pinning a newer commit.
4. **Comment format drift.** A future editor replacing `# v4` with prose breaks Renovate's version-comment recognition. Low stakes (no Renovate today); the upgrade-path comment shows the expected line shape.

## Acceptance criteria

1. All seven `uses:` refs in the three workflows are full-length 40-hex SHA pins matching this spec's table exactly.
2. Every pinned line carries its version comment (`# v4`, `# v2`, `# v5`, `# v24` as applicable).
3. Each of the three files contains the upgrade-path comment block under its `name:` line, verbatim per this spec.
4. `git diff` shows no changed lines other than the seven `uses:` lines and the added comment blocks. Permissions blocks, triggers, steps, `with:` inputs, and run scripts are untouched (including lint.yml's absent permissions block and its `npx awesome-lint` line, which P8 owns).
5. Each modified file parses as YAML (for example `python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" <file>` for each of the three), and ref lines keep their original indentation (6-space dash form for checkout/setup-node steps, 8-space form for named steps).
6. The upgrade path (commits-API URL method plus the annotated-tag warning) is present in the repo, satisfying "documented" without external references.

## Research

- https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions (pinning guidance; full-SHA immutability; Dependabot does not alert on SHA-pinned actions)
- https://docs.renovatebot.com/modules/manager/github-actions/ (bare SHA without version comment is disabled by default; basis for the version-comment format)
- https://api.github.com/repos/actions/checkout/commits/v4 (commits-API resolution, method of record, pattern for all five actions)
- https://api.github.com/repos/DavidAnson/markdownlint-cli2-action/git/tags/28a7e8bdb81fd8ad675883de92c758ab78e0ce10 (peeled commit SHA for the annotated v24 tag)
- https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-github-action-cve-2025-30066 (CISA remediation pins a specific commit)
- https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066 (tag-retarget attack the pin defends against)
- https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/ (attack chain analysis; unpinned actions are mutable)

Full graded claim table with retrieval dates: `docs/superpowers/research/2026-09-16-actions-sha-pin-all-workflows-research.md`.

## Codebase context

From the context gate (`docs/superpowers/context/2026-09-16-actions-sha-pin-all-workflows-context.md`), all four success criteria met: the seven-ref inventory above is corroborated by two independent reads (gate grep plus cartographer per-file reads); permissions are `contents: read` plus `issues: write` at stale.yml:8-10 and links.yml:8-10, and lint.yml declares none (P8's territory); no other Actions surface exists anywhere (no action.yml, no composite actions, no reusable-workflow callers), so seven refs is the complete set; and the three files contain zero comments today, so the under-`name:` block placement sets the convention rather than following one. The workspace baseline at context time: HEAD `af077117bec632c636ec914ddb8af002e6e4bc4b`.
