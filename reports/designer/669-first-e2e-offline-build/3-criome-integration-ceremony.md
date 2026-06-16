# criome main-integration sequence + cluster-root provisioning ceremony

*Designer report 669, file 3. The live/gated track, second milestone. Companion
to the first-e2e-offline-build session. Grounds the operator handoff for the
cluster-root admission gate and designs the deploy-time provisioning ceremony
that makes the two-node mesh non-circular.*

## What is already true (grounded, not aspirational)

The admission gate is real and wired end-to-end on the designer branch. The
crypto is `blst` BLS12-381 min-pk, not the placeholder. Concretely:

| Surface | State | Location |
|---|---|---|
| `signal-criome` contract delta | PUSHED to origin, branch `criome-admission-gate`, tip `4b27b935` | `IdentityRegistration.admission (Optional SignatureEnvelope)`, `CriomeDaemonConfiguration.cluster_root (Optional BlsPublicKey)` + `with_cluster_root` builder, `RejectionReason::UnauthorizedRegistration` |
| `criome-auth-pilot` | LOCAL (unpushed), jj bookmark `criome-auth-pilot` at `47b1dd0d`, repo's `main` bookmark still at `tzkynmkvltxu` (sema locks) | gate threaded config → `CriomeDaemon` → `RootArguments` → `IdentityRegistry`; `register()` rejects unadmitted external keys; criome self-registers its own Host identity by direct store write (bypasses the gate as local authority) |
| `criome` MAIN | still ships placeholder + ungated `register()` | `src/actors/signer.rs:94` emits `criome-skeleton-bls-signature`; `src/actors/registry.rs:90` only dedups |
| `meta-signal-criome` | `NotBuiltYet` skeleton, but already cross-imports `signal-criome:lib:CriomeDaemonConfiguration` | `schema/lib.schema`: single `Configure(CriomeDaemonConfiguration)` op; replies `Configured`/`ConfigurationRejected`/`RequestUnimplemented` |
| Tests | 33 green incl. `cluster_root_gates_registration` (unadmitted → `UnauthorizedRegistration`, admitted → `IdentityReceipt`); clippy `-D warnings` + fmt + `nix flake check` clean as of SO audit 227 | `tests/daemon_skeleton.rs:560` |

Two facts the operator must not miss:

1. **The auth-pilot `Cargo.lock` pins `signal-criome` at `783cc2fab1c2`**
   (the contract-additions commit) **but the branch tip is `4b27b935`**
   (the nota-text fixture fix, SO audit 228 P1). The pin is one commit behind
   the pushed branch tip. This is *fine for compilation* — `783cc2fa` already
   carries the three contract additions — but the repin step below moves it to
   `main` anyway, which resolves the skew.

2. **There is no CLI command anywhere that signs a `RegistrationStatement`.**
   The only code that mints an admission is `cluster_root_admission(...)` inside
   the `admission.rs` test module and the inline body of
   `cluster_root_gates_registration`. The provisioning ceremony is therefore a
   genuine gap, not a wiring oversight — see the second half of this report.

## Part 1 — Operator main-integration checklist

Code repos: designers ship feature branches in `~/wt/...`; **operator owns main
and the rebase/repin**. This is the operator's checklist, in strict order. Every
`jj`/`git` message is inline (`-m`); never an editor.

### Step 0 — preflight (operator confirms the starting state)

- [ ] `signal-criome` origin has bookmark `criome-admission-gate` at `4b27b935`
      and `main` at `fb3fa444` (the schema-runtime-lock refresh). Confirm:
      `jj -R /git/github.com/LiGoldragon/signal-criome bookmark list --all`.
- [ ] `criome` MAIN still has the placeholder (`grep criome-skeleton-bls-signature`).
- [ ] auth-pilot bookmark `criome-auth-pilot` is at `47b1dd0d`, tests green
      locally before integration: `nix flake check` inside the auth-pilot
      worktree (it was green at SO audit 228; re-confirm after any rebase).

### Step 1 — land `signal-criome` `criome-admission-gate` → `signal-criome` main

The contract is the upstream dependency; it merges first so criome can repin to
main. The branch is a clean superset of main (three additive record fields +
fixtures), so a fast-forward / linear move is the intent.

- [ ] Move `main` to the branch tip:
      `jj -R /git/github.com/LiGoldragon/signal-criome bookmark set main -r criome-admission-gate`
      (if main has advanced since `fb3fa444`, rebase the branch onto main first;
      there is no conflicting change so it should be clean).
- [ ] Push: `jj -R /git/github.com/LiGoldragon/signal-criome git push --bookmark main`.
- [ ] Optionally delete the now-merged branch on origin once main carries it.
- [ ] Sanity: `nix flake check` in `signal-criome` (the nota-text fixtures were
      the SO audit 228 P1 fix — this is what guards regeneration drift).

### Step 2 — repin `criome` (auth-pilot) to `signal-criome` main

- [ ] In the criome `Cargo.toml`, the dependency becomes
      `signal-criome = { git = "https://github.com/LiGoldragon/signal-criome.git", branch = "main" }`
      (auth-pilot currently says `branch = "criome-admission-gate"`).
- [ ] Refresh the lock so it resolves to the new main commit:
      `cargo update -p signal-criome` (this also clears the `783cc2fa` vs
      `4b27b935` skew — both are now subsumed by main).
- [ ] `cargo build` + `cargo test`; expect the same 33 green.

### Step 3 — merge `criome-auth-pilot` → `criome` main

This is the substantive landing: the whole BLS core + admission gate replaces
the placeholder. The auth-pilot is a separate jj repo whose `origin` is the
criome GitHub repo, so this is an integrate-into-main, not a branch push.

- [ ] Bring the auth-pilot content onto criome main. Because auth-pilot's own
      `main` bookmark is the stale `tzkynmkvltxu` and the work is on
      `criome-auth-pilot` (`47b1dd0d`), the operator either (a) advances main to
      the branch tip in this repo and pushes, or (b) cherry-picks/rebases the
      four-commit stack (BLS core / actor wiring / P1 fixes / admission gate +
      scheme-check) onto the real criome main. Recommend (a): the auth-pilot
      *is* the integration worktree.
      `jj -R ~/wt/github.com/LiGoldragon/criome/criome-auth-pilot bookmark set main -r criome-auth-pilot`
      then push main to origin.
- [ ] Confirm the placeholder is gone from main:
      `grep -r criome-skeleton-bls-signature` returns nothing.
- [ ] Confirm `register()` on main carries the `Option<ClusterRoot>` gate.

### Step 4 — whole-system check

- [ ] `nix flake check` on integrated criome main (build + test + clippy + fmt;
      this is the gate that was green at SO audit 227/228 — it must stay green).
- [ ] Spot-run the daemon binary: `criome-daemon <signal-file.rkyv>` with a
      configuration carrying no `cluster_root` (virgin/dev) and confirm it binds
      a `0600` socket and serves one `RegisterIdentity` (the existing
      `criome_daemon_signal_frame_registers_identity` path).

### Step 5 — close the loop

- [ ] Note on bead `primary-kr40` (the real-blst/signed-RegisterIdentity work):
      signal-criome admission contract on main; criome main carries the gate;
      `nix flake check` green. Remaining kr40 items stay open: production key
      custody and the provisioning ceremony (Part 2).
- [ ] The repo `INTENT.md` for criome and signal-criome should already describe
      the gate; if main's `INTENT.md` predates it, update on the same integrate.

**Do NOT in this milestone:** build the ceremony CLI, encrypt the key file, or
build out meta-signal-criome. Per the psyche directive of 2026-06-16
("lets not worry about key encryption for now"), key custody and the daemon-level
self-admission ceremony are deferred; the active push is
networking-through-the-router. Part 2 is the *design* for when that track
resumes, not work to land now.

## Part 2 — the cluster-root provisioning ceremony

### The three Spirit anchors

- **`ermr` (trust root, Decision, Medium):** "a cluster-root identity signs
  member keys, and that signature is criome registry admission gate
  (RegisterIdentity requires a valid root signature); cross-system peers trust
  keys chained to the cluster root. This … gives a non-circular first
  cross-system-trust bootstrap." This is the *what*. The ceremony is its *how*.
- **`psc6` (key custody, Decision, Medium):** "criome generates its master BLS
  keypair on first run and persists the secret to a `0600` key file; the secret
  never leaves criome. Transitional bootstrap until meta-signal-criome carries
  an authenticated key config." This governs the *member-node* key. The ceremony
  must also say where the *cluster-root* secret lives — psc6 doesn't, and the
  cluster-root key is a different, more sensitive secret.
- **`kr40` (bead, P1):** the work item. Its notes already specify the deferred
  ceremony: "the cluster-root provisioning ceremony (deploy-time: cluster-root
  signs each node's criome master key → the criome self-admission)."

### Who is cluster-root, and where its secret lives

The cluster-root is a **distinct BLS keypair that is not any node's criome master
key.** Each node's criome daemon already has its own master key (psc6); the
cluster-root is the trust anchor *above* them. Modeling it as a `MasterKey`
instance (the same type, a different secret) is correct and already supported —
`MasterKey::generate` / `load_or_generate` / `sign` are all that a signer needs,
and `ClusterRoot::new(public_key)` is the verifier side.

Custody recommendation, consistent with psc6's transitional spirit but explicit
about the higher stakes:

- The cluster-root secret is **operator-custodied, off the member nodes.** It
  lives on the deploy/bootstrap host (the machine the operator runs the ceremony
  from), as a `0600` file, the same `MasterKey` persistence the daemon uses.
  Reusing `MasterKey::persist` (atomic `create_new` + `mode(0o600)` + `fsync`,
  unsafe-file rejection on load) means the cluster-root file gets the same
  hardening the master key already has — no new custody code.
- It is **never** placed on a member node and never travels over the working or
  meta socket. Only its *public* key reaches a node, as `cluster_root` inside
  `CriomeDaemonConfiguration`.
- For the live pilot this is a single human/operator-held secret. The eventual
  model (post-deferral) is the same one psc6 names for the master key: an
  authenticated `meta-signal-criome` config delivers it. The cluster-root secret
  itself never needs meta delivery — only its public key does.

This keeps a clean asymmetry: **public keys travel; secrets don't.** The
cluster-root public key travels to every node (as a trust anchor) and the member
public key travels to the cluster-root (to be signed); neither secret moves.

### How a member node's master key gets an admission signature

This is the missing primitive. A member node's daemon, on first run, generates
its master key (psc6) and self-registers its own `Host(criome)` identity by
direct store write — that path bypasses the gate as the local authority and is
*already implemented*. But for the node to be admissible into *another* registry
(and for any *external* identity, e.g. a `Developer` or `Agent` principal, to be
admitted into a node's registry), someone must sign a `RegistrationStatement`
with the cluster-root secret. The `RegistrationStatement` canonical bytes are
`CRIOME-REGISTRATION-ADMISSION-V1 || identity-tag || purpose-tag ||
len-prefixed(identity-name) || len-prefixed(public-key)` — already defined in
`admission.rs` and shared verbatim by signer and verifier.

Three candidate mechanisms:

**Option A — a one-shot `criome` CLI admission-signing command (RECOMMENDED).**
Add a subcommand to the bundled thin CLI (the daemon's first client) that the
*operator* runs on the deploy host, holding the cluster-root secret. It takes one
NOTA argument describing the target binding (identity + public key + purpose) and
emits a `SignatureEnvelope` (the admission). Shape, obeying the one-argument /
method-only / typed-noun rules:

```
criome "(AdmitRegistration (<cluster-root-key-path> (IdentityRegistration <identity> <public_key> <fingerprint> <purpose> None)))"
  -> prints a SignatureEnvelope NOTA document (the admission)
```

The owning noun is a `RegistrationAdmission` (or the existing `ClusterRoot`
gaining a `sign_admission(&MasterKey, &IdentityRegistration) -> SignatureEnvelope`
companion to `admits`). It is *not* a daemon operation: it is a local,
offline, secret-holding act, exactly like `git tag -s`. The daemon never sees the
cluster-root secret; it only verifies the resulting envelope. This matches the
"CLI is the daemon's first client, not a triad leg" rule and the
"one argument, no flags" rule — the cluster-root key path and the binding are one
NOTA object.

Why A over the others: it is the smallest non-circular primitive, it keeps the
cluster-root secret off every daemon and off every wire, it reuses the exact
`RegistrationStatement` bytes the gate already verifies (no second
implementation), and it is the natural deploy-time step ("operator signs each
node's key"). It is also testable as a pure function — the same path
`cluster_root_gates_registration` already exercises inline.

**Option B — `meta-signal-criome` `Configure` carrying the admission.** Rejected
as the *signing* mechanism. The meta plane configures a daemon (socket, store,
`cluster_root` *public* key); it is the right channel to *deliver the trust
anchor* but the wrong place to *mint* admissions. Minting requires the
cluster-root *secret*, which must never reach a daemon. `Configure` stays
public-key-only. (Meta *does* have a role — see the deploy sequence.)

**Option C — an external authority (e.g. spirit/Developer key).** Rejected for
the first live pilot as over-scoped. `ermr` is explicit that the cluster-root is
criome's own trust anchor for a non-circular bootstrap; introducing an external
authority re-opens the circularity question (who admits the external authority?).
A is the bootstrap; C is a later federation story.

### The non-circular two-node mesh deploy sequence

The circularity worry: "node B trusts the cluster-root, but who tells node B the
cluster-root key, and who signs node B into node A?" The break is that **the
cluster-root is provisioned *before* either node and is the same anchor for
both** — it is not derived from either node.

```mermaid
sequenceDiagram
    participant Op as Operator (deploy host, holds cluster-root SECRET)
    participant A as Node A criome daemon
    participant B as Node B criome daemon

    Note over Op: 0. generate cluster-root keypair once (0600, off both nodes)
    Op->>A: 1. Configure: socket, store, cluster_root = ROOT_PUB (virgin start)
    Op->>B: 1. Configure: socket, store, cluster_root = ROOT_PUB (virgin start)
    Note over A: 2. first run: generate master key (psc6),<br/>self-register Host(criome) via direct store write
    Note over B: 2. first run: generate master key (psc6),<br/>self-register Host(criome) via direct store write
    A-->>Op: 3. export master PUBLIC key
    B-->>Op: 3. export master PUBLIC key
    Note over Op: 4. criome AdmitRegistration: sign A's key into B's registry,<br/>and B's key into A's registry (offline, cluster-root secret)
    Op->>B: 5. RegisterIdentity(A-binding + admission)  -> IdentityReceipt
    Op->>A: 5. RegisterIdentity(B-binding + admission)  -> IdentityReceipt
    Note over A,B: 6. mesh: each registry holds the peer's<br/>cluster-root-admitted key; attestations cross-verify
```

The acyclic dependency order is: **cluster-root keypair → node master keys →
admissions → cross-registration.** No step depends on a later one. The
cluster-root is the single shared upstream; both nodes chain to it without
chaining to each other. That is precisely the "non-circular first
cross-system-trust bootstrap" of `ermr`.

Two refinements:

- Step 1 (`Configure` with `cluster_root`) is the **legitimate meta-plane role**:
  the public anchor is delivered as `CriomeDaemonConfiguration.cluster_root`,
  which is exactly the field that already exists and which meta-signal-criome
  already cross-imports. For the deferred/pre-meta state, the same record is the
  binary startup config the daemon decodes — startup and meta reconfiguration
  share the one definition (the SHARED-TYPE OWNERSHIP note in
  meta-signal-criome's schema). So no new contract is needed for delivery.
- Step 5 uses the *ordinary* `RegisterIdentity` path with the admission slot
  populated — the path the gate already enforces. The operator is the client; in
  production the registering principal would carry its own admission.

### Should the first live e2e run gated or via the dev self-admit hatch?

**Recommendation: the first live e2e runs GATED (configured `cluster_root`).**

Reasoning:

- The whole point of this milestone (`ermr`, `kr40`) is that the registry is "no
  longer self-asserted when a cluster root is configured." A first e2e that runs
  *ungated* would demonstrate the old, broken posture the SO audits 225/226
  called out, and would not exercise the admission gate at all.
- The gated path is fully tested (`cluster_root_gates_registration`) and needs
  only the one missing piece — the Option A signing command — to be operable by
  a human rather than inline test code. That command is small.
- The virgin/self-admit hatch (`cluster_root: None`) should remain, but scoped to
  exactly two uses: (1) a node's own `Host(criome)` self-registration, which is
  already a direct-store-write bypass independent of the hatch, and (2)
  single-node dev/unit runs where there is no peer to trust. It is the *escape
  hatch for development*, explicitly not the live posture.

The one honest caveat: running gated requires the Option A admission-signing
command, which **does not exist yet**. So the literal "first live e2e" is gated
*only after* that small command lands. Until then, a developer can demonstrate
the gate inline (as the test does) but cannot run it as an operator ceremony.
This is the single remaining blocker between "wired" and "operable gated e2e",
and it sits behind the current networking-through-the-router priority by psyche
directive.

## Open decisions for the psyche / other lanes

1. **Cluster-root custody depth.** psc6 covers the member master key but not the
   cluster-root secret. Confirm the recommended posture (operator-held `0600`
   file on the deploy host, public key delivered via `Configure`) or record a new
   custody Decision for the cluster-root specifically. This is a candidate Spirit
   `Record` (a new Constraint/Decision distinct from psc6) once the psyche
   re-engages the key-custody track.
2. **When to build the Option A admission CLI.** It is the only missing piece for
   a gated live e2e and is small (one CLI subcommand + a `sign_admission` method
   beside `ClusterRoot::admits`). Currently deferred behind
   networking-through-the-router. The psyche or operator decides whether to pull
   it forward when the router milestone needs a real two-node trust mesh.
3. **Whether the operator integrates Part 1 now.** Part 1 (landing the contract +
   gate to main) is independent of the deferred custody/ceremony work and could
   land immediately to remove the placeholder from criome main. Confirm the
   operator should integrate now vs. hold until the router track needs it.
