# Codex succession pilot receipt

## Result

A fresh, independent candidate-home pilot completed its first real read-only turn. It did not transfer the predecessor's native identity, transcript, checkpoint, or store.

- Native UUID: `01a0f316-22b2-7851-8fec-203f698471a4`
- First turn: `01a0f316-2324-77b0-98ca-7eb87152a99c`
- Turn metadata: `gpt-6.1-sol`, effort `medium`, at `2026-09-30T16:11:52.187Z`.
- Candidate rollout: `/home/li/.codex-next-8mkkxq293hk2/sessions/2026/09/30/rollout-2026-09-30T10-11-49-01a0f316-22b2-7851-8fec-203f698471a4.jsonl`.
- Independent Flow claim: `f69847`, with `/home/li/primary/flows/.f69847.flow-id` present (mode 0600).

The first prompt contained the supplied old-seat final handoff verbatim, with only paragraph breaks flattened for the single-argument launcher, and explicitly stated that Fable's later succession decision superseded same-UUID/model transfer. The initial local launch used candidate binary and candidate `CODEX_HOME`; it produced the real census answer but had no candidate app-server connection.

## First answer evidence

The final answer identified seven existing old-server consumers: unregistered PID 1824790 on legacy PID 1936, and six registered clients on promoted PID 1960. It mapped their panes, FDs, and sockets; found no candidate-server external consumer at that time; identified both Flow units' remaining legacy `Requires=`/`After=` dependency; and stated that retirement must wait for those consumers and dependency replacement. It also identified itself as candidate binary/home but local-only at that moment. It made no files, service, seat, messaging, network, readiness-probe, or lifecycle changes.

## Candidate endpoint repair

The generated `codex-next-flow-client` wrapper exports the candidate `CODEX_HOME` and executes Codex unchanged. The separate plain `codex-next` wrapper adds `--remote`; Flow's client therefore omitted remote by construction.

The completed same-store UUID was resumed once in `w1:pZ` using:

```
codex-next-flow-client resume 01a0f316-22b2-7851-8fec-203f698471a4 \
  --remote unix:///home/li/.codex-next-8mkkxq293hk2/app-server-control/app-server-control.sock \
  -C /home/li/primary
```

A first resume including the old dangerous permission override failed before connection because remote resume rejects that override. The successful resume made no prompt or new turn. Current pilot PID 2016681 FD 40 (socket inode 51905571) is connected to candidate app-server PID 1965146 FD 11 (inode 51904921), through candidate socket inode 33454845.

Herdr pane `w1:pZ` records the witnessed UUID as a Codex identity and display title `Field.{ Sol f69847 } | GPT-6.1-Sol (Luna-tier)`. The terminal's own title remains `Fix launcher handoff formatting | primary`.

## Old-seat closure

After the meaningful pilot answer, the authorized old route was closed with:

```
herdr pane close w1:pV
```

Herdr returned `{"type":"ok"}`. The old Field Luna UUID `01a0ee49-43e2-7b02-8a24-b81025548ba8` is absent from the current Herdr roster. Its native files and Flow lane were not deleted. No other seat or server was touched for the closure.

## Remaining binding fault

The pilot is not yet addressable through Messenger. `messenger-clj list` has no `f69847` row and retains stale `025548`. One no-probe registration attempt,

```
hm-register f69847 field_luna_successor --session default \
  --native-thread 01a0f316-22b2-7851-8fec-203f698471a4
```

was refused: `Herdr agent_session is malformed or does not match the agent`.

The live Herdr record holds a correct session identity with `agent_session.agent = codex`, but its top-level `agent` field is `field_luna_successor`, a stale result of an earlier incorrect metadata report that treated `--agent` as a display name. Releasing the documented metadata authority and issuing a higher-sequence `report-agent` correction with `--agent codex` did not change that top-level value. Further repair was held: the authorized scope limited this to metadata interfaces, and restarting the completed pilot merely to force detector reclassification was not attempted.

## Final lifecycle repair and registration

The remaining malformed Herdr record was repaired without changing native identity or creating a turn. Before repair, the completed pilot remained idle with the same UUID, first turn, and candidate remote peer. `w1:pZ` was split to fresh owned `w1:p0`, then only `w1:pZ` was closed; both Herdr calls returned typed `{"type":"ok"}`. No other pane, seat, service, server, Flow lane, or native file was changed.

The same candidate UUID was resumed once in `w1:p0` through the explicit candidate remote endpoint. Final Herdr lookup is addressable as `field_luna_successor` and records:

- harness agent: `codex`;
- `agent_session.agent`: `codex`;
- UUID: `01a0f316-22b2-7851-8fec-203f698471a4`;
- pane: `w1:p0`;
- title: `Field.{ Sol f69847 } | GPT-6.1-Sol (Luna-tier)`.

Final pilot PID is 2031545. Its Unix socket peer is candidate app-server PID 1965146: pilot socket inode 52056123 connects to app-server FD 11/socket inode 52052998 at the candidate endpoint. The existing first answer and native transcript remain the only model turn.

The one supported registration retry then succeeded:

```
Registered f69847: field_luna_successor (default)
```

`messenger-clj list` reads back `f69847 field_luna_successor default idle`. Stale predecessor `025548` remains separately listed as `STALE`; it was not altered by this repair.
