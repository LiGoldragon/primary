# Nota-Next Archived-Intent Integration

Phase 2 dedicated append: integrate the 47 archived Spirit intent records routed
to `repos/nota-next/ARCHITECTURE.md` into that one surface as coherent direction
prose, then commit and fast-forward push via the repo's own jj.

## Task and scope

- Target surface: `/git/github.com/LiGoldragon/nota-next/ARCHITECTURE.md`
  (own git+jj; `repos/nota-next` symlinks here).
- Inputs: `/home/li/primary/agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`
  (47 ids routed to nota-next) and `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`
  (verbatim record text).
- Mandate: integrate (not raw-dump), group thematically, synthesize into existing
  sections, dedupe against existing prose, redact any `[SECRET]` record.

## Result: integrated and pushed

- Records integrated: all 47 routed ids, each cited inline by Spirit id.
- Commit: `bea7e284` (`bea7e2840ac2`) on `main`.
- Push: success, fast-forward only — origin `main` moved `5fbe60b0` ->
  `bea7e284` ("Move forward bookmark main"). `main` and `main@origin` now equal.
- `[SECRET]` redactions: none. The three archive-wide secret ids (`go41`,
  `wn7q`, `2qhw`) are not in this set; verified none of the 47 carry a SECRET
  marker or non-Zero privacy. No secret value was written.

## Pre-flight gate (all conditions met before any edit)

- Working copy clean, `@` empty directly on `main` (`5fbe60b0`).
- `jj git fetch` => "Nothing changed"; `main` and `main@origin` identical, so
  main not behind origin and not divergent. No `jj new`/rebase needed.
- No other agent owned `nota-next` (Observe Roles: `nota-designer` lane held no
  claims; the active `system-designer` claims cover CriomOS/clavifaber/lojix
  family, not nota-next).

## Sections touched

- Direction: added typed-text rationale and NOTA+schema-as-pure-data half-step
  to SEMA; embedding-safe bracket-string carrier; bare-atom default and
  `;;`-comment rule; qualifies-as-vs-is parse-time promotion. Strengthened the
  `@`-binder retirement with full parser-removal and positional authored surface.
- Planes: enriched the `NotaString` codec bullet with the two bracket-string
  forms (inline `[text]`, four-char bracket-pipe block with indentation stripping).
- Boundary: added positional-struct and delimiter semantics (vector vs struct
  reading, strict key-value brace, known-enum slot omission, optional-empty
  variant rendering, flat multi-arg type references, over-bracketing avoidance,
  plural-reply vectors); the schema-vs-NOTA division of labor (schema owns all
  type-name vocabulary; NOTA owns structure and `None`/`(Some x)`; three
  delimiters map to three schema sections; namespace is a key-value map); and the
  macros-as-data block (macros are serializable data trees, type-directed
  structural matching via `#[derive(StructuralMacroNode)]`, grouped declaration
  form, locked `(Macro Input+ Output)` syntax, index-then-lazy loading,
  formatter-derived-from-macros).
- New section "Binary boundary": rkyv as the single encoded form with NOTA as the
  text projection at the CLI/inspection edge; rkyv root+box layout mirrored;
  text/binary boundary in the client; CLI-with-NOTA forces binary daemon
  protocol; daemon builds NOTA-free behind a `nota-text` feature; one rkyv
  `Configure` startup message doubling as runtime meta op; typed self-descriptive
  feedback enums; `SymbolPath` identity rendered as NOTA at edges; one-NOTA-arg
  Help; trace events rendered as NOTA; assembled-schema canonical NOTA-and-rkyv
  codec with `(Public/Private Name Value)` visibility wrapper.

## Records by theme

- Direction / rationale: `rnrg` `61lk` `7y8w` `0dsr` `laim` `fvtf`, `@`-binder `own9`.
- Collection / positional / delimiter semantics: `qw1j` `voa8` `ghw7` `vr32`
  `3sq4` `oqwb` `wqdi` `3naf` `vqbt` `sqx6` `2dzp` `6oun` `5myr` `ychx`.
- Bracket-string forms: `vfjw` `f8m3` `7rrs` `3qjw` `bhs5`.
- Macros-as-data: `4itr` `xai7` `v0n6` `fo38` `h6fh` `ydpa` `5p9s`.
- Binary boundary: `a9sq` `n5ch` `b1vi` `o2xk` `t4gd` `cyik` `ur16` `bexd`
  `r0le` `hetk` `8p0r` `pmg5` `hc0t` `zg84`.

## Dedup and conflict decisions

- Records already captured by existing prose were folded by enrichment, not
  re-stated: the `@`-binder retirement, `Vec`/`BTreeMap`/`Option` codec shapes,
  `is_*`/`qualifies_as_*` predicates, and the typed structural-macro-node
  mechanism each already had a home and were extended rather than duplicated.
- `ychx` (Low certainty) read `[]` as struct-and-fields; this contradicts the
  High/Medium-certainty `qw1j`/`voa8`/`own9` that `[]` stays a vector never
  redefined as struct. Resolved per those high-certainty records and cited
  `ychx` as the earlier exploration that resolved into the current direction,
  rather than propagating the superseded claim.
- `7rrs`/`bhs5`/`f8m3`/`vfjw` are genuinely truncated in the source dump (cut at
  `[|...\`). Their durable readable substance (two bracket-string forms; inline
  `[text]`; pipe-block with escaped close markers) is integrated; no truncated
  tail was invented, and it aligns with the existing `[|...|]` text-form prose.

## Checks run

- All 47 ids present and cited: verified (52 distinct Spirit ids now cited in the
  file, the 47 plus pre-existing `j9du`/`hh3z`/`bpyu` and the new `nota-text` is
  not an id). One initially-uncited id (`ychx`) added per the conflict decision.
- Markdown sanity: no `---` horizontal rules; heading tree is
  `# Architecture` / `## Direction` / `## Planes` / `## Boundary` /
  `## Binary boundary`; file 180 -> 375 lines.
- `nix eval .#packages.x86_64-linux` => `[ "default" ]` (flake intact; docs-only
  change does not affect derivations).
- `jj status`: only `ARCHITECTURE.md` modified.

## Blockers / follow-up

- None blocking. The lane-level `(Release repo-scaffolder)` acknowledgment named
  a `schema-next` path, indicating a concurrent append worker shares the
  `repo-scaffolder` lane; my narrow `nota-next` path claim was accepted and the
  edit affected only the intended file, so the integration is unaffected. Future
  parallel append fan-outs should claim under distinct lane identifiers to avoid
  the shared-lane release ambiguity.
