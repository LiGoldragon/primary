# Flow 5a3ee4 — Codex update and redeploy

Trigger: Astra released by OpenAI; update Codex on CriomOS-home, redeploy li, redeploy Zeus (Bird).

## Log

- Investigated: Codex at owned-agents/codex/ in CriomOS-home, pinned v0.152.1. Update script: update.py.
- Zeus is a cluster node, Bird is a user on Zeus/Tiger.
- Deployments via Lojix typed requests.
- Codex updated 0.152.1 → 0.153.2 in CriomOS-home, committed b36502d, pushed.
- pi-models.nix marked deprecated in same commit.
- CriomOS flake lock updated to pin new Home, committed 2c34e94, pushed.
- Zeus CompleteHost deployment 158 accepted.
- li UserEnvironment deployment 159 accepted.
- li UserEnvironment deployment 159: **Succeeded**.
- Zeus CompleteHost deployment 158: **Failed** — CopyClosure BuilderUnreachable (Prometheus builder unreachable, same as deployment 30).
- Bird UserEnvironment on Zeus: blocked by Zeus CompleteHost failure.
- ChatGPT desktop updated 26.901.20858 → 26.901.31953 in CriomOS-home, committed 7e99bd1, pushed.
- CriomOS flake lock updated again to pin ChatGPT update, committed 5ed835d, pushed.
- Round 2 deploys at CriomOS rev 5ed835d:
  - li UserEnvironment deployment 161: **Succeeded** (Codex 0.153.2 + ChatGPT 26.901.31953).
  - Zeus CompleteHost deployment 162: **Failed** — CopyClosure BuilderUnreachable (same Prometheus issue).
  - Bird UserEnvironment on Zeus: still blocked.
- pi-models.nix marked deprecated (psyche: "pi is slop").
- Diagnosis: deployments 158 and 162 used the stale LAN transport `ssh-ng://root@192.168.18.95`; `nix copy` failed immediately with "No route to host." Lojix maps all CopyClosure failures to `BuilderUnreachable` regardless of actual cause (`schema_runtime.rs:3724`). Prometheus was never unreachable. The correct transport is `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)`.
- Zeus CompleteHost deployment 165 at CriomOS rev eefa86f: **Succeeded**. Lojix records 165 Current/LiveActivation. Zeus system running.
- Bird UserEnvironment deployment 166 at same rev failed: CopyClosure with `ssh-ng://bird@zeus.goldragon.criome` — no SSH key for bird from Ouranos.
- Bird UserEnvironment deployment 167 with root-mediated transport `(ssh-ng://root@zeus.goldragon.criome root@zeus.goldragon.criome)`: **Succeeded**. Lojix records 167 Current/LiveActivation.
- Lojix 0.20.3 implemented: `ClosureCopy` now always copies as root — extracts host from the caller's `nix_store_uri` and constructs `ssh-ng://root@<host>`, so UserEnvironment deployments with user-scoped transport no longer fail at CopyClosure. Lojix commit `d3c0ac90`, CriomOS pin `59d12e6f`.
- Ouranos CompleteHost deployment 179 at CriomOS rev 59d12e6f: activation failed (pre-existing `complex-init.service` issue), but system updated and Lojix 0.20.3 running.
- Bird UserEnvironment deployment 180 with user-scoped transport `(ssh-ng://bird@zeus.goldragon.criome bird@zeus.goldragon.criome)`: CopyClosure **passed** (root-derived URI worked), activation failed (bird SSH has no authorized key from Ouranos — separate from the Lojix fix).
- Zeus CompleteHost deployment 181 at CriomOS rev 59d12e6f: **Succeeded**. Lojix records 181 Current.
