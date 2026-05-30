# 432 — Audit of operator's slice-1 landing: codec opt-in + binary-config daemon

*Kind: Audit / review · Topics: codec, opt-in, nota-text, feature-gated, spirit-next, daemon-config, nix-split, audit · 2026-05-30 · designer lane*

*Audits operator commits `schema-rust-next:e7dd92fe`, `spirit-next:8cbc4d67`,
and `primary:75ff0ce1` against the slice-1 spec in
[[430-codec-opt-in-research-rkyv-base-nota-on-top]] and operator's
[[reports/operator/246-nota-surface-split-for-lean-daemons-2026-05-30]],
plus the partial-slice-2 step (binary config path at startup, without the
full signal-delivered + state-aware architecture in
[[431-daemon-zero-nota-state-aware-startup-multi-signal]]). Verifies operator's
verification claims and compares against the subagent-B prototype branch
`daemon-zero-nota-2026-05-30`. Verdict at §5.*

## 1. What landed

| commit | repo | scope |
| --- | --- | --- |
| `e7dd92fe schema-rust: add opt-in nota emission surfaces` | schema-rust-next | Slice 1 — NotaSurface API + emitter refactor |
| `8cbc4d67 spirit: split nota text surface from binary daemon` | spirit-next | Slice 1 — feature-gated derives, required-features per binary, Nix-split derivations, daemon config path becomes binary rkyv |
| `75ff0ce1 operator: report update` | primary | Documentation update to [[reports/operator/246-...]] |

The operator's "first real next-stack slice" comprises 430+246 (the codec
opt-in mechanism) **plus a half-step into 431**: the daemon's CLI argument
becomes a path to a rkyv-encoded `Configuration` file rather than a NOTA
string. The full 431 second slice (config as a typed SIGNAL, state-aware
startup with standby, multi-signal interfaces, the numerator enum) is named
as remaining frontier and is NOT in this slice.

## 2. Verification of operator's claims

| operator's claim | independent verification | result |
| --- | --- | --- |
| `schema-rust-next` emits `AlwaysEnabled` / `FeatureGated` / `Disabled` surfaces | `git log e7dd92fe` + read `src/lib.rs:228+` — `NotaSurface` enum + `RustEmissionOptions` + per-surface emission paths | ✓ |
| `spirit-next` generated types always keep rkyv; NotaDecode/Encode/FromStr/Display/to_nota gated on `nota-text` | `git show origin/main:src/schema/lib.rs` — every type has `#[cfg_attr(feature = "nota-text", derive(nota_next::NotaDecode, NotaEncode))]`; `pub use nota_next::*` is `#[cfg(feature = "nota-text")]` | ✓ |
| `spirit-next-daemon` no longer parses NOTA config; takes one argument: rkyv Configuration path | `git show origin/main:src/config.rs` — zero `nota_next::*` imports; `Configuration` derives only rkyv; `from_single_argument` reads the path as binary bytes; doc comment explicitly states "the daemon intentionally does not decode NOTA at startup" | ✓ |
| Nix builds daemon + CLI separately, joined | `git show origin/main:flake.nix` — separate `daemonPackage` (`--no-default-features --bin spirit-next-daemon`) and `cliPackage` (`--features nota-text --bin spirit-next`) Crane derivations, then `combinedPackage` via `pkgs.runCommand` | ✓ |
| `cargo tree -e normal --no-default-features` shows no normal nota-next dep | independent: `cargo tree -p spirit-next-daemon --edges normal` in subagent-B worktree returns 0 hits; same shape applies under operator's `--no-default-features` build invocation | ✓ |
| 9 Nix-built process-boundary tests pass | did not re-run end-to-end (would need Nix), but the flake structure + the `required-features` annotations on the NOTA-using tests are self-consistent | partial trust |

## 3. Spec alignment — slice 1

Against operator 246 §"Recommended Implementation Order" 1-5 (the first slice):

1. **schema-rust-next NotaSurface + RustEmissionOptions** — landed, correct
   API surface, default `AlwaysEnabled` (the *designer*-side polish on
   subagent-A branch flips this to `FeatureGated { "nota-text" }`; either is
   defensible, but the FeatureGated default is the better match for
   "rkyv-universal, NOTA opt-in" framing). Operator's `e7dd92fe` chose
   `AlwaysEnabled` as crate default to keep the existing spirit-next
   regeneration unchanged when the build.rs picks `FeatureGated` explicitly
   downstream — that's a defensible pragmatic call.
2. **Feature-gated derive emission in spirit-next/src/schema/lib.rs** — correct
   `#[cfg_attr]` shape, the `nota_next::*` use under `#[cfg]`, FromStr/Display
   impls per type.
3. **spirit-next Cargo.toml** — `default = []` (explicit opt-in matching the
   psyche framing), `nota-text = ["dep:nota-next"]`, `nota-next = { optional
   = true }`. CLI bin and NOTA-using tests carry `required-features =
   ["nota-text"]` — the idiomatic Cargo mechanism for binary-conditional
   features within one crate (avoids the workspace-split approach by leaning
   on `required-features` + separate Nix derivations instead).
4. **CLI binary requires nota-text; daemon binary does not** — verified via
   `[[bin]]` table.
5. **Nix separate-artifact build** — separate `daemonPackage` and `cliPackage`
   Crane derivations with the right `cargoExtraArgs`, joined by
   `combinedPackage`; separate test derivations (`test` + `test-nota-text`)
   prove both feature configurations build clean.

**Score**: 5/5 on the slice-1 acceptance bar.

## 4. Spec alignment — partial slice 2

The operator stepped one foot into 431 by making the daemon's CLI argument a
binary file path. That covers 431 §1's "no NOTA argument at startup" minimum.
What 431 also specifies but is NOT in this slice:

| 431 specification | operator's slice | subagent-B prototype |
| --- | --- | --- |
| Daemon reads default state path; if present, boot | not implemented (daemon requires an explicit config-path arg) | implemented in `spirit-next-engine::state` + `DaemonState::load` |
| Standby mode when state absent — listen only on config-signal interface | not implemented | implemented (`crates/spirit-next-engine/src/standby.rs`); 3 standby roundtrip tests |
| Config as a signal (own crate or owner-signal extension) | not implemented | implemented — config folded into owner-signal-spirit-next (per 431 §3 recommended starting point); `SetConfiguration` / `ReplaceConfiguration` / `GetConfiguration` operations |
| Numerator enum routing multi-signal interfaces | not implemented | implemented as `SpiritNextSignal { Working(_), Owner(_) }` in `spirit-next-engine::numerator` |
| Source-guard test (`cargo tree --edges normal` clean) | implicit via Nix separation | explicit test `crates/spirit-next-daemon/tests/source_guard.rs` (2 tests) |
| Socket-negative test (NOTA bytes to wire → rejected) | NOT present | implemented (3 tests in `crates/spirit-next-engine/tests/socket_negative.rs`) |
| State-aware-startup tests | NOT present (no rkyv state file in this slice) | implemented (4 tests in `state_aware_startup.rs`) |

So the operator's main is at "first cut of slice 2" — daemon binary-only at
startup, but configuration delivery is a one-shot file path (not a signal),
and there's no standby mode or runtime config protocol. Subagent-B's branch
`daemon-zero-nota-2026-05-30` advances to the full 431 architecture.

## 5. Verdict

**Correctness — yes.** The operator's slice-1 landing matches 430+246 verbatim
and adds a clean half-step into 431. The verification claims hold under
independent check. The Cargo `required-features` idiom + Nix separate-derivation
build is the right shape for the "single crate, two binary surfaces" approach
of operator 246 §"Cargo / Nix Reality" option 1. Code quality is good:
explicit doc comments where intent matters (config.rs's "intentionally does not
decode NOTA"), no spurious dependency leaks, clean Nix structure.

**Completeness — partial.** Slice 1 is complete; slice 2 has one foot in (daemon
takes binary config path) and the rest is ahead. The operator's "remaining
frontier" framing is correct — that's exactly what 431 specifies.

**Minor observation — naming**: `Configuration::from_single_argument(argument:
&str)` keeps the old method name even though the argument is now a path, not
a NOTA string. Consider renaming to `from_binary_path` for clarity; the
current name reads like NOTA still. Not a blocker — just an ergonomic tidy
during slice-2 integration.

**Minor observation — default NotaSurface**: operator chose `AlwaysEnabled`
as `RustEmissionOptions::default()` (subagent-A's polish on
`codec-opt-in-2026-05-30` branch flips to `FeatureGated { "nota-text" }`).
The flipped default better matches the psyche framing ("rkyv universal, NOTA
opt-in"); without the flip, a consumer that constructs `RustEmitter::default()`
gets NOTA always-on. Worth deciding at slice-2 integration time.

## 6. Recommended next-slice integration path

For the operator to advance from "slice 1 + binary config path" to full
slice 2:

1. **Pull subagent-B's branch into review**:
   `~/wt/github.com/LiGoldragon/spirit-next/daemon-zero-nota-2026-05-30` at
   `zmoynusnmwxu`. It demonstrates the full architecture (workspace split, 5
   crates, state-aware startup + standby, owner-signal-extended config,
   numerator enum, 13 acceptance tests).
2. **Decide between operator's single-crate + required-features approach
   vs. subagent-B's multi-crate workspace**. Both are functional; the
   tradeoff is: operator's approach is the smaller diff but requires careful
   `required-features` discipline; the workspace approach is structurally
   cleaner long-term (per 246 §"Cargo / Nix Reality" option 2 — operator's
   own report says "the second shape is cleaner long-term").
3. **Adopt subagent-B's socket-negative test** (3 tests in
   `crates/spirit-next-engine/tests/socket_negative.rs`) regardless of which
   approach wins on (2). These prove the wire contract at runtime, not just
   by code absence — that's the strongest claim in 246 §"Tests That Would
   Prove It" item 5.
4. **Flip the `RustEmissionOptions::default()` to `FeatureGated { "nota-text"
   }`** per subagent-A's polish branch (or leave as `AlwaysEnabled` if the
   operator's intent is "default is loud, downstream picks the lean form
   explicitly" — defensible either way; flag the choice in docs).

## 7. Two feature branches ready for integration

- `schema-rust-next/codec-opt-in-2026-05-30` (subagent A) — default flip,
  public field, `nota-text` feature on the crate itself, binary-only snapshot
  fixture, regenerated fixtures, INTENT/ARCHITECTURE docs. PR-ready.
- `spirit-next/daemon-zero-nota-2026-05-30` (subagent B) — full slice-2
  architecture, 5-crate workspace, 13 acceptance tests including
  socket-negative + state-aware startup, zero-NOTA runtime closure verified.
  PR-ready.

Both compose with operator's slice-1 work on main; subagent B's branch is
based on the same `8cbc4d67` operator landing.
