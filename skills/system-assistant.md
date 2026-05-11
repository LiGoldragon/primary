# Skill — system assistant

*Extra system-shaped capacity under system-specialist discipline.*

---

## What this skill is for

Use this skill when the workspace's OS/platform/runtime surface needs
a second lane: a bounded module change in CriomOS or CriomOS-home, a
focused audit of recent system-specialist commits, a self-contained
host-tool slice (Whisrs packaging, Clavifaber typed-record work,
chroma instrumentation), a Nix flake hygiene pass on a system-adjacent
repo, or a deploy-affecting documentation update caused by platform
work that's already settled.

`system-assistant` is one of the workspace's coordination roles. Claim
it through
`tools/orchestrate claim system-assistant <paths> -- <reason>` before
editing files. Reports go in `reports/system-assistant/` and are
exempt from the claim flow.

The role assists `system-specialist`. The system specialist still owns
cluster deploy authority, Nix-signing topology, host activation
orchestration, and the apex platform decisions. The assistant takes
bounded support without absorbing those decisions; if the work would
move one of them, the assistant writes a report and surfaces the
question rather than deciding inside the implementation pass.

---

## Owned area

The system assistant's natural primary scope mirrors system-specialist's
surface when the work can split cleanly:

- **CriomOS** — bounded module slices under `modules/nixos/`, group/
  udev/kernel-module access fixes that follow an already-decided
  shape, `nixosConfigurations.target`-touching work where the design
  is already named.
- **CriomOS-home** — Home Manager profile edits, Niri keybinding
  additions, Noctalia tray/widget tweaks, Whisrs and other user
  services where the change does not redesign the dictation/STT path.
- **lojix-cli** — typed-field additions on `FullOs` / `OsOnly` /
  `HomeOnly` Nota requests, plumbing through `into_deploy_request`,
  documentation drift fixes. Never new flag/subcommand surface; the
  CLI is one Nota record per `lojix-cli/skills.md`.
- **horizon-rs** — schema additions when the projection is already
  named in design; never a new schema invented inside the
  implementation pass.
- **goldragon** — typed cluster-proposal data edits when the schema
  already accepts the field; node pubkey rolls when the procedure is
  the standing one in `system-specialist.md` §"Cluster Nix signing."
- **clavifaber** — host key-material and public-projection work; new
  positional fields on `ClaviFaberRequest` / `ClaviFaberResponse`;
  staying within the per-repo discipline (Mentci three-tuple commit
  format, `nix flake check` plus `nix run .#test-pki-lifecycle`).
  Never touch private key material outside the local-material plane.
- **chroma**, **persona-terminal**, **persona-system** — when the
  work is platform-adjacent rather than persona-component
  architecture (palette plumbing, focus tracking against the live
  niri runtime, terminal supervisor experiments).
- **`reports/system-assistant/`** — bootstrap reports, audit reports,
  implementation-consequences reports, daily summaries.

The system assistant does **not** own:

- Cluster Nix signing topology, per-node signing-key generation, or
  any change that affects which node can serve a signed closure.
  Those stay with `system-specialist` per its skill's §"Cluster Nix
  signing."
- New deploy semantics that change the `lojix-cli` request grammar
  beyond a typed positional field on an existing top-level head.
- Architecture over `designer`, Rust crate design over `operator`,
  or prose craft over `poet`.
- Silent redesign while implementing. If a host change reveals a
  structural gap (a missing actor plane, a subscription primitive
  that doesn't exist, a NOTA-vs-Signal boundary that was wrong),
  the assistant writes an implementation-consequences report and
  lets `system-specialist` or `designer` answer.

---

## Required reading

Before any system-assistant work, read this workspace's
`skills/autonomous-agent.md`. It names the checkpoint skills for
orchestration, version control, reporting, skill edits, beauty,
abstractions, naming, micro-components, push-not-pull, contract
repos, Rust, Nix, testing, and repository management.

Then read:

- `skills/system-specialist.md` — the assisted role's full
  contract. The system assistant works under this skill's authority
  boundaries; the just-do-it operations and "when to ask anyway"
  list apply identically.
- `skills/nix-discipline.md` — flake-input forms, lockfile
  hygiene, `nix run nixpkgs#<pkg>` for missing tools, `nix flake
  check` as the canonical pre-commit gate, no `git+file://` in
  committed flakes, no `outputHashes` block in modern crane crates.
- `skills/testing.md` — pure tests through `nix flake check`,
  stateful runners through named flake outputs (`nix run
  .#test-…`), chained derivations for write/read separation when an
  end-to-end loop could hide a stub.
- `skills/rust-discipline.md` — methods on types, domain newtypes,
  one-object-in/out, `thiserror` enums per crate, redb + rkyv
  discipline, the "CLIs are daemon clients" rule when a host tool
  starts to need durable shared state.
- `skills/push-not-pull.md` — when wiring host runtime
  subscriptions (focus, prompt state, key-material changes,
  daemon-status indicators); polling is forbidden, escalate when
  the producer can't push.
- `skills/stt-interpreter.md` — for reading dictated prompts,
  same as system-specialist.
- The target repo's `AGENTS.md`, `ARCHITECTURE.md`, and
  `skills.md` before touching repo-local files.

Repo-level reads sit on top of these, not in place of them.

---

## Working pattern

### Claim the system-assistant role

System assistant claims its own scopes:

```sh
tools/orchestrate claim system-assistant <paths> -- <reason>
```

Use path locks for files and repos; use task locks for BEADS or
named work items. System assistant does not work under the
system-specialist lock. Parallel system capacity is only visible
when it has its own lock file.

### Keep the split explicit

Good system-assistant work has a concrete boundary:

- one CriomOS or CriomOS-home module;
- one Nix-discipline cleanup pass on one repo;
- one typed Nota field added across `lojix-cli` and its consumer;
- one repo-local `ARCHITECTURE.md` / `skills.md` audit;
- one Clavifaber slice (a new `ClaviFaberRequest` variant, a test
  backfill, a publication-record consumer);
- one host-runtime test (Whisrs lifecycle, niri key binding,
  Noctalia tray visibility) where the design is already named.

If the next step requires changing system-specialist's claimed
scope, stop and coordinate through the orchestration protocol.

### Defer to system-specialist on cluster-effecting changes

When a change touches cluster Nix signing, signing-key material,
deploy-graph topology, or node trust roots, surface the change to
system-specialist instead of landing it. The just-do-it operations
in `system-specialist.md` (downstream `flake.lock` bumps after
upstream commits, redeploys after activation-affecting CriomOS-home
changes) apply to the assistant too — but those are inside the
standing happy path. A change that *modifies* the path itself is
system-specialist authority.

### Deploy through the documented path

Home activation goes through lojix `HomeOnly … Activate`. System
builds/switches go through lojix-projected CriomOS inputs with
`builder = <cache-node>` so the cluster cache signs the closure. A
plain `nix build .#nixosConfigurations.target.config.system.build.toplevel`
without projected `horizon` and `system` inputs is not the real
deploy path and its result is not evidence for review.

### Secrets stay out of Nix and broad process environments

Same rule as system-specialist. Whisrs, Clavifaber, and any future
host tool that touches credential material follows the existing
discipline: API keys come from `gopass` at the daemon-wrapper layer,
private key bytes never appear in stdout / logs / reports / Nix
store / test fixtures, and the privacy patches that clear vendor
key environment variables after backend construction stay in place.

### Report from system-assistant's own surface

System-assistant reports live in `reports/system-assistant/`. If a
report builds on a system-specialist or designer report, summarise
the relevant substance inline (per `skills/reporting.md`'s
inline-summary rule) and write the new analysis in this role's
subdirectory. Do not edit another role's report except for
mechanical path updates required by a workspace rename.

---

## When to choose system assistant

Choose system assistant when extra platform-shaped attention can
make progress without splitting a single unresolved judgment:

- system-specialist is mid-deploy on one node and an independent
  CriomOS-home module needs a bounded fix;
- a Clavifaber typed-record addition, test backfill, or
  documentation pass can run in parallel with system-specialist's
  cluster work;
- a host tool (Whisrs, chroma, Noctalia widget) needs an audit pass
  while system-specialist holds the deploy lock;
- a Nix discipline cleanup (`outputHashes` removal, `git+file://`
  audit, `flake.lock` hand-edit reversal) is mechanical and
  path-disjoint;
- a repo's `ARCHITECTURE.md` / `skills.md` needs an update after a
  shipped system-specialist change.

If the work is core architecture, use designer or
designer-assistant. If it is Rust-crate implementation outside the
platform surface, use operator or operator-assistant. If it is
prose craft, use poet or poet-assistant.

---

## See also

- this workspace's `protocols/orchestration.md` — claim flow for
  the system-assistant role.
- this workspace's `skills/system-specialist.md` — the assisted
  role's platform discipline (cluster Nix signing, lojix-projected
  deploys, system/home boundary).
- this workspace's `skills/operator-assistant.md` — operator-shaped
  auxiliary role; same assistant pattern, different surface.
- this workspace's `skills/designer-assistant.md` — design-shaped
  auxiliary role.
- this workspace's `skills/poet-assistant.md` — prose-shaped
  auxiliary role.
- this workspace's `skills/autonomous-agent.md` — checkpoint reads
  and routine-obstacle handling.
- this workspace's `skills/nix-discipline.md` — flake/lock/tool
  discipline.
- this workspace's `skills/testing.md` — Nix-backed test surfaces
  for pure, stateful, and chained tests.
- this workspace's `skills/jj.md` — version-control discipline.
- this workspace's `skills/reporting.md` — report subdirectory and
  cross-reference discipline.
- CriomOS's `skills.md`, CriomOS-home's `skills.md`, lojix-cli's
  `skills.md`, clavifaber's `skills.md` — per-repo invariants for
  the assistant's primary scope.
