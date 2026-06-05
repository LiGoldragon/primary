# Spirit Working Instruction Removal Audit

## Scope

Active production Spirit v0.5.2 was queried with:

```sh
spirit "(Observe (Records ((Any []) None Any Any SummaryOnly)))"
```

This returned 1,647 public summary records. I screened for summaries that
look like task directives and applied the after-the-task test from
`skills/intent-log.md`: if the summary stops guiding once the named task is
done, it does not belong in Spirit.

## Removed

These records were obvious working instructions rather than durable psyche
intent:

- `00mn` — "Use subagents to bring orchestrate toward Spirit maturity."
- `1fz3` — "Use inline jj workflow for U6 commit and push."
- `78cg` — "Audit schema macro generation for old-macro reuse..."
- `8gbv` — "Test the new Spirit privacy setting..."
- `ciz2` — "Run full version-projection verification for U6 when feasible."
- `d5v4` — "Deploy updated Pi profile locally."
- `ehwu` — "Fix /310 bead dependencies, then work available beads with subagents."
- `ifna` — "Run cargo with CARGO_BUILD_JOBS=2 and Nix checks with max-jobs 0 for this task."
- `jmdi` — "Use an asynchronous subagent for substantial parallel work while the operator implements..."
- `l3x7` — "Use subagents for the schema and NOTA macro MVP pass."
- `m341` — "Finish primary-kbmi.2.1..."
- `m6xq` — "Dispatch sub-agents to bring orchestrate designer-implementation to match Spirit's current maturity..."
- `o7o7` — "Migrate live Spirit to v0.2 now."
- `q8qo` — "Implement /318 R10 agent contract rename preparation..."
- `reh3` — "Start atomic socket handover prototype..."
- `ujj4` — "Use system-specialist lane rather than second-system-assistant for primary-kbmi.2.1 scope claim."
- `y89j` — "Refresh Spirit work before orchestrate parity work."
- `ziip` — "Refresh reports and intent before selecting next work."
- `apre` — "Rename runtime migration lookup types in version-projection only."
- `dqur` — "Use jj non-interactively and avoid raw git commits for the rename work."
- `ndkp` — "Update Pi and investigate auto-compaction failure."

## Kept For Now

Some records start with an imperative verb but carry durable system shape. I
left those alone because removal would discard real design intent:

- `0ktv` — cloud component should exist as a working Cloudflare DNS tool.
- `5f68` — public `spirit-next` repository should exist as the running
  schema-derived Spirit pilot.
- `60an` — owner-signal-version-handover contract should exist.
- `571/cpsv/hgvm/cupj/va72`-style records — implementation-shaped summaries
  that also encode design decisions. These need a later split/correction pass,
  not a blind remove.

## Reboot Records

The records from the reboot incident are genuine intent:

- `bev5` — home profile activation must persist across reboot; reboot rollback
  to an older Claude is a bug.
- `9375` — legacy Spirit daemon slots that remain deployed should be fixed to
  run, not removed as the primary fix.
