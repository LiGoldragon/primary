# Locked Persona/signal audit

Audit date: 2026-05-23.

Scope: read-only audit for the NOTA bracket-string migration. The only file written by this agent is this subreport.

## Lock state

`second-operator.lock` holds the active `signal-persona-origin` crate and identifier rename lock. The lock covers the Persona/signal migration surface, including:

- signal contracts: `signal-persona-origin`, `signal-persona`, `signal-persona-message`, `signal-persona-router`, `owner-signal-persona-router`, `signal-persona-mind`, `signal-persona-introspect`, `signal-persona-system`, `signal-persona-harness`, `signal-persona-terminal`, `owner-signal-persona-terminal`.
- daemon/client repos: `persona`, `persona-router`, `persona-mind`, `persona-spirit`, `persona-message`, `persona-introspect`, `persona-system`, `persona-harness`, `persona-terminal`.
- adjacent locked non-Persona roots: `terminal-cell`, `signal-frame`, `signal-core`, `criome`, and `/home/li/primary`.

These repos cannot be safely migrated now because the active rename is changing crate names, identifiers, manifests, lockfiles, and related examples. Bracket-string edits in the same files would create avoidable conflicts.

Blocked/missing state:

- `/git/github.com/LiGoldragon/signal-persona-auth` is listed in the lock but is missing on disk in this workspace, so it was not audited.
- `persona-spirit` has dirty working-copy edits in `Cargo.toml`, `Cargo.lock`, and `tests/design_d_routing.rs`.
- `owner-signal-persona-terminal` has a dirty `Cargo.lock`.
- The remaining audited repos reported clean working copies at read time, but all are still locked by `second-operator`.

## Direct `nota-codec` pins

Every available locked Persona/signal repo audited has a direct `nota-codec` main-branch dependency in `Cargo.toml`. The corresponding `Cargo.lock` entries observed for these repos resolve `nota-codec` to `538555e895529e2884b7d37d20c66aadc2a49c08`, matching the already-merged bracket-string-capable `nota-codec` main.

Repos with direct `nota-codec` dependencies:

- `signal-persona-origin`
- `signal-persona`
- `signal-persona-message`
- `signal-persona-router`
- `owner-signal-persona-router`
- `signal-persona-mind`
- `signal-persona-introspect`
- `signal-persona-system`
- `signal-persona-harness`
- `signal-persona-terminal`
- `owner-signal-persona-terminal`
- `persona`
- `persona-router`
- `persona-mind`
- `persona-spirit`
- `persona-message`
- `persona-introspect`
- `persona-system`
- `persona-harness`
- `persona-terminal`

Deferred action after the rename lock clears:

- Refresh each repo's lockfile after the rename branch is stable, not during this audit.
- Prefer Nix-owned checks for the refresh. `cargo test` can be used as an inner-loop only.
- Add or preserve a dependency witness where useful with a constraint-style name such as `nota_codec_pin_resolves_to_bracket_string_capable_main`.

## Authored NOTA quotation findings

Focused `rg` did not find quote-delimited strings inside the locked `examples/*.nota` fixtures, except a prose comment in `signal-persona-introspect/examples/canonical.nota`. The remaining obvious authored NOTA quote delimiters are in Rust tests, documentation examples, and Nix checks.

### `persona-spirit`

Findings:

- `tests/actor_runtime.rs:194`, `:198`, and `:202` submit `Record` operations with `"topic one"`, `"context"`, and `"quote"` quote-delimited strings.
- `tests/actor_runtime.rs:513` submits `(State ("capture this intent"))`.

Deferred migration:

- Change those authored operation strings to bracket strings, for example `[topic one]`, `[context]`, `[quote]`, and `(State ([capture this intent]))` if the `State` wire shape still expects the nested record/transparent wrapper after the active rename.
- Add or rename witnesses to make the constraint explicit:
  - `record_accepts_bracket_string_summary_context_and_quote`
  - `state_accepts_bracket_string_statement`
  - `topic_catalog_observation_uses_bracket_string_records_without_write_plane`
- Run the repo's Nix checks after the dirty `persona-spirit` rename edits land.

### `persona-mind`

Findings:

- `tests/cli.rs:75` uses `(NoteSubmission ... "note body")`.
- `tests/cli.rs:92` uses `(Report "reports/operator/105-command-line-mind-architecture-survey.md")`.
- `tests/cli.rs:104` uses `(StatusChange ... "started")`.
- The same test file already has bracket-string equivalents later in the daemon CLI path, so this is likely older coverage rather than a parser requirement.

Deferred migration:

- Convert the older text mapping test to bracket strings: `[note body]`, `(Report [reports/operator/105-command-line-mind-architecture-survey.md])`, and `[started]`.
- Keep the later daemon CLI coverage as the canonical model.
- Suggested witness names:
  - `mind_text_mutation_accepts_bracket_strings`
  - `mind_text_report_reference_accepts_bracket_string_path`
  - `mind_cli_mutates_work_item_with_bracket_strings`

### `persona-router`

Findings:

- `tests/smoke.rs:113` decodes `(PtySocket "/tmp/responder.terminal.sock" None)`.
- `tests/smoke.rs:129` decodes `(HarnessSocket "/tmp/responder.harness.sock" None)`.
- The signal contract tests already show the likely target shape with bracket socket paths, for example `(HarnessSocket [/tmp/responder.harness.sock] None)` in `signal-persona-router/tests/round_trip.rs`.

Deferred migration:

- Convert socket endpoint examples to bracket strings.
- Prefer test names that describe the accepted contract:
  - `router_bootstrap_decodes_bracket_string_pty_endpoint`
  - `router_bootstrap_decodes_bracket_string_harness_endpoint`
  - `router_bootstrap_examples_do_not_require_quote_delimiters`

### `persona-message` and `signal-persona-message`

Findings:

- `persona-message/README.md:24` shows `message '(Send designer "Need a layout pass.")'`.
- `persona-message/skills/persona-message-harness.md:25` shows `message '(Send operator "status text")'`.
- `persona-message/skills/persona-message-harness.md:62` shows `message '(Send recipient "body text with spaces")'`.
- `signal-persona-message/ARCHITECTURE.md:73` shows `message '(Send designer "hi")'`.
- `signal-persona-message/ARCHITECTURE.md:226-238` already uses bracket strings for the deeper worked wire example.

Deferred migration:

- Convert human-authored CLI examples to bracket strings: `message '(Send designer [Need a layout pass.])'`, `message '(Send operator [status text])'`, and `message '(Send recipient [body text with spaces])'`.
- Preserve examples with bare atoms where a bare atom is the intended shape.
- Add or keep a Nix-owned example/help witness:
  - `help_examples_do_not_require_quote_delimiters`
  - `message_cli_accepts_bracket_string_body`
  - `message_cli_accepts_bracket_string_with_apostrophe`

### `persona`

Findings:

- `flake.nix:1406-1408` expects sandbox profile records such as `(ReadOnlyBind "/nix")`, `(ReadOnlyBind "/run/current-system")`, and `(ReadWriteBind "$out/sandbox")`.
- `flake.nix:1432-1433` expects `(CredentialRoot "$out/credentials")` and `(ReadWriteBind "$out/credentials")`.

These are Nix-owned tests already, but the expected NOTA output still encodes ordinary path strings with quote delimiters.

Deferred migration:

- Change the sandbox profile and manifest producers to emit bracket strings for ordinary authored path values where practical, then update the grep witnesses accordingly.
- Keep shell interpolation readable; the expected form can use bracket strings around the interpolated path.
- Suggested witness names:
  - `sandbox_profile_emits_bracket_string_bind_paths`
  - `sandbox_manifest_emits_bracket_string_credential_root`
  - `canonical_sandbox_examples_emit_bracket_strings`

## Repos with no obvious quoted authored NOTA found

The focused audit found no obvious quote-delimited authored NOTA examples/tests/fixtures in the currently available checked state of:

- `signal-persona-origin`
- `signal-persona`
- `signal-persona-router`
- `owner-signal-persona-router`
- `signal-persona-mind`
- `signal-persona-introspect`
- `signal-persona-system`
- `signal-persona-harness`
- `signal-persona-terminal`
- `owner-signal-persona-terminal`
- `persona-introspect`
- `persona-system`
- `persona-harness`
- `persona-terminal`

This is not a full parser audit. It is a focused read-only scan for obvious authored quote delimiters in locked surfaces.

## Deferred migration plan

After `second-operator` releases the signal-persona-origin rename lock:

1. Re-read all affected repo `AGENTS.md` and `skills.md` files before editing each repo.
2. Claim the specific repo group being migrated; do not batch all locked repos unless the migration will touch all of them in one coordinated pass.
3. Start with dirty or actively changed repos only after their owner has landed or abandoned the rename edits: `persona-spirit` and `owner-signal-persona-terminal`.
4. Refresh direct `nota-codec` locks only after each repo's rename state is stable.
5. Convert authored examples/tests from quote delimiters to bracket strings in this order:
   - `persona-spirit` runtime operation tests.
   - `persona-mind` text CLI mutation tests.
   - `persona-router` bootstrap socket endpoint tests.
   - `persona-message` and `signal-persona-message` CLI/help documentation examples.
   - `persona` sandbox profile and manifest Nix checks.
6. Expose or preserve Nix-owned witnesses. Constraint-style names to use where applicable:
   - `cli_accepts_bracket_string_with_apostrophe`
   - `canonical_examples_emit_bracket_strings`
   - `help_examples_do_not_require_quote_delimiters`
   - `record_accepts_bracket_string_summary_context_and_quote`
   - `state_accepts_bracket_string_statement`
   - `router_bootstrap_examples_do_not_require_quote_delimiters`
   - `sandbox_profile_emits_bracket_string_bind_paths`
7. Run `nix flake check` or the repo-specific named Nix check/app for each changed repo. Treat `cargo test` as inner-loop evidence only.

No repo source changes were made during this audit.
