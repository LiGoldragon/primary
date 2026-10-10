# Datom codec final integration

Datom codec 0.22.0 pins Protos `1bf659e5489cf1ac05cc293ee2e8068774fb48bd`.
The shared budget now carries Protos's reader budget into structural reading,
and a qualified structural head is preserved as non-variant input so an
ordinary Datom variant rejects it at its own path.

The earlier scalar cases remain covered: timestamps and `Ada:one` read as
strings; `Some.42` reads as either `Option<String>` or `Option<i64>`;
`3.14` and `Some.3.14` read as decimals; writers retain flat `Some` bodies.

## Sources

- `/git/github.com/LiGoldragon/datom-codec` commit `cd0255d774847826d53d063ab856ebe0dd09e250`
- Protos commit `1bf659e5489cf1ac05cc293ee2e8068774fb48bd`
