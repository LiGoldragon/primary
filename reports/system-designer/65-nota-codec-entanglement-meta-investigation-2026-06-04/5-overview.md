---
title: 65.5 — Overview — the nota-codec entanglement, synthesised
role: system-designer
variant: Psyche
date: 2026-06-04
topics: [nota-codec, bracket-strings, hand-rolled-parsers, chroma, sema-engine, latent-break, lockfile, migration]
description: |
  Orchestrator synthesis of the four-angle nota-codec entanglement investigation.
  The headline corrects the earlier framing: this is not a redb-2 "cohort" problem
  and it is not really caused by sema-engine adoption — it is ONE component
  (chroma) whose hand-rolled config parser is already broken at nota-codec HEAD
  and survives only on a stale lockfile. nota-codec history is linear; the quote
  removal at f761421 deleted Token::Str; every consumer declares branch=main, so
  the break is a latent time bomb gated only by committed locks. The fix is to
  port chroma's config.rs onto NotaDecode (deleting its bracket->quote re-encoder)
  and bump every lock to HEAD — the schema chain and sema-engine compile unchanged.
---

# 65.5 — Overview: the nota-codec entanglement

Kind: psyche (orchestrator synthesis of the meta-investigation)
Topics: nota-codec, bracket-strings, hand-rolled-parsers, chroma, sema-engine, latent-break
Date: 2026-06-04

## Intent Anchors

[NOTA strings come EXCLUSIVELY from bracket forms; quotation marks do not form string types; the nota-codec encoder structurally cannot emit a quote.] (AGENTS.md hard override)

[No hand-rolled parsers — parsing goes through the NOTA codec / NotaDecode derive surface, not bespoke lexers.] (skills/rust/parsers.md)

[Sema-engine is the exclusive interface to the database; the boundary cleanup surfaced this entanglement.] (Spirit 2563)

## The finding, in one line

It is **not a cohort and not really about sema-engine**: it is **chroma alone**,
whose hand-rolled config parser is **already broken at nota-codec HEAD** and only
compiles today because its `Cargo.lock` pins an old revision. It is a latent time
bomb, urgent on its own.

## What is actually true (correcting my earlier framing)

My report 63 / earlier chat framed this as "the redb-2 cohort has stale
nota-codec pins; adopting sema-engine drags nota-codec forward and breaks the
cohort." The investigation corrects that on three points:

1. **nota-codec history is linear, not two branches.** `538555e` (chroma's pin;
   bracket strings + `Token::Str`, no shape layer) → shape layer added
   (`323a3a7`+) → `d00fbf5` (the schema chain's pin; shape layer **and** still
   `Token::Str`) → **`f761421`** (deletes `Token::Str`; a quote becomes a hard
   `Error::QuoteStringDelimiter`) → `24e7823` (HEAD). Verified by
   `git merge-base --is-ancestor`.

2. **The break is latent, gated only by stale lockfiles.** Every consumer —
   chroma, sema-engine, signal-sema, signal-frame, schema — declares
   `nota-codec = { branch = "main" }`. Cargo unifies one revision per git source,
   so the next fresh resolve to HEAD forces all of them onto `24e7823`. None of
   the committed locks include the quote-removal rev yet; a CI run or fresh
   checkout without the committed lock **already breaks chroma today**,
   independent of any sema-engine work.

3. **chroma is the lone live holdout, and it is doubly anti-pattern.** Its
   `src/config.rs` (`use nota_codec::{Lexer, Token}`; matches the removed
   `Token::Str`) hand-rolls a 742-line bespoke lexer whose
   `config_text_with_bracket_strings_as_quoted` rewrites bracket strings
   `[..]`/`[|..|]` **back into `"`-quoted strings** to feed the old
   quote-accepting lexer — the exact inversion of the bracket-only rule. It also
   uses free functions (method-only violation). The schema chain
   (signal-sema/signal-frame/schema) and sema-engine have **no quote-lexing in
   their own code** — they are HEAD-clean; re-resolving them to `24e7823` is a
   no-op-plus-verify. Other repos with old pins (signal-frame, nota-config) use
   the correct API and are forward-compatible (lock bump only). `corec`/`askicc`
   carry their own separate lexers (a different conversation).

So the blast radius is essentially **one component**.

## Why it happened — the conceptual root

This is one discipline (NOTA strings come exclusively from bracket forms)
cutting through the dependency graph and severing the single component that
**hand-rolled its own NOTA parser** instead of decoding through `NotaDecode`.
It is the **same anti-pattern as the sema-engine boundary bypass**: chroma
hand-rolls a NOTA parser (instead of the codec) *and* hand-rolls a redb store
(instead of sema-engine). One component, two bespoke substrates where the shared
one was intended. Fixing both is the same move — adopt the shared substrate —
and they can be done in one pass.

## The fix (and the sequence)

1. **Port `chroma/src/config.rs` onto `NotaDecode`/`NotaRecordShape` on current
   nota-codec.** Delete the `Token::Str` scan and the entire bracket→quote
   re-encoder (`config_text_with_bracket_strings_as_quoted`,
   `read_config_block_string`, `read_config_bracket_string`,
   `copy_config_quoted_string`, `push_quoted_string`, `copy_config_comment`).
   Decode `config.nota` as a typed record through the derive surface. Fold the
   method-only fix in the same pass (the config free functions move onto an
   owning `Configuration` impl). This satisfies `skills/rust/parsers.md` and the
   method-only override at once. (bead `primary-n1ao`)
2. **`cargo update -p nota-codec` to HEAD (`24e7823`) in every consumer.** The
   schema chain and sema-engine compile unchanged — verify with build/test, do
   not expect code changes. Confirm chroma's `config.nota` fixtures use only
   bracket-form strings (any `"`-quoted config files must migrate; the current
   lexer rejects them).
3. **Then chroma's sema-engine adoption** (the original boundary fix,
   `primary-y0ec`) lands cleanly — ideally in the same wave as step 1, since both
   are "adopt the shared substrate."

**Do NOT** solve this by re-pinning chroma to old nota-codec — that perpetuates
the debt and leaves the time bomb armed.

## What this means for the broader cleanup

My earlier recommendation — "sequence nota-codec modernization → sema-engine
adoption across the redb-2 cohort, and don't dispatch more stray ports" —
collapses to something much smaller and more urgent: **there is no cohort;
chroma is the one stale parser, and it is already broken at HEAD.** Fix chroma's
two hand-rolled substrates (parser + store) together; for everything else,
moving to current sema-engine is a lockfile refresh, not a parser migration.

## For the psyche

- Confirm the fix direction: **port chroma `config.rs` to `NotaDecode` + bump all
  nota-codec locks to HEAD**, not re-pinning.
- Note the **urgency**: chroma is broken at nota-codec HEAD today and survives
  only on a stale committed lock — a fresh checkout / CI breaks it now. This
  should jump ahead of other stray-port work.
- The chroma `config.rs` port and chroma's sema-engine adoption are the same
  anti-pattern (hand-rolled vs shared substrate) and should land together.

## See also

- `0-frame-and-method.md` — the frame.
- `1-version-delta-and-dependency-graph.md` — the linear nota-codec history, the f761421 quote removal, the latent-via-stale-locks mechanism.
- `2-blast-radius-stale-parser-cohort.md` — chroma is the lone live stale parser; everything else is a lock bump.
- `3-conceptual-root-and-related.md` — the bracket-only discipline severing the hand-rolled parser; the shared-anti-pattern link to the sema-engine bypass.
- `4-solution-and-sequencing.md` — the NotaDecode port + lock-bump plan.
- Beads `primary-n1ao` (chroma config migration), `primary-y0ec` (sema-engine boundary strays).
- `reports/system-designer/63-sema-engine-boundary-conformance-audit-2026-06-04.md` — the cohort framing this corrects.
