Presentation.{ «The cluster and deployment» }

The three machines, how they reach each other, how a change is built, deployed and undone, and how the cluster is watched. Say "yes" to a number to land it; for two texts, name the number.

**1. What Ouranos and Prometheus are for**
Kind: vision. Module: cluster. Action: create.
> Ouranos is the laptop he sits at; it is spared heavy work and keeps no AI model, ever. Prometheus is the builder, the only home for AI models, and provides the services; it can only be built on itself. Builds run on Prometheus; if it is unreachable they run locally.

Rests on: 25 and 26 Sep, 15 Sep, 24 Sep.

**2. Zeus is stable**
Kind: vision. Module: cluster. Action: edit.
> Zeus is where his partner works. It is a stable machine, and nothing is tested on it.

Rests on: 8 Aug, 19 Sep.

**3. The cable rule**
Kind: vision. Module: cluster. Action: edit.
> The built-in port faces upstream and USB faces downstream. A machine with sharing turned on shares its internet to any USB network device plugged into it. Nothing else is coded.

Rests on: 22 Sep, 1 Oct.

**4. The access point turns itself on**
Kind: vision. Module: cluster. Action: edit.
> A machine turns its access point on when its cable actually gives internet, and every device logs in with its own certificate. The automatic rule replaces the admin switch.

Rests on: 24 Sep, 22 Sep.

**5. Deploy means deploy**
Kind: intent. Module: lojix. Action: edit.
> When he says deploy, deploy, with no second question, and always include his user environment. Whatever is merged and not yet deployed is deployed by whoever finds it. After a user environment, redeploy the operating system so a reboot cannot bring back an older one.

Rests on: 19 Aug, 6 Sep, 29 Sep, 7 Sep.

**6. Explaining never holds the update**
Kind: intent. Module: lojix. Action: edit.
> An explanation of an update to another machine is sent with the deployment and never holds it back.

Rests on: 22 Aug, 28 Sep.

**7. The order of deployment**
Kind: intent. Module: lojix. Action: edit.
> Once he calls a change usable, it goes to Ouranos first, then Prometheus, then Zeus last. Each machine finishes before the next starts.

Rests on: 26 Sep. The order is proposed.

**8. Retry is one command**
Kind: intent. Module: lojix. Action: edit.
> A deployment he ordered keeps going until it lands. A retry is one command that names the failed deployment and runs it again exactly as it was. The fix that unblocks it must hold the next time too.

Rests on: 26 Sep, 28 Sep.

**9. What a deployment records**
Kind: knowledge. Module: lojix. Action: edit.
> Each deployment record keeps the machine, source version, input, route, result, new generation and the generation it can roll back to. The deployment report is written from it.

Rests on: 3 Oct, 24 Sep. The fields are proposed.

**10. Rollback or roll forward**
Kind: intent. Module: breaking-upgrades. Action: edit.
> A big change comes with an automatic countdown of [N] minutes. If the network and remote access come back on the new version, the countdown is cancelled; if not, the machine returns to the old one. When no working version exists to return to, the change rolls forward.

Rests on: 15 Sep, 24 Sep. Give N.

**11. Never done to a machine**
Kind: intent. Module: operating-system. Action: edit.
> No hot fixes: a fix goes through the user environment or a full redeploy. Nothing stateful or tuned by hand; any stateful exception is his to approve. No fix is written for one person or one machine.

Rests on: 19 Aug, 1 Oct, 9 Aug.

**12. Monitoring**
Kind: vision. Module: cluster. Action: edit.
> One light collector on each machine feeds one dashboard on Prometheus with history graphs of CPU, memory and disk. Alerts on full disks, unreachable machines and failed deployments reach his phone through the messenger.

Rests on: 3 Oct. The collector and dashboard are proposed.
