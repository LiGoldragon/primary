# Integration step 1: deploy-path branches onto main

Integrator subflow of da88cf, on ouranos, 2026-09-25, 21:25 to 22:50 CST. Nothing was deployed or activated. Evaluations ran on ouranos with `max-jobs 0`. Builds were offloaded to `ssh-ng://nix-ssh@prometheus.goldragon.criome`. Every push was verified with `git ls-remote` against the real GitHub remote. Grades: **W** = witnessed here, **C** = claimed by another flow, **U** = unknown.

## Result

| Repo | main before | main after | Pushed and verified |
|---|---|---|---|
| CriomOS-lib | `c74b2224` | `6db67c3bd53bdc308169a34e76f66a5332af0f89` | yes (W) |
| lojix | `c4bba4fa` | `c4bba4fa`, **not moved** | no; the check stalled (see below) |
| CriomOS-home | `5f14f9da` (00f95a's Flow 0.12.2 + messenger-clj, landed after lock 6820 released at 21:40) | `4a9d85d72b0c4057cf82293175a882cbde199b87` | yes (W) |
| CriomOS | `d193bafc` | `3e2cc8be83f03859dc4fafe6ddba17280c488e22` | yes (W) |

**Evaluated toplevels at CriomOS `3e2cc8be` (W):**
- prometheus: `/nix/store/hfc5kcivb5zib5mcccjn317r98ciimwh-nixos-system-prometheus-26.11.20260813.0e251e2.drv`
- ouranos: `/nix/store/mglzzvfa0fjda9xvr52nshcgq32dvq3j-nixos-system-ouranos-26.11.20260813.0e251e2.drv`

**Method.** This repeats the deploy-gap subflow's method.

```
nix eval --raw --option max-jobs 0 \
  --override-input {horizon,system,deployment,secrets} path:/var/lib/lojix/generated-inputs/goldragon/<host>/complete-host/<input> \
  "git+file:///git/github.com/LiGoldragon/CriomOS?rev=3e2cc8be…#nixosConfigurations.target.config.system.build.toplevel.drvPath"
```

The same drvs came out of an earlier run that overrode `criomos-home` with the unpushed merge. For comparison, Prometheus's running generation 55 is `0baaav…` (built from `da85c4a9`).

## 1. lojix

- `a67f5773` (7.0.0, branch `lojix-horizon-datom31-00f95a`) is a direct fast-forward of main `c4bba4fa`: it is two commits on top, with no rebase needed. **W**
- **Check.** `nix flake check github:LiGoldragon/lojix/a67f5773…` offloaded. Evidence line (W): `building '/nix/store/cjcxs2hxa766qzchb5vqrpzgp64fja0p-Cargo.toml.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`.
- **The check did not run to completion.**
  - The first run was interrupted at about 21:58.
  - The re-run was killed at about 22:24 on the main flow's order. It had stalled: its six build-hook sessions held every Prometheus builder slot but moved almost no data, and the matching Prometheus daemon workers were idle.
- Lojix main was therefore **not** moved, as ruled.
- CriomOS pins `a67f5773` directly, which is immutable on the remote branch. Per the main flow, its cargo tests ran earlier in 38de5b's wave. **C**
- Open: fast-forward lojix main once a full check passes.

## 2. CriomOS-lib

- The bookmark `models-da88cf` is `6db67c3b`: one commit on main `c74b2224` that restores `gemma-4-26b-a4b` beside `qwen3.5-122b-a10b` in `data/largeAI/llm.json`. **W**
- The repo has no flake checks; its only output is `lib`.
- Its commit records no check. The JSON parses and lists the two models. **W**
- It was fast-forwarded and pushed. Consumer evaluation ran through CriomOS: both toplevels evaluate with it.

## 3. CriomOS-home

**Order.** I waited for Orchestrate lock 6820 (00f95a) to be released. It was released at 21:40, polled every 60 s. Main then held `5f14f9da` "Declare Flow 0.12.2 and messenger-clj 0.2.5".

**Lock scoping.** A whole-repo lock was refused by the path overlap with lock 1019 (f7941a, `codex-artifact-gateway` files). I locked the 25 paths the merge touches instead (lock 6846).

**Merge.** A jj merge commit of main `5f14f9da` and `04446e78` (the Prometheus Home line: Herdr, Message, Codex-next and Claude-bypass repairs). Conflicts and how each was resolved:

- **`flake.nix`**
  - Kept main's `flow` (`34aaf787`, 0.12.2) and `messenger-clj` (`dfcf91f0`).
  - Dropped the branch's older `flow` `7cc19af0`, an ancestor of 0.12.2 (25 behind).
  - Took the branch's `message` `8aa6d7b4` (09-24, "Present hash-free recipient datoms at Herdr boundary"). It diverged from message main: 1 ahead, 3 behind. Newest declared by the running line. **W**
  - Kept both check lists: `messenger-clj-package` plus `flow-service-path`, `herdr-agent-executable`, `herdr-codex-integration` and `codex-next`, and `codex-next` in `basePackages`.
- **`modules/home/profiles/min/flow.nix`**
  - Main's null-safe package option and assertions.
  - Plus the branch's Codex stable/next client and endpoint environment, and its Herdr package selection.
- **`modules/home/profiles/min/message.nix`**: both sides had the same `{{…}}` writer line; the branch's pre-open preservation script was kept.
- **`checks/message-service-path`**: the branch version, which is a superset of main's.
- **`checks/flow-service-path`**
  - The branch structure, with `expectedFlowRevision` set to `34aaf787`.
  - Main's assertion index (1), plus an added assertion on `FLOW_CODEX_NEXT_SOCKET`.
- **`flake.lock`**: main's lock plus `nix flake update message`. Its only root-level differences from main: `message` moves to `8aa6d7b4`.

**flow-nexus unit versus live ouranos (W).**
- Evaluated `nixosConfigurations.target.config.home-manager.users.li.systemd.user.services.flow-nexus` at CriomOS `3e2cc8be` with ouranos inputs. Compared it with `systemctl --user cat flow-nexus` and the running process environment (PID 3450235).
- The live unit is the 04446e78-line unit plus the hand drop-in `override.conf`, which sets `ExecStart=/nix/store/c044v5pa…-flow-0.12.2/bin/flow-nexus`.
- The declared unit is identical in every field:
  - `FLOW_SOURCE_ROOT`;
  - `FLOW_CODEX_STABLE_{CLIENT,SOCKET,HOME,MODELS}` and `FLOW_CODEX_NEXT_{CLIENT,SOCKET,HOME,MODELS}`, with the same client store paths `0s199vn7…codex-stable-flow-client` and `x74szg3c…codex-next-flow-client`;
  - the same `PATH` (herdr-0.8.2, harness-0.3.4, codex-0.153.4, claude-code-2.1.280);
  - `ExecStart` is the same flow-0.12.2 store path, with no flags;
  - the same `After`/`Requires` on `codex-remote-control.service`, and `Restart=on-failure`.
- Nothing had to be added. The variable missing in deployment 29, `FLOW_CODEX_STABLE_CLIENT`, is declared. When activated, the drop-in becomes redundant.

**Checks.**
- `nix flake check` fails at evaluation on **Home main `5f14f9da` and on `04446e78` alone** with the same error, so the failure is **pre-existing**. **W**
  - The error: `Refusing to evaluate package 'platform-tools_r37.0.1-linux.zip' … unfree`. The Blueprint check set pulls androidenv without an unfree allowance.
  - The same failure blocks building single `checks.x86_64-linux.<name>` attributes, because the whole set is filtered with `isDerivation`.
- Workaround: the Home-specific checks were built directly with `callPackage` on each `checks/<name>` against the flake's inputs (with nixpkgs `allowUnfree`), offloaded. Evidence line (W): `building '/nix/store/0j77cxmkxk3z8acc5bliy2yhdq63ipjr-flow-service-path.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`. Results:
  - `flow-service-path`: pass (`/nix/store/bs81pz4a…-flow-service-path`)
  - `message-service-path`: pass (`/nix/store/h8hr9via…-message-service-path`)
  - `messenger-clj-package`: pass (`/nix/store/j5zqnp8r…-messenger-clj-home-package`)
  - `herdr-agent-executable`, `herdr-codex-integration`, `herdr-toast-delivery`, `codex-next`, `agent-intercom`: **not proven**. `herdr-agent-executable-contract.drv` has sat at "waiting for the upload lock to ssh-ng://nix-ssh@prometheus" since about 22:26. The merge did not touch these five checks; they come unchanged from the `04446e78` line that Prometheus gen 55 runs.
- Home was pushed on the main flow's gate: the Home-specific checks plus both host toplevels.

## 4. CriomOS

- On the main flow's refinement, the branch was **not merged**. Only its tip `da85c4a9` "Bind USB downlinks by stable udev bus role" was duplicated onto `d193bafc`, as `786ac218`. It touches `checks/router-usb-downlink-binding/default.nix` (new), `modules/nixos/network/networkd.nix` and `modules/nixos/router/default.nix`, with no conflicts. **W**
- The 12 pin-only branch commits were superseded by main and dropped.
- `prometheus-usb-downlink-5f38bc` was not touched.
- `headscale.nix` and `tailscale.nix` were not touched. The router module changed only by the duplicated USB commit.
- Pin commit `3e2cc8be` on top:
  - `lojix.url` → `a67f5773…`; lock `lojix` `c4bba4fa`→`a67f5773`, and `lojix/horizon` `40d04d25`→`ee8d6f8d`
  - `criomos-home.url` → `4a9d85d7…`; lock `478b4ea0`→`4a9d85d7`
  - lock `criomos-lib` `6e3bcb08`→`6db67c3b` (the input is unpinned in `flake.nix`, so the lock only)

**Checks.**
- As the main flow notes (Field report, C), the aggregate `nix flake check` fails because a Blueprint auto-discovered, target-dependent check is missing its target. This is pre-existing.
- It also fails for a second reason (W): `checks/lojix-ownership/default.nix` hard-codes `expectedRevision = "c4bba4fa…"`, `expectedPackageName = "lojix-6.0.0"` and `expectedHomeRevision = "f652ba9a…"`.
  - The Home revision already mismatched `d193bafc`'s Home pin (`478b4ea0`), so this check was already failing on main. It is pre-existing.
  - With the Lojix 7 pin it now also fails on the lojix revision.
  - Because Blueprint forces the whole check set, this blocks single-check builds such as `checks.x86_64-linux.router-usb-downlink-binding`.
  - Owed: update `lojix-ownership` to `a67f5773`, `lojix-7.0.0` and Home `4a9d85d7`.
- The deploy gate, per the main flow, is the two offloaded toplevel evaluations above. Both succeed. **W**
- `router-usb-downlink-binding`, built directly with `callPackage` at `3e2cc8be`, offloaded: see the addendum below.

## Locks

Released:
- 6832: lojix
- 6833: CriomOS-lib
- 6834: CriomOS
- 6846: CriomOS-home paths

No lock of this subflow remains.

## Unknowns and blockers

- **lojix main is still 6.0.0.** It needs a full offloaded check of `a67f5773` that runs to completion; tonight's stalled on the builder.
- **Five Home checks** (Herdr, Codex-next, agent-intercom) are unproven because the upload lock to Prometheus is stuck. Who holds that lock is **U**.
- **CriomOS `lojix-ownership`** is stale (see above).
- **Home's aggregate check** fails on unfree platform-tools. It is pre-existing and needs its own fix.
- **message `8aa6d7b4`** is not on message main (1 ahead, 3 behind). The Home now pins a side revision; the running line pinned the same one.
- The toplevel drvs are evaluated only; nothing was realized. Realizing Prometheus still pulls the model closure through ouranos. The catalog is now two models (Qwen3.5-122B and Gemma 4 26B BF16, about 128 GB); Gemma's size here comes from `sizeGB` in `llm.json`.

## Sources

- Lock and push evidence: `orchestrate` replies (6832, 6833, 6834, 6846, 6820 poll log); `git ls-remote` of `LiGoldragon/{CriomOS-lib,CriomOS-home,CriomOS}`.
- Pre-existing failures: `nix flake check --no-build` of Home `5f14f9da` and `04446e78`.
- Live unit: `systemctl --user cat flow-nexus`, `/proc/3450235/environ`.
- Scratch logs: `/tmp/claude-1001/-home-li-primary/da88cf8d-06f7-4a70-9c7a-e7c8cdb78908/scratchpad/integrate-1/`
  - `lojix-check-1.log`, `lojix-check.log`
  - `home-check.log`, `home-checks.log`, `home-checks.nix`
  - `eval-pre.out`, `eval-home-override.out`, `eval-final.out`
  - `declared-flow-nexus.json`
  - `criomos-usbcheck.{nix,log}`
  - `lock6820.log`
- Brief: `flows/da88cf/reports/prometheus-pending.md`.
