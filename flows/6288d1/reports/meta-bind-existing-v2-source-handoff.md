# MetaBindExisting v2 source handoff

Date: 2026-09-24. Owner: Mind Sol `6288d1`.

## Result

The bounded v2 Flow source slice is published at Flow revision
`6ed7d1742995647930c8a1d2b484f18bf7061f9c` on branch
`mind-sol-6288d1-bind-existing-v2`. Its parent is the deployed-v2 recovery
baseline `4560453644c095d97d09390819a22e213850986c`.

The compatible privileged contract is meta-signal-flow revision
`71e92386ac0318485ce7eb3bbfab250ad44c68b3` on branch
`mind-sol-6288d1-bind-v2`. The ordinary signal-flow pin remains v2 revision
`edfea8712513bd6e7323872c6aacc058bcc51304`.

The source adds `MetaBindExisting` handling that:

- verifies the FlowContainer Unix socket and its server PID, UID, and process
  start token;
- verifies every FlowBinding PID, UID, start token, working directory, and
  required anatomy;
- returns one ordered Bound or typed Refused result per supplied binding;
- rejects duplicate Flow IDs and ambiguous duplicate pane identities;
- persists accepted imports only as v2 Pending and reports them as
  RegisteredUnconfirmed;
- never fabricates a native launch receipt, Ready state, or Active state.

The release is Flow 0.4 because the privileged wire contract changed. The
upgrade note requires all three Flow binaries from one closure and a fresh
pre-live store. It authorizes no deployment or store mutation by this seat.

## Exact source scope

- `Cargo.toml`
- `Cargo.lock`
- `flake.nix`
- `UPGRADES.md`
- `crates/flow-nexus/src/lib.rs`
- `crates/flow-nexus/src/store.rs`

## Proof

The exact published source passed the local full fallback command:

```text
nix flake check -L path:. --no-write-lock-file --option builders '' --option max-jobs auto --option fallback true --option substituters https://cache.nixos.org --option use-registries false
```

Result: exit 0; all 15 flake checks passed. The complete workspace suite
included four Flow CLI tests, two Flow Meta tests, and 44 Flow Nexus tests.
The two new process-import tests passed. Formatting and deny-warnings Clippy
passed.

The preceding no-fallback Prometheus attempt did not execute the checks to a
terminal result: cache lookups timed out repeatedly. It was interrupted after
the cache retries had already established the external availability failure,
then the living-authorized local fallback above was used.

Remote readback after push resolved the branch to exact Flow revision
`6ed7d1742995647930c8a1d2b484f18bf7061f9c`.

## Open acceptance gap

Binding an already-running seat is intentionally not enough to make it
delivery-ready. The imported row remains Pending/RegisteredUnconfirmed, and
Message must hold it. The v2 contract currently has no privileged operation
that verifies an existing seat's machine-produced native first-prompt receipt
and promotes that exact binding to Active. A separate narrow confirmation
contract and runtime slice is therefore required before the first real Message
delivery to an imported seat. It must verify the native transcript evidence;
it must not turn process liveness into a fabricated readiness receipt.

The first live acceptance should bind a non-Psyche existing seat, confirm it
from its machine-produced native receipt, send one harmless marker through
Message, and separately witness transport plus target presentation/read.

## Routing

The old Psyche High `836818` route is held for its successor and was not sent
or awakened. This handoff retains the exact evidence for the successor. Field
owns build, activation, fresh-store bootstrap, and live acceptance.

## Sources

- Living and routed implementation constraints in this flow's native
  transcript, 2026-09-24.
- meta-signal-flow v2-compatible v4 contract revision
  `71e92386ac0318485ce7eb3bbfab250ad44c68b3`.
- Flow source revision `6ed7d1742995647930c8a1d2b484f18bf7061f9c`.
- Local full flake-check terminal receipt from this seat, 2026-09-24.
