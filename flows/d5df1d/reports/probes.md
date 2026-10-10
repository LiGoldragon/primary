# Probes the book «Ethos invariants» relies on

Purpose: rerun on a Nix build of ethos-zero c2653d, to settle whether the binary the audit probed behaves as that revision does. The audit ran each file below through the existing local binary `target/debug/ethos-zero` (mtime 2026-10-04) of the ethos-zero checkout at c2653d. Command for each, with `out` an empty directory:

```
ethos-zero 'Generate.{ /abs/<file>.ethos /abs/out }'
```

The reply in each case was `Generated.[ /abs/out/<file>.rs ]`. Each file is given whole, as it ran. Expected observations are what the audit saw in the generated Rust; a rerun matches when each holds.

## golden.ethos

```
Library                       ; Flow Nexus types
[]                            ; imports: none
[                             ; types
  FlowId.{ String }           ; one flow, by id
  Layer.[                     ; decides the model
    Primary
    Secondary
    Tertiary
    Quaternary ]
  Details.{                   ; a metaflow's state
    Layer
    Topic.{ String }          ; Core when none
    State.[                   ; where it stands
      Awake.FlowId            ; its current flow
      Asleep                  ; a request wakes it
      Ended ]
    Past.{ Vector<FlowId> } } ; oldest first
  Metaflow.[                  ; one per aspect
    Psyche.Details
    Mind.Details
    Field.Details ] ]
[                             ; kinds
  Layered.[ layer.[ Layer ] ] ; sits at a layer
  Wakeable.{                  ; can be woken
    [ Layered ]               ; superkinds
    []                        ; associated types
    []                        ; constants
    [ wake![ FlowId ] ] } ]   ; yields its flow
[                             ; associations
  Metaflow.[ Wakeable ] ]     ; a metaflow wakes
```

Expected:
- G1. Generated, not refused. `pub struct FlowId { pub string: String, }`, `pub struct Topic { pub string: String, }`, `pub struct Past { pub flow_id_vector: std::vec::Vec<FlowId>, }`: three single-field structs. Supports the row "A struct of one position is refused: not enforced (probe)".
- G2. Every `pub struct` and `pub enum` is preceded by `#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]`. Supports "Every struct and enum bears both datom traits: enforced" and Proposal 9 ("The generator derives `Composing`").
- G3. The file ends with `const _: () = { fn assert_metaflow_wakeable<T: Wakeable>() {} let _ = assert_metaflow_wakeable::<Metaflow>; … }`. Supports "An association asserts at compile time: enforced (probe)".
- G4. `std::vec::Vec<FlowId>` written fully qualified; no `use` line. Supports "Names fully qualified, no imports in Rust: enforced (probe)".
- G5. Field `flow_id_vector` for `Vector<FlowId>`. Supports "Fields named after their types: enforced (probe)".
- G6. `fn wake(&mut self) -> FlowId` in `trait Wakeable`. Not a book row; a check of the read.

## fnmem.ethos

The Memory section of «The Flow Nexus vision», with its undeclared `Event` replaced by `String`.

```
Memory                          ; Flow's
[  flow:[ FlowId Request ] ]
[  Metaflow.[                   ; one variant per
      Psyche.Details            ; aspect; the struct
      Mind.Details              ; holds its details
      Field.Details ]
   Details.{
      Layer.[                   ; decides the model
         Primary
         Secondary
         Tertiary
         Quaternary ]
      Topic                     ; Core when it has
                                ; no topic of its own
      State.[
         Awake.FlowId           ; its current flow
         Asleep                 ; a request wakes it
         Ended ]
      Past.Vector<FlowId>       ; oldest first
      Queue.Vector<Request> }   ; waiting, oldest
                                ; first
   Topic.Dense
   Dense.String                 ; PascalCase
   Flow.{                       ; one per run
      FlowId
      Session.String            ; the harness's id
      Events.Vector<String> } ]
```

Expected:
- F1. Generated. `pub type Topic = Dense;` and `pub type Dense = String;`: a wrap of a wrap accepted. Supports "No double wrapping: not enforced (probe)".
- F2. `Awake(flow::FlowId)` and `pub type Past = std::vec::Vec<flow::FlowId>;`: imported names qualified by source. Supports G4's row.

## s2.ethos

```
Library
[]
[ Deep.[ A.[ B.[ C.[ D.[ E.[ F G ] ] ] ] ] ]
  Low.[ lowvariant Other ]
  Under_Score.{ String Integer }
  Unit.{} ]
[]
[]
```

Expected:
- S1. Generated, no comment anywhere in the file. Supports "A comment on every section and layered line: not enforced (probe)".
- S2. Six enum levels on one line accepted: `pub enum Deep`, `A_Data`, `A_Data_B_Data` … `A_Data_B_Data_C_Data_D_Data_E_Data { F, G }`. Supports "Each element on a new indented line: not enforced (probe)" and "Inline until too deep: not enforced (probe: six levels accepted)".
- S3. `pub struct Under_Score { … }` generated. Supports "Inline payload named with an underscore: partly; an authored underscore name is accepted (probe)".
- S4. `pub enum Low { lowvariant, Other, }` and `pub struct Unit {}`. Not book rows.

## m2.ethos

```
Library
[ std:Mutex ]
[ Lock.{ Mutex<String> Integer } ]
[]
[]
```

Expected:
- M1. Generated, no comment in the file; field `pub string_mutex: std::Mutex<String>`, no `use`. Supports S1's and G4's rows. (The Mutex row itself rests on flows/1d0733/reports/mutex-probe.md, run on a Nix build, not on this binary.)

## Not relied on by the book

single.ethos, mutex.ethos and m3.ethos were also run. The book's rows do not rest on them: the lowercase refusal (single.ethos) is not a row, and the Mutex import refusals (mutex.ethos, m3.ethos) are superseded by the 1d0733 report.

## Sources

- Probe files and outputs: /tmp/claude-1001/-home-li-primary/d5df1daf-854d-4469-8700-0997eb3babb1/scratchpad/probes (scratch, not durable; inputs copied whole above).
- /home/li/primary/flows/d5df1d/reports/ethos-audit.md, section 3.
- /home/li/primary/flows/d5df1d/books/invariants.md, the table and Proposal 9.
- Provenance receipt: unavailable (no PROVENANCE handoff).
