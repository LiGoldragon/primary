# Context Handover — Found the persistent root contract (Criome as an on-demand blockchain)

Supersedes the prior `FreshSession-Handover.md`. The mirror stand-up it described
is now built in the components; this handover carries the psyche's forward
direction and is honest about what has not truly happened.

## The focus for the next session (the psyche's architectural intention)

Build the **Criome bootstrap ceremony**: a genuine genesis that founds a
**persistent root contract** — the root of trust and the authorized signer set —
**once and durably**, so nodes stop re-founding identity and trust every time
they boot.

Why this is the essential next work: today the signer set is hand-seeded and each
node's identity key is generated on first boot and exchanged in a two-pass deploy.
That amounts to **haywire-bootstrapping trust on every boot**, and it is why the
mirror is **not production-ready**. A founded, persistent root is the missing
piece.

The design vision in the psyche's words: **Criome is a kind of blockchain, but
with no constant heartbeat — it authorizes on-demand.** The bootstrap ceremony is
what makes it a real one: a genesis root that persists, from which membership and
authority derive, rather than being re-wired each boot.

## The enduring architecture this serves (Criome + mirroring)

- Mirroring is **how Spirit itself operates** over the components that already
  exist — **Spirit, Criome, router** — with no new components. A change recorded
  on one node: the router (the "voice") carries it to the peer router, Criome
  decides genuineness, it becomes a Spirit record on the peer. The larger aim:
  every node converges to the same state — open Spirit on any machine and see the
  same thing.
- **Validity is Criome quorum consensus.** A change becomes real only when a
  majority of nodes' Criomes co-sign it (2-of-3; 2-of-2 for two nodes).
  Quorum-or-nothing; if the quorum cannot be gathered the change **waits** — never
  last-writer-wins. This is architecture (matter), not Spirit intent.
- **The router handshake is Criome-rooted.** On first connect the two routers
  **mutually prove node identity** with a Criome-issued identity proof, then the
  channel is **encrypted per-session with forward secrecy** — identity and
  encryption share **one Criome trust root**. Once a router is wired to its
  Criome, that encrypted, mutually-authenticated session is the only peer path.
  The founded root contract should ultimately anchor this handshake too, so the
  proof derives from the genesis rather than from first-boot seeds.

## Honest state — what is and is not true

- **The persistent root contract does not exist.** Criome has a real majority
  JUDGE (BLS, reboot-durable) and now real cross-node quorum COLLECTION, but the
  authorized signer set is hand-seeded and identities are founded at first boot.
  There is no genesis, no persistent root of trust; the one built trust anchor is
  a single key, not itself a quorum. This is the crux to close.
- **The mirror was never proven live on the standing machines.** All component
  work is merged to the component mains and green in tests / in-process on the
  workbench. The live turn-on on the two standing nodes (`5::7` / `5::8`) was
  planned and gated on psyche go-ahead; it **did not run**. "A real running mirror
  on the metal" is therefore not yet demonstrated, and the single both-directions
  end-to-end run was left for that live proof.
- Already built and test-verified, so the next session does not redo it: router
  self-origination; Spirit live-apply ingress with fail-closed re-judge; the A→B
  live join; Criome 2-of-2 quorum collection (propose → gather → judge → commit,
  withhold when short); mutual identity proof + encrypted router session
  (ephemeral X25519 + ChaCha20-Poly1305, forward secrecy); durable outbox + push
  redial; the off-by-default mirror toggle on the owner-only meta socket; and the
  security cutover (plaintext path closed once session-capable, real verifier
  wired, quorum-required mode with a seeded 2-of-2).
- An independent security review judged the quorum + identity + encryption core
  sound (no forged vote, no sub-quorum change, no impersonation, traffic
  unreadable, forward secrecy holds, keys transient). Its conclusion reinforces
  this focus: real trust rests on a real verifier and a **real, admitted
  contract** — i.e. the founded root the next session builds.

## Open questions for the next session (left open on purpose)

- What is the genesis ceremony — who or what founds the root contract, how is it
  persisted, and how is it authenticated on later boots without re-founding?
- How does membership (the signer set) get admitted and rotated against a
  persistent root, instead of hand-seeded?
- What does "on-demand, no heartbeat" mean for the root — when is authority
  re-checked, and what persists between on-demand authorizations?
- How does the founded root feed both the router identity handshake and the
  mirror quorum, so both derive from one persistent root?

## Pointers (for rediscovery, not re-reading)

- `agent-outputs/PersistentSpiritMirror/CriomeQuorumReadiness-Scout.md` — Criome
  readiness: the judge exists; establishment was hand-loaded, with no founding
  ceremony and a single-key trust anchor. This maps the gap most directly.
- `agent-outputs/PersistentSpiritMirror/MirrorArchitecture-Design.md` — the
  approved mirror architecture (router-mediated, quorum-gated, the Criome-rooted
  encrypted handshake).
- `agent-outputs/PersistentSpiritMirror/SecurityAudit-QuorumAndChannel.md` — the
  security review and its deploy-time must-fixes.
- `agent-outputs/PersistentSpiritMirror/MirrorBuild-Weave.md` — the build weave
  (epic `primary-nbmq`); every bead complete except the live proof, which still
  carries the deploy version bump, the two-node instantiation, and the on-metal
  run.
- Component `ARCHITECTURE.md` files (criome, router, spirit) now document the
  quorum protocol, the Criome-rooted encrypted handshake, and mirror-as-Spirit-
  operation.
