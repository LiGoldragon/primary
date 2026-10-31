
## 13.0.0 → 14.0.0 — stream durable delivery status

### What breaks

`Send` and `SendThread` now carry the shared `SendRequest`. Message returns
`SendAccepted` followed by a typed sender-filtered snapshot and subsequent
`SendChanged` updates; clients resume with the shared `DeliveryCursor`.

### Deploy

Repin `meta-signal-message` and Message to this contract. The Message Nexus
must consume Flow's sender-authenticated delivery stream and forward its
accepted state and updates on the originating connection.
