# Rust Auditor Review — Persistent Spirit A→B Mirror, Non-Gated Front

## Task and scope

Independent audit of the landed non-gated front of the persistent Spirit A→B
mirror slice, before the gated deploy chain (VM authoring → deploy → gate-arming
→ shipper enable) builds on it. Two code changes plus two disposition beads:

- `mirror` `c2e4fed8` (branch `criome-auth-witness`) — x3l7, reject unspecified
  TCP bind at `TryFrom<DaemonConfiguration>`.
- `spirit` `4a017504` (branch `criome-authorization-push`) — om4g.1/om4g.2, new
  `criome-gate` cargo feature + `observe_gate_head` + daemon dispatch.
- sos8 (checkout disposition) and 85hv (shipper confirmation).

## Files and commands consulted

- Evidence: `GeneralCodeImplementer-BeadEvidence.md`, `TrackerWeaver-WeavePlan.md`.
- `mirror/.../src/config.rs`, `src/service.rs`, `src/schema_daemon.rs` @ `c2e4fed8`.
- `spirit/.../Cargo.toml`, `src/daemon.rs`, `src/engine.rs`, `src/lib.rs`,
  `src/criome_gate.rs`, `src/trace_event.rs`, `src/shipper.rs`.
- `jj` inspection: commit identities, push state, bookmark divergence,
  merge-bases, ancestry, per-config cfg gating, network-ingress sweep.
- Read-only Spirit `PublicTextSearch` for mirror-ingress intent → no matching
  public record (negative evidence; grounding taken from the weave plan's cited
  psyche acceptance of the tailnet-bind stopgap).
- NOT run: `cargo build`/`test`. Local Rust build fails at `max-jobs=1` per the
  task constraint; no `/nix/store` search. Green results are the implementer's
  prometheus evidence — see H1 for why that evidence does not cover the tree the
  gated chain must build on.

## Verdict

The two code changes are individually correct and follow workspace Rust
discipline. **The front is NOT yet safe for the gated chain to build on as-is**,
because there is no single coherent tree. Both changes live on unmerged feature
branches, and the spirit branch diverges from `main` *before* the strict-positional
v11 store migration, so its green prometheus evidence does not cover the
post-rebase tree. Must-fix items below (H1, plus M1/M2 to accept) precede the
gated chain.

## Findings by severity

### HIGH

**H1 — om4g.2 landed on a branch that diverges from spirit `main` before the v11
migration; its build evidence does not cover the tree the gated chain needs.**
`criome-authorization-push` (`4a017504`) is pushed to `@origin` but is **not
merged to `main`** and **`main` (05269499) is not an ancestor of it**. The
merge-base is `9e413baa9a` (spirit 0.19.0). `main` independently advanced through
the strict-positional signal-spirit v11 + v10→v11 store migration; the branch
does not contain it. Concretely, `main` changed files the branch lacks:
`src/engine.rs` (+39), `src/production_migration.rs` (+1132),
`src/store/mod.rs`, `Cargo.toml`, `Cargo.lock`, `tests/mirror_shipper.rs`. The
branch's own `Cargo.lock` pins `signal-spirit 5d0905a7` (pre-strict-positional);
`main` pins `151d49c8`. The branch itself edits `engine.rs` and `Cargo.toml`, so
a rebase onto `main` **will conflict** in at least those two files.
Consequence: the prometheus matrix (`cargo check` × 3 configs, `cargo test
--features mirror-shipper`) was green against the *old* contract base, not
against v11 `main`. The gated slice `1e6b.5` (enable `mirror-shipper` on current
`main`) has no coherent tree today — `main` lacks `criome-gate`, the branch lacks
v11. This directly contradicts the sos8 framing that "the slice builds from a
clean pushed rev."
Correction: rebase `criome-authorization-push` onto spirit `main` (resolve
`engine.rs` / `Cargo.toml`), re-run the 3-config check matrix +
`criome_gate_1of1` on prometheus, and only then treat the front as landed.

### MEDIUM

**M1 — No runtime witness for the criome-gate-only observe path (the actual
om4g.2 shipped-daemon behavior).** `spirit/src/daemon.rs:171-174` dispatches
`observe_gate_head()` under `cfg(all(criome-gate, not(mirror-shipper)))`, but no
test carries `required-features = ["criome-gate"]`; the only behavioral witness,
`criome_gate_1of1`, requires `mirror-shipper` and exercises the *other* method
`gate_and_ship_head`. `observe_gate_head` is referenced by no test. So the
shipped-daemon config is only compile-checked (`cargo check --features
criome-gate`) — its observe/emit behavior and the non-overlapping dispatch are
unproven at runtime. Per the architectural-truth-tests rule, a newly admitted
config needs an end-to-end boundary witness, not a compile check.
Correction: add a `criome-gate` (+`testing-trace`) witness proving an armed gate
emits `AuthorizationObjectName::Observed` and an unarmed gate is a no-op
(`Ok(None)`), driven through the daemon `handle_working_input` boundary.

**M2 — x3l7 is bind-hardening, not authenticated ingress; the receiver still
accepts unauthenticated appends.** `is_unspecified()` rejects only `0.0.0.0`/`::`;
it does **not** verify the bound address is within the tailnet CGNAT range, and
the TCP ingress applies **no per-request auth** — `service.rs` `WorkingSignal`
states verbatim "no per-request auth; criome deferred," treating any TCP peer as
working traffic straight into `engine.handle`. Any peer that can route to the
specific bound port can append to node B's mirror store unauthenticated. This is
the psyche-accepted interim (weave plan; 85hv 2026-06-13), but the *security
intent* "authenticated ingress" is not met by this slice — it rests entirely on
(a) the tailnet ACL and (b) the deploy choosing a non-public bind address, which
the check does not enforce. The meta tier is structurally Unix-only
(`MetaOrder`); the TCP path is the sole network ingress and it is now the only
bind site (sweep confirms one `TcpListenerDaemon`, no other listener), so there
is no *bypass* of the check — but the check's protection is narrow.
Correction (acceptance, not code): make explicit before enabling the shipper
that node B ingress is tailnet-ACL-only and depends on a correct specific bind
address; the per-request criome/BLS attestation remains deferred (x3l7 real fix /
router-attestation variant).

### LOW / residual

- **L1** — In a plain `criome-gate` production build (no `testing-trace`), the
  observe path has no durable effect: `daemon.rs` discards the result
  (`let _ = engine.observe_gate_head().await;`) and the trace record is
  `#[cfg(feature = "testing-trace")]`. Each working commit still performs a
  criome socket round-trip (`spawn_blocking`) whose outcome is thrown away — cost
  with no recorded signal. The deploy must also enable `testing-trace` (or
  `mirror-shipper`) for om4g.2 to produce any observable effect.
- **L2** — The "never bind unspecified" invariant is enforced only at the config
  boundary. `Service::new(engine, SocketAddr)` is `pub` and accepts any address;
  production is safe (only `schema_daemon.rs:61` constructs it from a validated
  `Configuration`), but the invariant is not defended at `Service::new`/bind.
  Defense-in-depth note.
- **L3** — `accepts_specific_tailnet_address` uses `127.0.0.1` and labels it
  "tailnet." The test proves "a specific address is accepted," not "a tailnet
  address," and would equally accept a public IP — which is exactly the M2 gap.
  A test asserting acceptance of a specific *public* IP would document the known
  limitation honestly.
- **L4** — The mirror x3l7 change also diverges from mirror `main` (b8cf8eca) by
  one docs commit (merge-base 5102f5ed); `c2e4fed8` is pushed to `@origin` but
  unmerged. Trivial to reconcile (docs vs `config.rs`, no overlap), but the front
  is two unmerged feature branches, not a landed integration.

## Rust discipline (confirmed positive)

- Typed errors at boundaries: `ConfigurationError::ListenAddressUnspecified` and
  `ObserveGateError` (thiserror, `#[from] StoreError` / `#[from] CriomeGateError`)
  — no anyhow at edges.
- Feature graph correct and non-overlapping across all three configs:
  `criome-gate = [dep:criome, dep:signal-criome]`;
  `mirror-shipper = [criome-gate, dep:mirror, dep:signal-mirror]`; daemon
  dispatch `cfg(all(criome-gate, not(mirror-shipper)))` vs `cfg(mirror-shipper)`
  are mutually exclusive. `versioned_log_head` cfg correctly relaxed to
  always-compiled (needed by the observe path, `pub` → no dead-code warning);
  `criome_gate.rs` imports no mirror-only types, so the criome-gate-only config
  has no compile-out gap. (Compile-verified on prometheus per evidence — on the
  divergent base; see H1.)
- No hand-rolled parser: address via `str::parse::<SocketAddr>()`; unspecified
  check via std `SocketAddr::ip().is_unspecified()` (correct for both v4-any and
  v6-any). Method-on-data-bearing-type discipline and full-word names hold.
- sos8 confirmed: `spirit-strict-positional-v11` = `main` = `@origin` =
  `05269499`; pushed, no dirty work lost.
- 85hv confirmed: `MirrorShipper` (`configure`, `ship_unshipped`,
  `publish_checkpoint`, `is_armed`, `address`) present under `mirror-shipper` on
  `main`.

## Must-fix before the gated chain proceeds

1. Rebase `criome-authorization-push` onto spirit `main`, resolve
   `engine.rs`/`Cargo.toml`, and re-run the 3-config check matrix +
   `criome_gate_1of1` on prometheus (H1). Rebase `criome-auth-witness` onto
   mirror `main` (L4).
2. Add a `criome-gate`-only runtime witness for `observe_gate_head` (M1).
3. Record explicit acceptance that node B ingress remains unauthenticated
   (tailnet-ACL + correct non-public bind), before `mirror-shipper` is enabled
   (M2).

## Provisional / follow-up (not authority)

- Consider enforcing "bound address must be a tailnet address" (CGNAT
  100.64.0.0/10) rather than merely "not unspecified," if the psyche wants the
  bind check to carry more of the trust boundary. Currently deferred by design.
- Consider whether arming `criome-gate` in production without `testing-trace`
  (L1) is intended, given it does criome work per commit with no recorded outcome.
