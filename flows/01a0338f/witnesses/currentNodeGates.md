# Current node gates

Method: code read `/home/li/primary/repos/goldragon/datom.dotos`, `/home/li/primary/repos/horizon-rs/lib/src/{magnitude,node,user}.rs`, `/home/li/primary/repos/CriomOS/modules/nixos`, and `/home/li/primary/repos/CriomOS-home/modules/home` through the delegated `current_node_gates` subflow on 2026-08-25.

Horizon magnitude is ordered `Zero < Min < Medium < Large < Max`. Consumer booleans are monotonic: `size.medium` means at least Medium, while exact Medium is `medium == true && large == false` or the raw proposal value `Medium`. Projected user size is the lesser of declared user size and viewpoint-node size. CriomOS deploys a Home only when the user has a public key for that viewpoint.

Current authoritative node declarations:

```text
Node          Size    Species/role                 Agent Intercom        Deployed homes
balboa        Zero    Center                       Local                  none
ouranos       Large   EdgeTesting                  Local + Graphical      li
prometheus    Max     LargeAiRouter                Local                  none
tiger         Max     EdgeTesting                  Local + Graphical      bird, li
zeus          Max     Edge                         none                   bird, li
vm-testing    Min     TestVm                       Local                  none
mirror-alpha  Min     TestVm                       Local                  none
mirror-beta   Min     TestVm                       Local                  none
```

There is no exact Medium node. `behavesAs.edge` is true for Ouranos, Tiger, and Zeus. `AgentIntercomGraphical` is true only for Ouranos and Tiger. Current x86_64 homes therefore receive:

```text
Host      Medium-threshold Home profile    General Edge desktop    Codex Desktop
Ouranos   yes (Large)                      yes                     yes
Tiger     yes (Max)                        yes                     yes
Zeus      yes (Max)                        yes                     no
```

No current gate installs Claude Desktop. `AgentIntercomLocal` installs the pinned Codex and Claude CLIs plus intercom/MCP integration. `AgentIntercomGraphical` additionally installs the unofficial Codex Desktop package, bridge, computer-use UI, remote-mobile-control, and system portal/AT-SPI/uinput prerequisites; Graphical requires Local and x86_64.

System gates observed:

- `behavesAs.edge`: desktop baseline, Bluetooth, portals, niri, and size-dependent edge applications.
- bare metal: firmware, graphics, printing, geolocation, virtual-video, virtualization, and machine drivers.
- Center without Router: networkd/DHCP; currently Balboa.
- Router and Large-AI: Prometheus networking, LLM service, firewall, and runtime user.
- Large + Center: Prometheus nspawn support.
- TailnetClient: Ouranos, Prometheus, and TestVm guests; TailnetController: Ouranos.
- PersonaDevelopment: Ouranos Gitolite/repository-ledger/Lojix services.
- TestVm and VmHost: guest profiles and Prometheus KVM guest emission.
- Medium threshold: keep Nix derivations; Large threshold: keep outputs.
- NixBuilder/NixCache/dispatcher: explicit capabilities plus derived role gates.

Home size gates are cumulative. Min carries baseline packages and Agent Intercom; Medium adds VSCodium, pinned agent extensions, Emacs, qutebrowser, and medium development/media packages; Large adds Chrome and coding/browser-use packages; Max adds multimedia-heavy packages.
