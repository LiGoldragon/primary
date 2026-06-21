# Maintainer plan — Mentci/Criome/Spirit production audit

## Maintainer responsibility in this epic

The maintainer lane should continuously answer:

- What is actually deployed on `ouranos`?
- Which commits are on main vs only in worktrees/branches?
- Which daemon/store/socket is live?
- Which deploy path is safe to run now?
- Which prior claims were verified live rather than inferred from reports?

## Current known production facts to keep in view

- Spirit is running from `/nix/store/phm2l3c...-spirit` and the parser/OOM gate has been verified live.
- Active Spirit referents are now clean: active records have referents and active referents are kebab-case.
- The system’s current boot default is a bad OsOnly generation that dropped broad firmware. Bluetooth was runtime-repaired by pointing the kernel firmware path to the booted generation; a normal reboot still needs a corrected system generation or boot default handling.
- The `mentci-egui` / `mentci-lib` repos already have current INTENT/ARCHITECTURE aligned with thin-client discipline.
- `introspect` is not just a draft, but it is not yet the full Mentci observation backend.

## Audit checklist before any Mentci/Criome deploy

1. Version control
   - `jj status` in each target repo.
   - Confirm branch/main location and whether designer work is in `~/wt` or `/git` main.
   - Confirm pushed remote refs before Nix/lojix deploy.
2. Build gates
   - `cargo test` for changed Rust crates.
   - `nix build` for binaries/packages used by deployment.
   - No local path flake refs in deploy commands.
3. Runtime gates
   - `systemctl --user status` for user daemons: Spirit, Mentci, Introspect where relevant.
   - `systemctl status` for system daemons: Criome/lojix/system generation as relevant.
   - Verify socket paths and modes.
4. Production safety
   - Do not reboot `ouranos` until firmware-containing generation is restored/defaulted.
   - Memory-cap bulk jobs with detached `systemd-run` units.
   - Treat failed async/subagent runs as untrusted unless outputs are independently present.
5. Spirit/Criome path
   - First contract should be localhost one-of-one / auto-approve for Spirit requests, mirroring current authorized-key behavior.
   - Log approvals and compare expected vs actual approvals before adding nodes.

## Report template

For each maintainer audit pass, record:

- Scope and repos inspected.
- Live daemon paths and versions.
- Main/branch/working-copy status.
- Build/test commands and results.
- Runtime/socket observations.
- Production risks and recommended stop/go.
- Claims verified, claims contradicted, claims still unverified.

## Compact maintainer prompt

Audit the Mentci/Criome/Spirit production arc. Verify main branches, live daemon store paths, socket health, boot generation safety, Spirit database state, and whether Mentci/introspect/Criome claims are actually deployed. Write a concise maintainer report with stop/go risks and exact evidence.
