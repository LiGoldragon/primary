Presentation.{ «A scalar newtype carries its scalar's capabilities» Proposal }
# A scalar newtype carries its scalar's capabilities

Created by Fable 5.1, alone.

### Proposal 1: A scalar newtype carries its scalar's capabilities · psyche-belief › vision/ethos.md

**Comment** Added after the newtype line of "What a declaration turns into". The newtype line stays; what a newtype over a scalar can do is said once, so no association names it.

  A head over a single type declares a newtype: a single-member tuple struct holding it, so every declared name is its own type and carries its own derive.
+
+ A newtype over a scalar carries its scalar's capabilities: ordering, equality, hashing, and arithmetic where the scalar has it. They are implied by the newtype, as the datom traits are; an association names a trait written in the file, declared there or imported: Summarizable, Textualizable.
+
+ The Ethos:
+
+ ```ethos
+ Library
+ []                      ; imports
+ [ LockId.Integer        ; types: scalar newtypes
+   LockName.String ]
+ []                      ; traits
+ []                      ; associations: none; the
+                         ;   scalar's capabilities
+                         ;   come with the newtype
+ ```
+
+ The Rust generated from it:
+
+ ```rust
+ // what Integer can do, LockId can do
+ #[derive(Datomizable, Compositional,
+          Clone, Copy, PartialEq, Eq,
+          PartialOrd, Ord, Hash)]
+ pub struct LockId(pub Integer);
+ #[derive(Datomizable, Compositional,
+          Clone, PartialEq, Eq,
+          PartialOrd, Ord, Hash)]
+ pub struct LockName(pub String);
+ ```
