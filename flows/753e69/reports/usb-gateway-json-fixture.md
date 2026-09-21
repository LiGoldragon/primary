# Horizon USB gateway JSON fixture — published producer

Horizon remote `usb-gateway-6db4fe@origin` resolves to immutable commit `37416e10c00cc6a22c73528759df5b15bd6d8428`. Its predecessor `944ad387684426da7648ded61d259d88df86802f` introduced the typed service; the later commit enforces at most one USB gateway per node, adds the test dev dependency, and uses the observed Ouranos MAC in its fixture. Field Sol independently read the remote bookmark and clean worktree. The Prometheus-only check `nix build --max-jobs 0 --builders @/etc/nix/machines --option fallback false .#checks.x86_64-linux.default --no-link` passed after the correction. The earlier successful build did not compile the new JSON fixture and is not the acceptance gate.

The exact normalized serde JSON object asserted by `lib/tests/datomic_proposal.rs` is:

```json
{"usbIpv4Gateway":{"downstream":"enp0s20f0u1c2","downstreamMac":"00:0e:c6:33:4f:97","gateway":"10.44.0.1/24","uplink":"enp0s31f6"}}
```

The one-line UTF-8 byte sequence with no final newline has SHA-256 `9784027889067b1e8b7f8aeacdbdde7c3a8a2f852f638a33ce822efd807da722`. This is a published **serde fixture**, not a Goldragon Ouranos projection or Lojix-materialized `horizon.json`. The consumer writer under CriomOS lock `4017` may use the exact tag/field spelling to prepare its module, but must take the later actual projected payload and matching producer/consumer pins before an integration acceptance claim. No activation is authorized by this fixture.
