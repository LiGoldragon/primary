# Intel I219-LM Ethernet carrier drop research

## Executive finding

The failure on `ouranos` was a physical-link-layer loss on the onboard Intel I219-LM controller, not a DHCP, DNS, NetworkManager profile, or unplugged-cable problem. The local kernel log shows the sequence:

1. `e1000e ... enp0s31f6: NIC Link is Down`
2. `e1000e ... enp0s31f6: Failed to enable ULP`
3. NetworkManager then saw carrier off and correctly refused to activate the wired profile.

The most likely class of fault is the Intel `e1000e` power-management / PHY-management path for I219-LM, involving ULP/S0ix/SMBus/Management Engine handoff. EEE was a plausible contributor and disabling it plus bouncing the interface recovered the link, but the logs do not prove EEE was the original trigger.

## Local facts

| Item | Observed value |
|---|---|
| Host | `ouranos` |
| Hardware vendor/model | Lenovo `21MLS18Y00` |
| BIOS | `N47ET23W (1.12)`, dated 2024-12-18 |
| Ethernet controller | Intel Ethernet Connection (18) I219-LM, PCI ID `8086:550b`, rev 20 |
| Driver | `e1000e` |
| Kernel | Linux `7.0.1` |
| Interface | `enp0s31f6` |
| Failure state | `NO-CARRIER`, `/sys/class/net/enp0s31f6/carrier = 0`, speed `-1`, duplex `unknown` |
| Recovery action | `ethtool --set-eee enp0s31f6 eee off`, then `ip link set enp0s31f6 down/up` |
| Recovered state | carrier `1`, speed `1000Mb/s`, full duplex, NetworkManager connected |

The link partner advertised 10/100/1000 autonegotiation while the local NIC still reported no link. That means the cable and remote port were not simply invisible. The local PHY/driver state was stuck or failed to negotiate carrier.

The recovery test also showed:

- gateway ping over Ethernet succeeded with 0% packet loss
- public IP ping over Ethernet succeeded with 0% packet loss
- NetworkManager connectivity check reported `full`

## What ULP and EEE are

ULP is Intel Ultra Low Power handling inside the `e1000e` driver and Intel PHY/firmware path. It is tied to runtime suspend, S0ix, wake-on-LAN, and Management Engine / manageability behavior on LM parts.

EEE is IEEE 802.3az Energy Efficient Ethernet. It lets Ethernet links enter low-power idle states and wake/renegotiate as needed. It is negotiated between the NIC and the switch/router. If either side is slow or buggy, the visible symptom can be link flap, no carrier, low negotiated speed, or repeated activation failure.

On this host, EEE before recovery was `enabled - inactive`, and the link partner did not advertise EEE. That reduces confidence that EEE itself was the root cause. Disabling EEE was still a useful mitigation because it removes one low-power link-negotiation variable from a known brittle NIC family.

## Upstream evidence

### I219-LM ULP and Management Engine are a known brittle path

Ubuntu bug 1865570 states that some ThinkPads failed suspend because the I219 chip on some platforms is controlled by the Management Engine, which needed more time while setting ULP mode. The bug's fix rationale says: `I219 chip of some platforms is controlled by ME, which needs more time when setting ULP mode. Wait for ME to finish setting ULP mode.`

Source: https://bugs.launchpad.net/ubuntu/+source/linux/+bug/1865570

That same bug thread includes an explicit test where disabling `e1000e_s0ix_entry_flow()` / `e1000e_s0ix_exit_flow()` made repeated suspend work, with the reporter concluding that the S0ix implementation was the culprit. That does not prove our failure was suspend-triggered, but it places I219-LM ULP/S0ix handling in the known-risk bucket.

### e1000e has had multiple ULP failure fixes

A 2020 upstream patch was titled `e1000e: continue to init phy even when failed to disable ULP`. It says ThinkPad P14s systems failed to disable ULP by ME after an e1000e S0ix change; the example error sequence included `Failed to disable ULP`, `PHY Wakeup cause`, and `Hardware Error`. The patch rationale says continuing PHY initialization allowed the device to work.

Source: https://www.spinics.net/lists/kernel/msg3554191.html

A 2024 upstream patch was titled `e1000e: move force SMBUS near the end of enable_ulp function`. It says a prior commit introduced a regression on PCH_MTP_I219_LM18, including Ethernet failing after suspend/resume and the link changing from 1000 Mbps to 10 Mbps. The patch was verified on Lenovo laptops including hardware ID `8086:550b`, exactly this host's Ethernet device ID.

Source: https://lore.kernel.org/netdev/20240517135059.10646-1-hui.wang@canonical.com/

This is the strongest external match: `ouranos` has Intel I219-LM device `8086:550b`, and upstream specifically lists Lenovo systems with that ID in a ULP/SMBus regression fix.

### Persistent EEE disablement is normally done through NetworkManager or boot-time ethtool

Modern NetworkManager has an `ethtool.eee-enabled` connection setting. The local `nm-settings-nmcli` manual confirms:

```text
ethtool.eee-enabled
Format: ternary
Valid values: on, off, ignore
```

A Unix & Linux answer also recommends `nmcli connection modify <connection_name> ethtool.eee-enabled off` when NetworkManager supports the ethtool setting.

Source: https://unix.stackexchange.com/questions/729508/how-to-permanently-disable-eee-energy-efficient-ethernet-on-ethernet-card

## Current firmware angle

`fwupdmgr get-updates` reports available firmware updates:

- System Firmware: current `0.1.12`, available `0.1.17`, high urgency
- Intel Management Engine: current `0.10.2403`, available `0.15.2515`, high urgency

The Management Engine update matters because upstream ULP bugs explicitly mention I219 being controlled by ME on some platforms. I did not apply firmware updates; they require external power and reboot, so they need an explicit maintenance window.

## Root-cause assessment

Most likely:

- The I219-LM PHY or e1000e driver power-management state got wedged after carrier loss.
- The failed ULP transition is a symptom of that brittle path and may also have prevented clean recovery until the interface was bounced.
- The LM manageability path and ME/SMBus handoff are likely involved, based on upstream matches for Lenovo I219-LM hardware.

Possible but less proven:

- EEE negotiation confused the link partner or NIC enough to trigger the carrier drop. Disabling EEE recovered the link, but the pre-fix state was `enabled - inactive`, not clearly active.
- Firmware age contributed. The available ME and system firmware updates are relevant but not proven causal.
- A transient cable/switch event initiated the carrier loss, and the Intel power path then failed to recover.

Unlikely:

- NetworkManager profile mismatch: the profile was bound to `enp0s31f6`, DHCP was normal after carrier returned, and NetworkManager's error followed kernel carrier state.
- Plain cable unplug: ethtool saw link partner advertisement while the kernel reported no local carrier.
- DNS or route failure: after link recovery, gateway and public IP pings succeeded over Ethernet.

## Prevention options

### Low-risk immediate mitigation

Set the NetworkManager wired profile to keep EEE off:

```sh
nmcli connection modify 'Wired connection 1' ethtool.eee-enabled off
nmcli connection down 'Wired connection 1'
nmcli connection up 'Wired connection 1'
```

This should persist in NetworkManager connection state. It is not yet declarative Crayon OS state unless represented in the NixOS/Home networking configuration.

### Declarative host mitigation

Add a host-level oneshot or NetworkManager connection setting in CriomOS that applies `ethtool --set-eee enp0s31f6 eee off` for this Lenovo/I219-LM interface. This makes the known-good mitigation survive reboot and profile rebuilds.

Prefer the NetworkManager `ethtool.eee-enabled = off` path if the declarative NixOS module surface can represent it cleanly. Use a small systemd oneshot only if the NetworkManager declarative path is too awkward.

### Firmware maintenance

Schedule a firmware maintenance window with power attached and apply Lenovo System Firmware and Intel Management Engine updates through fwupd. The ME update is specifically relevant to this class because upstream e1000e ULP issues cite ME-controlled I219 behavior.

### Recurrence diagnostic bundle

If the problem recurs before permanent mitigation, collect this before and after recovery:

```sh
journalctl -k -b | grep -Ei 'e1000e|enp0s31f6|ULP|SMBUS|PHY|Link is'
nmcli device show enp0s31f6
cat /sys/class/net/enp0s31f6/carrier /sys/class/net/enp0s31f6/operstate
ethtool enp0s31f6
ethtool --show-eee enp0s31f6
ethtool -S enp0s31f6
```

If the link only recovers after reboot or module reload, escalate beyond EEE to one or more of: kernel regression check, ME/system firmware update, e1000e module parameter testing, or disabling deeper PCI runtime power management for the device.

## Recommended next action

Best practical prevention sequence:

1. Persist `ethtool.eee-enabled off` for `Wired connection 1`.
2. Add a declarative Crayon OS host setting for the same behavior so it survives rebuilds.
3. Schedule and apply Lenovo System Firmware and Intel Management Engine updates.
4. If the failure recurs with EEE disabled and firmware current, test a targeted e1000e power-management mitigation such as disabling SmartPowerDown or PCI runtime PM for this device.

Do not start with broad kernel parameters like `pcie_aspm=off` unless narrower mitigations fail; those have wider power and platform effects.
