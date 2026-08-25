# Minimal Lojix training proposal

Add this to the authored Lojix skill:

> The logical node selects what is built; the activation destination selects
> which machine is changed. Before a state-changing deployment, verify that
> they identify the same node. If they do not, stop.

This is the smallest rule that prevents deployment 49's Zeus-on-Ouranos
failure without constraining controllers, evaluators, builders, or build-only
work.

## Source

- `flows/01a02fe5/reports/wrongHomeDeployment.md`
- Flow `01a02fe5`.
