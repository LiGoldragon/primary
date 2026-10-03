# ethos-zero 15.0.0: the four roots

ethos-zero now reads the four roots of vision-ethos: Library, Signal, Operation and Memory. `Memory` replaces `Sema`. `Operation` generates `Operation` and `Outcome` enums the way Signal generates `Query` and `Response`. The Flow Nexus's four files generate and still print back byte-identical. To make the Signal and Operation files generate, a struct position may now declare its type in place (`Brief.String`). That was not in the brief, but those files need it. Main is at 3d330276cce4 on origin, in four commits on top of 06d73e0.

## What landed

| commit | content |
|---|---|
| 040a1b4b Test the Memory and Operation roots and types declared in a position | The tests, written first and seen failing (below). |
| 54a08259 Read Memory for Sema and the Operation root; declare a type in a struct position | `error.ethos`, `src/error.rs` (`Problem.Renamed.String`), `src/lib.rs`, `src/conception.rs`, `src/checking.rs`, `src/generation.rs`, `src/protosization.rs`, new `src/sectioning.rs`. |
| ed572b6c Rename the Sema fixture to Memory; generate and compile the Flow Nexus files | `fixtures/entry-sema.ethos` becomes `entry-memory.ethos`, whose generated Rust is byte-identical to 14.2.0's. `tests/generated/flow-{library,signal,operation,memory}.rs` are new and held fresh. |
| 3d330276 Document the four roots and 15.0.0 upgrade; mark Operation sections proposed | `README.md`, `UPGRADES.md`, `ethos-zero.ethos` comment, `Cargo.toml`/`Cargo.lock` 15.0.0. |

1. **Memory.** It has the same two sections and the same generation as Sema. `Sema` is now refused with `Rejected.{ file { 1 1 } Conceptual.{ [ 0 ] Renamed.Memory } }`, which the CLI test asserts exactly. The successor comes from `Succeeding for Root`.
2. **Operation.** The sections are imports, operations, outcomes and types. It generates `pub enum Operation` and `pub enum Outcome`, and each variant carries its payload (`Start(Start_Data)`, `Started(flow::FlowId)`, `Failed(String)`). An Operation that declares a type named `Operation` or `Outcome` is refused. Signal and Operation share one code path: `Sectioning::implied_enums` gives `Query`/`Response` for Signal and `Operation`/`Outcome` for Operation.
3. **The proposed mark** sits in UPGRADES ("The section order is proposed, pending the living's word"), in the README, and in the comment block of `ethos-zero.ethos`.
4. **Positions declared in place.** `Brief.String`, `State.[ Running Ended ]` and `Capsule.{ Home.String Login.Vector<String> }` each declare a type under its own name, in the file's namespace. The position holds it by name (`brief: Brief`), and the type is emitted before its holder. A second `Brief` anywhere in the file is refused as a `Duplicate` at its head. Error locations inside these types are correct; I probed `{ 4 25 } Undeclared.Bogus` and `{ 4 7 } Duplicate.Brief`. 14.x refused such a position as `Expected.Reference`. That refusal is why `flow-signal.ethos` failed (`{ 4 12 }`), and why the Operation file would also have failed.

## Decisions taken that are not in the brief or the vision

- **Naming of a type declared in place.** It takes its own name (`Brief`, `State`, `Capsule`) and not a derived `_Data` name. This follows "a type used once is declared inline where it is used". A variant's inline payload keeps its `X_Data` name, as before.
- **How Operation is carried.** It is "Plain", like Library and Memory: the datom kinds are derived unconditionally and there is no rkyv. The reason is that an Operation does not cross a wire. The trade-off: datom-codec is linked into a Nexus that uses its Operation types, which vision-nexus wants compiled out (Memory already does the same). This is the living's to judge.
- **Comments are not printed.** The no-argument CLI prints `ethos-zero.ethos` without its comments, so the "proposed" mark is in the source file but not in that output.

## Consumers to rename (listed in UPGRADES, not changed)

I read the head of all 141 `.ethos` files under `/git`. Seven are headed `Sema`:

- spirit-ethos/sema.ethos
- spirit/schema/sema.ethos
- core-schema/tests/fixtures/bootstrap/sema.ethos
- core-ethos/tests/fixtures/bootstrap/sema.ethos
- primary-next/reports/spiritEthosFixtures/sema.ethos
- primary-next/flows/f6db8d/witnesses/substrate/probe-ethos/sema-record.ethos
- primary-next/flows/f6db8d/witnesses/substrate/probe-ethos/sema-plain.ethos

No Rust consumer under `/git` names `File::Sema`, `TypeDeclaration` or `Variant::Struct`; the build scripts only call Potential, Actualizing and Generating.

## Testing

- **Red.** Before the change, `cargo test --no-fail-fast` gave: in `cli`, 2 failed (Sema refusal; the four flow files Check). In `ethos`, 10 failed (Memory ×4, the Sema refusal, Operation ×2, positions declared in place ×3).
- **Green.** After the change, `cargo test`: lib 20, cli 16, ethos 30, freshness 4, generated 19, print 9, signal-without-datom 2, with 0 failed. `cargo fmt --check`, `cargo clippy --all-targets -D warnings` and `cargo doc -D warnings` are all clean. These ran locally and were bounded (`ulimit -v 16G`, `timeout`).
- **Flow Nexus modules.** In `tests/generated.rs` the crate stands in for `flow` (`extern crate self as flow`), so `flow-library`, `flow-operation` and `flow-memory` compile. An `Operation::Start` and a Memory `Flow` round-trip as datom text. `flow-signal.rs` generates and is held fresh, but it is not compiled: its rkyv-archived types carry the Library's `Voice`, `FlowId` and `Event`, and a Library type does not derive rkyv. A Signal that imports Library types therefore does not compile today. That is an open gap, recorded in UPGRADES.
- **Nix.** `nix flake check` ran on `github:LiGoldragon/ethos-zero/3d330276cce48e5cce144fb6ed81b9aa7817f336` as the detached user unit `ez15check` (MemoryMax=8G, RuntimeMaxSec=7200). Result: "all checks passed!", exit 0, finished at 22:57:31 (about a minute; the dependencies were cached on prometheus). The checks were build, test (same counts as the local run), fmt, clippy, doc, no-free-functions and no-inherent-methods. dependency-ethos regenerated the pinned `protos.rs`, `protos-kinds.rs`, `datom-codec.rs` and `datom-codec-kinds.rs` (Library files).

## Gaps for the main flow

- The `knowledge-ethos` skill still says three roots, Sema, and that a struct position is a reference. It should be regenerated from the Curriculum source to cover Memory, Operation and positions declared in place.
- The Signal→Library rkyv gap (above).
- Whether Operation should be carried as "Plain" (above).

## Sources

- /git/github.com/LiGoldragon/ethos-zero at 3d330276cce4 (UPGRADES.md, README.md, src/sectioning.rs, tests/).
- /home/li/primary/flows/3ec648/rulings.md, rulings 3 and 9.
- vision-ethos, knowledge-ethos and vision-nexus skills as loaded on 2026-10-02.
- Unit log: scratchpad `check15.log`.
