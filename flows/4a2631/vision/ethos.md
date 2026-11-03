# Ethos

## On "The new direction", Proposals 4 and 5, 2026-11-03
Book "The new direction" (https://claude.ai/artifact/JSLBE5RhGUp1zUBvdKdc88), second version; these proposals did not land.
P4, Each root has an implied namespace (vision:ethos, Imports), on `signal` in `Library [ signal_flow:signal:[ Input Output ] ; … signal_flow:[ Call Caller ] ]`:
"Some interesting ideas here but that's not going to work. We'd have to look at or design, in more depth, the whole registry concept or at least in the short term see how Ethos names namespaces. I'm afraid we might have to go deeper to really do this properly.
We have to be careful what we put in the vision that would be used to audit the current Ethos so that we don't put a half-designed thing that would end up with a broken system. You can see the problem: you say "signal flow" and then "signal" so there's a missing abstraction here. An abstraction is being ignored, right? There's the "signal" in the first name that's obviously being ignored. It seems to not count because you have to say "signal" again.
Maybe let's just put that on the back burner for now. I don't even know what that means but that's what I'm saying."
P5, The registry (vision:long:ethos), on `Development` in `Registry.[ Declarative.Vector<Binding> … Development.{ Declarative.Vector<Binding> Overrides.Vector<Binding> } ]`:
"I don't think that's it. The registry: there isn't just one. There's one registry but it has multiple entries. Some are declarative and some are of the development kind. We don't redeclare the declarative kind and the development kind. We just have a way to name it. We have a way to name which declarative registry we're overwriting and the overrides are only going to apply to the names that they override."
