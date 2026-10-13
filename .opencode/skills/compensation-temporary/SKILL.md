---
name: compensation-temporary
description: "A temporary condition holds: a host, builder, service or network route differs from its standing state for a stated period; or the network between hosts matters to the work."
dependencies: []
---

The current network topology is set by the skill variable `Network topology`.

A temporary condition does not stop work: what needed the missing host builds or runs locally, or waits for it; everything else goes on.

A condition's line is removed when it ends.
