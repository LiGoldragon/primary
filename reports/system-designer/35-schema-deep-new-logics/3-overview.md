# Overview — schema-deep new logics (orchestrator synthesis)

*Orchestrator synthesis of the `/35` meta-report. The pilot
shipped: all 10 tests of the deliverable's witness family pass
under `nix flake check`, branch `schema-deep` pushed to
`origin/schema-deep` (commit `rnwxqrlzmrmm`). Pilot is ready
for psyche review and (when promoted) for operator amalgamation
per `skills/double-implementation-strategy.md`.*

## What landed

A working schema-deep pilot at `~/wt/github.com/LiGoldragon/lojix/schema-deep/`. 3,224 lines of new code (1,939 in `src/runtime/` for the actor topology + methods on schema-emitted nouns; 588 in `tests/`; 80 in `schema/lojix.schema`; the rest in binaries, build, flake, error). Branch pushed; `nix flake check` returns `all checks passed!`.

The schema-deep promise from `/35/1` §"What 'schema-deep' buys" is realised: `schema/lojix.schema` is the single source of truth for **28 typed nouns** spanning every surface the daemon touches — 4 root enums (Input, Output) and 6 namespace enums (SemaCommand, SemaResponse, ActorRequest, ActorReply, plus payload helpers), 18 namespace records/newtypes, and `DaemonConfiguration` as a schema-emitted record parsed from the daemon's single NOTA argument. Hand-written Rust attaches methods to those emitted nouns; the 9-plane Kameo topology has every actor's State naming the noun it IS; no free functions in production code (enforced by `tests/no_free_functions.rs` architectural-truth grep test).

End-to-end witness — `lojix_next_build_only_pipeline_on_sandbox` (test 9) spawns the actual `lojix-next-daemon` + `lojix-next` CLI binaries, sends a NOTA `Submit`, daemon drives all 9 actors in sequence, writes a `GenerationRecord`, subsequent CLI `Query` returns the snapshot. `lojix_next_activation_on_nspawn_sandbox` (test 10) exercises Activator + ObservationFan with a sandbox-mode toolchain that issues `nspawn-sandbox-activate`; observation stream surfaces `Activating Complete` + `Observed Complete`.

## The most important finding — schema-next limit navigated, not forked

The current `schema-next` (locked at `807c5250`) enforces exactly 4 positional root objects, and only `Input`/`Output` get full signal-frame plumbing (route enum, short header, encode/decode). The subagent (Spirit 883 authorized fork-if-needed) **chose to navigate rather than fork**: placed `SemaCommand`/`SemaResponse`/`ActorRequest`/`ActorReply`/`DaemonConfiguration` as **namespace enums/structs**. They still get rkyv derives and NOTA codec methods — they just don't get signal-frame methods. Acceptable for the pilot because those types stay in-process today.

This is a meaningful win: the pilot proves schema-deep on the existing substrate, no fork required. The schema-next-extension question becomes a **future decision triggered by a specific need** (e.g. splitting SEMA into its own daemon → SemaCommand crosses a process boundary → wants signal-frame), not a precondition for this work. Two named paths-forward if/when that need arrives:

- **(A)** Extend `schema-next` to support N root enums.
- **(B)** Add a namespace-level marker macro `(Signal SemaCommand ...)` that opts the type into signal-frame emission.

The orchestrator's reading: option (B) is cleaner — keeps the schema language additive, lets each namespace type opt-in to wire framing where needed. But this is a decision for when the need is concrete, not now.

## Test family results — all 10 green

| # | Test | What it proves | Result |
|---|---|---|---|
| 1 | `lojix_next_schema_lowering_reaches_nested_macros` | schema-next macro registry covered nested struct/enum bodies | ok |
| 2 | `lojix_next_input_output_round_trip_rkyv` | wire frame symmetry | ok |
| 3 | `lojix_next_input_lowers_to_sema_command_exhaustively` | Executor covers every `Input` variant | ok |
| 4 | `lojix_next_sema_response_maps_back_to_output_exhaustively` | Executor covers every `SemaResponse` variant | ok |
| 5 | `lojix_next_actor_topology_includes_every_plane` | 9-plane manifest | ok |
| 6 | `lojix_next_trace_witnesses_full_pipeline` | pipeline reached every named plane | ok |
| 7 | `lojix_next_no_free_functions_outside_main_and_tests` | architectural-truth grep | ok |
| 8 | `lojix_next_no_zst_actors` | `mem::size_of` > 0 for every actor | ok |
| 9 | `lojix_next_build_only_pipeline_on_sandbox` | real daemon + CLI driving full pipeline end-to-end | ok |
| 10 | `lojix_next_activation_on_nspawn_sandbox` | Activator + ObservationFan witness `Activating Complete` + `Observed Complete` | ok |

Plus the flake checks (`build`, `test`, `fmt`, `clippy`, `schema-deep-build-script`, `actor-mailboxes-schema-emitted`, `binary-boundary-test`) all pass.

## What the pilot proves about the vision

The three concrete wins from `/35/1` §"What 'schema-deep' buys":

1. **One source of truth for every typed noun in the runtime.** ✓ Realised. 28 types in one `.schema` file, zero hand-written parallel mirrors.
2. **Migration is type-checked at the schema layer.** ½ Realised. schema-rust-next emits the types; the Rust compiler catches type mismatches when methods get out of sync. Full schema-diff → historical-projection automation is the next-slice work.
3. **Actor protocols are also typed.** ✓ Realised. `ActorRequest` and `ActorReply` are in the schema; the actor mailbox vocabulary is schema-derived even for in-process actors. Current Kameo message types (`Apply`, `DriveBuild`, `Dispatch`) wrap schema-emitted payloads; a future iteration could collapse to one `ActorRequest`-dispatch surface per actor.

## What would land in lojix proper if operator amalgamated

Eight concrete items the subagent listed; the orchestrator's compressed reading:

1. **`schema/lojix.schema` as source of truth.** Deletes the existing 3-place type-family drift (wire in `signal-lojix`, runtime in `lojix`, sema in another module).
2. **`Input::lower_to_sema_command` as the executor entry.** Replaces `RuntimeRoot::handle(RuntimeRequest)` match arm.
3. **`Store::apply(SemaCommand) -> SemaResponse` as single-writer surface.** Collapses `DeploymentLedgerActor` + `DeploymentActor`.
4. **The 9-actor topology.** Replaces existing 5-actor topology with denser plane separation (LojixRoot + dispatcher + auth + builder + copier + activator + gc_root + store + fan + trace).
5. **Trace witness pattern.** Existing lean lojix has no comparable typed trace infrastructure — gap closes.
6. **`ProcessToolchain` + `DaemonConfiguration` as schema-emitted records.** Replaces hand-authored equivalents.
7. **`no_free_functions` architectural test.** Catches the three free functions currently in the existing lean lojix's `src/runtime.rs` (`deployment_rejected`, `failure_text`, `unique_in_process_directory`) — those migrate to methods on owning types during amalgamation.

Lift estimate: ~3,200 new lines replace ~3,600 existing lines (net reduction). The contract spine moves from hand-authored to schema-derived. Operator-class work, well within `skills/double-implementation-strategy.md` "amalgamate best-of-prototypes onto main" pattern.

## What is NOT delivered (intentional next-slice work)

- Redb backing (Store is in-memory)
- Schema-diff / upgrade machinery
- Real criome socket (`CriomeBackedRequired` policy is defined but not wired)
- `owner-signal-lojix` ordinary signal contract (pilot ships only the working signal surface)
- Real `nspawn` boot in `nix flake check` (test 10 uses sandbox-mode marker `nspawn-sandbox-activate`; real activation needs root+cgroup, not available inside `nix-build`'s chroot)
- Vectors in `SemaResponse` (single-record-per-response per spirit-next precedent)

None of these block psyche review or the amalgamation conversation; they shape the next slice's pickup queue.

## Adjacent intent surfaced during the session

Two new Spirit records landed from other agents while this work was running:

- **905** (`[criomos lojix horizon]` Decision Maximum) — audit production CriomOS changes that have NOT been ported to the next lojix+horizon rewrite stack; create a report; use findings to guide the port.
- **908** (`[criomos lojix horizon]` Decision Maximum) — port high-confidence production CriomOS changes into the next lojix+horizon rewrite stack immediately where the correct change is clear; then test those builds.

These are a parallel arc on the EXISTING lean stack (`horizon-leaner-shape`), not the schema-deep pilot. They feed the lean stack's near-term cutover (the `/34` arc); they do not block or compete with the schema-deep pilot. **When operator amalgamation considers the schema-deep pilot, the changes 905/908 brings into the lean stack must also be carried forward** — the amalgamation target is whichever lojix shape will be production at promotion time. Right now that's the lean stack plus whatever 905/908 ports; the schema-deep pilot must rebase / absorb those when promoted.

## Five open psyche questions (unchanged from `/35/1`)

Restating because the subagent's success doesn't answer them — psyche decisions remain owed:

1. **Worktree on existing `lojix` (done) vs new repo `lojix-next` paralleling `spirit-next`?** Pilot landed on existing `lojix`/`schema-deep`. Easy to relocate if you'd rather have a separate repo (move worktree, update paths in `flake.nix`).
2. **Sandbox OS choice.** Pilot uses an in-process sandbox-mode toolchain (test 10's `nspawn-sandbox-activate` marker). Real `nspawn` activation needs flake-level plumbing that's pure operator work; the architectural shape is proven.
3. **Schema-next vector support.** Subagent navigated WITHOUT fork. Authorization (Spirit 883) remains in your hands for when the need is concrete; the orchestrator-preferred path-forward is option (B) namespace-level `(Signal X ...)` marker macro.
4. **/29 role-merge.** Stays deferred for this pilot — confirmed by no need to use it.
5. **Promotion criteria.** Proposed: (a) all 10 tests pass — ✓; (b) sandbox-OS witness — ✓ (in-process for now, real nspawn is pure plumbing); (c) "what would land in lojix proper" deliverable — ✓ (above + in `/35/2` §"What would land in lojix proper"). All three met. Awaiting your call to authorize operator amalgamation.

## Bottom line

The schema-deep pilot ships. The vision in `/35/1` proves out at the implementation level. Five psyche decisions await; the most load-bearing one is #5 (promotion authorization). The pilot was built without forking schema-next (a meaningful win for the substrate). Adjacent records 905/908 feed the lean stack and become amalgamation-time concerns. The pilot is parallel to the `/34` lean-lojix cutover arc — neither blocks the other.

## See also

- `0-frame-and-method.md` — orchestrator frame + subagent brief
- `1-vision-schema-deep-new-logics.md` — vision (what the subagent implemented against)
- `2-schema-deep-lojix-next-pilot.md` — subagent's implementation report (the full per-file accounting)
- `reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md` — parallel lean lojix MVP arc
- `~/wt/github.com/LiGoldragon/lojix/schema-deep/` — the pilot itself (commit `rnwxqrlzmrmm` on branch `schema-deep`, pushed)
- `~/wt/github.com/LiGoldragon/lojix/schema-deep/ARCHITECTURE.md` — per-repo ARCH
- `skills/double-implementation-strategy.md` — designer-pilot → operator-amalgamation discipline
