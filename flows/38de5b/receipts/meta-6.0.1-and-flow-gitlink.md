# meta-signal-flow 6.0.1 and flow gitlink bump

Flow 38de5b, subflow receipt, 2026-09-25.

## 1. meta-signal-flow 6.0.1

- Base: main 4748cfa (6.0.0). Fresh clone in scratchpad `meta-signal-flow-38de5b-fable`; Orchestrate lock 6442 acquired and released.
- Change: `ethos/signal.ethos` line 2 no longer imports `RecipientDisposition` from `signal_flow` (no such type; unused).
- Regeneration: `src/generated/signal.rs` is byte-identical. Imports emit nothing into the generated Rust, and build.rs regenerates with the pinned ethos-zero `4bf73ca` and `assert_eq!`s against the committed file; that check passed.
- `cargo test --features datom`: 5 passed, 0 failed.
- Version: 6.0.0 -> 6.0.1. Rule (versioning skill): bump the surface changed by public behavior, wire, storage, package or deployment. The package source changed; the wire and the generated types did not. So this is a patch bump.
- Landed: main f715883 (`git ls-remote origin refs/heads/main` = f715883459361ee6604ae0f2c29ea4a5ff4cf407).
- `git grep RecipientDisposition` at f715883 returns nothing.

## 2. /home/li/primary/flow

- Kind: **submodule gitlink**. `git ls-files -s flow` gives mode 160000 at 42b98ba. The path is a nested clone with its own `.git` directory (origin `LiGoldragon/flow`). Primary has **no `.gitmodules`**, so this is an orphan gitlink, not a registered submodule, and `git submodule update` would not manage it.
- Bump: the brief read 8f8a71a from ls-remote. By the time of the fetch, main had advanced to 28a78d2 ("Flow 0.9.0: Replace, LaunchStatus and Observe.Launch"), with 8f8a71a as its ancestor. The nested clone was fetched, checked out `main` and fast-forwarded to 28a78d2, and the gitlink was committed in primary: "primary: bump flow gitlink to current main".
- Recommendation: the review (reports/ethos-review.md) and the audits call the path a stale gitlink or nested clone and return it to the main flow as a Primary-structure question. None of them recommends pointing it at /git/github.com/LiGoldragon/flow. Only the bump was done.
- Remaining risk: the gitlink will go stale again unless something re-bumps it. Registering it in `.gitmodules`, removing it, or replacing it with a pointer is for the main flow to decide.
