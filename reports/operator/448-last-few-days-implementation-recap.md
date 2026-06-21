# 448 — Last few days implementation recap

## Scope

This recap covers the operator-visible implementation wave represented by
reports 420 through 447, with emphasis on code that landed or was integrated to
main. Designer-only analysis is included only where it changed the operator
lane or produced branches the operator merged.

## Mentci became a real component

The Mentci concept moved from an egui-adjacent workbench idea into a component
triad with a daemon runtime, working signal, meta-signal configuration, and a
shared client model.

Landed pieces:

- `signal-standard`: first shared typed socket vocabulary.
- `signal-mentci`: programmable UI contract, including question presentation,
  interface observation, answering, edited-answer proposals, and update push.
- `meta-signal-mentci`: typed daemon configuration contract.
- `mentci`: daemon runtime plus thin client over Unix sockets and binary
  startup, with in-memory question state, decisions, observations,
  subscriptions, edited proposals, and frame codec.
- `mentci-lib`: first as a daemon-shaped approval model, then re-founded on the
  live `signal-mentci` contracts after designer report 707 showed the old
  library had become stale.
- `mentci-egui`: revived as a daemon client surface, then adapted to consume
  `mentci-lib::ObservationModel` and `RenderNota` instead of duplicating
  approval and observation logic.

Key final heads from the latest integration:

- `signal-mentci` `58dd5a26d9b2` — public readers on projected interface state.
- `mentci-lib` `0731c374f9c0` — shared model consumes live `signal-mentci`
  contracts.
- `mentci-egui` `8c8b426e78eb` — consumes the shared model from main.
- `mentci` `ada047880d9d` — daemon bridge uses the shared
  `mentci_lib::CriomeVerdict` mapping.
- `meta-signal-mentci` `42222f306e71` — typed component socket endpoints.

The old egui top row for direct criome/nexus driving was removed from the
conceptual surface. The revived client path is the daemon transcript and
component socket model, with socket roles named by component kind such as
`Mentci`, `MetaMentci`, `Criome`, and `MetaCriome`, not generic ordinary/meta.

Verified gates included cargo tests and clippy for `signal-mentci`,
`mentci-lib`, `mentci-egui`, and `mentci`; the egui live-daemon observe test
passed.

## Criome authorization park substrate landed

The client-approval design was clarified: criome owns keys and the pending
authorization queue; Mentci approves or denies by criome-minted parked
authorization identity/slot; criome signs after approval.

Landed or integrated pieces:

- `signal-criome` `ff9ac192b21c` — parked authorization surface.
- `meta-signal-criome` `4940e4b13c57` — approval surface for parked
  authorization.
- `criome` `68b92c66de73` — client-approval witness binaries landed on main.

The track also absorbed the defect pass from designer reassessment: the
working-socket reject bypass, dead rejection contract surface, slot ordering,
and silent reject-on-unknown-slot concerns were fixed in criome before the
later witness landing.

This is the substrate that makes the Mentci approval loop meaningful: criome can
park a request, Mentci can observe it, and a client can answer by slot instead
of re-supplying the authorization evaluation by value.

## Mentci and criome were proven together

The live integration moved beyond a single-process test. We tested a sandboxed
daemon setup where Mentci connects to its own daemon socket and observes state.
The user-facing result was visible in the egui screenshot: the old direct-driver
status row was disconnected, while the real bottom daemon transcript showed the
new `ObserveInterfaceState` path.

The current proof is still narrow: it establishes daemon-client connectivity,
projection, NOTA rendering fallback, and the criome client-approval chain. The
next Mentci proof slice remains the approval card plus a criome+Mentci NixOS VM
test.

## Criome E1 transport started

Designer built and reported E1 increments 1 through 3; operator kept the
integration context aligned:

- peer addressing contract: `PeerNode`, `PeerAddress`, and peers config shape;
- `PeerEnvelope` wire header;
- TCP peer transport primitive with BLS wire crypto, distinct DST separation,
  verify-before-parse framing, and real TCP round-trip tests.

The remaining E1 implementation is increment 4: daemon serve-loop integration,
peer solicitation off the actor thread, timeout handling, nonce/replay handling,
and k-of-n quorum tally.

## Orchestrate gained a daemon-owned worktree registry

Designer's worktree protocol was integrated across the orchestrate triad and
local prototype patches were removed.

Landed heads:

- `signal-orchestrate` `a785cc77d45c` — worktree registry contract.
- `meta-signal-orchestrate` `135c2e7a8c13` — register/refresh meta orders and
  portable main dependency.
- `orchestrate` `0cd090455491` — daemon-owned typed worktree registry, scanner,
  projection, handlers, and tests.

The primary `tools/orchestrate` path remains an argv compatibility surface over
the dedicated orchestrate daemon triad. The registry state owner is the
daemon, and `worktrees.nota` is the typed projection/GC manifest rather than a
separate hand-maintained artifact.

The codegen skew found during the prototype was resolved: the landed stack
resolves current `schema-next` main `4b7e830a7001` and `schema-rust-next` main
`90d853c33ade`, not the stale intermediate pins.

Cargo tests and clippy passed for `signal-orchestrate`,
`meta-signal-orchestrate`, and `orchestrate`.

## Schema preservation and cleanup completed

The two risky `schema-rust-next` worktrees were investigated before cleanup.
Neither was safe to merge directly, but both were preserved.

Pushed preservation bookmarks:

- `schema-rust-next`
  `operator/preserve-schema-rust-next-reaction-expand` at `8b147fac`.
- `schema-rust-next`
  `operator/preserve-schema-rust-next-structural-forms-integration` at
  `a0138ce1`.
- `schema-next` `operator/preserve-schema-next-capability-resolution` at
  `3709fc15`.
- `schema-next` `operator/preserve-schema-next-structural-forms-integration` at
  `b7af872e`.

Removed stale branch names after preservation:

- `schema-rust-next`: `next/schema-capability-resolution` and
  `structural-forms-integration`.
- `schema-next`: `next/schema-capability-resolution` and
  `structural-forms-integration`.

Broad cargo sweep passed:

- `schema-next`: all-target/all-feature test and clippy, plus no-default lib
  test.
- `schema-rust-next`: all-target test and clippy with `nota-text`, plus
  no-default lib test.

Current relevant heads:

- `schema-next` `4b7e830a7001` — one lowering engine plus macro-registry
  pre-expansion pass.
- `schema-rust-next` `90d853c33ade` — impl catalog and typed malformed-name
  errors.

The preserved `reaction-expand` work should be treated as a mining source for a
fresh port over current schema mains, not as a branch to merge.

## Propagation stack mainlined earlier in the window

The criome-gated propagation stack was landed to main across:

- `criome` `6c75804c` — publish-side authorized-object matching retirement.
- `router` `94712199` — criome authorized-object projection.
- `spirit` — gated propagation loop integration after rebase over the current
  mirror shipper line.

Targeted cargo checks passed for criome, router, and Spirit's
`end_to_end_offline_full_chain` mirror-shipper path. Nix checks were not run for
that stack.

## Cleanup and branch hygiene

Feature bookmarks integrated during this wave were retired after main landing:

- Mentci re-found branches in `signal-mentci`, `mentci-lib`, and `mentci-egui`.
- Orchestrate registry branches in `signal-orchestrate`,
  `meta-signal-orchestrate`, and `orchestrate`.
- Schema stale worktree branch names after preservation.
- Earlier criome-gated propagation loop bookmarks and worktrees.

## What is still next

The most valuable next implementation slices are:

- Mentci CLI read/answer roster so the daemon has a grep-assertable text client.
- Mentci egui approval card so it can answer parked criome questions, not only
  observe.
- Criome+Mentci NixOS VM proof on Prometheus using the existing module/test
  foundation.
- Criome E1 increment 4: daemon peer listener, quorum solicitation, and tally.
- A fresh schema capability-resolution port only if the preserved work is still
  wanted over the current one-lowering-engine and impl-catalog model.
