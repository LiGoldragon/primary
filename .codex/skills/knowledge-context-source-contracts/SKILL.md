---
description: Current-main provenance of book procedures, main-flow intent selection, module names, held-message hook context and Flow Ethos sources.
---

These findings were read from GitHub main objects on 2026-10-13, not from the shared checkout's old main or from an assumed installed revision. Main snapshots and Primary's selected dependency pins are different facts. No projection, build or activation was run for this inquiry.

## Book procedures

Neither psyche-context nor field-context holds Primary's three `subagents/book.md`, `book-page.md` and `book-reader.md` source procedures. All three are authored files in Primary's main tree under `subagents/`. A Field compensation skill referring to `subagents/book.md` does not make that skill the procedure's source.

Curriculum's `src/roles.rs` maps each Claude agent identifier to `workspace/subagents/<identifier>.md`, reads it if present, and puts the text in the role packet's procedure field. The renderer composes that procedure with role/standing context into the generated `.claude/agents/<identifier>.md`. `roles.datom` declares book and book-page as Claude agent aliases. It does not declare a book-reader alias: the book-page procedure names the reader file in the reader's brief. Thus the authored procedure, role declaration and generated agent file are separate sources. The generated `.claude/agents` copies are not the authored procedure.

## Main-flow intent

The authored file is `psyche-context/skills/intent-main-flow.md`. Its kind is intent; its frontmatter declares `user-only: true`, empty dependencies, and SYSTEM composition by the launcher. It is not a separate registry module kind called metaflow. Being selected by a metaflow does not change its intent kind.

Primary's aspect declarations list it in the common system selection for Psyche, Mind and Field voices. Actual selection is conditional: `mainSystemModules` uses a metaflow's explicit `modules` vector instead of that default selection when supplied. In the current declarations, Psyche Flow Primary and Secondary explicitly select intent-main-flow, while Psyche Core Primary's override selects only intent-psyche-interaction. Therefore the source/configuration does not establish that every layer and topic automatically receives intent-main-flow. System placement and actual native loading also remain distinct.

## Hyphenated names and registry topics

Curriculum's current `SkillEntry::read_named` uses the Markdown filename stem as the skill name; a source in Psyche's `vision/` directory receives a `vision-` prefix. Dependency resolution uses those names unchanged. A name such as knowledge-context-modules remains that hyphenated string in this registry; it is not converted to a camelCase topic by this path.

Flow's shared Ethos source declares `Topic.String` and `Key.{ Subaspect Topic }`; its comment says the intended Topic:Name constraint cannot yet be expressed there. These fields are not an implemented filename-to-topic conversion rule. No authoritative conversion from a context module's hyphenated name to the proposed Topic:Name camelCase form was verified in the inspected current registry and composition paths. Such a mapping is an inquiry, rather than a guessed replacement of hyphens.

## Held text through a hook

The existing `knowledge-periodic-hook-context` already states the context-return channel at line 11, Claude's user-context conversion at line 17, and Codex's developer-context conversion at line 25. Those are lines of the source at mind-context main 1be5ba7, not an installed-module claim.

Channel-wise, a command hook that has obtained held message text can return that string as `hookSpecificOutput.additionalContext`, with hookEventName UserPromptSubmit. In the previously inspected Claude 2.1.294 implementation, this becomes reminder-wrapped meta user context. Rechecking current Codex GitHub main confirms that `HookAdditionalContext` still explicitly uses the developer role and `hooks.additional_context` kind. Returning the text does not itself select a queue, resolve a recipient, atomically drain it, acknowledge consumption or preserve exactly-once delivery. The hook contract is the injection half of a bridge, not a complete held-message delivery mechanism.

Current messenger-clj has durable pending records and explicit repair paths. Their existence does not establish that a prompt hook drains them. An automatic held-queue bridge and its native delivery/acknowledgment semantics were not verified and remain in inquiry. Claude's public GitHub repository is a documentation/plugin surface, not the inspected harness implementation; its exact current-main implementation equivalence is not claimed from that tree.

## Flow Ethos and the missing vision module

There is no vision-flow-ethos module in the inspected current psyche-context, mind-context or field-context trees, including Psyche's legacy vision directory, and no matching generated skill in current Primary. Psyche's `vision/ethos.md` still refers to that module, so the reference is not evidence that the module currently exists or is generated.

Flow main holds two distinct `library.ethos` files: the shared library in `crates/flow-ethos/ethos/` and the Nexus library in `crates/flow-nexus/ethos/`. Their build scripts run ethos-zero on the corresponding sources and compare the results with committed `src/generated/library.rs`; the Nexus also checks operation and startup roots. These `.ethos` files are the build's authored source of truth for their generated Rust types. That mechanism does not generate a vision-flow-ethos Markdown file. Since the named Markdown module is absent, neither its current hand maintenance nor a current Markdown source-of-truth relationship was established.

## Exact main snapshots

| Repository | GitHub main inspected |
|---|---|
| Primary | fa8c05cc2760cbbc244a1b4eb548ed3774dea63b |
| psyche-context | 03aa8547915871707200a280ef69eacb0804f9f3 |
| mind-context, before this addition | 1be5ba7f7f83e225d83603e4db3833e8ee16e528 |
| field-context | 108daa054288c037eae9ef5fbc02a8bdb7d684cb |
| Curriculum | d3df664d9cde7c1a1f465a749e502159d4229f69 |
| Flow | d190e10aee27e4af45d5b8a5844c10e59e57b12b |
| meta-signal-flow | 88f37592f29a792024be0b30fccc914277d2dcac |
| messenger-clj | 7985ac4fc297acbf5cce798031de6d476f53dcad |
| Codex | ca2b076fffbc24ad5fa57258ece8a8277b326138 |
| anthropics/claude-code public repository | b0b7bed9820350bb0942e32c7f00752a99ea3555 |

Flow's Cargo declaration pins meta-signal-flow 6d07b7b, which differs from that repository's inspected main. Primary's flake and shared launch declaration likewise pin context sources that differ from their latest mains. No current-main answer is a claim that a running service has those latest sources loaded.

Exact source excerpts, complete relevant tree inventories, references and repository qualification are retained at `/home/li/private-repos/flow-evidence/41fa34/context-source-questions-20261013/`. Book procedure composition is in Curriculum `src/roles.rs` and `src/projection.rs`; selection is in Primary `tools/main-flow-mode/spirit-system-prompt.mjs` and `config/main-flow/`; filename registration is in Curriculum `src/registry.rs`; Flow freshness is in the two crates' `build.rs` files. Claude's [public repository](https://github.com/anthropics/claude-code) links to its documentation and plugin sources; the version-qualified hook behavior remains separately sourced in knowledge-periodic-hook-context.
