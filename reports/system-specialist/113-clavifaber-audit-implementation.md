# 113 — Clavifaber audit recommendations: implementation

The audit at report 112 named three near-term recommendations and
deferred two. This is the implementation closing report.

## What landed

| Recommendation | Status | Commit |
|---|---|---|
| Tighten `IdentitySetup` quarantine (PEM-shaped-but-wrong → loud fail, not quarantine) | landed | clavifaber `d4ce7802` |
| Parse-before-skip in CA / server / client cert handlers; loud-fail on unparseable; server cert fails on half-existence | landed | clavifaber `d4ce7802` |
| CriomOS complex-init operator-override sentinel `.disabled` | landed | CriomOS `29fcc8aa` |
| Cluster identity vs sshd identity — designer decision | filed | bead (designer P2) |
| `(SkipIfRegistered <db>)` pre-flight for ExecStartPre when cluster DB exists | filed | bead `primary-ncw` (P3) depending on `primary-e3c` |

Plus a script fix discovered while running pki-lifecycle end-to-end:
GPG keygrips starting with a digit (this run: `9B05...`) were being
lexed as `Int(9)` by the NOTA bare-identifier lexer. Five sites in
`scripts/test-pki-lifecycle` now quote the keygrip.

## Behaviour changes (operator-visible)

### Identity (IdentityDirectory.existing_identity)

Three buckets:

| On-disk state | Old behaviour | New behaviour |
|---|---|---|
| Absent | Generate fresh | Generate fresh (unchanged) |
| Present, valid Ed25519 PKCS#8 PEM | Load and use | Load and use (unchanged) |
| Present, not even a PEM block (e.g., literal "CORRUPT DATA") | Quarantine + regenerate | Quarantine + regenerate (unchanged) |
| **Present, PEM with WRONG LABEL** (e.g., `BEGIN CERTIFICATE`) | Quarantine + regenerate | **Fail loudly** — `Error::Corrupt`; the file is untouched |
| **Present, PEM with right label but wrong algorithm** (e.g., RSA private key written as `PRIVATE KEY`) | Quarantine + regenerate | **Fail loudly** — same as above |

The narrowed quarantine path means a structurally-typed file we don't
recognise can't silently rotate the host's identity. Operators get a
typed error and decide.

### Certificates (CA / server / client issuance)

| On-disk state | Old behaviour | New behaviour |
|---|---|---|
| Absent | Issue | Issue (unchanged) |
| Present, valid PEM cert | Skip | Skip (unchanged) |
| **Present, unparseable garbage** | Silently skipped (treated as "exists") | **Fail loudly** — `Error::Certificate`; the file is untouched |
| Server only: cert+key half-existence | Re-issued both (silently rotating the EC keypair) | **Fail loudly** — operator must delete both files together (or restore from backup) |

The loud-fail error messages name the offending path and the operator
action (`rm` to force re-issue, or restore from backup). Per-cert-kind
ergonomics in `clavifaber/skills.md` §"Force-rotate".

### CriomOS complex-init operator override

`unitConfig.ConditionPathExists = "!/etc/criomOS/complex/.disabled"`.
To lock clavifaber out of a specific host:

```sh
touch /etc/criomOS/complex/.disabled
```

The unit becomes a no-op; sshd / NetworkManager dependencies move on
without clavifaber running. Remove the sentinel to re-enable.

## Test surface — final state

31 cargo tests across 8 files; 4 nix flake check derivations; 8
pki-lifecycle phases; 1 rootless bwrap deployment test. All green.

| Test file | Tests |
|---|---|
| `tests/actor_topology.rs` | 2 |
| `tests/actor_trace.rs` | 3 |
| `tests/certificate_validity_window.rs` | 3 |
| `tests/forbidden_edges.rs` | 3 |
| `tests/identity_directory_lifecycle.rs` | 7 (+1 new: PEM-wrong-label) |
| `tests/issuance_idempotency.rs` | 9 (+6 new: CA/client loud-fail, server cert/key/half-cert/half-key loud-fail, valid-cert-skip path uses a real PEM fixture) |
| `tests/publication_writing.rs` | 2 |
| `tests/request_surface.rs` | 2 |
| `scripts/test-pki-lifecycle` | 8 phases (impure, real gpg + yggdrasil) |
| `scripts/test-deployment-sandbox` | 1 end-to-end (rootless bwrap container) |

## Deferred to follow-up beads

- **Designer question**: cluster identity vs sshd host identity. The
  two parallel Ed25519 host identities (audit §D) are the largest
  architectural smell. Filed for designer decision.
- **`(SkipIfRegistered <db>)` pre-flight**: depends on the cluster DB
  landing (primary-e3c, parked). The bead's body explains how to
  wire it as `ExecStartPre` when the substrate exists.

## What this changes for existing CriomOS hosts

Re-deploying after this lands on a host with valid existing keys:
**no behavioural change** — IdentitySetup loads the existing key, cert
handlers skip after parsing. The new code paths only fire on
abnormal disk state.

Re-deploying on a host with abnormal state (truncated cert, garbage
key, half-existence): **previously silent overwrite or rotation; now
loud failure**. Operator intervention required.

Re-deploying on a host where the operator has touched
`/etc/criomOS/complex/.disabled`: **complex-init does not run**.
Other systemd-managed concerns (sshd, NetworkManager) proceed
normally.
