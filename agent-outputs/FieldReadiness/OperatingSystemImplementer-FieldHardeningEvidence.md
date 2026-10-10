# Operating-System Implementer — Field-Hardening Follow-ups Evidence (2026-07-03)

Durable field-hardening follow-ups building on the prior OS worker's VM-field
changes (`CriomOS f8eb6ff7`, `CriomOS-home 3738e2f2`; evidence at
`agent-outputs/FieldReadiness/OperatingSystemImplementer-VmFieldPrepEvidence.md`).
Nothing here reverts that work.

Acting model: Claude Opus 4.8 (1M context), high reasoning. Ran on `ouranos`.

## Dispositions

| Task | State | Live host touched? |
|------|-------|--------------------|
| 1. orchestrate systemd --user supervisor | declarative unit LANDED+PUSHED+VERIFIED (build+eval) | No — live cutover DEFERRED to a watched window (steps below) |
| 2. cheap-fix #8: whole-OS eval recipe doc | LANDED+PUSHED (CriomOS AGENTS.md) | No |
| 3. cheap-fix #12: VM inventory doctrine doc | LANDED+PUSHED (CriomOS AGENTS.md) | No |
| 4. two field-readiness beads (RECORD only) | FILED: `primary-wgae`, `primary-oftl` | n/a |

The running orchestrate daemon (pid 58903) was NOT stopped, restarted, or
disturbed. Confirmed alive + responsive at closeout (46 min elapsed, sockets
present, `orchestrate "(Observe Roles)"` responds).

## Task 1 — orchestrate-daemon systemd --user supervisor

### What landed — CriomOS-home main `faf8c230` (pushed)

Root cause context: `orchestrate-daemon` (multi-agent claim/coordination daemon
for the `primary` workspace) was installed imperatively
(`nix profile install git+file:///git/github.com/LiGoldragon/orchestrate`,
locked non-portably) and started by hand
(`setsid nohup orchestrate-daemon <signal>`) with no supervisor — so its earlier
crash silently took the whole claim fabric down until a manual restart. This is
the same class as the prior worker's "fold local hack" ssh change.

Changed files (commit `faf8c230`):
- **New** `modules/home/profiles/min/orchestrate.nix` — mirrors the spirit.nix
  daemon pattern. Defines `systemd.user.services.orchestrate-daemon`:
  `ExecStart = ${orchestrate}/bin/orchestrate-daemon
  ${config.home.homeDirectory}/primary/orchestrate/orchestrate-daemon.signal`,
  `Restart=on-failure`, `RestartSec=2s`, `StartLimitIntervalSec=60`/`Burst=5`,
  `Install.WantedBy = [ "default.target" ]` (start-on-login). Gated on
  `size.min && criomosHome.orchestrate.enable` (enable defaults true — the
  toggle is a declarative off-switch for the cutover-sensitivity below).
- `flake.nix` — added input `orchestrate.url =
  github:LiGoldragon/orchestrate?rev=8f9b41707ecbffe6206e3109adc495890c045121`
  with `inputs.nixpkgs.follows = "nixpkgs"`. Pinned to the EXACT rev of the
  currently-running v0.4.1 daemon, so the cutover is supervisor-only with zero
  daemon behavior change. Portable `github:` ref (not the imperative
  `git+file://`).
- `modules/home/default.nix` — added `./profiles/min/orchestrate.nix` to the
  explicit imports list (beside spirit.nix).
- `flake.lock` — `nix flake lock` added only the orchestrate subtree;
  `orchestrate/nixpkgs` and `orchestrate/rust-build/nixpkgs` both dedup-follow
  CriomOS-home's nixpkgs. Existing pins untouched (no `nix flake update`).

Design note: the signal path is li/ouranos-`primary`-specific (like the
prometheus ssh matchBlock in profiles/min/default.nix). It uses
`config.home.homeDirectory` so it is not a hardcoded `/home/li` literal. The
`orchestrate` CLI agents invoke is still the imperative profile install (same
rev/version, so wire-compatible); folding that into `home.packages` is a natural
follow-up but was kept out of scope to minimise cutover blast radius.

### Verification (build + eval, non-activating)

- `nix-instantiate --parse` on orchestrate.nix, flake.nix, default.nix → OK.
- `nix flake lock` → orchestrate pinned at `8f9b4170`, nixpkgs deduplicated,
  only the new subtree added.
- Built the orchestrate package as CriomOS-home resolves it (follows applied),
  via `getFlake … .inputs.orchestrate.packages.x86_64-linux.default`:
  instantiates `orchestrate-0.4.1` (version parity with the running daemon) and
  realises successfully → output `bin/` carries `orchestrate-daemon`,
  `orchestrate`, `meta-orchestrate`. Proves the pinned input + `follows`
  compile against LiGoldragon/nixpkgs.
- `lib.evalModules` render of the unit → exact rendered fields:
  `ExecStart = <orchestrate>/bin/orchestrate-daemon
  /home/li/primary/orchestrate/orchestrate-daemon.signal`,
  `Restart = on-failure`, `RestartSec = 2s`, `WantedBy = [ default.target ]`,
  `Description = Orchestrate multi-agent claim/coordination daemon`.

No lojix deploy was submitted (a Home Build's execution is currently
unobservable — see bead `primary-wgae`; the local build+eval above is the real
proof).

### DEFERRED live cutover — exact safe steps (watched quiet window)

Goal: adopt the running manual daemon (pid 58903) under systemd supervision
without dropping active claim coordination. The redb at
`/home/li/primary/orchestrate/orchestrate.redb` is the durable claim store and
survives a restart, so claims reload on restart; the only risk window is
in-flight requests during the ~1s restart. Do this only when
`orchestrate "(Observe Roles)"` shows no lane mid-claim (or the operator accepts
transient reacquire).

1. (Optional, makes activation fast) build-only first:
   ```
   meta-lojix '(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=faf8c230d0fa Build None [])))'
   ```
   (Admission is not execution proof — bead `primary-wgae`.)
2. Stop the manual daemon so it releases its sockets (kill-BEFORE-start avoids
   split-brain; the daemon unlinks stale socket inodes on rebind, so no manual
   socket cleanup is needed):
   ```
   kill 58903            # graceful SIGTERM; confirm: ! kill -0 58903 2>/dev/null
   ```
3. Activate the home generation (installs + starts the unit). With
   home-manager's sd-switch this both installs and starts orchestrate-daemon.service:
   ```
   meta-lojix '(Deploy (Home (goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriomOS-home?rev=faf8c230d0fa Activate None [])))'
   systemctl --user daemon-reload
   systemctl --user start orchestrate-daemon.service     # no-op if sd-switch already started it
   ```
4. Verify:
   ```
   systemctl --user status orchestrate-daemon.service    # active (running); MainPID = new daemon
   systemctl --user show -p Restart orchestrate-daemon.service   # Restart=on-failure
   orchestrate "(Observe Roles)"                         # responds; claims reloaded from redb
   ls -l /home/li/primary/orchestrate/orchestrate.sock   # socket present
   ```
5. Rollback if the unit misbehaves:
   ```
   systemctl --user stop orchestrate-daemon.service
   setsid nohup orchestrate-daemon /home/li/primary/orchestrate/orchestrate-daemon.signal &
   ```
   (declarative unit stays installed but stopped; then diagnose.)

Additional notes:
- **Reboot persistence** also needs the ouranos SYSTEM generation to pin a
  criomos-home input that includes `faf8c230` (a Home Activate covers the live
  session only). Confirm/schedule a System Switch if reboot-survival is required.
- **Version-neutral**: the unit runs orchestrate v0.4.1 @ `8f9b4170`, identical
  to pid 58903 — supervision only, no behavior shift.
- **Unplanned-activation hazard (flag to operator)**: now that the unit is on
  CriomOS-home main, the NEXT home Activate by ANY agent installs+starts it. If
  that happens while pid 58903 still runs, home-manager either fails to bind
  (→ Restart loop) or rebinds and orphans pid 58903 (→ two daemons on one redb).
  Mitigation: treat the next ouranos home Activate AS this cutover (do step 2
  first), or land a quick `criomosHome.orchestrate.enable = false` until the
  window is scheduled. Home Activates on ouranos are deliberate/rare and are
  currently deferred anyway (the prior worker's ssh fold-in also awaits one), so
  practical risk is low — but it must be watched.

## Tasks 2 & 3 — CriomOS agent-doc doctrine — CriomOS main `4140322e` (pushed)

Two bullets added to `AGENTS.md` "Hard process rules" (docs-only; no code/version
surface):
- **#8 whole-OS eval recipe**: bare `nix eval`/`flake show`/`flake check` throws
  `CriomOS: no system input was provided` by design (system/horizon/deployment/
  secrets are throwing stubs until lojix materializes them). Documented the
  witnessed working recipe: build
  `.#nixosConfigurations.target.config.system.build.toplevel` with
  `--override-input {system,horizon,deployment,secrets}` pointed at
  `/var/lib/lojix/generated-inputs/<cluster>/<node>/<full-os|os-only|home>/…`.
  (Input names + host layout verified live; witnessed ~47s / 26 drvs.)
- **#12 VM inventory**: `microvm -l` is blind on CriomOS hosts (assumes an
  `/etc/nixos` flake they lack; reports empty beside a live guest). Use
  `systemctl list-units 'microvm@*'` + `ls /var/lib/microvms`; a guest's runtime
  is `microvm@<name>.service`.

## Task 4 — beads filed (RECORD only, label `field-readiness`)

- **`primary-wgae`** (P2): lojix admitted a Home Build with no observable
  execution/outcome via journal or ByNode — sustained-session deploy loop;
  touches the deploy daemon. Diagnosis deferred.
- **`primary-oftl`** (P3): converge the nixos-test-follows-kvm capability from
  CriomOS `builder.nix` (fast path) into its canonical home
  `horizon-rs/lib/src/node.rs` on the next lojix daemon redeploy.

## Edit-coordination note (incident + clean recovery)

CriomOS-home's canonical checkout held another agent's uncommitted listener/
dictation work, so all CriomOS-home edits were done in an isolated jj workspace
and landed on main (their commit `b300b067` had already advanced main; my commit
is a clean child). For CriomOS, the shared checkout was initially clean but a
concurrent agent added `vm-guest-networking` work (`router/default.nix` +
`test-vm-host.nix`) into it mid-session; my first `jj commit` there accidentally
swept their uncommitted changes into my commit and moved their bookmark. Caught
before any push; recovered with `jj op restore` to their last op (`5644f88`),
which fully restored their working copy + bookmarks (`main`→f8eb6ff7,
`vm-guest-networking`→00131f3c, their durable work safe+pushed on
`vm-guest-networking@origin`) and reverted my contamination. Redid the AGENTS.md
edit in a fresh isolated workspace and landed cleanly (`4140322e`). Both my
isolated workspaces were `jj workspace forget`-ed and removed at closeout.

## Checks run
- Parse: `nix-instantiate --parse` on all edited .nix files → OK.
- `nix flake lock` (CriomOS-home) → orchestrate pinned + nixpkgs deduped.
- Build: orchestrate-0.4.1 realised through the followed nixpkgs → yields
  `orchestrate-daemon`.
- Eval: `lib.evalModules` render of the unit → correct ExecStart/Restart/
  WantedBy.
- Live host: pid 58903 untouched (alive + responsive at closeout).
- Pushes: CriomOS-home `faf8c230`, CriomOS `4140322e`.

## Follow-ups for the psyche / operator
- Perform the orchestrate cutover in a watched window (steps above); or land
  `criomosHome.orchestrate.enable=false` interim if a stray home Activate is a
  concern before the window.
- Fold the `orchestrate` CLI into `home.packages` (retire the imperative
  `nix profile install`) once the daemon cutover is proven.
- Diagnose `primary-wgae` (Home Build observability) — it currently blocks
  clean deploy-loop verification.
