# Flow 674a4dab

Design audit of the CriomOS / Lojix / Horizon stack: acquire what the psyche
wanted from recent Codex transcripts (read in depth, not from logs alone), then
audit the current state of CriomOS, CriomOS-home, Goldragon, Lojix, Horizon and
the package/source repositories for broken separation of concerns, duplicated
sources of truth, and slop; propose the end-shape; close with the three most
important questions.

STT note: the living said "Logix" — the repository is `lojix`. "Horizon" is
`horizon-rs` plus `criomos-horizon-config`.

## Plan

- Wave 1: psyche acquisition per plane (OS/Home/Goldragon, Lojix, Horizon,
  packages/sources, origins in older sessions) + structural maps (Nix side,
  Rust side).
- Wave 2: archaeology of how each flagged shape came to be; audit against the
  acquired vision, seeking disconfirming evidence.
- Wave 3: verification of findings, end-shape proposal, report.

## State

Delivered: reports/criomosStackAudit.md (consolidated) and the artifact
https://claude.ai/code/artifact/9202d962-c173-4ce1-aa03-1a8aca5be273 .
the three questions await the psyche's rulings; distillation
proposal awaits approval (scratchpad/distillationDraft.md, §6 of the report).

Earlier state:

Wave 1: maps landed (witnesses/nixSideMap.md, witnesses/rustSideMap.md);
psycheLojix.md landed; OS/Home/Goldragon, Horizon, packages, origins in flight.
psycheOsHomeGoldragon.md landed.
psycheHorizon.md and psycheStackOrigins.md landed.
psychePackagesSources.md landed.
Wave 2b dispatched: audits of the Nix side, Lojix, Horizon/Goldragon, and packages/sources against the acquired vision. auditLojix.md landed: Lojix largely aligned (OS-only, no-flag CLIs, no hardwired hosts); broken Query.ByDeployment (one hard-coded false), stub CheckHostKeyMaterial, empty manifests, 11 duplicated types, request knobs without psyche ask; it accepts content-addressed flake emission on the strength of CriomOS's own flake.nix comment (agent origin) — provenance to be settled by the Rust archaeology and challenged in wave 3.
Wave 2a dispatched: archaeology of the shapes the maps surfaced (Nix side,
Rust side) — git history plus the transcripts of the days each shape landed.

Map conflict to resolve: the Rust map says the cluster proposal (nodes, users)
is goldragon/datom.dotos and criomos-horizon-config/horizon.dotos holds only
pan-horizon config; the Nix map says horizon.dotos holds the topology.

Remembered: 01a048a6, 01a04881 — depth 1
Most relevant: the AgentIntercomGraphical gate bundled generic graphical
prerequisites with agent-specific GUIs; the living's working hypothesis was that
the gate was really an Edge-node concern under an unrelated name; deployment
preflight is blocked because no manifest supplies transport/builder/selector.

Caution for the report: "way too complex. start with ultra minimal" (01a02fe5
L1489) was said of a proposed skill-training text, not of Lojix itself; cite
it only for the psyche's general cut toward minimal proposals.

## Candidate questions for the psyche (from acquired tensions)

- criomos-core and extended-horizon: one repository or two? (core = shared
  Nix interpretation superseding CriomOS-lib; extended-horizon = Nix derivation
  over Lojix-emitted Horizon; relationship unruled.)
- Horizon's line: which derived fields stay in the Rust reducer and which move
  to Nix ("WHAT, never HOW", "mostly just the reducer", "hack for now").
- NodeSpecies + NodeService merge into one roles vector: settled 2026-05-21,
  never re-confirmed.
- Deployment selection: what a manifests/*.dotos entry contains, who authors it.

## Recurring cause candidates (for the report's cause section)

- A tentative psyche question ("home ostensibly, right?", "that could be a
  standalone repo") captured by the agent as a settled ruling; the psyche
  catches it hours later ("why did you change the design?", "you mean that
  repo already existed?"). Evidence: 01a0437d L516/L4164; 01a02b4b L932.
- Agent-initiated repositories/extractions accepted by silence (CriomOS-lib,
  CriomOS-pkgs, criomos-horizon-config; lojix daemon from an agent plan).
- Composite gates named for a use rather than a concept (AgentIntercomGraphical).
- Agents add knobs/variables/timeouts the psyche never asked for; psyche
  removes them ("what timeout? I never approved any timeout").

## Working-copy state (witnessed 2026-08-28, probe: git rev-parse/rev-list)

The /git checkouts agents read are not at main: CriomOS HEAD detached at
21af0c3, 11 behind origin/main 45e83fb; CriomOS-home HEAD 4e36d44, 9 behind
origin/main ed6832c (64 files differ); goldragon, lojix, horizon-rs local main
each 1 behind origin/main; lojix has 13 untracked `.beads/` (dolt) files.
CriomOS-lib, CriomOS-pkgs, criomos-horizon-config are at origin/main.
Consequence: wave-1 maps and the first Nix audit read stale code; wave 3
re-verifies every current-state claim against origin/main via `git archive`
into the scratchpad. Running subflows were told.

archaeologyRustSide.md landed: Lojix's whole internal architecture was built
by agents in June 2026 with no surviving psyche transcript; the +11.5k-line
spike (2026-08-04, durable deploy transitions) and the flow/model type split
(2026-08-06) were autonomous agent decisions (sessions with zero psyche
messages); horizon-rs's 54-field Node and nine species were authored by the
living on 2026-04-23; criomos-horizon-config was an agent extraction that
horizon-rs main reportedly still does not consume (to verify at origin/main).

Lojix verification (origin/main 33b8b6b): ByDeployment `false` at
schema_runtime.rs:4187 CONFIRMED, untested; CheckHostKeyMaterial stub at
:4276-4283 CONFIRMED, no consumer anywhere; 11 identical type pairs CONFIRMED,
converted by scattered inline code (no From impls); 10 store tables: 8 used,
container-lifecycle produced-but-never-queried, outbox/transition-intent
internal only; WatchDeployments/WatchCacheRetention have no consumer outside
lojix; flake emission ~490 lines coupled to CriomOS by input names
(horizon/system/deployment/secrets) — agent-designed 2026-04-24, no psyche
transcript; the 13 dirty lojix files are `.beads/` dolt residue.
schema_runtime.rs 8,127 lines: pipeline ~2425, materialization/store ~1610,
query serving ~865, inline tests ~2049.

auditHorizon.md landed (origin/main): criomos-horizon-config has no consumer
(domain suffixes hardcoded in horizon-rs domain.rs:108,121 and authored in
goldragon datom.dotos:276; LAN also in CriomOS-lib); horizon-rs emits ~54
fields/node of which BehavesAs(11)+is_*(16)+ComputerIs(5)+lid-switch(3) are
Nix-derivable; species 11 + services 7, roles merge unimplemented; all data
still .dotos; AgentIntercom removal RESOLVED on main; prometheus SSH block
hardcoded in CriomOS-home. End-shape: ~15-field reducer, criomos-core
interprets, pan-horizon config a real second input.

Artifact design plan (report page): subject is a stack audit read by its
owner — utilitarian editorial, no hero. Palette: ground #F7F5F0 (warm paper)
/ dark #15171B; ink #1E2126 / #E6E3DC; accent cold cobalt #2B4C9B (dark
#7FA1F0) for plane labels and links; severity: blocks #B3372B, duplicates
#B07A1C, unasked #5B6B7A, resolved #2E7D5B. Type: display "Fraunces" (serif
with character, used for section titles only), body "Source Serif 4", data/
diagrams "IBM Plex Mono". Layout: a fixed left rail of plane names as the
table of contents; ASCII diagrams in mono blocks with overflow-x; findings as
a two-column ledger (what it is | what is wrong) with a severity chip; the
three questions as the closing full-width block. Distillation draft in
scratchpad/distillationDraft.md.

Nix verification (origin/main): F4/F5 REFUTED — AgentIntercomGraphical and the
blanket x86 gate are gone on main (CriomOS 0e81e59, CriomOS-home 59d8423);
desktop gating = Edge + Medium + per-package meta.platforms. F1 pkgs-from-Home
CONFIRMED (flake.nix:160); F3 PARTLY — embedded constants now dead code,
both Homes take constants from CriomOS-lib via mkForce (flake.nix:765), still
not from Horizon; stateVersion in three places; prometheus hardcoded twice;
/home/li paths hardcoded; mirror.nix force-disabled; element.nix orphan;
compat/migration hooks; CriomOS-home 73 inputs, 4 nixpkgs revisions (herdr,
orca-ide keep their own). New on main the first audit missed: core-packages.nix
(criomos.corePackages.{codex,claude} — the psyche's "realized option"),
owned-agents/, claude-remote-control.nix, hexis input, codex desktop-gate.nix
wrapper (provenance unverified), +13 Home checks (61 total), +1 OS check.

desktop-gate.nix provenance: agent initiative (799f8fd, 2026-08-28) realizing
"the desktop apps using it locally"; no psyche ask for a gate or wrapper.
Report and artifact updated. All subflows returned; no Locks held.

2026-08-29 — the psyche asked what "manifest" in question 3 is. Witnessed:
`manifests/*.dotos` in CLAUDE.md is the Curriculum skill-deployment manifest
(`manifests/active-outputs.dotos`, deleted 2026-08-25 in 339b22a81); Lojix has
no manifest concept (grep of src/README/AGENTS at origin/main: nothing). Flow
01a048a6 conflated it with OS deployment selection; this flow repeated the
conflation. Report, page and question 3 corrected: the real object is the
per-node `Deploy.Host` typed request, which exists nowhere durable.

2026-08-29 — the psyche removed the manifests line from the entry files and
asked what the Deploy.Host payload looks like; answered from the signal-lojix /
meta-signal-lojix ethos and the real Zeus invocation; appended to the report.

2026-08-29 — instruction: redesign the Deploy.Host payload without any
repetition. Proposal composed in the main flow; appended to the report as
"Deploy request, redesigned". (A vision/ file first written for this was
removed: the psyche corrected that vision/ holds psyche only, not rulings or
instructions; the psyche-interraction skill's wording is in error.)

2026-08-29 — psyche approved the psyche-interraction skill correction
("you only log psyche not rulings"); edit of the authored source in
Curriculum/skills plus regeneration of the generated trees dispatched to a
subflow. Result pending.
