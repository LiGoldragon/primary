---
title: 515 — SignalRuntime resolves the no-emission-home blocker; "signal schema" means two files
role: designer
variant: Psyche
date: 2026-06-04
topics: [runtime, signal, nexus, sema, schema-rust-next, spirit, component-triad, port-readiness, boundary]
description: |
  The report-514 blocker (three-plane split emits no SignalEngine) is
  resolved by a fifth emission target, SignalRuntime, on the daemon's
  OWN signal.schema — not by report 514's A or B. The key correction:
  "signal schema" names two distinct files (public WireContract contract
  vs daemon-local SignalRuntime runtime). Verified workspace-wide: spirit
  builds clean, engine-complete, boundary clean, no other component blocked.
---

# 515 — SignalRuntime resolves the blocker; "signal schema" means two files

## What this report settles

Report 514 witnessed a real blocker: the three-plane split
(`WireContract` signal + `NexusRuntime` + `SemaRuntime`), once the
all-in-one `ComponentRuntime` module was removed, emitted **no
`SignalEngine`** — so a daemon that implements `SignalEngine` could not
leave `ComponentRuntime`. That report weighed two resolutions, (A)
make `NexusRuntime` also emit signal, and (B) make the runner absorb
triage so the `SignalEngine` trait retires, and it leaned (B).

**Both were wrong-framed.** The operator landed a third option — **(C)
a separate daemon-local `SignalRuntime` emission target** — and it is
the right one. This report records the resolution, the conceptual
correction underneath it (why 514 could not see C), and the
workspace-wide verification that C is complete and the contract/daemon
boundary is clean everywhere.

## The resolution — `RustEmissionTarget::SignalRuntime`

`schema-rust-next` now has **five** emission targets, not four
(`src/lib.rs:294-321`):

| Target | `runtime_planes()` | Emits |
|---|---|---|
| `WireContract` | `none()` | Wire vocabulary + codecs only — zero engines |
| `ComponentRuntime` | `all()` | All three engines (legacy all-in-one) |
| **`SignalRuntime`** | **`signal_only()`** | **Wire vocab + `SignalEngine`** |
| `NexusRuntime` | `nexus_only()` | `NexusEngine` |
| `SemaRuntime` | `sema_only()` | `SemaEngine` |

A daemon now does the three-plane split with three runtime targets and
no all-in-one: `signal.schema → SignalRuntime`,
`nexus.schema → NexusRuntime`, `sema.schema → SemaRuntime`. The
generator change is one helper, `ModuleEmission::signal_runtime_module`
(`schema-rust-next/src/build.rs:145`); spirit's `build.rs:31-34` now
calls `signal_runtime_module("signal") + nexus_runtime() +
sema_runtime()`, having dropped `wire_contract_module("signal")` and
`ComponentRuntime` entirely.

## The conceptual correction — "signal schema" is two different files

This is the load-bearing lesson, and the reason report 514 could only
see A and B. The word "signal schema" was doing double duty:

1. **The public signal contract** — `signal-<component>/schema/…`, a
   *separate repo*, emitting to **`WireContract`**: wire vocabulary +
   codecs only, zero engines. This is what peers link against. (For
   spirit: `signal-spirit/schema/signal-spirit.schema`, still on the
   legacy `RustEmitter` path, engine-free.)

2. **The daemon-local signal runtime** — `<component>/schema/signal.schema`,
   a *different file inside the daemon crate*, beside `nexus.schema`
   and `sema.schema`, emitting to **`SignalRuntime`**: the same wire
   shape PLUS the `SignalEngine` trait (admission / triage / reply) the
   daemon implements.

Same word, different files, different emission targets, different jobs.
Report 514 collapsed them, so its question "which plane emits
`SignalEngine`?" had only two visible answers — fold it into Nexus (A)
or delete it (B). Once the two meanings are kept apart, (C) is obvious:
the daemon's signal *runtime* schema emits the engine; the public
signal *contract* never does. A daemon's `SignalEngine` is generated
from its OWN `signal.schema`, never from the contract.

This distinction was already stated at the source of truth —
`schema-rust-next/src/lib.rs:216-225` says verbatim: "New signal and
meta-signal contract repos should opt into `RustEmissionTarget::WireContract`.
Daemon-local signal runtime schemas should opt into
`RustEmissionTarget::SignalRuntime`." The defect was only that the
workspace triad skill never propagated it. Now fixed:
`skills/component-triad.md` §"'Signal' names two different schema files"
+ the repo-layout block + the Runtime-triad Signal section.

## Why C beats my (B) lean — plane honesty

I retract 514's lean toward (B). (B) — runner absorbs triage, the
`SignalEngine` trait retires — dissolves a typed plane seam into a
generic runner. (C) keeps `SignalEngine` a generated, plane-local trait
the daemon implements, exactly parallel to `NexusEngine` and
`SemaEngine`. Each of the three planes emits exactly one engine bound
to exactly one daemon actor:

| Plane | Engine trait | Daemon actor |
|---|---|---|
| Signal | `SignalEngine` (`spirit/src/schema/signal.rs:1156`) | `SignalActor` (`impl` at `engine.rs:209`) |
| Nexus | `NexusEngine` (`schema/nexus.rs:712`) | `Nexus` (`impl` at `nexus.rs:153`) |
| SEMA | `SemaEngine` (`schema/sema.rs:692`) | `Store` (`impl` at `store.rs:51`) |

That symmetry is the more plane-honest design. (B) may still be a
*later* cleanup if the runner ever subsumes wire ingress generically,
but it was too coupled to do as part of the split, and `SignalRuntime`
made it unnecessary.

## Verified — workspace-wide, not just spirit

Three parallel recon agents (designer workflow, 2026-06-04):

- **Build clean + engine-complete.** `cd spirit && cargo check` exits
  0 ("Finished dev profile"). All three engine traits present, each
  generated by its plane's runtime target, each implemented for a
  distinct actor (table above). `spirit/schema/` holds only
  signal/nexus/sema (`.schema` + `.asschema`); no `lib.schema`; no
  `ComponentRuntime` reference anywhere in `build.rs`/`lib.rs`.

- **Boundary clean across every contract.** `signal-spirit` generated
  output has `grep -c Engine == 0` (the only "Engine" token is
  `SchemaEngine`, the build-time lowering compiler — not a runtime
  engine). The full contract population — `signal-spirit`,
  `signal-cloud`, `signal-upgrade`, `signal-domain-criome`,
  `meta-signal-cloud`, `meta-signal-upgrade`, `meta-signal-domain-criome`
  — all emit wire vocab only, zero engines. **No leaks workspace-wide.**

- **No other component blocked.** Every daemon component is already off
  the all-in-one: `spirit` (signal+nexus+sema), `cloud` and
  `domain-criome` (nexus+sema). `upgrade` is a standalone non-daemon
  utility still on `ComponentRuntime`, which is fine — it is not a
  component that needs the resolution.

## My `spirit-plane-split` branch is superseded

The branch at `~/wt/.../spirit/spirit-plane-split` used
`wire_contract_module("signal")` — `WireContract` for the daemon's own
signal schema. That is precisely the bug 514 diagnosed: a daemon emits
no `SignalEngine` if its signal schema is `WireContract`. The operator's
main used `signal_runtime_module("signal")` (`SignalRuntime`) and is
correct and landed. My branch should be abandoned, not integrated; it
was the symptom, not a candidate fix.

## Two small open items (not blockers)

1. **Code-repo ARCHITECTURE silent-gaps.** `spirit/ARCHITECTURE.md`
   (§Runtime triad) and `signal-spirit/ARCHITECTURE.md` (§Role)
   describe the Signal plane / signal contract but do not name the
   `SignalRuntime` / `WireContract` targets. These are operator-owned
   code-repo main files; recommend the operator (or a designer `next`
   branch) add the target names so each repo's own doc carries the
   distinction. The workspace skill now does.

2. **cloud / domain-criome have no daemon-local signal plane** (they
   split as nexus+sema only). Worth confirming this is intentional —
   how do those daemons receive and triage inbound signals if they
   emit no `SignalEngine`? Either they front on a shared signal
   mechanism, or their signal handling predates the split. Flagging as
   an observation to verify, not a conclusion; it does not affect the
   spirit resolution.

## Bottom line

The blocker is resolved, verified live, and clean workspace-wide. The
durable lesson — keep "the signal schema" as two distinct files
(`WireContract` contract vs `SignalRuntime` daemon runtime) — is now in
the triad skill. Report 514 stands as the bug witness with a
supersession note pointing here.
