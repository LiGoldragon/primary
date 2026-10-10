# CriomOS Implementer Evidence — Re-home Guardian Prompt Config to meta-signal-spirit

## Task and scope

Rework the runtime source of the Spirit Guardian prompt so its configuration
flows through **meta-signal-spirit** (the owner-policy meta contract), per an
explicit psyche decision, replacing the prior `SPIRIT_GUARDIAN_PROMPT_DIR`
env-var override directory (jj `77410e79`). Same outcome: the acknowledged
strict-bar role is the active Guardian prompt, swappable without a full
rebuild+redeploy, with a sane fallback if unset; wire-coupled sections (reason
catalogue, NOTA verdict grammar) stay code-rendered. Implement, build, test,
commit. STOP before the lojix deploy. NOT deployed.

## What meta-signal-spirit is (investigation result)

`meta-signal-spirit` is the **MetaSignal owner-policy contract crate** for the
`spirit` daemon (sibling to `signal-spirit`, the ordinary public contract). It
carries owner-only operations the peer-callable working socket must not hold:
`Configure`, `Import`, `CollectRemovalCandidates`, `ObserveHead`,
`ObserveHeadObject`. It is schema-derived (`schema/meta-signal.schema` ->
`src/schema/meta_signal.rs` via `schema-rust`), wire-only (no runtime/SEMA).

It is a SUITABLE home, confirmed by direct source reading plus a scout map:

- The meta socket is served by the SAME daemon process / `Engine` / `Nexus` as
  the working socket. `Engine::configure` already receives `ConfigureRequest`
  and applies its targets to LIVE runtime state: `archive_database_target` ->
  `Store::set_archive_target`; `mirror_target` -> `MirrorShipper::configure`;
  `criome_gate_target` -> `CriomeGate::configure_socket` +
  `Nexus::configure_operation_authorizer`. The Guardian lives in that same
  `Nexus` (`guardian: Option<AgentGuardian>`), so `Engine::configure` can reach
  it the same way.
- `signal-spirit`'s `SpiritGuardianAgentConfiguration` carries socket / provider
  / model / timeout / max-tokens but NO prompt field, so threading the prompt
  through meta-signal-spirit needs NO signal-spirit wire change (avoids the
  cross-repo blast radius the psyche rejected).

Key property (matches every existing Configure target): Configure targets are
runtime policy applied in-process, NOT durable SEMA state. A restarted daemon
returns to defaults until an owner re-sends `Configure`. The Guardian prompt
target follows this exactly: a fresh daemon starts on the compiled-in
acknowledged strict-bar role; an owner hot-swaps it live via `Configure` with no
rebuild; on restart it falls back to the compiled-in role. This satisfies
"swappable without rebuild+redeploy, sane fallback if unset."

## How the prompt config now flows

1. Owner sends `meta-spirit "(Configure (Default None None (Some (Prompt [<role text>]))))"`
   over the owner-only meta socket (the `meta-spirit` CLI parses generic NOTA, so
   no CLI code change was needed).
2. `meta_signal_spirit::Input::Configure(ConfigureRequest{ .., selected_guardian_prompt_target })`
   routes to `Engine::configure`.
3. `Engine::configure` maps the target to a `GuardianPromptSource`
   (`Default` -> `compiled_in`, `Prompt(text)` -> `role_override(text)`) and calls
   `Nexus::set_guardian_prompt_source` -> `AgentGuardian::set_prompt_source`.
4. The next verdict renders the new role section; reason catalogue and verdict
   grammar stay enum-rendered, so the override cannot shift the wire vocabulary.
5. The receipt echoes the now-active target.

The env-dir mechanism (`SPIRIT_GUARDIAN_PROMPT_DIR`, `override_directory`,
`from_environment`, `with_override_directory`) is removed — no competing path.

## Affected repos and versions

- **meta-signal-spirit**: 0.4.0 -> **0.5.0** (minor: compatible wire addition).
  Pushed to `main` at **`92f2578d4ed76153ef41820a2bee98f655b0d883`**. Prior main
  (`98704a35`) is also kept on the `criome-auth-witness` bookmark.
  - Schema: added `GuardianPromptText String`, `GuardianPrompt { GuardianPromptText }`,
    `GuardianPromptTarget [Default (Prompt GuardianPrompt)]`,
    `SelectedGuardianPromptTarget (Optional GuardianPromptTarget)`; added the
    field to `ConfigureRequest` and `ConfigureReceipt` (mirror/criome pattern).
  - Regenerated `src/schema/meta_signal.rs`; updated `src/lib.rs` builders
    (`ConfigureRequest::new` / `ConfigureReceipt::new` gain the 4th
    `Option<GuardianPromptTarget>` arg, plus `guardian_prompt_target` accessors);
    updated `examples/canonical.nota`, `tests/round_trip.rs`, `tests/frame.rs`;
    fixed a stale `Input::HEADS` assertion (added `ObserveHeadObject`);
    documented the new target in `ARCHITECTURE.md`.
- **spirit**: stays at **0.20.0** (landed-only; the contract repin folds into the
  same unreleased minor as the prior strict-bar work). Bookmark
  `guardian-runtime-config-prompt` at **`098f6eff`**, two commits ahead of spirit
  `main@origin` (`43d6a069`): `77410e79` (strict-bar role + plumbing scaffold),
  then `098f6eff` (this re-home). NOT pushed (deploy stop point).
  - Changed: `Cargo.lock` (repin meta-signal-spirit 0.5.0 @ 92f2578d),
    `src/guardian_prompt.rs` (`GuardianPromptSource` = `Compiled | RoleOverride(String)`,
    drop env-dir + its tests, add role-override tests, `intent_guardian_system_prompt`
    made `pub(crate)`), `src/guardian.rs` (`from_contract` defaults to `compiled_in`,
    add `AgentGuardian::set_prompt_source` + diagnostic
    `intent_guardian_system_prompt`), `src/nexus.rs` (`set_guardian_prompt_source`,
    `guardian_intent_system_prompt`), `src/engine.rs` (apply target in `configure`;
    echo in receipt; `guardian_intent_system_prompt` accessor), `src/lib.rs`
    (gate `GuardianPromptSource` re-export under `agent-guardian`),
    `ARCHITECTURE.md`, and the 5 test files with `ConfigureRequest::new` call
    sites (+ new engine-level behavioral test in `tests/meta_configure.rs`).
  - **`src/guardian-prompts/role.md` is byte-identical to `77410e79`** (verified
    by empty `jj diff`): the acknowledged strict-bar role is preserved verbatim
    and remains the compiled-in default.

## Build + test evidence (commands and results)

meta-signal-spirit (at /git/github.com/LiGoldragon/meta-signal-spirit):
- `META_SIGNAL_SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo build --features nota-text` -> Finished (regenerated artifacts).
- `cargo build` (default, binary-only) -> Finished.
- `cargo test --features nota-text` -> round_trip 9/9, frame 1/1, doc 0/0 passed.
- `cargo test` (default) -> passed (dependency_boundary surface).
- `cargo clippy --features nota-text` -> clean.

spirit (at /home/li/primary/repos/spirit-guardian-config):
- `cargo build --features agent-guardian --lib` -> Finished.
- `cargo build --features agent-guardian,mirror-shipper --lib` -> Finished.
- `cargo build --features agent-guardian --bins` -> Finished.
- `cargo build --features agent-guardian,mirror-shipper --bin meta-spirit --bin spirit-daemon` -> Finished.
- `cargo test --features agent-guardian --lib` -> 11 passed, 0 failed. Includes
  new `role_override_swaps_the_role_section_without_rebuild`,
  `compiled_in_source_renders_exactly_the_baked_prompt`,
  `blank_role_override_falls_back_to_the_compiled_in_role`, and the preserved
  strict-bar markers in `assembled_system_prompt_carries_the_strict_bar_role`.
- `cargo test --features agent-guardian --test meta_configure` -> 4 passed, 1
  PRE-EXISTING failure (`configure_sets_archive_target_and_leaves_live_database_unchanged`).
  Includes new `meta_configure_guardian_prompt_target_swaps_and_restores_the_live_role` (PASS).
- `cargo test --features agent-guardian,mirror-shipper --test public_surface --test criome_gate_1of1 --test mirror_shipper` -> 1/1, 3/3, 2/2 passed.
- `cargo test --features agent-guardian --test dependency_surface` -> 3/3 passed.
- `cargo clippy --features agent-guardian --lib` and `--features agent-guardian,mirror-shipper --lib` -> clean.
- `cargo fmt --check` -> exit 0 (clean).

Pre-existing failure verified NOT mine: the one `meta_configure` failure
(`ReferentGuardianRejected(HarnessUnavailable)` where the test expects
`GuardianRejected`) reproduces IDENTICALLY on a pristine `77410e79` baseline
workspace (created with `jj workspace add --revision 77410e79`, run, then
forgotten/removed). It is the known referent-guardian-test-helper gap from the
prior evidence, in a working-write referent path my rework does not touch.

Nix flake check not run: `repos/` is untracked in the primary git tree, so Nix
cannot see the jj workspace flake source (same limitation the prior evidence
noted). The flake's named checks wrap the same `cargoTest` over the tests proven
above; the deploy agent should run `nix flake check` from a normal pushed
checkout.

## jj commit ids

- meta-signal-spirit: `92f2578d4ed76153ef41820a2bee98f655b0d883` (change
  `mqlpyzwk`), bookmark `main`, **PUSHED** to origin.
- spirit: `098f6eff` (change `mwlrxrtx`), bookmark
  `guardian-runtime-config-prompt`, on top of `77410e79`. **NOT pushed**.

## EXACT deploy command sequence for the follow-up agent (do NOT run in this task)

The Spirit daemon is a home-manager systemd USER service in CriomOS-home
(`modules/home/profiles/min/spirit.nix`, builds `inputs.spirit`). This is a
Home/environment deploy through the CriomOS-home `spirit` input.

1. meta-signal-spirit is ALREADY pushed (`92f2578d`). Nothing to push there.

2. Push + integrate the spirit change to spirit main. From
   `/home/li/primary/repos/spirit-guardian-config`:
   - Confirm spirit `main@origin` has not moved past `43d6a069`; if it has, rebase
     `guardian-runtime-config-prompt` onto the new main first.
   - `jj bookmark set main -r guardian-runtime-config-prompt` then
     `jj git push --bookmark main`
     (or push the feature bookmark and integrate per main-feature-integration).
   - Record the resulting pushed spirit commit rev as `<spirit-rev>`.
   - NOTE: spirit's `Cargo.lock` already pins meta-signal-spirit to the pushed
     `92f2578d`, so the closure resolves from remotes (no path inputs).

3. Bump the CriomOS-home `spirit` input to `<spirit-rev>`:
   `cd /home/li/primary/repos/CriomOS-home && nix flake lock --update-input spirit`
   (or pin the `spirit` input rev to `<spirit-rev>` and relock). Commit + push
   CriomOS-home. Capture the pushed CriomOS-home rev as `<criomos-home-flake-ref>`.
   Run `nix flake check` from that pushed checkout to exercise the named checks.

4. CONFIRM the live target before deploying (name cluster, node, user, kind,
   mode, builder, rollback, evidence). Query the live node first:
   `lojix "(Query (ByNode (<cluster> <node> None)))"`
   Resolve the actual cluster/node/user running this home profile from the live
   registry / CriomOS-home horizon.users — do not guess.

5. Submit the Home deploy from the pinned CriomOS-home rev (fill confirmed
   cluster/node/user/builder). Use `Build` first to prove the closure, then
   `Activate`:
   `meta-lojix "(Deploy (Home (<cluster> <node> <user> <proposal-source> <criomos-home-flake-ref> Build None [])))"`
   `meta-lojix "(Deploy (Home (<cluster> <node> <user> <proposal-source> <criomos-home-flake-ref> Activate None [])))"`
   A `(Deployed ...)` reply does not prove activation.

6. Activation checks:
   - `lojix "(Query (ByNode (<cluster> <node> None)))"` until the new closure is current.
   - On host: `systemctl --user status spirit-daemon` active; daemon binary
     resolves to the 0.20.0 package.
   - Verify the compiled-in strict-bar role is active by default (a clear
     standing directive accepts; a matter candidate is refused).
   - Verify the live hot-swap: send
     `meta-spirit "(Configure (Default None None (Some (Prompt [<new role text>]))))"`
     then confirm the guardian's behavior reflects the new role with NO redeploy;
     send `(Configure (Default None None (Some Default)))` to restore the
     compiled-in role. (Host-side checks need an operator on the live node.)

## EXACT rollback path

The deployed identity is the CriomOS-home `spirit` input pin.

- Prior deployed `spirit` rev (0.18.1): `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f`
  (from the prior evidence; confirm against the live CriomOS-home flake.lock before
  relying on it).
- In `/home/li/primary/repos/CriomOS-home`: revert the `spirit` input rev in
  `flake.lock` back to that rev (revert the bump commit, or pin + relock),
  commit + push; capture `<criomos-home-rollback-ref>`.
- Re-deploy the home from the rollback rev:
  `meta-lojix "(Deploy (Home (<cluster> <node> <user> <proposal-source> <criomos-home-rollback-ref> Activate None [])))"`
- Verify with `lojix "(Query (ByNode (<cluster> <node> None)))"` and
  `systemctl --user status spirit-daemon`.
- Fast in-session fallback with NO redeploy: because the prompt override is
  runtime policy, an owner can send
  `meta-spirit "(Configure (Default None None (Some Default)))"` to restore the
  compiled-in strict-bar role on the running daemon, or simply restart the daemon
  (it starts Compiled). The durable rollback is still the input-rev revert above.
- meta-signal-spirit rollback (only if the contract itself must be reverted):
  prior contract main is `98704a35` (v0.4.0), preserved on `criome-auth-witness`;
  reverting spirit's lock to that rev requires also reverting the spirit change,
  so treat the spirit `<spirit-rev>` revert as the unit of rollback.

## Blockers / psyche decisions

- meta-signal-spirit IS a suitable home (confirmed): it reaches the same daemon/
  engine/nexus that owns the Guardian, and needs no signal-spirit wire change.
  No blocker; no improvisation of an alternate mechanism.
- DESIGN CHOICE (flag, reversible): the override is scoped to the Guardian ROLE
  section (one prompt string), not all 7 prose sections. This keeps the contract
  minimal and confines the swappable surface to the psyche-facing prose while the
  wire-coupled sections stay code-rendered. If the psyche wants per-section
  overrides through Configure, that is a contract extension (more
  `GuardianPromptTarget` payload) — a separate decision.
- PERSISTENCE (flag): like every existing Configure target, the prompt override
  is in-process runtime policy, lost on restart (fallback = compiled-in
  strict-bar role). If the psyche wants the override to survive restart, that
  requires NEW durable persistence for Configure targets (none exists today for
  archive/mirror/criome either) — a separate, larger change.
- COMPOSITION (carried from prior work, still true): the strict-bar text is the
  ROLE section, not the entire system prompt; code still appends record/justification/
  ladder/checklist + enum-rendered reason catalogue + verdict grammar + few-shot.
- Pre-existing referent-guardian-test-helper gap (unrelated) should be tracked/
  fixed before a clean `nix flake check`.
- Not pushed (spirit) and not deployed, per the stop point.
