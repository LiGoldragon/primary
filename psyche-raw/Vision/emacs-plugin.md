## 2026-08-21T10:58:38+02:00 · session 01a0238b · standalone repository and CriomOS-home input

> The emacs plugin would get its own repo, and become an input to criomos-home.

Context: While continuing the Emacs extension proposal from realization flow `01a020ff`, the psyche placed the plugin in its own repository and made that repository an input to `criomos-home`.

## 2026-08-21T10:59:25.686+02:00 · session 01a0238b · exact source-event timestamp

> The emacs plugin would get its own repo, and become an input to criomos-home.

Context: This preserves the exact source-event timestamp and provenance from `/home/li/.codex/sessions/2026/08/21/rollout-2026-08-21T10-58-38-01a0238b-2c53-76e1-9ae9-5c87f909544f.jsonl:9`. It supersedes only the timestamp on the preceding entry; the ruling is unchanged.

## 2026-08-21T20:16:12+02:00 · session 01a0238b · a new public repo

> 1. yes a new public repo.

Context: This answers whether the Emacs plugin should use the existing whole-distribution `CriomOS-emacs` repository or a new focused repository. The psyche selected a new repository and ruled that it is public.

## 2026-08-21T20:16:12+02:00 · session 01a0238b · the D-Bus is good

> 2. the dbus is good

Context: This answers the proposed transport fork between a narrow Chroma-owned session D-Bus theme protocol and a dedicated bidirectional Unix-stream protocol. The psyche selected D-Bus.

## 2026-08-21T20:16:12+02:00 · session 01a0238b · Ignis theme generation remains in CriomOS-home

> 3. yes

Context: This answers whether Ignis theme generation remains owned by `criomos-home`, with the standalone Emacs plugin owning projection only. The psyche confirmed that ownership split.

## 2026-08-21T20:18:25+02:00 · session 01a0238b · approved implementation shape

> good enough, approved

Context: The psyche approved the proposed names and complete implementation shape: public repository `chroma-emacs`; Emacs feature `chroma-theme` and global `chroma-theme-mode`; Chroma-owned D-Bus desired-theme publication with persisted monotonic revisions, change signals, typed acknowledgements, and queryable per-consumer `Pending`, `Applied`, `Unavailable`, or `Failed` state; full Lisp errors retained in Emacs with bounded typed failure reported to Chroma; Ignis generation and declarative configuration owned by `criomos-home`; no plugin scheduling, palette generation, embedded paths, or disabling of unrelated overlay themes; and a cohesive three-repository implementation with repository-local checks plus an end-to-end daemon witness in `criomos-home`.
