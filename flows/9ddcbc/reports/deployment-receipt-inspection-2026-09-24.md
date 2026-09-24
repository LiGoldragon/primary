# Flow → Message → Network deployment packet inspection

Observed 2026-09-24 from retained Field Medium `9ddcbc`. This is a read-only
inspection plus build receipts. No service was activated, restarted, disabled,
or removed.

## Current deployment identity

Lojix ordinary queries supply the immutable caller record that the systemd
store paths do not:

- `Query.ByDeployment.{ 27 }` reports the current Ouranos user environment as
  completed/succeeded, immutable CriomOS revision
  `cef111108623617987b6e366ccbe4176c093d6b5`, closure
  `/nix/store/y2mh6ajiag7b0bx4rps0llpaz0l78ipg-home-manager-generation`.
  `/home/li/.local/state/nix/profiles/home-manager` independently resolves to
  that closure (Home generation 1031).
- `Query.ByDeployment.{ 4 }` reports the current Ouranos host environment as
  completed/succeeded, immutable CriomOS revision
  `36653a125de8f14518af2dddf89333610891d140`, closure
  `/nix/store/41cvi7l9rjy3n05jixzqdk937rg8gz27-nixos-system-ouranos-26.11.20260813.0e251e2`.
  `/run/current-system` independently resolves to that closure.

This is the minimum source-request → realized closure → persistent profile
chain required for later deployment receipts. The current NixOS-reported
configuration revision is `Unknown`, so `nixos-version`, systemd `ExecStart`,
and store paths alone must not be reported as source revision proof.

## Repository transport observation

Psyche `836818` reported two intermittent GitHub SSH refusals from the Primary
working copy on Ouranos between 2026-09-24 14:39 and 14:43 UTC. The exact error
was `Permission denied (publickey)`. Each refused push or `ls-remote` succeeded
within seconds on a retry without a configuration change; this flow separately
observed the same refusal during readback at about 14:43 UTC after its preceding
push had returned success. Psyche reports that the user agent held one ED25519
key throughout and that every push it called landed later had a successful
`ls-remote` witness.

The cause is **unknown**. Agent socket behavior, the held key, concurrent work,
and GitHub-side behavior remain untested hypotheses. No key, agent, socket,
configuration, service, or active diagnostic probe was changed or performed.
For deployment receipts, a successful push response and a later successful
remote readback remain distinct grades; a refusal alone neither retracts a
prior successful push nor proves that it landed.

## Running unit provenance

- `message-daemon.service` is a symlink into current Home generation 1031 at
  `/nix/store/qnw31dki9shwkv59229a6xrc517k8091-home-manager-files`. It invokes
  `/nix/store/hma89ndhd03dyh2wiv3f0v47qvf6wfmb-message-0.12.0/bin/message-daemon`
  and is failed. This unit is attributable through Lojix deployment 27 to
  CriomOS revision `cef111...`.
- `flow-nexus.service` is a regular mutable file dated 2026-09-17, invokes
  `/home/li/.local/bin/flow-nexus`, and is active. The binary SHA-256 is
  `98f68df32f144efde2fd53c14e8afe35dce984db1f0ce957b63b281d6f923a0e`.
  It is absent from current Home generation 1031, so its exact Git source
  revision is **unknown**.
- `agent-intercom-fleet-cleanup.service` and `.timer` are regular mutable files
  dated 2026-08-09 and absent from current Home generation 1031. The timer is
  active/waiting, while the service is failed because it invokes the absent
  mutable `.pi` source path. Their creating caller and Git revision remain
  **unknown**.
- `yggdrasil.service` and `NetworkManager.service` come from the current host
  closure, therefore their deployment caller is Lojix deployment 4 and
  CriomOS revision `36653a...`. This does not imply that later network source
  repairs are deployed.

## Existing build proofs

- Flow Home consumer revision
  `09c56b37d12df750b33900b2c86f9c2412bd4e54` passed the configured Prometheus
  builder check: drv
  `/nix/store/wdnfypgym8rimi3c0a744rl933rqigpa-flow-service-path.drv`, output
  `/nix/store/b549m611v1dg7dhgy08vp737xfr9y006-flow-service-path`. It asserts
  `FLOW_SOURCE_ROOT=/home/li/primary` and a packaged `herdr`, `flow-id`, Codex,
  and Claude PATH. This consumer-only check does not itself pin or validate a
  Flow producer graph.
- Message Home consumer revision
  `9a85262ae34c41bf6d82a6c927e0b3c24e2a52c0` passed its configured-builder
  contract: drv
  `/nix/store/z6kb9s23wyymsyxz015m8hqa9br21ni5-message-service-path.drv`, output
  `/nix/store/v1appbkz48daampb6vihiswj2gxlqxij-message-service-path`.
- Agent Intercom baseline at `9a85262a...` passed remotely: drv
  `/nix/store/a8rayf32xbiqk64k8px9zcwj1qcy3f44-agent-intercom-integration-contract.drv`,
  output
  `/nix/store/8qpmap0fpvwghrbqmgp3mw85xhwbw0k1-agent-intercom-integration-contract`.
- `eb7bae`'s single corrective cleanup candidate
  `ba5bcac8d04b04f0f83d698f66f7e18139a116ae` passed remotely: drv
  `/nix/store/g1jbqfwckzhx8bn8kb550wb5r4kfmyjp-agent-intercom-integration-contract.drv`,
  output
  `/nix/store/k7g9kq5vdwynjqc7kh1fcq9aw0kklnfc-agent-intercom-integration-contract`,
  log SHA-256
  `e7f4fed96c138dd6b1fefa285613e7b71b51185c48269bd35c5cbdf5354cda94`.
  Its proposed Home generation evaluation is still running under `eb7bae`;
  no duplicate job was started.
- Network source `bd6a16da85f386dd4fcee8538c28bc06d4b6b12f` passed the focused remote
  declared-port and NDP contracts, but it is not deployed.
- Field High `9e735b` reports the first Flow source/test proof green at immutable
  revision `4560453644c095d97d09390819a22e213850986c`, remote bookmark
  `mind-sol-6288d1-gate-integration`. The full Prometheus no-fallback gate exited
  zero with 9/9 flake checks and 54/54 tests. The retained log at
  `flows/6288d1/reports/flow-gate-4560453644c095d97d09390819a22e213850986c.log`
  independently hashes to
  `062697a45e10d4804a197645f315f2721562b6ea18e0bbebab71ff53faf76b60`.
  This is source/test proof only; it is neither packet acceptance nor activation.
- The final integrated Message lineage is not green. Mind `6288d1` is repinning
  manifests, and `47764b`'s disjoint `Pending => Parked` guard child
  `75356175` must merge into the sole Message gate. The earlier packaged Message
  consumer check is not final integrated-lineage proof.

## Accepted sequence and receipts

Field High `9e735b` coordinates the accepted packet. The activation order is
Flow, then Message, then Network. For each step the receipt must include:

1. the immutable Lojix deployment request and its recorded source revision;
2. the realized output closure and terminal deployment result;
3. independent persistent profile and running-unit readback;
4. exact `ExecStart`, environment, socket, process start time, and state;
5. a focused live acceptance result, with rollback generation/closure retained.

Flow acceptance must use typed `flow "ResolveRecipient.<id>"`. The Flow
source/test gate is green, while activation remains held for the root accepted
packet. Message follows Flow and is the current integrated-lineage blocker.
Network follows Message. The stale cleanup timer remains held for the accepted
root packet. No activation is authorized by this inspection.
