# Network Mode Nexus proof of concept

This source-only tool demonstrates a durable desired-state control plane for a
cascaded routed topology. It stores node modes, a stable subnet allocation
ledger, revisioned compare-and-swap transitions, and an audit trail. `plan`
emits typed reconciliation intent. It never runs `ip`, NetworkManager, DHCP,
DNS, or firewall commands.

CriomOS remains the data-plane reconciler. A later integration must translate
an accepted plan into the existing typed Horizon, Lojix, Goldragon and CriomOS
contracts and must keep source, build, materialization, installation, runtime,
and end-to-end evidence separate.

```sh
node tools/network-mode-nexus-poc/network-mode-nexus.mjs init \
  --state /tmp/network-mode.json --pool 10.44.0.0/16 --link-prefix 24

node tools/network-mode-nexus-poc/network-mode-nexus.mjs transition \
  --state /tmp/network-mode.json --request /tmp/transition.json

node tools/network-mode-nexus-poc/network-mode-nexus.mjs plan \
  --state /tmp/network-mode.json
```

Modes are `offline`, `edge-gateway`, `edge-gateway-ap`, `transit-gateway`,
`transit-gateway-ap`, and `leaf`. Gateway modes enforce the local convention:
the integrated NIC is the uplink and the USB NIC is the downlink. AP mode is an
explicit administrative transition; it is never inferred from cable state.
