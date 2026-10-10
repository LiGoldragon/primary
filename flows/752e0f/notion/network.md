# A semi-stateless chain of NAT subnets from whichever node has internet

Context: after the Zeus probe showed Prometheus's USB downlink never brought up.

> Can't we design a network where, if a node gets internet reachability, it then becomes a top-level NAT subnet and passes a second-order-sized subnet to the second node, which in this case is Prometheus? Couldn't we make it sort of semi-stateless, using existing tools and infrastructure and normal setup, so that we maintain this coherent subnet (not a single subnet) for internet access from nodes that can get it? Would that be a simple architecture and easy to do?

-- psyche, typed, 2026-09-25, directly to Psyche High 752e0f. Logged as notion: a design put as a question.

## Existing works on resharing internet

> And yeah on the resharing of internet, what are the existing works? Is it really thin and is it kind of brittle? Has nobody even really done internet rerouting properly?

-- psyche, typed, 2026-09-25, directly to Psyche High 752e0f.

## The 4-to-6 conversion at the node with internet

> A few years ago I was going to do a 4-to-6 conversion (stateful conversion, I think), so that the internal IPv6, easy-to-configure large subnets would just route externally to IPv4 seamlessly. Essentially the node that would get internet would do the 4-to-6 conversion. It would spawn a service for that and create this IPv6 subnet that routes to the internet and we could even get a

-- psyche, typed, 2026-09-25, directly to Psyche High 752e0f. The message ends mid-sentence at "we could even get a"; the rest is asked for.
