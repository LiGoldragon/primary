<!-- to-the-living:start -->
Presentation.{ «Ethos categories and sugar, second edition» }

# Ethos categories and sugar, second edition

### Proposal 1: psyche-context › vision/ethos.md

  In Naming, after its paragraph.

  Traits are qualifier-named: Runnable, Textualizable, Structural,
  Embodied. Run is not a trait. The verbs Rust imposes, Write and Read
  among them, are tolerated as legacy, for cognitive ease while Rust
  and ethos code are switched between so often; once ethos is the
  authored language that debt is removed.

+ A name says what it names in the system's own words; a word that means something only beside its neighbours, such as First, is not a name.
+
```ethos
+ Library.{
+ []                                  ; imports
+ [ Prompt.[ SystemPrompt             ; types
+           StartupPrompt ] ]
+ [ Named.[ name.[ String ] ] ]       ; traits
+ [ Named.[ Prompt ] ] }              ; associations
```

### Proposal 2: psyche-context › vision/ethos.md

  In Trait syntax, after its last paragraph.

  A trait's identity is its name and its constraints, as stated in the
  Identity section above.

+ A capability is named in lowercase camelCase, because it is not a variant: its lowercase first letter tells it from a variant, as a topic's does.
+
```ethos
+ Library.{
+ []                                  ; imports
+ [ Brief.String ]                    ; types
+ [ Briefing.[ brief.[ String ]       ; traits
+              rewriteBrief!{ [ Named ]
+                             [ String ] } ]
+   Named.[ name.[ String ] ] ]
+ [ Brief.[ Briefing Named ] ] }      ; associations
```

### Proposal 3: psyche-context › vision/ethos.md

  In Declaration: File, its first paragraph and its example block.

- The unit is File: one file, one Rust module. No namespace inside a
- file. An ethos file is written in the sweet form: the root's head,
- then the sections as siblings, the outer braces omitted. The braced
- form — the root's head opening braces that hold every section — is
- the canonical form. The sweet form is kept out of the main logic run:
- before the text is read as ethos at all, the file is converted
- mechanically to the canonical form, so the ethos reader sees only
- proper ethos.
+ The unit is File: one file, one Rust module. No namespace inside a file. The braced form — the root's head opening braces that hold every section — is the canonical form.
+ A file's usual form is the root's variant, its dot and the brace on one line, then a break, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement.
+ A file that holds a single thing breaks nowhere.
+
```ethos
+ Library.{
+ []                                  ; imports
+ [ Sink.{ String Integer } ]         ; types
+ [ Fillable.[ create:[ Self ]        ; traits
+              drain![ Vector<String> ] ] ]
+ [ Fillable.[ Sink ] ] }             ; associations
```

  …
  A Library's sections, in order, are imports, types, traits and
  associations. Every root's first section is its imports; its own
  sections follow.

```
- ; the sweet form, as a file is written: the head, then the sections as siblings
- Library
- [ protos:String ]               ; imports
- [ Record.{ String Integer } ]   ; types
- []                              ; traits
- []                              ; associations
- 
- ; the canonical form the reader sees, after the mechanical conversion
- Library.{
-   [ protos:String ]
-   [ Record.{ String Integer } ]
-   []
-   []
- }
```

### Proposal 4: psyche-context › vision/ethos.md

```
+------------------------+
| entries that share     |
| a category             |
+------------------------+
            |
      are held in
            v
+------------------------+
| one vector under       |
| the category           |
+------------------------+
            |
       written as
            v
+------------------------+
| Prompting.[            |
|   SystemPrompt         |
|   StartupPrompt ]      |
+------------------------+
```

```
+----------------------------+
| an association             |
| Head.[ members ]           |
+----------------------------+
       |              |
  head names     head names
  a trait        a type
       v              v
+-------------+ +-------------+
| members:    | | members:    |
| the types   | | the traits  |
| bearing it  | | it bears    |
+-------------+ +-------------+
```

  In Non-repetition, after its last paragraph; and in Associations, its first sentence.

  Terseness is in the low amount of noise, never in shortened words.

+ Where entries share a category, the category holds a vector of them; no entry repeats its category.
+ In associations, a trait borne by several types holds the vector of them: `Prompting.[ SystemPrompt StartupPrompt ]`.
+ An association whose head is a type keeps the vector of traits that type bears.
+
Not yet parseable: Ethos has no white square brackets, white braces or colon imports yet.

```text
+ Library.{
+ [ :flow:[ Key ] ]                   ; imports
+ [ SystemPrompt.⟦ Key ⟧              ; types
+   StartupPrompt.⟦ Key ⟧
+   Placements.⦃ SystemPrompt
+                StartupPrompt ⦄ ]
+ [ Prompting.[ text.[ String ] ] ]   ; traits
+ [ Prompting.[ SystemPrompt          ; associations
+               StartupPrompt
+               Placements ] ] }
```
Not yet parseable: Ethos has no white square brackets, white braces or colon imports yet.

  …
  ## Associations
  
- An association declares that a type bears a trait: the type's name, a
+ An association declares that a type bears a trait. A trait head lists the types that bear it. A type head is the type's name, a
  dot, a bracket of its traits. In the Signal and Sema roots the

### Proposal 5: psyche-context › vision/ethos.md

  In White braces define a struct, after its paragraph.

  White braces define a struct, so a struct definition looks different from a struct value. The definition, in ethos, names the types of its positions inside white braces; the value, in datom, fills them inside plain braces.

+ A white brace is read at its own layer and becomes the plain form before the ethos reader sees the text.

  In White square brackets define a vector, after its paragraph.

  White square brackets around an item type define a vector type, replacing the word Vector, which is so common: `⟦String⟧` is the vector of String. The vector value keeps its plain brackets in datom.

+ A white square bracket is read at its own layer and becomes the plain form before the ethos reader sees the text.

### Proposal 6: ethos-zero › src/checking.rs

  In impl Checkable for Association, and the traits after it.

```rust
  impl Checkable for Association {
  …
+         let head = &self.identity.name;
+         if scope.groups(head) {
+             self.identity.check(scope).place(0)?;
+             let members = &self.members;
+             let listed = members.list_all(scope);
+             return listed.place(1);
+         }
  …
          self.identity.check(scope).place(0)?;
  …
-         self.traits.refer_each(scope, Role::Trait, 0).place(1)
+         self.members.bear(scope).place(1)
      }
  }
+ 
+ /// The trait whose capabilities tell whether an
+ /// association's head names a trait, declared or
+ /// a Protos intrinsic, so that it lists the
+ /// types bearing it.
+ pub(crate) trait Grouping {
+     fn groups(&self, head: &Name) -> bool;
+     /// The Protos intrinsic a head names.
+     fn builtin(&self, head: &Name) -> Builtin;
+ }
+ 
+ /// The intrinsic a head names, if it names one.
+ type Builtin = Option<Intrinsic>;
+ 
+ impl Grouping for Scope<'_> {
+     fn groups(&self, head: &Name) -> bool {
+         let resolved = self.resolve(head);
+         if let Resolution::Trait(_) = resolved {
+             return true;
+         }
+         let builtin = self.builtin(head);
+         let role = builtin.map(|one| one.role());
+         role == Some(Role::Trait)
+     }
+ 
+     fn builtin(&self, head: &Name) -> Builtin {
+         use Resolution::Imported;
+         use Resolution::Intrinsic as Known;
+         let named = Intrinsic::identify(&head.0);
+         match self.resolve(head) {
+             Known(intrinsic) => Some(intrinsic),
+             Imported(origin, emitted) => {
+                 let from = origin.as_ref();
+                 let own = from == "protos";
+                 let same = &emitted == head;
+                 named.filter(|_| own && same)
+             }
+             _ => None,
+         }
+     }
+ }
+ 
+ /// The outcome of a check that reports no value.
+ type Checked = Result<(), Error>;
+ 
+ /// The trait whose capability checks a type a
+ /// grouped association lists: an unsourced type.
+ trait Listing {
+     fn list(&self, scope: &Scope) -> Checked;
+ }
+ 
+ impl Listing for Reference {
+     fn list(&self, scope: &Scope) -> Checked {
+         if self.source.is_none() {
+             return self.refer(scope, Role::Type);
+         }
+         let form = crate::Form::Name;
+         let problem = Problem::Expected(form);
+         Err(Error::conceptual(vec![], problem))
+     }
+ }
+ 
+ /// The trait whose capabilities check the
+ /// references an association lists.
+ trait Members {
+     /// Each as a type a trait head lists.
+     fn list_all(&self, scope: &Scope) -> Checked;
+     /// Each as a trait a type head bears.
+     fn bear(&self, scope: &Scope) -> Checked;
+ }
+ 
+ impl Members for [Reference] {
+     fn list_all(&self, scope: &Scope) -> Checked {
+         let mut at = 0;
+         for member in self {
+             let listed = member.list(scope);
+             listed.beside(at).place(0)?;
+             at += member.span();
+         }
+         Ok(())
+     }
+ 
+     fn bear(&self, scope: &Scope) -> Checked {
+         self.refer_each(scope, Role::Trait, 0)
+     }
+ }
+ 
+ /// The trait whose capability reads the
+ /// associations as single types bearing traits:
+ /// a grouped entry spread over the types it
+ /// lists, in order.
+ pub(crate) trait Bearing {
+     fn bearings(&self) -> Vec<Association>;
+ }
+ 
+ impl Bearing for File {
+     fn bearings(&self) -> Vec<Association> {
+         let File::Library(library) = self else {
+             return vec![];
+         };
+         let scope = Scope {
+             file: self,
+             identity: None,
+             associated: &[],
+         };
+         let mut read = Vec::new();
+         for entry in &library.associations {
+             let head = &entry.identity.name;
+             if !scope.groups(head) {
+                 read.push(entry.clone());
+                 continue;
+             }
+             for member in &entry.members {
+                 let identity = Identity {
+                     name: member.name.clone(),
+                     constraints: vec![],
+                 };
+                 let borne = Reference {
+                     source: None,
+                     name: head.clone(),
+                     arguments: vec![],
+                 };
+                 read.push(Association {
+                     identity,
+                     members: vec![borne],
+                 });
+             }
+         }
+         read
+     }
+ }
```

### Proposal 7: ethos-zero › src/conception.rs

  In impl Conceiving<Association> for Protos.

```rust
                  constraints: vec![],
              },
-             traits: body.bracket().place(1)?,
+             members: body.bracket().place(1)?,
          })
      }
  }
```

### Proposal 8: ethos-zero › src/generation.rs

  In the imports, impl Emitting for Association and impl Emitting for File.

```rust
  use quote::quote;
  
+ use crate::checking::Bearing;
  …
-         let mut assertions = Vec::with_capacity(self.traits.len());
-         for trait_definition in &self.traits {
+         let mut assertions = Vec::new();
+         for trait_definition in &self.members {
              let assertion = Ident::new(
  …
-                 for association in &library.associations {
-                     let item = association.emit(scope);
+                 for each in self.bearings() {
+                     let item = each.emit(scope);
  …
```

### Proposal 9: ethos-zero › src/lib.rs

  The Association struct.

```rust
      Static,
  }
  
- /// An association: a type, by its identity, bears traits.
+ /// An association: a type, by its identity,
+ /// bears traits; or a trait, by its identity,
+ /// is borne by the types listed. The head's
+ /// role decides.
  #[derive(Clone, Debug, PartialEq, Eq)]
  pub struct Association {
-     /// The type's identity.
+     /// The head: a type's identity or a trait's.
      pub identity: Identity,
-     /// The traits it bears.
-     pub traits: Vec<Reference>,
+     /// The traits the type bears, or the types
+     /// bearing the trait.
+     pub members: Vec<Reference>,
  }
```

### Proposal 10: ethos-zero › src/protosization.rs

  In impl Protosizing for Association.

```rust
  impl Protosizing for Association {
      fn protos(&self) -> Protos {
-         self.identity.heading(
-             Separator::Period,
-             "".enclosed(Enclosure::Bracketed, self.traits.reference_nodes()),
-         )
+         let members = &self.members;
+         let nodes = members.reference_nodes();
+         let bracket = Enclosure::Bracketed;
+         let body = "".enclosed(bracket, nodes);
+         let period = Separator::Period;
+         self.identity.heading(period, body)
      }
  }
```

### Proposal 11: ethos-zero › tests/ethos.rs

  At the end of the file.

```rust
          Problem::TraitWanted("String".to_owned())
      );
  }
+ 
+ /// A Library of three types and one trait, its
+ /// associations section the one given.
+ fn prompted(associations: &str) -> String {
+     let types = "Key.{ String } \
+         SystemPrompt.{ Key Integer } \
+         StartupPrompt.{ Key String }";
+     let count = "count.[ Integer ]";
+     let traits = format!("Prompting.[ {count} ]");
+     format!(
+         "Library [] [ {types} ] [ {traits} ] \
+         [ {associations} ]"
+     )
+ }
+ 
+ /// The Rust a source generates.
+ fn generated(source: &str) -> String {
+     match read(source).generate() {
+         Ok(rust) => rust,
+         Err(_) => panic!("{source} generates"),
+     }
+ }
+ 
+ #[test]
+ fn a_trait_head_generates_as_its_types() {
+     let single = generated(&prompted(
+         "SystemPrompt.[ Prompting ] \
+         StartupPrompt.[ Prompting ]",
+     ));
+     let types = "SystemPrompt StartupPrompt";
+     let group = format!("Prompting.[ {types} ]");
+     let grouped = generated(&prompted(&group));
+     assert_eq!(grouped, single);
+     let mixed = generated(&prompted(
+         "SystemPrompt.[ Prompting ] \
+         Prompting.[ StartupPrompt ]",
+     ));
+     assert_eq!(mixed, single);
+ }
+ 
+ #[test]
+ fn a_trait_head_prints_as_written() {
+     let source = prompted("Prompting.[ Key ]");
+     let file = read(&source);
+     let printed = file.protosize().textualize();
+     let entry = "[ Prompting.[ Key ] ]";
+     assert!(printed.contains(entry), "{printed}");
+ }
+ 
+ #[test]
+ fn a_head_names_a_trait_or_a_type() {
+     let source = prompted("Nothing.[ Key ]");
+     let name = "Nothing".to_owned();
+     let problem = Problem::Undeclared(name);
+     let refused = (vec![1, 3, 0], problem);
+     assert_eq!(source.refusal(), refused);
+ }
+ 
+ #[test]
+ fn a_trait_head_lists_only_unsourced_types() {
+     let entry = "Prompting.[ Key Prompting ]";
+     let both = prompted(entry);
+     let name = "Prompting".to_owned();
+     let at = vec![1, 3, 0, 1, 0, 1];
+     let refused = (at, Problem::Role(name));
+     assert_eq!(both.refusal(), refused);
+     let entry = "Prompting.[ protos:String ]";
+     let sourced = prompted(entry);
+     let problem = Problem::Expected(Form::Name);
+     assert_eq!(sourced.refusal().1, problem);
+ }
```
### Proposal 12: psyche-context › vision/ethos.md

  In Roots, its paragraph.

  Library, Signal, Operation, Memory. No version in a file. Signal's sections are
- queries and responses, since there is communication; Sema's are record
+ queries and responses, since there is communication; Memory's are record
  types, the rest to be decided. Signal gives a Nexus its main types and
- Sema its database types.
+ Memory its database types.

  In Associations, its first paragraph.

  An association declares that a type bears a trait: the type's name, a
- dot, a bracket of its traits. In the Signal and Sema roots the
+ dot, a bracket of its traits. In the Signal and Memory roots the
  associations of the query, response and record types are implied and
  never written. In a Library they are the fourth section, after the
  traits.

### Proposal 13: psyche-context › vision/nexus.md

  In its paragraph on the basic ontology, in Documents, and in the start paragraph.

  The basic ontology of an actor and dataflow system is designed before
- implementation; signal and sema are designed against it as if new, the
+ implementation; signal and memory are designed against it as if new, the
  old code at most inspiration.
  …
- The nexus and sema documents are undesigned; when they are designed
+ The nexus and memory documents are undesigned; when they are designed
  they live in the Nexus's main repository.
  …
  Its executable holds a default configuration as a constant. On start
- it looks for its Sema database at the default location: a database
+ it looks for its Memory database at the default location: a database
  that exists holds the configuration; a database created new is
  seeded with the defaults.

### Proposal 14: psyche-context › vision/memory.md, a new file

```markdown
+ ---
+ description: Memory, the database engine of a Nexus, or its record types are being designed or judged.
+ dependencies: [vision-ethos, vision-nexus]
+ ---
+ 
+ ## What memory is
+ 
+ Memory is the database engine of a Nexus, authored in Ethos so the
+ stored types are visible; its root, Memory, declares record types. It
+ matters more than nexus, because operational editing should yield the
+ migration with the edit.
+ 
+ ```
+ Memory
+ []                                                        ; imports
+ [ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
+                                                           ; the remaining sections are to be decided
+ ```
```

### Proposal 15: psyche-context › vision/sema.md, a deleted file

```markdown
- ---
- description: Sema, the database engine of a Nexus, or its record types are being designed or judged.
- dependencies: [vision-ethos, vision-nexus]
- ---
- 
- ## What sema is
- 
- Sema is the database engine of a Nexus, authored in Ethos so the
- stored types are visible; its root, Sema, declares record types. It
- matters more than nexus, because operational editing should yield the
- migration with the edit.
- 
- ```
- Sema
- []                                                        ; imports
- [ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
-                                                           ; the remaining sections are to be decided
- ```
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
