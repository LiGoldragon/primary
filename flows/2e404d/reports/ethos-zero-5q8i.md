# ethos-zero 5q8i: rulings 1 and 7

Branch `5q8i-2e404d` of github.com/LiGoldragon/ethos-zero, head `970459d100ddee5f62a76c05642ecfabefba6329`, version 28.0.0, built on main `8c95310` (27.0.0). It is pushed to the branch only and is not merged to main.

Gate: `nix run github:Mic92/nix-fast-build -- --remote prometheus --no-nom --no-download --eval-workers 1 --flake 'git+file:///git/worktrees/ethos-zero-5q8i-2e404d?rev=970459d…#checks.x86_64-linux'` exited 0. All 13 checks pass, including fmt, freshness, flow-contract and flow-contract-datom, and signal-without-datom. Log: `/home/li/primary/flows/2e404d/ethos-zero/gate-970459d.log`. Cargo.nix was regenerated with build-base's crate2nix through the flake dev shell; only the crate's own version line changed.

## Ruling 1: `Lock.LockRequest` beside a type `Lock`

The carrying rule now applies only to a bare variant. A variant with its own payload, whether `Lock.LockRequest`, `Code.Code`, `Code.{ … }` or `Code.[ … ]`, is accepted beside a declared or imported type of the same name in every section. It generates `Input::Lock(LockRequest)`, `Code(Code)`, `Code(Code_Data)` and so on. The `Payload` refusal (the `Refusing` trait in checking.rs) is removed, and so is `Problem.Payload`. `fixtures/lock-signal.ethos` is the vision's Signal word for word; it is generated into `tests/generated/lock-signal.rs` and compiled together with every other fixture.

## Ruling 7: field names and namespaces

Finding: the brief's premise does not hold. In 27.x a namespace never enters a field name: `field_base` uses only `Reference.name` and ignores `source`. `orchestrate_nexus_configuration_configuration_state` comes from `ConfigurationState<OrchestrateNexusConfiguration>`, where `OrchestrateNexusConfiguration` is the type argument and not a namespace. That name is the vision's constructed-type rule (type-first, like `string_vector`), applied exactly. 28.0.0 leaves field naming unchanged. If Fable wants `configuration_state` there, that is a change to the vision's `string_vector` / `lock_option` rule, and it is Fable's to make.

What was really missing was the collision guard. 27.x silently generated `Pair.{ String String FirstString }` with two `first_string` fields, which Rust then refuses to compile. Checking now names every struct's fields exactly as generation does: types-section structs, structs declared in place, and inline variant payloads in every root. The later of two colliding positions is refused as `Conceptual.{ <path> DuplicateField.<field> }`. Through the CLI the refusal reads `Rejected.{ <file> { line column } … DuplicateField.first_string }`. `Problem.DuplicateField.String` takes Payload's slot in error.ethos.

## Tests added or changed

- tests/ethos.rs:
  - `a_variant_named_as_a_defined_type_declaring_a_payload_carries_that_payload` and `a_root_section_variant_named_as_a_defined_type_declaring_a_payload_carries_that_payload` replace the two refusal tests.
  - `the_vision_lock_signal_takes_lock_beside_a_declared_lock` is new.
  - `a_bare_variant_named_as_an_imported_type_carries_it` now has `Block.Block` accepted.
  - `a_field_is_named_for_its_type_alone_never_its_namespace` is new.
  - `positions_whose_fields_would_meet_are_refused_at_the_later_position` is new. It covers a Library struct, a struct declared in place, an enum variant payload, a Signal input and a Memory record.
  - `a_repeated_type_is_told_apart_as_first_and_second` is new.
- tests/cli.rs: `check_takes_a_variant_named_as_a_defined_type_declaring_a_payload` replaces the old location test, and `check_locates_positions_whose_fields_would_meet_naming_the_file_and_the_field` is new.
- The fixture counts in freshness.rs (23) and print.rs (25) are updated. `tests/generated.rs` mounts `lock_signal`.

Every generated file the crate carries was regenerated. Only `src/error.rs` changed (one variant), and `tests/generated/lock-signal.rs` is new.

## Consumer blast radius

Each consumer's `.ethos` files were generated with 27 (main `8c95310`) and with 28 (`970459d`) and the outputs compared. No consumer files were changed. Across the named set and a sweep of all 80 repositories that name ethos-zero (174 files), no file that 27 generates comes out different under 28. No field name changes, and no file is newly refused as `DuplicateField`. The only effect is that files 27 refused as `Payload.<Name>` now get past that refusal.

| consumer @ rev | files | generated output changed | note |
|---|---|---|---|
| flow @ ethos27-e3a7d1 6e44e303 | 13 | none | |
| flow @ main 967f2f52 (= ethos27-896bac) | 12 | none | |
| signal-flow @ 4982eeb | 2 | none | |
| meta-signal-flow @ cdb4e7d | 2 | none | |
| signal-curriculum-nexus @ ethos27-896bac 4358aa1 | 1 | none | |
| Curriculum @ 1b6c454 | 3 | none | |
| orchestrate @ ethos27-2e404d e78534f | 3 | none | memory.ethos's field is unchanged |
| signal-orchestrate @ ethos27-2e404d 8335cf9 | 1 | none | |
| meta-signal-orchestrate @ ethos27-2e404d 055950b | 1 | none | |
| energy-nexus @ 2623947 | 4 | none | operation.ethos: 27 refused it as `Payload.Reading`; 28 generates it |
| signal-energy-nexus @ 7ca10eb | 1 | none | refused by both (`Duplicate.Input`) |
| meta-signal-energy-nexus @ 3264d6f | 1 | none | refused by both; 28 gets past `Payload.Threshold` to `Duplicate.Input` |
| herdr-nexus @ c0bcca1 | 10 | none | meta-call and public-call refused by both (`Duplicate.Input`) |
| signal-herdr-nexus @ 813d329 | 1 | none | refused by both; 28 gets past `Payload.Unknown` to `Wrapping.{ Unknown Pane }` |
| meta-signal-herdr-nexus @ 2d96171 | 1 | none | |
| belief-nexus, signal-belief-nexus, meta-signal-belief-nexus @ main | 3 | none | refused by both (`Undeclared.Query`) |
| message, signal-message, meta-signal-message @ ethos27-e3a7d1 | 4 | none | |

nexus @ ethos27-2e404d tracks no `.ethos` file, so there was nothing to measure. Outside the named set, these files now generate where 27 refused them: chronos, clavifaber, horizon-rs, lojix ingress, meta-signal-introspect, meta-signal-persona, meta-signal-terminal, signal-criome, signal-introspect, orchestrate main's two clients, signal-orchestrate main, and two ethos-test fixtures. The full tables are `/home/li/primary/flows/2e404d/ethos-zero/radius-named.tsv` and `radius-all.tsv`, and the script is `radius.sh`.

Before merging to main: `Problem::Payload` disappears from the public `Error` contract. A consumer that matches `Problem` exhaustively must replace that arm with `DuplicateField`. UPGRADES.md 28.0.0 says so.
