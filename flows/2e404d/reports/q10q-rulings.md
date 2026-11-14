# q10q: the four rulings built on ethos27-896bac

All four rulings are built, gated and proven. Nothing is merged, deployed or switched, and every main is where it was. The evidence is in `/home/li/primary/flows/2e404d/q10q/`.

## Heads (branch ethos27-896bac, each pushed, each a fast-forward of the previous head)

| repo | was | now | main (unchanged) |
|---|---|---|---|
| signal-curriculum-nexus | 3e8b5b9 | 4358aa1 | none |
| build-base | 65a94e1 | 9706bad | 8aa29e1 |
| Curriculum | f3117a1 | 1b6c454 | e3ffb31 |
| flow | a50f0f6 | 967f2f5 | 40104be |
| curriculum-deploy | 16233a2 | 832bde7 | 380061a |

The landing order is unchanged: build-base, then signal-curriculum-nexus, then Curriculum, then flow and curriculum-deploy. curriculum-deploy now pins Curriculum 1b6c454 as a crate, so it lands after Curriculum.

## Gates (prometheus, nix-fast-build --remote, against the pushed revisions)

Every gate exits 0. The logs are in `gates/`, summarised in `gates/exits.txt`. The `-full` logs list each check without `--skip-cached`.

- **signal-curriculum-nexus 4358aa1:** exit 0. Passes crate-versions, crate-features, cargo-nix, fmt, doc, test-default, the member check and default.
- **build-base 9706bad:** exit 0, all four of its own checks.
- **Curriculum 1b6c454:** exit 0. Passes crate-versions, crate-features, cargo-nix, curriculum (default and datom) and default. The new `refresh::tests` pass.
- **flow 967f2f5:** exit 0, all 19 checks, curriculum-cargo-nix among them. 931 tests pass; counted the same way, the a50f0f6 gate log also gives 931.
- **curriculum-deploy 832bde7:** exit 0. Passes fmt, build, clippy, test and external-data.
- **Negative test** (`gates/negative-stale-emission.log`): a deliberately stale `src/emission.rs` fails Curriculum's build with "src/emission.rs is stale; regenerate it from emission.ethos".

## Ruling 1: the refresh call is an Emission

- `Curriculum/emission.ethos` is the sketch byte for byte; Check accepted it without renaming anything. It generates `src/emission.rs`, and build.rs now checks it fresh alongside `generated.rs` and `memory.rs`.
- The registry issues the refresh with `refresh_program.emit(&ProcessLauncher)`:
  - `src/refresh.rs` holds `impl Emittable<ProcessLauncher> for RefreshProgram`, which runs the program as a child process.
  - The registry acts on the `RefreshOutcome`: `Refreshed` admits the sources; `Failed` and `Unstarted(e)` refuse with the same messages as before.
- The program path is still read from `CURRICULUM_CONTEXT_REFRESH_PROGRAM`. It is now held as `RefreshProgram(String)`, so a path that is not UTF-8 is refused at start with "CURRICULUM_CONTEXT_REFRESH_PROGRAM is not UTF-8". That is the one new refusal.
- The generated `Emission` and `Outcome` enums are compiled but nothing calls them. ethos-zero 27 generates no dispatch over `Emission`, and its README has the consumer implement `Emittable` for the carried type, which is what runs.

## Ruling 2: ComposeRole is the one renderer

- Generate and Check now get every role packet from the Curriculum Nexus's ComposeRole, through signal-curriculum-nexus:
  - `role_projection::composed` is the one place a packet's text is made, for ProjectRoles and Generate alike.
  - The packet assembly from the skill sources is removed (`roles::packet`, `module_body`, the Pi skill target, `SkillCatalog::named`). The skill sources now serve only the skills.
- **Decision:** Generate needs to know where the Nexus is. `Generate`, `Check` and `Visualize` take a fourth string, the Nexus socket, named explicitly as ProjectRoles names it:

  ```
  Generate.{ «/curriculum» [ … ] «/workspace» «/run/user/1001/curriculum/curriculum.sock» }
  ```

  - This changes curriculum-deploy's request text. Nothing in CriomOS or CriomOS-home invokes Generate; it is run by hand.
  - Visualize counts roles without asking the Nexus.
- The tests answer ComposeRole from a stand-in Curriculum. It binds its socket before the runtime starts, so nothing waits for readiness.
- **Packet proof** (`composition/runs/deploy-compare.txt`). Old Generate is 16233a2's binary, rendering from the sources. New Generate is 832bde7 against the new Curriculum Nexus. Both run over the live belief mains and the same roles.datom:
  - **P1, old vs new packets:** 0 equal; 31 differ only in leading and trailing whitespace of the description and of each module body; 0 differ otherwise.
  - The difference itself is shown in `composition/runs/packet-whitespace.diff`, a unified diff with `$` marking each line end. An example:
    - `description: "The approach is known. …"` becomes `description: "\nThe approach is known. …\n"`.
    - A blank line follows each `<!-- module: … -->` and precedes each `<!-- end-module: … -->`.
  - **P2, new Generate vs new ProjectRoles:** 31 of 31 byte-equal.
  - **P3, skills and role inventory, old vs new:** 128 of 128 equal in each of `.agents`, `.claude` and `.opencode`, and the inventory is equal.
  - New Generate reports `Generated.{ 128 31 }`, Check `Checked.{ 128 31 }`, ProjectRoles `RolesProjected.{ 31 }`.

## Ruling 3: the roles file format comes from Curriculum

- **Choice: a crate dependency on Curriculum.** curriculum-deploy depends on `curriculum` (git, rev 1b6c454, `default-features = false`, `features = ["datom"]`) and uses `curriculum::generated::{Roles, RolesDocument}`.
  - The format stays where Curriculum's `curriculum.ethos` declares it; nothing moves.
  - `RoleDefinition`, `Roles` and `RolesDocument` are gone from `curriculum-deploy.ethos` and its generated Rust. Its imports from the contract shrink to `RoleSelection` and `Surface`.
- **Cost:** curriculum-deploy's Cargo.lock now carries Curriculum's dependency graph (nexus, tokio and the rest, 278 lines).
  - The lock was resolved by `cargo metadata` on prometheus, because local cargo is disabled.
  - curriculum-deploy builds with crane, not on build-base, so this edge needs no build-base set.
- Moving the format into signal-curriculum-nexus was the alternative. I did not take it, because that would put a file format that is not on the wire into the wire contract.

## Ruling 4: the renames

- `ResolvedSkills` is now `SkillsResolved`, and `ResolvedSources` is now `SourcesResolved`:
  - in the contract (ethos, generated Rust, tests, UPGRADES);
  - in Curriculum (`service.rs`);
  - in flow (`context.rs`);
  - in curriculum-deploy (its pin only; it never named them).
- The contract stays at 0.1.0, since it was never released. build-base's set moved 0.1.0 from 3e8b5b9 to 4358aa1, with feature sets unchanged.
- Cargo.lock, Cargo.nix and crate-hashes.json were regenerated with build-base 9706bad's crate2nix in Curriculum and flow, and their `base` lock moved to 9706bad.
- **rkyv bytes unchanged, confirmed three ways:**
  - The contract's `tests/published.rs` decodes the replies recorded from e3ffb31 as `SkillsResolved` and `SourcesResolved`.
  - In the proof, all five inputs' frames are byte-equal between the live and new binaries (F1).
  - The only printed difference is the tag (F2: "rest equal: yes" for both).

## Composition proof (live belief mains)

The beliefs are psyche fdd8775, mind 573223d and field a515b80, which are today's origin mains. The new binary (Curriculum 1b6c454, datom, built by build-base `binaries`) was compared with the running one (b8rj8j4w); the results are in `composition/runs/compose-compare.txt`:

- **Permaflows:** 40, with 985 module positions. 0 differences in printed text, decoded results, Output frames or Input frames, in every client and Nexus pairing (A–E).
- **Roles:** 31 roles, RoleComposed 31 of 31 for each client. 0 differences in frames, printed text or stderr (R1–R4).
- **The rename:** shows only in ResolveSkills and ResolveSources printed text, as the tag (F2).
- **Nexus logs:** empty in every run.

The harness is in `composition/harness/` (`proof-2e404d.sh` drives it), and it ran in `/tmp/2e404d-q10q` on prometheus.

## Not done, or for Fable

- **A third renderer remains.** Curriculum keeps its own Claude packet renderer, `claude_agent.rs` (`curriculum --claude-agent-markdown`), which quotes the description as YAML. CriomOS-home's `install-curriculum-claude-agents` uses it. Ruling 2 named curriculum-deploy's renderer, so I left this one. Should it give way to the one renderer too?
- **The gate tests Generate against a stand-in Nexus only.** curriculum-deploy's external-data check now runs Generate against the stand-in Curriculum rather than a real Nexus. The Nexus publishes no readiness event, and a real one would need a wait for its socket. The end-to-end run over the real Nexus is the packet proof above.
