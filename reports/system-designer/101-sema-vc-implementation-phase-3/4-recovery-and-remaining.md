# 101/4 — Recovery dossier: exact state, in-flight work, and the remaining steps

*Written under an imminent session-usage cutoff so any future session (this
lane or another) resumes from this file rather than forensics. Everything
below is verified as of writing; trust the branch heads over memory.*

## The branch stack (all pushed, all adversarially reviewed)

| Repo | Branch | Head | State |
|---|---|---|---|
| nota-next | `structural-shape-extension` | `e92a9295` | approved; integration bead filed |
| schema-next | `typed-macro-library` | `d7b34a24` | approved (sibling of the identity line; deps on the nota-next branch) |
| schema-next | `schema-content-identity` | `3e72902d` | approved |
| schema-next | `storage-family-declarations` | `89fe33a9` | approved; sits on `schema-content-identity` |
| schema-rust-next | `record-family-emission` | `9892d59d` | approved |
| triad-runtime | `tailnet-listener` | `1b5d0f17` | approved |
| sema-engine | `versioned-family-identity` | `53426b14` | approved |
| sema-engine | `versioned-fold` | `3593ffe6` | approved (tamper commit); fix-round adds 2 witnesses |
| mind | `memory-graph-family` | `313b7c87` | approved (rebased onto `b9cd8c23`) |
| spirit | `versioned-store-pilot` | `a50cc732` | needs-fixes → fix-round in flight; flake.lock refreshed/pushed by orchestrator; **nix build blocked, fix known (below)** |
| mirror, signal-mirror, meta-signal-mirror | `main` (greenfield) | `46193e3b` / `d06dd7bd` / `fa96dc37` | needs-fixes → fix-round in flight (two proven wedge bugs) |

## In-flight fix-round (run `wf_8b2831ee-e40`), may be cut by the limit

Three fix agents + re-reviewers. If cut, their partial work is in these
workspaces as jj commits/working copies — inspect with `jj log`/`jj diff`
before re-dispatching, and brief continuations on the diff, not from scratch:

1. **mirror-fixes** — repos `/git/github.com/LiGoldragon/mirror` (+
   signal-mirror), on main. Closing: (a) crash-window re-send wedge — novel
   remainder must be computed against loaded known rows (digest-verified)
   with a head-only re-advance when the entry remainder is empty
   (sema-engine rejects empty commits — skip the entry transaction);
   (b) retire-then-re-register wedge — resume the surviving chain on
   re-registration or refuse typed; plus cheap advisories (bounded
   `observed_tcp_peers`, StoreName `/` validation, typed CLI/config errors,
   dead SEMA meta verbs routed-or-deleted, drop signal-mirror's unused
   thiserror, pin the `mirror:sema` store name with a test). The prior
   reviewer's reproduction driver was at `/tmp/mirror-crash-witness`.
2. **spirit-fixes** — workspace
   `/home/li/wt/github.com/LiGoldragon/spirit/versioned-store-pilot`.
   Closing: sema-engine Cargo pin bump `39991c18 → 3593ffe6`;
   mutation/retraction log-coverage witnesses in `tests/versioned_store.rs`;
   migration crash-window documentation; typed migration-marker key
   constructor.
3. **tamper-fixes** — workspace
   `/home/li/wt/github.com/LiGoldragon/sema-engine/versioned-fold`.
   Closing: behavioral witnesses for `CheckpointRowMissing`
   (engine.rs:1347) and `SegmentMissing` at its load-path raise site
   (engine.rs:1349-1354), per the reviewer's spelled-out construction in
   tests/tamper.rs.

## The spirit nix-build fix (diagnosed, not yet applied — needs the fix-round to land first)

`nix build .#store-migration` fails: the flake's `patchedCargoLock` step
(flake.nix:285-289) strips all LiGoldragon git `source` lines from
Cargo.lock, and the lock currently carries TWO `nota-next` entries (spirit's
own dep on `structural-shape-extension` at flake/Cargo.toml; everything else
on `main`), which collapse into "package `nota-next` is specified twice".
Nothing in spirit's graph needs the branch (the new derive forms are
consumed by schema-next@typed-macro-library, which is NOT in this graph —
storage-family-declarations is a sibling based on schema-content-identity).
**Fix recipe** (apply in the spirit workspace AFTER the fix-round agent is
done there, then build, then push):

1. `Cargo.toml:62`: `nota-next = { git = ..., branch = "main", optional = true }`.
2. `flake.nix:12-13`: input `nota-next-source.url = "github:LiGoldragon/nota-next"` (main).
3. `flake.nix:171`: update the `--replace-fail` match string to the
   branch-main form of the dependency line.
4. `cargo update -p nota-next`, run `cargo test --features nota-text`
   (quick re-verify), `nix flake lock`, then
   `nix build .#store-migration --no-link` (nix works in the orchestrator
   shell, NOT in agent sandboxes).
5. Commit + `jj bookmark set versioned-store-pilot -r @-` + push.

Note: once the operator integrates nota-next@structural-shape-extension into
nota-next main (bead already filed), this distinction dissolves entirely.

## Remaining arc items after the fix round

1. Re-review verdicts land → stitch fix-round chapter into this directory
   (5-fix-round.md), update this dossier's table.
2. Apply the nix fix above; prove `packages.store-migration` builds.
3. File the close-out beads: (a) operator integration of the full branch
   stack in order — nota-next → schema-next ×3 → schema-rust-next →
   triad-runtime (with lojix/message PeerIdentity arms) → sema-engine ×2 +
   mind together (layout-3 reset for mind.sema; orchestrate/persona/router
   storage_kernel residue migrations ride this) → spirit pilot (with the
   production migration run: `spirit-migrate-store` BEFORE the new daemon
   opens the store); (b) system-operator deploy of mirror-daemon on ouranos
   (CriomOS module, tailnet bind, configuration via
   mirror-write-configuration); (c) production shipper actor (component-side;
   test fixture exists in mirror/tests/end_to_end_arc.rs); (d) TCP listener
   tier emission in schema-rust-next (the mirror's hand-wired ingress is the
   template; also honor meta_socket_mode from configuration); (e)
   PortableCheckpoint byte form into sema-engine; (f) nota-next brace-map
   structural shape so stream+family bodies drop their precedent-bound
   string-keyed field walks (v0n6 residue); (g) RecordKey domain-key |
   identifier sum type; (h) guardian-journal v2 history fold-forward
   (optional, psyche's call); (i) coordinated rename slice for the
   crate-prefixed daemon nouns (MirrorEngine/SpiritDaemon idiom vs
   C-CRATE-PREFIX).
4. Meta-report 101 frame (0-frame-and-method.md) + final arc synthesis;
   spirit-record realization notes; release the lane claims.

## Orchestration lesson (for any agent running multi-agent builds here)

When a session-usage cutoff looms, interrupted sub-agents leave worktree
state but lose their context; continuation agents pay a real re-absorption
cost (hundreds of thousands of tokens this arc). Soften before the cut:
keep briefs self-contained, have agents commit early and often (jj
workspaces made recovery possible at all), and when the limit is near, stop
dispatching and write the recovery dossier first. Do not claim recovery is
free; it is cheaper than restarting, not cheap.
