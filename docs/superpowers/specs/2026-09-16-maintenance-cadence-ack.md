# maintenance-cadence-ack (P4) design spec

Work package P4 of awesome-sysml-v2. Absorbs intent #3 (maintenance plan): the plan now exists as automation and only needs to be written down. Documentation-only change to `contributing.md` and `README.md`.

## Problem

The repo runs three maintenance automations, all landed by P6, P7, and P8: a weekly link scan, a monthly freshness report, and blocking lint gates. Nothing in the repo's human-facing docs says any of this. A contributor reading contributing.md learns the local commands and stops there; a maintainer looking for the cadence has to open workflow YAML. The cadence was real but undocumented, and undocumented automation is indistinguishable from neglect.

The weekly-scan question from the packages discussion is settled by the facts: yes, `links.yml` already covers it, with its Monday cron plus the PR-time advisory run. P4 documents what exists and changes no behavior.

## Goals

- Add a top-level `## Maintenance` section to contributing.md, placed after the `### Link check` subsection, describing the three automations exactly as the amended workflows behave.
- Extend the README Contributing one-liner so its pointer list names maintenance.
- Absorb the drift traps from the context gate: advisory versus blocking asymmetry, failure-only versus always upsert, github.com-only freshness scope, push-based freshness measurement, and the commit-versus-push wording note for criterion 4.

## Non-goals

- No workflow file changes. P6, P7, P8, and P9 own the workflows; all landed at HEAD b562394.
- No new cron schedules and no daily scans.
- No awesome-list entry content changes (the README Contributing pointer line is documentation, not a list entry).
- No editorial SLA tooling.
- No re-litigation of the 24-month window or the upsert and label design; those are facts to describe.

## Design

### Placement

contributing.md at HEAD b562394 is 40 lines: `## Inclusion criteria` (line 5), `## Entry format` (13), `## Local commands` (23) with the npx fence (27-30) and the `### Link check` subsection (32-40). The new section is appended at the end of the file, after the Link check subsection, as a `##` sibling of `## Local commands`, not a `###` child of it. Reading order stays contributor instructions first, maintainer cadence last. The file's style is terse and imperative; the section text below matches it.

### Exact new section text for contributing.md

Append verbatim after line 40:

````markdown
## Maintenance

Three automated workflows keep the list current. They live in `.github/workflows/` and need no manual upkeep; this section describes what each one does so contributors and maintainers can tell automation from neglect.

### Link scan (weekly)

`links.yml` checks the links in every Markdown, HTML, and reStructuredText file in the repository every Monday at 18:00 UTC, on every pull request, and on manual dispatch. The check is advisory: a PR with broken links gets a warning but is never blocked by it. The "Link Checker Report" issue is created or updated only when links actually break; a week with no broken links leaves that issue untouched.

### Freshness report (monthly)

`stale.yml` runs on the first day of each month at 06:00 UTC, or on manual dispatch. It collects the `github.com` repository URLs from README.md and lists repos with no push in the last 24 months. The report is advisory: an entry past the window can still be valid under the foundational-value exception (criterion 4). The "Freshness report" issue is refreshed on every run, including months with no stale entries. Criterion 4 speaks of a commit within 24 months; the report measures the repository's last push, which is usually but not always the same thing.

### Lint gates (every PR and push to main)

`lint.yml` runs `awesome-lint@2.3.0` on README.md, and `markdownlint` on README.md and contributing.md, on every pull request targeting main and every push to main. These gates block merge on failure. The local markdownlint command above installs an unpinned npx package and may differ from the version CI runs; the pinned `awesome-lint@2.3.0` matches CI exactly.
````

Facts pinned in that text, each verified against the workflow files at HEAD b562394:

- links.yml: weekly cron `0 18 * * 1` (Monday 18:00 UTC), `pull_request` trigger, `fail: false` with a `::warning::` step summary, issue step gated on `github.event_name != 'pull_request' && exit_code != 0`. Advisory, never blocking; report issue upserts on broken links only.
- stale.yml: monthly cron `0 6 1 * *` (06:00 UTC, day 1), 24-month cutoff compared against `pushed_at`, URL grep restricted to `https://github.com/` in README.md, unconditional create-or-update of the "Freshness report" issue, foundational-value exception named in the report body.
- lint.yml: `pull_request` and `push` on main, `npx awesome-lint@2.3.0` plus the markdownlint-cli2 action, both blocking; local markdownlint is unpinned npx (contributing.md line 29).

### README one-liner rewrite

Current line 128, the entire body of `## Contributing`:

```markdown
See [contributing.md](contributing.md) for the inclusion criteria, entry format, and local lint commands.
```

Replacement:

```markdown
See [contributing.md](contributing.md) for the inclusion criteria, entry format, local lint commands, and maintenance cadence.
```

The pointer stays one line and its list now names maintenance, so a README reader can tell the doc covers the cadence before clicking through. The wording change touches no awesome-lint rule.

## Risks

- **Doc drift on future workflow edits.** The section names filenames, times, and thresholds. A later workflow change must update the section in the same PR; the acceptance criteria pin today's behavior so any drift is caught at review.
- **Commit-versus-push flattening.** Criterion 4 says "commit within 24 months"; the freshness job measures `pushed_at`. Writing them as identical would introduce a false claim into the docs. The section carries one sentence distinguishing them, and an acceptance criterion pins it.
- **Local and CI markdownlint divergence.** Already true before this change. The section documents it rather than hiding it, and treats the CI action as authoritative.
- **Coverage gap misread.** awesome-lint lints README.md only, so the new contributing.md section is gated by the markdownlint action alone. No new gap, but reviewers should not expect awesome-lint coverage there.

## Acceptance criteria

1. contributing.md contains `## Maintenance` as a top-level heading placed after the `### Link check` subsection, and the section describes all three automations accurately:
   - link scan runs weekly Monday 18:00 UTC plus an advisory PR-time run that never blocks merge;
   - the Link Checker Report issue upserts only when links break; clean weeks never touch it;
   - the freshness report runs monthly on day 1 at 06:00 UTC, uses a 24-month window measured on last push, covers github.com repository URLs from README only, upserts the Freshness report issue on every run including clean months, and acknowledges the foundational-value exception;
   - lint gates block on every PR targeting main and every push to main, running `awesome-lint@2.3.0` on README.md plus markdownlint on README.md and contributing.md, with the local markdownlint flagged as unpinned and possibly different from CI;
   - one sentence distinguishes criterion 4's "commit within 24 months" from the push-based measurement.
2. README's Contributing one-liner is extended to include maintenance in its list, per the exact replacement above.
3. `npx markdownlint-cli2 "README.md" "contributing.md"` exits 0.
4. `npx awesome-lint@2.3.0 README.md` exits 0.
5. `git diff --name-only` against the base commit lists exactly `README.md` and `contributing.md`. No file under `.github/workflows/` is added, modified, or deleted, and no other files change.

## Codebase context

From the context gate (`docs/superpowers/context/2026-09-16-maintenance-cadence-ack-context.md`, verdict CONTEXT_COMPLETE, 8/8 claims), re-verified directly against the working tree before writing this spec. HEAD b562394. contributing.md is 40 lines with sections at 5, 13, 23, and the Link check subsection at 32-40; no maintenance or cadence text exists anywhere yet. README's `## Contributing` is lines 126-128, one sentence delegating to contributing.md. `.markdownlint-cli2.jsonc` disables only MD013, so the long lines in the new section are safe. Heading style is `##` top level, `###` subsection, with no heading-order lint constraints. The context doc's drift traps are carried verbatim into the Goals and Acceptance criteria above.

## Research

research: skipped (no-open-world-questions; documents the repo's own automation)

Round 0 log: `docs/superpowers/research/2026-09-16-maintenance-cadence-ack-research-log.md`. All behavioral claims in this spec were checked against `.github/workflows/links.yml`, `.github/workflows/stale.yml`, `.github/workflows/lint.yml`, `contributing.md`, and `README.md` at the current working tree.
