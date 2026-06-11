# Scope NOTA Correction

Operator correction report for the recursive `DomainScope` deployment on 2026-06-11.

## Correction

Report `reports/operator/366-recursive-domain-scope-deploy-2026-06-11.md` claimed that live Spirit accepted this scope form:

```nota
(Technology Software)
```

That was wrong. The only reason it worked was that I had generated a custom NOTA path parser in `schema-rust-next` for scope enums. That violated the schema/NOTA discipline: scope values must use the ordinary schema-emitted recursive enum codec, not handwritten path parsing, and the text surface must not hide a stop marker behind custom parsing.

## Correct Shape

`DomainScope` is now a normal recursive enum text surface.

Valid scope forms:

```nota
(Technology All)
(Technology (Software All))
(Technology (Software (Engineering SoftwareArchitecture)))
```

Invalid shortcut form:

```nota
(Technology Software)
```

Live Spirit now rejects the shortcut with:

```text
spirit: invalid NOTA input: unknown TechnologyScope variant Software
```

## Implemented

- `schema-rust-next` commit `0bc4591f` (`schema-rust-next: use derived NOTA for recursive scopes`)
  - Removed generated `nota_next::Block` path parsing for scope enums.
  - Removed manual `impl NotaEncode for DomainScope`.
  - Emitted normal `nota_next::NotaDecode` / `nota_next::NotaEncode` derives for scope enums.
  - Replaced hidden `This` terminal variants with explicit `All` variants.

- `spirit` commit `980e73ba` (`spirit: use ordinary NOTA for domain scopes`)
  - Repinned `schema-rust-next` to `0bc4591f`.
  - Regenerated `src/schema/domain.rs`.
  - Bumped Spirit to `0.9.2`.
  - Added regression coverage that `(Technology Software)` fails and the explicit `All` forms round-trip.

- `CriOMOS-home` commit `a65af681` (`home: pin spirit scope NOTA correction`)
  - Pinned Spirit to `980e73ba`.
  - Pinned the nested Spirit `schema-rust-next-source` input to `0bc4591f`.
  - Activated the corrected generation locally on `ouranos`.

## Verification

Schema generator:

```text
cargo test
```

Spirit:

```text
cargo test --features nota-text
cargo test --no-default-features
cargo test --features production-migration
cargo clippy --all-targets --features agent-guardian,production-migration,testing-trace -- -D warnings
nix build .#default
```

CriOMOS-home:

```text
nix build .#checks.x86_64-linux.spirit-deployment
lojix-run '(HomeOnly goldragon ouranos li [/git/github.com/LiGoldragon/goldragon/datom.nota] [github:LiGoldragon/CriomOS-home/main] Activate None None)'
```

Live daemon:

```text
spirit Version
(VersionReported (0.9.2 (1457 6719775989566111262)))

spirit '(Count ((Full [(Technology All)]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
(RecordsCounted (12 (1457 6719775989566111262)))

spirit '(Count ((Full [(Technology (Software All))]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
(RecordsCounted (12 (1457 6719775989566111262)))

spirit '(Count ((Full [(Technology (Software (Engineering SoftwareArchitecture)))]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
(RecordsCounted (5 (1457 6719775989566111262)))

spirit '(Count ((Full [(Technology Software)]) Any Any Any None (Exact Zero) (AtLeastCertainty Minimum) Any))'
spirit: invalid NOTA input: unknown TechnologyScope variant Software
```

Services:

```text
agent-daemon.service: active/running, NRestarts=0, ExecMainStatus=0
spirit-daemon.service: active/running, NRestarts=0, ExecMainStatus=0
```
