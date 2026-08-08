# 7 — overview: what the core-crate refresh means for the new lojix stack

cloud-designer synthesis of the six surveys (1-6). 2026-06-06.

## The one-sentence story

While lojix was being brought online M1, **the core stack grew the ability to
EMIT the whole daemon lojix hand-wrote** — `triad_main` / `ComponentDaemon` /
`GeneratedDaemonRuntime` / `DaemonEntry`, with `ConnectionContext` peer-creds
threaded into a `handle_working_input` hook, a `DaemonConfiguration` trait, and
an `ExitReport` process tail — but the emitted daemon is **serial and models the
two authority tiers asymmetrically**, so adopting it as-is would *regress*
lojix's three load-bearing M1 choices. The refresh therefore splits cleanly into
**safe wins to take now**, a **peer-cred hardening that needs one policy
decision**, and an **emitter-alignment track that is feed-back-then-adopt, not
adopt-now**.

## The twist: the emitted daemon is real, but it is a downgrade if taken blind

`schema-rust-next` HEAD (`6685e7b`) ships `daemon_emit.rs` (~980 lines) that
emits a complete daemon: hook trait, argv parsing, single/multi-listener bind
with `ListenerTier{Working,Meta}` (the structural twin of lojix's
`ListenerRole{Ordinary,Owner}`), a decode→execute→encode spine, `DaemonError`,
and `DaemonEntry::run_to_exit_code`. It overlaps ~90% of lojix's hand-written
`daemon.rs`. But three lojix properties the emitted spine does **not** host:

1. **Concurrency (the M1 headline).** The emitted `handle_working_stream` runs
   work **synchronously inline** in the accept loop. lojix offloads each request
   onto `triad_runtime::BoundedWorkers` so a multi-minute `nix` build never
   blocks queries or the other socket — the proven "~4 ms query answered while a
   deploy ran" win (intent `2alg`/`k6w1`, audit reports 30-31). Adopting the
   emitted daemon today makes lojix serial again.
2. **Two typed wire contracts into one Nexus root.** lojix funnels BOTH
   `signal-lojix` and `meta-signal-lojix` into ONE `nexus::SignalInput`
   (`OrdinaryInput`/`MetaInput`) through a single `SchemaRuntime::execute`
   runner. The emitter drives the *working* tier as one contract and treats the
   *meta* tier as a raw `handle_meta_stream` **escape hatch** — demoting lojix's
   first-class typed owner path.
3. **Per-request engine over a shared store.** lojix builds a fresh
   `SchemaRuntime` per request over `Arc<Store>` (so the in-flight deploy cursor
   `active_deploy`/`active_operation` is never shared); the emitted runtime holds
   one long-lived `&Engine`.

**Conclusion:** lojix's hand-written `daemon.rs` is not legacy to delete — it is
the **reference implementation of three properties the emitter must grow** before
any concurrent daemon can adopt it. The correct move is feed-back-then-adopt.

## What is safe to take now (low risk, no generated-code shape change)

| Action | Why | Effort | Risk |
|---|---|---|---|
| Bump `triad-runtime` `fdfd1831`→`33b9531` | Purely additive: `ConnectionContext` + `DaemonConfiguration` trait + `ExitReport`. Everything lojix already consumes (`daemon.rs`/`workers.rs`/`runner.rs`/`frame.rs`/`argument.rs`) is **byte-identical** to lojix's pin; only new transitive dep is `rustix` (no-default, std+net), `forbid(unsafe_code)` kept. | small | very low |
| Bump `nota-next` `fb600e3`→`f0e435a` (lockfile only) | Keeps lojix aligned with what the emitter builds against. The two commits are a dead-code parser removal (at-binder, which lojix never used — zero `@` in its schemas) and a `#[shape(keyword)]` derive addition lojix doesn't reference (lojix uses only `NotaDecode`/`NotaEncode` value-codecs). | small | near-zero |

Neither changes lojix's checked-in `src/schema/*.rs`. They are alignment, not
behavior.

## What needs ONE decision before it can land

**Close audit R3 — owner-socket peer-credential auth via `ConnectionContext`.**
Today lojix authorizes the privileged owner tier (Deploy/Pin/Unpin/Retire)
**purely by socket file mode** (`validate_owner_socket_mode`, `daemon.rs:99`) —
there is no peer check. `triad-runtime`'s new `ConnectionContext::from_stream`
(`SO_PEERCRED` uid/gid/pid, no unsafe) is the hosted primitive that closes it,
and lojix already has the exact seam: the hardcoded `OriginRoute(0)`
(`daemon.rs:222`) already threads through the engine's
`apply_sema_write`/`observe_sema_read`. Wiring is small — read peer creds on the
owner socket, mint a real `OriginRoute`. **Blocked on a policy the survey cannot
infer (PSYCHE DECISION):**

- *Which uid(s) count as owner* for the meta tier?
- *On a peer-credential mismatch, REJECT the connection, or TAG a non-owner
  `OriginRoute` and let the engine refuse the privileged verbs?*

This is defense-in-depth on top of (not instead of) the file-mode guard.

## The emitter-alignment track (feed-back, then adopt — sequence carefully)

**Prerequisite, mechanical but mandatory if bumping the emitter:** bump
`schema-rust-next` `c0a331a`→**HEAD `6685e7b` directly** — NEVER stop in the
`7f59b39..799f678` window (the `gb95` over-reach there strips the frame codec
from the contracts and breaks `*_signal_frame` calls; `799f678` fixes it). Both
contracts (`ec0678c`) re-emit too. Re-run with the `*_UPDATE_SCHEMA_ARTIFACTS`
env; expect **~100+ lines of formatting churn per generated file** from GAP-1
tokenization — verified semantically identical (pure `prettyplease`
canonicalization, no type/route/logic change). The build's freshness check is
red until artifacts are refreshed and re-checked-in.

**Then the daemon-adoption decision (PSYCHE DECISION).** Feed lojix's three
properties back into the emitter as designer requirements:

1. a **concurrent-spine option** (offload `handle_working_input` onto
   `BoundedWorkers`, fresh per-request engine over `Arc<Store>`),
2. a **two-wire-contract single-Nexus-root** working tier (so the owner tier is
   a first-class typed engine path, not an escape hatch),
3. preservation of the **R1/R2 hardening** (8 MiB max-frame, 10 s read-timeout)
   in the generated `WorkingTransport`.

Until those land in the emitter, lojix keeps its hand-written daemon and adopts
only the shape-compatible pieces (`DaemonConfiguration` trait alignment,
`ConnectionContext`, `DaemonError`/`DaemonEntry` vocabulary).

## Deferred-but-tracked (named follow-ons, not refresh gaps)

- **Streaming push frames.** `schema-next` now has the `Stream { token opened
  event close }` + `opens`/`belongs` construct (`c2b3546`/`30a88be`) that
  `signal-lojix/lib.schema:11-20` documents as *missing* — that comment is now
  **obsolete and factually false**. lojix fakes streaming as request/reply
  (`Watch*`→`SubscriptionToken`); its event payloads are already pre-shaped as
  the stream legs. Real adoption is a large four-crate effort
  (`schema-next` + `schema-rust-next` `EmittedSubscriptions` + `triad-runtime`
  streaming + `signal-frame`) on the **fastest-moving surface in the stack** —
  hold until it stabilizes; the per-request `SchemaRuntime` would also need to
  start holding the subscription registry across requests.
- **`sema-engine` storage port.** `sema-engine` HEAD has identified record
  families + identified mutation (`817236a`/`e1aeef1`) that match the shape of
  lojix's in-memory tables. But it is **premature**: M1 needs no persistence, and
  `sema-engine`'s read-plan execution does not yet cover the multi-field equality
  `gc_roots` needs (`generation_identifier`+`cluster_name`+`node_name`+`label`),
  so a port today recreates lojix's linear-scan logic plus an rkyv+redb cost. Gate
  on a real cross-restart-persistence requirement.

## Cross-repo flags surfaced (not lojix code — for the owning lanes)

- **`triad-runtime` doc is stale:** its INTENT.md/ARCHITECTURE.md say `triad_main!`
  is "NOT YET BUILT" — false; `schema-rust-next` HEAD emits the equivalent.
- **`nota-codec` INTENT.md is stale:** still describes the legacy-quote decode
  path that `f761421` deleted.
- **`signal-frame` is a declared-but-unused dep** in both lojix contracts
  (`signal-lojix`/`meta-signal-lojix` Cargo.toml) — zero non-comment uses;
  vestigial, candidate for removal.
- **Wire-framing duplication:** `schema-rust-next` and `signal-frame` each
  implement a *different* length-prefixed framer; reconciling to one is a
  decision above lojix as a downstream consumer.
- **Short-header tier collision (audit R7):** meta `Deploy` == ordinary `Query`
  == `0x0` — a contract-side wart worth carrying into the emitter bump.

## Drift-baseline correction

The frame's drift table did not list a `schema-next` pin; survey 3 found lojix
actually pins `schema-next` at `5311f9a`, so three commits the brief flagged
(`a2123f8`, `5311f9a`, `6a12bcc`) are **already in lojix's pin** and not new for
it. The new-for-lojix `schema-next` work is the stream-lifecycle construct
(`c2b3546`/`30a88be`) plus the `MacroExpansion` rename + variant-derive
(`77e71a4`, which forces the `nota-next` bump). Stream-free re-emission is
byte-identical.

## Recommended staging

1. **Now (safe):** bump `triad-runtime`→`33b9531` and `nota-next`→`f0e435a`.
   No generated-code change; pure alignment.
2. **On owner-uid policy decision:** wire `ConnectionContext` on the owner
   socket; close audit R3.
3. **On emitter-adoption decision:** linear bump `schema-rust-next`→HEAD +
   both contracts, re-emit + verify formatting-only churn; align
   `DaemonConfiguration` to the trait; then feed the three properties back into
   the emitter before retiring any hand-written daemon code.
4. **Deferred-tracked:** streaming (after the 4-crate surface stabilizes),
   `sema-engine` storage (on a persistence requirement).
5. **Doc hygiene (other lanes / opportunistic):** correct the obsolete
   streaming comment in `signal-lojix/lib.schema`; the `triad-runtime` and
   `nota-codec` stale-doc flags; consider dropping the vestigial `signal-frame`
   dep.
