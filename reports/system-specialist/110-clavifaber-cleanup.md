# 110 — Clavifaber cleanup pass

Big rename / re-shape / re-think pass through clavifaber, driven by
the user's directive after report-109's named-ugly-parts list.

## What landed

One clavifaber commit (bb0279ce) + one CriomOS commit (09d6b662) +
one workspace-skill-rule edit + one P1 security defect closed.

## Removals

| Removed | Why |
|---|---|
| `Converge` request, `InspectState` request, `ConvergenceComplete` / `StateReport` / `ConvergeLedger` response variants | Convergence is system-orchestration territory ("is the actual state matching the desired state?"). Belongs to lojix or whatever the cluster orchestrator becomes. Per the user: "ClaviFaber doesn't have to do anything about converge … there's no converge in ClaviFaber. We should take all of that out of there." |
| `src/state.rs` (sema-backed `State`, `ConvergenceLedgerEntry`, `InputHash`) | The convergence-ledger gate's whole reason was Converge. Without it, no need for a database in clavifaber. |
| `sema` and `redb` dependencies | No more durable state. |
| `flake.nix` chained `state-write` / `state-read` derivations | They witnessed convergence-ledger durability. Gone with convergence. |
| `WifiCertificate` actor + `EnsureWifiServerCertificate` / `EnsureWifiClientCertificate` messages | Was a forwarding helper to `CertificateIssuer` adding only idempotent-skip. Idempotency now lives directly on per-handler request types. |
| `SshHostKey` actor + `WritePublicKeyProjection` message-on-its-own-actor | Folded into `HostIdentity` — the projection is a method on the noun that owns the private key. |
| `PublicationCollector` actor | Forwarding helper without state; `PublicKeyPublicationWriting::execute` does the assembly inline. |
| `PublicKeyPublicationRequest` (legacy) | Per the user: "I don't know where this public key publication request is. If you don't know what it is, then you can remove it." |
| Clap CLI surface (`complex-init`, `derive-pubkey`, `ca-init`, `server-cert`, `node-cert`, `verify`) + `clap` dependency | NOTA-only operator interface per workspace discipline. The per-verb requests ARE the canonical CLI surface, just expressed as inline NOTA records. |
| `TextFile` wrapper + `ServerCertificateFiles` wrapper in `request.rs` | Two ways to write a file is one too many. `AtomicFile` direct is the one way. |
| Hand-rolled JSON parser `extract_private_key` | Replaced with `serde_json::from_slice` + `.get("PrivateKey").and_then(...)`. Two lines. Per the new no-hand-rolled-parsers skill rule. |
| `tests/converge.rs`, `tests/state_schema.rs` | Tested the removed surface. Substance migrated to per-handler tests. |

## Reshapings

### NOTA-only operator surface

Eight focused requests, each its own `NotaRecord`-deriving struct in
`src/request.rs`. One positional NOTA record per CLI invocation.

| Request | Replaces | What it does |
|---|---|---|
| `IdentitySetup` | `IdentityDirectoryInitialization` (renamed) + `complex-init` Clap command | Ensure SSH ed25519 host identity (key.pem + ssh.pub); idempotent. |
| `OpenSshPublicKeyDerivation` | `PublicKeyDerivation` (renamed) + `derive-pubkey` Clap command | Re-derive ssh.pub from persisted private key. |
| `CertificateAuthorityIssuance` | `CertificateAuthorityInitialization` (renamed) + `ca-init` Clap command | Sign a CA cert; idempotent on output existence. |
| `ServerCertificateIssuance` | `ServerCertificateCreation` (renamed) + `server-cert` Clap command | Mint P-256 keypair + cert; idempotent. |
| `ClientCertificateIssuance` | `NodeCertificateCreation` (renamed; "node" was confusing — it's an EAP-TLS *client* cert) + `node-cert` Clap command | Sign a client cert binding a host SSH ed25519 pubkey; idempotent. |
| `CertificateChainVerification` | `CertificateVerification` (renamed) + `verify` Clap command | Verify chain: issuer-DN match + **validity window** (NEW, primary-4kr) + signature. |
| `YggdrasilKeypairSetup` | NEW (was the Yggdrasil half of `Converge`'s `YggdrasilPlan`) | Generate per-host yggdrasil keypair file (mode 0600); return the static `(YggdrasilProjection address public_key)`. |
| `PublicKeyPublicationWriting` | NEW (was the publication half of `Converge`) | Assemble + atomically write `publication.nota` with typed identity / yggdrasil / wifi-cert fields. |

### Five actors (was eight)

```
RuntimeRoot
  ├── HostIdentity              (gains WritePublicKeyProjection by folding SshHostKey)
  ├── GpgAgentSession           (DelegatedReply over spawn_blocking — gpg-agent IO)
  ├── CertificateIssuer         (X.509 minting; uses signer-closure → GpgAgentSession)
  ├── YggdrasilKey              (DelegatedReply over spawn_blocking — yggdrasil binary)
  └── TraceRecorder (test only)
```

Removed: `WifiCertificate` (forwarding helper), `SshHostKey` (folded
into `HostIdentity`), `PublicationCollector` (forwarding helper).

### Typed publication wrappers

```rust
pub struct PublicKeyPublication {
    pub node_name: String,
    pub open_ssh_public_key: String,
    pub yggdrasil: Option<YggdrasilProjection>,         // NEW: typed wrapper
    pub wifi_client_certificate: Option<WifiClientCertificate>, // NEW: typed wrapper
}
```

`YggdrasilProjection { address, public_key }` and
`WifiClientCertificate { pem }` are PascalCase NOTA records, not
snake-case-string-with-`_pem`-suffix fields. Per the user: "I don't
understand this Wi-Fi client certificate M naming. Why is it in snake
case? Shouldn't that be a type? Shouldn't it be in Haskell case?"

### Per-handler idempotency

Every issuance handler skips when its output file(s) already exist —
no CA read, no gpg-agent traffic. Re-running clavifaber on an
already-set-up host is a fast no-op.

### Validity-window check on cert verification (primary-4kr P1, closed)

`src/x509.rs::CertificateChain::verify` reads
`tbs_certificate.validity.{not_before, not_after}` and rejects
out-of-window certs. Three witness tests in
`tests/certificate_validity_window.rs` cover expired, not-yet-valid,
and in-window cases (the in-window test asserts the validity check
happens BEFORE the signature check).

### `serde_json` for external-tool output

`src/yggdrasil.rs::extract_private_key` is now two lines using
`serde_json::Value::get`, replacing 17 lines of hand-rolled string
slicing.

## CriomOS knock-on

`modules/nixos/complex.nix` no longer issues a single `Converge` mega-
call. The `complex-init` systemd oneshot now sequences two NOTA-only
calls:

```sh
clavifaber '(IdentitySetup "/etc/criomOS/complex")'
clavifaber '(PublicKeyPublicationWriting <host> "/etc/criomOS/complex" None None "/etc/criomOS/complex/publication.nota")'
```

Yggdrasil keypair generation stays None for now — the consolidation
with `modules/nixos/network/yggdrasil.nix`'s own seed step is filed as
`primary-8b3` and lives separately from this cleanup.

The `clavifaber.redb` state file is no longer in the directory layout.
Existing CriomOS hosts will have the file leftover but unused; CriomOS
doesn't need to clean it up explicitly (next deploy doesn't write or
read it; an operator can `rm` it any time).

## New workspace-level skill rule

Added to `~/primary/skills/rust-discipline.md` §"No hand-rolled
parsers": if a format has a name (JSON, TOML, YAML, …), there's a
parser library — use it. Hand-rolled string-slicing parsers are
forbidden. Two carve-outs: trivial single-character splits and bare
`<integer>::from_str` parses.

The rule names two paths when no library exists: find one (almost
always exists), or write a real parser as its own micro-component
crate per `~/primary/skills/micro-components.md`.

## Beads filed during the work

- `primary-qp7` (P2, role:operator, repo:nota-codec): nota-codec's
  encoder must use `""" """` multiline syntax for strings containing
  newlines. Surfaced because the wifi-cert PEM (with embedded
  newlines) round-trip-fails through inline `"..."` encoding. Today
  the publication-writing test uses a single-line fixture PEM.

## Beads closed during the work

- `primary-4kr` (P1, security): validity-window check on
  `CertificateChain::verify`.

## Test surface — final state

| Test file | Tests |
|---|---|
| `tests/actor_topology.rs` | 2 (size + spawn) |
| `tests/actor_trace.rs` | 3 (ensure-identity, derivation ordering, yggdrasil ensure-then-read) |
| `tests/certificate_validity_window.rs` | 3 (NEW; primary-4kr witnesses) |
| `tests/forbidden_edges.rs` | 3 (gpg_agent, AtomicFile, yggdrasil ownership) |
| `tests/identity_directory_lifecycle.rs` | 6 (mode bits, idempotency, quarantine, derivation, mode stability, missing-key failure) |
| `tests/issuance_idempotency.rs` | 3 (NEW; CA / server / client skip on disk existence) |
| `tests/publication_writing.rs` | 2 (NEW; typed publication record + None-fields-omitted) |
| `tests/request_surface.rs` | 2 (NOTA round-trip + inline-NOTA dispatch) |
| `scripts/test-pki-lifecycle` | 8 phases (impure, real gpg + yggdrasil) |

24 cargo tests + 4 nix flake check derivations + 8 pki-lifecycle
phases. All green.

## Constraint witnesses (post-cleanup)

`ARCHITECTURE.md` now organises constraints into four tables, each row
mapping a sentence-form constraint to a same-named witness test.
Total: 23 witnesses guarded by tests, including 3 NEW for
validity-window and 3 NEW for per-handler idempotency.

## What clavifaber does NOT do (post-cleanup)

- Convergence orchestration (lives in lojix or future orchestrator)
- Cluster-side aggregation of publication files (haywire stage = SSH
  pull; future = primary-e3c)
- Rotation / renewal scheduling (parked; rotation will land on the
  actors that already own each plane)
- State persistence beyond filesystem (no sema, no redb, no daemon)

## Per-bead status after this pass

| Bead | Status |
|---|---|
| `primary-3t9` (YggdrasilKey actor) | Closed earlier (still landed; survives this cleanup with renamed surface) |
| `primary-ari` (WifiCertificate actor) | Closed earlier — but the actor itself is now removed; the wifi cert plane lives on `CertificateIssuer + per-handler idempotency` instead. The bead's intent (wifi cert lifecycle) is satisfied by the new `ClientCertificateIssuance` request and its idempotency witness. |
| `primary-jg1` (audit) | Closed earlier; this cleanup retightens the same constraints with a smaller surface. |
| `primary-7a7` (durable redb state + systemd convergence runner) | Closed earlier — but the artifacts it produced are now gone (state.rs, the chained Nix derivations, the convergence-runner shape). The bead represents a direction the workspace later reversed. **Worth flagging as a "shipped then reverted" entry in the lineage.** |
| `primary-4kr` (validity-window check) | Closed by this pass. |
| `primary-qp7` (nota-codec multiline encoder) | NEW; filed during this pass. |
| `primary-8b3` (clavifaber-as-sole-owner of yggdrasil keypair) | Open; still applies (the consolidation question with `network/yggdrasil.nix` is unchanged by this cleanup). |
| `primary-3m0` (umbrella: actors-per-concern) | 7 of 9 children closed; the cluster-side `primary-e3c` is parked. The umbrella's acceptance criterion ("no monolithic key setup script") is satisfied by the per-handler shape. |

## Next moves the user authorised

User asked for a systemd-nspawn test of clavifaber on a clean host
(after the cleanup landed). That's the next deliverable in this
session. It builds on the new shape — the multi-call CriomOS
complex-init script is what the nspawn-launched container will
exercise. Targeting a minimal CriomOS configuration (host identity
+ publication, no cluster CA in the sandbox).
