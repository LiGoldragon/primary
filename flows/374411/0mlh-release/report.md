# 0mlh naming release: Field completion

## Published inputs

- Final CriomOS-home revision: `08361fef939664f26b06b86b8cdf28512adc10f4`.
- Final persona revision: `cd9222c1aae69b62db6d5de6304801578fc44aa6`.
- Immutable CriomOS consumer and published main: `b376324de50e18ef2e7c2e1996e79476f62b2b5e`.
- The superseded Home `1460ce…` was not published, materialized, or activated by this lane.

## Lojix and live generation

- Watched Realize deployment 547 completed `Some.Succeeded`.
- Watched ActivateNow deployment 548 completed `Some.Succeeded` at database marker 13145.
- Lojix records Current generation `/nix/store/j2zdzk9dyv0myxqj1znp97gn5jfj6z65-home-manager-generation`, exactly the generation in the authoritative handoff.
- Terminal evidence: `step5-live/realize-terminal.txt` and `step5-live/activate-terminal.txt`.

## Stopped backup and runtime replacement

- Flow and Curriculum were inactive before their whole stores were copied.
- The stopped backup is `rollback/stopped-runtime-current-j8/` (235 MiB); its manifest is `step5-live/stopped-backup-manifest.sha256`.
- Fresh pre-release Configuration and the exact 38-entry rollback Metaflows payload are in `step5-live/configuration-before.datom` and `step5-live/metaflows-rollback-payload.datom`.
- Curriculum is running as PID 2790283 from `/nix/store/79zjg9f0iz9ljndlqnw6csv7bvyc7psc-rust_curriculum-0.1.0/bin/curriculum-nexus`.
- Flow was explicitly restarted and is running as PID 2790869 from `/nix/store/f9g55ar1qplr8lyjpnzymmg56da7xx0x-flow-configured-0.54.7/bin/flow-nexus-daemon`; its ordinary and owner sockets and the Curriculum socket are listening. Evidence: `step5-live/runtime-after-start.txt` and `step5-live/flow-restart-pids.txt`.

## Naming replay

- The final 38-declaration payload SHA-256 is `d84f0486bcb097e2caf4a61da4d291b3f6c2605b562fd67c0dcdd4e4d13e6b14`.
- Its single owner replay answered `Configured.Unchanged`: Home activation had already installed the same family.
- The readback Metaflows family equals the payload. Before and after the replay, all 19 Configuration fields are identical. Against the old release, only field 9 (Metaflows) and field 15 (its counter) changed; SendServers stayed equal.
- Evidence: `step5-live/replay-reply.datom`, `step5-live/configuration-new-after-replay.datom`, and `step5-live/replay-structural-diff.json`. The bounded runtime warning journal is empty.

## Fresh harness witnesses

- The module-name oracle is three colon-delimited fields: `kind:topic:integer`. It does not use the Flow address or the model's address answer.
- Codex Sol Flow `fc7e01` has retained actual-system and actual-first-prompt module lists. Every identity in both lists matches the oracle and none uses dash-version (`-vN`) naming.
- Claude Haiku Flow `acfae8` has a retained actual-first-prompt module list, and every identity matches the oracle without dash-version naming. Its configured system-module list also matches, but the native transcript did not retain the actual `--system-prompt-file` bytes after Flow released the held `/proc` file at binding. Claude actual-system verification therefore remains an evidence gap.
- Evidence and hashes: `step6-witnesses/module-name-oracle.json`, the two `*-modules.txt` excerpts, and `step6-witnesses/SHA256SUMS`.

No naming release was applied to another host.
