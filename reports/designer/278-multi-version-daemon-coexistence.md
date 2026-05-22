# Multi-version daemon coexistence — version-suffixed sockets, CLIs, and a default-resolution shim

Designer-lane design report. Triggered 2026-05-22 by psyche record
108 (intent/deploy.nota, Medium certainty). The driver is the
imminent Spirit-Magnitude cutover: the migrated `v0.1.1` redb at
`/home/li/.local/state/persona-spirit/persona-spirit.redb.v0.1.1.migrated-20260522075112`
cannot be served by the deployed `v0.1.0` daemon binary, and the
v0.1.0 daemon still owns the live `persona-spirit.redb`.

## 1. The problem

Currently `modules/home/profiles/min/spirit.nix` deploys exactly
one Spirit daemon for the user session: one `writeShellScriptBin
"spirit"` wrapper, one `systemd.user.services.persona-spirit-daemon`
invoking the daemon with one NOTA tuple
`("…/spirit.sock" "…/owner.sock" "…/persona-spirit.redb" 384 None)`,
one stateDirectory `~/.local/state/persona-spirit/`.

When v0.1.1 home-redeploys, the systemd unit's `ExecStart` flips
to the new binary, which opens the redb file at the same path. If
the on-disk schema is v0.1.0 layout, v0.1.1 either refuses to open
it or corrupts on first write. The v0.1.0 binary has already
vanished from the user profile by then.

No in-place cutover preserves rollback. The psyche's proposal —
both daemons coexist, each on its own socket pair, each opening its
own redb, a default-resolution shim picking which one bare `spirit`
talks to — is the multi-version coexistence pattern.

## 2. Does the pattern make sense?

Yes. The triad's component model places one redb behind one
daemon, with socket addresses configurable per invocation. Nothing
in the spirit code, the signal contract, or the runtime assumes a
singleton daemon per machine — that assumption lives entirely in
the home-manager module's path choices. Making path choices
version-aware is a configuration-layer change, not a contract or
runtime change.

The same shape generalises to every component (`lojix`, `criome`,
`persona-mind`, etc.) once it has more than one deployed version on
a single machine. The pattern earns its keep beyond Spirit.

Cost: one extra systemd-user unit per coexisting version, one extra
wrapper script per version, one symlink managed by home-manager
activation. The state directory grows by one level — a per-version
subdirectory — which the daemon already accepts since paths are
arguments.

## 3. The five concrete shape decisions

### 3.1 Sockets — per-version subdirectory

Pick: **(a) per-version subdirectory**.

```
~/.local/state/persona-spirit/
  v0.1.0/
    spirit.sock
    owner.sock
    persona-spirit.redb
  v0.1.1/
    spirit.sock
    owner.sock
    persona-spirit.redb
  current -> v0.1.1            (home-managed symlink)
```

Why subdirectory not filename suffix:

- The daemon takes a triple `(ordinary owner store)` — they must
  live together for one version. A subdirectory keeps the three
  inseparable; filename suffixes scatter them.
- Backups and migration outputs already use a per-file timestamp
  suffix convention. Re-using suffixes for version creates two
  parallel suffix vocabularies on the same files.
- redb's lock file lives next to the redb file. Subdirectory
  isolates locks per version automatically.

Daemon argument shape **does not change**: still
`(ordinary-sock-path owner-sock-path store-path 384 None)`. Only
the paths the home-manager module computes change.

### 3.2 CLI binaries — per-version wrapper, default via symlink

Pick: **(c) hybrid — per-version wrapper scripts + a default
shim symlink**.

For each deployed version, home-manager installs a wrapper named
`spirit-vX.Y.Z` in `~/.nix-profile/bin/`:

```bash
# ~/.nix-profile/bin/spirit-v0.1.1  (writeShellScriptBin output)
export PERSONA_SPIRIT_SOCKET="${PERSONA_SPIRIT_SOCKET:-~/.local/state/persona-spirit/v0.1.1/spirit.sock}"
export PERSONA_SPIRIT_OWNER_SOCKET="${PERSONA_SPIRIT_OWNER_SOCKET:-~/.local/state/persona-spirit/v0.1.1/owner.sock}"
exec /nix/store/…/bin/spirit "$@"
```

The default unsuffixed `spirit` resolves through the shim mechanism
in §3.3 — it is not a separately-written wrapper.

Why per-version wrappers rather than one wrapper reading
`SPIRIT_VERSION`:

- Per-version wrappers are nix-store-stable — each path is content-
  addressed, so rollback to a prior home generation revives the
  prior wrappers automatically.
- A version-selector env var is runtime-mutable inside a single
  shell — useful for ad-hoc experiments but ambiguous as the
  defining mechanism. Subagents and systemd units don't read
  user-shell env reliably.
- The CLI's "one Signal peer" invariant from
  `skills/component-triad.md` is preserved per binary — each
  suffixed binary still talks to exactly one daemon socket pair.

### 3.3 Shell shim — home-managed symlink in `~/.nix-profile/bin/`

Pick: **(b) symlink in PATH** — home-manager activation script
maintains `~/.nix-profile/bin/spirit` pointing at the currently-
selected `spirit-vX.Y.Z` wrapper.

Why symlink not shell alias not wrapper-with-config-file:

- Symlinks work for every process — interactive shells, systemd
  units, subagents, cron scripts. Shell aliases only work in
  interactive shells that loaded them.
- A wrapper reading a config file gives runtime switching but adds
  indirection on every invocation, and changes outside home-manager
  become invisible to subsequent redeploys.
- The symlink is created by home-manager activation, so the default
  is declarative in `spirit.nix`. Rollback of the home generation
  rolls back the default alongside the wrappers.

For ad-hoc per-shell override against the non-default version, the
developer invokes the suffixed binary directly:
`spirit-v0.1.0 '(Query …)'`. No env var, no config file.

### 3.4 Default-version declaration — Nix module option

Pick: **(a) declarative in the home-manager module**.

The spirit module gains a list of versions to deploy and a
single-version `currentDefault` choice:

```nix
config.persona-spirit = {
  deployedVersions = [ "v0.1.0" "v0.1.1" ];
  currentDefault   = "v0.1.1";
};
```

Home-manager evaluates this once per generation and:

- Generates one wrapper `spirit-vX.Y.Z` per element of
  `deployedVersions`.
- Generates one systemd user unit
  `persona-spirit-daemon-vX.Y.Z.service` per element.
- Creates the `~/.nix-profile/bin/spirit` symlink pointing at
  `spirit-${currentDefault}`.

Why declarative not runtime-mutable: switching the default is a
deliberate operation, not an ambient-state question. Rebuild-
required is a feature — the change is reviewed, committed,
rollback-able. Runtime-mutable defaults split the source of truth
across two surfaces. Cost is one home-redeploy per default switch.

### 3.5 Cutover protocol — verify before flip

Five steps for v0.1.0 → v0.1.1:

1. **Land module change.** First home-redeploy sets
   `deployedVersions = [ "v0.1.0" "v0.1.1" ]`,
   `currentDefault = "v0.1.0"`. Both daemons start; v0.1.1 opens
   an empty `v0.1.1/` directory. Bare `spirit` still v0.1.0.

2. **Copy migrated database.** Stop v0.1.1 daemon, copy
   `persona-spirit.redb.v0.1.1.migrated-…` to
   `v0.1.1/persona-spirit.redb`, restart v0.1.1.

3. **Verify v0.1.1 explicitly.** Invoke
   `spirit-v0.1.1 '(Query …)'` — bare `spirit` is still v0.1.0.
   Confirm migrated content reads back.

4. **Flip the default.** Second home-redeploy with
   `currentDefault = "v0.1.1"`. Symlink retargets; new shells and
   subagents see `spirit -> spirit-v0.1.1`. v0.1.0 stays alive for
   rollback.

5. **Retire v0.1.0.** After a confidence period, third redeploy
   drops v0.1.0 from `deployedVersions`. Unit, wrapper, and home
   generation references all disappear. The v0.1.0 redb file stays
   on disk for archival until the operator deletes it.

## 4. What changes where

All changes are in CriomOS-home (system-specialist surface).
Nothing changes in the persona-spirit triad — daemon argument
shape, CLI argument shape, contract names, and signal trees are all
unchanged.

**`modules/home/profiles/min/spirit.nix`** — full rewrite:

- Takes the persona-spirit flake input and projects per-version
  derivations. Either the input carries a set keyed by version, or
  multiple persona-spirit inputs are declared in `flake.nix`
  (`persona-spirit-v0_1_0`, `persona-spirit-v0_1_1`).
- Builds `home.packages` by mapping over `deployedVersions` — one
  `writeShellScriptBin "spirit-${v}"` per entry.
- Builds `systemd.user.services` by mapping over
  `deployedVersions` — one `persona-spirit-daemon-${v}` per entry,
  each with its NOTA argument naming the per-version paths.
- Adds a `home.activation` step that creates/updates the
  `~/.nix-profile/bin/spirit` symlink to point at
  `spirit-${currentDefault}`.
- Removes the workspace-level `sessionVariables` setting
  `PERSONA_SPIRIT_SOCKET` / `PERSONA_SPIRIT_OWNER_SOCKET` to fixed
  paths — those env vars now live per-wrapper.

**`flake.nix`** in CriomOS-home — second persona-spirit input
added. v0.1.0 is already pinned (per operator/151); v0.1.1's tag
will be created when the next release is cut.

**`flake.lock`** — updates from the second input. Per the
2026-05-21 Constraint in intent/deploy.nota, this lock-file update
is part of the deployment workflow.

**Nothing changes** in the persona-spirit, signal-persona-spirit,
or owner-signal-persona-spirit repos.

## 5. Lifecycle examples

**Adding v0.2.0 later** — append `"v0.2.0"` to `deployedVersions`,
leave `currentDefault` alone. One redeploy stands the new daemon
up; verification follows; one more redeploy flips the default.
Three versions can transiently coexist for diamond rollouts.

**Emergency rollback after default flip** — one redeploy reverts
`currentDefault` to the previous version. Both daemons still
running, both redbs intact; rollback is the symlink retarget.

**Extending to lojix** — same module shape applies. lojix's module
would gain `deployedVersions` and `currentDefault`. The shim
symlink lives under `/etc` rather than the user profile because
lojix is system-scope, but the discipline is the same.

## 6. Bead recommendation

**File a bead for system-specialist, do not implement directly.**
The implementation surface is entirely CriomOS-home — a
system-specialist lane. Designer-lane work ends with this report.
The operator driving the Spirit-Magnitude migration should file the
bead.

Proposed title: "Multi-version persona-spirit daemon coexistence in
home-manager (v0.1.0 + v0.1.1)".

Concrete tasks:

1. Refactor `modules/home/profiles/min/spirit.nix` to take
   `deployedVersions` (list of version strings) and `currentDefault`
   (one version string).
2. Generate one `writeShellScriptBin "spirit-${v}"` per version
   setting per-version socket env vars.
3. Generate one `systemd.user.services.persona-spirit-daemon-${v}`
   per version with NOTA argument
   `("…/v/spirit.sock" "…/v/owner.sock" "…/v/persona-spirit.redb"
   384 None)`.
4. Add a `home.activation` step maintaining
   `~/.nix-profile/bin/spirit` as a symlink to
   `spirit-${currentDefault}` — atomic-symlink compatible with
   home-manager's activation discipline.
5. Update `flake.nix` to expose v0.1.0 and v0.1.1 separately (or
   one input providing per-version derivations); update
   `flake.lock`.
6. Document the cutover protocol from §3.5 in a `docs/` entry
   inside CriomOS-home.
7. Manual verification: home-redeploy lands both daemons; both
   sockets exist; `spirit` resolves to `currentDefault`; both
   suffixed binaries resolve to their daemons.

Label: `system-specialist`. Cross-link to operator/151, designer/
273, intent/deploy.nota record 108.

## 7. Open psyche questions

None blocking. Three soft notes:

- **Confidence period before retiring v0.1.0** is unspecified.
  Suggestion: leave v0.1.0 deployed for at least one work week
  after the default flips. Faster is fine if the psyche decides
  v0.1.1 is verified; discipline is "don't retire on the same day
  you flip".
- **State-directory cleanup on retirement** is out of home-
  manager's scope. When v0.1.0 is dropped from
  `deployedVersions`, `~/.local/state/persona-spirit/v0.1.0/`
  remains. Cleanup is a separate operator call — too easy to
  accidentally drop an unverified database.
- **Extending to other components** (lojix, criome, persona-mind,
  persona-orchestrate) is the natural next step. Flag once a
  second component needs a coexistence cutover.
