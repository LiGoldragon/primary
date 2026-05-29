# 0 · Frame and method

## Directive (psyche, 2026-05-28)

Reload secret-handling skills + intent. Document the never-show
discipline — gopass env-var wrapping and sops-nix cluster secrets —
so the skills state how to handle secrets without ever seeing them.
Run the mint script to create the gopass token. Research the clean
sops-nix path, then deploy the token to the prometheus llama-server
and deploy the new AI node with Gemma 4. Build on prometheus; never
pull the AI models into the local store.

## Intent captured

Spirit records 1011–1017:

- 1011 (Constraint, Maximum) — an agent never sees a secret value.
- 1012 (Principle, Maximum) — secrets written only to encrypted stores.
- 1013 (Decision) — gopass for the session, sops-nix for the cluster.
- 1014 (Decision) — document the secret discipline in the skills.
- 1015 (Decision) — deploy the token + Gemma 4 to prometheus.
- 1016 (Constraint, Maximum) — build on prometheus, not locally; do
  not pull the model derivations into the local store.
- 1017 (Clarification) — psyche authorized cloud-designer to carry
  this end to end, including operator-lane steps.

(Records 1011/1012 carried noisy word-topics from a topic-vector
mistake; their descriptions are correct. The secret area is indexed
cleanly via 1013/1014.)

## Method

Three background research scouts mapped the terrain read-only: sops
infrastructure, the llama-server module + model inventory, and the
deploy mechanism. Their syntheses are files 1–3. Then the safe,
in-lane, reversible work ran directly — mint, encrypt, skill (file 4
records what's done and verified). The production-deploy decisions
are surfaced to the psyche in file 4 before any deploy-tooling change,
because the research revealed the clean path is gated by a deploy-tool
limitation and an in-flight system-operator reconcile of the exact
module surface.

## Files

- `1-sops-infra.md` — how sops-nix works in this cluster.
- `2-llama-and-models.md` — the llama-server module, api-key, inventory.
- `3-deploy-mechanism.md` — lojix-cli and the build-on-prometheus path.
- `4-overview.md` — synthesis, what's done, the deploy decision.
