# Triage Log — 2026-09-15-awesome-sysml-v2-findings

| Finding | First seen | Last seen | Verdict | Rationale |
|---------|------------|-----------|---------|-----------|
| I1 freshness-window-mismatch | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | Three lenses corroborate 24-month criterion (contributing.md:10) vs 12-month cutoff (stale.yml:22) |
| I2 link-report-issue-spam | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | Fixed-title create without upsert confirmed against stale.yml:44-48 contrast |
| I3 stale-curl-set-e-aborts | r1 2026-09-15 | r1 2026-09-15 | downgraded HIGH to MEDIUM | Advisory monthly job (stale.yml:5), loud failure in Actions log, no data loss |
| I4 actions-not-sha-pinned | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | Mutable major-tag pins confirmed in all three workflows |
| I5 npx-awesome-lint-unpinned | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | No package.json or lockfile anywhere in repo |
| I6 lint-yml-no-permissions | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | Only workflow missing a top-level permissions block |
| I7 pr-checklist-omits-markdownlint | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | Template line 4 omits markdownlint that contributing.md and lint.yml both require |
| I8 link-health-no-contributor-path | r1 2026-09-15 | r1 2026-09-15 | kept, MEDIUM | No PR-time link check; links.yml cron-only with fail: false |
| kill duplicates (k-03, k-07, k-13, k-14) | r1 2026-09-15 | r1 2026-09-15 | dropped | Restate surviving I5, I7, I2, I3; not recorded as advisories |
