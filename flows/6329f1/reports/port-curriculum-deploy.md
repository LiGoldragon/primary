# Port: curriculum-deploy

Report for flow 6329f1.

## Result

curriculum-deploy 0.4.0 ported to the ProtoformStack train and merged
to main at f3f2ee33. Curriculum data migrated to canonical datom at
143125b1.

## Main rev

curriculum-deploy `origin/main`: `f3f2ee33d66121ce445c63e54de756601f55beea`
Curriculum `origin/main`: `143125b1750161ec5da421d1b301342c4c04dc7f`

## Diff verdict

All four generated trees (.claude, .agents, .codex, .pi/agents) are
byte-identical between the new curriculum-deploy 0.4.0 generating from
Curriculum 143125b1 and primary's rendered trees. Confirmed by both a
scratch-directory diff and a real `nix run .#generate-skills` into
primary (built through the remote builder) followed by `jj status`
showing no rendered-tree changes.

## Summary

1. All 708 lines of hand-written DatomRealizing/DatomTextualizing replaced
   by generated Datomic impls from `curriculum-deploy.ethos` (ethos Library).
2. Request root is a data enum: `Generate.{ /curriculum /primary }` is the
   only accepted form. No CurriculumRequest wrapper.
3. No Meaning-to-Text normalization: Text positions accept Text, not Meaning.
   Curriculum's roles.datom migrated to canonical datom (curly-quoted strings,
   spaced delimiters, no parenthesized text).
4. Generated Rust committed as `src/generated.rs` with a rustfmt-formatted
   freshness test through the ethos-zero library. Round-trip test on the
   migrated Curriculum data proves the datom migration.
5. Pins: protos 56c683ec, datomic a27f9b8e, ethos-zero 31c5984c (dev),
   Curriculum 143125b1. Version 0.4.0.
6. All 5 cargo tests pass (3 standard + 2 external-data), clippy clean, fmt
   clean, all 8 nix flake checks pass (built through the remote builder).

## Primary files changed

After updating primary's flake.nix and running `nix run .#generate-skills`:

- `flake.nix` -- curriculum-deploy input 74581e74 -> f3f2ee33, Curriculum
  input 5716f71a -> 143125b1, usage string updated, Check invocation
  updated from `CurriculumRequest.{Check.{...}}` to `Check.{ ... }`.
- `flake.lock` -- follows the input updates.
- `skills/generated-role-outputs.datom` -- format changed: paths now
  curly-quoted (e.g., `".claude/agents/read-trivial.md"`), spaced
  delimiters. Content identical.
- No changes in `.claude`, `.agents`, `.codex`, `.pi` (byte-identical).

Not committed in primary; the main flow commits.

## API deviations

Three deviations documented in `reports/api-deviations.md`:
1. ethos-zero Library mode omits standard derives (worked around with
   `src/generated_ext.rs`).
2. Paths starting with `.` in datom are curly-quoted by datomize; old
   unquoted inventory files are unreadable (cleanup skips gracefully).
3. ~~Meaning/Text boundary~~ resolved: Curriculum data migrated.

## Sources

- curriculum-deploy origin/main f3f2ee33 (witnessed)
- Curriculum origin/main 143125b1 (witnessed)
- nix flake check (8 checks, all passed, remote builder)
- nix run .#generate-skills into primary (remote builder, jj status witnessed)
- diff -rq of .claude, .agents, .codex, .pi/agents (byte-identical)
