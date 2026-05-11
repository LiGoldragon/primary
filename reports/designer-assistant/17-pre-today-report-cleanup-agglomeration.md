# 17 - Pre-today report cleanup agglomeration

*Designer-assistant report. Date: 2026-05-11. Scope: all report
files under `reports/` with filesystem timestamp before
2026-05-11, excluding `.gitkeep`. The user explicitly authorized
cross-role deletion of pre-today reports for this cleanup pass.*

---

## 0 - Outcome

This report is the replacement archive for the pre-2026-05-11 report
set. After this report lands, the old report files listed in section 8
can be deleted. "Keep" in a subagent audit meant "valuable enough to
carry forward"; it does **not** mean keeping the old pre-today file
after this agglomeration.

Four subagents audited the old reports by lane:

- designer reports;
- designer-assistant reports;
- operator and operator-assistant reports;
- system-specialist, system-assistant, poet, and top-level reports.

I then verified contentious items against current files:

- `ESSENCE.md`
- `AGENTS.md`
- `protocols/orchestration.md`
- `protocols/active-repositories.md`
- `skills/kameo.md`
- `skills/actor-systems.md`
- `skills/rust-discipline.md`
- `skills/contract-repo.md`
- `skills/push-not-pull.md`
- `skills/architectural-truth-tests.md`
- `reports/designer/114-124`
- `reports/designer-assistant/15-16`
- current active repo `ARCHITECTURE.md` files where needed.

There were 95 pre-today report files in scope.

## 1 - Current Truth Baseline

Use these current documents instead of old reports:

- `reports/designer/114-persona-vision-as-of-2026-05-11.md` -
  Persona federation overview.
- `reports/designer/115-persona-engine-manager-architecture.md` -
  engine manager, `ConnectionClass`, `EngineRoute`, host-level
  supervision.
- `reports/designer/116-124` - current component development plans and
  synthesis.
- `reports/designer-assistant/15-architecture-implementation-drift-audit.md`
  - current implementation drift audit.
- `reports/designer-assistant/16-new-designer-documents-analysis.md` -
  current critique of the May 11 designer packet.
- `protocols/active-repositories.md` - current repo attention map and
  live truth pins.
- `skills/kameo.md` and `skills/actor-systems.md` - current actor runtime
  and actor discipline.
- `skills/rust-discipline.md` - Rust, daemon, redb/rkyv, and Kameo
  implementation discipline.

Do not use old reports to reopen direct `ractor`, `persona-actor`,
`workspace-actor`, shared `persona-sema`, `signal-persona-store`,
`persona-wezterm`, local `persona-message` ledgers, polling tails, or
tmux/WezTerm-mux-as-runtime-truth.

## 2 - Preserved Durable Points

### 2.1 Actor Runtime And Actor Shape

Current truth: direct Kameo is the Rust actor runtime. Actor nouns carry
data. Kameo's key architectural fact is that `Self` is the actor: the
actor type is the state-bearing noun, not a behavior marker separated
from state.

Preserved from old reports:

- No invented actor wrapper crates. `persona-actor`, `workspace-actor`,
  and similar names were hallucinated abstractions unless a future
  current report explicitly reopens them.
- Public zero-sized actor nouns are against workspace discipline. Kameo
  permits them mechanically, but public actor types should carry data.
- Actorization is not complete merely because a crate depends on Kameo.
  Tests must prove mailbox topology, blocking-plane isolation, restart
  policy, and trace paths.
- Kameo is pre-1.0 and must be pinned deliberately. Kameo 0.20 requires
  Rust 1.88. Known footguns include fallible `tell`, registry globality,
  restart-from-args reconstruction, `spawn_in_thread` needing multi-thread
  Tokio, and link-death semantics.
- Public domain handles around actors are acceptable when they carry
  stable domain semantics, lifecycle, error vocabulary, or capability
  restrictions. Do not expose raw actor machinery as the only library API
  when a domain handle prevents misuse.

Current unresolved actor-related work remains in
`reports/designer-assistant/15` and `reports/designer/124`: adjacent
repos still have direct `ractor`/ZST debt, and some Persona actor traces
still need promotion from witness phases to real actors.

### 2.2 Persona Mind And Native Work Graph

Current truth: `persona-mind` is the central state component for
orchestration and work graph evolution. BEADS and lock files are
transitional compatibility surfaces.

Preserved from old reports:

- The native work graph replaces BEADS by import, not by a live bridge.
  Import old BEADS IDs as aliases once; do not dual-write bd and mind.
- Central work graph operations need typed ready/blocked views, event-log
  substrate, and projections. The event log is the durable truth; views
  are derived.
- Display IDs are user-facing aliases, not durable identity. The old
  proposed algorithm is still usable if needed: BLAKE3 over stable ID,
  Crockford/base32 prefix, extend on collision.
- Caller identity, timestamp, sender, and class enter the envelope/auth
  context, not request payloads.
- Current mind still owes parts named in the May 11 plan: event-log
  completion, `CommitBus`, real subscriptions, `ConnectionClass` audit
  tagging, `ThirdPartySuggestion`, and one-time BEADS import.

### 2.3 Signal, Contracts, Nexus, And NOTA

Current truth: Signal is the typed binary fabric. NOTA is the text syntax.
Nexus is semantic content written in NOTA syntax, not a second parser.

Preserved from old reports:

- Contract repos name relations. A contract's root enum variants are the
  vectors of that relation. Name the relation in plain English before
  naming records.
- Prefer noun-form wire records and context-specific newtypes over
  `String` or generic payload names.
- Avoid generic variants like `Ok`, `Generic`, `Mixed`, or under-specified
  `Body`.
- The twelve verbs remain a useful documentation/order scaffold. LLMs may
  help propose type expansions or query-repair candidates, but they are
  not the query language.
- Delimiters earn their place. Curly braces were dropped. Bind and wildcard
  are typed records, not sigils and not schema-name conventions. There is
  no separate Nexus codec.
- Contract-owned value invariants matter. Do not let request payloads
  supply timestamps, sender IDs, or infrastructure identity.

Unresolved/current:

- `MessageBody(String)` remains a debt in `signal-persona-message` and
  `signal-persona-harness`. Replace it with a typed Nexus payload before
  router/harness durable schemas harden, or at least add the typed form
  additively first.
- Contract repo boundaries need a fresh decision. Older reports assumed
  one relation per contract; May 11 plans sometimes broaden component
  contracts to multiple relations. This is called out in
  `reports/designer-assistant/16`.
- `ConnectionClass` is now needed across multiple domains. The old
  "keep it in `signal-persona` until a second domain needs it" trigger
  has fired. See `reports/designer-assistant/16`.

### 2.4 Sema-db, redb, And rkyv

Current truth: today's `sema` is a typed redb+rkyv database library
pending rename to `sema-db`. It is not the eventual universal `Sema` and
not a shared daemon.

Preserved from old reports:

- No `signal-persona-store` and no shared store actor. Storage is an
  implementation detail of the owning stateful component.
- Each state-bearing component owns its redb file and its table layer:
  mind owns `mind.redb`, router owns `router.redb`, harness owns
  `harness.redb`, terminal owns terminal metadata, etc.
- redb owns ACID table ordering; rkyv owns value encoding.
- A store should have one writer actor per redb file or one explicit
  store kernel that owns all writes. Other actors ask it to write and
  subscribe after commit.
- Emit after durable commit, not inside the transaction.
- Do not use arbitrary rkyv archives as redb keys without a deliberate
  key type. Keep corruption and format/version mismatches loud.
- Header/version/format witnesses are part of durable database design.

Unresolved/current:

- `reports/designer-assistant/16` calls out redb writer ownership gaps in
  the May 11 plans.
- `reports/designer-assistant/15` and `reports/designer/124` preserve the
  remaining signal/signal-core overlap and sema raw-byte slot-store debt.

### 2.5 Router And Delivery Lessons

Current truth: router is the delivery reducer and owns durable router
state. `persona-message` is a stateless NOTA-to-Signal proxy, not a local
ledger.

Preserved from old reports:

- "Write succeeded" is not delivery. PTY writes can succeed without the
  harness actually consuming/responding. Delivery needs durable attempt
  state plus result/observation.
- Commit before effect: router commits acceptance/pending state before
  side effects, and terminal delivery state commits before PTY input.
- After a side effect, failures may be `SentUnconfirmed`, not simply
  rejected or delivered.
- Guard facts must carry generation/freshness. A stale focus/input fact
  must not authorize delivery.
- Unknown actor/recipient should become a typed blockage or typed
  rejection, not an indefinite pending state.
- Scenario data, delivery policy, harness definitions, and prompt/training
  text should become typed records/config, not embedded test prose.

Current unresolved items are in `reports/designer/118`,
`reports/designer/121`, `reports/designer/122`, and
`reports/designer-assistant/16`: preserve `OtherPersona` provenance,
settle input-buffer producer, retire stale `persona-message` delivery
paths, and land stateful router-to-terminal witnesses.

### 2.6 Terminal, PTY, And Desktop Incidents

Current truth: `terminal-cell` is the low-level PTY/transcript primitive;
`persona-terminal` is the Persona-facing supervisor/policy layer.

Preserved from old reports:

- Gas City's model failed because it mixed Dolt-backed hot-loop state,
  polling reconciliation, tmux as runtime truth, and process/session
  fragility. Salvage only the useful nouns: durable work, executor,
  event log, subscription, harness definition, and city/session directory.
- abduco is good prior art for minimal attach/detach and emergency/manual
  containment, but it is not enough for Persona. Persona needs PTY
  ownership, transcript, programmatic input, resize/lifecycle events, and
  typed observations.
- WezTerm mux can preserve sessions only if the mux owns the process; a
  bare GUI terminal is not durable ownership.
- GUI terminals are views over durable PTY owners. The viewer can die
  without killing the child. Transcript truth belongs to the durable owner,
  not the viewer scrollback.
- Terminal programmatic input must not repeat the earlier high-latency
  relay mistake. Human byte pass-through is direct and fast; programmatic
  injection closes a gate only for the short critical section.
- If `persona-terminal` needs cell lifecycle without polling, `terminal-cell`
  likely needs a push-shaped `WorkerObservation` stream rather than
  periodic snapshot asks.

### 2.7 System, Chroma, And Sandbox Discipline

Preserved from old reports:

- Production desktop is not the lab. Tests that can crash or wedge the
  compositor, terminal, browser, Ghostty, or user services need disposable
  sessions or VMs.
- Theme/visual daemons must not enumerate `/dev/pts`, emit OSC into
  terminals, or trigger unbounded global terminal reload fanout.
- `send-text` is child input, not a safe terminal-control delivery
  mechanism. Internal terminal RPCs without render-completion ack are not
  reliable truth.
- Host desktop sockets are never inherited accidentally. A test may ask
  for host-display mode, but then it binds exactly named sockets and keeps
  home/state/runtime/services disposable.
- Sandbox ladder:
  - Tier 0: pure Nix/source witnesses.
  - Tier 1: local desktop-lite sandbox with explicit isolated vs
    host-display modes.
  - Tier 2: Prometheus `systemd-nspawn` or NixOS-container runner for real
    systemd/user-service behavior.
  - Tier 3: full NixOS VM for compositor/terminal/browser crash-risk tests.

Current gap: this sandbox strategy is not yet a canonical skill or current
system architecture doc. Carry it here until system-specialist promotes it.

### 2.8 Clavifaber And Cluster Trust

Preserved from old reports:

- Clavifaber emits typed publication records; it does not write cluster
  database files directly.
- Cluster trust is a separate long-lived owner if/when it exists.
- `signal-clavifaber` was proposed as one contract repo with two channels:
  host publication push and trust distribution.
- Publication push is one-shot request/reply; cluster-trust mints slots or
  commits.
- Trust distribution is a subscription: current state on connect, then
  deltas.
- Remaining ownership questions: cluster-side consumer, real Yggdrasil
  source, and whether trust distribution belongs in a separate repo if the
  relation broadens.

Current Persona docs do not absorb this because it is adjacent
system-specialist work, not the Persona federation.

### 2.9 Poet, Library, And OCR Source Work

Preserved from old poet reports:

- Current library path is `/git/github.com/LiGoldragon/library`, surfaced
  in this workspace through `~/primary/repos/library`.
- Caraka source gaps remain:
  - Sharma/Dash seven-volume Caraka with Cakrapani commentary is the highest
    value acquisition target.
  - Meulenbeld HIML likely needs a non-Anna path.
  - Bhavaprakasha, Sarngadhara, Yoga Ratnakara, and Astanga Sangraha remain
    hard gaps.
  - IA per-page OCR ZIPs are useful but need concatenation.
  - Anna-only files may need membership/API key; large non-Anna mirrors can
    fail through client timeout.
- The 1922 Nirnaya-Sagara Caraka+Cakrapani scan was tested and rejected as
  unrecoverable.
- Plutarch Moralia V remains the next Tier S OCR target; Vidyasagara Caraka
  needs a short trial before budget is committed.
- OCR prompts should allow `[unreadable: reason]` for whole bad regions
  rather than forcing hallucinated text.

Current live files also carry some of this:
`/git/github.com/LiGoldragon/library/ocr-targets.md` and
`/git/github.com/LiGoldragon/caraka-samhita/notes/translation-sources.md`.
Those files currently cite the old poet report; after deletion, this report
is the local archive target for that citation.

### 2.10 Rust Toolchain / Fenix Lockstep

The old `reports/designer/99-shared-rust-toolchain-pin-proposal.md` is not
implemented: `tools/sync-rust-fenix` does not exist as of this pass.
`skills/nix-discipline.md` already mentions fenix lockstep and also points
at the missing script.

Preserved action:

- Either create `~/primary/tools/sync-rust-fenix`, or edit the skill/lore
  references so they do not claim the script exists.
- The intended mechanism is still plausible: choose one canonical Rust flake
  for `fenix`, run `nix flake lock --inputs-from path:<canonical>` in other
  Rust repos, then commit/push each repo.

## 3 - Content Not Carried Forward

These old themes are intentionally retired:

- Direct `ractor` as the current runtime.
- `persona-actor` / `workspace-actor` wrapper crates.
- A shared `persona-sema` or `signal-persona-store`.
- `persona-orchestrate` as a separate work graph daemon.
- Local `persona-message` durable ledger, `actors.nota` writes, polling
  `Tail`, or `persona-wezterm` delivery path.
- A single Persona reducer daemon replacing the May 11 federation.
- Old assistant/operator/designer role-split reports superseded by
  `AGENTS.md` and `protocols/orchestration.md`.
- Old context-reset handoff/status/work-queue reports.
- Old sema design drafts superseded by current `sema`/`sema-db` framing.

## 4 - Still-Unresolved Work Brought Forward

This pass leaves these items explicitly live:

1. `ConnectionClass` home: it is now cross-domain; decide whether it moves
   to `signal-core` or a narrow auth/identity contract.
2. Engine-boundary socket model: central `ConnectionAcceptor` vs
   component-owned sockets with manager-minted auth context.
3. Redb writer ownership: enforce one writer/store actor per redb file.
4. `OtherPersona` provenance: do not erase it by rewriting to `System`;
   carry source class plus effective gate decision.
5. Input-buffer owner: likely `persona-terminal`, not `persona-system`, but
   the May 11 docs need alignment.
6. Contract repo relation boundaries: one relation per repo vs multiple
   named relations in one component contract.
7. Typed Nexus message bodies: replace opaque `MessageBody(String)` before
   durable router/harness schemas harden.
8. `persona-message` identity transition: what replaces `ActorIndex` /
   `actors.nota` while router-owned registry queries are not ready.
9. Harness transcript privacy: raw bytes should likely stay in terminal;
   harness should push typed observations/references unless explicitly
   authorized.
10. Terminal-cell worker observations: decide push stream vs manual
    snapshot; reject polling.
11. System sandbox strategy: promote the sandbox ladder into a system skill
    or architecture document.
12. Rust fenix lockstep: create or correct `tools/sync-rust-fenix`.
13. External reference sweep: several active repo docs still cite old
    reports. They should be redirected to current architecture docs or this
    cleanup report in a separate repo-by-repo pass.

## 5 - Verification Notes

Contentious checks I verified locally:

- The fenix sync helper does not exist: `tools/` contains `orchestrate` and
  `wezterm-palette-rpc-test`, but no `sync-rust-fenix`.
- `skills/nix-discipline.md` already documents `--inputs-from` and mentions
  the missing helper; that skill needs correction or the helper needs to
  land.
- `protocols/active-repositories.md` already states the current actor truth:
  direct Kameo, actor density, and stale `ractor`/`persona-actor`/
  `workspace-actor` language.
- `persona-mind/ARCHITECTURE.md` currently names `StoreKernel` as the store
  boundary and still lists old reports in its reading list; this is part of
  the external reference sweep.
- `library/ocr-targets.md` and `caraka-samhita/notes/translation-sources.md`
  currently cite `reports/poet/84`; this report carries those OCR facts after
  deletion.

## 6 - Reference Replacement Rule

When a live doc cites a deleted pre-today report, use this replacement rule:

- Persona federation/current architecture -> `reports/designer/114-124`.
- Current implementation drift -> `reports/designer-assistant/15`.
- Critique/questions on the May 11 designer packet ->
  `reports/designer-assistant/16`.
- Retired pre-today report substance -> this report.
- Kameo usage -> `skills/kameo.md` and `skills/actor-systems.md`.
- redb/rkyv/sema-db usage -> `skills/rust-discipline.md` and current
  component `ARCHITECTURE.md`.
- report hygiene and naming -> `skills/reporting.md`.

## 7 - Subagent Audit Summary

The subagent classifications were consistent:

- Most old reports are superseded status, handoff, work-queue, or earlier
  architecture drafts.
- The useful old content falls into a few themes: Kameo caveats, contract
  relation naming, native work graph, redb/rkyv shape, terminal/PTY incident
  lessons, system sandboxing, Clavifaber cluster-trust relation, and poet OCR
  source trails.
- "Keep" recommendations from subagents were treated as "preserve content
  here"; pre-today standalone report files are still deleted under the user's
  instruction.

## 8 - Deleted Report Manifest

The deletion scope is every pre-2026-05-11 report file below:

```text
reports/1-gas-city-fiasco.md
reports/designer-assistant/1-role-split-bootstrap.md
reports/designer-assistant/10-abduco-terminal-survivability-research.md
reports/designer-assistant/11-durable-pty-session-tools-research.md
reports/designer-assistant/3-ractor-only-actor-architecture-recheck.md
reports/designer-assistant/4-kameo-ractor-no-zst-switch-assessment.md
reports/designer-assistant/5-kameo-testing-assistant-findings.md
reports/designer-assistant/6-public-handle-case-for-kameo.md
reports/designer-assistant/7-contract-relation-naming-survey.md
reports/designer-assistant/8-designer-recent-work-and-kameo-testing-audit.md
reports/designer-assistant/9-persona-mind-implementation-pins-prepass.md
reports/designer/100-persona-mind-architecture-proposal.md
reports/designer/106-actor-discipline-status-and-questions.md
reports/designer/107-contract-enum-naming-pass-mind.md
reports/designer/108-review-of-operator-assistant-101.md
reports/designer/109-answers-to-operator-assistant-102.md
reports/designer/111-signal-clavifaber-contract-shape.md
reports/designer/12-no-polling-delivery-design.md
reports/designer/19-persona-parallel-development.md
reports/designer/26-twelve-verbs-as-zodiac.md
reports/designer/31-curly-brackets-drop-permanently.md
reports/designer/4-persona-messaging-design.md
reports/designer/40-twelve-verbs-in-persona.md
reports/designer/45-nexus-needs-no-grammar-of-its-own.md
reports/designer/46-bind-and-wildcard-as-typed-records.md
reports/designer/57-cross-repo-cargo-path-audit.md
reports/designer/63-sema-as-workspace-database-library.md
reports/designer/64-sema-architecture.md
reports/designer/66-skeptical-audit-of-sema-work.md
reports/designer/68-architecture-amalgamation-and-review-plan.md
reports/designer/70-code-stack-amalgamation-and-messaging-vision.md
reports/designer/72-harmonized-implementation-plan.md
reports/designer/73-signal-derive-research.md
reports/designer/76-signal-channel-macro-implementation-and-parallel-plan.md
reports/designer/78-convergence-with-operator-77.md
reports/designer/79-architecture-files-audit.md
reports/designer/80-open-questions-inventory.md
reports/designer/81-three-agent-orchestration-with-assistant-role.md
reports/designer/86-handoff-from-context-reset-2026-05-08.md
reports/designer/91-workspace-snapshot-skills-and-architecture-2026-05-09.md
reports/designer/92-sema-as-database-library-architecture-revamp.md
reports/designer/93-persona-orchestrate-rust-rewrite-and-activity-log.md
reports/designer/97-persona-system-vision-and-architecture-development.md
reports/designer/98-critique-of-operator-95-orchestrate-cli-protocol-fit.md
reports/designer/99-shared-rust-toolchain-pin-proposal.md
reports/operator-assistant/101-operator-assistant-next-work-candidates.md
reports/operator-assistant/102-situation-after-mindroot-surface.md
reports/operator-assistant/103-reorientation-after-router-witness.md
reports/operator-assistant/82-three-agent-orchestration-feedback.md
reports/operator-assistant/85-signal-persona-system-integration-audit.md
reports/operator-assistant/88-recent-code-signal-sema-audit.md
reports/operator-assistant/90-rkyv-redb-design-research.md
reports/operator-assistant/93-operator-work-and-sema-impact-review.md
reports/operator-assistant/95-operator-work-review-after-designer-93.md
reports/operator-assistant/96-high-signal-fixes-after-operator-review.md
reports/operator-assistant/97-persona-mind-actor-density-compliance-review.md
reports/operator-assistant/98-kameo-persona-mind-code-shape.md
reports/operator-assistant/99-kameo-adoption-and-code-quality-audit.md
reports/operator/100-persona-mind-central-rename-plan.md
reports/operator/101-persona-mind-full-architecture-proposal.md
reports/operator/103-actor-abstraction-drift-correction.md
reports/operator/104-kameo-migration-prognosis.md
reports/operator/105-command-line-mind-architecture-survey.md
reports/operator/106-persona-mind-constraints-and-witness-pass.md
reports/operator/107-persona-mind-world-rescan.md
reports/operator/52-naive-persona-messaging-implementation.md
reports/operator/54-niri-focus-source-vision.md
reports/operator/61-router-trained-relay-test-implementation.md
reports/operator/67-signal-actor-messaging-gap-audit.md
reports/operator/69-architectural-truth-tests.md
reports/operator/71-parallel-signal-contract-architecture-plan.md
reports/operator/74-signal-sema-persona-forward-implementation.md
reports/operator/77-first-stack-channel-boundary-audit.md
reports/operator/83-operator-feedback-on-assistant-orchestration.md
reports/operator/87-architecture-truth-pass.md
reports/operator/95-orchestrate-cli-protocol-fit.md
reports/operator/97-native-issue-notes-tracker-research.md
reports/operator/99-designer-98-integration.md
reports/poet/62-ayurvedic-source-audit.md
reports/poet/64-ayurvedic-source-acquisition-pass.md
reports/poet/65-bibliography-move-to-ghq.md
reports/poet/84-vision-ocr-trial-and-scan-quality-audit.md
reports/system-assistant/1-bootstrap-and-clavifaber-research.md
reports/system-specialist/100-wezterm-live-palette-research.md
reports/system-specialist/101-chroma-wezterm-crash-suspects.md
reports/system-specialist/102-wezterm-mux-survivability.md
reports/system-specialist/103-abduco-agent-session-survivability.md
reports/system-specialist/104-chroma-ghostty-kameo-state.md
reports/system-specialist/105-system-component-sandbox-strategy.md
reports/system-specialist/81-do-it-all-tier2-cascade.md
reports/system-specialist/94-criomos-platform-discipline-audit.md
reports/system-specialist/96-system-specialist-agglomerated-archive.md
reports/system-specialist/97-clavifaber-repo-preparation.md
reports/system-specialist/98-clavifaber-typed-publication.md
reports/system-specialist/99-chroma-wezterm-freeze-incident.md
```

Today's reports and `.gitkeep` files are intentionally outside this
deletion scope.
