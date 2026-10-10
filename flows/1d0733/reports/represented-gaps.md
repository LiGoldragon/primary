# Represented gaps closed: roles of imported names

Build host: `hostname` over ssh returned `prometheus` for every cargo and nix run. The scratch trees are `/tmp/rg/b` (bare, 2e13b3d on 21da35b) and `/tmp/rg/br` (braced, d844d23 on 406410c) on Prometheus, with no remotes. Nothing was pushed or landed, and nothing in Primary was committed.

## How roles are read

- **Finding the declarations.** A new `build.rs` runs `cargo metadata --offline --filter-platform $TARGET` on the crate. For each direct normal dependency, it takes every `.ethos` file at the root of that dependency's package directory. It embeds them with `include_str!` into `$OUT_DIR/dependencies.rs` as `Dependency { source, declarations }`. The source is the dependency's crate name. One alias table adds `datom` for `datom_codec`. The result is that `protos` gets protos.ethos and protos-kinds.ethos, and `datom_codec` and `datom` both get datom-codec.ethos and datom-codec-kinds.ethos. These are the same files the dependency-ethos check passes to the tool, at the revision Cargo built against. Under Nix they come from crane's vendored sources. The build dependency is `serde_json = "1"`, which adds 32 lines to Cargo.lock.
- **Reading them.** `Dependencies::known()` (src/conception.rs, behind a `OnceLock`) reads each declaration the way the tool reads any file, as far as the concept: canonicalize, then protosize, then `Conceiving<File>`. It does not learn roles from the declaration's own imports. `Knowing::role(source, name)` resolves the name in each declaration of that source. A declared type is `Role::Type`, a declared trait is `Role::Trait`, and an import, an intrinsic or an undeclared name has no role. datom-codec-kinds.ethos declares `Represented` as a trait.
- **Conception.** `Ethosizable<File>` conceives the file, then learns roles. Every `Imported` gets `role: Option<Role>`, taken from its source and emitted name. In the text, an import stays a bare name; the print ignores the role.
- **Checking.** `Reference::refer` takes the learned role of an imported name, where until now it accepted whatever role was asked. An inline-sourced reference (`datom:Represented`) is looked up in `Dependencies` directly. Every role mismatch at that site raises `Role::wanted()`, the role the position wants: `Expected.Type` where a type is wanted, `Expected.Trait` where a trait is wanted. This applies to locally declared names, imported names and intrinsics alike. A name its source does not declare (`crate:`, `std:`, `super:`, `datom:Error`) keeps the role its position asks.
- **Signature stance.** src/signature.rs treats a name like a local one when its role is known: a type stands concrete, a trait binds. An unknown role keeps the earlier rule: a trait in an input, a type in a yield.
- **Form and Problem.** `Form` had no `Type` value, so `Type` was appended to error.ethos's Form. No Problem was added. `Problem::Role` is removed: its `Role.String` line is gone from error.ethos, and src/error.rs was regenerated to match. No source or test refers to it. UPGRADES.md keeps its 13.0.0 entry, which records the output of that release.

## Problems observed

| Source | Problem, path |
|---|---|
| `[ datom:[ Represented ] ] [ Ticket.Represented ]` | Expected.Type, [1 1 0 1] |
| `[ datom:[ Represented ] ] [ Tickets.Vector<Represented> ]` | Expected.Type, [1 1 1 0] (the angled sibling) |
| `[ datom:[ Represented ] ] [ Holder.{ Represented Integer } ]` | Expected.Type, [1 1 0 1 0] |
| `[] [ Holder.{ Integer datom:Represented } ]` | Expected.Type, [1 1 0 1 1] |
| `[] [ Holder.{ Shown Integer } ] [ Shown.[ show.[ String ] ] ]` | Expected.Type, [1 1 0 1 0] |
| `[ datom:[ Path ] ] [ Ticket.Integer ] [] [ Ticket.[ Path ] ]` | Expected.Trait, [1 3 0 1 0] |

The CLI was run on `/tmp/f3c/gap.ethos` (the Holder case). Before the change it printed `Checked./tmp/f3c/gap.ethos`. After the change it printed `Rejected.{ /tmp/f3c/gap.ethos { 3 12 } Conceptual.{ [ 1 1 0 1 0 ] Expected.Type } }`.

The learned roles were witnessed through a test. For `datom:[ Represented Path Error ] datom_codec:Composing protos:[ Extent Textualizable ] crate:Represented`, the roles are Trait, Type, none, Trait, Type, Trait, none.

A locally declared trait or a `protos:` intrinsic in the wrong position also gives Expected.Type or Expected.Trait. `Problem::Role`, which they raised before, no longer exists.

## Tests

Four tests are new in tests/represented.rs:

- `an_import_learns_its_role_from_the_dependency_declarations`
- `a_trait_imported_into_a_type_position_is_refused_as_no_type`
- `a_trait_in_a_field_position_is_refused_as_no_type`
- `a_type_imported_where_a_trait_is_wanted_is_refused_as_no_trait`

The Represented association tests are unchanged and pass.

## Check counts (cargo test on Prometheus; identical in both trees)

| suite | bare | braced |
|---|---|---|
| lib | 21 | 21 |
| cli | 17 | 17 |
| ethos | 33 | 33 |
| flow_contract (inner 2) | 1 | 1 |
| freshness | 4 | 4 |
| generated | 20 | 20 |
| print | 9 | 9 |
| represented | 13 (was 9) | 13 (was 9) |
| signal_without_datom | 2 | 2 |
| `cargo fmt --check`, `cargo clippy --all-targets -D warnings` | pass | pass |
| flake check attributes | 8/8 | 8/8 |

The 8 attributes are build, test, fmt, clippy, doc, dependency-ethos, no-free-functions and no-inherent-methods. Each was built with `nix build` under the overrides: protos `path:/tmp/protos-i5`, and datom-codec `git+file:///tmp/dc-f3` at d6191ff (bare) or 776cf4b (braced). After that, `nix flake check --keep-going` printed "running 0 flake checks…" and "all checks passed!" and exited 0. The count is 0 because every derivation was already built. The test attribute passing under Nix shows that the build script finds the vendored declarations inside the sandbox.

## Goldens

Every fixture, every `tests/generated/*.rs` and src/ethos-zero.rs is byte-equal to its base. The only generated change is src/error.rs: `Form` gains `Type,`, and `Problem` loses `Role(String),`. The freshness tests pass.

## Files touched (both trees)

- Cargo.toml: `build = "build.rs"` and `[build-dependencies] serde_json`
- Cargo.lock
- build.rs (new)
- error.ethos
- src/error.rs: `Form.Type` added, `Problem.Role` removed
- src/lib.rs: `Imported.role`
- src/conception.rs: `Dependency`, `Dependencies`, `Knowing`, `Learning`
- src/checking.rs: `Learned`, `Wanting`, refer
- src/signature.rs
- tests/represented.rs

## Patches

- `represented-gaps-bare-ethos-zero.patch`: `git diff 21da35b 2e13b3d`, applied on the bare represented tree.
- `represented-gaps-braced-ethos-zero.patch`: `git diff 406410c d844d23`, applied on the braced represented tree.

The two patches are textually identical. Each patch was applied with `git apply --index` to a fresh clone of its base, and the resulting tree equals the scratch tree: 679c65 for bare, 468403 for braced.

## Sources

- /home/li/primary/flows/1d0733/reports/fork3-complete.md
- /home/li/primary/flows/1d0733/reports/fork3-bare-represented-ethos-zero.patch
- /home/li/primary/flows/1d0733/reports/fork3-braced-represented-ethos-zero.patch
- /home/li/primary/flows/d5df1d/log.md (2026-10-10 ruling)
- /home/li/primary/flows/d5df1d/reports/special-representation-form.md
- Provenance receipt: unavailable.
