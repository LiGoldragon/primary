# 111 — Clavifaber existing-host integration audit

The user asked: what could go wrong when CriomOS deploys clavifaber's
`complex-init` to a host that **already has key material** — could
clavifaber overwrite a good key and break things downstream?

Two ideas the user surfaced:

1. **Per-step existence check** — every step asks "does this already
   exist?" before creating.
2. **Disable the service** when all the host's public keys are
   already in the cluster database.

Below: what's already there, what could still bite, and a weighing
of the two ideas.

## What clavifaber does on a re-run today

After the cleanup pass (report 110), each request handler is
idempotent on disk-existence:

| Request | Re-run behaviour |
|---|---|
| `IdentitySetup` | Loads the existing private key if parseable; **quarantines** (renames to `key.pem.broken.<unix-seconds>`) and **regenerates** if unparseable; generates fresh if absent. Always rewrites `ssh.pub` from whatever identity is in scope. |
| `OpenSshPublicKeyDerivation` | Reads existing private key; rewrites `ssh.pub` (always — that's the verb). Fails (correctly) if no private key is present. |
| `CertificateAuthorityIssuance` | `if output.exists() { skip; return Ok(...) }`. Doesn't read the file. |
| `ServerCertificateIssuance` | `if cert.exists() && key.exists() { skip; return Ok(...) }`. Doesn't read either file. |
| `ClientCertificateIssuance` | `if cert.exists() { skip; return Ok(...) }`. Doesn't read it. |
| `CertificateChainVerification` | Read-only; never mutates. |
| `YggdrasilKeypairSetup` | YggdrasilKey actor's `ensure` returns early if the file exists. Doesn't read it. |
| `PublicKeyPublicationWriting` | Always re-assembles + atomic-writes `publication.nota`. The publication has no private bytes; cheap to rewrite. |

So the per-step existence check (idea 1) is **already implemented**
for IdentitySetup, the three cert handlers, and YggdrasilKeypairSetup.
The remaining audit is about *what the existence check doesn't catch*.

## Risks for existing hosts (categorised)

### A. The `IdentitySetup` quarantine path is too eager

`HostIdentity::EnsureIdentity` → `IdentityDirectory::existing_identity`
(`src/identity.rs:21`) does:

```
if !key.pem.exists() → return None (handler will generate fresh)
else load_identity():
  Ok(id)  → return Some(id)
  Err(e)  → quarantine (rename key.pem → key.pem.broken.<seconds>)
            and pretend it didn't exist (return None → handler generates fresh)
```

The Err branch fires on **any** parse failure: `SigningKey::from_pkcs8_pem`
returning an Err. That error covers:

- File contents are not valid PEM at all (genuine corruption)
- File contents parse as PEM but the inner DER isn't PKCS#8 PrivateKey
- File contents are PKCS#8 but for a non-Ed25519 algorithm
- File was truncated mid-write (shouldn't happen if AtomicFile is the
  only writer, but possible if a prior non-AtomicFile path wrote it)
- File has a stray BOM or unexpected whitespace that the PEM parser
  rejects in a future ed25519-dalek version

The first two are real "this is not a usable Ed25519 host key" cases
where quarantine + regenerate is right. **The last three could
quarantine a perfectly good key on a host that's been running for
years**, replacing the host's identity silently. Downstream cluster
trust (the cert that binds the old public key, the SSH known_hosts
entry on every peer) breaks.

**Severity**: medium-high. Probability is low but consequence is
expensive (rotate the host's identity across the cluster).

### B. Cert-file existence checks are naive

The three cert handlers use bare `.exists()`. If a cert file exists
but is **truncated, garbage, or a half-written PEM**, we skip and the
host has a broken cert.

Symptom path:

1. Operator manually copies a backup cert that's truncated mid-PEM
2. Re-deploy: clavifaber sees the file exists, skips
3. NetworkManager / wpa_supplicant tries to use the cert, fails
4. Operator confused: "I redeployed, why isn't it working?"

**Severity**: low-medium. Existence-not-equals-validity is a known
class of footgun.

### C. `ServerCertificateIssuance` half-existence

Current: `if cert.exists() && key.exists() { skip }`. If the cert is
deleted but the key survives (or vice versa), clavifaber re-mints
both. The new cert + new key pair is internally consistent, but
**anyone who trusted the OLD public key now can't verify the new
cert**. The old key file (still on disk before re-issuance) gets
overwritten by the new key — silently.

**Severity**: low (operator-induced; "I deleted half the pair" is
already abnormal).

### D. Two parallel SSH ed25519 host identities

This is the biggest "wait, what?" finding.

CriomOS today has TWO Ed25519 host keys per host:

1. `/etc/ssh/ssh_host_ed25519_key` — managed by `services.openssh`,
   used by sshd as the host identity, and by the nix dispatcher as
   the SSH client identity (referenced in `modules/nixos/nix.nix:151`).
2. `/etc/criomOS/complex/key.pem` — managed by clavifaber, named
   "node identity" by `IdentityDirectory`, used in the cluster
   wifi-PKI client cert and the `publication.nota` projection.

Both are Ed25519. Both are "this host's identity". Neither knows
about the other. The horizon-built trust list
(`dispatchersSshPubKeys`, `nix_pub_key_line`) names key (1). The
publication.nota names key (2). If a peer ever needs to correlate
"the SSH-host-key fingerprint" to "the cluster-PKI identity", they
can't — the host has two identities and the system's records use
different ones depending on the consumer.

This isn't a regression from the cleanup — it predates clavifaber's
introduction in CriomOS. But it surfaces in any audit of "what
clavifaber touches on existing hosts".

**Question for the user**: should clavifaber's cluster identity BE
`/etc/ssh/ssh_host_ed25519_key` (read-only consumer of what sshd
already manages), or is the parallel identity intentional?

**Severity**: high architectural concern; low immediate-breakage risk
for existing hosts (because clavifaber writes to a separate path,
it doesn't overwrite sshd's key).

### E. Yggdrasil keypair conflict (already filed as primary-8b3)

Today: clavifaber's `YggdrasilKeypairSetup` creates a keypair file at
the operator-named path; the existing `modules/nixos/network/yggdrasil.nix`
also seeds its own keypair via its preStart. If both run, two yggdrasil
identities per host — the publication carries one, the daemon uses the
other.

For the current CriomOS deploy, complex-init passes `None` for the
yggdrasil field, so clavifaber doesn't touch the yggdrasil plane.
**No active conflict today**, but the bead's still open.

### F. No "force-reissue" path

Per-step idempotency means: once a key/cert exists, clavifaber
preserves it forever. There's no `--force` flag, no "rotate this
specific concern", no envvar override. If an operator decides "this
host's wifi cert is compromised, re-issue it", they have to manually
delete the cert file before re-running clavifaber. That works but
it's undocumented and easy to get wrong (delete the wrong file →
breakage).

**Severity**: low (operator-side workaround works); discoverability
is the real cost.

### G. No "skip everything" operator override

There's no `CLAVIFABER_DISABLE=1` envvar or sentinel-file check that
says "this host is already provisioned correctly; the systemd unit
should exit 0 without touching anything". The systemd unit always
runs all steps; idempotency means it does no work in the steady
state, but it still spawns the actor runtime, opens directories, and
checks file existence. Cheap, but not zero.

For a host with strict "do not modify keys" policy (e.g., a HSM-
backed identity), even the existence-check approach isn't enough —
the operator wants the unit to never invoke clavifaber.

**Severity**: low; discoverability gap.

### H. `complex-init` runs `before NetworkManager.service sshd.service`

CriomOS's unit ordering puts complex-init early in boot. That's right
for "make sure the host has its identity before networking" but it
also means **complex-init runs every boot, even when nothing needs to
change**. Idempotency keeps the cost bounded (~milliseconds), but the
host's boot path now depends on clavifaber not breaking.

If a future clavifaber version has a bug that makes
`HostIdentity::EnsureIdentity` fail (e.g., a wrong PEM library
upgrade), every CriomOS host's boot fails on complex-init's
`Type=oneshot, RemainAfterExit=true` unit, and sshd doesn't start
because of the `before` ordering.

**Severity**: medium. The mitigation is robust testing of the
identity flow (which we have) and the ability to remove/disable
complex-init without rebuilding the OS.

### I. No transactional rollback

If a deploy produces a corrupted clavifaber output (CA cert that
doesn't verify, a yggdrasil keypair file with wrong shape), the
host's keys are mutated. To restore: hand-restore from backup. There
is no transactional revert. (For SSH host key on
`/etc/ssh/ssh_host_ed25519_key`, sshd doesn't roll back either, so
this isn't a clavifaber-specific gap.)

**Severity**: low (no realistic rollback path for cryptographic
identity in any shape).

## The two user-proposed approaches, weighed

### Idea 1: per-step existence check

**Status**: already done. The cleanup made it explicit; it's the
default behaviour of every cert handler and YggdrasilKeypairSetup.

**Refinements worth making** (covered in "Recommendations"
below):

- Parse the existing file before declaring it valid (catches risk B).
- Don't quarantine on every parse failure — quarantine only when we
  can prove the file is unrecoverable, not when a single library
  version disagrees about format (refines risk A).

### Idea 2: disable the service when all keys are in the cluster DB

**Pure version**: clavifaber queries the cluster DB; if our public
keys are registered, exit. Skip everything.

**Why this is the right shape long-term**: the cluster IS the source
of truth for which hosts are admitted. A host coming up should ask
"am I already known here?" before doing anything irreversible.

**Why it's premature today**: the cluster DB doesn't exist yet
(haywire stage = each host writes publication.nota to a public-
readable path; the consumer-side aggregation is `primary-e3c`,
parked). There's nothing to query.

**Near-term variant that *does* fit today's stage**: a
**sentinel file** at `/etc/criomOS/complex/.provisioned` (or in the
host's lojix-projected horizon view). The systemd unit's
`unitConfig.ConditionPathExists = "!/etc/criomOS/complex/.provisioned"`
gates it: if the operator has marked the host as provisioned, the
unit doesn't run. The operator removes the sentinel to re-enable
runs.

This is mechanically simple (a one-line systemd condition + a
one-time `touch` after the first successful deploy) and gives the
operator the "this host is locked, don't touch it" override that's
missing today (risk G).

### My recommendation: do both, in stages

1. **Now (low-risk fixes)**: parse-before-skip in cert handlers; back
   off the IdentitySetup quarantine to the truly-unrecoverable case;
   document the "delete file to force re-issue" path.
2. **Next (operator override)**: add the sentinel-file
   `ConditionPathExists` gate in CriomOS's complex-init unit.
3. **Future (cluster DB pre-flight)**: when the cluster DB lands
   (`primary-e3c`), add a clavifaber CLI verb `(SkipIfRegistered <db-path-or-url>)`
   that exits 0 if the host's public keys are already registered.
   Wire that as `ExecStartPre` on complex-init.

## The two-SSH-identities question is independent of this audit

Risk D (two parallel Ed25519 host keys) is real but not a new
breakage from the cleanup. It deserves a designer report and possibly
a workspace-wide decision: should the cluster identity be the SSH
host key, or a separate identity? Answering it would simplify
clavifaber considerably (no more `IdentitySetup`; just consume
`/etc/ssh/ssh_host_ed25519_key`) but might lose flexibility (separate
rotation cadences, separate compromise scope).

I'm filing this as a separate bead rather than acting on it in this
audit.

## Recommendations — what to do now

1. **`CertificateAuthorityIssuance`** / **`ServerCertificateIssuance`** /
   **`ClientCertificateIssuance`**: change the skip check from `file.exists()`
   to "file exists AND parses as a CertificateDer (or as a valid
   private key for the server-key file)". If existence-but-not-parseable,
   either fail loudly OR quarantine + re-issue. **Decide the policy
   per-handler**:
   - CA cert: quarantine + re-issue (CA can be re-derived from the
     same GPG key; downstream certs that referenced the old CA cert
     by issuer-DN still verify).
   - Server cert + private key: **fail loudly** (re-issuance loses
     the old EC private key permanently; never silently rotate).
   - Client cert: quarantine + re-issue (the cert binds the host's
     SSH ed25519 public key, which is stable; new client cert is
     functionally equivalent if the SSH key is the same).
   
2. **`HostIdentity::EnsureIdentity`**: narrow the quarantine to "the
   PEM body exists but is structurally not Ed25519 PKCS#8" rather
   than "any decode error". Specifically: if the file isn't even valid
   PEM, that's a different failure (not a key-format mismatch); fail
   loudly rather than quarantine. **The quarantine path is the most
   destructive thing clavifaber can do; tighten it.**

3. **CriomOS `complex-init` unit**: add
   `unitConfig.ConditionPathExists = "!/etc/criomOS/complex/.disabled"`.
   An operator who wants to lock out clavifaber on a specific host
   does `touch /etc/criomOS/complex/.disabled`. Documented escape
   hatch.

4. **Documentation** in `clavifaber/skills.md`: add a section on
   force-rotate and lock-out, naming the file paths an operator
   manipulates to control the deployment.

## Code changes I'll land if you say "do it"

I haven't implemented the recommendations yet — the changes shift
behaviour in ways that affect production hosts (specifically the
"fail loudly when output exists but is unparseable" path), so this
audit goes to you for a yes/no first.

Concretely, the diff would be:

- `src/request.rs`: add a `parse_existing` helper used by each cert
  handler before the skip; per-handler policy on parse-failure (fail
  vs quarantine vs re-issue) per recommendation 1.
- `src/identity.rs`: split the quarantine check between "not even
  PEM" (fail) and "PEM but wrong key type" (quarantine), per
  recommendation 2.
- `CriomOS/modules/nixos/complex.nix`: add the sentinel
  `ConditionPathExists` per recommendation 3. Plus `systemd.tmpfiles.rules`
  for the sentinel-directory if needed.
- `clavifaber/skills.md` + `ARCHITECTURE.md`: document the operator
  override and force-rotate paths.

Witness tests for each:

- `tests/issuance_idempotency.rs` extended: garbage-cert-file +
  `CertificateAuthorityIssuance` → quarantine + re-issue; same for
  client cert; **server cert with garbage cert-or-key → fail with
  typed Error**.
- `tests/identity_directory_lifecycle.rs` extended: not-even-PEM
  private key → fail (not quarantine); PEM-but-wrong-algorithm →
  quarantine.

## Beads to file (if you greenlight)

- `clavifaber: tighten HostIdentity quarantine; quarantine only on
  PKCS#8/algorithm mismatch, not on PEM-parse failure` (P2,
  role:system-specialist).
- `clavifaber: per-cert-handler parse-before-skip with explicit
  per-kind failure policy` (P2, role:system-specialist).
- `CriomOS: complex-init operator-override sentinel
  /etc/criomOS/complex/.disabled` (P3, role:system-specialist;
  small change).
- `clavifaber: cluster identity vs sshd host identity — designer
  question` (P2, role:designer; the architectural question from
  risk D).
- (Future, when cluster DB exists) `clavifaber:
  (SkipIfRegistered <cluster-db>) verb for ExecStartPre`
  (P3, role:system-specialist; depends on primary-e3c).

## What's already safe

For the avoidance of doubt, these are **not** breakage risks today:

- Re-deploying complex-init on a host with a valid existing key:
  IdentitySetup loads, no overwrite, ssh.pub re-derives identically.
- Re-issuing CA / server / client certs with all output files present:
  skip, no re-issue, no gpg-agent traffic.
- Concurrent complex-init invocations on one host: AtomicFile's
  rename is atomic; only one wins; the loser gets a typed Err. The
  steady state after the race is internally consistent (one
  identity), just non-deterministic which.
- Re-running with the same yggdrasil keypair path: skip, no rotation
  (witness in `tests/...` for both yggdrasil test paths).

The risks above are **edge cases**, not happy-path failures. The
happy path is in good shape.
