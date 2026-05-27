# Frame — schema-deep new logics

*Meta-report orchestrator's frame. Psyche directive 2026-05-27:
reload fresh intent + schema-next/nota-next state, fortify the
rust skill (agents skip it; the rust code has been shitty),
write the vision for how nota-next + schema-next + schema-rust-next
power the new lojix-horizon logics, then dispatch a background
subagent on a worktree branch to implement the concept with all
tests passing and at least one sandbox operating system booted
on the new logics — psyche framing: "almost a full rewrite".*

## Psyche intent captured this turn

Three Spirit records (2026-05-27):

- **883** (`[schema-next nota-next logics lojix horizon actors]` Decision Maximum) — schema-deep rewrite of new lojix-horizon logics on nota-next + schema-next, deep actor system with schema-defined actor interfaces and schemas, method-only Rust per existing override, "almost a full rewrite". Psyche authorizes modifying schema-next itself if depth requires it.
- **884** (`[skills rust skill-discipline fortification]` Correction Maximum) — agents skip the rust skill when writing rust; resulting code is shitty; fortify the skill mechanism so it cannot be skipped at the authoring moment. Structural prevention, not hortative reminder. (Speech-to-text "rest skill" = "rust skill".)
- **885** (`[concept worktree subagent-dispatch designer-protocol]` Decision Maximum) — methodology: vision lands in meta-report, then dispatch background subagent on worktree branch to implement concept (new logics running with all tests passing plus at least one sandbox OS booted on the new logics).

## Method

Five threads, in order:

1. **Self-train on the schema-derived stack.** Read `schema-next`, `nota-next`, `schema-rust-next`, and `spirit-next` (the public runnable pilot — the precedent for what's being built here). Read `skills/rust-discipline.md` + linked sub-skills + `skills/abstractions.md` + `skills/actor-systems.md` + `skills/component-triad.md` + `skills/enum-contact-points.md` + `skills/typed-records-over-flags.md` + `skills/feature-development.md`. Done this turn.
2. **Fortify the rust skill.** AGENTS.md hard override mandating the read BEFORE rust authoring (universal surface across harnesses); Claude Code project hook (`.claude/settings.json` PreToolUse on Write/Edit of `.rs`) as backstop. Both applied this turn; hook validated (jq schema check + pipe-test on .rs and .md paths).
3. **Write vision.** `1-vision-schema-deep-new-logics.md` carries the substantive vision (orchestrator-authored, the "what to implement" reference for the subagent).
4. **Dispatch subagent in background.** Self-contained brief in §"Subagent dispatch brief" below; subagent reads it, implements, reports back to `2-...md`.
5. **Chat reply.** Locator + the open psyche questions inline.

## What lives where in this directory

- `0-frame-and-method.md` — this file. Orchestrator's frame, method, dispatch brief.
- `1-vision-schema-deep-new-logics.md` — orchestrator-authored vision: schema-deep rewrite, pipeline, runtime triad, deep actor topology, sandbox-OS witness, open questions.
- `2-...md` — slot reserved for the subagent's implementation report.
- `N-overview.md` — slot reserved for orchestrator's synthesis when the subagent returns.

## Relationship to prior work

- **`/34-mvp-and-sandbox-audit/`** — audited the existing lean lojix (horizon-leaner-shape) for MVP + sandbox readiness. `/34/5` synthesised: dramatically advanced feature branch (~20 commits past `/30`), one blocking compile break (B-0 rename), 4 missing structural cutover prerequisites, sandbox-pass needs a witness. `/34` is the **existing-lean-stack picture**; `/35` is the **schema-deep-pilot picture parallel to it**. The two arcs do not compete: `/34` ships the existing lean stack to production faster; `/35` proves the longer-arc schema-deep direction. Operator can amalgamate per `skills/double-implementation-strategy.md` when both have evidence.
- **`spirit-next`** is the precedent. It proves the schema-derived runtime triad works at a real process boundary (`schema/spirit.schema` → schema-next → schema-rust-next → CLI NOTA + daemon rkyv socket). The vision and dispatch brief follow the spirit-next layout exactly.
- **Fortification surface** — the AGENTS.md insert sits immediately ABOVE the existing method-only-no-free-functions hard override (intent record 882). The new override (intent record 884) is the "before you write any Rust at all, read the skills" gate; the method-only override is one specific rule within those skills. Together they form a two-step fence: read the skills, then write code that satisfies all of them.

## Subagent dispatch brief

*Verbatim. This is what the subagent reads as its complete instruction set. The Agent invocation prompt references this file by path; the subagent reads it first.*

### You are a designer subagent

You are a designer-class subagent dispatched by the system-designer lane. Your task is to implement a schema-deep pilot rewrite of the new lojix-horizon logics on a worktree feature branch, demonstrating the concept end-to-end with all tests passing and at least one sandbox operating system booted on the new logics. The psyche framed this as "almost a full rewrite"; take the depth seriously.

### Context — read these in this order

1. `/home/li/primary/AGENTS.md` — workspace compact contract. Pay particular attention to the rust skill hard override (the FIRST rust-related hard override now mandates reading skills/rust-discipline.md and its linked sub-skills BEFORE writing any Rust this session — added 2026-05-27 per intent record 884) and the method-only-no-free-functions override below it. Both are absolute.
2. `/home/li/primary/skills/rust-discipline.md` — Rust discipline index. Then read all sub-files linked from it (`skills/rust/methods.md`, `skills/rust/errors.md`, `skills/rust/storage-and-wire.md`, `skills/rust/parsers.md`, `skills/rust/crate-layout.md`).
3. `/home/li/primary/skills/abstractions.md` — verb belongs to noun. §"Schema-emitted nouns" is the load-bearing section for this work.
4. `/home/li/primary/skills/actor-systems.md` — deep actor topology rules; ZST actors are anti-pattern; State field names the noun the actor IS.
5. `/home/li/primary/skills/component-triad.md` §"Runtime triad" — Signal/Executor/SEMA pattern.
6. `/home/li/primary/skills/feature-development.md` — worktree pattern + multi-repo arc coordination.
7. `/home/li/primary/skills/jj.md` — version control. Every description-taking jj command MUST pass `-m '...'` inline; never let jj open `$EDITOR`.
8. `/git/github.com/LiGoldragon/spirit-next/ARCHITECTURE.md` AND `/git/github.com/LiGoldragon/spirit-next/schema/spirit.schema` — the precedent pilot. Your work is shape-parallel to spirit-next.
9. `/git/github.com/LiGoldragon/schema-next/ARCHITECTURE.md` AND `/git/github.com/LiGoldragon/nota-next/INTENT.md` AND `/git/github.com/LiGoldragon/schema-rust-next/INTENT.md` — the substrate.
10. `/home/li/primary/reports/system-designer/35-schema-deep-new-logics/1-vision-schema-deep-new-logics.md` — the vision you are implementing. This brief summarises; the vision has more depth.
11. `/home/li/primary/reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md` — current lean lojix state (parallel arc; do NOT delete or interfere with horizon-leaner-shape work).

### Worktree setup

Create a new worktree on lojix from `main` (not from horizon-leaner-shape — this is a greenfield pilot, not a port):

```sh
mkdir -p ~/wt/github.com/LiGoldragon/lojix/
jj -R /git/github.com/LiGoldragon/lojix workspace add ~/wt/github.com/LiGoldragon/lojix/schema-deep
cd ~/wt/github.com/LiGoldragon/lojix/schema-deep
jj new main -m 'schema-deep: initial worktree from main'
```

Branch name: `schema-deep`. Worktree path: `~/wt/github.com/LiGoldragon/lojix/schema-deep/`.

Claim the worktree path before editing:

```sh
tools/orchestrate claim system-designer-assistant '[draft:lojix-schema-deep-pilot]' ~/wt/github.com/LiGoldragon/lojix/schema-deep -- 'schema-deep pilot subagent dispatched from /35'
```

### What to build — the deliverable

A working pilot inside `~/wt/github.com/LiGoldragon/lojix/schema-deep/`. Eight artifacts:

1. **`schema/lojix.schema`** — the authored schema declaring every typed noun the runtime touches: `Input`, `Output`, `SemaCommand`, `SemaResponse`, AND internal actor request/reply types (the "schema-deep" depth: even actor mailboxes get schema-emitted message types). Position 1 = imports/exports `{ }`, position 2 = root enum definitions `[ ]`, position 3 = namespace map `{ }`. See `/git/github.com/LiGoldragon/spirit-next/schema/spirit.schema` for the canonical 7-line example you scale up.
2. **`build.rs`** — runs the schema-next macro registry over `schema/lojix.schema` via `SchemaEngine::lower_source_with_context`, asserts the registry reached nested struct-field and enum-variant macros (per spirit-next pattern at `build.rs`), feeds Asschema into schema-rust-next's `RustEmitter`, writes the generated Rust module to `OUT_DIR`.
3. **`src/lib.rs`** — `include!(concat!(env!("OUT_DIR"), "/lojix_generated.rs"));` plus the hand-written `runtime/` modules organized by actor.
4. **`src/runtime/`** — hand-written Rust attaching METHODS to the schema-emitted nouns. Deep actor topology on Kameo 0.20. Proposed topology in vision §"Deep actor topology" (LojixRoot, OperationDispatcher, AuthorizationGate, PlanMaterializer, Builder, ClosureCopier, Activator, ObservationFan, GenerationLedger, EventAppender, GcRootPinner, SubscriptionStream). Every actor's State carries its data; no ZST actors; no `Arc<Mutex<T>>` between actors; release-before-notify on resource-owning actors; trace witnesses on every plane.
5. **`src/bin/lojix-next-daemon.rs`** — daemon binary. Single NOTA argument carrying daemon config (socket paths, redb path, etc.). Per `skills/component-triad.md` §"The single argument rule". `fn main()` is the only free function allowed.
6. **`src/bin/lojix-next.rs`** — thin CLI client. Single NOTA argument carrying an `Input` record. Connects to daemon via Unix socket. `fn main()` is the only free function allowed.
7. **`flake.nix`** — modeled on `spirit-next`'s. `nix flake check` runs the test family (see below). `nota-next`, `schema-next`, and `schema-rust-next` go in as flake inputs.
8. **`tests/`** — the test family (see "Tests" below). Every test under `nix flake check` (per `skills/testing.md`). No mocks when an integration test would suffice.

Plus `README.md`, `INTENT.md`, `ARCHITECTURE.md`, `Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, per the spirit-next pattern.

### Hard rules (every keystroke)

- **No free functions.** Every function lives on a non-zero-sized data-bearing type or trait impl. Except `fn main()` in binaries and inside `#[cfg(test)]` modules. AGENTS.md hard override; enforce in every file you write.
- **Schema-emitted types are the nouns.** Do NOT hand-write parallel type mirrors. When you need a new typed noun, add it to `schema/lojix.schema` and rebuild.
- **Single argument rule.** Both binaries take exactly one NOTA argument (string, file path, or rkyv path). No flags.
- **Methods on emitted types live in separate `.rs` files under `src/runtime/`.** If you need a verb on a schema-emitted struct, write `impl GeneratedType { fn verb(&self) ... }` in a runtime-module file. The emitted type's declaration stays in the generated module; methods are agent-authored alongside.
- **No ZST actors.** Every Kameo actor's State carries data. The State field names the noun the actor IS. `mem::size_of::<EachActor>() > 0` test required.
- **No string typification.** Domain values are typed newtypes (e.g. `GenerationIdentifier(u64)`, not `String`).
- **Typed `Error` enum per crate** via `thiserror`; no `anyhow`/`eyre` at crate boundaries.
- **NOTA strings come EXCLUSIVELY from bracket forms.** Never emit `"`.
- **Headless jj.** Every `jj` command with a description passes `-m` inline. NEVER let jj open `$EDITOR`. If you dispatch sub-sub-agents (you generally shouldn't), restate this rule in their prompts.

### Tests — the deliverable's witness

`nix flake check` must pass and run at minimum:

1. `lojix_next_schema_lowering_reaches_nested_macros` — build.rs assertion (the schema-next macro registry covered nested field/variant macros).
2. `lojix_next_input_output_round_trip_rkyv` — wire frame symmetry.
3. `lojix_next_input_lowers_to_sema_command_exhaustively` — Executor's typed match covers every `Input` variant.
4. `lojix_next_sema_response_maps_back_to_output_exhaustively` — Executor's typed match covers every `SemaResponse` variant.
5. `lojix_next_actor_topology_includes_every_plane` — manifest of expected actors (per `skills/actor-systems.md` §"Test actor density").
6. `lojix_next_trace_witnesses_full_pipeline` — deploy ran through every named plane (trace IS the testable claim).
7. `lojix_next_no_free_functions_outside_main_and_tests` — architectural test (you can grep the source tree).
8. `lojix_next_no_zst_actors` — `assert!(std::mem::size_of::<Each>() > 0)`.
9. **`lojix_next_build_only_pipeline_on_sandbox`** — spawn daemon, send NOTA `Input` via CLI, daemon drives full pipeline, writes `GenerationRecord`, sandbox image built and pinned as GC root.
10. **`lojix_next_activation_on_nspawn_sandbox`** — `nspawn-dune-on-prometheus` (or adapted equivalent) boots a sandbox image; daemon activates a new generation against it; observation stream returns `ActivationComplete`. (Study `CriomOS-test-cluster`'s `checks/nspawn-*` to see how the existing nspawn runner is invoked; adapt or reuse.)

Tests 9 + 10 are the sandbox-OS witness that Spirit 883 names as the precondition for "almost a full rewrite running."

### Reporting back

When you finish (or hit a hard blocker), write a report at:

```
/home/li/primary/reports/system-designer/35-schema-deep-new-logics/2-<descriptive-name>.md
```

Include:

- Summary of what you built (paths, structure, line counts).
- Test results (each test's pass/fail with output excerpt for any failure).
- Any schema-next or nota-next limits you hit (e.g. "vectors required for `Vec<GenerationRecord>`; schema-next does not yet express them"); these need psyche notification. Capture as Spirit `Clarification` records (topic vector at minimum `[lojix schema-next concept]`).
- Architectural decisions you had to make that the brief didn't pin (e.g. how you handled GC root pinning across the nspawn boundary).
- "What would land in lojix proper if operator amalgamated" list (per `skills/double-implementation-strategy.md`).

If you can't make progress on a particular sub-deliverable, REPORT THE BLOCKER. Don't ship half-implementations as if they work; the psyche has explicitly warned that shitty code is the failure mode this whole exercise is trying to fix.

### Don't do these things

- Don't push to `main` of any repo. Designer lanes do not push to main (AGENTS.md hard override, intent record 515). `jj git push --bookmark schema-deep --allow-new` is fine — that's your branch.
- Don't delete or modify the existing `horizon-leaner-shape` branch or worktree.
- Don't dispatch sub-sub-agents unless the work is genuinely parallelizable; if you do, every sub-sub dispatch must be `run_in_background: true` (AGENTS.md hard override, intent record 539).
- Don't commit changes to the orchestrator workspace (`/home/li/primary/`). Reports go via Write/Edit; the user controls commits.
- Don't modify `/home/li/primary/AGENTS.md`, `/home/li/primary/ESSENCE.md`, `/home/li/primary/INTENT.md`, or any other workspace guidance file — if you find a workspace rule needs adjustment, report it in `2-...md` and let the orchestrator decide.
- Don't `cat`/`head`/`tail`/`sed`/`awk` from Bash when Read/Edit fit. Don't search `/nix/store`. (Per AGENTS.md hard overrides.)

### Intent capture

The psyche prompt that initiated this work landed with the orchestrator, not you. Intent is already captured as Spirit records 883/884/885. Do NOT re-capture. But: if you discover something during implementation that the psyche should know (a fundamental schema-next limitation, a test that the brief said would work but doesn't), capture YOUR discovery as a Spirit `Clarification` record with magnitude at least `Medium`.

### Closing

This is "almost a full rewrite" pilot work per the psyche. Schema-deep means every typed noun in the runtime comes from one authored `.schema` file. Method-only means every verb lives on a noun. Deep actors means every plane is a named Kameo actor with State that names what the actor IS. Sandbox OS witness means the new logics actually drive a deploy against a real (sandbox) OS, not a mock.

Take the depth seriously. Begin.

## Risks + open questions

- **Worktree path collision.** Existing `horizon-leaner-shape` worktree at `~/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/` is unaffected; new path `~/wt/github.com/LiGoldragon/lojix/schema-deep/` is parallel.
- **Schema-next language gaps.** spirit-next's `ARCHITECTURE.md §Known limits` mentions schema doesn't yet express vectors; lojix's deploy events naturally want vectors (`Vec<GenerationRecord>`, `Vec<ObservationRecord>`). Psyche authorized modifying schema-next if depth requires (record 883). Subagent surfaces concrete vectors-needed list before forking schema-next.
- **Existing horizon-leaner-shape work.** The subagent does NOT delete or alter it. The schema-deep pilot is greenfield; horizon-leaner-shape continues on its own arc until cutover or amalgamation.
- **Sandbox OS test.** Prometheus's `nspawn-dune-on-prometheus` runs from `CriomOS-test-cluster`. The new logics need a sandbox-OS witness either by re-anchoring that flake or via a fresh sandbox. Subagent decides.
- **Settings hook caveat.** `.claude/settings.json` didn't exist when THIS session started; the watcher won't pick it up until the psyche opens `/hooks` once or restarts Claude Code. The hook is correctly written (syntax + pipe-test passed); it just needs that reload step. Surface in chat.
- **Open psyche questions** (also restated in `1-vision`):
  1. Worktree on existing `lojix` (default) vs new repo `lojix-next` paralleling `spirit-next` exactly?
  2. Sandbox OS choice: `nspawn-dune-on-prometheus` (default) or fresh?
  3. Schema-next vector support: authorize subagent to fork-and-modify if blocking?
  4. /29 role-merge: stays deferred for this pilot (default)?
  5. Promotion criteria for pilot → lojix main?
