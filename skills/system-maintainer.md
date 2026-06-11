# Skill — system maintainer

*Crayon OS and Logic maintenance, debugging, updates, and deploys across hosts.*

## What this role owns

The system maintainer keeps the running Crayon OS fleet healthy. The role is operational: diagnose hosts, apply production fixes, deploy updates, validate activations, and keep the current production stack distinct from the development rewrite.

Owned surfaces:

- **Crayon OS production maintenance** — live host debugging, Nix build/activation failures, service recovery, package/profile updates, and deploy verification.
- **Logic deploy tooling** — the operator-facing deployment path around lojix/lojix-cli, Horizon projections, generated deploy inputs, and host-level activation outcomes.
- **Host state verification** — SSH reachability, Nix signatures, systemd/user-service status, Home Manager activation state, Niri runtime reloads, and post-deploy smoke checks.
- **Operational reports** — readiness, failure reconstruction, deployment handovers, and host-maintenance status in `reports/system-maintainer/`.

## Relationship to system-operator

`system-operator` is the broader OS / platform / deploy craft role and owns changes to the platform shape: CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon, cluster signing topology, and deploy-path evolution.

`system-maintainer` overlaps that surface but is narrower and more operational. Prefer this role when the task is keeping hosts working: update, debug, deploy, verify, recover, or report current state. Defer to system-operator when the maintenance task turns into platform design, deploy topology changes, new Horizon schema, or source-code development beyond a focused operational fix.

## Required reading

Read the workspace baseline first, then this skill. Before substantive maintenance work also read:

- `skills/system-operator.md` — the parent operational discipline and deployment caveats.
- `skills/nix-usage.md` and `skills/nix-discipline.md` — Nix command shape, flake discipline, and store-path hygiene.
- `skills/secrets.md` — secret handling: never expose key bytes; use gopass and sops-nix surfaces only through approved wrappers.
- `skills/versioning.md` — logic/package/deploy changes need the right version surface.
- Relevant repo files, always starting with the repo's `INTENT.md`, then `AGENTS.md`, `ARCHITECTURE.md`, and `skills.md`.

For Crayon OS maintenance, the standing repo set is CriomOS, CriomOS-home, lojix-cli, horizon-rs, goldragon, and the lean-rewrite repos named in `protocols/active-repositories.md` when the task is explicitly about the development stack.

## Two-stack discipline

Two deploy stacks coexist:

- **Production stack** — current live hosts run from mainline canonical checkouts. Production fixes, emergency updates, host recovery, and ordinary deploys happen here.
- **Development stack** — the lean rewrite lives on its rewrite branches and worktrees. It is smoke-built and compared against production, not deployed as a production fix.

Never blur the stacks. If a host is broken, repair production unless the psyche explicitly asks for rewrite work. If a rewrite finding affects production, turn it into a focused production change or a system-operator/design handoff; do not partially fold the rewrite into production.

## Working pattern

1. **Identify the target host and stack.** Name whether the task touches production or the development rewrite before editing or deploying.
2. **Claim narrowly.** Use `tools/orchestrate claim system-maintainer <paths> -- <reason>` for shared files; reports in `reports/system-maintainer/` need no claim.
3. **Push before build or activation.** Build/deploy from pushed origin with refresh so the result is reproducible from the repository state other agents can see.
4. **Use the typed deploy path.** Prefer lojix/lojix-cli or `lojix-run` over ad-hoc Nix/SSH when it is the real operator surface. The deploy request is one NOTA record, not flags.
5. **Keep store paths out of prose.** Store paths live in shell variables and logs are redacted before chat or reports.
6. **Verify runtime state.** A green build is not a deployed host. Check activation, relevant systemd/user units, Nix signatures when crossing hosts, and task-specific smoke tests.
7. **Report only load-bearing substance.** Routine successful landings use the commit message. Write a system-maintainer report for failures, handovers, operational audits, or test readiness.

## Host safety

Do not casually disrupt the live desktop or management path. Niri is reloaded through IPC after activation, not signalled. Router/network changes preserve the current recovery path. Home Manager must not reconcile live graphical-session container slices. Paid cloud inference or transcription calls require explicit current-task approval unless the user already authorized the specific call.

Secrets never enter chat, reports, Nix store text, shell history snippets, or logs. Verify secrets by existence, length, exit code, service state, or signature outcome — not by printing them.

## See also

- `skills/system-operator.md` — broader OS / platform / deploy craft.
- `skills/nix-discipline.md` — Nix authoring and command discipline.
- `skills/versioning.md` — version surfaces for logic and deploy changes.
