# References: Chronos, second edition

Source: flows/984e88/books/02-chronos.md. Not rendered. Builds on references/01-chronos.md, whose provenance, archive and destroy entries and Chronos 0.3.0 survey stand.

## The living's two comments on Proposal 2

- flows/984e88/vision/ethos.md, 2026-10-14, the last record: fraction or angle library; a hand-maintained, specified vector of types imported from Rust that the Ethos-to-Rust compiler links against, like built-ins; later, programmatic feedback naming where each type comes from. Anchored on `Decimal` in `Location`.
- flows/984e88/vision/chronos.md, 2026-10-14, the last record: sign and nakṣatra are not kept; they are methods or obtained by a request on an arc; absolute and relative positions; the lunation at 31° between Sun and Moon reads as Taurus. Relayed with "elevation" kept [sic].

## Where they land

- Proposal 1, new section Positions are arcs: from the chronos.md record. Archive of that record on approval.
- Proposal 3, two paragraphs under Imports in vision-ethos, after the intrinsic names line: from the ethos.md record. Archive on approval. Related earlier psyche on a core library of built-ins and a registry of manifests (flows/*/vision/ethos.md, "inline import ... core built-ins ... registry") is not crystallized here.
- Proposal 2 (anatomy), 4 (vector shape), 5 (angle type), 6 (arc print), 7 (derivation route): machine design following both comments; Proposal 7's option 2 is the "request on an arc" reading of the chronos.md record.

## Crate findings

Read 2026-10-15 by a read-only subflow, two facts spot-checked by the author (the chronos lock, and num-rational's Eq and Hash).

- chronos `Cargo.toml` (/git/github.com/LiGoldragon/chronos) names anise "0.10", hifitime "4", solar-positioning "0.5". `Cargo.lock`: anise 0.10.6, hifitime 4.3.1, solar-positioning 0.5.3, num-rational 0.4.2 (transitive; not in Cargo.toml). Witnessed by the author.
- anise 0.10.6: no angle type. `src/math/angles.rs` has free functions on f64: `between_0_360` (line 22), `between_0_tau` (33), `between_pm_180` (37). `src/math/units.rs` has only `LengthUnit`. Witnessed by the subflow in ~/.cargo/registry.
- hifitime 4.3.1: no angle, degree or radian anywhere in `src`; Duration and Epoch only. Witnessed by the subflow. Epoch is a later candidate for `Instant`; not proposed.
- solar-positioning 0.5.3: `SolarPosition { azimuth: f64, zenith_angle: f64 }` (`src/types.rs:130`), private fields, derives Debug, Clone, Copy, PartialEq; no angle newtype. Witnessed by the subflow.
- num-rational 0.4.2: `Ratio<T>` (`src/lib.rs:51`); `impl<T: Clone + Integer> Eq` and a hand-written `Hash` that agrees with Eq for unreduced ratios (lines 408 to 414, read by the author); serde feature; no rkyv in its Cargo.toml (grep by the author, empty). `Rational64` alias inferred from docs, not grepped.
- turns 0.1.2 (crates.io, updated 2026-05-18, created 2026-04-19, 164 downloads): `turns::Angle<T>(pub T)` (`lib.rs:41`), unsigned integer, the full range one turn; aliases Angle8 to Angle128; `from_degrees` (69); derives PartialEq, Eq, Hash, Default, Copy (40); serde only. Read from the downloaded tarball by the subflow.
- uom 0.38.0 (2026-02-14): `Quantity<D,U,V>`, storage chosen by feature, rational64 among them; Eq (`system.rs:1007`) and Hash (1015) bounded on V; serde; no rkyv. The plane angle module was inferred, not opened.
- fraction 0.17.0 (2026-08-22): `GenericFraction<T>` enum with NaN and infinity variants; Eq and Hash; serde under `with-serde-support`; no rkyv.
- angular-units 0.2.4 (2018-11-21): `Deg<T>`, `Rad<T>`, `Gon<T>`, `Turns<T>`; PartialEq, PartialOrd, Hash, no Eq.
- angle 0.5.0 (2022-03-29): `Deg<N>`, `Rad<N>`; no Eq or Hash. Its rkyv status not checked.
- measurements 0.11.1 (2025-10-18): `Angle`, f64 (inferred); Copy, Clone, Debug, Default only.
- fixed 1.31.0 and corvid_fixed 0.1.2: fixed-point numbers, not opened.
- None of the candidates whose manifests were read names rkyv; hence the per-type adapter in Proposal 4. That an adapter crate is needed apart from datom-codec follows from the Nexus compiling without datom-codec (knowledge-ethos); the adapter name `ethos_imports::Ratio` is a placeholder.
- Generated types derive rkyv Archive, Serialize, Deserialize, Clone, Debug, PartialEq, Eq and Hash (knowledge-ethos), which is why an f64-carrying angle cannot be a field type without a wrapper.

## The choices, from the first edition

- 3.1 solar and lunar formats: re-posed as Proposal 8 for arcs; the lunation default follows the living's lunation example.
- 3.2 became Proposal 9, unchanged.
- 3.3 where the count starts: removed. Signs and nakṣatras are named enums, derived; an arc is degrees from 0°.
- 3.4 how a position prints: re-posed as Proposal 6, how an arc is written in datom.
- 3.5 became Proposal 10, unchanged.
- 3.6 became Proposal 11, with `Body` replaced by `Reading`.
- 3.7 became Proposal 12, unchanged; spans still unchecked machine knowledge.
- 3.8 became Proposal 13, unchanged.
- 3.9 became Proposal 14, unchanged.

## Figures

- The watch figure of the first edition drew its horizontal branches as arrows into box corners; the builder read their verbs as bare nodes. Redrawn in the builder's fork form (a bar with legs, verbs beside the legs); every verb now parses as an edge verb (checked with ascii-graph on 2026-10-15).
- The derivation figure is new: Moon 151°, Sun 120°, lunation 31°, Taurus 1°, Kṛttikā 4°20′ (26°40′ + 4°20′ = 31°).

## Build notes

- book-build.clj accepts `###` only as `### Proposal N: title`, so every choice is its own proposal with a numbered ruling.
