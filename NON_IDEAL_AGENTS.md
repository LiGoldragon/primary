# primary workspace — non-ideal agent operations

This file is the operational mirror of `AGENTS.md` for accepted, temporary
non-idealities in the primary workspace. The workarounds here are known and
sanctioned: honor them without stalling, and route the proper fix to a bigger
feature or a psyche design decision rather than force-fixing out of an unrelated
lane. When you discover a new non-ideality that is not yours to fix now, append
it here; keep ordinary rules in `AGENTS.md` and the ideal shape in
`ARCHITECTURE.md`.

## Subagent and Protos compaction reminders

- Value using lots of `gpt-5.6-luna` `xhigh` agents in explicit, dedicated, well-scoped tasks; use `gpt-5.6-terra` at `high` or `xhigh` for refactoring and writing code; never spawn a Sol subagent. (Psyche, 2026-08-07; supersedes the earlier terra-for-every-non-trivial line.)
- When `subflows` or `psyche-interraction` is invoked, keep each invoked skill primordial for the whole session, including after compaction.
- After every compaction during Protos-family work, reacquire the current Protos psyche vision from current authority/design documents and live beads before touching code.
- Before any Protos-family or quick-new work, consult and, when a boundary changes, update [the stack segregation tracker](reports/ProtosStackSegregation.md). It is the temporary MVP workaround; terminal correct-new remains protected pending separately ruled resumption.

## Remote builder depends on the Goldragon Wi-Fi

`prometheus.goldragon.criome` may be unreachable unless Wi-Fi is connected to
the `goldragon.criom` access point. Before giving up, connect or reconnect to
that access point and ping the host; if the ping succeeds, retry the remote
builder.

## Stale git linked-worktree registrations linger in backing repos

- **Removing a worktree directory without cleaning the backing repo's git worktree
  registry leaves a prunable stale entry.** The retired `git`/`bd worktree create`
  recipe registered linked worktrees under `agent-worktrees/`; when those
  directories were deleted, the backing repo kept a dangling registration that
  `git worktree list` reports as `prunable`. Clear an existing one in a backing
  repo with `git worktree prune`.

  ```sh
  git -C repos/<repo> worktree list --porcelain   # entries marked prunable are stale
  git -C repos/<repo> worktree prune               # clears them
  ```
- **Proper fix:** create and tear down worktrees only through the orchestrator's
  lifecycle — `RequestWorktree` scaffolds a jj workspace, `ConcludeWorktree`
  (Merged or Rejected) removes it — so no manual directory deletion strands a git
  registration. A periodic sweep can prune the residue across backing repos until
  every legacy git-worktree registration is gone.
- Witnessed 2026-07-16: CriomOS, signal-introspect, and signal-standard each
  carried one stale `prunable` registration pointing at a removed
  `agent-worktrees/` directory.

## Handwritten Nomos/Logos mirror types until self-hosting

- **Every new Nomos object currently gets a corresponding handwritten Rust
  type that closely mirrors its Logos type** — similar structure, but
  different field types: the Nomos-side fields hold promise/unresolved values
  to be evaluated from the Ethos payload, where the Logos-side fields hold
  final concrete values. Maintaining these near-duplicate pairs by hand is a
  sanctioned bootstrap hack (psyche-ruled 2026-08-01,
  `design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md`). Keep the
  pair structurally in step when either side changes; drift between a mirror
  pair is a defect, not a design choice.
- **Proper fix:** the self-hosting loop
  (`design/ProtosEngine/threeLayerNamingAndNomosBootstrap-2026-08-01.md`
  section 8): a specialized Nomos object consumes Ethos type declarations and
  emits both Logos types — the final concrete type and its promise-variant
  mirror — so the Ethos-to-Logos transformation trait is fulfilled without
  handwritten pairs. When that generator lands, the handwritten mirrors
  become its first test fixtures and are retired.
