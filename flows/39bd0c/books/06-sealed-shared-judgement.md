Judgement on «Sealed and shared types in Ethos», every example and trait.

Proposal 1: the example is right and whole; Titled, Requested, Composed and Verifying are qualifier-named, every type associated, and verified: takes two traits as inputs and yields Result<Self Refusal>, which is the sealing itself. One amendment of form: the associations comment stands on a line of its own while every other section's comment trails its first line; put it trailing, it fits.

Proposal 2: the example is right; Paned and Waiting are qualifier-named, both types associated, wait! takes a trait. Two amendments of text, below. The first is needed: "A shared type never travels: it bears no datom traits" contradicts the standing line that every declared type bears both datom traits, so that line is amended in the same proposal or the module contradicts itself. The second answers the implementer's second question in the direction the sealed type already takes: state must start somewhere, so a shared type too is built only by a capability with no self; the example already has it.

The implementer's first question, the Rust receiver of a ! capability on a shared type, and the third, a poisoned lock, are the hand-written body's and the generator's; neither needs his ruling, and I add no proposal for them.

### Proposal 1, amended associations lines · psyche-context › vision/ethos.md

```ethos
[ Address.[ Titled ]              ; associations
  Refusal.[ Titled ]
  VerifiedContext.[ Verifying ] ] }
```

### Proposal 2, amended text · psyche-context › vision/ethos.md

- Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates, so every ethos-declared type always bears both traits and no declared type can exist without them.
+ Ethos Zero emits `Datomizable` and `Compositional` on every struct and enum it generates but a shared one, so every ethos-declared type that travels bears both traits and no such type can exist without them.
+ A shared type, like a sealed one, is built only by a capability with no self, borne by a trait it is associated with in the same file.

```ethos
[ PaneId.[ Paned ]                ; associations
  WakeWaits.[ Waiting ] ] }
```

No further proposal added. Parse the amended lines on the branch before publishing; if a block is rejected, keep the original and send me the line.
