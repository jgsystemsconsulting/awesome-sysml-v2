"""Apply ARL Round 1 fixes to the lit-capture plan. Each pair must match exactly once."""
import io, sys

PATH = r"C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\plans\2026-09-16-lit-capture.md"
text = io.open(PATH, encoding="utf-8").read()

PAIRS = []

PAIRS.append((
"- Every task ends with one conventional commit (`type(lit): ...`) made from the repo root; working tree clean before the next task starts.",
"- Every task ends with one conventional commit (`type(lit): ...`) made from the repo root; working tree clean before the next task starts.\n- Listing order inside tasks is implementation-first, tests-second by design: a task's suite run is already green once its listing is applied, so the run steps say so explicitly. There is no per-task red run; red/green discipline lives in the per-assert test structure and Task 9's final sweep."))

PAIRS.append((
"- [ ] **Step 4: Run to verify the checks fail**\n\nRun: `python test_lit_fetch.py`\nExpected: FAIL lines with `AttributeError: module 'lit_fetch' has no attribute 'fold'` (and siblings).",
"- [ ] **Step 4: Run the suite**\n\nRun: `python test_lit_fetch.py`\nExpected: the five new checks PASS (the implementation landed in Step 1, so this task has no red run; a FAIL here means transcription drifted \u2014 stop and fix before committing)."))

PAIRS.append((
"- [ ] **Step 4: Run to verify the new checks fail**\n\nRun: `python test_lit_fetch.py`\nExpected: the six new checks FAIL with `AttributeError`; the five Task 1 checks PASS.",
"- [ ] **Step 4: Run the suite**\n\nRun: `python test_lit_fetch.py`\nExpected: the six new checks PASS after the five Task 1 checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted \u2014 stop and fix)."))

PAIRS.append((
"- [ ] **Step 4: Run to verify the new checks fail**\n\nRun: `python test_lit_fetch.py`\nExpected: the six new checks FAIL with `AttributeError`; the eleven earlier checks PASS.",
"- [ ] **Step 4: Run the suite**\n\nRun: `python test_lit_fetch.py`\nExpected: the six new checks PASS after the eleven earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted \u2014 stop and fix)."))

PAIRS.append((
"- [ ] **Step 4: Run to verify the new checks fail**\n\nRun: `python test_lit_fetch.py`\nExpected: the four new checks FAIL with `AttributeError`; all earlier checks PASS.",
"- [ ] **Step 4: Run the suite**\n\nRun: `python test_lit_fetch.py`\nExpected: the four new checks PASS after all earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted \u2014 stop and fix)."))

PAIRS.append((
"- [ ] **Step 4: Run to verify the new checks fail**\n\nRun: `python test_lit_fetch.py`\nExpected: the two new checks FAIL with `AttributeError`; earlier checks PASS.",
"- [ ] **Step 4: Run the suite**\n\nRun: `python test_lit_fetch.py`\nExpected: the two new checks PASS after the earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted \u2014 stop and fix).",
2))

PAIRS.append((
"- [ ] **Step 4: Run to verify the new checks fail**\n\nRun: `python test_lit_fetch.py`\nExpected: the four new checks FAIL with `AttributeError`; earlier checks PASS.",
"- [ ] **Step 4: Run the suite**\n\nRun: `python test_lit_fetch.py`\nExpected: the four new checks PASS after the earlier checks (implementation landed in Step 1, no red run; a FAIL means transcription drifted \u2014 stop and fix)."))

PAIRS.append((
"""    u2 = lit_fetch.work_url("W1111111111", None)
    assert u2.endswith("/works/W1111111111?select=" + lit_fetch.SELECT_FIELDS)
    assert "api_key" not in u2 and "mailto" not in u2""",
"""    u2 = lit_fetch.work_url("W1111111111", None)
    q2 = urllib.parse.parse_qs(urllib.parse.urlparse(u2).query)
    assert q2["select"] == [lit_fetch.SELECT_FIELDS]
    assert "api_key" not in u2 and "mailto" not in u2"""))

PAIRS.append((
"import json,glob;edges=[json.loads(l)",
"import json,glob,pathlib;edges=[json.loads(l)"))

PAIRS.append((
"have={p.split('/')[-1][:-5] for p in glob.glob('.lit/papers/*.json')}",
"have={pathlib.Path(p).stem for p in glob.glob('.lit/papers/*.json')}"))

PAIRS.append((
"""    if kind == "wid":
        return "wid:" + value
    return "title:" + fold(entry.get("title") or "")""",
"""    if kind == "wid":
        return "wid:" + value
    if kind == "arxiv" and not entry.get("title"):
        return "arxiv:" + value
    return "title:" + fold(entry.get("title") or "")"""))

PAIRS.append((
'''def envelope(records):
    return json.dumps({"meta": {"count": len(records)}, "results": records})''',
'''def envelope(records):
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
    return calls'''))

PAIRS.append((
'''    lit_fetch.http_get = fake_http(handler)
    status, headers, body = lit_fetch.http_get("https://api.openalex.org/works/W1")
    assert status == 200''',
'''    fake_urlopen(handler)
    status, headers, body = lit_fetch.http_get("https://api.openalex.org/works/W1")
    assert status == 200'''))

PAIRS.append((
'''    handler.calls = []
    lit_fetch.time.sleep = slept.append
    lit_fetch.http_get = fake_http(handler)
    lit_fetch.http_get("https://api.openalex.org/works/W1")
    assert slept == [7.0]''',
'''    handler.calls = []
    lit_fetch.time.sleep = slept.append
    fake_urlopen(handler)
    lit_fetch.http_get("https://api.openalex.org/works/W1")
    assert slept == [7.0]'''))

PAIRS.append((
'''    lit_fetch.http_get = fake_http(handler)
    try:
        lit_fetch.http_get("https://api.openalex.org/works/W1")
        raise AssertionError("expected BudgetExhausted")''',
'''    fake_urlopen(handler)
    try:
        lit_fetch.http_get("https://api.openalex.org/works/W1")
        raise AssertionError("expected BudgetExhausted")'''))

PAIRS.append((
'''    lit_fetch.http_get = fake_http(handler)
    try:
        lit_fetch.http_get("https://api.openalex.org/works/W1")
        raise AssertionError("expected HTTPError")''',
'''    fake_urlopen(handler)
    try:
        lit_fetch.http_get("https://api.openalex.org/works/W1")
        raise AssertionError("expected HTTPError")'''))

PAIRS.append((
'''        lit_fetch.http_get = fake_http(handler)
        with contextlib.redirect_stdout(io.StringIO()):
            run = lit_fetch.Run()
            try:
                lit_fetch.verb_ids("|".join(ids), lit, None, False, run)''',
'''        fake_urlopen(handler)
        with contextlib.redirect_stdout(io.StringIO()):
            run = lit_fetch.Run()
            try:
                lit_fetch.verb_ids("|".join(ids), lit, None, False, run)'''))

PAIRS.append((
'''        lit_fetch.write_record(rec, lit)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            assert lit_fetch.verb_status(lit) == 0
        text = out.getvalue()
        assert "papers=1 edges=2 boundary=2 inbox_pending=0" in text''',
'''        lit_fetch.write_record(rec, lit)
        lit_fetch.write_edges(lit, lit_fetch.edges_of([rec]))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            assert lit_fetch.verb_status(lit) == 0
        text = out.getvalue()
        assert "papers=1 edges=2 boundary=2 inbox_pending=0" in text'''))

PAIRS.append((
'''    for e in malformed:
        e.pop("_ref", None)
        run.fail(e.get("ref", "?"), "unparseable ref")''',
'''    for e in malformed:
        e.pop("_ref", None)
        run.fail(e.get("ref", "?"), "unparseable ref")
        e["last_error"] = "unparseable ref"'''))

PAIRS.append((
'''            by_id = {bare_wid(r["id"]): r for r in parse_envelope(body)}
            records = []
            for wid in chunk:
                if wid in by_id:
                    record, wrote = write_one(by_id[wid], lit_dir, run,
                                              seed=seed_flag, source="fetch")
                    records.append(record)
                else:
                    canonical = resolve_alias(wid, aliases)
                    if canonical != wid:
                        run.fail(wid, "404; alias " + canonical
                                 + " also absent from response")
                    else:
                        run.fail(wid, "404; requested id absent from response")
            write_edges(lit_dir, edges_of(records))''',
'''            by_id = {bare_wid(r["id"]): r for r in parse_envelope(body)}
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
            write_edges(lit_dir, edges_of(records))'''))

PAIRS.append((
"report response-absent ids as 404 failures, then one edge union per chunk;",
"report response-absent ids as 404 failures, learn 301 merges when a response returns a canonical record for a requested id (alias saved, one merge note), then one edge union per chunk;"))

PAIRS.append((
"`BudgetExhausted` propagates after queuing the entry, leaving the original queue intact; regenerates the index when anything was written)",
"`BudgetExhausted` propagates without rewriting, so the original queue file stays intact; regenerates the index when anything was written)"))

PAIRS.append((
'''        except Exception as exc:
            entry["last_error"] = str(exc) or exc.__class__.__name__
            remaining.append(entry)''',
'''        except Exception as exc:
            reason = str(exc) or exc.__class__.__name__
            entry["last_error"] = reason
            run.fail(entry.get("ref", "?"), reason)
            remaining.append(entry)'''))

PAIRS.append((
'''        except BudgetExhausted:
            entry["last_error"] = "budget exhausted; re-run when the daily budget resets"
            remaining.append(entry)
            raise''',
'''        except BudgetExhausted:
            raise'''))

PAIRS.append((
'queued with their reason in "last_error". A BudgetExhausted abort leaves\n    the original queue intact except entries already resolved this run, and\n    re-runs are idempotent through skip-if-exists."""',
'queued with their reason in "last_error". A BudgetExhausted abort\n    re-raises before the rewrite, leaving the original queue file intact, and\n    re-runs are idempotent through skip-if-exists."""'))

PAIRS.append((
'''    ensure_corpus(lit_dir)
    record, wrote = write_one(payload, lit_dir, run, seed, source)
    write_edges(lit_dir, edges_of([record]))
    if wrote:
        regenerate_index(lit_dir)
    return record''',
'''    ensure_corpus(lit_dir)
    edges_before = len(load_edges(lit_dir))
    record, wrote = write_one(payload, lit_dir, run, seed, source)
    edges_after = write_edges(lit_dir, edges_of([record]))
    if wrote or edges_after != edges_before:
        regenerate_index(lit_dir)
    return record'''))

PAIRS.append((
'''    """Write one already-fetched payload: record (skip-if-exists) plus edges,
    then regenerate the index when something was written."""''',
'''    """Write one already-fetched payload: record (skip-if-exists) plus edges,
    then regenerate the index when anything changed (record written or edges
    added), so edge-only changes never leave the index stale."""'''))

PAIRS.append((
"(write one already-fetched payload plus its edges; regenerates the index when something was written)",
"(write one already-fetched payload plus its edges; regenerates the index when the record was written or the edge set changed)"))

PAIRS.append((
"- Consumes: `normalize_work` (Task 1), `union_edges`, `remap_edges`, `load_aliases`, `resolve_alias`, `render_index`, `now_iso` (Tasks 1-2).",
"- Consumes: `normalize_work`, `union_edges`, `remap_edges`, `resolve_alias`, `render_index`, `now_iso` (Tasks 1-2); `load_aliases` is defined in this task."))

PAIRS.append((
'''REPO="/c/Users/gower/OneDrive/Documents/GitHub/jgs-lit-memory"
for f in SKILL.md lit_fetch.py; do
  cmp "$REPO/skills/lit-capture/$f" "$HOME/.zcode/skills/lit-capture/$f" \\
    && cmp "$REPO/skills/lit-capture/$f" "$HOME/.claude/skills/lit-capture/$f" \\
    && cmp "$REPO/skills/lit-capture/$f" "$HOME/.agents/skills/lit-capture/$f" \\
    && echo "identical: $f"
done''',
'''REPO="/c/Users/gower/OneDrive/Documents/GitHub/jgs-lit-memory"
for d in "$HOME/.zcode/skills/lit-capture" "$HOME/.claude/skills/lit-capture" "$HOME/.agents/skills/lit-capture"; do
  cmp "$REPO/skills/lit-capture/SKILL.md" "$d/SKILL.md" || exit 1
  cmp "$REPO/lit_fetch.py" "$d/lit_fetch.py" || exit 1
done
echo "mirrors identical"'''))

PAIRS.append((
"Expected: `identical: SKILL.md` and `identical: lit_fetch.py`, no cmp output.",
"Expected: `mirrors identical`."))

PAIRS.append((
"`--status` prints `papers=1 edges=<len referenced_works> boundary=<same minus 1> inbox_pending=0` and a `last-synced:` line matching the index.",
"`--status` prints `papers=1 edges=<len referenced_works> boundary=<same count, every reference target being a boundary node> inbox_pending=0` and a `last-synced:` line matching the index."))

PAIRS.append((
'''    """Verified title search. Returns True only when a record was written.''',
'''    """Verified title search. Returns True when the paper is present
    afterwards: written now, or already in the corpus via skip-if-exists.'''))

PAIRS.append((
"- `verb_title(title, author, year, lit_dir, api_key, run) -> bool` (True only when a record was written)",
"- `verb_title(title, author, year, lit_dir, api_key, run) -> bool` (True when the paper is present afterwards: written or already in the corpus)"))

PAIRS.append((
'''        assert "last-synced: 2" in out2.getvalue()   # a real ISO timestamp''',
'''        assert "last-synced: 20" in out2.getvalue()   # a real ISO timestamp'''))

PAIRS.append((
"| Repo layout and install | 0, 8, 9 |",
"| Repo layout and install | 0, 8, 9 |\n| Corpus layout (`.lit/` tree, findings dir, git-tracked default, `git add .lit`) | 4, 8 |"))

PAIRS.append((
"- Offline, no network: `python test_lit_fetch.py` must print `all checks passed` and exit 0. All network-dependent checks run against `lit_fetch.http_get` fakes; sleeps are patched to no-ops inside the test process.",
"- Offline, no network: `python test_lit_fetch.py` must print `all checks passed` and exit 0. Call-site checks run against `lit_fetch.http_get` fakes; retry/backoff/budget checks run the real `http_get` over a faked `urllib.request.urlopen`; sleeps are patched to no-ops inside the test process."))

failures = 0
for pair in PAIRS:
    old, new = pair[0], pair[1]
    expected = pair[2] if len(pair) > 2 else 1
    n = text.count(old)
    if n != expected:
        print("MISMATCH (%d found, expected %d): %r" % (n, expected, old[:90]))
        failures += 1
    else:
        text = text.replace(old, new)

if failures:
    print("ABORTED: %d pair(s) mismatched; file unchanged" % failures)
    sys.exit(1)

io.open(PATH, "w", encoding="utf-8", newline="\n").write(text)
print("applied %d replacement groups OK" % len(PAIRS))
