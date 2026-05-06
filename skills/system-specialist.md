# Skill — system specialist

*Maintaining the operating-system layer underneath the workspace.*

---

## What this skill is for

Use this skill when the work is about making the operator's system run:
CriomOS, CriomOS-home, lojix deployment, horizon projection, desktop
runtime, user services, input devices, Niri, Noctalia, and system/home
interfaces.

The system specialist is a capability, not a primary-workspace lock role.
Do not claim the `operator` role merely because this skill is active. Follow
whatever coordination protocol the current workspace uses, but keep the
concept separate: this skill is about OS/platform work.

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

Secrets stay out of Nix and broad process environments. For paid cloud
inference, follow the repo rule: local model first, then ask before using a
paid key unless the user explicitly authorized that call in the current task.

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

CriomOS today wires Nix signing only on **cache nodes**
(`isNixCache = true`): `services.nix-serve.secretKeyFile` in
CriomOS's `modules/nixos/nix.nix`. Non-cache nodes have no
`nix.settings.secret-key-files` and no signing private key on
disk. Paths they build are `ultimate`-trusted locally but carry
no transferable signature.

Trust direction is wired correctly: every node's
`trusted-public-keys` is rolled up from datom by horizon-rs
(`lib/src/horizon.rs`, filter on `nix_pub_key_line`).

The asymmetry: pubkeys are declared in datom for several nodes
(ouranos, prometheus, tiger), but only the cache node has a
matching secret on disk. A pubkey in datom for a non-cache node
is **phantom** — declared trust, no real signing capability.

**Symptom**: `lojix-cli (FullOs … Switch None)` builds on the
dispatcher, then `nix copy --to ssh-ng://<target>` fails with
"cannot add path X because it lacks a signature by a trusted
key."

**Diagnostics**:

- Local sig: `nix path-info --sigs <path>` — `ultimate`
  without a `Sig:` means unsigned local build.
- Cache sig: `curl http://nix.<cache>.<cluster>.criome/<storehash>.narinfo`
  and read the `Sig:` line.
- Reproduce push failure: `nix copy --to ssh-ng://root@<target> <path>`.

**Workarounds, in increasing scope**:

- Pull from cache before copy: `nix copy --from
  http://nix.<cache>.<cluster>.criome <path>` on the dispatcher.
  Replaces the unsigned local copy with a signed one. Only
  works when the cache has the closure.
- Build on a signing node: set `builder = <cache>` in the Nota
  request.
- `--no-check-sigs` on copy. Last resort; weakens cluster trust.

**Real fix (not yet landed)**: wire
`nix.settings.secret-key-files` per node in `nix.nix`, generate
real keypairs, store secrets durably, and update datom with real
pubkeys. New pubkeys propagate to every node's trust list on
next deploy.

---

## See also

- CriomOS's `skills.md`
- CriomOS-home's `skills.md`
- this workspace's `skills/stt-interpreter.md`
- this workspace's `skills/autonomous-agent.md`
- lore's `AGENTS.md`
