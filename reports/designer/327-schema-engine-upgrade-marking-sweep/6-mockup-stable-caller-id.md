*Kind: Mockup · Topic: stable-durable-caller-id · Wave: designer/327 mockup-1 · Date: 2026-05-24*

# 327 · Mockup 1 — StableCallerId for upgrade-time session resumption

## §1 What I implemented

A working `StableCallerId` newtype in `signal-frame::caller` plus a
consumer-side `SessionResumptionMap` sketch, with witnesses across
field-stability, hex projection, and NOTA round-trip. All `cargo test`
suites and `nix flake check` pass.

### §1.1 Worktree + branch

| Item | Value |
|---|---|
| Worktree | `/git/github.com/LiGoldragon/signal-frame-mockup-stable-caller-id-1` |
| Branch | `mockup-stable-caller-id-1` |
| Base | `main` at `70812f3 schema: add v0.1 concept schema` |
| Commit | `077a76c MOCKUP: stable durable Caller ID for upgrade-time session resumption` |

The mockup branch sits as a git worktree under the existing
signal-frame ghq checkout. The pre-existing primary signal-frame
working copy already had unrelated WIP (`schema/signal-frame.concept.schema`)
so I branched off `main` directly and kept my mockup isolated.

### §1.2 File-by-file diff stat

| Path | Lines | Role |
|---|---|---|
| `Cargo.toml` | +2 | adds `blake3 = "1"` (the workspace convention used by `signal-criome` and `signal-lojix`) |
| `Cargo.lock` | +70 | resolved blake3 closure |
| `src/caller.rs` | +167 | `Caller::stable_id()`, `StableCallerId`, `StableCallerIdParseError`, hex projection, `NotaEncode`/`NotaDecode` |
| `src/lib.rs` | +9 | module + re-exports |
| `src/session_resumption.rs` | +74 | new file — consumer-side `SessionState` + `SessionResumptionMap` sketch |
| `tests/stable_caller_id.rs` | +178 | 13 witnesses |
| `macros/src/schema_reader.rs` | +1 / -4 | unrelated `cargo fmt` normalisation |

Total mockup additions (excluding Cargo.lock + fmt drift): roughly 430
lines of code, of which the heart is the `Caller::stable_id` method
(~30 lines), the `StableCallerId` type with hex codec (~95 lines), and
the test witnesses (~178 lines).

### §1.3 Key types

**`StableCallerId`** — `pub struct StableCallerId([u8; 16])`. Derives
`Archive`, `RkyvSerialize`, `RkyvDeserialize`, `Debug`, `Clone`,
`Copy`, `PartialEq`, `Eq`, `PartialOrd`, `Ord`, `Hash`. Hashable
because the daemon-side resumption map keys on it. Fixed `[u8; 16]`
rather than `Vec<u8>` because the size is contract-stable; the
identifier is half a BLAKE3 digest. Wire form on rkyv is the raw 16
bytes; wire form on NOTA is a 32-character lowercase hex string
written as a bracket-string `[deadbeef…]` (bare-string ineligible
because hex starts with a digit).

**`Caller::stable_id(&self) -> StableCallerId`** — Builds a BLAKE3
digest over the canonical encoding:

```text
pid:        4 bytes big-endian
start_time: 1-byte presence tag + (8 bytes big-endian | empty)
executable: 1-byte presence tag + (8-byte length-prefix + bytes | empty)
```

Then truncates the BLAKE3 XOF output to 16 bytes. The presence-tag
discipline matters: a `Caller` with `start_time: None` and one with
`start_time: Some(0)` must hash to different identifiers; the
witness `presence_tag_distinguishes_none_from_some` enforces this.

**`SessionResumptionMap`** (sketch in `src/session_resumption.rs`) —
holds `HashMap<StableCallerId, SessionState>` with `record` and
`resume` methods. `SessionState { payload: Vec<u8> }` is opaque on
purpose; a real daemon substitutes its own session-state record. The
module carries a `// MOCKUP per designer/327 mockup-1` marker and a
module-doc paragraph stating it lives in `signal-frame` only as long
as needed to demonstrate the API shape; real consumption belongs in
the upgrade-aware daemon code.

## §2 Spawn-envelope consumer investigation

The instructions hinted that "Internal(component_name from the spawn
envelope)" in `signal-persona-origin/ARCHITECTURE.md §4` implies a
spawn-envelope mechanism whose consumer should be findable in
`persona/src/` or `upgrade/src/`. I traced it.

### §2.1 Where the spawn envelope is defined

`SpawnEnvelope` (the wire-level signal record) lives in
`/git/github.com/LiGoldragon/signal-engine-management/src/lib.rs`
around line 247:

```rust
pub struct SpawnEnvelope {
    pub engine_identifier: signal_persona_origin::EngineIdentifier,
    pub component_kind: ComponentKind,
    pub component_name: signal_persona_origin::ComponentName,
    pub owner_identity: signal_persona_origin::OwnerIdentity,
    pub state_dir: WirePath,
    pub domain_socket_path: WirePath,
    pub domain_socket_mode: SocketMode,
    pub engine_management_socket_path: WirePath,
    pub engine_management_socket_mode: SocketMode,
    pub peer_sockets: Vec<PeerSocket>,
    pub manager_socket: WirePath,
    pub engine_management_protocol_version: EngineManagementProtocolVersion,
}
```

### §2.2 Where the spawn envelope is consumed

The richer in-process projection is
`persona::engine::ComponentSpawnEnvelope`
(`/git/github.com/LiGoldragon/persona/src/engine.rs:707`). It carries
all the kernel/OS-side details (paths, modes, peers, command, etc.)
and the `signal_spawn_envelope()` method
(`persona/src/engine.rs:781`) reduces it to the wire-level form for
transmission. Consumers downstream:

- `persona/src/supervisor.rs:96` — `spawn_envelope_for_instance(…)`
  consumed by the supervisor when bringing components up
- `persona/src/supervision_readiness.rs:240` —
  `Readiness::from_envelope` projects readiness facts off the
  envelope
- `persona/src/readiness.rs:156/164` — same shape on the
  cross-engine readiness path
- `persona/src/direct_process.rs` — pervasive: writes the envelope
  file (`:325`), threads it through 20+ helper functions building the
  component process

### §2.3 No existing Caller-or-StableCallerId consumer in `upgrade/`

Search of `upgrade/src/{handover,execution,catalogue,invocation}.rs`
for `Caller`, `StableCallerId`, `session`, `resumption`, `reconnect`
finds zero hits. The upgrade machinery currently does not consult
either provenance system; resumption-by-identity is **prospective**.
That makes the consumer-side sketch in this mockup architecturally
fresh — there is no existing code to mimic or merge against.

### §2.4 How spawn envelope + Caller compose

The spawn envelope is persona's **side** of provenance — it records
who the **daemon** is, where it sits, which sockets it owns. The
Caller is the **CLI's** side — it records who the **parent process
of the CLI** is. SO_PEERCRED on the socket connects the two: the
persona-system uid on an internal socket means "an internally
supervised component is on the other end, look up its
ComponentName via the spawn envelope," while the engine_owner_uid
on the user-writable socket means "an external owner CLI is on the
other end, look up its parent via the Caller."

Resumption across an upgrade cutover needs **both** halves to be
stable across the cutover:

- spawn-envelope side: the new daemon needs to recognise that the
  component on the far end of the internal socket is the same one
  the old daemon was talking to → ComponentName + EngineIdentifier
  composite is already stable.
- Caller side: the new daemon needs to recognise that the CLI on
  the far end of the user-writable socket has a parent shell that
  was already in a session with the old daemon → StableCallerId
  fills this gap.

The mockup focuses on the second half (Caller-side) because that's
what the psyche directive named. The spawn-envelope half is already
stable by virtue of ComponentName being a closed enum + the
EngineIdentifier surviving the cutover.

## §3 Test results

### §3.1 New witnesses (`tests/stable_caller_id.rs`)

| Test | What it asserts |
|---|---|
| `identical_callers_produce_identical_stable_id` | round-trip identity |
| `different_pid_produces_different_stable_id` | pid field-stability |
| `different_start_time_produces_different_stable_id` | start_time field-stability |
| `different_executable_produces_different_stable_id` | executable field-stability |
| `presence_tag_distinguishes_none_from_some` | None vs Some(0) hash differently |
| `stable_id_hex_is_thirty_two_lowercase_chars` | hex projection shape |
| `stable_id_hex_round_trip` | `to_hex` / `from_hex` round-trip |
| `stable_id_hex_rejects_wrong_length` | parse error path |
| `stable_id_hex_rejects_non_hex` | parse error path |
| `stable_id_nota_round_trip` | NOTA encode/decode round-trip |
| `stable_id_nota_text_is_hex_string` | NOTA emits hex projection |
| `resumption_map_records_and_resumes_by_stable_id` | consumer-map happy path |
| `resumption_map_keys_survive_caller_clone` | reconnect lookup hits same key |

All 13 pass.

### §3.2 Cargo full-suite

```text
caller             — 0 tests   ok
channel_macro      — 22 tests  ok
channel_macro_compile_fail — 1 test ok
command_line       — 5 tests   ok
frame              — 21 tests  ok
namespace          — 3 tests   ok
namespace_sections_compile_fail — 1 test ok
stable_caller_id   — 13 tests  ok
doc-tests          — 0 tests   ok
```

All pre-existing suites are unchanged by the mockup; the new suite
adds 13 witnesses.

### §3.3 Nix flake check

```text
checks.x86_64-linux.default — all checks passed!
```

Built against the locked rust-toolchain. The `blake3` dep adds an
incremental build cost (compiling blake3 + cc + arrayref + arrayvec
+ constant_time_eq + cpufeatures + find-msvc-tools + libc + shlex)
but the build completes cleanly on the remote build host.

## §4 Open questions for operator

### §4.1 Crate placement — signal-frame or signal-persona-origin?

I put `StableCallerId` in `signal-frame::caller` because `Caller`
lives there. The argument for moving it to `signal-persona-origin`:
the stable identifier is a *provenance* concept, and
`signal-persona-origin` already owns provenance records
(`IngressContext`, `MessageOrigin`, `OwnerIdentity`,
`ConnectionClass`, `ComponentName`). The argument for keeping it in
`signal-frame`: the Caller machinery is frame-mechanics-level (every
contract uses it via `Request<P>`), so the stable projection of the
Caller belongs alongside it; promoting to `signal-persona-origin`
would re-introduce a dependency layer that the three-layer migration
just removed (`signal-persona-origin` now depends on `signal-frame`,
not the other way around).

**My recommendation:** stay in `signal-frame::caller`. The
`StableCallerId` is a projection of the existing `Caller`, not a
new provenance record. Moving it would require a reverse dependency
edge.

### §4.2 BLAKE3 dependency cost

Adding `blake3 = "1"` to `signal-frame` pulls in `cc`, `cpufeatures`,
`arrayref`, `arrayvec`, `constant_time_eq` as transitive
dependencies. `signal-frame` is a foundational substrate library —
*every* component triad depends on it. The blake3 transitive cost
shows up everywhere.

**Alternatives I considered and reject:**

- `siphash` (std `DefaultHasher`) — not cryptographically stable
  across Rust toolchain versions; collisions are cheap; identifier
  wouldn't be durable across rebuilds.
- `blake2b_simd` smaller-output variant — same dep weight,
  inferior performance to blake3 in our typical workload.
- `sha2` — heavier deps, slower on modern hardware, no
  XOF (extendable-output) shape for clean 16-byte truncation.
- Hand-rolled non-cryptographic mixing (FxHash, fnv) — fast but
  the identifier becomes adversarially weak; an attacker who can
  shape a parent shell command path could plausibly forge a
  collision.

**My recommendation:** keep blake3. The workspace already uses it
in `signal-criome` and `signal-lojix`; adding it to signal-frame
extends an existing convention rather than introducing a new one.
The transitive cost is paid once across the workspace.

### §4.3 Whether `signal-frame` is the right home for the consumer sketch

`SessionResumptionMap` lives in `signal-frame::session_resumption`
in this mockup, marked MOCKUP. The real implementation should live
in the upgrade-aware daemon code (`persona/src/upgrade.rs` or a
successor). I left it in signal-frame only so the witnesses can
exercise it without pulling in a daemon dependency. **Operator
should move it out** when integrating; the daemon module needs to
cooperate with the session-state store, not with signal-frame's
type catalogue.

### §4.4 What `SessionState` actually carries

I left `SessionState { payload: Vec<u8> }` as an opaque blob. Real
session state for the upgrade-time resumption case includes:

- pending replies the old daemon hadn't sent yet
- active subscriptions and their cursor positions
- exchange identifiers / lane sequences the CLI expects to resume on
- ownership facts the daemon validated at session start

Operator should decide whether `SessionState` is concrete (one
struct shape) or generic (`SessionState<T>` with the daemon picking
its own payload type). Erring on concrete-per-daemon means the type
moves out of `signal-frame` entirely; erring on generic means it
stays in `signal-frame` as a substrate, which is harder to justify
when only the upgrade machinery consumes it.

### §4.5 BLAKE3 output truncation to 16 bytes

The mockup uses BLAKE3's XOF (extendable-output) and reads 16 bytes.
This is half the natural 32-byte BLAKE3 output. The choice of 16
matches the canonical size of a "small but cryptographically
non-trivial" identifier (UUID-sized, fits in a register-pair on
modern hardware) and keeps wire form short (32 hex chars rather
than 64). Operator should confirm 16 is enough collision resistance
for the resumption-map use case — the map only holds active
sessions, so the birthday bound at 2^64 expected collisions before
trouble is comfortably oversized.

### §4.6 Hex projection or bare bytes in NOTA?

I chose hex (32-char lowercase, bracket-string-wrapped). Alternative
is NOTA's `#hex…` byte-literal — more compact, less universal in
debugging tooling. Recommendation: hex.

## §5 Cross-references

### §5.1 Upstream designer reports informing this mockup

- `reports/designer/301-design-elegant-cli-macro-with-caller-injection.md` —
  introduced `Caller { pid, executable, start_time }` and its
  placement on `Request<P>`. This mockup builds the next layer:
  given a Caller, what's its stable durable identity.
- `reports/designer/307-design-golden-ratio-namespace-split.md` —
  namespace discipline that informs where `session_resumption`
  lives in the lib re-exports.
- `reports/designer/315-design-sema-upgrade-and-handover-current-state.md` —
  upgrade machinery state that this mockup's resumption story
  would eventually plug into.
- `reports/designer/327-schema-engine-upgrade-marking-sweep/0-frame-and-method.md` —
  the wave-frame report under which this mockup was dispatched.

### §5.2 Existing Caller code touched

- `signal-frame/src/caller.rs:69-103` — `Caller` struct + `new` +
  `from_kernel` (pre-existing; extended with `stable_id()`)
- `signal-frame/src/request.rs:33,52,65` — `Request.caller`,
  `with_caller` (unchanged; the stable_id projection is read-only)
- `signal-frame/src/command_line.rs:637,644` —
  `Caller::from_kernel()` call sites in the CLI client path
  (unchanged; the macro-emitted CLI doesn't yet need stable_id)
- `signal-frame/tests/command_line.rs:158-210` —
  existing `client_shape_sends_request_with_caller_and_prints_reply`
  test (unchanged; demonstrates the kernel-capture path stable_id
  builds on)

### §5.3 Spawn-envelope code surveyed (not modified)

- `signal-engine-management/src/lib.rs:247-260` —
  wire-level `SpawnEnvelope` record
- `persona/src/engine.rs:707-803` — in-process
  `ComponentSpawnEnvelope` + `signal_spawn_envelope` projection
- `persona/src/supervisor.rs:96` — supervisor consumption
- `persona/src/supervision_readiness.rs:240` + `readiness.rs:156,164`
  — readiness consumption
- `persona/src/direct_process.rs` (pervasive) — process-bringup
  consumption
- `signal-persona-origin/ARCHITECTURE.md §4` — the SO_PEERCRED
  mapping that names "Internal(component_name from the spawn
  envelope)"

### §5.4 Operator integration notes

If operator integrates this mockup, the carry-forward items are:

1. Move `SessionResumptionMap` out of `signal-frame` into the
   upgrade-aware daemon code (likely `persona/src/upgrade.rs` or
   a new `upgrade/src/resumption.rs`).
2. Concretize `SessionState` to the daemon's actual session
   record (pending replies, subscription cursors, exchange
   identifiers, etc.).
3. Decide on the wire form for snapshotting the map across the
   cutover boundary — rkyv archive of `Vec<(StableCallerId,
   SessionState)>` is the obvious shape and the rkyv derives are
   already in place on `StableCallerId`.
4. Add an integration test that exercises the upgrade cutover
   path end-to-end: start an old daemon, open a session, kill
   the daemon, start the new daemon with the snapshot, reconnect
   the same CLI parent, assert session resumption hits.
5. Consider whether `Caller::from_kernel()` should also capture
   the `start_time` of the **grandparent** process (the shell
   launching the CLI's parent) — would extend stable_id's
   resilience to short-lived parent shells, but doubles the
   `/proc` reads. Out of scope for this mockup.

## §6 Constraints honoured

Mockup work happened on a fresh git worktree (one of the named
jj-escape-hatch cases — non-jj worktree off main); inline `git commit
-m` for the one commit. No emojis, no `---` rule lines, no mermaid.
`// MOCKUP per designer/327 mockup-1` markers land in `caller.rs`,
`session_resumption.rs`, `lib.rs`, `Cargo.toml`, and the test file
header.
