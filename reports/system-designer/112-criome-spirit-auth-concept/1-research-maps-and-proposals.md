# 112.1 — research maps and mechanism proposals

Four research maps over the pinned source, then the three mechanism proposals the
design phase produced. All file:line references are confirmed against the pinned
checkouts under `/git/github.com/LiGoldragon/`.

## Map 1 — the criome capability surface (and the skeleton reality)

criome is a single-Unix-user Kameo daemon exposing a closed
`CriomeRequest`/`CriomeReply` wire over length-prefixed `signal-frame`, reached over
a `0600` Unix socket; a client sends exactly one request and reads exactly one reply.
It offers two distinct "authenticate an operation" shapes:

1. **Attestation** — `Sign(SignRequest)` over a free `ContentReference{digest,
   purpose, schema_version}` → `SignReceipt{attestation}` carrying an out-of-band
   `Attestation{content, signer, envelope: SignatureEnvelope{scheme, public_key,
   signature: BlsSignature}, issued_at, expires_at, audit_context}`. (`AttestArchive`
   is locked to `ComponentRelease`, `AttestAuthorization` to `Authorization` content
   — only `Sign` takes a free `ContentReference`.) `signal-criome/schema/lib.schema:7,263`.
2. **Routed-authorization** — `AuthorizeSignalCall(SignalCallAuthorization{
   request_digest, contract, operation, scope, requester, nonce, expires_at})` →
   `AuthorizationPending`; peers `RouteSignatureRequest`/`SubmitSignature`; observed
   via `ObserveAuthorization`; verified via `VerifyAuthorization`. Permission is
   constituted by signatures over the exact `request_digest` that satisfy criome's
   policy, returned as `AuthorizationGranted(AuthorizationGrant)`. There is **no**
   `RequestAuthorization` variant — `AuthorizeSignalCall` is the entry point.

**THE LOAD-BEARING FINDING — criome's cryptographic core is a skeleton.** Today criome
is a typed-record router with durable state and a live replay/expiry guard, **not a
working BLS authenticator**:

- Signing emits the literal placeholder string `criome-skeleton-bls-signature` — no
  `blst` key load, no real sign (`criome/src/actors/signer.rs:94-95`).
- `VerifyAttestation` returns `InvalidSignature` even on a fully-matching attestation
  (real BLS verify unimplemented) (`criome/src/actors/verifier.rs:58`).
- `AuthorizeSignalCall` never consults a policy table and **always returns
  `AuthorizationPending`** — the grant path (policy lookup, master-key signing,
  quorum aggregation) is unbuilt (`criome/src/actors/authorization.rs:104-126`).
- **No caller authentication on the socket at all** — any same-UID process connects
  and is trusted; the `0600` mode is the entire boundary (`criome/src/daemon.rs:73`).
- `RegisterIdentity` does not yet verify the architecturally-required Developer/master
  signature — it only dedups and stores, so the registry is not yet trustworthy
  (`criome/src/registry.rs:90`).
- `ObjectDigest{value:String}` is `blake3(bytes).to_hex()`; the digest is supplied by
  the **client** — criome never recomputes it (`signal-criome/src/lib.rs:56-60`).
- `ContentPurpose` (closed) = `SignedObject | ComponentRelease | ChannelGrant |
  ChannelRetract | Authorization | Archive | PrivilegeElevation` — no spirit/intent
  variant; `PrivilegeElevation` and `Archive` already exist
  (`signal-criome/schema/lib.schema:59`).

Consequence: every layer of any design is gated on criome's real `blst` sign/verify
milestone. Spirit-side work can proceed against the placeholder, but nothing is
**end-to-end verifiable** until criome's next cryptographic milestone ships.

## Map 2 — spirit's write path and the caller-identity gap

Write path: emitted daemon reads `ConnectionContext` (kernel SO_PEERCRED uid/gid/pid)
→ `WorkingTransport` decodes a typed `Input` → `EngineActor` mailbox serializes →
`SpiritDaemon::handle_working_input` (`daemon.rs:139`) → `Engine::handle_async` →
`Nexus::guard_record` (`nexus.rs:602`) judges record CONTENT via the LLM guardian →
`Store::record_entry` commits to the `*.sema` log → `Output::RecordAccepted`.

**The exact defect the pilot targets:** at `daemon.rs:142` the binding is
`_connection: &triad_runtime::ConnectionContext` — the kernel-vouched peer identity
is captured by the transport and then **thrown away** before the engine sees it. The
guardian judges WHAT is written; **nothing binds WHO wrote it.** An owner-only import
path bypasses the guardian entirely, which makes authentication more urgent, not
optional.

Hooks: the `guard_*` seam (between guardian-accept `nexus.rs:609` and
`store.record_entry` `nexus.rs:612`) is a single `&mut Nexus` single-flight chokepoint
all seven content mutations share — the natural before-commit insertion point. Spirit
already has the exact client machinery needed (blocking `UnixStream` +
`block_in_place` + `LengthPrefixedCodec`) in `AgentGuardian::call_agent`, and a
fail-closed posture on guardian `HarnessUnavailable` (`nexus.rs:744`) to mirror.

## Map 3 — sema content-addressing: what is signable, and the deploy reality

- **`EntryDigest`** — a real 32-byte blake3 over (domain-tag
  `sema-engine-versioned-commit-log-entry-v2`, store_name, schema-hash,
  commit_sequence, snapshot, previous_entry_digest, each operation's update_digest),
  rendered to lowercase hex. `from_entry_fields` folds `previous_entry_digest`, so
  **one chain-head signature transitively commits the entire prior log**. This is the
  cryptographically-adequate signing target.
- **`StateDigest`** — a whole-store blake3 fold **truncated to a 64-bit Integer**
  (`store/mod.rs:1018`). Cryptographically inadequate; **must not be signed**. Spirit
  surfaces only this on the wire today — there is no `EntryDigest` accessor yet.
- **Deploy coupling.** Deployed spirit (0.13.0) runs the 0.4.0-era engine (rev
  `dbe29427`), which stores `EntryDigest` on every entry but has **no**
  `versioned_chain_head()` accessor — the O(1) head exists only at 0.6.2
  (`engine.rs:1084`). **Both** criome and spirit source trees pin sema-engine
  `branch=main` (0.6.2) — so the pilot is more 0.6.x-coupled than "ship on 0.4.0"
  implies; building from current sources against 0.4.0 would require un-bumping the
  pin. Per-commit head read is O(n) on 0.4.0 (negligible at 1258 records),
  O(1) on 0.6.x.

## Map 4 — principal model and fit

criome's identity registry knows `Persona | Agent | Host | Developer | Cluster`. The
pilot's hard question (Map 2's gap): a spirit caller maps to **which** principal? The
SO_PEERCRED uid is an OS access-control fact, **not a BLS signature** — so "the uid"
authenticates the *connection's owner*, while "a registered Identity that signed the
request" authenticates the *caller cryptographically*. These are different security
claims. The pilot fits criome's first verifier-shaped milestone and the Lojix
routed-authorization pattern, but pushes criome beyond it in three places: a real
sign/verify path, a trustworthy `RegisterIdentity`, and (for human-approval) the
not-yet-existing `meta-signal-criome` contract.

## The three mechanism proposals

- **P1 — after-the-fact, out-of-band attestation (non-blocking).** After the guardian
  accepts and the record commits, spirit asks its local criome to attest over the
  committed entry's `ObjectDigest`; the `Attestation` is a separate out-of-band record
  keyed by the entry digest. The write never waits on criome. Honors out-of-band
  discipline; lowest write-path risk.
- **P2 — authorize-before-commit (blocking gate).** After guardian-accept, before
  commit, spirit asks criome to authorize the exact request digest and commits only on
  a grant; routine via escalation-to-sign, sensitive via escalation-to-approve.
  *Strongest prevention, but:* criome's authorization is **async-by-design**
  (`AuthorizationPending` → `ObserveAuthorization`), so a synchronous gate is not on
  the wire — P2 requires a deferred-commit state machine spirit lacks plus
  `meta-signal-criome` (for approve), which does not exist.
- **P3 — sign the log identity (chain-head attestation).** criome attests over the
  `EntryDigest` chain-head, making the whole genesis-chained log tamper-evident under
  criome's key; per-commit now, batched/checkpointed later. Strong integrity witness;
  but binds the **log to criome's key**, not the submitter.

The synthesis blended these; the critic showed the blend hid a fourth, better cell
(after-the-fact attestation that binds the **caller**) — carried into
`2-concept-decisions.md`.
