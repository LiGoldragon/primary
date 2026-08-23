# Common-ground repository precedent

## Outcome

Two recent threads meet the living's current ruling from different angles.

Flow `68512643` is the deeper architectural precedent. It recently reacquired
and assembled the Datom/Ethos/Protos records: two consumers remain distinct,
their shared mechanism belongs to a third conceptual substrate, and both
depend directly on it. Its distillation remained a proposal awaiting review,
so authority lies in the original verbatim records it gathered.

Flow `01a02f23` is the immediate repository-ownership analogue: Orca packaging
was placed in its own repository instead of being reached through or crammed
into Home.

## Current Vision

Current flow `01a030a1`, transcript line 605, source event
`2026-08-23T22:53:43.989Z`:

> to me, this looks like a need to abstract the common ground between OS and home to a separate repo, and using that repo as the source for anything that is shared between them. indirection is bad design

## Earlier Vision: shared substrate rather than consumer indirection

Flow `012fbf07`:

> no, I dont think so. they share an approach, but are different
> languages. they could have a shared substrate (traits with a shared
> implementation and types)

The living rejected the inference that Ethos should consume Datom's parser.
Datom and Ethos remain distinct; common machinery has its own substrate.

Flow `a5587095`:

> remember; once we open the Meaning delimiter (that what were
> calling it), all the delimiters and structured parsing spectrum is
> available, until that closing delimiter comes in and changes the
> parser's context; that is how all our languages parse and why we
> can design so freely. This is important and is the part of the
> code which can be shared between all parsers (should be in protos;
> protos is the name we give to the style which all our dialects
> share; hence why the final fully-decomposed engine with 3 daemons
> is the protos engine, with datom sort of sitting besides it, as it
> is only for pure, typed data)

This locates the shared code in the repository named for the shared concept,
not in either consuming language.

Flow `012fbf07` gives the same topology for signals:

> the signal ID must be how agents interpreted my vision for an
> ability for the router to differentiate between signal types for
> sorting them out. router is for signals to go across the network.
> it should be an enum in a universal signal repo that all components
> depend on, which wrap the objects. that universal-signal repo could
> also serve other functions that all signals need to deal with
> (handshake payload basically)

The dependency direction is explicit: every consumer depends on the universal
source; no component is used as an indirect carrier for the others.

The broader commonality test is recorded in
`psyche-raw/Vision/traitsAsCapabilities.md`:

> So, if we take all the common behavior, we want to have as many
> common traits as possible, because then we're creating the right
> abstraction. So, all protos dialects, whether it's datum [Datom],
> ethos, nomos, or logos, are transcodable.

## Earlier Vision: repository ownership rather than cramming Home

Flow `01a02f23`:

> I think an orca repo is smarter than cramming more stuff in the home repo

The standing report then proposed CriomOS-home consume only the pinned package
output. That consumption detail was agent inference, but the separate Orca
repository boundary is the living's ruling.

## Connection to OS and Home

The repeated architecture is:

```text
consumer A ─┐
            ├──> repository owning the common concept
consumer B ─┘
```

not:

```text
consumer A ──> consumer B ──> shared value
```

Applied to the current subject, neither CriomOS nor CriomOS-home owns their
common ground. A separate Horizon-derived repository owns the shared values and
machinery; OS and Home depend on it directly. OS-specific composition remains
in CriomOS, Home-specific composition remains in CriomOS-home, and only the
actual intersection moves.

This corrects the preceding proposal in this flow: a
`CriomOS-home.lib.homeConstruction` export still makes OS reach common ground
through Home. It removes duplicated code but preserves the wrong ownership and
dependency direction.

## Authority boundary

The current statement identifies a separate repository and direct consumption
of shared ground. It does not yet name the repository, enumerate its values,
or rule whether `extended-horizon` is the final name. The earlier wording that an
extended-Horizon repository “could be” used was permissive, not a mandate.

No distilled Intent currently states the broad phrase “indirection is bad
design.” Its scope must be clarified before treating it as a universal rule.

## Sources

- Flow `01a030a1`, transcript lines 605 and 615.
- `flows/01a030a1/vision/commonGround.md`
- `flows/68512643/log.md`
- `flows/68512643/reports/datomEthosMonolithDistillation.md`
- `flows/012fbf07/vision/threeStacks.md`
- `flows/a5587095/vision/protosIsTheSharedStyle.md`
- `psyche-raw/Vision/traitsAsCapabilities.md`
- `flows/01a02f23/log.md`
- `flows/01a02f23/vision/orca.md`
- `flows/01a02f23/reports/agentHarnessPackaging.md`
- `flows/01a02b4b/vision/homeEquivalence.md`
