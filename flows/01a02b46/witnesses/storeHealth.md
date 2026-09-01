# Store health and signature state

Method: read `nix show-config` locally and over strict SSH; read local candidate metadata with `nix path-info --json --recursive --sigs --no-pretty <candidate>` and `nix path-info --recursive --closure-size --human-readable <candidate>`; query the candidate with target-local `nix path-info`; read target `df -B1 /nix`, `df -B1 -i /nix`, `stat -f`, `readlink`, and `nix store info`; and read the active unit's `ExecStartPre` configuration.

The realized candidate is locally present as:

```text
/nix/store/jz6mg0qlm3w3h2h5jxwldccncjgcz22j-nixos-system-zeus-26.11.20260813.0e251e2
```

Its local path metadata has `signatures: []`. Its recursive local closure contains 3,579 registered paths: 1,203 with no signatures and 2,376 with at least one signature. The reported recursive NAR closure size is 34.5 GiB. These are store metadata queries; they do not verify file contents.

On Zeus, the same candidate is not a valid path (`error: path ... is not valid`). Zeus remains on `system-63-link` and `/run/current-system` resolves to the generation-63 NixOS path. Current `/nix` capacity is 66,240,503,808 bytes free; inode capacity is 28,191,543 free (10% used). The target's local store probe reports Nix `2.34.6` and `Trusted: 1`.

Both local and target Nix configuration report `require-sigs = true`, empty `secret-key-files`, and trusted public-key entries for cache.nixos.org, ouranos, prometheus, tiger, and zeus. The local service also uses `builders = @/etc/nix/machines`. The active Lojix unit writes `effect_timeout_seconds = 2700` into its startup configuration.

The unsigned candidate plus target signature policy is a credible independent copy-failure cause, and the Lojix source comment explicitly warns that unsigned daemon-to-daemon transfer is rejected under `require-sigs`. It is not the leading explanation for this incident because the correlated SSH session ran for essentially the full 2700-second effect timeout; the actual stderr was discarded before terminalization.

No `nix store verify`, garbage collection, path deletion, or copy was run. The target's reported free space and inode count do not establish whether any of the roughly 13 GiB consumed during the failed transfer is valid registered store data or temporary/incomplete transfer residue.

