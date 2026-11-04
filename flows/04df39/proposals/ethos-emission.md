Presentation.{ «Ethos for Emission» }

# Ethos for Emission

Created by Fable, from his comment on Version one. Brainstorm: how Ethos could carry what the Nexus modules now write and ethos-zero rejects, the Emission root and an import of a Signal's Input and Output. Each alternative is a short-term hack; the design of Ethos itself belongs to a focused flow.

### Proposal 1: Emission in today's Ethos · psyche-belief › vision/ethos.md

**Comment** Three ways, smallest first. He rules which, or none.

**Alternative 1** A sigil marks a root Ethos does not yet know: the file opens with the sigil and the root's name, and ethos-zero reads the sections as a Library's. The sigil is removed when the root is native.

```ethos
~Emission
[]
[ Command.{ Verb Vector<Argument> } ]
[ Outcome.[ Done Refused.Integer ] ]
[ Verb.[ List Show ]
  Argument.[ Name.String Quiet ] ]
```

**Alternative 2** Emission is a Signal whose inputs are the emissions and whose outputs the outcomes, the file named emission.ethos; the root's name says nothing, the file's name does. Nothing in ethos-zero changes.

```ethos
Signal
[]
[ Command.{ Verb Vector<Argument> } ]  ; emissions
[ Outcome.[ Done Refused.Integer ] ]   ; outcomes
[ Verb.[ List Show ]
  Argument.[ Name.String Quiet ] ]
```

**Alternative 3** Emission is added to ethos-zero as a fourth root beside Signal, Operation and Memory, with the implied trait Emittable; the Signal's Input and Output become importable names, `signal_herdr:[ Input Output ]`. The proper way, and the one that waits for the Ethos flow.

```ethos
Emission
[ signal_herdr:[ Input Output ] ]
[ Command.{ Verb Vector<Argument> } ]
[ Outcome.[ Done Refused.Integer ] ]
[ Verb.[ List Show ]
  Argument.[ Name.String Quiet ] ]
```
