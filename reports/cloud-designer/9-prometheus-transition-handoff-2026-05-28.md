# 9 · Prometheus transition — handoff to cloud-operator

Handing the prometheus Gemma/auth deployment to cloud-operator. All
design + config is in place and pushed; what remains is a **safe
activation** on a router node with **no console access**. This report
is the take-over context; the beads carry the work items.

## Goal

Bring prometheus (the largeAI node + LAN router) onto the new config:
both multimodal Gemma 4 models serving, llama-server auth enforced via
the sops-fed token. Build on prometheus; never pull models locally.

## Current state (all pushed unless noted)

- **CriomOS-lib** `main` @ `de676a8e` — `gemma-4-31b` + `gemma-4-26b-a4b`
  added to `data/largeAI/llm.json` (multi-shard BF16 + an `mmproj`
  field; hashes from HF LFS metadata, URLs commit-pinned). `fetchHfModel`
  + `nix-prefetch-huggingface` also landed here.
- **CriomOS** `main` @ `699c7a66` — `modules/nixos/llm.nix`: `apiKeyFile`
  → `config.sops.secrets.localLlmApiToken.path`; `sops.secrets.localLlmApiToken`
  declared; `mmproj = <fetchurl>` preset line for multimodal models;
  criomos-lib lock bumped.
- **goldragon** `main` @ `c8b5840d` — `secrets/local-llm-api-token.sops`
  (token age-encrypted to prometheus; minted blind via gopass at
  `goldragon.criome/local-llm-api-token`).
- **lojix-cli** branch `cloud-designer-llm-api-token-2026-05-28` @ `1cebc93b`
  — `src/artifact.rs` exposes `localLlmApiToken` in the generated
  secrets flake. **NOT yet on main — review + merge needed.** Until
  merged, deploy with `nix run github:LiGoldragon/lojix-cli/cloud-designer-llm-api-token-2026-05-28`
  (remote form — never a local `path:` checkout, per `skills/nix-discipline.md`).
- **Build:** the Gemma models + the new system generation
  (**gen 44**, `imiggsb678kn…`) are **already built/cached on prometheus**
  — a retry will not re-download.
- **prometheus right now:** booted the **old gen 40** (`4l0g3573…`) after
  a reboot; router + old models working. **`BootOnce` is staged:**
  gen 44 is the one-shot next-boot, default stays gen 40 (revertible).

## The incident + the hard lesson (do not repeat)

A live **`Switch`** deploy to prometheus knocked it off the network —
**twice**. Root cause: the activation runs *inside* the ssh, and our ssh
to prometheus rides the very router (hostapd/dnsmasq) the activation
restarts. When `switch-to-configuration switch` stops those, the ssh
dies, the half-finished activation is killed, and the router stays
down → unreachable. A backup WAN does **not** save this — it doesn't
change our administrative path into prometheus. (Spirit 1105, 1117.)

**Therefore, on the router node:**
- Use **`BootOnce`** (revertible) or `Boot` — never `Switch` — until
  there is console access. `BootOnce` runs `switch-to-configuration
  boot` (installs the bootloader, **restarts nothing**), keeps the old
  gen as default, and sets the new gen as a one-shot — so a reboot
  applies it and a second power-cycle reverts, **recoverable without
  console**.
- To activate **live without changing the boot default**, the action is
  `switch-to-configuration test` (applies the running config, leaves the
  bootloader alone). A full `Switch` always rewrites the boot default.
- A live activation can only survive the ssh drop if run **detached**
  on the host (`systemd-run`), so the restart completes after the ssh
  dies. Even then it commits the new gen as default (lockout risk if the
  new router config is broken). `BootOnce` is safer.

## Open technical points for the operator

1. **No console/out-of-band access to prometheus** — the core exposure.
   Get serial/IPMI/physical KVM before any risky activation; it makes a
   bad boot recoverable.
2. **Vision (mmproj) is runtime-unverified.** The mmproj is wired via a
   `mmproj = <path>` line in the llama-server router preset. Whether this
   llama.cpp build's `--models-dir` router applies a per-model mmproj is
   unconfirmed. Cheap to iterate: the weights are cached, so fixing the
   mmproj wiring is a config-only redeploy.
3. **Possible wifi password change.** The new gen's `hostapd` pre-start
   (`make-hostapd-wlp195s0-files`) changed — the interface is unchanged
   (`wlp195s0`), but the SAE password appears to move to the sops
   secret. If that value differs from the current wifi password, clients
   will need the new password after activation. Confirm before
   activating. This is from CriomOS `main` router-wifi-projection work
   ("align/tolerate derived router wifi names"), not the LLM changes —
   **coordinate with system-operator**, who owns the router projection.
4. **Build on prometheus** with `builder = prometheus` so models build
   remotely and nothing is realized locally (intent 1016).

## Recommended completion path

1. Get console/out-of-band access to prometheus.
2. Review + merge the lojix-cli branch to main (then deploy uses
   `github:LiGoldragon/lojix-cli` main).
3. Confirm (with system-operator) the router-wifi-projection change is
   correct for prometheus and whether the wifi password changes.
4. Deploy with **`BootOnce`**, reboot, verify gen 44 came up clean
   (router intact, both Gemma models serving, auth rejects tokenless
   requests, vision works). If clean → commit permanent. If broken →
   power-cycle reverts to gen 40.

## Anchors

- Incident root-cause: `reports/cloud-designer/8-deploy-network-incident-2026-05-28.md`.
- Execution detail: `reports/cloud-designer/6-secret-deploy-and-gemma-2026-05-28/5-execution.md`.
- Secret skill: `skills/secrets.md`. Remote-form skill: `skills/nix-discipline.md`
  §"Build, run, and deploy from the remote".
- Deploy command shape: `lojix-cli '(FullOs goldragon prometheus
  [/git/github.com/LiGoldragon/goldragon/datom.nota]
  [github:LiGoldragon/CriomOS/main] BootOnce (Some prometheus) None)'`.
- Intent: spirit 1011–1017, 1022–1023, 1032–1033, 1041, 1105, 1117, 1124.
