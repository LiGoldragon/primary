# Prometheus USB backup router access

## Frame

The psyche asked to move into production CriomOS work and use the newly connected Prometheus USB devices as backup connection points: one USB Wi-Fi adapter and two USB Ethernet adapters. The desired shape was a sturdy fallback management path, not another fragile high-tech layer that disappears during a system switchover.

## Live state applied

Prometheus now has the USB devices active as backup access paths in the running system:

- USB Wi-Fi `wlp199s0f0u4` is running as an access point with SSID `CRIOM Backup` on 2.4 GHz channel 11.
- Primary router Wi-Fi `wlp195s0` remains the existing `criome` AP on channel 6.
- USB Ethernet `enp197s0f4u1c2` is attached to `br-lan`.
- USB Ethernet `enp199s0f0u2` is attached to `br-lan`.
- `br-lan` remains the shared LAN bridge with the existing router DHCP/DNS/NAT path.

The backup Wi-Fi password was generated without printing it, stored as a gopass entry at `goldragon/router-backup-wifi-password`, and committed only as sops ciphertext in `goldragon/secrets/router-backup-wifi-password.sops`.

## Durable code landed

Pushed commits:

- `horizon-rs` `bb3e72a17dca` — adds typed backup wireless data under `RouterInterfaces`.
- `lojix-cli` `4c66b8a6fa55` — exposes the generated cluster sops files needed by CriomOS.
- `goldragon` `0298d216ff62` — authors Prometheus' `CRIOM Backup` interface and encrypted password.
- `CriomOS` `c250d9a6ce8e` — bridges USB Ethernet driver families, adds an independent backup hostapd service, and prevents automatic router-service restart on switch.
- `CriomOS` `15f1a52c05ff` — changes backup hostapd from `multi-user.target` startup to device-unit startup, so absent USB Wi-Fi does not make boot degraded and plugging it in later starts the backup AP.
- `CriomOS` `0f5428883f83` — adds an explicit udev `SYSTEMD_WANTS` trigger for the backup Wi-Fi interface, strengthening late-plug startup after an absent-at-boot device.
- `CriomOS-home` `0828935ee506` — pins the new `lojix-cli` in the user profile.

## Verification

Passed:

- `horizon-rs`: `cargo test` and remote `nix flake check github:LiGoldragon/horizon-rs --refresh`.
- `lojix-cli`: `cargo test` and remote `nix flake check github:LiGoldragon/lojix-cli --refresh`.
- `CriomOS-home`: local and remote `nix flake check`; `HomeOnly ... Activate` completed.
- Prometheus runtime: `hostapd-backup-wireless.service` active; AP enabled; both USB Ethernet links enslaved to `br-lan`.
- CriomOS router module: targeted Nix evaluation with generated Prometheus horizon + secrets confirmed the backup hostapd service is `wantedBy`/`bindsTo` `sys-subsystem-net-devices-wlp199s0f0u4.device`, udev has a `SYSTEMD_WANTS` trigger for `hostapd-backup-wireless.service`, and USB Ethernet matching carries `Bridge = br-lan`, `ConfigureWithoutCarrier = true`, `RequiredForOnline = no`, and `cdc_ncm`.
- Prometheus BootOnce deploy: built on Prometheus with `lojix-cli` builder `(Some prometheus)` and staged generation 45 as the one-shot boot entry. Current and persistent default entry remain generation 40.
- Prometheus staged LLM surface: generation 45 includes the Gemma 4 model IDs `gemma-4-31b` and `gemma-4-26b-a4b` alongside the existing model set.

## Deployment blocker

The earlier full Prometheus `FullOs ... Eval` through local evaluation failed while evaluating the existing `prometheus-llama-router.service` model closure. The follow-up deploy used Prometheus itself as the builder, which allowed the model-heavy closure to evaluate/build where the model store state exists.

The live backup access is active now through runtime commands. The durable OS generation is staged as BootOnce, not switched live. It will be exercised on the next reboot; if it fails, systemd-boot should fall back to the persistent generation 40 default after the one-shot attempt is consumed.
