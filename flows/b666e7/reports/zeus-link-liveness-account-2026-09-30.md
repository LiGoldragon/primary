# Zeus link liveness: lasting account

Prepared 2026-09-30 for Mind Astra and Fable from Field Sol's corrected
cross-host journal packets. This is an account of what the evidence settles;
it is not a host-action or root-cause report. No host, service, configuration,
or source was changed for this account.

## Judgment

Zeus did not have continuous wired reachability after the first recovery. The
bounded evidence establishes a second, synchronized carrier outage from about
17:01 to 21:07 on 2026-09-29, roughly four hours. After stable carrier
returned, DHCP and Yggdrasil came back automatically within seconds. A
successful wired or overlay ping and authenticated SSH on the morning of
2026-09-30 prove contact at that later time only; they do not prove overnight
continuity.

The evidence settles the physical/link boundary and recovery sequence. It does
not settle the physical trigger, the reason for the negotiation delay, or what
happened outside the observed windows.

## Witnessed facts and source origin

The exact journal lines below are literal lines supplied in Field Sol's
`1bc255` correction packet. Times are local `-06:00`.

- Ouranos `systemd-networkd` recorded `enp0s20f0u1c2: Lost carrier` at
  `17:01:17`; Zeus's kernel recorded `enp0s31f6: NIC Link is Down` at
  `17:01:17.851411`. Zeus `charon` recorded `10.44.0.10 disappeared` at
  `17:01:23.856299`.
- Ouranos recorded carrier gained, lost, gained at `21:07:10`, `21:07:11`,
  and `21:07:14`. Zeus recorded `Up 10 Mbps Half Duplex` and then `Down` at
  `21:07:10.287684` and `21:07:10.288675`, followed by stable
  `Up 1000 Mbps Full Duplex` at `21:07:13.956734`.
- Field's packet reports the Zeus address reappeared at about `21:07:15` and
  Yggdrasil traffic was inbound/outbound on both hosts at `21:07:16`.
  The packet's `Kea DHCP4_LEASE_ALLOC` at `21:07:15.990` is a Field summary,
  not a quoted raw journal line; it identifies MAC
  `90:2e:16:47:ea:e3` receiving `10.44.0.10`.

The same packet contains the earlier exact lines: Ouranos lost carrier at
`14:50:55`, Zeus went link-down at `14:50:57.208866`, and the sequence around
the reported physical unplug/replug was Ouranos gain `15:26:41`, loss
`15:46:31`, gain `15:46:34`, stable gain `15:48:54`; Zeus went up at 1 Gb/s
`15:46:34.197327`, logged an xHCI resume error/reinitialization at
`15:46:45.798591`, briefly went up at 10 Mbps half duplex at `15:46:46.163168`,
down at `15:46:48.217117`, and up at 1 Gb/s full duplex at
`15:48:54.391684`. Zeus `charon` recorded `10.44.0.10 appeared` at
`15:48:56.576894`; the literal Ouranos Kea line records that lease allocation
at `15:48:56.404`. Yggdrasil sessions followed within seconds.

The living physically unplugged and replugged the cable and saw a light near
the Sep 29 `15:26` transition. That physical act and its exact causal timing
were not agent-witnessed. Zeus uptime was nearly 13 days, so these events do
not indicate a Zeus reboot. No Ouranos host-visible USB disconnect/reprobe or
networkd restart was observed in the bounded window.

## What follows, and what does not

The aligned Ouranos and Zeus records are independent host journal witnesses of
the same carrier loss and recovery. They establish that the outage was at the
wired carrier/link boundary, followed by automatic address and overlay
recovery. They do not establish why the link dropped or why stable negotiation
took until 21:07. Possible classes remain connector, cable, adapter, PHY,
power, or negotiation; selecting one would exceed the evidence.

The Zeus xHCI resume error is temporally coincident with the first recovery
sequence and concerns another PCI device. It is not causal proof. The Kea
allocation and Yggdrasil observations show post-carrier recovery, not a
continuous-contact interval. There is no evidence here for overnight state.

The earlier method failed as a liveness method: its bounded watch ended around
15:35, shortly after the first carrier recovery, and no follow-up watch covered
the later four-hour outage. That is a method gap, not a seat failure. Future
accounts must preserve the bounded observation interval and avoid extending a
successful point check into a continuity claim.

## Lasting recovery direction

Network services already recover the address and Yggdrasil session after a
stable carrier. Before adding any recovery actuator, isolate the physical/link
cause. The next useful design is a passive continuous watch of both ends,
recording carrier transitions, negotiation mode, address appearance, DHCP
identity, and overlay contact. It should stop at a declared boundary and leave
a follow-up notice or handoff so a later outage is not silently outside the
account.

When the living authorizes that watch, distinguish one intervention at a time:
first correlate the two carrier logs; then, only with the physical path
identified, check cable/connector, adapter, and peer/port individually while
preserving the capture. Treat any resulting causal statement as a new witness,
not as an inference from this packet. No such check has been enacted here.

## Open questions for Mind and Fable

- What physical or peer event caused the 17:01 loss and the 21:07 negotiation
  sequence?
- Was contact absent for the rest of the night, or did an unobserved recovery
  occur? The present evidence cannot answer this.
- What passive watch boundary and follow-up mechanism will make the next
  liveness claim cover the interval it names?

### Packet provenance

- Field Sol `1bc255`, correction packet: exact Ouranos/Zeus journal lines for
  the 14:50–15:48 and 17:01–21:07 windows; summarized Kea/Yggdrasil details
  for 21:07; morning ping/SSH result.
- Field Sol `6f51ad`, correction packet: cross-host corroboration and the
  method lesson that this establishes a four-hour outage, not cause or
  overnight continuity.
- Existing report `flows/1bc255/reports/zeus-reachability-2026-09-29.md`:
  earlier bounded read-only context, including the 15:35 watch boundary and
  its limits. It is not evidence of continuous contact after that boundary.
