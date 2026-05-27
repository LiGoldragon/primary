# 1 · Spirit substance — cloud topic records

*Sub-agent A's findings. Filed by orchestrator because the Explore
subagent type is read-only; substance below is the subagent's
verbatim recap, not orchestrator synthesis.*

Records: 17 total on the `cloud` topic. All classified.

## Identity and purpose

The cloud component is a planned triad (daemon + working signal +
owner signal) that owns cloud-provider API management [281]. Its
raison d'être is to serve as the home for provider API
machinery, initially focused on Cloudflare but architected to
eventually accommodate Google Cloud and cloud hosters such as
Hetzner [296]. The psyche has established this as a foundational
service within the persona-spirit architecture for managing
external cloud resources.

## Scope — current ground and projected expansion

**Current ground.** Cloudflare DNS and redirect rules are
established as the first concrete cloud target [282, 680]. The
first daemon target is to manage Cloudflare DNS records and
similar Cloudflare-managed resources [685]. This represents the
initial production slice — modest but focused, narrowing down
the sprawling concept of "cloud provider APIs" to a concrete,
deliverable MVP [294].

**Projected expansion.** The component is architected for growth
toward Google Cloud and cloud hosting providers like Hetzner
[296], though these remain future targets. Build-time opt-ins
mean providers can be added without forcing all consumers to
handle all integrations [283, 342].

## Settled design decisions

The cloud component will be organized as a three-part triad with
Cloudflare DNS, Cloudflare settings, and redirect rules as
first-generation targets [294]. Cloud plan preparation belongs
on the owner signal surface rather than the working surface
[325]. Provider integrations are build-selectable, with
capability observation explicitly distinguishing
built-but-unconfigured providers from providers not compiled
into the daemon at all [342] — this rules out silent failures and
improves debuggability.

For Cloudflare credentials, the pattern is environment-variable
population via password-manager tooling (the existing FEMOS
utility pattern) [682]. The implementation will prefer Cloudflare
CLI over direct HTTP API for the first integration, if
operationally simpler [688]. The first daemon runs
almost-stateless, maintaining only a volatile in-memory cache of
last-known Cloudflare state; persistent storage is deferred
until the state justifies it [687]. First cloud cache is
runtime/volatile, with acceptable cache loss, since Cloudflare
remains the source of truth [681].

Notably, the production push is prioritized: the MVP deliberately
skips the new schema-engine approach to ship faster [684].

## Open questions and clarifications

Authentication is flagged as requiring investigation — the current
environment-variable pattern is recognized as a starting point
but safer alternatives should be explored during detailed design
[682]. The signal language is intentionally kept small and typed
initially [683], suggesting some expansion anticipated but
deferred. The cloud daemon's eventual self-upgrade capability is
mentioned as "possible when support is cheaply available" [284,
295], but conditions and mechanisms remain undefined.

## Constraints

One production constraint is already documented: the cloud
component production slice uses the old Rust signal macro path
[679], a technical debt inherited from the current architecture
but acknowledged as a blocking-magnitude issue for production
deployment.
