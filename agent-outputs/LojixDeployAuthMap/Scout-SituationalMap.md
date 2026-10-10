# Scout Situational Map — Lojix Deploy/Authentication Architecture

Read-only reconnaissance of how `lojix` (CriomOS deploy orchestrator) runs and
authenticates on `ouranos`, the true cause of the failed HOME activate, why
other deploys succeed, and the current-vs-intended auth architecture. No state
was changed. Observations are cited; interpretations are labeled `INTERP`.

## Scope And Method

Consulted: `systemctl show`/`status` for `lojix-daemon.service`; `journalctl -u
lojix-daemon.service`; `/proc/3488/environ`; `lojix "(Query (ByNode ...))"`;
`~/.local/state/nix/profiles/`; the failing home-manager `activate` script in
the store; lojix source at `/git/github.com/LiGoldragon/lojix/src/`; beads
(`bd`); recent OS-deploy handoffs under `agent-outputs/`. I did **not** run any
`ssh`, deploy, activate, or restart, and did not probe keys.

## Headline: The Two Framing Assumptions In The Brief Are Both Wrong

- "lojix now runs as root and SSHes as `root@ouranos`" — **partly wrong.** The
  daemon runs as **user `li` (uid 1001)**, not root. It only SSHes as
  `root@<node>` for *remote/system* effects; the failed HOME activate ran a
  **local** activate script with no SSH at all.
- "the daemon uses ROOT's keys/agent, not li's gpg-agent" — **wrong.** The live
  daemon environment has `SSH_AUTH_SOCK=/run/user/1001/gnupg/S.gpg-agent.ssh` —
  that is **li's gpg-agent**. So the earlier "red herring" reclassification is
  itself mistaken.
- The `session-bind@openssh.com` hypothesis is a **red herring for both observed
  failures** — but for a different reason than assumed (see Q1/Q2).

## Q1 — How Lojix Actually Runs And Authenticates

### Observations
- Binary: `/home/li/.nix-profile/bin/lojix` and `meta-lojix` both resolve to
  `/nix/store/2a719h33...-lojix-0.3.10/bin/…`. Version **0.3.10**.
- It is a **systemd SYSTEM service** dropped to user `li`, not a `--user`
  daemon and not root:
  - `FragmentPath=/etc/systemd/system/lojix-daemon.service`
  - `User=li`, `Group=users`, `WorkingDirectory=/var/lib/lojix`
  - `ExecStart=…/lojix-daemon /run/lojix/startup.rkyv`
  - Cgroup `/system.slice/lojix-daemon.service`, Main PID 3488.
- Live process confirms: `ps` shows PID 3488 owned by `li`;
  `/proc/3488/status` → `Uid: 1001 1001 1001 1001`.
- Live daemon environment (`/proc/3488/environ`): `USER=li`, `HOME=/home/li`,
  `SSH_AUTH_SOCK=/run/user/1001/gnupg/S.gpg-agent.ssh`. **No `XDG_RUNTIME_DIR`,
  no `DBUS_SESSION_BUS_ADDRESS`** in the daemon env.
- Daemon config (`/nix/store/p827…-lojix-daemon-configuration.nota`): node
  `ouranos`; cluster spec `(goldragon prometheus Hermetic
  github:LiGoldragon/CriomOS-test-cluster /var/lib/lojix/cluster.nota)`; sockets
  `/run/lojix/ordinary.sock` (mode 432) and `/run/lojix/owner.sock` (mode 384).
- Code path per deploy shape (`src/schema_runtime.rs`):
  - HOME activate → `run_activate` (4355) → `is_local_context()` (4364): if the
    dispatcher is already the target `USER` on the target node, it runs
    `local_activate_invocation()` = `"{store_path}/activate"` **locally, no ssh**
    (4314-4316). Otherwise `remote_activate_invocation` SSHes (4326-4329).
  - SYSTEM `FullOs Switch` → `runs_detached_self_switch()` (4152) →
    `run_self_switch` (4247) → `ssh root@<node> systemd-run --unit=lojix-self-switch-deploy-<id> …`.
  - Closure copy / remote profile / remote activate all target
    `SshTarget::root_at_node(...)` i.e. **`ssh root@<node>`** (3948, 3990, 1342),
    with `--substitute-on-destination` so the target pulls **signed** paths from
    the cluster cache (comment 3924-3929: "unsigned daemon-to-daemon transfer is
    rejected under require-sigs").

### Interpretation (INTERP)
- For the psyche's HOME activate (`goldragon ouranos li … Activate`): the daemon
  *is* li on ouranos, so `is_local_context()` is true → the activate runs
  **locally as li in the daemon's minimal (non-login) environment**. No SSH, no
  agent, no `session-bind` on this path. That gpg-agent journal line was
  coincidental.
- For SYSTEM/remote effects the daemon authenticates by **SSH as `root@<node>`
  using li's gpg-agent key**. This SSH path demonstrably works (see Q3, gen 33).

## Q2 — True Root Cause Of The Failed HOME Activate

### Observations
- Failure (journal, `-o cat`, Jul 03 10:34:06):
  `lojix deploy pipeline effect failed at Activate:
  /nix/store/gic8cd5h6avhyrcbwmzikl2iz2m0v253-home-manager-generation/activate
  exited with exit status: 1:` then `DeployRejected(… BuilderUnreachable …)`.
  The captured stderr after the final `:` is **empty**.
- The `BuilderUnreachable` label is a **generic catch-all**, not a diagnosis.
  `src/schema_runtime.rs:2603-2619` (`fail_pipeline`) maps **both**
  `EffectStage::CopyClosure` **and** `EffectStage::Activate` failures to
  `DeployRejectionReason::BuilderUnreachable`. Lines 2610-2611:
  ```
  nexus::EffectStage::CopyClosure => meta::DeployRejectionReason::BuilderUnreachable,
  nexus::EffectStage::Activate    => meta::DeployRejectionReason::BuilderUnreachable,
  ```
  `NixCommand::run` (4670-4687) builds the detail string as
  `"{program} {args} exited with {status}: {stderr.trim()}"`.
- The failing generation link **was created**:
  `~/.local/state/nix/profiles/home-manager-836-link` (mtime 2026-07-03 10:34)
  → `gic8…-home-manager-generation`. In the activate script (read from the
  store), `nix-env --profile … --set "$newGenPath"` is line 272, *after*
  `checkNewGenCollision || exit 1` (265). So the activate **passed collision
  check and the profile-set**, then failed at a **later** activation step.
- Live user runtime for li exists and is reachable: `/run/user/1001` present
  with a full systemd user manager; `loginctl` shows li session 4 = `manager`;
  `XDG_RUNTIME_DIR=/run/user/1001 systemctl --user is-system-running` → **`degraded`**.
- In the activate script (`reloadSystemd`, lines 551-588): it defaults
  `XDG_RUNTIME_DIR` to `/run/user/$(id -u)` (= `/run/user/1001`); on a
  `running|degraded` status it enters the reconcile branch and runs `sd-switch`
  (579) **without** `|| true`, i.e. under `set -euo pipefail`.
- The live home generation never advanced: `home-manager` symlink → `835-link`
  → `28qcd…` (gen id 37, mtime Jul 02 16:42); `836-link` exists but is **not**
  current; **no** `837-link` exists. `lojix` query confirms current home path =
  `28qcd541…` (deployment id 37).

### Interpretation (INTERP)
- The real failure is **the home-manager `activate` script exiting 1 when run
  locally by the system daemon**, mislabeled `BuilderUnreachable`. It is **not** a
  builder-reachability problem, **not** an SSH/auth problem, and **not**
  `session-bind`.
- Because `836-link` was created, the failure is at a **post-`nix-env --set`
  step**: candidate steps, ranked — (1) `sd-switch` reconcile against li's
  **`degraded`** live user systemd (551-582, runs under `set -e`); (2) an
  `onChange`/editor-extension hook (e.g. `codium --list-extensions` at 545, the
  claude-code extension relink at 593+); (3) `dconf load` via `dbus-run-session`
  (450). The **empty captured stderr** weakly argues against a collision-style
  failure (those print to stderr) and toward a step whose non-zero exit produced
  no stderr that lojix captured.
- Architectural root cause (INTERP): the system daemon runs **user activation in
  an impoverished non-login environment** (no `XDG_RUNTIME_DIR`/`DBUS` of its
  own) and leans on li's *interactive* login-session runtime, which is currently
  `degraded`. The activation is thus coupled to fragile external session state.
- **The exact failing line is an UNKNOWN** — it cannot be pinned read-only
  because the journal captured empty stderr and re-running the activate mutates
  state. Getting it is an implementer step (below).

## Q3 — Why Other Deploys "Succeed" (Contradiction Reconciled)

### Observations
- The **same daemon (PID 3488)** logs many `Deployed(AcceptedDeploy …)` lines
  interleaved with the failures — so deploys are flowing through one daemon, not
  a separate path.
- Failure taxonomy in the journal:
  - HOME **Activate** gen 39 (Jul 03 10:34): local activate exit 1 → rejected.
  - SYSTEM **Switch** gen 38 (Jul 02 16:55): `ssh -o BatchMode=yes
    root@ouranos.goldragon.criome systemd-run --unit=lojix-self-switch-deploy-38
    --wait …` ran remotely (so **SSH auth succeeded**) but the inner
    `nix-env --set` + `switch-to-configuration switch` + `bootctl` script
    **`code=exited, status=4/NOPERMISSION`** → rejected (also mislabeled
    `BuilderUnreachable`).
  - Earlier: `MaterializeHorizon` failures → `ProposalSourceUnreachable`;
    a `MaterializeHorizon: No such file or directory` case.
- Successes on the same daemon:
  - SYSTEM **BootOnce** gen 33 recorded `Current` (query shows `33 … FullOs
    BootOnce Current`); handoff
    `agent-outputs/BootOnceColemakDeploy/OperatingSystemImplementer-Evidence.md`
    ran `meta-lojix "(Deploy (System (goldragon ouranos FullOs … BootOnce None []
    None)))"` → `(Deployed (33 (541 541)))`. **BootOnce uses the same
    `ssh root@ouranos` path** and succeeded — proving remote root SSH auth works.
  - Many HOME deploys `Deployed` before Jul 02 16:42, advancing generations up
    to `835`/id 37.
- **Since Jul 02 16:42 (gen 835), no home generation has become live.** Every
  `Deployed` line after that (gen 38 ×4 on Jul 03, gen 39 at 14:03) did **not**
  create a new current home generation link. Between 10:34 and now the only
  `Activate`-stage event in the journal is the single failure.

### Interpretation (INTERP) — the contradiction largely dissolves
- What is broken through the daemon **right now**: HOME **Activate** (local
  activate exit 1) and SYSTEM **Switch** (remote inner script exit 4). What still
  **works**: HOME **Build**, SYSTEM **BootOnce**, and closure copies.
- So "other agents deploying successfully" is best explained as **they are doing
  Build-mode / BootOnce / non-Switch deploys, or reporting daemon *admission* or
  *build* as success — not live home activation.** The frozen home pointer (gen
  835 since Jul 02 16:42) is strong evidence that **nobody is successfully live
  home-activating through the daemon** — including the "successful" sessions.
- Same-identifier pattern (gen 39 `Deployed` at 10:32, `Rejected` at 10:34,
  `Deployed` at 14:03) is consistent with **Build succeeding while Activate
  fails** on the same target.

### Unknown (named precisely)
- I could **not confirm** whether any other agent is live-home-activating via a
  **direct user-path workaround** (running `home-manager`/`activate` themselves
  as li in a full login shell, bypassing the daemon). Evidence searched and
  found empty: `~/.zsh_history` / `~/.bash_history` had no `meta-lojix`/deploy
  lines; no `agent-outputs/` file references `session-bind`/`gpg-agent`/
  `root@ouranos`/`BuilderUnreachable`. A direct login-shell activation *would*
  succeed (full `XDG_RUNTIME_DIR`/`DBUS`, consistent session), so it is a
  plausible unobserved workaround — but I have **no positive evidence** of it.
  To confirm, inspect the other live sessions' transcripts/handoffs (there are
  several concurrent `claude`/`codex` orchestrators in `ps`).

## Q4 — Current Vs Intended Architecture

### Observations
- **Current working remote path** = `ssh root@<node>` (`SshTarget::root_at_node`,
  3948/3990/1342) + signed cluster cache via `--substitute-on-destination`
  (comment 3924-3929). This is the live daemon-to-node mechanism; it relies on
  li's gpg-agent SSH key having root access to the node.
- **Intended daemon-to-daemon Criome-authenticated path is NOT built** — it is
  open tracker work:
  - `primary-om4g` [EPIC] "criome auth core: production gate, quorum plane, key
    custody, and the proven propagation loop" — **4/17 children complete (23%)**.
    Open children include: `.15` "Finish the direct criome peer lane: daemon
    serve-loop + nonce-bound tally + two-node test" (P1), `.6` cluster-root
    `AdmitRegistration` minting ceremony (P1), `.5` BLS12-381 aggregate verify
    (P2), `.9` encrypted multi-key KeyStore replacing the bare MasterKey (P1),
    `.3` idempotent `SubmitAuthorizationApproval` (P1), `.11` wire the gate to
    `LoopProvenGreen` (P1).
  - `primary-om4g` description states the gate is "compiled-out scaffolding," the
    approval path is "placeholder/non-idempotent," and the key is a "bare
    MasterKey" — i.e. confirmed code gaps on `main`.
  - `primary-1e6b` [EPIC] "Persistent two-VM Spirit A→B mirror over the
    criome-authenticated path (prometheus)" and its `.3` "Criome A→B trust seed"
    are open — the two-daemon authenticated transfer is future work.

### Interpretation (INTERP)
- The "future: a lojix daemon authenticating to another lojix daemon via Criome
  authentication that is not yet built" is **confirmed**: the current path is
  SSH-as-root + signed cache; the Criome mutual-auth/quorum plane is a partially
  scaffolded epic, not the live path.
- **Important distinction the brief conflates:** the Criome daemon-to-daemon auth
  story is about **remote** deploys (node A → node B). The **failing HOME
  activate is a *local same-node* activation** — Criome auth would **not** fix
  it. The home-activate failure is an **activation-environment bug**, orthogonal
  to the auth roadmap.

## Q5 — Fix Options (Hack Vs Intended Direction)

### (a) Hotfix / duct-tape — make local user activation work in the daemon
Framing note: the premise's "run lojix as a *user* daemon that shells SSH using
li's root key" is partly moot — the daemon **already** runs as li with li's
gpg-agent (which already has root@ouranos SSH access, proven by BootOnce). The
real local-activate hotfix is to **give the daemon a consistent user session
environment** for the local activate, e.g. one of:
- inject `XDG_RUNTIME_DIR=/run/user/1001` and a valid
  `DBUS_SESSION_BUS_ADDRESS` into the activate child (or run it via
  `systemd-run --user`/a login shell), and/or repair li's **`degraded`** user
  systemd so `sd-switch` reconcile succeeds; and
- first, pin the actual failing step (see Follow-ups) so the fix targets it.
- **Why it is duct-tape (INTERP):** it couples a system-level daemon to li's
  interactive login-session runtime and to li's gpg-agent root key as the deploy
  authority. Risks: broad, unauthenticated **root access to the node** driven by
  an agent-run daemon (no mutual auth, no per-deploy signing/quorum); brittle
  dependence on a live login session; and it does not address reboot-persistence
  (a live home activation still needs a matching system generation). It is
  exactly the posture the Criome epic exists to replace.

### (b) Proper / intended direction — Criome daemon-to-daemon authentication
- Build out `primary-om4g` (arm the production gate, idempotent approvals,
  encrypted KeyStore, BLS aggregate verify, cluster-root admission minting, the
  direct criome peer lane serve-loop + nonce-bound tally + two-node test) so
  **remote** deploys authenticate daemon-to-daemon instead of via a shared root
  SSH key, then `primary-1e6b` for the proven two-node path.
- **Caveat (INTERP):** this fixes the *remote/system* auth posture. It does
  **not** by itself fix the local HOME-activate exit-1, which needs the
  activation-environment fix in (a). Treat them as two separate work items.

## What Was NOT Checked / Unknowns
- Exact failing line of the home activate (empty captured stderr; re-run
  mutates) — **UNKNOWN**; needs a manual capture (below).
- Exact failing command inside the SYSTEM Switch inner script (status
  4/NOPERMISSION) — not pinned from the journal.
- Whether any concurrent session is home-activating via a direct-user workaround
  — searched (history, agent-outputs) and found **no positive evidence**; other
  sessions' transcripts not inspected.
- I did not run `ssh root@ouranos` or any deploy/activate to avoid state/auth
  side effects; remote-root-SSH success is inferred from gen-33 BootOnce and the
  gen-38 systemd-run actually executing remotely.

## Suggested Follow-ups (for an implementer, not done here)
1. Reproduce the home activate manually as li with full output capture, e.g.
   run `/nix/store/gic8…-home-manager-generation/activate` (or the current
   generation's) under a login shell with stdout+stderr teed, to pin the failing
   step. (Mutating — needs authorization; do it in a controlled window.)
2. Check li's `degraded` user systemd (`systemctl --user --state=failed`) — a
   failed user unit is the leading suspect for `sd-switch` aborting activation.
3. Consider fixing the mislabel in `src/schema_runtime.rs:2610-2611` so an
   Activate-stage failure surfaces the real detail rather than
   `BuilderUnreachable` (it hid this root cause for both failures).

## Key Source/Evidence Pointers
- `/etc/systemd/system/lojix-daemon.service` (User=li system unit)
- `/proc/3488/environ` (li's gpg-agent socket; no XDG_RUNTIME_DIR/DBUS)
- `journalctl -u lojix-daemon.service` (both failures, verbatim)
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`: 2603-2619
  (rejection mapping), 4314-4367 (local/remote activate + is_local_context),
  4152-4249 (system self-switch), 3924-3953 (closure copy / root_at_node),
  4670-4687 (error string)
- `/nix/store/gic8…-home-manager-generation/activate`: 265 (collision), 272
  (nix-env --set), 450 (dconf), 551-588 (reloadSystemd/sd-switch)
- `~/.local/state/nix/profiles/home-manager*` (frozen at 835; 836 not current)
- beads `primary-om4g`, `primary-1e6b` (Criome auth = open future work)
- `agent-outputs/BootOnceColemakDeploy/OperatingSystemImplementer-Evidence.md`
