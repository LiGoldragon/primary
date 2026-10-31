# Client compatibility: diagnosis and bounded alignment dependency

## Coffee-short account
The shell still selected Flow 0.40.0 after NEXT became 0.42.1. Some replies still decode; others fail, and old Send reply layouts can misread the new public projection. The same harmless requests fail in the old client and succeed in the matching client. Exact NEXT clients work now by full path; durable Home alignment remains a proposal, not a landed fix. Code removed/added: **0/0**. No activation occurred.

## Witness
Raw captures: `/home/li/witnesses/24eb5c-heartbeat-client/*.json`. Each includes UTC timestamp, executable, request, endpoint, status, raw stdout/stderr.

At 2026-10-31T04:51:26Z, old executable resolves to `/nix/store/nygs0aj2rb0caz6bdfjqm89h3qm1imm4-flow-0.40.0/bin/flow`; `--version` prints `flow 0.40.0`. Matching `/nix/store/79pwswrvy664x2aflh3wnawscky9chsz-flow-0.42.1/bin/flow` prints `flow 0.42.1`.

Against the SAME `/run/user/1001/flow-042-next/flow.sock`:

| Request | Old client | Matched client |
|---|---|---|
| `Current.{ Field flow Secondary }` | exit 0, `Current.Awake.24eb5c`, empty stderr | identical |
| `Metaflows` | exit 2, empty stdout, rancor diagnostic | exit 0, `Listed.[ … ]`, empty stderr |

Against the SAME `/run/user/1001/flow-042-next/flow-meta.sock`, old `flow-meta Configuration` exits 2 with empty stdout/rancor diagnostic; matched client exits 0 with `Configuration.{ … }` and empty stderr. Endpoint overrides were per-command only. No mutating Send probe was repeated.

Exact error: `failed without error information; enable debug assertions and the `alloc` feature in rancor for error information`.

## Cause and immutable contract evidence
NEXT source: `/home/li/primary/flow` Git object **d3ab87ee18b1dd30947d5f0089f5abb4bafa80d5**, not the older `repos/flow` checkout and not the rejected `repos/flow-nexus` tree. Its Cargo.lock pins signal-flow **7b737d903e93015e5b6b6baabd3126009707a1ef** (38.0.0), meta-signal-flow **dba1e407c314dc4b8552e7d9abad1eddd2ea836b** (47.0.0).

Release source **122defe** for 0.40.0 pins signal-flow **3b3e323cdeafe28696b1345f5d12026dcc93addd** (32.0.0), meta-signal-flow **457da255aad8c1e2ee547f5271766afa9ab26836** (40.0.0). This is a release-source comparison; the exact installed old package derivation/source identity has not been recovered.

* Flow 122defe `crates/flow/src/main.rs:74–103`: request is written before `rkyv::from_bytes::<Response>` validates the reply. A decoding failure is not evidence that a requested effect failed.
* signal-flow 7b737d9 `src/generated/signal.rs:1126–1129`: public SendAccepted now holds cursor and visible state; old payload additionally held LogicalDeliveryId. New `VisibleSendReceipt` is NativeReceipt alone (`:1106`), while old SendReceipt included LogicalDeliveryId. Response also gained SendRefused before Sent. Flow d3ab87 `message_projection.rs:78–92` performs these exact public projections. Thus an old decoder expects the wrong discriminant/payload layout for new Send replies. Validation may reject or may accept unrelated bytes as an old field: a successful old decode is not trustworthy compatibility.
* meta-signal-flow dba1e407 `src/generated/signal.rs:158–170` adds default_minutes and counters to ConfigurationSnapshot, alongside other contract changes. Metaflows contains QueueEntry/Request; Flow d3ab87 `flow-ethos/ethos/library.ethos:23–42` replaces Result.String with typed ResultPayload and adds Task/Done. These are concrete incompatible schema changes, not a claim of one isolated byte causing every validation failure.

Original Send evidence: `/home/li/.claude/projects/-home-li-primary/7751c3e2-9fb3-5639-b6bf-15000f7c5519.jsonl:414–424`: old abrupt sends return the same rancor error; matching client returns `Sent.{ Codex … … }`. Earlier garbled D/K delivery-id values are relayed observations, not independently re-decoded archives. Exact raw binary replies were not retained, so their byte-by-byte interpretation remains unproved. No inference that the old failed sends were undelivered; do not retry them merely because the client failed to decode.

The opaque rancor diagnostic is a separate observability defect; no diagnostic-code repair is proposed in this bounded alignment change. Bare Result.String rejection on 0.42 is a distinct input-schema change, not this reply-decoding defect.

## Durable alignment boundary
Canonical CriomOS-home **437455a4a5a0b47d71b23c6f37b3188f250dcb0d**: `modules/home/profiles/min/flow.nix:12` selects inputs.flow; `:69` installs deployment. `packages/flow-deployment/default.nix:9` takes the same input and its final output links flow, flow-meta, flow-nexus and flow-hook together. Bumping that shared input changes more than clients.

Field core Secondary reports prior separate owner `/root/prometheus_diagnosis` absent; its pushed declaration checkpoint is **ee0d02af6c16af3942e60c7b00a288686713a932**, separate worktree `/home/li/worktrees/criomos-home-flow-pair-c2b552`. Canonical Home and that worktree contain foreign dirty work, left untouched.

Primary authorized Field core Secondary one read-only alignment proposal at canonical437455a4, targeting d3ab87 clients without runtime/service/socket/Memory changes. Its source hand is inspecting consumer effects. Await its precise proposal/Primary judgment. Full-path matched clients are the witnessed operational workaround, **not** a persisted PATH repair. Before/after runtime source is unchanged d3ab87; owned code lines removed/added **0/0**. Existing Home activation/tracker holds remain.

## Current alignment disposition
The earlier client-only hold is superseded. Mind flow Secondary and Field core Secondary relay direct PsychePrimary→FieldPrimary authorization for ONE combined Home inputs.flow0.42.1 + Wispr.12 change/activation through the SAME eligible Home worker, preserving actual runtime unit, Memory, sockets, seats and queues. That Home owner is the sole alignment lane; this heartbeat seat creates no duplicate client implementation. Actual closure still awaits activation/PATH/Send witnesses. The exact full-path matched-client bypass remains a witnessed workaround, not proof that Home alignment has landed.
