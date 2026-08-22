Subject: Ouranos ordinary Lojix state for goldragon/zeus.

Method: probe `systemctl is-active lojix-daemon.service`, socket existence, and
`LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix
'Query.ByNode.(goldragon zeus None)'`.

Observed: `lojix-daemon.service` is active; both ordinary and owner sockets
exist. The typed ordinary query returned `Queried.([] [] (625 625))` with no
Zeus generation or deployment records at marker 625.

Inference: the current Ouranos Lojix durable view has no committed
`goldragon/zeus` generation or deployment. This does not prove that Zeus's
target-side profiles or any separately hosted daemon have no state.

Unknown: no target-side Lojix query was attempted; the request was specifically
to re-query Ouranos ordinary state.
