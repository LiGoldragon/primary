# Code Kill Audit

Task: audit epic `primary-5rzf`, bead `primary-5rzf.7`, against the verifier-confirmed code-kill scope and the reported full `nix flake check --no-write-lock-file` failure in `/git/github.com/LiGoldragon/persona`.

Conclusion: `primary-5rzf.7` is not closeable yet. The reported `persona-message` fixed-output hash mismatch is unrelated to the `.7` cleanup, but verifier item C3 is only fixed in the isolated `/git/github.com/LiGoldragon/lojix-primary-5rzf-7` worktree and is still stale in the canonical occupied `/git/github.com/LiGoldragon/lojix` checkout.

## Findings

### Blocker: C3 remains unresolved in the canonical `lojix` checkout

Verifier item C3 requires replacing the stale `horizon-re-engineering` direction in `/git/github.com/LiGoldragon/lojix/README.md`.

Observed evidence:

- `/git/github.com/LiGoldragon/lojix-primary-5rzf-7/README.md:17` contains `horizon-leaner-shape`.
- `/git/github.com/LiGoldragon/lojix/README.md:17` still contains `horizon-re-engineering`.
- `CodeKill-Evidence.md` records that `/git/github.com/LiGoldragon/lojix` was claimed by `system-designer`, so the worker created `/git/github.com/LiGoldragon/lojix-primary-5rzf-7` and filed `primary-pg6f` for disposition.
- `bd --readonly show primary-pg6f` shows an open worktree-disposition bead for partial merge of `README.md` cleanup or discard if another integration path is chosen.

Risk: closing `.7` now would unblock closeout while one verifier-confirmed code-surface stale reference remains in the canonical in-scope repo. The isolated worktree is valid coordination evidence, but it is not yet the landed or otherwise accepted state of the canonical `lojix` surface.

Expected correction: dispose `primary-pg6f` before closing `.7`: either merge/apply the README cleanup into the canonical `lojix` path when ownership permits, or document and execute an alternate integration path that makes `/git/github.com/LiGoldragon/lojix/README.md` no longer point new work at `horizon-re-engineering`. Then rerun the C3 grep against the canonical path.

### Non-blocker: persona full-flake failure is unrelated to `.7`

The full `nix flake check --no-write-lock-file` failure in `/git/github.com/LiGoldragon/persona` should not itself block `.7`.

Observed evidence:

- `jj diff --git` in `/git/github.com/LiGoldragon/persona` shows the `.7` flake edits only rename the `persona-mind` input/package/check/launcher references to `mind`.
- The diff leaves `persona-message.url` and `packages.x86_64-linux.persona-message` structurally unchanged.
- Rerunning `nix flake check --no-write-lock-file` fails while checking `packages.x86_64-linux.persona-message` at `flake.nix:573`, with fixed-output derivation hash mismatch:
  - specified `sha256-gh/xTkxKHL4eiRXzWv8KP7vfjSk61Iq48x47BEDFgfk=`
  - got `sha256-h+t2xTBz5yt2YIO+1VMIIGlCU7gyp2LYOFvaV1nwOXU=`
- Narrow Nix checks for the touched rename surface pass:
  - `nix eval --no-write-lock-file .#packages.x86_64-linux.mind.pname` returns `"mind"`.
  - `nix eval --no-write-lock-file .#checks.x86_64-linux.mind.name` returns `"mind-test-0.3.0"`.

Risk: none for `.7` causality. This remains a full-flake/environment or upstream input integrity problem for `persona-message`, not a plausible consequence of the `.7` `mind` rename.

Expected correction: when `.7` is otherwise complete, close it with an explicit note that the full persona flake check is known red for unrelated `persona-message` fixed-output hash mismatch, and carry that failure to the appropriate owner if full-flake green remains required elsewhere.

## Audit Questions

1. Does `CodeKill-Evidence.md` show every verifier-confirmed `.7` item was handled?

It shows actions for C1-C4, but not all are fully handled in canonical in-scope surfaces. C1, C2, and C4 are handled in the edited paths. C3 is handled only in `/git/github.com/LiGoldragon/lojix-primary-5rzf-7`; the canonical `/git/github.com/LiGoldragon/lojix/README.md` still contains the stale term.

2. Are the focused checks sufficient for the touched code surfaces?

Mostly yes for the surfaces actually changed: `jq` covers `primary.code-workspace`; `rg` covers removed dead names in scoped primary/persona/meta paths; `cargo fmt --check`, full `cargo test`, the targeted daemon test, and narrow `nix eval` checks cover the persona Rust and flake rename surface. The missing piece is not another persona check; it is final disposition and verification of the canonical `lojix` C3 surface.

3. Is the `persona-message` fixed-output hash mismatch unrelated to `.7`, or did `.7` edits plausibly cause it?

It is unrelated. The `.7` persona diff changes `persona-mind` to `mind`; the reproduced full-flake failure is at unchanged `persona-message` package evaluation and reports a fixed-output Rust channel file hash mismatch.

4. Should `primary-5rzf.7` remain open, be closed with an explicit unrelated-check note, or get a follow-up blocker bead?

Leave `primary-5rzf.7` open. Do not create a new follow-up bead: `primary-pg6f` already exists for the required isolated `lojix` worktree disposition. The tracker should either keep `.7` open until `primary-pg6f` is resolved or explicitly link/block `.7` on `primary-pg6f` before later closeout.

## Evidence Checked

- Read `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/Verifier-Ledger.md`.
- Read `/home/li/primary/agent-outputs/WorkspaceStalenessSweep/CodeKill-Evidence.md`.
- Ran `bd show primary-5rzf.7`; bead remains `IN_PROGRESS` with worker evidence comment.
- Ran `bd --readonly show primary-pg6f`; open disposition bead exists for `/git/github.com/LiGoldragon/lojix-primary-5rzf-7`.
- Ran `orchestrate "(Observe Roles)"`; `/git/github.com/LiGoldragon/lojix` is claimed by `system-designer`.
- Ran `rg -n "persona-mind|signal-persona-mind"` across the scoped persona, primary workspace, and meta-signal-router paths; no hits.
- Ran `rg -n "horizon-re-engineering|horizon-leaner-shape"` against canonical and isolated `lojix` READMEs; canonical path still has `horizon-re-engineering`, isolated path has `horizon-leaner-shape`.
- Ran `jj diff --git` in `/git/github.com/LiGoldragon/persona`; inspected rename-only flake/code/test changes around `mind`.
- Ran `jq empty /home/li/primary/primary.code-workspace`; passed.
- Ran `cargo fmt --check` in `/git/github.com/LiGoldragon/persona`; passed.
- Ran `cargo test` in `/git/github.com/LiGoldragon/persona`; passed, with 75 passed and 1 existing ignored test in the displayed integration/unit run.
- Ran `cargo test --test daemon constraint_persona_daemon_launches_prototype_supervised_components_through_engine_supervisor`; passed.
- Ran `nix eval --no-write-lock-file .#packages.x86_64-linux.mind.pname`; returned `"mind"`.
- Ran `nix eval --no-write-lock-file .#checks.x86_64-linux.mind.name`; returned `"mind-test-0.3.0"`.
- Ran `nix flake check --no-write-lock-file` in `/git/github.com/LiGoldragon/persona`; failed at unchanged `packages.x86_64-linux.persona-message` with fixed-output derivation hash mismatch.

## Residual Risks

- `primary.code-workspace` and several agent-output files live in a dirty `/home/li/primary` worktree alongside many unrelated changes by other workers. This audit did not revert or normalize unrelated state.
- This audit did not enter `/home/li/primary/private-repos` and did not sweep Spirit intent records, per dispatch boundaries.
- This audit did not close or update tracker state because `.7` is not closeable under the observed C3 canonical-surface gap.
