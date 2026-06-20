# Spirit intent quality audit — negative-guideline and repetition sweep

## Scope

Audited active public Spirit records after the psyche flagged the record beginning `[Stop creating stray push-* bookmarks...]` as invalid intent and said: `[this isnt valid intent; negative guidelines arent intent.]`

The sweep covered the active public record set through Spirit:

- pre-retirement active public count: 1324
- post-retirement active public count: 1323
- parsed by the audit scanner: 1320 of the pre-retirement records; four records hit parser edge cases, so the automated duplicate/negative lists are a conservative first pass rather than a proof of absence
- active kind distribution in the parsed set: Decision 549, Principle 324, Correction 172, Clarification 150, Constraint 125

## Action already taken

### Retired qjie — stray push bookmark record

Spirit record `qjie` (the stray `push-*` bookmark record) was retired because the psyche directly identified it as invalid intent.

Pre-retirement lookup tombstone:

```nota
(RecordFound (qjie ([(Technology (Software (Engineering VersionControl)))] Correction [Stop creating stray push-* bookmarks. The psyche does not want agents pushing per-change or per-report push-named bookmarks; they accumulate as clutter and the psyche wants the practice to stop. Land work on main through the standard flow, or use a clearly-named review branch only when review is genuinely needed and delete it after merge. Existing stale push bookmarks should be cleaned up.] High Minimum Zero [])))
```

Retirement receipt:

```nota
(Retired qjie)
```

Post-retirement lookup returned `record not found`, and active public count dropped from 1324 to 1323.

## Findings

### Main failure pattern

Spirit has been used partly as a rulebook for agent process corrections. That creates records whose operative content is a negative instruction to agents rather than an affirmative statement of psyche intent. Some still contain a valid positive rule that should be clarified; others should probably be retired and left in AGENTS, skills, repo docs, or reports.

The strongest signal is the active `Correction` and `Clarification` volume: 322 parsed active records are one of those two kinds. Many are genuine corrections, but the density makes repeated overcapture likely.

### High-confidence cleanup candidates

These are the records I would handle first. They are not all the same action: some should retire, some should clarify into affirmative form, and some should be rehomed into documentation.

| Record | Current shape | Recommended handling |
|---|---|---|
| `7hrd` — working orders are not intent | Negative meta-guideline about what agents must not log. | Clarify or rehome. Affirmative surviving rule: Spirit holds durable psyche decisions, principles, corrections, clarifications, and constraints, not task orders. |
| `rvnf` — do not avoid Spirit because of overcapture | Negative first clause, positive discipline underneath. | Clarify to affirmative: agents apply the conservative Spirit gate and record only explicit durable intent. |
| `q9n2` — research question means assess and stop | Agent-response workflow rule, framed as stop/do-not-escalate. | Rehome to interaction skill unless the psyche wants this retained as an authorial work preference. |
| `hg6k` — troubleshooting should apply narrow safe fix | Agent-response workflow rule, overlaps with `q9n2` in stop/continue behavior. | Rehome or merge with interaction guidance. |
| `0sef` — injected info is not a stop instruction | Agent-process instruction with repeated negative wording. | Rehome to human-interaction / agent workflow guidance. |
| `el7z` — do not block waiting for subagent | Agent orchestration process rule; important, but Spirit is acting as rules storage. | Rehome to AGENTS / human-interaction; retire or clarify only if psyche confirms. |
| `q402` — reports exempt from claim flow | Operational coordination rule. | Rehome to orchestration docs; retire from Spirit if documentation already carries it. |
| `rqbj` — no line-number suffixes in chat | Chat formatting rule, not durable system intent. | Rehome to human-interaction/chat policy; likely retire. |
| `dfqp` — answer with report locator or backfill | Chat/report workflow correction. | Rehome to reporting skill; likely retire after docs cover it. |
| `b8la` — operator-safety and dirty repos | Pi/operator workflow tuning. | Rehome to Pi/operator-safety docs; likely retire from Spirit. |

### Negative phrasing that may hide valid affirmative intent

These should not be mechanically removed. They contain real design boundaries, but their summaries should be made affirmative if they remain active:

| Record | Why it tripped the audit | Safer affirmative center |
|---|---|---|
| `ax2k` — pre-production compatibility | Opens with `do not surface backward compatibility...`; nevertheless it matches a hard workspace rule. | Pre-production design optimizes for the best shape and expects coordinated breakage except at explicit production/external boundaries. |
| `di1r` — jj inline/headless commands | Uses `NEVER` and `do not`, but protects an operational deadlock boundary. | jj commands that can open an editor are invoked with inline/headless message flags. |
| `j4r1` — stateful software installs | Negative list of forbidden mutable installs. | Agent tool execution uses Nix ephemeral/declarative surfaces for software, with runtime application data as the only mutable state. |
| `jn3m` — Spirit database cutover | Negative cutover rule. | A Spirit profile cutover preserves reachability of existing records through migration or an explicit side-by-side test surface. |
| `kg2z` — Spirit CLI invocation style | Mostly documentation rule. | Inline NOTA is the ordinary Spirit CLI input; file-path input is reserved for cases where inline input is genuinely unsuitable. |
| `kx32` — prometheus deploy safety | Negative operational safety rule. | Prometheus deploys preserve router reachability and use safe activation paths for network-owning services. |

### Overlap and repetition candidates

The scanner found a small set of high-similarity pairs. These are worth manual Spirit maintenance because they look like duplicate capture, standalone clarification, or same-substance repetition.

| Pair | Shared substance | Suggested handling |
|---|---|---|
| `oxgh` / `5mbd` — assembled schema struct map representation | Both say assembled-schema structs use key-value brace maps from field names to field types. | Supersede into one record or retire the weaker duplicate. |
| `kkq3` / `u0ik` — schema variants and macros | Both say schema variants may be ordinary vectors or macros, and macros bring their own schema-reading logic. | Merge/clarify; likely duplicate. |
| `0be2` / `b95h` — schema files next to Rust source | Both say schema files create the data types libraries use and may live beside Rust source. | Merge; one appears to be a refined restatement. |
| `ppuk` / `sfwv` — assembled schema artifact | Both describe the resolved assembled schema / Asschema as pure NOTA with macros resolved. `sfwv` is a standalone clarification/gap-fill. | Resolve the clarification into the target record and retire/remove standalone `sfwv`. |
| `5sta` / `ugig` — plane identity as data-carrying enum | Both describe the schema root plane surface as a matchable data-carrying enum. | Merge or clarify one as the canonical formulation. |
| `7tqc` / `zste` — daemon boilerplate versus engine logic | Both say component logic belongs in engine/logic objects and daemon startup/transport boilerplate belongs behind libraries/macros. | Merge; likely same architectural intent. |
| `gmlv` / `r1un` — actor reaction/action enums | Both say schema-created base enums define actor reaction/action input/output types that execution matches. | Merge or clarify. |
| `b9qx` / `k5ov` — cloud-designer/cloud-operator lane registration | Similar wording but different lane referents. | Not a duplicate; keep separate or represent lane registration in a structured registry instead of Spirit. |

### Gap-fill and standalone clarification risk

Fifteen active parsed records contain `gap-fill`; several are `Clarification` records rather than edits to their targets. These should be reviewed under the `ResolveClarification` discipline, because standalone clarification records make future readers reconcile multiple active records manually.

Priority review set:

- `sfwv` — assembled schema artifact; overlaps `ppuk`
- `pokt` — schema naming mirror
- `ublb` — REST-shaped wire data types
- `v1ya` — schema daemon/agent resolving schemas and caching assembled material
- `yenl` — one-capturer rule default capturer; may already be correctly manifested in `skills/intent-log.md`

## Recommended maintenance plan

1. Treat `qjie` as complete: it is retired and tombstoned above.
2. Do not bulk-remove every record containing `do not`, `never`, or `must not`; many are real design decisions badly worded.
3. Run a review batch over the high-confidence process-rule records and ask the psyche for one batch authorization: retire from Spirit, clarify affirmatively, or keep.
4. Run a second batch over the overlap pairs, using `Supersede` for true duplicates and `ResolveClarification` for standalone clarifications.
5. After each Spirit maintenance batch, update the corresponding durable guidance file so valid rules are not lost when removed from Spirit.

## Command artifacts

Temporary audit artifacts were written under `/tmp/spirit-audit/` during this pass:

- `public-active.out` — raw pre-retirement active public observe output
- `qjie.lookup` — qjie tombstone lookup
- `audit_spirit.py` — scanner for negative-guideline and similarity candidates
- `audit.tsv` — scanner output

They are not durable workspace state; this report is the durable audit record.
