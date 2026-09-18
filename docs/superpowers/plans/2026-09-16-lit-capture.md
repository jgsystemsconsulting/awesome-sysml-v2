# lit-capture (jgs-lit-memory) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `jgs-lit-memory`: a stdlib-only `lit_fetch.py` that captures OpenAlex works into a per-project git-tracked `.lit/` corpus (records, citation edges, aliases, inbox, generated index), plus the `lit-capture` agent skill that drives capture, triage, and corpus queries.

**Architecture:** One Python file with four layers: pure corpus logic (normalize, fold/verify, chunk, dedupe, edge union, alias remap, index template), a network layer behind a single `http_get` seam the offline tests fake, an atomic write model (temp file plus `os.replace` everywhere), and flag-selected CLI verbs. A generated `.lit/SKILL.md` contract and a hand-written agent skill sit on top. Corpus data never enters the tool repo.

**Tech Stack:** Python 3.9+ standard library only (`urllib`, `json`, `argparse`, `pathlib`, `datetime`, `time`, `re`, `sys`, `os`), git, Windows Git Bash as primary shell.

**Spec:** `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-lit-capture.md` (executors read the spec alongside this plan; the spec's locked facts and acceptance checks govern).

## Global Constraints

Copied from the spec. Every task implicitly includes these.

- Repo: `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory`, `git init`, branch `main`, empty of corpus data. Corpus data inside the tool repo is a locked non-goal, ever.
- `lit_fetch.py` is a single file. Imports limited to: `urllib.request`, `urllib.error`, `urllib.parse`, `json`, `argparse`, `pathlib`, `datetime`, `time`, `re`, `sys`, `os`.
- Verbs `--doi`, `--openalex`, `--arxiv`, `--title`, `--ids`, `--inbox`, `--status`, `--check` are mutually exclusive; one per invocation. `--title` doubles as a required modifier of `--arxiv`. `--author` and `--year` are optional modifiers of `--title` and `--arxiv`. Common flags: `--dir` (default `.lit` relative to cwd), `--api-key` (default env `OPENALEX_API_KEY`), `--seed` (batch override only).
- Exit codes: 0 all requested work succeeded or was already present; 1 any failure; 2 usage error (bad flags, no identifiers, `--arxiv` without `--title`, malformed direct-verb arguments).
- Base URL `https://api.openalex.org`. No `mailto` parameter ever (the polite pool is ignored per the deprecations page). Append `api_key=<key>` only when a key is present.
- Payload trim: `select=id,doi,display_name,publication_date,publication_year,authorships,referenced_works,cited_by_count,topics,open_access,primary_location,abstract_inverted_index`.
- Batch: `filter=ids.openalex:<pipe-OR>`, `per-page=100`, chunks of at most 100 IDs. Search: `per-page=5`. Timeouts: 30 seconds per request.
- Retry: 429 and 5xx back off 1, 2, 4, 8, 16 seconds across at most 5 attempts; `Retry-After` overrides the schedule when present; `X-RateLimit-Remaining: 0` aborts remaining chunks immediately.
- Keyless mode is degraded, not broken: one warning line naming the call type and the $0.10/day keyless budget before any budgeted call (batch `--ids`, `--title` search, `--inbox` with title-form or arxiv-form entries). Singleton calls never warn.
- All writes atomic: temp file in the target directory plus `os.replace`. Index `.lit/SKILL.md` regenerates after any successful write operation; never on `--status`.
- Record IDs bare (`W2741809809`), file name equals record `id`; DOIs lowercase with `https://doi.org/` stripped; `referenced_works` bare W-ids.
- Repo prose (README, skill copies, embedded index template) contains no em dashes and passes `python ~/.zcode/scripts/prose_check.py` with no unjustified findings. Backticked CLI flags (`--doi`) are a documented prose_check false positive; the flags stay as written.
- Windows Git Bash is the primary shell; also plain Windows Python and POSIX. Python 3.9 minimum.
- Every task ends with one conventional commit (`type(lit): ...`) made from the repo root; working tree clean before the next task starts.
- Listing order inside tasks is implementation-first, tests-second by design: a task's suite run is already green once its listing is applied, so the run steps say so explicitly. There is no per-task red run; red/green discipline lives in the per-assert test structure and Task 9's final sweep.

## Research

Full findings: `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\research\2026-09-16-lit-capture-research.md` (Track 3, converged in 2 rounds; round log and merged pool beside it). Load-bearing facts this plan relies on, with primary sources:

- Auth and budget: API keys since 2026-02-13; `mailto` ignored; keyless daily budget $0.10; singleton GETs free; list/filter $0.10 per 1k; search $1 per 1k; 429 fires on budget exhaustion or over 100 req/s. https://help.openalex.org/api/authentication/ and https://help.openalex.org/access/example-costs/ and https://help.openalex.org/api/deprecations/
- 429 semantics, `X-RateLimit-*` headers, 301 merge redirects: https://help.openalex.org/api/errors/
- DOI singleton forms verified by live probes: `/works/doi:10.1038/nature12373` and `/works/https://doi.org/10.7717/peerj.4375` both resolve. https://help.openalex.org/api/get-single-entities/
- No `arxiv` key on the work `ids` object; arXiv-only papers resolve by verified title search. https://help.openalex.org/data/works/attributes/
- Pipe-OR filters accept up to 100 values with `per-page=100`; long query URLs can exceed roughly 4 KB and get rejected. https://help.openalex.org/api/filtering/ and https://help.openalex.org/api/searching/
- Abstracts exist only as `abstract_inverted_index`, null on roughly 40 to 55 percent of works, may carry trailing junk; reconstruction is a position-based join.
- `referenced_works` is lossy relative to printed reference lists (DOI-match bias); the graph is documented as biased, not authoritative. https://help.openalex.org/data/works/citations/
- License: OpenAlex metadata CC0; reconstructed abstracts are for local corpus use. https://raw.githubusercontent.com/ourresearch/openalex-docs/main/license.md

## File structure

All paths in the new repo `C:\Users\gower\OneDrive\Documents\GitHub\jgs-lit-memory` unless noted.

```
jgs-lit-memory/
  README.md                      prose: what it is, install, usage, limits (Task 8)
  lit_fetch.py                   single file, stdlib only (Tasks 0-7)
  test_lit_fetch.py              offline assert-based checks, no framework (Tasks 0-7)
  skills/lit-capture/SKILL.md    canonical skill copy (Task 8)
```

Installed copies (Task 9) of `SKILL.md` and `lit_fetch.py` go to `C:\Users\gower\.zcode\skills\lit-capture\`, `C:\Users\gower\.claude\skills\lit-capture\`, and `C:\Users\gower\.agents\skills\lit-capture\`.

`lit_fetch.py` internal layout, built in order:

1. Module docstring and imports (Task 1)
2. Pure corpus logic: identity, normalization, verification (Task 1); queue, graph, index template (Task 2)
3. OpenAlex network layer (Task 3)
4. Corpus write model (Task 4)
5. Verbs and CLI (Task 5 singleton verbs and main; Task 6 batch and inbox; Task 7 status and check)

`main()` in Task 5 routes all eight verbs. The batch, inbox, status, and check branches call functions defined in Tasks 6 and 7; Python resolves those names at call time, so the module imports cleanly between tasks and unimplemented verbs are only reachable by flags their tests do not pass until their task lands.

## Commit discipline

- One commit per task, conventional style: `feat(lit): ...`, `fix(lit): ...`, `test(lit): ...`, `docs(lit): ...`, `chore(lit): ...`.
- Commit from the repo root. `git status --short` must be empty after each commit.
- Never commit corpus data, temp files, or `*.tmp` artifacts. The tool repo never contains a `.lit/` directory.

---

### Task 0: Environment verify, repo init, offline test runner

**Files:**
- Create: `lit_fetch.py` (docstring stub)
- Create: `test_lit_fetch.py` (runner skeleton)

**Interfaces:**
- Consumes: nothing.
- Produces: `test_lit_fetch.py` with a `CHECKS` list and a `main()` that runs every check, prints `PASS <name>` or `FAIL <name>: <reason>` per check, exits 0 with `all checks passed` or exits 1. Later tasks append test functions and extend `CHECKS`.

**Model:** flash

- [ ] **Step 1: Verify the toolchain**

```bash
python -c "import sys; assert sys.version_info >= (3, 9), sys.version; print(sys.version.split()[0])"
git --version
```

Expected: a version string 3.9 or higher, and a git version line. Stop and report if either fails.

- [ ] **Step 2: Create the repo**

```bash
mkdir -p "/c/Users/gower/OneDrive/Documents/GitHub/jgs-lit-memory/skills/lit-capture"
cd "/c/Users/gower/OneDrive/Documents/GitHub/jgs-lit-memory"
git init -b main
git symbolic-ref --short HEAD
```

Expected: `main`.

- [ ] **Step 3: Write the module stub**

`lit_fetch.py`:

```python
"""lit_fetch.py: capture OpenAlex works into a .lit corpus.

Single file, Python 3.9+ standard library only. Part of jgs-lit-memory.
See README.md and skills/lit-capture/SKILL.md.
"""
```

- [ ] **Step 4: Write the test runner skeleton**

`test_lit_fetch.py`:

```python
"""Offline checks for lit_fetch.py. Plain asserts, no test framework.

Run: python test_lit_fetch.py   (exit 0 when all checks pass)
Network calls never leave the test process: every test that reaches the
network installs a fake via lit_fetch.http_get (see Task 3).
"""

import sys

import lit_fetch

CHECKS = []


def main():
    failed = 0
    for check in CHECKS:
        try:
            check()
            print("PASS " + check.__name__)
        except Exception as exc:
            failed += 1
            print("FAIL " + check.__name__ + ": "
                  + exc.__class__.__name__ + ": " + str(exc))
    if failed:
        print(str(failed) + " check(s) failed")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run the runner**

Run: `python test_lit_fetch.py`
Expected output: `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "chore(lit): init repo and offline test runner"
```

---

### Task 1: Pure identity core: fold, bare IDs, abstract reconstruction, normalization, title verification

**Files:**
- Modify: `lit_fetch.py` (imports and pure-logic section)
- Modify: `test_lit_fetch.py` (fixtures and five checks)

**Interfaces:**
- Consumes: nothing.
- Produces (all later tasks rely on these exact names):
  - `fold(title: str) -> str` (lowercase, punctuation to spaces, whitespace collapsed; `None`/empty maps to `""`)
  - `bare_wid(value: str) -> str` (strips `https://openalex.org/`, strips whitespace)
  - `bare_doi(value) -> str | None` (lowercase, strips `https://doi.org/`; `None`/empty maps to `None`)
  - `reconstruct_abstract(inv_idx: dict | None) -> str | None` (position-based join; falsy input returns `None`; trailing junk kept verbatim)
  - `normalize_work(payload: dict, seed: bool, source: str, captured_at: str | None = None) -> dict` (full record schema; `captured_at` defaults to now UTC)
  - `verify_title(query_title: str, candidates: list, author_surname=None, year=None) -> dict | None` (single verified candidate or `None`; zero or multiple matches after supplied checks return `None`)

**Model:** flash

- [ ] **Step 1: Add the imports and pure-logic section to lit_fetch.py**

Append below the module docstring:

```python
import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from pathlib import Path

OA_PREFIX = "https://openalex.org/"
DOI_PREFIX = "https://doi.org/"


# ---------------------------------------------------------------------------
# pure corpus logic: identity and normalization (no network)
# ---------------------------------------------------------------------------

def bare_wid(value):
    """Strip the https://openalex.org/ prefix; return e.g. W2741809809."""
    return str(value).strip().removeprefix(OA_PREFIX)


def bare_doi(value):
    """Lowercase and strip any https://doi.org/ prefix; None stays None."""
    if not value:
        return None
    d = str(value).strip().lower()
    if d.startswith(DOI_PREFIX):
        d = d[len(DOI_PREFIX):]
    return d or None


def fold(title):
    """Lowercase, turn punctuation into spaces, collapse whitespace."""
    if not title:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-z\s]", " ", str(title).lower())).strip()


def reconstruct_abstract(inv_idx):
    """Rebuild abstract text from an abstract_inverted_index.

    None or empty stays None. Trailing junk in the index is kept verbatim;
    v1 never strips it (spec: joined text kept verbatim).
    """
    if not inv_idx:
        return None
    positions = {}
    for word, idxs in inv_idx.items():
        for i in idxs:
            positions[i] = word
    return " ".join(positions[i] for i in sorted(positions))


def normalize_work(payload, seed, source, captured_at=None):
    """Map a raw OpenAlex work object to the corpus record schema.

    The record id is the bare canonical W-id and always matches the file name
    the caller writes. captured_at defaults to now, ISO 8601 UTC.
    """
    if captured_at is None:
        captured_at = now_iso()
    return {
        "id": bare_wid(payload["id"]),
        "doi": bare_doi(payload.get("doi")),
        "display_name": payload.get("display_name"),
        "publication_date": payload.get("publication_date"),
        "publication_year": payload.get("publication_year"),
        "cited_by_count": payload.get("cited_by_count"),
        "authors": [a["author"]["display_name"]
                    for a in payload.get("authorships") or []
                    if a.get("author", {}).get("display_name")],
        "topics": [t["display_name"] for t in payload.get("topics") or []
                   if t.get("display_name")],
        "oa_url": (payload.get("open_access") or {}).get("oa_url"),
        "venue": ((payload.get("primary_location") or {}).get("source") or {})
                 .get("display_name"),
        "referenced_works": [bare_wid(w)
                             for w in payload.get("referenced_works") or []],
        "seed": seed,
        "captured_at": captured_at,
        "source": source,
        "abstract": reconstruct_abstract(payload.get("abstract_inverted_index")),
    }


def verify_title(query_title, candidates, author_surname=None, year=None):
    """Return the single verified candidate, else None.

    A candidate survives when fold(title) matches the query exactly and, when
    supplied, its authorships contain the surname (case-folded) and
    publication_year matches. Zero survivors, or two or more after the
    supplied checks, return None: near-misses and ambiguity never auto-write.
    """
    matches = [c for c in candidates
               if fold(c.get("display_name")) == fold(query_title)]
    if author_surname is not None:
        s = author_surname.lower()
        matches = [c for c in matches
                   if any(s in (a.get("author", {}).get("display_name") or "").lower()
                          for a in c.get("authorships") or [])]
    if year is not None:
        matches = [c for c in matches
                   if str(c.get("publication_year")) == str(year)]
    if len(matches) == 1:
        return matches[0]
    return None


def now_iso():
    """Current time, ISO 8601 UTC with Z suffix."""
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
```

Note: `now_iso` is defined here because `normalize_work` defaults `captured_at` to it. Python resolves the name at call time, so definition order inside the file is safe.

- [ ] **Step 2: Add fixtures and the failing checks to test_lit_fetch.py**

Add imports at the top (the file currently imports only `sys` and `lit_fetch`):

```python
import json
```

Append the frozen fixtures and checks above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# frozen fixtures
# ---------------------------------------------------------------------------

SAMPLE_PAYLOAD = {
    "id": "https://openalex.org/W1111111111",
    "doi": "https://doi.org/10.1234/Sample.2021",
    "display_name": "A Sample Study of Graphs and Edges",
    "publication_date": "2021-06-01",
    "publication_year": 2021,
    "cited_by_count": 12,
    "authorships": [
        {"author": {"display_name": "Jane Doe"}},
        {"author": {"display_name": "Ravi Patel"}},
    ],
    "topics": [{"display_name": "Graph theory"}, {"display_name": "Data systems"}],
    "open_access": {"oa_url": "https://example.org/pdf"},
    "primary_location": {"source": {"display_name": "Journal of Samples"}},
    "referenced_works": [
        "https://openalex.org/W2222222222",
        "https://openalex.org/W3333333333",
    ],
    "abstract_inverted_index": {"Sample": [0], "study": [1], "of": [2],
                                "graphs": [3], "and": [4], "edges": [5],
                                "Copyright": [6], "2021": [7]},
}

CANDIDATES = [
    {"id": "https://openalex.org/W1111111111",
     "display_name": "A Sample Study of Graphs and Edges",
     "publication_year": 2021,
     "authorships": [{"author": {"display_name": "Jane Doe"}}]},
    {"id": "https://openalex.org/W4444444444",
     "display_name": "a sample study of graphs and edges",
     "publication_year": 2019,
     "authorships": [{"author": {"display_name": "Bob Roe"}}]},
    {"id": "https://openalex.org/W5555555555",
     "display_name": "A Sample Study of Graphs and Nodes",
     "publication_year": 2021,
     "authorships": [{"author": {"display_name": "Jane Doe"}}]},
]


def make_payload(wid, refs=()):
    """A minimal valid OpenAlex work payload for a synthetic W-id."""
    return {
        "id": "https://openalex.org/" + wid,
        "doi": None,
        "display_name": "Paper " + wid,
        "publication_date": None,
        "publication_year": 2020,
        "cited_by_count": 0,
        "authorships": [],
        "topics": [],
        "open_access": {},
        "primary_location": None,
        "referenced_works": ["https://openalex.org/" + r for r in refs],
        "abstract_inverted_index": None,
    }


# ---------------------------------------------------------------------------
# checks: pure identity core
# ---------------------------------------------------------------------------

def test_fold():
    assert lit_fetch.fold("Hello,  World!") == "hello world"
    assert lit_fetch.fold("  State-of-the-Art Methods ") == "state of the art methods"
    assert lit_fetch.fold(None) == ""
    assert lit_fetch.fold("") == ""


def test_bare_ids():
    assert lit_fetch.bare_wid("https://openalex.org/W2741809807") == "W2741809807"
    assert lit_fetch.bare_wid(" W1111111111 ") == "W1111111111"
    assert lit_fetch.bare_doi("https://doi.org/10.1038/Nature12373") == "10.1038/nature12373"
    assert lit_fetch.bare_doi("10.1234/X") == "10.1234/x"
    assert lit_fetch.bare_doi(None) is None
    assert lit_fetch.bare_doi("") is None


def test_reconstruct_abstract():
    assert lit_fetch.reconstruct_abstract(
        {"A": [0], "b": [1], "graph": [2, 4], "of": [3]}) == "A b graph of graph"
    assert lit_fetch.reconstruct_abstract(None) is None
    assert lit_fetch.reconstruct_abstract({}) is None
    junk = {"Real": [0], "title": [1], "Copyright": [2],
            "(c)": [3], "2020": [4], "ACM": [5]}
    assert lit_fetch.reconstruct_abstract(junk) == "Real title Copyright (c) 2020 ACM"


def test_normalize_work():
    rec = lit_fetch.normalize_work(SAMPLE_PAYLOAD, seed=True, source="capture",
                                   captured_at="2026-09-16T00:00:00Z")
    assert rec["id"] == "W1111111111"
    assert rec["doi"] == "10.1234/sample.2021"
    assert rec["display_name"] == "A Sample Study of Graphs and Edges"
    assert rec["publication_date"] == "2021-06-01"
    assert rec["publication_year"] == 2021
    assert rec["cited_by_count"] == 12
    assert rec["authors"] == ["Jane Doe", "Ravi Patel"]
    assert rec["topics"] == ["Graph theory", "Data systems"]
    assert rec["oa_url"] == "https://example.org/pdf"
    assert rec["venue"] == "Journal of Samples"
    assert rec["referenced_works"] == ["W2222222222", "W3333333333"]
    assert rec["seed"] is True
    assert rec["source"] == "capture"
    assert rec["captured_at"] == "2026-09-16T00:00:00Z"
    assert rec["abstract"] == "Sample study of graphs and edges Copyright 2021"
    bare = dict(SAMPLE_PAYLOAD, abstract_inverted_index=None,
                primary_location=None, doi=None)
    rec2 = lit_fetch.normalize_work(bare, seed=False, source="fetch",
                                    captured_at="2026-09-16T00:00:00Z")
    assert rec2["abstract"] is None
    assert rec2["venue"] is None
    assert rec2["doi"] is None
    assert rec2["seed"] is False and rec2["source"] == "fetch"


def test_verify_title():
    q = "A Sample Study of Graphs and Edges"
    # two fold-matches, no disambiguator: ambiguous, none verifies
    assert lit_fetch.verify_title(q, CANDIDATES, None, None) is None
    # surname disambiguates to exactly one
    hit = lit_fetch.verify_title(q, CANDIDATES, "Doe", None)
    assert hit is not None and lit_fetch.bare_wid(hit["id"]) == "W1111111111"
    # year disambiguates to exactly one
    hit = lit_fetch.verify_title(q, CANDIDATES, None, "2021")
    assert hit is not None and lit_fetch.bare_wid(hit["id"]) == "W1111111111"
    # near miss never matches
    assert lit_fetch.verify_title("Study of Graphs and Nodes", CANDIDATES, None, None) is None
    # wrong surname rejects
    assert lit_fetch.verify_title(q, CANDIDATES, "Smith", None) is None
    # wrong year rejects
    assert lit_fetch.verify_title(q, CANDIDATES, None, "1999") is None
```

- [ ] **Step 3: Extend CHECKS**

Replace the `CHECKS = []` line with:

```python
CHECKS = [
    test_fold,
    test_bare_ids,
    test_reconstruct_abstract,
    test_normalize_work,
    test_verify_title,
]
```

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the five new checks PASS (the implementation landed in Step 1, so this task has no red run; a FAIL here means transcription drifted — stop and fix before committing).

- [ ] **Step 5: Run to verify all pass**

After Step 1's implementation is in place, run again:
Run: `python test_lit_fetch.py`
Expected: five `PASS` lines, then `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): pure identity and normalization core"
```

---

### Task 2: Pure queue, graph, and index-template logic

**Files:**
- Modify: `lit_fetch.py` (append to the pure-logic section)
- Modify: `test_lit_fetch.py` (six checks)

**Interfaces:**
- Consumes: `bare_wid`, `bare_doi`, `fold` (Task 1).
- Produces:
  - `PAGE_SIZE = 100`
  - `chunk_ids(ids: list, size: int = PAGE_SIZE) -> list` (list of lists; dedupe preserving first-seen order, chunks of at most `size`)
  - `parse_ref(ref) -> tuple | None` (`("doi"|"wid"|"arxiv"|"title", value)` or `None` when malformed)
  - `entry_key(entry: dict) -> str` (reads `entry["_ref"]` set by `read_inbox` in Task 6; keys look like `doi:...`, `wid:W...`, `title:<folded>`)
  - `corpus_keys(papers_dir: Path) -> set` of strings (union of `wid:`, `doi:`, `title:` keys over existing records)
  - `dedupe_inbox(entries: list, known_keys: set) -> tuple` of `(kept, duplicates)`; an entry duplicates when its key is in `known_keys` or seen earlier in the same file
  - `union_edges(existing: list, new: list) -> list` (dedupe on `(source, target)`, existing order first)
  - `resolve_alias(wid: str, aliases: dict) -> str` (follows alias chains to the final canonical id, cycle-safe)
  - `remap_edges(edges: list, aliases: dict) -> list`
  - `INDEX_TEMPLATE: str` (em-dash-free, no `__` placeholders left after render)
  - `render_index(papers: int, edges: int, boundary: int, inbox_pending: int, generated_at: str) -> str`

**Model:** flash

- [ ] **Step 1: Append the queue/graph/index section to lit_fetch.py**

Append below the Task 1 section (before the network section that comes later):

```python
# ---------------------------------------------------------------------------
# pure corpus logic: inbox queue, citation graph, generated index
# ---------------------------------------------------------------------------

PAGE_SIZE = 100

REF_RE = re.compile(r"^(doi|arxiv|title):(.+)$", re.S)
WID_RE = re.compile(r"^W\d+$")


def chunk_ids(ids, size=PAGE_SIZE):
    """Dedupe preserving first-seen order, then split into chunks of at most
    `size`. Chunks are computed after skip/dedupe (spec)."""
    seen = set()
    unique = []
    for raw in ids:
        w = bare_wid(raw)
        if w and w not in seen:
            seen.add(w)
            unique.append(w)
    return [unique[i:i + size] for i in range(0, len(unique), size)]


def parse_ref(ref):
    """Parse one inbox ref. Returns (kind, value) or None when malformed.

    kind is "doi", "wid", "arxiv", or "title". "W<digits>" is a wid; anything
    else must carry one of the three kind prefixes.
    """
    if not ref:
        return None
    r = str(ref).strip()
    if WID_RE.match(r):
        return ("wid", r)
    m = REF_RE.match(r)
    if m:
        return (m.group(1), m.group(2).strip())
    return None


def entry_key(entry):
    """Normalize one inbox entry to its dedupe key form (spec: doi refs to
    normalized DOI, W-ids to W-id, title-form and arxiv-form to folded title)."""
    kind, value = entry["_ref"]
    if kind == "doi":
        return "doi:" + (bare_doi(value) or value)
    if kind == "wid":
        return "wid:" + value
    if kind == "arxiv" and not entry.get("title"):
        return "arxiv:" + value
    return "title:" + fold(entry.get("title") or "")


def corpus_keys(papers_dir):
    """Known-ID set for inbox dedupe: canonical W-ids, bare normalized DOIs,
    and folded display_names of existing records."""
    keys = set()
    for path in sorted(Path(papers_dir).glob("*.json")):
        rec = json.loads(path.read_text(encoding="utf-8"))
        keys.add("wid:" + rec["id"])
        if rec.get("doi"):
            keys.add("doi:" + rec["doi"])
        if rec.get("display_name"):
            keys.add("title:" + fold(rec["display_name"]))
    return keys


def dedupe_inbox(entries, known_keys):
    """Return (kept, duplicates). Duplicate = key in known_keys, or key equal
    to an earlier entry in the same file."""
    kept, duplicates, seen = [], [], set()
    for entry in entries:
        k = entry_key(entry)
        if k in known_keys or k in seen:
            duplicates.append(entry)
        else:
            seen.add(k)
            kept.append(entry)
    return kept, duplicates


def union_edges(existing, new):
    """Union edge lists, deduped on (source, target), input order preserved."""
    out, seen = [], set()
    for e in list(existing) + list(new):
        key = (e["source"], e["target"])
        if key not in seen:
            seen.add(key)
            out.append({"source": e["source"], "target": e["target"]})
    return out


def resolve_alias(wid, aliases):
    """Follow alias chains to the final canonical W-id. Cycle-safe."""
    seen = set()
    while wid in aliases and wid not in seen:
        seen.add(wid)
        wid = aliases[wid]
    return wid


def remap_edges(edges, aliases):
    """Repoint every edge endpoint through the full alias table."""
    return [{"source": resolve_alias(e["source"], aliases),
             "target": resolve_alias(e["target"], aliases)}
            for e in edges]


INDEX_TEMPLATE = r"""> Generated by lit_fetch.py. Do not edit; the next capture regenerates this file.

# Literature corpus (`.lit/`)

This is the project's captured literature corpus: papers pulled from research
conversations, normalized from OpenAlex metadata. Read this file first each
session; it carries the counts and the query recipes.

| metric | count |
|---|---|
| papers (full records) | __PAPERS__ |
| edges | __EDGES__ |
| boundary nodes (edge endpoints without records) | __BOUNDARY__ |
| inbox pending | __INBOX__ |

last-synced: __GENERATED__

Records live in `papers/<W-id>.json`. The citation graph lives in
`graph/edges.jsonl`, one `{"source": ..., "target": ...}` per line, where
`source` cites `target`. Boundary nodes appear only as edge endpoints; promote
one by fetching its W-id (pass it to `--ids`).

## Query recipes (Git Bash)

Grep for a title fragment across the corpus:

```bash
grep -ril "fragment" .lit/papers/
```

Extract boundary IDs (edge endpoints with no record yet):

```bash
python -c "import json,glob,pathlib;edges=[json.loads(l) for l in open('.lit/graph/edges.jsonl') if l.strip()];have={pathlib.Path(p).stem for p in glob.glob('.lit/papers/*.json')};print('\n'.join(sorted(({e['source'] for e in edges}|{e['target'] for e in edges})-have)))"
```

Count edges per paper:

```bash
python -c "import json,collections;c=collections.Counter();[c.update([json.loads(l)['source'] for l in open('.lit/graph/edges.jsonl') if l.strip()]) for _ in [0]];print(c.most_common())"
```

Find papers citing a given W-id (who cites W123):

```bash
python -c "import json;print('\n'.join(json.loads(l)['source'] for l in open('.lit/graph/edges.jsonl') if json.loads(l)['target']=='W123'))"
```

## Caveats

`referenced_works` is lossy relative to printed reference lists: OpenAlex
matches references by DOI, so the stored graph is biased toward DOI-matchable
citations. Treat the graph as biased, not authoritative.

License: OpenAlex metadata is CC0. Reconstructed abstracts are for local
corpus use; do not redistribute them.
"""


def render_index(papers, edges, boundary, inbox_pending, generated_at):
    """Fill the generated .lit/SKILL.md template. Placeholder replacement, not
    str.format, so the recipe snippets can contain braces freely."""
    text = INDEX_TEMPLATE
    for key, value in [("PAPERS", papers), ("EDGES", edges),
                       ("BOUNDARY", boundary), ("INBOX", inbox_pending),
                       ("GENERATED", generated_at)]:
        text = text.replace("__" + key + "__", str(value))
    return text
```

- [ ] **Step 2: Add the failing checks to test_lit_fetch.py**

Append above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# checks: queue, graph, index template
# ---------------------------------------------------------------------------

def test_chunk_ids():
    ids = ["W3", "W1", "W2", "W1"] + ["W%d" % i for i in range(4, 250)]
    chunks = lit_fetch.chunk_ids(ids)
    assert all(len(c) <= 100 for c in chunks)
    assert [len(c) for c in chunks] == [100, 100, 49]
    flat = [w for c in chunks for w in c]
    assert len(flat) == len(set(flat))
    assert flat[:3] == ["W3", "W1", "W2"]
    assert lit_fetch.chunk_ids([]) == []


def test_parse_ref():
    assert lit_fetch.parse_ref("doi:10.1038/nature12373") == ("doi", "10.1038/nature12373")
    assert lit_fetch.parse_ref("W2741809807") == ("wid", "W2741809807")
    assert lit_fetch.parse_ref("arxiv:2401.12345") == ("arxiv", "2401.12345")
    assert lit_fetch.parse_ref("title:Some Title Here") == ("title", "Some Title Here")
    assert lit_fetch.parse_ref("nonsense") is None
    assert lit_fetch.parse_ref("") is None
    assert lit_fetch.parse_ref(None) is None


def test_entry_key_and_dedupe():
    known = {"wid:W1111111111", "doi:10.1234/sample.2021",
             "title:a sample study of graphs and edges"}
    entries = [
        {"ref": "W1111111111"},
        {"ref": "doi:HTTPS://DOI.ORG/10.1234/Sample.2021"},
        {"ref": "title:A Sample Study of Graphs and Edges",
         "title": "A Sample Study of Graphs and Edges"},
        {"ref": "doi:10.9999/new.thing"},
        {"ref": "doi:10.9999/new.thing"},
        {"ref": "title:  A  NEW Paper!", "title": "A  NEW Paper!"},
    ]
    for e in entries:
        e["_ref"] = lit_fetch.parse_ref(e["ref"])
    kept, dups = lit_fetch.dedupe_inbox(entries, known)
    assert len(dups) == 4
    assert [lit_fetch.entry_key(e) for e in kept] == [
        "doi:10.9999/new.thing", "title:a new paper"]


def test_union_edges():
    a = [{"source": "W1", "target": "W2"}, {"source": "W1", "target": "W3"}]
    b = [{"source": "W1", "target": "W2"}, {"source": "W2", "target": "W3"}]
    assert lit_fetch.union_edges(a, b) == [
        {"source": "W1", "target": "W2"},
        {"source": "W1", "target": "W3"},
        {"source": "W2", "target": "W3"},
    ]


def test_remap_edges():
    edges = [{"source": "W1", "target": "W2"}, {"source": "W9", "target": "W3"}]
    aliases = {"W2": "W5", "W5": "W7", "W9": "W1"}
    assert lit_fetch.remap_edges(edges, aliases) == [
        {"source": "W1", "target": "W7"},
        {"source": "W1", "target": "W3"},
    ]


def test_render_index():
    text = lit_fetch.render_index(3, 10, 5, 1, "2026-09-16T00:00:00Z")
    assert "| 3 |" in text and "| 10 |" in text and "| 5 |" in text and "| 1 |" in text
    assert "last-synced: 2026-09-16T00:00:00Z" in text
    assert "biased" in text and "CC0" in text
    assert "\u2014" not in lit_fetch.INDEX_TEMPLATE
    assert "\u2014" not in text
    assert "__" not in text
```

- [ ] **Step 3: Extend CHECKS**

```python
CHECKS = [
    test_fold,
    test_bare_ids,
    test_reconstruct_abstract,
    test_normalize_work,
    test_verify_title,
    test_chunk_ids,
    test_parse_ref,
    test_entry_key_and_dedupe,
    test_union_edges,
    test_remap_edges,
    test_render_index,
]
```

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the six new checks PASS after the five Task 1 checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted — stop and fix).

- [ ] **Step 5: Run to verify all pass**

Run: `python test_lit_fetch.py`
Expected: eleven `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): queue, graph, and index template pure logic"
```

---

### Task 3: OpenAlex network layer behind the http_get seam

**Files:**
- Modify: `lit_fetch.py` (network section)
- Modify: `test_lit_fetch.py` (fake helpers and six checks)

**Interfaces:**
- Consumes: nothing from the pure layer except `json`/`re` stdlib.
- Produces:
  - `BASE_URL = "https://api.openalex.org"`, `TIMEOUT = 30`, `MAX_ATTEMPTS = 5`, `BACKOFF_SCHEDULE = (1, 2, 4, 8, 16)`, `UA = "lit_fetch/1.0 (jgs-lit-memory)"`, `SELECT_FIELDS` (the verbatim select list)
  - `BudgetExhausted(Exception)`, `BackoffExhausted(Exception)`
  - `http_get(url: str, timeout: int = TIMEOUT) -> tuple` returning `(status: int, headers: dict, body_text: str)`; retries 429/5xx on the schedule with `Retry-After` override; raises `BudgetExhausted` when a success response carries `x-ratelimit-remaining: 0`; raises `BackoffExhausted` after `MAX_ATTEMPTS` failures. This function is the network seam: offline tests replace `lit_fetch.http_get`.
  - `with_params(path: str, params: dict, api_key) -> str` (appends `api_key` only when present; never `mailto`)
  - `work_url(identifier: str, api_key) -> str`, `ids_filter_url(wids: list, api_key) -> str`, `search_url(title: str, api_key) -> str`
  - `parse_envelope(body: str) -> list` (the `results` list)
  - `warn_keyless(call_type: str, api_key) -> None` (one stderr line naming the call type and the $0.10/day budget, only when key is falsy)

**Model:** flash

- [ ] **Step 1: Append the network section to lit_fetch.py**

```python
# ---------------------------------------------------------------------------
# OpenAlex network layer (the only code that touches the network)
# ---------------------------------------------------------------------------

BASE_URL = "https://api.openalex.org"
TIMEOUT = 30
MAX_ATTEMPTS = 5
BACKOFF_SCHEDULE = (1, 2, 4, 8, 16)
UA = "lit_fetch/1.0 (jgs-lit-memory)"
SELECT_FIELDS = ("id,doi,display_name,publication_date,publication_year,"
                 "authorships,referenced_works,cited_by_count,topics,"
                 "open_access,primary_location,abstract_inverted_index")


class BudgetExhausted(Exception):
    """X-RateLimit-Remaining read 0: abort the run, keep completed writes."""


class BackoffExhausted(Exception):
    """A call kept failing through the full backoff schedule."""


def _retry_delay(headers, attempt_index):
    """Retry-After (seconds) when the response carries one, else the schedule."""
    if headers is not None:
        try:
            ra = headers.get("Retry-After")
        except AttributeError:
            ra = None
        if ra:
            try:
                return float(ra)
            except ValueError:
                pass
    return BACKOFF_SCHEDULE[min(attempt_index, len(BACKOFF_SCHEDULE) - 1)]


def http_get(url, timeout=TIMEOUT):
    """GET a URL. Returns (status, headers, body_text).

    Retries 429 and 5xx on the backoff schedule; Retry-After overrides.
    A successful response with x-ratelimit-remaining == 0 raises
    BudgetExhausted. urllib follows 301 merge redirects itself; the record
    body returned is already the canonical work.
    """
    for attempt in range(MAX_ATTEMPTS):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                headers = {k.lower(): v for k, v in resp.headers.items()}
                if headers.get("x-ratelimit-remaining") == "0":
                    raise BudgetExhausted(url)
                return resp.status, headers, body
        except BudgetExhausted:
            raise
        except urllib.error.HTTPError as e:
            if not (e.code == 429 or 500 <= e.code < 600):
                raise
            headers = e.headers
        # failed attempt: sleep the schedule (Retry-After overrides), then retry
        time.sleep(_retry_delay(headers, attempt))
    raise BackoffExhausted(url)


def with_params(path, params, api_key):
    """Build an API URL. api_key appended when present; no mailto, ever."""
    if api_key:
        params = dict(params, api_key=api_key)
    return BASE_URL + path + "?" + urllib.parse.urlencode(params)


def work_url(identifier, api_key):
    """Singleton work URL: /works/doi:<doi> or /works/<W-id> (free)."""
    return with_params("/works/" + urllib.parse.quote(identifier, safe=":/"),
                       {"select": SELECT_FIELDS}, api_key)


def ids_filter_url(wids, api_key):
    """Batch list URL: pipe-OR filter, per-page=100 (budgeted)."""
    return with_params("/works",
                       {"filter": "ids.openalex:" + "|".join(wids),
                        "per-page": str(PAGE_SIZE),
                        "select": SELECT_FIELDS}, api_key)


def search_url(title, api_key):
    """Verified title search URL (budgeted)."""
    return with_params("/works", {"search": title, "per-page": "5",
                                  "select": SELECT_FIELDS}, api_key)


def parse_envelope(body):
    """results list from a list/filter/search envelope {"meta": ..., "results": [...]}."""
    return json.loads(body).get("results", [])


def warn_keyless(call_type, api_key):
    """One warning line before any budgeted call when no key is configured."""
    if not api_key:
        print("warning: {0} without OPENALEX_API_KEY; the keyless budget is "
              "$0.10/day and this call is budgeted".format(call_type),
              file=sys.stderr)
```

- [ ] **Step 2: Add fake helpers and the failing checks to test_lit_fetch.py**

Add to the imports at the top:

```python
import io
import urllib.parse
```

Directly below `import lit_fetch`, pin sleeps to no-ops for the whole test process (backoff tests never wait):

```python
lit_fetch.time.sleep = lambda seconds: None
```

Append above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# fakes: the network seam
# ---------------------------------------------------------------------------

def fake_http(handler):
    """Wrap a handler(url) -> (status, headers, body) as a fake lit_fetch.http_get."""
    calls = []

    def get(url, timeout=30):
        calls.append(url)
        return handler(url)

    get.calls = calls
    return get


def envelope(records):
    return json.dumps({"meta": {"count": len(records)}, "results": records})


def fake_urlopen(handler):
    """Patch urllib.request.urlopen UNDER the real lit_fetch.http_get, for
    tests that exercise retry/backoff/BudgetExhausted logic itself. handler(url)
    returns (status, headers, body_text) or raises. Returns the seen URLs."""
    calls = []

    class FakeResp:
        def __init__(self, status, headers, body):
            self.status = status
            self.headers = dict(headers)
            self._body = body

        def read(self):
            return self._body.encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    def urlopen(req, timeout=30):
        url = req.full_url
        calls.append(url)
        result = handler(url)
        if isinstance(result, Exception):
            raise result
        return FakeResp(*result)

    lit_fetch.urllib.request.urlopen = urlopen
    return calls


# ---------------------------------------------------------------------------
# checks: network layer (all offline through the fake)
# ---------------------------------------------------------------------------

def test_url_builders():
    u = lit_fetch.work_url("doi:10.1038/nature12373", "KEY")
    assert u.startswith("https://api.openalex.org/works/doi:10.1038/nature12373?")
    assert "select=" in u and "api_key=KEY" in u
    u2 = lit_fetch.work_url("W1111111111", None)
    q2 = urllib.parse.parse_qs(urllib.parse.urlparse(u2).query)
    assert q2["select"] == [lit_fetch.SELECT_FIELDS]
    assert "api_key" not in u2 and "mailto" not in u2
    u3 = lit_fetch.ids_filter_url(["W1", "W2"], None)
    q = urllib.parse.parse_qs(urllib.parse.urlparse(u3).query)
    assert q["filter"] == ["ids.openalex:W1|W2"]
    assert q["per-page"] == ["100"]
    u4 = lit_fetch.search_url("Graphs and Edges", None)
    q = urllib.parse.parse_qs(urllib.parse.urlparse(u4).query)
    assert q["search"] == ["Graphs and Edges"]
    assert q["per-page"] == ["5"]


def test_parse_envelope():
    assert lit_fetch.parse_envelope('{"meta": {"count": 2}, "results": [1, 2]}') == [1, 2]
    assert lit_fetch.parse_envelope('{"meta": {}}') == []


def test_retry_then_success():
    attempts = []

    def handler(url):
        attempts.append(url)
        if len(attempts) == 1:
            raise lit_fetch.urllib.error.HTTPError(
                url, 503, "oops", {}, io.BytesIO(b""))
        return (200, {"x-ratelimit-remaining": "9999"}, "{}")

    fake_urlopen(handler)
    status, headers, body = lit_fetch.http_get("https://api.openalex.org/works/W1")
    assert status == 200
    assert len(attempts) == 2


def test_retry_after_overrides_schedule():
    slept = []

    def handler(url):
        if len(handler.calls) == 0:
            handler.calls.append(url)
            raise lit_fetch.urllib.error.HTTPError(
                url, 429, "slow down", {"Retry-After": "7"}, io.BytesIO(b""))
        return (200, {"x-ratelimit-remaining": "99"}, "{}")

    handler.calls = []
    lit_fetch.time.sleep = slept.append
    fake_urlopen(handler)
    lit_fetch.http_get("https://api.openalex.org/works/W1")
    assert slept == [7.0]
    lit_fetch.time.sleep = lambda seconds: None


def test_budget_exhausted():
    def handler(url):
        return (200, {"x-ratelimit-remaining": "0"}, "{}")

    fake_urlopen(handler)
    try:
        lit_fetch.http_get("https://api.openalex.org/works/W1")
        raise AssertionError("expected BudgetExhausted")
    except lit_fetch.BudgetExhausted:
        pass


def test_http_404_propagates():
    calls = []

    def handler(url):
        calls.append(url)
        raise lit_fetch.urllib.error.HTTPError(url, 404, "nope", {}, io.BytesIO(b""))

    fake_urlopen(handler)
    try:
        lit_fetch.http_get("https://api.openalex.org/works/W1")
        raise AssertionError("expected HTTPError")
    except lit_fetch.urllib.error.HTTPError as e:
        assert e.code == 404
    assert len(calls) == 1
```

- [ ] **Step 3: Extend CHECKS**

```python
CHECKS = [
    test_fold,
    test_bare_ids,
    test_reconstruct_abstract,
    test_normalize_work,
    test_verify_title,
    test_chunk_ids,
    test_parse_ref,
    test_entry_key_and_dedupe,
    test_union_edges,
    test_remap_edges,
    test_render_index,
    test_url_builders,
    test_parse_envelope,
    test_retry_then_success,
    test_retry_after_overrides_schedule,
    test_budget_exhausted,
    test_http_404_propagates,
]
```

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the six new checks PASS after the eleven earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted — stop and fix).

- [ ] **Step 5: Run to verify all pass**

Run: `python test_lit_fetch.py`
Expected: seventeen `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): OpenAlex network layer with backoff and budget guard"
```

---

### Task 4: Atomic corpus write model

**Files:**
- Modify: `lit_fetch.py` (write-model section)
- Modify: `test_lit_fetch.py` (imports, four checks)

**Interfaces:**
- Consumes: `normalize_work`, `union_edges`, `remap_edges`, `resolve_alias`, `render_index`, `now_iso` (Tasks 1-2); `load_aliases` is defined in this task.
- Produces:
  - `atomic_write(path, text)` (temp file in the target directory plus `os.replace`; creates parent dirs)
  - `ensure_corpus(lit_dir)` (creates `papers/`, `graph/`, `findings/`)
  - `write_record(record, lit_dir)` (plain atomic record write, no skip logic)
  - `Run` class with `written`, `skipped`, `failed`, `failures`, `fail(identifier, reason)`, `summary() -> str` starting `written=N skipped=M failed=K` plus one `failed: <id> (<reason>)` line per failure
  - `write_one(payload, lit_dir, run, seed, source) -> tuple` of `(record, wrote_bool)`; skip-if-exists post-fetch (canonical record exists: no record write, existing `seed`/`captured_at` untouched, counted skipped)
  - `edges_of(records) -> list` (`{"source": record_id, "target": ref}` per reference)
  - `load_edges(lit_dir) -> list`, `write_edges(lit_dir, new_edges) -> int` (remaps existing endpoints through the full alias table, unions with `new_edges`, dedupes, rewrites atomically)
  - `load_aliases(lit_dir) -> dict`, `save_aliases(lit_dir, aliases)`
  - `boundary_nodes(lit_dir) -> set` (edge endpoints with no `papers/<id>.json`)
  - `count_inbox(lit_dir) -> int`
  - `regenerate_index(lit_dir)` (writes `.lit/SKILL.md` from counts plus a fresh `last-synced` timestamp)

**Model:** flash

- [ ] **Step 1: Append the write-model section to lit_fetch.py**

```python
# ---------------------------------------------------------------------------
# corpus write model (atomic everywhere)
# ---------------------------------------------------------------------------

def atomic_write(path, text):
    """Write text atomically: temp file in the same directory, then os.replace."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def ensure_corpus(lit_dir):
    """Create the corpus directory tree on first use in a fresh --dir."""
    for sub in ("papers", "graph", "findings"):
        (Path(lit_dir) / sub).mkdir(parents=True, exist_ok=True)


class Run:
    """Accumulates the end-of-run summary block."""

    def __init__(self):
        self.written = 0
        self.skipped = 0
        self.failed = 0
        self.failures = []

    def fail(self, identifier, reason):
        self.failed += 1
        self.failures.append((identifier, reason))

    def summary(self):
        lines = ["written={0} skipped={1} failed={2}".format(
            self.written, self.skipped, self.failed)]
        lines += ["failed: {0} ({1})".format(i, r) for i, r in self.failures]
        return "\n".join(lines)


def write_record(record, lit_dir):
    """Atomically write one normalized record. File name equals record id."""
    atomic_write(Path(lit_dir) / "papers" / (record["id"] + ".json"),
                 json.dumps(record, indent=2, ensure_ascii=False) + "\n")


def write_one(payload, lit_dir, run, seed, source):
    """Normalize and write one record with post-fetch skip-if-exists.

    The canonical id is only knowable after the fetch, so the skip happens
    here. An existing canonical record is never rewritten: its seed and
    captured_at stay untouched, and the run counts it as skipped.
    Returns (record, wrote)."""
    record = normalize_work(payload, seed=seed, source=source)
    path = Path(lit_dir) / "papers" / (record["id"] + ".json")
    if path.exists():
        run.skipped += 1
        return record, False
    write_record(record, lit_dir)
    run.written += 1
    return record, True


def edges_of(records):
    """Citation edges from normalized records: source cites target, bare W-ids."""
    return [{"source": r["id"], "target": t}
            for r in records for t in r["referenced_works"]]


def load_edges(lit_dir):
    p = Path(lit_dir) / "graph" / "edges.jsonl"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def load_aliases(lit_dir):
    p = Path(lit_dir) / "graph" / "aliases.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_aliases(lit_dir, aliases):
    atomic_write(Path(lit_dir) / "graph" / "aliases.json",
                 json.dumps(aliases, indent=2, sort_keys=True) + "\n")


def write_edges(lit_dir, new_edges):
    """Union new edges into edges.jsonl, healing as we go: existing endpoints
    are remapped through the full alias table before the union, so stale
    endpoints collapse onto canonical ones. Full idempotent rewrite, atomic."""
    existing = remap_edges(load_edges(lit_dir), load_aliases(lit_dir))
    combined = union_edges(existing, new_edges)
    atomic_write(Path(lit_dir) / "graph" / "edges.jsonl",
                 "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in combined))
    return len(combined)


def boundary_nodes(lit_dir):
    """Edge endpoints that have no papers/<id>.json. No placeholder records
    are ever created for them (spec)."""
    papers_dir = Path(lit_dir) / "papers"
    have = {p.stem for p in papers_dir.glob("*.json")} if papers_dir.is_dir() else set()
    endpoints = set()
    for e in load_edges(lit_dir):
        endpoints.add(bare_wid(e["source"]))
        endpoints.add(bare_wid(e["target"]))
    return endpoints - have


def count_inbox(lit_dir):
    p = Path(lit_dir) / "inbox.jsonl"
    if not p.exists():
        return 0
    return sum(1 for line in p.read_text(encoding="utf-8").splitlines() if line.strip())


def regenerate_index(lit_dir):
    """Regenerate .lit/SKILL.md after any successful write operation."""
    ensure_corpus(lit_dir)
    papers = len(list((Path(lit_dir) / "papers").glob("*.json")))
    text = render_index(papers, len(load_edges(lit_dir)),
                        len(boundary_nodes(lit_dir)), count_inbox(lit_dir),
                        now_iso())
    atomic_write(Path(lit_dir) / "SKILL.md", text)
```

- [ ] **Step 2: Add imports and the failing checks to test_lit_fetch.py**

Add to the imports at the top:

```python
import pathlib
import tempfile
```

Append above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# checks: write model (offline, temp dirs)
# ---------------------------------------------------------------------------

def test_atomic_write_and_corpus_init():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        lit_fetch.ensure_corpus(lit)
        assert (lit / "papers").is_dir()
        assert (lit / "graph").is_dir()
        assert (lit / "findings").is_dir()
        lit_fetch.atomic_write(lit / "graph" / "edges.jsonl", "x\n")
        assert (lit / "graph" / "edges.jsonl").read_text(encoding="utf-8") == "x\n"
        assert not list(lit.rglob("*.tmp"))


def test_edges_and_aliases_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        lit_fetch.ensure_corpus(lit)
        lit_fetch.write_edges(lit, [{"source": "W1", "target": "W2"}])
        lit_fetch.write_edges(lit, [{"source": "W1", "target": "W2"},
                                    {"source": "W2", "target": "W3"}])
        assert lit_fetch.load_edges(lit) == [
            {"source": "W1", "target": "W2"},
            {"source": "W2", "target": "W3"},
        ]
        # alias healing on write: stale endpoint remaps, union dedupes
        lit_fetch.save_aliases(lit, {"W3": "W5"})
        lit_fetch.write_edges(lit, [{"source": "W5", "target": "W1"}])
        assert lit_fetch.load_edges(lit) == [
            {"source": "W1", "target": "W2"},
            {"source": "W2", "target": "W5"},
            {"source": "W5", "target": "W1"},
        ]


def test_index_and_status_counts():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        rec = lit_fetch.normalize_work(SAMPLE_PAYLOAD, seed=True, source="capture",
                                       captured_at="2026-09-16T00:00:00Z")
        lit_fetch.write_record(rec, lit)
        lit_fetch.write_edges(lit, lit_fetch.edges_of([rec]))
        lit_fetch.regenerate_index(lit)
        index = (lit / "SKILL.md").read_text(encoding="utf-8")
        assert "| 1 |" in index
        assert "boundary" in index.lower()
        assert "last-synced: " in index
        assert lit_fetch.boundary_nodes(lit) == {"W2222222222", "W3333333333"}
        assert lit_fetch.count_inbox(lit) == 0
        (lit / "inbox.jsonl").write_text('{"ref": "W1"}\n{"ref": "W2"}\n',
                                         encoding="utf-8")
        assert lit_fetch.count_inbox(lit) == 2


def test_run_summary():
    run = lit_fetch.Run()
    run.fail("W1", "404")
    assert run.summary() == "written=0 skipped=0 failed=1\nfailed: W1 (404)"
```

- [ ] **Step 3: Extend CHECKS**

Add `test_atomic_write_and_corpus_init`, `test_edges_and_aliases_roundtrip`, `test_index_and_status_counts`, `test_run_summary` after `test_render_index` (keeping `test_url_builders` and the network checks after them). The list now has 21 entries in this order: the 11 pure checks, then these four, then the 6 network checks.

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the four new checks PASS after all earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted — stop and fix).

- [ ] **Step 5: Run to verify all pass**

Run: `python test_lit_fetch.py`
Expected: 21 `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): atomic corpus write model"
```

---

### Task 5: Singleton capture verbs and the CLI

**Files:**
- Modify: `lit_fetch.py` (verbs section and `main`)
- Modify: `test_lit_fetch.py` (imports, two checks)

**Interfaces:**
- Consumes: everything from Tasks 1-4.
- Produces:
  - `promote_payload(payload, lit_dir, run, seed=True, source="capture") -> dict` (write one already-fetched payload plus its edges; regenerates the index when the record was written or the edge set changed)
  - `capture_identifier(identifier, is_wid_form, lit_dir, api_key, run) -> dict` (singleton GET; records `requested -> canonical` in `aliases.json` and prints a one-line merge note when a W-id request resolved through a 301 to a different canonical id)
  - `verb_title(title, author, year, lit_dir, api_key, run) -> bool` (True when the paper is present afterwards: written or already in the corpus)
  - `build_parser() -> argparse.ArgumentParser`, `pick_verb(args) -> str`, `validate_verb(args, verb) -> None`
  - `main(argv=None) -> int` routing all eight verbs with the exit-code contract (0/1/2)

**Model:** standard

- [ ] **Step 1: Append the verbs section and CLI to lit_fetch.py**

```python
# ---------------------------------------------------------------------------
# verbs and CLI
# ---------------------------------------------------------------------------

def promote_payload(payload, lit_dir, run, seed=True, source="capture"):
    """Write one already-fetched payload: record (skip-if-exists) plus edges,
    then regenerate the index when anything changed (record written or edges
    added), so edge-only changes never leave the index stale."""
    ensure_corpus(lit_dir)
    edges_before = len(load_edges(lit_dir))
    record, wrote = write_one(payload, lit_dir, run, seed, source)
    edges_after = write_edges(lit_dir, edges_of([record]))
    if wrote or edges_after != edges_before:
        regenerate_index(lit_dir)
    return record


def capture_identifier(identifier, is_wid_form, lit_dir, api_key, run):
    """Singleton capture by DOI form or W-id. Records the 301 merge alias when
    a W-id request resolves to a different canonical id, and prints one merge
    note. DOI requests need no alias entry: they dedupe through the canonical
    id itself."""
    ensure_corpus(lit_dir)
    status, headers, body = http_get(work_url(identifier, api_key))
    payload = json.loads(body)
    canonical = bare_wid(payload["id"])
    requested = bare_wid(identifier) if is_wid_form else None
    aliases = load_aliases(lit_dir)
    if requested and requested != canonical and requested not in aliases:
        aliases[requested] = canonical
        save_aliases(lit_dir, aliases)
        print("merge: {0} -> {1}".format(requested, canonical))
    return promote_payload(payload, lit_dir, run, seed=True, source="capture")


def verb_title(title, author, year, lit_dir, api_key, run):
    """Verified title search. Returns True when the paper is present
    afterwards: written now, or already in the corpus via skip-if-exists.

    On no verified hit: writes nothing, counts one failure, and prints the top
    candidates for a human decision."""
    warn_keyless("title search", api_key)
    status, headers, body = http_get(search_url(title, api_key))
    candidates = parse_envelope(body)
    hit = verify_title(title, candidates, author, year)
    if hit is None:
        run.fail(title, "verification failed")
        print("no single verified match; top candidates:")
        for c in candidates[:5]:
            print("  {0}  {1}  {2}".format(bare_wid(c.get("id", "W?")),
                                           c.get("publication_year"),
                                           c.get("display_name")))
        return False
    promote_payload(hit, lit_dir, run, seed=True, source="capture")
    return True


VERB_FLAGS = ("doi", "openalex", "arxiv", "title", "ids", "inbox", "status", "check")


def build_parser():
    p = argparse.ArgumentParser(
        prog="lit_fetch.py",
        description="Capture OpenAlex works into a .lit corpus.")
    p.add_argument("--doi", help="capture by DOI (singleton, free)")
    p.add_argument("--openalex", help="capture by OpenAlex W-id (singleton, free)")
    p.add_argument("--arxiv", help="arXiv id; requires --title (no arXiv lookup exists)")
    p.add_argument("--title", help="verified title search; also the modifier of --arxiv")
    p.add_argument("--author", help="surname disambiguator for --title/--arxiv")
    p.add_argument("--year", help="year disambiguator for --title/--arxiv")
    p.add_argument("--ids", help='pipe-separated W-ids, e.g. "W123|W456"')
    p.add_argument("--inbox", action="store_true", help="triage .lit/inbox.jsonl")
    p.add_argument("--status", action="store_true", help="print corpus summary")
    p.add_argument("--check", action="store_true", help="live smoke test of endpoint forms")
    p.add_argument("--dir", default=".lit", help="corpus root (default .lit)")
    p.add_argument("--api-key", default=os.environ.get("OPENALEX_API_KEY"),
                   help="OpenAlex API key (default env OPENALEX_API_KEY)")
    p.add_argument("--seed", action="store_true",
                   help="mark --ids records seed=true (batch override only)")
    return p


def pick_verb(args):
    if args.arxiv and not args.title:
        print("error: --arxiv requires --title (OpenAlex has no arXiv ID "
              "lookup); supply the exact title, or capture the DOI with --doi",
              file=sys.stderr)
        sys.exit(2)
    names = [n for n in VERB_FLAGS if getattr(args, n)]
    if args.arxiv and "title" in names:
        names.remove("title")   # --title is the required modifier of --arxiv
    if len(names) != 1:
        print("error: give exactly one of --doi/--openalex/--arxiv/--title/"
              "--ids/--inbox/--status/--check", file=sys.stderr)
        sys.exit(2)
    return names[0]


def validate_verb(args, verb):
    if verb == "doi":
        d = bare_doi(args.doi)
        if not d or not d.startswith("10."):
            print("error: --doi expects a DOI like 10.1038/nature12373",
                  file=sys.stderr)
            sys.exit(2)
    if verb == "openalex":
        if not WID_RE.match(args.openalex.strip()):
            print("error: --openalex expects a W-id like W2741809807",
                  file=sys.stderr)
            sys.exit(2)


def main(argv=None):
    args = build_parser().parse_args(argv)
    verb = pick_verb(args)
    validate_verb(args, verb)
    lit_dir = Path(args.dir)
    api_key = args.api_key or None
    run = Run()
    try:
        if verb == "doi":
            try:
                capture_identifier("doi:" + bare_doi(args.doi), False,
                                   lit_dir, api_key, run)
            except BudgetExhausted:
                raise
            except Exception as exc:
                run.fail(args.doi, str(exc) or exc.__class__.__name__)
        elif verb == "openalex":
            try:
                capture_identifier(bare_wid(args.openalex), True,
                                   lit_dir, api_key, run)
            except BudgetExhausted:
                raise
            except Exception as exc:
                run.fail(args.openalex, str(exc) or exc.__class__.__name__)
        elif verb == "arxiv":
            print("note: resolving by verified title search (arXiv id "
                  + args.arxiv + " is not an OpenAlex lookup key)")
            verb_title(args.title, args.author, args.year, lit_dir, api_key, run)
        elif verb == "title":
            verb_title(args.title, args.author, args.year, lit_dir, api_key, run)
        elif verb == "ids":
            verb_ids(args.ids, lit_dir, api_key, args.seed, run)
        elif verb == "inbox":
            verb_inbox(lit_dir, api_key, run)
        elif verb == "status":
            return verb_status(lit_dir)
        elif verb == "check":
            return verb_check(api_key)
    except BudgetExhausted:
        print(run.summary())
        print("budget exhausted; completed writes stand")
        return 1
    except Exception as exc:
        print(run.summary())
        print("error: " + (str(exc) or exc.__class__.__name__))
        return 1
    print(run.summary())
    return 0 if run.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

The `ids`, `inbox`, `status`, and `check` branches call functions defined in Tasks 6 and 7. Python resolves them at call time; until those tasks land the module imports cleanly and those flags are simply not exercised.

- [ ] **Step 2: Add imports and the failing checks to test_lit_fetch.py**

Add to the imports at the top:

```python
import contextlib
```

Append above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# checks: singleton verbs (offline through the fake)
# ---------------------------------------------------------------------------

def test_singleton_capture_and_alias():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"

        def handler(url):
            assert "/works/W9999999999?" in url
            return (200, {"x-ratelimit-remaining": "9999"},
                    json.dumps(SAMPLE_PAYLOAD))   # canonical id W1111111111

        lit_fetch.http_get = fake_http(handler)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run = lit_fetch.Run()
            lit_fetch.capture_identifier("W9999999999", True, lit, None, run)
        assert run.written == 1 and run.skipped == 0 and run.failed == 0
        assert "merge: W9999999999 -> W1111111111" in out.getvalue()
        assert (lit / "papers" / "W1111111111.json").exists()
        assert lit_fetch.load_aliases(lit) == {"W9999999999": "W1111111111"}
        assert lit_fetch.load_edges(lit)[0]["source"] == "W1111111111"
        assert "last-synced: " in (lit / "SKILL.md").read_text(encoding="utf-8")
        # re-run: skip-if-exists, no rewrite, still counted
        run2 = lit_fetch.Run()
        with contextlib.redirect_stdout(io.StringIO()):
            lit_fetch.capture_identifier("W9999999999", True, lit, None, run2)
        assert run2.skipped == 1 and run2.written == 0 and run2.failed == 0


def test_title_verb_verification_gate():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"

        def handler(url):
            assert "search=" in url and "per-page=5" in url
            return (200, {"x-ratelimit-remaining": "9999"}, envelope(CANDIDATES))

        lit_fetch.http_get = fake_http(handler)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run = lit_fetch.Run()
            wrote = lit_fetch.verb_title("A Sample Study of Graphs and Edges",
                                         None, None, lit, None, run)
        assert wrote is False
        assert run.written == 0 and run.failed == 1
        assert "top candidates" in out.getvalue()
        assert not (lit / "papers" / "W1111111111.json").exists()
        # surname disambiguates: writes one record
        run2 = lit_fetch.Run()
        with contextlib.redirect_stdout(io.StringIO()):
            wrote = lit_fetch.verb_title("A Sample Study of Graphs and Edges",
                                         "Doe", None, lit, None, run2)
        assert wrote is True and run2.written == 1
        assert (lit / "papers" / "W1111111111.json").exists()
```

- [ ] **Step 3: Extend CHECKS**

Add `test_singleton_capture_and_alias` and `test_title_verb_verification_gate` after `test_run_summary`, before the network checks. Total 23 entries.

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the two new checks PASS after the earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted — stop and fix).

- [ ] **Step 5: Run to verify all pass**

Run: `python test_lit_fetch.py`
Expected: 23 `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 6: Smoke the CLI offline (usage errors, exit code 2)**

```bash
python lit_fetch.py --arxiv 2401.12345; echo "exit=$?"
python lit_fetch.py --doi not-a-doi --dir /tmp/lit-x; echo "exit=$?"
python lit_fetch.py --doi 10.1/x --status; echo "exit=$?"
```

Expected: first prints the `--arxiv requires --title` error, `exit=2`; second prints the DOI format error, `exit=2`; third prints the exactly-one error, `exit=2`.

- [ ] **Step 7: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): singleton capture verbs and CLI"
```

---

### Task 6: Batch and inbox triage verbs

**Files:**
- Modify: `lit_fetch.py` (append to the verbs section)
- Modify: `test_lit_fetch.py` (four checks)

**Interfaces:**
- Consumes: `chunk_ids`, `parse_ref`, `entry_key`, `corpus_keys`, `dedupe_inbox`, `resolve_alias` (Task 2); `warn_keyless`, `ids_filter_url`, `parse_envelope`, `BudgetExhausted` (Task 3); write model (Task 4); `capture_identifier`, `verb_title` (Task 5).
- Produces:
  - `parse_ids(raw: str) -> list` (split on `|`, `bare_wid` each, dedupe preserving order)
  - `verb_ids(raw, lit_dir, api_key, seed_flag, run) -> None` (skips existing corpus ids before chunking; warns keyless before the budgeted call; per chunk: write records `seed=seed_flag, source="fetch"`, report response-absent ids as 404 failures, learn 301 merges when a response returns a canonical record for a requested id (alias saved, one merge note), then one edge union per chunk; on `BudgetExhausted` regenerates the index if anything was written and re-raises; regenerates the index once at the end when anything was written; exits 2 via `sys.exit` when no usable ids)
  - `read_inbox(lit_dir) -> list` (JSONL entries with parsed `_ref` attached; `None` when unparseable)
  - `resolve_entry(entry, kind, value, lit_dir, api_key, run) -> bool` (doi/wid via `capture_identifier`; title/arxiv via `verb_title` using the entry's `title`, `author`, `year`; raises on hard errors)
  - `verb_inbox(lit_dir, api_key, run) -> None` (dedupe, resolve, then exactly one atomic inbox rewrite after all resolutions; failures stay queued with a `last_error` field; `BudgetExhausted` propagates without rewriting, so the original queue file stays intact; regenerates the index when anything was written)

**Model:** standard

- [ ] **Step 1: Append batch and inbox verbs to lit_fetch.py**

Insert above the `VERB_FLAGS` line (still inside the verbs section):

```python
def parse_ids(raw):
    """Split a pipe-separated id string, normalize, dedupe, preserve order."""
    out, seen = [], set()
    for part in str(raw).split("|"):
        w = bare_wid(part)
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out


def verb_ids(raw_ids, lit_dir, api_key, seed_flag, run):
    """Batch fetch by W-id. Skips ids already in the corpus before chunking,
    warns keyless before the budgeted call, writes seed=false source="fetch"
    records (seed_flag overrides), unions edges once per chunk, and reports
    ids absent from a response as 404 failures."""
    ensure_corpus(lit_dir)
    ids = parse_ids(raw_ids)
    if not ids:
        print("error: --ids needs at least one W-id", file=sys.stderr)
        sys.exit(2)
    papers_dir = Path(lit_dir) / "papers"
    todo = [w for w in ids if not (papers_dir / (w + ".json")).exists()]
    run.skipped += len(ids) - len(todo)
    if not todo:
        return
    warn_keyless("batch --ids", api_key)
    aliases = load_aliases(lit_dir)
    try:
        for chunk in chunk_ids(todo):
            status, headers, body = http_get(ids_filter_url(chunk, api_key))
            by_id = {bare_wid(r["id"]): r for r in parse_envelope(body)}
            records = []
            for wid in chunk:
                payload = by_id.get(wid) or by_id.get(resolve_alias(wid, aliases))
                if payload is None:
                    run.fail(wid, "404; requested id absent from response")
                    continue
                canonical = bare_wid(payload["id"])
                if canonical != wid and wid not in aliases:
                    aliases[wid] = canonical
                    save_aliases(lit_dir, aliases)
                    print("merge: {0} -> {1}".format(wid, canonical))
                record, wrote = write_one(payload, lit_dir, run,
                                          seed=seed_flag, source="fetch")
                records.append(record)
            write_edges(lit_dir, edges_of(records))
    except BudgetExhausted:
        if run.written:
            regenerate_index(lit_dir)
        raise
    if run.written:
        regenerate_index(lit_dir)


def read_inbox(lit_dir):
    """Read inbox entries as dicts, skipping blank lines. Attaches the parsed
    ref as the internal "_ref" key (None when unparseable)."""
    p = Path(lit_dir) / "inbox.jsonl"
    if not p.exists():
        return []
    entries = []
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        entry["_ref"] = parse_ref(entry.get("ref"))
        entries.append(entry)
    return entries


def resolve_entry(entry, kind, value, lit_dir, api_key, run):
    """Promote one inbox entry. Returns True on success, False on a
    verification failure (already reported by verb_title); raises on hard
    errors (404, network, budget)."""
    if kind == "doi":
        capture_identifier("doi:" + bare_doi(value), False, lit_dir, api_key, run)
        return True
    if kind == "wid":
        capture_identifier(value, True, lit_dir, api_key, run)
        return True
    title = entry.get("title") or (value if kind == "title" else None)
    if not title:
        raise ValueError("no title available to search")
    return verb_title(title, entry.get("author"), entry.get("year"),
                      lit_dir, api_key, run)


def verb_inbox(lit_dir, api_key, run):
    """Triage the inbox: dedupe, resolve every entry, then rewrite the inbox
    exactly once, atomically, keeping only entries that remain. Failures stay
    queued with their reason in "last_error". A BudgetExhausted abort
    re-raises before the rewrite, leaving the original queue file intact, and
    re-runs are idempotent through skip-if-exists."""
    entries = read_inbox(lit_dir)
    parseable = [e for e in entries if e["_ref"]]
    malformed = [e for e in entries if not e["_ref"]]
    for e in malformed:
        e.pop("_ref", None)
        run.fail(e.get("ref", "?"), "unparseable ref")
        e["last_error"] = "unparseable ref"
    papers_dir = Path(lit_dir) / "papers"
    known = corpus_keys(papers_dir) if papers_dir.is_dir() else set()
    kept, duplicates = dedupe_inbox(parseable, known)
    run.skipped += len(duplicates)
    if any(e["_ref"][0] in ("title", "arxiv") for e in kept):
        warn_keyless("inbox title/arxiv search", api_key)
    remaining = list(malformed)
    for entry in kept:
        kind, value = entry.pop("_ref")
        try:
            ok = resolve_entry(entry, kind, value, lit_dir, api_key, run)
            if not ok:
                entry["last_error"] = "verification failed"
                remaining.append(entry)
        except BudgetExhausted:
            raise
        except Exception as exc:
            reason = str(exc) or exc.__class__.__name__
            entry["last_error"] = reason
            run.fail(entry.get("ref", "?"), reason)
            remaining.append(entry)
    atomic_write(Path(lit_dir) / "inbox.jsonl",
                 "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in remaining))
    if run.written:
        regenerate_index(lit_dir)
```

- [ ] **Step 2: Add the failing checks to test_lit_fetch.py**

Append above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# checks: batch and inbox verbs (offline through the fake)
# ---------------------------------------------------------------------------

def test_batch_two_chunks_and_keyless_warning():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        ids = ["W%d" % (9000000000 + i) for i in range(1, 151)]
        calls = []

        def handler(url):
            calls.append(url)
            q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            wids = q["filter"][0].split(":")[1].split("|")
            return (200, {"x-ratelimit-remaining": "9999"},
                    envelope([make_payload(w) for w in wids]))

        lit_fetch.http_get = fake_http(handler)
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            run = lit_fetch.Run()
            lit_fetch.verb_ids("|".join(ids), lit, None, False, run)
        assert len(calls) == 2                       # 100 + 50
        assert run.written == 150 and run.skipped == 0 and run.failed == 0
        assert "keyless" in err.getvalue()           # warning before the budgeted call
        assert len(list((lit / "papers").glob("*.json"))) == 150
        assert "last-synced: " in (lit / "SKILL.md").read_text(encoding="utf-8")


def test_batch_skips_and_reports_absent():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        lit_fetch.ensure_corpus(lit)
        lit_fetch.write_record(
            lit_fetch.normalize_work(make_payload("W9000000001"), seed=True,
                                     source="capture",
                                     captured_at="2026-09-16T00:00:00Z"), lit)

        def handler(url):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            wids = q["filter"][0].split(":")[1].split("|")
            return (200, {"x-ratelimit-remaining": "9"},
                    envelope([make_payload(w) for w in wids if w != "W9000000002"]))

        lit_fetch.http_get = fake_http(handler)
        with contextlib.redirect_stdout(io.StringIO()):
            run = lit_fetch.Run()
            lit_fetch.verb_ids("W9000000001|W9000000002|W9000000003",
                               lit, None, False, run)
        assert run.skipped == 1            # W9000000001 already in corpus, never fetched
        assert run.written == 1            # W9000000003
        assert run.failed == 1             # W9000000002 absent from response
        assert "404" in run.failures[0][1]


def test_budget_abort_keeps_completed_writes():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        ids = ["W%d" % (9100000000 + i) for i in range(1, 151)]

        def handler(url):
            if "W9100000101" in url:       # second chunk
                return (200, {"x-ratelimit-remaining": "0"}, "{}")
            q = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            wids = q["filter"][0].split(":")[1].split("|")
            return (200, {"x-ratelimit-remaining": "500"},
                    envelope([make_payload(w) for w in wids]))

        fake_urlopen(handler)
        with contextlib.redirect_stdout(io.StringIO()):
            run = lit_fetch.Run()
            try:
                lit_fetch.verb_ids("|".join(ids), lit, None, False, run)
                raise AssertionError("expected BudgetExhausted")
            except lit_fetch.BudgetExhausted:
                pass
        assert run.written == 100
        assert len(list((lit / "papers").glob("*.json"))) == 100
        # every completed paper is valid JSON: atomic writes, no half files
        for p in (lit / "papers").glob("*.json"):
            json.loads(p.read_text(encoding="utf-8"))
        assert "last-synced: " in (lit / "SKILL.md").read_text(encoding="utf-8")


def test_inbox_triage_flow():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        lit_fetch.ensure_corpus(lit)
        lines = [
            {"ref": "W1111111111", "title": "", "note": "seed paper",
             "added_at": "2026-09-16T10:00:00Z"},
            {"ref": "doi:10.1234/Sample.2021", "note": "dup of seed by doi",
             "added_at": "2026-09-16T10:01:00Z"},
            {"ref": "not a ref", "note": "malformed",
             "added_at": "2026-09-16T10:02:00Z"},
            {"ref": "title:A Brand New Paper", "title": "A Brand New Paper",
             "author": "Newman", "year": "2024", "note": "to resolve",
             "added_at": "2026-09-16T10:03:00Z"},
        ]
        (lit / "inbox.jsonl").write_text(
            "".join(json.dumps(e) + "\n" for e in lines), encoding="utf-8")

        def handler(url):
            if "search=" in url:
                cand = make_payload("W4444444444")
                cand["display_name"] = "A Brand New Paper"
                cand["publication_year"] = 2024
                cand["authorships"] = [{"author": {"display_name": "Al Newman"}}]
                return (200, {"x-ratelimit-remaining": "9999"}, envelope([cand]))
            return (200, {"x-ratelimit-remaining": "9999"},
                    json.dumps(SAMPLE_PAYLOAD))

        lit_fetch.http_get = fake_http(handler)
        with contextlib.redirect_stdout(io.StringIO()):
            run = lit_fetch.Run()
            lit_fetch.verb_inbox(lit, None, run)
        assert run.written == 2         # wid singleton + verified title search
        assert run.skipped == 1         # doi entry resolves to the existing canonical
        assert run.failed == 1          # unparseable ref stays queued
        remaining = [json.loads(l)
                     for l in (lit / "inbox.jsonl").read_text(encoding="utf-8").splitlines()
                     if l.strip()]
        assert len(remaining) == 1 and remaining[0]["ref"] == "not a ref"
        assert "last_error" in remaining[0]
        assert (lit / "papers" / "W1111111111.json").exists()
        assert (lit / "papers" / "W4444444444.json").exists()
        # re-run: nothing left to promote, malformed entry still queued
        with contextlib.redirect_stdout(io.StringIO()):
            run2 = lit_fetch.Run()
            lit_fetch.verb_inbox(lit, None, run2)
        assert run2.written == 0 and run2.failed == 1
        # a later duplicate of a promoted paper dedupes against the corpus
        extra = {"ref": "title:A Sample Study of Graphs and Edges",
                 "title": "A Sample Study of Graphs and Edges",
                 "note": "dup by title", "added_at": "2026-09-16T11:00:00Z"}
        with (lit / "inbox.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(extra) + "\n")
        with contextlib.redirect_stdout(io.StringIO()):
            run3 = lit_fetch.Run()
            lit_fetch.verb_inbox(lit, None, run3)
        assert run3.skipped == 1 and run3.written == 0 and run3.failed == 1
        lines_left = [l for l in (lit / "inbox.jsonl").read_text(encoding="utf-8").splitlines()
                      if l.strip()]
        assert len(lines_left) == 1     # only the malformed entry remains
```

- [ ] **Step 3: Extend CHECKS**

Add `test_batch_two_chunks_and_keyless_warning`, `test_batch_skips_and_reports_absent`, `test_budget_abort_keeps_completed_writes`, `test_inbox_triage_flow` after the Task 5 checks. Total 27 entries.

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the four new checks PASS after the earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted — stop and fix).

- [ ] **Step 5: Run to verify all pass**

Run: `python test_lit_fetch.py`
Expected: 27 `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): batch and inbox triage verbs"
```

---

### Task 7: Status and check verbs

**Files:**
- Modify: `lit_fetch.py` (append to the verbs section)
- Modify: `test_lit_fetch.py` (two checks)

**Interfaces:**
- Consumes: write-model readers (Task 4), `work_url`/`ids_filter_url`/`search_url`/`http_get`/`parse_envelope` (Task 3), `bare_wid` (Task 1).
- Produces:
  - `verb_status(lit_dir) -> int` (prints `papers=N edges=M boundary=B inbox_pending=P` then `last-synced: <ts>`; prints `never` for last-synced when no generated index exists yet; read-only, no regeneration)
  - `CHECK_DOI = "10.1038/nature12373"`, `CHECK_ID = "W2741809807"` (both live-probed during research, 2026-09-16)
  - `verb_check(api_key) -> int` (probes DOI singleton, W-id singleton, two-ID batch filter, title search; prints `OK` or `FAIL <name>: <reason>` per form; exit 1 when any form fails; the batch probe reuses the canonical id returned by the DOI probe so no invented ids are needed)

**Model:** standard

- [ ] **Step 1: Append status and check verbs to lit_fetch.py**

Insert above `VERB_FLAGS`:

```python
def verb_status(lit_dir):
    """Corpus summary to stdout. Read-only; never regenerates the index.
    last-synced reads the generated index's timestamp line and prints
    "never" when no generated index exists yet."""
    papers_dir = Path(lit_dir) / "papers"
    papers = len(list(papers_dir.glob("*.json"))) if papers_dir.is_dir() else 0
    edges = len(load_edges(lit_dir))
    boundary = len(boundary_nodes(lit_dir))
    pending = count_inbox(lit_dir)
    last = "never"
    index_path = Path(lit_dir) / "SKILL.md"
    if index_path.exists():
        m = re.search(r"^last-synced: (.+)$",
                      index_path.read_text(encoding="utf-8"), re.M)
        if m:
            last = m.group(1).strip()
    print("papers={0} edges={1} boundary={2} inbox_pending={3}".format(
        papers, edges, boundary, pending))
    print("last-synced: {0}".format(last))
    return 0


CHECK_DOI = "10.1038/nature12373"   # live-probed 2026-09-16 (plan Research section)
CHECK_ID = "W2741809807"            # live-probed 2026-09-16 (plan Research section)


def verb_check(api_key):
    """Live smoke test of the four load-bearing endpoint forms. Exit 1 when
    any form fails. Run on first use and whenever OpenAlex behaves oddly."""
    ok = True
    doi_result = {}

    def probe(name, fn):
        nonlocal ok
        try:
            fn()
            print("OK   " + name)
        except Exception as exc:
            ok = False
            print("FAIL {0}: {1}".format(name, exc))

    def probe_doi():
        payload = json.loads(http_get(work_url("doi:" + CHECK_DOI, api_key))[2])
        doi_result["wid"] = bare_wid(payload["id"])

    def probe_wid():
        payload = json.loads(http_get(work_url(CHECK_ID, api_key))[2])
        assert bare_wid(payload["id"]) == CHECK_ID

    def probe_batch():
        url = ids_filter_url([CHECK_ID, doi_result.get("wid", CHECK_ID)], api_key)
        results = parse_envelope(http_get(url)[2])
        assert isinstance(results, list)

    def probe_search():
        results = parse_envelope(http_get(
            search_url("crystal structure prediction", api_key))[2])
        assert isinstance(results, list)

    probe("doi singleton   /works/doi:" + CHECK_DOI, probe_doi)
    probe("W-id singleton  /works/" + CHECK_ID, probe_wid)
    probe("two-ID batch filter", probe_batch)
    probe("title search", probe_search)
    return 0 if ok else 1
```

- [ ] **Step 2: Add the failing checks to test_lit_fetch.py**

Append above `CHECKS`:

```python
# ---------------------------------------------------------------------------
# checks: status and check verbs
# ---------------------------------------------------------------------------

def test_status_never_before_index():
    with tempfile.TemporaryDirectory() as tmp:
        lit = pathlib.Path(tmp) / ".lit"
        rec = lit_fetch.normalize_work(SAMPLE_PAYLOAD, seed=True, source="capture",
                                       captured_at="2026-09-16T00:00:00Z")
        lit_fetch.write_record(rec, lit)
        lit_fetch.write_edges(lit, lit_fetch.edges_of([rec]))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            assert lit_fetch.verb_status(lit) == 0
        text = out.getvalue()
        assert "papers=1 edges=2 boundary=2 inbox_pending=0" in text
        assert "last-synced: never" in text
        # after a regeneration the real timestamp shows up
        lit_fetch.regenerate_index(lit)
        out2 = io.StringIO()
        with contextlib.redirect_stdout(out2):
            lit_fetch.verb_status(lit)
        assert "last-synced: never" not in out2.getvalue()
        assert "last-synced: 20" in out2.getvalue()   # a real ISO timestamp


def test_check_forms_fake():
    def handler(url):
        if "search=" in url:
            return (200, {"x-ratelimit-remaining": "9"}, envelope([]))
        if "ids.openalex" in url:
            return (200, {"x-ratelimit-remaining": "9"},
                    envelope([make_payload("W2741809807")]))
        if "/works/W2741809807?" in url:
            return (200, {"x-ratelimit-remaining": "9"},
                    json.dumps(make_payload("W2741809807")))
        return (200, {"x-ratelimit-remaining": "9"}, json.dumps(SAMPLE_PAYLOAD))

    lit_fetch.http_get = fake_http(handler)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = lit_fetch.verb_check(None)
    assert rc == 0
    assert out.getvalue().count("OK") == 4
    assert "FAIL" not in out.getvalue()
```

- [ ] **Step 3: Extend CHECKS**

Add `test_status_never_before_index` and `test_check_forms_fake` at the end. Total 29 entries.

- [ ] **Step 4: Run the suite**

Run: `python test_lit_fetch.py`
Expected: the two new checks PASS after the earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted — stop and fix).

- [ ] **Step 5: Run to verify all pass**

Run: `python test_lit_fetch.py`
Expected: 29 `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 6: Commit**

```bash
git add lit_fetch.py test_lit_fetch.py
git commit -m "feat(lit): status and check verbs"
```

---

### Task 8: Capture skill (SKILL.md) and README

**Files:**
- Create: `skills/lit-capture/SKILL.md`
- Create: `README.md`

**Interfaces:**
- Consumes: the finished `lit_fetch.py` CLI (Tasks 5-7); the `jgs-paper-voice` frontmatter convention (`name`, one-paragraph `description` naming trigger conditions).
- Produces: the canonical skill copy and repo README. The skill invokes the script by the `.zcode` absolute path so all three mirrors stay interchangeable. All prose follows the Written Prose Standard: no em dashes, no slop vocabulary.

**Model:** standard

- [ ] **Step 1: Write skills/lit-capture/SKILL.md**

````markdown
---
name: lit-capture
description: Capture scholarly papers met in research conversations into this project's .lit corpus, triage the capture inbox, and answer literature questions from the local corpus before re-searching. Use when a paper with a DOI, arXiv id, OpenAlex W-id, or exact title plus author or year comes up and looks worth keeping, when the user asks to capture, save, or file a paper, or when a literature question may already be answered by the corpus. Not for casual mentions the user has not asked to keep.
---

# lit-capture

Run this as a procedure. The corpus lives in `.lit/` at the root of the current
project repo and is git-tracked there. The script `lit_fetch.py` is the only
component that touches the network, and it talks to OpenAlex only. Everything
else is agent reading and writing.

Invoke the script by its installed path so no PATH setup is needed:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --status
```

Common flags: `--dir <path>` (corpus root, default `.lit`; always run from the
repo root), `--api-key <key>` (default env `OPENALEX_API_KEY`).

## 1. When to trigger

A paper enters the conversation with enough identity to fetch (DOI, arXiv id,
W-id, or exact title plus author and/or year) and looks worth keeping. Capture
takes under a minute and never leaves the chat.

## 2. Extract, do not fetch blindly

Scan the conversation for DOIs (`10.xxxx/...`), arXiv ids, OpenAlex W-ids, and
full titles. This is agent-driven reading, not code-based NLP; the script never
parses prose. Dedupe against the corpus before capture: read the generated
`.lit/SKILL.md` for counts and last-synced, then grep `papers/` for the
identifiers you found.

## 3. Capture offline first

Append one JSONL line per item to `.lit/inbox.jsonl`. The `ref` grammar is
exactly one of:

```json
{"ref": "doi:10.1038/nature12373"}
{"ref": "W2741809807"}
{"ref": "arxiv:2401.12345", "title": "<verbatim title>"}
{"ref": "title:<verbatim title>"}
```

Title-form and arxiv-form entries also carry `"title"` (verbatim), plus
optional `"author"` (surname) and `"year"`. Every entry carries `"note"` (why
it came up) and `"added_at"` (ISO timestamp). This works with no network and
survives the session.

## 4. Fetch now when online

With user consent or standing habit, run the script per item, or as one batch:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --ids "W2741809807|W2100837265"
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --doi 10.1038/nature12373
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --title "Exact Title" --author Surname --year 2024
```

Report the `written=N skipped=M failed=K` summary block to the user. Then stage
the capture: `git add .lit`.

Title searches and batches are budgeted calls; without an API key the script
warns and draws on the small keyless daily budget. Singleton DOI and W-id
lookups are free.

## 5. Findings stub (optional)

For papers worth a note, write `findings/<year>-<slug>.md` from this template:

```markdown
# <paper title>

- W-id: <W-id>
- Captured: <YYYY-MM-DD>, why: <one line on why it came up>
- Claim worth remembering: <one sentence>
```

Prose in findings follows the Written Prose Standard: lead with the finding,
no em dashes, no filler.

## 6. Triage

Periodically run:

```bash
python "$HOME/.zcode/skills/lit-capture/lit_fetch.py" --inbox
```

Title-form and arxiv-form entries resolve through their `"title"` field
(arXiv entries get theirs from the paper as captured); supply `"author"` and
`"year"` to disambiguate. Drop entries no longer wanted by deleting their
lines. Failures stay queued with their reason in `last_error`; fix the entry
or delete it, then re-run.

## 7. Query the corpus

Read `.lit/SKILL.md` first each session (counts, recipes, last-synced), then
answer literature questions from `papers/` and `graph/edges.jsonl` before
re-searching. The index carries copy-pasteable recipes: title grep, boundary
ID extraction, edges per paper, papers citing a given W-id.

## 8. Limits

Abstracts are often null (OpenAlex stores them only as an inverted index and
only for roughly half of works). Use the corpus for identity, graph, and
retrieval, not as a full-text store. `referenced_works` is lossy relative to
printed reference lists; treat the graph as biased, not authoritative.
````

- [ ] **Step 2: Write README.md**

````markdown
# jgs-lit-memory

`lit_fetch.py` captures scholarly papers from OpenAlex into a per-project
`.lit/` corpus: one normalized JSON record per paper, citation edges between
them, optional findings notes, and a low-friction inbox for offline capture.
The companion `lit-capture` skill drives the capture procedure from research
conversations, so the next session queries the local corpus instead of
re-searching the same papers.

## Install

Copy, do not link, matching the existing skill mirror pattern. Run from the
repo root:

```bash
mkdir -p "$HOME/.zcode/skills/lit-capture" "$HOME/.claude/skills/lit-capture" "$HOME/.agents/skills/lit-capture"
cp skills/lit-capture/SKILL.md lit_fetch.py "$HOME/.zcode/skills/lit-capture/"
cp skills/lit-capture/SKILL.md lit_fetch.py "$HOME/.claude/skills/lit-capture/"
cp skills/lit-capture/SKILL.md lit_fetch.py "$HOME/.agents/skills/lit-capture/"
```

Edits happen in this repo, then get re-copied to the three mirrors. The skill
invokes the script by the `.zcode` absolute path, so all three mirrors stay
interchangeable and no PATH setup is needed.

## Usage

One resolution verb per invocation.

| Invocation | Behavior |
|---|---|
| `--doi <doi>` | Singleton capture by DOI (free). seed=true, source="capture". |
| `--openalex <W-id>` | Singleton capture by W-id (free). Same write semantics. |
| `--arxiv <id> --title <t>` | No arXiv lookup exists in OpenAlex; resolves through the verified title search. Bare `--arxiv` is a usage error. |
| `--title <t> [--author <surname>] [--year <yyyy>]` | Budgeted search with client-side verification. Near-misses print as candidates and write nothing. |
| `--ids "W1\|W2\|..."` | Batch fetch, 100 per call, skips existing records. seed=false, source="fetch"; `--seed` overrides. |
| `--inbox` | Triage `.lit/inbox.jsonl`: dedupe, resolve, rewrite the queue once. Failures stay queued with their reason. |
| `--status` | Corpus summary. Read-only. |
| `--check` | Live smoke test of the four endpoint forms. |

Common flags: `--dir <path>` (default `.lit`), `--api-key <key>` (default env
`OPENALEX_API_KEY`), `--seed`, `--author`, `--year`.

Exit codes: 0 success or already present, 1 any failure, 2 usage error.

## Corpus layout

`.lit/` lives in the project that produced it and is git-tracked there:

```
.lit/
  papers/<W-id>.json      one normalized record per paper
  graph/edges.jsonl       {"source": citing W-id, "target": cited W-id}, one per line
  graph/aliases.json      {"alias W-id": "canonical W-id"} recorded on 301 merges
  findings/<year>-<slug>.md  optional human notes
  inbox.jsonl             offline capture queue
  SKILL.md                generated corpus contract; never hand-edited
```

All writes are atomic (temp file plus `os.replace`). A crash mid-batch leaves
completed records on disk and never a half-written file. Edges are a
full-rewrite idempotent union, so the next successful run heals partial runs.

## Limits

- Abstracts come only from `abstract_inverted_index`, are null on roughly 40
  to 55 percent of works, and keep their trailing junk verbatim. The corpus is
  for identity, graph, and retrieval, not full text.
- `referenced_works` is lossy relative to printed reference lists; the graph
  is biased toward DOI-matchable citations.
- OpenAlex metadata is CC0. Reconstructed abstracts are for local corpus use.
- Without an API key, budgeted calls (batches, title searches, inbox triage
  with search entries) draw on a small keyless daily budget and the script
  warns first. Singleton DOI and W-id lookups are free.

## Testing

```bash
python test_lit_fetch.py        # offline checks; the network is faked
python lit_fetch.py --check     # live smoke test of endpoint forms
```

Set `OPENALEX_API_KEY` for the full daily budget. Get a key from OpenAlex.
````

- [ ] **Step 3: Run the prose gate**

Run: `python ~/.zcode/scripts/prose_check.py README.md skills/lit-capture/SKILL.md`
Expected: no findings, or only the documented backticked-flag false positives (`--doi`, `--ids`, and siblings inside code spans). Fix any finding that is not a command flag. Confirm by eye that neither file contains an em dash character.

- [ ] **Step 4: Commit**

```bash
git add README.md skills/lit-capture/SKILL.md
git commit -m "docs(lit): capture skill and README"
```

---

### Task 9: Mirror install and final acceptance sweep

**Files:**
- Create: installed copies of `SKILL.md` and `lit_fetch.py` in `C:\Users\gower\.zcode\skills\lit-capture\`, `C:\Users\gower\.claude\skills\lit-capture\`, `C:\Users\gower\.agents\skills\lit-capture\`
- Modify: nothing else

**Interfaces:**
- Consumes: every deliverable from Tasks 0-8.
- Produces: three identical skill mirrors and a recorded acceptance sweep.

**Model:** flash

- [ ] **Step 1: Full offline suite**

Run: `python test_lit_fetch.py`
Expected: 29 `PASS` lines, `all checks passed`, exit 0.

- [ ] **Step 2: Install the mirrors**

```bash
REPO="/c/Users/gower/OneDrive/Documents/GitHub/jgs-lit-memory"
for d in "$HOME/.zcode/skills/lit-capture" "$HOME/.claude/skills/lit-capture" "$HOME/.agents/skills/lit-capture"; do
  mkdir -p "$d"
  cp "$REPO/skills/lit-capture/SKILL.md" "$d/SKILL.md"
  cp "$REPO/lit_fetch.py" "$d/lit_fetch.py"
done
```

- [ ] **Step 3: Verify the mirrors are identical**

```bash
REPO="/c/Users/gower/OneDrive/Documents/GitHub/jgs-lit-memory"
for d in "$HOME/.zcode/skills/lit-capture" "$HOME/.claude/skills/lit-capture" "$HOME/.agents/skills/lit-capture"; do
  cmp "$REPO/skills/lit-capture/SKILL.md" "$d/SKILL.md" || exit 1
  cmp "$REPO/lit_fetch.py" "$d/lit_fetch.py" || exit 1
done
echo "mirrors identical"
```

Expected: `mirrors identical`.

- [ ] **Step 4: Run the spec's acceptance checks in order**

1. Offline suite (Step 1 above): pass. Covers the spec's `test_lit_fetch.py` acceptance check and the 150-ID acceptance check (two batch calls of 100 plus 50 plus the leading keyless warning) via `test_batch_two_chunks_and_keyless_warning`, and the interrupted-batch-valid-JSON check via `test_budget_abort_keeps_completed_writes`.

2. Live endpoint smoke (needs `OPENALEX_API_KEY`; keyless works degraded and consumes a sliver of the $0.10/day budget):

```bash
python lit_fetch.py --check; echo "exit=$?"
```
Expected: four `OK` lines (DOI singleton, W-id singleton, two-ID batch filter, title search), `exit=0`.

3. Live DOI capture into a throwaway dir, then status agreement:

```bash
tmp=$(mktemp -d)
python lit_fetch.py --doi 10.1038/nature12373 --dir "$tmp"; echo "exit=$?"
ls "$tmp/papers/"
python lit_fetch.py --status --dir "$tmp"
grep "last-synced:" "$tmp/SKILL.md"
```
Expected: summary `written=1 skipped=0 failed=0`, exit 0; exactly one `W<digits>.json` in `papers/` whose file name equals the `id` inside the record; `--status` prints `papers=1 edges=<len referenced_works> boundary=<same count, every reference target being a boundary node> inbox_pending=0` and a `last-synced:` line matching the index.

4. Prose gate on repo markdown:

```bash
python ~/.zcode/scripts/prose_check.py README.md skills/lit-capture/SKILL.md
```
Expected: no unjustified findings (backticked command flags are the documented exception, same as in the spec's mechanical gate note).

5. Em-dash scan over all repo prose including the generated index template:

```bash
grep -rn $'\u2014' README.md skills/ lit_fetch.py test_lit_fetch.py && echo "FOUND" || echo "clean"
```
Expected: `clean`. (The template assert in `test_render_index` covers this permanently.)

- [ ] **Step 5: Commit**

```bash
git add -A
git status --short
git commit -m "chore(lit): install skill mirrors and final acceptance sweep" --allow-empty
```

(`--allow-empty` only if the copies produced no repo-side diff; otherwise the sweep leaves nothing to commit and this becomes a no-op verification. Never commit anything under a `.lit/` directory into this repo.)

---

## Spec coverage map

| Spec section | Task(s) |
|---|---|
| Repo layout and install | 0, 8, 9 |
| Corpus layout (`.lit/` tree, findings dir, git-tracked default, `git add .lit`) | 4, 8 |
| Record schema (papers/<W-id>.json) | 1, 4 |
| Edge rules (direction, 301 aliases, boundary nodes, promotion) | 2, 4, 5, 6 |
| Verbs `--doi`, `--openalex`, `--arxiv`, `--title` | 5 |
| Verbs `--ids`, `--inbox` | 6 |
| Verbs `--status`, `--check` | 7 |
| Dedupe and canonicalization (skip-if-exists, batch skip, inbox dedupe) | 4, 5, 6 |
| Title verification (fold, near-miss, disambiguation) | 1, 5 |
| Network behavior (base URL, envelopes, select, api_key, keyless warnings, backoff, Retry-After, X-RateLimit-Remaining, timeouts) | 3 |
| Write model and failure handling (atomic writes, per-chunk edges, index regen, dir auto-create, summary, exit codes) | 4, 5, 6 |
| Generated `.lit/SKILL.md` (banner, scope, counts, recipes, caveat, license) | 2, 4 |
| Skill procedure (8 sections, ref grammar, findings stub) | 8 |
| Testing (offline checks, `--check`, manual acceptance) | 1-7, 9 |
| Advisory defaults (`--status` prints `never` without a generated index; inbox rewrite uses the same temp-plus-`os.replace` atomic write) | 7, 6 |

Self-review notes: every acceptance check in the spec maps to a task or an offline check named in Task 9; interface names were cross-checked across tasks (`write_edges` takes two arguments everywhere, `entry_key` reads `_ref` set by `read_inbox`, `corpus_keys` takes the `papers/` path); the only deliberate mid-build gap is the documented call-time resolution of verbs between Tasks 5 and 7.

## Verification

- Offline, no network: `python test_lit_fetch.py` must print `all checks passed` and exit 0. Call-site checks run against `lit_fetch.http_get` fakes; retry/backoff/budget checks run the real `http_get` over a faked `urllib.request.urlopen`; sleeps are patched to no-ops inside the test process.
- Live: `python lit_fetch.py --check` reports OK on all four endpoint forms. With `OPENALEX_API_KEY` set this is the full-fidelity run; keyless it runs degraded and silently consumes a sliver of the $0.10/day keyless budget (the spec's warning list covers batch, title search, and inbox calls, not `--check`).
- Manual acceptance, from the spec, executed in Task 9: live DOI capture into a throwaway `--dir` with `--status` agreement; the 150-ID two-call batch with leading keyless warning (offline check); the interrupted batch that leaves valid JSON on disk (offline check; a live Ctrl-C variant is optional); prose gate and em-dash scan; mirror identity via `cmp`.

Mechanical gate note: `prose_check.py` reports findings for CLI command flags (`--doi`, `--ids`, `--check` and siblings) inside backticks. As in the spec, these are excluded from the dash rule; the flags stay as written because renaming them would corrupt the CLI contract they define. No em dashes exist in this plan.
