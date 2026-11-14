# One renderer of role packets: the Claude agent renderer removed

Curriculum's `claude_agent.rs` and `curriculum --claude-agent-markdown` are removed on a branch. A Claude agent file's text is now made in one place only: curriculum-deploy's `role_projection::composed`, which renders the RoleComposition that ComposeRole returns. Both branches are pushed and gated, and each is a fast-forward of its main. Nothing is merged, deployed or switched. The evidence is in `/home/li/primary/flows/2e404d/claude-agent/`.

## The premise did not hold for CriomOS-home main

- **The installer is not on main.** `install-curriculum-claude-agents` was never in the history of CriomOS-home main (d140957). `git log -S claude-agent-markdown origin/main` finds nothing.
  - It was added in ef2f8dde ("install composed book author agents", 2026-10-22). That commit exists only on side branches and on the local checkout's `main`, which has diverged from origin by 1205 commits and has foreign uncommitted edits.
- **Nothing live runs it.** On ouranos, the live curriculum-nexus unit has an empty `ExecStartPost=`, and `install-curriculum-claude-agents` is not on PATH.
- **No other main calls it.** I searched the origin/main of every LiGoldragon repository for `claude-agent-markdown`, `claude_agent_markdown` and `RendersClaudeAgent`. Only Curriculum itself matched.
- **So no installer was changed.** CriomOS-home's only change is the relock of `curriculum-source`, so that its Home is built and checked with the Curriculum that lacks the flag.

## Heads (branch claude-agent-2e404d, pushed)

| repo | main (unchanged) | branch | fast-forward of main |
|---|---|---|---|
| Curriculum | 1b6c454 | 8881cc11ef4e328d97aa6ab6d281614da8dc0eea | yes |
| CriomOS-home | d140957 | 3ec49da0069996265c2df8750bca432bbf289629 | yes |

- **Curriculum 8881cc1** removes:
  - `src/claude_agent.rs` and `tests/claude_agent.rs`;
  - the flag handling in `src/main.rs` (the CLI now prints any reply as datom);
  - the client's `NamesRequestedRole`;
  - the README section on the flag.

  Nothing else is lost from the tests: role composition (each module once, provenance) stays covered by `tests/explicit_role_policy.rs`. Cargo.lock and Cargo.nix are unchanged, so crate2nix did not need to run.
- **CriomOS-home 3ec49da** moves one lock node, `curriculum-source`, from 1b6c454 to 8881cc1:
  - its `original` stays `github:LiGoldragon/Curriculum`;
  - its base stays build-base 9706bad.

  This is the lock `nix flake update curriculum-source` will write once Curriculum main fast-forwards to 8881cc1.
- **Worktrees:**
  - `/git/worktrees/Curriculum-claude-agent-2e404d`
  - `/git/worktrees/CriomOS-home-claude-agent-2e404d`

## Gates (prometheus; logs in `claude-agent/gates/`, exits in `gates/exits.txt`)

- **Curriculum 8881cc1** (nix-fast-build --remote --no-nom --no-download): **exit 0**. It passes crate-versions, crate-features, cargo-nix, curriculum (default and datom) and default.
- **CriomOS-home through nix-fast-build: exit 1, and main fails the same way.**
  - The failure is in evaluation: `attribute 'criomos' missing` at `modules/home/profiles/min/codex-next.nix:16`, raised while the flake filters `checks`.
  - Unchanged main d140957 fails identically (`gate-CriomOS-home-d140957-baseline.log`).
  - This is not caused by this change, and no single check can be selected past it. Flow e3a7d1's gate of 6eb8118 hit the same error.
- **CriomOS-home's Curriculum check**, built directly (`check-curriculum-resolver-deployment-*.log`): **exit 0** at both d140957 and 3ec49da.
  - I called `checks/curriculum-resolver-deployment` by `--impure --expr` against the committed revision, with nixpkgs from the flake's own input.
  - It runs the real Nexus and CLI, ComposeStartup and `ComposeRole.{ illustrator ClaudeAgent }` among them.
- **The ouranos Home**, built the way the last release built it:
  - Command: CriomOS 032f84e `#homeConfigurations.li.activationPackage`, with horizon, secrets and system taken from `/tmp/offload/f0f146-home-inputs` on prometheus.
  - **Baseline: exit 0**, giving **pkxvlf56wj29qrqqbabcrvz5klxjp8dh**. That is the live generation, so the inputs are confirmed.
  - **New:** the same build plus `--override-input criomos-home …/3ec49da`. **Exit 0**, giving **fy9dq6dbg3y7hcw3bhhlngqblz9bqvqq**.
  - The closure difference is only rust_curriculum (−24.9 KiB) and the Curriculum source (−21.0 KiB) (`before-after/home-generations.txt`).
- **The two `gate-CriomOS-home-d140957-curriculum-8881cc1*` logs** were my first attempts. They overrode the input on main before the branch existed, and they hit the same evaluation error.

## Before and after: the installed agent files

- **The Home installs no agent file, before or after.**
  - Neither generation has `.claude` in home-files, and neither closure has a path named `*claude-agents*`.
  - The curriculum unit's `ExecStartPost=` is empty in both.
  - The "after" for every role is therefore exactly the "before": none.
- **Leftovers from an older Home that did run the installer** are still in `~/.claude/agents`:
  - `general-purpose.md` and `book-author.md`, dated Nov 3;
  - an orphaned temporary file, `.general-purpose.AmKzA2`, dated Nov 1.

  They are stale: they say `effort: medium`, and roles.datom now says High. In primary, the project-level files of the same names take precedence. I left them alone (copies are in `before-after/installed-user/`).
- **The two renderers compared, all 15 ClaudeAgent roles** (`before-after/claude-agent-vs-composerole.diff`):
  - Old renderer: the live `curriculum --claude-agent-markdown` (1b6c454) against the live Nexus.
  - ComposeRole renderer: primary's `.claude/agents/*.md`, written by curriculum-deploy 832bde7 over the same belief revisions (psyche fdd8775, mind 573223d, field a515b80).
  - **Result:** each file differs in one line only, `model: sonnet` against `model: "sonnet"`. Both are YAML for the same string.
  - Descriptions, efforts, tool lists and bodies are byte-equal. Every description is printable ASCII.
- **The new CLI** (`before-after/new-cli-behaviour.txt`):
  - It refuses `--claude-agent-markdown` with "curriculum accepts exactly one inline Datom request", exit 1.
  - Its `ComposeRole.{ general-purpose ClaudeAgent }` reply from the live Nexus is byte-equal to the 1b6c454 CLI's.

## The one form kept, and one edge for Fable

- **Kept: curriculum-deploy's form.** It is what primary holds, and it is valid for every role today.
- **What only the removed renderer did:**
  - quoted the description by YAML's rules, escaping control characters as `\uXXXX`;
  - checked that role, model and tool names are plain;
  - re-checked the payload hashes;
  - refused a Restricted role that inherits its tools.
- **The edge:** curriculum-deploy quotes with Rust's `{:?}`. For a description containing a control character or a combining mark, that writes `\u{…}`, which is not YAML. No description has such a character now.
- **For Fable:** whether the one renderer should take YAML quoting and those checks. The change would be in curriculum-deploy, which this work did not touch.
