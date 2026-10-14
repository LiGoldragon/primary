---
description: Effort levels advertised by the installed Claude and Codex model catalogs, and the configured Haiku effort correspondence.
---

On 2026-10-13, read-only initialized sessions returned the following model capabilities. These are the installed harness catalogs for the qualified account/configuration, not successful generation tests at every effort or an exhaustive catalog for arbitrary providers.

## Claude Code 2.1.294

| Resolved model | Advertised effort levels |
|---|---|
| claude-fable-5-1, claude-fable-5 | low, medium, high, xhigh, max |
| claude-opus-5-5, claude-opus-5, claude-opus-4-8, claude-opus-4-7 | low, medium, high, xhigh, max |
| claude-sonnet-5-5, claude-sonnet-5 | low, medium, high, xhigh, max |
| claude-haiku-5-5 | low, medium, high, xhigh, max |
| claude-opus-4-6, claude-sonnet-4-6 | low, medium, high, max |
| claude-haiku-4-5-20251001 | no effort capability/level list advertised |

In this actual catalog, aliases fable, opus, sonnet and haiku resolved respectively to Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5; default resolved to Sonnet 5.5. Alias resolution and effort defaults are not immutable model identities. The bundled source separately checks model support for effort, xhigh and max; accepting a frontmatter string alone is not proof that that model executes it unchanged.

## Codex 0.161.0-alpha.2

| Model | Advertised reasoning-effort levels |
|---|---|
| gpt-6.1-sol, gpt-6-astra, gpt-6-sol, gpt-5.6-sol, gpt-5.6-terra | low, medium, high, xhigh, max, ultra |
| gpt-6-luna, gpt-5.6-luna | low, medium, high, xhigh, max |
| hidden gpt-reserve, hidden codex-auto-review | low, medium, high, xhigh, max |
| hidden gpt-5.5 | low, medium, high, xhigh |

`model/list` returned ten entries with no next cursor. A model being advertised, including Terra or a hidden model, does not make it a configured seat or an approved model role. An explicit role's configured effort is also distinct from the catalog's default effort.

## The configured Haiku row

The normal Psyche launcher declaration `config/main-flow/psyche.edn` explicitly sets Quaternary to `claude-haiku-5-5` at **medium**, as it does for the other Claude layers. `claude-main-flow-launch.mjs` passes the selected model and effort to the native CLI. The inspected generated Claude trivial/tester agent definitions also set `model: haiku` and `effort: medium`. These inspected declarations agree with the living's 2026-10-12 “Layer and model equivalence” record in `flows/d68c82/vision/model-roles.md`. That record names medium for Claude throughout and low for OpenAI's Luna Quaternary. It does not establish low for Haiku.

The old `knowledge-layer-models` table is absent from current mind-context main: `f84525c8421f6b1df5e6fc6edef0465cf5008ba9` deleted it and redirected lookups to `vision-model-roles`. An old checkout copy is not a current source rule. This knowledge records the observed configuration; the canonical living correspondence remains in `vision-model-roles`. No living wording or shared dirty checkout was changed. This is not an audit of every live process override.

## Witness

Claude's SDK initialize response was obtained with hooks disabled and no user/model turn; the owned process was normally terminated with exit 143. Codex's raw installed app-server returned `model/list` after initialization without starting a thread/model turn; its owned process ended with exit 0. The Claude bundled capability functions and model entries corroborate its response. Catalogs, arguments, source excerpts and copied launch declarations are retained in `/home/li/private-repos/flow-evidence/41fa34/harness-knowledge-20261013/`, especially `claude-initialize.json` and `codex-model-list.json`.
