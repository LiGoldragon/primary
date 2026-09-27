# c56100 command-gate Stage 1 witness

## Session

- Native session UUID: `627d132f-a077-4bbf-a64c-e8261834c8be`.
- Claude Code: `2.1.280`.
- Model: `claude-sonnet-5`; each native turn records effort `medium`.
- Launch included `--settings flows/c56100/supervisor/source-only-gate-settings.json`, `--include-hook-events`, `--verbose`, and `--output-format stream-json`; it did not use `--bare`.
- Raw native stream SHA-256: `2bed913f1c6c2f6ba40f913f1c16a3dca1c2fe647e0cf44303477a585c36ae43`. The raw stream is retained outside this commit as a session audit record.

## Native Skill receipts

The stream records successful native `Skill` tool results, each `Launching skill: <name>`, for: `subflow`, `compensation-nix`, `nix-workflow`, `edit-coordination`, `orchestrate`, `file-editing`, `testing`, `testing-push-landed`, `behavior`, `secrets`, and `flow-evidence`.

## Gate probe

After all Skill receipts, the only Bash request was exactly `echo SOURCE_ONLY_GATE_PROBE`. The native stream contains:

- `PreToolUse:Bash` hook response with `permissionDecision: deny` and `SOURCE_ONLY_GATE: Bash denied before execution`;
- a native `permission_denials` entry naming that same Bash tool use; and
- a `non_execution_kind: permission-rule` result, with no probe output.

The worker then replied exactly `GATE_PROBE_COMPLETE`. It made no source edit, lock, Nix, test, build, Flow, Message, Herdr, credential, service, or persona-test operation.

## Gate scope and limits

`source-only-bash-gate.sh` denies every Bash request except direct `jj` inspection/commit/bookmark/push forms and exact Orchestrate observe/lock/release forms. It rejects shell separators, redirection, substitutions, escapes, and environment wrappers before matching. It therefore rejects Nix evaluation/check/build, formatter, test, scenario, and arbitrary shell commands before execution.

The future launcher must keep this settings file and hook outside the worker source tree, retain `--include-hook-events`, and never use `--bare` (which skips hooks). This is a Claude tool boundary, not an OS isolation boundary: a launcher that omits or replaces settings, uses `--bare`, or grants the worker write access to the hook/config defeats it. A source Stage 2 remains unapproved.
