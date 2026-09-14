# Criome-authorized Lojix activation — boundary audit at the call sites

Flow 6cc91b subflow. Read-only audit; nothing built, nothing run. Every
`file:line` below was opened or grepped in this flow (WITNESSED) unless the
line is marked CLAIMED.

Driving vision (flows/024bc7/vision/criome.md, 2026-09-13): *"Criome should
essentially take over the authentication layer of Lojix to deploy to have a
root call on the host that needs to activate the operating system."*

---

## 1 · The current admission path of a Lojix activation

WITNESSED, step by step. Repo `/git/github.com/LiGoldragon/lojix`.

1. **Two sockets bound.** `src/daemon.rs:138-155` binds `ListenerRole::Ordinary`
   and `ListenerRole::Owner` with configured modes. CriomOS defaults:
   `/run/lojix/ordinary.sock` 0660, `/run/lojix/meta.sock` 0600
   (`CriomOS/modules/nixos/lojix.nix:99-124`).
2. **Connection dispatch.** `src/daemon.rs:429-434` routes by listener role.
   Deploy lives only on the owner branch.
3. **The only authentication check in the whole path.**
   `src/daemon.rs:463` — `self.owner_authority.authorize(connection.context())?`.
   Implementation `src/daemon.rs:337-358`: a Unix peer is admitted iff its
   kernel-vouched `SO_PEERCRED` uid *and* gid equal the daemon's own effective
   uid/gid (`src/daemon.rs:330-334`, `rustix::process::geteuid/getegid`); a TCP
   peer is refused outright (`Error::UnauthorizedOwnerTcpPeer`).
   **That is the entire admission decision.** No signature, no attestation, no
   identity beyond "same uid as the daemon process".
4. **Frame decode.** `src/daemon.rs:464-466` reads the `meta-signal-lojix`
   frame. `Deploy` and `Test` decouple onto job actors
   (`src/daemon.rs:472-480`); everything else runs synchronously.
5. **Content validation (not authentication).** `src/schema_runtime.rs:2618-2651`
   — `meta::Input::Deploy` runs four rejections in order:
   `unsupported_deploy_reason`, `deployment_routing_rejection`,
   `proposal_source_rejection`, `source_revision_policy_rejection`, then
   records `RecordDeploySubmitted`. These validate *shape and routing*, never
   *who asked*.
6. **The root call.** `src/schema_runtime.rs:5455-5478` (`HostActivation::ssh_invocation`)
   builds the remote command:
   `nix-env -p /nix/var/nix/profiles/system --set <store> && <store>/bin/switch-to-configuration <boot|switch|test>`
   and hands it to `src/schema_runtime.rs:5240-5251`:

   ```rust
   NixCommand::new("ssh", vec!["-o".into(), "BatchMode=yes".into(),
                               self.ssh_destination.clone(),
                               remote_command.into_text()])
   ```

   The destination is a request-carried verbatim `user@host`
   (`src/schema_runtime.rs:5197-5216` validates only that it is one nonempty
   login plus host). `src/schema_runtime.rs:5226-5238` classifies the login:
   `"root"` → `RemoteUserActivationAuthority::RootMediated`; matching user →
   `MatchedUser`; anything else → `UnprivilegedMismatch`, refused at
   `src/schema_runtime.rs:6102-6113`. BootOnce wraps the same script in
   `systemd-run` on the target (`src/schema_runtime.rs:5503-5512`).

### What it trusts today

- **The daemon's uid.** Anyone who can run a process as the lojix service
  account can deploy. Under CriomOS that account is an unprivileged operator
  user, not root (`CriomOS/modules/nixos/lojix.nix:56-64, 234-235`; the option
  carries no default — CLAIMED that production sets an unprivileged account,
  since no host inventory was found in that repo).
- **The socket file mode**, 0600 on the meta socket.
- **Ambient SSH.** The daemon activation path passes *only* `-o BatchMode=yes`.
  No `IdentityFile`, no `IdentitiesOnly`, no `UserKnownHostsFile`, no
  `StrictHostKeyChecking`, no `IdentityAgent none` (WITNESSED: grep for those
  options over `src/schema_runtime.rs` returns nothing; only `BatchMode` at
  `:5246`). So the deploy borrows the daemon user's ambient `~/.ssh/config`,
  agent, and known_hosts, and the target host's `root` `authorized_keys` is the
  real authorization decision — made outside Lojix entirely.
- **Contrast, same repo:** the daemon-free `lojix-bootstrap` path *does* carry
  explicit credential policy — `src/bootstrap.rs:1474` writes a private
  `Host *` config with `IdentityFile`, `UserKnownHostsFile`,
  `GlobalKnownHostsFile /dev/null`, `StrictHostKeyChecking`,
  `IdentitiesOnly yes`, `IdentityAgent none`, and `src/bootstrap.rs:1497`
  passes them again on the command line. The daemon path has no equivalent.
- Lojix's own ARCHITECTURE.md:327-332 already names this as owed work
  (Spirit `h03z`): credentials "custodied and authenticated through criome
  rather than borrowing the operator's logged-in session (GPG/SSH agent)."

---

## 2 · What Criome can already assert — and whether Lojix references it

### Criome's assertions (WITNESSED)

- **Identity.** `Identity.[ Persona.PrincipalName Host.PrincipalName
  Developer.PrincipalName Agent.PrincipalName Cluster.PrincipalName ]`
  — `signal-criome/ethos/signal.ethos:123`. Registry actor at
  `criome/src/actors/registry.rs`.
- **Signing.** `AttestationSigner` holding a `MasterKey`
  (`criome/src/actors/signer.rs:21-27`); real BLS12-381 min-pk via `blst`;
  the secret never leaves the process (`criome/src/master_key.rs:1-13, 36-37`).
- **Verification.** `AttestationVerifier::verify`,
  `criome/src/actors/verifier.rs:40-112`: content-reference match, signer
  resolution, revocation, key match, scheme (min-pk only), BLS check, expiry.
  Decisions `VerificationDecision.[ InvalidSignature UnknownSigner
  ReplayAttempted Valid Revoked Expired ]`
  (`signal-criome/ethos/signal.ethos:93`).
- **Authorization.** `AuthorizationCoordinator`
  (`criome/src/actors/authorization.rs:15-17, 84-237`);
  `evaluate_authorization` at `criome/src/actors/root.rs:1033-1059` dispatches
  on `AuthorizationMode.[ AutoApprove ClientApproval Quorum ]`.
  Grant shape: `AuthorizationGrant.{ AuthorizationRequestSlot
  AuthorizedObjectReference AuthorizationPolicySatisfaction
  SignatureAuthorizationResult Vector<StampedSignatureEnvelope> Identity
  TimestampNanos Option<TimestampNanos> }`
  (`signal-criome/ethos/signal.ethos:180`).
- **The already-existing hook.** `AuthorizedObjectReference.{ ComponentKind
  ObjectDigest AuthorizedObjectKind }` and
  `ComponentKind.[ Message Router Criome Mind Spirit Persona Agent Mirror
  Introspect Harness Terminal System **Lojix** Orchestrate ]`,
  `AuthorizedObjectKind.[ Time Operation Contract Agreement Head ]`
  — `/git/github.com/LiGoldragon/signal/ethos/interface.ethos:7`.
  **A Lojix operation is already a namable authorized object today.**
  Criome's signer already encodes the `Lojix` tag when signing a grant
  (`criome/src/actors/signer.rs:222`).
- **Sockets.** Ordinary (`signal-criome/ethos/signal.ethos:13-46`) carries
  `Sign`, `VerifyAttestation`, `AttestAuthorization`, `EvaluateAuthorization`,
  `VerifyAuthorization`, `AuthorizeSignalCall`, `ObserveNodePublicKey`, quorum
  verbs. Meta (`meta-signal-criome/ethos/signal.ethos:14-28`) carries
  `Configure`, `InitiateRootFounding`, `AcceptRootFounding`,
  `SubmitAuthorizationApproval`, `FetchParkedRequests`, `AnswerParkedRequest`,
  intercept-policy admin.
- **"Root" in Criome is root-of-trust, not OS root.**
  `criome/src/founding.rs:1-14, 56-64, 230-243` — a unanimous BLS founding
  ceremony seeding the registry's trust anchor. No exec, spawn, or
  `Command::new` anywhere in `criome/src`.

### Does Lojix reference any of it? WITNESSED grep

```
$ cd /git/github.com/LiGoldragon/lojix
$ grep -rni "criome" --include='*.rs' --include='*.toml' --include='*.nix' . | grep -vi criomos
tests/common/mod.rs:59:                string: "criome".to_owned(),
tools/tests/common/mod.rs:61:                string: "criome".to_owned(),
```

Two hits, both a cluster-name string in a test fixture. **Zero references in
`src/`, `nexus/`, `clients/`, `tools/src/`, or `Cargo.toml`.** Lojix has no
criome dependency, no criome client, no attestation type. Symmetrically,
`grep -rni 'lojix\|deploy\|activat\|nixos-rebuild'` over criome yields only the
`ComponentKind::Lojix` tag (`criome/src/actors/signer.rs:222`), a test fixture
(`criome/tests/daemon_skeleton.rs:173`), and prose comments. `activat` and
`nixos-rebuild` have zero hits in criome.

This confirms Codex's finding: Criome-authorized activation is absent at every
activation site.

---

## 3 · How router consumes Criome attestation — the working example

WITNESSED, `/git/github.com/LiGoldragon/router`.

- **Sign.** `criome_attestation.rs:137-174` (`sign_forward`) builds a
  `ForwardContentPreimage` over origin identity + full payload
  (`:280-329`, domain-separated blake3), wraps it in a criome `SignRequest`
  (`:144-149`), and sends it through `criome_client.rs:42-47`
  (`CriomeRequest::Sign`) over the Unix socket at `config.criome_socket_path`
  (`criome_client.rs:83-115`). On failure it returns `unattested()`
  (`criome_attestation.rs:257-274`) — real digest, **empty signature**, so the
  far side must reject it.
- **Verify.** `criome_attestation.rs:180-192` re-derives the digest from the
  wire-claimed origin plus the received payload, reconstructs the `Attestation`
  (`:198-218`), and calls `criome_client.rs:53-65`
  (`CriomeRequest::VerifyAttestation`). Gate at `criome_attestation.rs:238-249`:
  **only `VerificationDecision::Valid` passes**; every other decision *and*
  every transport error collapse to one refusal,
  `RouterForwardRefusalReason::z2VLzK`. Fail-closed.
- **Call site.** `router.rs:381-388` — `verifier.verify(...)` runs in
  `TailnetForwardIngress::handle_forward` *before* the forward is applied;
  failure returns `ForwardRefused`. Outbound signing at `peer_delivery.rs:221`.
- **Identity bootstrap.** `router.rs:1107-1145` asks criome
  `ObserveNodePublicKey` with five retries and backoff; if criome never
  answers it pins `UNRESOLVED_CRIOME_HOST_ID` and can then sign or verify
  nothing — degraded, still fail-closed.
- **Enablement.** `daemon.rs:114-135`: a configured `criome_socket_path`
  constructs the real `CriomeForwardAttestation` + `CriomeIdentityProver` and
  requires encrypted peer sessions; `None` falls back to the plaintext
  `AcceptFixedTestIdentity` stand-in (`forward_attestation.rs:60-141`).
- **Router never runs crypto itself** (`criome_client.rs:8-9`,
  `criome_attestation.rs:7`) — it asks a colocated criome over a Unix socket.
  `CriomOS/modules/nixos/persona-router.nix:46-56` hardwires that socket to
  `/run/criome/criome.sock` with the comment that the criome module must be
  co-resident.

**The shape to copy:** a thin client crate, a preimage the two sides derive
identically, one verdict enum, one fail-closed gate placed *before* the effect.

---

## 4 · The gap, stated precisely

The single decision that separates "a byte arrived on a socket" from "a root
shell runs `switch-to-configuration switch` on a production node" is
`src/daemon.rs:463`: an integer comparison of uid and gid. Everything after it
validates shape, never principal.

Consequently:

- **No principal is recorded.** A `DeployHandle` and every durable deploy row
  carry a deployment identifier and routing snapshot; they carry no identity of
  who requested the activation. There is nothing to audit, revoke, or replay-check.
- **No attestation is verified.** Criome can already verify BLS attestations
  and already names `ComponentKind::Lojix` / `AuthorizedObjectKind::Operation`
  as an authorized-object coordinate — and Lojix asks it nothing.
- **The root call is authenticated by the host, not by the fleet.** The real
  gate is `root@target`'s `authorized_keys` plus the daemon user's ambient SSH
  agent. A compromised operator session is a fleet-wide root compromise, with no
  second factor and no per-deploy record.
- **The daemon activation path is weaker than the bootstrap path in the same
  repo** (§1, `bootstrap.rs:1474` vs `schema_runtime.rs:5246`).
- **Both daemons are already Unix-socket neighbours by design**
  (criome 0660 working socket, `CriomOS/modules/nixos/criome.nix:16-23`), so
  the transport the router uses is available to Lojix unchanged. Whether lojix
  and criome are in fact enabled on the same hosts is CLAIMED-unknown: CriomOS
  holds modules only, no host inventory.

---

## 5 · Proposed contract for Criome-authorized activation

A proposal, not a decision. Written in the existing ethos/signal style
(`meta-signal-lojix/ethos/signal.ethos`).

**Which side asks:** Lojix asks. The `lojix-meta` client obtains a Criome
attestation over the deploy request it is about to send; `lojix-nexus` asks
Criome to verify it. Criome stays a pure decision service and gains no
knowledge of deploys, exactly as it stays ignorant of routes today.

**Which side verifies:** Criome verifies the signature and evaluates the
authorization; Lojix enforces the verdict. Lojix runs no crypto — the router
precedent (`criome_client.rs:8-9`).

**Where the root call happens:** unchanged, `schema_runtime.rs:5240-5251`.
Criome does not gain an exec path and must not. The new gate sits in
`daemon.rs::serve_owner`, immediately after `owner_authority.authorize` at
`:463` and before `submit_deploy` at `:472` — so a refused activation never
reaches a durable row, let alone an ssh.

**The preimage:** a canonical digest over `(ClusterName, NodeName,
GenerationArtifact, RequestedDeploymentAction, DeploymentTransport,
SourceRevisionPolicy, ImmutableRevision)` — i.e. `DeploymentRequestIdentity`,
which `signal-lojix/ethos/signal.ethos:70` already defines. That record is the
natural `ObjectDigest`; no new preimage type is needed. The attestation's
`ContentReference.ContentPurpose` would need one new variant,
`HostActivation`, alongside the existing
`[ ChannelGrant SignedObject ChannelRetract PrivilegeElevation Authorization
Archive ComponentRelease ]` (`signal-criome/ethos/signal.ethos:212`) — or it
reuses `PrivilegeElevation`, which is arguably what an activation is.

**Signal variants** (added to `meta-signal-lojix/ethos/signal.ethos`):

```
; new records
  ActivationAttestation.{ ObjectDigest Identity SignatureEnvelope TimestampNanos ReplayNonce }
  AttestedDeploySubmission.{ DeploySubmission ActivationAttestation }
  ActivationAuthorizationRejection.{ ActivationRefusalReason DatabaseMarker }
  ActivationRefusalReason.[ AttestationInvalid SignerUnknown SignerRevoked
                            AttestationExpired ReplayAttempted
                            AuthorizationDenied AuthorizationPending
                            CriomeUnavailable ]

; the Deploy variant becomes attested
  Deploy.AttestedDeploySubmission

; new reply variant
  DeployUnauthorized.ActivationAuthorizationRejection
```

Lojix-side error: `Error::UnauthorizedActivation { reason }`, sibling of the
existing `UnauthorizedOwnerPeer` / `UnauthorizedOwnerTcpPeer`
(`src/lib.rs:203`).

Criome side needs **no new verbs**: the existing ordinary `Sign` /
`VerifyAttestation` / `EvaluateAuthorization` and the existing
`AuthorizedObjectReference{ ComponentKind::Lojix, digest,
AuthorizedObjectKind::Operation }` already express this. Escalation to a human
is the existing meta-socket `SubmitAuthorizationApproval` /
`FetchParkedRequests` path — which is also what flows/6cc91b/vision/secrets.md
describes ("you'll get notified that something needs to get access").

**Offline behaviour — fail closed, with one deliberate exception.**
Criome unreachable ⇒ `DeployUnauthorized(CriomeUnavailable)`, mirroring
`criome_attestation.rs:238-249`. Under criome's `Quorum` mode an unreachable
peer leaves the round pending indefinitely (`criome/src/actors/root.rs:2038-2040,
2467-2469`) and an unfounded node returns terminal `AuthorizationUnavailable`
(`root.rs:1509-1533`); Lojix maps `Pending` to `AuthorizationPending` and does
not block the connection. The one exception is `lojix-bootstrap`: it is the
authorized daemon-free crossing (ARCHITECTURE.md §1) and runs before any
criome exists on a new host, so it keeps its explicit private-key SSH policy
and is out of this contract. **Open question for the psyche:** whether a
production host that cannot reach criome should be undeployable — the vision's
plain reading says yes.

**The smallest witness test.** A pure policy test with no daemon, no build, no
network — the exact shape of `tests/owner_peer_authority.rs:13-20`:

```
tests/activation_attestation_authority.rs
  activation_authority_accepts_valid_criome_verdict()
  activation_authority_rejects_invalid_signature()
  activation_authority_rejects_when_criome_unreachable()   // fail-closed
  activation_authority_rejects_digest_mismatch()           // attestation over a different DeploymentRequestIdentity
```

over a trait `ActivationAuthorizable` with a stub verdict source, sitting
beside `PeerAuthorizable` in `src/daemon.rs`. The fourth case is the one that
matters: it proves the attestation binds *this* deployment, not merely that
some signature verified.

---

## 6 · Unknowns

1. **Is criome enabled on the hosts lojix deploys to, and on the operator
   workstation?** CriomOS holds modules only; no host inventory was found in
   that repo. Unresolved.
2. **Which identity signs a deploy** — `Identity::Developer` (the operator),
   `Identity::Agent` (an agent flow), or `Identity::Cluster`? The vision's
   "root call on the host" suggests the *host* must also be satisfied, which
   would mean a second gate target-side, not just daemon-side.
3. **Does the target-side root call itself become criome-mediated?** Today
   Lojix ssh's as root. The vision may mean Criome replaces the SSH key
   entirely — a criome-authorized local activation agent on each node — which
   is a much larger change than gating the socket. Not decided here.
4. **`ContentPurpose::PrivilegeElevation` vs a new `HostActivation` variant** —
   a contract-owner decision.
5. **Replay window and clock.** Criome gates votes on local clock
   (`criome/tests/witness_clock_gate.rs:1-24`); the activation attestation needs
   a stated freshness window. Not proposed here.
6. **Nothing was built or run.** Every claim is source reading. No compile, no
   test execution, no live socket was exercised.

---

## Sources

- `/git/github.com/LiGoldragon/lojix` — `ARCHITECTURE.md`, `Cargo.toml`,
  `src/daemon.rs`, `src/schema_runtime.rs`, `src/bootstrap.rs`, `src/lib.rs`,
  `src/ingress.rs`, `tests/owner_peer_authority.rs`, `tests/common/mod.rs`
- `/git/github.com/LiGoldragon/criome` — `ARCHITECTURE.md`, `src/actors/{signer,verifier,authorization,root,registry}.rs`,
  `src/{master_key,founding,conveyance,deploy_encode}.rs`, `tests/`
- `/git/github.com/LiGoldragon/router` — `src/criome_attestation.rs`,
  `src/forward_attestation.rs`, `src/criome_client.rs`, `src/router.rs`,
  `src/peer_delivery.rs`, `src/daemon.rs`
- `/git/github.com/LiGoldragon/signal-lojix/ethos/signal.ethos`,
  `/git/github.com/LiGoldragon/meta-signal-lojix/ethos/signal.ethos` and
  `src/generated/signal.rs`
- `/git/github.com/LiGoldragon/signal-criome/ethos/signal.ethos`,
  `/git/github.com/LiGoldragon/meta-signal-criome/ethos/signal.ethos`
- `/git/github.com/LiGoldragon/signal/ethos/{signal,interface}.ethos`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/{lojix,criome,persona-router}.nix`
- `/home/li/primary/flows/024bc7/vision/criome.md`,
  `/home/li/primary/flows/6cc91b/vision/{criome,secrets}.md`
