# Skill — Nix usage

*Daily Nix command shapes, builder checks, and store-path hygiene.*

---

## What this skill is for

Use this skill when running Nix commands in the workspace: inspecting daemon
configuration, forcing a build through the remote builder, capturing build
outputs, or deciding which command surface is evidence.

This skill is operational. For flake-input forms, lock-file pinning,
`git+file://` avoidance, missing tools, and test-runner discipline, read this
workspace's `skills/nix-discipline.md`. For CriomOS deployment and host-module
rules, read CriomOS's `skills.md`.

---

## Inspect the active Nix configuration

Use Nix to ask Nix what the daemon sees:

```sh
nix config show | rg '^(builders|builders-use-substitutes|max-jobs|substituters|trusted-public-keys|trusted-users)'
```

`builders = @/etc/nix/machines` means the daemon reads its remote builder list
from `/etc/nix/machines`. Inspect that file directly when you need the machine
line:

```sh
sed -n '1,120p' /etc/nix/machines
```

Do not search the Nix store for configuration. If a value is Nix-controlled,
inspect the source checkout, evaluate the option, or ask the Nix daemon.

---

## Remote builder smoke test

The active host configuration exposes the remote builder through the Nix
daemon: `builders = @/etc/nix/machines`, with
`builders-use-substitutes = true`. The current machine entry is the
`ssh-ng://nix-ssh@prometheus.goldragon.criome` builder for `x86_64-linux`,
declared in `/etc/nix/machines`.

To force a build onto the remote builder, set local build slots to zero on the
command:

```sh
result=$(nix build <installable> --no-link --print-build-logs \
  --option max-jobs 0 \
  --option builders '@/etc/nix/machines' \
  --print-out-paths)
```

Use `--rebuild` or an uncached small derivation when the goal is to prove the
builder path instead of accepting a substitute. The success witness is Nix's
own build log: it says the derivation is building on
`ssh-ng://nix-ssh@prometheus.goldragon.criome`, then copying the result from
that same store.

`max-jobs = 0` is a per-command remote-only lever. Keep the daemon's normal
default unless the host should never perform local builds. With
`max-jobs = 0`, a build that cannot reach any configured remote builder fails
instead of falling back to local work.

Use daemon-scheduled `nix build` as the smoke test. A direct user-shell probe
such as `ssh nix-ssh@prometheus.goldragon.criome` or
`nix store info --store ssh-ng://nix-ssh@prometheus.goldragon.criome` checks
the caller's SSH credentials, not necessarily the daemon's machine entry, and
can fail even while remote builds work.

---

## Store paths stay in variables

When a command returns a store path, keep it in a shell variable:

```sh
result=$(nix build <installable> --no-link --print-out-paths)
ls "$result"
```

Do not paste raw store paths into chat, reports, skills, commit messages, or
architecture docs. Store hashes drift on rebuild; prose that freezes a path
becomes stale immediately.

---

## Which command is evidence

- Use `nix build` when the build result or closure is the evidence.
- Use `nix flake check` when a repo's pure test suite is the evidence.
- Use `nix run .#<app>` when the repo exposes a stateful runner or one-shot
  tool as an app.
- Use `nix run nixpkgs#<package> -- <arguments>` when a tool is missing from
  `PATH`.

A direct build of a CriomOS `nixosConfigurations.target` without
lojix-projected inputs is not a real deployment check. For that path, use
lojix and the target repo's skill. CriomOS's `skills.md` carries the
network-neutral module and deploy rules.

---

## See also

- this workspace's `skills/nix-discipline.md` — flake inputs, lock discipline,
  missing tools, and `nix flake check`.
- this workspace's `skills/testing.md` — Nix-backed test surfaces.
- CriomOS's `skills.md` — host deployment and NixOS module rules.
- lore's `nix/basic-usage.md`, `nix/flakes.md`, and
  `nix/integration-tests.md` — Nix CLI references.
