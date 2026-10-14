<!-- to-the-living:start -->
Presentation.{ «Nuts and bolts, not welding» }

# Nuts and bolts, not welding

```
      bolted                   welded

  +----------+             +----------+
  |  theirs  |             |  theirs  |
  |          |             |          |
  |  o    o  |  bolt holes |~~~~~~~~~~| seam
  +--|----|--+             |  ours    |
     |    |   <- bolts     |  fused   |
  +--|----|--+             |  inside  |
  |  o    o  |             +----------+
  |  ours    |
  +----------+

  undo: unscrew            undo: cut
  replace: either side     replace: both
  crack: stops at joint    crack: runs through
  inspect: a wrench        inspect: x-ray
  made: apart, tested      made: as one, in
        alone                    one shop
```

## The figure, read

A bolt joins two parts at an interface both were made to: a hole, a thread, a torque. Each part comes from its own maker, is tested alone, and either can be replaced, upgraded or serviced without touching the other. A crack in one part stops at the joint. The joint is checked with a wrench. A weld fuses the parts: they must be one material, the heat changes the metal around the seam, a crack runs through both, replacing one means cutting, and the only inspection is an x-ray. A car body is welded where one maker builds one part for one purpose; everything from other makers is bolted to it.

A component's published interface is its bolt holes. Our part joins theirs there, and theirs can be replaced or upgraded, ours tested alone, a fault stays on one side, and the joint is one readable file of ours. Modifying the component is welding: it fuses the two, alters their code around the seam, carries every crack across, and is inspected only by reading their internals. Welding is right inside what we build as one piece for one purpose; between parts, nuts and bolts.

## How the step was taken

Astra found that a service unit cannot parent a Herdr pane. This flow's blocker note said the first thing to check was whether Herdr itself could restart the pane. The Secondary's order to Field widened that into: if it cannot, name the smallest supported way to make it do so, a Herdr feature or a declared change to Herdr, and build it. Field returned the smallest Herdr-only change. This flow, asked to settle the seam, endorsed it as the smallest shape, on the reasoning that Herdr already owned the pane and a second owner for the process should be avoided. The Secondary ordered it built and Astra began it.

Every seat measured smallest the same way, by lines changed and processes involved; the design skill says "Propose the smallest working shape first" and no loaded sentence says what smallest measures. Every seat sent the fix to where the state lives, the pane host, and no seat asked whose concept a seat's lifecycle is. No loaded skill names the boundary between composing a component through its interface and modifying it. No seat knew whose software Herdr is, and none listed that as an unknown. And the hub relayed a proposal as an order without judging its design, which multiplied the error instead of catching it.

Ownership is not the root. Had Herdr been ours, a seat-lifecycle policy inside a pane host would still have been a weld: a component carries its own concept, and another concept enters it only through its published interface. Ownership decides who may edit the file; the boundary decides what belongs in it.

## What the weld would have cost

Herdr's source is not this system's to change, so the committer's liveness would wait on Herdr's owner. Every later Herdr version could drop the patch. The committer's lifecycle, identity, session resume, lock and message route would be bound to Herdr's internals, and a terminal host would hold this system's authority over its own seat. A seat policy would live in a pane host, to be cut out again when Flow launches seats. A policy flagged "only for the committer" would be one user's special case inside a general tool. A bug would reach every pane; a deploy would restart the service under every seat; a test would mean building Herdr. The patch, once begun, reached Herdr's API, schema, terminal state, readiness, CLI and target resolution, nine partial files before a working handler, and the route first demanded qualifying source hashes and declared objects: a small-looking insertion was not a small system. A twenty-line weld touches two owners, one foreign contract and one general tool; a forty-line bolted part touches one owner and uses one contract as given. Counted in owners, concepts, authorities and contracts, the bolted part is the smaller shape; counted in lines it is not.

## Distillation

### Proposal 1: spirit-core, new line

Target: psyche-skills, spirit-core, after "Start with the smallest shape that works."

Added: Nuts and bolts, not welding: a component carries its own concept. Our part joins another's at the interface it publishes; when the interface lacks what we need, we build our part on the interface, choose another component, or change our design. We never modify a component to carry a concept that is not its own; one that is not ours we never modify at all.

### Proposal 2: compensation-design, the measure of smallest

Target: field-skills, compensation-design, the line "Propose the smallest working shape first."

Removed: Propose the smallest working shape first.

Added: Propose the smallest working shape first. Smallest is measured in owners, concepts, authorities and contracts touched, never in lines of change; a shape that modifies another's component is welding, not the smallest.

### Proposal 3: compensation-design, ownership before change

Target: field-skills, compensation-design, after the line of Proposal 2.

Added: Before changing a component, establish whose it is and what concept it carries.

## Question 1

Proposal 1 puts the rule in spirit, since every flow loads spirit by default and the rule is to hold every machine. Is spirit the right level, or does it go to vision-design, which only a designing flow loads?

## Question 2

A component that offers an extension point meant for others, a hook, a plugin interface, a policy field it already exposes: is using that point a bolt hole, as the proposals assume, or a weld?

## Question 3

Between this system's own components, the messenger, the orchestrator, Flow, is modifying one to carry another's concept also welding, as Proposal 1 says, or is welding allowed inside what we own?
<!-- to-the-living:end -->
