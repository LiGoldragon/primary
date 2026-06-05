# 7 — Adversarial verification of the three port maps

Each component map (reports 4/5/6) was re-checked against source by an independent
skeptic instructed to default to refuted/uncertain. All three verdicts:
**accurate to source, SOUND, correctly sequenced.** No port plan was refuted; two
*blockers* were downgraded (the base is more ready than the maps claimed), and one
new gap was caught. Details below.

## Verdicts at a glance

| Component | Accurate? | Verdict | The sharpest finding |
|---|---|---|---|
| message | yes | SOUND | The live Rust contract carries forbidden Sema words even though the concept schema looks clean; message+router must ship as ONE delivery-spine unit |
| router | yes | SOUND | Two blockers overstated (downgraded); the real risk is an *unexercised emitter path*, not a missing API |
| orchestrate | yes | SOUND | New gap: config ingestion still parses NOTA text at startup (violates 7x50), so bootstrap work is broader than "add a policy seed" |

## Confirmed (load-bearing facts the skeptics re-verified in source)

- **All three are entirely pre-triad.** Zero `triad-runtime` / `schema-rust-next` /
  `schema-next` deps in any of the three `Cargo.toml`s (empty grep, all three). No
  plane schemas, no engine-trait impls anywhere. Verbatim confirmation of every
  daemon-shape claim (message's 584-line Kameo `daemon.rs`; router's six child
  actors + raw `UnixListener` + dual-mode `main.rs`; orchestrate's `std::thread` +
  free-function daemon over the `signal-executor`/`block_on` stack).
- **message's catch is real.** `signal-message`'s `signal_channel!` block tags
  `Assert MessageSubmission` / `Assert StampedMessageSubmission` / `Match InboxQuery`
  — forbidden Sema words on the live wire (R24/`7l7l`), masked by a clean-looking
  `.concept.schema`. This *corrects* report 1's "message is cleaner on R24."
- **orchestrate's state-plane alignment is real** — it already runs one
  `orchestrate.sema` through `sema-engine` exclusively (no raw redb), satisfies the
  single-NOTA-argv + one-peer-CLI rules, and validates `ShortHeader` cross-socket.
  Its engine-trait runtime + three-plane schemas + meta rename are the work.

## Downgraded blockers (the base is MORE ready than the maps said)

1. **`ox7e` "sema-engine can't express router's storage identity" — DOWNGRADED.**
   `sema-engine` already exposes BOTH `register_table` (plain keyed) AND
   `register_identified_table` (auto-counter), each callable multiple times. Router's
   append-log delivery tables and the triple index map onto these directly. The real,
   narrower risk: there is **no worked example of a multi-table or plain-keyed
   `SemaEngine`** (spirit's `store.rs` calls `register_identified_table` exactly once),
   and **it is unproven that the `SemaRuntime` *emitter* generates `register_table`
   calls** at all. So the risk is an *unexercised emitter path + no reference impl*,
   not a missing engine API. Verify the emitter targets plain keyed tables before
   assuming router's seven-table store emits cleanly.

2. **Payload-less dual-lowering (`primary-vllc`) — DOWNGRADED to low-risk, both
   router and orchestrate.** The `schema-rust-next` emitter source positively handles
   `None`-payload variants in every codegen path the skeptics read (`emit_route_impl`,
   `emit_signal_frame_impl` route/short-header, the variant-token emitter, and the
   constructor emitter correctly *skips* payload-less variants). spirit's own
   checked-in `sema.rs`/`signal.schema` carry fully payload-less enums (`Kind`,
   `Magnitude`, the unit `WriteInput`/`ReadInput` variants) that emit and compile
   green. There is **no evidence of a dual-lowering defect anywhere in the base
   repos** (empty grep for `vllc`/`dual-lower`/`payload-less`). Net: the generic case
   is *proven*; a porter should still confirm each component's own enums emit, but it
   does NOT gate schema authoring. (Report 3 said "NOT GROUNDED"; the verifiers go
   further — the emitter affirmatively handles it.)

## New gap caught (not in any map)

- **orchestrate's daemon-config ingestion still parses NOTA TEXT at startup**
  (`read_to_string` + `nota_codec` Decoder in `main.rs`), whereas the `7x50`
  discipline — and spirit's daemon — consumes a *pre-encoded rkyv binary artifact*.
  So the bootstrap work is broader than "add a `bootstrap-policy.nota` seed": the
  config-ingestion path itself must move to the signal-file/rkyv argument shape. (A
  parallel concern exists for router's `RouterBootstrap::from_nota_lines`, which map 5
  already flagged.)

## Sequencing the verifiers stressed

- **The meta-signal rename (`r9qy`) gates everything with a meta tier, and is
  COUPLED across router + orchestrate** — one fleet rename covers both
  `meta-signal-router` and `meta-signal-orchestrate`. Router's Steps B–G cannot
  *start* until the rename lands (its in-daemon `signal.schema` imports
  `meta-signal-router:signal:Input`); orchestrate's *in-daemon planes + ordinary
  contract* do NOT wait on it, only its meta-tier slice does. The rename is
  **mechanical, not first-of-kind**: `meta-signal-cloud` / `meta-signal-domain-criome`
  / `meta-signal-upgrade` already exist on disk.
- **message + router are ONE delivery-spine unit.** "message ported" is not a
  self-contained deliverable — its load-bearing witness (the live message→router
  delivery round-trip, report 74's #1 gap) cannot go green until router's receive
  side is co-ported. persona today asserts delivery by NAME ONLY
  (`MESSAGE_ROUTER_COMPONENTS` is just an enum pair).
- **Two patterns are genuinely first-of-kind** (budget as pattern-establishing, not
  copy-from-spirit): the first real `MultiListenerDaemon` consumer (spirit is
  single-listener) and the first bootstrap-once pre-encoded-policy artifact.

## Citation drift (minor, noted for accuracy)

The base moved during the run: router `@` is now `c87732c8` (empty working copy on
`570aaab6`, the content commit the map cites — correct); `triad-runtime` `@` is now
`054bd702` (MultiListenerDaemon + 2 witness tests still present, claim holds);
`schema-rust-next` `@` is `6e58ed4` on `c0a331a`. The cited content states are
correct; only the working-copy hashes advanced.
