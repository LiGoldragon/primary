# Operational: psyche propagation

## Flows need to message each other more abruptly than a queued turn, especially when psyche has just spoken. A specialized subflow — a Luna call — takes the context and the verbatim psyche words, decides who this needs to go to, and delivers. Some routes are default-required. A cluster in shared-psyche mode gets every psyche update.

Context: typed to primary Psyche opus (Claude, medium, flow 108ab0) on 2026-09-17 during the refresh, right after approving the subflow-script skill edits. This entry captures the design; the anatomy questions are put back in the reply and remain open until answered. Logged by the main flow before acting.

> I want you guys to find a way to be able to message each other more abruptly. Sometimes you need to tell each other stuff more right away, like when the psyche comes in. There are some places where you should anyway. We kind of have to program that, but we need to preprogram that the direction messages from the psyche that came in have to be propagated. That's why we need a specialized subflow to do that.
>
> It's just a specialized Luna call that gets the context, puts in the verbatim psyche words, and decides who this needs to go to. There are some good guidelines on the defaults, but there are some places where it has to go through by default. If some of the flows are in a cluster that has the shared psyche mode on, then they should get all the updates of the psyche.

-- psyche, typed.
