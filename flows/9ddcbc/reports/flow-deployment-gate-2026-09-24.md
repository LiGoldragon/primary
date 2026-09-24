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

## Home source unblock completed

Field High subsequently clarified that this flow owns source preparation and
`eb7bae` remains the sole deployment packet executor. Orchestrate lock 5006
reserved only CriomOS Home `flake.nix` and `flake.lock`; existing lock 3776
covered the Flow module and focused check. No other lock was changed.

The immutable Home candidate is
`c4fa2395fa9a9a143a8955ecaeb3c961a28f5447` on remote branch
`field/flow-deploy-9ddcbc`; one `ls-remote` readback matched that revision. It:

- pins Flow `4560453644c095d97d09390819a22e213850986c` with nar hash
  `sha256-Feav6OOlpmk9TwJxHWgUI5ZQeYfzYgRvy5p/62R5ybg=`;
- selects the pinned default Flow package for the fixed `li` user;
- enables that user's Flow unit by default;
- includes `FLOW_SOURCE_ROOT=/home/li/primary` and the packaged `herdr`,
  `flow-id`, Codex, and Claude PATH; and
- registers a focused flake check that asserts the exact locked revision and
  writes it into the check artifact.

The configured Prometheus cache timed out on all five attempts. Under the
living-authorized unavailable-builder fallback, the focused check passed
locally: drv
`/nix/store/xpxnk9cynq4ycn9nivqh4rwsm0x8vw2c-flow-service-path.drv`, output
`/nix/store/by85pk6ynkxi8x9vh8snwgn9631xg298-flow-service-path`; its
`flow-revision` file contains the exact accepted Flow revision.

The candidate and receipt were transported to `eb7bae`. Lock 5006 was then
released; lock 3776 remains. The remaining gate is the sole executor's parent
CriomOS pin, materialized-target realization, and Lojix request/journal chain.
No standalone Home closure is represented as the deployable embedded Home
generation. No Lojix submission or activation occurred here. The separate
Mind refresh source `029ab7a6d0cb1cd4403f8f77bf47f2438211beb2` explicitly says
`no deploy` and was not substituted for the authorized Flow revision.

## Canonical combined packet adopted

The living subsequently ordered immediate green-v2 composition and lifted the
Message pre-deploy hold. `eb7bae` published the sole canonical Home packet
`904185761771308172d18c1ee8f6ca4e2b37a1d7` and CriomOS parent
`90702b6e9aa3aa9b82b4f17c5f2bd566d0abc030`. Exact source inspection proves:

- Home pins Flow `4560453644c095d97d09390819a22e213850986c`, nar hash
  `sha256-Feav6OOlpmk9TwJxHWgUI5ZQeYfzYgRvy5p/62R5ybg=`;
- Home pins Message `a8c6a924d5d04fbfcbf0a7e2e1b145076d327a53`, nar hash
  `sha256-wvYVLpJ049j0kkKejiLHEPqhptkDYd3V/I4LE8EC9WU=`;
- Home contains the nested Struct writer and packaged writer-boundary semantics
  from `9a85262ae34c41bf6d82a6c927e0b3c24e2a52c0`;
- Home contains the Flow package selection, default `li` enablement,
  `FLOW_SOURCE_ROOT`, and packaged runtime PATH; and
- CriomOS `90702b6e...` pins Home `904185...` with nar hash
  `sha256-EQYtYZam1uPCem0w59dLc9x0bXnumAO1ShQH2szN47E=`.

The scoped source diff between the locally composed candidate and Home
`904185...` was empty. This flow adopted the canonical commit and did not
publish a second packet. Lock 5022 was released.

After one Prometheus timeout, the living-authorized local fallback completed:

- Flow focused check: drv
  `/nix/store/xpxnk9cynq4ycn9nivqh4rwsm0x8vw2c-flow-service-path.drv`, output
  `/nix/store/by85pk6ynkxi8x9vh8snwgn9631xg298-flow-service-path`; exact Flow
  revision present in the artifact.
- Message focused check: command exit zero, drv
  `/nix/store/18zwprxsks9zvp53v5bqnpsbzwg2d7v6-message-service-path.drv`, output
  `/nix/store/ykdirs8d8v7n0id19inr9lmazi4p28wa-message-service-path`. The
  positive nested-Struct packaged writer produced a nonempty configuration.
  The printed Meaning rejection was the required old parenthesized-form
  negative case.
- The Message package test run reported zero failures: 12 library tests, plus
  agent registry 2, convergence 4, delivery 2, Flow delivery 8, message store
  2, process boundary 3, PTY 1, relay 7, startup 4, and migration 2.

The concrete handoff was transported to `eb7bae`, Psyche High `836818`, Psyche
Medium `d8df70`, and Mind `6288d1`. Field High `9e735b` was not registered, so
its one delivery attempt is held as `attempt-5008062ae4ab`; it was not retried.
`eb7bae` remains the sole executor for the Lojix request/journal binding,
realized closure, persistent profile, units/sockets/PIDs, and live tests.

## Canonical Lojix motion observed

A later read-only `Query.ByNode.{ goldragon ouranos None }` distinguished the
executor's two attempts:

- deployment 28 was rejected as `FlakeReferenceMalformed`, with no immutable
  revision; and
- deployment 29 was admitted for `UserEnvironment.li`, `ActivateNow`,
  `LiveActivation`, `RequireImmutable`, exact CriomOS revision
  `90702b6e9aa3aa9b82b4f17c5f2bd566d0abc030`, admission marker 698. Its
  observed lifecycle was `Building` with no terminal result.

This is the first actual Lojix request/journal source linkage for the canonical
pair. `Building` is not a realized closure, activation, persistent-profile
witness, or live acceptance. This flow submitted no request or retry.
