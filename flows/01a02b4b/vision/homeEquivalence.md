# Embedded and independent Home

## 2026-08-23T15:44:25+02:00 — there should be no difference between the embedded and independent home

> there should be no difference between the embedded and independent home. the part which is shared ought to be directly from lojix-emitted horizon output, or from a shared nix machinery which uses the said horizon as input only. embedded home should be only the absolute minimum nix code necessary to embed a home logic which is otherwise completly identical. Do you understand what I mean?

Context: The living answered the discovered divergence between Home evaluated
inside `nixosConfigurations.target` and the independent Home output. The ruling
places their shared logic behind Lojix-emitted Horizon output or shared Nix
machinery whose only setup input is that Horizon, while limiting the embedded
surface to the minimum wrapper necessary to embed the same Home logic.

## 2026-08-23T17:14:15+02:00 — whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon

> whatever in home is currently originating in the OS must originate from the horizon or the extended-horizon (that could be a standalone repo for deriving some data in nix from the horizon data coming out of lojix)

Context: The living located every Home value currently inherited from the OS
in either Lojix-emitted Horizon data or an `extended-horizon` derivation layer.
The possible standalone repository derives Nix data from the Horizon emitted by
Lojix; the surrounding OS evaluation is not the source of those Home values.
