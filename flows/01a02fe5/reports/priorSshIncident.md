# Prior SSH incident

The closest recent incident is the 2026-08-19 failure on `ouranos`, where a Lojix `CopyClosure` used same-host SSH as `li`. It is a strong lead for an SSH outage involving an agent boundary, but it does not establish that the present all-host failure has the same cause.

## Observations

- Session `01a0193f-059c-7393-9d4d-4bb50ef1bc98` recorded deployment 3 reaching `CopyClosure` failure at 2026-08-19 11:24:52 CEST. The retained daemon journal also showed an ordinary-query worker `WireShapeError` panic at 11:24:35, while the daemon remained active. Source: transcript line 515 in `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T10-59-15-01a0193f-059c-7393-9d4d-4bb50ef1bc98.jsonl`.
- Read-only audit session `01a01959-df1e-7221-893c-f792588cc5c4` found the shell and user manager had `SSH_AUTH_SOCK=/run/user/1001/gnupg/S.gpg-agent.ssh`, owned by `li:users`, while `/proc/1369/environ` for `lojix-daemon.service` had no `SSH_AUTH_SOCK`. Default `~/.ssh/id_*` files were absent; manual SSH depended on the agent. The same audit recorded `PAM: Authentication failure for li from 127.0.0.1` at 11:24:52 and the matching Lojix `CopyClosure` failure. Source: transcript lines 177–180 in `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T11-28-35-01a01959-df1e-7221-893c-f792588cc5c4.jsonl`.
- The audit read Lojix source showing the child effect inherited the daemon environment and had null stdin (`/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:5920-5935`); `ssh-ng://[username@]hostname` carried no identity in the URI. Host-key negotiation had already reached authentication, so the witness was not a host-key rejection. Same-host activation still issued `CopyClosure` first (`schema_runtime.rs:3499-3506`), so no-copy was not an available explanation.

## Cause classification

- Confirmed observation: the daemon lacked the working session's SSH-agent endpoint, and the target logged PAM authentication failure at the same terminal timestamp as `CopyClosure`.
- Historical primary hypothesis, well supported by those observations: the missing daemon `SSH_AUTH_SOCK` prevented OpenSSH/Nix from using the working agent, while no readable default key existed. The transcript itself calls this the “exact environment boundary,” but this remains a causal inference rather than a separately replayed SSH witness.
- Not supported as the cause: host-key mismatch or basic local reachability. The prior audit saw authentication reached after host-key negotiation; it did not report a transport timeout.

## Repair and verification

- The declarative repair was pushed in CriomOS commit `0cdb1f239d7b9bfa4151b692682647a40819ea32` at 2026-08-19 11:39:01 (commit time). It set the existing `services.lojix.sshAuthSocket` to the selected local user's GPG-agent endpoint, deriving the UID: `"/run/user/${toString config.users.users.${localUser}.uid}/gnupg/S.gpg-agent.ssh"`. The focused ownership check asserted both the derived option and an environment containing only `SSH_AUTH_SOCK`. Source: transcript lines 145–148 in `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T11-37-20-01a01961-e2db-7421-ab24-a0aeb91bc765.jsonl`.
- A follow-up corrected the shape so the module owned a typed socket mode and rendered a runtime wrapper that runs `id -u` after systemd applies `User=`; the persona selected `service-user-gpg-agent`. Commit `e518e91d6433` was reported pushed with `nixfmt` and `nix-instantiate --parse` green. Focused evaluation remained blocked by the intentionally absent materialized system input, so those checks were not a complete runtime proof. Source: session transcript `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T12-28-36-01a01990-d18a-7480-9b77-dffade085b62.jsonl` (assistant result containing `e518e91d6433`).
- Runtime verification after the declarative system switch is preserved in `/home/li/primary/sessions/realization/2026-08-19T105900.md:46-52`: the temporary drop-in was reverted, only Lojix was restarted, and the active daemon had `SSH_AUTH_SOCK=/run/user/1001/gnupg/S.gpg-agent.ssh` supplied by the permanent wrapper. The same historical handoff reports deployment 8 reached terminal state at 12:46:51, which is a later successful Lojix deployment but not an isolated SSH-only regression test.

## Unknowns and applicability

- The prior transcript did not perform a fresh direct `ssh` or `nix copy` after repair; it explicitly retained that post-repair authentication as untested. The successful later deployment and live daemon environment are indirect verification of the durable path.
- No evidence here proves why every current SSH destination, including localhost, fails. Current symptoms could instead be client config, agent/socket availability, network/listener, host authorization, or another shared layer. The present incident must be independently probed before reusing the old fix.

## Sources

- `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T10-59-15-01a0193f-059c-7393-9d4d-4bb50ef1bc98.jsonl`, line 515.
- `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T11-28-35-01a01959-df1e-7221-893c-f792588cc5c4.jsonl`, lines 177–180.
- `/home/li/.codex/sessions/2026/08/19/rollout-2026-08-19T11-37-20-01a01961-e2db-7421-ab24-a0aeb91bc765.jsonl`, lines 145–148.
- `/home/li/primary/sessions/realization/2026-08-19T105900.md`, lines 46–52.
- Prior flow/session IDs: `01a0193f`, `01a01959`, `01a01961`, `01a01990`; current parent flow `01a02fe5`.
