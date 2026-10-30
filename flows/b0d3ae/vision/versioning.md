# Versioning

## 2026-10-30 — Flow Nexus version 1 is a full rewrite from the bare proposal, by Mind on a fresh dedicated flow pair; a versioning module holds everything said on versioning and nothing old; multiple capsules, no environment variable, upgrade while running, test in different capsules; terminology: the whole running system is the metaflow, a persistent address is a permaflow; metaflows talk to each other so an upgrade runs incrementally without a compatible store
Context: the living, in the Psyche core Primary chat b0d3ae, leaving to shave, after the bare Flow Nexus book reached version 9.

Take the proposal vision that you've made so far and get your mind to start writing Flownexis version 1, which is a full rewrite. Do you understand how to do the full rewrite? I don't think we landed that but we should.

You should just get the proposal that you made for the new version and make it separate or maybe a versioning module, right? You should just find all the stuff we've said about versioning and make sure that it is just that. You can remove any old crap that you might find in the versioning module that might already exist.

I don't know so I trust you to write the versioning module the right way and simply then get your mind on a fresh flow, on a fresh dedicated flow pair, to start a full rewrite. We aren't necessarily going to switch too soon but at least we can start testing it.

Make sure that it can operate in multiple capsules, that nothing depends on an environment variable, and that everything is designed so that we can easily upgrade the nexus while running the system and test it in different capsules. Maybe even eventually allow for multiple flow nexuses to send messages through each other, where we could actually achieve that through a specialized interface that would be like intercapsule messaging.

Actually you know what? I think the meta flow. We need some terminology to talk about different parts here. There's a capsule. I don't think that is the right term because the capsule is really the whole thing. Maybe that's the metaflow. What we call a metaflow now is just a persistent flow or a permaflow maybe. Our main flow also works and whatever you pick doesn't matter. We can change later.

These meta flows, which we call capsules now, could talk to each other. Then you would have a situation where you could update without having a compatible store because you could get communication across metaflows. That would allow you to start incrementally starting the new flows in the next metaflow, where they could still talk to the perma flows in the former metaflow or in the metaflow that's being upgraded from. Does all of this make any sense to you?
