# 5 — Overview

## Result

This meta-report starts the downstream NOTA bracket-string migration
after the core `nota-codec` and `nota` branches landed on `main`.

The migration is partially landed and well tested where landed. Every
pushed implementation slice listed below has Nix evidence. The remaining
open pieces are not bracket-string grammar problems; they are blocked by
larger signal-stack migrations or an active Persona/signal rename lock.

## Subreports

- `0-frame-and-dispatch.md` — refreshed intent, recent report context,
  active locks, test naming preference, and dispatched subagent slices.
- `1-nota-config-and-spirit-surface.md` — `nota-config`
  implementation result.
- `2-deploy-stack-consumers.md` — deploy-stack migration result plus
  coordinator follow-up.
- `3-adjacent-nota-consumers.md` — adjacent-consumer migration result
  plus coordinator follow-up.
- `4-locked-persona-signal-audit.md` — read-only locked-surface audit.

## Landed With Nix Evidence

- `nota-config` `b38f4719`
  (`Strengthen nota-config bracket string witness`);
  `nix flake check` passed.
- `horizon-rs` `ae8754d3` on `main`
  (`horizon-rs: refresh main NOTA codec consumers`);
  `nix build .#checks.x86_64-linux.default` passed.
- `horizon-rs` `7a3072c7` on `horizon-leaner-shape`
  (`horizon-rs: migrate NOTA fixtures to bracket strings`);
  `nix build .#checks.x86_64-linux.default` passed.
- `chronos` `3ad63337`
  (`chronos: migrate NOTA examples to bracket strings`);
  `nix flake check --print-build-logs` passed.
- `chroma` `04c55e5f`
  (`chroma: migrate NOTA examples to bracket strings`);
  `nix flake check --print-build-logs` passed.
- `clavifaber` `eec30b0b`
  (`clavifaber: migrate NOTA request surface to bracket strings`);
  `nix flake check --print-build-logs` passed.
- `signal-lojix` `a007e8b6` on `horizon-leaner-shape`
  (`signal-lojix: migrate NOTA sum records to bracket strings`);
  `cargo test` and `nix flake check --print-build-logs` passed.
- `lojix-cli` `bf73b9d3`
  (`lojix-cli: migrate NOTA request examples to bracket strings`);
  `nix flake check --print-build-logs` passed.

The strongest recurring test-name pattern was constraint naming:

- `nota_argument_accepts_apostrophe_text_without_quote_delimiters`
- `source_path_with_apostrophe_must_not_require_quote_delimiters`
- `public_certificate_with_apostrophe_must_not_require_quote_delimiters`
- `error_messages_with_apostrophes_do_not_require_quote_delimiters`
- `config_paths_with_apostrophes_do_not_require_quote_delimiters`

These names are preferable to generic `bracket_string` tests because
they pin the production reason for the migration: authored NOTA should
fit naturally inside shell double quotes while ordinary text can contain
apostrophes.

## Open Blockers

`lojix` is not committed from this pass. After `signal-lojix` advanced
to `a007e8b6`, `lojix` no longer fails on the old `NotaSum` cleanup;
it fails because the daemon/client code still uses retired
`signal-lojix` and `signal-frame` names such as `wire::LojixFrame`,
`wire::LojixFrameBody`, `wire::LojixChannelReply`,
`wire::LojixChannelRequest`, `wire::DeploymentSubmission`, and
`wire::DeploymentObservationSubscription`. The current contract emits
`Frame`, `Operation`, `Reply`, `LojixReply`, `LojixEvent`, and
`StreamKind`.

Tracker: bead `primary-36iq.6.1` (`lojix` current signal API port).

`nexus` is not committed from this pass. The checkout had unrelated
pre-existing dirty work, and `nix flake check --print-build-logs`
is blocked before Nexus tests run by locked dependency `signal`
`36dd4bc9`, which still imports removed `nota_codec::NotaSum` in
`edit.rs` and `query.rs`.

Tracker: bead `primary-36iq.6.2` (Nexus stale `signal` dependency
refresh).

Locked Persona/signal source edits remain deferred while
`second-operator` owns the broad `signal-persona-origin` rename lock.
The read-only audit found available locked repos already resolving
`nota-codec` to bracket-string-capable `538555e8`, and it lists the
specific post-lock quote examples to migrate.

## Bead State

Updated tracker state:

- `primary-36iq.3` remains open because the live installed Spirit CLI
  profile pin still rejects bracket strings even though `nota-config`
  has a pushed Nix witness.
- `primary-36iq.6` remains open and is now blocked by
  `primary-36iq.6.1` and `primary-36iq.6.2`.
- `primary-36iq.7` remains open for the broader authored-example sweep;
  it now records the pushed migration progress and the remaining locked
  or blocked surfaces.

## Recommendation

Treat this migration start as successful for the repos that were pushed
and Nix-verified. Do not try to force-close the overall bracket-string
consumer migration until the `lojix` signal API port, the Nexus stale
`signal` dependency, and the locked Persona/signal quote examples are
handled in their owning lanes.
