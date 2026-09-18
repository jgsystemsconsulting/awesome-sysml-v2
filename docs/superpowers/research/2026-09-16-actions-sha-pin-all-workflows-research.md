# Research: actions-sha-pin-all-workflows (P9)

## Research brief

- **Primary question**: For each of the five GitHub Actions referenced by the repo's workflows, what is the commit SHA that its current version tag points to, so `uses:` refs can be pinned by full-length SHA?
- **Sub-questions**: per-action tag-to-SHA resolution for actions/checkout@v4, actions/setup-node@v4, lycheeverse/lychee-action@v2, peter-evans/create-issue-from-file@v5, DavidAnson/markdownlint-cli2-action@v24.
- **Success criteria**: SC1 each SHA from a primary source; SC2 each SHA records tag + retrieval date; SC3 pinning pitfalls surfaced.
- **Out of scope**: whether to pin (decided, P9); awesome-lint npm version (P8); Dependabot setup (backlog).
- **Budget**: cap 3 rounds; used 2.

## Findings

Decision-bearing (all ESTABLISHED, retrieved 2026-09-16):

| Action | Tag | Commit SHA | Tag type | Independent paths |
|--------|-----|-----------|----------|-------------------|
| actions/checkout | v4 | `11d5960a326750d5838078e36cf38b85af677262` | lightweight | commits API + refs API |
| actions/setup-node | v4 | `49933ea5288caeca8642d1e84afbd3f7d6820020` | lightweight | commits API + refs API + releases page |
| lycheeverse/lychee-action | v2 | `e7477775783ea5526144ba13e8db5eec57747ce8` | lightweight | commits API + refs API + releases page |
| peter-evans/create-issue-from-file | v5 | `e8ef132d6df98ed982188e460ebb3b5d4ef3a9cd` | lightweight | commits API + refs API + releases page |
| DavidAnson/markdownlint-cli2-action | v24 | `21c1be1b93ad9ed58fa840aacc3f279cde2a72ff` | **annotated** (tag object `28a7e8bdb81fd8ad675883de92c758ab78e0ce10`) | commits API + git/tags peel |

Supporting claims:

- Official guidance: pinning to a full-length commit SHA is currently the only way to use an action as an immutable release (docs.github.com security-hardening, primary; single doc, scout+skeptic same URL).
- tj-actions/changed-files, March 2025: attackers rewrote existing version tags; hash-pinned consumers were not impacted (wiz.io 2025-03-15; unit42.paloaltonetworks.com 2025-03-20, both secondary; CISA remediation pins a specific commit, primary, 2025-03-26).
- Dependabot "will not create alerts for actions pinned to SHA values" (docs.github.com, primary).
- Renovate: "Actions pinned to a bare SHA without a version comment are disabled by default" (docs.renovatebot.com, primary) — version comments on pin lines keep bot updates enabled and aid readability.
- Maintenance dissent: SHA pins force manual bumps even for minor updates (stepsecurity.io 2024-10-14, secondary).
- A pin is point-in-time; automerge can move a pin without diff review (securitylab.github.com, primary).
- GitHub immutable-actions roadmap item closed as not planned (github/roadmap#592, primary).
- No 2025-2026 supply-chain compromise of the five named actions was found (skeptic absence claim, PROVISIONAL).

## Synthesis

Distinct source counts per decision-bearing claim: checkout 2, setup-node 3, lychee-action 3, create-issue-from-file 3, markdownlint-cli2-action 2. All five ESTABLISHED with at least two independent primary retrieval paths (commits API, git refs/tags API, releases pages). The annotated-tag pitfall is real for exactly one of the five (markdownlint-cli2-action v24): the refs API returns the tag object SHA first; the pinned value must be the peeled commit SHA, which round 1 verified through two paths and which matches the digger's commits-API value. Open question named and closed: no primary source states whether `uses:` would reject a tag-object SHA; the question is moot because the spec pins the peeled commit SHA, correct under either reading. Non-decision-bearing PROVISIONAL claims (API method docs, enterprise policy, git tag semantics) are minor and named here. Eight skeptic URL probes failed (github.blog changelog guesses, one Stack Overflow 403, one DNS failure); none is tied to a graded claim. Method of record for future bumps: `https://api.github.com/repos/<owner>/<repo>/commits/<tag>` returns the commit SHA directly and is the upgrade path the in-repo comment should document.

## Sources

| URL | Class | Used for |
|-----|-------|----------|
| https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions | primary | pinning guidance; Dependabot alert note |
| https://docs.github.com/en/rest/git/refs?apiVersion=2022-11-28 | primary | refs API method |
| https://docs.github.com/en/rest/commits/commits?apiVersion=2022-11-28 | primary | commits API method |
| https://api.github.com/repos/actions/checkout/commits/v4 | primary | checkout SHA |
| https://api.github.com/repos/actions/checkout/git/ref/tags/v4 | primary | checkout tag type |
| https://api.github.com/repos/actions/setup-node/commits/v4 | primary | setup-node SHA |
| https://api.github.com/repos/actions/setup-node/git/ref/tags/v4 | primary | setup-node SHA (path 2) |
| https://github.com/actions/setup-node/releases/tag/v4 | primary | setup-node SHA (path 3) |
| https://api.github.com/repos/lycheeverse/lychee-action/commits/v2 | primary | lychee-action SHA |
| https://api.github.com/repos/lycheeverse/lychee-action/git/ref/tags/v2 | primary | lychee-action SHA (path 2) |
| https://github.com/lycheeverse/lychee-action/releases/tag/v2 | primary | lychee-action SHA (path 3) |
| https://api.github.com/repos/peter-evans/create-issue-from-file/commits/v5 | primary | create-issue-from-file SHA |
| https://api.github.com/repos/peter-evans/create-issue-from-file/git/ref/tags/v5 | primary | create-issue-from-file SHA (path 2) |
| https://github.com/peter-evans/create-issue-from-file/releases/tag/v5 | primary | create-issue-from-file SHA (path 3) |
| https://api.github.com/repos/DavidAnson/markdownlint-cli2-action/commits/v24 | primary | markdownlint SHA |
| https://api.github.com/repos/DavidAnson/markdownlint-cli2-action/git/ref/tags/v24 | primary | annotated tag object SHA |
| https://api.github.com/repos/DavidAnson/markdownlint-cli2-action/git/tags/28a7e8bdb81fd8ad675883de92c758ab78e0ce10 | primary | peeled commit SHA |
| https://www.wiz.io/blog/github-action-tj-actions-changed-files-supply-chain-attack-cve-2025-30066 | secondary | tag-retarget incident |
| https://unit42.paloaltonetworks.com/github-actions-supply-chain-attack/ | secondary | attack chain, mitigation |
| https://www.cisa.gov/news-events/alerts/2025/03/18/supply-chain-compromise-third-party-github-action-cve-2025-30066 | primary | CISA remediation |
| https://www.stepsecurity.io/blog/github-actions-security-best-practices | secondary | maintenance dissent |
| https://docs.renovatebot.com/modules/manager/github-actions/ | primary | version-comment requirement |
| https://git-scm.com/book/en/v2/Git-Basics-Tagging | primary | annotated tag semantics |
| https://docs.github.com/en/enterprise-cloud@latest/admin/enforcing-policies/enforcing-policies-for-your-enterprise/enforcing-policies-for-github-actions-in-your-enterprise | primary | enterprise pin policy |
| https://github.com/github/roadmap/issues/592 | primary | immutable actions not planned |
| https://securitylab.github.com/resources/github-actions-building-blocks/ | primary | point-in-time pin caveat |
