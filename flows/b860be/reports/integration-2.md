# Integration step 2 (b860be): integration-2-b860be on CriomOS and CriomOS-home

Step-2 integrator subflow of b860be, on ouranos, 2026-09-26. I stopped early on the main flow's wind-down order, so the checks and VM tests below were **not run**. No `main` was moved, nothing was deployed, no message was sent to another flow. Evaluation ran on ouranos (`max-jobs = 0` in `nix config show`), and no build was started. Grades: **W** = witnessed here, **C** = claimed by another flow.

## Result (W, `git ls-remote https://github.com/LiGoldragon/<repo>.git`)

| Repo | Bookmark | Revision on the forge |
|---|---|---|
| CriomOS-home | `integration-2-b860be` | `7dd9e666a601945d99422c5dd63c65c8f8c4d474` |
| CriomOS | `integration-2-b860be` | `416afd41ad3cf38c8c374aa4192c181b50905211` |

Workspaces: `~/wt/github.com/LiGoldragon/{CriomOS,CriomOS-home}/integration-2-b860be` (made with `jj workspace add`). Orchestrate lock 7099 is released.

## Inputs as found on the remotes (W)

- CriomOS-home: `integration-2-da88cf` = `8a60835c`, `wave3-home-da88cf` = `182400f0`, `heartbeat-gate-b860be` = `9d721984`. All three are children of `98255d10`.
- CriomOS: `integration-2-da88cf` = `fd0be3f0`. It was still `fd0be3f0` at the last read; the main flow's note that it had moved to `c5ddf3a8` did not match the remote. `hotfix-removal-b860be` = `d9f808ec`, whose parent is `fd0be3f0`. `wave3-checks-da88cf` was absent from the remote at first (it existed only as local commits up to `50acd70e`, with more work uncommitted in its worktree). It appeared later at `a28fadfe`, a stack of six check-only commits on `c5ddf3a8`. CriomOS main = `e6a83edc`.
- field-clj main = `deps-hash-b860be` = `a2c278d3`.
- goldragon: `tailnet-repair-da88cf` = `e8ce1e42`, whose parents are `a3fdb232` and `0d462a33`.
  - **Brief claim corrected:** `e8ce1e42` does *not* hold the tailnet secrets. `3e6ecfa9` is not an ancestor of it, and its tree has only the four older `secrets/*.sops`.
  - goldragon main later became `ddf27e0c`, whose parents are `3e6ecfa9` and `e8ce1e42`. I checked it: its diff from `e8ce1e42` is only the five tailnet `.sops` files, and its `secrets/` is identical to `3e6ecfa9`'s.

## Home line (W)

1. `5ed097a1` merges `8a60835c`, `182400f0` and `9d721984` with `jj new … -m`. It has **no conflicts**, so I resolved nothing. The merge commit is empty (`jj diff -r 5ed097a1 --name-only` gives nothing). `nix flake lock --no-update-lock-file` changed nothing. field-luna-heartbeat is imported only from `modules/home/default.nix`; the field-monitoring module does not declare it, so the two do not overlap.
2. `7dd9e666` sets `field-clj.url = "git+ssh://git@github.com/LiGoldragon/field-clj.git?rev=a2c278d3…"`, then runs `nix flake update field-clj`. Only the `field-clj` lock node changed. Scope: `flake.lock`, `flake.nix`.

## CriomOS line (W)

1. `30dc65df` sits on `d9f808ec` (the hotfix removal, a fast-forward from `fd0be3f0`). It points `criomos-home.url` at `5ed097a1` and runs `nix flake update criomos-home`. The lock nodes that changed are criomos-home, flow, message, core-checkup-source, field-monitoring-source and field-luna-research-source; flow and message are Home's nodes only, not root inputs. Scope: `flake.lock`, `flake.nix`.
2. `2f810b7e` merges `30dc65df` with `a28fadfe` (wave3-checks). **No conflicts.** The merge is empty.
3. `accd6419` is the checks ruling. Blueprint's `nixos-*` check set filters `nixosConfigurations` on `x.pkgs…system`, so even listing the check names forces the host and throws `no horizon input was provided`. A name filter at the consumer therefore cannot work. The small CriomOS-side change is to call `inputs.blueprint { inputs = inputs // { self = inputs.self // { nixosConfigurations = { }; }; }; }`, which leaves Blueprint itself unchanged. `nixosConfigurations.target` is still published. Result: `checks.x86_64-linux` evaluates with only the `system` override and lists **48 checks**, with no `nixos-target`. Scope: `flake.nix`.
4. `416afd41` points `criomos-home.url` at `7dd9e666` and runs `nix flake update criomos-home`. The changed nodes are criomos-home and field-clj. Lojix stays `f090da079f71…` in both flake.nix and the lock. Scope: `flake.lock`, `flake.nix`.

## Composed-host evaluation (W)

**Horizon build.** `nix build --option max-jobs 0 'git+ssh://git@github.com/LiGoldragon/goldragon?rev=e8ce1e42…#horizon-definition'` gave `/nix/store/6i5v50mh…-horizon-definition`, and `#horizon-cli` gave `/nix/store/ahf5fwg8…-horizon-0.13.0`. Both were already in the store, so there were no build lines.

**Horizon projection.** `horizon-cli --node <n> < horizon-definition.datom` wrote `scratchpad/i2/horizon-<n>/horizon.json`. Each sits under a flake exposing `horizon = fromJSON …`.
- ouranos projects `usbDownlink 10.44.0.0/24` and `tailnetController` with `certificateAuthority` `MIIBzDCCAXOgAwIBAgIUQbqv…` (620 characters). Its TLS references are headscaleTlsCertificate and headscaleTlsKey, and its client key is tailnetPreauthKeyOuranos.
- prometheus projects country MX, `maxJobs` 8, `isRemoteNixBuilder` true, Metal with 16 cores, and tailnetPreauthKeyPrometheus. It sees the same CA on `exNodes.ouranos`.

**Secrets input.** This is real ciphertext, not fixtures: `scratchpad/i2/secrets-goldragon/` holds the nine `secrets/*.sops` from goldragon `3e6ecfa9` (identical to `ddf27e0c`) under a `sopsFiles` flake.

**The command, for each host `<n>`:**
```
nix eval --raw "path:$C#nixosConfigurations.target.config.system.build.toplevel.drvPath" \
  --override-input horizon path:$S/horizon-<n> \
  --override-input system path:/var/lib/lojix/generated-inputs/goldragon/<n>/complete-host/system \
  --override-input deployment path:/var/lib/lojix/generated-inputs/goldragon/<n>/complete-host/deployment \
  --override-input secrets path:$S/secrets-goldragon
```

| CriomOS | ouranos toplevel | prometheus toplevel |
|---|---|---|
| `30dc65df` | `mfhwaya7…-nixos-system-ouranos-26.11.20260813.0e251e2.drv` | `26ykhq1x…-nixos-system-prometheus-…drv` |
| `416afd41` | `6rap67pm…-nixos-system-ouranos-26.11.20260813.0e251e2.drv` | `z8ah830b…-nixos-system-prometheus-…drv` |

**Probe of `416afd41`** (`scratchpad/i2/probe.nix`, which gives the same values as on `30dc65df`, apart from Home activation):
- **ouranos**
  - networks: `05-usb-downlink`, `40-br-downlink`; netdev: `20-br-downlink`.
  - Kea on `br-downlink`, NAT on, internal interface `br-downlink`, NetworkManager unmanaged `interface-name:br-downlink`.
  - The `usbDownlinkLegacyHotfix` activation script is present.
  - `security.pki.certificateFiles` = `[…-tailnet-certificate-authority.pem]`.
  - tailnet-enroll unit present; headscale and tailscale on.
  - sops secrets: headscaleTlsCertificate, headscaleTlsKey, opencodeServerPassword, tailnetPreauthKeyOuranos. `nix max-jobs` 0.
  - Home user li, activation `rj5bay8a…-home-manager-generation.drv`. fieldLunaHeartbeat.enable = false, herdr.server.enable = false; no heartbeat, checkup, census, research or herdr user units, and no user timers.
- **prometheus**
  - `cfg80211.ieee80211_regdom=MX`; Kea on `br-lan`; NAT off; no hotfix activation.
  - The same CA pem; tailnet-enroll unit present, headscale off, tailscale on.
  - sops secrets: localLlmApiToken, routerBackupWifiPassword, routerWifiSaePasswords, tailnetPreauthKeyPrometheus. `nix max-jobs` 8. No Home users.

## Checks: evaluation only; nothing was built

**CriomOS**
- On `30dc65df` (before wave-3), per check through the wrapper `scratchpad/i2/wrap`, 41 check directories: 34 evaluate. The other seven fail:
  - ms2130-uvc-aspect-quirk (kernel pin)
  - lojix-ownership (`machine` missing)
  - opencode-testing-policy (`horizon` missing)
  - resolver-role-policy
  - router-non-router-lazy
  - wireguard-untrusted-proxy
  - criome-daemon-config-roundtrip (`Cannot build criome-0.9.0.drv`, import-from-derivation). This last one is the known pre-existing red: criome 0.9.0 fails to build on Prometheus (C, from the main flow).
- On `416afd41`: the 48-name set evaluates (above). The per-check drvPath pass was stopped by the wind-down after three checks. agent-intercom-command-ownership printed a failure with no error text captured, which is **unconfirmed**; agent-intercom-transport and bluetooth-resume-power-policy evaluated. So whether wave-3 clears its six checks on this merge is **untested here**. It is claimed built on Prometheus by wave-3 on `a28fadfe` (C).

**Home** (on `5ed097a1`, with the system override): the drvPaths of flow-service-path (`7ba7n1id…`), message-service-path (`mj2q09zr…`), herdr-agent-executable, herdr-server and field-monitoring all evaluate. These were **not rebuilt** on `7dd9e666`.

**Builds run:** none. **VM tests** (tailnet-enrollment, usb-downlink-chain): not run on these revisions. The last witnessed passes are da88cf's: tailnet-enrollment on `c5ddf3a8`, and usb-downlink-chain on `fd0be3f0` (`62cmcfmy…`). The field-clj FOD fix has not been built by me; that it builds is claimed by the field-clj writer (C).

## Readiness verdict

**Not ready to move the mains.** The merges are clean and both hosts evaluate with the CA, the UsbDownlink and the real secrets, but no merged check or VM test has run on `416afd41` or `7dd9e666`.

## For a successor

1. **Rerun the CriomOS per-check evaluation** on `416afd41`, from `$C=~/wt/…/CriomOS/integration-2-b860be`:
   ```
   nix eval --raw "path:$C#checks.x86_64-linux.<n>.drvPath" \
     --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system
   ```
   Each call takes minutes; `scratchpad/i2/build-one.sh` is ready. Then build each check one at a time with `--option max-jobs 0 -L` and keep the lines matching `building '…' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`. Build tailnet-enrollment and usb-downlink-chain last, one at a time.
2. **Home:** build flow-service-path, message-service-path, herdr-agent-executable, herdr-server and field-monitoring on `7dd9e666`. Then build the ouranos Home activation (`rj5bay8a…`); it is the first real witness that the field-clj FOD hash is correct.
3. **Main moves, if all green:**
   - CriomOS-home main `4a9d85d7` → `7dd9e666`. Fast-forward: `4a9d85d7` is an ancestor through `98255d10`; confirm with `jj log -r '4a9d85d7 & ::7dd9e666'`.
   - CriomOS main `e6a83edc` → `416afd41`. Fast-forward: `e6a83edc` is an ancestor through `c5ddf3a8`.
4. **Deploy revisions:**
   - ouranos and Prometheus: CriomOS `416afd41` (or main after the fast-forward) + goldragon `ddf27e0c`, the same data as `e8ce1e42` plus the nine secrets.
   - No rebase is needed. Lojix's generated secrets input must carry all nine goldragon files; today `/var/lib/lojix/generated-inputs/goldragon/<n>/complete-host/secrets` holds only four, so a Lojix run from `ddf27e0c` has to regenerate it.

Sources: `/tmp/claude-1001/-home-li-primary/b860be42-d89d-4eee-a0c2-216ec0107a86/scratchpad/i2/` — `goldragon-def.log`, `horizon-cli.log`, `horizon-*/`, `secrets-goldragon/`, `eval*-*.{out,err}`, `probe*.json`, `probe.nix`, `per-check-eval.txt`, `check-eval2.txt`, `criomos-checks-names.json`, `home-check-eval.txt`, `wrap/`.
