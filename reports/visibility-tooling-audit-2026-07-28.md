# Visibility tooling audit — 2026-07-28

## Scope and method

This is a read-only audit of `/home/li/primary`, the deployed user profile,
and the declarative sources in `CriomOS-home` (with the current
`CriomOS-emacs` source consulted where it explains the editor surface). It
does not install, activate, update, or alter configuration. External claims
are checked against primary maintainer documentation on 2026-07-28.

Evidence labels used below:

- **Wired**: declarative source and a live local witness agree.
- **Configured**: declarative source names the capability; its live use was
  not exercised in this audit.
- **Present**: binary or extension exists locally, but no configuration makes
  it a primary workflow.
- **Missing witness**: the desired experience is not demonstrated by a local
  component or by a maintained upstream contract.

## Observations

### Existing review and history stack

| Need | Current state | Evidence / practical reading |
|---|---|---|
| Change-tree / history graph | **Wired** — VSCodium has VisualJJ 0.28.1, pinned as a VSIX input and listed by `codium --list-extensions`. | VisualJJ is the authoritative graphical JJ surface here: the Home module explicitly says VisualJJ is colocated in SCM for the actual JJ workflow. Its maintained product documentation describes a change tree, editing prior changes, splitting/squashing/reordering, and GitHub requests. [VisualJJ marketplace page](https://marketplace.visualstudio.com/items?itemName=visualjj.visualjj) |
| Structural code diff | **Wired** — `difft` 0.19.2 is installed and Jujutsu config sets `ui.diff-formatter = ['difft', '--color=always', '$left', '$right']`. | Difftastic parses supported syntax rather than comparing only lines; it falls back to line diff for unsupported or very large input. It can recursively compare two directories, but that is a directory-to-directory operation, not a VCS change summary. [Difftastic manual](https://difftastic.wilfred.me.uk/introduction), [directory usage](https://difftastic.wilfred.me.uk/usage.html) |
| Whole-change scale and deletions | **Present, low-friction** — JJ 0.40.0 supports `jj diff --summary`, `--stat`, and `--types`. A live dirty primary worktree rendered five changed files and a 607/25 insertion/deletion stat. | This is already the safest first screen for large agent changes. `--summary` makes adds/modifies/deletes explicit; `--stat` supplies magnitude. However, the current JJ config has `ui.color = "never"`; use `--color=always` interactively until that policy is deliberately changed. JJ documents `--summary`, `--stat`, and operation-log diffs. [JJ CLI reference](https://docs.jj-vcs.dev/latest/cli-reference/) |
| Terminal history/review UI | **Present** — `delta`, `lazygit`, `meld`, `broot`, `tokei`, and `scc` are installed. `lazygit` has an empty user config. | Delta and Meld can improve a selected Git comparison, but they do not make JJ's operation/change graph canonical. Lazygit is Git-oriented; adopting it as the primary control surface would blur the explicit VisualJJ/JJ boundary. |
| Emacs code navigation and local condensation | **Configured** — Emacs 30.2 has Magit, `magit-delta`, Difftastic, git-gutter, Projectile, deadgrep, ztree, Imenu-list, Consult, Eglot, and Flycheck. | `consult-imenu` is bound in the active Emacs configuration; Eglot extends Xref. GNU Emacs documents Imenu as the per-buffer definition index and notes that Eglot can supply that index from a language server. [Emacs Imenu](https://www.gnu.org/software/emacs/manual/html_node/emacs/Imenu.html), [Eglot](https://elpa.gnu.org/packages/eglot.html) |
| Semantic, cross-file navigation | **Partly wired** — `nil`, `rust-analyzer`, `clangd`, `typescript-language-server`, and `gopls` are on `PATH`; the checked Emacs source explicitly maps only `nix-ts-mode` to `nil`. | The available servers make a useful semantic workflow plausible, but this audit did not witness active Eglot sessions for Rust, C/C++, TypeScript, Go, or Python. This is not evidence of failure; it is a configuration/use witness still needed. VSCodium explicitly disables Nix and Rust language-server paths, so it is deliberately not the semantic IDE. |
| Repository/topology view across files | **Missing witness** — Mermaid preview/lens extensions are installed, and the workspace contains authored Mermaid diagrams. | These render a supplied architecture model; they do not derive a trustworthy dependency/call graph from the source. No installed graph generator, universal ctags, or maintained code-architecture explorer was witnessed. A diagram should therefore be described as authored/curated, not as discovered truth. |
| Live agent ownership and worktree state | **Wired but text-dense** — Orchestrate's daemon owns canonical state; its `Observe Roles`, `Observe Lanes`, `Observe Worktrees`, and `Query` commands returned live typed records. | The live data includes active claims, recent activities, lane age, worktree status, and scope/reason. It is good governance data but poor at-a-glance visualization because the NOTA responses are long, flat text. The daemon and CLI boundary are documented in [local `orchestrate/ARCHITECTURE.md`](/home/li/primary/orchestrate/ARCHITECTURE.md). |
| Agent activity/event visibility | **Partly wired** — Agent Intercom adapters are declaratively installed for Pi, Codex, Claude, and OpenCode; Codium also has Claude Code, ChatGPT/Codex, and Pi extensions. Aggregator is configured to index Claude project/subagent sources in `MetadataOnly` mode. | These are individual-harness or recovery/metadata surfaces, not one shared event timeline. Current upstream Agent Intercom advertises managed-worker status/logs and lifecycle operations, but the profile's pinned source revision must be checked before relying on a newer upstream capability. [Agent Intercom orchestrator package](https://pi.dev/packages/%40dataforxyz/agent-intercom-orchestrator) |

### Repository and deployment facts that constrain a choice

- The Home profile already treats Emacs and Codium as co-installed choices;
  `preferredEditor` decides `EDITOR`, `VISUAL`, and MIME ownership. A visibility
  addition need not replace Emacs.
- VisualJJ is deliberately pinned and Nix-patched for NixOS. VSCodium
  extensions have marketplace auto-update disabled. This favors a small,
  explicitly declared stack over manual extension experimentation.
- `CriomOS-home`'s roadmap still lists `home-tl6` (wire `CriomOS-emacs` as a
  flake input) as open. The live Home Emacs module therefore remains a
  separately maintained configuration surface; do not assume every capability
  in the sibling Emacs repository is activated through Home.
- The primary worktree was already dirty from other work. JJ read commands
  normally snapshot the working copy, producing operation-log noise. Any
  future read-only dashboard should invoke `jj --ignore-working-copy` when a
  possibly stale snapshot is acceptable, rather than unexpectedly changing
  repository bookkeeping.

## Hypotheses

1. The highest value is not another editor. It is a three-level review ritual:
   **magnitude and deletion first**, then **tree/history placement**, then
   **semantic inspection of only the suspicious symbols**. The required
   components already exist.
2. A curated architecture map will help more than an automatically inferred
   all-language dependency graph at this scale. It can name components,
   contracts, state owners, and generated boundaries — facts static tooling
   commonly misses — while Mermaid already renders it in the auxiliary Codium
   surface.
3. Governance is presently data-rich but visually under-compressed. A read-only
   projection of Orchestrate and JJ would make concurrent work, mass deletion,
   stale claims, and unpushed worktree status much easier to notice without
   granting a dashboard mutation authority.

These are design judgments, not implementation facts; validate them with a
short real-work trial before changing the declarative profile.

## Recommendations

### Smallest useful stack: use what is already deployed

1. **Make VisualJJ the graphical repository lens.** Open it alongside the
   Source Control panel for change-tree placement and multi-change context.
   Treat the built-in Git graph only as a compatibility view: the Home config
   itself says VisualJJ is the actual JJ workflow. VS Code's graph and
   repository panels are useful generic UI concepts, but their maintained
   documentation is Git-specific. [VS Code source control](https://code.visualstudio.com/docs/sourcecontrol/overview)

2. **Put the terminal aggregate before any file diff.** For each substantial
   agent result, first run:

   ```sh
   jj --color=always diff --summary
   jj --color=always diff --stat
   jj --color=always diff --types
   ```

   The first command makes deleted paths visible, the second shows change mass,
   and the third catches file/symlink/type changes. Follow with the existing
   Difftastic-backed `jj diff` only after the aggregate looks proportionate.
   JJ also has `jj op log --op-diff --summary` for *repository operation*
   visibility, not merely code visibility.

3. **Keep Emacs as the semantic microscope.** Use Project/Projectile +
   deadgrep for cross-file condensation, `consult-imenu`/Imenu-list for the
   current file's shape, and Eglot/Xref for definition/reference navigation
   where a server is confirmed active. This directly addresses “cannot inspect
   line by line” without changing the preferred editor. Do not represent
   VSCodium's outline as semantic truth while its language servers are
   intentionally disabled; VS Code's Outline depends on symbols supplied by
   language extensions. [VS Code Outline](https://code.visualstudio.com/docs/editing/userinterface)

4. **Use Orchestrate as the current agent-control ledger.** `Observe Lanes`,
   `Observe Worktrees`, and a bounded `Query` answer who is acting, on what,
   and with which claims. For a human review, capture only a bounded result,
   not an unfiltered historical dump. Agent Intercom can remain the harness
   communication/lifecycle layer, not a second source of governance truth.

This stack is immediately usable: it requires no installation, no editor
migration, and no new source of truth.

### One very small follow-up worth considering

Add a declaratively packaged **read-only `change-radar` command** rather than
a new general-purpose application. It should consume JJ's summary/stat/type
output and render a compact directory tree with:

- changed-file count and line magnitude per top-level directory;
- a dedicated red deletion/type-change section;
- changed generated/lock/config paths as a separate attention group;
- links or copyable paths to open the selected file in Emacs or Codium.

This is a narrow condensation layer over the existing authoritative tools. It
does not parse source semantics, change the repository, or replace JJ. Start
with terminal output; promote it to a GUI only if the behavior proves useful.

### Deeper dashboard opportunity: a local, read-only “work lens”

If the small command succeeds, the next coherent project is a local dashboard
with no write controls. It would join four **separate, labeled** streams:

| Panel | Read-only input | Question answered |
|---|---|---|
| Change radar | `jj --ignore-working-copy diff --summary/--stat/--types` | What changed, how much, and what disappeared? |
| History / risk | bounded `jj op log --op-diff --summary` plus VisualJJ deep link | Was the work rewritten, rebased, or pushed? |
| Work ownership | Orchestrate `Observe Lanes`, `Observe Worktrees`, bounded `Query` | Who is acting now, where, and how old is the claim? |
| Evidence | BEADS state/comments plus selected check outcomes supplied by agents | What was claimed, challenged, and actually verified? |

The dashboard must be a projection, never the owner of state. It should label
its last-refresh time, show stale/unavailable sources rather than inventing
status, and avoid ingesting full private transcripts by default. Its most
valuable alerts are simple: a high deletion ratio, a large unreviewed diff,
an active claim with a stale age, an unpushed worktree, and a task reported
done without a visible test/check witness. A Nix package/home module can make
the implementation reproducible; it should be evaluated and built separately
from activation, per the local Nix workflow.

## Unknowns and verification needed before any change

- Whether VisualJJ's installed version displays the desired directory-level
  diff totals and deletion emphasis in this particular JJ repository. This was
  not visually exercised.
- Which non-Nix Eglot servers auto-start successfully in the deployed Emacs
  configuration, and whether their project roots/indexing time are acceptable
  on the largest repositories.
- Whether `agent-intercom`'s locally pinned revision exposes the newer
  upstream list/status/log features; the source pin, not the current package
  page, is authoritative for that answer.
- Whether Orchestrate offers a stable machine-readable observation form beyond
  its current NOTA replies. A dashboard should consume a documented typed
  contract, not screen-scrape prose.
- The preferred interaction shape: one terminal pane / Emacs buffer / Codium
  side panel / dedicated window. This is a user-experience choice that cannot
  be inferred from configuration.

## Source index

- Local configuration: [VSCodium module](/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix), [Home Emacs module](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix), [Orchestrate profile](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/orchestrate.nix), [Aggregator profile](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/aggregator.nix), [Agent Intercom profile](/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix), [Home roadmap](/git/github.com/LiGoldragon/CriomOS-home/docs/ROADMAP.md).
- Local runtime: `jj 0.40.0`, `difft` 0.19.2, Emacs 30.2, VSCodium 1.112.01907; installed extensions were queried with `codium --list-extensions` on 2026-07-28.
- Maintainer sources: [VisualJJ](https://marketplace.visualstudio.com/items?itemName=visualjj.visualjj), [Jujutsu](https://docs.jj-vcs.dev/latest/cli-reference/), [Difftastic](https://difftastic.wilfred.me.uk/), [GNU Emacs Imenu](https://www.gnu.org/software/emacs/manual/html_node/emacs/Imenu.html), [Eglot](https://elpa.gnu.org/packages/eglot.html), [VS Code Source Control](https://code.visualstudio.com/docs/sourcecontrol/overview), [VS Code Outline](https://code.visualstudio.com/docs/editing/userinterface), [Agent Intercom](https://pi.dev/packages/%40dataforxyz/agent-intercom-orchestrator).
