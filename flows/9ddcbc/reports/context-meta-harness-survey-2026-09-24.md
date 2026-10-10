# Context and meta-harness survey

Read-only snapshot collected 2026-09-24 15:04 UTC by an internal exploration
worker delegated from retained Field Medium `9ddcbc`. The worker made no edit,
commit, cleanup, prune, reset, lock, route, wake, seat, message, or deployment.

## Native binding and context evidence

Exact binding:

- Herdr session/pane: `messaging-build/w0:p2`
- terminal: `term_65bef46ad013e44`
- Herdr agent: `field-medium-9ddcbc`
- native thread: `01a0c051-d38e-7d92-a79e-c609ddcbc64b`
- observed state: `working`, `interactive_ready=true`
- model: `gpt-5.6-sol`

`tools/field-census.mjs --overview --json` recorded the binding at
15:04:06.052 UTC. The focused visible-footer collector at 15:04:18.404 UTC
reported harness `codex`, model `gpt-5.6-sol`, effort `medium`, and
`contextPercent=null`. No accepted footer context percentage was visible, so
the actual footer metric is **unavailable**.

The census separately reported 139,086 `lastInputTokens`, 54%, a 258,400-token
window, and arithmetic remainder 119,314 with
`occupancy.status=last-input-proxy` and `exactTokens=null`. Its source is
`thread/read + rollout tail`. This is a last-input proxy, not current resident
context occupancy. Thread cumulative tokens and the account's 10,080-minute
quota are different scopes again. None of these values proves native resident
occupancy, refresh need, an over-threshold condition, or a dead session.

Relevant contracts are `tools/field-census/README.md`,
`flows/0347d0/reports/harness-visual-indicator-inventory.md`, and this seat's
prior declaration in
`flows/9ddcbc/reports/owner-refresh-addendum-2026-09-22.md`.

## Repository and worktree snapshot

The bounded inventory covered Flow, Message, Lojix, CriomOS, and CriomOS Home.
Registered Jujutsu workspace records at observation time were:

- Flow: 5, reported clean
- Message: 10, reported clean
- Lojix: 12, reported clean
- CriomOS: 48, reported clean
- CriomOS Home: 31 records; 20 explicit external worktree paths reported clean

At 15:04 UTC the CriomOS Home source root was dirty only in the four active Flow
deployment paths: `flake.nix`, `flake.lock`,
`modules/home/profiles/min/flow.nix`, and
`checks/flow-service-path/default.nix`. This was the source-critical work owned
by this flow, later published as immutable Home candidate
`c4fa2395fa9a9a143a8955ecaeb3c961a28f5447`.

About 11 Home workspace records exposed no explicit root in `jj workspace
list`; their per-worktree state is **unknown**. Filesystem discovery also found
four Flow and fifteen Message directories beyond registered paths. They are
classified **unknown/unregistered**, never duplicate, obsolete, or abandoned.
The Flow gate directory
`/home/li/wt/github.com/LiGoldragon/flow/mind-sol-6288d1-gate-integration`
was filesystem-visible but absent from that clone's current Jujutsu workspace
list, so its workspace-registration state is unknown.

Repository heads observed at the bounded snapshot were Flow source root
`61d765e4`, Message main `55657f4e`, Lojix main `c4bba4fa`, CriomOS main
`bd6a16da`, and the then-dirty Home branch at parent `8be78063`. These are
timestamped observations, not claims about later heads or deployment state.

## Bounded chronology and evidence grades

- **2026-09-23, design/test:** Mind's transition/hold proposal at
  `flows/6288d1/reports/transition-hold-operational-flow-nexus-proposal.md`
  records an isolated 32-test pass. It explicitly provides no live Herdr or
  deployment proof. The pending-file experiment still lacks a declared
  successor drain.
- **2026-09-24, Flow source/test:** Flow
  `4560453644c095d97d09390819a22e213850986c` passed the configured Prometheus
  no-fallback gate: 9/9 flake checks and 54/54 tests. The retained log hash is
  `062697a45e10d4804a197645f315f2721562b6ea18e0bbebab71ff53faf76b60`.
  This is source/test proof. The Home inclusion gap was later repaired in
  `c4fa2395...`; Lojix deployment remains the executor's separate stage.
- **Message:** the earlier consumer check passed, but the final integrated
  lineage remains unproven. Mind's repin and the `Pending => Parked` guard merge
  remain the gate. The deployed Home-generation-27 Message service is failed;
  that is current runtime state, not candidate deployment proof.
- **Network:** CriomOS `a50e20c` landed NDP/USB policy and `59b3229` pinned Home
  with two focused remote passes. Whole-system evaluation was blocked before a
  derivation because the materialized Lojix JSON uses
  `node.routerInterfaces`, while current source expects
  `node.network.routerInterfaces`. No activation followed.
- **Current deployment boundary:** Lojix records current Home deployment 27,
  CriomOS `cef111...`, generation 1031; current host deployment 4, CriomOS
  `36653a...`. Future Flow, Message, and Network stages each require an
  immutable Lojix request/source record, realized closure/result, independent
  persistent-profile and running-unit readback, live acceptance, and rollback
  witness.

## Evidence commands

The worker used:

- `node tools/field-census.mjs --overview --json`
- `node tools/field-census/harness-visual-indicators.mjs --session messaging-build --pane w0:p2`
- `herdr agent list --session messaging-build`
- `herdr pane list --session messaging-build`
- `jj --repository <repo> --ignore-working-copy workspace list`
- `jj --repository <repo> --ignore-working-copy status`
- bounded `find` inventory under `/home/li/wt`

All context figures, repository states, and worktree counts are observation-time
evidence. Unknown readings remain unknown.
