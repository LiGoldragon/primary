# ethosSourceFiles

## 2026-08-25 — sema and nexus in the signal repos: a problem

(Spoken during the audit of 01a03603, on seeing the authored-interfaces
layout — the diagram is quoted from the material the psyche was
reading.)

> I can see a problem already:
>
>      AUTHORED INTERFACES
>       +--------------------------+       +--------------------------+
>       | signal-orchestrate       |       | meta-signal-orchestrate  |
>       |                          |       |                          |
>       | signal.ethos             |       | signal.ethos             |
>       | nexus.ethos              |       | nexus.ethos              |
>       | sema.ethos               |       | sema.ethos               |
>       +------------+-------------+       +-------------+------------+
>                    |                                   |
>                    +----------------+------------------+
>
> sema and nexus in the signal repos.

Context (agent-authored, separate from the psyche's words): the flagged
fact matches 01a03603's own decision ledger, decision 6 — nexus.ethos
and sema.ethos exist in both wire repos as "exact empty Interface
documents". The problem statement extends this topic's 2b34fafa ground
(one .es file, one Rust module) to placement across a component's
repositories.
