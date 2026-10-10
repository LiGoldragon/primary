# Corrected transient USB observer handover

This replaces the earlier transient observer handover. It is a runtime-only procedure for a later Field Sol executor. It has not been run on Ouranos, and this report does not authorize a start, a network probe, a replug, a restart, or a persistent unit installation.

## Exact artifact and generated-unit provenance

Mind Sol source revision `6485b64eaf328273d44b718d4c11da86b7554edd` fixes the carrier lookup: an entry under `brif` resolves to the bridge-port directory, which has no `carrier`; the implementation uses that entry only for membership and reads the matching member NIC's `carrier` through `/sys/class/net/<member>/carrier`.

The exact package is:

- package: `/nix/store/jmf1i2bglrwd4z4yn49bp55i1rgllv5z-usb-downlink-observer-0.1.0`
- executable: `/nix/store/jmf1i2bglrwd4z4yn49bp55i1rgllv5z-usb-downlink-observer-0.1.0/bin/usb-downlink-observer`
- derivation: `/nix/store/wcdfjac0a4y2wsyw22csgv8b1f7accmy-usb-downlink-observer-0.1.0.drv`
- NAR hash: `sha256-G7lKjP4eqRV76lvovUIdVfnmp8ejuE1Ta+wMuVlMTZk=`
- NAR size: `705152` bytes
- local path metadata: `signatures=[]`, `ultimate=false`

The package is not asserted to be signed or transferable through any particular cache route. The 112-byte `px7` check witness is not this package and must not be used as the executable.

The generated VM system unit used for command extraction is `/nix/store/714x81zd7i4zplkifykzlpamlks3x3vc-nixos-system-ouranos-test/etc/systemd/system/usb-downlink-observer.service`. Its generated `ExecStart` is the package executable above with `br-downlink`; its generated environment is reproduced exactly below. It permits only `AF_UNIX` and `AF_NETLINK`, denies IP traffic, has an empty capability bounding set, uses `NoNewPrivileges=true`, `UMask=0077`, `ProtectSystem=strict`, `ProtectHome=true`, and permits writes only at `/run/usb-downlink-observer`.

## Later executor command

Run only after Field preflight and applicable authorization. Field Sol is the sole later executor.

```sh
/run/current-system/sw/bin/systemd-run --system --unit=usb-downlink-observer-transient.service --collect --service-type=simple --description='Passive USB downlink evidence observer' --property='After=systemd-networkd.service kea-dhcp4-server.service' --property='Wants=systemd-networkd.service' --property='RuntimeDirectory=usb-downlink-observer' --property='RuntimeDirectoryMode=0755' --property='RuntimeDirectoryPreserve=no' --property='Restart=on-failure' --property='UMask=0077' --property='RestrictAddressFamilies=AF_UNIX' --property='RestrictAddressFamilies=AF_NETLINK' --property='CapabilityBoundingSet=' --property='NoNewPrivileges=true' --property='PrivateTmp=true' --property='ProtectSystem=strict' --property='ProtectHome=true' --property='ReadWritePaths=/run/usb-downlink-observer' --property='IPAddressDeny=any' --setenv='LOCALE_ARCHIVE=/nix/store/c59mcax29xrwyfdqs308wkmn2srnmzkn-glibc-locales-2.42-67/lib/locale/locale-archive' --setenv='PATH=/nix/store/wi4a31hyc5snfynn9s5000khsjd6dawm-iproute2-7.1.0/bin:/nix/store/97d5ygrvqj55f4nx1x34wfdcc7qn11c0-coreutils-9.11/bin:/nix/store/ibg16grw5is7i7ilnflc5xmj6fwksqkl-findutils-4.11.0/bin:/nix/store/4dgym2zhac9vy0vrih4gsplh0wpfl13m-gnugrep-3.12/bin:/nix/store/rxd8p6g4k4s0sx4q1szmzvp9rsmhmfys-gnused-4.10/bin:/nix/store/mc901k2s1n3v1disrj0356l7lwz7l6vg-systemd-261.1/bin:/nix/store/wi4a31hyc5snfynn9s5000khsjd6dawm-iproute2-7.1.0/sbin:/nix/store/97d5ygrvqj55f4nx1x34wfdcc7qn11c0-coreutils-9.11/sbin:/nix/store/ibg16grw5is7i7ilnflc5xmj6fwksqkl-findutils-4.11.0/sbin:/nix/store/4dgym2zhac9vy0vrih4gsplh0wpfl13m-gnugrep-3.12/sbin:/nix/store/rxd8p6g4k4s0sx4q1szmzvp9rsmhmfys-gnused-4.10/sbin:/nix/store/mc901k2s1n3v1disrj0356l7lwz7l6vg-systemd-261.1/sbin' --setenv='TZDIR=/nix/store/vlgjd2179ahfh509p1aid8fl22bw8ri3-tzdata-2026c/share/zoneinfo' /nix/store/jmf1i2bglrwd4z4yn49bp55i1rgllv5z-usb-downlink-observer-0.1.0/bin/usb-downlink-observer br-downlink
```

The transient adaptations are intentionally narrow. `--collect` and the transient unit name avoid installation or enablement. `RuntimeDirectory=usb-downlink-observer`, mode `0755`, and `RuntimeDirectoryPreserve=no` replace the declarative tmpfiles setup, provide the only writable directory allowed by `ProtectSystem=strict`, and remove that directory when the unit is stopped. The generated unit's executable, bridge argument, ordering, wants, restart policy, generated locale archive, PATH, TZDIR, and sandbox properties are otherwise unchanged.

To stop a later transient observation, use only:

```sh
systemctl stop usb-downlink-observer-transient.service
```

No manual cleanup, replug, probe, restart, or configuration change belongs to this procedure.

## Isolated VM test receipt

The final test ran as an isolated NixOS VM through the configured Prometheus builder and succeeded with output:

`/nix/store/y6rkkfr2yfjrw17y29q86mrsji4kyx0s-vm-test-run-transient-observer-corrected-handover`

The temporary test created `br-downlink` and a `fixture-port` veth member. It asserted both that `/sys/class/net/fixture-port/carrier` was `1` and that `/sys/class/net/br-downlink/brif/fixture-port/carrier` did not exist. It then invoked the full command above, using the exact package and generated environment.

The VM asserted that the transient service became active; `public.json` exposed `carrierUp` and the intentionally disabled recognizer state; the runtime directory had mode `0755`; `public.sock` and `public.json` existed; the effective service allowed `AF_UNIX` and `AF_NETLINK`, did not allow `AF_INET`, denied IP ranges, and had an empty capability bounding set. It stopped the transient unit and waited until `/run/usb-downlink-observer` no longer existed.

The test observed a bridge FDB event produced by its own veth setup, so it does not claim a production peer identity or a network-health result. It proves only the corrected direct-member carrier path and the transient service lifecycle/sandbox behavior in an isolated VM. No production host was started, stopped, probed, replugged, or restarted.
