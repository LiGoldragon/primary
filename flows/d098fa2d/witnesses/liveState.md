Subject: Current Lojix daemon and Zeus live record.

Method: probe hostname; test -S /run/lojix/ordinary.sock; test -S /run/lojix/owner.sock; readlink -f /run/current-system/sw/bin/lojix; systemctl is-active lojix-daemon.service

The dispatcher is `ouranos`. Both Lojix sockets exist, the active daemon/client build resolves to Lojix 0.17.5, and `lojix-daemon.service` is active.

Method: probe `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon zeus None)'`

The typed ordinary query returned `Queried.([] [] (625 625))`: no Zeus generations and no Zeus deployment records in the current daemon state. A comparable query for `ouranos` returned existing records, proving the query reached the live daemon rather than merely parsing locally.

Method: probe `find /var/lib/lojix/generated-inputs/goldragon/zeus -maxdepth 4 -type f -printf '%P\\n'`

Retained `complete-host`, `full-os`, `home`, and `user-environment` generated-input trees exist for Zeus. The complete-host horizon was timestamped 2026-07-25 and the full-os horizon 2026-07-02, so these are historical materialized inputs, not proof of a current deployment.

Method: probe `awk '{print $1, $2, $3, $4, $5, $6, $7}' /etc/nix/machines`; `nix config show`

The dispatcher configuration names Prometheus as a remote builder and has `builders = @/etc/nix/machines`, `max-jobs = 1`, and `fallback = true`. This local setting does not settle the request-owned optional `NixBuilderSpec`; current Lojix passes an explicit builder only when the request supplies one.
