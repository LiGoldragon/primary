# 8 — overview: the cloud verdict

cloud-designer, 2026-06-07. Synthesis of the six explorer dimensions + four
adversarial verifications + the completeness census (workflow `wwudq57zz`, 11
agents). The highest-numbered file IS the synthesis. This zooms
`reports/cloud-designer/35-actor-divergence-forensics/` onto cloud and reaches a
**sharper** verdict than the workspace-wide one.

## The one-paragraph answer

cloud is the **sharpest instance of the actor divergence in the workspace, and the
least defensible**. Where report-35's workspace verdict was "neither a clean good
reason nor a clean hallucination — two skills contradict each other," cloud's verdict
is harder: cloud **contradicts itself inside its own repo** (its `ARCHITECTURE.md`
§"Actor Shape" mandates one-actor-per-concern with a "provider calls must not block
the listener" rule that its production code **actively violates** with an unbounded
stall), and the actor pattern it mandates is **already implemented next door in
`criome` with kameo 0.20 today, on the same domain**. There is no surviving "sync was
necessary" steelman: actor-per-concern is proven buildable here, the blocking hazard
is a real (untested) production bug against cloud's own written constraint, and the
actor fix is achievable **in cloud alone** without any substrate change. What sync
*does* legitimately rest on is narrow — the synchronous engine-trait **spine** is
inherited from the blessed `1483`/`1487` deferral. Everything above that spine is
cloud's own unblessed, self-contradicting choice.

## What's verified (load-bearing, all confirmed)

- **Zero actors, both runtimes.** No kameo, no tokio, no `impl Actor` anywhere in
  cloud — confirmed by grep, Cargo.lock transitive closure, and `git -S kameo --all`
  (kameo **never existed in any commit**). cloud runs two sync, actorless runtimes
  (files 1, 2).
- **The production runtime violates cloud's own no-block rule.** The live legacy
  `Daemon` holds a single global `Arc<Mutex<Store>>` **across** a blocking,
  **timeout-free** `flarectl` subprocess; both listeners share that lock; each accept
  loop is serial. One hung `flarectl` = **unbounded stall of both sockets and all
  clients**. Directly contradicts `ARCHITECTURE.md:40-41` (file 4, thesis-3
  confirmed).
- **§"Actor Shape" is frozen, unimplemented aspiration** — byte-identical since its
  birth commit, never reconciled when the schema track landed, and the
  implementation-slice section even **dropped** its earlier actor language while
  leaving the mandate header standing (files 3, 5).
- **No cloud-topic Spirit record blesses sync OR mandates actors.** The 58 cloud
  records govern stack choice and the two-contract split; the thread-vs-actor
  question is governed only at the workspace level by non-cloud-tagged records
  (`2alg`/`k6w1`/`tj99` shape; `1483`/`1487` deferral) (file 3).

## The decisive new evidence this audit added beyond report-35

1. **The workspace is bifurcated, and the mandate is proven buildable next door.**
   `nexus` and **`criome`** run full kameo 0.20 actor stacks — `criome/src/actors/`
   is a living actor-per-concern tree (`root`/`store`/`registry`/`signer`/`verifier`/
   `authorization`/`subscription`). cloud's §"Actor Shape" is **almost verbatim the
   realized `criome` pattern.** So the mandate is not abstract: it is implemented on
   the same domain, today. cloud was simply placed on the sync triad stack while
   authoring an actor mandate copied from the kameo stack (file 7, MISS-1).
2. **The actor design was ACTIVE intent, abandoned mid-flight — not idle
   aspiration.** Fossil evidence: a test literally named
   `…uses_provider_actor_and_caches_last_known_state` whose body is a plain mutex
   field (MISS-3); the contract's `UnsupportedReason::ProviderRateLimited` defined but
   unused (the `RateLimitGate` seam, MISS-5); the dropped slice-language (file 5).
3. **The fix is cloud-local.** The emitted `ComponentDaemon` engine is an opaque
   `type Engine` accessed by `&Engine`; cloud can make it a kameo `ActorRef` tree and
   bridge sync→actor at `handle_working_input`, **with no triad-runtime or emitter
   change** (file 6, thesis-4). The substrate explicitly leaves this hole
   (`workers.rs:13`).
4. **cloud has a structural twin.** `domain-criome` is the same actorless template;
   the criome domain runs **three** daemons — `criome` (actors) + `cloud` +
   `domain-criome` (both sync). Any template fix touches both (MISS-2).

## The layered truth (cloud-specific, mirrors report-35's three layers)

| Layer | Status | Verdict |
|---|---|---|
| Sync engine-trait **spine** (accept loop + decode→execute→encode) | **Inherited + blessed.** Forced by triad-runtime + emitter; rests on the recorded `1483`/`1487` deferral. | Legitimate. Cannot be made actor-native by cloud alone. |
| **Actor tree** behind the spine (the five named concern-actors) | **Cloud's own choice.** The door was left open; cloud chose `Engine = Arc<SchemaStore>` instead. | Unblessed; contradicts `actor-systems.md` **and cloud's own `ARCHITECTURE.md`**. |
| The **blocking hazard** in the live legacy runtime | **A real, untested production bug.** Global lock across timeout-free IO + serial accept = unbounded stall. | Violates cloud's own written constraint; arguably must be fixed regardless of the actor decision. |
| The **bounded-thread (`k6w1`) fallback** | **Unrealized everywhere.** `BoundedWorkers` exported, zero callers across the whole triad stack. | The "we have a concurrency story" claim is currently empty. |

## What was withdrawn / corrected (keeping myself honest)

- The in-cloud framing "unblessed-but-**consistent** realization" is **too generous**
  — it only looks consistent if you don't look sideways at `criome`.
- The "thread-per-connection via triad-runtime" claim was **wrong**: the realized
  schema path is single-threaded serial (`BoundedWorkers` is dead). Corrected in
  files 2, 6, 7.
- "cloud's most explicit unfulfilled mandate" (superlative) and "only `ba35849`"
  (provenance) were trimmed as unverified/imprecise (file 7).

## The decision the psyche faces (genuinely theirs — no Spirit recorded this turn)

This is the same fork as report-35, now with cloud-specific stakes, a live
counter-example, and a clear cloud-local path. Three things to decide:

- **A — actors now (cloud-local), matching your instinct and `criome`.** Make
  `cloud`'s `type Engine` a kameo `ActorRef` tree (`CloudflareProvider` as a
  blocking-plane `CommandPool` with timeouts, `PlanStore`/`PolicyStore` owning their
  state), bridged behind the sync triad spine. No substrate change. Retire/realize
  §"Actor Shape" instead of leaving it frozen. The same template lands in
  `domain-criome`. This is what `criome` already proves works.
- **B — keep sync, reconcile the docs.** Accept the sync engine-trait substrate as
  cloud's end-state, **delete or de-mandate** §"Actor Shape" (it currently reads as a
  live mandate with no backing), and update `actor-systems.md` to carry the
  carve-out. Weaker: it leaves the criome domain straddling two substrates with no
  recorded reason, and still requires fixing the blocking hazard.
- **The one fix that's arguably independent of A/B:** the **blocking hazard** is a
  real production bug against cloud's own constraint. Even under B, at minimum drop
  the coarse outer `Arc<Mutex<Store>>` (decouples the two listeners; `Store` already
  has fine-grained locks) and add provider-call timeouts. Under A it dissolves
  naturally into the provider actor.

**Two questions only the psyche can answer**, because no intent record does:
1. Direction A or B for cloud (and therefore `domain-criome`)?
2. **Why does the criome domain straddle both substrates** — is cloud/domain-criome's
   placement on the sync stack a deliberate decision, or an unblessed default that
   should converge onto `criome`'s actor stack? This is the root question; the answer
   becomes the Spirit record that supersedes/clarifies the frozen §"Actor Shape" and
   ties back to `1483`/`1487`.

My read, stated plainly and held as a recommendation not a decision: **A**, because
`criome` removes the only real objection (buildability) and the fix is cloud-local —
but the cross-domain "why two substrates" question (2) is the psyche's to settle
first, since it governs both cloud and `domain-criome` and is the thing no record
currently answers.
