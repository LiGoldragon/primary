# 118 — criome auth: working implementation reference for main integration

*The psyche asked for "a working implementation we can base the main impl on."
This is the reference: what is built and tested on the `criome-auth-pilot` branch,
the cluster-root admission gate, and the exact contract delta the operator applies
to wire the gate into `RegisterIdentity` on main. Branch worktree:
`~/wt/github.com/LiGoldragon/criome/criome-auth-pilot`; four commits on `main`
`2a02cf4d`; local (not pushed). Builds offline; `clippy -D warnings` + `fmt` clean;
**31 tests green.***

## What is on the branch (the working implementation)

| Commit | What it delivers |
|---|---|
| real BLS master key + verify | `MasterKey` (`blst` min-pk: generate, load-or-generate 0600, sign), `VerifyBls` on `BlsPublicKey`, `Hexadecimal`; retires the placeholder. 4 unit tests. |
| wire real BLS through the actors | self-owned signing (criome signs as `Host("criome")`; caller in audit context), real `VerifyAttestation`; register→sign→verify=Valid, tamper→Invalid. |
| SO audit P1/P2/P3 fixes | startup master-key/registry reconcile (fail-loud, typed `Error::Startup`); expired→`Expired`; atomic-0600 key file + unsafe-file rejection; envelope-scheme check; full-statement preimage (binds content/signer/audit/validity/scheme); `start()` liveness check; ARCHITECTURE.md refreshed. |
| cluster-root admission gate | `admission.rs`: `RegistrationStatement` + `ClusterRoot::admits`; 4 tests (admitted / non-root-rejected / relabelled-rejected / malformed-rejected). |

Test coverage: 10 lib-unit (6 `master_key` + 4 `admission`) + 2 actor-discipline +
19 daemon = 31, all green.

## The admission gate (the trust-root, Spirit `ermr`)

A key is admitted into a criome registry only when the **cluster-root** signed it.
The working core (`src/admission.rs`):

- **`RegistrationStatement`** — the canonical, domain-separated bytes the cluster-root
  signs: `identity` + `public_key` + `purpose` (length-delimited, tagged). Built
  identically by the cluster-root signer and criome's verifier, so an admission is
  valid only for the exact identity↔key↔purpose binding.
- **`ClusterRoot`** — holds the configured trust-anchor public key; `admits(reg,
  admission)` = the admission envelope is issued under the cluster-root key **and**
  is a valid BLS signature over the statement. Reuses the real BLS path
  (`MasterKey::sign` on the signing side, `BlsPublicKey::verify_bls` on the
  verifying side).

This closes the **cryptographic half** of `kr40` — the self-asserted-registry gap the
SO audits flagged. What remains is the mechanical wiring (below) + production key
custody.

## Contract delta for `signal-criome` (the operator's main-integration step)

The gate verifies a cluster-root signature carried on the wire and a configured
trust anchor. Three additions to `signal-criome` (pre-production, break freely):

- `IdentityRegistration` gains `admission (Optional SignatureEnvelope)` — the
  cluster-root's signature over the registration statement (`Optional` so a
  dev/virgin daemon with no configured root still bootstraps).
- `CriomeDaemonConfiguration` gains `cluster_root (Optional BlsPublicKey)` — the
  trust anchor; `None` only in dev/virgin bootstrap.
- `RejectionReason` gains `UnauthorizedRegistration`.

After regenerating `signal-criome`, the `IdentityRegistration` construction sites in
criome (`on_start`, the daemon tests) take `admission: None` for the dev path; the
cluster-root-signed path supplies `Some(envelope)`.

## `register()` integration shape

`IdentityRegistry` holds an `Option<ClusterRoot>` (from
`CriomeDaemonConfiguration.cluster_root`, threaded via `RootArguments`). `register`
gates before storing:

```rust
async fn register(&self, registration: IdentityRegistration) -> CriomeReply {
    if let Some(root) = &self.cluster_root {
        match &registration.admission {
            Some(admission) if root.admits(&registration, admission) => {}
            _ => return rejection(RejectionReason::UnauthorizedRegistration),
        }
    }
    // ... existing duplicate-check + store path ...
}
```

criome's own `Host("criome")` self-registration in `on_start` is admitted the same
way: the cluster-root signs criome's master public key at provisioning, and that
admission is supplied with the self-registration (or, in dev/virgin mode with no
configured root, it self-admits — the transitional bootstrap, consistent with
`psc6`).

## Why this is a reference, not main itself

The contract additions touch `signal-criome` (a git-pinned contract crate) and need
a coordinated regenerate + repin + `nix flake check` — the operator's main lane.
The branch is left **local** (not pushed) per "push only when asked." The gate's
hard part — the cryptography and the admit/reject decision — is done and tested
here; the wire integration is mechanical.

## Remaining for trustworthy production auth

- Wire the admission gate into `RegisterIdentity` (the contract delta above) — then
  the registry is no longer self-asserted; `kr40` closes.
- Production key custody for both the master key and the cluster-root: `mlock`/
  `zeroize`/passphrase, and the eventual authenticated `meta-signal-criome` key
  configuration (supersedes the transitional `psc6` 0600-file bootstrap).
- The first cross-system trust edge (provisioning: the cluster-root signs each
  node's criome master key) — the deploy-time ceremony that makes the mesh
  non-circular.
