# 27 — Bringing the new lojix stack online: milestones + execution plan

cloud-designer lane, 2026-06-05. Psyche directive: "bring this new logic
stack online if you can ... at least we can build things with it and
evaluate ... you can even design a way to use the Prometheus [VM] ... maybe
you can actually try a deploy to it." Effort: ultracode. Intent captured
this turn: `nhwv` (raw/pretty is new-stack-only), `jxi9` (build-and-evaluate
milestone + Prometheus-VM target).

This plan supersedes report 26's "fix everything for cutover" framing with a
**staged** one: the psyche's bar for THIS round is *buildable + evaluable*,
not production-durable. The investigator finding (Prometheus's "VM" is
nspawn, and a self-contained fixture closure exists) makes a real build
reachable WITHOUT report 26's largest hole (the materialization subsystem).

## The key unlock — a self-contained buildable closure

`github:LiGoldragon/CriomOS-test-cluster#dune-nspawn-toplevel` is a
`fixtureSystem "dune"` → `config.system.build.toplevel`
(`CriomOS-test-cluster/flake.nix:202-215`). Its per-node identity (the
fixture horizon `fixtures/horizon/dune.json`) is **baked into the flake**, so
it builds with a plain `nix build <flake>#dune-nspawn-toplevel
--no-link --print-out-paths` — **no `--override-input horizon` materialization
needed.** This is exactly the invocation the new daemon's `run_nix_build`
already issues (`schema_runtime.rs:1143-1153`).

Contrast the production path: `<CriomOS>#nixosConfigurations.target.config.
system.build.toplevel` + `--override-input horizon <projected.json>`
(`lojix-cli/build.rs:181-186`, `artifact.rs`). The node identity comes from
the override, not the attribute. That materialization subsystem is the
**production-cutover** work (report 26 gap 1/2), deliberately deferred here.

## Prometheus "VM" = nspawn, and a boot harness already exists

Per the investigation (report a4749601): Prometheus (`prometheus.goldragon.
criome`, the `LargeAiRouter`/large-ai-center role per 6njo) has **no qemu/
microvm VM**; its "VM capability" is **systemd-nspawn / `nixos-container`**
(`criomos-nspawn`, enabled by `size.large && behavesAs.center`). The proven
boot path is `CriomOS-test-cluster/scripts/nspawn-dune-on-prometheus`: build
`dune-nspawn-toplevel`, ssh to Prometheus, `criomos-nspawn create dune
<store-path>` → `start` → poll `shell dune hostname` → assert → teardown.
ssh route to Prometheus is configured (ssh config, known_hosts, /etc/hosts,
WireGuard `5::5`); WG liveness unverified (read-only). nspawn activation is
`criomos-nspawn`, NOT `nix-env`/`switch-to-configuration`.

## Milestones

### M1 — build + evaluate (the psyche's stated bar) — IN PROGRESS

Goal: the new daemon evals + builds a real, self-contained NixOS closure
(`dune-nspawn-toplevel`) end-to-end through the full stack — CLI → owner
socket → daemon → Nexus deploy pipeline → real `nix` IO → store path.

Change set (current pins; no engine-dep bump — see Deferred):

1. **meta-signal-lojix contract** (`triad-port/schema/lib.schema`): add
   `FlakeAttribute String` + `build_attribute (Optional FlakeAttribute)` on
   `SystemDeployment`. Honest, minimal extension: lets an operator name an
   exact flake output to build (fixtures, tests, direct closures); absent =
   the production `nixosConfigurations.target` path. Regenerate the contract.
2. **Fix A1** (`schema_runtime.rs` `target_attribute`): if `build_attribute`
   present → use it directly (`<flake>#<attr>`); else System →
   `nixosConfigurations.target.config.system.build.toplevel`, Home →
   `homeConfigurations.<user>.activationPackage`. (Removes the broken
   `{cluster}.{node}` form.)
3. **Pipeline termination by SystemAction** (`decide_effect_completion`):
   `Eval` → finish after eval (drvPath only); `Build` → finish after build
   (no copy/activate); `Switch/Boot/Test/BootOnce` → full chain. Carry the
   raw `SystemAction` on `DeployPipeline`. This makes a **Build-only
   submission the safe first real test** — no copy/activate, which are still
   addressing-broken.
4. Regenerate daemon artifacts + `cargo build` GREEN.
5. **Smoke test:** run the daemon on two `/tmp` sockets, send a System
   `Build` submission (`flake = github:LiGoldragon/CriomOS-test-cluster`,
   `build_attribute = dune-nspawn-toplevel`) via the CLI, observe
   FlakeAuth → Eval → Build → store path in the reply. (Local build; this
   machine reaches the Prometheus nix cache.)

### M2 — deploy to Prometheus's nspawn "VM" (the stretch — "could be cool")

Boot the built `dune-nspawn-toplevel` as an nspawn guest on Prometheus via
the new stack. Needs a new **nspawn-activation effect** (`criomos-nspawn
create/start` over ssh to the criome domain) — distinct from the system-
profile activate. Requires fixing addressing (A3: criome domain, not bare
node) + a live Prometheus. The legacy `nspawn-dune-on-prometheus` is the
baseline to match. Gated on M1 + live-host reachability.

### M3 — production node deploy (the real cutover work) — DEFERRED

The full projection + materialization + `--override-input` port for
`nixosConfigurations.target`, plus the proper system activate (A2: thread
closure path + `switch-to-configuration`) and addressing (A3). This is
report 26's gap list and the parity-for-cutover bar (tvbn/fe2j). Not part of
"build + evaluate."

## Deferred (explicitly out of M1, noted to the psyche)

- **Engine-dep refresh (streaming).** triad-runtime/schema-rust-next/
  schema-next moved forward with the streaming substrate (triad-runtime
  `de33226` streaming subscription runtime + `9708fc3` token registration;
  schema-next stream-lifecycle metadata; schema-rust-next streaming support).
  lojix is pinned to the pre-streaming commits. Streaming is **orthogonal to
  building a closure**, so M1 stays on current pins (one variable at a time).
  Bumping for day-one streaming is a clean follow-on after M1 is GREEN.
- Real sema-engine/redb persistence (in-memory is fine for M1 per `jxi9`).
- The report 26 runtime-state gaps (demoting live-set, rollback ring,
  durable in-flight) — production-cutover, not build+evaluate.

## Status

- M1 change set being implemented this session; baseline `nix eval` of the
  dune drvPath running to confirm target + network reachability.
- Reports 26 (completeness audit) + this (execution plan) bracket the work:
  26 says what a full cutover needs; 27 says what "build + evaluate" needs
  now and what is deferred.
