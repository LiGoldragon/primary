# 28 — lojix M1 reached: the new stack builds + evaluates, online end-to-end

cloud-designer lane, 2026-06-05. Follows the plan in report 27. The psyche's
bar for this round — "bring the whole stack online so that at least we can
build things with it and evaluate" — is **met**. The new schema-derived lojix
daemon evaluates and builds a real NixOS closure end-to-end through its own
Nexus pipeline with real `nix` IO, including a live two-socket daemon-binary
round-trip.

## What is proven (three passing smokes, real `nix` IO)

`lojix/triad-port/tests/build_smoke.rs` (run: `cargo test --test build_smoke
-- --ignored --nocapture`). All three green, 8.33s combined:

1. **`eval_dune_fixture_through_the_engine`** — a System `Eval` deploy driven
   through the engine reached `Deployed`. Real path: SignalArrived →
   RecordDeploySubmitted → ResolveFlakeAuth (`nix flake metadata`) → Building →
   NixEval (`nix eval --refresh --raw <flake>#dune-nspawn-toplevel.drvPath`) →
   Deployed. Produced drv
   `/nix/store/vnqscazqif8…-nixos-system-dune-26.05.20260422.0726a0e.drv`.
2. **`build_dune_fixture_through_the_engine`** — a System `Build` deploy
   reached `Deployed`, realising the closure
   `/nix/store/9id9drl314y7…-nixos-system-dune-26.05.20260422.0726a0e` (a full
   NixOS system). Path adds NixBuild after eval, then finishes (no
   copy/activate).
3. **`daemon_binary_socket_roundtrip_eval`** — the **fully-online** proof:
   spawns the actual `lojix-daemon` binary, which decodes its inline-NOTA
   config, binds both authority-tiered unix sockets, receives an `Eval` deploy
   over the **owner socket** via the length-prefixed frame codec, runs the full
   pipeline, and replies `Deployed`. Exercises process + config decode +
   two-socket bind + frame codec + pipeline + real `nix`.

The target is `github:LiGoldragon/CriomOS-test-cluster#dune-nspawn-toplevel`
— a self-contained `fixtureSystem "dune"` toplevel (fixture horizon baked in),
so no `--override-input` materialization is needed (that is the deferred M3
production work).

## The change set (M1)

Two crates, current engine pins (no streaming-dep bump — see Deferred).

- **meta-signal-lojix contract** (`triad-port/schema/lib.schema`): added
  `FlakeAttribute String` + `build_attribute (Optional FlakeAttribute)` on
  `SystemDeployment`. Lets a deploy name a directly-buildable flake output
  (fixtures / tests / any self-contained closure); absent = the production
  `nixosConfigurations.target` path. Contract regenerated
  (`META_SIGNAL_LOJIX_UPDATE_SCHEMA_ARTIFACTS=1`).
- **daemon** (`triad-port/src/schema_runtime.rs`):
  - **A1 fix** — `DeployPipeline::target_attribute` now returns the
    `build_attribute` override, else the action's production attribute
    (`nixosConfigurations.target.config.system.build.toplevel` /
    `homeConfigurations.<user>.activationPackage`). The old broken
    `{cluster}.{node}` form is gone.
  - **`DeployAction` typed enum** (System action | Home {mode,user}) with
    methods `produces_closure()` / `activates()` / `target_attribute()` —
    replaces what would have been stored bool flags (rust-discipline: no
    flag-soup; verb-belongs-to-noun).
  - **Pipeline termination by action** — `Eval` finishes after eval (drv
    only); `Build` finishes after the realised closure (no copy/activate);
    activating actions run the full chain. This makes a **Build-only
    submission the safe first real test** — it never reaches the still
    addressing-incomplete copy/activate.
  - daemon artifacts regenerated; `cargo build` GREEN; regular `cargo test`
    green (no regressions).
- **tests** — `tests/build_smoke.rs` (the three smokes above).

## Online now vs deferred

**Online (M1):** eval + build of self-contained closures, through the engine
and through the live daemon binary on two sockets. This is "build things with
it and evaluate."

**M2 — deploy to Prometheus's nspawn "VM" (stretch, blocked this session):**
Prometheus is **unreachable from here right now** (ssh + the `nix.prometheus`
cache both time out — WireGuard/mesh down), so no live deploy was possible
regardless of code. M2 also needs a **new nspawn-activation effect**
(`criomos-nspawn create/start <name> <store-path>` over ssh to the criome
domain) — distinct from system-profile activate — plus the A3 addressing fix
(criome domain, not bare node). The legacy `nspawn-dune-on-prometheus` is the
baseline to match.

**M3 — production node deploy (deferred cutover work):** the full projection +
materialization + `--override-input` port for `nixosConfigurations.target`,
the proper system activate (A2: thread closure path + `switch-to-configuration`),
and addressing (A3). Report 26's gap list; the parity-for-cutover bar.

**Deferred, noted:** the engine-dep streaming bump (triad-runtime/schema-rust-
next/schema-next moved forward with the streaming substrate; orthogonal to
building a closure, kept off M1 to change one variable at a time); real
sema-engine/redb persistence (in-memory fine for M1 per `jxi9`); surfacing the
realised store path in the `Deployed` reply (today it carries only the
deployment id + marker; the path is in the engine/event log).

## Action needed — the triad-port trees are UNTRACKED (persistence risk)

`~/wt/github.com/LiGoldragon/{lojix,signal-lojix,meta-signal-lojix}/triad-port`
are **plain directories with no `.git`/`.jj`** — not real worktrees. The entire
schema-derived rewrite plus this M1 work lives there untracked. It survives
across sessions (it was there when this session started) but is one `rm` from
loss and is not on any branch. This needs **operator integration**: land each
`triad-port` tree on a feature branch in its `/git/.../<repo>` repo (per the
main-and-next lane split, operators own that integration). Flagging
prominently; the work is real and green and should not stay stranded in
untracked dirs.

## Status

M1 complete and green. Next concrete steps, in order: (1) get the triad-port
trees onto real branches (persistence); (2) when Prometheus is reachable, build
M2's nspawn-activation effect and attempt the live `dune` nspawn deploy through
the new stack; (3) the streaming-dep bump for day-one streaming; (4) M3
materialization toward production cutover.
