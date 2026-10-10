# Home Message integration helper

## Published slice

Primary6852f4 delegated three disjoint paths in its isolated Home integration
worktree to Flow908786's medium implementation worker. Reservation1995 was
released after the worker published and verified actual GitHub proposal
`proposal/6852f4-message-flow-home` at
`c2ac15a754aa790578f72d3ed41aa44967fa2607`.

The paths are:

- `modules/home/profiles/min/message.nix`
- `checks/message-service-path/default.nix`
- `checks/message-flow-wiring/default.nix`

Primary retains the final Home/CriomOS flake integration and consumer lock.
This helper is not the completed deployment candidate.

## Configuration and behavior

The module generates the producer-owned nested configuration request,
selects the existing `messenger-v6.sema`, and starts `message-nexus` with one
binary configuration argument. The candidate archive path is
`message-daemon.rkyv`; current runtime uses `message-daemon.signal`, which
must remain represented in the restoration capture.

The worker's read-only observation found both active Message sockets mode
0600, their ordinary/owner paths, the router socket path, v6 database path,
and owner label `message`. The final module preserves those coordinates and
reads uid from the service user. An earlier proposal's username label and
0660 ordinary mode were corrected before this receipt.

The candidate explicitly uses an empty component-ingress list. Primary
accepted that intended configuration in its actual response; it is not a
claim that the current live archive's complete ingress list was decoded.

Message requires and orders after Flow and receives the intended
`FLOW_SOCKET`. Its ordinary and owner wrappers select the corresponding
runtime sockets. Flow's ordinary/meta wrappers are included in the combined
wiring witness.

## Exact-source checks

The worker ran the two check expressions against the exact published helper
source with local Nix build scheduling disabled and the configured Prometheus
builder. The final command exited0. Its captured receipt files are
`/tmp/flow-908786-home-message-expr-checks-c2ac15a7.{out,err,status}`.

| Check expression | Output |
| --- | --- |
| `checks/message-service-path/default.nix` | `/nix/store/az2yw73m7wwag0xvd4a2qdsaq80q652h-message-service-path` |
| `checks/message-flow-wiring/default.nix` | `/nix/store/q77asszkr5ly4ardn70m6wv17hpmw1b7-message-flow-wiring` |

The service check executes the Home-generated writer, requires Message's
positive writer/read-back check, and verifies decoding reaches the component
boundary before an intentionally unusable database-directory path refuses
store opening. The directory remains empty.

The wiring check executes all four real wrappers against disposable Unix
sockets, observes a complete nonempty length-prefixed frame and requires the
client to reject an absent response. This proves wrapper socket selection
and request transmission, not a real daemon response or recipient
consumption. It also depends on the five named Message and six Flow behavior
checks listed in the component reports.

Primary's final graph must export and execute its named integration checks,
including merged Home Manager products and both medium-default checks. These
helper-expression receipts do not substitute for that graph, a realized Home
generation, current-pair restoration or production acceptance. No live
activation, restart, migration or store operation occurred in this slice.
