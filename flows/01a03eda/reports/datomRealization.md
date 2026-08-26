# Latest Datom vision realization

The latest directly ruled Datom surface from `ac1e9ec8` was implemented and pushed.

- Protos `1e0890175319`, version 0.7.0: headless guillemet structural blocks, tests, documentation, and upgrade instructions.
- Datom `bc16426703fa`, version 0.3.0: guillemet maps without a `Map.` head and type-directed roots. Enum text begins at its variant; record text begins directly at `{…}`.

The implementation preserved the existing map-entry model. It did not introduce positional key/value pairs because that was an inference in the remembered flow, not a direct ruling by the living.

The changed external fixture was first witnessed failing with `DatomFault { problem: Shape }`. After implementation, the Protos and Datom local suites passed, as did `nix flake check -L --no-write-lock-file` for each repository through the configured remote builder. Both PathLocks were released and both repositories were reported clean.

## Sources

- Flow `ac1e9ec8`, especially the originating transcript records for typed maps without `Map`, guillemet selection, and enum-root behavior, and `vision/datomSyntax.md`.
- Protos revision `1e0890175319`.
- Datom revision `bc16426703fa`.
- Realization subflow `/root/realize_latest_datom` and its implementation child.
