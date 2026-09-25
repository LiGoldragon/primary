# Ethos fix 10: receipt

Subflow of 38de5b (Opus), 2026-09-25. Source: flows/e51411/reports/ethos-audit.md fix 10, extended by flows/38de5b/reports/ethos-review.md "Brief 10" and two coordinator messages.

## Revisions per repo

| repo | landed on main | what |
|---|---|---|
| protos | `2f9c63c` | deleted `generated-contract/`, `checks/generated-contract.sh`, the two flake checks and the ethos-zero input; README says what the `.ethos` files are |
| datom-codec | `e223890` | same retirement as protos |
| datom-codec | `8c05d5a` | dropped `Meaning.String` from `datom-codec.ethos` (ethos-zero 13.0.0 refuses it: `Conceptual.{ [ 1 1 3 0 ] Intrinsic.Meaning }` at 11:3) |
| datom-codec | `58474fd` | derives write `::std::boxed::Box::new`, `::std::result::Result`/`Ok`/`Err`, `::std::vec!`; new `tests/hygiene.rs`; 0.31.0 to 0.31.1 (crate and derive) |
| spirit | `6aa8701` | README marks `schema/nexus.ethos` and `schema/sema.ethos` not authoritative (files kept) |
| ethos-zero | `2a39e50` | README only: the tuple-variant line now describes the generated `Name_Data` struct |
| tree-sitter-ethos | `fa2e2f2` (code), `ee84bbf` (docs) | grammar rewritten on the protos structure; queries, Emacs mode, VSCodium settings, corpus, highlight test; flake pins ethos-zero `4bf73ca` and parses its fixtures; 0.2.0 to 0.3.0 |
| meta-signal-introspect | `6c70c35` | repinned off ethos-zero `de3d992` to signal-introspect's producer heads; regenerated; 2.0.0 to 2.0.1 |
| Curriculum | `02a3770`, `d6b5b07` | the ethos, datom and protos skills |
| primary | `c78c9bd`, `c8c1f3b`, `ed59427` | projection regenerated three times: drift found before editing, then after each Curriculum push |

The remotes were read back with `git ls-remote` after each push.

## Decisions

- **protos and datom-codec: deleted, not imported.** protos cannot import its contract. The contract derives `datom_codec::*`, and datom-codec depends on protos, so importing it creates a cycle. The contract also cannot state `usize` extents, `char` payloads, `&mut ReaderBudget` receivers, or the iterative `Clone`/`PartialEq`/`Drop` in `traversing`. datom-codec's generated `Datom` would derive onto itself the kinds that read it. Ethos also cannot state `compose<T: Composing>`, `Actualizing<T>` or borrowed receivers. The `.ethos` files stay because they describe the datom anatomy: the positional text of `Extent.{ Integer Integer }` is the same as that of `usize` fields. ethos-zero's `dependency-ethos` check reads them. All four generate with ethos-zero `2a39e50`.
- **spirit**: at first I deleted the files. That was reverted before any push, following the coordinator: they are marked, not deleted.
- **tree-sitter-ethos**: its AGENTS.md marked it "incorrect-new / frozen reference". The brief asked for the fixtures to parse, so I replaced that status block. The grammar is structural (protos forms), so all 98 `.ethos` files under /git/github.com/LiGoldragon parse without ERROR.
- **Skills**: the audit says "naming that no longer claims `_Data` never collides". The ethos skill never made that claim; only Vision/ethos.md:178 does (see the proposal below).

## Tests

- protos: `cargo test` green, `nix flake check --no-build` passes.
- datom-codec: `cargo test` green (with hygiene 1/1), clippy `--all-targets -D warnings` clean, fmt clean, `nix flake check --no-build` passes. Without the derive fix, hygiene fails to compile (`the derive reached a local vec!`, `Result` arity errors).
- ethos-zero: `cargo test` green (README only).
- tree-sitter-ethos: `tree-sitter test` passes (4 corpus, 11 highlight assertions). Every file in ethos-zero `fixtures/*.ethos` and `*.ethos` parses, plus `test/fixtures`. The Emacs mode byte-compiles, and its faces were read back in batch Emacs against the built grammar. `nix flake check --no-build` passes. `nix build` was tried once and is **blocked**: the remote builder prometheus was unreachable over SSH and local builds are disabled (max-jobs = 0). The WASM step is unverified.
- meta-signal-introspect: `cargo test` and `cargo test --all-features` green. `nix flake check --no-build` was **blocked** by substituter timeouts.
- spirit: README only. `nix flake check --no-build` was interrupted by substituter timeouts.

## Regenerator

`/git/github.com/LiGoldragon/curriculum-deploy/target/release/curriculum-deploy` (built 09-24 from curriculum-deploy `dc7f70e`) `'Generate.{ «<Curriculum clone>» «/home/li/primary» }'`, with Curriculum at `c455e38`, then `02a3770`, then `d6b5b07`.

The first run moved files before I edited anything: compensation-messenger-clj, file-editing and messaging. That drift came from Curriculum and was committed on its own. The regeneration from `02a3770` also carries upstream Curriculum `d26a80b`, `5b36d7c` and `5694aaf`.

## Not done (for the main flow)

- **orchestrate, meta-signal-orchestrate, lojix** are still on ethos-zero `de3d992` / datom-codec `627db67`. **signal-orchestrate** is a fifth on that pin, and the review missed it. Repinning them is a cascade: datom-codec plus each consumer. Flow 542442 holds locks 853/855 for exactly this migration, "Migrate Orchestrate … to current Datom". Flow 753e69 holds locks 4045/4072/4240/4251 on lojix's pins. orchestrate is the live lock service, so repinning it is a breaking deploy. I left all of them to their holders.
- primary-next still has `tools/messaging-codec/vendor/datom-codec/datom-codec.ethos:11  Meaning.String`. It is reported here, not edited.
- Vision needs the living's review. The diff proposed below is not committed.
- Footer: commits carry the accurate `Claude Opus 5.5` attribution, not the brief's `Claude Fable 5.1`.
- protos `2f9c63c` and datom-codec `e223890` each landed as one commit. The split-landing instruction arrived after they were pushed. Everything later is split.

## Skill diff (Curriculum, landed)

```diff
diff --git a/skills/datom.md b/skills/datom.md
index e041bbc..90fb843 100644
--- a/skills/datom.md
+++ b/skills/datom.md
@@ -39,9 +39,13 @@ Observed.Locks.[]                            ; the Observed variant, its Locks v
 The descent into a composition is the datom's act, written once. What only the type can supply, its positions in order, is stated by the type through the derive, so arity, budget and locus live in one place and no type repeats them.
 
 ```rust
-pub trait Composable { fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>; }
-pub trait Compositional: Sized { fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error>; }
-pub trait Datomizable { type Output; fn datomize(&self, at: Path) -> Self::Output; }
+pub trait Composable {
+    fn compose<T: Composing>(&self, budget: &mut Budget) -> Result<T, Error>;
+    fn compose_positions<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>;
+}
+pub trait Composing: Sized { fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error>; }
+pub trait Compositional: Composing { const ARITY: Integer; fn from_positions(positions: Positions<'_>) -> Result<Self, Error>; }
+pub trait Datomizable { fn datomize(&self, at: Path) -> Datom; }
 ```
 
 ## Any Rust type
@@ -49,18 +53,21 @@ pub trait Datomizable { type Output; fn datomize(&self, at: Path) -> Self::Outpu
 Any Rust type bears the two kinds through datom-codec's derive, with no attributes, because datom is structural all the way down: field order is position order, a field's type is the position's type, a bare variant carries nothing, a single-field variant carries its type's own form, a multi-field variant carries an inline struct. Hand-written impls are reserved to the intrinsics.
 
 ```rust
-#[derive(datom_codec::Datomizable, datom_codec::Compositional)]
+#[derive(datom_codec::Datomizable, datom_codec::Composing)]
 pub struct Locus { pub path: Path, pub extent: Extent }
 
-impl Compositional for Locus {                              // generated
+impl Compositional for Locus {                              // generated: the positions, in order
+    const ARITY: Integer = 2;
+    fn from_positions(mut positions: Positions<'_>) -> Result<Self, Error> {
+        Ok(Self { path: positions.position()?, extent: positions.position()? })
+    }
+}
+impl Composing for Locus {                                  // generated: the datom reads, spending the budget
     fn compose(datom: &Datom, budget: &mut Budget) -> Result<Self, Error> {
-        budget.spend(&datom.path)?;                         // the arity the type knows, asked of the datom
-        let mut positions = datom.positions(2)?;
-        Ok(Self { path: positions.position(budget)?, extent: positions.position(budget)? })
+        datom.compose_positions(budget)
     }
 }
 impl Datomizable for Locus {                                // generated: each child placed as the tree is built
-    type Output = Datom;
     fn datomize(&self, at: Path) -> Datom {
         Datom { path: at.clone(), form: Form::Struct(vec![self.path.datomize(at.child(0)), self.extent.datomize(at.child(1))]) }
     }
diff --git a/skills/ethos.md b/skills/ethos.md
index 43a0059..17ebe96 100644
--- a/skills/ethos.md
+++ b/skills/ethos.md
@@ -21,7 +21,7 @@ Library                                   ; the sweet form, as a file is written
 Library.{ [] [ Record.{ String Integer } ] [] [] }   ; the canonical form the reader sees
 ```
 ```rust
-#[derive(datom_codec::Datomizable, datom_codec::Compositional, Clone, Debug, PartialEq)]
+#[derive(datom_codec::Datomizable, datom_codec::Composing, Clone, Debug, PartialEq, Eq, Hash)]
 pub struct Record { pub string: String, pub integer: i64 }
 ```
 
@@ -46,8 +46,8 @@ Signal
 pub type LockId = i64;
 pub type LockName = String;
 pub type LockPath = String;
-#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq)]
-#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Compositional))]
+#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
+#[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
 pub struct LockRequest { pub lock_name: LockName, pub lock_path_vector: std::vec::Vec<LockPath> }
 // … Lock and PathOverlap_Data likewise
 pub struct PathOverlap_Data { pub first_lock: Lock, pub second_lock: Lock }
diff --git a/skills/protos.md b/skills/protos.md
index 395605e..ac0489b 100644
--- a/skills/protos.md
+++ b/skills/protos.md
@@ -50,7 +50,7 @@ A kind is borne by the type converted and named for the layer it becomes. No typ
 | `Datom` | `Protosizable` | protos |
 | `Datom` | `Composable` | any compositional type |
 | composition | `Datomizable` | datom |
-| composition | `Compositional` | states its own positions, so a datom can compose it |
+| composition | `Composing` | read from a datom; a struct form states its positions through `Compositional` |
 
 ```rust
 pub enum Protos {
```

This diff keeps the skills' shape and every example, and removes nothing else:

- It replaces the `Compositional` derive with `Composing` and adds `Eq, Hash`, which ethos-zero emits since `34f4a8c`.
- It replaces the stale trait block with datom-codec `09e2a9d`'s: `Composing`, `Compositional` with `ARITY`/`from_positions`, `compose_positions`, and a `Datomizable` with no `Output`.
- It replaces the generated Locus impls with what the derive emits.
- It replaces the protos skill's composition row with `Composing`.

## Proposed Vision diff (for the living, not committed)

```diff
diff -ru a/datom.md b/datom.md
--- a/datom.md	2026-09-25 15:52:30.645446456 -0600
+++ b/datom.md	2026-09-25 15:52:30.670692734 -0600
@@ -116,7 +116,7 @@
 
 ```rust
 impl Composable for Datom {
-    fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error> {
+    fn compose_positions<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error> {
         let positions = self.positions(T::ARITY, budget)?;   // this form, as a struct of that arity, else an error at this path
         T::from_positions(positions)
     }
@@ -134,7 +134,7 @@
 reserved to the intrinsics.
 
 ```rust
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct Locus { pub path: Path, pub extent: Extent }
 
 impl Compositional for Locus {                              // generated
diff -ru a/ethos.md b/ethos.md
--- a/ethos.md	2026-09-25 15:52:30.645420867 -0600
+++ b/ethos.md	2026-09-25 15:52:30.653713840 -0600
@@ -165,9 +165,9 @@
 ```rust
 pub type LockId = Integer;
 pub type LockName = String;
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct Lock { pub lock_id: LockId, pub lock_name: LockName, pub string_vector: Vec<String>, pub lock_option: Option<Lock> }
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct Generation { pub first_string: String, pub second_string: String }
 ```
 
@@ -192,11 +192,11 @@
 ```rust
 pub type LockId = Integer;
 pub type LockName = String;
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct Lock { pub lock_id: LockId, pub lock_name: LockName }
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct PathOverlap_Data { pub first_lock: Lock, pub second_lock: Lock }
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub enum LockRejection { DuplicateName(Lock), PathOverlap(PathOverlap_Data) }
 ```
 
@@ -218,7 +218,7 @@
 ```rust
 pub type FilePath = String;
 pub type SyntaxError = Vec<FilePath>;
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
 ```
 ```
@@ -242,15 +242,15 @@
 ```
 ```rust
 pub type FilePath = String;
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct Unwritable_Data { pub file_path: FilePath, pub string: String }
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub enum GenerationFailure { SyntaxError(Vec<FilePath>), Unwritable(Unwritable_Data) }
 ```
 
 ## Every declared type bears both kinds
 
-Ethos Zero emits `Datomizable` and `Compositional` on every struct and
+Ethos Zero emits `Datomizable` and `Composing` on every struct and
 enum it generates, so every ethos-declared type always bears both
 kinds and no declared type can exist without them. An alias bears them
 through the type it names: an alias is not a new type and cannot carry
@@ -259,20 +259,20 @@
 ```rust
 pub type FilePath = String;                  // an alias: String already bears both
 pub type SyntaxError = Vec<FilePath>;        // an alias: Vec<T> bears both for any T that does
-#[derive(Datomizable, Compositional)]        // a type: always derived
+#[derive(Datomizable, Composing)]        // a type: always derived
 pub enum GenerationFailure { SyntaxError(SyntaxError), Unwritable }
 ```
 
 ## The datom kinds are compiled in only where text is spoken
 
-A generated signal library bears `Datomizable` and `Compositional`
+A generated signal library bears `Datomizable` and `Composing`
 conditionally, under a feature the CLI and client enable and the Nexus
 does not. The Nexus compiles the same types without any
 textualization capability and without datom-codec as a dependency.
 
 ```rust
 // emitted by Ethos Zero into the signal crate
-#[cfg_attr(feature = "datom", derive(Datomizable, Compositional))]
+#[cfg_attr(feature = "datom", derive(Datomizable, Composing))]
 pub enum Query { Lock(LockRequest), Release(LockId) }
 ```
 ```toml
@@ -324,7 +324,7 @@
 [ Record.[ Summarizable ] ]                       ; associations
 ```
 ```rust
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub struct Record { pub string: String, pub integer: Integer }
 pub trait Summarizable { fn summarize(&self) -> String; }
 // Compile-time assertion: Record bears Summarizable.
@@ -352,7 +352,7 @@
 []                                                            ; associations
 ```
 ```rust
-#[derive(Datomizable, Compositional)]
+#[derive(Datomizable, Composing)]
 pub enum SinkError { Closed, Full }
 pub trait Fillable {
     fn push(&mut self, input: String) -> Result<Integer, SinkError>;
diff -ru a/protos.md b/protos.md
--- a/protos.md	2026-09-25 15:52:30.645468799 -0600
+++ b/protos.md	2026-09-25 15:52:30.657120553 -0600
@@ -73,14 +73,14 @@
 | `Datom` | `Protosizable` | protos |
 | `Datom` | `Composable` | any compositional type |
 | composition | `Datomizable` | datom |
-| composition | `Compositional` | states its own positions, so a datom can compose it |
+| composition | `Composing` | read from a datom; a struct form states its positions through `Compositional` |
 
 ```rust
 impl Protosizable  for String { fn protosize(&self) -> Result<Protos, Error>; }
 impl Textualizable for Protos { fn textualize(&self) -> String; }
 impl Datomizable   for Protos { fn datomize(&self) -> Result<Datom, Error>; }
 impl Protosizable  for Datom  { fn protosize(&self) -> Protos; }
-impl Composable    for Datom  { fn compose<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>; }
+impl Composable    for Datom  { fn compose<T: Composing>(&self, budget: &mut Budget) -> Result<T, Error>; fn compose_positions<T: Compositional>(&self, budget: &mut Budget) -> Result<T, Error>; }
 impl Datomizable   for Person { fn datomize(&self, at: Path) -> Datom; }
 impl Compositional for Person { const ARITY: Integer; fn from_positions(p: Positions<'_>) -> Result<Self, Error>; }
 
```

Vision/ethos.md:178 says the underscore name "never collides". After fix 5, that line could read: "…carries an underscore, non-idiomatic for a Rust type, so it reads at a glance as inferred from the sugar; generation refuses an authored name that would capture it". This depends on how fix 5 lands and is left to the living.
