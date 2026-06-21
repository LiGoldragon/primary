# 711 — mentci bootstrap phase 2: approval card + read-only/write mode (on the epic) + operator handoffs

Phase 2 of the criome/mentci/spirit bootstrap, on the designer-maintained epic
branch `criome-mentci-bootstrap`. The egui approval card and the read-only/write
criome-access mode are built and verified across the designer-owned repos; the
remaining pieces (the daemon mode projection, the lockstep integration, the
two-daemon nixosTest) are operator handoffs with ready specs.

## What landed this session (epic `criome-mentci-bootstrap`)

- **egui approval card** — `mentci-egui` `729f1d3d`. The shell renders
  `mentci-lib`'s approval cursor (the pending-question queue, the selected
  question's source/prompt/explanation/suggested-answer/context) and answers it
  with Approve/Reject/Defer through the shared model (`verdict_for_selected` →
  `UserEvent::AnswerQuestion`). It dispatches the model's own `Cmd` instead of
  hand-rebuilding the request (fixes the 708 MVU-defeated finding). This closes
  the 708/709 headline gap: egui was view-only; it can now answer.
- **read-only/write criome-access mode** (designer-owned parts of the lockstep):
  - `signal-mentci` `9a475450` — `CriomeAccess [ReadOnly ReadWrite]` + a bare
    `criome_access` field on `InterfaceState` (regenerated), with
    `InterfaceState::criome_access()` and
    `ProjectedInterfaceState::criome_access() -> Option<CriomeAccess>` (`Some`
    only for `FullProjection`).
  - `mentci-lib` `ecef557f` — `ObservationView.criome_access`, derived in
    `view()` from the Mentci socket's latest full projection (`None` on a narrow
    interest = observation-only).
  - `mentci-egui` `729f1d3d` — the card gates Approve/Reject/Defer on
    `Some(ReadWrite)`; `ReadOnly`/`None` renders observation-only + the mode in
    the header.

Verified: signal-mentci 6 tests, mentci-lib 11 tests (incl. the mode-surfacing
test), egui build + clippy clean. egui's `--all-targets` live-daemon test is the
**lockstep gate** — it passes once the daemon's `full_state` carries the field
(handoff 2). All three epic branches pushed to origin.

## Architecture decided 2026-06-21 (manifested in repo INTENT/ARCHITECTURE)

The Spirit guardian declined the read-only/write + daemon-routing decision as
design-detail (`InsufficientWarrant`), so its canonical home is the repo docs
(being written into `mentci-lib`, `signal-mentci`, `mentci-egui`
INTENT.md/ARCHITECTURE.md this session):

- **Daemon-routing.** Clients reach criome only through the mentci daemon; a
  client answers by sending `AnswerQuestion` to the daemon, which routes the
  verdict to criome by the parked `AuthorizationRequestSlot`. The client never
  opens a criome socket; `mentci-lib` is the client-side library and the daemon
  imports only `CriomeVerdict`.
- **Read-only/write mirror.** The daemon holds its criome connection read-only
  (observe parked) or write (observe + submit) and mirrors that level to
  clients; a client of a read-only daemon opens observation-only.

## The a/b divergence — resolved on main (verify-and-close, do NOT re-integrate)

Operator integrated the earlier *client-direct* (a) seam to mentci-lib main
(`f628b371`), then the (b) daemon-routing correction (`a13115b1`). So **main is
already (b)** (no `Cmd::SubmitCriomeVerdict`, routes via `AnswerQuestion`). My
epic `b9cd9dab` is therefore redundant — the mode commit sits on top of it;
operator integrates the mode delta, not `b9cd9dab` itself. Verify:
`jj -R <mentci-lib> file show -r main src/cmd.rs | grep -c SubmitCriomeVerdict`
prints `0`.

## Operator handoffs

### 1. Integrate the mode increment as ONE lockstep

Adding `criome_access` to `InterfaceState` changes the rkyv/NOTA wire shape of
`FullProjection`. Pre-production, no backward-compat — but the daemon and all
clients must rebuild **together** against the regenerated `signal-mentci`; no
mixed-version socket pair. Land signal-mentci `9a475450` + mentci-lib `ecef557f`
+ mentci-egui `729f1d3d` + the daemon delta (handoff 2) in one integration.
Narrow-interest projections carry no mode (`None` → observation-only), so they
stay backward-shaped.

### 2. Daemon mode projection (the lockstep's daemon piece) — ready spec

The daemon already computes the mode (`application_context()` returns
write-enabled iff `self.criome_bridge.is_some()`); it must write it into
`full_state` so the mirror reaches clients. **Option A (recommended):** thread a
`CriomeAccess` through `project`/`full_state` from the `StateApplicationContext`
already in scope in `apply_with_context`'s `ObserveInterfaceState` arm:

- `impl From<StateApplicationContext> for CriomeAccess` (`criome_write_available`
  → `ReadWrite`, else `ReadOnly`) — a method/From, not a free function.
- `full_state(&self, criome_access: CriomeAccess)` passes it as the new 6th arg
  of `InterfaceState::new`; `project`/`observe` thread it through.
- `import CriomeAccess` from `signal_mentci` in `state.rs`.

Daemon tests assert on `PendingQuestionsProjection` (no `InterfaceState`), so
they are unaffected; only direct `full_state`/`project` callers need the new arg
(none found in `tests/`). Full per-line spec: workflow `mentci-phase2-parallel`
output, "Operator delta — mentci daemon".

### 3. Two-daemon nixosTest (criome + mentci on Prometheus) — design ready

Recycle `criome-nixos-module-142`'s `criome.nix`; author a sibling `mentci.nix`;
expose the mentci flake packages (daemon, the NOTA→rkyv configuration encoder,
the CLI). One NixOS guest runs both daemons under a single `criome` system user
(so the `0600` meta-socket boundary is exercised, not bypassed by root); the
testScript flips criome to `ClientApproval` over its meta socket, parks an
authorization, drives mentci to observe + answer it, and asserts criome records
the grant (daemon-routing: mentci delivers the verdict by slot). Full design:
workflow output, "criome+mentci nixosTest design". This is the largest remaining
surface and the multi-daemon proof the bootstrap needs.

### 4. Integrate the egui card (`729f1d3d`) with the lockstep above.

## Method note

This phase ran a parallel design workflow (`mentci-phase2-parallel`: mode spec,
divergence, nixosTest, INTENT — four grounded streams) while the egui card was
finished in the foreground; the buildable mode increment was then applied + built
by the orchestrator (builds need network/sandbox), and the INTENT docs by a
background agent. The detailed per-file specs live in the workflow output.
