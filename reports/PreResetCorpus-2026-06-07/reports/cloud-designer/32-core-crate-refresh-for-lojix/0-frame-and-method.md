# 32 — core-crate refresh, contextualized for the new lojix stack

cloud-designer lane, 2026-06-06. Psyche order: *"look into the latest
development with the core crates. refresh intent. contextualize for new lojix
stack."* This is a working order (look-into / refresh / contextualize), not
durable intent — no Spirit capture.

This is a meta-report directory (sub-agent session). The frame + method are
here; each surveyed crate cluster has a numbered report; the synthesis is the
highest-numbered file (`7-overview.md`).

## Why now

The new lojix stack (`lojix/triad-port`, `signal-lojix/triad-port`,
`meta-signal-lojix/triad-port`) was brought online M1 (engine eval+build of the
`dune` fixture, live two-socket daemon round-trip, concurrent serving via
`triad_runtime::BoundedWorkers`) — reports 26-31. It was built against a
snapshot of the core crates. Since then the core crates moved forward. A drift
scan of lojix's pins vs each crate's `main` HEAD shows lojix is behind on the
crates that *generate its own code* and *host its runtime*:

| Core crate | lojix pins | `main` HEAD | Behind by |
|---|---|---|---|
| `schema-rust-next` (build emitter) | `c0a331a` | `6685e7b` | the whole daemon-emitter arc: `triad_main` emitter (`33337d7`), ConnectionContext hook (`6685e7b`), frame-codec-for-wire-contracts (`799f678`), GAP-1 string→token migration (`4ac90de`), Plane namespace family |
| `triad-runtime` (runtime kernel) | `fdfd1831` | `33b9531` | ConnectionContext peer-creds (`33b9531`), daemon-emit: DaemonConfiguration + ExitReport + triad_main (`1bd383b`), doc reconciliation (`08b624a`) |
| `nota-next` | `fb600e3` | `f0e435a` | `#[shape(keyword=…)]` derive (`f0e435a`), at-binder removal (`d996a30`) |
| `nota-codec` | `f761421` | `f761421` | at HEAD |
| `nota-config` | `bd9173a` | `bd9173a` | at HEAD |

The headline before any deep read: **the core stack now emits and supports a
GENERATED daemon** (`triad_main` + `ConnectionContext` + `DaemonConfiguration` +
`ExitReport` + emitted frame codec + `handle_working_input` hook). The lojix
stack hand-wrote all of that (`daemon.rs`, `DaemonConfiguration`, the two-socket
wiring, the per-request engine plumbing). The central question this session
answers: **how much of lojix's hand-written runtime is now the emitter's job,
and what must lojix re-align to adopt the generated path?**

## Method

Six survey agents run in parallel, one per crate cluster, each reading recent
commits + `ARCHITECTURE.md` + `INTENT.md` + key source, extracting (a) what's
new since lojix's baseline, (b) how it bears on the new lojix stack, (c)
concrete port/adopt/align recommendations with effort. A seventh perspective —
the lojix-stack-state agent — characterizes what lojix hand-wrote vs what the
latest emitter would generate. The orchestrator synthesizes `7-overview.md`.

- `1-triad-runtime.md` — runtime kernel: ConnectionContext, daemon-emit, triad_main, the daemon ownership boundary.
- `2-schema-rust-next.md` — the Rust emitter: what it now generates for a component daemon, the handle_working_input hook, GAP-1 token migration, Plane.
- `3-schema-next.md` — schema engine: Asschema-retired, Assembled→MacroExpansion, stream lifecycle metadata, direct stream lowering.
- `4-nota-next-and-codec.md` — NOTA codec: `#[shape(keyword)]`, at-binder removal, quoted-string rejection, block strings.
- `5-sema-and-signal-frame.md` — storage + wire: sema-engine identified mutation/record families, signal-frame schema codec arc; whether lojix's hand-written Store has a path onto sema-engine.
- `6-lojix-stack-state.md` — current lojix triad-port: hand-written vs generatable surface, and what re-emitting under the latest emitter would change.
