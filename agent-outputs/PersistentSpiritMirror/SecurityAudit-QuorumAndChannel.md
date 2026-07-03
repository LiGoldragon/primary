# Security Audit — Quorum + Identity + Encrypted Channel (bead primary-nbmq.11)

Scope: the committed `.4` (Criome quorum collection) and `.6` (encrypted
authenticated router session + mutual identity proof) security path, plus the
Spirit authorized-apply re-judge (`.2`/`.3`) it composes with. Read-only,
adversarial. Bead `.5` (durable outbox, concurrently edited) is out of scope.

Method: source inspection of the committed heads on each repo's `main`
(criome `8fbde55`, router `c73b7b1`, spirit `7fc43d6`, signal-* heads). I did
NOT execute the test suites — see "Checked evidence" for why and what that
leaves open. Every claim below is tagged **observed** (read in the code) or
**interpretation**.

Anchors use `repo/path:line`. Repos: criome = `criome`, router = `router`,
spirit = `spirit`.

## Verdict

**YES, with must-fixes.** The cryptographic core is sound and fail-closed as
written:

- Quorum authorization runs the real majority evaluator on real BLS signatures;
  there is **no count-based shortcut, no 1-of-1 fallback for a 2-of-2 contract,
  and no path to `Authorized` below a true majority.** Peer-unreachable genuinely
  **waits** (withheld forever), never last-writer-wins.
- The mutual identity proof is verified **both ways** against each node's own
  criome, binds the session's ephemeral encryption key into the signed digest
  (defeating a man-in-the-middle key swap), and is replay-resistant at both the
  router's challenge-freshness check and the signed-digest level.
- The encryption uses a fresh per-session ephemeral X25519 keypair, transcript-
  bound directional ChaCha20-Poly1305 keys with a never-repeating nonce counter,
  a key-confirmation step, and real forward secrecy (ephemeral secrets consumed
  and dropped). Session/symmetric keys are transient and never persisted or
  logged; the BLS master key never leaves criome.

The must-fixes are **not** breaks in the crypto. They are the migration/deploy
posture that the `.4`/`.6` code deliberately leaves open for `.9`/`.10`: the
plaintext dual-accept path, and the deploy-time invariants (real criome-backed
provers, `Quorum` mode, the admitted 2-of-2 contract) without which piece 6 is a
no-op. The system must not be trusted to carry real notebook content on an
eavesdroppable network until the plaintext path is closed and those invariants
are verified live.

## Findings by severity

### MUST-FIX

**M1 — The plaintext dual-accept ingress leaves the channel unencrypted and
downgradeable while it is open.** (observed)
`router/src/router.rs:534` accepts a bare `Input::ForwardMessage` **unconditionally**,
including when the node is fully session-capable (`identity_prover = Some`;
`router.rs:515-548`). Two consequences:
- **No confidentiality on that path.** The forwarded record body, actors, and
  routed-object octets travel in cleartext (the encrypted session is only used
  when the *initiator* opens with `SessionClientHello`). Security addition 8
  (psyche-confirmed) is not delivered for any forward that takes the plaintext
  path — and today the standing daemon's outbound prover is `None`/plaintext
  (per the `.9` handoff note), so in practice everything is cleartext until `.9`.
- **Active-downgrade surface.** A responder that can speak the session still
  serves plaintext to anyone presenting a valid per-forward attestation; an
  on-path attacker can therefore force the cleartext path.

What holds the line (defense in depth, genuinely real): both paths funnel through
`handle_forward` (`router.rs:387-394`) → `ApplyForwardedMessage`
(`router.rs:1757`), which enforces (a) a criome BLS forward attestation binding
sender identity **and** exact payload content (`router/src/criome_attestation.rs:168-207,227-238`;
criome cross-checks the content digest at `criome/src/actors/verifier.rs:41` and
does a real BLS verify), and (b) a replay + clock-skew admission window
(`router/src/forward_attestation.rs:165-208`). So the plaintext path **cannot be
used to forge, inject, or replay a forward** — an attacker with no registered
identity and no peer master key is refused. Injection/authorization-bypass is NOT
possible via plaintext; **confidentiality and downgrade-resistance are.**

Correction: once both standing daemons run the encrypted session (`.9`), reject a
bare `ForwardMessage` when `identity_prover` is `Some` (require `SessionClientHello`).
Timing: **close it in `.9`/`.10`, before the toggle is flipped on for live
content.** Until then, treat the link as authenticated-but-cleartext and do not
mirror confidential records over it.

**M2 — `.9` must wire the real criome-backed provers, not the offline stand-ins.**
(observed / interpretation)
The offline `AcceptFixedIdentityProver` (`router/src/identity_proof.rs:243-285`)
and `AcceptFixedTestIdentity` (`router/src/forward_attestation.rs:99-134`) accept
**any** peer that merely claims the fixed identity — they check identity equality
and digest binding but verify **no real signature**. They exist for single-host /
offline witnesses and are selected by the `*_offline` / `None` constructors
(`router/src/router.rs:1114-1133`). The production path
(`CriomeIdentityProver` + `CriomeForwardAttestation`, `router.rs:1155-1171`) is
the one that reaches a real criome and enforces `UnknownSigner`. If `.9` deploys
the standing daemon with an offline prover or `None`, authentication degrades to
"trust anyone" / cleartext, silently nullifying all of piece 6. The `.4`/`.6`
code is correct; this is a deploy gate the audit cannot confirm from this code.
Correction: `.9` MUST use `CriomeIdentityProver` and `CriomeForwardAttestation`,
and a witness must prove an unregistered peer is refused on the standing pair.

**M3 — Deploy must pin `Quorum` mode and the admitted 2-of-2 contract, or the
independent re-judge is bypassed.** (observed / interpretation)
`criome/src/actors/root.rs:730-738`: in `AuthorizationMode::AutoApprove` the
re-judge returns `Authorized` **without looking at the evidence at all**, and in
`ClientApproval` it parks. The default is `Quorum` (`root.rs:98`, `daemon.rs:48`)
and the mode is only settable over the **owner-only meta socket**
(`root.rs:357-358`, `meta_signal_criome::Input::Configure`), so it is not
remotely reachable — good. But it is a config footgun: an `AutoApprove` node
auto-authorizes every arriving foreign record. Likewise the Spirit apply gate
must be configured with the real admitted 2-of-2 mirror-contract digest; with no
contract it falls back to a per-object digest (`spirit/src/apply_ingress.rs:124-130`)
that the criome has not admitted, which fails closed as `MissingContract`
(safe) — the risk is *misconfiguration to a weaker contract*, not the fallback.
Correction (deploy invariant `.9` owns): both nodes stay `Quorum`; both local
criomes and the Spirit gate reference the admitted 2-of-2 contract; the peer
identity→key seed is registered on both.

### SHOULD-FIX

**S1 — Caller-supplied round-id: fail-SAFE for authorization, but a liveness /
storage-DoS lever.** (observed)
`criome/src/tables.rs:859-861` upserts the durable round keyed on the round-id
**alone**; `record_vote` (`tables.rs:298-304`) dedups only by voter identity. So:
- A second `ProposeQuorumAuthorization` with a colliding round-id **overwrites**
  an in-flight round's stored state (liveness: the legitimate round is clobbered).
- Votes whose `voter` is not a contract member are stored but never counted (the
  evaluator only counts registered `KeyMember`s), yet they still accumulate in
  the round row — unbounded growth from distinct fake voter identities (storage
  DoS on that row).

This is **fail-safe for authorization** exactly as flagged: a mis-targeted or
colliding vote does not verify, because the vote's BLS signature binds the
operation and moment, and `assemble_evidence` re-stamps against the *stored*
round's operation/proposition (`criome/src/actors/root.rs:1354-1382`,
`language.rs:568-583`) — a vote cast for a different operation fails signature
verification and cannot be counted (**confirmed**). The exposure is liveness, and
it is reachable by whoever can submit criome frames (the trusted peer in 2-of-2;
more relevant at M-of-N). Correction: bind the round-id to the operation digest
(the flagged refinement) so distinct operations cannot collide, and reject a vote
whose `voter` is not a contract member at `submit_quorum_vote` ingress
(`root.rs:1286-1306`).

**S2 — Missing negative witnesses for two load-bearing properties.** (observed)
The witness suite is genuinely adversarial, not happy-path only: it proves
withhold-until-majority and a below-majority `QuorumShort` refusal
(`criome/tests/quorum_collection.rs:189,282-298`), peer-unreachable-waits
(`:303`), unregistered-peer refusal and replayed-proof refusal
(`router/tests/encrypted_peer_session.rs:477,528`), fresh-ephemeral-per-session
(`:587`), plus unit tamper/forward-secrecy/distinct-key checks
(`router/src/peer_session.rs:687-727`) and forward replay/skew/content-binding
(`router/src/forward_attestation.rs:328-397`). Two properties the code enforces
but no test locks:
- **MITM ephemeral-key-swap refusal** — the core anti-MITM property (a swapped
  ephemeral key breaks the signed digest at `verifier.rs:41`). Add a router
  witness that swapping the ephemeral key in a peer's hello yields refusal.
- **Forged/foreign-key vote not counted** — today the short-quorum witness
  *drops* a signature; add one that *injects* a present-but-invalid signature for
  a member and confirms it is not counted (`language.rs:568-583`).

### NICE-TO-HAVE

**N1 — `QuorumShape::is_valid_majority` admits 1-of-1.** (observed)
`criome/src/language.rs:671-674`: `required=1, authorities=1` passes ("majority of
one"). Correct in the abstract, and not reachable for the 2-of-2 mirror (admission
of a 1-member contract is required to hit it, and that is owner-only), but it
means a degenerate single-member contract self-authorizes. Consider rejecting
`authorities < 2` for mirror-class contracts, or documenting that any admitted
1-member contract is equivalent to no quorum.

**N2 — Vote preimage does not bind the contract digest.** (observed)
The `OperationStatement` signing bytes bind {signer, operation, moment}
(`criome/src/language.rs:210-219`) but not the contract. Harmless for the single
mirror contract; a latent generalization risk if the same node-set ever co-signs
the same operation digest under two different-semantics contracts. Consider
folding the contract digest into the vote preimage.

**N3 — Sealed ciphertext carried as `Vec<u64>` (one byte per u64).** (observed)
`router/src/peer_session.rs:464-470` — 8x wire bloat and a silent `as u8`
truncation of out-of-range octets. Not a security bug (the bytes are AEAD-
protected; truncation only makes `open` fail), but a wire-discipline/efficiency
nit worth a `Vec<u8>` payload type.

## What the crypto core actually guarantees (checked, for the record)

- **No sub-majority authorization.** `round_state` marks a round `Authorized`
  **only** when the reused `ContractStore::evaluate` returns `Authorized` on the
  assembled Evidence (`criome/src/actors/root.rs:1319-1340`); `Threshold::decide`
  counts distinct satisfied members and requires `satisfied >= required`
  (`language.rs:418-443`); missing store/registry ⇒ not authorized (fail-closed,
  `root.rs:1329-1335`, `evaluate_authorization` `root.rs:740-750`).
- **Votes bind to member + operation + moment.** `has_valid_signature_from`
  requires the envelope's key to equal the member's *registered* key and a real
  BLS verify over `OperationStatement{signer, operation, stamp-proposition}`
  (`language.rs:568-583`); the signer identity is in the preimage, so one member's
  vote cannot be counted for another, and a cross-operation replay fails.
- **Time-quorum enforced.** The `AttestedMoment` needs a strict-majority of
  registered time authorities' real signatures, checked before the rule
  (`language.rs:620-654`, `ContractStore::evaluate` `language.rs:144-147`); the
  peer independently re-checks the moment names the full member set at its
  threshold (`root.rs:1265-1271,1449-1459`).
- **Admission rejects degenerate sets.** Sub-majority thresholds, empty
  thresholds, and duplicate members are refused at `AdmitContract`
  (`language.rs:455-477`).
- **Mutual, MITM-resistant handshake.** Each side verifies the peer's proof
  against its own criome and its own freshly-issued challenge
  (`router/src/peer_session.rs:320-322,519-529`; `identity_proof.rs:216`); the
  ephemeral key is folded into the signed digest (`identity_proof.rs:301-319`)
  and criome cross-checks the digest (`verifier.rs:41`), so a swapped ephemeral
  key or a swapped identity fails; the BLS preimage binds both the content digest
  and the challenge nonce (`master_key.rs:205-209`).
- **Real forward secrecy + AEAD discipline.** Fresh ephemeral X25519 per session
  consumed by ECDH and dropped (`peer_session.rs:146-169`); directional keys
  KDF'd from the shared secret bound to the transcript, key material zeroized
  (`peer_session.rs:219-241`); nonce = a per-direction monotonic counter that
  errors on overflow, never repeats under a key (`peer_session.rs:243-273`); key
  confirmation proves the peer derived identical keys (`peer_session.rs:351-360`).
- **Fail-closed apply.** The Spirit ingress refuses unless the carried entry
  re-hashes to the authorized operation digest (`spirit/src/apply_ingress.rs:115`),
  the local criome re-judge returns `Authorized` (`engine.rs:786-804`,
  `apply_ingress.rs:170-194`), and criome is reachable/armed (`engine.rs:794-799`).
- **Secrets hygiene.** BLS master key held only in `MasterKey`, persisted 0600
  atomically, never logged, no `Debug` exposure (`criome/src/master_key.rs:35-106`);
  session keys never persisted; nothing prints key material.

## What `.9` (live-wiring) and `.10` (both-directions rewire) must preserve

1. Real criome-backed provers/verifiers on the standing pair (M2); never the
   offline/`None` variants.
2. `authorization_mode = Quorum` on both criomes; both local criomes and the
   Spirit gate reference the admitted 2-of-2 mirror-contract digest; peer
   identity→key seeded on both (M3).
3. Close the plaintext `ForwardMessage` ingress once both daemons speak the
   session (M1); do not flip the live toggle for confidential content while it is
   open.
4. Preserve **withhold-until-authorized**: when rewiring Spirit origination from
   the 1-of-1 gate to the async propose→completion quorum boundary, a pending
   proposal must never surface as a valid record until the round is `Authorized`
   (`root.rs:1319-1349`). Do not introduce a "commit locally, spread later"
   shortcut — that would break "quorum or nothing."
5. Preserve the independent re-judge and content-address re-hash on apply
   (`spirit/src/apply_ingress.rs:115,170-194`) on both directions.
6. Keep session/symmetric keys transient. The `.5` durable outbox stores routed
   objects and delivery state only — it must never persist session or symmetric
   key material.

## Residual risks / checked evidence

- **Not executed, inspected.** I did not run `cargo test`: the stateful witnesses
  spawn criome/router daemons over Unix sockets and require a full workspace
  build (criome + router + signal-* + triad-runtime + kameo), which is heavy and
  I kept off the shared checkout while `.5` is in flight elsewhere. Findings are
  from source reading. Prerequisite to confirm green: a workspace build + the
  named integration tests (`criome/tests/quorum_collection.rs`,
  `router/tests/encrypted_peer_session.rs`,
  `router/tests/criome_forward_lands_in_mirror.rs`). The implementer-named
  witnesses exist in-tree and are adversarial (S2 notes the two gaps).
- **Trust anchor assumption.** Soundness of both the identity proof and the
  quorum rests on the criome registry holding only the correct peer identity→key
  bindings (seeded at deploy). A wrong/extra seed is outside this code; `.9` owns
  it.
- **Time is quorum-attested, not wall-clock-checked** in the evaluator for plain
  `Threshold` contracts (`language.rs:615-654` checks internal consistency + the
  time-signature quorum, not "now ∈ window"). Not a hole for the 2-of-2 mirror
  (it uses no `ActiveAfter`/`ActiveUntil`/`TimeSwitch` rule) and cross-operation
  replay is blocked by the operation digest; noted so a later time-gated contract
  does not assume absolute-time enforcement here.

Owner: rust-auditor (security). Bead: primary-nbmq.11.
