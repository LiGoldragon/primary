# Flow-only deployment gate

Observed by retained Field Medium `9ddcbc` under Field High `9e735b`'s
Flow-only execution authority. No Lojix deployment request was submitted and no
service, profile, lock, DNS, authentication, controller, seat, Message,
Network, or cleanup state was changed.

## Accepted source/test proof

The authorized Flow source is immutable revision
`4560453644c095d97d09390819a22e213850986c`, remote bookmark
`mind-sol-6288d1-gate-integration`. Field High reports the full configured
Prometheus no-fallback gate exited zero with 9/9 flake checks and 54/54 tests.
The retained log
`flows/6288d1/reports/flow-gate-4560453644c095d97d09390819a22e213850986c.log`
locally hashes to
`062697a45e10d4804a197645f315f2721562b6ea18e0bbebab71ff53faf76b60`.

## Exact blocking gate

The current deployable source graph does not include that Flow release:

- CriomOS Home `origin/main` is
  `09cace84f11d56e1d4299e4921942c5fbfb0211e`.
- Its `flake.nix` has no Flow input or package pin.
- Its `modules/home/profiles/min/flow.nix` requires an explicit non-null
  `criomosHome.flow.package`, defaults the module to disabled/null, and current
  target source provides no enabling package assignment.
- That current module also lacks the independently checked
  `FLOW_SOURCE_ROOT=/home/li/primary` and packaged `herdr`, `flow-id`, Codex,
  and Claude PATH change from Home revision
  `09c56b37d12df750b33900b2c86f9c2412bd4e54`.
- Current CriomOS main
  `bd6a16da85f386dd4fcee8538c28bc06d4b6b12f` pins CriomOS Home
  `09cace84f11d56e1d4299e4921942c5fbfb0211e`.

Consequently, a Lojix request against the current immutable CriomOS source
would realize a Home closure without the authorized Flow Nexus package and
unit. Store realization or activation from this graph cannot satisfy the
Flow-only deployment request.

## Ownership boundary

Existing Orchestrate lock 3776 covers only the Flow/Message Home modules,
their focused checks, and `modules/home/default.nix`. It does not cover the
CriomOS Home `flake.nix`/`flake.lock`, the CriomOS parent pin, or a target
configuration enabling `criomosHome.flow` with the selected package. Lock 4964
belongs to `eb7bae` and covers only the Agent Intercom cleanup module/check.
No deployment or Nix build process was observed in flight.

The unblock requires one scoped immutable source packet that:

1. pins Flow `4560453644c095d97d09390819a22e213850986c` in CriomOS Home;
2. selects its `flow-nexus` package for the Ouranos Home configuration;
3. includes the checked `FLOW_SOURCE_ROOT` and packaged PATH unit contract;
4. publishes the resulting CriomOS Home revision;
5. pins that revision in one immutable CriomOS revision;
6. passes the focused consumer and generation build gates; and
7. names the Lojix request source revision before activation.

Those flake, parent-pin, and target-selection paths require exact reservation
and an accepted source packet. This report does not claim that reservation or
broaden the Flow-only activation authority.
