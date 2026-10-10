# Spirit Guardian Secret Access — Implementation Evidence

## Task and scope
Fix the running Spirit daemon's inability to resolve its guardian secret (the
DeepSeek API key at gopass path `platform.deepseek.com/api-key`), which was
failing every guardian-gated Spirit WRITE with `DaemonUnconfigured`. Then run
the prepared qjrf retirement and close bead `primary-tu9i`.

Host: ouranos (user li, uid 1001). Live-host systemd --user work.

## Root cause (observed, proven)
- The daemon is supervised by **systemd --user** (PPID chain: spirit-daemon ->
  `systemd --user` (uid 1001) -> system systemd). Unit: `spirit-daemon.service`,
  loaded via home-manager symlink into the nix store.
- The store-managed unit sets **no `Environment=`**, so the daemon inherited only
  systemd's minimal default `PATH` (`/nix/store/...systemd-260.1/bin/` only). That
  PATH lacks `/home/li/.nix-profile/bin`, where `gopass` and `gpg` live.
- The guardian shells out to `gopass` to fetch its model API key. With `gopass`
  not on PATH the spawn fails with ENOENT — the reported
  `secret unavailable: ... No such file or directory (os error 2)` — so the
  guardian returns `DaemonUnconfigured` and all writes are rejected. Reads never
  hit the guardian, so they worked throughout.
- **Key discovery:** the guardian model call actually runs in a *separate*
  process, **`agent-daemon.service`** (spirit-daemon declares
  `Wants=/After=agent-daemon.service` and delegates the guardian call to it).
  agent-daemon had the *same* crippled PATH. Fixing only spirit-daemon left the
  write still failing with the identical error; agent-daemon is the operative
  process that fetches the secret.
- Reproduction (value never printed): with the daemon's PATH,
  `gopass show platform.deepseek.com/api-key` fails; with a PATH that includes
  `/home/li/.nix-profile/bin` it returns exit 0.

## Durable fix applied (in scope: supervised restart with corrected environment)
Added systemd drop-ins (no secret value stored — the daemon fetches the secret
itself at runtime):
- `/home/li/.config/systemd/user/spirit-daemon.service.d/10-guardian-secret-path.conf`
- `/home/li/.config/systemd/user/agent-daemon.service.d/10-guardian-secret-path.conf`

Each contains:
`[Service]` / `Environment=PATH=/home/li/.nix-profile/bin:/run/current-system/sw/bin:/run/wrappers/bin`

Then `systemctl --user daemon-reload` and `systemctl --user restart` of both
services. The drop-in directories are plain writable dirs (spirit's already
held a hand-added `.disabled` file; agent's dir I created), NOT store symlinks,
so this required no nix rebuild / redeploy / host-module edit. systemd re-reads
drop-ins on every start, so the fix persists across restarts and reboots.

## Health / restart evidence
- `spirit-daemon`: active, MainPID 109842, ExecMainStatus=0, PATH now includes
  `/home/li/.nix-profile/bin`.
- `agent-daemon`: active, MainPID 112451, ExecMainStatus=0, PATH corrected.
- `systemctl --user show ... -p DropInPaths` lists both `.conf` drop-ins.
- Reads healthy throughout (`spirit "(Lookup qjrf)"` returns the record).
- **Proof the guardian can now authorize mutations:** the retirement WRITE no
  longer returns `secret unavailable`/`DaemonUnconfigured`. The guardian executed
  the DeepSeek model call and returned a *reasoned* verdict — impossible without
  the API key it now resolves from gopass.

## qjrf retirement — NOT completed (blocked on a new, legitimate guardian gap)
Running `spirit /.../scratchpad/retire-qjrf.nota` now returns:
`GuardianRejected(InsufficientWarrant)` — "no verbatim psyche quote authorizes
retiring qjrf; the provided poetic phrases describe intent's quality, not a
directive to remove a record."

The prepared NOTA's testimony vector was five poetic phrases sourced from the
Castaneda corpus in `scratchpad/cast/`, not a verbatim psyche directive to
retire. Investigation of durable surfaces (bead `primary-cxzb` closed as
"psyche-approved", bead `primary-tu9i`, the June-26 legacy-disposition
handovers, the intent-log skill, Spirit text search) found only **agent-authored
summaries** asserting the retirement was psyche-approved — no verbatim psyche
quote authorizing it.

The psyche's own recorded rules forbid manufacturing that warrant: qjrf itself
("inferring to close the loop produces fake hallucinated records"), record
`gni3` ("agent-authored content is not psyche-authorized"), and the decision
surface ("only psyche statements become Spirit records; agent-written reports
and files are not intent sources"). Laundering a bead's "psyche-approved"
assertion into fabricated testimony to pass the guardian would be exactly the
violation those records — and the guardian — exist to prevent, using the retired
record's own removal as the vehicle. I therefore did not fabricate testimony.

`spirit "(Lookup qjrf)"` still shows qjrf ACTIVE (not retired).

## Bead
`primary-tu9i` kept **OPEN** (retirement did not succeed). Appended full
evidence note; added label `guardian-warrant`. The daemon blocker named in the
bead title is resolved and proven; the retirement now needs the psyche's
verbatim authorizing directive.

## Blockers / follow-up for the psyche
1. Retirement of qjrf needs a **verbatim psyche directive** to retire the record
   / relocate the intent definition. With that quote in the testimony, the
   retirement will pass (daemon is healthy). This is a psyche decision, not an
   agent one.
2. Recommended (scope-guarded, NOT done unilaterally): make the PATH fix fully
   declarative in the criomos-home module that generates these user units (add
   `Environment`/`path` to `systemd.user.services.{spirit,agent}-daemon`), so a
   future full home redeploy carries it. That is a home-module edit + redeploy —
   heavier than a supervised restart — so it is left as a recommendation.

## Secret hygiene
The token value was never printed, logged, or written to any file, bead,
report, commit, or message. All gopass reads used exit-status-only checks. The
fix makes the daemon resolve the secret itself at runtime (PATH correction); no
token was injected into any unit or file.
