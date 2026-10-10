# Persona: its state, what was slated for it, and the older Nexus generation

Read-only witness for the main flow's minimal-Persona anatomy proposal. Method: `git` inspection of
the checkouts under `/git/github.com/LiGoldragon/` and file reads under `/home/li/primary`; three
read-only subflows fanned out the grepping, their findings marked CLAIMED where not re-verified here.
Paths are absolute. Nothing was edited, no HEAD moved.

## The one fact that governs the proposal

WITNESSED — the standing ruling already says Persona must be rewritten. The living's words,
`/home/li/primary/flows/e06e4c07/vision/archive-nexus.md:208-210`, 2026-08-19, STT:

> But everything we're going to build is going to be a nexus
> now, and anything that has already been built that did not take the
> shape of The nexus is going to be rewritten.

WITNESSED — distilled into standing vision at `/home/li/primary/Vision/nexus.md`, `## Why everything
is a Nexus`: "Everything built from now on is a Nexus, and what was built in another shape is
rewritten as one." Persona is in the other shape: **one** socket, not two; a `-daemon` binary, not a
`-nexus`; no dependency on the `nexus` crate. Details in §1 and §3.

## 1 · Persona itself

WITNESSED unless marked.

- Path `/git/github.com/LiGoldragon/persona`; remote `git@github.com:LiGoldragon/persona.git`.
  Checkout **clean**, **detached HEAD** at `09ee526cbde8dd6a9dc54b1b3583e2a034d0e063`.
- **Not at origin/main.** `origin/main` is `9469b0a`, 2026-08-13, `docs: mark Protos estate status`;
  HEAD is **21 commits ahead** of it. Those 21 are pushed — HEAD equals `origin/f6db8d-arity-front`
  exactly — but **never merged to main**, so the entire Datom migration of Persona lives on an
  unmerged branch. `origin/f6db8d-datom-migration` sits at `651fe75`, inside the same run.
- Last ten commits, all `li`, all dated 2026-09-12: `09ee526` Repin the persona-message flake
  input to message 0.12.0 at its landed head · `5fd40b3` Document the 0.5.0 breaking upgrade ·
  `3f13bac` Correct two comments that still named the deleted signal-frame · `8590f45` Repin the
  persona-message flake input to message 0.12.0 · `a9f6b79` Advance to the arity-split front; land
  the Datom migration; 0.5.0 · `651fe75` Give router-write-configuration the ten fields it now
  takes · `a3e36ac` Keep the sandbox artifact names the scripts actually write · `7e8dd0c` Drop
  signal-frame and signal-sema from the dependency table · `67cc0b4` Correct the CLI text statement
  in AGENTS.md · `5367e97` Follow the contracts check renames in the flake.
- First commit `dd96d3a 2026-05-06 persona: scaffold core state contract`.
- **Nix**: `nix flake show` evaluated clean, exit 0, warnings only (`crane`/`fenix` overrides on
  inputs having no such input); `apps`, `checks` and `packages` present for both Linux systems. A
  full `nix build` was **not run** — not cheap or bounded.

### What it does today

- README (`/git/github.com/LiGoldragon/persona/README.md`): "Persona is the engine manager
  and integration repository for the multi-harness AI system." Wires component repos through
  Nix; component implementation lives in `meta-signal-persona`, `sema-engine`, `router`,
  `system`, `harness`, `message`.
- `ARCHITECTURE.md` is 1811 lines. §0 TL;DR: `persona-daemon` is "the host-level engine-management
  daemon", runs as a dedicated `persona` system user, supervises N engine instances, allocates
  per-engine sockets and state directories.
- Binaries: `persona` (CLI), `persona-daemon`, `persona-write-configuration`, plus a
  `persona_component_fixture` and six `wire_*` test shims.
- **One socket.** `/git/github.com/LiGoldragon/persona/src/configuration.rs` carries a single
  `manager_socket_path` ("the working listener") and a `socket_mode`. No meta socket, no
  `persona-meta` binary — though `meta-signal-persona` exists as a contract repo.
- Sema: `/git/github.com/LiGoldragon/persona/src/manager_store.rs` (1199 lines) is a Kameo
  `ManagerStore` actor over `sema-engine`, one table `manager.records`, `SchemaVersion::new(4)`,
  store at `manager.sema` beside the socket or at `$PERSONA_MANAGER_STORE`. The stored kinds are
  `StoredEngineRecord { engine: EngineIdentifier, status: EngineStatusReport }`,
  `ComponentProcessState`, `StoredActiveVersion`. ARCHITECTURE §1.5: "The manager Sema store owns
  the engine catalog: engine identities, owners, component desired state, lifecycle observations,
  and inter-engine route declarations."
- **No quota anything.** `grep -rni "quota|rate.limit|subscription" src/` returns nothing.
  This confirms the 692df8 witness the brief cites.
- Size: 12 370 lines of Rust across `src/`; 15 test files. Stale internals: `ARCHITECTURE.md`
  §"Pending schema-engine upgrade" points at four `reports/designer/*.md` and `reports/operator/*.md`
  files that **do not exist** — `reports/` holds only three May 2026 design reads.

### Where it is deployed or referenced

CLAIMED (subflow, greps over CriomOS, CriomOS-home, CriomOS-pkgs, CriomOS-lib, lojix, cloud):

- **Persona is not running anywhere.** No systemd unit for `persona` or `persona-daemon` exists in
  any of those repos, and CriomOS has **no** flake input named `persona`; `signal-persona` appears
  only transitively via the `spirit` input (`/git/github.com/LiGoldragon/CriomOS/flake.lock:3777`).
- The only Persona-named unit is `persona-router.service`
  (`/git/github.com/LiGoldragon/CriomOS/modules/nixos/persona-router.nix:133`), imported
  unconditionally by `.../criomos.nix:22` but gated `mkIf personaRouterEnabled` on a `PersonaRouter`
  node service that appears in no node of `/git/github.com/LiGoldragon/goldragon/proposal.datom`. It
  starts only inside the VM test `.../criome-auth-integrated-test.nix:91`, and its package comes
  from the `router` flake input, not from `persona`.
- `PersonaDevelopment` is a live node-service tag (on `ouranos`) gating Lojix identity ownership,
  repository-receive and the Spirit home daemon — a tag, not a unit, and not Persona.
  `/git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix:322` asserts the
  *absence* of the old `persona-spirit` daemon.

### How upkept the ecosystem is

WITNESSED (`git log -1` per repo): `mind` 2026-07-31 and `spirit` 2026-08-08 (docs-only commits, 21
and 18 dirty files respectively), `router` 2026-08-13 (docs only); `persona`, `harness`, `terminal`,
`message`, `system`, `introspect`, `orchestrate` all 2026-09-12, with `harness`, `terminal` and
`system` each carrying one unpushed "Found in tree: orphaned repin…" commit. That 2026-09-12 wave was
a mechanical repin, not feature work.

## 2 · What was slated for Persona

Psyche records, oldest first. All CLAIMED from a subflow's gathering except the three marked
WITNESSED, which this flow read directly.

1. `/home/li/primary/flows/012fbf07/vision/gradientsOfAuthority.md`, 2026-08-11, typed,
   `## 2026-08-11 — no more beads for handover; the meta-harness replaces beads`:
   > No more beads. Beads are tools which means lowest authority; using them for handover is stupid. In fact, we need to replace beads with our meta-harness (context-stratification-seizure) approach to get much better results. but datom and ethos first, so we can actually write all this logic
2. WITNESSED `/home/li/primary/vision-raw/gradientsOfAuthority.md:126-129`, 2026-08-11,
   `## 2026-08-11 — until we design the meta-harness (persona) properly`:
   > yes, until we design the meta-harness (persona) properly and all the
   > data is passed along the right agent call, like magic (you are logging
   > psyche right?)
3. `/home/li/primary/flows/358f143a/vision/workspace20.md`, 2026-08-17, typed,
   `## 2026-08-17 — role skills hold the awareness seat for now; the persona meta-harness will move this fast`:
   > skills for now. It might evolve differently later. This will move quite fast as we build the persona meta-harness
4. WITNESSED `/home/li/primary/flows/15b67974/vision/persona.md`, 2026-08-21, typed,
   `## 2026-08-21 — persona untouched for a long time, yet slated to orchestrate the entire meta harness`:
   > That repo hasent been touched in a long time, even though it's
   > slated to orchestrate the entire meta harness (called persona)
5. WITNESSED `/home/li/primary/vision-raw/spiritComponentAndFile.md:14-21`, 2026-08-21, typed:
   > persona-spirit? that is an abandonned repo. What is in there that
   > isnt in spirit? Plus spirit is to be abandonned for psyche.
6. `/home/li/primary/flows/cff271af/vision/reports.md`, 2026-08-22:
   > Until we have a more advanced meta-harness that can do really cool stuff, like fetch a bunch of responses from a bunch of previous flows as the prompt, or perhaps even after editing it through another flow, passing that as a prompt to yet another flow, until we have that, we essentially have to depend on the current infrastructure, which is that the most useful and precious context is only that which the parent flow gives it as its starting prompt.
7. WITNESSED `/home/li/primary/flows/1a6ca4/vision/personaMetaHarness.md`, 2026-09-05, STT:
   > That phase is like the wild west phase of thinking machines, and the persona meta-harness is going to bring in the dawn of the more complete thinking machine systems, which will be a complex infrastructure of a kind of thinking machine legal system interworking apparatus.
8. `/home/li/primary/flows/6cc91b/notion/persona.md`, 2026-09-13, STT (a **notion**, hedged in
   the file itself):
   > Those are nexuses, like some kind of high-level orchestrator or persona, I think, that might be the meta. I think the persona is basically the root orchestrator, the system D of this whole concept.
9. WITNESSED `/home/li/primary/flows/024bc7/vision/sandbox.md`, 2026-09-13, STT:
   > Establish a coherent system here where you're going to figure out a way to start a new process, maybe with this harness component that you need to describe anatomically well. You can have just a proof of concept of it all, like the persona. Just start a full sandbox.
10. `/home/li/primary/flows/024bc7/vision/soul.md`, 2026-09-13, STT (duplicated at
    `/home/li/primary/flows/bcd02a/notion/persona.md`):
    > We're going to create this private layer, the soul, basically. We could call it that: the soul. It's like the private part of the persona.
11. WITNESSED `/home/li/primary/flows/6cc91b/vision/forge.md:9`, 2026-09-14, typed:
    > Let's do all of the main components that are in production now and our most important candidates, which are persona, to get all of this started: managing it and sandboxing it, which will allow us to do well. Persona will involve components that take care of sandboxing and things.
12. `/home/li/primary/flows/6cc91b/vision/pairHierarchy.md`, 2026-09-14, STT:
    > eventually will have representation in one of the nexuses, like in Persona, the different layers of authority.

WITNESSED — `/home/li/primary/vision-raw/persona.md` contains only the line `# Persona`. Nothing
about Persona has ever been distilled into `/home/li/primary/Vision/` or `/home/li/primary/Intent/`:
a grep for "persona" over both returns zero hits. **Persona has no standing vision document.**

Reports naming Persona substantively (CLAIMED, subflow), all under `/home/li/primary/flows/`:
`1a6ca4/reports/componentVision.md` ("Spawn order: supervisor -> sema-upgrade -> mind -> orchestrate
-> router -> harness -> terminal -> message -> introspect -> spirit"); `6cc91b/reports/stateAudit.md`
("persona is 15455 lines with a 1811-line architecture document and no live process"; "each build
their own daemon shell on `triad-runtime` rather than on `nexus`"); `6cc91b/reports/audit.md`
("Almost nothing runs … persona (15.5k) … built, tested, and idle"; "criome, persona and upgrade ship
no meta client at all"); `7b4d4c/reports/proposal.md` (fork F19: "`persona` … is subsumed by the
Nexus, or revived as the layer above it"); `fd301d9a/reports/kameoContext.md` ("Persona has eight
actors and manual lifecycle"); `6cc91b/reports/visionMap.md`; `34d94e/reports/visionStateAudit.md`
("aspirations, not verified deployments").

## 3 · The older generation of Nexus work

WITNESSED unless marked.

- The `nexus` skill (loaded through the Skill tool) opens: "A Nexus is the long-running whole with
  at least two sockets, a default CLI client per socket, and the signal contracts it is compiled
  with. Its long-running executable is `<nexus>-nexus`; call it a Nexus, never a daemon."
- `/git/github.com/LiGoldragon/nexus` — remote `git@github.com:LiGoldragon/nexus.git`, clean,
  detached HEAD `c495f2a` **equal to origin/main**. A **library only**, v0.5.0, **510 lines** across
  `authority.rs configuration.rs lib.rs relocation.rs situation.rs`; deps `rkyv` + `thiserror`.
  Six commits, all 2026-09-10 to 2026-09-12, first `e67735e 2026-09-10 Nexus: establish universal
  configuration lifecycle`. README: "the universal library for Nexus components… owns the standard
  ontology shared by every long-running Nexus."
- **Only two repositories consume it**: `grep -l 'LiGoldragon/nexus' */Cargo.toml` →
  `/git/github.com/LiGoldragon/orchestrate` and `/git/github.com/LiGoldragon/lojix`.
  CLAIMED (subflow): orchestrate is a three-crate workspace `orchestrate-nexus` / `orchestrate` /
  `orchestrate-meta`, clean and at origin/main `9070cbb`, the canonical shape; lojix is at
  `0bb3d66`, clean but **7 commits behind** its origin/main `c4bba4f`, and pins an older `nexus` rev
  than orchestrate does.
- CLAIMED (`/home/li/primary/flows/857335/reports/nexus-gap-audit.md`, 2026-09-10): Nexus compliance
  has been audited for Lojix, Horizon, Orchestrate and Ethos Zero only — Persona is not in it.
- Design flows: `e06e4c07` (index line 8, "Nexus vocabulary settled") holds no `reports/`; the
  vocabulary lives in `/home/li/primary/flows/e06e4c07/vision/archive-nexus.md`. `5c8be3ca`
  (index line 10) is the flow-artifacts protocol, **not** a Nexus flow. The distillation ran through
  `acbb6006`, `4decf7`, `564f55` and `fe34eb` into `/home/li/primary/Vision/{nexus,flowNexus}.md`.
  `archive-nexus.md` carries superseding notes from `fe34eb` (2026-09-10): the living ruled the
  Nexus-Core runtime concept overthinking; there is no Nexus root and no separate engine part.

### Persona predates Nexus and was not built on it

WITNESSED. Persona's first commit is 2026-05-06; the `nexus` repo's is 2026-09-10 — four months
later. `grep nexus` over `/git/github.com/LiGoldragon/persona/Cargo.toml` and `flake.nix` finds no
`nexus` dependency. Persona sits on the *older* stack: `sema-engine`, `triad-runtime`, `kameo`, and
ten `signal-*` / three `meta-signal-*` contract crates. Its binaries are `persona-daemon`, the
naming the skill retires. Persona is the predecessor generation; `orchestrate` and `lojix` are the
only two things rewritten onto the Nexus base so far.

## 4 · Good ideas left behind

Designed or logged, never built. Source and one verbatim line each.

1. **A meta socket and a `persona-meta` CLI.** `/home/li/primary/flows/6cc91b/reports/stateAudit.md`
   (CLAIMED): "No `meta-persona` binary despite `meta-signal-persona`". The contract repo exists; the
   privileged surface does not.
2. **The meta-harness replacing Beads for handover.**
   `/home/li/primary/flows/012fbf07/vision/gradientsOfAuthority.md`: "we need to replace beads with
   our meta-harness (context-stratification-seizure) approach to get much better results."
3. **Persona deciding each flow's system prompt at launch, replacing subagents.**
   `/home/li/primary/Vision/flowNexus.md`: "A Nexus component decides the system prompt and
   everything about a launch, replacing the harness's subagents with specialized harnesses launched
   with specialized system prompts." (Distilled into Flow Nexus, not Persona — the slot is open.)
4. **Chained-flow prompt assembly.** `/home/li/primary/flows/cff271af/vision/reports.md`: "fetch a
   bunch of responses from a bunch of previous flows as the prompt, or perhaps even after editing it
   through another flow, passing that as a prompt to yet another flow".
5. **Sandboxing as a Persona concern, with a full-sandbox proof of concept on Prometheus.**
   `/home/li/primary/flows/6cc91b/vision/forge.md:9`: "Persona will involve components that take care
   of sandboxing and things." The scaffolding exists as shell scripts
   (`/git/github.com/LiGoldragon/persona/scripts/persona-engine-sandbox`), not as a component.
6. **Layers of authority represented inside Persona.**
   `/home/li/primary/flows/6cc91b/vision/pairHierarchy.md` (CLAIMED): "eventually will have
   representation in one of the nexuses, like in Persona, the different layers of authority."
7. **The Soul — the private layer.** `/home/li/primary/flows/024bc7/vision/soul.md` (CLAIMED):
   "It's like the private part of the persona." Chartered, not active (per `CLAUDE.md`).
8. **Reducer-owned single-state-machine core.**
   `/git/github.com/LiGoldragon/persona/reports/2026-05-06-persona-core-state-machine.md`: "Persona
   state itself is the reducer-owned truth: commands enter, transitions land, observations are
   appended, and every projection reads from that same record."
9. **The desktop control plane / composer.**
   `/git/github.com/LiGoldragon/persona/reports/2026-05-07-persona-desktop-control-plane.md`: "the
   human writes Persona messages through a dedicated composer, and where the router can ask the
   compositor for short critical-section authority".
10. **Per-engine state and socket scoping.** `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md`
    §1.5: "Exact host paths are deployment-owned, but the `<engine-id>` scoping is architectural."
    The one piece of the old design a minimal Persona most plausibly keeps.
11. **Schema-driven contract emission.** `ARCHITECTURE.md` §"Pending schema-engine upgrade": "convert
    to a single `persona/persona.schema` file." Its design reports no longer exist in the repo;
    Ethos + Datom now occupy this role.
12. **`persona-system` / FocusTracker.** `ARCHITECTURE.md` §0.7: "plan substance does not grow until
    system is unpaused by a real consumer." Built, paused, never consumed.

## Sources

- `/git/github.com/LiGoldragon/persona` — `git log`, `git status`, `git rev-list`,
  `git for-each-ref`, `nix flake show`; `README.md`, `ARCHITECTURE.md`, `Cargo.toml`, `flake.nix`,
  `src/configuration.rs`, `src/main.rs`, `src/manager_store.rs`, `reports/*.md`.
- `/git/github.com/LiGoldragon/nexus` — `git log`, `README.md`, `Cargo.toml`, `src/`; and
  `git log -1` plus `git rev-list --count origin/main..HEAD` in `mind`, `router`, `spirit`,
  `harness`, `terminal`, `message`, `system`, `introspect`, `orchestrate`, `lojix`.
- `/home/li/primary/Vision/nexus.md`, `Vision/flowNexus.md`, `vision-raw/persona.md`,
  `vision-raw/gradientsOfAuthority.md`, `vision-raw/spiritComponentAndFile.md`,
  `vision-raw/actorLibrary.md`, `flows/index.md`.
- `/home/li/primary/flows/e06e4c07/vision/archive-nexus.md`, `flows/15b67974/vision/persona.md`,
  `flows/1a6ca4/vision/personaMetaHarness.md`, `flows/024bc7/vision/{soul.md,sandbox.md}`,
  `flows/6cc91b/vision/{forge.md,pairHierarchy.md}`, `flows/6cc91b/notion/persona.md`,
  `flows/bcd02a/notion/persona.md`, `flows/857335/reports/nexus-gap-audit.md`.
- The `nexus` and `flow-evidence` skills, loaded through the Skill tool.
- Three read-only subflows of this flow (deployment references; psyche records; Nexus generation),
  whose findings are marked CLAIMED where not re-verified here.
