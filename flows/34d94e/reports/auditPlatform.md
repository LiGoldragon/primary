# Platform source audit — 2026-09-14

This is a bounded read-only audit of the current checked-out sources and one
read-only unit-status query. It does not establish that a source pin is what a
running machine uses, except where stated under Runtime observation.

## Direction and applicability

The authored universal rule is that each newly built component is a Nexus;
the Nexus has at least ordinary and privileged meta sockets and compiled signal
contracts. [Vision/nexus.md:13-14] [Vision/nexus.md:35-39]
[Vision/nexus.md:51-57] Its default client may accept Datom text at the edge,
but it exchanges binary Signal with the Nexus. [Vision/nexus.md:41-49]

Datom is explicitly the typed textual edge form, while components speak
signal. [Vision/datom.md:14-21] This supports the current CLI pattern rather
than identifying textual CLI input as a protocol violation. Protos supplies
structure, not dialect meaning; Datom, Ethos and future Nomos/Logos ride that
substrate. [Vision/protos.md:5-12] [Vision/protos.md:16-23]

Ethos declares types and Datom supplies values. [Vision/ethos.md:5-6]
Ethos roots include Signal and Sema, which respectively name a Nexus's main
types and storage types. [Vision/ethos.md:18-21] Intent requires context to
stay at its own layer and identifies Datom and Ethos Zero as parts that must
be solid. [Intent/context.md:3-6] [Intent/anatomy.md:3-7]

The living direction dated 2026-09-13 is that Criome should become Lojix's
deployment-authentication layer for the root call which activates a host.
[flows/024bc7/vision/criome.md:3-10] The same date records a request for a
Nexus capable of the relay attachments and says no Python. This is a direction
for the attachment work; it does not itself prove that every small stopgap is
forbidden. [flows/6cc91b/vision/nexus.md:3-9]

## What exists in source

### CriomOS and Criome

CriomOS declares itself as a NixOS platform parameterized by Lojix-produced
system, package, Horizon, and deployment inputs. [CriomOS/flake.nix:1-2]
It pins inputs for Orchestrate, router, Criome, and Lojix; comments identify
the router's Criome-attestation/node-identity path and Criome as a BLS
attestation daemon. [CriomOS/flake.nix:30-33] [CriomOS/flake.nix:73-86]

The Criome NixOS module declares a working socket and an owner-only meta socket
and documents `ObserveNodePublicKey` and `AcceptRootFounding`; it keeps the
master key out of the Nix store. [CriomOS/modules/nixos/criome.nix:16-30]
It also documents a persistent Sema store and a clean-genesis requirement for
the v5 parent-bearing contract. [CriomOS/modules/nixos/criome.nix:45-52]
This is source/declarative configuration evidence, not a witnessed founding or
Criome-authorized Lojix deploy.

### Lojix

The Lojix module runs `lojix-nexus`, leaves its configuration to the Nexus,
and derives Sema and ordinary/meta socket paths from the service state/runtime
paths. [CriomOS/modules/nixos/lojix.nix:22-29]
[CriomOS/modules/nixos/lojix.nix:92-110] The ordinary Lojix client actualizes
one Datom query, signalizes it, exchanges bytes over its configured socket,
and restores the typed response. [lojix/clients/ordinary/src/lib.rs:43-65]

Lojix's flake defines Cargo tests, a fresh-daemon startup test, failure
evidence, and a NixOS same-host test activation. [lojix/flake.nix:169-199]
The latter uses a real Lojix daemon and both sockets while Nix/SSH are fake
effect boundaries. [lojix/flake.nix:286-290] Its fixture waits for both
sockets and drives a meta `Deploy.Host` request. [lojix/flake.nix:361-384]
These are declared test coverage; this audit did not execute them.

### Orchestrate

Orchestrate's ordinary CLI parses inline Datom with a bounded reader, then
signalizes the typed query and restores a typed response from socket bytes.
[orchestrate/crates/orchestrate/src/main.rs:73-107] Its process fixture uses a
Unix listener and the shared `signal` framing crate, then proves both a typed
Datom request/response and malformed-input failure. [orchestrate/crates/orchestrate/tests/client.rs:1-33]
[orchestrate/crates/orchestrate/tests/client.rs:66-96]

Its flake declares workspace, live-Nexus, lock-contract, configuration,
authority, socket, relocation, stopping, and client test checks.
[orchestrate/flake.nix:80-180] Vision says it must be unconditionally deployed
for every home user with its meta binary. [Vision/orchestrate.md:3-7]

### Protos, Datom, and Ethos Zero

Protos assigns extent to syntax and path to Datom, while a reader carries the
budget; it defines the explicit conversion chain from text through Protos and
Datom to a composition. [Vision/protos.md:53-61] [Vision/protos.md:63-87]
The Datom source has Nix Cargo-test checks. [datom/flake.nix:30-32]

Ethos Zero documents the implemented pipeline: canonical text → Protos →
checked `File` → generated Rust, and says signal declarations gate Datom
derives so a Nexus need not depend on the text codec. [ethos-zero/src/lib.rs:1-30]
Its freshness tests compare generated Rust with committed modules and all
seventeen fixtures. [ethos-zero/tests/freshness.rs:1-29]
[ethos-zero/tests/freshness.rs:43-57] This aligns with the authored statement
that Zero is not yet a daemon/Nexus and is held fresh by a test.
[Vision/ethos.md:430-441]

## Runtime observation

At audit time, a read-only `systemctl show` found `lojix.service` loaded,
active, and running from `/etc/systemd/system/lojix.service`. `orchestrate`,
`orchestrate-nexus`, and `criome` unit names were not found. This establishes
only these local unit states. It does not reveal the configured contract pins,
stored configuration, socket health, deployment history, or Criome/Lojix
authorization behavior.

## Gaps and bounded suggestions

1. **Criome-to-Lojix authorization:** current source separately configures the
   Criome attestation service and Lojix deployment authority, but this audit
   found no direct source/test citation proving a Criome attestation is required
   and verified by Lojix before host activation. That integration remains the
   material gap against the 2026-09-13 direction.
2. **Attachment relay:** the current non-Python `tools/prompt-relay` is a
   manually invoked operational tool, not a durable Nexus with Sema, Signal,
   ordinary/meta sockets, or router edge. It is a real bounded stopgap, while
   the requested Nexus attachment capability remains unimplemented.
3. **Deployment evidence:** active local Lojix is witnessed, but no live
   Criome founding, active Criome unit, or authorized production deployment was
   observed. Do not infer those facts from Nix sources or flake test fixtures.

**Codex suggestion:** define the Criome-authenticated deployment edge as an
Ethos signal contract before implementation, including the attestation,
host/root authority, durable decision record, and observation receipt; then
add a hermetic Lojix/Criome integration test that proves refusal without a
valid attestation and success with one. Keep Datom as the client/operator text
edge and Signal as the wire format.

**Codex suggestion:** design the attachment Nexus separately from the prompt
relay stopgap. Its contract should preserve source provenance and durable
delivery state, and its deployment should only follow a living decision on
authority and placement.

## Sources

- `Vision/nexus.md`, `Vision/datom.md`, `Vision/protos.md`, `Vision/ethos.md`,
  `Vision/orchestrate.md`; authored directions read 2026-09-14.
- `Intent/context.md`, `Intent/anatomy.md`; authored directions read 2026-09-14.
- `flows/024bc7/vision/criome.md` and `flows/6cc91b/vision/nexus.md`, both
  dated 2026-09-13.
- `/git/github.com/LiGoldragon/{CriomOS,lojix,orchestrate,datom,ethos-zero}`;
  checked source revisions at audit time, not built or executed.
- Read-only `systemctl show` observation on 2026-09-14.
