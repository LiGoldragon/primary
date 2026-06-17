# 674.2 — Ground intent: binding constraints for criome's internal language

The binding Spirit records and prior criome design (reports 112/114/116/118/123,
designer 673) distilled to hard constraints for the criome internal-language
deliverable (Nexus object/verb vocabulary). Each governing Spirit record's
description is bracket-quoted literally below. The design phase (files 5–8) must
satisfy every constraint here; where this file says FIXED, the line is not a
design choice.

## The six governing Spirit records (descriptions quoted literally)

**`vhs2`** (Decision, Medium) — domains Engineering Architecture / Security
Authentication / Distributed ProtocolDesign; referents `criome Crayome Nexus`:

> [Crayome's internal language is a limited typed policy language over public-key
> identity atoms - NOT a general-purpose virtual machine - drawing its
> limited-operation discipline from the constrained VMs of Ethereum, Tezos, and
> Solana. Public keys are the atomic unit of identity; above them it composes
> complex identity contracts from signature and time-lock mechanics: signature
> quorums of k-of-n form and thresholds that increase or decrease over elapsed
> time. It carries explicit divergence-reconciliation objects for when two
> networks split and how the reconciliation is determined, where conflict
> resolution may be mediated by an LLM-oracle call to a provider which itself
> resolves through one of those identity contracts - for example a paid expert
> panel adjudicating the fairest resolution model. This is criome's Nexus object
> and verb vocabulary, the objects and operations the identity world treats, to
> be researched, defined in schema, and prototyped.]

**`z9d6`** (Principle, Medium) — domains Distributed ProtocolDesign / Data
Modeling; referents `criome spirit router mirror`:

> [Criome authorization contracts should be content-addressed composable
> objects: each component can decide acceptance based on another accepted object
> or contract, and those dependencies should refer to each other's
> content-addressed contract objects rather than ad hoc mutable state.
> Threshold, majority, or time-window acceptance policies are criome contract
> logic layered on those composable authorization objects.]

**`2st7`** (Decision, High) — domains Security Authentication / Security
Authorization; referents `spirit criome`:

> [Spirit criome-auth pilot mechanism is settled. criome authenticates the
> SUBMITTER, the SO_PEERCRED caller resolved to a registered criome Identity, not
> merely the log. The mechanism is an after-the-fact, non-blocking, out-of-band
> attestation binding the caller to the exact per-operation content-addressed
> digest. criome verifies the bytes and principal while the spirit guardian keeps
> the full content verdict. This settles the envelope design left open by w2g3.]

**`w2g3`** (Decision, Medium) — domains Security Authentication / Security
Authorization; referents `spirit criome`:

> [Spirit should be an early pilot consumer of Criome-backed operation
> authorization: Spirit operations that require authentication ask Criome to
> authorize an exact content-addressed request or log-message digest, with the
> concrete envelope design still open.]

**`wckt`** (Decision, Medium) — domain Engineering Architecture; referents
`router criome mirror spirit`:

> [CriomOS communication architecture. Each agent runs in its own microVM sandbox
> (all spaces become smart). ONE router per system is the communication fabric,
> carrying cross-sandbox traffic locally AND cross-network traffic
> router-to-router. criome stays auth-only (signs and verifies, never transports);
> the router transports; the mirror version-controls and moves objects; the
> tailnet provides confidentiality and criome BLS attestations provide per-frame
> authenticity. Intra-host sandbox-to-router transport is tap/L3 for now, vsock
> deferred because it loses SO_PEERCRED. This realizes i99x (router owns the
> remote delivery path) and narrows l3k4 so the harness-side-ack delivery fact
> applies to the local-harness path only, delivery becoming per-path. The
> per-agent-microVM model refines a4i6 (physical VM boundary; logical
> per-component-per-domain agent spaces nest inside one VM).]

**`d6he`** (Decision, High) — domain Engineering Architecture; referents
`spirit criome router mirror`:

> [The first end-to-end production milestone is the spirit -> vcs -> criome ->
> router -> mirror chain. When Spirit accepts a new log object, Spirit asks the
> local criome daemon to authenticate the exact content-addressed object/event
> for propagation. Criome trusts that local request because the system-side
> boundary will structurally ensure it came from Spirit, then verifies the
> request has the expected type/shape for a Spirit-authenticated object, signs or
> authorizes it under a cluster-root-admitted identity, and propagates the
> authenticated event through Router. Router is the transport fabric for the
> propagation; remote criome/mirror participants receive the authenticated event
> and the remote mirror fetches/restores the announced object state. This keeps
> criome auth-only, Router transport-only, and mirror as the object
> version-control substrate. Threshold/majority timing for when criome announces
> acceptance remains future criome contract logic, not a Router requirement for
> the first PoC slice.]

## The core data model — z9d6's content-addressed composable authorization objects

This is the spine of the whole deliverable. The object/verb vocabulary is **not**
a new policy system; it is the typed surface over z9d6's composable objects.

- **C1 — Content-addressed composable authorization objects are THE data model.**
  Per z9d6: each authorization object is content-addressed; one object can decide
  acceptance based on another accepted object or contract; dependencies refer to
  each other's **content-addressed contract objects, not ad hoc mutable state**.
  Every object the vocabulary defines must be addressed by the digest of its own
  bytes, and every reference between objects must be a content-address reference,
  never a name/handle into mutable state. This composability — object-references-
  object-by-digest — is the mechanism that makes the language a language.

- **C2 — Threshold / majority / time-window policies LAYER ON the composable
  objects; they are not primitives beside them.** Per z9d6's closing sentence:
  [Threshold, majority, or time-window acceptance policies are criome contract
  logic layered on those composable authorization objects.] So k-of-n quorums,
  majority rules, and time-varying thresholds are expressed AS composable objects
  (a quorum object references its member-identity objects by content-address; a
  time-window policy object references the underlying acceptance object), not as a
  separate parallel feature set. The design must show threshold/majority/time-
  window emerging from composition, not bolted on.

- **C3 — Public keys are the atomic identity unit; everything composes above
  them.** Per vhs2: [Public keys are the atomic unit of identity; above them it
  composes complex identity contracts from signature and time-lock mechanics.]
  The base atom is a public key (BLS, matching deployed criome — report 114's
  `MasterKey` / `BlsPublicKey`). Identity contracts are composite objects over
  these atoms. There is no identity object below the public key.

- **C4 — The two composition mechanics are signature quorums and time-locks.**
  Per vhs2, complex identity contracts compose from exactly: (a) **signature
  quorums of k-of-n form**, and (b) **thresholds that increase or decrease over
  elapsed time** (time-varying / time-locked thresholds). The PoC must
  demonstrate both: a static k-of-n quorum AND a threshold that changes with
  elapsed time. These map onto z9d6's threshold and time-window policy classes.

## The limited-policy-language line (vhs2) — FIXED

- **C5 — A LIMITED typed policy language, NOT a general-purpose VM. FIXED.** Per
  vhs2, the language is [a limited typed policy language over public-key identity
  atoms - NOT a general-purpose virtual machine]. The frame (file 0) states this
  line is fixed. The vocabulary takes only the limited-operation **discipline** of
  the Ethereum/Tezos/Solana constrained VMs — bounded, total, terminating
  evaluation over a closed operation set — NOT their generality (no Turing-
  complete execution, no arbitrary user code, no gas-metered general computation,
  no unbounded loops). Authorization evaluation must be total and terminating by
  construction. The research file (3) studies these VMs for the discipline to
  borrow; the design (5) must keep the operation set closed and typed.

- **C6 — Typed and closed.** "Typed policy language" plus the workspace
  triad/NOTA discipline means the object set and verb set are closed taxonomies
  (NOTA enums), positional records, every identifier a full English word. No
  open-ended user-supplied scripting surface.

## Auth-only / non-transport (wckt) — FIXED

- **C7 — criome stays auth-only: signs and verifies, never transports. FIXED.**
  Per wckt: [criome stays auth-only (signs and verifies, never transports); the
  router transports; the mirror version-controls and moves objects]. The richer
  identity engine does NOT make criome transport, fetch, route, or move objects.
  The vocabulary's verbs are confined to minting/composing/evaluating
  authorization objects and producing/verifying signatures and attestations. Any
  verb that would move bytes, deliver a message, or version-control an object is
  out of scope — that is router/mirror, not criome.

- **C8 — Stay inside the established CriomOS division of labor.** Per wckt and
  d6he, the fixed split is: criome authenticates (per-frame BLS authenticity),
  router transports, mirror version-controls/moves objects, tailnet/Yggdrasil
  provides confidentiality. The internal language extends criome's auth role only.
  Threshold/majority **timing** for when criome announces acceptance is explicitly
  [future criome contract logic, not a Router requirement] (d6he) — i.e. it lives
  in criome's policy objects, reinforcing C2.

## Submitter authentication via content-addressed digest (2st7 / w2g3)

- **C9 — Authenticate the SUBMITTER bound to the exact per-operation
  content-addressed digest.** Per 2st7: criome [authenticates the SUBMITTER, the
  SO_PEERCRED caller resolved to a registered criome Identity, not merely the log
  ... binding the caller to the exact per-operation content-addressed digest].
  The vocabulary's attestation/authorization objects bind a principal (a
  registered Identity resolved from the kernel-vouched SO_PEERCRED caller) to an
  exact content-address. The atomic unit of "what is authorized" is the
  content-addressed digest of one operation, not a coarse log/whole-store witness.
  Report 112's Map 3: sign the real 32-byte blake3 `EntryDigest` per operation;
  never the truncated 64-bit `StateDigest`.

- **C10 — The envelope is after-the-fact, non-blocking, out-of-band.** Per 2st7
  (settling w2g3's [concrete envelope design still open]): the attestation is
  after-the-fact, the write never blocks on criome, and the attestation is a
  separate out-of-band record keyed by the operation digest — no proof field
  embedded in the authorized content itself. The vocabulary must keep
  authorization objects separable from the objects they authorize (which C1's
  content-addressing already enforces — the attestation references the target by
  digest).

- **C11 — criome verifies the bytes + principal; the consumer keeps the full
  semantic verdict.** Per 2st7: [criome verifies the bytes and principal while the
  spirit guardian keeps the full content verdict]. The language authorizes /
  attests cryptographic facts (these bytes, this principal, this policy
  satisfied); it does not make the semantic/admissibility decision. "criome
  verifies; the consumer decides" — keep policy evaluation cryptographic and
  mechanical, not semantic.

## The end-to-end chain (d6he) and the deployed model the vocabulary extends

- **C12 — The vocabulary lives inside the spirit → vcs(mirror) → criome → router
  → mirror chain.** Per d6he, criome's role in the first production milestone:
  verify a local request came from the authorized component (structurally vouched
  by the system boundary), verify expected type/shape, then [sign or authorize it
  under a cluster-root-admitted identity] and emit the authenticated event for
  Router to transport. The internal language must produce exactly such an
  authenticated authorization object/attestation; it is the "auth" node of d6he,
  nothing more. The offline realization of this chain is already proven (designer
  673), with criome stubbed (`AcceptFixedTestIdentity`) per the psyche's
  "no key encryption for now" steer — the vocabulary is the real-crypto fill-in
  for that stub.

- **C13 — cluster-root admission is the trust root the vocabulary builds on.**
  Per d6he ([a cluster-root-admitted identity]) and reports 116/118 (Spirit
  `ermr`): a key is admitted into a criome registry only when the cluster-root
  signed the `RegistrationStatement` (identity + public_key + purpose). Report
  118's `ClusterRoot::admits` and `RegistrationStatement` already implement this
  on the `criome-auth-pilot` branch. Identity objects in the new vocabulary
  resolve their trust to a cluster-root-admitted registration; the vocabulary
  does not invent a second admission authority.

- **C14 — Extend the deployed criome model; do not replace it.** Already built
  and tested (reports 114/118, branch `criome-auth-pilot`): real `blst` min-pk
  BLS (`MasterKey`, `VerifyBls` on `BlsPublicKey`), self-owned signing (criome
  signs as `Host("criome")`, caller in `audit_context`), `AttestationPreimage`
  binding content+caller+purpose+validity+scheme, the `Identity` registry over
  `Persona | Agent | Host | Developer | Cluster` principals, `ContentReference{
  digest, purpose, schema_version}`, `Attestation` / `SignatureEnvelope`, the
  `Sign` (free `ContentReference`) and async `AuthorizeSignalCall` paths, and the
  cluster-root admission gate. The new object/verb vocabulary EXTENDS this surface
  with composable policy objects (quorum, time-varying threshold, divergence-
  reconciliation) — it is criome's existing Nexus engine vocabulary made richer,
  not a fourth engine (frame, file 0; triad records `a71r`/`3d5z`).

## The divergence-reconciliation requirement (vhs2)

- **C15 — Explicit divergence-reconciliation objects are a first-class part of
  the vocabulary.** Per vhs2: [It carries explicit divergence-reconciliation
  objects for when two networks split and how the reconciliation is determined].
  When two networks split, the language must express, as composable objects, both
  the divergence fact AND how reconciliation is determined. This is a defined
  object class, not an afterthought.

- **C16 — Reconciliation MAY be mediated by an LLM-oracle that itself resolves
  through an identity contract.** Per vhs2: [conflict resolution may be mediated
  by an LLM-oracle call to a provider which itself resolves through one of those
  identity contracts - for example a paid expert panel adjudicating the fairest
  resolution model]. The reconciliation mechanism may delegate to an oracle, and
  the oracle provider is itself selected/authorized by one of the same composable
  identity contracts (recursion: the oracle's authority is a quorum/threshold
  object — e.g. the paid expert panel is a k-of-n quorum). The PoC must show this
  interface with a **stub** LLM-oracle (frame, file 7) — the recursion (oracle
  authorized through an identity contract) must be visible in the type shape even
  though the call is stubbed. "may be" — the oracle is one reconciliation strategy
  among possible others, not the only one.

## Cross-cutting workspace discipline (binding on the schema + Rust files)

- **C17 — Triad/NOTA discipline.** Objects and verbs are NOTA positional records
  (type first, declared-order fields, no labels); closed-taxonomy enums; full
  English-word identifiers (`Identifier` not `Id`, names don't carry ancestry);
  bare atoms unless delimiters are needed, never quotation marks. The vocabulary
  is criome's Nexus object/verb set (triad: daemon + working signal + meta policy
  signal); signal types are the contract data types, the signal tree is the whole
  schema shape.

- **C18 — Rust discipline (binds file 7 PoC).** Every function is a method /
  associated function on a non-zero-sized data-bearing type or a trait impl; no
  free functions (except `#[cfg(test)]` / `fn main()`); no ZST-namespace methods;
  conversions are `impl From`; typed per-crate `Error`; typed domain values; no
  hand-rolled parsers; schema-emitted code emits into `impl` blocks. The PoC is a
  standalone, actually-compiled-and-run demonstration of identity atoms,
  quorum/timelock/time-varying composition, authorization evaluation, and the
  stubbed divergence-reconciliation + oracle interface — not yet integrated into
  criome proper.

- **C19 — No backward compatibility; build for the single best shape.** Pre-
  production: the vocabulary may break every existing criome consumer at once.
  Do not constrain the design to be opt-in or byte-stable. The deployed
  `signal-criome` contract (report 118's deltas: `admission`, `cluster_root`,
  `UnauthorizedRegistration`) may be extended freely.

## One-line summary of the FIXED lines

1. Limited typed policy language, NOT a general-purpose VM (vhs2). FIXED.
2. criome auth-only — signs/verifies, never transports (wckt). FIXED.
3. Build ON z9d6's content-addressed composable authorization objects (the core
   data model); threshold/majority/time-window policies layer on them.
4. Triad-consistent: criome's Nexus object/verb vocabulary, not a fourth engine.
5. Authenticate the submitter bound to the exact per-operation content-addressed
   digest; after-the-fact, non-blocking, out-of-band (2st7); criome verifies
   bytes+principal, consumer keeps the semantic verdict.
