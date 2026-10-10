# Zeus live system state

Method: probe the configured Zeus read-only route with `readlink`, `systemctl`, `bootctl`, journal queries, Nix path metadata, and filesystem-capacity queries.

## Observations

- `/run/current-system` and `/nix/var/nix/profiles/system` resolve to the successful deployment-54 tested closure `v8fpnkhj8lv6yh0x03xj9izlzjzrcssy-nixos-system-zeus-26.11.20260813.0e251e2`.
- `/run/booted-system` remains the previous generation 63 because no reboot was authorized or performed.
- systemd-boot current entry remains generation 63; its persistent default is the new generation 64.
- `systemctl is-system-running` returned `running`; the failed-unit set was empty after deployment 55.
- The previously failed `complex-init.service` journal reported the legacy request-shape parse error. After deployment 55 it was no longer failed.
- Reported capacity was 56G free of 468G on `/` and 336M free of 500M on `/boot`.

## Hypotheses

None. The differing booted generation is expected before a reboot.

## Unknowns

The live closure lacks an exported `configuration-revision` file. Immutable source provenance is therefore established by Lojix deployment 54/55 rather than that runtime file.
