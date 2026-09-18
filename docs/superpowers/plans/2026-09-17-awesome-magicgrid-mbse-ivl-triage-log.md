# IVL triage log: 2026-09-17-awesome-magicgrid-mbse

Target: implemented worktree C:\Users\gower\OneDrive\Documents\GitHub\awesome-magicgrid-mbse (+ template README cross-link)
Plan: docs/superpowers/plans/2026-09-17-awesome-magicgrid-mbse.md
Spec: docs/superpowers/specs/2026-09-17-awesome-magicgrid-mbse.md

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|

## Check commands

- `npx awesome-lint@2.3.0 README.md` (cwd new repo)
- `npx markdownlint-cli2 "README.md" "contributing.md"`
- `lychee --accept '200,204,301,308,403' --no-progress --max-retries 3 README.md` (PATH includes ~/bin)
- `gh run list -R jgsystemsconsulting/awesome-magicgrid-mbse --workflow Lint --limit 1`
- `curl -sSL -o /dev/null -w '%{http_code}' https://jgsystemsconsulting.github.io/awesome-magicgrid-mbse/`
- section-count python recount; cross-link greps; CC0 greps

## Baseline
### awesome-lint
- Linting
✔ Linting
EXIT:0
### markdownlint
markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)
Finding: README.md contributing.md
Linting: 2 files
Summary: 0 issues in 0 files
EXIT:0
### lychee
🔍 58 Total (in 2s 90ms) 🔗 58 Unique ✅ 58 OK 🚫 0 Errors 🔀 14 Redirects

Hint: Followed 14 redirects. You might want to consider replacing redirecting URLs with the resolved URLs. Use verbose mode (`-v`/`-vv`) to see redirection details.
EXIT:0
### CI tip
completed	success	Fix MoEs expansion to measures of effectiveness	Lint	main	push	35255411361	25s	2026-09-17T17:52:53Z
### Pages
200
### sections
entries 55
4 Official Resources
2 Books and Formal Publications
12 Papers and Case Studies
4 Training and Courses
10 Videos and Talks
2 Example Models
3 Tool Support
4 Community
5 Related Methodologies
disclaimer True
sister_new 1
cc0_license True
cc0_citation True
mit_site False
magicgrid_css_lib False
### template cross-link
4:For the MagicGrid MBSE methodology, see the sister list [awesome-magicgrid-mbse](https://github.com/jgsystemsconsulting/awesome-magicgrid-mbse).

| C1 Goodreads/catalog link fails lychee (README Books) | R1 | R1 | Genuine | Flaky/non-accept status (202/503/timeout) on catalog URLs; replaced with stable Google Books search + vendor page |
| M1 Intro sister markdown link count 1 | R1 | R1 | Design | Task 7 dropped intro href for remark-lint double-link; bidirectional AC via Related + docs + template |
| M2 Example Models missing sysml-magicgrid-vccs | R1 | R1 | Genuine | Restored VCCS sample; section now 3 entries sorted |
| A1 First CI lint fail on topics | R1 | R1 | Advisory-skipped | Historical; tip green after Task 8 meta |
| A2 Redirect hygiene | R1 | R1 | Advisory-skipped | Gate-neutral |

## Round 1 Summary

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| C1 Books catalog lychee fail | behavior, regression, contract | CRIT | Genuine | Fixed |
| M1 intro sister link count | behavior | MAJ | Design | Wontfix (Round 1) |
| M2 VCCS sample missing | behavior | MAJ | Genuine | Fixed |
| A1 first CI fail | behavior | ADV | Advisory-skipped | Skipped (Round 1) |
| A2 redirects | regression | ADV | Advisory-skipped | Skipped (Round 1) |

Fixes applied: 2
Inflation rate: 0% (0 of 3 CRITICAL+MAJOR findings triaged FP; 1 Design)
Validation: PASS
Commands: awesome-lint -> 0; markdownlint -> 0; lychee x3 -> 0 Errors each; push f60d1a7

## Round 2 Summary

Confirmation wave for Round 1 Genuine fixes (Books catalog URL, VCCS sample). All three lenses: resolved / still stands with evidence. Merged verdict NO_CRITICAL_OR_MAJOR.

| Finding | Lens | Severity | Verdict | Action |
|---------|------|----------|---------|--------|
| Books catalog lychee (confirm) | behavior, regression, contract | CRIT | resolved by this change | Confirmed |
| VCCS sample (confirm) | behavior, contract | MAJ | resolved by this change | Confirmed |
| (none new CRIT/MAJ) | - | - | - | - |

Fixes applied: 0
Inflation rate: n/a (0 CRITICAL+MAJOR findings this round)
Validation: PASS
Commands: awesome-lint 0; markdownlint 0; lychee 59 OK 0 Errors; CI lint 35257606788 success

## Converged: Round 2

Track 1: Merged verdict NO_CRITICAL_OR_MAJOR.
Total rounds: 2  |  Total fixes: 2
Implementation verification ready.

