# Independent first-wave counter-audit

Cohort: CriomOS-home fe0492 + CriomOS consumer 628cf7.
Independent review completed before reading the Opus audit.
Read-only inspection delegated to nix_counter_audit; findings below are that subflow's witnessed source and receipt observations, synthesized by Mind nexus Secondary a6689e. No candidate changes or deployment performed.

## Disposition

PASS: bounded first-wave source review, private-cohort evaluation, real consumer package-context qualification, projections, and remote check build receipts. HOLD: publication/deployment acceptance. No scoped code failure found. Receipt inspection is not an independently rerun remote build.

## Findings

- PASS — fe0492 versus 6e9e89 differs only in flake.nix whitespace. Producer packet hashes and consumer post-check-hashes.json identify evaluated producer fe0492 and consumer 628cf7 bytes.
- PASS — consumer flake.nix:196-198 invokes inputs.criomos-home.lib.mkBirdCodexSelectionCheck with its pkgs. Producer flake.nix:696-700 exposes the factory; gates/bird-codex-selection/default.nix:29-33 uses that instance directly, without nixpkgs reimport or stub.
- PASS — consumer modules/nixos/userHomes.nix:97-105 supplies production pkgs to Home, with useGlobalPkgs=true. package-context-receipt.json exits 0. package-context-qualification.json compares source, system, five overlays, allowUnfree and representative derivations; this qualifies injection/context, not structural equality of every function.
- PASS — producer modules/home/profiles/min/default.nix:296-325 no longer installs duplicate codex-remote-tools. modules/home/profiles/min/codex-remote-control.nix:18-23,111-128 supplies the selected provider. Gate :62-65 imports Min; :94-101 filters and merges actual packages with ignoreCollisions=false; :118-119 asserts one provider; :171-175 executes codex-remote.
- PASS — consumer-check-receipt.json evaluates the check with exit 0; consumer-check-build-receipt.json exits 0 and stderr records remote Prometheus builds. Earlier consumer-c206/collision-negative-receipt.json exits 1 with builder exit 25 and conflicting bin/codex-remote paths; that negative evidence is from c206, not a fresh fe0492 mutation build.
- PASS — producer modules/home/codex-endpoints.nix:13-55 declares package and policy options and derived tools; codex-next and codex-remote-control share the selected package/home/socket. Consumer modules/nixos/userHomes.nix:15-25,56-58 selects Li true/true/true and Bird true/false/true for default-next/bootstrap/artifact-disabled. projection-receipt.json exits 0 and records matching real codex-0.163.0 derivations, exact homes/sockets, assertions true, keep-old. unlisted-projection-receipt.json exits 0 with false/false/false and keep-old defaults.
- PASS within lexical scope — check build runs source guard; source-guard-result.json records 21 classified retained entries and zero new violations. Guard consumes allowed digests per occurrence, so duplicated grandfathered lines are violations. Synthetic negative controls cover direct literal, data, concat, interpolation and storePath. No fresh real-source reintroduction mutation build was witnessed for this pair.
- HOLD — evaluation explicitly overrides criomos-home to a private source path; final repository lock pin remains pending. Exact private bytes were qualified; published dependency connection was not.
- HOLD — whole-Home activation evaluation fails while fetching field-clj from med/cli-tools.nix because of SSH host-key failure. This does not demonstrate an endpoint fault, but full Home activation acceptance is unestablished.
- HOLD — keep-old intentionally leaves occupied cutover for Field; it does not hold failure restart/reboot or prove compatibility. Native occupied-client/backups and cutover acceptance remain unwitnessed.

## Stated limits, not failures of this wave

21 retained store-literal occurrences remain: checks/bird-home-isolation/default.nix (2), checks/herdr-toast-delivery/default.nix (2), lib/primary-committer-hook-trust.nix (1), modules/home/profiles/min/herdr.nix (2), packages/harness-profile/default.nix (2), packages/harness-profile/owned-rust-exports.json (12). Lexical guard boundaries include non-.nix/.json files, multiline construction, and movement of an allowed identical line within its file. Name-based Li/Bird selection, broader eradication and history waves remain outside this bounded acceptance.

## Evidence locations

- /home/li/private-repos/flow-evidence/0c85a3/nix-store-reference-design-20261018/consumer-package-gate-formatted/packet.json
- /home/li/private-repos/flow-evidence/42265e/nix-store-literals-20261019/consumer-package-context/

Field acceptance.json was treated as an attributed synthesis and checked against receipt argv, exits, stderr and projection outputs. Findings above report inspected evidence, not direct observation of the running deployment.
