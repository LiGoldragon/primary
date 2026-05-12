# 30 - Minimal Criome as Persona trust root research

Date: 2026-05-12

Research-only designer-assistant report. No repository code was edited and no
BEADS were filed. This report reads the user's new direction as an independent
research pass alongside the designer's work: "use the Creom/Criome daemon in a
minimal Spartan form" for authentication, signed object/update verification,
cross-persona authorization, and high-risk Persona requests.

## 0 - Bottom line

The direction is sound if the boundary stays sharp:

- Persona's local engine trust model should stay as decided in designer/125:
  local authority comes from the `persona` user, socket ownership, socket modes,
  spawn envelopes, and router channel state. Do not reintroduce per-component
  in-band proof gates.
- Minimal Criome should be the cryptographic trust root at the edges:
  external persona/persona messages, signed object and release verification,
  developer and agent signing keys, delegation records, and audit receipts.
- BLS is the signing substrate. Do not stage an Ed25519 first milestone or
  keep Ed25519 as a fallback path in the Criome trust design.
- Prompt audit should live in Persona, probably `persona-mind`, not inside
  Criome. Criome can say "this request was signed by this principal under this
  valid delegation"; mind decides whether the request is safe to absorb or
  execute.
- The current `/git/github.com/LiGoldragon/criome` implementation is not this
  daemon yet. It is a ractor-based sema-ecosystem record validator with a TODO
  permission step and no real signing implementation.
- If the existing `criome` repo is repurposed, the old sema-validator code and
  architecture need an explicit "shelved at commit X" marker. Otherwise this
  should become a new sibling repo with a name like `criome-trust` or
  `criome-auth`, and the eventual Criome vision remains the convergence target.

The key design rule: **Criome verifies and records cryptographic authority;
Persona decides and acts.**

## 1 - Current facts from the repos

### 1.1 Current `criome` source

`/git/github.com/LiGoldragon/criome/AGENTS.md` and
`/git/github.com/LiGoldragon/criome/skills.md` describe current `criome` as the
state engine around sema records: receive typed `signal` frames, validate, write
to sema, and forward effect-bearing work.

The source matches that narrower implementation:

| Fact | Evidence |
|---|---|
| Actor runtime is direct `ractor`, not Kameo. | `/git/github.com/LiGoldragon/criome/Cargo.toml` depends on `ractor = 0.15`; `/git/github.com/LiGoldragon/criome/src/daemon.rs` uses a ZST `Daemon` actor marker plus separate `State`. |
| The daemon topology is record-engine shaped. | `/git/github.com/LiGoldragon/criome/src/lib.rs` documents `Daemon -> Engine, Reader x N, Listener -> Connection`. |
| Implemented behavior is M0 assert/query/deferred verbs. | `/git/github.com/LiGoldragon/criome/src/engine.rs` implements `Assert`, `Query`, `Subscribe` snapshot-ish behavior, and E0099 for deferred verbs. |
| Permission/auth is only a placeholder. | `/git/github.com/LiGoldragon/criome/src/validator/permissions.rs` says MVP is `SingleOperator`; post-MVP is BLS tokens/quorum proofs; function body is `todo!()`. |
| Tests do not exercise cryptographic trust. | `/git/github.com/LiGoldragon/criome/tests/engine.rs` checks assert/query, handshake, and unimplemented verb diagnostics. |

So the current repo has a useful daemon skeleton and sema-backed state
instinct, but it does not yet contain the minimal trust-root implementation.
Its ractor/ZST actor shape is also stale relative to the current workspace
actor skills: `skills/actor-systems.md`, `skills/kameo.md`, and
`skills/rust-discipline.md` now name Kameo 0.20 as the Rust actor runtime and
reject public ZST actor nouns.

### 1.2 Current Criome architecture is intentionally mixed

`/git/github.com/LiGoldragon/criome/ARCHITECTURE.md` has a prominent
"eventual, not today" scope marker. It says eventual Criome is the universal
computing paradigm, replacing Git/editor/SSH/web and encompassing network
identity and auth/security through quorum-signature multi-sig. It also says the
today implementation is narrower: a sema-ecosystem records validator.

This distinction is also in:

- `/home/li/primary/ESSENCE.md` section "Today and eventually - different
  things, different names".
- `/home/li/primary/protocols/active-repositories.md` row for `criome`.
- `reports/designer/110-cluster-trust-runtime-placement.md`, which previously
  decided that cluster-trust should not be placed inside today's `criome`
  daemon because today's daemon was narrower.

The user's new direction changes the pressure. It does not automatically mean
"put everything into the current sema-validator." The clean reading is:
**start a minimal present-day Criome trust component that is a realization step
toward eventual Criome.** That can be done by repurposing the repo only if the
old scope is explicitly shelved.

### 1.3 Signal auth vocabulary is inconsistent today

There is useful skeleton vocabulary but also drift:

- `/git/github.com/LiGoldragon/signal/src/auth.rs` defines
  `AuthProof::SingleOperator`, `AuthProof::BlsSignature`, and
  `AuthProof::QuorumProof`, plus a 48-byte `BlsG1` wrapper.
- `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md` says the frame envelope,
  handshake, auth, and identity primitives moved to `signal-core`.
- `/git/github.com/LiGoldragon/signal-core/ARCHITECTURE.md` and
  `/git/github.com/LiGoldragon/signal-core/src/frame.rs` say the opposite for
  today's kernel: frames carry no in-band authentication or provenance.
- `/git/github.com/LiGoldragon/signal-persona-auth/ARCHITECTURE.md` explicitly
  says `signal-persona-auth` is origin context, not an authentication library,
  and has a test rejecting a Persona-specific `AuthProof` type.

That means the minimal Criome design should not casually reuse the name
`AuthProof`. Use narrower names like `SignatureEnvelope`, `SignedObject`,
`VerificationReceipt`, `DelegationGrant`, or `SignedPersonaRequest` so future
agents do not confuse local Persona origin tags with cryptographic proof.

## 2 - Where minimal Criome fits Persona

### 2.1 Keep local Persona trust local

Persona's local trust model is already settled:

- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` section 1.6 says local
  trust comes from manager-created sockets, ownership, permissions, and spawn
  context.
- `reports/designer/125-channel-choreography-and-trust-model.md` says
  filesystem ACLs are the local engine boundary, `ConnectionClass` is an origin
  tag, router owns channel state, and mind choreographs channel grants.
- `/git/github.com/LiGoldragon/signal-persona-auth/ARCHITECTURE.md` says
  `IngressContext` is provenance, not proof.

Minimal Criome should not replace this with "every component checks a
signature." That would undo the big simplification from designer/125 and
recreate the class-gate/auth-proof sprawl that was just removed.

### 2.2 Use Criome at real trust boundaries

Criome belongs where local ACLs are insufficient:

| Boundary | Criome role | Persona role |
|---|---|---|
| Signed release/update | Verify artifact digest, developer signature, release authorization, and optional quorum. | `persona-daemon` only spawns/upgrades to a verified component closure. |
| Cross-persona or cross-host request | Verify sender principal, signature, delegation, expiry, audience, and replay nonce. | Router checks channel state; mind adjudicates unknown or risky channels. |
| Agent/harness privilege request | Verify the harness/agent key and any grant/delegation attached to the request. | Mind decides whether to grant; system/terminal/harness execute only through local authorized channels. |
| Cluster trust / public key publication | Store public trust records and signed trust updates. | CriomOS/lojix consumers use verified public material; ClaviFaber stays narrow. |
| Git/GitHub as dumb storage | Verify content digest and signed release record; retrieval source is not trusted. | Nix/CriomOS deploys only from verified artifacts. |

That gives the clean rule: **filesystem ACLs authorize local connections;
Criome authenticates claims that originate outside that local trust domain or
that change the trust root itself.**

### 2.3 Prompt audit belongs to `persona-mind`

The user described a future prompt-auditing system: another persona or agent
asks a persona to do work, and the system verifies the prompt is not trying to
induce injurious behavior.

That is not a signature problem. Signature verification answers "who signed
this, with what key, under what grant, over what exact bytes?" It does not
answer "is this prompt safe, useful, manipulative, or policy-compliant?"

Recommended flow:

```text
future network/persona-message boundary
  -> ask Criome to verify SignedPersonaRequest
  -> router commits message with verified principal/provenance
  -> router checks authorized-channel table
  -> if no active channel, router parks and asks persona-mind
  -> persona-mind runs prompt audit / policy adjudication
  -> mind grants one-shot, permanent, time-bound, or deny
  -> router enforces the channel result
```

Criome can persist the cryptographic verification receipt. Mind owns the
decision and audit semantics.

## 3 - Minimal Criome capability set

The Spartan form should be small enough that the whole component stays in one
LLM context window. It should not try to become the universal computing
paradigm now.

### 3.1 Contract first

Create a contract crate before runtime work. Candidate name:
`signal-criome-trust` or `signal-criome-auth`.

It should be a typed contract crate only:

- rkyv + NOTA derives on the same contract types, matching the Pattern A
  reversal in reports/designer/138.
- no daemon, no actor runtime, no database code.
- closed enums, no `Unknown`, no generic stringly bags.

Candidate record families:

| Family | Records |
|---|---|
| Principal identity | `PrincipalId`, `PrincipalKind`, `PrincipalName`, `PublicKeyFingerprint`, `PrincipalStatus`. |
| Key binding | `SigningPublicKey`, `SignatureScheme`, `KeyPurpose`, `KeyBinding`, `KeyRevocation`. |
| Signed object | `ObjectDigest`, `ObjectDigestAlgorithm`, `ObjectFormat`, `SignatureEnvelope`, `SignedObject`. |
| Release/update trust | `ComponentRelease`, `ArchiveFingerprint`, `NarHash`, `DeveloperSignature`, `ReleaseAuthorization`, `ReleaseVerification`. |
| Persona request trust | `SignedPersonaRequest`, `PersonaRequestAudience`, `DelegationGrant`, `DelegationScope`, `DelegationDuration`. |
| Verification reply | `VerificationAccepted`, `VerificationRejected`, `RejectionReason`. |
| Audit stream | `TrustEvent`, `SignatureVerified`, `SignatureRejected`, `GrantRevoked`, `ReplayRejected`. |

Avoid a generic `AuthProof` root. It is too overloaded in the current docs.

### 3.2 Minimal daemon actors

If this lands now, use Kameo rather than current `criome`'s ractor pattern.
Data-bearing actors:

| Actor | Owns |
|---|---|
| `CriomeTrustRoot` | runtime root, child supervision, socket lifetime. |
| `TrustStore` | sema-db/redb writer for principals, keys, grants, release records, and audit events. |
| `SignatureVerifier` | CPU verification work and scheme-specific adapter calls. |
| `ReleaseVerifier` | artifact digest/release policy verification. |
| `DelegationLedger` | grant lookup, expiry, revocation, replay/nonce state. |
| `TrustEventPublisher` | push stream of accepted/rejected verification events. |

Private signing keys are the dangerous question. The minimal daemon can start
as a verifier/trust registry and hold public keys plus revocation/grant state.
If it also holds an engine signing key, keep that key as a specific
`EngineSigningKey` plane with OS permissions, explicit key purpose, and tests
that no generic actor can read it.

Do not make "agent private keys" all live inside the daemon by default. An
agent/harness can own a private key under its own OS-protected state and
register the public key plus purpose in Criome. Criome verifies the request;
Persona adjudicates the effect.

### 3.3 State tables

Minimal durable tables:

| Table | Key | Value |
|---|---|---|
| `principals` | `PrincipalId` | principal kind/name/status. |
| `public_keys` | `PublicKeyFingerprint` | public key, scheme, purpose, status, owner principal. |
| `delegation_grants` | `DelegationId` | issuer, subject, scope, duration, status. |
| `release_records` | `(component, version/digest)` | signed release authorization and verification status. |
| `object_signatures` | `(object_digest, signer)` | signature envelope and verification result. |
| `replay_guard` | `(principal, audience, nonce)` | accepted/rejected replay state. |
| `trust_events` | monotonic sequence | typed audit event. |
| `meta` | schema | schema version and store identity. |

Everything that can be replayed or used later should be a typed event, not a
line log.

## 4 - Signing scheme research

### 4.1 BLS is the selected signing substrate

The eventual Criome architecture names quorum-signature multi-sig, and current
`signal/src/auth.rs` already has a BLS skeleton. BLS earns its complexity when
aggregate or threshold signatures are central: many developers/signers produce
one compact proof, or a quorum signs one object. The user has now resolved the
first-milestone question: Criome should use BLS, not Ed25519.

External research:

- Supranational's `blst` is a BLS12-381 signature library focused on
  performance and security, with Rust bindings and production use in Ethereum
  consensus clients and Filecoin clients. Sources:
  `https://github.com/supranational/blst` and
  `https://www.supranational.net/press/introducing-blst`.
- `zkcrypto/bls12_381` is a Rust BLS12-381 curve implementation, but its
  README warns that the implementation has not been reviewed or audited.
  Source: `https://github.com/zkcrypto/bls12_381`.
- `threshold-bls` documents normal, blind, and threshold BLS signatures, but it
  is a smaller crate surface and should be treated as research/reference until
  audited for our threat model. Source:
  `https://docs.rs/threshold-bls/latest/threshold_bls/`.

Recommendation: use `blst` for the first serious verification path, and make
the exact ciphersuite/scheme a closed enum variant, not a string. Also require
domain separation in the signed bytes so a release signature cannot be replayed
as a persona-message authorization.

### 4.2 No Ed25519 staging path

Do not implement a simpler single-signer Ed25519 bridge first. It would create
an attractive compatibility surface that later agents would preserve, test, and
route around. The minimal Criome trust component should be small, but it should
be small around the chosen primitive.

The design should still avoid open string schemes. Use a closed BLS enum with
explicit variants, for example:

```text
SignatureScheme
  | Bls12_381MinPk
  | Bls12_381MinSig
```

Then choose one BLS variant for the first implementation. Adding another BLS
variant is a schema bump with tests, not a runtime surprise. Adding a non-BLS
scheme is outside this report's recommendation after the user's clarification.

## 5 - Object and update verification

The user's goal is to move trust away from Git/GitHub. The right form is not
"trust a Git commit hash." It is "retrieve bytes from anywhere, verify the
canonical content digest and the signed release authorization."

For Nix-shaped artifacts, prefer existing Nix object semantics:

- Nix store object metadata includes `narHash`, the hash of the filesystem
  object serialized as a Nix Archive, and cache signatures for input-addressed
  store objects. Source:
  `https://nix.dev/manual/nix/2.24/protocols/json/store-object-info`.
- Nix content-addressed outputs are keyed by the output data, not how the
  output was produced. Source:
  `https://nix.dev/manual/nix/2.32/store/derivation/outputs/content-address.html`.
- `nix store make-content-addressed` can rewrite closures into
  content-addressed form, though the command is still experimental. Source:
  `https://nix.dev/manual/nix/2.30/command-ref/new-cli/nix3-store-make-content-addressed`.

Recommended signed release record:

```text
ComponentRelease
  | component:        ComponentName
  | source_repo:      RepoName
  | artifact:         ObjectDigest or NarHash
  | closure:          Vec<NarHash>             -- if release is a closure
  | contract_versions: Vec<ContractVersion>
  | schema_versions:   Vec<SchemaVersion>
  | built_by:         PrincipalId
  | authorized_by:    SignatureEnvelope or QuorumSignature
  | valid_from:       TimestampNanos
  | expires_at:       Option<TimestampNanos>
```

The signed bytes must bind the digest to its purpose: component name, release
channel, target platform, contract/schema versions, and audience. A detached
signature over only raw bytes is too easy to replay in another context.

## 6 - What should be shelved or preserved from current `criome`

If the current repo is repurposed:

| Preserve | Reason |
|---|---|
| "Text never crosses the daemon boundary" discipline. | Minimal trust daemon should speak Signal/rkyv internally and NOTA only through CLIs. |
| sema-backed state instinct. | Trust roots, keys, grants, and audit events are durable typed records. |
| `criome runs nothing` instinct. | Verification can happen in daemon; effect execution still belongs elsewhere. |
| Content-addressing emphasis. | Directly relevant to signed release/object trust. |

| Shelf or rewrite | Reason |
|---|---|
| ractor actor tree. | Current skills require Kameo 0.20; public ZST actor markers are stale. |
| Graph/Node/Edge validator surface if the repo becomes trust-focused. | It is a different capability than authentication/update trust. |
| Old `AuthProof` naming. | Too overloaded and conflicts with `signal-persona-auth` being provenance-only. |
| Universal architecture in present-tense implementation sections. | It causes agents to read eventual Criome as today's daemon. |

If the old sema-validator remains important, a new repo is cleaner than a
repurpose. If the old code is not currently important, a hard reset of `criome`
is defensible, but the reset must write down the shelved commit in
`ARCHITECTURE.md` so future agents can recover ideas without preserving stale
code.

## 7 - Integration sketch

```text
External persona / developer / agent
  -> SignedPersonaRequest or SignedObject
  -> Criome trust daemon verifies signature, key status, grant, digest, nonce
  -> Criome returns VerificationAccepted / VerificationRejected
  -> Persona boundary stamps provenance / verified principal
  -> Router checks channel table
  -> Mind adjudicates missing or risky channels
  -> Local component performs effect only through local Signal contract
```

Important distinction:

- `ConnectionClass` / `MessageOrigin` remain Persona provenance records.
- Criome verification receipts are cryptographic facts.
- Router channel state is the authorization cache.
- Mind policy is where safety and judgment live.
- Local sockets remain the local trust boundary.

## 8 - Research questions for the designer/user

1. **Repo identity.** Should the existing `criome` repo be repurposed into the
   minimal trust daemon, or should the trust daemon be a new sibling repo while
   current `criome` remains the sema-ecosystem validator?
2. **First BLS ciphersuite.** BLS is settled. The remaining question is whether
   the first contract variant should be `Bls12_381MinPk`,
   `Bls12_381MinSig`, or a more specific workspace-named BLS ciphersuite.
3. **Private key custody.** Does Criome store private signing keys, or only
   public trust state and verification receipts? My recommendation is
   public-verifier first, with a narrowly named engine signing key only if a
   witness requires it.
4. **First witness.** Which should land first: signed release verification,
   signed cross-persona job request, or agent privilege elevation? I recommend
   signed release/object verification first because it is narrow and directly
   tests "GitHub is dumb storage."
5. **Prompt audit boundary.** Confirm that Criome verifies identity/grants and
   `persona-mind` owns the prompt-audit decision. Putting prompt audit in
   Criome would mix cryptographic verification with agent policy.
6. **Signal auth cleanup.** Should the stale `signal`/`signal-core` AuthProof
   disagreement be cleaned during this wave, or should the new Criome contract
   avoid those names and leave cleanup separate?

## 9 - Suggested report-only handoff shape

No BEADS filed by this report, per instruction. If/when implementation work is
assigned, I would hand off this order:

1. Write the scope decision: repurpose current `criome` or create a new
   minimal trust sibling.
2. Create the contract crate with typed records and round trips.
3. Implement the smallest daemon: start, register public key, verify a signed
   object, reject a tampered object, write typed trust events.
4. Add Persona integration only at the boundary: `persona-daemon` release
   verification or future network/persona-message signed request verification.
5. Add a sandbox smoke that uses real signed bytes and a real tamper failure.

Do not start with broad prompt-auditing, generic policy engines, or
multi-component crypto gates. Those are where the shape would sprawl.
