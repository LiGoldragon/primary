# 20 - Review of designer 129 and 130

Date: 2026-05-11
Role: designer-assistant

Reviewed:

- `reports/designer/129-sandboxed-persona-engine-test.md`
- `reports/designer/130-skill-bundles.md`
- `skills/README.md`

## Executive read

Designer/129 is directionally right: apex `persona` runner,
`systemd-run --user` outer supervision, optional `bwrap` strict mount
profile, host-side Ghostty attaching to terminal-cell sockets, and
per-harness credential directories are the right architecture.

Designer/130 is also directionally right: a simple `skills/README.md`
bundle index is the right first mechanism. The index exists and matches
the report's four-bundle shape.

The main fixes are not structural. They are safety and precision fixes:

1. Do not let a prompt-bearing Codex subscription test consume the live
   host refresh token.
2. Do not expose unredacted sandbox home snapshots as artifacts.
3. Use the actual Codex CLI reasoning levels available on this host:
   `low`, `medium`, `high`, `xhigh`, not `minimal`.
4. Make the programming bundle include Nix discipline somehow, because
   Nix-backed tests are part of how this workspace writes code.

## Findings on designer/129

### 1 - Codex snapshot auth is not safe enough for a prompt witness

Designer/129 correctly identifies Codex refresh-token rotation as the
central risk, but the proposed gate witness is still too weak.

The report proposes:

- copy host `~/.codex/auth.json` into sandbox;
- run one full prompt-bearing Codex federation witness;
- assert the host file is byte-unchanged;
- assert host `codex login status` still returns OK.

That can pass while the host has already been damaged. If the sandboxed
Codex run refreshes the copied token bundle, the host `auth.json` file
will indeed remain byte-unchanged, but its refresh token may now be stale
server-side. The host access token can remain valid until the next
refresh, so `codex login status` is not a strong enough postcondition.

OpenAI's Codex CI guidance confirms the dangerous part of the model:
Codex refreshes `auth.json`, writes refreshed tokens back, and operational
rules require one `auth.json` per runner or serialized workflow stream.

Recommendation:

- Codex prompt-bearing full-engine tests should use API-key auth by
  default (`codex-api` path), or a dedicated persistent sandbox
  `auth.json` created by a one-time sandbox/device login.
- The live host `~/.codex/auth.json` may be used only for no-prompt
  parse/status smoke tests, or for a deliberately opt-in destructive-risk
  experiment.
- Replace `full_engine_codex_smoke_preserves_host_auth` with two
  witnesses:
  - `codex_host_auth_snapshot_is_parse_only`
  - `codex_subscription_witness_uses_dedicated_runner_auth`

This is the highest-signal correction.

### 2 - Raw sandbox home snapshots should not be an artifact

Designer/129 lists `sandbox $HOME snapshot` as an inspectable artifact,
then asks in Q6 whether token-shaped strings should be redacted.

That should not be a question. The answer is yes, and the safer default
is stronger: do not publish a raw home snapshot at all.

The sandbox home can contain copied `auth.json`, `.credentials.json`,
settings files, provider caches, logs, and agent-created files. A report
artifact should be a sanitized manifest plus targeted witness outputs,
not a copy of the directory tree.

Recommendation:

- Replace `sandbox $HOME snapshot` with
  `sandbox_home_pollution_manifest`.
- The manifest records paths, file sizes, selected hashes for
  non-secret files, and redacted detector results.
- Credential files and token-shaped values are excluded from artifacts
  by construction.

### 3 - Do not pass Claude issued tokens through `systemd-run --setenv`

Designer/129's preferred Claude row says:

`--setenv CLAUDE_CODE_OAUTH_TOKEN=<token>`

That puts a secret in the unit invocation shape. Depending on how the
unit is launched and inspected, this can leak through command history,
process metadata, or unit properties.

Recommendation:

- Materialize the token in a root/user-private credential file or secret
  store.
- Pass it with `LoadCredential=claude-oauth-token:<path>`.
- Inside the runner, export `CLAUDE_CODE_OAUTH_TOKEN` only for the
  Claude child process by reading `$CREDENTIALS_DIRECTORY/claude-oauth-token`.

The child process still needs the token in its environment if Claude Code
requires that interface, but the token should not appear in the
`systemd-run` command line.

### 4 - Codex CLI uses `low`, not `minimal`, on this host

Designer/129 uses `reasoning_effort = "minimal"` in the TL;DR, model
section, witness names, and Codex config examples.

The local Codex model catalog currently exposes these supported reasoning
levels for both `gpt-5.4-mini` and `gpt-5.3-codex-spark`:

- `low`
- `medium`
- `high`
- `xhigh`

It does not expose `minimal`.

Recommendation:

- For Codex CLI subscription tests, use `model_reasoning_effort = "low"`.
- If an API-key path uses the OpenAI API directly and that endpoint
  accepts a lower setting, document that as API-specific and keep it out
  of Codex CLI config examples.
- Rename `codex_subscription_witness_uses_mini_minimal_reasoning` to
  `codex_subscription_witness_uses_mini_low_reasoning`.

### 5 - Use current terminal contract names in the flow

The sequence diagram says:

- `TerminalInject`
- `pattern_uid`

Current `signal-persona-terminal` names are:

- `AcquireInputGate`
- `WriteInjection`
- `ReleaseInputGate`
- `PromptPatternId`

Recommendation:

- Replace `TerminalInject` with the concrete `WriteInjection`-centered
  transaction.
- Replace `pattern_uid` with `prompt_pattern_id`.

This is low severity, but exact names matter because these reports train
implementation.

### 6 - Pi should be forced to the local provider path

Designer/129 says Pi has no external API/pollution risk. More precise:
the intended Pi witness has no paid cloud model API when it is forced to
the `prometheus` provider, but Pi still has auth/config surfaces and may
perform startup network behavior.

Recommendation:

- The Pi witness should set provider/model explicitly, for example
  `--provider prometheus --model prometheus/glm-4.7-flash --no-session`,
  or write equivalent settings into the sandbox `PI_CODING_AGENT_DIR`.
- Add a witness that the Pi run did not fall back to an OpenAI/Codex
  provider path.

## Findings on designer/130 and skills/README

### 1 - `nix-discipline.md` is operational, but also programming-critical

Designer/130 and `skills/README.md` put `nix-discipline.md` only in the
`operational` bundle. That follows a one-skill-one-bundle rule, but it
creates a practical miss: when the user says "read all programming
skills" before code work, agents will not necessarily read the Nix rules
that govern tests, flake inputs, and runnable witnesses.

In this workspace, Nix-backed tests are not just operations. They are
part of how code is considered real.

Recommendation:

- Either allow duplicate membership and add `skills/nix-discipline.md`
  to `programming`, or
- keep one primary bundle but add a composite bundle named
  `workspace-code` / `implementation` that expands to `programming` plus
  `nix-discipline` and the relevant operational commit/report basics.

The second option preserves one primary home while giving humans the
phrase they actually want.

### 2 - The bundle index needs an adoption hook

`skills/README.md` exists, but the required-reading chain still names
specific skills in `AGENTS.md` and `skills/autonomous-agent.md`. The
index says how to resolve bundle phrases, but no upstream rule says
"when the human names a bundle, read `skills/README.md` first."

Recommendation:

- Add a short note to `AGENTS.md` or `skills/autonomous-agent.md`:
  "If the user names a skill bundle such as programming, operational,
  role, or specialty, resolve it through `skills/README.md` and read the
  listed files."

This is not urgent, but without the hook the index is less canonical than
the report implies.

### 3 - Exact-one-bundle may be too rigid

The exact-one-bundle rule keeps the index clean, but it fights the real
shape of several skills:

- `testing.md` is programming and operational.
- `nix-discipline.md` is operational and implementation-critical.
- `architecture-editor.md` is specialty and design/programming-adjacent.
- `skill-editor.md` is operational and design-adjacent.

Recommendation:

- Keep "primary bundle" for maintenance.
- Add optional "composite bundles" for actual human commands:
  - `implementation`: programming + `nix-discipline`
  - `architecture`: programming + `architecture-editor`
  - `skill-work`: operational + `skill-editor` + `architecture-editor`

That keeps the index hand-maintained but avoids false exclusions.

## Recommended edits

For designer/129:

1. Promote Codex dedicated-runner auth to the subscription-auth
   recommendation. Treat live host auth snapshots as parse/status only.
2. Change Codex CLI reasoning from `minimal` to `low`.
3. Replace raw sandbox home snapshot artifacts with sanitized manifests.
4. Replace `--setenv CLAUDE_CODE_OAUTH_TOKEN=<token>` with
   `LoadCredential=claude-oauth-token:<path>` plus runner-local export.
5. Use current terminal contract names: `PromptPatternId`,
   `AcquireInputGate`, `WriteInjection`, `ReleaseInputGate`.
6. Force Pi's provider/model and add a no-fallback witness.

For designer/130 / `skills/README.md`:

1. Decide whether duplicate bundle membership is allowed.
2. If not, add composite bundles.
3. Ensure a code-work bundle includes `nix-discipline.md`.
4. Add an upstream adoption note so bundle phrases resolve through
   `skills/README.md`.

## Sources checked

- Local Codex model catalog via `codex debug models`: `gpt-5.4-mini`
  and `gpt-5.3-codex-spark` support `low`, `medium`, `high`, `xhigh`.
- OpenAI GPT-5.4 mini/nano announcement: GPT-5.4 mini is available in
  Codex and uses 30% of GPT-5.4 quota; GPT-5.4 nano is API-only.
- OpenAI Codex CLI docs: Codex CLI can authenticate with ChatGPT account
  or API key.
- OpenAI Codex CI/CD auth docs: one `auth.json` per runner or serialized
  workflow stream; Codex may refresh and rewrite `auth.json`.
- Claude Code model config docs: `haiku` is the simple-task alias, and
  startup `--model` / `ANTHROPIC_MODEL` are supported.
- Claude Code CLI docs: `--no-session-persistence` is print-mode only;
  `CLAUDE_CODE_SKIP_PROMPT_HISTORY` is the equivalent environment
  control in any mode.
