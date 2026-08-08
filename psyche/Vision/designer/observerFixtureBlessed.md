# The fixture is blessed

> "the fixture is blessed, and / for imports"

— psyche, 2026-08-07, captured 2026-08-07T22:10Z (Designer session d63804f2)

Context, kept apart from the quote: "the fixture" is the Designer's
observer-interface counter-proposal, presented 2026-08-07 evening:

    Interface.{1 0 0}
    [signal/domain.[ObserverFilter ObservationEvent]]
    {
      [Tap.ObserverFilter
       Untap.ObservationTapToken]
      [ObservationTapped.ObservationTapToken
       ObservationUntapped.ObservationTapToken]
      [UnknownObservationTap.ObservationTapToken]
      [Observation.ObservationEvent]
    }

with, in signal-domain:

    ObservationEvent.[OperationObserved.OperationKind
                      EffectObserved.EffectKind
                      ObservationLagged.DiscardedOperationCount
                      ObservationEnded.ObservationEndReason]

The blessing carries the fixture's internal choices as presented:
stream-section entries are element-type only (the filter rides the
Input initiation entry); the version stays the typed triple
`{Major Minor Patch}`; `Tap`/`Untap` naming; the typed
`ObservationTapToken.Integer` newtype; `EffectObserved` implies
effects become recorded; refusals sit in the Refusal section per the
universal-sections ruling.
