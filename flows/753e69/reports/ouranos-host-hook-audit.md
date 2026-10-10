# Ouranos host firewall hook: carried audit

**Scope:** read-only audit of Terra's operational persistence bridge on
2026-09-21. This is evidence for Terra and Field Astra, not a declaration that
the bridge is a CriomOS deployment.

## Live observations

`firewall.service` is enabled and active (`exited`). Systemd loads the drop-in
from `/etc/systemd/system.control/firewall.service.d/90-field-prometheus-usb.conf`.
The observed root-owned drop-in is mode `0644`, 127 bytes, and contains:

```ini
[Service]
ExecStartPost=/etc/systemd/field-prometheus-usb-firewall.sh
ExecReload=/etc/systemd/field-prometheus-usb-firewall.sh
```

The hook path exists, is root-owned mode `0700`, 732 bytes, and was modified at
`2026-09-21 12:39:17 -0600`. Its root-only mode prevented byte-for-byte reading
in this audit.

Systemd's current execution definition retains the Nix-generated firewall
`ExecStart` and first `ExecReload`, then appends the hook as `ExecStartPost` and
a second `ExecReload`. The journal records the generated reload from
12:39:33 to 12:39:34 local time, followed by the hook process exiting zero at
12:39:34. This is a live reload-success receipt, though it cannot establish the
current iptables contents.

NetworkManager is active. The active `prometheus-share-temporary` profile has
UUID `92eb01d2-2087-44c9-a6ff-b2420df89d33`, exact USB interface
`enp0s20f0u1c2`, and matching configured MAC `00:0E:C6:33:4F:97`. It is IPv4
shared at `10.44.0.1/24`, IPv6 disabled, never-default, autoconnect enabled,
and priority 200. Its last NM activation timestamp is 12:42:45 local.
The direct USB route is `10.44.0.0/24`; the preferred default stays on
`enp0s31f6` at metric 100, with Wi-Fi at metric 600. The NM connection-keyfile
directory is root-owned mode `0700`, so this audit could not read the keyfile
or independently establish its file mode or saved flag.

## Transcript-only root receipt

Terra's recorded Attempt 9 supplies the exact hook source. It sets
`IPT=/run/current-system/sw/bin/iptables`, USB `enp0s20f0u1c2`, WAN
`enp0s31f6`, and subnet `10.44.0.0/24`. Its `add_input` and `add_nat` functions
use `iptables -C` before inserting or appending. The recorded rule set is:

- INPUT: DHCP UDP/67 scoped to the USB interface, comment
  `field-6db4fe-dhcp`.
- INPUT: DNS UDP/53 and TCP/53 scoped to the USB interface and
  `10.44.0.0/24`, comments `field-6db4fe-dns-udp` and
  `field-6db4fe-dns-tcp`.
- NAT POSTROUTING: MASQUERADE scoped to source `10.44.0.0/24` and output
  `enp0s31f6`, comment `field-6db4fe-nat`.

The same receipt reports that one controlled reload left exactly those three
marked filter rules and one marked NAT rule. It also records the NM keyfile at
`/etc/NetworkManager/system-connections/prometheus-share-temporary.nmconnection`
as mode `0600` and saved. Those are claims from a root-capable prior run, not
facts directly read in this audit: current `iptables-save` was permission
denied and passwordless escalation was unavailable.

## Assessment and limits

The described firewall shape is narrow for its stated purpose. DHCP is
interface-scoped; DNS is interface and subnet-scoped; source NAT is subnet and
WAN-scoped. The hook does not itself add forwarding acceptance, so the sharing
path still depends on NetworkManager shared-mode behavior and the generated
firewall policy.

The `-C` then insert/append pattern makes ordinary serial invocation
idempotent. It is not atomic against an unrelated concurrent manual run: a
second process could insert a duplicate between the check and mutation. The
service's serialized reload path avoids that expected race.

This is mutable host `/etc` state rather than a NixOS generation. It is wired
to run after generated firewall startup and reload, so its design supports an
ordinary reboot, but neither reboot nor NM reconnect was tested here. A future
Nix switch, firewall rewrite, or iptables/nft backend change can alter the
`nixos-fw` chain or compatibility assumptions. The `/etc/systemd/system.control`
override may also remain after such a switch; a declarative owner must choose
one NAT/firewall owner and explicitly coordinate removal or coexistence.

An unprivileged current `systemd-analyze verify firewall.service` reports the
0700 hook as inaccessible. That reflects the verifier caller's access and does
not override the root service's observed successful execution.

## Rollback

The recorded narrow rollback removes only the named hook and drop-in, runs a
daemon reload, then removes only iptables rules with the four
`field-6db4fe-*` comments. Do not reset the firewall globally. The exact
rule-deletion commands were not independently available in this audit. Do not
withdraw the working temporary rules until a declarative replacement has passed
its activation and path checks.

## Sources

- Live local read-only inspection on Ouranos: systemd unit metadata and journal,
  `nmcli`, route state, ownership/mode metadata, 2026-09-21.
- Terra Attempt 9 raw receipt in
  `/home/li/.claude/projects/-home-li-primary/b80e5510-ebe7-436e-9259-2a47735f232d.jsonl`.
- `flows/753e69/reports/network-path-plan-2026-09-21.md`.
