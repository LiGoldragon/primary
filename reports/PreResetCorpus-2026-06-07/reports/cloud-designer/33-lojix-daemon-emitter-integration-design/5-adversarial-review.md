# 5 — adversarial review of the design draft

Three independent reviewers, distinct lenses. All verified claims against
source. The architecture is sound; the revisions are precision/completeness, not
redesign.

| Lens | Verdict | Core finding |
|---|---|---|
| Property-completeness | needs-revision | All four properties genuinely hosted (verified the deploy cursor lives on `SchemaRuntime`, not `Store`, so a fresh per-request engine over `Arc<Store>` is correct); six precision gaps. |
| Consumer-safety | **sound** | Concurrency is genuinely opt-in; `message`/`spirit`/`repository-ledger` untouched; two gating/scope gaps. |
| Schema/emitter-coherence | needs-revision | Token-discipline + NOTA-dialect + method-only all respected; bounds/variant/typed-invariant gaps. |

## The ten binding revisions (all fold into `6-design.md`)

1. **Two-contract error bounds.** The emitted concurrent hook trait bounds
   `Self::Error: From<SignalFrameError>` against the ONE working contract
   (`daemon_emit.rs:293,382`). The typed meta funnel decodes a SECOND contract
   with a DISTINCT `SignalFrameError` (lojix already carries two arms,
   `OrdinaryFrame`/`MetaFrame`, `lib.rs:46-49`). Import the meta error under a
   distinct ident and extend the bound to `From<MetaSignalFrameError>`.
2. **`ListenerError::OwnerUidMismatch` is a NEW VARIANT.** triad-runtime's
   `ListenerError` is single-variant `Io(#[from] io::Error)` (`daemon.rs:62-66`).
   Fail-closed needs a structured `OwnerUidMismatch { expected, actual }` +
   thiserror arm — a real (additive, source-compatible because matched
   non-exhaustively) stage-1 kernel change, not "just a constructor."
3. **Fail-closed propagation framing corrected.** In the offload model the worker
   runs detached (`dispatch` returns `Ok(())` immediately); its `Result` goes
   nowhere but a local log (lojix `eprintln`s, `daemon.rs:185`). The security
   property is **not executing** — drop the stream before decode/engine. The
   typed error is for the worker's local log only, NOT cross-thread propagation;
   "`DaemonError` absorbs it" overstated a channel that doesn't exist post-offload.
4. **`OriginRoute` minting is currently vacuous.** `SchemaRuntime`'s sema handlers
   underscore-ignore `_origin_route` (`schema_runtime.rs:1419-1433`). So 9v7h is
   satisfied **solely** by the edge reject. Route-minting is cosmetic/forward-
   looking until a future engine change consumes the route.
5. **lojix adoption plumbing undercounted.** lojix's `Error` has no
   `From<ListenerError>`; lojix's `DaemonConfiguration` is a plain rkyv struct,
   NOT an impl of triad-runtime's trait. Stage 4 must add the `ListenerError` arm +
   `From` impl and implement the trait (with the new `owner_user_id` field). Still
   a large net deletion, but the "~40-line impl" undercounts the adoption surface.
6. **Three-valued listener-shape selector, not a widened boolean.**
   `is_multi_listener()` gates SIX emission sites; OR-ing concurrent into the
   boolean collapses three cases into a binary, so the concurrent path would
   inherit the escape-hatch import set + bind body. Model the tier as ONE field
   `meta: Option<MetaTierShape>` where `enum MetaTierShape {
   EscapeHatch(MetaListenerTier), ConcurrentNexus(ConcurrentNexusTier) }` — a
   component structurally cannot declare both, and every site matches the enum.
   (Typed-domain-values: the mutual-exclusion invariant lives in the type, not prose.)
7. **Concurrent × streaming is an emit-time-rejected combination.** The concurrent
   spine replaces `GeneratedDaemonRuntime` wholesale (no long-lived engine), so the
   `EmittedSubscriptions` registry has nowhere to live. lojix/cloud don't stream
   (out of scope now), but make `ConcurrentNexus` mutually exclusive with
   `emits_stream` at emit time, or a future stream adopter silently mis-emits.
8. **`Send + 'static` bounds on the concurrent trait variant.**
   `BoundedWorkers::dispatch` needs `F: FnOnce()+Send+'static`. Add
   `type Engine: Send + 'static` and `Error: … + Send + 'static` on the concurrent
   variant only. lojix satisfies it by luck; without the bound a future non-Send
   component fails in the DOWNSTREAM build (`render` only catches parse failures,
   not trait-bound failures). Add an emission test asserting the bounds.
9. **`WorkingTransport` parameterized for bounds on both paths.** It hardcodes
   `LengthPrefixedCodec::default()` (4 GiB) and never sets a read timeout. To host
   R1/R2 it gains max-body + read_timeout fields constructed in `bind`; absent →
   emit `::default()` + no timeout verbatim (byte-stable). The serial
   `with_frame_bounds` must actually apply `set_read_timeout` (or narrow it to
   R1-only and stop claiming R2 on the serial path).
10. **Bind-time assertion for `PeerCredential` + `None` uid.** Promote from "risk
    candidate" to design: when the shape declares `OwnerAuthority::PeerCredential`,
    `DaemonBinder::bind` returns a typed configuration error if
    `owner_user_id()` is `None` — fail-closed at bind, before serving. Prevents a
    silent fail-open that would defeat 9v7h.

## What the reviewers confirmed (the design's load-bearing claims hold)

- Property 1 genuinely hosted: the deploy cursor is on `SchemaRuntime`
  (`schema_runtime.rs:32-33`), not `Store` (`Mutex<StoreState>`), so a fresh
  per-request engine over `store.clone()` isolates in-flight state while sharing
  durable tables — exactly `BoundedWorkers` offload. `Store` is `Send+Sync`,
  `SchemaRuntime` is auto-`Send`.
- Option B is genuinely the minimal runtime change: the `MultiListenerDaemon`
  shell + both `handle_stream(&mut self)` signatures stay byte-identical; the
  `owner_user_id()->Option<u32>{None}` accessor follows the established
  defaulted-`None` pattern. Option A (forcing `Arc<Self>+Sync` into the shell) is
  correctly rejected — it would break `message`'s actor `&mut self`.
- `cloud` is structurally `lojix` minus the `BoundedWorkers` offload (identical
  funnel, bounds, per-request engine; serial only because it runs `serve_*`
  inline) — proving `ConcurrentNexusTier` is a shared cloud/lojix shape, not
  lojix-private.
- `message` (default trait, `Mutex<MessageEngine>`, `&mut self`), `spirit`
  (`with_meta_tier` escape hatch + streaming), and `repository-ledger` (raw
  listener, no emitter/runtime dep) all regenerate byte-identically / are outside
  the blast radius.
- Token-discipline, NOTA positional+typed records, and method-only (the
  `GeneratedRequestWorker<Daemon>` `PhantomData<fn()->Daemon>` is a legitimate
  type-binder, same as `DaemonCommand`) are all respected.
