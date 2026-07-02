# Field Readiness — 13: Tooling Field (jj / nix / spirit / orchestrate / beads / tests)

RECON pass, 2026-07-02, host ouranos. Task: probe every constant-use tool for readiness and
sustained-use failure modes ahead of a long Fable 5 session. Read/round-trip probes only; no
commits, no durable Spirit records, no beads created. Every claim is tagged WITNESSED (command
run, output observed) or INFERRED (reasoned from evidence).

## VERDICT

The tooling field is READY for a sustained session — every daemon answers in milliseconds, the
remote builder and cache are hot, and a real flake check ran end-to-end in under a minute — with
three known jam points to pre-empt: bd's cold-start compaction stall, spirit skill-vs-deployed
shape drift, and primary-main push contention between concurrent agents.

## PER-TOOL STATUS TABLE

| Tool | Working? | Speed | Reliability | Sustained-use failure mode |
|---|---|---|---|---|
| jj (Jujutsu) | YES (WITNESSED) | instant | clean working copy; push to origin succeeded 3 min before this probe (op log) | push-rejected when another agent advances `main` first; stale-workspace errors if entering the 3 leftover workspaces; bookmark litter slows reading |
| nix eval/build | YES (WITNESSED) | warm eval 0.065s (router, 41 checks); forced remote build round-trip 1.1s | daemon healthy (`nix store info` Trusted:1); disk 51% used, 433G free | local capacity is deliberately tiny (max-jobs=1, cores=2): any build that can't reach prometheus becomes a long serial stall |
| remote builder (prometheus) | YES (WITNESSED) | tiny drv built remotely + copied back in 1.1s; real check < ~1 min | single builder in `/etc/nix/machines` (6 slots, big-parallel,kvm) | single point of failure; user-level ssh probe is denied by design (daemon holds the key), so mid-session diagnosis is indirect |
| binary cache | YES (WITNESSED) | `nix-cache-info` answers on `http://nix.prometheus.goldragon.criome` (priority 30) + cache.nixos.org | dry-run of router's heaviest integration check: ~1 drv to build, rest substituted | cache is the same host as the builder — one host outage takes both |
| spirit CLI (read path) | YES (WITNESSED) | 3–5 ms per query | `PublicTextSearch spirit` → record qjrf; `Lookup qjrf` → RecordFound; `PublicRecords` → 26 records; daemon up 2d at `~/.local/state/spirit/spirit.sock` | strict canonical NOTA rejects skill-example shapes (see kinks K2/K3); deployed build may lag today's v11 checkout |
| spirit (write path) | NOT EXERCISED (recon) | n/a | guardian `agent-daemon` running (WITNESSED, pid via pgrep); Record → nexus → feature-gated `AgentGuardian` (source-read) | guardian resolves an LLM provider endpoint + API key per call (`agent/src/provider.rs`) — provider outage or key expiry blocks intent capture |
| orchestrate claim/release | YES (WITNESSED) | 3 ms | Claim + Release round-trip on a scratch path accepted and acknowledged; RoleSnapshot shows 2 live claims by other lanes | none observed; ad-hoc lane names are accepted, so lane-name collision could release someone else's claim if reused carelessly (INFERRED) |
| beads (bd) | YES (WITNESSED) | 18.2s cold (`bd stats`, dolt "conjoin" compaction), 0.8s steady (`bd ready`) | 1002 issues, 153 open, 108 ready; push-state fresh (last_push today 10:54Z) | one-time compaction stall on first touch; embeddeddolt exclusive single-writer lock under concurrent agents (documented in `work-tracking` skill) |
| test harness (flake checks) | YES (WITNESSED) | `router-runtime-cannot-poll` built ON the remote builder end-to-end in < ~1 min; only 1 drv built | 41 named checks eval in router alone; cache coverage near-total | no continuous entry point exists (see K8); heavy integration/VM checks are manual, prometheus-gated |

## Commands and paths consulted (evidence anchors)

- jj: `jj status`, `jj bookmark list`, `jj op log --limit 3`, `jj git remote list`, `jj workspace list` in `/home/li/primary`
- nix: `nix config show`, `cat /etc/nix/machines`, `nix store info`, `df -h /nix /`, `curl http://nix.prometheus.goldragon.criome/nix-cache-info`, forced-remote probe `nix build --option max-jobs 0 --impure --expr 'derivation …'`, `nix eval /git/github.com/LiGoldragon/router#checks.x86_64-linux --apply builtins.attrNames`, dry-runs and one real build of `router#checks.x86_64-linux.router-runtime-cannot-poll`
- spirit: `spirit "(PublicTextSearch …)"`, `spirit "(Lookup qjrf)"`, `spirit "(PublicRecords ((Full [(Technology All)]) None))"`, `spirit "(Count)"` (rejected); wrapper read at `~/.nix-profile/bin/spirit`; source at `/git/github.com/LiGoldragon/spirit/src/bin/spirit.rs`, `src/nexus.rs`; guardian source `/git/github.com/LiGoldragon/agent/src/provider.rs`, `engine.rs`; `ss -xlp` for live sockets
- orchestrate: `orchestrate "(Observe Roles)"`, Claim/Release round-trip on a scratchpad path
- bd: `bd stats`, `bd ready`, `bd --version` (1.0.0 dev), `.beads/` inspection
- host: `systemctl list-timers`, `systemd-tmpfiles --cat-config` (`q /tmp … 10d`, daily clean timer), `pgrep -af spirit|agent-daemon`
- context: `reports/persona-system-audit/00-README.md`, `23-testing-strategy.md`; skills `version-control`, `nix-usage`, `nix-discipline`, `spirit-cli`, `spirit-query`, `work-tracking`, `testing`, `edit-coordination`

## KINK LEDGER

### K1 — bd cold-start compaction stall + single-writer lock
- What: first `bd` command of the day ran 18.2s with dolt `conjoin of database` compaction logs; steady-state is 0.8s. The `work-tracking` skill separately documents the embeddeddolt exclusive lock failing concurrent commands.
- Where: `/home/li/primary/.beads/embeddeddolt`.
- Blast radius: a mid-flow tracker touch stalls the session ~20s, or fails outright when two agents hit the lock; agents may misread the stall as a hang.
- Likelihood: HIGH for the stall (once per cold DB), MEDIUM for lock conflict under multi-agent load.
- Fix: pre-warm with one `bd stats` at session start; keep bd usage sequential per the skill; retry-on-lock.
- Cheap vs bead: CHEAP (pre-warm habit). A bead only if lock conflicts recur.
- Evidence: WITNESSED — `time bd stats` 18.220s total with conjoin log lines; `time bd ready` 0.806s immediately after.

### K2 — spirit skill examples drift from the deployed Input surface
- What: `spirit "(Count)"` → `unknown Input variant Count`, yet the spirit-query doctrine lists `Count` among read-only operations. Single-word bracket text is rejected: `(PublicTextSearch [nota])` → `non-canonical string delimiter … use nota` (multi-word bracket text is accepted).
- Where: spirit-query/spirit-cli skill surfaces vs the deployed CLI/daemon.
- Blast radius: every fresh agent following the skill verbatim burns a retry loop mid-session; worse, an agent may misread validation rejection as daemon failure (the skill itself says to treat that as a blocker).
- Likelihood: HIGH — it bit this recon on the first two attempts.
- Fix: reconcile skill query examples against the deployed Input enum (correct `Count` shape or remove it; state the bare-atom rule for single canonical words in the example line itself).
- Cheap vs bead: BEAD for skill-editor (generated surfaces must be reconciled from LiGoldragon/skills, not patched here).
- Evidence: WITNESSED — both error outputs above, 3ms each.

### K3 — deployed spirit may lag the strict-positional v11 checkout
- What: spirit-daemon has 2d00h uptime running store path `…-spirit/bin/spirit-daemon`; the checkout head at `/git/github.com/LiGoldragon/spirit` is `spirit: adopt strict-positional signal-spirit contract with v10→v11 store migration` dated 2026-07-02 02:04 (bookmark `spirit-strict-positional-v11`). Skills instruct agents to read wire shape from source; source and deployed binary may not be the same version. Corroborating: audit-cited record ids `vcin` lookup → `record not found`, while current-store id `qjrf` resolves; checkout CLI source defaults the socket to `/tmp/spirit.sock` while the deployed wrapper pins `~/.local/state/spirit/spirit.sock`.
- Where: `/git/github.com/LiGoldragon/spirit` checkout vs running daemon; doctrine citing pre-migration record ids (e.g. `CriomOS-test-cluster/INTENT.md` per audit 23).
- Blast radius: an agent trusting source-read wire shapes against a lagging daemon (or vice versa) gets validation rejections mid-flow; doctrine citing dead ids sends agents on false lookups.
- Likelihood: MEDIUM.
- Fix: verify deployed-vs-checkout version before the session leans on source-read wire shapes; redeploy or note the delta; refresh doctrine record-id citations post-migration.
- Cheap vs bead: BEAD (version verification + citation refresh crosses repos).
- Evidence: WITNESSED uptime (`ps -o etime=` → 2-00:13:50), checkout head (`jj log -r @`), wrapper content, `(Lookup vcin)` → record not found. Version lag itself is INFERRED — I did not resolve the deployed store path to a commit.

### K4 — primary `main` push contention between concurrent agents
- What: primary is actively shared — the op log shows another lane pushed `main` 3 minutes before this probe; RoleSnapshot shows 2 live claims by other lanes; 20+ stale `operator/report-*` bookmarks and 3 extra jj workspaces exist.
- Where: `/home/li/primary` (`jj op log`, `jj bookmark list`, `jj workspace list`).
- Blast radius: `jj git push --bookmark main` rejected mid-flow when the remote advanced; the escape hatch (fetch, inspect divergence, ask) halts normal work by design.
- Likelihood: MEDIUM-HIGH during a sustained multi-agent session.
- Fix: commit-and-push promptly in small units; on rejection follow the `version-control` escape hatch instead of force-moving. Bookmark/workspace litter is a separate cheap cleanup.
- Cheap vs bead: CHEAP (discipline already documented); optional small bead for bookmark/workspace cleanup.
- Evidence: WITNESSED op log entries (`push bookmark main … 3 minutes ago`), bookmark and workspace listings.

### K5 — single remote builder = single point of long-stall failure
- What: `/etc/nix/machines` has exactly one builder (`ssh-ng://nix-ssh@prometheus.goldragon.criome`, 6 slots) and the primary substituter is the same host. Local fallback is max-jobs=1 / cores=2. Direct user ssh to the builder is denied (daemon-held key), so a session cannot easily diagnose builder-side pressure (disk, load).
- Where: `/etc/nix/machines`, `nix config show`.
- Blast radius: if prometheus is down or degraded, any uncached build serializes onto a 1-job local slot — a rebuild becomes a multi-hour stall; cache misses double the pain because the priority-30 cache is the same host.
- Likelihood: LOW-MEDIUM (it was fast and healthy at probe time: 1.1s forced-remote round-trip, real check < ~1 min).
- Fix: none cheap in-session; know the symptom (build "hangs" copying/waiting) and prefer dry-run first (`nix build --dry-run` shows the miss surface). A second builder or documented degraded-mode guidance is bead-level.
- Cheap vs bead: BEAD (infra), plus the CHEAP habit of dry-running heavy builds first.
- Evidence: WITNESSED machines file, cache-info fetch, forced remote build, check build log (`building … on 'ssh-ng://nix-ssh@prometheus…'`). Builder-side disk/load NOT CHECKED (no access path).

### K6 — Spirit write path depends on a live LLM provider + API key
- What: intent capture flows through the guardian: `spirit/src/nexus.rs` holds a feature-gated `AgentGuardian` with `guardian_required`; `agent/src/provider.rs` resolves each guardian call to endpoint + model + secret API key. `agent-daemon` is running.
- Where: `/git/github.com/LiGoldragon/agent/src/provider.rs`, `engine.rs`; `spirit/src/nexus.rs`.
- Blast radius: provider outage, key expiry, or NOTA-output failures (engine retries a bounded number of attempts) block Record mid-session; per the spirit-cli skill this is a surfaced blocker, not a file fallback.
- Likelihood: LOW-MEDIUM.
- Fix: none cheap; treat guardian rejection/erroring per skill (fix input or surface blocker). Key-freshness check at session start could be a small bead.
- Cheap vs bead: BEAD (optional pre-session guardian liveness/key probe).
- Evidence: source-read WITNESSED; write path itself NOT EXERCISED (recon boundary — no durable records created).

### K7 — leftover demo daemons squatting /tmp
- What: a tmux session `criome-mentci-spirit-demo-20260701-150210` still runs debug `criome-daemon` (~22h uptime) and `mentci-daemon` against `/tmp/criome-mentci-spirit-demo-…` sockets/config/logs. `/tmp` has a 10-day age rule cleaned daily (`q /tmp 1777 root root 10d`, systemd-tmpfiles-clean daily).
- Where: `pgrep -af`, `ss -xlp`, tmpfiles config.
- Blast radius: stray daemons can collide with future demo runs (socket paths, state confusion); tmpfiles can eventually reap their state under them. Production spirit is NOT exposed — its socket lives in `~/.local/state/spirit/`, not /tmp.
- Likelihood: LOW for jamming the main session; MEDIUM for confusing the next demo run.
- Fix: owner kills the tmux session (`tmux kill-session -t criome-mentci-spirit-demo-20260701-150210`) when the demo is done. Not performed — recon is read-only.
- Cheap vs bead: CHEAP.
- Evidence: WITNESSED process list, socket list, tmpfiles rule.

### K8 — no continuous-testing entry point exists
- What: component repos have no hosted CI (only `kameo` and `whisrs` carry `.github/workflows`); the host has no test timers (`systemctl list-timers`: logrotate, fwupd, tmpfiles, fstrim only). Testing is entirely pull-based: per-repo `nix flake check`, manual cluster apps (`test-criome-auth-witness`, `run-criome-auth-on-prometheus`, `spirit-upgrade-test-runner` in `CriomOS-test-cluster/flake.nix`), and the harness e2e that skips by default (audit 23 §2B).
- Where: repos under `/git/github.com/LiGoldragon/`, host timers.
- Blast radius: regressions accumulate silently between manual check runs; a sustained session discovers breakage only when it trips over it. This is the gap the audit's staged plan (23 §4) addresses.
- Likelihood: certain (it is a structural gap, not a flake).
- Fix: the staged path in `reports/persona-system-audit/23-testing-strategy.md` (Stage 0 harness crate → Stage 1 two-daemon check → …); at minimum a scheduled `nix flake check` sweep over the core repos.
- Cheap vs bead: BEAD (already mapped by audit 23).
- Evidence: WITNESSED absence after scoped search (workflows glob, timers list, cluster flake grep).

## Probe artifacts and cleanup

- Orchestrate claim `recon-tooling-probe` on a scratchpad path: claimed and RELEASED (witnessed acknowledgment).
- Two tiny store paths created: the forced-remote probe derivation output and the `router-runtime-cannot-poll` check result (a normal, beneficial cache entry). Both are unrooted (`--no-link`) and GC-managed; nothing to hand-clean.
- No Spirit records, no beads, no commits, no repo files created besides this report.

## Not checked / unknowns

- Builder-side (prometheus) disk and load: no access path from this user; NOT CHECKED.
- Spirit write path behavior end-to-end (guardian round-trip): NOT EXERCISED by boundary.
- Whether the deployed spirit store path corresponds to the v11 or pre-v11 commit: NOT RESOLVED (K3).
- Green status of the broader check suites (only one check built; the rest eval'd/dry-run only).
- meta-orchestrate worktree inventory surface: present on PATH, not exercised.
- bd remote push target health beyond fresh `push-state.json` (last_push today): the push path itself was not exercised.
