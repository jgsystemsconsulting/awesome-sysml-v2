# Research: Models and Case Studies candidates

## Research brief

**Primary question:** Which open SysML v2 model repositories and case-study packs exist beyond the current awesome-sysml-v2 Example Models list, and which are suitable as curated awesome-list entries for research use?

**Sub-questions:**
1. What is already listed under Example Models in awesome-sysml-v2 (baseline inventory)?
2. Which additional public GitHub (or similar) repos primarily ship SysML v2 models or case studies rather than tools?
3. Which candidates look like real systems / domain case studies (Apollo-class) vs tutorial or book packs?
4. Which candidates fail common awesome criteria (empty, fork-only, not SysML v2, abandoned without foundational value)?
5. Do OMG / SysML community pages point at model packs not already listed?

**Success criteria (decisions this research must support):**
1. Baseline list of the nine current Example Models entries with canonical URLs.
2. At least a shortlist of additional candidate model/case-study repos with URL, one-line description, and source class.
3. Explicit note when a candidate is PROVISIONAL (single source) vs ESTABLISHED.
4. Clear rejects or caution flags (duplicates of listed repos, tool-not-model, dead links).
5. Guidance usable by the spec: expand-in-place with optional Case studies / Learning packs subheads only if enough distinct entries exist; no full-GitHub dump.

**Out of scope:**
- Editing the README.
- Ranking commercial tool sample models that require licenses.
- Building an automated GitHub crawler.
- Deep technical review of model correctness.

**Budget:** 1-2 rounds, ~12 tool calls per lens. Prefer primary repo pages and official community directories.

**Date:** 2026-09-17

## Findings

### Baseline (nine current Example Models)

Canonical URLs already on the list (keep under renamed section):

| Link text | URL |
|-----------|-----|
| airbus/apollo-11-sysml-v2 | https://github.com/airbus/apollo-11-sysml-v2 |
| BruceDouglass/SysML-v2-MasterClass | https://github.com/BruceDouglass/SysML-v2-MasterClass |
| doug-rosenberg/structured-use-cases | https://github.com/doug-rosenberg/structured-use-cases |
| GfSE/SysML-v2-Models | https://github.com/GfSE/SysML-v2-Models |
| MBSE4U/dont-panic-batmobile | https://github.com/MBSE4U/dont-panic-batmobile |
| MBSE4U/sysmod-sysmlv2 | https://github.com/MBSE4U/sysmod-sysmlv2 |
| MBSE4U/the-sysmlv2-book-examples | https://github.com/MBSE4U/the-sysmlv2-book-examples |
| Open-MBEE/structured-use-cases | https://github.com/Open-MBEE/structured-use-cases |
| sensmetry/advent-of-sysml-v2 | https://github.com/sensmetry/advent-of-sysml-v2 |

Digger confirmed these ship actual SysML v2 model content (ESTABLISHED as the baseline set).

### Net-new candidate

| Repo | Verdict | Notes |
|------|---------|-------|
| [MBSE4U/PLEML](https://github.com/MBSE4U/PLEML) | **Add (ESTABLISHED)** | Description "MBPLE Examples (SysML v2)". Tree includes `PLEML/PLEML.sysml` and drone product-line Examples `*.sysml`. Stars 9, last push 2026-06-14, not archived. Meets activity window. |

Suggested blurb: `MBPLE (model-based product line engineering) example models in SysML v2.`

### Rejects and cautions

| Item | Verdict | Why |
|------|---------|-----|
| Systems-Modeling/SysML-v2-Release | **Do not re-list** under Models | Official samples exist under `sysml/` / `kerml/`, but the repo is already under Official Implementations. Cross-section duplicate. |
| MBSE4U/goodSysMLv2 | Reject | Practices library without .sysml model files (PROVISIONAL scout). |
| MBSE4U/SysMLv2JupyterBook | Reject | Jupyter tutorials, not a model pack (PROVISIONAL scout). |
| mycr0ft/awesome-sysml | Reject as source | SysML v1 focus. |
| Tool repos (syson, SysMD, osate, …) | Reject for this section | Tools, not model packs. |
| doug-rosenberg vs Open-MBEE structured-use-cases | **Keep both; b-13 open** | Both `fork:false`, same description string, different tip commits (2026-08-23 vs 2026-09-09). Not a GitHub parent/child fork. Same-project identity still unproven. |

### Subhead guidance

Most of the nine are book, beginner, challenge, or library packs. Apollo-class domain case studies are sparse (Apollo 11, GfSE collection). A `### Case studies` / `### Learning packs` split would leave Case studies thin and fight the single-section alphabetical rule unless each subhead is treated as its own sort bucket. **Recommendation: one H2, no H3 split this pass.**

sysml.org did not surface additional model-pack directories in this research.

## Synthesis

Expand-in-place: rename the section, keep the nine, add **MBSE4U/PLEML** in alphabetical order, do not re-add SysML-v2-Release, do not invent a Projects category, do not split Case studies vs Learning packs until more domain case studies exist. Curated shortlist only; no automated GitHub dump. structured-use-cases dual listing stays; identity resolution remains backlog b-13.

## Sources

| URL | Class | Retrieved |
|-----|-------|-----------|
| https://github.com/Systems-Modeling/SysML-v2-Release | primary | 2026-09-17 |
| https://github.com/MBSE4U/PLEML | primary | 2026-09-17 |
| https://github.com/MBSE4U/goodSysMLv2 | primary | 2026-09-17 |
| https://github.com/airbus/apollo-11-sysml-v2 | primary | 2026-09-17 |
| https://github.com/BruceDouglass/SysML-v2-MasterClass | primary | 2026-09-17 |
| https://github.com/doug-rosenberg/structured-use-cases | primary | 2026-09-17 |
| https://github.com/Open-MBEE/structured-use-cases | primary | 2026-09-17 |
| https://github.com/GfSE/SysML-v2-Models | primary | 2026-09-17 |
| https://github.com/MBSE4U/dont-panic-batmobile | primary | 2026-09-17 |
| https://github.com/sensmetry/advent-of-sysml-v2 | primary | 2026-09-17 |
| https://sysml.org/ | primary | 2026-09-17 |
| https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/README.md | primary | 2026-09-17 |
| https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/contributing.md | primary | 2026-09-17 |
| https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/docs/superpowers/backlog.md | secondary | 2026-09-17 |
| https://github.com/jgsystemsconsulting/awesome-sysml-v2/blob/main/docs/superpowers/runbooks/awesome-submission.md | secondary | 2026-09-17 |
| GitHub REST `repos/MBSE4U/PLEML` and git trees | primary | 2026-09-17 |
| GitHub REST fork metadata for both structured-use-cases repos | primary | 2026-09-17 |
