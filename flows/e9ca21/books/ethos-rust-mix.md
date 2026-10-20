<!-- to-the-living:start -->
Presentation.{ «Ethos and Rust in Shapes and placement» }

# Ethos and Rust in Shapes and placement

```
+--------------------------------+
| record, August:                |
| ethos shows the Rust           |
| it generates                   |
+--------------------------------+
               |
               | led to
               v
+--------------------------------+
| Rust written by hand under     |
| each Ethos example             |
+--------------------------------+
               |
               | landed in
               v
+--------------------------------+
| vision-ethos                   |
+--------------------------------+
               |
               | shown whole in
               v
+--------------------------------+
| imports and definition         |
| brackets, second edition       |
+--------------------------------+

+--------------------------------+
| records, October:              |
| just show me the Ethos         |
+--------------------------------+
               |
               | crystallized as
               v
+--------------------------------+
| Proposal 2                     |
+--------------------------------+
               |
               | removes, by
               v
+--------------------------------+
| Proposal 3: the Rust under     |
| Shapes and placement           |
+--------------------------------+
```

### Proposal 1: mind-context › inquiry/ethos-rust-examples.md, a new file

+ ---
+ description: Why vision-ethos closes its Ethos examples with Rust, and how that Rust differs from what the generator emits.
+ ---
+
+ ## Rust under the Ethos examples
+
+ vision-ethos closes its Ethos examples with the Rust each is meant to turn into, as an earlier record asked: ethos shows what Rust is generated. That Rust is written by hand, not taken from the generator, and no label says which block is Ethos and which is Rust. Under Shapes and placement, for the Lock Signal, ethos-zero emits the aliases as i64 and String, a struct LockRequest, a struct Lock, and derives on every type; the hand-written block has no structs and no derives, and writes Integer, datom-codec's name for i64, where the generator writes i64. A book that shows the section as it stands puts the two blocks side by side.
+
+ Later records say the opposite of the earlier one: show the Ethos, and the Rust it generates only when the work is on how Ethos generates Rust. Proposal 2 carries them together. Eleven other sections of vision-ethos close with Rust written the same way; once Proposal 2 stands, each is proposed kept as generated Rust, replaced by the generator's output, or removed.

### Proposal 2: psyche-context › vision/ethos.md

+ ## Ethos is shown, not the Rust it generates
+
+ An example shows the Ethos alone. Rust is shown only where the subject is how Ethos generates Rust, and then it is the Rust the generator emits.

### Proposal 3: psyche-context › vision/ethos.md

````text
    Lock.{ LockId LockName } ]
  ```
- ```rust
- pub enum Query    { Lock(LockRequest), Release(LockId) }
- pub enum Response { Locked(Lock), Released(Lock) }
- pub type LockId = Integer;
- pub type LockName = String;
- pub type FlowId = String;
- ```
````
<!-- to-the-living:end -->
