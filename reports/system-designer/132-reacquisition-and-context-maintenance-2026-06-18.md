# 132 — Reacquisition + context maintenance: the corrected state, the live arc, the one blocker

*The psyche asked me to reacquire recent reports and Spirit, do a context
maintenance pass, and bring forward the most pressing issues and questions.
This is that pass. Method: a six-reader fan-out (my lane, operator,
prime-designer criome, other lanes, Spirit intent, branch+bead state) →
synthesis → an adversarial completeness critic, then my own direct
verification of the two load-bearing facts. The critic caught a real
synthesis error (below); I corrected it before writing anything here.*

## 1 — Two beliefs my post-compaction context carried were wrong

My summarized context said (a) "ebev rollout is my live thread with an open
sequencing question" and (b) "networking through the router is paused." Both
are stale, and one is inverted:

- **ebev was overtaken twice.** It was live the morning of 2026-06-17, then
  the spirit→criome→router→mirror PoC slices (reports 123–128) took over,
  then the Spirit-guardian admission-gate thread (129/130/131) took over from
  *that*. My genuinely most-recent landed work is the **guardian
  negative-guideline deploy** (report 131, 2026-06-18 10:31) — done, on main
  across the spirit triad, deployed live to ouranos (`spirit` 0.14.0).
- **Networking is not paused — it is the active, psyche-directed arc.** The
  2026-06-16 directive was *"lets not worry about key encryption for now. we
  need networking through the router."* What is deferred is the
  **key-encryption / key-custody track**, not networking. I had conflated the
  two. M1 (signal-router forwarding contract) + M2 (router transport) **landed
  on main** (operator rebase-replayed; the `router-network-transport` origin
  branches are now stale duplicates — content is mainlined, original SHAs are
  not ancestors, **do not re-push them**). Operator built routed-contract-object
  delivery on top (`router` main `629ca92`).

## 2 — The 15df correction (a methodology trap worth recording)

The synthesis claimed Spirit record `15df` (the ebev anchor) "does not exist
in the store" and built a maintenance action + an open question around a
fabricated "anchoring gap." The critic flagged it; I verified directly with
`Lookup` (which bypasses observation filters):

> Per Spirit `15df` (Correction, High): [Intent single source of truth becomes
> Spirit: capture and query intent in one place, not in per-repo files. Each
> repo ARCHITECTURE.md is the file kept current for architectural state.
> Per-repo INTENT.md files migrate off into Spirit gradually, opportunistically
> whenever a repo is touched. Read intent now means read Spirit.]

`15df` is live and `bead primary-ebev` cites it correctly. Two reader agents
hit the same trap: `PublicTextSearch` is **full-text over descriptions and
referents, not an ID lookup** — searching the bare token `15df` returns
nothing, which they misread as "absent." For ID retrieval use `(Lookup <id>)`.
ebev is properly anchored; there is no capture-first gate before any future
doc-rewrite — the genuine ebev question is purely sequencing.

## 3 — My lane's actual threads (system-designer)

| Thread | State | Reality |
|---|---|---|
| Guardian admission gate (130/131) | **done** | Landed on the spirit triad mains, deployed live to ouranos. `NegativeGuideline` rejection verified through the deployed CLI. |
| spirit→criome→router→mirror chain + networking | **live arc** | M1/M2 networking landed; 5-branch offline-e2e stack landed (`xj51`); criome real BLS + admission gate landed (`kr40` core). Three of my feature branches remain (object-notice, router-m3 scaffold, criome SpiritLogObject auth). Offline full-chain PoC green. |
| ebev (intent substrate) | **parked, anchored** | Mechanism (`spirit-render`) built + landed on `spirit` main; anchored by `15df`. Remaining = deploy (operator) + the AGENTS.md/intent-skills rewrite (psyche-scoped) + gradual per-repo migration. Not the foreground. |
| criome key-encryption / cluster-root provisioning | **deferred (psyche)** | Blocks M3/M4, `at7x`, `5zur`. The admission **gate** exists + is tested; only the admission-**signing ceremony** is missing. |

The two designer-owned decisions that gate finishing my in-flight branches —
I will resolve these myself, not put them to the psyche:

1. **`ObjectNoticeAccepted` semantics** (signal-mirror `mirror-object-notice`,
   `24ee1949`). Lean: *accepted == announced head present/restored*, with a
   separate queued/deferred reply for mere admission. Now sharpened by the fact
   that operator's routed-object-delivery model already shipped (`router`
   `37f9387`/`629ca92`) — the mirror reply must fit a delivery model that
   exists, which pushes toward present/restored.
2. **Router m3 durable replay shape** (report 125). The replay window is
   process-local memory today; it must land **with** real attestation, not
   after (a valid signed frame is trivially replayable until the
   seen-`(signer, nonce)` window is durable). Open: skew tolerance (m3 default
   5 min) and the durable SEMA family name/shape (shared with operator, who
   owns durable storage).

## 4 — The single isolated blocker (verified)

Per primary commit `c8f2f51f` and my direct check of `criome` `origin/main`
(`3c05122`): `src/admission.rs` is present (`ClusterRoot::admits` +
`cluster_root_gates_registration` tested), the BLS placeholder is retired
("…is retired; this is real"), and `src/bin` contains **only**
`criome-daemon.rs` — **no minting/ceremony binary exists**. So the entire
criome/networking arc collapses to one missing piece: a tool that **mints a
cluster-root-signed `RegistrationStatement`** (the cluster-root admission-
signing ceremony). One decision to build it unblocks `9x9f` M3/M4, `at7x`
remaining slices, and `5zur` entirely.

It sits in the seam between the deferred key-custody track and the active
networking track, which is why it needs a psyche ruling: minting requires the
cluster-root signing key to exist and be usable — arguably part of what
*"don't worry about key encryption"* parked — yet it is admission/signing, not
encryption or production key custody (mlock/zeroize/passphrase/provisioning).

## 5 — Top pressing issues (ranked)

1. **(self — corrected) My next move starts from "guardian is done — what's
   next on the live arc," not "resume ebev."** Acting on the stale frame would
   re-open a parked thread and risk re-pushing rebase-replayed branches over
   current main.
2. **(needs psyche) The cluster-root admission-signing ceremony** — §4. The
   smallest concrete unblock for three threads; the gate is already built and
   tested.
3. **(self) Resolve the two designer-owned decisions** in §3 and finish the
   three in-flight feature branches to a clean, integration-ready state for
   operator. This is offline/contract work — **not** gated on the key track,
   so it is productive regardless of the §4 decision.
4. **(operator → me) Incoming schema break.** Operator's strict-positional
   struct syntax (report 412, Spirit `lpk9`, branch `schema-namespaces-poc`
   `af3705c` — *not yet on `schema-next` main*) retires the old struct-body
   pair form across ~52 consumer `.schema` files. Part of the positional port
   is already on `router`/`signal-router` main; the namespaces wave is staged.
   I must author new schemas in the new form and migrate mine ahead of / with
   the land.
5. **(system-operator loose end) FullOS deploy.** The guardian deploy used the
   CriomOS-home HomeOnly path; the FullOS switch against `CriomOS/main` is
   blocked by an unrelated eval error — `attribute 'testVm' missing` in
   `modules/nixos/test-vm-guest.nix`.

## 6 — Open question for the psyche

**Un-defer the cluster-root admission-signing ceremony?** This is the one fork
whose answer changes what I do next; I am asking via `AskUserQuestion`.
Recommendation: **un-defer just the admission-signing ceremony** (build the
one-shot cluster-root signing CLI; keep production key custody deferred) —
it's the single unblock for three threads and the gate is already built. The
honest caveat: it touches the key track the psyche parked, so it is a genuine
ruling, not mine to assume.

Lower-priority, surfaced but not asked as modal forks:

- **ebev sequencing** (rewrite-now vs deploy-pilot-first) is real but parked;
  `15df` itself says migration is *"gradual, opportunistic"* and the bead
  records the psyche's *"we don't have to do that now."* Not pressing.
- **Cross-lane items waiting on the psyche** (other lanes, not mine to ask):
  first real Hetzner spinup (cloud — needs API token + SSH key + size choice);
  disk reclaim / Nix prune-guard rollout (116 GB / 97.9% of active-repo bytes
  in Rust `target/`, fix proven, unlanded); Immich phone-media host choice
  (proposed twice — videographer report 6 + cloud-operator 389).

## 7 — Context-maintenance actions

Done this pass:

- Verified `15df` exists; dropped the synthesis's false "anchoring gap"
  maintenance action and "capture-first" framing.
- Verified the criome admission gate + retired BLS placeholder on `origin/main`.
- Added reconciling notes to the three beads whose status lags reality:
  `primary-9x9f` (M1/M2 landed; re-scope to M3/M4), `primary-xj51` (5-branch
  stack mainlined; only nix-sandbox github-fetch caveat remains),
  `primary-kr40` (real BLS + admission gate landed; description's "placeholder"
  lead is stale; carve the deferred key-custody/ceremony residue out).

Proposed, needs psyche authority (conservative-removal discipline — flagged,
not acted on):

- **Spirit fold/retire candidates:** `w2g3` (envelope "still open") is
  subsumed by `2st7` (High, "settles the envelope left open by `w2g3`") and
  `d6he` — a `w2g3` clarification was already correctly rejected twice. Fold
  candidates: `7let`→`se72`, `2uhh`→`i4ak`, `5myr`→ the schema-namespace
  cluster. These are maintenance, not errors.

Awareness only (other lanes' reports — do not supersede):

- designer 675 cites a stale criome tip (`cd1de18` vs origin `3c05122`);
  674.15 §4/§6 "criome main untouched, operator-carried" is stale (landed via
  operator 408/409). The criome contract-SEMA persistence gap 675 named is
  closing now (`criome` `3c05122`, today).

## 8 — Rest of the workspace (broad reacquisition, for situational awareness)

- **criome is the center of gravity.** The schema-first policy language landed
  on both triad mains (operator 408–410); contract-SEMA persistence is landing
  today. The prime designer just opened **676 — contract-machinery comparison**
  (criome vs Ethereum/Tezos/Solana; thesis: criome is predicate/validator
  family, not stateful-VM) — frame only, unwritten.
- **Cloud on-ramp:** Hetzner Phase 1 built + verified (contracts pushed, daemon
  branch unpushed) — awaiting the live-spinup inputs.
- **Mobile media:** Immich proposed as the phone-upload substrate from two
  lanes against the same Spirit records (`vgon`/`87ts`/`iwbt`).
- **Disk:** 116 GB in Rust `target/`; per-flake prune-guard fix proven in
  sandbox, unlanded.
