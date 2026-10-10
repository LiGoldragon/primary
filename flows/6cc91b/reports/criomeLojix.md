# Criome-authorized Lojix activation — boundary audit at the call sites

Flow 6cc91b subflow. Read-only; nothing built or run. Every `file:line` was opened or grepped in this flow (WITNESSED) unless marked CLAIMED.

Vision (flows/024bc7/vision/criome.md, 2026-09-13): *"Criome should essentially take over the authentication layer of Lojix to deploy to have a root call on the host that needs to activate the operating system."*

## 1 · Current admission path of a Lojix activation

WITNESSED, `/git/github.com/LiGoldragon/lojix`.

1. **Sockets bound.** `src/daemon.rs:138-155` binds `ListenerRole::Ordinary` and `ListenerRole::Owner`. CriomOS defaults `/run/lojix/ordinary.sock` 0660, `/run/lojix/meta.sock` 0600 (`CriomOS/modules/nixos/lojix.nix:99-124`).
2. **Dispatch.** `src/daemon.rs:429-434` routes by role; Deploy exists only on the owner branch.
3. **The one authentication check in the whole path.** `src/daemon.rs:463` — `self.owner_authority.authorize(connection.context())?`. Implementation `src/daemon.rs:337-358`: a Unix peer is admitted iff its kernel-vouched `SO_PEERCRED` uid *and* gid equal the daemon's own effective uid/gid (`:330-334`, `rustix::process::geteuid/getegid`); a TCP peer is refused (`Error::UnauthorizedOwnerTcpPeer`). **That is the entire admission decision** — no signature, no attestation, no principal beyond "same uid".
4. **Decode.** `src/daemon.rs:464-466` reads the `meta-signal-lojix` frame; `Deploy`/`Test` decouple onto job actors (`:472-480`).
5. **Content validation, not authentication.** `src/schema_runtime.rs:2618-2651` runs `unsupported_deploy_reason`, `deployment_routing_rejection`, `proposal_source_rejection`, `source_revision_policy_rejection`, then `RecordDeploySubmitted`. These check shape and routing, never who asked.
6. **The root call.** `src/schema_runtime.rs:5455-5478` (`HostActivation::ssh_invocation`) builds `nix-env -p /nix/var/nix/profiles/system --set <store> && <store>/bin/switch-to-configuration <boot|switch|test>` and hands it to `src/schema_runtime.rs:5240-5251`:

   ```rust
   NixCommand::new("ssh", vec!["-o".into(), "BatchMode=yes".into(),
                               self.ssh_destination.clone(),
                               remote_command.into_text()])
   ```

   The destination is a request-carried verbatim `user@host`; `:5197-5216` validates only that it is one nonempty login plus host. `:5226-5238` classifies the login: `"root"` → `RemoteUserActivationAuthority::RootMediated`, matching user → `MatchedUser`, else `UnprivilegedMismatch`, refused at `:6102-6113`. BootOnce wraps the same script in `systemd-run` on the target (`:5503-5512`).

**What it trusts today.** (a) The daemon's uid — anyone who can run a process as the lojix service account can deploy; under CriomOS that is an unprivileged operator user (`lojix.nix:56-64, 234-235`; the option has no default, so CLAIMED that production sets an unprivileged account — no host inventory found). (b) The 0600 socket mode. (c) **Ambient SSH**: the daemon activation path passes *only* `-o BatchMode=yes`. Grep over `src/schema_runtime.rs` finds no `IdentityFile`, `IdentitiesOnly`, `UserKnownHostsFile`, `StrictHostKeyChecking` or `IdentityAgent` — only `BatchMode` at `:5246`. The deploy borrows the daemon user's ambient ssh config, agent and known_hosts; the real authorization decision is `root@target`'s `authorized_keys`, made outside Lojix entirely.

**Contrast in the same repo:** the daemon-free `lojix-bootstrap` path *does* carry explicit credential policy — `src/bootstrap.rs:1474` writes a private `Host *` config with `IdentityFile`, `UserKnownHostsFile`, `GlobalKnownHostsFile /dev/null`, `StrictHostKeyChecking`, `IdentitiesOnly yes`, `IdentityAgent none`, repeated on the command line at `:1497`. The daemon path has no equivalent. Lojix's own `ARCHITECTURE.md:327-332` already names this as owed work (Spirit `h03z`): credentials "custodied and authenticated through criome rather than borrowing the operator's logged-in session (GPG/SSH agent)."

## 2 · What Criome can already assert, and whether Lojix references it

WITNESSED.

- **Identity.** `Identity.[ Persona.PrincipalName Host.PrincipalName Developer.PrincipalName Agent.PrincipalName Cluster.PrincipalName ]` — `signal-criome/ethos/signal.ethos:123`; registry at `criome/src/actors/registry.rs`.
- **Signing.** `AttestationSigner` holding a `MasterKey` (`criome/src/actors/signer.rs:21-27`); BLS12-381 min-pk via `blst`; the secret never leaves the process (`criome/src/master_key.rs:1-13, 36-37`).
- **Verification.** `AttestationVerifier::verify`, `criome/src/actors/verifier.rs:40-112` — content-reference match, signer resolution, revocation, key match, scheme (min-pk only), BLS check, expiry. `VerificationDecision.[ InvalidSignature UnknownSigner ReplayAttempted Valid Revoked Expired ]` (`signal-criome/ethos/signal.ethos:93`).
- **Authorization.** `AuthorizationCoordinator` (`criome/src/actors/authorization.rs:15-17, 84-237`); `evaluate_authorization` at `criome/src/actors/root.rs:1033-1059` dispatches on `AuthorizationMode.[ AutoApprove ClientApproval Quorum ]`. Grant: `AuthorizationGrant.{ AuthorizationRequestSlot AuthorizedObjectReference AuthorizationPolicySatisfaction SignatureAuthorizationResult Vector<StampedSignatureEnvelope> Identity TimestampNanos Option<TimestampNanos> }` (`signal-criome/ethos/signal.ethos:180`).
- **The hook that already exists.** `AuthorizedObjectReference.{ ComponentKind ObjectDigest AuthorizedObjectKind }` with `ComponentKind.[ … Lojix … ]` and `AuthorizedObjectKind.[ Time Operation Contract Agreement Head ]` — `/git/github.com/LiGoldragon/signal/ethos/interface.ethos:7`. A Lojix operation is already a namable authorized object, and criome's signer already encodes the `Lojix` tag when signing a grant (`criome/src/actors/signer.rs:222`).
- **Sockets.** Ordinary (`signal-criome/ethos/signal.ethos:13-46`): `Sign`, `VerifyAttestation`, `AttestAuthorization`, `EvaluateAuthorization`, `VerifyAuthorization`, `AuthorizeSignalCall`, `ObserveNodePublicKey`, quorum verbs. Meta (`meta-signal-criome/ethos/signal.ethos:14-28`): `Configure`, `InitiateRootFounding`, `AcceptRootFounding`, `SubmitAuthorizationApproval`, `FetchParkedRequests`, `AnswerParkedRequest`, intercept-policy admin.
- **"Root" in Criome is root-of-trust, not OS root** (`criome/src/founding.rs:1-14, 56-64, 230-243`). There is no exec, spawn, or `Command::new` anywhere in `criome/src`; criome cannot itself make a root call.

**Witnessed grep — does Lojix reference any of it?**

```
$ cd /git/github.com/LiGoldragon/lojix
$ grep -rni "criome" --include='*.rs' --include='*.toml' --include='*.nix' . | grep -vi criomos
tests/common/mod.rs:59:                string: "criome".to_owned(),
tools/tests/common/mod.rs:61:                string: "criome".to_owned(),
```

Two hits, both a cluster-name string in a test fixture. **Zero in `src/`, `nexus/`, `clients/`, `tools/src/`, or `Cargo.toml`** — no dependency, no client, no attestation type. Symmetrically, `grep -rni 'lojix\|deploy\|activat\|nixos-rebuild'` over criome yields only the `ComponentKind::Lojix` tag (`signer.rs:222`), a fixture (`criome/tests/daemon_skeleton.rs:173`), and prose comments; `activat` and `nixos-rebuild` have zero hits. This confirms Codex's finding.

## 3 · How router consumes Criome attestation — the working example

WITNESSED, `/git/github.com/LiGoldragon/router`.

- **Sign.** `criome_attestation.rs:137-174` builds a `ForwardContentPreimage` over origin identity + payload (`:280-329`, domain-separated blake3), wraps it in a criome `SignRequest` (`:144-149`), sends it via `criome_client.rs:42-47` (`CriomeRequest::Sign`) over the Unix socket at `config.criome_socket_path` (`criome_client.rs:83-115`). On failure, `unattested()` (`:257-274`) — real digest, empty signature.
- **Verify.** `criome_attestation.rs:180-192` re-derives the digest from the wire-claimed origin plus the received payload, reconstructs the `Attestation` (`:198-218`), calls `criome_client.rs:53-65` (`VerifyAttestation`). Gate at `criome_attestation.rs:238-249`: **only `VerificationDecision::Valid` passes**; every other decision and every transport error collapse to one refusal, `RouterForwardRefusalReason::z2VLzK`. Fail-closed.
- **Call site.** `router.rs:381-388` — verification runs in `TailnetForwardIngress::handle_forward` *before* the forward is applied. Outbound signing at `peer_delivery.rs:221`.
- **Identity bootstrap.** `router.rs:1107-1145`: `ObserveNodePublicKey` with five retries and backoff; if criome never answers, `UNRESOLVED_CRIOME_HOST_ID` is pinned and the router can sign and verify nothing — degraded, still fail-closed.
- **Enablement.** `daemon.rs:114-135`: a configured `criome_socket_path` builds the real attestor and requires encrypted peer sessions; `None` falls back to the plaintext `AcceptFixedTestIdentity` (`forward_attestation.rs:60-141`).
- Router never runs crypto itself (`criome_client.rs:8-9`); it asks a colocated criome (`CriomOS/modules/nixos/persona-router.nix:46-56` hardwires `/run/criome/criome.sock`, "the criome module must be co-resident").

**The shape to copy:** a thin client crate; a preimage both sides derive identically; one verdict enum; one fail-closed gate placed *before* the effect.

## 4 · The gap, precisely

The single decision separating "bytes arrived on a socket" from "a root shell runs `switch-to-configuration switch` on a production node" is `src/daemon.rs:463` — an integer comparison of uid and gid. Everything after it validates shape, never principal.

- **No principal is recorded.** Deploy rows carry an identifier and a routing snapshot, never who requested the activation. Nothing to audit, revoke, or replay-check.
- **No attestation is verified.** Criome can already verify BLS attestations and already names `ComponentKind::Lojix` / `AuthorizedObjectKind::Operation`, and Lojix asks it nothing.
- **The root call is authenticated by the target host, not by the fleet.** A compromised operator ssh session is a fleet-wide root compromise, with no second factor and no per-deploy record.
- **The daemon path is weaker than the bootstrap path in the same repo** (`bootstrap.rs:1474` vs `schema_runtime.rs:5246`).
- Both daemons are already designed as Unix-socket neighbours (criome's 0660 working socket, `CriomOS/modules/nixos/criome.nix:16-23`), so the transport is available unchanged. Whether lojix and criome are in fact enabled on the same hosts is CLAIMED-unknown: CriomOS holds modules only, no host inventory.

## 5 · Proposed contract for Criome-authorized activation

A proposal, not a decision. Written in the `meta-signal-lojix/ethos` style.

**Who asks:** Lojix. The `lojix-meta` client obtains a Criome attestation over the deploy it is about to send; `lojix-nexus` asks Criome to verify it. Criome stays a pure decision service, ignorant of deploys as it is of routes.

**Who verifies:** Criome verifies the signature and evaluates authorization; Lojix enforces the verdict and runs no crypto (router precedent).

**Where the root call happens:** unchanged, `schema_runtime.rs:5240-5251`. Criome gains no exec path and must not. The new gate sits in `daemon.rs::serve_owner`, immediately after `:463` and before `submit_deploy` at `:472`, so a refused activation never reaches a durable row, let alone an ssh.

**The preimage:** a canonical digest over `DeploymentRequestIdentity`, which `signal-lojix/ethos/signal.ethos:70` already defines (`{ DeploymentEnvironment ClusterName NodeName GenerationArtifact RequestedDeploymentAction ActivationEffect SourceRevisionPolicy Option<ImmutableRevision> }`). No new preimage type is needed. The attestation's `ContentPurpose` needs one new variant `HostActivation` alongside `[ ChannelGrant SignedObject ChannelRetract PrivilegeElevation Authorization Archive ComponentRelease ]` (`signal-criome/ethos/signal.ethos:212`) — or it reuses `PrivilegeElevation`, arguably what an activation is.

**Signal variants** (added to `meta-signal-lojix/ethos/signal.ethos`):

```
  ActivationAttestation.{ ObjectDigest Identity SignatureEnvelope TimestampNanos ReplayNonce }
  AttestedDeploySubmission.{ DeploySubmission ActivationAttestation }
  ActivationAuthorizationRejection.{ ActivationRefusalReason DatabaseMarker }
  ActivationRefusalReason.[ AttestationInvalid SignerUnknown SignerRevoked
                            AttestationExpired ReplayAttempted
                            AuthorizationDenied AuthorizationPending
                            CriomeUnavailable ]
  Deploy.AttestedDeploySubmission                        ; replaces Deploy.DeploySubmission
  DeployUnauthorized.ActivationAuthorizationRejection    ; new reply variant
```

Lojix-side error `Error::UnauthorizedActivation { reason }`, sibling of the existing `UnauthorizedOwnerPeer` (`src/lib.rs:203`).

**Criome needs no new verbs.** The existing `Sign`, `VerifyAttestation`, `EvaluateAuthorization` and `AuthorizedObjectReference{ ComponentKind::Lojix, digest, AuthorizedObjectKind::Operation }` already express this. Escalation to a human is the existing meta-socket `SubmitAuthorizationApproval` / `FetchParkedRequests` path — which is also what flows/6cc91b/vision/secrets.md describes ("you'll get notified that something needs to get access").

**Offline — fail closed, with one exception.** Criome unreachable ⇒ `DeployUnauthorized(CriomeUnavailable)`, mirroring `criome_attestation.rs:238-249`. Under criome's `Quorum` mode an unreachable peer leaves a round pending indefinitely (`criome/src/actors/root.rs:2038-2040, 2467-2469`) and an unfounded node returns terminal `AuthorizationUnavailable` (`root.rs:1509-1533`); Lojix maps those to `AuthorizationPending` and does not block the connection. The exception is `lojix-bootstrap`: the authorized daemon-free crossing (ARCHITECTURE.md §1), running before any criome exists on a new host, keeps its explicit private-key SSH policy and stays out of this contract. **Open for the psyche:** whether a production host that cannot reach criome should be undeployable — the vision's plain reading says yes.

**Smallest witness test.** Pure policy, no daemon, no build, no network — the shape of `tests/owner_peer_authority.rs:13-20`, over a trait `ActivationAuthorizable` beside `PeerAuthorizable` in `src/daemon.rs`:

```
tests/activation_attestation_authority.rs
  activation_authority_accepts_valid_criome_verdict()
  activation_authority_rejects_invalid_signature()
  activation_authority_rejects_when_criome_unreachable()   ; fail-closed
  activation_authority_rejects_digest_mismatch()           ; wrong DeploymentRequestIdentity
```

The fourth case is the load-bearing one: it proves the attestation binds *this* deployment, not merely that some signature verified.

## 6 · Unknowns

1. Is criome enabled on the hosts lojix deploys to, and on the operator workstation? CriomOS holds modules only; no host inventory found.
2. Which identity signs a deploy — `Developer`, `Agent`, or `Cluster`? The vision's "root call on the host" suggests the *host* must also be satisfied, implying a second gate target-side, not only daemon-side.
3. Does the target-side root call itself become criome-mediated? The vision may mean Criome replaces the SSH key entirely — a criome-authorized local activation agent per node — a far larger change than gating the socket.
4. `ContentPurpose::PrivilegeElevation` vs a new `HostActivation` variant: a contract-owner decision.
5. Replay window and clock. Criome gates votes on local clock (`criome/tests/witness_clock_gate.rs:1-24`); the activation attestation needs a stated freshness window, not proposed here.
6. Nothing was built or run. Every claim is source reading — no compile, no test execution, no live socket.

## Sources

- `/git/github.com/LiGoldragon/lojix` — `ARCHITECTURE.md`, `Cargo.toml`, `src/{daemon,schema_runtime,bootstrap,lib,ingress}.rs`, `tests/owner_peer_authority.rs`, `tests/common/mod.rs`, `tools/tests/common/mod.rs`
- `/git/github.com/LiGoldragon/criome` — `ARCHITECTURE.md`, `src/actors/{signer,verifier,authorization,root,registry}.rs`, `src/{master_key,founding,conveyance,deploy_encode}.rs`, `tests/`
- `/git/github.com/LiGoldragon/router` — `src/{criome_attestation,forward_attestation,criome_client,router,peer_delivery,daemon}.rs`
- `signal-lojix/ethos/signal.ethos`; `meta-signal-lojix/ethos/signal.ethos` and `src/generated/signal.rs`
- `signal-criome/ethos/signal.ethos`; `meta-signal-criome/ethos/signal.ethos`
- `/git/github.com/LiGoldragon/signal/ethos/{signal,interface}.ethos`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/{lojix,criome,persona-router}.nix`
- `/home/li/primary/flows/024bc7/vision/criome.md`, `/home/li/primary/flows/6cc91b/vision/{criome,secrets}.md`
