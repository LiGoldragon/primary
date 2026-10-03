<!-- to-the-living:start -->
Presentation.{ «Quota query: implementation handoff delivered» }

### 1. One component, two provider readers

Extend the existing **Harness** component and its typed `signal-harness` contract. One CLI request gathers Claude and Codex observations and returns one combined snapshot. No new repository is needed.

### 2. What the call returns

For each subscription: plan, every quota window and model limit, remaining percentage, reset time, daily allowance, and variance from the window’s target pace.

For each live session: model, available context measurements, their source, and freshness. Subscription quota stays separate from session context.

### 3. What the numbers mean

Neither provider exposes an absolute token or dollar allowance through the witnessed quota sources. Missing values remain unknown. Transcript-derived context is labeled as a last-request proxy.

Credentials stay inside the program. It does not refresh credentials, launch model sessions, or add idle polling. Historical accounting remains with Persona.

### 4. Implementation handoff delivered

The requirements and native component design are published. Secondary Opus **28d847** is reachable again, and messenger accepted the complete implementation and testing handoff.

The earlier delivery blockage is resolved. Implementation and testing results are still pending; no working command is claimed yet.
<!-- to-the-living:end -->
