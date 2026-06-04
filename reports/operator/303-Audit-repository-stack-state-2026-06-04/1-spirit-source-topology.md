---
title: 1 — Spirit source topology
role: operator
variant: Audit
date: 2026-06-04
topics: [spirit, source-topology, deployment, contracts, pins]
description: |
  Audit of the current Spirit source topology, production and next
  deployment bindings, Spirit contract repos, CriomOS-home pins, and
  version/skew risks for the operator repository stack state audit.
---

# 1 — Spirit source topology

## Headline Findings

Spirit is split, but not as one source tree divided across two repos. It is
two parallel implementations plus a successor scaffold:

- Production today is `persona-spirit` at
  `/git/github.com/LiGoldragon/persona-spirit`, deployed through
  `CriomOS-home` as versioned `persona-spirit` slots. The unsuffixed
  `spirit` command points at the `v0.3.0` slot.
- The separate `/git/github.com/LiGoldragon/spirit-next` repo is the active
  schema-derived runnable pilot. It is intentionally separate from production
  so operators can iterate without disturbing intent capture.
- The `/git/github.com/LiGoldragon/spirit` repo and its
  `signal-spirit` / `core-signal-spirit` contracts are a schema-driven
  successor scaffold from the persona-prefix-retirement line. They are not
  what production or the installed `spirit-next` slot use today.

The most important naming trap: the installed `spirit-next` command is not
built from the separate `spirit-next` repo. `CriomOS-home` wires it from the
`persona-spirit-next` flake input, and that input currently points at
`github:LiGoldragon/persona-spirit?ref=main`.

## Production Today

Production intent capture uses the `persona-spirit` v0.3.0 deployment:

- `CriomOS-home` pins `persona-spirit-v0-3-0` to
  `persona-spirit` revision
  `df09280a464f8a7be1c20ff433de4bfc4afc7f53`.
- `modules/home/profiles/min/spirit.nix` defaults
  `criomosHome.personaSpirit.currentDefault` to `v0.3.0`.
- The user profile's unsuffixed `spirit` wrapper resolves to the
  `spirit-v0.3.0` wrapper and exports sockets under
  `/home/li/.local/state/persona-spirit/v0.3.0/`.
- The running `persona-spirit-daemon-v0.3.0.service` starts
  `persona-spirit-daemon` with a single NOTA configuration argument naming
  the v0.3.0 ordinary socket, owner socket, upgrade socket, and redb path.

At that pinned `persona-spirit` revision, production ordinary Spirit depends
on `signal-persona-spirit` revision
`4c7b51ff56a90c2838c4a3475fb219a8b43cc12f`. The owner/control contract pin is
`owner-signal-persona-spirit` revision
`cf932a619e1f6f3afc80cb62b6c0da6460e1c1f0`.

## What `spirit-next` Uses Today

There are two surfaces named `spirit-next`:

- Installed slot: `~/.nix-profile/bin/spirit-next` is the side-by-side
  `persona-spirit` next slot. It uses `PERSONA_SPIRIT_NEXT_SOCKET` and
  `PERSONA_SPIRIT_NEXT_OWNER_SOCKET`, talks to
  `persona-spirit-daemon-next.service`, and stores state under
  `/home/li/.local/state/persona-spirit/next/`.
- Separate repo: `/git/github.com/LiGoldragon/spirit-next` is a schema-derived
  pilot crate with `spirit-next` and `spirit-next-daemon` binaries. It uses
  `schema/lib.schema -> schema/lib.asschema -> src/schema/lib.rs`, build deps
  `schema-next` and `schema-rust-next`, optional `nota-next` for the CLI text
  surface, and optional `triad-runtime` for testing trace.

The separate `spirit-next` repo does not depend on `signal-persona-spirit`,
`owner-signal-persona-spirit`, `signal-spirit`, or `core-signal-spirit` today.
Its `Cargo.lock` pins:

- `schema-next` `711b5fc9fe8809336c7fc54d90c1aa40cf614cc6`
- `schema-rust-next` `a789a85e71b0c7b60402ca68c5ac553d6ca65a5c`
- `triad-runtime` `2b51462fef72540610de0df3f1f0c7ccebc4b653`
- `nota-next` `b33b5b51ce10aa7f44027b7290bfe008c90e7ce5`

## Contract Repo State

Current concrete repos:

- `/git/github.com/LiGoldragon/signal-persona-spirit` — active production
  ordinary Spirit contract. Production pins `4c7b51ff...`; current checkout
  main is ahead at `a69769b...` (`add removal candidate collection`).
- `/git/github.com/LiGoldragon/owner-signal-persona-spirit` — active
  production owner/control contract. Production pins `cf932a...`.
- `/git/github.com/LiGoldragon/signal-spirit` — schema-driven successor
  ordinary contract for the renamed `spirit` component. Not used by
  `CriomOS-home`, production `persona-spirit`, or the separate `spirit-next`
  pilot today. The only dependency found is `/git/.../spirit/Cargo.lock` on
  branch `designer-running-concept-2026-05-26` at `ad8272ff...`.
- `/git/github.com/LiGoldragon/core-signal-spirit` — schema-driven successor
  privileged/control contract scaffold. Not used by production today.
- `/git/github.com/LiGoldragon/spirit` — schema-driven successor component
  repo. Its own docs say `persona-spirit` continues to carry v0.3 production
  until feature parity arrives. It is not pinned by `CriomOS-home`.

No local checkout exists for `/git/github.com/LiGoldragon/owner-signal-spirit`
or `/git/github.com/LiGoldragon/meta-signal-spirit`.

## Version And Skew Risks

1. Wrapper-name skew: `spirit-next` in the profile means
   `persona-spirit`'s next slot, not the separate `spirit-next` repo. A deploy
   audit that assumes otherwise will inspect the wrong source.

2. Production-vs-checkout skew: production pins `persona-spirit` at
   `df09280a...` and `signal-persona-spirit` at `4c7b51ff...`, while the local
   `persona-spirit` checkout has uncommitted changes and the local
   `signal-persona-spirit` checkout is ahead at `a69769b...`. Read deployed
   wire shape from the pinned revision, not from the working checkout.

3. Cross-consumer contract skew: `persona` and `upgrade` currently lock
   different `signal-persona-spirit` revisions (`60394925...` and
   `2073d2fd...`) than production Spirit (`4c7b51ff...`) and current main
   (`a69769b...`). Any live cross-component call path must identify which
   contract revision it compiled against.

4. Contract-split skew: active design points toward moving Signal types into
   `signal-spirit`, but the separate `spirit-next` pilot currently owns its
   Signal/Nexus/SEMA roots inside `schema/lib.schema`. Treat `signal-spirit`
   as pre-cutover until that dependency is actually wired.

5. State-slot skew: `spirit` and installed `spirit-next` use separate sockets
   and separate redb files. Capturing through one does not write the other's
   database. Normal agent intent capture should continue through unsuffixed
   `spirit` unless explicitly testing a side slot.

## Command Evidence

Repository existence and absent owner/meta variants:

```sh
find /git/github.com/LiGoldragon -maxdepth 1 -mindepth 1 -printf '%y %f\n' \
  | sort \
  | rg '(^d signal-persona-spirit$|^d owner-signal-persona-spirit$|^d signal-spirit$|^d core-signal-spirit$|^d spirit$|^d spirit-next$|meta-signal-spirit|owner-signal-spirit)'
```

Output:

```text
d core-signal-spirit
d owner-signal-persona-spirit
d signal-persona-spirit
d signal-spirit
d spirit
d spirit-next
```

Active repository map:

```text
/home/li/primary/protocols/active-repositories.md:37-40
schema-next, schema-rust-next, triad-runtime, and spirit-next are active
schema-derived stack repos. The active map names spirit-next, not spirit.
```

CriomOS-home pin and default:

```text
/git/github.com/LiGoldragon/CriomOS-home/flake.nix:144
persona-spirit-v0-3-0.url =
  "github:LiGoldragon/persona-spirit?rev=df09280a464f8a7be1c20ff433de4bfc4afc7f53";

/git/github.com/LiGoldragon/CriomOS-home/flake.nix:146
persona-spirit-next.url = "github:LiGoldragon/persona-spirit?ref=main";

/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix:175-178
currentDefault default = "v0.3.0";
```

Locked inputs:

```sh
jq -r '.nodes | to_entries[] |
  select(.key|test("persona-spirit-(v0-1-0|v0-1-1|v0-2-0|v0-3-0|next)$")) |
  [.key, .value.locked.repo, .value.original.ref // .value.original.rev // "", .value.locked.rev] |
  @tsv' /git/github.com/LiGoldragon/CriomOS-home/flake.lock
```

Relevant output:

```text
persona-spirit-next   persona-spirit   main       df09280a464f8a7be1c20ff433de4bfc4afc7f53
persona-spirit-v0-3-0 persona-spirit   df09280... df09280a464f8a7be1c20ff433de4bfc4afc7f53
```

Profile wrappers:

```sh
readlink -f "$(command -v spirit)"
readlink -f "$(command -v spirit-next)"
```

Output:

```text
/nix/store/n0pi3ahjv5s766lnxyvv0z7qyvy7aaw8-spirit-v0.3.0/bin/spirit-v0.3.0
/nix/store/y43j833yc5jpr5r5kwkjavkj5mb5raap-spirit-next/bin/spirit-next
```

Wrapper contents:

```text
spirit wrapper exports:
PERSONA_SPIRIT_SOCKET=/home/li/.local/state/persona-spirit/v0.3.0/spirit.sock
PERSONA_SPIRIT_OWNER_SOCKET=/home/li/.local/state/persona-spirit/v0.3.0/owner.sock

spirit-next wrapper exports:
PERSONA_SPIRIT_NEXT_SOCKET=/home/li/.local/state/persona-spirit/next/spirit.sock
PERSONA_SPIRIT_NEXT_OWNER_SOCKET=/home/li/.local/state/persona-spirit/next/owner.sock
```

Running services:

```sh
systemctl --user --no-pager --plain list-units 'persona-spirit-daemon*'
```

Relevant output:

```text
persona-spirit-daemon-next.service   loaded active running
persona-spirit-daemon-v0.3.0.service loaded active running
```

Generated start scripts:

```text
persona-spirit-daemon-v0.3.0:
exec .../persona-spirit-daemon '([/home/li/.local/state/persona-spirit/v0.3.0/spirit.sock] [/home/li/.local/state/persona-spirit/v0.3.0/owner.sock] [/home/li/.local/state/persona-spirit/v0.3.0/upgrade.sock] [/home/li/.local/state/persona-spirit/v0.3.0/persona-spirit.redb] 384 None None None None)'

persona-spirit-daemon-next:
exec .../persona-spirit-daemon '([/home/li/.local/state/persona-spirit/next/spirit.sock] [/home/li/.local/state/persona-spirit/next/owner.sock] [/home/li/.local/state/persona-spirit/next/upgrade.sock] [/home/li/.local/state/persona-spirit/next/persona-spirit.redb] 384 None None None None)'
```

Production nested Cargo pins from the pinned `persona-spirit` revision:

```sh
jj -R /git/github.com/LiGoldragon/persona-spirit \
  file show -r df09280a464f8a7be1c20ff433de4bfc4afc7f53 root:Cargo.lock \
  | rg -n 'signal-persona-spirit|owner-signal-persona-spirit'
```

Relevant output:

```text
548:name = "owner-signal-persona-spirit"
550:source = "git+https://github.com/LiGoldragon/owner-signal-persona-spirit.git?branch=main#cf932a619e1f6f3afc80cb62b6c0da6460e1c1f0"
1122:name = "signal-persona-spirit"
1124:source = "git+https://github.com/LiGoldragon/signal-persona-spirit.git?branch=main#4c7b51ff56a90c2838c4a3475fb219a8b43cc12f"
```

Separate `spirit-next` repo dependency pins:

```sh
rg -n 'schema-next|schema-rust-next|triad-runtime|nota-next' \
  /git/github.com/LiGoldragon/spirit-next/Cargo.toml \
  /git/github.com/LiGoldragon/spirit-next/Cargo.lock
```

Relevant output:

```text
Cargo.toml:45: nota-next = ... optional = true
Cargo.toml:49: triad-runtime = ... optional = true
Cargo.toml:52: schema-next = ...
Cargo.toml:53: schema-rust-next = ...
Cargo.lock:451: schema-next ... #711b5fc9fe8809336c7fc54d90c1aa40cf614cc6
Cargo.lock:461: schema-rust-next ... #a789a85e71b0c7b60402ca68c5ac553d6ca65a5c
Cargo.lock:608: triad-runtime ... #2b51462fef72540610de0df3f1f0c7ccebc4b653
Cargo.lock:290: nota-next ... #b33b5b51ce10aa7f44027b7290bfe008c90e7ce5
```

No `spirit-next` repo pin in CriomOS-home:

```sh
rg -n 'LiGoldragon/spirit-next|spirit-next\.url|repo": "spirit-next"' \
  /git/github.com/LiGoldragon/CriomOS-home/flake.nix \
  /git/github.com/LiGoldragon/CriomOS-home/flake.lock
```

Output contains no `LiGoldragon/spirit-next` match; the only relevant line is
`persona-spirit-next.url = "github:LiGoldragon/persona-spirit?ref=main"`.

Working-copy caution:

```sh
jj -R /git/github.com/LiGoldragon/persona-spirit st --no-pager
```

Relevant output:

```text
Working copy changes:
A src/argument.rs
M src/daemon.rs
M src/lib.rs
M src/migration.rs
Working copy  (@) : xqusozwm 52261680 (no description set)
Parent commit (@-): rpokknqm 7233075c main | persona-spirit: collect removal candidates
```

I did not modify, revert, commit, or push any repository checkout.
