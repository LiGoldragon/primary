# ethos-zero contracts in vision shape

signal-ethos-zero 2.0.0 (`5a6ae291`) and meta-signal-ethos-zero 2.0.0
(`f8fe91bb`) are on main. Both are on signal 8.0.0 (`f35460de`, which had
landed on protos and datom-codec 0.32.2), ethos-zero 16.0.0 (`c2653dd8`),
protos `15b41da8` and datom-codec `4dff16b4`. Nothing was deployed. Nothing
serves either contract.

## For the morning book: Observe, before and after

1.0.0, flat. Every type is declared apart:

```
Signal
[]
[ Observe.ObservationSelection
  … ]
[ Observed.Observation
  … ]
[ …
  Generation.{ FileLocation ArtifactPath }
  ObservationSelection.[ Assemblies ]
  AssemblySummary.{ FileLocation ArtifactPath }
  AssemblySnapshot.{ Vector<AssemblySummary> }
  Observation.[ Assemblies.AssemblySnapshot ]
  … ]
```

2.0.0, vertical (ethos-zero's own print). The payloads are inline,
`AssemblySummary` is merged into `Generation`, and `FileLocation` comes from
the Library:

```
Signal
[ signal_ethos_zero:[ …
    FileLocation ] ]
[ Observe.[ Assemblies ]
  … ]
[ Observed.[ Assemblies.Vector<Generation> ]
  … ]
[ Generation.{ FileLocation
               ArtifactPath.String }
  … ]
```

The datom text of `Observe` is unchanged: `Observe.Assemblies`. `Observed`
lost one brace level: `Observed.Assemblies.{ [ … ] }` became
`Observed.Assemblies.[ … ]`.

## Holder types removed: 11

- Ordinary (7):
  - Wrappers of one value: `GenerationRequest`, `SubscriptionRequest`,
    `AssemblySnapshot`, `ProjectionFault`.
  - Payloads declared apart, now inline: `ObservationSelection`,
    `Observation`, `SyntaxFault`.
- Meta (4):
  - Wrappers: `MetaSubscriptionRequest`, and the `SourceIndex` struct (now
    `Vector<FileLocation>`).
  - Payloads now inline: `MetaObservation`, `ConfigurationRefusal`.
- Duplicates merged as well (not counted above):
  - `AssemblySummary` into `Generation`.
  - Meta's `Source` into the Library's `FileLocation`.
  - `SourceName` and `RelativePath` were declared in both files and are now
    declared once.

Top-level named declarations went from 31 to 8: 3 in the Library, 2 in the
ordinary Signal, 3 in the meta Signal.

## Library

The Library is `signal-ethos-zero/ethos/library.ethos`. It holds
`SourceName`, `RelativePath` and `FileLocation`.

- ethos-zero 16 lets a Signal import a Library. `x:[ A ]` generates the
  Rust path `x::A`. Both Signals import `signal_ethos_zero:[ … ]`.
- signal-ethos-zero refers to itself by that name through
  `extern crate self as signal_ethos_zero`. This is the same device as
  ethos-zero's flow-contract test.
- meta-signal-ethos-zero now depends on signal-ethos-zero. Before, it was a
  dev-dependency.
- Why the Library lives in signal-ethos-zero: no Ethos Nexus repository
  exists, and peers depend on wire repositories, never on a Nexus. This was
  my choice and is open to correction.

## Wire identity and datom text

The greeting digest covers the Library as well as the Signal:

- Ordinary: `ETHOS` is library then signal. The digest is
  `-1927924637596380248`.
- Meta: `build.rs` writes `CONTRACT` = signal-ethos-zero's `LIBRARY` then
  meta's file. The digest is `-1340365494544471030`.
- Both digests were computed outside the crate, in Python FNV-1a. The same
  script reproduces the 1.0.0 digest `423590495342270605`.

No variant was renamed. Every value whose data did not change reads and
prints the same text. Five shapes lost a brace level. UPGRADES.md lists each
one, and a test sees the old text refused:

- `Generate`, `Subscribe`, `Unsubscribe`, `GenerationStarted`: `{ { s p } }`
  became `{ s p }`.
- `Observed.Assemblies`: `{ [ … ] }` became `[ … ]`.
- `RustProjectionRejected`: `{ reason }` became `reason`.
- meta `Subscribe`, `Unsubscribe`: `{ Sources }` became `Sources`.
- meta `Observed.Sources`, `SourcesChanged`: `{ [ … ] }` became `[ … ]`.

## Not done, and why

- **Reply naming is kept.** `GenerationRejected` (the answer to Generate) and
  `GenerationRefused` (the subscription event) both carry
  `GenerationRefusal`. The vision example would name the reply `Refused` and
  let its variants name the reason. Renaming would change the datom text of
  every refusal, so the names stay. The living should rule on this.
- **Unanswered queries.** `Subscribe` and `Unsubscribe` have no paired
  past-tense reply (`Subscribed`, `Unsubscribed`). `Unsubscribe` also
  duplicates abandoning the exchange (signal's `Dispatch::Abandon`). Adding
  or removing vocabulary was outside the brief, so both are left as they
  were.
- **The generator's print and naming are kept as they are:**
  - The print keeps a structure whose elements are all leaves on one line,
    for example `FileLocation.{ SourceName RelativePath }` and the import
    list. That is its rule ("one of which has a next layer").
  - Inline payloads become `<Variant>_Data` in Rust, for example
    `Observe_Data`, `InvalidEthos_Data` and `ConfigurationRejected_Data`.
  - In-place names such as `Start`, `End`, `Reason` and `ArtifactPath`
    become file-level Rust aliases even though each is used once.
- **Signal carries one digest source.** `Contracted::CONTRACT_SOURCE` takes a
  single `&str`. Meta therefore concatenates in `build.rs`; it cannot use
  `concat!` across crates. If signal digested several sources, the
  build-script step would go away.
- **No other roots.** The contracts have no Operation or Memory root. Those
  belong to a Nexus, and none exists yet.

## Tests

| Run | Repository | Result |
|-|-|-|
| `cargo test` (no datom) | signal-ethos-zero | 5 exchange envelope + 1 frame round trip, ok |
| `cargo test --features datom` | signal-ethos-zero | 5 + 3 (examples 3 queries/8 responses, old holder text refused), ok |
| `nix flake check` | signal-ethos-zero | exit 0 (build, test, generated-contract, exchange-envelope, datom-contract, doc, fmt, clippy, no-free-functions, no-inherent-methods) |
| `cargo test` (no datom) | meta-signal-ethos-zero | 4 + 1, ok |
| `cargo test --features datom` | meta-signal-ethos-zero | 4 + 3 (examples 4/10, old holder text refused), ok |
| `nix flake check` | meta-signal-ethos-zero | exit 0, same checks |

- **Generated Rust is checked on every build.** `build.rs` regenerates each
  file and asserts it matches the committed Rust byte for byte. It also
  asserts that each ethos file (comments aside) equals ethos-zero's
  `Printable::print`.
- **Each new check was seen failing once.**
  - The layout guard panicked when `library.ethos` was put on one line.
  - Each old-text test failed when given the new text.
- **One datom-codec.** `cargo tree -d` lists datom-codec 0.32.2 twice, as a
  normal dependency and as a build dependency. Both are the same source, so
  it is one datom-codec.
- **How Nix was run.** Both nix checks ran on `path:` of the jj worktree.

## Sources

- Worktrees: `~/wt/github.com/LiGoldragon/{signal-ethos-zero,meta-signal-ethos-zero}/vision-f1c841`. Lock 11678 was released.
- ethos-zero c2653dd8:
  - `UPGRADES.md` 16.0.0
  - `tests/flow_contract.rs`, the `extern crate self` device
  - `tests/generated/flow-signal.rs`, import paths
  - `src/printing.rs`, through `Printable`
- signal f35460de: `UPGRADES.md` 8.0.0, and `src/accord.rs` (`Contracted`
  and FNV-1a `of_source`).
- The vision-ethos, vision-nexus and knowledge-ethos skills.
- `Vision/ethos.md` (Library, Imports).
- `flows/91ea9f/vision/ethos.md` (inline unless used twice, depth about three).
