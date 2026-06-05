# Operator Report 323 — Spirit streaming, meta slot, and stack readiness

Date: 2026-06-05
Role: operator

## Scope

This report covers the operator-side implementation after the intent refresh
around Spirit streaming subscriptions, the required meta slot, and the
schema-rust-next runtime token migration.

The implementation work landed on code-repo `main` branches. Primary report
state lands here so future agents can reconstruct what was actually pushed and
what remains open.

## Landed code

### Spirit streaming pilot

Spirit `main` now carries commit `186d97b1`:

`spirit: add intent subscription streaming pilot`

That commit adds the first working subscription path:

- `schema/signal.schema` adds `SubscribeIntent(Query)` as an input that opens
  `IntentEventStream`.
- `schema/signal.schema` adds `SubscriptionStarted(IntentSubscription)` and
  `Event(IntentEvent)` outputs.
- `schema/nexus.schema` adds the internal visible feature operation:
  `OpenIntentSubscription(Query)` and `IntentSubscriptionOpened`.
- `src/subscription.rs` owns Spirit's component-specific subscription hub:
  filter matching, retained socket writers, and typed event delivery.
- `src/nexus.rs` mints subscription tokens through
  `triad_runtime::SubscriptionTokenIssuer`; the daemon does not mint hidden
  subscription identity.
- `src/daemon.rs` registers a subscriber after writing the ordinary
  `SubscriptionStarted` reply, then returns to the accept loop so the daemon is
  not blocked by a live subscription client.
- `src/bin/spirit.rs` keeps the one-argument CLI rule: the CLI sends one NOTA
  input, prints the ordinary output, and only for `SubscribeIntent` continues
  reading pushed subscription-event frames.

The process-boundary witness is:

`tests/process_boundary.rs::cli_subscription_receives_matching_intent_events_without_blocking_daemon`

It starts the daemon, starts a subscriber CLI, records a nonmatching intent that
does not push to the subscriber, then records a matching intent and asserts that
the subscriber receives `Output::Event(IntentRecorded(...))` with the same
`SemaReceipt` returned by the ordinary recording client.

### Meta slot

Spirit `Configuration` now carries:

`meta_socket_path: Option<ConfigurationPath>`

The current slice does not bind a meta listener and does not author a
meta-signal surface yet. It reserves the typed binary configuration slot so the
daemon has a structural home for component policy/configuration authority.

The witness is:

`tests/daemon_command.rs::daemon_configuration_carries_optional_meta_socket_slot`

### Stack alignment and Nix repair

Spirit `main` also now carries:

- `44ded6ff` — `spirit: align nix schema stack pins`
- `ed9bafa7` — `spirit: align cargo runtime pin`

The Nix build initially failed usefully four times:

- First, the configured binary cache/remote path
  `nix.prometheus.goldragon.criome` timed out and Nix disabled it.
- Then, the Spirit flake still pinned `triad-runtime-source` before the
  `signal-frame` dependency existed, so the vendoring patch expected a line
  that did not exist.
- Then, after the runtime/schema pins moved, the root `signal-frame` dependency
  that Spirit now owns was not rewritten to the vendored path, causing Cargo to
  attempt a GitHub fetch inside the sandbox.
- Then, `schema-next` expected `nota-next` structural macro types while the
  flake still pinned an older `nota-next`.

The fixes were:

- Update `flake.lock` for `nota-next-source`, `schema-next-source`,
  `schema-rust-next-source`, and `triad-runtime-source`.
- Add the missing root `signal-frame` vendoring rewrite in `flake.nix`.
- Update `Cargo.lock` to the same `triad-runtime` commit that Nix now builds.

Final Nix verification passed with the custom remote builder/cache bypassed:

`timeout 180s nix build .#default -L --option builders "" --option substituters "https://cache.nixos.org"`

### Schema-rust-next token migration

Schema-rust-next `main` currently carries these relevant commits:

- `fd84aae` — trace object emission tokenized.
- `fa0d4fa` — Nexus runner emission tokenized.
- `e332b5e` — engine trait emission tokenized.

The Spirit artifacts were regenerated against `schema-rust-next` `e332b5e`,
and Spirit builds against that generator.

Honest status: this is not a full string-emitter removal. A fresh count after
these commits still found hundreds of `format!` / `self.line` / `push_str` /
`write!` occurrences in `schema-rust-next/src/lib.rs`. Some are not codegen
debt, but the count is high enough that the runtime emitter cannot be called
fully migrated yet. Worker subagent `Lagrange` is currently assigned to a
non-overlapping follow-up slice in `schema-rust-next`.

## Verification

Spirit local verification after the streaming and alignment work:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo test` — passed after the generator
  update and schema regeneration.
- `cargo test --all-features` — passed after the final public-surface cleanup
  and again after aligning `Cargo.lock`.
- `cargo clippy --all-targets --all-features -- -D warnings` — passed after
  the final public-surface cleanup and again after aligning `Cargo.lock`.
- `nix build .#default -L --option builders "" --option substituters
  "https://cache.nixos.org"` with a `timeout` guard — passed after flake and
  Cargo pins were aligned.

Schema-rust-next verification for the token slices already on main:

- The pushed generator commits were tested by the implementers with `cargo fmt`,
  `cargo test`, and `cargo clippy --all-targets --all-features -- -D warnings`.
- Spirit regeneration and full Spirit tests are an additional downstream
  witness that the tokenized runner/trait emission still emits usable code.

## Design fit

The streaming feature follows the user's Nexus-visibility rule. The public
wire input is Signal: `SubscribeIntent(Query)`. The internal feature is visible
in Nexus as `OpenIntentSubscription(Query)`. The effect result is visible in
Nexus as `IntentSubscriptionOpened(IntentSubscription)`. The daemon only binds
the live socket writer to the already-minted typed token and asks the
subscription hub to publish typed events.

The generic mechanics are not reimplemented in Spirit:

- Length-prefixed transport stays in `triad-runtime::LengthPrefixedCodec`.
- Subscription tokens, registry, publisher, and stream framing stay in
  `triad-runtime` / `signal-frame`.
- Spirit owns only component-specific concepts: `Query` matching,
  `IntentEvent`, `IntentRecorded`, and the policy that `RecordAccepted`
  produces a pushed event.

The top-level public surface stays constrained. Generated plane nouns remain
under `spirit::schema::{signal,nexus,sema}` and the public-surface test still
passes. The new subscription helper is under `spirit::subscription`, not
re-exported as a top-level daemon noun.

## Remaining production gaps

The new Spirit is meaningfully closer to production, but these are still real:

1. The meta slot is only configuration so far. The daemon still needs the
   actual meta signal surface and listener path.
2. The subscription pilot is live-process streaming only. It does not preserve
   subscriptions across daemon restart, and it currently publishes only
   recorded-intent events.
3. The schema-rust-next token migration is incomplete. Runtime-critical slices
   are better, but the file still contains substantial string-emitter debt.
4. Production cutover from deployed `persona-spirit` still needs an explicit
   migration/cutover proof, not just local process-boundary parity tests.
5. The broader generated-runner and multi-listener adoption needs a final
   exemplar pass once the meta listener is real.

## Operator questions

No blocking question remains for the current commits. The next design decision
worth making explicit is whether the meta signal for Spirit should be authored
inside the Spirit repo immediately as the component-local meta surface, or
whether a separate `meta-signal-spirit` repo should be created before
production cutover. The user's latest guidance allows either shape, but says
every component must have the meta slot.
