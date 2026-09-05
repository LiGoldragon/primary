# Codex explicit-command implementation

The Home implementation changes normal `codex` back to the canonical pinned
upstream package. `codex-remote` is a separately named launcher that executes
the upstream CLI with only `--remote unix://` before its untouched arguments.
It has no argument scanner, fallback route, working-directory injection, or
permission flags. The persistent `codex-remote-control` service remains the
owner of the app-server.

The provider and its consumers remove `direct-codex` and `codex-raw`. Agent
Intercom's Codex child now receives the canonical package directly and no
longer receives `--yolo`; Claude-specific names remain. Native managed
configuration remains the full-access authority:
`approval_policy = "never"` and `sandbox_mode = "danger-full-access"`.

The `codex-remote` behavioral check was first run against a temporary faulty
provider that injected `--cd "$PWD"`; it failed on the unexpected argument.
After restoring the fixed provider, the same check built green on the
configured prom remote builder. The remote-control service contract and the
native permission/default configuration check also built green. The
Agent Intercom integration contract built green with `--max-jobs 0` and the
configured remote builder.

A follow-up review found that the fixture used `printf '%s\\n'`, which
printed a literal backslash-n and could not delimit argv values. The corrected
fixture uses real newlines and built green remotely with `--max-jobs 0`. It
also proves that `codex-remote` keeps the caller's working directory, supplies
only `--remote unix://`, and forwards an explicit `--cd /worktree` unchanged.
Thus normal directory selection remains native Codex behavior: the launcher
does not choose a directory, while callers can supply Codex's own `--cd`.
The retired scanner's cwd injection, fallback routing, raw dispatch, and
permission flags are intentionally absent under the approved interface; the
remote execution contract plus existing Agent Intercom, permission-default,
and remote-control contracts cover the retained behavior. No additional
launcher behavior is missing.

One early `ai-agent-launch-orchestration` build allowed a small activation
script dependency to build locally despite an explicit remote-builder setting.
The check derivation itself ran remotely and passed, but that invocation does
not satisfy the remote-only workflow. Later builds used `--max-jobs 0`.

The remote-only `pi-harness-profile` build fails on both the candidate and the
unchanged base because its Pi model assertions find no
`openai-codex/gpt-5.6-{sol,terra,luna}` models. This implementation does not
alter those model expectations.

No Codex-harness authored skill text names these retired executable aliases, so
the approved source work requires no skill amendment.

## Sources

- Approved proposal and instruction: `/home/li/.codex/sessions/2026/09/05/rollout-2026-09-05T13-51-12-01a07168-8c84-7d32-80b0-1508a5caa846.jsonl`, physical records 416 and 425 (user instruction at ordinal 424).
- Current Home source and checks in the isolated `CodexExplicitCommands-8a5caa` worktree.
- Remote builder configuration: `/etc/nix/machines`.
