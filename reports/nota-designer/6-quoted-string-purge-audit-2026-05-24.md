# Quoted String Purge Audit

## Load-Bearing Result

This pass removed quote-delimited NOTA strings from the most current
unclaimed teaching surfaces I found and strengthened the core
bracket-string witnesses. The remaining quote-shaped examples are either
explicit legacy-compatibility tests, the deployed Spirit CLI caveat, or
blocked migration surfaces now tracked in BEADS.

## Fixed Surfaces

- `skills/skills.nota` now uses bracket strings in the canonical skill
  index, so the workspace's primary NOTA example no longer teaches
  quotation-mark strings.
- `skills/nota-design.md` now shows bracket strings in every NOTA data
  example and says PascalCase string content is delimited as `[User]`.
- `skills/component-triad.md` no longer calls the single CLI argument a
  "NOTA string literal"; it calls it an inline NOTA argument.
- `skills/spirit-cli.md` and `skills/intent-log.md` now warn before the
  live Spirit examples that quote-delimited values are a temporary
  deployed-Spirit compatibility caveat, not authored NOTA style.
- `nota` documents `[| ... |]` as a safe multiline wrapper for
  NOTA-like content until the closing `|]` delimiter appears.
- `nota-codec` documents the same block-string wrapper property and
  labels quote-string parsing/error paths as legacy migration support.
- `message` README now shows `message "(Send designer [Need a layout
  pass.])"` instead of quote-delimited message text.

## Tests

- `nota-codec`: `nix flake check --print-build-logs` passed. New
  witnesses:
  - `block_string_wraps_multiline_nota_like_content`
  - `multiline_nota_like_string_emits_block_form_without_quote_delimiters`
- `nota`: `nix flake check --print-build-logs` passed.
- `message`: `nix flake check --print-build-logs` passed.
- `primary`: no `flake.nix`; changes are guidance/report-only.

## Remaining Exceptions

- Live `spirit` still rejects bracket-string arguments with
  `expected string literal or bare identifier, got LBracket`. The
  examples in `skills/spirit-cli.md` and `skills/intent-log.md` cannot
  switch until the deployed profile pin moves.
- `nota-codec` still has quote-delimited decode fixtures, but every
  remaining fixture is named as legacy migration compatibility.
- Locked Persona/signal repos still have old examples. Bead
  `primary-36iq.7.1` tracks the post-rename cleanup for persona-spirit,
  persona-mind, persona-router, message/signal-message surfaces that
  still apply after renames, and persona sandbox output examples.
- Horizon/lojix live docs still have a few quote-shaped examples that
  should move with the active horizon/lojix migration. Bead
  `primary-36iq.7.2` tracks that cleanup instead of patching under the
  system-designer migration.
- Existing broad trackers remain relevant: `primary-36iq.3` for the
  Spirit profile pin/caveat, `primary-36iq.6.1` for the lojix current
  signal API port, `primary-36iq.6.2` for Nexus's stale signal
  dependency, and `primary-36iq.7` for the overall authored-example
  sweep.

## Audit Commands

Fresh focused greps used in this pass:

```sh
rg -n '\([A-Za-z][A-Za-z0-9_-]* [^\n)]*"[^"]+"|\{[^\n}]*"[^"]+"|spirit '\''\([^'\''\n]*"|message '\''\([^'\''\n]*"|Decoder::new\("[^\n]*\\"' /home/li/primary /git/github.com/LiGoldragon -g '!target/**' -g '!result/**' -g '!node_modules/**' -g '!Cargo.lock' -g '!flake.lock' -g '!*.lock' -g '!*.stderr'

rg -n 'quote-delimited|string literal|quoted string|double-quoted|triple-quote|quotation-mark|quotation mark|uses quotations|"""' /home/li/primary/skills /git/github.com/LiGoldragon/nota /git/github.com/LiGoldragon/nota-codec -g '!target/**'
```

