# Deployment transport preflight

- DNS/Yggdrasil: Ouranos `201:6de1:5500:7cac:2db9:759e:42d2:fb1d`; Prometheus `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f`; Zeus `200:17f7:4fad:e50b:a50c:2048:2169:41f7`.
- Declared root deployment transports: `ssh-ng://root@<host>.goldragon.criome`, paired with `root@<host>.goldragon.criome`.
- `ssh -o BatchMode=yes -o ConnectTimeout=8 -o StrictHostKeyChecking=yes root@prometheus.goldragon.criome true`: success.
- Same Zeus probe: success.
- Prometheus current and booted system both resolve to `7f8kpzcnj3x03p5057fvs91k6wjvjwqz-nixos-system-prometheus-26.11.20260813.0e251e2`; 45 boot entry files; nix-daemon and sshd active.
- Zeus current and booted system both resolve to `kgg7yk3b22w0dakn9sz3l6nz23rcw5ly-nixos-system-zeus-26.11.20260813.0e251e2`; 13 boot entry files.
- Ordinary Query.ByNode: Prometheus has historical terminal Lojix records, including deployment 31 TestActivation failed at build; no records/active rows for Zeus.
