# Skill — system specialist

*Maintaining the operating-system layer underneath the workspace.*

---

## What this skill is for

Use this skill when the work is about making the system run:
CriomOS, CriomOS-home, lojix deployment, horizon projection, desktop
runtime, user services, input devices, Niri, Noctalia, and system/home
interfaces.

`system-specialist` is one of the workspace's seven coordination roles
(alongside `operator`, `operator-assistant`, `designer`,
`designer-assistant`, `poet`, and `poet-assistant`). Claim it through
`tools/orchestrate claim system-specialist <paths> -- <reason>` before
editing files in the OS / platform surface. Reports go in
`reports/system-specialist/` and are exempt from the claim flow.

---

## Owned area

The system specialist knows how these pieces fit:

- **CriomOS**: NixOS host platform, system modules, device access, groups,
  udev, kernel modules, and the `nixosConfigurations.target` surface.
- **CriomOS-home**: Home Manager profile, Niri bindings, Noctalia, user
  packages, user services, and desktop tools such as Whisrs.
- **lojix-cli**: deploy/build/activate entry point that projects cluster
  proposals into the inputs CriomOS and CriomOS-home consume.
- **horizon-rs**: typed projection/schema source for horizon fields.
- **goldragon**: the cluster proposal data used by lojix for Li's machines.

When a task crosses system and home boundaries, preserve ownership. Example:
Whisrs packaging, keybindings, tray state, clipboard recovery, and transcript
history live in CriomOS-home; `/dev/uinput` group/module/udev access lives in
CriomOS.

---

## Required reading

Read every file below before doing substantive
system-specialist work. The list emphasises Nix and
deployment discipline, plus the Rust crates that ship as host
tools (lojix-cli, horizon-rs, clavifaber, chroma).

**Workspace baseline (every role reads these)**

- `ESSENCE.md`
- `lore/AGENTS.md`
- `protocols/orchestration.md`
- `skills/autonomous-agent.md`
- `skills/beauty.md`
- `skills/naming.md`
- `skills/jj.md`
- `skills/reporting.md`
- `skills/beads.md`
- `skills/skill-editor.md`
- `skills/repository-management.md`
- `skills/stt-interpreter.md`

**Role contracts**

- `skills/system-specialist.md` (this skill)
- `skills/system-assistant.md`
- `skills/operator.md` — knows what binaries get deployed.

**Platform discipline**

- CriomOS's `skills.md` — cluster domain generation, network-neutral
  NixOS module discipline, and the real deploy path.
- `skills/nix-discipline.md`
- `skills/testing.md`
- `skills/micro-components.md`
- `skills/contract-repo.md`
- `skills/push-not-pull.md`
- `skills/language-design.md` — Nota is the lojix surface.

**Rust applied to platform work**

- `skills/abstractions.md`
- `skills/rust-discipline.md` (index)
- `skills/rust/methods.md`
- `skills/rust/errors.md`
- `skills/rust/storage-and-wire.md`
- `skills/rust/parsers.md`
- `skills/rust/crate-layout.md`
- `skills/actor-systems.md`
- `skills/kameo.md`
- `skills/architectural-truth-tests.md`
- `skills/architecture-editor.md`

The repo-level reads (`AGENTS.md`, `ARCHITECTURE.md`,
`skills.md`, plus `docs/ROADMAP.md` and open BEADS for
CriomOS / CriomOS-home) sit on top of these workspace skills
when work enters a specific repo.

---

## Working pattern

Start by reading the relevant repo's `AGENTS.md`, `ARCHITECTURE.md`, and
`skills.md`. For CriomOS and CriomOS-home, also run `bd list --status open`
and read `docs/ROADMAP.md`.

Prefer the existing deployment path over one-off commands:

- Home activation goes through lojix `HomeOnly ... Activate`.
- System builds/switches go through lojix-projected CriomOS inputs.
- Build pushed origin with `--refresh` before trusting the result.
- Keep store paths in shell variables, not prose.
- Do not signal niri.

Niri config changes are not live when they land in a repo or after a
successful build. For changes to `programs.niri.settings` that must affect
the running session, push the CriomOS-home commit, activate the home profile
through lojix `HomeOnly ... Activate`, then reload Niri with
`niri msg action load-config-file`. `load-config-file` is Niri's IPC reload
action; it is allowed. SIGHUP or other process signals remain forbidden. Do
not claim a new window rule, keybind, or runtime setting is being tested until
activation and IPC reload have both happened.

Secrets stay out of Nix and broad process environments. For paid cloud
inference, follow the repo rule: local model first, then ask before using a
paid key unless the user explicitly authorized that call in the current task.

---

## Just-do-it operations

Some operations are part of the standing system-specialist contract: they
follow inevitably from earlier work in the same session, and stopping to
ask about them produces friction without producing a decision. Do them
without confirming.

- **Downstream flake.lock bumps after upstream commits.** When you push
  a change to `lojix-cli`, `horizon-rs`, `nota-codec`, `nota-derive`, or
  any other repo whose output is consumed via flake-input by
  `CriomOS-home` (and transitively by the running system), update
  `CriomOS-home/flake.lock` to point at the new commit and redeploy.
  The chain `nix flake update <input> → commit → push → HomeOnly Activate`
  is the standard path. The rule of thumb: *if you said "use the new
  version" earlier in this session, the user already authorized the lock
  bump.*
- **Re-deploying after activation-affecting home changes.** When a
  CriomOS-home commit changes activation behavior (new module, new
  service, new home.activation hook), run `HomeOnly Activate` against
  the local node to make the change live. Don't leave the user with a
  green commit and a stale generation.
- **Re-deploying after CriomOS-home flake-input bumps.** Same shape as
  the previous: if the input bump is the *whole* point of the change,
  the deploy is part of the change.

If something goes wrong mid-procedure (build failure, signature
rejection, etc.), surface that — the obstacle is the question, not
whether to proceed. The rule above is about *the standard happy path
following from the work just done*, not about pushing through real
errors silently.

---

## Runtime interfaces

The system specialist gives the user working interfaces, not just packages:

- keybindings that work in Niri;
- visible status for long-running actions;
- user services that restart through Home Manager activation;
- recovery paths for fragile desktop input;
- logs that expose operational state without leaking private content.

For STT prompts and likely transcription mistakes, read this workspace's
`skills/stt-interpreter.md`.

---

## Working with role assistants

There is no generic assistant role. `system-assistant` is the
system-shaped lane: bounded module slices in CriomOS or
CriomOS-home, focused audits of system-specialist commits,
self-contained host-tool work (Whisrs packaging, Clavifaber
typed-record additions, chroma instrumentation), Nix-discipline
hygiene passes, or repo-local doc updates after a shipped
system-specialist change. See this workspace's
`skills/system-assistant.md`. `operator-assistant` can take
bounded implementation-adjacent support when the scope is
operator-shaped: a narrow code fix, test backfill, or dependency
audit in an implementation repo. `designer-assistant` can take
bounded design-adjacent support: report inventory, cross-reference
cleanup, or protocol/skill edits already decided by designer.
`poet-assistant` can take prose or publishing-support work when the
surface is poet-shaped.

System-specialist deployment authority — cluster Nix signing,
signing-key generation, deploy-graph topology, host activation
orchestration — stays with this role. Role assistants read this
skill and the target repo's `skills.md` before claiming, then
report under their own role subdirectory.

---

## Operator interface — Nota only

Cluster deploy requests flow through `lojix-cli` and the operator
surface is exactly one Nota record. The CLI takes no flags and no
subcommands. New deploy behavior lands as a typed positional field
on `FullOs` / `OsOnly` / `HomeOnly` in
`lojix-cli/src/request.rs`, never as a flag, env-var dispatch, or
custom argv parser. The Nota record IS the operator's surface and
the audit trail.

The same shape applies cluster-wide: cluster proposals
(`goldragon/datom.nota`), horizon projections, and any future
operator-facing data live as typed Nota records read by
`nota-codec`. New fields are positional in source-declaration
order; reordering or renaming is a breaking change.

See lojix-cli's `skills.md` for the per-repo specifics.

---

## Cluster Nix signing

CriomOS today wires *daemon-attached* Nix signing only on **cache
nodes** (`isNixCache = true`): `services.nix-serve.secretKeyFile`
in CriomOS's `modules/nixos/nix.nix`. Non-cache nodes have no
`nix.settings.secret-key-files` and no signing private key on
disk. Paths they build are `ultimate`-trusted locally but carry
no transferable signature.

Trust direction is wired correctly: every node's
`trusted-public-keys` is rolled up from datom by horizon-rs
(`lib/src/horizon.rs`, filter on `nix_pub_key_line`).

How signed paths actually flow: **only `nix-serve` signs**, and
it signs only over HTTP at request time. Direct
nix-daemon-to-nix-daemon transfer over `ssh-ng` carries whatever
signatures the source path already has — locally built paths on
non-cache nodes have none.

To bridge that gap, `lojix-cli/src/copy.rs` always passes
`--substitute-on-destination` to `nix copy`. The target prefers
substituting each path from its own substituters (the cluster
HTTP cache) over receiving the raw path from the source. When
the cache has the closure, the target gets it signed and
verified; when the cache misses, the copy falls back to the
unsigned ssh-ng path and fails.

**Practical consequence**: deploys must route the build through
a cache node so the cache has the closure to serve. Use
`builder = <cache-node>` in the Nota request — e.g.
`(FullOs goldragon zeus … Switch prometheus)`. The cache builds,
nix-serve signs on serve, the target substitutes signed.
**`builder = None` is broken** for cross-host deploys: the
dispatcher builds locally, nothing in the cluster has the
closure, substitution misses, ssh-ng fallback delivers unsigned
paths, target rejects.

**Diagnostics**:

- Local sig: `nix path-info --sigs <path>` — `ultimate` without
  a `Sig:` means unsigned local build.
- Cache sig: `curl http://nix.<cache>.<cluster>.criome/<storehash>.narinfo`
  and read the `Sig:` line.
- Reproduce push failure:
  `nix copy --to ssh-ng://root@<target> <path>`.
- Confirm fix:
  `nix copy --substitute-on-destination --to ssh-ng://root@<target> <path>` —
  if the cache has the path, you'll see lines like
  `copying path '…' from 'http://nix.<cache>.<cluster>.criome'`
  and zeus accepting.

**Generating per-node signing keys** (the procedure the user
asked for, partially landed): on each host, generate at
`/etc/nix/secret-key`:

```sh
ssh root@<host> '
  nix-store --generate-binary-cache-key <host>.<cluster>.criome \
    /etc/nix/secret-key /etc/nix/secret-key.pub &&
  chmod 400 /etc/nix/secret-key &&
  chmod 444 /etc/nix/secret-key.pub
'
```

Then read `/etc/nix/secret-key.pub` and replace the matching
node's `NodePubKeys.nix` field in `goldragon/datom.nota`. Push
goldragon. Redeploy each updated host so its trust list reflects
the new pubkeys (use `builder = prometheus` for the redeploys
because non-cache nodes still don't sign).

The keys are *inert* until CriomOS wires
`nix.settings.secret-key-files` in `modules/nixos/nix.nix` —
that's the still-pending architectural fix that would let
non-cache nodes' daemons sign locally-built paths and let
`builder = None` deploys produce verifiable closures.

---

## See also

- CriomOS's `skills.md`
- CriomOS-home's `skills.md`
- this workspace's `skills/stt-interpreter.md`
- this workspace's `skills/autonomous-agent.md`
- this workspace's `skills/system-assistant.md`
- this workspace's `skills/operator-assistant.md`
- this workspace's `skills/designer-assistant.md`
- this workspace's `skills/poet-assistant.md`
- lore's `AGENTS.md`
