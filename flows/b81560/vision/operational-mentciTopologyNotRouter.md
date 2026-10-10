# Operational: Mentci is not a router per se — it has many connections because it's the user's interface; components talk directly, security is designed over the whole

## Mentci has a lot of connections because it's the user interface. It could have meta access to everything as admin/developer. Components talk directly. We design security over all nexuses. Eventually nexuses that shouldn't talk can't at the system level

Context: artifact comment by the living on the Session Flashbook, 2026-09-19,
on the "Mentci Router" label in the architecture diagram. The living corrects:
Mentci is not a router — it has many connections because it's the user's
interface. Currently flat admin access for development. Nexuses talk directly
to each other by design. Security is designed over all nexuses at the whole
level. Logged by the main flow before acting.

> Well, we don't have to think of Menchie as a router per se, because then we can think of many things as a router. There's just a topology, and Menchie has potentially a lot of connections because it's the user's interface. It could potentially, as a developer or admin, have meta access to everything, which is what we're deploying now: a Menchie that has access to everything because it's just a uni. It's a flat access, prototype development type system.
>
> There's no other user, so it's just me with my all-powerful admin as the developer. The Nexus will just have access to all the Nexuses, but then that will change. It's not that it's a router per se. It's not really a router. The router would be the part where someone can try to reach an Nexus more dynamically, like outside on another node, or to reach an Nexus it doesn't have direct access to, or to, I don't know, maybe.
>
> Conventionally, things just talk to each other, and if some things have to be logged, then these components will log them because that's how we design it. We design our own security over all of the Nexuses, so we have correctness there on the whole. But yeah, eventually, whatever nexuses aren't supposed to talk to each other aren't even going to be able, at the system level, to do so.

-- psyche, artifact comment on Session Flashbook. ("Menchie" reads "Mentci"; STT correction.)
