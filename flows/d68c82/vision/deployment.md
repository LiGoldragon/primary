
## One source for every Flow part, so no version divergence

> There should only be one package or one source for all of them and so there should be no version divergence.

Context: the Flow CLI and the Flow Nexus were reported at different versions.
-- psyche, STT, 2026-10-13.

## Everything is installed from source

> Well the only way to install anything on our system is to install it from source. If none of them are installed from source, then none of them are installed properly anyway and all of these so-called installations should be removed because that's not how we install anything.

Context: Flow was found reaching the machine through two flake pins, a hand nix-profile install, a stale link from an unmerged branch, and a debug build in /tmp.
-- psyche, STT, 2026-10-13.

## Harness components live in the home environment, for now

> Flow only needs to be installed in the home environment. We can just have all of the harness components installed in the home environment for now until we actually start to layer things and create different permissions and things like that. We're not there yet so let's just keep it simple.

-- psyche, STT, 2026-10-13.

## Work on main until it works

> I don't know why we're using branches. That thing isn't even in production so let's just work on `main` until it actually works. Get everything merged unless it makes no sense. If that is the case then that's another failure, right? Oh my god, we need to figure out how to avoid that failure.

Context: Field reported the Flow fix for typed store and SYSTEM sits on an unmerged child branch, so Flow main cannot be deployed.
-- psyche, STT, 2026-10-13.

## The meta-flow identifier everywhere; declarative deployment; clean up; nexuses are the long term

> If the send command still needs the flow ID, then my change hasn't been done properly. The send command should use the same identifier that we're using now, which is the 3-field identifier of a metaflow. I want the whole system to use that everywhere.
>
> Essentially the flow ID is registered as the corresponding current flow ID for a metaflow and is resolved in the runtime. The agent doesn't have to figure any of this stuff out.
> - Get Mind to fix that right now and deploy through the proper way of deploying, which is how it should be deployed. If it's not, then it should be deployed that way and fixed as well.
> - Get somebody to audit and make sure everything is deployed declaratively. If not, actually deploy declaratively and get rid of all of this dirty mess of garbage code that doesn't even run, that we're not even using, that isn't deployed properly, or that doesn't have the right version deployed.
> - Clean up the system. I feel like I'm telling you this and you won't even be able to do it. You'll come up with some reason why there's a blocker, why there's this dependency on this thing that nobody uses. You can try and use your judgment to see that a lot of the code, which is actually frustrating, is not even being used.
> - I want to move towards using the nexuses everywhere. They're the long-term vision and then we have this short-term mission. Let's go over all of this, this long-term and short-term stuff everywhere.
> - I want an extensive book on this: what's the short term, what's the long term. Let's put it down in the vision properly and then let's readjust everything, all of the context types below that, to the vision, and all of the code as well.

-- psyche, STT, 2026-10-13.
