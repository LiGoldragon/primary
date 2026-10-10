# Context Handover — Operational Criome (founding + witness clock + two-round), live-proof pending

Supersedes `Handover-CriomeBootstrapCeremony.md`. Focus: make Criome (spelled
C-R-I-O-M-E) a truly operational, self-founding cryptographic authority. The
core is built, audited, and confirmed in-process; what remains is the live proof
on two test nodes. This handover carries the psyche's full design vision, the
designs deliberately deferred, and the exact current situation.

## Execution model (read first — this was a recurring miscommunication)

The psyche operates nothing by hand. He does not code, deploy, or run commands;
he directs and permits agents, and agents perform every action. "Owner-gated,
no auto-approval" means an authorized agent explicitly performs the act (e.g.
the founding accept) with the psyche's permission — it never means the psyche
types anything. Do not hand the psyche manual steps; carry out the work.

## The design vision (settled psyche intent)

- **The Criome** is all Criomes; a **Criome unit** is one cryptographic contract
  (the existing `Contract` type). Every Criome carries a **`parent`**; authority
  chains to a single global **root**, whose `parent` is a `Root` sentinel (it is
  its own origin).
- **Root identity** is a content-addressed hash of the accepted initial state
  that **commits to the founding keys**; the admitting signatures ride
  **attached** to that anchor, never folded into the hashed body. Identity
  exists at founding.
- **Founding ceremony:** the involved nodes' Criome **master keys** sign;
  **unanimous / total vote** (every node willingly establishes its root);
  acceptance is an **explicit owner-gated action on the meta socket, no
  auto-approval**; conveyed **over the router** (node identity = Criome master
  pubkey; no new peer lane). On reboot the node re-verifies the anchor and every
  attached signature and **never re-founds**.
- **Witness clock:** each signer signs a request only if **its own clock** reads
  now inside the request's time window, refusing otherwise — so every signature
  testifies "this time is now." The quorum's signing forms a consensus **Criome
  clock**; on-demand, no heartbeat. A request whose window would exceed a lease
  is invalid.
- **Two-round commit:** a round-1 majority only *opens* round 2; only a round-2
  majority — each round-2 signer having independently verified a round-1
  majority — authorizes. Round 2 need not be a subset of round 1 (a
  majority-of-total guarantees honest overlap). Stop at two rounds; both rounds
  fall inside the window. **Non-double-signing:** an honest node refuses a
  second *conflicting* successor to the same Criome (one honest successor per
  `(contract, head)`) — this carries safety without an explicit refusal list; a
  conflicting proposal gets an explicit refused/resubmit.
- **Ownership:** default **self-owned** (a parent cannot unilaterally revoke a
  child). Root **founding is unanimous**; root **rotation is threshold-quorum,
  not unanimous** (one lost/offline node must never freeze the root).
- **Deployment authority is the point:** Criome is meant to become the
  authentication/authorization layer for deployment, with SSH kept only as a
  fallback. (The deploy-authorization object + deployer wiring were scoped out
  of this build; the live proof authorizes a *native* Criome op, not a real
  deployment.)

## Deferred by design (phase-2; the data model preserves all of it)

- **Leased self-ownership:** a parent grants time-bounded self-ownership; the
  child renews to stay live; on lapse ownership reverts to the parent —
  implemented as **passive local expiry** (a stale grant fails to validate), not
  broadcast revocation. `window ⊆ lease` is a signer-side refusal. A lease seam
  sits beside the clock gate.
- **Sub-Criome as a quorum member:** a member can itself be a sub-Criome
  (recursive quorum) via **sign-the-same-object-everywhere + a participation
  bitmap** (not sub-certificates over different messages). **Membership ≠
  parentage** — any Criome may be a member of any other's quorum without being
  its child. A sub-Criome voting elsewhere is not mutating its own state, so its
  lease does not gate its vote. Host keeps unilateral power to drop a member;
  evaluation must be acyclic / depth-bounded.
- **Commutative-merge concurrency:** compatible (order-independent, same
  end-state) changes may both commit; requires mechanically-decidable, agreed
  commutativity and a merge-capable state model. The non-double-sign conflict
  predicate is kept pluggable for this.
- **Sparse replication:** a node holds only its ancestor line to the root (plus
  any referenced member-Criomes and *their* ancestors); the root is the only
  globally-shared object.
- **Cold / hardware-wallet root keys:** eventually root keys on a hardware
  wallet (Ledger). Tension: BLS aggregation is poorly supported on consumer
  wallets (which favor Ed25519/secp256k1) — likely a scheme split (BLS for the
  quorum, a wallet-friendly curve for cold custody). Founding signatures are
  already scheme-tagged for this.
- **Byzantine safety at scale:** the code implements honest majority-of-total,
  safe/veto-strong at 2-of-2; at n≥3 a supermajority (2f+1 of 3f+1) is required.
  The limit is documented, not overclaimed.
- **Root rotation** (old+new co-sign), a **parent-revocable ownership type**,
  and **universal-lease dead-state (lost-key zombie) handling** remain unbuilt.
- **Closest prior art: KERI** (self-certifying genesis, delegation, witness
  receipts, log-replay) plus TUF, ACME/Vault, Roughtime, Certificate
  Transparency.

## Built, pushed, audited, confirmed (completed)

Tracker epic **`primary-79z1`**.

- **criome `main` `0608a42c` (0.5.0):** founding ceremony + reboot-verify +
  cross-node founding conveyance over the router; per-signer witness-clock gate
  (both the signer and the peer re-check, on both rounds); two-round commit;
  non-double-sign with a durable, restart-surviving anti-equivocation ledger;
  the operator CLI **`criome-founding`** (`observe-node-public-key`,
  `initiate-founding`, `observe-founding`, `accept-founding`).
- **signal-criome 0.8.0 (`c71ef716`)** and **meta-signal-criome 0.5.0
  (`bf916c1d`):** the wire contract — the `parent` field + `Root` sentinel,
  founding-certificate types (anchor commits to keys, signatures attached and
  scheme-tagged), `RoundPhase`, and the founding + conveyance ops. Append-only,
  no discriminant shift; clean-genesis re-digest (test nodes hold nothing to
  preserve).
- **CriomOS `399f29e79f48`:** test-VM criome deploy modules reconciled — the old
  hand-seeded trust anchor / signer set fully **retired** (the ceremony replaces
  it), public working socket + owner-only `0600` meta socket configured. Pins
  criome `cee89b9b` — **needs bumping to `0608a42c`.**
- **Independent audit + confirmation:** the cryptographic core delivers its
  properties — no forged clock, no sub-quorum authorization, no partial or
  forged founding, no impersonation, no auto-approval, no Byzantine overclaim.
  Three HIGH defects were found and fixed and independently re-confirmed: F1
  (the cluster wedged after one committed change — non-originators now converge
  on the same head), F2 (the anti-equivocation ledger was RAM-only — now durable
  and reconstructed on boot), F3 (the founding initiator did not BLS-verify a
  conveyed peer signature — now verified before unanimity). One LOW residual
  closed (the veto is now written durable-first, so a vote is never emitted
  without its persisted veto row).
- Two-node founding and repeated-deploy convergence are proven **in-process**
  (full suites + `nix flake check` green). **Not yet run live on the nodes.**

## Current situation — the live proof (open; bead `primary-79z1.15`)

Goal: deploy criome+router to the two test nodes **`mirror-alpha` (5::7)** /
**`mirror-beta` (5::8)** via lojix behind a horizon feature, found a 2-of-2 root
cross-node, then authorize a native head-advance op through the two-round commit
under the clock gate — capturing anchor-identical founding and an agreed op on
both nodes.

Confirmed facts:
- The mirror nodes are already proper **lojix-managed cluster nodes**
  (`goldragon/datom.nota`, `TestVm`/`Pod` guests hosted on `prometheus`,
  services `[(TailnetClient)]`). No re-modeling needed.
- This session's host is **ouranos**, which runs the lojix daemon locally
  (`lojix-daemon.service`, deployed `lojix-0.4.1`; owner socket
  `/run/lojix/owner.sock` owned by `li`, so deploys are admissible).

Settled model and open items:
- **The feature is a horizon feature defined in horizon-rs** — that is its
  designed home. Add a **`NodeService::CriomeTesting`** variant (follow the
  `WebHost` addition pattern), and a CriomOS `criome-testing.nix` module that,
  when the service is enabled, boots criome (public + owner-meta sockets) + the
  co-resident router and ships the `criome-founding` CLI. **Remove** the
  half-wired `PersonaRouter` feature (`persona-router.nix` gates on a service
  absent from the schema) — the psyche confirmed it can go.
- **Deployer bootstrapping (confirmed hazard):** lojix compiles the horizon
  schema **into the daemon**; `NodeService::from_nota` is a closed match with no
  catch-all. So adding `CriomeTesting` to `datom.nota` while the running daemon
  lacks the variant breaks projection of the **whole cluster**. The deployer
  (lojix on ouranos) must be **rebuilt and self-redeployed** with the new
  variant *before* the cluster data references it. The psyche approved this
  self-redeploy of ouranos.
- **`drop-next` branches (verify current state before acting).** lojix pins
  `horizon-lib` to horizon-rs's `drop-next` branch (`Cargo.toml`); an earlier
  check found horizon-rs `origin/drop-next` == `origin/main`. But a
  **synchronizer** actively advances `drop-next` branches across the lojix repos
  (it moved lojix's own `drop-next` on 2026-07-04), so re-verify before assuming
  the `drop-next → main` repoint is a no-op. Do the repoint in a worktree. lojix
  `main` is currently clean; a prior agent's stray working-copy work (a checked-in
  schema regeneration, authored under the psyche's identity) is preserved on
  origin at bookmark `recovered/drop-next-7a7ffabf`.
- **The tailnet is not the deploy path** (open). The psyche states the tailnet
  code "was never useful, never brought up." A worker observed lojix activating
  via `ssh-ng://root@<node>.<cluster>.criome` over MagicDNS — which the dead
  tailnet cannot serve. The real reachability path (prometheus answered over
  **yggdrasil**) must be determined, and lojix's activation path corrected if it
  wrongly assumes the tailnet.
- **The guests were never instantiated** (lojix `Query` → `GenerationUnknown`
  for all nodes). `prometheus` (Host) must be deployed to stand up the mirror
  `Pod` guests before the mirrors are reachable/deployable.

Shape of the remaining work (all agent-executed, with psyche permission): add
`CriomeTesting` to horizon-rs `main` and remove `PersonaRouter`; repoint lojix `horizon-lib` to
`main` in a worktree; add the CriomOS `criome-testing.nix` module and bump the
criome input to `0608a42c`; rebuild and self-redeploy the ouranos lojix daemon;
determine the real node-reachability path; add `(CriomeTesting)` to the mirror
nodes in `datom.nota` (only after the daemon is rebuilt); deploy prometheus to
instantiate the guests, then the mirrors; drive `criome-founding` (observe keys
→ assemble cohort → initiate → agent performs the explicit accept on both →
observe `Founded` with the same anchor); then authorize a native head-advance op
through two-round + clock-gate and confirm both nodes agree.

## Doctrine / skill fixes the psyche flagged (matter, for a skill-editor lane)

- Docs/skills wrongly imply a node-service feature can be added without
  rebuilding the deployer. Reality: node-service features are defined in
  **horizon-rs** and require a **deployer rebuild + redeploy** before the cluster
  data references them (the schema is compiled into lojix).
- An agent left stray working-copy work in the shared lojix checkout instead of a
  worktree. Skills need a documented **worktree rule** and a **dirty-peer-checkout
  recovery** procedure (preserve the work on a pushed branch, restore `main`).
- The **`general-code-implementer` claim lane is shared** across concurrent
  agents; `(Observe Roles)` does not surface such ad-hoc lanes, and
  `(Release <lane>)` is **wholesale** — it drops every claim held under the lane,
  not just the intended path. This inadvertently dropped peer claims twice this
  session (CriomOS-home/chroma; router/signal-spirit — both re-claimed, though
  the peers' original reason strings were lost). Fix direction: a path-scoped
  release, and/or surface ad-hoc lanes in Observe.

## Artifact pointers

- `agent-outputs/PersistentSpiritMirror/CriomeOperational-SpecAndBuildPlan.md` —
  the protocol spec + build plan.
- `agent-outputs/PersistentSpiritMirror/CriomeCeremony-CurrentStateScout.md` —
  current-state code map (pre-build; still useful for orientation).
- `agent-outputs/PersistentSpiritMirror/CriomePriorArt-Research.md` — KERI/TUF/
  Roughtime/CT prior-art mapping.
- Tracker epic `primary-79z1` (all beads closed except `.15` live proof).
