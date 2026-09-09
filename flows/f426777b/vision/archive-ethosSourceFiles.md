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

## 2026-08-25 — nexus and sema ethos are not designed yet; when designed they live in the nexus' main repo

(Ruled after the audit showed the empty placeholders, the
Interface-only dialect, and the hand-written Rust state of nexus and
sema in Orchestrate.)

> lets make it clear first; the nexus and sema ethos arent designed
> yet, but when they are they will live in the nexus' main repo

Context (agent-authored, separate from the psyche's words): two
clarifications carried — (a) the nexus and sema ethos document kinds
do not exist yet; the empty Interface-skeleton files in the wire repos
are placeholders for an undesigned kind, not designs; (b) their ruled
home, once designed, is the Nexus's main repository — the component
repo of the three-repo anatomy (component + two signal repos,
012fbf07 2026-08-11). Direct consequence for the generator's contract:
a wire repository carries signal.ethos only; the triplet-per-repo
requirement has no ruled ground.
