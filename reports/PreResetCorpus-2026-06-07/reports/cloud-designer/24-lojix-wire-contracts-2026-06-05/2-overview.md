# Phase 1 overview — the two lojix wire contracts (GREEN)

Cloud-designer orchestrator synthesis. 2026-06-05. Phase 1 of the lojix triad
port: author + review the two wire contracts. Outcome: **GREEN** after the
review's two additive blockers were fixed.

## What landed (in `drafts/`)

- `signal-lojix.lib.schema` — the ordinary contract. Input root
  `[Query WatchDeployments WatchCacheRetention Unwatch CheckHostKeyMaterial]`;
  matching reply/rejection roots; defines the shared record types ONCE
  (DeploymentIdentifier, Generation/GenerationListing, the two event payloads,
  ProposalSource, FlakeReference, DatabaseMarker, the typed rejection reasons).
- `meta-signal-lojix.lib.schema` — the owner-only policy contract.
  `[Deploy Pin Unpin Retire]` + typed replies; cross-imports the shared types
  from `signal-lojix:lib:TypeName` rather than redefining them.
- `signal-lojix.ARCHITECTURE.md` — re-targeted: the stale three-layer /
  signal_channel! model deleted, replaced by the schema-derived per-plane
  triad + two-contract split + streaming-day-one + a Migration-history note +
  the local-builds-permitted note.

The review (`1-review.md`) verified NOTA legality against the **live**
schema-next parser (`declarative.rs:1616-1646`), the two-contract authority
split, born-`meta-signal-`, the cross-import path form against real precedents,
and cloud-template shape fidelity.

## Fixes applied after review (YELLOW → GREEN)

- **GAP 1** — the request side now carries the full
  `SystemAction [Eval Build Boot Switch Test BootOnce]` (was the narrowed
  4-variant `ActivationKind`), so eval-only and build-only deploys are
  expressible. `ActivationKind` is retained only on the `Generation`
  (live-set) record, which by definition is something activated.
- **GAP 2** — `CheckHostKeyMaterial` added to the ordinary contract as a fifth
  read verb, with the `KeyMaterial*` records salvaged 1:1 from `check.rs`.
- `ProposalSource` / `FlakeReference` moved to the ordinary contract as
  shared types (needed by both legs once CheckHostKeyMaterial landed); meta
  now cross-imports them — single-definition preserved.
- Trimmed the 64-line schema header to the decision + a pointer; stripped the
  `</content>`/`</invoke>` paste artifacts from the ARCHITECTURE draft.

Full generation-validation (parse + emit through schema-next →
schema-rust-next) happens in Phase 2 when `build.rs` wires the package context
that resolves the cross-imports; the record/enum forms here are parser-verified
and form-identical to the cloud template.

## The load-bearing finding — streaming is not schema-emittable today

The probe was decisive: the schema-derived stack (schema-next +
schema-rust-next) that the cloud triad actually ships has **no streaming
construct at all** — exactly two roots (Input/Output) + a namespace, no
event/stream root, no `opens`/`belongs` relation. Stream support exists only in
the OLD hand-written `signal_channel!` macro path, which the triad is moving
away from. The cloud port never needed streams; lojix is genuinely the first.

Per decision `2tfa` ("if the generator cannot yet emit streams, that
enhancement is on the lojix path rather than dropping streaming from the
contract"), Phase 1 took **Option A**: the Watch/Unwatch subscription handshake
is authored in the emittable form (ordinary request → SubscriptionToken reply)
and the two event payloads are defined once as namespace records — so the
streaming vocabulary stays in the contract and nothing is lost. The
daemon-pushed event *frame* (the actual push of `DeploymentPhaseEvent` items)
becomes a tracked schema-next + schema-rust-next enhancement on the lojix path:

- **schema-next grammar:** a fourth optional positional root (an event/stream
  root enum) + per-variant `opens`/`belongs` relation annotations, lifting the
  old `signal_channel!` event/stream grammar into the SchemaSource model.
- **schema-rust-next emitter:** a `RustEmissionTarget::WireContract` path that,
  when the event root is present, emits the event enum, a StreamingFrame body,
  the stream-relation witnesses, and the event NOTA + signal-frame codec
  (the `emit_mail_event_support` machinery currently gated off for
  WireContract).

This is authorized: record `6wzz3up583b428kh3ok` explicitly permits modifying
schema-next when the port demands it. The provisional post-grammar event-root
shape is recorded at `signal-lojix.lib.schema` head + ARCHITECTURE §4 as the
target for that work.

## Next

1. **Place** the GREEN schemas onto `next` branches: `signal-lojix` (its own
   repo) gets `schema/lib.schema` + the re-targeted `ARCHITECTURE.md`;
   `meta-signal-lojix` lands as a path-dep package (decision
   `11yimmwp4pueiudhl30`) carried in the lojix tree until cutover.
2. **Phase 2** — the daemon plane schemas (`lojix/schema/nexus.schema` with the
   deploy-pipeline Effect vocabulary incl. a local-build effect — the
   hallucinated local-build guard `783n` is dropped here; `lojix/schema/sema.schema`
   with the four tables), `build.rs` per the cloud template, and porting the
   `schema-deep-iteration-2` prototype's domain logic into the generated engine
   impls (collapsing the 9-actor topology into three engines + effect handlers +
   one container-observer actor).
3. **The streaming-emission enhancement** runs as a parallel schema-next /
   schema-rust-next work item; the daemon can be built against the handshake
   contract and wired to push events once the event root lands.
