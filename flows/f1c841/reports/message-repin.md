# Message repin: message contracts and Message onto ethos-zero 16, signal 7, Flow 0.19.0

Subflow of f1c841, 2026-10-03. Everything is on main and pushed. Nothing was
deployed. The running nexuses and the nix profile were not touched. flow,
flow-test and the orchestrate family were not edited.

## Versions

| Repository | Before | After | Main commit |
| --- | --- | --- | --- |
| signal-message | 8.0.0 (d5742005) | 9.0.0 | 0f5c0f0db88c |
| meta-signal-message | 0.8.0 (14f57596) | 0.9.0 | f8ca09fc91d4 |
| message | 0.17.1 (7ffd4a27) | 0.18.0 | 64ea9eb935c9 |

## Pins after

- signal-message 9.0.0: ethos-zero 0edfc0c3 (16.0.0, build), signal
  66e7b153 (7.0.0), signal-flow c297d987 (8.0.0), meta-signal-flow 69f9c146
  (12.0.0), protos 15b41da8 and datom-codec 4dff16b4 (0.32.2, optional).
- meta-signal-message 0.9.0: the same, plus signal-message 0f5c0f0d (9.0.0).
- message 0.18.0 (workspace): signal-message 0f5c0f0d, meta-signal-message
  f8ca09fc, signal-flow c297d987, meta-signal-flow 69f9c146, protos 15b41da8,
  datom-codec 4dff16b4; signal 66e7b153 through them. These are the very
  revisions flow 0.19.0 (4f3670ef) pins. sema-engine stays 516f01fe (0.16.0):
  the build did not need 0.18.0.
- protos 0.31.0, datom-codec 0.31.0 and ethos-zero 10.0.0 remain in
  message's lock only as build dependencies of signal 7.0.0's own build
  script (`cargo tree -i protos@0.31.0 -e normal,build`); the runtime graph
  holds one codec, 0.32.2.

## What changed

- **Generated Rust is fresh and unchanged.** Each contract's build.rs
  regenerates from `ethos/signal.ethos` with ethos-zero 16.0.0 and asserts
  equality with the committed `src/generated/signal.rs`; both builds pass, so
  the Signal-root output is byte-identical. The ethos sources were not
  edited.
- **`signal::Contracted` for `Query`** over `ETHOS` in both contracts (the
  pattern signal-flow 8.0.0 set). New `tests/greeting.rs` in each: own
  source is Greeted, another source is refused with this digest, and the
  other contract's greeting (signal-flow's on signal-message; signal-message's
  on meta-signal-message) is refused. Seen failing (did not compile) with
  the impl removed.
- **The `datom` feature no longer enables `signal/datom`** (signal 7.0.0's
  pins datom-codec 0.31.0; neither contract holds a signal type).
- **`.textualize()` became `.compact()`** in both contracts' datom tests (the
  signal-message datom tests failed with vertical text before this change)
  and in the `message` and `message-meta` reply printing, so the CLI replies
  stay one line.
- message's `flake.nix` crane `version` string moved from 0.17.1 to 0.18.0.
- **Store.** No stored record's archive changes: the ethos of signal-message,
  meta-signal-message and meta-signal-flow is unchanged from the previous
  pins, and signal-flow 7.0.0 -> 8.0.0 only appended variants and types
  (`FlowId`, `FlowAspect` unchanged). A 0.17.x store opens unchanged.
- `UPGRADES.md` entries landed in all three repositories saying what a
  deployer does: rebuild Message and Flow together, start Flow first, no
  unit, store or configuration change.

## Commands and results

| Command | Where | Result |
| --- | --- | --- |
| `cargo test --all-features` | signal-message | generated_contract 5, greeting 3: green |
| `cargo test` | signal-message | generated_contract 2, greeting 3: green |
| `cargo clippy --all-targets --all-features -- -D warnings`, `cargo fmt --check` | signal-message | clean |
| `nix flake check` | signal-message | all checks passed (build, test, test-generated-contract, test-datom, test-doc, doc, fmt, clippy) |
| `cargo test --all-features` | meta-signal-message | contract 3, greeting 3: green |
| `cargo test` | meta-signal-message | greeting 3: green |
| clippy `-D warnings`, fmt | meta-signal-message | clean |
| `nix flake check` | meta-signal-message | all checks passed |
| `cargo test --workspace` | message | message 2, message-defaults 1, message-meta 1, configuration_lives_in_the_store 4, message_through_flow 13: green |
| `cargo clippy --workspace --all-targets -- -D warnings`, `cargo fmt --check` | message | clean |
| `nix flake check path:<copy without target/>` | message | all checks passed (clippy, default, fmt, message-cannot-invoke-herdr, message-component-cannot-own-local-ledger, message-runtime-cannot-reference-retired-terminal-brand, no-free-functions, no-inherent-methods) |

All Nix checks ran for x86_64-linux only, built on prometheus. message's
flake check ran on a `path:` copy of the committed tree because the worktree
sits under a stray `.git` at `~/wt/github.com/LiGoldragon/message/` that
hides `flake.nix` from a `git+file` evaluation; that stray repository is not
this flow's and was left alone.

## Witness: Message against a real Flow 0.19.0

Method: `nix build` flow at 4f3670ef (`/nix/store/5nbjl9i6...-flow-0.19.0`)
and message 0.18.0 (`/nix/store/783swgrz...-message-0.18.0`); in a fresh
temporary HOME and XDG_RUNTIME_DIR, start `flow-nexus` (no arguments,
unconfigured), then `message-nexus` (its defaults point at
`$XDG_RUNTIME_DIR/flow/flow{,-meta}.sock`), then run the clients.

| Client call | Message 0.18.0 reply |
| --- | --- |
| `message 'Send.{ [ 7d41e0 ] Soft Text.hello }'` | `SendRejected.SenderUnknown` (Flow's ResolvePeer answered NotAFlow) |
| `message-meta 'Send.{ [ 7d41e0 ] Soft Text.hello }'` | `SendRejected.UnknownRecipient.7d41e0` (Flow's vet answered `DeliveryRejection::UnknownFlow`) |

Both replies are Flow 0.19.0 replies decoded by Message 0.18.0 over the
real sockets; neither Nexus wrote to stderr. Not witnessed: a delivery into
a live Herdr pane (that needs a configured Flow and Herdr; flow-test's
ground, not touched).

**Correction to the brief.** The same script with message 0.17.1
(`/nix/store/c00hqwp5...-message-0.17.1`) against Flow 0.19.0 gave the same
two replies. On these two paths (ResolvePeer, vet) an old Message does read
Flow 0.19.0's frames: meta-signal-flow's ethos did not change between 11.0.0
and 12.0.0, and the plain Signal frame of signal 5.0.0 and 7.0.0 decoded
alike here. So "no Message on main can talk to Flow 0.19.0" is not true for
these paths; whether 0.17.1 survives Deliver, Observe and a reply holding an
appended signal-flow 8.0.0 variant was not tested. Message 0.18.0 removes
the question by holding exactly Flow's revisions.

## Red and open items

- Nothing is red.
- Message, like Flow 0.19.0, still speaks the plain Signal frame: no
  greeting, no exchange layer. The `Contracted` impls are ready for that
  design task.
- sema-engine stays 0.16.0 (UnsupportedReadPlan, non-atomic version stamp).

## Vision conflicts (for the psyche seat; not redesigned)

Judged against vision-ethos. signal-message `ethos/signal.ethos` and
meta-signal-message `ethos/signal.ethos`:

1. **Not vertical.** Imports, queries and responses each sit on one line;
   struct types such as `MessageConfiguration.{ ... }` and
   `SendRejection.[ ... BodyRefused.{ FlowId BodyRefusal } ... ]` hold
   next layers on one line. Reprinting changes `ETHOS` and the contract
   digest.
2. **Variant payloads held in invented types.** signal-message:
   `Send.SendRequest`, `Submitted.Submission`, `Receipts.Submission`,
   `SendRejected.SendRejection`, `MessageRejected.MessageRejection`,
   `ReceiptObserved.Receipt`. meta-signal-message: `Configure.MessageConfiguration`,
   `Redeliver.RedeliverRequest`, `Configured.Configured` (a reply repeating
   its own name), `ConfigureRejected.ConfigureRejection`,
   `RedeliverRejected.MessageRejection`.
3. **Types used once declared apart.** meta-signal-message's four socket
   path aliases (`OrdinarySocketPath.String` and the rest), each used only
   in `MessageConfiguration`; `Activation`, `RedeliverRequest`,
   `ConfigureRejection`; signal-message's `Priority` and `Grade` are each
   used once (in `SendRequest`, `Receipt`).
4. **Shared names live in Signal files, not a Library.** `MessageId`,
   `SendRequest`, `Submission`, `Receipt`, `SendRejection`,
   `MessageRejection` are imported by meta-signal-message from
   signal-message's Signal; `MessageId`, `Content`, `BodyRefusal`,
   `DeliveryRejection`, `InterruptWitness` come from meta-signal-flow's
   Signal. No Library, Operation or Memory root exists in either repository;
   the Message store's records are hand-declared in message-nexus.
5. **Rejection naming.** `MessageRejected` names the subject, not the past
   act; `Refused.DeliveryRejection` in `Grade` echoes another contract's
   type rather than carrying its payload in the variant.

## Sources

- Brief from f1c841; `flows/f1c841/reports/flow-contracts-repin.md` (the
  pattern followed).
- Repositories under `/git/github.com/LiGoldragon/`, worked in
  `~/wt/github.com/LiGoldragon/{signal-message,meta-signal-message,message}/message-repin-f1c841`.
- signal-flow main c297d987 (`UPGRADES.md`, `tests/greeting.rs`), meta-signal-flow
  main 69f9c146, flow 4f3670ef `Cargo.toml`.
- `jj diff --from 1c9e4b30 --to c297d987 -- ethos` (signal-flow, appended
  only); `jj diff --from 2ac045c2 --to 69f9c146 --stat` (meta-signal-flow,
  no ethos change).
- Skills: knowledge-ethos, knowledge-nexus, vision-ethos, versioning,
  breaking-upgrades, testing.
- Orchestrate lock 11667 (MessageRepin).
