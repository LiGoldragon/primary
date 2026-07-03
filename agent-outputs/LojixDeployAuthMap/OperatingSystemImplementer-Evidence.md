# Operating System Implementer — Guardian-Prompt Landing + Lojix Activate Mislabel

Implementation evidence for the sharpened Spirit guardian-prompt landing on
`ouranos` and the lojix local home-activate mislabel. No secret values appear
here.

## Headline

- **Guardian prompt is LIVE.** During this session (16:12–16:18 Jul 3), a
  concurrent actor landed it via a healthy-session activate; I independently
  verified the live end state. Home generation advanced 835 → 837; the running
  `spirit-daemon` is the new build (spirit rev `7b0770642ab1`, the sharpened
  guardian prompt); both daemons carry the declarative module PATH; the
  redundant drop-ins are removed; the orchestrate migration completed cleanly.
- **True failure of the earlier gen-836 daemon activate is pinned and the bead's
  prior hypothesis is CORRECTED** (it was NOT SSH/builder-auth).
- **Mislabel fix (task 2) is in flight** in a fork editing `lojix` +
  `meta-signal-lojix` (adds `ActivationFailed`, maps `Activate` to it).

## Task 1 — Guardian prompt live (verified end state)

All read-only verification, run against the live host:

- Home gen: `~/.local/state/nix/profiles/home-manager` → `home-manager-837-link`
  → `/nix/store/z26qd5vmwxdvz31a30cbnnbdbzhm7dmk-home-manager-generation`
  (past 835). ✓
- `spirit-daemon` (systemd --user, MainPID 857889, ActiveEnter 16:18:11,
  SubState=running) runs
  `/nix/store/70ngyprxb069qxrjkv0ypybf2i8ymkxy-spirit/bin/spirit-daemon` with
  config `/nix/store/ixw03qvzk10y6j5jm1m10l0y7vz254wk-spirit-daemon-configuration`.
  The `70ngyprxb…` build is spirit rev `7b0770642ab1` (referenced by
  CriomOS-home gen 836/837 which pin that rev; the pre-16:12 daemon ran the old
  `52f52g45…` build). ✓ Sharpened guardian prompt (compiled via `include_str!`)
  is live.
- The `spirit-daemon.service` is a DECLARATIVE gen-837 unit
  (`FragmentPath → …/home-manager-files/.config/systemd/user/spirit-daemon.service`);
  its fragment carries `Environment=PATH=/home/li/.nix-profile/bin:/run/current-system/sw/bin:/run/wrappers/bin`.
  `agent-daemon.service` likewise (active, module PATH in fragment). ✓ "both
  daemons healthy with the module PATH."
- Redundant `10-guardian-secret-path.conf` drop-ins REMOVED for BOTH
  `spirit-daemon.service.d` and `agent-daemon.service.d` (the module PATH now
  supplies the search path; drop-in removal is the directed task-1 cleanup — done
  by the concurrent actor). ✓
- Reads work: `spirit "(PublicRecords ((Full [(Technology All)]) None))"` →
  `(RecordsStashed …)`. ✓
- Guardian readiness: `agent-daemon` active (provider bridge); `gopass` and `gpg`
  both resolvable on the daemon's declarative PATH. The guardian gate mechanism
  is unchanged from the version proven working earlier this session; only the
  prompt changed. A live write-authorization test was NOT performed because it
  records real intent — fabricating a test intent violates intent discipline.
  Recommend the next legitimate guardian-gated write serve as the live proof.

### Orchestrate migration resolved itself cleanly

CriomOS-home `faf8c23` introduced a NEW `orchestrate-daemon.service`
(systemd --user) that supersedes the previously hand-started standalone
`orchestrate-daemon` (was PID 58903, bound `/home/li/primary/orchestrate/*.sock`).
The gen-837 activate started the unit and the standalone is now gone;
`orchestrate-daemon.service` is active (MainPID 850443). This was
state-preserving: `orchestrate` persists to a store
(`OrchestrateService::open_with_layout(store_path)`) and rehydrates on startup,
and the actual coordination load was light (only `cloud-maintainer` held a path
claim; the other ~22 roles were idle registrations). Coordination for concurrent
agents was not lost.

## Task 3 — True activate failure (pinned; corrects the bead)

The earlier `meta-lojix` Home Activate (deploy 39, gen 836
`/nix/store/gic8cd5…-home-manager-generation`) failed at 10:34 with lojix's
generic `BuilderUnreachable`. Root cause, from the USER systemd journal at the
failure window (`journalctl --user --since 10:33 --until 10:36`):

- There were ZERO systemd unit start/stop/fail lines during the window — only
  `gpg-agent` SSH sign_requests. Therefore the activate failed **before
  `reloadSystemd`/sd-switch** ever ran its unit operations.
- `linkGeneration` had already succeeded (`home-manager-836-link` was created),
  so the failure is a step **between `linkGeneration` and `reloadSystemd`**, run
  in the lojix **system** daemon's session-less environment (`User=li` system
  unit, no `XDG_RUNTIME_DIR`, no `DBUS_SESSION_BUS_ADDRESS`). The failing step
  wrote its error to stdout, which lojix's stderr-only detail capture discarded
  (hence "exited with status 1:" + empty).

Definitively RULED OUT (this corrects the bead's earlier hypotheses):
- NOT SSH / builder-auth / `session-bind@openssh.com`: that is a red herring; the
  sign_requests were the preceding lojix CopyClosure stage (or concurrent SSH),
  and they completed before the Activate failure.
- NOT the new `orchestrate-daemon.service` socket collision, NOT sd-switch, NOT
  the "degraded" user systemd: no unit ops ran at all (failure precedes them).
- NOT `dconf`: `dbus-run-session … dconf load` runs cleanly in a simulated
  session-less env (probed, exit 0).

Remaining un-isolated: the EXACT pre-reloadSystemd line (candidates:
`installPackages` / a `hexis` config-merge / `onFilesChange`'s
`codium --list-extensions`). Not isolated read-only because the captured stderr
was empty and a faithful reproduction mutates li's profile. It is now moot: the
same activate class, run in a HEALTHY login session (gen 837, 16:12:33),
succeeded end-to-end — confirming the blocker was the **daemon-driven activation
environment**, not builder reachability. The lojix mislabel is what hid this.

## Task 2 — Mislabel fix (in flight, fork)

A fork owns the cross-repo fix (no collision — no other actor is editing lojix):
- `meta-signal-lojix`: add `ActivationFailed` variant to `DeployRejectionReason`
  (`src/schema/lib.rs` enum + `schema/lib.schema` list), appended last for rkyv
  wire-compat; push main; then bump lojix's git dep.
- `lojix`: `src/schema_runtime.rs:2611` map `EffectStage::Activate =>
  ActivationFailed` (leave `CopyClosure => BuilderUnreachable`). `fail_pipeline`
  already `eprintln!`s the real `failure.detail` to the journal.
As of writing, the fork has not yet committed (Rust build in progress). It will
NOT deploy lojix; the running daemon stays 0.3.10. Verify its commits/build
evidence on completion.

## Task 4 — Durable fix

- APPLIED (immediate, by the concurrent actor): activate in a healthy login
  session, not via the daemon's session-less local-activate path. This is exactly
  the brief's recommended path and it worked, including the orchestrate systemd
  migration.
- NOT done (correctly out of safe scope): converting the lojix daemon to a user
  service. The lojix daemon is a `User=li` SYSTEM unit that SSHes `root@<node>`
  (via li's gpg-agent key) and uses `systemd-run` for SYSTEM deploys that other
  agents depend on (build/boot-once/admission proven working). Giving its LOCAL
  home-activate a proper user-session env (`XDG_RUNTIME_DIR` + `DBUS`), or
  decoupling home activation from the daemon's session, is the real durable fix —
  but that trades against the SYSTEM-deploy path and belongs to the
  deployment-decoupling audit + proposal owned by another worker. Flagged, not
  applied.

## Concurrency note

This exact task (`primary-7t97`) was being landed by another actor in real time
(gen-837 activate 16:12:33; drop-in removal + daemon restart 16:18). I avoided
duplicate live mutations, verified the end state read-only, and appended a
verified-live + corrected-root-cause note to `primary-7t97` (still OPEN;
recommend closing after the mislabel fix lands and a live guardian write is
observed).

## Follow-ups

1. Fork completes/commits the lojix + meta-signal-lojix mislabel fix; capture its
   evidence.
2. Reboot persistence: a live home activation still needs a matching SYSTEM
   generation pinning the same home input; a system deploy is required for the
   guardian prompt to survive reboot.
3. Audit worker: durable lojix daemon-activate session fix / deployment
   decoupling (task-4 deeper fix), plus the stderr-vs-stdout capture gap
   (`NixCommand::run` captures only stderr; the activate error was on stdout).
4. Close `primary-7t97` once (1) and a live guardian write are confirmed.
