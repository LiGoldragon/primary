# Orchestrate locking

## I don't want to have all these branches; I really don't want to have it like we used to, where we just worked with orchestrate, and we can lock files; we don't have to lock the whole repo; plus, the flows don't need to be locked because, if you have the right attitude, files can be appended only in the flow, or you just create an entry

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the message that also carries the integrator-flow, subflow-identity, and transcript-over-files visions (integratorFlow.md, subflowIdentity.md, transcriptOverFiles.md, same date), and answers the "we have to merge everything" concern of the previous turn (worktreeHygiene.md) by superseding the branch-based workflow itself. "Like we used to, where we just worked with orchestrate" names the earlier pattern: one shared checkout, file-level locks issued by the orchestrate Nexus, no per-flow branches. The right-attitude clause — "files can be appended only in the flow, or you just create an entry" — pairs with the subflow-identity vision that follows: an entry per subflow, keyed by its unique job name, so concurrent flows never collide. Logged by the main flow before acting.

> I don't want to have all these branches. I really don't want to have it like we used to, where we just worked with orchestrate, and we can lock files. We don't have to lock the whole repo. Plus, the flows don't need to be locked because, if you have the right attitude, files can be appended only in the flow, or you just create an entry.

-- psyche, typed.
