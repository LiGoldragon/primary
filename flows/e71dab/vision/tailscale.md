
# Fix the Tailscale problem; build on Prometheus, not Ouranos

Context: the living gave this direction before sleeping, asked that cluster topology, data and administrator roles/features guide any additions, and left judgment to Fable. The transcriber corrected “next” to “Nix” and “Uranus” to “ouranos.”

> Okay well, you can get that Tailscale problem figured out and fixed. Make sure you follow the topology of the cluster, data, and administrator roles and features in order to add data in order to know which host does what. I leave it to Fable's best judgment because I'm going to sleep and I want this to be done. You can present me with what has been done afterwards but I want you to stop doing [Nix] builds and [Nix] tests on [ouranos] and move everything to Prometheus now.

-- psyche, typed, 2026-09-25 ~22:05.

## Remote builders are the default; local fallback is allowed on failure

Context: refining the build-host order after the report that Prometheus was answering as remote builder. This narrows the prior absolute Ouranos prohibition: local Ouranos building is allowed only when remote building fails, not as routine.

> You can't really write down literally the skills but we're moving back to remote builders. Of course you can fall back to local building but I guess you don't have a way to wake me up if something goes wrong. I'll hear the laptop running because it's next to me. Prometheus should be doing the builds and running the fan hard so I shouldn't hear my laptop run really hard most of the time.

-- psyche, typed, 2026-09-25 ~22:08.
