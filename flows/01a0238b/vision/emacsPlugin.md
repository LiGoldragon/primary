# Emacs plugin

## Standalone repository and CriomOS-home input

> The emacs plugin would get its own repo, and become an input to criomos-home.

Context: While continuing the Emacs extension proposal from flow `01a020ff`,
the psyche placed the plugin in its own repository and made that repository an
input to `criomos-home`.

Provenance: Codex transcript
`/home/li/.codex/sessions/2026/08/21/rollout-2026-08-21T10-58-38-01a0238b-2c53-76e1-9ae9-5c87f909544f.jsonl`,
timestamp `2026-08-21T08:59:25.686Z`, user-message record ordinal 8,
physical line 9, turn `01a0238b-e2c9-7021-90ac-6fc2c50d21bb`, message
`msg_01a0238b-e476-7ad2-b938-5e194676eb97`.

## Public repository, D-Bus, and Home-owned theme generation

> 1. yes a new public repo.
>
> 2. the dbus is good
>
> 3. yes

Context: The answers select a new public repository rather than the existing
whole-distribution `CriomOS-emacs` scaffold; select the proposed narrow
Chroma-owned session D-Bus protocol rather than a dedicated bidirectional Unix
stream; and keep Ignis theme generation in `criomos-home` while the plugin owns
projection only.

Provenance: Codex transcript
`/home/li/.codex/sessions/2026/08/21/rollout-2026-08-21T10-58-38-01a0238b-2c53-76e1-9ae9-5c87f909544f.jsonl`,
timestamp `2026-08-21T18:15:44.884Z`, user-message record ordinal 232,
physical line 233, turn `01a02589-37bd-7301-8300-69206501773d`, message
`msg_01a02589-37f4-79d0-9ce4-c51b55b68b9e`.

## Approved implementation shape

> good enough, approved

Context: The psyche approved public repository `chroma-emacs`; Emacs feature
`chroma-theme` and global `chroma-theme-mode`; Chroma-owned D-Bus desired-theme
publication with persisted monotonic revisions, change signals, typed
acknowledgements, and queryable per-consumer `Pending`, `Applied`,
`Unavailable`, or `Failed` state; full Lisp errors retained in Emacs with
bounded typed failure reported to Chroma; Ignis generation and declarative
configuration owned by `criomos-home`; no plugin scheduling, palette
generation, embedded paths, or disabling of unrelated overlay themes; and a
cohesive three-repository implementation with repository-local checks plus an
end-to-end daemon witness in `criomos-home`.

Provenance: Codex transcript
`/home/li/.codex/sessions/2026/08/21/rollout-2026-08-21T10-58-38-01a0238b-2c53-76e1-9ae9-5c87f909544f.jsonl`,
timestamp `2026-08-21T18:18:15.894Z`, user-message record ordinal 281,
physical line 282, turn `01a0258b-85b8-7fa3-90df-d59314a20885`, message
`msg_01a0258b-85d6-7660-b0ee-211b77f8807d`.
