# Tailnet merge to mains (da88cf deploy path), 2026-09-26

Subflow of 38de5b. W = witnessed here. No Lojix request was submitted and nothing was activated. Evaluation ran on ouranos with `max-jobs 0` and `builders @/etc/nix/machines`. Builds offloaded to `ssh-ng://nix-ssh@prometheus.goldragon.criome`. Fresh clones: `scratchpad/{goldragon,CriomOS,CriomOS-home}-mains-38de5b` (session 38de5bbb). Orchestrate locks 7392, 7393 and 7394 (one per clone) are released. Lock 7391 was a combined first attempt, released unused.

## Result

| Repo | main before | main after | How |
|---|---|---|---|
| goldragon | `ddf27e0c` | `ddf27e0c` (unchanged) | Already merged before this run. `ddf27e0c` "Merge tailnet-repair-da88cf into main" (li, 01:11) has parents `3e6ecfa9` (the five ciphertexts) and `e8ce1e42` (the bookmark head, with the CA). |
| CriomOS | `e6a83edc` | **`e6a83edc` (NOT pushed)** | `78121a03` fast-forwards cleanly, but the Prometheus `nix flake check` failed two remote builds. Stopped per the brief. |
| CriomOS-home | `4a9d85d7` | **`657f4ba8`** | Fast-forward to `f35913c1` (the 0.16 next pair). Then, on the coordinator's mid-task order, `657f4ba8` "field-clj: pin 3e5f450" went on top, on both `integration-2-b860be` and `main`. `git ls-remote` shows both at `657f4ba8167132a70357a4326532bcda2416b789`. |

## goldragon checks (W)

- The CA is in cluster data. `TailnetController.{ Some.<CA> { headscaleTlsCertificate } { headscaleTlsKey } }`. The decoded certificate:
  - subject and issuer: `CN=goldragon tailnet CA`
  - validity: 2026-09-26 to 2036-09-23
  - extensions: `CA:TRUE, pathlen:0` (critical); `keyCertSign, cRLSign`; critical name constraint `Permitted DNS:.goldragon.criome`
  - SHA-256 fingerprint: `BA:7A:EC:8E:…:AB:AD:51:27`
- Each of the five ciphertexts has one age recipient:
  - `headscaleTlsCertificate`, `headscaleTlsKey`, `tailnetCertificateAuthorityKey` and `tailnetPreauthKeyOuranos` are encrypted to `age15k8h…57zf0` (ouranos).
  - `tailnetPreauthKeyPrometheus` is encrypted to `age1wgft…qrg3d` (prometheus).
- Cluster data has five `TailnetClient` preauth names. Only **two** of them, Ouranos and Prometheus, reference files that exist. The other three are unminted by design (tailnet-repair-slice §3): `tailnetPreauthKeyMirrorAlpha`, `tailnetPreauthKeyMirrorBeta` and `tailnetPreauthKeyVmTesting`.
- `nix flake check` at `ddf27e0c` passed (rc 0). Its checks are horizon-definition, synchronizer and synchronizer-configuration. Building the outputs made 183 `building … on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'` lines, including `synchronizer-0.4.0.drv`. Store paths:
  - `/nix/store/6i5v50mhq6ljhi9s6vr1fbfmrvgz6w53-horizon-definition`
  - `/nix/store/c5yr2zxfhwpzinpvcmwdsgz63c66w7la-synchronizer-0.4.0`
  - `/nix/store/4y05wrvpw0rw8amlpzm10gmrcbd543x1-goldragon-synchronizer-configuration-check`

## CriomOS `78121a03` (integration-2-b860be)

Pins and ancestry (W):
- `78121a03` is a descendant of main `e6a83edc` (fast-forward possible) and contains `fd0be3f0`.
- It pins lojix `3fc95f0c` (8.1.0), so the merge would advance lojix from 8.0.0 to 8.1.0.
- It pins criomos-home **`7e96dcf5`**, not `f35913c1` or `657f4ba8`. The 0.16 next pair and the field-clj fix reach a deploy only after criomos-home is repinned.

The check was `nix flake check --keep-going --override-input system <lojix ouranos system>` (rc 1; log `scratchpad/criomos-check-38de5b.log`):
- **tailnet-declaration passed**: `/nix/store/r0ijhfq0jpywjj7jn72vjssknf9rvhls-tailnet-declaration`
- **tailnet-enrollment (VM) passed**: `/nix/store/l1v3zl23c84w2nbg2q4456w2idagxxlj-vm-test-run-tailnet-enrollment` (the same output as da88cf's integration-2 run)

Remote build failure 1 is a **regression on the b860be line**. It breaks `checks.usb-downlink-chain`, which passed at `fd0be3f0`. Its source is `d9f808e` "usb-downlink: remove the ouranos hotfix declaratively", in `modules/nixos/network/usb-downlink-hotfix.nix`:
```
error: build of '/nix/store/jh01wdhf59dqyky5zysa84bvj12p7vvq-usb-downlink-remove-hotfix.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome' failed
> In …/bin/usb-downlink-remove-hotfix line 26:
>     profileRemoved=yes
>     ^------------^ SC2034 (warning): profileRemoved appears unused.
```
This failure cascades into `activate.drv`, `nixos-system-prometheus-test` and `vm-test-run-usb-downlink-chain` (drv `xb7mva1s…`). The same module is on ouranos through UsbDownlink, so the real ouranos toplevel probably hits it too. That is **inferred** and was not evaluated here.

Remote build failure 2 is **likely pre-existing**. The criome pin `2f4dded8` is identical on main. It breaks `checks.criome-daemon-config-roundtrip`:
```
error: build of '/nix/store/31afdlsyfqwfg78sihrflywi8rmkydnj-criome-deps-0.9.0.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome' failed
criome-deps> error[E0432]: unresolved import `schema_rust::bootstrap::BootstrapInterfaceGeneration`
  --> …/meta-signal-criome-0.8.0/build.rs:18:19
```

Evaluation failures. None is a build.
- `nixosConfigurations.target`, `homeConfigurations` and `checks.agent-intercom-command-ownership` fail with "no horizon input was provided". These are stub inputs, and Lojix materializes them at deploy.
- `checks.home-activation-equivalence` fails with "called with unexpected argument 'inputs'".
- `nixosModules.testing` fails with "Path 'modules/nixos/testing/default.nix' does not exist".

## CriomOS-home checks (W)

Evaluation ran through CriomOS `78121a03` with criomos-home overridden, and the Lojix ouranos complete-host generated inputs supplied `horizon`, `system`, `deployment` and `secrets`.
- `checks.flow-message-next` at `f35913c1`: `/nix/store/8mdzlxbdsqigk9g8gsva4ns87l6k75v9-flow-message-next`
- ouranos generation at `f35913c1`: drv `aq6sc1cd…`, output `/nix/store/0qxxx3j5jdxsm97r3ia5008ad1bnp9rn-home-manager-generation`
- ouranos generation at `657f4ba8`: drv `mpz5lq43…`, the **same output** `0qxxx3j5…`
  - The field-clj deps FOD keeps its hash, so the derivation hash modulo FODs is unchanged. The generation still contains `a15b2pbq…-field-clj-uberjar`.
- These outputs were already realized, so this run printed no fresh build lines. `nix path-info --store http://nix.prometheus.goldragon.criome` confirms that Prometheus's cache holds `0qxxx3j5`, `8mdzlxbd`, `6i5v50mh` and `a15b2pbq`.
- The `657f4ba8` lock diff touches only `field-clj` (`a2c278d3` to `3e5f4501`) and its `clj-build` (`9c1778b2` to `8cc9991f`).

## Not sent

The b7da5d message in the brief assumed all three mains were merged. CriomOS was not merged, so the message was **not sent**. The main flow decides. A draft that fits the facts:

> From 38de5b: mains for the second ouranos deploy: goldragon main ddf27e0c (already merged; CA + 2 minted preauth refs + TLS refs verified), Home main 657f4ba8 (0.16 next pair + field-clj 3e5f450 — pin this); CriomOS main HELD at e6a83edc: integration-2-b860be 78121a03 (lojix 8.1.0) passes tailnet-declaration + tailnet-enrollment on Prometheus but fails usb-downlink-remove-hotfix shellcheck SC2034 (d9f808e, regression; breaks usb-downlink-chain) and criome-deps (pre-existing). Do not deploy until CriomOS main lands. field-clj FOD fix is already in Home 657f4ba8.
