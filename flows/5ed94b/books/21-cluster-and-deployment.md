Presentation.{ «The cluster and deployment» }

The three machines, how they reach each other and the internet, how a change reaches a machine and how it is undone, and how the cluster is watched. Each statement is followed by your own words. Where your words leave a gap, the filling is marked proposed.

## Part 1. What he wants

### The three machines and what each is for

Ouranos is your laptop, the machine you sit at. It runs the flows, and it is spared heavy work.

> I'll hear the laptop running because it's next to me. Prometheus should be doing the builds and running the fan hard so I shouldn't hear my laptop run really hard most of the time.

-- 25 September 2026

No AI model is ever kept on Ouranos.

> There should be no AI models on [ouranos] ever and we can garbage collect.

-- 26 September 2026

Prometheus is the builder and the only home for AI models, and it builds itself.

> There must never be AI models on any other node than Prometheus, which is why Prometheus can only be built on Prometheus.

-- 26 September 2026

Prometheus also provides the services, such as the Git server and the build pipeline.

> We can set up a Git server on Prometheus. Let's use Prometheus as a service provider, create those services on criome, and just make this massive proof of concept that works, even with our own build pipeline for the app and on our own machine, Prometheus.

-- 15 September 2026

Zeus is where your partner works. It is a stable machine, and nothing is tested on it.

> So Zeus, another host where my partner works, is having problems.

-- 8 August 2026

> If anything, Zeus is a stable node. We shouldn't be testing stuff.

-- 19 September 2026

Two more hosts are coming. What each machine does is written in the cluster data and read from there.

> I have two more hosts to add to the cluster, which could function as really useful things like routers and a secondary user interface for the persona harness, even a minimal version.

-- 18 September 2026

> Make sure you follow the topology of the cluster, data, and administrator roles and features in order to add data in order to know which host does what.

-- 25 September 2026

### How they are reached

The network is one identity-based private mesh, IPv6 inside, and any machine with internet can be the gateway.

> We're going to have this tailnet identity-based network, super efficient, IPv6 internal, with intelligent subnet/subnetworks with IP4 to IP6 on the gateway server. Anybody can be a gateway that has enough features.

-- 13 September 2026

If an existing mesh tool already does this, it is used.

> Maybe there's something like that we should just be using already anyway, like a tailnet mesh, like internet propagation and domain name resolution of your own choosing type thing that already exists and that I'm wasting my time trying to emulate.

-- 24 September 2026

Cables follow one rule. The built-in port faces upstream and USB faces downstream. A machine with sharing turned on shares its internet to any USB network device plugged into it. Nothing else is coded.

> The built-in port is for upstream, and the USB is for downstream. We just reuse that pattern, and no matter how we plug things in, that's how I would want it to work, right? Kind of statelessly.

-- 22 September 2026

> All that needs to happen is for nodes that have the USB Ethernet sharing turned on. Whenever a network device comes up on USB, it shares internet onto it and allows Yexto [sic] traffic to go through. That's it. Everything else is situational and has nothing to do with what the code should do.

-- 1 October 2026

You want your own Wi-Fi, from Prometheus. A machine turns its access point on when its cable actually gives internet. Every device logs in with its own certificate.

> I'd rather use Prometheus's Wi-Fi.

-- 29 September 2026

> Yeah, I think turning it on and off automatically when we get detected, not just when you detect a cable, but when the cable is giving us internet access and logging with certificates. Yes, certificates are what I want

-- 24 September 2026

Heavy transfers take the shortest path: Prometheus straight to Zeus.

> It's just Prometheus to Zeus for the transfers. You would want to build on Prometheus anyway, and then get all the files going from Prometheus to Zeus directly.

-- 26 September 2026

### How a change is built

Builds run on Prometheus. If it is unreachable, the build runs locally.

> We should prioritize using [Nix] builds for everything.

-- 25 September 2026

> Well when the builder isn't reachable we just build locally.

-- 24 September 2026

### How a change is deployed

Lojix is the one way to deploy.

> The interface is lojix and meta-lojix CLI only.

-- between 14 and 19 August 2026

"Deploy" means deploy, with no second question. It always includes your user environment. Whatever is merged and not yet deployed gets deployed by whoever finds it.

> well lets talk later where it should be recorded but dont ask again. If I say deploy just deploy it

-- 19 August 2026

> Well, I want the user's environment to be up to date and refreshed. Whenever I say deploy, I always want that.

-- 6 September 2026

> You can deploy home whenever. If something isn't home that means it needs to be deployed and if it's not deployed that means somebody forgot to do their job. Just do their job for them and deploy.

-- 29 September 2026

After a user environment is deployed, the operating system is redeployed too, so a reboot cannot bring back an older one.

> After a user is deployed, we need to redeploy the entire operating system so that, if there's a reboot, the user environment isn't replaced with an older version.

-- 7 September 2026

Explaining comes before updating someone else's machine, but it never holds the update back.

> I want to update host zeus in my cluster. see if you can explain what that looks like first.

-- 22 August 2026

> So me asking the machine to update Zeus for days isn't enough to convey my intention that I want it to be updated? You're still asking me if that's what I want?

-- 28 September 2026

### The order of deployment

Work starts on the machine the flow runs on. Then it is tested in a sandbox. Once you call it usable, it goes to the rest of the network, and it keeps being redeployed after that.

> We're working on the host that we're on. This is where we're going to deploy

-- 19 September 2026

> We can go from proof of concept to testing in a sandbox to deploying on anything that has enough vision right now.

-- 15 September 2026

> I want to start doing constant redeployment when I declare the environment that we're testing to be usable, right? Then we can deploy `main` on the rest of the network.

-- 26 September 2026

Proposed: the order is Ouranos, then Prometheus, then Zeus last, because Zeus is the stable machine. Each machine finishes before the next one starts.

### Retry

A deployment you ordered keeps going until it lands. The fix that unblocks it must hold the next time too.

> Right now I want you to not stop until Zeus has been updated and the same with Prometheus.

-- 26 September 2026

> Make sure you don't make this a fix that only works once.

-- 28 September 2026

Proposed: a retry is one command that names the failed deployment and runs it again exactly as it was, with no request rebuilt by hand.

### What a deployment records

Every running service can be traced back to the source that built it.

> They're built and installed from CriomOS so you can check the source that built that generation.

-- 24 September 2026

You get a deployment report.

> Anyway I'm really still wondering where my deployment report is or where my deployment is.

-- 3 October 2026

Problems that block updates come to you as a book.

> Let's bring up the problems that are blocking updates from going smoothly and send them to Psyche to make a book for me to see.

-- 26 September 2026

Proposed: each deployment record keeps the machine, the source version, the input it was given, the route it was sent by, the result, the new generation, and the generation it can roll back to. The report is written from that record.

### How a change is rolled back

A big change comes with an automatic countdown. If the network and remote access come back on the new version, the countdown is cancelled. If they don't, the machine returns to the old version.

> If you do anything major, have an automatic countdown rollback on some of these really big, potentially breaking things so that we can recover potentially.

-- 15 September 2026

> Elegantly and in a non-breaking way, fix the deploy with the fixes, without breaking anything, without making me lose my remote access, for example, or crashing the network

-- 15 September 2026

When nothing working exists to return to, the change rolls forward.

> There's no rolling back because if we roll back we fall off the cliff.

-- 24 September 2026

### What is never done to a machine

No hot fixes. A fix goes through the user environment or a full redeploy.

> dont do hot fixes

-- 19 August 2026

> use the nix user env only, or OS redeploy

-- 19 August 2026

Nothing stateful and nothing tuned by hand. Any stateful exception is yours to approve.

> I don't want stateful stuff. I want declarative features and then the [nodes] use the features and the behavior is predictable.

-- 1 October 2026

> I need to be captain of any stateful hack basically.

-- 1 October 2026

No fix is written for one person or one machine.

> nothing in this should hardwire bird or zeus anywhere

-- 9 August 2026

You are never asked to type at a machine. A machine can be rebooted over the network, and its startup screen can be seen without a monitor.

> You need a way to reboot it from LAN and then I need a way to see the BIOS without a monitor.

-- 24 September 2026

### What is monitored and how it is shown

Monitoring costs little, gathers a lot, and shows it as pictures. It covers CPU, memory and disk on every machine, and it raises alerts.

> I want to know what the best system is for monitoring in terms of low overhead and getting lots of useful data that can maybe be visualized. It should have some interesting UI for visualizing how the cluster is behaving, what kind of CPU usage, memory usage, disk usage, that kind of stuff, like cluster monitoring, alerts, and things like that.

-- 3 October 2026

Proposed: one light collector on each machine feeds one dashboard on Prometheus, with history graphs. Alerts on full disks, unreachable machines and failed deployments reach you through the messenger.

## Part 2. What exists today

Seen today on Ouranos: Home deployment 83 is recorded in Lojix as succeeded. Generation 1045 is the active Home generation. Generation 1039 is still kept, ready to roll back to. The Lojix service is running, and deployments go through it.

Earlier attempts today failed partway and were redone by hand. Lojix has no retry command: its only owner requests are deploy, pin, unpin, retire and test. A deployment's record keeps the source version and the outcome, but not the input file or the route it was sent by, so the request has to be rebuilt to try again. No deployment report is written from the record.

Ouranos runs no monitoring, no alerts and no countdown rollback. Its builds go to Prometheus. The cable from Prometheus to Zeus has a link, but internet on Zeus is not proven.

## Part 3. Questions

1. Should every deployment record keep its input and route, so a retry is one command that names the failed deployment? Answer yes.
2. How many minutes should the countdown run before a big change rolls itself back? Answer with a number.
3. Once a change is called usable, should it go to Ouranos first, then Prometheus, then Zeus last? Answer yes.
4. Should alerts for full disks, unreachable machines and failed deployments reach your phone through the messenger? Answer yes.
