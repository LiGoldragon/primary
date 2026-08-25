# Node configuration and gates

## Current nodes

```text
                              goldragon node declarations
                                         |
                +------------------------+------------------------+
                |                        |                        |
             species                   size                   services
                |                        |                        |
     Edge/Hybrid/EdgeTesting     exact ordered value      explicit capability
                |                        |                        |
        behavesAs.edge        threshold projection       AgentIntercomLocal
                |            min/medium/large/max               |
                |                        |             +----------+----------+
                |                        |             |                     |
        general desktop          Home/profile and   local runtime       + Graphical
        and video policy         retention gates     and CLIs        GUI prerequisites
                                                                         + Codex Desktop
```

```text
Node          Raw size   General desktop role   Agent GUI capability   Homes
balboa        Zero       no                     no                     —
ouranos       Large      edge                   yes                    li
prometheus    Max        no                     no                     —
tiger         Max        edge                   yes                    bird, li
zeus          Max        edge                   no                     bird, li
vm-testing    Min        no                     no                     —
mirror-alpha  Min        no                     no                     —
mirror-beta   Min        no                     no                     —

Exact Medium: none
```

The important separation is visible at Zeus: it is an Edge desktop node, but has no Agent Intercom Graphical capability. Ouranos and Tiger have both. Exact node size is a third, independent dimension.

## What the gates activate

```text
behavesAs.edge
└─ CriomOS Edge tree
   ├─ desktop baseline, portals, Bluetooth, niri
   └─ size-dependent desktop applications

size.medium  (threshold: Medium OR Large OR Max)
├─ CriomOS: keep Nix derivations
└─ Home med profile
   ├─ VSCodium + pinned Codex/Claude extensions
   ├─ Emacs and qutebrowser
   └─ medium development/media packages

size.large   (threshold: Large OR Max)
├─ CriomOS: keep Nix outputs
└─ Home large packages, Chrome, coding/browser-use surfaces

size.max
└─ Home multimedia-heavy packages

AgentIntercomLocal
├─ CriomOS/Home local runtime
├─ normal pinned Codex + Claude CLIs
└─ MCP/intercom/TUI integrations

AgentIntercomLocal + AgentIntercomGraphical + x86_64
├─ CriomOS: AT-SPI, uinput, screenshot/screencast portals
└─ Home: Codex Desktop, bridge, computer-use UI, remote mobile control

Claude Desktop
└─ no current package or gate
```

Exact Medium does not presently have a reusable consumer predicate. Existing `size.medium` is cumulative and would install on Large and Max too. Implementing the living's clarified exact-Medium target therefore needs an exact-value/equality gate rather than reusing `profiles/med` alone.

## What changed historically

```text
2026-04
NodeSpecies Edge / Hybrid / EdgeTesting
          |
          +─ TypeIs.*             duplicate one-hot view
          └─ BehavesAs.edge ───── general graphical desktop policy
                    |
                    └─ hasVideoOutput

2026-06
TypeIs removed
BehavesAs.edge retained ───────── same live CriomOS gate today

2026-07
AgentIntercomGateway/Peer          remote topology experiment
          |
          └─ replaced/rejected
                    |
AgentIntercomLocal + Graphical ── explicit opt-in agent GUI capability
                                  Graphical requires Local
```

The remembered node role was therefore `Edge`, exposed to consumers as `behavesAs.edge`. That role still controls the general desktop tree. `AgentIntercomGraphical` did not replace it; it split out a narrower agent-application GUI capability.

## Current package outcome

```text
Ouranos [Large, edge, Local+Graphical]
└─ li Home: med+large profiles, Codex CLI, Claude CLI, Codex Desktop

Tiger [Max, edge, Local+Graphical]
├─ bird Home: all profiles, Codex CLI, Claude CLI, Codex Desktop
└─ li Home:   all profiles, Codex CLI, Claude CLI, Codex Desktop

Zeus [Max, edge, no AgentIntercom capability]
├─ bird Home: all profiles, no native agent desktop gate
└─ li Home:   all profiles, no native agent desktop gate

No exact-Medium node currently exercises the requested future rule.
```

## Remaining design fork

The size boundary is ruled: exact Medium. The source reconstruction leaves one independent choice. The new desktop-package predicate can be either:

```text
A. exact Medium only
   node.size == Medium

B. exact Medium with the preserved general graphical role
   node.size == Medium && node.behavesAs.edge
```

Using `AgentIntercomGraphical` would instead preserve the newer, narrower agent-GUI opt-in and would contradict the clarification that it is not the intended size/profile gate unless separately ruled.

## Sources

- [Current-node witness](../witnesses/currentNodeGates.md)
- [Graphical-role history witness](../witnesses/graphicalRoleHistory.md)
- `goldragon/datom.dotos`
- `horizon-rs/lib/src/magnitude.rs`
- `horizon-rs/lib/src/node.rs`
- `horizon-rs/lib/src/user.rs`
- `CriomOS/modules/nixos/edge/default.nix`
- `CriomOS/modules/nixos/agent-intercom.nix`
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
- `CriomOS-home/modules/home/profiles/med/default.nix`
- Flow `01a0338f`
