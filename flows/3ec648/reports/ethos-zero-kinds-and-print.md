# ethos-zero: capability inputs are kinds; the print expands vertically

Repository: /git/github.com/LiGoldragon/ethos-zero, started from remote main
cf7dd128bcae (13.0.0). The local checkout was a stale detached HEAD (4bf73ca);
work was done on a new change over main@origin. Orchestrate lock 11485 held
on the repository for the work.

## Commits (on main, pushed)

- fac6b5869902 Take kinds as capability inputs; refuse concrete input types. Version 14.0.0.
- 2db764d200da Print ethos vertically, hanging, closers on the last line. Version 14.1.0.

New version: **14.1.0** (14.0.0 is the breaking change; 14.1.0 adds the printer).

## 1. Capability inputs are kinds (14.0.0)

- New module `src/signature.rs`: a reference in a capability's signature
  stands as Kept (Self, a head parameter, an associated type), Bounding (a
  kind: the method takes a parameter bounded by it), Bound (a kind an
  associated type of the enclosing kind is already bounded by, written
  `Self::Item`), or Concrete.
- Checking (`src/checking.rs`): a Concrete input is refused with the new
  `Problem.KindWanted.String` (added to `error.ethos`, `src/error.rs`
  regenerated), at the input's path, so Rejected names its line and column.
  A kind in an input or a yield is checked in the Kind role and accepted.
- Generation (`src/generation.rs`): each kind in an input or the yield gets
  its own method parameter, lettered from N (past the head's parameters):
  `resolve.{ [ Textualizable ] [ Self ] }` gives
  `fn resolve<N: Textualizable>(&self, input: N) -> Self where Self: Sized;`.
- Concrete means: a declared type, an intrinsic other than Self/Sized
  (`String`, `Vector<Self>` too), or a `protos:` intrinsic. An imported
  name carries no role: in an input it is taken as a kind, in a yield as a
  type. That is a choice I made, see open questions.
- Examples updated: `fixtures/capability-kinds.ethos` (`push!{ [ Summarizable ] … }`),
  its implementing test in `tests/generated.rs` (`push<N: Summarizable>`,
  which takes a `Line` and another `Buffer`), the unit-test sources in
  `src/lib.rs` and `tests/ethos.rs`, README "Kinds" section, new `UPGRADES.md`.
  `ethos-zero.ethos` has no capabilities; its Error contract gains `KindWanted`
  through `error.ethos`.

### Refused-contract list (also in UPGRADES.md)

Method: every `.ethos` under /git (137 files) generated with the 13.0.0
build and the 14.0.0 build, replies and outputs compared.

- Refused by 14.0.0 and accepted by 13.0.0: **none**.
- Concrete types in inputs that are imported names, so not refused but now
  generated as bounds on a struct, which rustc will refuse when those repos
  regenerate:
  - `github.com/LiGoldragon/protos/protos-kinds.ethos`: `protosize_with!{ [ ReaderBudget ] … }`.
  - `github.com/LiGoldragon/datom-codec/datom-codec-kinds.ethos`: `[ Path ]`
    (datom_form, datomize), `[ Datom Budget ]` (compose:), `[ Positions ]`
    (from_positions), `[ Budget ]` (compose, compose_positions, actualize).
  - The vendored copies in `primary-next/tools/messaging-codec/vendor/{protos,datom-codec}/`.
- Newly accepted: `primary-next/flows/f6db8d/witnesses/substrate/probe-ethos/sized-kind.ethos` (`c:[ Sized ]`).
- Three Signal files (meta-signal-flow, signal-message, meta-signal-message)
  differed between the two scans. A rerun shows identical output from both
  versions, so the files were changing under other flows during the scan.
- Those repositories were not changed.

### Test evidence

- Seen failing first: 5 new tests in `tests/ethos.rs` failed against the
  unchanged generator (kind in input, kind in yield, two kinds as two
  parameters, associated-type binding, concrete refusal). A 6th test,
  `self_and_the_kinds_own_parameters_stay_as_they_are`, passed from the
  start as a regression guard.
- Then passing. A CLI test locates `KindWanted.Rec` at `{ 4 28 }` in a
  vertical file.

## 2. Vertical print (14.1.0)

- New module `src/printing.rs` and public kind `Printable` (for `File` and
  `protos::Protos`). The rule: a structure with more than one element, one
  of which has a next layer (headed, or a brace or bracket), opens on its
  line, and its elements hang aligned beneath the first. The closer ends the
  last line. Leaves stay on one line. There is a space inside non-empty
  brackets, an empty one is `[]`/`{}`, and an angled enclosure stays tight
  (`Vector<Event>`). A file prints in the sweet form with comments dropped.
  Leaves are written by the protos writer. The new module only lays out lines.
- Fix needed for the print: the File ascent wrapped a typed variant with
  arguments in braces (`Generated.{ Vector<String> }`), which reads back as
  a struct variant, so the ascent was lossy (tree-types fixture). Variants,
  superkinds, bounds and associations now emit the reference and its angled
  arguments as siblings (`src/protosization.rs`).
- The self-description (no-argument CLI) now prints `ethos-zero.ethos`
  through the printer. `ethos-zero.ethos` and `error.ethos` were rewritten
  in the canonical print (comments kept in source).
- Fixtures: `fixtures/print/flow-{library,signal,operation,memory}.ethos`,
  the vision-ethos Flow Nexus text verbatim. I dropped the Operation line's
  comment because comments are not printed.
- Tests (`tests/print.rs`, 9): the four files round-trip byte-identical at
  the protos layer. Only the Library is conceived by ethos-zero, and it also
  round-trips through `File`. Signal is refused (`Brief.String` as a struct
  position), and Operation/Memory are not ethos-zero roots. Other tests:
  every fixture prints, reads back to the same File and prints the same; the
  crate's own ethos is canonical; references with arguments print as written.
  All 6 initial tests failed against a one-line stub. The CLI self-description
  test failed before main.rs changed. The own-ethos test failed against the
  old error.ethos.

## Gates

- `cargo test`: all suites green (lib 18, cli 14, ethos 24, freshness 3,
  generated 18, print 9, signal-without-datom 2). `cargo fmt --check`,
  `cargo clippy --all-targets -D warnings`, `cargo doc -D warnings` and the
  two guard scripts are clean locally.
- `nix flake check`: **not completed**. The run went over its 20-minute timeout while it was still copying the toolchain (gcc, glibc, python) from cache.nixos.org, before any ethos-zero derivation had built. No check failed, and no check passed. The run was not repeated, as the brief says.

## Open questions

- "Make it the one Check uses": Check prints only its datom reply
  (`Checked.<path>` / `Rejected.{ … }`), and it prints no ethos. I left CLI
  replies on one line, because they are datom, not ethos, and the
  dependency-ethos check and consumers match them. The printer is used by
  the self-description and the File. Making replies vertical, or adding a
  Print query, is yours to rule.
- An imported name in an input is taken as a kind. Ethos has no role on an
  import, so ethos-zero cannot refuse `crate:Path` there. The cost is
  rustc's refusal at regeneration in protos and datom-codec.
- protos owns "the only character writer". The vertical layout lives in
  ethos-zero on top of the protos writer. Moving it into protos would need a
  protos change and a repin.
- vision-ethos's "nothing with a next layer sits on one line" was read as:
  one element with a next layer stays inline with its bracket
  (`[ flow:[ FlowId Voice Event ] ]`). Several elements expand when any one
  has a next layer. This reproduces the vision example exactly.

## Sources

- /home/li/primary/flows/3ec648/rulings.md (rulings 3, 4)
- /home/li/primary/flows/3ec648/witnesses/ethos-zero-today.md
- /home/li/primary/flows/3ec648/reports/handover-state.md (the deep-dive form B/C)
- vision-ethos, knowledge-ethos, protos skills
- ethos-zero commits fac6b5869902, 2db764d200da; UPGRADES.md there
- Scan outputs: scratchpad scan-old/, scan-new/ (13.0.0 vs 14.0.0 over /git)
