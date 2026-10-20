<!-- to-the-living:start -->
Presentation.{ «The memory type and its traits» }

# The memory type and its traits

```
+------------------------------------------+
| Memory object, one file one main object  |
+------------------------------------------+
                    |
                    | defines
                    v
+------------------------------------------+
| stored types                             |
+------------------------------------------+
          |                       |
          | get from ethos-zero   | get by hand
          v                       v
+------------------+  +--------------------+
| rkyv and datom   |  | key, version,      |
| derives          |  | table (Rust)       |
+------------------+  +--------------------+
```

```
+------------------------------------------+
| Memory object                            |
+------------------------------------------+
      |              |               |
      | 1 declares   | 2 holds       | 3 implies
      v              v               v
+----------+  +-------------+  +-------------+
| trait    |  | types, each |  | traits for  |
| list     |  | with traits |  | every type  |
+----------+  +-------------+  +-------------+
      |              |               |
      | borne by     | borne by      | borne by
      v              v               v
+------------------------------------------+
| each stored type                         |
+------------------------------------------+
```

### Proposal 1: the memory object declares its traits · psyche-context › vision/ethos.md

Today a Memory object lists record types and nothing more: no traits, no key, no version, no table. ethos-zero gives every type in it the same rkyv and datom derives as every other type; the record key, the memory version and schema hash and the table are written by hand in Rust (Flow holds 39 record-key implementations and 13 memory definitions by hand, and none of its seven Ethos files is a Memory object).

The Memory object gains a section of its own that lists the traits; every type in it bears them. No syntax for that section exists or is designed, so no example is shown.

- What a reader sees: one list at the top of the object, then plain types. The traits are written, once, in the file.
- What the generator must know: a new Memory section, and the sema-engine trait paths and method signatures, so that it emits implementations; today it emits only assertions.
- Registry addressing: the object stays one main object under one name, and its traits live inside it.
- A trait added later: one line in the list, and every type in that object gains it. A single type cannot differ from the rest.
- "Every trait is written in ethos": met, written once at the object.

  Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.
+
+ A Memory object declares the traits its types bear, in a section of its own; every type defined in it bears those traits, and the generator emits them from that declaration.

Ruling: land, amend, or reject.

### Proposal 2: every trait is written out on each type · psyche-context › vision/ethos.md

Each stored type carries its own association, the form a Library already has. A Memory object has no associations section today, so it would gain one, or the types move to a Library. The trait name is illustrative.

```ethos
Library
[ super:[ Storable ] ]
[ Record.{ String Vector<Entry> }
  Entry.{ String Integer } ]
[]
[ Record.[ Storable ]
  Entry.[ Storable ] ]
```

- What a reader sees: each type's traits next to it. A long object repeats the same list on every type, and one type can lack it.
- What the generator must know: the same sema-engine facts as Proposal 1, since an association asserts a trait today and an implementation must still be emitted; it also needs to know which types are stored.
- Registry addressing: if the types sit in a Library, nothing in the object's name says it is the Memory; if they stay in a Memory object, the object is the one main object and the associations are inside it.
- A trait added later: every type is edited. A type left out is found by a mechanical check, and a type may deliberately differ.
- "Every trait is written in ethos": met most literally, in the file, once per type.

  Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.
+
+ A Memory object implies no trait: each type defined in it has its storable traits written in an association, as in any other root.

Ruling: land, amend, or reject.

### Proposal 3: a special memory object implies the traits · psyche-context › vision/ethos.md

The Memory root itself means that every type defined in it bears the storable traits. The file stays as it is today.

```ethos
Memory
[]
[ Record.{ String Vector<Entry> }
  Entry.{ String Integer } ]
```

- What a reader sees: no traits at all; the rule is in the vision. The same already holds for the datom traits on every type and for the associations of the Signal and Memory roots, which are implied and never written.
- What the generator must know: the storable set is fixed in Memory emission, as the rkyv derives are today. This ties ethos-zero to sema-engine's trait set, unless that set is named in one place the generator reads.
- Registry addressing: the root says the object is a Memory, so one name answers both what the object is and that its types are stored. This is the closest fit to one main object per file.
- A trait added later: one change to the rule or the generator, and every type in every Memory object gains it, with no file edited. The new trait is invisible in the files.
- "Every trait is written in ethos": the trait is implied by the root, so it is not written in the file; it is met only if the root's meaning is itself specified in ethos.
- Under all three the record key, the memory version and the table are still stated nowhere in Ethos.



  Four roots: Library, Signal, Operation, Memory. Signal declares what a Nexus says; Operation what it does, one operation type for every effect; Memory what it remembers; Library what they share. A memory trait carries a standard successful-or-unsuccessful change and, for each version, the upgrade from the previous format; that upgrade is the very edit the type needs.
+
+ The Memory root is a special object: every type defined in it bears the traits that let it be stored, implied by the root and never written in the file.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
