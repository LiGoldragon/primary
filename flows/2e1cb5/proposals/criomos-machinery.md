Presentation.{ «The machinery of CriomOS» Proposal }

# The machinery of CriomOS

Created by Fable 5.1, from the account "Operating system machinery", surveyed by Opus.

### Proposal 1: Units · psyche-belief › vision/criomos.md

::: comment
The account found ninety-two mechanisms in nine families, each standing in for a change pushed, a readiness said, a declared file or a Nexus's Memory. A section "Units", after "What Nix declares", gives each family its one shape. The first line takes the timers that poll and the watchers on another program's files; the daily store collection keeps its timer.
:::

+ ## Units

+ A unit that needs to know of a change is told of it by the program that makes the change: a subscription where the source is a Nexus, the program's own hook where it is not. A timer marks a period of the world, the daily store collection among them.

+ A unit says when it is ready, and a unit that needs it is ordered after it. A socket is connected to and answers: systemd holds every Nexus socket from boot, across each restart of the Nexus, and a connection made during a restart waits in the socket until the Nexus answers.

```ini
+ # a Nexus's sockets, held by systemd
+ [Socket]
+ ListenStream=%t/nexus/main/flow.sock
+ ListenStream=%t/nexus/main/flow-meta.sock
```

+ Nix declares a unit and nothing of what the unit does while it runs. A Nexus's configuration is its Memory, persisting in State, given by the owner's definitions when he changes them; a start is a start. Activation places files and starts units.

+ A program outside our Nexuses, a harness or a desktop tool, is configured through the door it offers for a declared file: a system settings path, a home variable, a flag. That file is Nix's whole, and the program's own file holds what the program writes. A harness's settings are part of its launch, written by the Flow Nexus from the harness definition.

```nix
+ # Claude's door: the managed settings path
+ environment.etc.${claudeDoor}.source =
+   claudeSettings;
```

::: shown
psyche-belief › vision/flow-nexus-v1.md
[ Furnish.{ Member FlowId }           ; beliefs into the workspace
  Settle.{ Member FlowId }            ; the harness's settings file
:::

+ A key is a declared secret: it reaches the host by the secret mechanism, and the program is pointed at its path. A host's own identity key is made once on the host and kept in State. Credential files reach a capsule through the Capsule, as the one copy it makes.

+ A fix lives where its cause is: in the hardware record when a part needs it, in a declared patch on the package when the package is wrong, in the owning program's declared setting otherwise; a unit's weight is declared on the unit. A diagnostic runs while someone reads it and goes with its reading. A change to a unit reaches the running unit at the switch: by restart, or by reload for a service whose restart would interrupt the host.

```nix
+ # a router's service: its configuration reloads it
+ systemd.services.dhcp.reloadTriggers =
+   [ dhcpConfiguration ];
```

+ A thing is enabled once, by its capability in the cluster data; a module reads the capability, and an option carries a value. What is retired is removed from the tree.

+ The belief repositories are registered once, with the Belief Nexus, which watches them and furnishes every workspace.

```mermaid
+ flowchart TB
+     s["a change, in its source"] -- "a Nexus: subscription" --> u["the unit that needs it"]
+     s -- "another program: its own hook" --> u
+     w["a period of the world"] -- "a timer" --> u
+     r["a unit ready"] -- "ordered after it" --> u
+     d["a declaration"] -- "the program's door: a path, a variable, a flag" --> p["a program outside our Nexuses"]
+     d -- "Define, when the owner changes it" --> m["a Nexus's Memory"]
```

### Proposal 2: Sockets from systemd · psyche-belief › vision/nexus.md

::: comment
The Nexus side of the readiness line, in "Sockets".
:::

+ A Nexus receives its sockets from systemd, which holds them from boot across every restart of the Nexus; the place names their paths, and the socket unit declares the same paths.

### Proposal 3: The sockets held there · psyche-belief › vision/nexus-v1.md

::: comment
One comment in the place example follows Proposal 2.
:::

```datom
- ; the sockets it makes there
+ ; the sockets systemd holds for it there
```

### Proposal 4: The Flow Nexus's unit · psyche-belief › vision/flow-nexus.md

::: comment
Curriculum is replaced by the Belief Nexus, and the socket held by systemd makes the reconnection clause unnecessary.
:::

- A Flow Nexus unit Wants Curriculum, a soft dependency, and reconnects to Curriculum when it returns, so a Curriculum restart leaves every Flow Nexus running.
+ A Flow Nexus unit Wants the Belief Nexus, a soft dependency, so a Belief Nexus restart leaves every Flow Nexus running.

```ini
  [Unit]
- Wants=curriculum-nexus.service
- After=curriculum-nexus.service
+ Wants=belief-nexus.service
+ After=belief-nexus.service
```
