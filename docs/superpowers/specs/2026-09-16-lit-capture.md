# Design spec: lit-capture (jgs-lit-memory)

Date: 2026-09-16
Status: draft for implementation planning
Mode: Track 3 superpowers, step 1 (spec author)
context: skipped (greenfield tool repo; no existing codebase touched)

## Problem

Research conversations surface scholarly papers, and the next session re-searches the same ones from scratch. lit-capture fixes this with a per-project, git-tracked corpus under `.lit/`: one normalized JSON record per paper, citation edges between them, optional findings notes, and a low-friction inbox for offline capture. A globally installed agent skill drives the capture procedure; a single stdlib-only Python script does the OpenAlex fetching. The agent queries the local corpus instead of re-searching.

Two components ship in v1:

1. The `lit-capture` skill (SKILL.md): reference extraction from the conversation, inbox capture, triage, findings stubs, and corpus query recipes. No code of its own.
2. `lit_fetch.py`: the only component that talks to the network. Fetches by DOI, OpenAlex ID, arXiv ID, or verified title search; normalizes records; appends papers and edges; regenerates the corpus index; reports status; smoke-tests the API forms.

## Corrections and locked facts

- Repo parent path corrected from the dispatch: `C:\Users\gower\Documents\GitHub` does not exist on this machine. The tool repo lives at `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory`, the same parent as existing repos. All other locked constraints unchanged.
- OpenAlex auth model, corrected against the research: the `mailto` polite-pool parameter is ignored per the official deprecations page (https://help.openalex.org/api/deprecations/, dated 2026-08-12); API keys exist since February 2026 (pyalex documentation, https://raw.githubusercontent.com/J535D165/pyalex/master/README.md). Keyless mode still works on a small daily budget; singleton work GETs are free. The design treats keyless as degraded, not broken.

## Goals

- Capture a paper encountered mid-conversation in under a minute, without leaving the chat.
- Keep the corpus inside the project that produced it, tracked in that project's git.
- Never corrupt the corpus on partial failure: writes are per file and atomic.
- Run on Windows Git Bash (primary), also plain Windows Python and POSIX. Python 3 standard library only.
- Make the citation graph useful even where only edge endpoints exist (boundary nodes).

## Non-goals (locked, v1)

- Harness hooks, cron, or GitHub Action freshness sync.
- Pack export or publishing (this is also where reconstructed-abstract licensing risk lives; deferring it keeps v1 clean under OpenAlex CC0 for local use).
- gsd-graphify integration.
- Any UI beyond the CLI and the generated index page.
- Any second metadata source. OpenAlex only.
- Corpus data inside the tool repo. Ever.

## Research

Full findings: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\research\2026-09-16-lit-capture-research.md` (round log and merged pools beside it). Round 2 synthesis grades SC1 through SC7; the load-bearing facts used here:

- Auth and budget: the mailto polite pool is ignored (deprecations page, August 2026); keys exist since February 2026 and lift the daily budget tenfold; keyless daily budget is $0.10; singleton GETs are free, list/filter calls cost $0.10 per 1k, search $1 per 1k. 429 fires on budget exhaustion or over 100 req/s. Response carries X-RateLimit-Limit / Remaining / Credits-Used / Reset and no Retry-After is documented.
  - https://help.openalex.org/api/authentication/
  - https://help.openalex.org/access/example-costs/
  - https://help.openalex.org/api/errors/
- Lookup forms: `/works/doi:10.1038/nature12373` and `/works/https://doi.org/10.7717/peerj.4375` both resolve (live probes). There is no `arxiv` key on the work `ids` object, so arXiv-only papers resolve by verified title search, or by DOI when one exists.
  - https://help.openalex.org/api/get-single-entities/
  - https://help.openalex.org/data/works/attributes/
- Batch: pipe-OR filters accept up to 100 values with `per-page=100`.
  - https://help.openalex.org/api/filtering/
  - Long query URLs can exceed roughly 4 KB and get rejected; split client-side.
    - https://help.openalex.org/api/searching/
- Abstracts exist only as `abstract_inverted_index`, null on roughly 40 to 55 percent of works, and can carry trailing junk. Reconstruction is a position-based join. Never load-bearing.
- `referenced_works` is lossy (not capped): the graph is biased toward DOI-matchable references and must be documented as such.
- Merges: duplicate works 301 to a canonical ID; clients follow redirects.
- License: OpenAlex metadata is CC0; reconstructed abstracts carry an upstream legal caveat that matters only for redistribution (out of scope).
  - https://raw.githubusercontent.com/ourresearch/openalex-docs/main/license.md

## Repository layout and install

New repo at `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory`, `git init`, empty of corpus data.

```
jgs-lit-memory/
  README.md                      prose: what it is, install, usage, limits
  lit_fetch.py                   single file, stdlib only
  test_lit_fetch.py              offline assert-based checks
  skills/lit-capture/SKILL.md    canonical skill copy
```

Install means copy, not link, matching the existing skill mirror pattern (frontmatter conventions per `jgs-paper-voice`): each of these directories gets `SKILL.md` and `lit_fetch.py` copied in.

- `C:\Users\gower\.zcode\skills\lit-capture\`
- `C:\Users\gower\.claude\skills\lit-capture\`
- `C:\Users\gower\.agents\skills\lit-capture\`

The skill invokes the script by the `.zcode` absolute path (`python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" ...`), so all three mirrors stay interchangeable and no PATH setup is needed. README documents the three copy commands and the note that edits happen in the repo, then get re-copied.

## Corpus layout (`.lit/`, in the using repo, git-tracked)

```
.lit/
  papers/<W-id>.json      one normalized record per paper
  graph/edges.jsonl       {"source": citing W-id, "target": cited W-id}, one per line
  graph/aliases.json      {"alias W-id": "canonical W-id"} recorded on 301 merges
  findings/<year>-<slug>.md  optional human notes, written by the agent
  inbox.jsonl             offline capture queue
  SKILL.md                generated corpus contract; never hand-edited
```

The using repo tracks `.lit/` in git by default; nothing to ignore. The skill tells the agent to `git add .lit` after capture.

### Record schema (papers/<W-id>.json)

All identifiers are stored bare: `id` is the bare W-id with the `https://openalex.org/` prefix stripped and always equals the file name; `referenced_works` is a list of bare W-ids; `doi` is lowercase with any `https://doi.org/` prefix stripped (may be null). `display_name`, `publication_date`, `publication_year`, `cited_by_count` keep their OpenAlex values; `authors` is the flattened list of `authorships[].author.display_name`; `topics` is the flattened list of `topics[].display_name`; `oa_url` comes from `open_access.oa_url`; `venue` comes from `primary_location.source.display_name` and may be null. Local fields: `seed` (bool), `captured_at` (ISO 8601 UTC), `source` ("capture" or "fetch"), `abstract` (reconstructed from `abstract_inverted_index` when present, else null; frequently null by design; the joined text is kept verbatim, trailing junk included, which v1 never strips).

File name is the canonical OpenAlex work ID (`W2741809809.json`). The ID inside the record always matches the file name.

### Edge rules

- Direction: `source` cites `target`, taken from `referenced_works` of each fetched paper. Endpoints are bare W-ids.
- 301 merges: when a fetch resolves through a redirect to a canonical W-id different from the requested one, the run records the mapping in `graph/aliases.json`, remaps every existing edge endpoint through the full alias table, and writes the record under the canonical id. Alias remap runs on every edge write, so stale endpoints heal without a separate pass.
- Edges may reference W-ids that have no `papers/<id>.json`. These are boundary nodes. No placeholder records are created for them.
- The generated index counts boundary nodes separately from full records, so the numbers never lie about corpus coverage.
- Promotion of a boundary node is a normal fetch: the skill's query recipes show how to list boundary IDs, and the agent passes them to the batch verb.

## lit_fetch.py contract

Single file. Imports limited to `urllib.request`, `urllib.error`, `urllib.parse`, `json`, `argparse`, `pathlib`, `datetime`, `time`, `re`, `sys`, `os`. One resolution verb per invocation (`--doi`, `--openalex`, `--arxiv`, `--title`, `--ids`, `--inbox`, `--status`, `--check` are mutually exclusive). `--title` doubles as a required modifier of `--arxiv`; `--author` and `--year` are optional modifiers of `--title` and `--arxiv`.

### Verbs (flag-selected modes)

| Invocation | Behavior |
|---|---|
| `--doi <doi>` | Singleton GET `/works/doi:<doi>` (free). Writes one record, seed=true, source="capture". |
| `--openalex <W-id>` | Singleton GET `/works/<W-id>` (free). Same write semantics as `--doi`. |
| `--arxiv <id>` | No dedicated endpoint: OpenAlex has no arXiv external-ID lookup (no `arxiv` key on `ids`; the DOI alias form is unverified and must not be used). Requires `--title` (plus `--author`/`--year` when known) and resolves through the same verified search path as `--title`; a bare `--arxiv` without `--title` is a usage error (exit 2) telling the caller to supply the title or the DOI. seed=true, source="capture". |
| `--title <t>` `--author <surname>` `--year <yyyy>` | GET `/works?search=<t>&per-page=5` (budgeted search call, keyless warning applies). Client-side verification: normalized title must match a candidate exactly (case, punctuation, whitespace folded); author surname and year are checked when given. On a verified hit, write it. On no verified hit, write nothing and print the top candidates for a human decision. Author and year are optional but strongly recommended by the skill. Write semantics match `--doi`: seed=true, source="capture". |
| `--ids "W1\|W2\|..."` | Batch list call: `filter=ids.openalex:<chunk>` with pipe-OR, `per-page=100`, chunks of at most 100 IDs handled internally in order. Chunks are computed after skip/dedupe. IDs requested but absent from the response are reported as failures (404). Skips IDs already in the corpus. Written records get seed=false, source="fetch"; `--seed` overrides seed to true. This is the boundary-promotion and expansion verb. |
| `--inbox` | Triage: read `.lit/inbox.jsonl`, dedupe (below), resolve entries via the same paths as above (title-form and arxiv-form entries resolve through verified search using the entry's title/author/year fields), write promoted records, then rewrite the inbox once, after all resolutions finish, keeping only the entries that remain (failures stay queued with their reason). A crash mid-run leaves the original queue intact; re-runs are idempotent through skip-if-exists. Entries whose `ref` does not parse are reported as failures and stay queued. Promoted entries take seed=true, source="capture". |
| `--status` | Print corpus summary to stdout: paper count, edge count, boundary-node count, inbox pending count, last-synced timestamp (the generated index's timestamp). Read-only; no regeneration. |
| `--check` | Live smoke test of the load-bearing endpoint forms: DOI singleton, W-id singleton, two-ID batch filter, title search. Prints OK or fail per form; exit 1 if any form fails. Run on first use and whenever OpenAlex behaves oddly. |

Common flags: `--dir <path>` (corpus root, default `.lit` relative to cwd; the skill always runs from the repo root), `--api-key <key>` (default `OPENALEX_API_KEY` env), `--seed` (batch override only), `--author <surname>` and `--year <yyyy>` (title-verification modifiers).

### Dedupe and canonicalization

- Dedupe key: canonical OpenAlex work ID, resolved after redirects. When a fetched record's `id` differs from the requested identifier (301 merge), store under the canonical ID, record the alias (see Edge rules), and print a one-line merge note. The DOI alias also resolves to a canonical W-id, so DOI captures dedupe correctly against later W-id captures.
- Skip-if-exists: singleton captures (`--doi`, `--openalex`, `--arxiv`, `--title`) and inbox promotions skip when the canonical record already exists: no write, existing `seed` and `captured_at` untouched, counted as skipped in the summary. The canonical id is only knowable after the fetch, so the skip happens post-fetch.
- Batch skips IDs with an existing `papers/<id>.json` unless absent from the corpus. No refresh semantics in v1; `cited_by_count` staleness is acceptable.
- Inbox dedupe (pure function, unit tested): the corpus known-ID set is the union of (a) canonical W-ids of existing records, (b) bare normalized DOIs of existing records, (c) folded `display_name` of existing records. Each inbox ref normalizes to its key form before comparison (doi: to normalized DOI; W-id to W-id; title-form and arxiv-form to folded title), and an entry is a duplicate when its key matches the set or another entry in the same file.

### Title verification (pure function, unit tested)

`fold(title)`: lowercase, strip punctuation, collapse whitespace. Verification passes when `fold(candidate) == fold(query)` and, when supplied, the candidate's authorships contain the surname (case-folded) and `publication_year` matches. Near-misses never auto-write; they print as candidates. When several candidates fold-match the query, none auto-verifies: the run writes nothing and lists them, and the supplied author or year disambiguates. The skill instructs the agent to re-run with a corrected title or accept a candidate by W-id.

### Network behavior

- Base URL: `https://api.openalex.org`. Singleton responses are a single work object; list, filter, and search responses are envelopes of the shape `{"meta": {...}, "results": [...]}`, and the script reads `results`.
- Auth: append `api_key=<key>` when a key is present. No mailto parameter (it is ignored server-side).
- Keyless warnings: before any budgeted call (batch `--ids`, `--title` search, `--inbox` containing title-form or arxiv-form entries) with no key configured, print one warning line naming the call type and the $0.10/day keyless budget, then proceed. Singleton calls never warn.
- 429 and 5xx: exponential backoff 1, 2, 4, 8, 16 seconds, five attempts maximum, then the chunk fails and is reported. Honor `Retry-After` when the response carries one (observed on live 429s even though the official docs omit it); otherwise use the backoff schedule. Honor `X-RateLimit-Remaining`: when it reads 0, abort the remaining chunks of the run immediately with a budget-exhausted summary; completed writes stand.
- Payload trimming: `select=id,doi,display_name,publication_date,publication_year,authorships,referenced_works,cited_by_count,topics,open_access,primary_location,abstract_inverted_index` (root-level fields only, per OpenAlex).
- Timeouts: 30 seconds per request via urllib.

### Write model and failure handling

- Per record: normalize in memory, then write `papers/<id>.json` atomically (temp file plus `os.replace`). A crash mid-batch leaves completed papers on disk and never a half-written file.
- Edges: after each chunk's record writes succeed, collect that chunk's edges, union with existing edges loaded from `edges.jsonl`, dedupe on (source, target), and rewrite the file atomically. A run that fails mid-way may leave edges one chunk stale; the next successful run heals this because edges are a full-rewrite idempotent union.
- Index: regenerate `.lit/SKILL.md` after any successful write operation (single fetch, batch, inbox triage). Never on `--status`.
- Write verbs auto-create the corpus directory tree (`papers/`, `graph/`, `findings/`) when absent, so first use in a fresh `--dir` works.
- End-of-run summary on stdout, one block: `written=N skipped=M failed=K`, then one line per failure with the identifier and reason (404, verification failed, backoff exhausted, budget exhausted). Exit codes: 0 all requested work succeeded or was already present; 1 any failure; 2 usage error (bad flags, no identifiers given, `--arxiv` without `--title`, malformed direct-verb arguments).

### Generated `.lit/SKILL.md` (the corpus contract)

Template embedded as a string constant in `lit_fetch.py` (keeps the single-file rule). Regenerated on every write. Contents:

- Generated banner: do not edit; regenerated by lit_fetch.py.
- Scope: fixed text naming this as the project's captured literature corpus, captured from research conversations, OpenAlex-sourced.
- Counts table: papers (full records), edges, boundary nodes (edge endpoints without records), inbox pending, generated timestamp (last-synced, ISO 8601 UTC).
- Query recipes, copy-pasteable in Git Bash: grep for a title fragment across `papers/`, extract boundary IDs with a short `python -c` snippet, count edges per paper, find papers citing a given W-id from `edges.jsonl`.
- Graph caveat: `referenced_works` is lossy relative to printed reference lists; treat the graph as biased, not authoritative.
- License note: OpenAlex metadata is CC0; reconstructed abstracts are for local corpus use.

## Skill procedure (skills/lit-capture/SKILL.md)

Frontmatter per the existing `jgs-paper-voice` convention (`name`, one-paragraph `description` naming trigger conditions). Body sections:

1. **When to trigger.** A paper enters the conversation with enough identity to fetch (DOI, arXiv ID, W-id, or exact title plus author/year) and looks worth keeping.
2. **Extract, do not fetch blindly.** Scan the conversation for DOIs (`10.xxxx/...`), arXiv IDs, OpenAlex W-ids, and full titles. This is agent-driven reading, not code-based NLP; the script never parses prose. Dedupe against the corpus by reading the generated `.lit/SKILL.md` counts and grepping `papers/` for the identifiers found.
3. **Capture offline first.** Append one JSONL line per item to `.lit/inbox.jsonl`. Ref grammar: `"ref"` is exactly one of `"doi:<doi>"`, `"W<digits>"`, `"arxiv:<id>"`, `"title:<verbatim title>"`. Title-form and arxiv-form entries also carry `"title"` (verbatim), plus optional `"author"` (surname) and `"year"`. Every entry carries `"note"` (why it came up) and `"added_at"` (ISO timestamp). This works with no network and survives the session.
4. **Fetch now when online.** With user consent or standing habit, run lit_fetch.py per item or as one `--ids` batch. Report the summary block.
5. **Findings stub (optional).** For papers worth a note, write `findings/<year>-<slug>.md` from the template in the skill: title, W-id, why captured, one claim worth remembering. Prose follows the Written Prose Standard.
6. **Triage.** Periodically run `--inbox`. Title-form and arxiv-form entries resolve through their `"title"` field (arXiv entries get theirs from the paper as captured); supply author and year to disambiguate. Drop entries no longer wanted by deleting their lines. Failures stay queued with their reason.
7. **Query the corpus.** Read `.lit/SKILL.md` first each session (counts, recipes, last-synced) and answer literature questions from `papers/` and `graph/edges.jsonl` before re-searching.
8. **Limits.** Abstracts are often null; use the corpus for identity, graph, and retrieval, not as a full-text store.

## Testing

- `test_lit_fetch.py`: offline, assert-based, stdlib `unittest`-free (plain asserts in functions, a `main()` that runs them all, exit nonzero on failure). Covers the pure logic named in the standing rule plus title verification: record normalization from a frozen sample OpenAlex payload, inverted-index abstract reconstruction (including the trailing-junk case and the null case), ID chunking (100 cap, order preserved, duplicates dropped), inbox dedupe (against corpus IDs and within file), title fold and verify (hit, near-miss rejection, surname and year checks), edge union dedupe.
- `--check`: the live half, exercising all four endpoint forms and reporting per form.
- Manual acceptance in the plan: a live DOI capture into a throwaway `--dir`, a `--status` run whose counts match the files on disk, an interrupted batch that leaves valid JSON on disk.

## Files to create (implementation plan input)

1. `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory\lit_fetch.py`
2. `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory\test_lit_fetch.py`
3. `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory\skills\lit-capture\SKILL.md`
4. `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory\README.md`
5. Installed copies of SKILL.md and lit_fetch.py in the three skill mirror directories.

## Acceptance checks

- `python test_lit_fetch.py` passes offline on Windows Git Bash.
- `python lit_fetch.py --check` reports OK on all four endpoint forms with a key set.
- `python lit_fetch.py --doi 10.1038/nature12373 --dir <tmp>` writes one canonical-ID JSON record, prints a summary, and regenerates the index; `--status` agrees with the files on disk.
- A 150-ID `--ids` run into a fresh `--dir` issues exactly two batch calls (100 plus 50) and prints a keyless warning first when no key is set.
- All repo markdown prose (README, skill copies) passes `python ~/.zcode/scripts/prose_check.py` with no unjustified findings; no em dashes anywhere in the repo prose. The embedded index template is held to the same standard, asserted em-dash-free by `test_lit_fetch.py`.
- The three skill mirrors hold identical SKILL.md and lit_fetch.py copies.

Mechanical gate note for this spec: `prose_check.py` reports 30 spaced-double-hyphen findings, every one a CLI command flag (`--doi`, `--ids`, `--check` and siblings) inside backticks in the contract tables. The avoid-ai-writing dash rule excludes command flags from the count; the flags stay as written because renaming them to satisfy the detector would corrupt the CLI contract they define. No em dashes exist in this file.

## Open questions

None. All design forks named in the dispatch are settled above; the repo-parent path correction is a filesystem fact, not a product decision.
