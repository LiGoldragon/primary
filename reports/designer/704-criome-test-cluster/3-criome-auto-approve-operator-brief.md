# 704-3 — Operator brief: criome auto-approve + Configure impl

For the operator lane (criome `main` owner). Designer supplies the contract
piece + this precise spec; operator integrates the runtime, because criome is
operator's live hot zone — three criome commits landed today (`1eaa783`,
`6ce7decd "add meta approval socket"`, …) while designer kept colliding off
stale checkouts. Division: **designer owns the signal-criome contract addition +
the nixosTest; operator owns the criome runtime on main.**

## Goal (Spirit `t00s`, `da5i`)

criome's verdict can be a configured **auto-approve** acceptance policy: every
well-formed `EvaluateAuthorization` is `Authorized` without quorum evidence — the
simplest verdict source, lets spirit→criome→mirror run for bootstrap/test. And
implement `Configure` (currently `NotBuiltYet`) so the meta socket does its
minimal job ("all components need a meta socket, even if just to configure them"
— `da5i`), setting the mode at runtime.

## Contract piece — DONE, ready to integrate

`signal-criome` branch **`criome-meta-authz`** (`080a527b`, off current main
`caa02a9`): adds `AuthorizationMode [Quorum AutoApprove]` and an
`authorization_mode` field to `CriomeDaemonConfiguration` (preserving
`MetaSocketPath`); `new()` defaults `Quorum`, `with_authorization_mode(...)`
setter + `authorization_mode()` accessor; regenerates clean,
`SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS=1` freshness green. Merge/rebase into
signal-criome main, then criome consumes it.

## Runtime spec (criome, against current `6ce7decd`)

Exact injection points (verified against `6ce7decd`):

1. **`src/actors/root.rs` — thread the mode onto `CriomeRoot`.**
   - Import `signal_criome::AuthorizationMode`.
   - `CriomeRoot` gains `authorization_mode: AuthorizationMode` (and a
     `configuration_generation` counter for `Configure`'s reply).
   - `Arguments` gains `pub authorization_mode: AuthorizationMode`;
     `Arguments::new` defaults `AuthorizationMode::Quorum`.
   - `CriomeRoot::new` takes the mode; `on_start` passes
     `arguments.authorization_mode` into `Self::new(...)`.

2. **`src/actors/root.rs` — auto-approve short-circuit** in the
   `CriomeRequest::EvaluateAuthorization(evaluation)` arm of `submit`, BEFORE the
   `(key_registry, contract_store)` lookup:
   ```rust
   if matches!(self.authorization_mode, AuthorizationMode::AutoApprove) {
       if &evaluation.object.digest != evaluation.evidence.operation.object_digest() {
           return rejection(RejectionReason::MalformedRequest);
       }
       let decision = EvaluationDecision::Authorized;
       self.publish_authorized_object_update(AuthorizedObjectUpdate {
           object: evaluation.object,
           contract: evaluation.contract.clone(),
           decision: decision.clone(),
           stamp: evaluation.evidence.stamp.clone(),
       }).await;
       return CriomeReply::AuthorizationEvaluated(AuthorizationEvaluated {
           contract: evaluation.contract,
           decision,
       });
   }
   ```
   Keeps the structural object/operation-digest integrity check; skips only the
   quorum. Publishes the authorized object so propagation proceeds.

3. **`src/actors/root.rs` — implement `Configure`** in `submit_meta` (replace the
   `RequestUnimplemented(NotBuiltYet)` arm): apply the runtime-changeable config
   — `self.authorization_mode = configuration.authorization_mode().clone()` (and
   cluster_root if desired) — increment the generation, reply
   `meta_signal_criome::Output::configured(Configured { generation })`. Socket/
   store rebinding stays out of scope (not runtime-changeable).

4. **`src/daemon.rs` — thread config → root.** `CriomeDaemon` gains
   `authorization_mode` (default `Quorum` in `new`); `from_configuration` reads
   `configuration.authorization_mode().clone()`; `bind()` passes it into
   `RootArguments`.

The `criome-write-configuration` encoder needs no change for the test path: the
daemon starts `Quorum`, then the test flips it to `AutoApprove` over the meta
socket via `Configure` — exercising the meta socket end-to-end.

## The proof (designer owns — `CriomeOS-test-cluster`)

A second check `criome-cluster-auto-approve`: a witness that (a) over the meta
socket (`CriomeMetaClient`) sends `Configure(config.with_authorization_mode(
AutoApprove))` → expects `Configured`; (b) over the working socket sends an
`EvaluateAuthorization` with threshold-short (zero-signature) evidence → expects
`Authorized`. Proves the meta socket, runtime reconfiguration, and auto-approve
together. Lands once the runtime above is on criome main.

## Why this division

Operator has out-paced designer on criome all day; the contract + test are the
clean designer surface, the runtime is operator's. If the psyche prefers,
designer will instead prototype the runtime on a branch off current `6ce7decd`
and hand it for rebase — but that re-enters the collision zone.
