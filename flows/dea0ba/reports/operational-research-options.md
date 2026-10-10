# Operational research options

Delegated research for Psyche Fable, 2026-10-03. This is a choice record,
not an implementation or an authorization to read accounts, install software,
or create a messaging identity.

## 1. Subscription allowance across harnesses

### 1. Event-triggered local allowance ledger — recommended

Use a small non-LLM collector only when a harness already emits a meaningful
event: a completed turn, an idle transition, a failure, or a hook notification.
The collector calls a harness-specific **read surface** where one exists,
appends a timestamped snapshot, and produces a view of remaining percentage,
reset time, and pace. It performs no check while every harness is idle.

Each snapshot needs its source and units: provider, opaque subscription/limit
identity, harness, window duration, reset time, observed time, and either
`official_allowance` or `estimate`. A provider-reported used/remaining value
and reset time are allowance facts. Token counters, transcript size, elapsed
window pace, and model-cost arithmetic are estimates; none can be subtracted
from an allowance percentage.

The local prior record establishes this distinction. A prior Codex
`account/rateLimits/read` response had percentage, a 10,080-minute window,
reset time, and available resets, while `account/usage/read` separately had
daily token buckets. The prior Claude investigation found no CLI quota/status
command; its statusline saw rate-limit data but discarded it. That statusline
shape is local implementation evidence, not a stable vendor contract.

Claude Code provides command/HTTP hooks without an LLM on `Stop`,
`StopFailure`, `Notification`, `PostToolBatch`, `SessionEnd`, and other
lifecycle events, including a `rate_limit` failure matcher. Its documented
events make it a suitable trigger, but do not themselves promise a remaining
allowance field. [Claude Code hooks](https://code.claude.com/docs/en/hooks)
documents the event boundary. Codex needs the same adapter pattern only when
its installed version exposes a trusted local event or hook surface.

The collector's authority boundary is narrow: a Codex adapter may read only a
local, read-only account endpoint; a Claude adapter may record an explicit
limit notice or supported export. Access tokens, Unix socket paths, browser
cookies, and prompt content stay outside the ledger. A missing reading is
`unknown`, never zero. Views may compare pace to the earlier 14%/day idea, but
that is a desired comparison line, not an allowance fact or adopted policy.

OpenAI directs a ChatGPT-plan user to Settings, the usage dashboard, or
Codex `/status` for the exhausted allowance, balance, and displayed reset
time; it also says consumption depends on the model, task complexity, context,
reasoning, speed, and tools. [OpenAI: Codex plan usage](https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan)
Anthropic likewise says Claude usage varies with conversation length and
complexity, feature use, model, and effort. [Anthropic: usage limits](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work)

### 2. Explicit human snapshot, carried honestly

Record a user-authorized reading from a provider dashboard or limit notice on
the next harness event, including its observation time and age. This preserves
an official number when no supported programmatic reader exists, especially
for Claude, but it is not an automatic check and it becomes stale. It must not
be displayed as live allowance.

Claude documents that plan usage is shared across Claude surfaces and Claude
Code and that a reset can restore a five-hour or weekly limit, but those pages
do not document a stable programmatic remaining-percentage interface.
[Claude Code limits](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code)
[Claude resets](https://support.claude.com/en/articles/17007452-what-is-a-limit-reset)

### 3. API-budget lane, separate from subscriptions

For an API-key harness, capture the documented response limit headers and
provider billing/cost data per request. This can be authoritative for an API
project's request/token budget, but it is not evidence of a ChatGPT or Claude
subscription allowance. OpenAI documents organization/project API limits and
response headers separately. [OpenAI API rate limits](https://developers.openai.com/api/docs/guides/rate-limits)

## 2. Cluster CPU, RAM, and disk monitoring

### 1. Self-hosted Netdata Agent per node, with an optional Parent — recommended

Netdata has the fastest path to useful visual monitoring: automatic host CPU,
memory, filesystem and disk-I/O charts, application/process groups, and
prebuilt alerts. A local dashboard works per node; children can stream to a
central Parent for a cluster view. The Parent and dashboard form the metrics
and access boundary; notification-receiver credentials are a separate outbound
boundary. Linux installation requires root, so each node agent should be
treated as privileged host observability software.

Vendor-published sizing, not a measurement on this cluster, is 1–5% of one
CPU core, 100–200 MB RAM on an empty system, 250–350 MB in typical
production, and about 4 GiB default local disk. [Netdata resource use](https://learn.netdata.cloud/docs/netdata-agent/resource-utilization/)
For a streaming child, Netdata publishes 2–10% of one core, 100–300 MiB, and
under 1 Mbps, with local metric storage avoidable. [Netdata sizing](https://learn.netdata.cloud/docs/welcome-to-netdata/enterprise-evaluation-guide)
Its `ram` database mode can avoid local metric disk I/O but loses retained
history after restart. [Netdata retention modes](https://learn.netdata.cloud/docs/netdata-agent/resource-utilization/disk-%26-retention)

This is continuous system-metric collection. That is appropriate for health
alerts and is distinct from the no-idle-polling rule for subscription checks.

### 2. Self-hosted Beszel Hub and agents, after a local overhead measurement

Beszel is a smaller-focused dashboard choice with historical host and Docker
statistics and configurable CPU, memory, disk, bandwidth, temperature, load,
and status alerts. [Beszel project overview](https://gh.beszel.dev/henrygd/beszel/blob/main/readme.md)
It also exposes basic systemd service state, CPU, and memory. [Beszel systemd](https://beszel.dev/guide/systemd)
Its extra-disk-usage cache can reduce disk wake-ups. [Beszel environment variables](https://beszel.dev/guide/environment-variables)

The Hub owns stored history, browser access, and alert routing; agents need
host visibility and communicate with it by WebSocket or SSH. Some systemd or
container views need privileged access. The project calls itself lightweight,
but this research found no primary-source CPU, RAM, or disk-overhead figure.
That makes a short, identical-workload measurement against Netdata necessary
before claiming it is lower overhead.

### 3. Prometheus node_exporter, Prometheus, Grafana, and Alertmanager

This is the most configurable and familiar self-hosted stack: exporters expose
host metrics, Prometheus retains and queries them, Grafana supplies dashboards,
and Alertmanager routes alerts. node_exporter exposes host metrics including
CPU counters. [Prometheus node_exporter guide](https://prometheus.io/docs/guides/node-exporter/)

It needs periodic scraping, a restricted exporter network boundary, Grafana
authentication, Alertmanager receiver credentials, and conscious retention and
cardinality choices. No single primary-source aggregate overhead figure was
found; measure the selected scrape interval, labels, and retention. Earlier
local work names a machine `Prometheus` and investigates its network/build
role, but did not establish a deployed metrics stack that can safely be
assumed here.

## 3. A separate machine account that notifies the living

### 1. Self-hosted ntfy for one-way operational notices — recommended first

Create separate identities: a machine publisher with write permission only on
one private topic, and the living's reader with read permission only. ntfy's
ACL supports user/admin roles and per-topic read/write permissions.
[ntfy access control](https://docs.ntfy.sh/config/?h=access)
The publisher sends a short HTTP notification, so it fits event-triggered
alerts from the allowance ledger or monitoring system. It is not a command
channel: replies, transcript content, secrets, and shell execution stay out
of scope until a separate authenticated ingress is designed.

The mobile clients are available for Android, iOS, F-Droid, and app stores.
[ntfy overview](https://docs.ntfy.sh/)
Phone type decides a material limit: Android can retain an instant-delivery
foreground connection to a self-hosted server, whereas iOS instant delivery
with ntfy's stock app requires forwarding poll requests through ntfy.sh or
running a custom app/push infrastructure. [ntfy phone delivery](https://docs.ntfy.sh/subscribe/phone/)
[ntfy iOS configuration](https://docs.ntfy.sh/config/?h=access)

### 2. Self-hosted Matrix with Element for a two-way secure conversation

Give the machine and living separate Matrix accounts and one private encrypted
room. Element provides iOS and Android clients, account/device verification,
and end-to-end encrypted messaging on self-hosted Matrix. [Element user guide](https://element.io/user-guide)
[Element self-hosting](https://element.io/built-on-matrix)

This is the stronger option if the living must reply from the same channel.
The machine bridge must hold only its own account/device credentials, and a
reply gateway must accept a tiny typed command set with explicit review; it
must never translate arbitrary chat into terminal commands. It carries more
server, encryption-key, backup, and client-support work than ntfy.

Stock Element mobile apps use Element's push gateway to reach Apple/Google
push services. A wholly owned push path requires a custom push gateway and a
custom-signed app, so self-hosting the homeserver alone is not the same as
fully self-hosted phone notifications. [Element push boundary](https://docs.element.io/latest/element-server-suite-classic/advanced-configuration/notifications-mdm-push-gateway/)

### 3. SimpleX as a privacy-forward future investigation

SimpleX SMP relays can be self-hosted and mobile clients can be configured to
use them. [SimpleX SMP server guide](https://github.com/simplex-chat/simplex-chat/blob/stable/docs/SERVER.md)
Its per-contact routing design does not naturally give the requested durable,
separate machine account, and this research found no official maintained
automation interface suitable for a machine sender. It is therefore a future
privacy candidate, not the simple initial choice.

## Local sources

- `flows/9fb0ad/vision/quotaTracking.md`
- `flows/9fb0ad/vision/clusterMonitoring.md`
- `flows/9fb0ad/vision/contactingTheLiving.md`
- `flows/6cc91b/vision/quotas.md`
- `flows/6cc91b/vision/notifications.md`
- `flows/5f4fea/reports/quota-accounting.md`
- `flows/692df8/reports/quotaVisualization.md`
- `flows/7328f4/vision/hooks.md`
- `flows/7328f4/vision/polling.md`

