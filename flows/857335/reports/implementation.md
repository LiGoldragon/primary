# Implementation

## Ethos Zero migration

Ethos Zero 6.0.0 uses one compatible runtime Cargo pair: Protos
`aac95b0d08a4c7eb7f73c8ea18309f9e2e89315f` and Datom
`35d26d822870356af9b04cacfec40d85600b541d`. The flake separately pins the
producer declaration heads Protos `d5616342f5c4654deda3af3858bad68af8b68ce8`
and Datom `35d26d822870356af9b04cacfec40d85600b541d`; this avoids a duplicate
Protos crate identity because the current Datom runtime revision itself pins
the former Protos revision.

The public model has Library, Signal, and Sema roots only. Library preserves
imports, type declarations, kind declarations, and associations. Signal emits
Query and Response with feature-gated Datom derives. Sema has only imports and
record-type sections. Types/Kinds roots and Fault vocabulary are absent, and
the CLI’s domain failure is `GenerationRejected`.

`File` implements public `protos::Protosizable<Output = Protos>`. Its structural
ascent calls Protos `Canonicalizable::canonicalize`, the infallible shared
canonical extent assignment, after it constructs the form. It has no
File-level Textualizable shortcut. A 5,000-declaration manually constructed
File ascends without consuming reader budget; exact canonical extents compare
equal to a separately read canonical form. Sweet structural errors resituate
canonical extents to authored source locations.

Conception retains every structural parent and argument index through Library,
Signal, Sema, imports, capability signatures, complex kinds, and associations.
Behavioral witnesses cover nested and attached references, complex kind paths,
recursive inline generated names, named fields, recursive Chain generation,
Signal without a Datom dependency, and full canonical round trips. Type-data
identity constraints are rejected both while reading and while checking a
manually constructed public File; only kind identity constraints remain.

## Gates

Local gates pass: `cargo check --all-targets`, `cargo fmt --check`,
`cargo clippy --all-targets -- -D warnings`, `cargo doc --no-deps`, and
`cargo test` (37 tests: 17 behavior, 7 CLI, 4 public integration, 3 freshness,
5 generated-contract, 1 isolated Signal-without-Datom).

Configured remote `nix flake check -L` passes package, build, test, format,
clippy, docs, policy, and the meaningful producer declaration gate. That gate
generates all four current declarations: Protos root and kinds, and Datom root
and kinds, using the configured remote builder.

## Sources

- `/home/li/primary/Vision/protos.md`
- `/home/li/primary/Vision/datom.md`
- `/home/li/primary/Vision/ethos.md`
- `/home/li/primary/flows/564f55/reports/landing.md`
- Protos runtime `aac95b0d08a4c7eb7f73c8ea18309f9e2e89315f`; declaration `d5616342f5c4654deda3af3858bad68af8b68ce8`
- Datom runtime `35d26d822870356af9b04cacfec40d85600b541d`; declaration `35d26d822870356af9b04cacfec40d85600b541d`
