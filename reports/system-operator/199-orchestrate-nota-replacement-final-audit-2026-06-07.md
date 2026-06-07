# Orchestrate NOTA Replacement Final Audit - 2026-06-07

## Question

Can the real `/git/github.com/LiGoldragon/orchestrate` component start replacing the current `/home/li/primary/tools/orchestrate` helper if the replacement surface is the one-argument NOTA CLI, not argv compatibility?

## Short Answer

The real component is ready for a controlled NOTA pilot of the core orchestration operations:

- `Claim`
- `Release`
- `Handoff`
- `Observe`
- `Submit`
- `Query`
- meta `Create`

It is not yet ready to replace the current primary helper for every agent without either preserving or consciously retiring the helper-only conveniences:

- managed daemon startup instead of helper lazy-start
- release guard / `verify-jj`
- status rendering plus beads listing
- updated primary documentation with NOTA examples

The highest-risk gap is **release guard bypass**: direct `(Release (...))` works, but it does not run the primary helper's jj safety check that refuses release when a claimed repo still has unresolved local-only push bookmarks.

## Tested Surfaces

### 1. Full Rust Test Suite

Command:

```sh
CARGO_BUILD_JOBS=2 cargo test --locked
```

Result: passed.

Coverage observed:

- daemon and CLI socket integration
- claim/release/handoff/conflict behavior
- dynamic role creation
- repository refresh tests
- legacy lock import
- ordinary/meta/upgrade socket rejection tests
- handover mirror tests
- generated schema contract checks

### 2. Full Nix Flake Check

Command:

```sh
nix flake check --max-jobs 1 --cores 2
```

Result: passed.

The check was already cached after the earlier `0.3.1` fix, but it still evaluated every package/check derivation and reported all checks passed.

### 3. Manual Disposable Daemon Smoke

I started `target/debug/orchestrate-daemon` against a temporary workspace with:

- fresh `orchestrate.redb`
- temporary ordinary/meta/upgrade sockets
- temporary `reports/`, `repos/`, and `orchestrate/roles.list`

Important NOTA wire-shape finding:

- `NotaRecord` structs are untagged positional records.
- Daemon config is:

```nota
([store] [ordinary-socket] [meta-socket] [upgrade-socket] [workspace] [git-index])
```

- A role claim is:

```nota
(Claim (system-operator [(Path [/tmp/scope])] [reason]))
```

not:

```nota
(Claim (RoleClaim ...))
```

This matters for agent documentation.

### 4. Manual Deep Sandbox

The successful deep sandbox did all of the following through the real binaries and NOTA text:

1. Started a disposable daemon.
2. Sent owner/meta:

```nota
(Create (orchestrate-audit-role Codex))
```

3. Claimed a scope:

```nota
(Claim (system-operator [(Path [/tmp/.../deep-scope])] [deep audit claim]))
```

4. Probed conflict from another role and received `ClaimRejection`.
5. Handed the scope to the dynamic role and received `HandoffAcceptance`.
6. Submitted activity and queried it back with:

```nota
(Submit (orchestrate-audit-role (Path [/tmp/.../deep-scope]) [activity probe]))
(Query (10 [(RoleFilter orchestrate-audit-role)]))
```

7. Verified lock projection contained:

```text
/tmp/.../deep-scope # handoff probe
```

8. Killed and restarted the daemon using the same redb store.
9. Observed the dynamic role and handed-off claim persisted after restart.
10. Released the dynamic role and verified its lock file was empty.

Representative successful replies:

```nota
(RoleCreated (orchestrate-audit-role Codex [/tmp/.../persona-role-orchestrate-audit-role-reports] [/tmp/.../workspace/reports/orchestrate-audit-role]))
(ClaimRejection (operator [((Path [/tmp/.../deep-scope]) system-operator [deep audit claim])]))
(HandoffAcceptance (system-operator orchestrate-audit-role [(Path [/tmp/.../deep-scope])]))
(ActivityList ([(orchestrate-audit-role (Path [/tmp/.../deep-scope]) [activity probe] 1780838437288900963)]))
```

## Current Helper Versus Real Component

### Covered by real component

The component now covers the core stateful orchestration engine:

- claim state in redb
- role registry
- dynamic role creation
- lock projection
- conflict detection
- handoff
- release
- activity submit/query
- ordinary/meta socket split
- schema freshness checks
- daemon restart persistence

### Still helper-only

The primary `tools/orchestrate` helper still owns:

- argv convenience parsing
- lazy daemon build/start
- `status` rendering as lock-file sections
- `bd list --status open --limit 20`
- `verify-jj`
- release guard that calls `verify_jj::release_guard(...)` before allowing release
- BEADS-scope claim rejection
- current user-facing usage text in `orchestrate/AGENTS.md`

The user clarified that argv compatibility is not desired. That removes one gap. The other helper-only items still matter because they are behavior, not syntax.

## Readiness Judgment

### Ready Now

Ready for controlled use as the real NOTA component in a pilot:

- start daemon explicitly with a known config
- send NOTA operations directly
- keep current `tools/orchestrate` available as fallback
- do not globally instruct all agents to use direct NOTA release yet

### Not Ready For Global Replacement Yet

Not ready to replace `/home/li/primary/tools/orchestrate` for all agents until these are addressed:

1. **Managed daemon service.**
   The compatibility helper currently lazy-starts the daemon. A real switch needs a user service or equivalent stable daemon lifecycle.

2. **Release safety.**
   Direct NOTA `(Release (...))` bypasses `verify-jj`. Either release guard becomes a real orchestrate/meta-signal policy operation, or primary keeps a separate explicit release-safety command and agent docs require it.

3. **Status expectations.**
   `(Observe (Roles))` and `(Observe (Lanes))` return typed state, but not the old lock-section rendering or beads list. If agents still need beads in the same command, a separate command must provide it.

4. **Documentation.**
   `orchestrate/AGENTS.md` still teaches the current helper syntax. Before switching agents, it needs direct NOTA examples and the untagged-struct reminder.

## Recommended Switch Plan

1. Add a managed user service for `orchestrate-daemon`.
2. Add the installed real `orchestrate` binary to the relevant Home profile.
3. Document the actual NOTA calls:

```nota
(Observe (Roles))
(Observe (Lanes))
(Claim (system-operator [(Path [/git/github.com/LiGoldragon/orchestrate])] [work reason]))
(Release (system-operator))
```

4. Keep `tools/orchestrate` as fallback for one short transition.
5. Do not retire helper release behavior until `verify-jj` has an explicit replacement or a conscious removal decision.

## Final Recommendation

Start using the real component in a controlled pilot now. Do not make it the universal replacement for every agent until daemon lifecycle and release safety are wired into the system.
