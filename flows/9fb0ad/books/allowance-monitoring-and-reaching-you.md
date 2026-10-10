Presentation.{ «Allowance, monitoring, and reaching you» }

Your three requests, researched by Mind Astra; our earlier work on each was found and read first. Nothing is installed or signed up for. Name one number per point.

## 1. Tracking your allowance across harnesses

Your words: "Let's go for a hook-based, push-based check and not a polling-based check because we don't need to check what the quota is if no agent is ever running ... this tool that uses no LLM can do another checkup." -- psyche, typed, 2026-10-03.

A small program with no model in it, run by the harness's own hooks on each event (a turn done, idle, failure), reads each provider's own allowance surface and appends a timestamped reading; official readings and our estimates are kept apart; an idle harness is never checked. Earlier flows wrote the accounting and visualization designs this builds on. Unknown, to be tried first: whether the installed Codex exposes a trustworthy local event or usage surface; Claude Code's hooks are documented.

1. Build it as described, Claude first, Codex when its surface is witnessed.
2. Build it, but trigger only at end of turn, not on every event.
3. Add an API-budget lane too, from response headers, for any key-based harness.

## 2. Watching the cluster

Three candidates: **Netdata** (one agent per node, optional parent for a cluster view; vendor figures 1–5% of one core, 100–350 MB; automatic charts and prebuilt alerts), **Beszel** (lighter in design, host and container history, alerts; no published overhead figure), and the **Prometheus + Grafana** stack (most configurable, most parts). Mind recommends Netdata as the fastest path to a rich visual, with alerts, and a measured Beszel comparison before claiming anything lighter.

4. Netdata now, per node with a parent.
5. Measure Beszel against Netdata on one node first, then choose.
6. Prometheus and Grafana.

## 3. The machine reaching your phone

Your words: "The machine would need to have its own account so that it actually gives me a notification ... I would probably favor something that we can self-host but we don't have to self-host right away." -- psyche, typed, 2026-10-03.

**ntfy**, self-hosted: the machine gets a write-only publishing identity, you a read-only one; a notice is one HTTP call; apps for Android and iOS. One edge: on iPhone, instant delivery needs the notice forwarded through ntfy's public relay or our own push setup; Android delivers directly. **Matrix with Element**: two accounts in one encrypted room, two-way, heavier to run; on a phone the stock app still uses Element's push gateway unless we build our own. Mind recommends ntfy first, one-way, never a command channel.

7. ntfy, self-hosted, one-way notices, the iPhone relay accepted for now.
8. ntfy on the public ntfy.sh first, self-host later.
9. Matrix and Element, two-way, from the start.
