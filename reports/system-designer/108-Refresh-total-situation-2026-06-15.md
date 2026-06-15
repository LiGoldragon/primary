# 108 — Refresh: total situation (system-designer lane), 2026-06-15

*A context-maintenance Refresh + light engine-analysis over everything this lane
designed/touched. It is the agglomeration landing witness: 20 superseded reports
retire on its landing (their substance verified into permanent docs / shipped
code / the live audit). Live state verified this session.*

## Executive summary

Five topic arcs converged on one point: the deployment of a versioned,
schema-relocated spirit.

1. **SEMA version-control (91–102)** — designed → vision → 3-phase implementation
   → audited → shipped across 9 repos. spirit **0.12.1** (v9 versioned store) is
   **deployed live**; the hardening tower + structural-forms relocation sits in the
   matched candidate branch family `structural-forms-integration` (spirit 0.13.0-to-be,
   sema-engine 0.6.2, layout 5), deploy-gated on the system-operator.
2. **Early-June spirit concept arc (51–89)** — privacy-as-`Magnitude` (Spirit
   1463), variant ladder, lifecycle ladder, hash-identity, guardian gates; decisions
   ratified to Spirit/INTENT; implementations largely pending in beads.
3. **Domain taxonomy (104–106)** — psyche-approved coarsening (**42 of 211 leaves
   kept**), bead `primary-fwe3`, principle **`qr5o` recorded to Spirit this session**;
   deploy-sequenced strictly after SEMA-VC.
4. **Structural-forms (103)** — the schema-macro-as-data epiphany; ownership moved
   to the prime-designer lane (`reports/designer/626–642`).
5. **Deploy/infra (59–90, 107)** — workspace reset (85), component-port program
   (74–77), terminal-plane (78–79), VM-testing (69–70); report 107 the live
   deploy-readiness verdict.

**Single load-bearing blocker:** the system-operator's staging-copy migration proof
for the layout 4→5 self-heal (`rebuild_from_log`, `primary-lmf3`). No design work
remains on the deploy itself.

**Two corrections to the survey's machine view:** `qr5o` **is** recorded (not
pending); and the deployed daemon restarted **08:37 today and self-resumed** from
persisted SEMA state (store intact, 1248 records) — evidence the resume path works.

## The arcs, by topic

### SEMA-VC / versioned-state (91–102)
Reusable `sema-engine` versioned, replayable, mirror-shippable store. Spine:
intent (Spirit 29pb/j487) → reconciliation (94) → grand design (95/96) → vision
(98) → handoff (97) → phases 1–3 (99–101) → audit (102). **Landed:** spirit 0.12.1
v9 store + logged-fold migration deployed; versioned CommitLog, record families,
mirror outbox API, layout self-heal all in `sema-engine`; intent-subscription pilot
(ubgg) live. Permanent home: `sema-engine`/`spirit` `ARCHITECTURE.md` + `INTENT.md`
+ Spirit records + bead pipeline. **Open:** the candidate family not yet deployed;
federation/privacy ambition (95/96) deferred on two psyche questions. **Canonical:**
102 (7-chapter audit), 107 (deploy verdict).

### Early-June spirit concept (51–89)
Production-parity assessment + refinement concepts. **Landed:** privacy =
`Magnitude` (Spirit 1463); variant/lifecycle ladders ratified (1472–1474, P1–P4);
nine skill migrations (report 52 → five skill files); record redesign v5→v6 in
deployed 0.12.1 (report 72). **Open:** privacy field in source not yet redeployed;
variant-ladder tier-1; `CollectRemovalCandidates` in source but not served by the
deployed binary; archive system; hash-identity refactor; guardian deletion/referent
gates await psyche confirmation (89 §6). Beads: `am9d`/`dn1e`/`uwo0`/`36iq`/`tiyo`.

### Domain taxonomy (104–106)
Naming audit (104) → coarsening curation cutting ~80% of leaves, 42 of 211 kept
(105) → operator hand-off (106). **Landed:** psyche-approved spec; bead
`primary-fwe3` (subsumes `gm78`); principle **`qr5o` recorded**. **Open:**
implementation deploy-gated strictly after SEMA-VC (the two store migrations must
not interleave); 106 deploy bar gated on the system-operator staging-copy proof.

### Structural-forms (103)
The epiphany that structural macros should be schema-driven data, not hand-parsed.
**Ownership moved** to the prime-designer lane — `reports/designer/626–642` (626
north-star, 635/641 slice menu, 642 positional-struct migration with separator
`key.TypeReference`). Nothing system-designer-owned remains; 103 kept only as this
lane's origin record.

### Deploy / infra / cross-cutting (59–90, 107)
Component-port program (triad-runtime spine, six SAFE-NOW ports 74–77),
terminal-plane decomposition (78–79), VM-testing/cluster-data (69–70), the full
workspace reset (85), the live deploy audit (107). **Open:** psyche concept
decisions in 59/73–76/78–79 (see below). Migration debt (orchestrate→triad_main,
sema→sema-engine consumers) is scheduled operator work.

## Light engine-analysis — the spirit intent engine

Daemon-centric triad; every claim status-marked (hooked / stubbed / contract-only /
conceptual / stale).

### Boundary map
- **spirit-daemon** (0.12.1 deployed, 0.13.0 candidate) — Signal/Nexus/SEMA runtime;
  owner `li`; `spirit.sock` (0o755), `meta-spirit.sock` (0o600).
- **sema-engine** (lib 0.4.0 deployed → 0.6.2 candidate, `STORAGE_LAYOUT` 5) — typed
  redb; owns CommitLog, VersionedCommitLog, record families, mirror outbox, layout
  self-heal. No binary, no tokio.
- **signal-spirit / meta-signal-spirit** — wire-contract crates. In the candidate,
  spirit **deletes** its in-repo `signal.rs` (5456 lines) + `meta_signal.rs` (773)
  and consumes these crates (intent u7tj) — newest, least-separately-reviewed.
- **mirror-daemon** (0.1.0, IDLE) — owner `mirror`; `working.sock` (0o660),
  `meta.sock` (0o600), **TCP 0.0.0.0:7474 unauthenticated**; binary rkyv config.

### Channel ledger
| Channel | Producer→Consumer | Contract | Transport | Status |
|---|---|---|---|---|
| Working signal | CLI/agent → spirit | signal-spirit | spirit.sock | HOOKED |
| Meta signal | meta-CLI → spirit | meta-signal-spirit | meta-spirit.sock | HOOKED |
| SEMA write | Nexus → sema-engine | (private) | in-process | HOOKED (chain-head advances) |
| SEMA read | Nexus → sema-engine | (private) | in-process | HOOKED |
| Intent subscription | Nexus → subscribers | signal-spirit | streaming Event | HOOKED (ubgg pilot) |
| Guardian journal | Nexus → journal | hand-written | in-process + sema table | HOOKED (v3 written) |
| Mirror ingress TCP | shipper(absent) → mirror | signal-mirror | TCP 0.0.0.0:7474 | STUBBED — unauthenticated |
| Mirror working Unix | shipper(absent) → mirror | signal-mirror | working.sock | CONTRACT-ONLY |
| Mirror outbox loop | sema-engine → shipper | versioned log | in-process + cursor | **CONCEPTUAL — load-bearing gap** |

### Per-component state
- **spirit-daemon** — actors: Nexus (mail keeper / effect executor / referent
  guardian), Signal admission (stateless), Store (sema-engine wrapper). Durable:
  StoredRecord (base36 ids), StoredReferent, Migration, GuardianDecision
  (feature-gated). Refuses socket plumbing, budget, trace mechanics, pre-v9 From-chain.
- **sema-engine** — no actors. Tables: CommitLog, VersionedCommitLog (family
  identity + entry/prior digest + CommitSequence), domain families, MirrorOutbox
  (persisted cursor). Layout-5 open refolds derived slots via `CanonicalView::fold`
  with full digest re-verification; never writes on rejected open. Refuses
  tokio/kameo, migration From logic, retention, transport.
- **mirror-daemon** — actor Service (owns Engine+Store). Tables StoredHead,
  ReceivedEntry (append-only), StoredCheckpoint, RetentionSetting (placeholder).
  Idempotent Append + crash-window dedup. Refuses retention enforcement, BLS,
  engine-owner topology.

### Trust boundaries
spirit's trust boundary is the **Unix socket ACL** (meta 0o600 owner-only); no
cryptographic sender verification; origin minted by daemon admission; config is
binary rkyv (daemon never parses NOTA). **mirror's TCP 0.0.0.0:7474 is
unauthenticated** — any tailnet peer can Append; `PeerIdentity::Tcp` carries IP
only; no BLS (deferred). This is the ingress hole `primary-x3l7` must close before
the shipper goes live (Spirit rj9y: "the bind address is the deployment's trust
boundary"). No TLS/signing/tokens anywhere.

### Drift — the one load-bearing gap
Everything in the versioned-store path is **HOOKED** (versioned log, outbox API,
layout self-heal, chain-head, v9 store, guardian v3, 1248 production records). The
**mirror durability loop** (spirit Nexus → outbox → mirror Append) is **CONCEPTUAL**
— the outbox API is ready, the ComponentShipper library exists, but spirit zero-wires
it (the candidate deleted `shipper.rs`), and the ingress is unauthenticated. Remote
durability (intent 29pb) is therefore **test-only**. Closing it is gated:
`x3l7` (auth) → `85hv` (production shipper) → enable.

## Live situation (verified 2026-06-15)

**Deployed now:** spirit-daemon 0.12.1 (flake.lock rev f4635c3c), restarted 08:37
today, self-resumed; pins sema-engine 0.4.0. Live store `spirit.sema` (4.0 MB,
schema v9, 1248 records); guardian journal at v3; pre-0.12-recovery backup present.
mirror-daemon idle on 0.0.0.0:7474 unauthenticated. Remote durability test-only.

**Pending (candidate, not deployed):** `structural-forms-integration` matched family
(spirit + sema-engine 0.6.2 layout 5 + signal-spirit + meta-signal-spirit) = VC
hardening tower + store god-impl decomposition (`x178`) + structural-forms wire
relocation, mirror shipper removed. Branch version reads 0.12.1; **must bump to
0.13.0** at deploy.

**The two-migration sequencing (critical — reports 106+107):**
1. **FIRST** `structural-forms-integration` (`qu28`): engine layout 4→5 self-heal
   via `rebuild_from_log` (`lmf3`). System-operator gates below.
2. **THEN** domain coarsening (`fwe3`, report 106): record domain-vector rewrite,
   rebased onto the deployed post-0.13.0 `signal-spirit`.
The two store migrations (layout self-heal + domain rewrite) **must not interleave**
— sequence them, or bundle both `From`-chain steps in one staged pass; never two
uncoordinated migrations against the live intent store.

## Open decisions

**System-operator (deploy gates, report 107):** (1) staging-copy migration proof —
the `rebuild_from_log` path is taken (not the no-log fallback), 1248 records + all
referents survive, `Observe`/`Count` correct, daemon restarts and self-resumes;
(2) run the ignored Nix/deploy integration tests; (3) bump to 0.13.0 + update
`skills/spirit-cli.md`; (4) confirm the relocated wire contract is shape-unchanged
(the newest change, `d2cf86fd`).

**Psyche (strategic):** (a) promote `structural-forms-integration` to deploy
candidate vs keep as clean substrate (operator Q1); (b) coarsening strictly-after
vs bundled-one-pass — hard constraint: migrations must not interleave; (c) when
`x3l7` (mirror auth) lands — it gates the shipper (`85hv`) and remote durability (29pb).

**Psyche (concept decisions blocking downstream work):** (4) `CollectRemovalCandidates`
Option A/B + privacy direction (59 D1/D6 — five core spirit designs blocked); (5)
message/router existence-log A vs 2-plane B (75/76 #2); (6) terminal session-control
owner (78/79 — terminal-cell ownership settled to orchestrate, Spirit bcca);
(7) record SHAPE flat vs per-kind variant (73 clar. A — gates 72 on new spirit);
(8) guardian gates: deletion/referent semantics, one guardian or two, referent-name
privacy (89 §6).

**Resolved this arc:** `im1l` (v7 referent fold) FIXED in candidate `c3a21070`,
non-blocking (live store is v9, path never runs); `gm78` (scope All buckets)
SUBSUMED by `fwe3`; `qr5o` recorded.

**Housekeeping still unlanded:** the SEMA-VC federation/privacy design visuals
(95/96) and the VC-seam / versioning-policy / fold-law notes (102 D1/D3) are still
report artifacts — migrate to `sema-engine`/`spirit` `ARCHITECTURE.md` on an
operator branch when next touched.

## Maintenance ledger — what retired, what's kept

This Refresh agglomerates the arc. **20 reports retired** on its landing (each with
a named, verified landing); the rest are kept as load-bearing working artifacts or
canonical references.

**Retired (Drop) — landing verified:**
- SEMA-VC implementation arc → `sema-engine`/`spirit` `ARCHITECTURE.md` + report 102
  + shipped code: **91, 92, 93, 97, 98, 99, 100, 101**.
- **104** → subsumed by 105 (coarsening evaporates 104's renames).
- **51** → 52 + skills; **53** → 56/61; **88** → Spirit oj3i + 89.
- **52** → five skill files (skill migration proof complete); **54** → Spirit 1463
  (privacy=`Magnitude`); research preserved in git.
- **66** → operator scope (chroma sandbox landed); **67/68** → 69/70 (VM-testing
  landed); **71** → 73 + 85 (stack-rewrite thread); **86** → 85; **90** → 85.

**Kept — canonical / live:** 102 (SEMA-VC audit), 105/106 (domain coarsening, live
`fwe3`), 107 (deploy audit), 85 (reset log), 87 (triad recipe), 74–79 (port program
+ terminal), 73/77 (schema-in-rust recipe), 63/65/69/70, 59 (blocked on psyche).

**Kept — pending psyche/design:** 95/96 (federation/privacy ambition), 55 (variant
ladder), 57/64 (engine variant, hash-identity), 89 (guardian gates), 103 (epiphany
origin record), 94 (VC forward-design lens), 56/58/60/61/62 (spirit concept psyche
reports — retire as their downstream beads land).
