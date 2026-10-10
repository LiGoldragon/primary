# Transient USB observer handover

This artifact supersedes every earlier transient observer command. Do not run an earlier message.

It is derived from the generated service in immutable BaseHost closure `/nix/store/hs9mi4mvna45i1bpfklamkm0ajk8i8qb-nixos-system-ouranos-26.11.20260813.0e251e2`, built from CriomOS `0fe91588d60b642de851dee3f08073082989de2b`. The closure NAR hash is `sha256-Td6ruNaeZqunzbMUXnBOHsMMMs4n2r0c6RJ06F9hQhI=`. The observer executable was preflight-witnessed executable; no generated observer unit or runtime directory exists on the live host, and no prior `systemd-run` command ran.

Field Sol is the sole executor. This starts one runtime-only system service. It does not install, enable, link, or override a unit; it disappears on reboot. It is not whole-system deployment.

```sh
/run/current-system/sw/bin/systemd-run --system --unit=usb-downlink-observer-transient.service --collect --service-type=simple --description='Passive USB downlink evidence observer' --property='After=systemd-networkd.service kea-dhcp4-server.service' --property='Wants=systemd-networkd.service' --property='RuntimeDirectory=usb-downlink-observer' --property='RuntimeDirectoryMode=0755' --property='RuntimeDirectoryPreserve=no' --property='Restart=on-failure' --property='UMask=0077' --property='RestrictAddressFamilies=AF_UNIX' --property='RestrictAddressFamilies=AF_NETLINK' --property='CapabilityBoundingSet=' --property='NoNewPrivileges=true' --property='PrivateTmp=true' --property='ProtectSystem=strict' --property='ProtectHome=true' --property='ReadWritePaths=/run/usb-downlink-observer' --property='IPAddressDeny=any' --setenv='LOCALE_ARCHIVE=/nix/store/c59mcax29xrwyfdqs308wkmn2srnmzkn-glibc-locales-2.42-67/lib/locale/locale-archive' --setenv='PATH=/nix/store/wi4a31hyc5snfynn9s5000khsjd6dawm-iproute2-7.1.0/bin:/nix/store/97d5ygrvqj55f4nx1x34wfdcc7qn11c0-coreutils-9.11/bin:/nix/store/ibg16grw5is7i7ilnflc5xmj6fwksqkl-findutils-4.11/bin:/nix/store/4dgym2zhac9vy0vrih4gsplh0wpfl13m-gnugrep-3.12/bin:/nix/store/rxd8p6g4k4s0sx4q1szmzvp9rsmhmfys-gnused-4.10/bin:/nix/store/mc901k2s1n3v1disrj0356l7lwz7l6vg-systemd-261.1/bin:/nix/store/wi4a31hyc5snfynn9s5000khsjd6dawm-iproute2-7.1.0/sbin:/nix/store/97d5ygrvqj55f4nx1x34wfdcc7qn11c0-coreutils-9.11/sbin:/nix/store/ibg16grw5is7i7ilnflc5xmj6fwksqkl-findutils-4.11/sbin:/nix/store/4dgym2zhac9vy0vrih4gsplh0wpfl13m-gnugrep-3.12/sbin:/nix/store/rxd8p6g4k4s0sx4q1szmzvp9rsmhmfys-gnused-4.10/sbin:/nix/store/mc901k2s1n3v1disrj0356l7lwz7l6vg-systemd-261.1/sbin' --setenv='TZDIR=/nix/store/vlgjd2179ahfh509p1aid8fl22bw8ri3-tzdata-2026c/share/zoneinfo' /nix/store/mvgklvrvmywxm4yjfv7h5p3sf1lf79kk-usb-downlink-observer-0.1.0/bin/usb-downlink-observer br-downlink
```

Every service behavior above is exact from the generated unit except these transient mechanics:

- `usb-downlink-observer-transient.service`, `--collect`, and direct start replace the declarative unit name and `WantedBy=multi-user.target`. They create no persistent unit or enablement.
- `RuntimeDirectory=usb-downlink-observer` and mode `0755` replace the generated module's tmpfiles precreation, `d /run/usb-downlink-observer 0755 root root -`. The directory is necessary because `ProtectSystem=strict` only permits this writable path.
- `RuntimeDirectoryPreserve=no` makes systemd's default removal behavior explicit. On a normal stop, the inner runtime directory and its public socket/state are removed. No manual deletion is requested.

The generated description, ordering, wants, restart policy, umask, two allowed address families, empty bounding set, privilege and filesystem hardening, read/write exception, IP denial, executable, bridge argument, locale archive, path, and timezone are otherwise unchanged. The earlier error came from manually reconstructing the environment instead of taking it from the generated service; specifically it selected a glibc locale path rather than the generated `glibc-locales` archive.

For a later observation, Field may inspect the public artifacts and unit properties without reading root diagnostics:

```sh
systemctl show usb-downlink-observer-transient.service -p ActiveState -p RestrictAddressFamilies -p IPAddressDeny -p CapabilityBoundingSet
stat -c '%a %n' /run/usb-downlink-observer /run/usb-downlink-observer/public.sock /run/usb-downlink-observer/public.json
cat /run/usb-downlink-observer/public.json
```

To end the transient service, use only:

```sh
systemctl stop usb-downlink-observer-transient.service
```

`--collect` and `RuntimeDirectoryPreserve=no` let systemd unload the stopped transient unit and remove the runtime directory. No cleanup command, replug, probe, or restart is part of this handover.

## Isolated test receipt

The command was tested in an isolated NixOS VM, realized through the configured Prometheus builder. It used the exact hs9 observer executable and all three generated environment values. The terminal test output was `/nix/store/j34sq6zqq2hk2sk0ahrq6kl4s41qv6cz-vm-test-run-transient-observer-systemd-run`.

The test started the transient unit through the command above, waited for it to become active, and asserted:

- `/run/usb-downlink-observer` exists with mode `0755` and contains `public.sock` and `public.json`;
- the effective unit allows `AF_UNIX` and `AF_NETLINK`, denies all IP ranges, and has an empty capability bounding set;
- the effective environment contains the exact `glibc-locales` `LOCALE_ARCHIVE` path; and
- after `systemctl stop`, `/run/usb-downlink-observer` no longer exists.

The VM had no `br-downlink`, so the observer recorded `linkAbsent` and its optional `bridge monitor` child reported that the bridge did not exist. That is an isolated startup condition, not a host event witness. The service itself remained active, its public socket and state were created, and the sandbox/lifecycle assertions passed. No production observer, network action, probe, or host mutation occurred during this test.
