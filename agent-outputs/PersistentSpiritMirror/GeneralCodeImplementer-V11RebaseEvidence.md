# General Code Implementer — v11 Rebase + M1 Witness Evidence

Addresses the blocking audit findings (H1, L4, M1) on the non-gated front of the
persistent Spirit A→B mirror slice. Prior green evidence was on a pre-v11 base;
this rebases both feature branches onto current mains and re-verifies on
prometheus against v11 `main`.

Source of task: `RustAuditor-Review.md` (H1/L4/M1), `GeneralCodeImplementer-BeadEvidence.md`.

## Rebased revs (new hashes)

| Repo | Bookmark | New tip | Parent (main) | Was |
|---|---|---|---|---|
| spirit | `criome-authorization-push` | `21421448` (M1 witness) → `14575379` (om4g.2) | `05269499` (v11 main) | `4a017504` (pre-v11, 5 commits) |
| spirit | `criome-authorization-push-prerebase` | `4a017504` (preserved original 5-commit line) | — | new bookmark |
| mirror | `criome-auth-witness` | `3933d11d` (x3l7) | `b8cf8eca` (0.2.0 main) | `c2e4fed8` (pre-0.2.0) |

All three bookmarks pushed to `origin`; `@origin == @git == local` confirmed for each.

## H1 — spirit rebase (om4g.2 onto v11 main)

**Scope decision (NEEDS REVIEW):** the branch `criome-authorization-push`
(`4a017504`) carried **5** commits on merge-base `9e413baa9a` (0.19.0). Only the
tip, `4a017504` (om4g.2, the criome-gate feature), is a bead in this slice. The
lower 4 commits — `899e99ed`, `d03f35db`, `08771c82` ("criome authorization
submit stream") and `202a6e24` ("refresh signal-router lock") — are a **separate
lane's WIP** (a live `spirit-auth-submit-stream` jj workspace exists) that
repoints `criome` / `signal-criome` / `router` from `branch = "main"` to
cross-repo `branch = "criome-authorization-push"` (pre-v11 branches). Bringing
them onto v11 would force those pre-v11 cross-repo branches into the tree and
would not build.

I therefore **rebased only the om4g.2 commit `4a017504` onto v11 `main`**
(`jj rebase -r 4a017504 -d main`), producing:
- `14575379` — om4g.2 criome-gate feature on v11 main
- `21421448` — M1 witness (child; see below)

The dropped 4-commit line is **preserved intact** on origin as
`criome-authorization-push-prerebase` (`4a017504`) so nothing is lost and the
rescoping is diffable. The submit-stream lane can rebase its own work from there.

**Verified this is safe:** om4g.2 (`4a017504`) touches only `Cargo.toml`,
`src/engine.rs`, `src/daemon.rs`, `src/lib.rs`. It does **not** touch
`src/criome_gate.rs`. The observe path (`observe_gate_head`) depends on
`observe_authorization`, `LocalHeadCapture::spirit_head`, `GateDecision::Observed`,
`CriomeGateError` — all already present in **main's** `criome_gate.rs`
(byte-identical to fork-point; main never touched it). So the criome-gate feature
is self-contained against v11 main's `criome_gate.rs`.

**Conflict resolution:** the scoped `jj rebase -r 4a017504 -d main` merged
**cleanly, zero conflicts.** om4g.2's edits and main's v11 edits fall in disjoint
regions:
- `Cargo.toml`: om4g.2 edits only the `[features]` block (adds `criome-gate`,
  changes `mirror-shipper = ["criome-gate", "dep:mirror", "dep:signal-mirror"]`);
  main edited only `version` (0.19.0→0.21.0) and left the `mirror-shipper` line
  identical to om4g.2's base, so the context matched. Result keeps **both**:
  version `0.21.0` + the criome-gate feature. Deps stay on `branch = "main"`
  (the cross-repo repointing lived in the dropped commits, so it never arrived).
- `Cargo.lock`: **untouched** — om4g.2 does not edit it, so main's v11 lock
  (`signal-spirit 151d49c8`) stands. No `5d0905a7` conflict (that pin lived in
  the dropped commits). No lock regeneration needed; criome/signal-criome are
  already in main's lock as mirror-shipper deps.
- `src/engine.rs`: clean 3-way merge. `configure()` retains **both** main's
  `agent-guardian` guardian-prompt handling AND om4g.2's `criome-gate` gate-arm
  block; om4g.2's `ObserveGateError`, `observe_gate_head`, and the relaxed
  `versioned_log_head` cfg all land beside main's guardian additions.
- `src/lib.rs`, `src/daemon.rs`: disjoint from main (main did not touch daemon.rs;
  its lib.rs `GuardianPromptSource` re-export is far from om4g.2's cfg flips).

## M1 — criome-gate-only observe witness (new test)

New file `spirit/tests/observe_gate_1of1.rs` (commit `21421448`), registered in
`Cargo.toml` with `required-features = ["criome-gate", "testing-trace"]`. It
closes the auditor's gap: the `cfg(all(criome-gate, not(mirror-shipper)))` daemon
dispatch had no behavioral test (the only witness, `criome_gate_1of1`, requires
`mirror-shipper` and drives `gate_and_ship_head`).

The witness drives the **real daemon boundary** —
`SpiritDaemon::handle_working_input(&mut engine, input, &connection)`, the exact
entry the running daemon calls per accepted working connection (stronger than the
existing witnesses, which drive the engine method directly and only comment that
it is "what handle_working_input calls"). `ConnectionContext::from(SocketAddr)`
makes the boundary test-constructible. Two proofs:
- `armed_gate_observes_head_and_emits_authorization_trace_through_daemon`: owner
  `Configure(CriomeGateTarget::Socket)` against a live AutoApprove criome (real
  Unix-socket round-trip on its own OS thread); one working record through the
  daemon emits exactly one `AuthorizationObjectName::Observed` trace event, no
  ship (no mirror in this build).
- `unarmed_gate_is_a_noop_through_daemon`: no Configure → `observe_gate_head`
  returns `Ok(None)`, zero authorization trace events.

Helpers are free functions in the `tests/` integration binary, matching the
established convention in `criome_gate_1of1.rs` (permitted under cfg-test).

## L4 — mirror rebase (x3l7 onto 0.2.0 main)

`jj rebase -r criome-auth-witness -d main`, **clean, zero conflicts.** The single
x3l7 commit touches only `src/config.rs` (unspecified-bind rejection +
`ListenAddressUnspecified` + 3 unit tests); main advanced by a breaking 0.2.0
change (`Store::register_store`) + a docs fold, neither touching `config.rs`. The
rebased branch builds as `mirror v0.2.0` and its `config.rs` change is intact.

## Fresh prometheus matrix evidence (on v11 `main`)

Ran on `prometheus.goldragon.criome` (cargo 1.96.0), source rsynced from the
rebased trees. All exit 0.

**spirit** (`criome-authorization-push` @ `21421448`):

| Config | Command | Result |
|---|---|---|
| neither | `cargo check` | Finished, exit 0 |
| criome-gate only | `cargo check --features criome-gate` | Finished, exit 0 |
| mirror-shipper | `cargo check --features mirror-shipper` | Finished, exit 0 |
| criome_gate_1of1 | `cargo test --features mirror-shipper --test criome_gate_1of1` | **3 passed** / 0 failed |
| new witness | `cargo test --features criome-gate,testing-trace --test observe_gate_1of1` | **2 passed** / 0 failed |

- `criome_gate_1of1`: `meta_configure_arms_and_clears_criome_gate_socket`,
  `socket_only_gate_observes_signed_auto_approved_authorization`,
  `authorized_head_ships_and_emits_projected_reference_denied_head_does_not_ship`.
- `observe_gate_1of1`: `armed_gate_observes_head_and_emits_authorization_trace_through_daemon`,
  `unarmed_gate_is_a_noop_through_daemon`.

**mirror** (`criome-auth-witness` @ `3933d11d`): `cargo test` — full suite green,
exit 0; the 3 x3l7 tests pass (`accepts_specific_tailnet_address`,
`rejects_ipv4_unspecified_address`, `rejects_ipv6_unspecified_address`).

## Flag — pre-existing warning (NOT introduced here; left out of scope)

The criome-gate and mirror-shipper spirit builds emit a benign
`unused imports` warning for five `signal_criome` authorization-flow types
(`AuthorizationObservation as SignalAuthorizationObservation`,
`AuthorizationPending`, `AuthorizationRequestSlot`, `AuthorizationStateRecord`,
`AuthorizationStatus`) at `src/criome_gate.rs:26-29`. Their only consumers live
in `#[cfg(feature = "agent-guardian")] impl SpiritOperationAuthorizer`
(`criome_gate.rs:450+`), while the `use` is unconditional — so **any** build
without `agent-guardian` warns, including v11 `main` itself under
`--features mirror-shipper`. This file is **not** touched by om4g.2, so the
warning is pre-existing in main's code, not a rebase artifact. Left unfixed to
keep the change minimal and preserve unrelated code.

**Recommended follow-up (trivial, separate change):** move those five imports
into a `#[cfg(feature = "agent-guardian")] use signal_criome::{...};` line so the
shipped-daemon (criome-gate-only) build is warning-clean. Requires re-verifying
the `agent-guardian` config.

## Files changed

- spirit `14575379`: `Cargo.toml`, `src/engine.rs`, `src/daemon.rs`, `src/lib.rs`
  (om4g.2 rebased; unchanged content from `4a017504`, re-merged onto v11).
- spirit `21421448`: `Cargo.toml` (new `[[test]]`), `tests/observe_gate_1of1.rs` (new).
- mirror `3933d11d`: `src/config.rs` (x3l7 rebased; unchanged content).

## Commands run (VCS / verification)

- `jj rebase -r 4a017504 -d main` (spirit, scoped), `jj rebase -r criome-auth-witness -d main` (mirror).
- `jj bookmark create criome-authorization-push-prerebase -r 4a017504` (preservation).
- `jj git push --bookmark …` × 3 (all landed; `@origin` aligned).
- prometheus: the matrix above via `ssh prometheus.goldragon.criome … cargo …`.
- Isolated jj workspaces (`spirit-cgv11`, `mirror-x3l7`) used for the rebases;
  both forgotten and removed after push. Repo paths claimed via Orchestrate for
  the duration, released at close. Default checkouts left clean on main.

## Blockers / follow-up requirements

- **Review the scope decision (H1):** the 4 dropped "authorization submit stream"
  commits are preserved on `criome-authorization-push-prerebase`. If that WIP is
  still wanted, the `spirit-auth-submit-stream` lane should rebase it onto v11
  separately (it needs its cross-repo criome/signal-criome/router branches
  rebased onto v11 first — a larger cross-repo integration, not this slice).
- The criome-gate-only build carries the pre-existing `agent-guardian`-gated
  unused-import warning (see Flag); trivial follow-up noted.
- Untouched by design: the authorization-gated / deploy-gated `primary-1e6b.*`
  beads. M2 (record explicit acceptance that node B ingress stays
  tailnet-ACL-only) is an acceptance action for the psyche, not a code change.
