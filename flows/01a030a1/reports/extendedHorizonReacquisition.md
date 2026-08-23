# extended-horizon reacquisition

## Exact flow

The discussion was flow `01a02b4b`, session
`01a02b4b-ab46-7921-8e47-928b294470be`, on 2026-08-23.
Flow `01a02f74` subsequently remembered that flow and mapped the current
implementation against it.

The living used `extended-horizon`. No typed living-psyche occurrence of
`horizon-extended` was found.

## Living-psyche ground

At source event `2026-08-23T15:14:06.129Z`, transcript line 905:

> whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon (that could be a standalone repo for deriving some data in nix from the horizon data coming out of lojix)

This follows the earlier ruling in the same flow:

> there should be no difference between the embedded and independent home. the part which is shared ought to be directly from lojix-emitted horizon output, or from a shared nix machinery which uses the said horizon as input only. embedded home should be only the absolute minimum nix code necessary to embed a home logic which is otherwise completly identical. Do you understand what I mean?

At source event `2026-08-23T16:28:17.917Z`, transcript line 932, the living
quoted the agent's definite wording and challenged it:

> Yes. extended-horizon is not another authority; it is a deterministic derivation layer over Horizon.
>
> you mean that repo already existed?

The challenge matters: no existing repository or settled implementation was
being asserted by the living.

## Agent proposal from that flow — not approved psyche

The agent proposed this anatomy:

```text
Lojix-emitted Horizon
          │
          ▼
extended-horizon
(pure Nix derivation of data Horizon does not carry directly)
          │
          ▼
one complete extended Horizon
          │
     ┌────┴────┐
     ▼         ▼
shared Home  shared OS logic
logic
     │
 ┌───┴─────────────┐
 ▼                 ▼
independent Home   minimal NixOS embedding
          │         │
          └────┬────┘
               ▼
      identical activation
```

Its proposed invariant was:

> Home value
> ├── written directly in setup-independent Home logic
> ├── read directly from Horizon
> └── derived purely from Horizon by extended-horizon
>
> Never: discovered from ambient `nixosConfig/osConfig`

The proposed repository contract was:

- input: Lojix-emitted Horizon;
- static dependencies: pinned Nix code and schemas;
- output: raw Horizon facts plus deterministic derived locale, package,
  styling, and other Nix-resolved facts consumers actually need;
- no inspection of NixOS configuration, the running host, or setup-specific
  environment state;
- no policy invented when Horizon does not contain its source.

The proposed value shape was:

```nix
{
  raw = <original Horizon>;
  derived = {
    # deterministic Nix-derived facts
  };
}
```

The angle-bracket value and comment above are the earlier agent's schematic,
not executable Nix and not an approved interface.

The agent also proposed Intent wording which the living did not approve. Its
open anatomy question was whether every Nix consumer receives one complete
extended-Horizon value, or consumers combine raw Horizon with selected derived
outputs independently.

## Correction recorded inside the source flow

After the living asked whether the repository already existed, the agent said:

> No. I was describing the proposed role, not claiming such a repository already exists.
>
> You said it “could be a standalone repo”; I then wrote too definitively. I have not verified an existing `extended-horizon` repository, and none has been created or authorized here.

The grounded distinction at that handoff was:

```text
Horizon             existing concept/output
extended-horizon    proposed deterministic Nix layer over Horizon
repository          possible future home for that layer
```

## Insight for the current repair

This is the missing predecessor to the current common-ground statement. A
CriomOS-home-exported construction record is indirect because the OS obtains
shared facts through Home. The earlier `extended-horizon` proposal instead
places Horizon-derived common facts outside both consumers and makes both OS
and Home depend on that source directly.

The records determine provenance and direction, but not yet the complete
repository anatomy. Before realization, the living still needs to rule:

- whether `extended-horizon` is now the repository's actual name;
- whether its public output is one complete extended Horizon or separately
  selectable derived capabilities;
- which current OS/Home values are genuinely shared and therefore move;
- which derived facts are mechanics versus policy that must be stated in raw
  Horizon first.

## Sources

- Flow `01a02b4b`, transcript lines 880, 905, 925, 932, and 936.
- `flows/01a02b4b/vision/homeEquivalence.md`
- `flows/01a02b4b/log.md`
- `flows/01a02f74/log.md`
- `flows/01a02f74/reports/currentVsVisionMap.md`
