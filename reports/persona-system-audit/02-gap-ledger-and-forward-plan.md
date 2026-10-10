# System Audit — Gap Ledger & Forward Plan (2026-07-01)

## State of the Whole

The pieces are real and mostly individually working, but they have never run together as one system outside tests. Three walls:

(1) They don't currently build as one coherent set (version-pin fragmentation across schema-rust-next/signal-frame + an unlanded criome-authorization-push fork → incompatible duplicate wire types → silent rkyv decode failures).

(2) The control-plane loop doesn't close (data plane message→router→harness/terminal→PTY/Pi is real on an authorized channel, but "mind decides, router enforces" is a typed no-op: mind answers AdjudicationRequest/ChannelList with NotInPrototypeScope, router has no client to mind + only an in-memory pull-only outbox; channels granted only manually via router meta socket).

(3) Most of the federation isn't packaged to deploy (CriomOS ships modules for only router/mirror/repository-ledger/criome/lojix; persona/mind/mentci/nexus/listener/orchestrate/spirit/sema have none; no composite federation role) and persona-as-supervisor is scaffold (one hardcoded "default" engine, Launch/Retire/Tap reject, no-op unit controller, FD handoff only in tests, supervises a fixture not real daemons). Deployed today = that 5-daemon systemd perimeter; mirror.service is crash-looping on ouranos (this host); ouranos is itself pre-cutover; only prometheus is a recorded lojix deploy.

## Ranked Gap Ledger

### Tier 1 — Blocks the Whole Cohering/Deploying

- **G1 Build incoherence**: version-pin fragmentation + unlanded criome-authorization-push fork. The gate for everything.
- **G2 Federation unpackaged**: no NixOS modules for the 8 core daemons; no composite federation node role.
- **G3 Channel-adjudication loop non-functional**: mind AdjudicationRequest/ChannelList = NotInPrototypeScope; no router→mind push.
- **G4 persona supervisor is scaffold**: single default engine; Launch/Retire/Tap reject; no-op controller; FD handoff test-only; no real-daemon e2e integration test.

### Tier 2 — Significant Unfinished / Operational

- **G5** No shared daemon-test harness; integration coverage is single-component-against-fakes; the one 4-process e2e skips by default + is in no flake check.
- **G6** lojix cutover incomplete: v0.4.0 landed but v0.3.10 runs; only prometheus Current; no gcroots tree; live Switch unproven on metal; torn-write reconciliation gap.
- **G7** mirror.service crash-looping on ouranos (live).
- **G8** system skeleton (only QueryStatus; niri backend unwired; health hardcoded); upgrade largely scaffold (only AttemptUpgrade real).

### Tier 3 — Narrower / Honestly-Flagged In-Repo

- **G9** Pervasive meta/config sockets unimplemented (message, harness, introspect, system, mind, listener, upgrade).
- **G10** No Claude/Codex live login in harness (Pi only; Claude observe-only); agent real provider default-off + streaming unimplemented.
- **G11** Foundation coupled gap: nota-next #[shape] derive → schema-next trait/impl emission leg not integrated.
- **G12** schema-rust-next .expect parse-panics; criome composite Composition escalates instead of evaluating; criome push side absent.
- **G13** mentci is a generic approval UI, not yet the Persona chat/delivery interface it's intended to be.

## Surprises That Overturn Assumptions

- schema-rust-next migration is essentially DONE (RustWriter string emitter gone; residual is polish + the -next rename) — contradicts the psyche's suspicion.
- criome UNDER-claims (BLS signing done while docs call it a next milestone).
- spirit's old "schema-upgrade unimplemented" limit is RESOLVED (real 8→9→10 migrations).
- The unfinished surface is TYPED (NotBuiltYet), so it compiles + greps clean — visible only by reading dispatch code.

## Forward Plan

Two tracks over one shared gate:

**Stage 0 (shared gate, first)**: land criome-authorization-push to main, unify schema-rust-next/signal-frame/contract pins to one coherent set, establish a real per-repo + composite build/test-green baseline. (Note: individual repos build green — lojix/horizon-rs/cloud confirmed BUILD_OK; CriomOS intentionally throws standalone without a lojix system-input override; forge has no build outputs. The COMPOSITE build under fragmented pins is the unverified risk.)

**Track A (cohere + testable)**:
1. Extract a shared daemon-test-harness crate.
2. First real two-daemon flake check message→router.
3. DECISION: close the control-plane loop (wire router→mind + implement mind adjudication) or formally adopt manual-grant bootstrap and document it.
4. Hermetic N-daemon federation smoke (real binaries, no VM) driving the proven data-plane chain — doubles as the real-daemon integration proof persona lacks.

**Track B (deploy together)**:
1. Immediate: refresh operator daemon to lojix 0.4.0 + fix the mirror crash-loop.
2. Package the 8 missing core daemons as NixOS modules (follow criome.nix/persona-router.nix pattern) — largest/highest-value.
3. Compose a PersonaFederation horizon node-role.
4. Prove in a CriomOS-test-cluster VM → low-blast edge node (zeus) live Switch → full cutover.

**Strategic point**: Stage 0 gates both tracks; Track A's hermetic federation smoke should precede Track B's federation packaging — deploying an incoherent, never-integrated set is premature.

## Open Decisions for the Psyche

1. Start with Stage 0 (recommended), the live fixes (lojix 0.4.0 + mirror), or the control-plane design call?
2. Whether to record the two candidate intents.
3. Archive the abandoned lore repo.
4. Drop the -next suffix and finish the schema-rust-next residual.
