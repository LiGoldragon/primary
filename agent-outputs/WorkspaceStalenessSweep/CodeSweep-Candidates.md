# Code Sweep Candidates

Task: Phase-1 read-only code sweep for epic `primary-5rzf`, bead `primary-5rzf.3`.

Scope: tracked files in active workspace code repositories named by
`/home/li/primary/protocols/active-repositories.md`, plus the tracked primary
workspace coordination/config files. The sweep did not inspect
`/home/li/primary/private-repos`. The `repos/assistant-reports` and
`repos/counselor-reports` symlinks resolve into `../private-repos/...` and were
treated as private-boundary stops.

Evidence rule applied: CANDIDATES below name the new thing, old thing, locator,
and evidence. Items missing any part, or whose old shape may still be live, are
under SUSPECTS.

## REPOS COVERED

77 active-map paths existed and were searched with tracked-file lists:

- `/home/li/primary`
- `/git/github.com/LiGoldragon/CriomOS`
- `/git/github.com/LiGoldragon/CriomOS-home`
- `/git/github.com/LiGoldragon/TheBookOfSol`
- `/git/github.com/LiGoldragon/chroma`
- `/git/github.com/LiGoldragon/chronos`
- `/git/github.com/LiGoldragon/cloud`
- `/git/github.com/LiGoldragon/criome`
- `/git/github.com/LiGoldragon/domain-criome`
- `/git/github.com/LiGoldragon/goldragon`
- `/git/github.com/LiGoldragon/harness`
- `/git/github.com/LiGoldragon/horizon-rs`
- `/git/github.com/LiGoldragon/introspect`
- `/git/github.com/LiGoldragon/lojix-cli`
- `/git/github.com/LiGoldragon/lore`
- `/git/github.com/LiGoldragon/mentci`
- `/git/github.com/LiGoldragon/mentci-lib`
- `/git/github.com/LiGoldragon/message`
- `/git/github.com/LiGoldragon/meta-signal-agent`
- `/git/github.com/LiGoldragon/meta-signal-cloud`
- `/git/github.com/LiGoldragon/meta-signal-criome`
- `/git/github.com/LiGoldragon/meta-signal-domain-criome`
- `/git/github.com/LiGoldragon/meta-signal-harness`
- `/git/github.com/LiGoldragon/meta-signal-introspect`
- `/git/github.com/LiGoldragon/meta-signal-mentci`
- `/git/github.com/LiGoldragon/meta-signal-message`
- `/git/github.com/LiGoldragon/meta-signal-mind`
- `/git/github.com/LiGoldragon/meta-signal-orchestrate`
- `/git/github.com/LiGoldragon/meta-signal-persona`
- `/git/github.com/LiGoldragon/meta-signal-repository-ledger`
- `/git/github.com/LiGoldragon/meta-signal-router`
- `/git/github.com/LiGoldragon/meta-signal-spirit`
- `/git/github.com/LiGoldragon/meta-signal-system`
- `/git/github.com/LiGoldragon/meta-signal-terminal`
- `/git/github.com/LiGoldragon/meta-signal-upgrade`
- `/git/github.com/LiGoldragon/meta-signal-version-handover`
- `/git/github.com/LiGoldragon/mind`
- `/git/github.com/LiGoldragon/nexus`
- `/git/github.com/LiGoldragon/nexus-cli`
- `/git/github.com/LiGoldragon/nota-config`
- `/git/github.com/LiGoldragon/nota-next`
- `/git/github.com/LiGoldragon/orchestrate`
- `/git/github.com/LiGoldragon/persona`
- `/git/github.com/LiGoldragon/repository-ledger`
- `/git/github.com/LiGoldragon/router`
- `/git/github.com/LiGoldragon/schema-next`
- `/git/github.com/LiGoldragon/schema-rust-next`
- `/git/github.com/LiGoldragon/sema`
- `/git/github.com/LiGoldragon/sema-engine`
- `/git/github.com/LiGoldragon/signal`
- `/git/github.com/LiGoldragon/signal-agent`
- `/git/github.com/LiGoldragon/signal-cloud`
- `/git/github.com/LiGoldragon/signal-criome`
- `/git/github.com/LiGoldragon/signal-domain-criome`
- `/git/github.com/LiGoldragon/signal-harness`
- `/git/github.com/LiGoldragon/signal-introspect`
- `/git/github.com/LiGoldragon/signal-mentci`
- `/git/github.com/LiGoldragon/signal-message`
- `/git/github.com/LiGoldragon/signal-mind`
- `/git/github.com/LiGoldragon/signal-orchestrate`
- `/git/github.com/LiGoldragon/signal-persona`
- `/git/github.com/LiGoldragon/signal-repository-ledger`
- `/git/github.com/LiGoldragon/signal-router`
- `/git/github.com/LiGoldragon/signal-sema`
- `/git/github.com/LiGoldragon/signal-spirit`
- `/git/github.com/LiGoldragon/signal-standard`
- `/git/github.com/LiGoldragon/signal-system`
- `/git/github.com/LiGoldragon/signal-terminal`
- `/git/github.com/LiGoldragon/signal-upgrade`
- `/git/github.com/LiGoldragon/signal-version-handover`
- `/git/github.com/LiGoldragon/spirit`
- `/git/github.com/LiGoldragon/system`
- `/git/github.com/LiGoldragon/terminal`
- `/git/github.com/LiGoldragon/terminal-cell`
- `/git/github.com/LiGoldragon/triad-runtime`
- `/git/github.com/LiGoldragon/upgrade`
- `/git/github.com/LiGoldragon/version-projection`

## CANDIDATES

### C1: Persona runtime still exposes `persona-mind` for the `mind` component

New thing: `mind` component/repo and `mind-daemon`.

Old thing killed: `persona-mind` component name/path.

Locator:

- `/git/github.com/LiGoldragon/persona/src/engine.rs:445` maps incoming
  `"persona-mind"` to `EngineComponent::Mind`.
- `/git/github.com/LiGoldragon/persona/src/engine.rs:544` emits
  `EngineComponent::Mind` as `"persona-mind"`.
- `/git/github.com/LiGoldragon/persona/flake.nix:21` names the input
  `persona-mind` while pointing at `github:LiGoldragon/mind`.
- `/git/github.com/LiGoldragon/persona/flake.nix:187` creates
  `persona-mind-prototype-launcher` for `mind-daemon`.

Evidence:

- Handoff evidence explicitly says "`persona-mind` is a dead name -- the thing
  is `mind` now."
- `protocols/active-repositories.md` lists `mind` at
  `/git/github.com/LiGoldragon/mind` as the active central Persona state
  component.
- `/git/github.com/LiGoldragon/mind/Cargo.toml` declares package and binaries
  under `mind` / `mind-daemon`, not `persona-mind`.

Private-boundary flag: none.

### C2: Primary workspace file still points at dead `persona-mind` checkout path

New thing: `/git/github.com/LiGoldragon/mind`.

Old thing killed: `/git/github.com/LiGoldragon/persona-mind`.

Locator:

- `/home/li/primary/primary.code-workspace:16` folder name
  `"persona-mind"`.
- `/home/li/primary/primary.code-workspace:17` folder path
  `"/git/github.com/LiGoldragon/persona-mind"`.

Evidence:

- Handoff evidence explicitly says "`persona-mind` is a dead name -- the thing
  is `mind` now."
- `protocols/active-repositories.md` lists `mind` at
  `/git/github.com/LiGoldragon/mind`.
- The active-map coverage command found `/git/github.com/LiGoldragon/mind`;
  the stale workspace path is not an active-map repo.

Private-boundary flag: none.

### C3: `lojix` README still sends implementation to superseded `horizon-re-engineering`

New thing: `horizon-leaner-shape` feature arc.

Old thing killed: `horizon-re-engineering` feature branch/worktrees as the
place to pick up new work.

Locator:

- `/git/github.com/LiGoldragon/lojix/README.md:17` says first implementation
  lands on the `horizon-re-engineering` feature branch.

Evidence:

- `/home/li/primary/protocols/active-repositories.md:135` says
  `horizon-leaner-shape` supersedes the earlier `horizon-re-engineering` work
  as of 2026-05-17.
- `/home/li/primary/protocols/active-repositories.md:145` says
  `horizon-re-engineering` worktrees still exist but are superseded and new work
  belongs on `horizon-leaner-shape`.

Private-boundary flag: none.

## SUSPECTS

### S1: `signal-persona-mind` references look stale but lack explicit rename evidence

New thing: likely `signal-mind`.

Old thing: `signal-persona-mind`.

Locator:

- `/home/li/primary/primary.code-workspace:72` names
  `"signal-persona-mind"`.
- `/home/li/primary/primary.code-workspace:73` points at
  `"/git/github.com/LiGoldragon/signal-persona-mind"`.
- `/home/li/primary/orchestrate/AGENTS.md:347` says the typed target is
  `signal-persona-mind`.
- `/git/github.com/LiGoldragon/meta-signal-router/skills.md:14` links to
  `../signal-persona-mind/ARCHITECTURE.md`.

Evidence status:

- `protocols/active-repositories.md` lists the active repo as `signal-mind`.
- The four-part confirmed rule is not satisfied because this sweep found no
  explicit `signal-persona-mind` to `signal-mind` rename/deprecation statement.

Private-boundary flag: none.

### S2: Router Wi-Fi code exists but has no new thing

New thing: unknown.

Old thing: router Wi-Fi / router wifi configuration surface.

Locator:

- `/git/github.com/LiGoldragon/CriomOS/checks/router-wifi-secret/default.nix:9`
  names "router Wi-Fi password".
- `/git/github.com/LiGoldragon/CriomOS/checks/router-wifi-horizon-policy/default.nix:9`
  names "router wifi country code".
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/router/default.nix:92`
  names "router Wi-Fi secret".

Evidence status:

- Handoff says "router Wi-Fi" is a mystery item the psyche never raised.
- The four-part confirmed rule is not satisfied because no replacement/new
  thing was identified.

Private-boundary flag: none.

### S3: `schema-rust-next` migration status disagreement belongs to verification or docs sweep

New thing: `RustModuleRenderer` plus `proc_macro2::TokenStream` / `quote!`
token wrappers.

Old thing: `RustWriter` / hand-rolled string emitter.

Locator:

- `/home/li/primary/protocols/active-repositories.md:37` still describes the
  old `RustWriter` string emitter as "mid-migration out" with remaining string
  surface transitional.
- `/git/github.com/LiGoldragon/schema-rust-next/INTENT.md:110` says there is no
  `self.line` / `format!`-built Rust source left in either emitter.
- `/git/github.com/LiGoldragon/schema-rust-next/INTENT.md:111` says the former
  `RustWriter` is gone and replaced by `RustModuleRenderer`.
- `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:5757` defines
  `RustModuleRenderer`; `/git/github.com/LiGoldragon/schema-rust-next/src/lib.rs:6064`
  routes item syntax through `emit_item_tokens`.

Evidence status:

- This looks like a finished effort still described as active in the workspace
  active-map doc, not a live code deletion candidate. The code still has a
  `line` method for the generated header, and repo docs explicitly allow that
  header exception. Keep off the confirmed code-deletion track unless verifier
  reroutes it as a docs correction.

Private-boundary flag: none.

### S4: `terminal` versus `terminal-cell` has conflicting live evidence

New thing: `terminal-cell` for active V1 harness Claude/Codex terminal tests.

Old thing: `terminal` / `persona-terminal` as a V1 harness test route.

Locator:

- `/git/github.com/LiGoldragon/persona/flake.nix:59` uses
  `persona-terminal.url = "github:LiGoldragon/terminal"`.
- `/git/github.com/LiGoldragon/persona/flake.nix:60` also imports
  `terminal-cell`.
- `/git/github.com/LiGoldragon/persona/flake.nix:214` creates
  `persona-terminal-prototype-launcher`.
- `/git/github.com/LiGoldragon/harness/ARCHITECTURE.md:314` still links
  `../terminal/ARCHITECTURE.md`.

Evidence status:

- `protocols/active-repositories.md` marks `terminal` archived/inactive until
  further notice and says not to route V1 harness Claude/Codex tests through it;
  use `terminal-cell` directly.
- `persona` code still has a broader supervised terminal topology, so this is
  not safe as a confirmed dead consumer without verifier deciding which
  terminal uses are still live.

Private-boundary flag: none.

### S5: `persona-spirit-daemon` names in deployment cleanup may be intentional guards

New thing: `spirit-daemon` service/binary.

Old thing: `persona-spirit-daemon` service family.

Locator:

- `/git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix:129`
  asserts the unversioned `persona-spirit-daemon` service is absent.
- `/git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix:133`
  asserts old `persona-spirit-daemon-v0.5.2` is absent.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:177`
  through `:188` list old `persona-spirit-daemon*` units in a stop/cleanup list.

Evidence status:

- The same deployment surface uses `spirit-daemon` at
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:173`
  and `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:200`.
- The old names appear to be cleanup/absence guards, not necessarily dead
  consumers. Leave for verifier; do not auto-kill from the code sweep.

Private-boundary flag: none.

## Commands And Checks

Commands consulted:

- `sed -n '1,260p' /home/li/primary/agent-outputs/WorkspaceStalenessSweep/Handoff-CodexEpicHandoff.md`
- `sed -n '1,220p' /home/li/primary/INTENT.md`
- `sed -n '1,240p' /home/li/primary/ARCHITECTURE.md`
- `sed -n '1,220p' /home/li/primary/protocols/active-repositories.md`
- `find /home/li/primary/repos -maxdepth 1 -mindepth 1 -type l -printf '%f -> %l\n'`
- `jj status` in `/home/li/primary`
- Per active repo: `jj file list | tr '\n' '\0' | xargs -0 -r rg -n --color never -i <pattern>`
- Targeted line reads with `sed` in `persona`, `mind`, `lojix`, `CriomOS`,
  `CriomOS-home`, `schema-rust-next`, `schema-next`, `signal-spirit`,
  `meta-signal-spirit`, `spirit`, `harness`, `terminal`, `terminal-cell`,
  `orchestrate`, `repository-ledger`, `signal-upgrade`, and
  `meta-signal-upgrade`.

Checks not run:

- No builds, tests, deletion checks, tracker state changes, commits, or pushes
  were run. This bead is read-only and the verifier bead is the deletion gate.

Boundary notes:

- Private symlink boundary observed and skipped:
  `repos/assistant-reports -> ../private-repos/assistant-reports` and
  `repos/counselor-reports -> ../private-repos/counselor-reports`.
- Spirit intent records were not used as evidence for findings. A broad
  validation pass over primary was discarded after it proved too wide for this
  bead; the findings above are based on the scoped repo/code searches and the
  handoff/active-map context.

## Unknowns And Follow-Up

- The verifier should decide whether C1 and C2 require code/config updates
  together, because `persona` currently treats `persona-mind` as an external
  component name while the repo and handoff call the name dead.
- The verifier should route C3 appropriately if code-repo README edits are owned
  by the docs kill bead rather than the code kill bead.
- S1 needs explicit rename evidence before it can become confirmed.
- S2 cannot be confirmed until a new/replacement thing is identified.
- S4 and S5 both have evidence that the old names may still serve live
  compatibility, topology, or cleanup purposes.
