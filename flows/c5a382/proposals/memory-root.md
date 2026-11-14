Presentation.{ «The Memory root's change and upgrade» }

# The Memory root's change and upgrade

Fable 5.1 wrote this proposal; Opus publishes it.

## psyche-belief › vision/memory.md

## What memory is, long term

In the long term, memory is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Memory, declares record types. It matters more than nexus, because operational editing should yield the migration with the edit.

```
Memory
[]                                                        ; imports
[ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
                                                          ; the remaining sections are to be decided
```

### Proposal 1: The Memory root's four sections · psyche-belief › vision/memory.md

**Comment** vision:ethos says a memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format, and that a version lives in a manifest. memory-engine 0.18 has these as Memorable, UpgradeFrom and MemoryDefinition, each written by hand per record; the flow Nexus writes seven of them. This proposal gives the Memory root the two sections that declare them, so ethos-zero generates the types and the assertions, and the engine's traits are the ones the vision names. ethos-zero today accepts a Memory root of two sections and no generic type declaration, so the first two ethos fences are what it is to accept and are rejected by it now; the manifest fence passes its Check.

  ## What memory is, long term

  In the long term, memory is the database engine of a Nexus, authored in Ethos so the stored types are visible; its root, Memory, declares record types. It matters more than nexus, because operational editing should yield the migration with the edit.

- ```
- Memory
- []                                                        ; imports
- [ Lock.{ LockId LockName FlowId LockPaths LockReason } ]  ; record types
-                                                           ; the remaining sections are to be decided
- ```
+ ## The four sections
+
+ A Memory root has four sections: imports, records, changes and upgrades. A record is a type the engine stores. A change names, for each record, the change the record accepts and the refusal it may answer with. An upgrade names, for each record, the previous format it upgrades from, declared inline: the format the type had before the edit, so the edit and its migration are read together.
+
+ ```ethos
+ Memory
+ [ orchestrate:[ LockId LockName FlowId   ; imports
+                 LockPaths LockReason ] ]
+ [ Lock.{ LockId LockName FlowId          ; records
+          LockPaths LockReason } ]
+ [ Lock.{ Change.[ Reserve.{ LockName  ; changes
+                             FlowId
+                             LockPaths
+                             LockReason }
+                   Release.FlowId ]
+          Refusal.[ Held.FlowId
+                    PathOverlap.Lock ] } ]
+ [ Lock.{ LockId LockName FlowId     ; upgrades
+          LockPaths } ]
+ ```
+
+ ## What the root generates
+
+ Every record bears Memorizable; the upgrade section makes it bear UpgradeFrom its previous format. The types are generated: the record, its change, its refusal and its previous format, each bearing the datom kinds under the feature, each archiving in rkyv. The two traits are defined once, in the standard library, and the generated Rust asserts the record bears them; the bodies, the change and the upgrade, are hand-written, as every interaction body is. A change is pure: it yields the successor record, or the record's own refusal, and the engine commits the successor.
+
+ ```ethos
+ Library
+ []
+ [ Decision<Record Refusal>.[            ; tentative
+      Ready.Record
+      Refused.Refusal ] ]
+ [ Memorizable.{
+      []
+      [ Change Refusal ]           ; associated
+      []
+      [ change:{ [ Option<Self> Change ]
+                 [ Decision<Self Refusal> ] } ] }
+   UpgradeFrom<Previous>.{
+      []
+      [ Refusal ]
+      []
+      [ upgrade_from:{ [ Previous ]
+                       [ Decision<Self Refusal> ]
+                     } ] } ]
+ []
+ ```
+
+ ```rust
+ // generated: the types, and the assertions
+ pub struct Lock { … }
+ pub enum Lock_Change {
+     Reserve(Reserve_Data), Release(FlowId) }
+ pub enum Lock_Refusal {
+     Held(FlowId), PathOverlap(Lock) }
+ pub struct Lock_Previous { … }   // before the edit
+ const _: () = {
+     fn memorizable<T: Memorizable>() {}
+     let _ = memorizable::<Lock>;
+     fn upgrades<T: UpgradeFrom<Lock_Previous>>() {}
+     let _ = upgrades::<Lock>;
+ };
+ ```
+
+ ```rust
+ // hand-written: the bodies
+ impl Memorizable for Lock {
+     type Change = Lock_Change;
+     type Refusal = Lock_Refusal;
+     fn change(current: Option<&Self>,
+               change: &Lock_Change)
+         -> Decision<Self, Lock_Refusal> { … }
+ }
+ impl UpgradeFrom<Lock_Previous> for Lock {
+     type Refusal = Infallible;
+     fn upgrade_from(previous: Lock_Previous)
+         -> Decision<Self, Infallible> {
+         Decision::Ready(Lock {
+             lock_reason: LockReason::Unknown,
+             ..previous.into() })
+     }
+ }
+ ```
+
+ ## The manifest
+
+ The ethos file is unversioned; the version of each record lives in the manifest beside it, memory.datom, one entry per record. The engine reads the version from the manifest and the schema hash from the record's declaration, the hash of its canonical ethos text, so two records with one shape share a hash and a changed shape changes it. An upgrade edge runs from the version before to the version in the manifest; only a forward edge is admitted.
+
+ ```ethos
+ Library
+ []
+ [ RecordName.String
+   Version.Integer
+   Entry.{ RecordName Version }
+   Manifest.Vector<Entry> ]
+ []
+ []
+ ```
+
+ ```datom
+ ; memory.datom, beside memory.ethos
+ [ { Lock 3 } ]
+ ```
+
+ ```mermaid
+ flowchart TB
+     e["memory.ethos"] -- "generates" --> t["types"]
+     e -- "hashes" --> h["schema hash"]
+     m["memory.datom"] -- "gives" --> v["version"]
+     t -- "hand-written" --> b["change, upgrade"]
+     b -- "engine commits" --> s["stored record"]
+ ```
