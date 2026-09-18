# Make awesome-sysml-v2 Public Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Flip `jgsystemsconsulting/awesome-sysml-v2` from private to public behind three recorded pre-flip gates, then verify anonymous reachability, field preservation, and Actions state, changing zero files and making zero commits.

**Architecture:** A four-task settings run, not a code change. Task 1 gates the flip: identity capture with an `isPrivate` assertion, a recorded secret scan over `af07711..HEAD`, and a gh flag availability check. Task 2 is the single visibility change (gh primary, REST fallback). Task 3 proves the anonymous payload and the three workflows. Task 4 sweeps the spec acceptance criteria and proves the workspace untouched. Every artifact lands in the run report in the SDD workspace; the repository keeps no record of this run.

**Tech Stack:** gh 2.88.0 (authenticated as repo owner, admin), git, curl, jq 1.7.1. All four verified present on the execution machine on 2026-09-15.

**Spec:** `C:\Users\gower\OneDrive\Documents\GitHub\awesome-sysml-v2\docs\superpowers\specs\2026-09-16-make-repo-public.md`

## Global Constraints

- GitHub settings operation only. No file writes in the repo, no commits, no CI or workflow edits. Spec: "No file changes, no commits, no CI edits."
- Every repo-scoped command uses the fully qualified slug `jgsystemsconsulting/awesome-sysml-v2` (wrong-target flip is a spec risk).
- The executor's gh is authenticated as the repo owner (admin), so `gh repo edit` is authorized without elevation.
- Any Task 1 gate failure stops the run as BLOCKED. The flip is never attempted with a failed gate.
- Process records go to the run report at `.superpowers/sdd/2026-09-16-make-repo-public/run-report.md` (SDD workspace, outside the repo). The parent creates the file and pastes its path into every task dispatch; the executor appends its step outputs to that path. This plan writes no repo files.
- Task 3 Step 2 defines PRE_DESC and PRE_TOPICS by pasting from the run report. If the description contains a single quote, dollar, or backslash, re-derive it in-session instead of pasting: `PRE_DESC="$(gh repo view jgsystemsconsulting/awesome-sysml-v2 --json description --jq .description)"` (the in-session re-derivation is equivalent because Task 3 runs immediately after the flip).
- Rollback asymmetry: reverting to private reverses the setting, not the exposure. Forks, clones, and crawler captures made while public persist. The Task 1 gates, not rollback, are the protection.
- A disabled workflow discovered during verification is a finding to record, never a fix to apply in P1 (spec non-goal).
- Org-level settings (fork policy, member permissions) are out of scope. Do not touch them.
- Tasks run in fresh subagents under SDD, so cross-task values (`PRE_DESC`, `PRE_TOPICS`, HEAD, flag path) travel through the run report text, not shell state.

## Research

research: skipped (no-open-world-questions; platform-settings operation)

Round 0 log: `docs/superpowers/research/2026-09-16-make-repo-public-research-log.md`. Command syntax is re-verified at execution time against the installed gh (Task 1, Step 5).

## Codebase context

Context gate skipped (nothing-to-map): P1 changes GitHub repo settings, not workspace files. Log: `docs/superpowers/context/2026-09-16-make-repo-public-context-log.md`.

Facts from earlier rounds, carried in the spec:

- Description is set. Topics are `awesome`, `awesome-list`, `mbse`, `sysml`, `sysml-v2`. `isPrivate` is true.
- Three workflows present: `Lint`, `Links`, `Freshness report`. Actions are SHA-pinned (P9).
- Advisory a-09 (round-2 review, 2026-09-15) verified no committed secrets in history; its review predates commit `af07711`.

Two facts re-measured on 2026-09-15 while authoring this plan (executors rely on their own measurements, these set expectations):

- `af07711..HEAD` currently holds **four** commits (`1747fa6`, `695dd1b`, `bf25772`, `b562394`), not the three the spec recorded. `b562394` landed after spec lock. The gate is "no scan hits", not a commit count; the executor records the count it finds.
- The working tree shows `?? docs/` untracked only. Those are the pipeline's own process artifacts, exempt under AC4.

## Run report convention

The run report is the package's only record and lives outside this repository. Each step below names exactly what to append. Nothing in this run writes to the repo.

---

### Task 1: Pre-flip gate

**Files:**
- Create: none. Modify: none. All output goes to the run report.

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: `HEAD at pre-flip` (full SHA from `git rev-parse HEAD`), `PRE_DESC` (exact description string), `PRE_TOPICS` (sorted JSON array of topic-name strings), and `flag_path` (`primary` or `fallback`). Tasks 2, 3, and 4 consume all four.

**Model:** flash

- [ ] **Step 1: Record HEAD**

Run from the repo root:

```bash
git rev-parse HEAD
```

Expected: a full SHA; currently starts with `b562394`. Append it to the run report as `HEAD at pre-flip`. Task 4 re-checks this value to prove zero commits were made.

- [ ] **Step 2: Capture identity and assert private**

Run:

```bash
gh repo view jgsystemsconsulting/awesome-sysml-v2 --json isPrivate,description,repositoryTopics
```

Expected: `"isPrivate": true`. Append the raw output to the run report.

If `isPrivate` is false, discriminate before closing (spec rule): compare the captured `description` and topic names against the known facts in Codebase context. A match means the repo is already public; record `already public at pre-flip`, skip Task 2 entirely, and continue with Task 3 (verification still applies) and Task 4. A mismatch means the command hit the wrong repo: stop as BLOCKED.

- [ ] **Step 3: Extract the normalized capture**

Run:

```bash
gh repo view jgsystemsconsulting/awesome-sysml-v2 --json description --jq .description
gh repo view jgsystemsconsulting/awesome-sysml-v2 --json repositoryTopics --jq '.repositoryTopics | map(.name) | sort'
```

Expected description: a non-empty string. Record it verbatim as `PRE_DESC`. Expected topics: `["awesome","awesome-list","mbse","sysml","sysml-v2"]`. Record the array exactly as printed as `PRE_TOPICS`.

The sort normalization is load-bearing: the gh capture carries topic name objects, while the anonymous REST payload in Task 3 carries plain strings. Comparing sorted name strings is the only form both sides share.

- [ ] **Step 4: Secret-scan currency (recorded artifact)**

Run the spec's exact command from the repo root (the `${{ secrets.` exclusion removes Actions secret-reference idioms, which are indirections, not credentials):

```bash
git log -p af07711..HEAD | grep -inE 'password|passwd|api[_-]?key|BEGIN [A-Z]+ PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|github_pat_' | grep -vF '${{ secrets.'
```

Expected: no output. Append to the run report: the baseline SHA `af07711`, the HEAD scanned (Step 1 value), the command verbatim, the commit count in the range (`git log --oneline af07711..HEAD | wc -l`; currently 4), and the empty output.

Any non-empty output is a hit and BLOCKS the flip. Do not triage hits or wave prose matches through. Paste the matching lines into the run report and stop as BLOCKED. The gate is not satisfied by prose; the recorded empty output is the flip precondition.

- [ ] **Step 5: Flag availability check**

Run:

```bash
gh repo edit --help | grep accept-visibility-change-consequences
```

Expected: one or more matching lines. Non-empty output sets `flag_path` to `primary`; empty output sets `flag_path` to `fallback`. Record the decision in the run report.

Done-when: the run report holds the HEAD value, the raw `gh repo view` capture showing `isPrivate: true` (or the recorded already-public branch), `PRE_DESC`, `PRE_TOPICS`, the scan artifact (baseline SHA, command verbatim, HEAD scanned, range count, empty output), and the `flag_path` decision. All three gates green before Task 2 starts.

---

### Task 2: The flip

**Files:**
- Create: none. Modify: none (a GitHub setting changes, not a file).

**Interfaces:**
- Consumes: `flag_path` from Task 1 Step 5.
- Produces: `isPrivate == false` on `jgsystemsconsulting/awesome-sysml-v2`, and the exact flip command used, recorded in the run report.

**Model:** flash

- [ ] **Step 1: Flip visibility (primary path)**

If `flag_path` is `primary`, run:

```bash
gh repo edit jgsystemsconsulting/awesome-sysml-v2 --visibility public --accept-visibility-change-consequences
```

Expected: exit 0 with no error output. The accept flag suppresses the interactive consequences prompt, so the command is non-interactive.

- [ ] **Step 2: Flip visibility (fallback path, only if primary unavailable)**

If `flag_path` is `fallback` (installed gh lacks the flag; the acknowledge flag is a gh-cli guard, not an API requirement), run the equivalent REST call with a typed boolean (`-F`, not `-f`, which sends the untyped string `"false"`):

```bash
gh api -X PATCH repos/jgsystemsconsulting/awesome-sysml-v2 -F private=false
```

Expected: exit 0 and a JSON payload containing `"private": false`.

- [ ] **Step 3: Confirm the setting took**

Run:

```bash
gh repo view jgsystemsconsulting/awesome-sysml-v2 --json isPrivate --jq .isPrivate
```

Expected: `false`. Append to the run report: which flip command was used (primary or fallback) and this confirmation output.

Done-when: `isPrivate` is false and the flip command used is recorded. If Step 1 or 2 failed, do not retry blind: capture the error, stop, and report; the run report distinguishes a failed flip (setting still private) from a flipped-but-unverified one.

---

### Task 3: Post-flip verification

**Files:**
- Create: none.

**Interfaces:**
- Consumes: `PRE_DESC` and `PRE_TOPICS` from the run report (Task 1 artifacts). Tasks run in fresh subagents, so read both values back from the report and paste them into the shell variables in Step 2.
- Produces: the anonymous 200 proof, the field-preservation comparison result, the workflow list output.

**Model:** flash

- [ ] **Step 1: Anonymous API status**

Run:

```bash
code=$(curl -s -o api_body.json -w "%{http_code}" https://api.github.com/repos/jgsystemsconsulting/awesome-sysml-v2)
echo "$code"
```

Expected output: `200`; record it and continue to Step 2. On `403`: inspect the body (`cat api_body.json`) — if it mentions rate limit, route to Step 4 (fallback); any other code is a failure to investigate before proceeding. Keep `api_body.json` for the report; delete it before Task 4 so the AC4 sweep sees a clean tree (it is scratch, not a repo file).

- [ ] **Step 2: Anonymous payload field comparison**

Set the Task 1 captures as shell variables in the same session, pasted from the run report (or re-derived per the Global Constraints escaping rule):

```bash
PRE_DESC='<paste the exact PRE_DESC string from the run report>'
PRE_TOPICS='["awesome","awesome-list","mbse","sysml","sysml-v2"]'
curl -s https://api.github.com/repos/jgsystemsconsulting/awesome-sysml-v2 | jq -e --arg d "$PRE_DESC" --argjson t "$PRE_TOPICS" '.visibility == "public" and .description == $d and (.topics | sort) == $t'
```

Use the actual `PRE_TOPICS` array recorded in Task 1 Step 3; the literal above is the expected value, not a substitute for the capture. Expected: `true` and exit 0. This single comparison proves AC1's payload half (`"visibility": "public"` in the anonymous body) and all of AC2 (description and topics match the pre-flip capture). Record the command and result.

- [ ] **Step 3: Actions state**

Run:

```bash
gh workflow list -R jgsystemsconsulting/awesome-sysml-v2 --all
```

Expected: three rows named `Lint`, `Links`, and `Freshness report`, each with state `active`. Public repos run Actions by default with no minute billing, so no enabling step exists or is allowed. Any row not `active`: record it as a finding in the run report and continue. Do not enable or edit anything (spec non-goal: a disabled workflow is a finding, not a fix).

- [ ] **Step 4: Rate-limit fallback (only if Step 1 routed here on 403)**

Run the HTML probe:

```bash
curl -s -o /dev/null -w "%{http_code}" https://github.com/jgsystemsconsulting/awesome-sysml-v2
```

Expected: `200`. This proves anonymous reachability. Then confirm the payload fields with the authenticated call. This step is self-contained: re-derive the captures in-session per the Global Constraints rule rather than relying on Step 2's shell:

```bash
PRE_DESC="$(gh repo view jgsystemsconsulting/awesome-sysml-v2 --json description --jq .description)"
PRE_TOPICS="$(gh repo view jgsystemsconsulting/awesome-sysml-v2 --json repositoryTopics --jq '.repositoryTopics | map(.name) | sort')"
gh api repos/jgsystemsconsulting/awesome-sysml-v2 | jq -e --arg d "$PRE_DESC" --argjson t "$PRE_TOPICS" '.visibility == "public" and .description == $d and (.topics | sort) == $t'
```

Expected: `true`, exit 0. Note the authenticated comparison proves field preservation but not anonymity; anonymity was proven by the HTML 200 probe. Record that split as the spec-sanctioned fallback evidence.

Done-when: the run report holds the anonymous `200` (or the fallback pair: HTML `200` plus authenticated jq pass), the jq comparison result, and the workflow list output with three `active` rows (or the recorded disabled-workflow finding).

---

### Task 4: Acceptance sweep and no-change proof

**Files:**
- Create: none. Modify: none. This task only reads and records.

**Interfaces:**
- Consumes: evidence from Tasks 1 through 3, plus the `HEAD at pre-flip` value from Task 1 Step 1.
- Produces: the four AC verdicts and the no-change statement in the run report.

**Model:** flash

- [ ] **Step 1: AC1 verdict**

Check the evidence: Task 3 Step 1 printed `200`, and Task 3 Step 2 (or the Step 4 fallback: HTML 200 plus the authenticated jq pass) proved `"visibility": "public"` in the payload. Record `AC1: PASS` with pointers to both outputs; the fallback pair is sanctioned evidence for AC1. Any miss: record `AC1: FAIL` with the actual outputs; the package is not complete on a FAIL.

- [ ] **Step 2: AC2 verdict**

Check the evidence: the Task 3 jq comparison exited 0, matching `description` exactly and sorted topic names exactly against the Task 1 capture. Record `AC2: PASS` with the pointer. A FAIL here means the flip altered metadata; capture both payloads and stop.

- [ ] **Step 3: AC3 verdict**

Check the evidence: the Task 3 Step 3 workflow list shows `Lint`, `Links`, and `Freshness report`, each with state `active`. Record `AC3: PASS` with the output. An inactive workflow makes this `AC3: FAIL` plus the finding already recorded in Task 3; the verdict is FAIL precisely because AC3 requires the listing to show active. No fix is applied in P1.

- [ ] **Step 4: AC4 verdict (zero changes, zero commits)**

Run from the repo root:

```bash
git status --porcelain
git rev-parse HEAD
```

Expected: `git status --porcelain` shows no tracked-file entries, that is no line starting with `M `, ` M`, `A `, or `D `. The line `?? docs/` (untracked) is the pipeline's own process records and is exempt under AC4; any other untracked line is an AC4 FAIL until identified. `git rev-parse HEAD` must equal the Task 1 Step 1 `HEAD at pre-flip` value, proving this run made zero commits. Record `AC4: PASS` with both outputs. A modified tracked file or a moved HEAD: `AC4: FAIL` with the diff of what changed.

- [ ] **Step 5: Close the run report**

Append the closing statement: all four AC verdicts with evidence pointers, the flip command used, the scan artifact reference (baseline SHA, HEAD scanned, empty output), and the sentence "No repo file changed and no commit was made in this run." The run report is the package's only record; the repository keeps none.

Done-when: four recorded verdicts with evidence pointers, HEAD unchanged from Task 1, and the tracked working tree clean of modifications.

---

## Rollback

Flip back with:

```bash
gh repo edit jgsystemsconsulting/awesome-sysml-v2 --visibility private --accept-visibility-change-consequences
```

REST equivalent: `gh api -X PATCH repos/jgsystemsconsulting/awesome-sysml-v2 -F private=true` (`-F` sends a typed boolean).

The setting reverses immediately; the exposure does not. Any fork, clone, or crawler capture made while public persists after the revert. Treat content exposure as permanent once the flip succeeds. This asymmetry is why Task 1 gates the flip instead of relying on rollback.
