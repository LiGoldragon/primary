# CriomOS Implementer Evidence — Spirit Guardian Runtime-Config Prompt

## Task and scope

Move the Spirit Guardian's prompt from compiled-in to runtime config so prompts
swap without rebuild + redeploy, and set the active prompt to the
psyche-acknowledged strict-bar role verbatim. Implement, build, test, commit.
STOP before the live lojix deploy. This is a CriomOS component change
(host-safety discipline applied).

## Workspace and coordination

- The live `spirit` checkout (`/home/li/primary/repos/spirit`) is dirty with
  unrelated in-flight criome-authorization work and is on bookmark
  `criome-authorization-push`. Per workspace rule, I did NOT share it.
- Worked in an isolated jj workspace from clean `main`:
  `/home/li/primary/repos/spirit-guardian-config` (created with
  `jj workspace add --revision main`).
- Orchestrate lane claimed and released: `criomos-implementer` with
  `(Path /home/li/primary/repos/spirit-guardian-config)`.
- Disposition bead filed: `primary-xe2y` (labels feature-branch, worktree).

## Version state (landed vs deployed) — important

- `spirit` repo `main` is already at **0.19.0** (committed, not working-copy
  only). The 0.18.1 the brief names is the **deployed pin**, not repo main.
- DEPLOYED spirit = **0.18.1**, pinned in
  `/home/li/primary/repos/CriomOS-home/flake.lock` as the `spirit` input rev
  `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f`.
- This change bumps from current main 0.19.0 to **0.20.0** (minor: new public
  surface + new runtime config knob + behavior change). Landed only, NOT
  deployed.

## Config surface added

Design choice: keep the change inside the `spirit` component (no `signal-spirit`
contract change), because the brief's load-bearing requirement is "swap and test
WITHOUT rebuild + redeploy." A contract-config (rkyv) field would still require
regenerating the `*.config.rkyv` and re-deploying it. The architecture already
keeps the prompt prose in standalone section files deliberately separate from
code; this change makes those sections runtime-overridable.

Mechanism (all in `spirit`):

- New `GuardianPromptSource` (`src/guardian_prompt.rs`, re-exported from
  `src/lib.rs`): resolves each prose section either from a runtime override
  directory or the compiled-in `include_str!` default. Reads each section FRESH
  per prompt render, so editing a file under the directory swaps the live
  guardian prompt with no rebuild and no regenerated config.
- New `GuardianPromptSection` enum: the typed contact point binding each
  section's runtime filename to its compiled-in default (no flag soup; override
  is the normal lookup, compiled-in is the absent-file case).
- Override directory env var: `SPIRIT_GUARDIAN_PROMPT_DIR`
  (`GuardianPromptSource::PROMPT_DIRECTORY_VARIABLE`), mirroring the crate's
  existing `SPIRIT_SOCKET` / `SPIRIT_META_SOCKET` deploy-set path convention.
  Format: a directory containing any of `role.md`, `referent.md`,
  `record-shape.md`, `justification-shape.md`, `burden-ladder.md`,
  `checklist.md`, `few-shot.md` (same names as `src/guardian-prompts/`).
- Sane-if-absent: absent variable, missing dir, missing file, unreadable file,
  or blank file all fall back PER SECTION to the compiled-in default. A daemon
  with no variable set behaves exactly as the baked prompt. Partial overlay
  (e.g. only `role.md`) is first-class.
- Wire-format safety preserved: only prose sections are overridable. The closed
  rejection-reason catalogue and the NOTA verdict grammar stay enum-rendered in
  code, so the prompt can never drift from the wire type the daemon parses.
- Daemon load path: `AgentGuardianConfiguration` gains a `prompt_source` field;
  `from_contract` resolves it via `GuardianPromptSource::from_environment()` at
  config load; `new()` defaults to compiled-in with a public
  `with_prompt_source` builder. `AgentGuardian::prompt_builder` passes the
  source into `GuardianPromptBuilder`.

## Active prompt set (verbatim)

`src/guardian-prompts/role.md` replaced with the psyche-acknowledged strict-bar
role verbatim (the "You are the Guardian of Spirit / THE ONE TEST / THE
ASYMMETRY / ... / Default to refusal." text). It becomes the compiled-in default
role and therefore the active role after a normal build, swappable at runtime via
the override directory.

Composition note (flag for psyche): the strict-bar prompt is placed as the role
section. Code still appends the other sections (record-shape, justification,
burden-ladder, checklist), the enum-rendered reason catalogue, the NOTA verdict
grammar, and the few-shot — these carry the wire-format discipline and the
detailed gates the strict-bar prose summarizes. Replacing the WHOLE assembled
prompt with only the strict-bar text would drop the verdict grammar and reason
atoms the daemon parses, so role-section placement is the faithful minimal
placement. If the psyche intends the strict-bar text to be the ENTIRE system
prompt, that is a separate decision.

## Changed files

- `src/guardian_prompt.rs` — GuardianPromptSection, GuardianPromptSource,
  instance-method prompt assembly reading through the source, new tests.
- `src/guardian.rs` — prompt_source field, from_contract env resolution,
  with_prompt_source builder, prompt_builder wiring.
- `src/lib.rs` — re-export GuardianPromptSource.
- `src/guardian-prompts/role.md` — verbatim strict-bar role.
- `ARCHITECTURE.md` — guardian prompts section updated to describe runtime
  override + strict-bar role (runtime-visible doc surface).
- `Cargo.toml` — version 0.19.0 -> 0.20.0.
- `Cargo.lock` — spirit package version bump only.

## Build + test evidence (commands and results)

- `cargo build --features agent-guardian --lib` -> Finished (clean).
- `cargo build --features agent-guardian --bins` -> Finished (clean).
- `cargo test --features agent-guardian --lib` -> 11 passed, 0 failed. Includes
  new: runtime_override_directory_swaps_the_role_section_without_rebuild,
  absent_override_directory_falls_back_to_the_compiled_in_prompt,
  blank_override_file_falls_back_to_the_compiled_in_section,
  assembled_system_prompt_carries_the_strict_bar_role.
- `cargo test --features agent-guardian --test public_surface --test
  daemon_command --test dependency_surface` -> all passed (1, 3, 3).
- `cargo clippy --features agent-guardian --lib` -> clean (no warnings).
- `cargo fmt` -> applied (let-chain formatting in guardian_prompt.rs).

Pre-existing failures (NOT caused by this change, verified against pristine
`main`): `tests/runtime_triad.rs` 57 passed / 7 failed and
`tests/meta_configure.rs` configure test fail identically on clean main
(43d6a069) with no edits. They are a referent-guardian test-helper gap
(auto-registered referents need a referent guardian the helper does not set);
out of this task's scope.

Nix flake check note: `nix flake check` could not run on this jj workspace
because `repos/` is untracked in the parent primary git tree, so Nix cannot see
the worktree flake source. The flake's named checks wrap `craneLib.cargoTest`
over the same tests proven above. The follow-up deploy agent should run
`nix flake check` from a normal `spirit` checkout of the pushed bookmark.

## Commit

- jj commit id: **77410e79** (change `mzkyynzp`), message
  "spirit: 0.20.0 — runtime-overridable guardian prompt + strict-bar role".
- Bookmark: `guardian-runtime-config-prompt` -> 77410e79, one commit ahead of
  `main` (43d6a069). NOT pushed (brief stops before deploy).

## EXACT deploy commands for the follow-up agent (do NOT run in this task)

The Spirit daemon is a home-manager systemd USER service in CriomOS-home
(`modules/home/profiles/min/spirit.nix`, builds `inputs.spirit`). So this is a
Home/environment deploy through the CriomOS-home `spirit` input.

1. Push the landed change and integrate to spirit main (jj escape hatch as
   needed):
   - From `/home/li/primary/repos/spirit-guardian-config`:
     `jj bookmark set main -r guardian-runtime-config-prompt` (fast-forward main;
     confirm main has not moved first) then
     `jj git push --bookmark main`
     OR push the feature bookmark and integrate per main-feature-integration.
   - Record the resulting pushed spirit commit rev (call it
     `<spirit-0.20.0-rev>`).

2. Bump the CriomOS-home `spirit` input to that rev:
   `cd /home/li/primary/repos/CriomOS-home && nix flake lock --update-input spirit`
   (or pin exactly: set the `spirit` input rev to `<spirit-0.20.0-rev>` and
   relock). Commit + push CriomOS-home. Capture the pushed CriomOS-home rev as
   `<criomos-home-flake-ref>`.

3. CONFIRM the live target before deploying (operating-system-operations: name
   cluster, node, user, kind, mode, builder, rollback, evidence). Query the live
   node first:
   `lojix "(Query (ByNode (<cluster> <node> None)))"`
   (The `(criome prometheus ...)` guess returned empty; the follow-up agent must
   resolve the actual cluster/node/user that runs this home profile from the
   live registry / CriomOS-home horizon.users — do not guess.)

4. Submit the Home deploy from the pinned CriomOS-home rev (template — fill the
   confirmed cluster/node/user/builder):
   `meta-lojix "(Deploy (Home (<cluster> <node> <user> <proposal-source> <criomos-home-flake-ref> Activate None [])))"`
   Use `Build` first to prove the closure, then `Activate`. A `(Deployed ...)`
   reply does not prove activation.

5. Activation checks:
   - `lojix "(Query (ByNode (<cluster> <node> None)))"` until the new closure is
     current.
   - On the host: `systemctl --user status spirit-daemon` is active; confirm the
     daemon binary path resolves to the 0.20.0 package; submit a known
     standing-directive vs a known matter candidate through the Spirit CLI and
     confirm the strict-bar verdicts (Accept for a clear standing directive,
     Matter/NonIntent refusal otherwise). These host-side checks need an
     operator on the live node.

Optional future hot-swap (no redeploy): once 0.20.0 is live, set
`SPIRIT_GUARDIAN_PROMPT_DIR` on the `spirit-daemon` user unit pointing at a
writable directory of section files; thereafter editing those files swaps the
guardian prompt with no rebuild. Establishing the env on the unit is a one-time
home redeploy; this is the mechanism, not required for the strict-bar prompt
(which ships as the compiled-in default in 0.20.0).

## EXACT rollback path to restore 0.18.1

The deployed identity is the CriomOS-home `spirit` input pin. Rollback = restore
the prior pin and re-activate:

- Prior deployed `spirit` rev (0.18.1):
  `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f`.
- In `/home/li/primary/repos/CriomOS-home`: revert the `spirit` input rev in
  `flake.lock` back to `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f` (revert the
  flake.lock bump commit, or pin the input to that rev and relock), commit +
  push; capture the rollback CriomOS-home rev `<criomos-home-rollback-ref>`.
- Re-deploy the home from that pinned rev:
  `meta-lojix "(Deploy (Home (<cluster> <node> <user> <proposal-source> <criomos-home-rollback-ref> Activate None [])))"`
- Verify with `lojix "(Query (ByNode (<cluster> <node> None)))"` and
  `systemctl --user status spirit-daemon`.
- Fast generation-level fallback on the host (no rebuild): activate the prior
  home-manager generation that pinned 0.18.1 via the host's home-manager
  generation switch; the durable rollback is still the input-rev revert above.

## Blockers / psyche decisions

- DESIGN FORK (psyche/reviewer): runtime prompt via daemon env-resolved
  directory (chosen, in-component, zero cross-repo bump, meets
  swap-without-redeploy) vs the convention-pure component-triad path of adding a
  typed `guardian_prompt` field to the `signal-spirit` contract (larger blast
  radius: signal-spirit 0.9.0 bump, relock, writer + Nix updates, and still a
  config regeneration to set the path). Flagged for a decision; the chosen
  design is reversible.
- COMPOSITION (psyche): strict-bar text placed as the role section, not as the
  entire system prompt (see Active prompt set). Confirm intent.
- ARCHITECTURE doctrine: the prior "daemon stays a single self-contained binary,
  prompt baked at compile time" property is intentionally relaxed to
  "self-contained default, runtime-overridable." ARCHITECTURE.md updated to say
  so; confirm this doctrine relaxation is acceptable.
- Pre-existing test failures on spirit main (referent-guardian helper gap) are
  unrelated but should be tracked/fixed before a clean `nix flake check`.
- Not pushed and not deployed, per the stop point.
