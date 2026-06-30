# Spirit Archive Rehoming — Phase 2 Small-Batch Append Handoff

Per-repo integration of archived Spirit intent records into sub-repo
`ARCHITECTURE.md` files, each committed and pushed independently.

## Task and scope

Integrate (not raw-dump) the archived Spirit records routed to each of 14
sub-repos under `/git/github.com/LiGoldragon/<name>`, synthesizing each into the
existing `ARCHITECTURE.md`, deduping against what is already captured, and
pushing each repo independently via its own jj. Pre-flight gate per repo:
`@` on `main`, `main` not behind origin, fast-forward push only.

## Inputs consulted

- Routing manifest: `/home/li/primary/agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`
- Dump: `/tmp/spirit-archive-extract/archived-spirit-records.dump.md` (505 records, local-only)

## Secret handling

The three `[SECRET]`-flagged ids (`go41`, `wn7q`, `2qhw`) route to CriomOS-home,
CriomOS, and lojix-cli respectively — none routed to any repo in this batch. No
redactions were required and no secret value was written.

## Result summary

13 of 14 repos integrated, committed, and pushed (fast-forward, origin-synced).
`skills` SKIPPED — divergent working copy (session's own churning lane).

| repo | records | commit (change / commit_id) | push |
| --- | --- | --- | --- |
| mentci-lib | 5 | `spryyoxz` / 1a7965fc | fast-forward, synced |
| mentci-egui | 4 | `mmqtwklu` / 8f9de29f | fast-forward, synced |
| nexus | 4 | `unotlyow` / b8935770 | fast-forward, synced |
| orchestrate | 4 | `woluookz` / b0841ca3 | fast-forward, synced |
| signal-agent | 4 | `ouxvllzy` / 1e507476 | fast-forward, synced |
| harness | 3 | `wmkowqzt` / f07c4dfe | fast-forward, synced |
| mind | 3 | `qzuzvpmw` / a10983d9 | fast-forward, synced |
| message | 2 | `luozwtvk` / d7dfb005 | fast-forward, synced |
| terminal-cell | 2 | `tlszsttt` / e87dd66b | fast-forward, synced |
| arca | 1 | `lsnmtnny` / cd072cd7 | fast-forward, synced |
| forge | 1 | `llnrvmnk` / bdfc0eee | fast-forward, synced |
| router | 1 | `rslnpvkq` / 14f85574 | fast-forward, synced |
| terminal | 1 | `przqmwmn` / 985dc926 | fast-forward, synced |
| skills | 1 | — | **SKIPPED** (divergent) |

Commit message on every pushed repo: `rehome: integrate archived intent records
into ARCHITECTURE` + `Co-Authored-By: Claude Opus 4.8 (1M context)`.

## Per-repo integration detail

### mentci-lib (7x5z, 80bl, jwm9, mu0o, xk7f)

Section touched: new **Mentci stack direction** section. `7x5z`
(universal-component-general UI) already realized throughout the doc and cited
as already-captured. Wove in `jwm9` (async engine layer, own actor system,
room for Nexus/SEMA, Android-portable), `80bl` (observation surface querying
introspect's schema-defined trace events, filter by component/message/signal
shape), `mu0o` (sandbox-to-deployed observation/debugging/approval/integration
console), `xk7f` (prompt-to-bead-weave routing via preflight model →
skills.nota → terminal-cell-driven harness session; orchestrate lanes own
naming/addressing).

### mentci-egui (cok7, nc9k, xen8, xlrk)

All four were already fully realized in existing sections. Added an **Archived
intent provenance** list mapping each id to its existing section (cok7→
Boundaries SystemThemeFollower; nc9k→Boundaries+Runtime Flow; xen8→Runtime Flow
component/authority labels; xlrk→Role/Boundaries/Runtime Flow), for
traceability rather than re-stating.

### nexus (fcsg, fuls, vdiu, z6qu)

ROUTING TENSION (see Blockers). This repo's `ARCHITECTURE.md` is the NOTA↔Signal
**text translator** daemon; the four records describe the **Nexus engine/
decision-effect plane** in the Signal/Nexus/SEMA triad — a related-but-distinct
meaning of "Nexus." Added a scoped **Nexus the plane vs. nexus the translator**
section distinguishing the two, capturing `fcsg` (NexusDecision/NexusEffect
language + generated runner loop), `fuls` (recursive inner runtime engine for
actor prioritization/backpressure/scheduling), `vdiu` (slim acknowledgement
output, follow-up queries), `z6qu` (internal-feature catalog for visibility,
typed-in→typed-out plane, recursive computation destination). Did not rewrite
the translator's identity.

### orchestrate (5d5o, irmw, potn, udgu)

Section touched: **Direction**. `udgu` (one-arg NOTA CLIs as complete surface,
tools/orchestrate retired) already thoroughly captured in Status/TL;DR/§8 —
noted as already-captured. Wove in `5d5o` (kept on current triad/signal/sema/
runtime crate set; dependency-surface update, not lockfile work), `potn`
(dynamic topic-named lanes as target; lane = work-session identity; discipline
as metadata; fixed role-lanes a compatibility shim), `irmw` (role = NOTA vector
of identifier tokens; last token = base discipline; preceding = specializations;
filesystem form hyphen-joined lowercase; ordinal prefixes disambiguate).

### signal-agent (7yth, f8k7, gdbf, l0w8)

Section touched: new **Component direction (archived intent)**. `f8k7`
(generic OpenAI-compatible provider API) largely already cited/captured; added
the build-time-opt-in/capability-observation detail. `7yth` (persona-llm-client
→ workspace-native `agent` triad incl. owner-signal-agent; supervised; hooks to
mind; typed NOTA via validate-and-retry, grammar-constrained when self-hosted).
`l0w8` (default + ordered fallback provider chain; daemon as reducer+checker
with Criome-escalating authorization). `gdbf`: its "abstraction over harness
backends" framing is SUPERSEDED by this repo's own Scope section (harness
backends deferred/discarded); preserved only its still-true core (HTTP-API-call
component, Router talks to agent) and explicitly noted the supersession.

### harness (eo25, hqg7, s8lq)

Sections touched: **§2 State and Ownership** (wove `hqg7`: production shape is
one daemon owning multiple harness instances as internal records/actors/
adapters, not one OS daemon per harness) and new **§3.1 Reliability and
browser-automation notes** (`eo25`: Pi compaction-abort is a recurring
reliability problem, treat stop-after-compaction as harness bug candidate;
`s8lq`: browser automation should attach to a visible tab so the human can
watch/intervene and keep login/2FA secrets out of prompts/logs).

### mind (wgii, wl2a, x92t)

Section touched: new **§6.4 Future direction** (none of the three were present;
all are post-persona-mind capabilities). `wgii` (agent errors logged into Mind
as typed events → skill-improvement loops + auditor input), `wl2a` (agent memory
defaults to shared system; Claude-specific memory an explicit gated path),
`x92t` (role-vector-driven skill loading; each token contributes to the boot
skill bundle persona-mind sends; composes with skills-bundle-into-roles intent;
noted role-vector encoding itself is owned by orchestrate's lane registry).

### message (alom, q73w)

Section touched: new **§3.1 Existence vs delivery, and the message-sent hook**.
`alom` (message owns the EXISTENCE fact at SO_PEERCRED ingress as the event it
emits; router authoritative for delivery; uid-addressed direct-delivery fast
path bypassing router) — wove carefully given the doc's "stateless / no durable
ledger" framing, scoping existence to the boundary fact not a local log. `q73w`
(hookable typed MessageSent action firing at the message-sent boundary for
hooks/UI/observers/routers/subscribers).

### terminal-cell (of73, ux9i)

Section touched: **§1.1** area. `of73` largely already captured (abduco
primitive, process-per-app, append-only transcript); added the non-triad-shape-
is-incidental point and the still-open question of which component owns the
terminal control/session surface. `ux9i` (three-way lifecycle split: orchestrate
owns instance lifecycle policy/ordering, systemd owns OS supervision/restart-
survival, terminal-control owns durable Sema instance record + restart
rediscovery/reattach) — noted consistency with "no Sema database here" (record
lives in terminal-control).

### arca (i1b5)

`i1b5` is the archived form of an intent ALREADY fully captured in the existing
**Cascade migration discipline** section (cites Spirit 319 / 2026-05-23). Added
the archived id `i1b5` as a co-citation reference; no substance re-stated.

### forge (gopu)

Section touched: status header. Wove `gopu` (forge is the build-system family /
eventual Nix replacement; forge-core shared contract; forge-nix-builder wraps
Nix as a library under the forge daemon; keep eternal Nix concepts, move auth to
Criome + binary signing to content-addressed store; generated Rust may become
content-addressed crates; Nix phases out as forge matures).

### router (57f9)

Section touched: **§2.9 Networked router-to-router forwarding**. Much of `57f9`
already captured via the existing spirit→criome→router→mirror milestone (Spirit
`wckt`/`d6he`). Added the standardized-routing-protocol specifics not yet
explicit: payload-blind router-typed envelope as sole subscription matcher for
non-direct passing; reference-shaped object-update fan-out (criome emits
authorized-object reference, subscribers fetch rkyv object); quorum-backed-by-
default accepted objects; after-time pulse scheduling re-acceptance; one mirror
per node; mirror as psyche's cross-machine self; mirror may fold into Spirit.

### terminal (f8tb)

Section touched: intro (after the mux-helpers note). Wove `f8tb` (canonical name
**terminal-control** with contracts signal-terminal-control / meta-signal-
terminal-control; owns name-to-socket registry, signal control-plane relay,
per-session prompt-pattern registry, session-observation Sema; folds into
neither harness nor orchestrate; terminal-cell stays abduco primitive and
absorbs the input-gate writer + prompt-matcher).

## Skipped repo

### skills (dfl5) — SKIPPED, divergent

After `jj git fetch`, `main` and `main@origin` both point to `ouzxxuzt`
(247f54f2, "skills: add read-only Spirit query composition"), but the local
working copy `@` (`yrlmxryy` / 5bc61b35, empty) sits on the OLD line (parent
`sotwrsol`) and is NOT a descendant of current `main` — the two are separate
heads with no shared tip. Committing on `@` and setting `main` to it would
rewind/rewrite the published `main`, not fast-forward. Per the brief's explicit
caution that `skills` is this session's actively-churning lane and must be
skipped if divergent, it was skipped to avoid a collision with the session's own
active churn.

`dfl5` (skills generator V1: one active NOTA manifest for generated Skill/Role
outputs, presence-means-active, plus a separate module dependency-only index
mapping module identifiers to source paths and dependency module identifiers)
remains UN-INTEGRATED.

## Checks run

- Per repo, pre-flight gate verified `main == main@origin` before describe/
  bookmark-set/push; every pushed bookmark move reported "Move forward bookmark
  main" (fast-forward) and a post-push `main == main@origin` equality check
  returned SYNCED for all 13.
- No build/test/flake checks run: this batch edits prose `ARCHITECTURE.md` files
  only; no code, schema, or Nix surface changed.

## Follow-up requirements

- **skills/dfl5**: re-attempt the append once the `skills` lane settles —
  rebase the integration onto the current `main@origin` head (`ouzxxuzt`) and
  fast-forward push, or hand to the lane owner. The local checkout at
  `/git/github.com/LiGoldragon/skills` has a stale `@` on the old line that
  should be abandoned/rebased before reuse.
- **nexus routing tension** (recommendation, provisional): the routing manifest
  sent the Nexus engine/decision-plane records to the nexus *translator* repo.
  Integrated as a clearly-scoped distinction, but a future maintainer may decide
  the Nexus-plane intent belongs with the engine-bearing component (e.g.
  criome/sema-engine) rather than the translator. Flagged, not acted on.
