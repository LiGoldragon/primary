# G6 Flow: Codex main-flow bundle in the first block (Flow 0.8.1)

This is task G6 of `flows/38de5b/reports/audit-flow.md`, plus the remote-control name item from G4. An Opus subflow of 38de5b did it on 2026-09-25.

- Repository: github.com/LiGoldragon/flow
- Branch `g6-38de5b`, cut from main 470dcc4 (0.8.0).
- Revision: 8f8a71a4d696d7fe0f85256ac2a20fb427f1e350 "Flow 0.8.1: Codex main-flow bundle at the top of the first block"
- `git ls-remote` shows both `main` and `g6-38de5b` at 8f8a71a. Main was fast-forwarded from 470dcc4. The g8-g9 branch had not landed on main, so no rebase was needed.
- Tests before, on 470dcc4: 74 passed. Tests after: 77 passed and 0 failed.
- `cargo fmt --check` is clean. `cargo clippy --all-targets` reports no warnings. One warning was already there before this change (`push_str("\n")` in composition.rs), and it is fixed.
- Files: `composition.rs`, `codex.rs` (a test only) and `herdr/launch.rs` (a test only). Also README.md, UPGRADES.md, Cargo.toml, Cargo.lock and flake.nix. None of the g8-g9 paths (`lib.rs`, `store.rs`) were touched.

## Mechanism: first block, not developer_instructions

The `codex-harness` skill describes `developer_instructions` as a developer-role message. It is sent beside the base instructions as a message of its own, and it is config. The ruling (38de5b log, 15:50Z; `receipts/codex-start-answer.md`) says something else: keep the stock base instructions and put the main-flow-mode text "at the top of the main Flow's first block", so that Codex children keep the stock base. A developer message is not the first block. And because it is set through config or the thread, it carries the same risk of reaching children that made the ruling set aside `model_instructions_file`.

So the bundle goes in the first block. `LaunchComposer` reads the bundle for Codex launches only. The bytes must be non-empty UTF-8, trimmed. Otherwise the result is `InvalidProfileField("system_prompt_bundle_file")`. The bundle text opens the body, followed by a blank line, then the `$main-flow` / `$name` lines. The line `System prompt: read <bundle>` is removed. Claude is unchanged, and still gets `--system-prompt-file`.

- In the `turn/start` input array, the typed skill items still come before the one text item. That text item is the first text block, and it begins with the bundle. Each skill item expands ahead of the prompt's words (see the codex-harness skill), so in context the skill bodies come before the bundle text.
- The bundle text is part of the hashed body. `prompt_sha256` covers it, and the receipt observer checks it as before.

## Remote-control name

The Flow ID is only known after the claim. `observe_native_binding` claims it from the native session id, and that id exists only after `agent start`. The `--remote-control` flag has to be passed at that start, so the Flow ID cannot be used for it. As the brief allowed, the name is built from the launch request ID's short form instead: `flow-` followed by the first 8 hex digits of SHA-256("flow-remote-control-v1\0" + launch request ID). Eight digits were chosen so the name cannot be mistaken for a 6-digit Flow ID. The request ID itself never enters the prompt, and the prompt's "Remote control:" line carries the same name. G3's hash-free test (no hex run of 16 or more characters) still passes.

## Tests added or changed

- `codex_first_block_opens_with_the_bundle_text_and_no_read_line` (composition)
- `codex_main_flow_first_text_block_opens_with_the_system_prompt_bundle` (codex.rs). It composes a real launch, builds the `turn/start` params, and checks that the first text item starts with the bundle and then `$main-flow\n$spirit\n\n`, with no read line and no bundle path.
- `codex_launch_refuses_an_empty_or_non_utf8_bundle`
- `claude_launch_records_its_remote_control_flag`. It now checks the `flow-<8 hex>` shape, that two request IDs give different names, and that the role does not change the name.
- The Codex prompt fixture and the Claude agent-start fixture were updated. `composed_prompt_carries_no_hash_request_id_or_source_text` is unchanged and passes.

## Version

The version went from 0.8.0 to 0.8.1. The rule, from the versioning skill: a public behaviour change updates the version surface. This one changes the Codex prompt and the Claude remote-control name. It changes neither wire nor storage. An attempt journaled by 0.8.0 is observed from its stored intent and is never recomposed (`lib.rs` Start, PromptAmbiguous path). That makes this a pre-1.0 patch. UPGRADES.md has a 0.8.1 entry.

## Not witnessed, and open

- No live Codex Start was run. A rollout showing the bundle at the top of the first user turn is still unwitnessed. The live service is not on 0.8.x.
- `nix flake check` was not run, because this host does not build locally.
- The remote-control name is unique per launch request, but it is not the Flow ID. G4's native title, set after the claim, is still where the Flow ID can be shown.
- Bundle text written by a caller may contain hex. The composer adds none.
