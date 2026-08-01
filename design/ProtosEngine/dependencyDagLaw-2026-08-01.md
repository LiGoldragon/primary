# Dependency DAG Law — 2026-08-01

Agent text answered: the manager's full explanation of the dependency
question — topological walk vs lazy-fixpoint machinery, with the Nix-style
mutual-reference contrast — ending: may an operation refuse whenever the
dependency graph contains a cycle, or is mutual derivation ever wanted?

Psyche ruling [psyche-verbatim]: "dag"

Seated: **transformation and derivation dependencies form a DAG; cycles
refuse with a typed error naming the loop, and the refusing operation
changes nothing** (atomicity law). Inside an atomic operation, cascaded
regeneration is ordered by a topological walk of the affected subgraph;
every affected declaration runs exactly once, after everything it needs.
Consequences: no lazy evaluation for dependency reasons, no fixpoint
evaluator, no constraint-region machinery — permanently out of the design.
This also closes the macro-time research's pivotal question
(`reports/MacroTimeEvaluationPriorArt-2026-08-01.md` correction appended
2026-07-31: acyclic flow suffices; Candidate A strict topological
evaluation is the ruled shape for derived configuration as well).
