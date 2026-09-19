# End-of-last-reply lifecycle observation is TESTING

> We should have an end-of-last-reply hook that notifies the Flow component using the Flow CLI of all the information it can give it. In the last response, possibly we should also send that to Flow, and then Flow would send that to the reaping agent to decide if that's the end of Flow and if it should be reaped. The Flow nexus should also be aware if there's a successor already up, and it could take a screenshot, even of that, and send it to the reaper to judge if the new Flow is up.

-- psyche, relayed verbatim by root on 2026-09-19. The ASCII apostrophe in `that's` is preserved from the source.

This is a request for a lifecycle design. It does not authorize a hook to retire a flow by itself.

Psyche consultation on 2026-09-19 proposes a typed ordinary-socket report,
`Report.EndOfTurn.{ … }`, translated from the harness through FlowCLI and routed
by FlowNexus to the reaper. The consultation distinguishes a final reply from
flow completion, requires children returned, locks released, changes pushed,
and successor/handoff readiness before retirement, and treats screenshots as
corroboration only. The socket and subscriptions are not implemented.

One design question remains with root rather than being attributed to Psyche:
how a reaper preserves unresolved work with accepted ownership without making a
completed predecessor immortal. The current user direction rejects using that
question as a blanket reason to retain completed predecessors.
