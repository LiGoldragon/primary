# G2 + G3 Flow: one lean first prompt (Flow 0.8.0)

These are tasks G2 and G3 of `flows/38de5b/reports/audit-flow.md`. An Opus subflow of 38de5b did them on 2026-09-25.

- Repository: github.com/LiGoldragon/flow
- Branch `g2-g3-38de5b`. It was rebased onto main 972d8d2, which includes I1/G10.
- Revision: 470dcc4721f9efbc4a60b44c0f8a11839e66112a "Flow 0.8.0: one lean first prompt"
- `git ls-remote` shows both `main` and `g2-g3-38de5b` at 470dcc4. Main was fast-forwarded from 972d8d2.
- Tests before, on 4671f8d: 65 passed. Main 972d8d2 had 69.
- Tests after: 74 passed and 0 failed. The known flaky test `marker_rendered_in_a_different_pane_keeps_the_flow_pending` passed in both runs.
- `cargo fmt --check` is clean. The fmt drift in composition.rs and launch.rs is fixed.
- `nix flake check` was not run to completion. This host refuses local builds (max-jobs = 0), and no remote builder took the derivations.
- Version: 0.7.1 changed to 0.8.0 in Cargo.toml, Cargo.lock and flake.nix. The rule, from the versioning skill: a public behaviour change updates the version surface. Here the prompt a launched Flow receives and the receipt protocol both changed, and a 0.7 journaled attempt cannot be promoted by 0.8. That makes it a pre-1.0 minor bump. UPGRADES.md has a 0.8.0 entry.
- Files: `composition.rs`, `herdr/launch.rs` and `codex.rs` (a test only), plus the receipt marker in one `lib.rs` test fixture. It also touched README.md, UPGRADES.md, Cargo.toml, Cargo.lock and flake.nix.

## G2: one prompt

- `start_native_harness` no longer passes a positional startup block. That block was a first user turn of its own. For Codex it also made `require_empty_bound_thread` refuse the later `turn/start`, since the thread already had a turn.
- Claude receives one write through `herdr agent prompt`. The block opens with `/<first skill> `, and the rest of the body is that command's argument. Claude reads a command only as the first token, so any other skills are listed in the body under "Then load through the Skill tool, in this order: …".
- The Claude observer now also accepts what the harness records for a command. I read these shapes from real transcripts under `~/.claude/projects`:
  - a user row carrying `<command-message>` / `<command-name>/x` / `<command-args>`;
  - an `isMeta` + `turnCompanion` expansion row with no `sourceToolUseID`, beginning with "Base directory for this skill:" and ending with `ARGUMENTS: <args>`.
  - The observer rebuilds `/name args` from those rows, verifies the body hash, requires the command to be the first selected skill, and checks the expansion prefix. After that it requires Skill-tool evidence for the remaining skills, as before.
- Codex receives one `turn/start`. It carries the typed skill items plus one text that opens with `$name` lines. `$main-flow` is added at the top when the profile omits it, which keeps what the old positional block provided. The text also carries "System prompt: read <bundle>", because Codex gets no system-prompt file.
- Tests that assert one prompt per harness:
  - the Claude start call ends at `--effort high`;
  - the Codex start ends at `model_reasoning_effort=high`, with no `$` and no `agent prompt`;
  - `claude_one_command_prompt_reaches_its_receipt` finds exactly one prompt-bearing Herdr call, and the one-command transcript reaches Observed;
  - `bound_first_turn_is_one_text_beside_its_typed_skills`.

## G3: lean, no hashes

- The body drops the `Launch request:` line, the inlined source text and the sha256 footer. Sources are listed by canonical absolute path, and only after their bytes have been checked against the profile hash.
- The footer is fixed: "When every skill has loaded, reply once with exactly this line and nothing else:" followed by the line `FLOW_LAUNCH_RECEIPT_V2`.
- The receipt is bound to the launch by native session, transcript cursor and the authenticated first turn. `prompt_sha256` and `receipt_sha256` stay in the store and the observer.
- The remote-control record line is still present, now hash-free. The name comes from the role, for example `--remote-control flow-field-high`, and no longer from `flow-<request id>`. The same name goes to Claude's `--remote-control` flag.
- Test: `composed_prompt_carries_no_hash_request_id_or_source_text` covers both harnesses. It checks for no hex run of 16 or more characters, no request ID, no body digest and no source text. The Start fixture `delayed_receipt_after_source_deletion_promotes_without_a_second_external_write` still reaches Started.

## Not witnessed, and open

- No live Haiku Start was run, so a native transcript showing one user turn before the receipt is still unwitnessed. The live service is still 0.6.0, and activating it belongs to G1/504461.
- Unconfirmed live, in Claude: a multi-line argument after `/spirit ` is passed through intact. Past transcripts show multi-line `<command-args>` preserved.
- Unconfirmed live, in Codex: the `$name` text lines beside the typed skill items expand each skill only once. That is the form the TUI itself sends.
- Codex's `$main-flow` text mention has no typed item unless the profile names main-flow. This is the same as the old positional block.
- The harness appends `ARGUMENTS: <body>` to the leading skill's expansion, so for Claude the body enters context twice. This is a harness behaviour.
- A role-based remote-control name is not unique across Flows of the same role. G4, the native title, should replace it with the Flow ID.
- Caller-supplied fields can still carry hex: the bundle path (a /nix/store path, for example), the model, the Herdr session and the instruction. The composer adds none.
