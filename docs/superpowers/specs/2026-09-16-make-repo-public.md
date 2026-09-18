# Spec: make-repo-public (P1)

- Date: 2026-09-16
- Package: P1 of the awesome-sysml-v2 work packages
- Status: design locked; ready for plan
- Research gate: skipped (no-open-world-questions)
- Context gate: skipped (nothing-to-map)

## Problem statement

The repository `jgsystemsconsulting/awesome-sysml-v2` is private (`isPrivate: true`, confirmed in earlier rounds). Every later package in the ordering depends on public visibility: the docs site (P2) needs a public homepage target, the awesome.re submission (P3) requires a public repo, and an awesome-list nobody can read has no value. P1 flips visibility to public and verifies nothing else broke in the process.

This is a GitHub settings operation. No file changes, no commits, no CI edits.

## Goals

1. Flip repository visibility to public.
2. Confirm description and topics survive the change unchanged.
3. Confirm the three Actions workflows (lint, links, freshness) are enabled and will run under public-repo defaults.
4. Confirm policy readiness before the flip: no secrets in git history (advisory a-09 verdict) and that verdict covers current HEAD.

## Non-goals

- docs/ site authoring (P2); homepageUrl (P2 wires it).
- Community meta files (P5).
- awesome.re submission (P3).
- Entry curation.
- Any CI or workflow file change. A disabled workflow discovered during verification is a finding to report, not a fix to apply here.
- Org-level settings changes (fork policy, member permissions). Out of scope; do not touch.

## Research

research: skipped (no-open-world-questions; platform-settings operation, no external fact to learn)

Round 0 Track 3 log: `docs/superpowers/research/2026-09-16-make-repo-public-research-log.md`. Command syntax is verified at execution time against the installed gh.

## Codebase context

Context gate skipped (nothing-to-map): P1 changes GitHub repo settings, not workspace files. Log: `docs/superpowers/context/2026-09-16-make-repo-public-context-log.md`.

Known facts from earlier rounds:

- Description is set.
- Topics are set: awesome, awesome-list, mbse, sysml, sysml-v2.
- `isPrivate` is true.
- Three workflows present (lint, links, freshness); actions SHA-pinned (P9).
- Advisory a-09 (round-2 review) verified no committed secrets in history.
- No CITATION issues.

## Design

### Tooling

`gh` 2.88.0 is installed and supports `--accept-visibility-change-consequences` (confirmed against `gh repo edit --help` at spec time). The executor re-checks the flag at execution in case gh changed; the REST fallback below covers the unsupported case.

### Pre-flip checks

Run all three before the flip. Abort on any failure and report.

1. Identity and state:

   ```
   gh repo view jgsystemsconsulting/awesome-sysml-v2 --json isPrivate,description,repositoryTopics
   ```

   Assert `isPrivate == true`. A false value means the repo is already public (the work may be done; verify and close) or the command hit the wrong repo (abort); discriminate by matching the recorded description and topic names before closing. Record the exact `description` string and the topics as a sorted list of name strings (`.[].name | sort`); post-flip comparison normalizes both captures to sorted topic-name strings before comparing, because the gh capture carries name objects while the anonymous REST payload carries plain strings.

2. Secret-scan currency, recorded: the a-09 verdict (round-2 review, 2026-09-15) verified no committed secrets and its review predates commit `af07711`. Scan the delta `af07711..HEAD` (workflow YAML, contributing.md, PR template — all authored in this pipeline) with:

   ```
   git log -p af07711..HEAD | grep -inE 'password|passwd|api[_-]?key|BEGIN [A-Z]+ PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|github_pat_' | grep -vF '${{ secrets.'
   ```

   The trailing exclusion removes Actions secret-REFERENCE lines (`${{ secrets.NAME }}`): those are indirections to GitHub-hosted secrets, not credential values, and every workflow in this repo uses that idiom. The exclusion is line-granular: a real credential sharing a line with a `${{ secrets.` reference would be filtered with it; that co-occurrence is an accepted residual for this delta, and any doubted line is triaged manually. No hits = pass. Any surviving hit blocks the flip. Record in the run report: the baseline SHA (`af07711`), the command verbatim, its output (empty), and HEAD scanned. The gate is not satisfied by prose; the recorded artifact is the flip precondition.

3. Flag availability: `gh repo edit --help | grep accept-visibility-change-consequences`. If absent, use the REST fallback in the flip step.

### Flip

Primary:

```
gh repo edit jgsystemsconsulting/awesome-sysml-v2 --visibility public --accept-visibility-change-consequences
```

Fallback when the installed gh lacks the flag (equivalent REST call; the acknowledge flag is a gh-cli guard, not an API requirement):

```
gh api -X PATCH repos/jgsystemsconsulting/awesome-sysml-v2 -f private=false
```

### Post-flip verification

1. Anonymous reachability and state. `gh api` always authenticates, so anonymity is proven with an unauthenticated curl:

   ```
   curl -s -o /dev/null -w "%{http_code}" https://api.github.com/repos/jgsystemsconsulting/awesome-sysml-v2
   curl -s https://api.github.com/repos/jgsystemsconsulting/awesome-sysml-v2
   ```

   The first must print 200. The second must show `"visibility": "public"`, and its `topics` and `description` must equal the pre-flip capture after normalizing topics to sorted name strings. Rate-limit fallback: unauthenticated api.github.com is capped at 60 requests/hour per IP; on HTTP 403 with a rate-limit body, retry after the window or use the HTML fallback `curl -s -o /dev/null -w "%{http_code}" https://github.com/jgsystemsconsulting/awesome-sysml-v2` (200 proves anonymous reachability; the API payload fields are then confirmed with the authenticated `gh api` call, and anonymity stands proven by the HTML 200).

2. Actions state:

   ```
   gh workflow list -R jgsystemsconsulting/awesome-sysml-v2 --all
   ```

   The lint, links, and freshness workflows must appear with state `active`. Public repos run Actions by default with no minute billing, so no enabling step is expected.

### Rollback

Flip back with the same command and `--visibility private`. The setting reverses immediately; exposure does not. Any fork, clone, or crawler capture made while public persists after the setting returns to private. Treat content exposure as permanent once the flip succeeds, even if visibility later reverts. This asymmetry is why the pre-flip checks gate the flip instead of relying on rollback.

## Risks

- Irreversible history exposure. Going public makes every commit in history world-readable, permanently, through forks, clones, and archive crawls. Mitigation: advisory a-09 verified no committed secrets, and the pre-flip currency check covers commits since that review. The repo is an awesome-list; its content is curated links to public resources by design.
- Fork and spam exposure. Public repos attract spam issues, drive-by PRs, and auto-forks. Community meta files (templates, moderation guidance) are P5, so P1 accepts this as a residual risk for the gap between P1 and P5. Org fork policy stays untouched.
- Actions surface under public defaults. Workflow runs and their artifacts become publicly visible; run minutes are free on public repos. The three workflows produce no sensitive artifacts and their actions are SHA-pinned (P9), so the supply-chain surface is unchanged.
- Wrong-target flip. Every command uses the fully qualified `owner/repo` name, and the pre-flip `isPrivate` assertion aborts if the target does not match expectations.

## Acceptance criteria

1. An unauthenticated GET of `https://api.github.com/repos/jgsystemsconsulting/awesome-sysml-v2` returns HTTP 200 with `"visibility": "public"`.
2. The anonymous payload's `description` and `topics` match the pre-flip capture exactly (description set; topics: awesome, awesome-list, mbse, sysml, sysml-v2).
3. `gh workflow list -R jgsystemsconsulting/awesome-sysml-v2 --all` lists the three workflows by name `Lint`, `Links`, and `Freshness report`, each with state `active`.
4. The package produces zero changes to workspace content files and zero commits. (Process artifacts under `docs/superpowers/` are exempt; they are the pipeline's own records.)

## Open questions

None. All design decisions are locked by the packages document and the dispatch.
