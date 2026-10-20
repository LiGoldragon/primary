```
+--------------------+
| Topic              |
+--------------------+
   | holds
   v
+--------------------+
| a coinage: a word  |
| made by a person   |
+--------------------+
   ^
   | yields
+---------------------------------+
| coin                            |
+---------------------------------+
   | checks             | refuses as
   v                    v
+---------------+  +--------------+
| entered text  |  | Malformation |
+---------------+  +--------------+
```

### Proposal 1: psyche-context › vision/ethos.md

+ ## An extendable enum takes coinages made on demand
+ 
+ An extendable enum has fixed variants, which are capitalized, and takes entries made on demand.
+ A made entry is a coinage: words only, an uncapitalized camelCase identifier, created on demand and more descriptive than a variant.
+ Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
  ## Every declared type bears both traits

### Proposal 2: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ The made-entry type is Coinage.

### Proposal 3: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ The made-entry type is Epithet.

### Proposal 4: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ The made-entry type is Appellation.

### Proposal 5: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
+ An enum is extendable when Coinage is one of its variants.

```ethos
+ Library.{
+ []
+ [ Coinage.{ String }
+   Colour.[ Red Green Blue Coinage ] ]
+ []
+ [] }
```

### Proposal 6: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
+ Every enum takes coinages; nothing in its declaration marks it.

### Proposal 7: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
+ A declared extendable enum generates one unit variant per fixed entry and a Coinage variant carrying the Coinage struct, whose one field is the coinage's string.

### Proposal 8: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
+ A coinage that is not an uncapitalized camelCase identifier is refused when it is made.

### Proposal 9: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
+ A coinage, once approved, is added to its enum as a capitalized fixed variant, and the system is recompiled.

### Proposal 10: psyche-context › vision/ethos.md

  Its first letter tells it apart from a fixed variant, and it carries the coinage as its string.
+ 
+ Promotion migrates every stored value holding the coinage to the new fixed variant in the same change; the coinage form is not read afterwards.

### Proposal 11: psyche-context › vision/datom.md

  carrying the Locks variant carrying an empty vector. A symbol alone,
- in a position expecting an enum, is a variant carrying nothing. A
- datom is not preceded by a Datom root; a comment may say it is datom.
+ in a position expecting an enum, is a variant carrying nothing when it is capitalized.
+ The datom reader reads an uncapitalized symbol alone, in a position expecting an extendable enum, as a coinage, written bare without the variant's head.
+ A datom is not preceded by a Datom root; a comment may say it is datom.
  Guillemets are the string delimiter, and parentheses are reserved for

### Proposal 12: psyche-context › vision/flow.md

- Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
+ Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a coinage, checked when created; core is the permanent topic. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.

### Proposal 13: flow › crates/flow-ethos/ethos/library.ethos

```diff
- Library
+ Library.{
  []
  [ FlowId.String
-   ; ethos-zero 16 cannot express Topic:Name yet; check camelCase at input.
-   Topic.String
+   ; A topic is a coinage; core is permanent.
+   Coinage.{ String }
+   Topic.Coinage
```
```diff
  []
- []
+ [] }
```

### Proposal 14: flow › crates/flow-ethos/src/generated/library.rs

```rust
  #[rustfmt::skip]
- pub type Topic = String;
+ #[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
+ #[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
+ pub struct Coinage {
+     pub string: String,
+ }
+ #[rustfmt::skip]
+ pub type Topic = Coinage;
```

### Proposal 15: flow › crates/flow-ethos/ethos/library.ethos

```diff
  Library.{
- []
+ [ protos:[ Textualizable ] ]
  [ FlowId.String
```
```diff
    Topic.Coinage
+   Malformation.[ Capitalized NotCamelCase ]
```
```diff
- []
- [] }
+ [ Coined.[ coin:{
+             [ Textualizable ]
+             [ Result<Self Malformation> ] } ] ]
+ [ Coined.[ Coinage Topic ] ] }
```

### Proposal 16: flow › crates/flow-ethos/src/generated/library.rs

```rust
  pub type Topic = Coinage;
+ #[rustfmt::skip]
+ #[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
+ #[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
+ pub enum Malformation {
+     Capitalized,
+     NotCamelCase,
+ }
  #[rustfmt::skip]
  pub type Blake3 = String;
```
```rust
      pub lease: Lease,
  }
+ #[rustfmt::skip]
+ pub trait Coined {
+     fn coin<N: protos::Textualizable>(
+         input: N,
+     ) -> std::result::Result<Self, Malformation>
+     where
+         Self: Sized;
+ }
+ #[rustfmt::skip]
+ const _: () = {
+     fn assert_coinage_coined<T: Coined>() {}
+     let _ = assert_coinage_coined::<Coinage>;
+ };
+ #[rustfmt::skip]
+ const _: () = {
+     fn assert_topic_coined<T: Coined>() {}
+     let _ = assert_topic_coined::<Topic>;
+ };
```

### Proposal 17: psyche-context › vision/flow.md

- Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
+ Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is Core: the permanent topic, the thing that keeps the machine going, the last topic to stand.

- A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.
+ A topic is Core, or a coinage: a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, kept to six characters and lengthened when two collide, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process. Anybody may call Flow, a flow for its own refresh among them: because the CLI checks the calling process, a flow refreshes itself safely.

- Every flow has a topic; a flow with no special topic has the topic core, the heart of its aspect. A topic is a core:Name, a camelCaseExpression checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche core Secondary <id> }.
+ Every flow has a topic; a flow with no special topic has the topic Core, the heart of its aspect. A topic is an extendable enum whose one fixed variant is Core; any other topic is a coinage, checked when created. A flow's title is one datom struct of its aspect, topic, layer and flow id: { Psyche Core Secondary <id> }.

### Proposal 18: flow › crates/flow-ethos/ethos/library.ethos

```diff
- Library
+ Library.{
  []
  [ FlowId.String
-   ; ethos-zero 16 cannot express Topic:Name yet; check camelCase at input.
-   Topic.String
+   ; A topic Flow fixes, or any other as a coinage.
+   Coinage.{ String }
+   Topic.[ Core Coinage ]
```
```diff
  []
- []
+ [] }
```

### Proposal 19: flow › crates/flow-ethos/ethos/library.ethos

```diff
  Library.{
- []
+ [ protos:[ Textualizable ] ]
  [ FlowId.String
```
```diff
    Topic.[ Core Coinage ]
+   Malformation.[ UndeclaredVariant NotCamelCase ]
```
```diff
- []
- [] }
+ [ Coined.[ coin:{
+             [ Textualizable ]
+             [ Result<Self Malformation> ] } ] ]
+ [ Coined.[ Topic ] ] }
```

### Proposal 20: flow › crates/flow-ethos/src/generated/library.rs

```rust
  #[rustfmt::skip]
- pub type Topic = String;
+ #[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
+ #[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
+ pub struct Coinage {
+     pub string: String,
+ }
+ #[rustfmt::skip]
+ #[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
+ #[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
+ pub enum Topic {
+     Core,
+     Coinage(Coinage),
+ }
```

### Proposal 21: flow › crates/flow-ethos/src/generated/library.rs

```rust
      Coinage(Coinage),
  }
+ #[rustfmt::skip]
+ #[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq, Hash)]
+ #[cfg_attr(feature = "datom", derive(datom_codec::Datomizable, datom_codec::Composing))]
+ pub enum Malformation {
+     UndeclaredVariant,
+     NotCamelCase,
+ }
  #[rustfmt::skip]
  pub type Blake3 = String;
```
```rust
      pub lease: Lease,
  }
+ #[rustfmt::skip]
+ pub trait Coined {
+     fn coin<N: protos::Textualizable>(
+         input: N,
+     ) -> std::result::Result<Self, Malformation>
+     where
+         Self: Sized;
+ }
+ #[rustfmt::skip]
+ const _: () = {
+     fn assert_topic_coined<T: Coined>() {}
+     let _ = assert_topic_coined::<Topic>;
+ };
```
