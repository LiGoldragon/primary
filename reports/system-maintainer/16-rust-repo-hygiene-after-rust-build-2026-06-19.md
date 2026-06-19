# Rust repo hygiene after rust-build — audit and outside research — 2026-06-19

## Scope and question

The question: after creating the shared `rust-build` flake, migrating the first important repos, and documenting `cargo-sweep` target hygiene, is new Rust repo work healthier? Are agents showing signs of hygiene? What does outside practice say, especially for agent work, Nix, and Rust?

I treated "since" as work after the shared helper existed and was being rolled out: commits after `2026-06-18 19:30` local time, plus current filesystem state after the first `cargo-sweep --recursive --maxsize 4GB` run.

## Short answer

The state is better in the repos that were explicitly migrated. It is not yet better as a workspace habit.

The good signs:

- The core migrated chain is clean: `nota-next`, `schema-next`, `schema-rust-next`, `spirit`, `signal-spirit`, `meta-signal-spirit`, `signal-agent`, `meta-signal-agent`, `signal-frame`, `signal-orchestrate`, `meta-signal-orchestrate`, and `orchestrate` now use `rust-build` and no longer hand-call raw Crane source filters in their flakes.
- Recent commits did not show obvious tracked-artifact hygiene failures: no changed `target/` files, no root scratch docs like `PLAN.md`, no `.env`, no backup-copy filenames in the recent diff scan.
- The manual `cargo-sweep --recursive --maxsize 4GB` cleanup worked as intended: it preserved newest artifacts and reclaimed about 31 GiB.

The bad signs:

- Of 42 Rust repos with relevant work since the helper existed, only 12 currently use `rust-build`.
- 26 of those 42 still expose raw `craneLib.filterCargoSources` or `craneLib.cleanCargoSource` in their current flake.
- Five repos had `flake.nix` / `flake.lock` touched after the helper existed but did not adopt it: `cloud`, `mentci-egui`, `meta-signal-introspect`, `meta-signal-message`, and `signal-standard`.
- `signal-standard` is the clearest agent-habit miss: it was bootstrapped after `rust-build` existed and still started with raw Crane policy.
- Target footprint rebounded from roughly 117 GiB after the sweep to roughly 149 GiB after new builds. A fresh dry-run says another 19.47 GiB is already reclaimable. That is normal for active Rust work, but it proves one manual sweep is not enough.

My read: agents comply when a task says "migrate this repo"; they are not yet automatically treating `rust-build` / source pruning / capped target cleanup as default Rust work hygiene. This matches outside agent-engineering guidance: prompts and docs are weaker than gates; standards that matter need automatic checks.

## Local evidence

### Current Rust-source hygiene snapshot

Current scan of Rust flakes under `/git/github.com/LiGoldragon` found the following shape:

| Population | Count |
|---|---:|
| Rust repos with relevant work since `2026-06-18 19:30` | 42 |
| Recent repos using `rust-build` | 12 |
| Recent repos still exposing raw `filterCargoSources` or `cleanCargoSource` | 26 |
| Recent repos whose flake changed after helper existed but did not adopt `rust-build` | 5 |

The five flake-touched misses are the most important hygiene signal because they were not merely old debt:

| Repo | Recent flake-touching commit | Current source-policy state |
|---|---|---|
| `cloud` | `cloud: DigitalOcean compute provider Phase 1 (synchronous Store path)` | raw `filterCargoSources`, broad `type == "directory"` still present |
| `mentci-egui` | `mentci-egui: consume approval flow commands` | raw `cleanCargoSource` |
| `meta-signal-introspect` | `meta-signal-introspect: refresh strict contract stack` | raw `filterCargoSources` |
| `meta-signal-message` | `meta-signal-message: enforce strict schema syntax` | raw `filterCargoSources`, broad `type == "directory"` still present |
| `signal-standard` | `signal-standard: bootstrap shared cross-component standards library` | raw `filterCargoSources`; newly bootstrapped after `rust-build` existed |

### Repos that show clear adoption

The following recently-worked repos use `rust-build` and have `rust-build` in the lock:

| Repo | Evidence |
|---|---|
| `nota-next` | `nota-next: use shared rust-build source policy`; repinned to custom-toolchain-support revision |
| `schema-next` | `schema-next: use shared rust-build source policy`; repinned |
| `schema-rust-next` | `schema-rust-next: use shared rust-build source policy`; repinned |
| `spirit` | `spirit: use shared rust-build source policy`; repinned |
| `signal-spirit` | `signal-spirit: use shared rust-build source policy` |
| `meta-signal-spirit` | `meta-signal-spirit: use shared rust-build source policy` |
| `signal-agent` | `signal-agent: use shared rust-build source policy` |
| `meta-signal-agent` | `meta-signal-agent: use shared rust-build source policy` |
| `signal-frame` | `signal-frame: use shared rust-build source policy` |
| `signal-orchestrate` | `signal-orchestrate: use shared rust-build source policy` |
| `meta-signal-orchestrate` | `meta-signal-orchestrate: use shared rust-build source policy` |
| `orchestrate` | `orchestrate: use shared rust-build source policy` |

This is real improvement, not just documentation. These flakes now route source cleaning through the guard that rejects `target`, `.git`, `.jj`, `.direnv`, and `node_modules` before Crane or repo extras run.

### Target footprint after one sweep and more work

The earlier cleanup run reclaimed about 31 GiB and left the scanned target total near 117 GiB. After subsequent Rust work, the current target footprint is back near the original total:

| Measurement | Value |
|---|---:|
| Current `target/` dirs found | 83 |
| Current total target footprint | 148,896 MiB |
| Fresh `cargo-sweep --dry-run --recursive --maxsize 4GB` reclaimable amount | 19.47 GiB |

Largest current `target/` trees:

| Repo | Size |
|---|---:|
| `mind` | 11,303 MiB |
| `router` | 11,272 MiB |
| `kameo` | 8,755 MiB |
| `spirit` | 7,939 MiB |
| `cloud` | 6,468 MiB |
| `terminal` | 4,959 MiB |
| `criome` | 4,208 MiB |

Important interpretation: this does not mean `cargo-sweep` failed. It means a one-shot sweep is not a control loop. Recent builds can legitimately push a repo above 4 GiB again because `cargo-sweep --maxsize` preserves the newest artifacts. The control loop needs to run periodically or on demand after high-volume build sessions.

### Tracked-artifact and scratch-file scan

A recent-diff scan after `2026-06-18 19:30` looked for:

- changed paths under `target/`;
- root scratch docs such as `PLAN.md`, `NOTES.md`, `ANALYSIS.md`, `DEBUG.md`, `TEMP.md`, `WIP.md`;
- backup/copy files such as `_old`, `_copy`, `_backup`, `.bak`, swap files;
- `.env` files.

Result: no hits in the recent changed-file set.

That is a positive sign: agents are not leaving the most obvious file-artifact trash in commits. The misses are more structural: build-policy adoption and disk hygiene automation.

## Outside research

### Agent work hygiene: prompts are not gates

Salesforce's agentic engineering guidance says the bottleneck moves from generation to verification: code can be produced faster than it can be trusted, so the engineering model must make confidence cheap. Their strongest rule for this audit is: replace prompts with quality gates. A prompt is a request; a gate is an enforced property in the pipeline. This maps exactly to our current state: `skills/rust-discipline.md` now says to use `rust-build`, but agents still touched flakes without adopting it.

Source: Salesforce Engineering, "Maintaining Code Quality at Agent Speed: 7 Patterns" — https://engineering.salesforce.com/maintaining-code-quality-at-agent-speed-7-patterns-for-agentic-engineering/

The `alint` agent-hygiene ruleset names similar failure classes for agent-heavy repos: no tracked artifacts, no root scratch docs, no versioned duplicate files, no debug residue, no model-attributed TODOs. Our recent-diff scan is aligned with those categories and found no obvious tracked-artifact/scratch failures. That supports a narrower conclusion: commit-trash hygiene is better than build-policy hygiene.

Source: `agent-hygiene@v1` — https://alint.org/docs/bundled-rulesets/agent-hygiene/

### Nix source hygiene: filter before hashing, compose filters

Crane's source-filtering documentation says Nix hashes source inputs and irrelevant files cause rebuilds; source filtering removes irrelevant files before hashing. It shows `craneLib.cleanCargoSource` for default Rust/Cargo sources and `craneLib.filterCargoSources` composed with extra filters for data files. Our `rust-build.cleanSource` follows that same composition model but adds a workspace-specific pre-prune guard.

Source: Crane source filtering — https://crane.dev/source-filtering.html

Nixpkgs `lib.cleanSourceWith` is the right primitive for this shape because it composes source filters and applies predicates lazily. The Nixpkgs docs explicitly contrast it with nested `builtins.filterSource`, where intermediate copies are worse. Our `rust-build.cleanSource` wraps `lib.cleanSourceWith`, so the landing is idiomatic.

Source: Nixpkgs source filtering functions — https://ryantm.github.io/nixpkgs/functions/library/sources/

### Rust target cleanup: cargo-sweep matches our preservation requirement

`cargo-sweep` exists for the exact distinction the user asked about: unlike `cargo clean`, it does not remove all build files; its motivation is preserving recent artifacts while limiting target size and managing many projects. It recommends `--dry-run` first and supports recursive cleaning.

Source: cargo-sweep docs — https://docs.rs/crate/cargo-sweep/latest

Cargo itself has been adding cache GC for Cargo home, but the Rust blog explicitly notes target directory cleaning is not yet included and is a future area. That means our current `cargo-sweep` practice is not redundant with stable Cargo behavior.

Source: Rust Blog, "Cargo cache cleaning" — https://blog.rust-lang.org/2023/12/11/cargo-cache-cleaning/

## Is the state better?

Yes, in the important chain that was explicitly remediated. No, as a default behavior across new work.

Better:

- The highest-importance schema/Spirit/orchestrate path has a real shared source-cleaning abstraction now.
- That abstraction has its own source-prune policy check.
- The largest old `target/` burden can be reduced without nuking active builds.
- Recent commits are not obviously tracking build artifacts or scratch junk.

Not better enough:

- New/active repos still start or continue with raw Crane patterns.
- Agents touching flakes are not automatically asking "should this use `rust-build`?".
- Disk pressure returns quickly without a scheduled or habitual sweep.
- The standard currently lives as prose plus a helper, not as an enforced check over changed repos.

## Are agents showing signs of hygiene?

Mixed.

Signs of hygiene:

- The explicit migration work was clean: no local-only inputs, no path flakes, pushed remote refs, no source-filter regressions in migrated repos.
- Recent diffs did not show tracked `target`, scratch docs, backup copies, or `.env` files.
- Some agents clearly ran Nix checks as part of the migration wave; the migrated repos had `nix flake check --no-build` and source-realizing checks.

Signs of missing habit:

- `signal-standard` was bootstrapped after `rust-build` existed but still hand-authored raw Crane source policy.
- `cloud` touched its flake after the helper existed and kept broad directory traversal policy.
- Several strict-contract porting waves refreshed flakes/locks without treating source hygiene as part of the flake touch.
- The target footprint rebound shows agents are building heavily but not cleaning as part of their normal closeout.

The best single sentence: agents are avoiding obvious trash commits, but not yet internalizing build-hygiene abstractions unless the task explicitly says so.

## Recommended next controls

### 1. Add an enforceable scanner, not just prose

Create a workspace scanner that fails when a changed Rust flake uses raw `craneLib.filterCargoSources` or `craneLib.cleanCargoSource` without `rust-build`. The scanner should be able to run in two modes:

- full workspace audit mode for system-maintainer;
- changed-repo/pre-push mode for agents.

This aligns with the external agent-engineering guidance: prompts communicate preferences; gates enforce standards.

### 2. Add a `rust-build` consumer hygiene check

`rust-build` should export a small `hygieneCheck` derivation helper that a consumer can include in `checks`. The check can read the source `flake.nix` and fail on direct raw Crane source-cleaning calls. It will not help repos that have not adopted `rust-build`, but it prevents relapse after migration.

### 3. Migrate the flake-touched misses first

Priority order based on actual post-helper flake touches:

1. `signal-standard` — newly bootstrapped shared contract standard; set the precedent early.
2. `cloud` — active, large `target`, broad directory predicate.
3. `meta-signal-message` — flake touched and broad directory predicate.
4. `meta-signal-introspect` — flake touched, still raw filter.
5. `mentci-egui` — flake touched, raw `cleanCargoSource`.

### 4. Then migrate high-footprint active repos

Next priority by target size and recent activity:

1. `mind`
2. `router`
3. `cloud`
4. `terminal`
5. `criome`
6. `message`
7. `system`
8. `terminal-cell`

The reason is not that `rust-build` shrinks local `target/`; it prevents Nix source traversal through those large trees and standardizes future Rust build setup.

### 5. Put `cargo-sweep` on a timer or closeout checklist

A one-shot sweep is useful but not durable. Options:

- user systemd timer from CriomOS-home: run `cargo-sweep --recursive --maxsize 4GB /git/github.com/LiGoldragon` daily or every few days;
- agent closeout rule: after high-volume Rust build sessions, dry-run then sweep;
- per-heavy-repo cap exceptions: e.g. `spirit` might reasonably use 8 GiB during active migration work.

I recommend a timer, because the rebound happened quickly and asking agents to remember cleanup will fail for the same reason asking them to remember source-policy adoption is failing.

## Bottom line

The remediation was technically correct and clearly improved the repos it touched. The broader agent system is not yet hygienic by default. The next step is to turn `rust-build` adoption and target cleanup from remembered practice into enforceable or scheduled machinery.
