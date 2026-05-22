# Intent Substrate Certainty Vocabulary Drift (v2, superseded by /269)

*v2. The original §4 mapping proposal (`High` to `Maximum`) is
superseded by `/269`'s widening of the certainty vocabulary into
the workspace-universal `signal-sema::Magnitude` type with seven
variants — including a first-class `High`. The seven drifted
records become valid as-is once Spirit consumes Magnitude; no
mapping is required. §1-§3 (diagnostic) and §5 (general substrate-
migration discipline) survive. See §4 and Status.*

Designer report. The legacy file substrate (`intent/*.nota`) carries
`Certainty High` on seven records that the deployed persona-spirit
daemon will reject with `unknown variant for enum Certainty`. This
is the first concrete substrate-replacement gotcha beyond the
surface-level "same kinds, same fields" assumption.

## 1. What was discovered

During the 2026-05-21 design conversation, the dispatching agent
tried to log an intent record through the `spirit` CLI carrying
`Certainty High`. The daemon refused the record. The deployed
signal contract at
`/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs`
lines 208-215 defines exactly three variants —
`Maximum`, `Medium`, `Minimum` — and the decoder treats every
other PascalCase token at that position as `unknown variant`.

`skills/intent-log.md` (lines 159, 254-263) already documents the
same three-variant vocabulary. The seven `High` records are
therefore drift from the file-substrate discipline too; the
deployed Spirit just makes the breakage executable instead of
latent.

## 2. Scope of the drift — count and examples

Across `intent/*.nota`, certainty token usage is:

| Variant | Count | Status |
|---|---|---|
| `Maximum` | 314 | conforming |
| `Medium` | 31 | conforming |
| `Minimum` | 6 | conforming |
| `High` | 7 | **drift — daemon rejects** |
| `Low` | 0 | n/a |

The seven `High` records cluster around two dates:

### 2a. `intent/persona.nota` — 2026-05-20 17:30 cluster (4 records)

All four are agent-self-narrated as "conservative-by-default
downgrade from Maximum." The agent invented `High` because the
intent-log skill had no rung between `Maximum` and `Medium`.

Line 351-356 (`Decision`, reuse-over-spawn orchestrator default).
Summary tail:
```
    "Psyche stating reuse-over-spawn as orchestrator default, with
    explicit uncertainty marker. Logged at High rather than Maximum
    per the conservative-by-default principle."
    High
    2026-05-20 17:30)
```

Line 393-398 (`Principle`, default channel-grant to mind). Summary
tail:
```
    "Default channel-grant policy for the mind-to-agents direction.
    Marked working principle per psyche's explicit uncertainty;
    logged at High rather than Maximum because psyche flagged
    openness to counter-evidence."
    High
    2026-05-20 17:30)
```

The other two (lines 358-363 context-compaction policy, lines
379-384 skills-bundle-into-roles) follow the same pattern.

### 2b. `intent/workspace.nota` — 2026-05-20 09:42 cluster (2 records)

Both carry the placeholder context `"psyche"` plus a report path
as the verbatim — agent shorthand for psyche-directed reading-list
records.

Line 455-460 (`Decision`, signal-frame/executor migration):
```
  "psyche"
  "reports/operator/141-signal-frame-executor-correction-examples.md"
  High
  2026-05-20T09:42:51Z)
```

The second (lines 475-480) is a `Clarification` pointing at
`/246-v4`, same shape.

### 2c. `intent/reports.nota` — 2026-05-20 11:53 (1 record)

Line 143-148, `Decision`, "Path correction and reinforcement after
the bundled fix report was renamed to v2." — `High`,
`2026-05-20T11:53:19+02:00`. Same reading-list-directive shape.

## 3. Why it matters — substrate-migration implication

The headline assumption going into the file → spirit migration was
that both substrates share the five-kind taxonomy and the
certainty vocabulary, so hand-relogging is mechanically
straightforward. The seven `High` records refute that at the data
layer: of 358 conforming records, seven (~2%) cannot survive a
naive round-trip — the daemon rejects them on parse, not on
semantic conflict.

The file substrate is permissive: NOTA parsers accept any
PascalCase token at the certainty position because the file is not
validated against a typed schema. The spirit substrate is strict:
`signal-persona-spirit`'s rkyv-archived enum has a closed-world
variant set enforced by the decoder. The lesson generalises — any
substrate replacement carries hidden vocabulary drift that only
surfaces when the strict substrate refuses old data.

Because workspace direction (`intent/persona.nota` 2026-05-20T15:30Z)
forbids import logic inside spirit, a naive bulk relog would strand
mid-stream on the first `High` record.

## 4. Resolution path (superseded by /269)

The original v1 proposal — normalise the seven `High` records by
mapping them to `Maximum` before relog — is **superseded by `/269`**.
The right move is widening the type, not narrowing the writer.

`/269` lands a workspace-universal `signal-sema::Magnitude` enum
with seven unit variants (`Minimum`, `VeryLow`, `Low`, `Medium`,
`High`, `VeryHigh`, `Maximum`) and retires `signal-persona-spirit`'s
three-variant `Certainty`. Once Spirit's `Entry.certainty` field
points at `Magnitude`, the seven drifted records become valid as-is:
no mapping, no rewritten summaries, no audit-trail breadcrumbs. The
agent that wrote `High` was right about the rung; the original type
was too narrow.

The §6 open question (`High` to what?) dissolves: nowhere. Status
update in `skills/intent-log.md` happens after the Spirit consumer
migration lands, listing the seven-variant Magnitude vocabulary in
place of the old three.

See `/269` for the type definition, home determination
(`signal-sema`), and consumer-migration plan.

## 5. Broader principle for substrate-migration discipline

Any substrate replacement should follow this discipline:

1. **Enumerate every closed-world enum on both sides before
   relogging.** Compare variant sets. Where they differ, design
   an explicit mapping. Don't assume parallel evolution kept the
   vocabularies aligned.

2. **The strict substrate is the ground truth.** When the deployed
   daemon rejects a token the file accepted, the daemon's
   vocabulary wins — the file substrate was permissive by
   accident, not by design. Migration is a normalisation pass,
   not a backward-compatible bridge.

3. **Surface mismatches in a report before bulk relog.** This
   report is the artifact of that discipline for the certainty
   case. Any future relog of a different field (kind taxonomy,
   focus areas, observation modes) should produce the equivalent
   audit before the first record moves.

4. **A "dumb tool" still needs the mapping table.** Even if the
   psyche directs a separate non-spirit tool to assist relogging,
   that tool needs the same vocabulary mapping baked in. Spirit's
   no-import rule isolates the daemon, not the migration
   responsibility.

## Status

v2 supersedes v1. The §4 mapping proposal (`High` to `Maximum`,
plus the §6 open question selecting between mapping variants) is
retired; resolution shifts to `/269`'s widening of the certainty
vocabulary into the universal `signal-sema::Magnitude` type. §1-§3
(the diagnostic — count of seven, cluster locations, why a strict
substrate refuses old data) and §5 (the broader substrate-migration
discipline — enumerate enums on both sides; strict substrate is
ground truth; surface mismatches in a report before bulk relog;
even a dumb tool needs the mapping table) survive as written.

See `reports/designer/269-universal-magnitude-type-design.md`.
