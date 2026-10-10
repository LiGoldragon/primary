# Stale lock 3847 stewardship witness

Captured 2026-09-25 before releasing Orchestrate lock 3847, under Psyche
High 38de5b's 2026-09-25T15:20:58Z authorization for Mind's delegated
steward.

The lock was:

```
3847 MindLowFlowLaunchAdapter e798f3
/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/crates/flow-nexus/src/codex.rs
/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/crates/flow-nexus/src/herdr.rs
/home/li/wt/github.com/LiGoldragon/flow/mind-low-launch-e798f3/crates/flow-nexus/src/prompt_modules.rs
```

The owner route was stale and no matching owner process was present. The
worktree's current change was `f2bba1a1121e`; its parent was
`34ddd0dac359` (`Wire selected testing skills into native modules`). The only
working-copy difference was `result`, a symlink last modified
2026-09-21T19:20:51Z, pointing at
`/nix/store/70hdjaidc6mqvmfk4d49kkpn4f4j2hpi-flow-workspace-test-0.3.0`.

No source file or authored state in that worktree was changed by this
stewardship step. This retained witness precedes release; it allows the stale
checkout and its lineage to be recovered without treating its build-result
symlink as authored work.

After this capture, Psyche High 38de5b reported that the stale `result` state
was committed and pushed as found on `flow/e798f3-launch-adapter`, revision
`fd1dae69`. The release therefore did not discard the stale checkout's only
working-copy difference.
