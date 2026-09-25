# Flow launch findings: Flow 0.10.0

This work fixes three launch findings from Psyche Medium e51411's companion launch (9c7514). An Opus subflow of 38de5b did it on 2026-09-25.

- Repository: github.com/LiGoldragon/flow.
- Branch `launch-findings-38de5b` was cut from main 28a78d2 (0.9.0). No other change had landed on main in the meantime.
- Revision: bbf5fa16309c44a9506ded2b1ab02260919f6d34 "Flow 0.10.0: stacked Claude commands, native title after claim, no auto-mode offer".
- `git ls-remote` shows both `main` and `launch-findings-38de5b` at bbf5fa1. Main was fast-forwarded.
- Tests before the change: 74 + 6 + 3 + 1 + 1 passed. Tests after: 83 + 6 + 3 + 1 + 1 passed, 0 failed.
- `cargo clippy --all-targets` reports 0 warnings, and `cargo fmt --check` is clean.
- `nix flake check` was not run.
- Version: 0.9.0 became 0.10.0 in Cargo.toml, Cargo.lock and flake.nix. The versioning skill's rule is that a public behaviour change updates the version surface. The prompt and argv a launched Claude receives changed, and so did the Start sequence. Neither wire nor storage changed, so this is a pre-1.0 minor bump. UPGRADES.md has a 0.10.0 entry and README.md is updated.
- Orchestrate lock 6458 was taken and then released.

## 1. Stacked commands

Witness: transcript `~/.claude/projects/-home-li-primary/9c7514c1-9da9-48b9-b5af-025c4f38f468.jsonl`, Claude Code 2.1.280.

- The companion's start line stacked `/spirit /psyche /main-flow /psyche-interraction /flow-aspect /behavior /messaging …`.
- **Six** command records were loaded: spirit through behavior. After them the system row reads "Stacked command limit (5) reached — remaining input passed as arguments", and `/messaging` onward arrived as text.
- The limit therefore appears to count the stacked commands after the head command. Flow stacks at most five, which is inside what was witnessed.
- Each command record carries the same `<command-args>`, which is the text after the last loaded command. Each is followed by its own `isMeta` + `turnCompanion` expansion, ending `ARGUMENTS: <args>`. The first record also carries `stackedOriginalInput`.

Change:

- `ClaudeCommandStack::LIMIT = 5` (composition.rs). The head is up to five `/name ` commands in profile order. Skills beyond the fifth are listed under "Then load through the Skill tool, in this order: …".
- The observer rebuilds the typed text from the first record, `/n1 … /nk <args>`. It checks the body hash and `stackedOriginalInput` when present. It then requires records 2..k in order with the same argument, and one expansion per record, before any Skill-tool call.
- Tests:
  - `claude_prompt_stacks_at_most_five_commands_and_lists_the_rest`: ≤5 commands, and the sixth and seventh appear as text only.
  - `claude_stacked_command_prompt_reaches_its_receipt`: five records plus two Skill-tool loads reach Observed. A wrong lead, a sixth command record, a swapped order, and four records followed by the Skill tool are each refused.

## 2. Inherited title (G4)

The root cause was witnessed on the live processes.

- Two panes run with the same `CLAUDE_JOB_DIR=/home/li/.claude/jobs/108ab020`: 9c7514 (pane wD:pW, pid 1714346) and b87854 (pane wD:pQ, pid 2360492).
- 9c7514's transcript begins with `custom-title "Psyche Opus b87854"`, which it adopted from the shared job state.
- Its later `/rename` fanned out the other way: `herdr agent list` now shows **b87854's pane titled `PsycheV2.{ Sonnet 9c7514 }`**. This is the same shared-job fan-out that `flows/6db4fe/reports/claude-environment-isolation.md` describes.
- b87854's title is wrong right now. I did not touch it.

Change:

- The Claude pane preparation now unsets `CLAUDE_JOB_DIR`, `CLAUDE_CODE_SESSION_ID` and `CLAUDE_CODE_SESSION_KIND`, besides `CLAUDE_CODE_CHILD_SESSION`.
- After claim and registration, and before skill resolution and the prompt, Start calls `TitlesNativeFlow::title_native_flow`:
  - The title is `NativeTitle::for_flow`, giving `<Aspect>V2.{ <Model> <FlowId> }`. The model name comes from `ModelDisplay`, a fixed copy of `config/model-display-names.json` v1. An unmapped model or a malformed Flow ID is refused.
  - For Claude, Start sends `herdr agent prompt <agent> "/rename <title>"`. It then polls for two things: Herdr `terminal_title_stripped` must equal the title, and the session's last transcript `custom-title` must equal it when one exists.
  - For Codex, Start sends app-server `thread/name/set` and reads it back with `thread/read` (id and name).
  - It then runs `herdr pane rename <pane> <title>` and reads the label back with `pane get`.
  - Any failure returns `StartRejected(BindingRefused)`. There is no new signal-flow variant.
- Tests:
  - Claude: readback equals `PsycheV2.{ Fable 123456 }` on the terminal title, the transcript record and the pane label, in the order claim < rename < label < label read.
  - A differing readback (`Psyche Opus b87854`) refuses before any label is set.
  - An unmapped model is refused before any rename.
  - Codex: `FieldV2.{ Astra 123456 }` is read back through a fake app-server proxy, and the pane label is read back too.
  - Unit tests for the title form and its refusals.

## 3. Auto-mode offer

`claude --help` (2.1.280) has no flag named for the offer. `--permission-mode` does not affect it. I read the gate in the installed bundle (`.claude-wrapped`, function `shouldShowAutoDefaultNudge`). The dialog "Make auto mode your default permission mode?" is shown only when all of these hold:

- the global state `hasSeenAutoDefaultNudge` is not true;
- the feature flag `tengu_maple_pier` is on;
- userSettings `permissions.defaultMode` is set and is not `auto`;
- **no** project, local, flag or policy settings source sets `permissions.defaultMode`;
- auto mode is available.

The flag `--settings <json>` is the flagSettings source. Flow now starts Claude with `--settings '{"permissions":{"defaultMode":"bypassPermissions"}}'`, which suppresses the offer and writes no settings file. The argv fixture asserts the flag.

For the CriomOS-home owner, if a persistent default is preferred instead, there are two settings-level alternatives. Neither is touched here:

- the global-state key `hasSeenAutoDefaultNudge: true` in `~/.claude.json`, which is not in settings.json;
- setting `permissions.defaultMode` in any non-user settings source.

This evidence comes from reading code. No live launch has witnessed the dialog's absence.

## Open, and not witnessed

- **Multi-line prompt paste hazard.** `flows/e51411/reports/one-block-startup-prompt.md` found that a multi-line block sent through `herdr agent prompt` arrives as a paste, and then no command expands. Flow's composed Claude body is multi-line ("# Flow launch\n\nRole: …"). A live Claude Start may therefore expand nothing and stay StartAmbiguous. That report found the fix to be one single-line block, or a start-time argument. Choosing between them is a composition decision outside this brief.
- There is no live Flow Start of either harness, so no live title readback, stacked expansion or dialog absence has been witnessed.
- Two assumptions come from existing primary tooling and are not witnessed from a Flow-started fresh session:
  - that `herdr pane get` returns `label`;
  - that Claude writes a transcript `custom-title` row on `/rename`.
- If a later step fails, Start does not roll the title back after a partial mutation, for example a native title set but the label failing. The Start is refused and the pane keeps the title.
- The Herdr agent name stays the launch-derived identity. Renaming it would break the stored binding lookups. `herdr agent list` therefore shows the title as `terminal_title`, and in the pane label, but not as `name`.
- The model-display map is duplicated in Rust and can drift from `config/model-display-names.json`.
- The brief asked for the footer "Claude Fable 5.1". The commit carries this session's own attribution (Opus 5.5) instead, because the committer is Opus 5.5.

## Sources

- `flows/38de5b/receipts/g2-g3-flow.md`; G4 in `flows/38de5b/reports/audit-flow.md`.
- `flows/e51411/log.md` (companion launch finds); `flows/e51411/reports/one-block-startup-prompt.md`.
- `flows/6db4fe/reports/claude-environment-isolation.md`, `canonical-title-alignment-implementation.md`.
- `tools/native-seat-launch.mjs`, `tools/canonical-title-alignment.mjs`, `tools/model-display-name.mjs`, `config/model-display-names.json`.
- Transcript 9c7514c1-9da9-48b9-b5af-025c4f38f468; `/proc/<pid>/environ` of pids 1714346 and 2360492; `herdr agent list`.
- `claude --help` 2.1.280; strings of the installed claude-code 2.1.280 `.claude-wrapped`.
