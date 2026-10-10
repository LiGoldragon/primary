# Stable and next services

## Codex updates by the same stable/next rotation done for Claude

Context: Codex had a new model (Sol 6.1); said to Mind Sol b666e7.

> Just repeat what we've done for [Claude] this morning and update Codex with the next server, so that the current next server becomes stable, and maybe make another version, another next. I don't know, but just find a way to proceed with updating Codex, or at least get the version that has Sol 6.1, or see if you can get Sol 6.1 already.

-- psyche, STT. 2026-09-29 21:23 UTC, b666e7, Mind Sol (session 01a0e9d1, line 3840). Reconstructed by fe945a from transcript. Transcription corrected: "Clojure" → "Claude".

## The rotation protocol: once every flow is on next, next becomes stable and the newer version goes on next

Context: Field Astra d5b96b had left the living on an older Codex; the new version was staged on next but held.

> Oh well, here's the protocol, right? The stable becomes the next [sic] once all the flows have moved onto the next socket. If all the flows are on the next socket now, next can become stable, and then we can put the next version on next.

-- psyche, typed. 2026-09-30 13:59 UTC, d5b96b, Field Astra (session 01a0ee2e, line 4095). Reconstructed by fe945a from transcript. "The stable becomes the next" kept as written; the following sentence says next becomes stable.

## The rotation becomes a compensation skill, named "compensation update"

Context: Three consecutive messages following the protocol above.

> This becomes a compensational skill.

> We can call it maybe "compensation update", or should we just call it Codex? Not sure.

> I mean compensation codex. Because it's a principle we can apply to more than one thing, we can maybe mention it in a compensation codex, but I think it's better just like compensation update. Or something like that.

-- psyche, typed. 2026-09-30 14:00-14:01 UTC, d5b96b, Field Astra (session 01a0ee2e, lines 4103, 4125, 4139). Reconstructed by fe945a from transcript.

## Each socket carries a version-hash suffix, so next moves to stable without renaming the socket

Context: Same exchange, on doing the rotation without breaking running sessions.

> ... Here's a clever thing: we would have to think of a clever way to do that, but each service is going to have this unique suffix.
>
> Maybe we can get the short version of the hash of the version of Codex that we're using for it, so that each socket will have a different name. That way, we can move the next to the stable without changing the socket name, so it doesn't break any of the sessions.
>
> Maybe we can do that in a hacky way, with a bunch of comments on how we're going to fix it next time. The current next can just stay called whatever it is, and the next next can have this new hash-suffixed version socket. That way, we don't break our current sessions.

-- psyche, typed. 2026-09-30 14:06 UTC, d5b96b, Field Astra (session 01a0ee2e, line 4151). Reconstructed by fe945a from transcript.

## The infinite socket rotation naming mechanism

Context: Asked of Mind Astra 6f51ad; names the mechanism of the entry above.

> Are we ready to deploy the next Codex infrastructure that will have Sol 6.1, the newest Codex? Using the infinite socket rotation naming mechanism that allows us to move next to stable without renaming the socket

-- psyche, typed. 2026-09-30 16:50 UTC, 6f51ad, MindV2 Astra (session 01a0e8d3, line 12777). Reconstructed by fe945a from transcript.
