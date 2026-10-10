# Minimal Lojix training

Approved and installed in the authored Lojix skill:

> The logical node selects what is built; the activation destination selects
> which machine is changed. Before a state-changing deployment, verify that
> they identify the same node. If they do not, stop.

This is the smallest rule that prevents deployment 49's Zeus-on-Ouranos
failure without constraining controllers, evaluators, builders, or build-only
work.

## Delivery

- Curriculum `8a773baa6915d37f8482b59a15c159ee28665dd8`
- Primary pin and regeneration `2813e0df150cd59e142fc918f20383f53905648b`
- Typed generation `Generated.{35 27}`
- Typed check `Checked.{35 27}`
- `nix flake check`: passed
- Static `Deployment*` definitions and authored references: zero

## Behavioral witness

An independent evaluator using pre-change Curriculum revision `83d46cb6`
called the request with logical node Zeus and activation destination Ouranos
structurally ready. An independent evaluator using the installed generated
skill stopped the same request, identified the nodes as distinct in the current
proposal, and required correction before submission.

## Source

- `flows/01a02fe5/reports/wrongHomeDeployment.md`
- Flow `01a02fe5`.
