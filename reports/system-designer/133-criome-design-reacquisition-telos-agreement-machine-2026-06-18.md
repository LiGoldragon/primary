# 133 — Criome design reacquisition: criome the agreement machine within Telos, and how my arc plugs in

> **Correction (psyche, 2026-06-18):** an earlier draft of §1 echoed report
> 677's conflation — "Telos is a universal agreement machine, and the quorum is
> its universal primitive." That is wrong. **criome** is the agreement machine
> (the agreement-and-authorization *organ* of Telos, not Telos itself); the
> quorum is **criome's** primitive. Telos is the whole meta-project. The Spirit
> records (`p3td`, `m0p2`, `pviw`) already hold the correct framing; the error
> was in the report. §1 below is corrected; report 677 (designer lane) still
> carries the conflation in its title/§0/diagram and needs the same fix.

*The psyche redirected mid-exchange: they've been doing criome design with the
designer + operator lanes and want me caught up before we proceed. This is that
catch-up, grounded against landed code. Method: a four-reader fan-out (676
comparison, 677 telos, fresh criome/Telos intent, landed criome code) →
synthesis, plus my own read of 677 + 676.5. Companion to the reacquisition in
report 132.*

## 1 — The reframe I'd lost

**Telos is a universal agreement machine, and the quorum is its universal
primitive.** Per `pviw` (Decision, High): [Telos is the name of the meta-project
… whose far horizon is eventual Criome and eventual Sema, the universal
computing paradigm, realized now as Persona]. Per `obuf`: [Telos is a universal
agreement machine for authorizations, and the quorum is its universal primitive
— everything is a quorum].

The insight is a *collapse*: what looked like four machines — an authorizer, a
clock, a divergence resolver, a state propagator — is one mechanism wearing
different clothes. A **quorum** is a threshold of admitted keys, each
contributing a real BLS signature over the *same* `blake3` content-addressed
proposition, stamped with an attested moment. Authorization = a quorum agrees an
act is permitted; time = a quorum agrees a window closed (`ay3y`); divergence =
a quorum agrees which fork wins (`gc0n`); admitted state = a quorum admits an
object, after which its *reference* propagates (`m0p2`). One primitive, two
scopes by membership: **self-quorum** (your own nodes → reliability + credible
time) vs **multi-party quorum** (distinct principals → cross-party trust).

**criome is the daemon that runs that primitive** — and 676 settles what kind of
machine it is: the **predicate/validator family** (Bitcoin Script, Cardano
EUTXO/Plutus, ERC-4337 `validateUserOp`), **not** the stateful-execution-VM
family (EVM/Michelson/Solana BPF). A contract evaluates to a three-valued
`Decision::{Authorized | Rejected | EscalateToPsyche}` and mutates nothing: no
gas (closed acyclic vocabulary halts structurally), no reentrancy (by-digest
acyclic references, never a runtime call), content-addressed immutable objects
(no `UpdateContract` verb), per-daemon SEMA + cross-party quorum instead of a
global ledger. It **leaves the blockchain genus entirely** — no chain, no
miners, no global consensus.

**What landed since 132's sweep (verified live, criome `3c05122`):** the
contract DAG is now durably persisted (`StoredContract` keyed by `ContractDigest`,
a SEMA contract family, `contract_snapshot()` rebuilding the evaluator from SEMA
on load); real BLS12-381 (min-pk via blst) is wired and the placeholder retired;
the attested-moment clock + replay binding are in; `signal-criome 9d8ea38`
carries the full `Contract/Rule/PolicyMember/AttestedMoment/Evidence` wire
surface. **The persistence gap 674/675 worried about is closed** — the criome
leg self-resumes across restart.

## 2 — The settled decisions that bind my lane

| Spirit | Decision | What it binds in my arc |
|---|---|---|
| `wckt` | criome is auth-only; signs/verifies, moves nothing | My router owns byte transport; criome's hop is verdict-only — the architectural justification for the whole arc's separation. |
| `2st7` (High) | criome-auth pilot mechanism is **settled** — authenticate the submitter, after-the-fact non-blocking attestation bound to the per-operation digest | The auth envelope is **no longer open design**; `w2g3` is closed. Build to this shape; verify via the real BLS min-pk path. |
| `d6he` (High) | first e2e milestone = spirit→vcs→criome→router→mirror; quorum announce-*timing* is future criome logic, not a router requirement | Router envelope work proceeds **without** waiting on quorum-timing semantics. The offline full chain already passes. |
| `57f9` (High) | router-typed envelope carries routing+object metadata for a serialized rkyv payload; router payload-blind | Unchanged. `m0p2`'s reference-pushing pulse *reinforces* it — the router fans out references and fetches rkyv objects on demand. |
| `m0p2` | the pulse pushes **references (digests), never payloads**; quorum-backed default | Router/mirror transport bytes on demand by digest; criome only emits the digest. |
| `ay3y` | quorum-attested crystallized-past clock; every signed object carries an `AttestedMoment` | The router envelope must **preserve the `AttestedMoment` stamp** on every BLS-signed frame — never strip or reorder. A sig bound to one moment can't be replayed under another. |
| `ermr` | cluster-root signs member keys; that signature **is** the registry admission gate; cross-host, a BLS attestation chained to the root replaces SO_PEERCRED | The admission-signing ceremony must mint *exactly* this cluster-root signature to bootstrap cross-host trust. |
| `x0ja` (Constraint, High) | one crypto basis — blake3 + criome BLS — across the whole VCS/backup system | Anything the ceremony mints must verify under the *same* BLS min-pk verify the gate uses; no scheme divergence. |

## 3 — How networking-through-the-router plugs into the agreement machine

The reframe elevates my lane's role. The router is not just message forwarding —
it is the **propagation / object-distribution layer of the agreement machine**.
`m0p2`: criome pushes references; components fetch the referenced rkyv object
*through the routing layer*. My M1/M2 forwarding plus the routed-contract-object
delivery operator built on top (`router 629ca92`) is the start of exactly this,
and `57f9`'s payload-blind envelope is its substrate.

Concrete constraints this puts on my design:

- **Fetch-by-digest, not criome-pushed payloads.** The envelope carries the
  reference; the bytes travel on demand.
- **Preserve the `AttestedMoment`** on every signed frame (`ay3y`).
- **criome evaluates locally, never mid-verdict over the router** (no reentrancy
  / no external call). The router must deliver a *complete* signed envelope;
  evidence is assembled before evaluation, not fetched during it.
- **m3 sequencing:** criome on the path is still stubbed (`AcceptFixedTestIdentity`,
  per the 2026-06-16 key-pause). When real attestation lands (m3) it must land
  **together with** router-owned durable replay + freshness (a
  `router-forward-replay` SEMA family rejecting duplicate `(signer, nonce)`, ~5
  min skew) — a valid signed frame is trivially replayable until the seen-window
  is durable.

## 4 — The admission-signing ceremony, sharpened

The criome design does **not** supersede the question I posed earlier — it
sharpens it to near-certainty and isolates the one genuinely-psyche part. The
design answers three of four sub-questions:

- **WHAT to build:** minting is an *effect*; criome is verdict-only (`wckt` + the
  predicate/validator placement), so the daemon structurally cannot be the
  minter. The tool is an **off-daemon one-shot signing CLI** that takes the
  cluster-root secret + an `IdentityRegistration` and emits a `SignatureEnvelope`
  over `RegistrationStatement::to_signing_bytes`, domain-tagged
  `CRIOME-REGISTRATION-ADMISSION-V1`.
- **WHETHER it's needed:** yes — `ermr` makes the cluster-root signature the
  admission gate, and cross-host attestation chained to that root *replaces*
  SO_PEERCRED. Without the mint there is no operable gated cross-host e2e at all.
- **HOW MUCH to invent:** almost nothing. The mint pattern exists verbatim in the
  landed test `cluster_root_gates_registration` (`tests/daemon_skeleton.rs:738`,
  `cluster_root.sign(&statement)`). The ceremony is a **lift of test code, not a
  design**.

What the design does **not** decide — and what is a genuine psyche fork — is the
**authorization to un-defer**: the 2026-06-16 *"no key encryption for now"*
parked the key track, and minting requires the cluster-root signing key to exist
and be usable, arguably inside what was parked. Yet it is signing/admission, not
encryption or production key custody (mlock/zeroize/passphrase/provisioning).
That boundary is the psyche's to resolve. Recommendation: **un-defer just the
ceremony.**

## 5 — Two open forks that bear on the router

677 §3 names two genuinely-undecided seams as *"the right next thing for the
psyche to steer"* — and both touch my lane:

- **Fork A — who computes impact?** Does criome compute the affected set and push
  references (richer criome, more state), or do components **subscribe by
  topic/digest and the router fans out** (criome stays minimal)? The second
  leans with `wckt`'s auth-only grain and the existing push-Subscribe pattern.
  **My lean: A2 (router fans out).**
- **Fork B — what drives the pulse?** Event-driven on admission only, or **also a
  periodic self-quorum time-attestation heartbeat** so "now" stays fresh in
  quiet periods (`ay3y` makes time a quorum object that recedes if never
  re-attested)? A heartbeat is itself a pulse that changes the router's traffic
  model, and it interacts with Fork A. **Dependent on A; revisit after.**

## 6 — Decisions

**Putting to the psyche (gate my next build):**
1. Un-defer just the admission-signing ceremony? (the one concrete unblock)
2. Fork A — router fans out (A2) vs criome computes impact (A1)?

**I'll decide myself (designer-owned), informed by the now-shipped router-object
delivery model:** `ObjectNoticeAccepted` semantics (lean: accepted == head
present/restored) and the router m3 durable-replay shape (skew + SEMA family
name). Fork B I'll hold until Fork A is steered.

## 7 — Live-bring-up seams to track (not silently work around)

- The deployed mirror binds **Tailscale, not Yggdrasil** — unify the fabric for
  the live chain?
- **Name collision:** `router/default.nix` is the WiFi/LAN router
  (hostapd/kea/nftables); the `message-router` deploy module is unbuilt and would
  collide. Resolve before building `criome.nix` / `message-router.nix`.
