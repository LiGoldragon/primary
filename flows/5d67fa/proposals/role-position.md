Presentation.{ «A role is a type» Proposal }

# A role is a type

Created by Fable 5.2, on the evidence of Psyche core Opus.

### Proposal 1: Two positions of one type, told apart by role · psyche-belief › vision/ethos.md

::: comment
A lock in the message Nexus holds two addresses, a sender and a recipient. Written as two bare addresses it generates a first and a second address, and nothing says which is which. The wrapping rule refuses a head that names nothing the type does not; here the head names the role, which the type does not. Opus read it as a name for the position only; I propose it as a type, since Ethos has types in positions and nothing else, and two types cannot be swapped where two fields of one type can.
:::

  A type that has a name is used by its name: a variant or a position carrying a defined type carries it bare, and a head over a type that is not a scalar, a struct, an enum, a vector or a newtype, is refused by ethos-zero. The newtype, a head over a single scalar, is the one wrapping there is; a struct whose only content is one other type is that type, written as it.

+ A struct that holds one type in two roles names each role as a head over the type, in the position. The role is a newtype over that type, as a head over a scalar is, so the two positions are two types and one cannot be given where the other is wanted. The text is the same either way.

+ The Ethos:

+ ```ethos
+ Library
+ [ flow:Address ]                       ; imports
+ [ Lock.{ Sender.Address                ; types: one type in two roles, each role a head in its position
+          Recipient.Address } ]
+ []                                     ; traits
+ []                                     ; associations
+ ```

+ The Rust generated from it:

+ ```rust
+ #[derive(Datomizable, Compositional)] pub struct Sender(pub Address);
+ #[derive(Datomizable, Compositional)] pub struct Recipient(pub Address);
+ #[derive(Datomizable, Compositional)]
+ pub struct Lock { pub sender: Sender, pub recipient: Recipient }   // a Recipient where the Sender goes does not compile
+ ```

+ The datom, the same as for two bare addresses:

+ ```datom
+ { { Psyche core Opus } { Mind core Sol } }
+ ```
