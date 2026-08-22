# Chroma slice 2: implementation-ready protocol account

Date: 2026-08-22
Scope: only the accepted-design slice covering persisted monotonic theme revisions, the public D-Bus snapshot/signals/registration/typed acknowledgements, per-consumer status, and removal of the one-shot Emacs projection.

## Outcome

Chroma currently has the right semantic owner and persistence/message seams, but no public D-Bus service, revision, consumer registry, or durable acknowledgement path. The existing Emacs adapter is a one-shot `emacsclient --eval` call: it can report process success, not that the requested theme became the postcondition. The implementation should therefore add a typed D-Bus edge around `ChromaRoot`, persist `(ThemeMode, revision)` atomically, make the root actor own consumer status, and delete the old Emacs concern/configuration. Existing UDS/rkyv/DOTOS control should remain separate and unchanged in this slice.

## What the brief/design settles

The accepted design in `flows/01a0238b/reports/emacsAdapterDesign.md` settles these behaviors:

- Chroma remains semantic authority for desired Light/Dark state.
- Every accepted desired-state change has a persisted monotonic revision that survives daemon restart.
- A public D-Bus service publishes the current snapshot, returns that snapshot from consumer registration, and signals later desired-state revisions.
- A consumer reports an applied acknowledgement or a typed bounded failure for a revision.
- Chroma exposes per-consumer `Pending`, `Applied`, `Unavailable`, and `Failed` status.
- A plugin subscribes before registration; registration reconciles the snapshot; owner loss/restart causes re-registration; stale revisions do not mutate status; duplicate acknowledgements for the current revision are idempotent and still check the postcondition.
- Home owns Ignis generation/deployment. Emacs becomes an external plugin/repository projection, not a Chroma-native one-shot concern.

The code-level names below are an implementation plan, not additional design approval.

## Exact authority versus proposed particulars

The prior transcript was searched rather than treated as a naming authority. The agent proposed illustrative calls equivalent to:

```text
RegisterConsumer("emacs") → (Dark, 42)
ThemeChanged(Dark, 43)
ReportProjection("emacs", 43, Applied)
ReportProjection("emacs", 43, Failed(code, bounded-summary))
```

The psyche's exact replies were `1. yes a new public repo.`, `2. the dbus is good`, `3. yes`, and then `good enough, approved` after the architecture and semantics were restated. Thus the report may rely on D-Bus, revisioned snapshot/signal/ack semantics, consumer statuses, a new public plugin repo, and Home-owned Ignis. It must not present the illustrative call names as already approved. The following remain unresolved and need an implementation-time ruling or a narrow protocol decision: well-known bus name; object path; interface name; exact method/signal signatures; stable consumer identity and owner binding; status query shape; failure-code enum and bounded-summary byte limit; authorization/spoofing behavior; and persistence migration for existing `state.redb` files.

## Repository and worktree state

The inspected product repository is `/git/github.com/LiGoldragon/chroma`. Its current source tree is legacy-wired for the old Emacs path. `jj status` at inspection time showed only the existing `.beads/issues.jsonl` addition in the shared Chroma worktree; no product file was changed by this subflow. The primary workspace `/home/li/primary` also contained unrelated flow changes already present before this record. No tests, builds, services, D-Bus calls, or deployment commands were run.

Relevant product instructions describe Chroma as a unified visual-state daemon and prescribe push-not-poll behavior. The current dependencies already include zbus 5.13.2, redb 2.6.3, rkyv 0.8, DOTOS, and Kameo. The durable project gate is the Nix flake: `checks.default` runs Cargo tests and `checks.sandbox-terminal` exercises a `dbus-run-session` plus UDS clients.

## Existing architecture and seams

### Persistence

`src/state.rs` defines `StateStore`, redb table constants, and `StoredVisualState`. The `theme` table's `current` key currently stores only an archived `ThemeMode`; `record_theme` delegates to a generic single-table archive writer. There is no revision, migration path, or state test. This is the natural atomic write seam: persist a single archived theme record containing mode and revision (or deliberately add a revision table in the same write transaction), then read it as the startup fallback. The choice between replacing the value shape and adding a table is unresolved because old `state.redb` compatibility is not specified.

### Root actor and current fanout

`src/daemon.rs` starts `ChromaRoot`, reads the persisted fallback, and dispatches UDS `SetTheme`/`GetTheme` messages. `set_theme` updates the root's current mode, persists it, enqueues the existing `ThemeApplier`, and returns `Response::Accepted`. This actor should own a `HashMap<ConsumerId, ConsumerState>` and the revision; a D-Bus interface should hold an actor reference and send typed messages rather than introduce an independently synchronized status map. A successful desired-state write should advance the revision before publishing; all registered consumers become `Pending` for that new revision, while unrelated appliers continue to operate.

### Current Emacs projection to remove

`src/theme.rs` defines `ThemeMode`, `ThemeConcern::Emacs`, `ThemeAdapters.emacsclient`, and the `EmacsThemeConcern` actor. The actor chooses `ignis-light` or `ignis-dark`, executes `emacsclient --eval`, discards stdout/stderr, applies a two-second timeout, and treats any successful process exit as success. It has no durable revision, registration, owner tracking, acknowledgement, or postcondition verification. `src/config.rs` accepts `Emacsclient`; `README.md`, `AGENTS.md`, `skills.md`, `ARCHITECTURE.md`, and `tests/config.rs` still document or fixture it. These are the complete removal/search seams identified by this inspection.

### D-Bus and existing protocol conventions

Chroma currently uses D-Bus only as a client (GeoClue on the system bus and Ghostty integration on the session bus). It does not own a public service. The public contract should be a small typed zbus interface, with D-Bus method/signal values mapped to domain types rather than free-form strings. The existing UDS protocol is rkyv/DOTOS framed request/response and should not be conflated with the D-Bus consumer protocol. The Nexus psyche favors typed signals and actor ownership; the accepted design explicitly approves D-Bus as the edge for this adapter.

## Proposed protocol shape (subject to the unresolved naming decisions)

Use a focused module such as `src/theme_dbus.rs` (or a protocol module selected by the implementer) containing the domain and zbus surface. The wire shape should express:

```text
ThemeRevision        = unsigned, monotonically increasing, persisted
ThemeSnapshot         = { mode: Light | Dark, revision: ThemeRevision }
ConsumerId            = stable bounded label/enum for a supported projection
ConsumerStatus        = Pending | Applied | Unavailable | Failed
Failure               = bounded typed code + bounded summary
```

Minimum operations/signals, without claiming exact names, are:

1. `RegisterConsumer(identity)` binds the caller's D-Bus owner to a consumer identity and returns the current `ThemeSnapshot` plus the current status (or a precisely ruled status response). Registration must be safe after subscribing to the desired-state signal.
2. A desired-state signal carries the full `ThemeSnapshot`, including mode and revision. It is push-not-poll and lets a consumer reconcile after missed signals by re-registration/snapshot.
3. `AcknowledgeApplied(identity, revision)` records success only for the current revision and bound owner. A duplicate acknowledgement for that same revision is idempotent and invokes/represents a postcondition check. A stale revision is a typed stale/no-op result and cannot regress status.
4. `AcknowledgeFailed(identity, revision, Failure)` records `Failed` only for the current revision and bound owner. Failure code and summary are bounded; full plugin diagnostics remain local to the plugin.
5. A status query (or registration response that is explicitly sufficient) exposes per-consumer status and revision. Owner disappearance transitions the bound consumer to `Unavailable`; a later registration of that identity gets a fresh snapshot and can return to `Pending`/`Applied`.

The D-Bus implementation should bind acknowledgements to the registration's unique owner, not trust an arbitrary consumer string. It should define whether multiple owners for one identity are rejected/replaced and how owner loss is observed (zbus name-owner tracking or an equivalent service lifecycle hook). These are safety decisions still requiring explicit protocol wording.

## File-level implementation plan

1. `src/state.rs`: introduce a persisted theme record with mode and revision, initialize the revision for legacy/no-record state, write mode+revision atomically, and expose a read path that preserves the monotonic value across restart. Add a migration/compatibility test once the legacy-file policy is chosen.
2. `src/daemon.rs`: add root revision and consumer registry state; make accepted `SetTheme` allocate/persist the next revision, mark active consumers pending, fan out the desired snapshot, and preserve existing applier behavior. Add typed root messages for register, ack-applied, ack-failed, owner-lost, and status/snapshot query. Define stale/duplicate behavior in the message handler.
3. New `src/theme_dbus.rs` (or an equivalently named module): define bounded domain types and zbus interface methods/signals; expose the service from `run`; route all operations into the root actor; bind registrations/acks to D-Bus unique names; emit the initial/current snapshot and desired-state changes. Keep exact bus/interface/path names in one protocol declaration.
4. `src/lib.rs`: export only the public domain types required by tests or sibling crates; avoid exposing internal actor state.
5. `src/theme.rs`: remove `ThemeConcern::Emacs`, `EmacsThemeConcern`, `ThemeAdapters.emacsclient`, and their fanout/reference branches. Do not replace them with another Chroma scheduler or palette generator; the external plugin owns application and verification.
6. `src/config.rs`: remove `Emacsclient` parsing and reject/remove the old configuration form according to the chosen compatibility policy. Update native config fixtures in `tests/config.rs`.
7. `README.md`, `AGENTS.md`, `skills.md`, `ARCHITECTURE.md`: describe the D-Bus desired-state/consumer boundary and remove claims that Chroma directly runs Emacs. Keep Home/Ignis ownership aligned with the accepted design.
8. `tests/state.rs` (new) and/or `src/state.rs` tests: cover first revision, increasing revisions, same-mode accepted changes (whether each accepted command advances), and restart persistence/migration.
9. `tests/theme_dbus.rs` or daemon protocol tests (new): cover registration snapshot, subscribe-before-register reconciliation, desired-state signal, pending transition, applied/failed current revision, stale ack, duplicate current ack, owner disappearance/unavailable, re-registration, and status query. Use a test D-Bus session and an actor/service harness; avoid source-text assertions.
10. `flake.nix`/sandbox test: extend the existing `dbus-run-session` integration gate with the public Chroma service and a fake consumer, or add a focused Nix check if the existing sandbox’s scope would obscure protocol failures. Preserve `nix flake check` as the handoff gate.

## Durable test gates and non-goals

The repository's durable gate is `nix flake check` (Cargo tests plus sandbox). The new behavioral tests must prove restart persistence and protocol state transitions, not merely inspect source text. The sandbox should exercise a real session bus and owner-loss path where feasible. Home's real E2E deployment/verification remains a later slice; this slice does not alter Home, deploy services, install packages, or publish a repository.

Do not silently redesign the UDS protocol, add a second privileged/ordinary socket, make the plugin generate palettes, or let Chroma wait on Emacs before accepting a desired-state change. Those would exceed this accepted D-Bus slice.

## Risks and unresolved questions returned to the caller

- Exact bus name, object path, interface, method/signal names, and D-Bus type encodings are not in the accepted wording; the transcript's call examples are agent-proposed illustrations.
- Legacy `state.redb` migration and the initial revision value are unspecified. Replacing the current archive shape without a migration ruling could discard or misread a user's existing theme state.
- It is not explicitly ruled whether an explicit request for the already-current mode creates a new revision. Existing `set_theme` accepts and persists every command, so deduplication would be a new semantic choice.
- Consumer identity, one-owner-per-identity policy, authorization, and owner-loss handling need security/compatibility wording. Without owner binding, a process could spoof an Emacs acknowledgement.
- Failure-code enum and bounded summary limit need a stable contract. Full Lisp errors must not cross the public boundary unbounded.
- Status query shape and whether `Unavailable` is retained across daemon restart are unresolved.
- D-Bus service startup/failure behavior relative to the existing UDS daemon loop needs a concrete lifecycle test.
- Existing docs/config/tests all describe the old concern; incomplete removal would leave a misleading compatibility surface.

## Sources

- `/home/li/primary/flows/01a0238b/reports/emacsAdapterDesign.md` — accepted slice, ownership, protocol behaviors, tests, implementation order.
- `/home/li/primary/flows/01a0238b/vision/emacsPlugin.md` — preserved psyche words and approved architecture context.
- `/home/li/primary/flows/01a0238b/witnesses/sourceBoundaries.md` — prior code-read witnesses for the one-shot path and current daemon boundary.
- `/home/li/primary/flows/01a020ff/log.md` — prior boundary record explaining why the one-shot projection is not a durable contract.
- `/home/li/.codex/sessions/2026/08/21/rollout-2026-08-21T10-58-38-01a0238b-2c53-76e1-9ae9-5c87f909544f.jsonl` — narrowly searched prior D-Bus proposal transcript; separates agent proposals from psyche replies.
- `/home/li/primary/psyche-raw/Vision/signalIsOurMessagingLayer.md` — typed signal convention.
- `/home/li/primary/flows/cff271af/reports/psycheOnSoftwareDesignAndNexus.md` — Nexus/actor rationale consulted without overriding the accepted D-Bus choice.
- `/git/github.com/LiGoldragon/chroma/src/state.rs` — current redb theme persistence.
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs` — root actor, UDS dispatch, persistence/enqueue seams, current absence of public D-Bus.
- `/git/github.com/LiGoldragon/chroma/src/theme.rs` — `ThemeMode`, Emacs concern, adapter, and one-shot process behavior.
- `/git/github.com/LiGoldragon/chroma/src/config.rs` — Emacsclient config parser.
- `/git/github.com/LiGoldragon/chroma/{Cargo.toml,Cargo.lock,flake.nix}` — dependencies and durable test gates.
- `/git/github.com/LiGoldragon/chroma/{README.md,AGENTS.md,skills.md,ARCHITECTURE.md,tests/config.rs,tests/theme.rs,tests/hard_constraints.rs}` — current documentation, fixtures, and testing conventions.
