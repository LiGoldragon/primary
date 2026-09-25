# Router firewall: the rationale, the router feature, the simplest fix

Flow e51411, read-only research, 2026-09-24. Nothing in CriomOS or on
Prometheus was changed. This report answers the living's comment on the
flashbook "Prometheus and the Network" (`flows/e51411/vision/network.md`):

> Well the concept of router is just a feature now so it's not a router per se. It has that feature. What's the whole rationale behind these firewall rules? Can we just make a really really simple fix that doesn't try to reimagine everything and introduce a bunch of other variables, because of security or whatever, and we haven't even questioned the whole rationale?

## Short answer

- **No reason was ever recorded.** No commit message, code comment, psyche
  record or vision record says why the router writes its own ruleset,
  why it turns off the NixOS firewall, or why the WAN drops unsolicited
  input. The ruleset was pasted in as a prototype in December 2023 and
  has been patched hole by hole since.
- **Router is a feature.** It is `Router.{}`, one entry in a node's
  capability list. Prometheus has seven such entries. It is not a node
  type.
- **The simplest fix is already written.** CriomOS `main` now has two
  small commits, `73ba25c` (NDP, 1 rule) and `bd6a16d` (declared TCP ports
  composed into the router ruleset, about 11 lines). Together they fix the
  NDP drop, port 80 and port 11434. Neither is deployed yet. The trade-off: every
  port a module declares open is now open on the WAN as well. This is
  what the NixOS firewall does on any node that is not a router.

## 1. The rationale

### What the record says (stated)

The ruleset first appears in the archived predecessor repository
`LiGoldragon/criomos-archive`, file `nix/mkKriomOS/router/default.nix`
(later `nix/mkCriomOS/router/default.nix`). Every commit that shaped it,
with its full message:

| Commit | Date | Message | What it did to the firewall |
|---|---|---|---|
| `df72903` | 2023-12-05 | `(initiatedFeature router)` | Created the module: `firewall.enable = false`, `nftables.enable = true`, input `policy drop`, LAN bridge accept, WAN established/related, WAN select ICMP (IPv4 only), `iifname wan counter drop "Drop all other unsolicited traffic"`, loopback accept, forward LAN→WAN, masquerade. |
| `56777c1` | 2023-12-05 | `(hackyWorkingPrototype router)` | Interface names and subnet only. |
| `1507dd8` | 2023-12-05 | `[removedUneededYggdrasilFWRule addedUntestedRouterHostapd]` | Changed the Yggdrasil module's `networking.firewall` ports, not the router ruleset. |
| `c91b3c6` | 2023-12-07 | `(hackyFixed yggdrasilMulticastDiscoveryRouter)` | Hand-copied Yggdrasil's fe80 UDP 9001 / TCP 10001 admits into the router ruleset, added `yggTun` to the trusted set, and added `router/yggdrasil.nix`. |
| `0ca0e78` | 2025-07-12 | `openPort(router ssh)` | Added `tcp dport ssh accept`, with no interface scope. |
| `e894277` | 2025-07-13 | `openFirewall(wlanDevice)` | Added the Wi-Fi interface to the trusted set. |
| `9f85328` | 2025-08-01 | `introduce(typeIs.routerTesting(nftables))` | `useNftables = typeIs.routerTesting; firewall.enable = !useNftables`. On a router without the `routerTesting` species, this turned the hand ruleset off and the NixOS firewall back on. |
| `4d4e5de` | 2026-03-22 | `(("feat", "wifi-pki"), ...)` | Set `useNftables = true` for good, with no stated reason. |

In the current CriomOS (`/git/github.com/LiGoldragon/CriomOS`) the module
was copied in at `eff6eea` (2026-04-23, "canonical rewrite ... copies from
criomos-archive"). Since then the firewall has been patched again for
test-VM taps (`ee49b20`, `3aa4780`, 2026-07-03), for NDP (`73ba25c`,
2026-09-23) and for declared TCP ports (`bd6a16d`, 2026-09-24).

The only written reasoning in the module is the rule comments, such as
"Allow trusted LAN to WAN", "Drop all other unsolicited traffic from
…" and "Accept everything from loopback interface". They say what each
rule does. They do not say why. The only critique ever written down is the
archive audit's `SEC-8` (`docs/AUDIT-2026-04-17.md`), which says the WAN
ICMP accept has no rate limit.

Psyche and vision records: I searched `Vision/`, `vision-raw/` and
`flows/*/vision/` for firewall, nftables, WAN and router. The hits are:
- the living's 2026-09-23 hypothesis that Yggdrasil is firewalled on the
  USB device (`flows/836818/vision/network.md`);
- "Let's fix the firewall so it's fully up" (`flows/836818/vision/flowNexus.md`);
- the comment this report answers (`flows/e51411/vision/network.md`);
- unrelated uses of "firewall" as a mind-layer metaphor
  (`flows/f55ec8/vision/layers.md`) and of "router" as a signal router
  (`Vision/nexus.md`).

None of them gives a rationale for these rules.

### Inference (not recorded anywhere)

- **The ruleset looks copied, not designed.** Its structure and its comment
  strings match the standard NixOS-as-a-router nftables example that
  circulated in 2022–2023: drop on input, trust the LAN, allow
  established traffic and select ICMP on the WAN, drop the rest, and
  masquerade. The commit names it a "hackyWorkingPrototype". I did not
  check the upstream source online.
- **Turning off the NixOS firewall was probably forced at first.** Older
  NixOS (before 23.05) refused to run a hand-written nftables ruleset while
  its iptables firewall was on. By December 2023 NixOS had an nftables
  firewall backend, so this was probably a habit carried over from the
  example, not a constraint. The `routerTesting` toggle in August 2025
  suggests the author was trying out a move between the two approaches.
- **"Drop everything on the WAN" assumes the WAN is the hostile internet.**
  On Prometheus the declared WAN `eno1` is the USB cable to Ouranos in the
  same room (10.44.0.0/24). Ouranos NATs to the internet. Nothing
  unsolicited from the internet reaches `eno1`.
- **"Everything is dropped on the WAN except ssh" was never a policy.** It
  comes from two unrelated rules: ssh was opened on every interface in
  July 2025, and it happens to come before the WAN drop.
- **The same defect has now happened three times.** Because the router
  disables the NixOS firewall, every module's
  `networking.firewall.allowed*Ports` is silently ignored on router
  nodes:
  - Yggdrasil's ports in December 2023, patched by hand-copying the fe80
    rules;
  - Yggdrasil NDP in September 2026 (`73ba25c`);
  - nix-serve port 80 and llama port 11434 in September 2026 (`bd6a16d`).

## 2. Router is a feature, not a node type

In CriomOS today:
- `modules/nixos/router/default.nix` gates everything on
  `config = optionalAttrs behavesAs.router { … }`.
- `behavesAs.router` comes from horizon-rs
  `lib/src/projection/viewpoint.rs`: `router = has(|c| matches!(c, Capability::Router))`.
  It is true when the node's capability list contains `Router`.
- `NodeCapability::Router(NoSettings)` is one variant among 21
  (`lib/src/generated/horizon.rs`). `NodeVariant` is only `Live` or
  `Installation`.
- In `goldragon/cluster-definition.datom`, Prometheus's capabilities are
  `[ Center LargeAi Router TailnetClient NixBuilder.6 NixCache VmHost ]`.

History: in the archive, router was a *species*. `typeIs.router`,
`routerTesting` and `largeAI-router` came from a species enum, which is
a kind of node. Horizon-rs replaced species with capabilities in
September 2026 (`fc03733`, `2594d54`). The module still behaves as if
it owns the whole machine: it replaces the host firewall instead of
adding router behaviour (forwarding, NAT, DHCP, access point) next to
the host's other features. That mismatch is the structural cause. The
router feature and the NixCache feature do not compose, because the router
feature discards what the cache feature declares.

## 3. The simplest fixes

What Prometheus declares (read from source, not evaluated):
- TCP 80 from `nix/cache.nix` (NixCache);
- TCP 11434 from `llm.nix` (LargeAi; the port is in CriomOS-lib `data/largeAI/llm.json`);
- TCP 10001 and UDP 9001 from `network/yggdrasil.nix`;
- TCP 22 from openssh's default `openFirewall`;
- UDP 41641 from tailscale `openFirewall = true` (TailnetClient).

### A. Let the router ruleset honour the declared ports (already on main)

- **Change:** `bd6a16d` "Compose declared TCP ports into router
  nftables". It adds about 11 lines to `router/default.nix` that emit
  `tcp dport N accept` for each entry in
  `config.networking.firewall.allowedTCPPorts`, placed before the WAN
  drop, plus a 60-line check `checks/router-declared-tcp-ports`. It is on
  `origin/main`. It passed the remote checks. It is **not deployed**
  (`flows/9ddcbc/reports/deployment-receipt-inspection-2026-09-24.md`).
- **Fixes:** port 80 and port 11434 on `eno1`, and any TCP service
  declared in the future. It does not fix NDP; `73ba25c` does that.
- **Does not cover:** `allowedUDPPorts` (tailscale 41641) and
  per-interface `networking.firewall.interfaces.<if>.allowed*` (the
  mirror's `tailscale0` port). Adding UDP to the same loop is about 4
  more lines.
- **Newly exposes:** every declared TCP port becomes reachable from the
  WAN, as it already is from `br-lan`, the Wi-Fi, `yggTun` and every
  interface on a non-router node. Today that means nix-serve on 80,
  which is unauthenticated and serves any store path, and the llama
  server on 11434, which takes an API key when the sops secret is
  present. They are reachable by whatever sits on `eno1`'s segment,
  which today is Ouranos's USB link. It also opens TCP 10001 to any
  source address, where before only link-local sources were admitted.
- **Keeps unchanged:** the rest of the hand-written ruleset (IPv4-only
  select ICMP, forward chain, masquerade).

### B. Delete the hand-written input chain and use the NixOS firewall with nftables

- **Change:** set `firewall.enable = true` (the nftables backend follows
  from `nftables.enable`). Delete the input chain, about 40 lines. Move
  the trusted set (`br-lan`, the Wi-Fi interfaces, `yggTun`, `vmt*`) to
  `networking.firewall.trustedInterfaces`. Keep the forward chain and
  the NAT table as they are. The result is fewer lines of our own code.
- **Fixes:** NDP, 80, 11434, UDP ports and per-interface ports. It
  removes the whole class of defect, because the router stops
  overriding the host firewall.
- **Newly exposes or introduces:**
  - all ICMPv6 except redirects and type 139 is accepted on every
    interface, not only NDP;
  - the DHCPv6 client port;
  - every declared TCP and UDP port on the WAN, as in A;
  - strict reverse-path filtering (`checkReversePath` defaults on, in a
    prerouting chain that also sees forwarded traffic). This is the one
    real new variable on a multi-interface router with VM taps and
    needs a VM test;
  - `ct state invalid` drops;
  - two input chains on the same hook. A hand rule left behind that
    drops would still win.

  This is the larger behavioural change of the three.

### C. Add only the two missing admits

- **Change:** the NDP rule, already on main (`73ba25c`, 1 rule plus a
  check), and one `iifname "eno1" tcp dport 80 accept`, 1 line. The
  witness's version of the port 80 rule was scoped to `isNixCache` and
  the USB subnet, which adds new inputs to the router module.
- **Fixes:** NDP and port 80. It does **not** fix 11434 or anything
  declared later.
- **Newly exposes:** nix-serve only, on the WAN.
- **Drawback:** this is a fourth hand-copied patch of the same kind.

### Verdict

A, together with the NDP rule already on main, is the simplest complete
fix. It rethinks nothing. Its whole claim is that "router" as a feature
should stop cancelling the ports other features declare. It is already
written, checked and pushed. The remaining step is to deploy it. That
step is blocked on the Lojix materialization shape
(`node.routerInterfaces` versus `node.network.routerInterfaces`,
`flows/9ddcbc/reports/usb-yggdrasil-durable-repair-2026-09-24.md`), not
on firewall design.

The trade-off is exposure. Declared ports become open on `eno1`. That
is harmless while `eno1` is a cable to Ouranos. It matters on a router
whose WAN faces a network nobody controls. Whether any port should stay
closed on the WAN has never been decided, because nobody ever stated
why the WAN drop exists. That is a question for the living, not a
precondition for A.

## Sources

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix`
  (current ruleset, lines 134–207).
- CriomOS commits `eff6eea`, `ee49b20`, `3aa4780`, `73ba25c`, `bd6a16d`,
  `eebeab5`; `checks/router-declared-tcp-ports/default.nix`.
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nix/cache.nix`,
  `modules/nixos/llm.nix:155`, `modules/nixos/network/yggdrasil.nix:61-63`,
  `modules/nixos/network/tailscale.nix`, `modules/nixos/mirror.nix:62`.
- `https://github.com/LiGoldragon/criomos-archive` (archived): commits
  `df72903`, `56777c1`, `1507dd8`, `c91b3c6`, `0ca0e78`, `e894277`,
  `9f85328`, `4d4e5de`; `docs/AUDIT-2026-04-17.md` (SEC-8, SCHEMA-1).
- `/git/github.com/LiGoldragon/horizon-rs/lib/src/projection/viewpoint.rs`,
  `lib/src/generated/horizon.rs` (`NodeCapability`, `NodeVariant`).
- `/git/github.com/LiGoldragon/goldragon/cluster-definition.datom`
  (Prometheus capabilities).
- `/git/github.com/LiGoldragon/CriomOS-lib/data/largeAI/llm.json`
  (`serverPort` 11434).
- nixpkgs `nixos/modules/services/networking/firewall-nftables.nix`
  (NixOS nftables firewall input chain, ICMPv6 and rpfilter defaults).
- `flows/d8df70/witnesses/prometheus-firewall-2026-09-24.md`,
  `flows/9ddcbc/reports/usb-yggdrasil-durable-repair-2026-09-24.md`,
  `flows/9ddcbc/reports/deployment-receipt-inspection-2026-09-24.md`.
- `flows/e51411/vision/network.md`, `flows/836818/vision/network.md`,
  `flows/836818/vision/flowNexus.md`, `flows/f55ec8/vision/layers.md`,
  `Vision/nexus.md`.
