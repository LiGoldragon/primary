# Registry pin removed: horizon

Before (`nix registry list | grep horizon`):
```
user   flake:horizon path:/tmp/flake-false-test/payload-stub
```
Before (`~/.config/nix/registry.json`):
```json
{
  "flakes": [
    {"from": {"id": "horizon", "type": "indirect"}, "to": {"path": "/tmp/flake-false-test/payload-stub", "type": "path"}}
  ],
  "version": 2
}
```

Evidence target missing: `ls /tmp/flake-false-test/payload-stub` and `ls /tmp/flake-false-test` both return "No such file or directory".

Owner search: grepped `/home/li/primary/flows/*/log.md` and `*/receipts/*.md` for `flake-false-test`/`payload-stub` — no matches (only the inventory report `flows/da88cf/reports/inventory-system.md` mentions it, no flow claims creating it). Checked `hm-list` — no live/working flow tied to this path.

Action: `nix registry remove horizon` (user scope only; system/global registries untouched, no declared files edited).

After (`nix registry list | grep horizon`): no output (entry gone).
After (`~/.config/nix/registry.json`):
```json
{"flakes": null, "version": 2}
```
