# Core checkup audit (item 49, Codex cf7879) — 2026-09-15 22:20 CST

Written by a Fable audit subflow of flow 840e42; placed here verbatim by the main flow because the subflow ran read-only.

## Verdict

1. Safe to leave running tonight: yes, with one caveat. Every repair path is triple-locked off (`allowRepair:false`, roster `allowRestart:false`, all four units `allowRestart:false`); wake is `enabled:false` and has no send route at all; the only writes are its own NDJSON/state files under `~/.config/core-checkup`.
2. It is not the ordered "codex job with a checklist": it is a deterministic node script (`tools/core-checkup.mjs`) whose only model call is one ephemeral `codex exec --model gpt-5.6-luna --sandbox read-only` judging a thin JSON summary — 48 calls/day at config effort `medium`.
3. It was activated by hand-written unit files (mode 600, 21:51, `~/.config/systemd/user/`) while the branch's own doc says "this change does not claim persistent activation"; the installed unit differs from the source-controlled one (store-path source, store-path roster, `StateDirectory`).
4. Must change before trusting it beyond tonight: (a) a SIGKILL at `TimeoutStartSec=120` or `MemoryMax=256M` (run one peaked at exactly 256M) leaves `state.json.lock` behind and every later run fails closed with `state/locked` — a stale-lock sweep or lock-with-PID is needed; (b) the Luna child runs in `/home/li` under a read-only sandbox that can still read `~/.codex`, `~/.claude` credentials and transcripts.
5. Tests: nine node tests exist and are behavioral, but `core-checkup.test.mjs` is wired into no Nix check (`grep core-checkup flake.nix` = 0); the CriomOS `checks/core-checkup-roster` is an evaluation check with two source-regex asserts.

## 1. Units and journal (witnessed)

`core-checkup.timer`: `OnBootSec=5m`, `OnUnitActiveSec=30min`, `Persistent=true`; next fire 22:21:54. `core-checkup.service`: `Type=oneshot`, `StateDirectory=core-checkup`, `TimeoutStartSec=120s`, `MemoryMax=256M`, `NoNewPrivileges`, `Environment=PATH=~/.nix-profile/bin:/run/current-system/sw/bin`. No `ProtectHome`, `ProtectSystem`, `PrivateTmp`, `ReadOnlyPaths`; `WorkingDirectory=!/home/li`. `RuntimeMaxSec` is ignored for oneshot (journal warns). ExecStart: `node /nix/store/63iv…-source/tools/core-checkup.mjs /nix/store/8xgi…-core-checkup-roster.json ~/.config/core-checkup/policy.json %S/core-checkup/events.ndjson %S/core-checkup/state.json`. The store source is byte-identical to primary branch `proposal/cf7879-overnight-queue-20260916` (219b4b9fb, 22:11 local), not to `origin/core-checkup-cf7879`. Journal: three runs at 21:51:14 (manual, after a daemon-reload at 21:51:13), 21:51:29 (timer enable), 21:51:54 (manual); all exit 0; 14–17s wall; memory peaks 256M, 180M, 167M.

## 2. Source

Primary: `tools/core-checkup.mjs`, `harness-facts.mjs`, `claude-flow-idleness.mjs`, `flow-idleness.mjs`, `codex-app-server-client.mjs`, `core-checkup-witness.mjs`, `docs/core-checkup.md`, `systemd/user/core-checkup.{service,timer}` (source unit uses `%h/primary/tools/…` and `/etc/core-checkup/roster.json`; installed unit does not). CriomOS `origin/core-checkup-criomos-cf7879` (2 commits): module + roster + check; `origin/proposal/cf7879-core-checkup-criomos` (6 commits, tip 8276eab): adds `artifacts/core-checkup-roster.nix`, a horizon-rs pinned input replacing `stubs/no-horizon`, `node-services.nix` case-insensitive lookup, plus unrelated `preinstalled` disk and `metal` changes in the same branch. Neither branch installs a user unit or timer. `/home/li/wt/primary-cf7879` has no core-checkup files and no `flows/cf7879`; the lane exists only on `origin/flow/cf7879` (`reports/to-840e42.md`).

## 3. Safety

Writes: `events.ndjson` (append, no rotation, ~2.9KB/run ≈ 140KB/day), `state.json` (atomic rename), `state.json.lock`, a `/tmp/core-checkup-luna-*` dir removed in `finally`. Restart: gated on `allowRepair===true && unit.owned===true && unit.allowRestart===true && is-failed && !prior`, once per run; all currently false, so `systemctl restart` cannot be reached. Deletes: none. Sends: none — `wake.send` is a function slot that JSON policy cannot populate, so even `enabled:true` would only log `wake/undelivered`; no message-daemon, orchestrate, or intercom call exists. Reads: `ip route/addr`, `ping -6 -c1 -W3` ×4, `systemctl is-active/is-failed` ×4, `claude agents --json`, the two Claude transcript files named in policy, app-server socket (`initialize`, `thread/read`, `thread/turns/list`, `account/rateLimits/read`, `account/usage/read`). Loops: none; bounds are 15s per socket op, 15s `claude agents`, 90s Luna, 120s unit — worst case exceeds 120s (see verdict 4). Secrets: no env passed; codex reads its own auth; Luna's prompt forbids commands but the sandbox does not.

## 4. Tests

`core-checkup.test.mjs` (9), `harness-facts.test.mjs` (3): injected `run`/adapters, assert behavior; two `assert.match` on the emitted NDJSON are generated-output asserts (allowed). Not in any Nix check; the primary flake checks list prompt-relay, component-evidence, third-seat, fan-out only. CriomOS check asserts `builtins.match ".*200:db8::1.*200:db8::2.*"` and `text == readFile artifact` — the latter compares the module's output to the artifact built from the same projection (self-confirming). I did not run either.

## 5. Observations vs my witness

Run logs: ouranos local-ygg, prometheus/zeus active, tiger failed (my `ping -6` to tiger: 100% loss — agrees); four units active (my `is-active orchestrate-nexus message-daemon`: active, active — agrees); primary-840e42 `approval-wait` (my `claude agents --json`: `status: waiting, waitingFor: permission prompt` — agrees); secondary-57a7aa `unknown` because two roster rows carry that sessionId (background blocked + interactive busy) — code-correct, but the secondary is in fact busy; e43002 `unknown`, cf7879 `busy` (not witnessed); quota account.primary 52% used; claude quota always `unknown`. Luna returned `attention` three times on identical summaries with findings differing between runs 1/3 (`permission_wait` present) and 2 (absent) — nondeterministic, adding nothing the deterministic rows do not already say.

Sources: unit files and journal (witnessed), store paths (read), git branches (read), `claude agents --json`, `systemctl`, `ping` (witnessed). Inferences marked as mine: stale-lock and credential-read risks, cost estimate.
