# CriomOS Ouranos closure validation

## Result

**PASS.** The immutable CriomOS commit
`475bf5c27efa843f97ad58cc99e611d519d0f40f` was evaluated and built
offline as the Ouranos `nixosConfigurations.target` toplevel, using the
already-materialized `system`, `horizon`, `deployment`, and `secrets` inputs.
No source checkout, pin, materialized input, Lojix store, service, generation,
or deployment was changed.

The requested shorthand `475bf5c27efa` is complete only as a local Jujutsu
prefix; the full immutable Git revision above resolves it. Jujutsu shows that
commit is `main` and names it `CriomOS: migrate Lojix store before startup`.
No newer revision was required.

The closure output itself is intentionally not recorded: it is a transient
store path. Its safe identity is NAR hash
`sha256-Fh3rmifkkD6u3waSdiaztifaIHXhm+YKZlbXtSAvG7Q=`.

## Coordination and boundaries

- `bd show primary-akw --json` confirms the recovery bead remains open.
- `orchestrate '(Observe Lanes)'` showed the active
  `LojixOuranosActivation` lane; `orchestrate '(Observe Worktrees)'` showed
  active CriomOS worktrees. This validation used neither as a write surface.
- The report path was claimed under the temporary
  `LojixClosureValidation20260728` lane before this report was created.
- All four expected materialized input directories existed. Their contents,
  including any secret values, were not printed, copied, or modified.
- The commands used `--offline`; no repository was fetched, updated, or
  altered. The only mutation was normal Nix build output in the store.

## Exact command shapes and results

The local materialized-input root is deliberately represented below as
`$input_base` rather than its live filesystem location. It contained the
`system`, `horizon`, `deployment`, and `secrets` subdirectories. This is the
exact supported invocation shape, with the full immutable source revision.

```sh
revision=475bf5c27efa843f97ad58cc99e611d519d0f40f
flake_ref="github:LiGoldragon/CriomOS?rev=$revision"

nix eval --offline --raw \
  --override-input system "$input_base/system" \
  --override-input horizon "$input_base/horizon" \
  --override-input deployment "$input_base/deployment" \
  --override-input secrets "$input_base/secrets" \
  "$flake_ref#nixosConfigurations.target.config.system.build.toplevel.drvPath"
```

Result: passed; Nix returned a toplevel derivation path (scrubbed).

```sh
closure=$(nix build --offline --no-link --print-out-paths \
  --override-input system "$input_base/system" \
  --override-input horizon "$input_base/horizon" \
  --override-input deployment "$input_base/deployment" \
  --override-input secrets "$input_base/secrets" \
  "$flake_ref#nixosConfigurations.target.config.system.build.toplevel")
```

Result: passed. `--no-link` avoided creating a result link or changing any
profile/generation.

The closure was queried through Nix and each requisite was tested for the two
executables without emitting store paths:

```sh
nix-store --query --requisites "$closure"
```

Result: passed. At least one closure requisite exposes each executable:

- `bin/lojix-migrate-store`
- `bin/lojix-daemon`

The generated `lojix-daemon.service` in the built toplevel was inspected only
for command positions. It has this verified order:

1. `ExecStartPre`: `lojix-migrate-store`
2. `ExecStartPre`: `lojix-write-configuration`
3. `ExecStart`: `lojix-daemon`

This is also consistent with the exact source at the immutable revision,
where the declaration lists those two `ExecStartPre` values in that order.

## Remaining gates

Yes: only live gates remain. Before activation, an authorized read-only
live-store witness must establish the schema/canonical-store precondition
without printing payloads. Then declaratively activate this validated
generation; the unit pre-start result, daemon sockets, ordinary query, and
readable deployment history must be witnessed. No Lojix deployment or Bird
work should proceed until those live gates pass.

## Non-results

This build proves evaluation and closure composition, not runtime behavior.
It did not inspect the live Lojix store, invoke a migrator, start/restart a unit,
activate a generation, query a daemon, or expose generated secret material.
