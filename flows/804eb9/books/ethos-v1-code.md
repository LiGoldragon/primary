### Proposal C1: ethos-zero › src/checking.rs

A file is checked root by root, then whole, its roots sharing one namespace; associations are gathered from every root. Rule: land, amend or reject.

```rust
  use datom_codec::{Integer, Path};

+ use crate::Root;
+ use crate::sectioning::Rooting;
  use crate::sectioning::{Hoisting, Referencing, Sectioning};
+ use crate::sectioning::{Opening, Prefixing};
  use crate::signature::{Place, Stance, Standing};
  use crate::{
```

```rust
              }
          }
-         if let File::Library(library) = self {
-             resolution = resolution.or(library.traits.resolve(name));
+         for declared in self.traits() {
+             let named = declared.resolve(name);
+             resolution = resolution.or(named);
+         }
+         for body in self.bodies() {
+             let imports = body.root.imports();
+             let imported = imports.resolve(name);
+             resolution = resolution.or(imported);
          }
-         let resolution = resolution.or(self.imports().resolve(name));
          if resolution != Resolution::Undeclared {
              return resolution;
```

```rust
  }

+ impl Checkable for Root {
+     fn check(&self, scope: &Scope) -> Checked {
+         self.contents().check(scope)
+     }
+ }
+
+ /// A file is checked root by root, then whole:
+ /// its roots share one module and one namespace.
  impl Checkable for File {
      fn check(&self, scope: &Scope) -> Result<(), Error> {
-         let checked = match self {
-             File::Library(library) => library.check(scope),
-             File::Signal(signal) => signal.check(scope),
-             File::Operation(operation) => operation.check(scope),
-             File::Memory(memory) => memory.check(scope),
-             File::Type(declaration) => declaration.check(scope),
-         };
-         checked.place(1)?;
+         for body in self.bodies() {
+             let checked = body.root.check(scope);
+             checked.prefixed(&body.path)?;
+         }
          // The derived names come first, so an authored name that would
          // capture one is the occurrence refused.
```

```rust
          names.extend(self.shared_sites());
          names.extend(self.declared());
-         names.distinct().place(1)?;
-         self.finite().place(1)?;
-         self.sealed().place(1)?;
-         self.shared().place(1)?;
-         self.foreign().place(1)
+         names.distinct()?;
+         self.finite()?;
+         self.sealed()?;
+         self.shared()?;
+         self.foreign()
      }
  }
```

```rust
      fn foreign(&self) -> Result<(), Error> {
          let mut foreign = Vec::new();
-         for import in self.imports() {
+         let mut imports = Vec::new();
+         for body in self.bodies() {
+             let root = body.root;
+             imports.extend(root.imports().iter());
+         }
+         for import in imports {
              let (source, names) = match import {
                  Import::One(source, imported) => (source, std::slice::from_ref(imported)),
```

```rust
                  if variant.holds(&foreign) {
                      return Err(Error::conceptual(
-                         vec![implied.section],
+                         implied.path.clone(),
                          Problem::Foreign(implied.name.0.clone()),
                      ));
```

```rust
                  if variant.holds(&shared) {
                      return Err(Error::conceptual(
-                         vec![implied.section],
+                         implied.path.clone(),
                          Problem::Shared(implied.name.0.clone()),
                      ));
```

```rust
                      if variant.holds(&sealed) {
                          return Err(Error::conceptual(
-                             vec![implied.section],
+                             implied.path.clone(),
                              Problem::Sealed(implied.name.0.clone()),
                          ));
```

```rust

  /// The trait whose capability lists the enums of a file whose variants are named first-level.
- trait Rooting {
+ trait InlineRooting {
      fn inline_roots(&self) -> Vec<InlineRoot<'_>>;
  }

- impl Rooting for File {
+ impl InlineRooting for File {
      fn inline_roots(&self) -> Vec<InlineRoot<'_>> {
          let mut roots = Vec::new();
```

```rust
                  owner: implied.name,
                  variants: implied.variants,
-                 path: vec![implied.section],
+                 path: implied.path,
              });
          }
```

```rust
  /// The trait whose capability lists every name a file root declares by
  /// authorship: its imports, its types and traits, and the types it implies.
- trait Declared {
+ pub(crate) trait Declared {
      fn declared(&self) -> Vec<DeclarationSite>;
  }

+ /// A `Type` root declares its one type.
+ impl Declared for TypeDeclaration {
+     fn declared(&self) -> Vec<DeclarationSite> {
+         self.names()
+     }
+ }
+
  impl Declared for crate::Library {
      fn declared(&self) -> Vec<DeclarationSite> {
```

```rust
  }

+ impl Declared for Root {
+     fn declared(&self) -> Vec<DeclarationSite> {
+         self.contents().declared()
+     }
+ }
+
+ /// Every root's names, each at its path from the
+ /// file's node, then those declared in place.
  impl Declared for File {
      fn declared(&self) -> Vec<DeclarationSite> {
-         let mut names = match self {
-             File::Library(library) => library.declared(),
-             File::Signal(signal) => signal.declared(),
-             File::Operation(operation) => operation.declared(),
-             File::Memory(memory) => memory.declared(),
-             File::Type(declaration) => declaration.names(),
-         };
+         let mut names = Vec::new();
+         for body in self.bodies() {
+             for mut site in body.root.declared() {
+                 let mut path = body.path.clone();
+                 path.append(&mut site.path);
+                 site.path = path;
+                 names.push(site);
+             }
+         }
          // A type declared in place is a declaration of the file, named at its head.
          for placed in self.inlined() {
```

```rust
  impl TraitDeclaring for File {
      fn trait_declaration(&self, name: &Name) -> Option<&TraitDeclaration> {
-         let File::Library(library) = self else {
-             return None;
-         };
-         library
-             .traits
-             .iter()
-             .find(|declaration| declaration.identity.name == *name)
+         for declared in self.traits() {
+             if declared.identity.name == *name {
+                 return Some(declared);
+             }
+         }
+         None
+     }
+ }
+
+ /// The trait whose capabilities gather what a
+ /// file's roots declare beside their types.
+ pub(crate) trait Gathering {
+     /// Every trait the roots declare.
+     fn traits(&self) -> Vec<&TraitDeclaration>;
+     /// Every association the roots write.
+     fn associations(&self) -> Vec<&Association>;
+ }
+
+ impl Gathering for File {
+     fn traits(&self) -> Vec<&TraitDeclaration> {
+         let mut traits = Vec::new();
+         for body in self.bodies() {
+             traits.extend(body.root.traits());
+         }
+         traits
+     }
+
+     fn associations(&self) -> Vec<&Association> {
+         let mut associations = Vec::new();
+         for body in self.bodies() {
+             let root = body.root;
+             let written = root.associations();
+             associations.extend(written);
+         }
+         associations
      }
  }
```

```rust
  }

+ /// Associations, one type to an entry.
+ type Spread = Vec<Association>;
+
+ /// The trait whose capability reads one
+ /// association as single types bearing traits.
+ pub(crate) trait Spreading {
+     /// A type head as written; a trait head as
+     /// one entry for each type it lists.
+     fn spread(&self, scope: &Scope) -> Spread;
+ }
+
+ impl Spreading for Association {
+     fn spread(&self, scope: &Scope) -> Spread {
+         let head = &self.identity.name;
+         if !scope.groups(head) {
+             return vec![self.clone()];
+         }
+         let mut read = Vec::new();
+         for member in &self.members {
+             let identity = Identity {
+                 name: member.name.clone(),
+                 constraints: vec![],
+             };
+             let borne = Reference {
+                 source: None,
+                 name: head.clone(),
+                 arguments: vec![],
+             };
+             read.push(Association {
+                 identity,
+                 members: vec![borne],
+             });
+         }
+         read
+     }
+ }
+
  impl Bearing for File {
      fn bearings(&self) -> Vec<Association> {
-         let File::Library(library) = self else {
-             return vec![];
-         };
          let scope = Scope {
              file: self,
```

```rust
          };
          let mut read = Vec::new();
-         for entry in &library.associations {
-             let head = &entry.identity.name;
-             if !scope.groups(head) {
-                 read.push(entry.clone());
-                 continue;
-             }
-             for member in &entry.members {
-                 let identity = Identity {
-                     name: member.name.clone(),
-                     constraints: vec![],
-                 };
-                 let borne = Reference {
-                     source: None,
-                     name: head.clone(),
-                     arguments: vec![],
-                 };
-                 read.push(Association {
-                     identity,
-                     members: vec![borne],
-                 });
-             }
+         for entry in self.associations() {
+             read.extend(entry.spread(&scope));
          }
          read
```

```rust

      fn borne(&self, bearer: &Name) -> Traits<'_> {
-         let File::Library(library) = self else {
-             return vec![];
-         };
          let mut names = Vec::new();
          for bearing in self.bearings() {
```

```rust
          }
          let mut borne = Vec::new();
-         for declared in &library.traits {
+         for declared in self.traits() {
              let name = &declared.identity.name;
              if names.contains(name) {
```

### Proposal C2: ethos-zero › src/conception.rs

The reader takes one root or a bracket of roots, refuses an empty vector and a Type root inside a vector. Rule: land, amend or reject.

```rust
  //! Conception: structural Protos to Ethos concepts.

- use datom_codec::Integer;
+ use datom_codec::{Integer, Path};
  use protos::{Enclosure, Protos, Separator, Symbol};

+ use crate::Head;
  use crate::{
      ArityProblem, AssociatedConstant, AssociatedType, Association, Capability, ConceptualErroring,
```

```rust
  }

+ /// A file is one root, or a vector of roots
+ /// generated into one module; a `Type` root
+ /// stands only alone.
  impl Conceiving<File> for Protos {
      fn conceive(&self) -> Result<File, Error> {
+         let bracket = Enclosure::Bracketed;
+         let listed = self.children(bracket);
+         let Some(nodes) = listed else {
+             let root = self.conceive()?;
+             return Ok(File::One(root));
+         };
+         if nodes.is_empty() {
+             return Problem::Empty.refused(vec![]);
+         }
+         let mut roots = Vec::new();
+         let each = nodes.iter().enumerate();
+         for (index, node) in each {
+             let at = index as Integer;
+             let root = node.conceive().place(at)?;
+             if let Root::Type(_) = root {
+                 let path = vec![at, 0];
+                 let problem = Problem::Root;
+                 return problem.refused(path);
+             }
+             roots.push(root);
+         }
+         Ok(File::Many(roots))
+     }
+ }
+
+ /// What a reading yields: the value, or the
+ /// error at its path.
+ type Read<T> = Result<T, Error>;
+
+ /// The trait whose capability refuses a reading
+ /// with a problem at a path.
+ trait Refusing {
+     fn refused<T>(self, path: Path) -> Read<T>;
+ }
+
+ impl Refusing for Problem {
+     fn refused<T>(self, path: Path) -> Read<T> {
+         let error = Error::conceptual(path, self);
+         Err(error)
+     }
+ }
+
+ /// The trait whose capability names the head
+ /// that replaced a retired head's name.
+ trait Renaming {
+     fn successor(&self) -> Option<Head>;
+ }
+
+ impl Renaming for Symbol {
+     fn successor(&self) -> Option<Head> {
+         Head::successor(&self.0)
+     }
+ }
+
+ impl Conceiving<Root> for Protos {
+     fn conceive(&self) -> Result<Root, Error> {
          let Protos::Headed {
              head,
```

```rust
              return Err(Error::conceptual(vec![], Problem::Root));
          };
-         match Root::identify(&head.0) {
-             Some(Root::Library) => Ok(File::Library(body.conceive().place(1)?)),
-             Some(Root::Signal) => Ok(File::Signal(body.conceive().place(1)?)),
-             Some(Root::Operation) => Ok(File::Operation(body.conceive().place(1)?)),
-             Some(Root::Memory) => Ok(File::Memory(body.conceive().place(1)?)),
-             Some(Root::Type) => {
+         match Head::identify(&head.0) {
+             Some(Head::Library) => {
+                 let read = body.conceive();
+                 let library = read.place(1)?;
+                 Ok(Root::Library(library))
+             }
+             Some(Head::Signal) => {
+                 let read = body.conceive();
+                 let signal = read.place(1)?;
+                 Ok(Root::Signal(signal))
+             }
+             Some(Head::Operation) => {
+                 let read = body.conceive();
+                 let operation = read.place(1)?;
+                 Ok(Root::Operation(operation))
+             }
+             Some(Head::Memory) => {
+                 let read = body.conceive();
+                 let memory = read.place(1)?;
+                 Ok(Root::Memory(memory))
+             }
+             Some(Head::Type) => {
                  let declaration: TypeDeclaration = body.conceive().place(1)?;
                  // A type file declares one type whole; an enum of it needs at
```

```rust
                      ));
                  }
-                 Ok(File::Type(declaration))
+                 Ok(Root::Type(declaration))
              }
-             None => match Root::successor(&head.0) {
+             None => match head.successor() {
                  Some(successor) => Err(Error::conceptual(
                      vec![0],
```

### Proposal C3: ethos-zero › src/conforming.rs

Conforming takes the root reader, Rooting, in place of Sectioning. Rule: land, amend or reject.

```rust

  use crate::checking::Declaring;
- use crate::sectioning::{Referencing, Sectioning};
+ use crate::sectioning::{Referencing, Rooting};
  use crate::{
      File, Identifiable, Intrinsic, Name, Position, Reference, Resolution, Resolving,
```

### Proposal C4: ethos-zero › src/generation.rs

Each root emits its types, implied enums, traits and associations, all roots into the one module, in root order. Rule: land, amend or reject.

```rust
  use quote::quote;

- use crate::checking::Bearing;
+ use crate::Root;
+ use crate::checking::{Bearing, Spreading};
  use crate::checking::{Checkable, Declaring, Inlining};
+ use crate::sectioning::Rooting;
  use crate::sectioning::{Hoisting, Referencing, ReferencingEach, Sectioning};
  use crate::signature::{Place, Stance, Standing};
```

```rust
  // ---------------------------------------------------------------------------

- impl Emitting for File {
-     fn emit(&self, scope: &Scope) -> TokenStream {
+ /// The trait whose capability yields the items
+ /// a root emits into its file's module.
+ trait Itemizing {
+     fn items(&self, scope: &Scope) -> Items;
+ }
+
+ /// The items a root emits, in order.
+ type Items = Vec<TokenStream>;
+
+ /// The trait whose capability marks an item to
+ /// be left as generated by the formatter.
+ trait Skipping {
+     fn skipped(self) -> TokenStream;
+ }
+
+ impl Skipping for TokenStream {
+     fn skipped(self) -> TokenStream {
+         quote! { #[rustfmt::skip] #self }
+     }
+ }
+
+ /// A root emits its types, then its implied
+ /// enums, then its traits, then its associations.
+ impl Itemizing for Root {
+     fn items(&self, scope: &Scope) -> Items {
          // prettyplease owns each generated item's canonical text. rustfmt makes
          // different width decisions for aliases and ordinary items, so each
```

```rust
          // are one item each and receive it here.
          let mut items = Vec::new();
-         match self {
-             File::Library(library) => {
-                 for declaration in &library.types {
-                     items.push(declaration.emit(scope));
-                 }
-                 for declaration in &library.traits {
-                     let item = declaration.emit(scope);
-                     items.push(quote! { #[rustfmt::skip] #item });
-                 }
-                 for each in self.bearings() {
-                     let item = each.emit(scope);
-                     items.push(quote! { #[rustfmt::skip] #item });
-                 }
+         for declaration in self.types() {
+             items.push(declaration.emit(scope));
+         }
+         // A Signal's `Query` and `Response`, an
+         // Operation's `Operation` and `Outcome`:
+         // each an enum of its section's variants,
+         // emitted when it has any.
+         use TypeDeclaration::Enum;
+         for implied in self.implied_enums() {
+             if implied.variants.is_empty() {
+                 continue;
              }
-             File::Signal(_) | File::Operation(_) | File::Memory(_) | File::Type(_) => {
-                 for declaration in self.types() {
-                     items.push(declaration.emit(scope));
-                 }
-                 // A Signal's `Query` and `Response`, an Operation's
-                 // `Operation` and `Outcome`: each an enum of its section's
-                 // variants, emitted when it has any.
-                 for implied in self.implied_enums() {
-                     if implied.variants.is_empty() {
-                         continue;
-                     }
-                     let enumeration = TypeDeclaration::Enum(
-                         Identity {
-                             name: implied.name,
-                             constraints: vec![],
-                         },
-                         implied.variants.to_vec(),
-                     );
-                     items.push(enumeration.emit(scope));
-                 }
+             let identity = Identity {
+                 name: implied.name,
+                 constraints: vec![],
+             };
+             let variants = implied.variants;
+             let listed = variants.to_vec();
+             let declared = Enum(identity, listed);
+             items.push(declared.emit(scope));
+         }
+         for declaration in self.traits() {
+             let item = declaration.emit(scope);
+             items.push(item.skipped());
+         }
+         for entry in self.associations() {
+             for each in entry.spread(scope) {
+                 let item = each.emit(scope);
+                 items.push(item.skipped());
              }
          }
+         items
+     }
+ }
+
+ /// A file emits its roots' items, in root order,
+ /// into its one module.
+ impl Emitting for File {
+     fn emit(&self, scope: &Scope) -> TokenStream {
+         let mut items = Vec::new();
+         for body in self.bodies() {
+             items.extend(body.root.items(scope));
+         }
          quote! {
              #![allow(dead_code, non_camel_case_types, non_snake_case)]
```

### Proposal C5: ethos-zero › src/lib.rs

A file becomes one root or a vector of roots; a root is an enum of the five heads. Rule: land, amend or reject.

```rust
  }

- /// The unit of declaration: one file, one Rust module; an enum of its four roots.
+ /// The unit of declaration: one file, one Rust
+ /// module, holding one root or a vector of them.
  #[derive(Clone, Debug, PartialEq, Eq)]
  pub enum File {
+     /// One root alone: `Library.{ … }`.
+     One(Root),
+     /// A vector of roots, generated into the one
+     /// module: `[ Library.{ … } Memory.{ … } ]`.
+     /// A `Type` root stands only alone.
+     Many(Vec<Root>),
+ }
+
+ /// A root of a file: an enum of its five heads.
+ #[derive(Clone, Debug, PartialEq, Eq)]
+ pub enum Root {
      /// Library: imports, types, traits and associations in that order.
      Library(Library),
```

```rust
  }

- /// The head of a file: which variant of [`File`] it is.
+ /// The head of a root: which variant of [`Root`]
+ /// it is.
  #[derive(Clone, Copy, Debug, PartialEq, Eq)]
- pub enum Root {
+ pub enum Head {
      /// The library root: what the others share.
      Library,
```

```rust
  }

- /// The trait whose capability yields which variant of [`File`] a value is.
+ /// The trait whose capability yields which
+ /// variant of [`Root`] a value is.
  pub trait Rooted {
-     /// The head the file is written under.
-     fn root(&self) -> Root;
+     /// The head the root is written under.
+     fn head(&self) -> Head;
  }

```

```rust

  // ---------------------------------------------------------------------------
- // Root and Intrinsic: named, identified by walking the variants
+ // Head and Intrinsic: named, identified by
+ // walking the variants
  // ---------------------------------------------------------------------------

- impl Named for Root {
+ impl Named for Head {
      fn name(&self) -> &'static str {
          match self {
-             Root::Library => "Library",
-             Root::Signal => "Signal",
-             Root::Operation => "Operation",
-             Root::Memory => "Memory",
-             Root::Type => "Type",
+             Head::Library => "Library",
+             Head::Signal => "Signal",
+             Head::Operation => "Operation",
+             Head::Memory => "Memory",
+             Head::Type => "Type",
          }
      }
  }

- impl Identifiable for Root {
+ impl Identifiable for Head {
      fn identify(name: &str) -> Option<Self> {
          for root in [
-             Root::Library,
-             Root::Signal,
-             Root::Operation,
-             Root::Memory,
-             Root::Type,
+             Head::Library,
+             Head::Signal,
+             Head::Operation,
+             Head::Memory,
+             Head::Type,
          ] {
              if root.name() == name {
```

```rust
  }

- impl Succeeding for Root {
+ impl Succeeding for Head {
      /// `Sema` was the memory root's head until 15.0.0.
      fn successor(name: &str) -> Option<Self> {
          if name == "Sema" {
-             Some(Root::Memory)
+             Some(Head::Memory)
          } else {
              None
```

```rust
  }

- impl Rooted for File {
-     fn root(&self) -> Root {
+ impl Rooted for Root {
+     fn head(&self) -> Head {
          match self {
-             File::Library(_) => Root::Library,
-             File::Signal(_) => Root::Signal,
-             File::Operation(_) => Root::Operation,
-             File::Memory(_) => Root::Memory,
-             File::Type(_) => Root::Type,
+             Root::Library(_) => Head::Library,
+             Root::Signal(_) => Head::Signal,
+             Root::Operation(_) => Head::Operation,
+             Root::Memory(_) => Head::Memory,
+             Root::Type(_) => Head::Type,
          }
      }
```

### Proposal C6: ethos-zero › src/printing.rs

A vector of roots prints with the bracket on the first line, each root head, dot and brace together, its sections two columns in. Rule: land, amend or reject.

```rust
  //! print expands vertically. A `Type` file's one declaration needs no break
  //! and follows its dot on the same line.
+ //!
+ //! A vector of roots opens its bracket on the
+ //! first line; each root's head, dot and brace
+ //! stand together, its sections hang beneath it
+ //! two columns in, and the last closes the brace:
+ //!
+ //! ```text
+ //! [ Library.{
+ //!   []
+ //!   [ Name.String ]
+ //!   []
+ //!   [] }
+ //!   Memory.{
+ //!   []
+ //!   [ Record.{ Name Integer } ]
+ //!   []
+ //!   [] } ]
+ //! ```

  use protos::{Enclosure, Protos, Protosizable, Separator, Textualizable};
```

```rust
  use crate::{File, Printable};

+ /// The trait whose capability prints a root
+ /// standing in a vector of roots.
+ trait Hanging {
+     /// Its head, dot and brace, then its
+     /// sections two columns in.
+     fn hang(&self) -> String;
+ }
+
+ /// The trait whose capability writes a section
+ /// on a new line, two columns in.
+ trait Indenting {
+     fn indented(&self) -> String;
+ }
+
+ impl Indenting for Protos {
+     fn indented(&self) -> String {
+         let indent = "\n  ";
+         let written = self.textualize();
+         let lines = written.replace('\n', indent);
+         format!("{indent}{lines}")
+     }
+ }
+
+ impl Hanging for Protos {
+     fn hang(&self) -> String {
+         let Protos::Headed {
+             head,
+             constraints: None,
+             separator: Separator::Period,
+             body,
+             ..
+         } = self
+         else {
+             return self.textualize();
+         };
+         let Protos::Enclosed {
+             enclosure: Enclosure::Braced,
+             children,
+             ..
+         } = body.as_ref()
+         else {
+             return self.textualize();
+         };
+         let mut text = head.0.clone();
+         text.push_str(".{");
+         for section in children {
+             text.push_str(&section.indented());
+         }
+         text.push_str(" }");
+         text
+     }
+ }
+
  impl Printable for Protos {
      fn print(&self) -> String {
          let mut text = match self {
+             Protos::Enclosed {
+                 enclosure: Enclosure::Bracketed,
+                 children,
+                 ..
+             } if !children.is_empty() => {
+                 let mut text = "[ ".to_owned();
+                 let mut first = true;
+                 for root in children {
+                     if !first {
+                         text.push_str("\n  ");
+                     }
+                     first = false;
+                     text.push_str(&root.hang());
+                 }
+                 text.push_str(" ]");
+                 text
+             }
              Protos::Headed {
                  head,
```

### Proposal C7: ethos-zero › src/protosization.rs

A root alone ascends as itself, a vector of roots as the bracket that holds them. Rule: land, amend or reject.

```rust
  use protos::{Canonicalizable, Enclosure, Extent, Protos, Protosizable, Separator, Symbol};

+ use crate::Root;
  use crate::{
      AssociatedConstant, AssociatedType, Association, Capability, Constraint, File, Identity,
```

```rust
      }
  }
- impl Protosizing for File {
+ impl Protosizing for Root {
      fn protos(&self) -> Protos {
-         let raw = match self {
+         match self {
              Self::Library(library) => "Library".headed(None, Separator::Period, library.protos()),
              Self::Signal(signal) => "Signal".headed(None, Separator::Period, signal.protos()),
```

```rust
              Self::Memory(memory) => "Memory".headed(None, Separator::Period, memory.protos()),
              Self::Type(declaration) => "Type".headed(None, Separator::Period, declaration.alone()),
+         }
+     }
+ }
+
+ /// A root alone ascends as itself; a vector of
+ /// roots as the bracket holding them.
+ impl Protosizing for File {
+     fn protos(&self) -> Protos {
+         let raw = match self {
+             Self::One(root) => root.protos(),
+             Self::Many(roots) => {
+                 let nodes = roots.protos_list();
+                 let vector = Enclosure::Bracketed;
+                 "".enclosed(vector, nodes)
+             }
          };
          // Shared Protos canonicalization assigns exact UTF-8 byte spans
```

### Proposal C8: ethos-zero › src/sectioning.rs

Sections are read per root, each at the path of its body: [ 1 ] for a root alone, [ i 1 ] for the root at index i. Rule: land, amend or reject.

```rust
  //! Library and Memory imply nothing.
  //!
+ //! A file holds one root or a vector of them,
+ //! generated into one module, so its roots
+ //! share one namespace. Each root's body has a
+ //! path from the file's node: `[ 1 ]` for a root
+ //! alone, `[ i 1 ]` for the root at index `i`.
+ //!
  //! A struct position may declare its type in place, `Brief.String`; that
  //! type is a declaration of the file like any other, named by its own name,
```

```rust

  use datom_codec::{Integer, Path};
+ use std::slice::from_ref;

  use crate::checking::Spanning;
- use crate::{File, Import, Name, Position, Reference, TypeDeclaration, Variant};
+ use crate::checking::{Checkable, Declared};
+ use crate::{Association, TraitDeclaration};
+ use crate::{Error, Placing, Root};
+ use crate::{File, Import, Name, Position};
+ use crate::{Library, Memory, Operation, Signal};
+ use crate::{Reference, TypeDeclaration, Variant};

- /// An enum a root implies: its name, its variants and the section holding them.
+ /// An enum a root implies: its name, its
+ /// variants and the path of the section holding
+ /// them.
  pub(crate) struct Implied<'a> {
      pub(crate) name: Name,
      pub(crate) variants: &'a [Variant],
-     pub(crate) section: Integer,
+     pub(crate) path: Path,
  }

- /// A type declaration and the path of its node from the file's body.
+ /// A type declaration and the path of its node
+ /// from the file's node.
  pub(crate) struct Placed<'a> {
      pub(crate) path: Path,
```

```rust
  }

- /// The trait whose capabilities read a file's sections by role.
+ /// A root of a file and the path of its body.
+ pub(crate) struct Body<'a> {
+     pub(crate) path: Path,
+     pub(crate) root: &'a Root,
+ }
+
+ /// The trait whose capabilities read a root's
+ /// sections by role.
  pub(crate) trait Sectioning {
      /// Where imported names come from.
```

```rust
      /// The types section's declarations.
      fn types(&self) -> &[TypeDeclaration];
-     /// The path, from the file's body, of the declaration at Protos index
-     /// `at` of the types section; a `Type` file's one declaration is the body.
+     /// The path, from the body, of the
+     /// declaration at Protos index `at` of the
+     /// types section; a `Type` root's one
+     /// declaration is the body.
      fn type_path(&self, at: Integer) -> Path;
-     /// The enums the root implies, in section order.
+     /// The enums the root implies, in section
+     /// order, each at its path from the body.
      fn implied_enums(&self) -> Vec<Implied<'_>>;
+     /// The traits the root declares.
+     fn traits(&self) -> &[TraitDeclaration];
+     /// The associations the root writes.
+     fn associations(&self) -> &[Association];
  }

- impl Sectioning for File {
-     fn imports(&self) -> &[Import] {
-         match self {
-             File::Library(library) => &library.imports,
-             File::Signal(signal) => &signal.imports,
-             File::Operation(operation) => &operation.imports,
-             File::Memory(memory) => &memory.imports,
-             File::Type(_) => &[],
+ /// A section implying an enum: the enum's name
+ /// and the variants.
+ type Section<'a> = (&'a str, &'a [Variant]);
+
+ /// The trait whose capability makes the enums
+ /// the request and reply sections imply, the
+ /// first section's at `[ 1 ]`.
+ trait Implicit<'a> {
+     fn implied(self) -> Vec<Implied<'a>>;
+ }
+
+ impl<'a> Implicit<'a> for [Section<'a>; 2] {
+     fn implied(self) -> Vec<Implied<'a>> {
+         let mut implied = Vec::new();
+         let sections = (1..).zip(self);
+         for (index, section) in sections {
+             let (name, variants) = section;
+             let name = Name::try_from(name);
+             let name = name.expect("static");
+             let path = vec![index];
+             implied.push(Implied {
+                 name,
+                 variants,
+                 path,
+             });
          }
+         implied
+     }
+ }
+
+ impl Sectioning for Library {
+     fn imports(&self) -> &[Import] {
+         &self.imports
      }

      fn types(&self) -> &[TypeDeclaration] {
-         match self {
-             File::Library(library) => &library.types,
-             File::Signal(signal) => &signal.types,
-             File::Operation(operation) => &operation.types,
-             File::Memory(memory) => &memory.types,
-             File::Type(declaration) => std::slice::from_ref(declaration),
-         }
+         &self.types
+     }
+
+     fn type_path(&self, at: Integer) -> Path {
+         vec![1, at]
+     }
+
+     fn implied_enums(&self) -> Vec<Implied<'_>> {
+         vec![]
+     }
+
+     fn traits(&self) -> &[TraitDeclaration] {
+         &self.traits
+     }
+
+     fn associations(&self) -> &[Association] {
+         &self.associations
+     }
+ }
+
+ impl Sectioning for Signal {
+     fn imports(&self) -> &[Import] {
+         &self.imports
+     }
+
+     fn types(&self) -> &[TypeDeclaration] {
+         &self.types
+     }
+
+     fn type_path(&self, at: Integer) -> Path {
+         vec![3, at]
+     }
+
+     fn implied_enums(&self) -> Vec<Implied<'_>> {
+         let queries = &self.queries[..];
+         let responses = &self.responses[..];
+         let request = ("Query", queries);
+         let reply = ("Response", responses);
+         [request, reply].implied()
+     }
+
+     fn traits(&self) -> &[TraitDeclaration] {
+         &[]
+     }
+
+     fn associations(&self) -> &[Association] {
+         &[]
+     }
+ }
+
+ impl Sectioning for Operation {
+     fn imports(&self) -> &[Import] {
+         &self.imports
+     }
+
+     fn types(&self) -> &[TypeDeclaration] {
+         &self.types
+     }
+
+     fn type_path(&self, at: Integer) -> Path {
+         vec![3, at]
+     }
+
+     fn implied_enums(&self) -> Vec<Implied<'_>> {
+         let operations = &self.operations[..];
+         let outcomes = &self.outcomes[..];
+         let request = ("Operation", operations);
+         let reply = ("Outcome", outcomes);
+         [request, reply].implied()
+     }
+
+     fn traits(&self) -> &[TraitDeclaration] {
+         &[]
+     }
+
+     fn associations(&self) -> &[Association] {
+         &[]
+     }
+ }
+
+ impl Sectioning for Memory {
+     fn imports(&self) -> &[Import] {
+         &self.imports
+     }
+
+     fn types(&self) -> &[TypeDeclaration] {
+         &self.types
      }

      fn type_path(&self, at: Integer) -> Path {
+         vec![1, at]
+     }
+
+     fn implied_enums(&self) -> Vec<Implied<'_>> {
+         vec![]
+     }
+
+     fn traits(&self) -> &[TraitDeclaration] {
+         &[]
+     }
+
+     fn associations(&self) -> &[Association] {
+         &[]
+     }
+ }
+
+ /// A `Type` root's one declaration is its body.
+ impl Sectioning for TypeDeclaration {
+     fn imports(&self) -> &[Import] {
+         &[]
+     }
+
+     fn types(&self) -> &[TypeDeclaration] {
+         std::slice::from_ref(self)
+     }
+
+     fn type_path(&self, _: Integer) -> Path {
+         vec![]
+     }
+
+     fn implied_enums(&self) -> Vec<Implied<'_>> {
+         vec![]
+     }
+
+     fn traits(&self) -> &[TraitDeclaration] {
+         &[]
+     }
+
+     fn associations(&self) -> &[Association] {
+         &[]
+     }
+ }
+
+ /// What every head's body bears: its check and
+ /// its declared names.
+ pub(crate) trait Checked: Checkable + Declared {}
+
+ impl<T: Checkable + Declared> Checked for T {}
+
+ /// What every head's body bears: its sections
+ /// read by role, its check, its declared names.
+ pub(crate) trait Contents: Sectioning + Checked {}
+
+ impl<T: Sectioning + Checked> Contents for T {}
+
+ /// The trait whose capability opens a root on
+ /// the body its head holds.
+ pub(crate) trait Opening {
+     fn contents(&self) -> &dyn Contents;
+ }
+
+ impl Opening for Root {
+     fn contents(&self) -> &dyn Contents {
          match self {
-             File::Library(_) | File::Memory(_) => vec![1, at],
-             File::Signal(_) | File::Operation(_) => vec![3, at],
-             File::Type(_) => vec![],
+             Root::Library(root) => root,
+             Root::Signal(root) => root,
+             Root::Operation(root) => root,
+             Root::Memory(root) => root,
+             Root::Type(root) => root,
          }
      }
+ }
+
+ impl Sectioning for Root {
+     fn imports(&self) -> &[Import] {
+         self.contents().imports()
+     }
+
+     fn types(&self) -> &[TypeDeclaration] {
+         self.contents().types()
+     }
+
+     fn type_path(&self, at: Integer) -> Path {
+         self.contents().type_path(at)
+     }

      fn implied_enums(&self) -> Vec<Implied<'_>> {
-         let (request, requests, reply, replies) = match self {
-             File::Library(_) | File::Memory(_) | File::Type(_) => return vec![],
-             File::Signal(signal) => ("Query", &signal.queries, "Response", &signal.responses),
-             File::Operation(operation) => (
-                 "Operation",
-                 &operation.operations,
-                 "Outcome",
-                 &operation.outcomes,
-             ),
+         self.contents().implied_enums()
+     }
+
+     fn traits(&self) -> &[TraitDeclaration] {
+         self.contents().traits()
+     }
+
+     fn associations(&self) -> &[Association] {
+         self.contents().associations()
+     }
+ }
+
+ /// The trait whose capabilities read a file's
+ /// roots, each at the path of its body.
+ pub(crate) trait Rooting {
+     /// Every root, with its body's path.
+     fn bodies(&self) -> Vec<Body<'_>>;
+     /// Every enum the roots imply, each at its
+     /// path from the file's node.
+     fn implied_enums(&self) -> Vec<Implied<'_>>;
+ }
+
+ impl Rooting for File {
+     fn bodies(&self) -> Vec<Body<'_>> {
+         let roots = match self {
+             File::One(root) => from_ref(root),
+             File::Many(roots) => roots.as_slice(),
          };
-         vec![
-             Implied {
-                 name: Name::try_from(request).expect("static identifier"),
-                 variants: requests,
-                 section: 1,
-             },
-             Implied {
-                 name: Name::try_from(reply).expect("static identifier"),
-                 variants: replies,
-                 section: 2,
-             },
-         ]
+         let alone = matches!(self, File::One(_));
+         let mut bodies = Vec::new();
+         let each = roots.iter().enumerate();
+         for (index, root) in each {
+             let at = index as Integer;
+             let path = match alone {
+                 true => vec![1],
+                 false => vec![at, 1],
+             };
+             bodies.push(Body { path, root });
+         }
+         bodies
+     }
+
+     fn implied_enums(&self) -> Vec<Implied<'_>> {
+         let mut implied = Vec::new();
+         for body in self.bodies() {
+             let root = body.root;
+             for mut each in root.implied_enums() {
+                 let mut path = body.path.clone();
+                 path.append(&mut each.path);
+                 each.path = path;
+                 implied.push(each);
+             }
+         }
+         implied
+     }
+ }
+
+ /// The trait whose capability places an error
+ /// below every step of a path.
+ pub(crate) trait Prefixing {
+     fn prefixed(self, path: &Path) -> Self;
+ }
+
+ impl<T> Prefixing for Result<T, Error> {
+     fn prefixed(self, path: &Path) -> Self {
+         let mut placed = self;
+         for step in path.iter().rev() {
+             placed = placed.place(*step);
+         }
+         placed
      }
  }
```

```rust
  }

- impl Hoisting for File {
+ impl Hoisting for Root {
      fn declarations(&self) -> Vec<Placed<'_>> {
          let mut placed = Vec::new();
```

```rust
          }
          for implied in self.implied_enums() {
-             implied
-                 .variants
-                 .hoist_variants(vec![implied.section], &mut placed);
+             let path = implied.path;
+             let variants = implied.variants;
+             let all = &mut placed;
+             variants.hoist_variants(path, all);
          }
          placed
```

```rust
  }

+ /// Every root's declarations, in root order,
+ /// each at its path from the file's node.
+ impl Hoisting for File {
+     fn declarations(&self) -> Vec<Placed<'_>> {
+         let mut placed = Vec::new();
+         for body in self.bodies() {
+             let root = body.root;
+             for mut each in root.declarations() {
+                 let mut path = body.path.clone();
+                 path.append(&mut each.path);
+                 each.path = path;
+                 placed.push(each);
+             }
+         }
+         placed
+     }
+
+     fn inlined(&self) -> Vec<Placed<'_>> {
+         let mut placed = Vec::new();
+         for body in self.bodies() {
+             let root = body.root;
+             for mut each in root.inlined() {
+                 let mut path = body.path.clone();
+                 path.append(&mut each.path);
+                 each.path = path;
+                 placed.push(each);
+             }
+         }
+         placed
+     }
+ }
+
  /// The trait whose capabilities walk the declarations below a node.
  trait Hoist {
```

### Proposal C9: ethos-zero › src/checking.rs

Signal, Operation and Memory check their traits and associations sections as a Library does. Rule: land, amend or reject.

```rust
  /// A sealed type's positions are private, so it is built only by a `:`
  /// capability yielding `Self` or `Result<Self X>` of a trait declared in the
- /// same file and associated with the type there. A file with no traits, any
- /// root but a Library, cannot build one.
+ /// same file and associated with the type there.
+ /// A file declaring no trait cannot build one.
  trait Sealing {
      fn sealed(&self) -> Result<(), Error>;
```

```rust
          names.extend(self.imports.names_in(0));
          names.extend(self.types.names_in(3));
+         names.extend(self.traits.names_in(4));
          names
      }
```

```rust
          names.extend(self.imports.names_in(0));
          names.extend(self.types.names_in(3));
+         names.extend(self.traits.names_in(4));
          names
      }
```

```rust
          let mut names = self.imports.names_in(0);
          names.extend(self.types.names_in(1));
+         names.extend(self.traits.names_in(2));
          names
      }
```

```rust
          self.queries.check_each(scope, 1)?;
          self.responses.check_each(scope, 2)?;
-         self.types.check_each(scope, 3)
+         self.types.check_each(scope, 3)?;
+         self.traits.check_each(scope, 4)?;
+         let written = &self.associations;
+         written.check_each(scope, 5)
      }
  }
```

```rust
          self.operations.check_each(scope, 1)?;
          self.outcomes.check_each(scope, 2)?;
-         self.types.check_each(scope, 3)
+         self.types.check_each(scope, 3)?;
+         self.traits.check_each(scope, 4)?;
+         let written = &self.associations;
+         written.check_each(scope, 5)
      }
  }
```

```rust
          self.declared().distinct()?;
          self.imports.check_each(scope, 0)?;
-         self.types.check_each(scope, 1)
+         self.types.check_each(scope, 1)?;
+         self.traits.check_each(scope, 2)?;
+         let written = &self.associations;
+         written.check_each(scope, 3)
      }
  }
```

### Proposal C10: ethos-zero › src/conception.rs

Signal and Operation read six sections and Memory four, the last two being traits and associations. Rule: land, amend or reject.

```rust
  impl Conceiving<Signal> for Protos {
      fn conceive(&self) -> Result<Signal, Error> {
-         let s = self.sections(4)?;
+         let s = self.sections(6)?;
          let Some(queries) = s[1].children(Enclosure::Bracketed) else {
              return Err(Error::conceptual(vec![1], Problem::Expected(Form::Section)));
```

```rust
              return Err(Error::conceptual(vec![3], Problem::Expected(Form::Section)));
          };
+         let traits = s[4].bracket().place(4)?;
+         let associations = s[5].bracket();
+         let associations = associations.place(5)?;
          Ok(Signal {
              imports: s[0].bracket().place(0)?,
```

```rust
              responses: responses.variants().place(2)?,
              types: declarations.declarations().place(3)?,
+             traits,
+             associations,
          })
      }
```

```rust
  impl Conceiving<Operation> for Protos {
      fn conceive(&self) -> Result<Operation, Error> {
-         let s = self.sections(4)?;
+         let s = self.sections(6)?;
          let Some(operations) = s[1].children(Enclosure::Bracketed) else {
              return Err(Error::conceptual(vec![1], Problem::Expected(Form::Section)));
```

```rust
              return Err(Error::conceptual(vec![3], Problem::Expected(Form::Section)));
          };
+         let traits = s[4].bracket().place(4)?;
+         let associations = s[5].bracket();
+         let associations = associations.place(5)?;
          Ok(Operation {
              imports: s[0].bracket().place(0)?,
```

```rust
              outcomes: outcomes.variants().place(2)?,
              types: declarations.declarations().place(3)?,
+             traits,
+             associations,
          })
      }
```

```rust
  impl Conceiving<Memory> for Protos {
      fn conceive(&self) -> Result<Memory, Error> {
-         let s = self.sections(2)?;
+         let s = self.sections(4)?;
          let Some(types) = s[1].children(Enclosure::Bracketed) else {
              return Err(Error::conceptual(vec![1], Problem::Expected(Form::Section)));
          };
+         let traits = s[2].bracket().place(2)?;
+         let associations = s[3].bracket();
+         let associations = associations.place(3)?;
          Ok(Memory {
              imports: s[0].bracket().place(0)?,
              types: types.declarations().place(1)?,
+             traits,
+             associations,
          })
      }
```

### Proposal C11: ethos-zero › src/lib.rs

Signal, Operation and Memory gain traits and associations fields. Rule: land, amend or reject.

```rust
      /// Library: imports, types, traits and associations in that order.
      Library(Library),
-     /// Signal: imports, the query variants, the response variants, the types carried.
+     /// Signal: imports, the query variants, the
+     /// response variants, the types carried, the
+     /// traits and the associations.
      Signal(Signal),
-     /// Operation: imports, the operation variants, the outcome variants, the types they carry.
+     /// Operation: imports, the operation
+     /// variants, the outcome variants, the types
+     /// they carry, the traits and the
+     /// associations.
      Operation(Operation),
-     /// Memory: imports, the record types stored.
+     /// Memory: imports, the record types stored,
+     /// the traits and the associations.
      Memory(Memory),
      /// Type: one type declaration alone, `Type.CommitMessage.[ Landing Fix.String ]`.
```

```rust
      /// The types the queries and responses carry.
      pub types: Vec<TypeDeclaration>,
+     /// The declared capability traits.
+     pub traits: Vec<TraitDeclaration>,
+     /// The type-to-trait assertions.
+     pub associations: Vec<Association>,
  }

```

```rust
      /// The types the operations and outcomes carry.
      pub types: Vec<TypeDeclaration>,
+     /// The declared capability traits.
+     pub traits: Vec<TraitDeclaration>,
+     /// The type-to-trait assertions.
+     pub associations: Vec<Association>,
  }

- /// The memory variant of a file: imports and record-type declarations.
+ /// The memory variant of a file: imports,
+ /// record-type declarations, traits and
+ /// associations.
  #[derive(Clone, Debug, PartialEq, Eq)]
  pub struct Memory {
```

```rust
      /// The record type declarations.
      pub types: Vec<TypeDeclaration>,
+     /// The declared capability traits.
+     pub traits: Vec<TraitDeclaration>,
+     /// The type-to-trait assertions.
+     pub associations: Vec<Association>,
  }

```

### Proposal C12: ethos-zero › src/protosization.rs

Every root ascends its traits and associations sections last. Rule: land, amend or reject.

```rust

  use crate::Root;
+ use crate::sectioning::Sectioning;
  use crate::{
      AssociatedConstant, AssociatedType, Association, Capability, Constraint, File, Identity,
```

```rust
      }
  }
+ /// The trait whose capability ascends a root's
+ /// traits and associations sections, its last.
+ trait Behaving {
+     fn behaviour(&self) -> Vec<Protos>;
+ }
+
+ impl<T: Sectioning> Behaving for T {
+     fn behaviour(&self) -> Vec<Protos> {
+         let bracket = Enclosure::Bracketed;
+         let traits = self.traits().protos_list();
+         let written = self.associations();
+         let associations = written.protos_list();
+         let mut sections = Vec::new();
+         for list in [traits, associations] {
+             let node = "".enclosed(bracket, list);
+             sections.push(node);
+         }
+         sections
+     }
+ }
+
  impl Protosizing for Signal {
      fn protos(&self) -> Protos {
```

```rust
                  "".enclosed(Enclosure::Bracketed, self.responses.variant_nodes()),
                  "".enclosed(Enclosure::Bracketed, self.types.declaration_nodes()),
-             ],
+             ]
+             .into_iter()
+             .chain(self.behaviour())
+             .collect(),
          )
      }
```

```rust
                  "".enclosed(Enclosure::Bracketed, self.outcomes.variant_nodes()),
                  "".enclosed(Enclosure::Bracketed, self.types.declaration_nodes()),
-             ],
+             ]
+             .into_iter()
+             .chain(self.behaviour())
+             .collect(),
          )
      }
```

```rust
                  "".enclosed(Enclosure::Bracketed, self.imports.protos_list()),
                  "".enclosed(Enclosure::Bracketed, self.types.declaration_nodes()),
-             ],
+             ]
+             .into_iter()
+             .chain(self.behaviour())
+             .collect(),
          )
      }
```

### Proposal C13: ethos-zero › src/sectioning.rs

Every root yields its own traits and associations to the shared readers. Rule: land, amend or reject.

```rust

      fn traits(&self) -> &[TraitDeclaration] {
-         &[]
+         &self.traits
      }

      fn associations(&self) -> &[Association] {
-         &[]
+         &self.associations
      }
  }
```

```rust

      fn traits(&self) -> &[TraitDeclaration] {
-         &[]
+         &self.traits
      }

      fn associations(&self) -> &[Association] {
-         &[]
+         &self.associations
      }
  }
```

```rust

      fn traits(&self) -> &[TraitDeclaration] {
-         &[]
+         &self.traits
      }

      fn associations(&self) -> &[Association] {
-         &[]
+         &self.associations
      }
  }
```

### Proposal C14: ethos-zero › ethos-zero.ethos

The crate own ethos documents the six-section and four-section root layouts. Rule: land, amend or reject.

```ethos
  ; The files read are of five roots, each section in this order:
  ;   Library    [ imports ] [ types ] [ traits ] [ associations ]
- ;   Signal     [ imports ] [ queries ] [ responses ] [ types ]
- ;   Operation  [ imports ] [ operations ] [ outcomes ] [ types ]   ; proposed, pending the living's word
- ;   Memory     [ imports ] [ record types ]
+ ;   Signal     [ imports ] [ queries ] [ responses ] [ types ] [ traits ] [ associations ]
+ ;   Operation  [ imports ] [ operations ] [ outcomes ] [ types ] [ traits ] [ associations ]   ; proposed
+ ;   Memory     [ imports ] [ record types ] [ traits ] [ associations ]
  ;   Type       one declaration                               ; proposed
  ; A file headed Sema is refused as Renamed.Memory. A file is an ordinary datom:
```

### Proposal C15: ethos-zero › src/checking.rs

A headed bare is checked as a new type over the type it holds, with arity known for each declared type. Rule: land, amend or reject.

```rust
  impl Resolving for TypeDeclaration {
      fn resolve(&self, name: &Name) -> Resolution {
-         let declared = match self {
-             TypeDeclaration::Struct(identity, _)
-             | TypeDeclaration::Enum(identity, _)
-             | TypeDeclaration::Alias(identity, _)
-             | TypeDeclaration::Sealed(identity, _)
-             | TypeDeclaration::Shared(identity, _) => &identity.name,
-         };
+         let declared = &self.identity().name;
          if declared == name {
              Resolution::Type(name.clone())
```

```rust
  impl Naming for TypeDeclaration {
      fn names(&self) -> Vec<DeclarationSite> {
-         match self {
-             TypeDeclaration::Struct(identity, _)
-             | TypeDeclaration::Enum(identity, _)
-             | TypeDeclaration::Alias(identity, _)
-             | TypeDeclaration::Sealed(identity, _)
-             | TypeDeclaration::Shared(identity, _) => vec![DeclarationSite {
-                 name: identity.name.clone(),
-                 path: vec![0],
-             }],
-         }
+         let identity = self.identity();
+         vec![DeclarationSite {
+             name: identity.name.clone(),
+             path: vec![0],
+         }]
      }
  }
```

```rust
      fn span(&self) -> Integer {
          match self {
-             TypeDeclaration::Alias(_, aliased) => aliased.span(),
+             TypeDeclaration::Newtype(_, held) => {
+                 // Its arguments stand beside it.
+                 held.span()
+             }
              TypeDeclaration::Struct(_, _)
              | TypeDeclaration::Sealed(_, _)
```

```rust
                          .any(|variant| variant.inhabited(file, owner, known))
              }
-             TypeDeclaration::Alias(_, aliased) => aliased.inhabited(file, owner, known),
+             TypeDeclaration::Newtype(_, held) => {
+                 // Where its type has a value.
+                 held.inhabited(file, owner, known)
+             }
          }
      }
```

```rust
  impl Identified for TypeDeclaration {
      fn identity(&self) -> &Identity {
+         use TypeDeclaration::Newtype;
          match self {
              TypeDeclaration::Struct(identity, _)
              | TypeDeclaration::Enum(identity, _)
-             | TypeDeclaration::Alias(identity, _)
+             | Newtype(identity, _)
              | TypeDeclaration::Sealed(identity, _)
              | TypeDeclaration::Shared(identity, _) => identity,
```

```rust
                  false
              }
-             TypeDeclaration::Alias(_, aliased) => aliased.holds(shared),
+             TypeDeclaration::Newtype(_, held) => {
+                 // What its type holds.
+                 held.holds(shared)
+             }
          }
      }
```

```rust
  }

+ /// The trait whose capability says how many
+ /// arguments a declared type takes.
+ trait Counting {
+     fn arity(&self, name: &Name) -> Arguments;
+ }
+
+ /// How many arguments a type takes, if known.
+ type Arguments = Option<usize>;
+
+ impl Counting for Scope<'_> {
+     fn arity(&self, name: &Name) -> Arguments {
+         let file = self.file;
+         let declared = file.declaration(name);
+         let identity = declared?.identity();
+         Some(identity.constraints.len())
+     }
+ }
+
  /// The trait whose capability checks a reference in the role its position gives it.
  pub(crate) trait Referring {
```

```rust
                  },
                  Resolution::Type(name) => {
-                     let arity =
-                         scope
-                             .file
-                             .declaration(&name)
-                             .map(|declaration| match declaration {
-                                 TypeDeclaration::Struct(identity, _)
-                                 | TypeDeclaration::Enum(identity, _)
-                                 | TypeDeclaration::Alias(identity, _)
-                                 | TypeDeclaration::Sealed(identity, _)
-                                 | TypeDeclaration::Shared(identity, _) => {
-                                     identity.constraints.len()
-                                 }
-                             });
+                     // Its declared arity.
                      ReferenceRequirement {
                          role: Role::Type,
-                         arity,
+                         arity: scope.arity(&name),
                      }
                  }
```

```rust
  }

- /// The trait whose capability tells whether an alias reaches a name through aliases and intrinsic containers alone.
- trait Cycling {
-     fn cycles(&self, target: &Name, file: &File, visited: &mut Vec<Name>) -> bool;
-     fn cycles_substituting(
-         &self,
-         target: &Name,
-         file: &File,
-         visited: &mut Vec<Name>,
-         application: AliasApplication<'_>,
-     ) -> bool;
- }
-
- /// The identity and actual arguments of an alias while its body is followed.
- /// Parameter references in that body are replaced before cycle detection.
- #[derive(Clone, Copy)]
- struct AliasApplication<'a> {
-     identity: &'a Identity,
-     arguments: &'a [Reference],
- }
-
- impl Cycling for Reference {
-     fn cycles(&self, target: &Name, file: &File, visited: &mut Vec<Name>) -> bool {
-         if self.source.is_some() {
-             return self
-                 .arguments
-                 .iter()
-                 .any(|argument| argument.cycles(target, file, visited));
-         }
-         if &self.name == target {
-             return true;
-         }
-         match file.resolve(&self.name) {
-             Resolution::Type(name) => {
-                 if visited.contains(&name) {
-                     return false;
-                 }
-                 visited.push(name.clone());
-                 match file.declaration(&name) {
-                     Some(TypeDeclaration::Alias(identity, aliased)) => aliased.cycles_substituting(
-                         target,
-                         file,
-                         visited,
-                         AliasApplication {
-                             identity,
-                             arguments: &self.arguments,
-                         },
-                     ),
-                     _ => false,
-                 }
-             }
-             Resolution::Intrinsic(_) | Resolution::Imported(_, _) => {
-                 for argument in &self.arguments {
-                     if argument.cycles(target, file, visited) {
-                         return true;
-                     }
-                 }
-                 false
-             }
-             Resolution::Trait(_)
-             | Resolution::Parameter(_)
-             | Resolution::Associated(_)
-             | Resolution::Ambiguous(_)
-             | Resolution::Undeclared => false,
-         }
-     }
-
-     fn cycles_substituting(
-         &self,
-         target: &Name,
-         file: &File,
-         visited: &mut Vec<Name>,
-         application: AliasApplication<'_>,
-     ) -> bool {
-         if self.source.is_none()
-             && self.arguments.is_empty()
-             && let Resolution::Parameter(index) = application.identity.resolve(&self.name)
-         {
-             return application.arguments[index as usize].cycles(target, file, visited);
-         }
-         if self.source.is_some() {
-             return self
-                 .arguments
-                 .iter()
-                 .any(|argument| argument.cycles_substituting(target, file, visited, application));
-         }
-         if &self.name == target {
-             return true;
-         }
-         match file.resolve(&self.name) {
-             Resolution::Type(name) => {
-                 if visited.contains(&name) {
-                     return false;
-                 }
-                 visited.push(name.clone());
-                 match file.declaration(&name) {
-                     Some(TypeDeclaration::Alias(identity, aliased)) => aliased.cycles_substituting(
-                         target,
-                         file,
-                         visited,
-                         AliasApplication {
-                             identity,
-                             arguments: &self.arguments,
-                         },
-                     ),
-                     _ => false,
-                 }
-             }
-             Resolution::Intrinsic(_) | Resolution::Imported(_, _) => self
-                 .arguments
-                 .iter()
-                 .any(|argument| argument.cycles_substituting(target, file, visited, application)),
-             Resolution::Trait(_)
-             | Resolution::Parameter(_)
-             | Resolution::Associated(_)
-             | Resolution::Ambiguous(_)
-             | Resolution::Undeclared => false,
-         }
-     }
- }
-
  /// The trait whose capability finds the declaration of a name in a file.
  pub(crate) trait Declaring {
```

```rust
  impl Checkable for TypeDeclaration {
      fn check(&self, scope: &Scope) -> Result<(), Error> {
-         let identity = match self {
-             TypeDeclaration::Struct(identity, _)
-             | TypeDeclaration::Enum(identity, _)
-             | TypeDeclaration::Alias(identity, _)
-             | TypeDeclaration::Sealed(identity, _)
-             | TypeDeclaration::Shared(identity, _) => identity,
-         };
+         let identity = self.identity();
          if !identity.constraints.is_empty() {
              return Err(Error::conceptual(
```

```rust
                  variants.check_children(&inner).place(1)
              }
-             TypeDeclaration::Alias(identity, aliased) => {
-                 aliased.check(&inner).lifted(1)?;
-                 if aliased.cycles(&identity.name, scope.file, &mut vec![]) {
-                     return Err(Error::conceptual(
-                         vec![0],
-                         Problem::Cycle(identity.name.0.clone()),
-                     ));
-                 }
-                 Ok(())
+             // A new type holds the one type it
+             // wraps, by value.
+             TypeDeclaration::Newtype(_, held) => {
+                 let checked = held.check(&inner);
+                 checked.lifted(1)
              }
          }
```

### Proposal C16: ethos-zero › src/conception.rs

A headed bare is read as a new type declaration, not an alias. Rule: land, amend or reject.

```rust

  use crate::Head;
+ use crate::TypeDeclaration::Newtype;
  use crate::{
      ArityProblem, AssociatedConstant, AssociatedType, Association, Capability, ConceptualErroring,
```

```rust
          let mut declaration: TypeDeclaration = self.conceive().place(index as Integer)?;
          if let Some(children) = arguments {
-             let TypeDeclaration::Alias(_, reference) = &mut declaration else {
+             let declared = &mut declaration;
+             let Newtype(_, held) = declared else {
                  return Err(Error::conceptual(
                      vec![(index + 1) as Integer],
```

```rust
                  ));
              };
-             reference.arguments = children.references().place((index + 1) as Integer)?;
+             let at = (index + 1) as Integer;
+             let arguments = children.references();
+             held.arguments = arguments.place(at)?;
          }
          Ok(declaration)
```

```rust
              Ok(TypeDeclaration::Enum(identity, v.variants().place(1)?))
          } else {
-             Ok(TypeDeclaration::Alias(identity, body.conceive().place(1)?))
+             let held = body.conceive().place(1)?;
+             Ok(Newtype(identity, held))
          }
      }
```

### Proposal C17: ethos-zero › src/conforming.rs

A new type datom is read as a struct of one position, the type it holds. Rule: land, amend or reject.

```rust
  //! brace of its positions; an enum variant carrying nothing is its head
  //! alone, one carrying a type is `Head.body`, one declaring a struct or an
- //! enum in place carries that payload; an alias is its aliased type. The
+ //! enum in place carries that payload; a new
+ //! type is a struct of one position. The
  //! intrinsic scalars are composed by datom-codec itself (`String`,
  //! `Integer`, `Decimal`, `Boolean`, `Meaning`); `Vector`, `Option` and
```

```rust
  use protos::BoundedProtosizable;

+ use crate::TypeDeclaration::Newtype;
  use crate::checking::Declaring;
  use crate::sectioning::{Referencing, Rooting};
```

```rust
          budget: &mut Budget,
      ) -> Result<(), Error>;
+     /// A new type's datom: a struct of one
+     /// position, the type it holds.
+     fn newtype(
+         &self,
+         wrapped_reference: &Reference,
+         datom: &Datom,
+         budget: &mut Budget,
+     ) -> Result<(), Error>;
  }

```

```rust
                  self.variants(name, variants, datom, budget)
              }
-             Some(TypeDeclaration::Alias(_, aliased)) => self.reference(aliased, datom, budget),
+             Some(Newtype(_, held)) => {
+                 // A struct of one position.
+                 self.newtype(held, datom, budget)
+             }
              // Shared state never travels as text.
              Some(TypeDeclaration::Shared(_, _)) => Err(datom.form("Shared")),
```

```rust
          }))
      }
+
+     fn newtype(
+         &self,
+         wrapped_reference: &Reference,
+         datom: &Datom,
+         budget: &mut Budget,
+     ) -> Result<(), Error> {
+         let held = wrapped_reference.clone();
+         let position = Position::Referenced(held);
+         let positions = [position];
+         self.positions(&positions, datom, budget)
+     }
  }
```

### Proposal C18: ethos-zero › src/generation.rs

A new type is emitted as a tuple struct of one field with the struct derives; cycles are found through new types, and boxed where they close. Rule: land, amend or reject.

```rust
  //! a recursive type archives and restores.

+ use crate::TypeDeclaration::Newtype;
  use proc_macro2::{Ident, Span, TokenStream};
  use quote::quote;
```

```rust
  }

- /// The trait whose capability tells whether a value holds the target type, through declared types, aliases, Option and Result, and Vector when the passage allows it.
+ /// A reach under way: the type sought, the
+ /// containment it may pass, the file whose
+ /// declarations it walks, and the declared
+ /// types it has already entered.
+ struct Reach<'a> {
+     target: &'a Name,
+     passage: Passage,
+     file: &'a File,
+     visited: Vec<Name>,
+ }
+
+ /// The trait whose capability tells whether a
+ /// value holds the target type, through declared
+ /// types, `Option` and `Result`, and `Vector`
+ /// when the passage allows it.
  trait Reaching {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool;
+     fn reaches(&self, reach: &mut Reach) -> bool;
+ }
+
+ /// The trait whose capability walks into a
+ /// declared type, once.
+ trait Entering {
+     /// Whether the declared type named reaches
+     /// the target; never twice the same one.
+     fn enter(&mut self, name: Name) -> bool;
+ }
+
+ impl Entering for Reach<'_> {
+     fn enter(&mut self, name: Name) -> bool {
+         if self.visited.contains(&name) {
+             return false;
+         }
+         let file = self.file;
+         let declared = file.declaration(&name);
+         self.visited.push(name);
+         let Some(declaration) = declared else {
+             return false;
+         };
+         declaration.reaches(self)
+     }
  }

  impl Reaching for Reference {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool {
+     fn reaches(&self, reach: &mut Reach) -> bool {
          if self.source.is_none() {
-             if &self.name == target || self.name.0 == "Self" {
+             let name = &self.name;
+             let itself = name.0 == "Self";
+             if name == reach.target || itself {
                  return true;
              }
-             match file.resolve(&self.name) {
-                 Resolution::Intrinsic(Intrinsic::Vector) if passage == Passage::ByValue => {
+             use Intrinsic::Vector;
+             use Resolution::Intrinsic as Known;
+             let by_value = Passage::ByValue;
+             let stops = reach.passage == by_value;
+             let file = reach.file;
+             match file.resolve(name) {
+                 Known(Vector) if stops => {
                      return false;
                  }
-                 Resolution::Type(name) if !visited.contains(&name) => {
-                     visited.push(name.clone());
-                     if let Some(declaration) = file.declaration(&name)
-                         && declaration.reaches(target, passage, file, visited)
-                     {
+                 Resolution::Type(name) => {
+                     if reach.enter(name) {
                          return true;
                      }
```

```rust
          }
          for argument in &self.arguments {
-             if argument.reaches(target, passage, file, visited) {
+             if argument.reaches(reach) {
                  return true;
              }
```

```rust

  impl Reaching for [Reference] {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool {
+     fn reaches(&self, reach: &mut Reach) -> bool {
          for reference in self {
-             if reference.reaches(target, passage, file, visited) {
+             if reference.reaches(reach) {
                  return true;
              }
```

```rust

  impl Reaching for [Position] {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool {
+     fn reaches(&self, reach: &mut Reach) -> bool {
          for position in self {
-             if position.reference().reaches(target, passage, file, visited) {
+             let held = position.reference();
+             if held.reaches(reach) {
                  return true;
              }
```

```rust

  impl Reaching for TypeDeclaration {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool {
+     fn reaches(&self, reach: &mut Reach) -> bool {
+         use TypeDeclaration::Enum;
          match self {
              TypeDeclaration::Struct(_, positions) | TypeDeclaration::Sealed(_, positions) => {
-                 positions.reaches(target, passage, file, visited)
+                 positions.reaches(reach)
              }
-             // Behind its lock, a shared type's state is reached through a pointer.
+             // Behind its lock, a shared type's
+             // state is reached through a pointer.
              TypeDeclaration::Shared(_, _) => false,
-             TypeDeclaration::Enum(_, variants) => variants.reaches(target, passage, file, visited),
-             TypeDeclaration::Alias(_, aliased) => aliased.reaches(target, passage, file, visited),
+             Enum(_, variants) => {
+                 // Through any of its variants.
+                 variants.reaches(reach)
+             }
+             Newtype(_, held) => {
+                 // It holds its type by value.
+                 held.reaches(reach)
+             }
          }
      }
```

```rust

  impl Reaching for Variant {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool {
+     fn reaches(&self, reach: &mut Reach) -> bool {
          match self {
-             Variant::Bare(name) => match file.declaration(name) {
-                 Some(_) => name.carried().reaches(target, passage, file, visited),
-                 None => false,
-             },
-             Variant::Typed(_, reference) => reference.reaches(target, passage, file, visited),
-             Variant::Struct(_, positions) => positions.reaches(target, passage, file, visited),
-             Variant::Enum(_, variants) => variants.reaches(target, passage, file, visited),
+             Variant::Bare(name) => {
+                 let file = reach.file;
+                 let held = file.declaration(name);
+                 if held.is_none() {
+                     return false;
+                 }
+                 // It carries the type it names.
+                 name.carried().reaches(reach)
+             }
+             Variant::Typed(_, reference) => {
+                 // It carries the type it names.
+                 reference.reaches(reach)
+             }
+             Variant::Struct(_, positions) => {
+                 // Its payload, declared in place.
+                 positions.reaches(reach)
+             }
+             Variant::Enum(_, variants) => {
+                 // Its payload, declared in place.
+                 variants.reaches(reach)
+             }
          }
      }
```

```rust

  impl Reaching for [Variant] {
-     fn reaches(
-         &self,
-         target: &Name,
-         passage: Passage,
-         file: &File,
-         visited: &mut Vec<Name>,
-     ) -> bool {
+     fn reaches(&self, reach: &mut Reach) -> bool {
          for variant in self {
-             if variant.reaches(target, passage, file, visited) {
+             if variant.reaches(reach) {
                  return true;
              }
```

```rust
              return true;
          }
-         match file.resolve(&self.name) {
-             Resolution::Intrinsic(Intrinsic::Vector) => return false,
-             Resolution::Type(name) => match file.declaration(&name) {
-                 Some(TypeDeclaration::Alias(_, aliased)) => {
-                     if aliased.closes(owner, file) {
-                         return true;
-                     }
-                 }
-                 Some(declaration) => {
-                     let earlier = match (file.place(&name), file.place(owner)) {
-                         (Some(named), Some(owning)) => named <= owning,
-                         _ => false,
-                     };
-                     if earlier
-                         && declaration.reaches(owner, Passage::ByValue, file, &mut vec![name])
-                     {
-                         return true;
-                     }
-                 }
-                 None => {}
-             },
-             _ => {}
+         use Intrinsic::Vector;
+         use Resolution::Intrinsic as Known;
+         let resolved = file.resolve(&self.name);
+         if let Known(Vector) = resolved {
+             return false;
+         }
+         if let Resolution::Type(name) = resolved
+             && (file, owner).returns(name)
+         {
+             return true;
          }
          for argument in &self.arguments {
```

```rust
  }

+ /// The trait whose capability says whether a
+ /// type declared no later than an owner reaches
+ /// it back by value.
+ trait Returning {
+     fn returns(&self, name: Name) -> bool;
+ }
+
+ /// A file and the owner a reach returns to.
+ type Owned<'a> = (&'a File, &'a Name);
+
+ impl Returning for Owned<'_> {
+     fn returns(&self, name: Name) -> bool {
+         let (file, owner) = *self;
+         let declared = file.declaration(&name);
+         let Some(declaration) = declared else {
+             return false;
+         };
+         let Some(named) = file.place(&name) else {
+             return false;
+         };
+         let owning = file.place(owner);
+         let Some(owning) = owning else {
+             return false;
+         };
+         if named > owning {
+             return false;
+         }
+         let mut reach = Reach {
+             target: owner,
+             passage: Passage::ByValue,
+             file,
+             visited: vec![name],
+         };
+         declaration.reaches(&mut reach)
+     }
+ }
+
  /// The trait whose capabilities yield a position's Rust type, boxed where it
  /// closes a by-value cycle, and the archive attribute it bears.
```

```rust

      fn recursive(&self, scope: &Scope, owner: &Name) -> bool {
-         self.reaches(owner, Passage::Any, scope.file, &mut vec![])
+         let mut reach = Reach {
+             target: owner,
+             passage: Passage::Any,
+             file: scope.file,
+             visited: vec![],
+         };
+         self.reaches(&mut reach)
      }

```

```rust
  }

+ /// The trait whose capability emits a new type
+ /// over the one type it wraps: a tuple struct of
+ /// one field with the derives a struct gets.
+ trait Wrapping {
+     fn wrap(&self, scope: &Scope) -> TokenStream;
+ }
+
+ /// A new type: its identity and the type it
+ /// holds.
+ type Wrapped<'a> = (&'a Identity, &'a Reference);
+
+ impl Wrapping for Wrapped<'_> {
+     fn wrap(&self, scope: &Scope) -> TokenStream {
+         let (identity, held) = *self;
+         let owner = &identity.name;
+         let name = owner.tokens();
+         let derive = identity.datom_derives();
+         let field = held.position(scope, owner);
+         let archive = held.archival(scope, owner);
+         let cyclic = held.recursive(scope, owner);
+         let bounds = match cyclic {
+             true => identity.recursion_bounds(),
+             false => TokenStream::new(),
+         };
+         quote! {
+             #derive
+             #bounds
+             pub struct #name(#archive pub #field);
+         }
+     }
+ }
+
  impl Emitting for TypeDeclaration {
      fn emit(&self, scope: &Scope) -> TokenStream {
```

```rust
                  variants.enumeration(&inner, &identity.name, identity)
              }
-             TypeDeclaration::Alias(identity, aliased) => {
+             Newtype(identity, held) => {
                  let inner = Scope {
                      file: scope.file,
```

```rust
                      associated: scope.associated,
                  };
-                 let name = identity.name.tokens();
-                 let parameters = identity.parameters(&inner);
-                 let aliased = aliased.emit(&inner);
-                 quote! { #[rustfmt::skip] pub type #name #parameters = #aliased; }
+                 (identity, held).wrap(&inner)
              }
          }
```

```rust
              items.extend(body.root.items(scope));
          }
+         let lints = quote! {
+             dead_code,
+             non_camel_case_types,
+             non_snake_case
+         };
+         // A new type's field writes its type in
+         // full, however deep the schema nests it.
+         let complexity = quote! {
+             clippy::type_complexity
+         };
          quote! {
-             #![allow(dead_code, non_camel_case_types, non_snake_case)]
+             #![allow(#lints)]
+             #![allow(#complexity)]
              #( #items )*
          }
```

### Proposal C19: ethos-zero › src/lib.rs

The alias declaration becomes a new type over one other type. Rule: land, amend or reject.

```rust
  }

- /// A type declaration: a struct of positions, an enum of variants, or an alias.
+ /// A type declaration: a struct of positions,
+ /// an enum of variants, or a new type over one
+ /// other type.
  #[derive(Clone, Debug, PartialEq, Eq)]
  pub enum TypeDeclaration {
```

```rust
      /// A headed bracket: the variants.
      Enum(Identity, Vec<Variant>),
-     /// A headed bare: the aliased type.
-     Alias(Identity, Reference),
+     /// A headed bare, `Name.String`: a new type
+     /// over the one type it holds, never an
+     /// alias; generated as a tuple struct of one
+     /// field with the derives a struct gets.
+     Newtype(Identity, Reference),
      /// A sealed struct, `Name.Sealed.{ positions }`: its positions are
      /// private in the generated Rust, and it is built only by a `:`
```

```rust
  #[derive(Clone, Copy, Debug, PartialEq, Eq)]
  pub enum Role {
-     /// A type: a position, an alias, an input, a yield, an argument.
+     /// A type: a position, a new type's held
+     /// type, an input, a yield, an argument.
      Type,
      /// A trait: a constraint, a supertrait, a bound, an association.
```

### Proposal C20: ethos-zero › src/protosization.rs

A new type whose held type takes arguments ascends with those arguments beside it. Rule: land, amend or reject.

```rust

  use crate::Root;
+ use crate::TypeDeclaration::Newtype;
  use crate::sectioning::Sectioning;
  use crate::{
```

```rust
      }
  }
+ /// A new type and the type it holds.
+ type Beside<'a> = (&'a Identity, &'a Reference);
+
+ /// The trait whose capability finds a new type
+ /// whose held type takes arguments, which stand
+ /// beside it in a list.
+ trait Besiding {
+     fn beside(&self) -> Option<Beside<'_>>;
+ }
+
+ impl Besiding for TypeDeclaration {
+     fn beside(&self) -> Option<Beside<'_>> {
+         let Newtype(identity, held) = self else {
+             return None;
+         };
+         if held.arguments.is_empty() {
+             return None;
+         }
+         Some((identity, held))
+     }
+ }
+
  impl DeclarationsProtosizing for [TypeDeclaration] {
      fn declaration_nodes(&self) -> Vec<Protos> {
          let mut nodes = Vec::new();
          for declaration in self {
-             match declaration {
-                 TypeDeclaration::Alias(identity, reference) if !reference.arguments.is_empty() => {
+             match declaration.beside() {
+                 Some((identity, reference)) => {
                      let body = match &reference.source {
                          Some(source) => source.as_ref().headed(
```

```rust
                  "".enclosed(Enclosure::Bracketed, variants.variant_nodes()),
              ),
-             Self::Alias(identity, reference) => {
-                 identity.heading(Separator::Period, reference.protos())
+             Self::Newtype(identity, held) => {
+                 let body = held.protos();
+                 let period = Separator::Period;
+                 identity.heading(period, body)
              }
              Self::Shared(identity, positions) => identity.heading(
```

```rust
      fn alone(&self) -> Protos {
          match self {
-             Self::Alias(identity, reference)
+             Self::Newtype(identity, reference)
                  if reference.source.is_none()
                      && reference.name.as_ref() == "Vector"
```

### Proposal C21: ethos-zero › src/sectioning.rs

Sectioning names the new type declaration in place of the alias. Rule: land, amend or reject.

```rust
              }
              TypeDeclaration::Enum(_, variants) => variants.hoist_variants(body, placed),
-             TypeDeclaration::Alias(_, _) => {}
+             TypeDeclaration::Newtype(_, _) => {}
          }
      }
```

### Proposal C22: ethos-zero › src/location.rs

A location writes its line and column as the new types Line and Column. Rule: land, amend or reject.

```rust
  use crate::sugaring::Sugaring;
  use crate::{Canonicalizable, Error, File, Locating, Location, Potential, Resituating};
+ use crate::{Column, Line};

  /// The trait whose capability finds the extent of the node a path names.
```

```rust
          };
          Location {
-             line: line as Integer,
-             column: column as Integer,
+             line: Line(line as Integer),
+             column: Column(column as Integer),
          }
      }
```

### Proposal C23: ethos-zero › src/checking.rs

A struct of one position and an enum of one variant are refused at their head, also when declared in place as a payload. Rule: land, amend or reject.

```rust
      TraitBody, TraitDeclaration, TypeDeclaration, Variant,
  };
+ use Problem::{SinglePosition, SingleVariant};

  /// A schema must remain small enough for complete whole-file checking to have
```

```rust
              associated: scope.associated,
          };
-         match self {
+         let checked = match self {
              TypeDeclaration::Struct(_, positions) => positions.check_children(&inner).place(1),
              TypeDeclaration::Sealed(_, positions) | TypeDeclaration::Shared(_, positions) => {
```

```rust
                  checked.lifted(1)
              }
+         };
+         checked?;
+         self.single()
+     }
+ }
+
+ /// The trait whose capability refuses a shape of
+ /// one member, at the head that names it: a
+ /// struct of one position is a new type, written
+ /// `X.String`, and an enum of one variant chooses
+ /// nothing.
+ trait Plural {
+     fn plural(&self, name: &Name) -> Checked;
+ }
+
+ impl Plural for [Position] {
+     fn plural(&self, name: &Name) -> Checked {
+         if self.len() != 1 {
+             return Ok(());
+         }
+         let named = name.0.clone();
+         let problem = SinglePosition(named);
+         Err(Error::conceptual(vec![0], problem))
+     }
+ }
+
+ impl Plural for [Variant] {
+     fn plural(&self, name: &Name) -> Checked {
+         if self.len() != 1 {
+             return Ok(());
+         }
+         let named = name.0.clone();
+         let problem = SingleVariant(named);
+         Err(Error::conceptual(vec![0], problem))
+     }
+ }
+
+ /// The trait whose capability refuses a
+ /// declaration or a payload of one member, once
+ /// what it holds has checked.
+ trait Single {
+     fn single(&self) -> Checked;
+ }
+
+ /// A sealed or shared struct keeps its one
+ /// position: it has no other way to be written.
+ impl Single for TypeDeclaration {
+     fn single(&self) -> Checked {
+         use TypeDeclaration::{Enum, Struct};
+         let name = &self.identity().name;
+         match self {
+             Struct(_, positions) => {
+                 // One position: a new type.
+                 positions.plural(name)
+             }
+             Enum(_, variants) => {
+                 // One variant chooses nothing.
+                 variants.plural(name)
+             }
+             _ => Ok(()),
+         }
+     }
+ }
+
+ impl Single for Variant {
+     fn single(&self) -> Checked {
+         match self {
+             Variant::Struct(name, positions) => {
+                 // One position: a new type.
+                 positions.plural(name)
+             }
+             Variant::Enum(name, variants) => {
+                 // One variant chooses nothing.
+                 variants.plural(name)
+             }
+             _ => Ok(()),
          }
      }
```

```rust
  impl Checkable for Variant {
      fn check(&self, scope: &Scope) -> Result<(), Error> {
-         match self {
+         let checked = match self {
              Variant::Bare(name) => name.define(),
              Variant::Typed(name, reference) => {
```

```rust
                  variants.check_children(scope).place(1)
              }
-         }
+         };
+         checked?;
+         self.single()
      }
  }
```

### Proposal C24: ethos-zero › src/conception.rs

A Type root enum of one variant is no longer refused by the reader, so the checker refuses it as in every root. Rule: land, amend or reject.

```rust
              Some(Head::Type) => {
                  let declaration: TypeDeclaration = body.conceive().place(1)?;
-                 // A type file declares one type whole; an enum of it needs at
-                 // least two variants, or it would be a struct or an alias.
+                 // A type file declares one type
+                 // whole; an empty enum declares
+                 // nothing. One of one variant is
+                 // refused as in every root.
                  if let TypeDeclaration::Enum(_, variants) = &declaration
-                     && variants.len() < 2
+                     && variants.is_empty()
                  {
                      return Err(Error::conceptual(
```

### Proposal C25: ethos-zero › error.ethos

The problems SinglePosition and SingleVariant are added. Rule: land, amend or reject.

```ethos
              Sealed.String
              Shared.String
-             Foreign.String ]
+             Foreign.String
+             SinglePosition.String
+             SingleVariant.String ]
    Form.[ File Section Import Name Declaration Variant Reference Constraint Trait Capability Constant Association ]
    Location.{ Line Column }
```

### Proposal C26: ethos-zero › src/checking.rs

A declared type, or a generated implied enum, that no association names as bearing a trait is refused as Traitless. Rule: land, amend or reject.

```rust
      TraitBody, TraitDeclaration, TypeDeclaration, Variant,
  };
+ use Problem::Traitless;
  use Problem::{SinglePosition, SingleVariant};

```

```rust
          self.sealed()?;
          self.shared()?;
-         self.foreign()
+         self.foreign()?;
+         self.traitless()
+     }
+ }
+
+ // Borne types (proposal): every type a file
+ // declares bears a trait.
+
+ /// The trait whose capability refuses a type no
+ /// association names as bearing a trait, in
+ /// either form: a type the file declares, in
+ /// place too, and an enum a Signal or an
+ /// Operation implies and generates. A `Type`
+ /// root has no associations, and stands as it is.
+ trait Bearers {
+     fn traitless(&self) -> Checked;
+ }
+
+ impl Bearers for File {
+     fn traitless(&self) -> Checked {
+         if let File::One(Root::Type(_)) = self {
+             return Ok(());
+         }
+         let mut bearers = Vec::new();
+         for bearing in self.bearings() {
+             if !bearing.members.is_empty() {
+                 let name = bearing.identity.name;
+                 bearers.push(name);
+             }
+         }
+         let mut declared = Vec::new();
+         for placed in self.declarations() {
+             let declaration = placed.declaration;
+             let identity = declaration.identity();
+             let name = identity.name.clone();
+             let mut path = placed.path;
+             path.push(0);
+             declared.push((path, name));
+         }
+         for implied in self.implied_enums() {
+             // An empty one is never generated.
+             if !implied.variants.is_empty() {
+                 let name = implied.name;
+                 let path = implied.path;
+                 declared.push((path, name));
+             }
+         }
+         let mut found = None;
+         for (path, name) in declared {
+             if !bearers.contains(&name) {
+                 found = Some((path, name));
+                 break;
+             }
+         }
+         let Some((path, name)) = found else {
+             return Ok(());
+         };
+         let problem = Traitless(name.0);
+         Err(Error::conceptual(path, problem))
      }
  }
```

### Proposal C27: ethos-zero › error.ethos

The problem Traitless is added, and the error types bear Sized. Rule: land, amend or reject.

```ethos
              Foreign.String
              SinglePosition.String
-             SingleVariant.String ]
+             SingleVariant.String
+             Traitless.String ]
    Form.[ File Section Import Name Declaration Variant Reference Constraint Trait Capability Constant Association ]
    Location.{ Line Column }
```

```ethos
    Column.Integer ]
  []
- [] }
+ [ Sized.[ Structural_Error Error Problem Form Location Line Column ] ] }
```

### Proposal C28: ethos-zero › ethos-zero.ethos

The crate own query, response and generation types bear Sized. Rule: land, amend or reject.

```ethos
  ; A file headed Sema is refused as Renamed.Memory. A file is an ordinary datom:
  ; its root's variant, the dot, then the braced sections (proposal).
+ ; Every type it declares bears a trait (proposal); these bear Sized.
  Library.
  {
```

```ethos
                                    ethos_zero:Problem } ] ]
  []
- [] }
+ [ Sized.[ Query Response Generation Conformance Generation_Error ] ] }
```
