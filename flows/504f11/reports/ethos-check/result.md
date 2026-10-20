# Ethos check, Proposals 2 to 6

Files in this directory: NAME.ethos (as written, "+ " removed) and NAME.braced.ethos. `run.sh` runs Inspect.

## Inspect
| file | as written | braced |
|---|---|---|
| library | Rejected, line 2 col 1, `Structural.ProtosError.{ Extent.{ 51 51 } Multiple }` | Inspected |
| signal | Rejected, 2:1, Extent 46 46, Multiple | Inspected |
| operation | Rejected, 2:1, Extent 45 45, Multiple | Inspected |
| memory | Rejected, 2:1, Extent 44 44, Multiple | Inspected |
| meta-signal | Rejected, 2:1, Extent 42 42, Multiple | Inspected |

The message "Multiple" means several top-level items. The root head on line 1 is followed by sections as sibling items, so the file is not one root.

## Braced form (the only change)
Line 1 `Library   ; c` becomes `Library.{  ; c`. A line `}` is added at the end. The `}` goes on its own line because the last line ends in a comment. Same for Signal, Operation, Memory.

## Minimal changes needed beyond the braced root
None. All five braced files are Inspected unchanged. The four points you named:
- `Arc.num_rational:Rational64`: parses, generates `pub type Arc = num_rational::Rational64;`. No change.
- `Relative.{ Body Body }`: parses, generates `Relative_Data` and `Reading::Relative(Relative_Data)`. No change.
- `chronos:[ ... ]` imports: parse, generate `chronos::Reading` etc. No change.
- Comments on their own lines: the files have none (all comments trail a line), so this was not exercised. A comment between sections was not tested.

## Conform
- `Conform.{ «library.braced.ethos» Reading «Relative.{ Sun Moon }» }` gives `Conformed.{ Reading «Relative.{ Sun Moon }» }`.
  - `Reading «Absolute.Sun»` gives Conformed.
  - `Relative.{ Sun }` gives `Unconformed ... Composition [ 1 ] Arity.{ 2 1 }` (negative control works).
- Signal file: Inspect names the queries type `Query`. Its variants are `Tell(Tell_Data)` and others.
  - `Query «Tell.{ [ Absolute.Sun ] None }»` gives `Unconformed.{ Query Error.{ Composition [ 1 0 0 ] Form.{ Reading Variant } } }`.
  - The failure is at the element of the Vector, whose type `Reading` is imported from chronos. The checker cannot see inside an imported type and expects a bare form.
  - `Tell.{ [ ] None }` gives Conformed, so the shape of Tell and `None` is accepted.
  - `Tell.{ [ ] Some.Foo }` gives `Composition [ 1 1 1 ] Form.{ Moment Bare }`, the same import limit.

## Edition 3 (03-chronos-golden-example-3.md, already braced)
Files: ed3-library.ethos, ed3-signal.ethos, ed3-operation.ethos, ed3-memory.ethos, ed3-meta-signal.ethos.
Inspect: all five Inspected, no rejections.
Conform: `Conform.{ «ed3-library.ethos» Reading «Relative.{ Sun Moon }» }` gives `Conformed.{ Reading «Relative.{ Sun Moon }» }`.
