# 80 — "do it all" Tier 2 cascade: Magnitude + AtLeast renames + small method splits, redeployed

*Five-repo coordinated cascade for the wire-breaking renames I'd
previously surfaced as needing user approval. All committed,
pushed, and the home generation is live on the new pipeline.*

---

## Final state — all wired through

| Layer | Pin / state | Verified |
|---|---|---|
| User's `lojix-cli` in PATH | new `lojix-cli-0.1.0` store binary | `which lojix-cli` resolved to it |
| Live home generation | new Home Manager generation | New gen activated cleanly |
| `CriomOS-home/flake.lock` `lojix-cli` pin | `e3090eaf52` (audit Tier 2) | `nix flake metadata` confirmed |
| `horizon-rs` main | `4a17d4799f1a` | pushed |
| `lojix-cli` main | `e3090eaf5262` | pushed; home consumes via flake input |
| `goldragon` main | `9894482f64ce` | pushed; consumed at deploy time |
| `CriomOS` main | `d281fdf314d2` | pushed; OS modules renamed |
| `CriomOS-home` main | `2e5e450e033a` | pushed; home modules renamed |

The redeploy used `nix run --refresh github:LiGoldragon/lojix-cli/main` so the *new* `lojix-cli` (with new `horizon-rs` Cargo.lock pin) was the one running the deploy — it generated horizon JSON with the new field shape, which the new CriomOS-home modules consumed correctly.

---

## What landed

### `horizon-rs` `4a17d479` — wire renames + small extraction

| Change | Before | After |
|---|---|---|
| Magnitude variants | `None`, `Med` | `Zero`, `Medium` |
| `AtLeast` field names | `at_least_min`, `at_least_med`, `at_least_large`, `at_least_max` | `min`, `medium`, `large`, `max` |
| serde-default helpers | `Magnitude::default_none` | `Magnitude::default_zero` |
| Magnitude::None handling in horizon::project | `matches!(trust, Magnitude::None)` | `matches!(trust, Magnitude::Zero)` |
| Lid-switch policy in `NodeProposal::project` (~17 lines of inline if/else) | inline | extracted to `BehavesAs::lid_switch_policy() -> LidSwitchPolicy` (private struct, three named slots: `on_battery`, `on_external_power`, `docked`) |

### `lojix-cli` `e3090eaf` — pin bump + small extraction

| Change | Before | After |
|---|---|---|
| Cargo.lock `horizon-lib` rev | `95e615a5` | `4a17d479` (precise pin; `nota-codec`/`derive` held back to non-tip) |
| Builder-target resolution in `DeployState::run` (~17 lines) | inline `match` block | extracted to `DeployRequest::resolve_builder_target(&self, &Horizon) -> Result<Option<SshTarget>>` |

### `goldragon` `9894482f` — datom.nota wire updates

Two surgical token changes:
- balboa's `size`: `None` → `Zero` (line 22)
- bird's per-user trust: `Med` → `Medium` (line 246)

The dozens of other `None` tokens in datom.nota are `Option<T>::None` (for `super_node`, `model`, etc.) — those stay.

### `CriomOS` `d281fdf3` — Nix module field accessor renames

`atLeastMin`/`atLeastMed`/`atLeastLarge`/`atLeastMax` → `min`/`medium`/`large`/`max` across:
- `modules/nixos/edge/default.nix`
- `modules/nixos/metal/default.nix`
- `modules/nixos/nix.nix`
- `modules/nixos/normalize.nix`
- `modules/nixos/users.nix`

55 occurrences as `.atLeast<X>` field accessors → renamed to `.min`/`.medium`/`.large`/`.max`. Three remaining occurrences were in comments — also updated to the new field names for consistency.

### `CriomOS-home` `fa0bc1ad` then `2e5e450e` — module renames + lojix-cli pin bump

- Same `atLeast*` → new-field rename across 12 nix files in `modules/home/`.
- Then `flake.lock` updated: `lojix-cli` `cf5dc347` → `e3090eaf52`.

19 occurrences as field accessors + 1 comment.

---

## How the cascade was tested live

The deploy command:

```sh
nix run --refresh github:LiGoldragon/lojix-cli/main -- \
  '(HomeOnly goldragon ouranos li \
    "/git/github.com/LiGoldragon/goldragon/datom.nota" \
    "github:LiGoldragon/CriomOS-home/main" \
    Activate None None)'
```

`--refresh` forced the resolver to fetch the latest `main` of `lojix-cli` (e3090eaf, which pins horizon-rs at 4a17d479). Without it, the cached old `lojix-cli` would have generated the *old* horizon JSON shape (`atLeastMin/atLeastMed/...`), which the new CriomOS-home modules would have rejected.

Output stream confirmed:
- `horizon` flake input overridden with the freshly-generated `horizon.json` (new field shape)
- 5 derivations built (home-manager-path, fontconfig conf, activation script, files, generation)
- All 18 home.activation steps completed cleanly (`linkGeneration`, `installPackages`, `dconfSettings`, `mergePiModels`, `reloadSystemd`, `vscodeProfiles`, etc.)
- Final generation: new Home Manager generation

Post-deploy verification: `which lojix-cli` resolves to the new `lojix-cli-0.1.0` store path, and re-running with `Build` mode against the same Nota request returns the same generation hash — the installed binary is the new one.

---

## What's still open (and filed)

### `primary-cde` (P3) — FullOs deploy hasn't happened yet

CriomOS modules are committed at `d281fdf3`, but the running *OS* is still on the previous generation built against the old field names. Until the next `FullOs Switch` deploy, the OS-level modules are unchanged on disk. Next OS deploy picks up the new modules + new horizon shape — should succeed because all the pieces are aligned.

Recommended invocation when ready:
```sh
lojix-cli '(FullOs goldragon ouranos \
  "/git/github.com/LiGoldragon/goldragon/datom.nota" \
  "github:LiGoldragon/CriomOS/main" \
  Switch prometheus None)'
```

`builder = prometheus` per `skills/system-specialist.md` §"Cluster Nix signing" — the cache node builds + signs, ouranos substitutes the signed closure. `builder = None` is broken for cross-host deploys.

I held off on running this myself because `FullOs Switch` is invasive (modifies the running system) and the user hadn't explicitly authorised an OS-level deploy in the current session.

### `primary-rb0` (P3) — horizon-rs test coverage backfill

`rust-discipline.md` §"Tests live in separate files" implies one test file per source file. `horizon-rs/lib/tests/` still only contains `magnitude.rs`. The other 11 source files (`address`, `cluster`, `error`, `horizon`, `io`, `machine`, `name`, `node`, `proposal`, `pub_key`, `species`, `user`) have no test files. Backfill is its own multi-day work.

The `horizon-rs` flake-check breakage (`primary-4mn`) also keeps `nix flake check` from running — fixing that is prerequisite to any CI gating.

### Items from retired report 75 no longer surfaced

Report 75 is now summarized in `reports/system-specialist/96-system-specialist-agglomerated-archive.md`; its surfaced items I labelled "needs human approval" are now *done* (Magnitude renames, AtLeast field renames, the smaller method-extraction items). The other "architectural smell" items I listed in 75 are either:
- Done in this session (`SshTarget` typed fields landed in earlier audit follow-up; `lid_switch_policy` extracted; `resolve_builder_target` extracted)
- Or genuinely not worth doing (the rest of `NodeProposal::project` and `DeployState::run` are linear pipelines whose data dependencies don't decompose cleanly; splitting buys only LOC reduction at the cost of structural risk)

---

## Files touched

- `/git/github.com/LiGoldragon/horizon-rs/lib/src/magnitude.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/horizon.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/proposal.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/node.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/user.rs`
- `/git/github.com/LiGoldragon/horizon-rs/lib/tests/magnitude.rs`
- `/git/github.com/LiGoldragon/lojix-cli/Cargo.lock`
- `/git/github.com/LiGoldragon/lojix-cli/src/deploy.rs`
- `/git/github.com/LiGoldragon/goldragon/datom.nota`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/edge/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nix.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/normalize.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/users.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/*.nix` (4 files)
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/*.nix` (5 files)
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/max/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`
- BEADS `primary-rb0`, `primary-cde` (filed)
