# Mentci introspection/Criome epic start — frame and dispatch

## Psyche directive captured

The 2026-06-21 psyche prompt starts a new Mentci-centered implementation arc. Speech-to-text spellings in the prompt are normalised here:

- **Menchie / Menchi / Mencie** → **Mentci**.
- The authorization/agreement component is **Criome**. Any earlier alternate transcription was a speech-to-text or agent spelling error.

## Durable substance to carry forward

- Mentci **writing mode** and **meta mode** are the same practical mode. Outside it, Mentci is primarily observation/light-operation mode, while still able to talk to systems such as message.
- Mentci is no longer just a sandbox proof: deploy the current test Mentci as an available surface and begin using it for component observation, debugging, approval, and integration.
- Mentci must follow the operating system theme. Prefer system-wide light/dark GUI configuration; if the toolkit/app needs explicit configuration, provide a light and dark Mentci theme derived from the system themes.
- Revive and update the `introspect` component and the optional tracing path. The target is schema-defined trace events flowing to introspect, with Mentci querying/filtering behavior by component type, message type, and schema-derived signal input/output shape.
- Schema-generated CLI help should be on main and then plugged into Mentci/Mentci-lib so component object types and signal interfaces can be explored programmatically rather than by hand-written help.
- Mentci-lib is the async engine layer below the GUI: an actor system that can host Nexus and SEMA planes and be embedded by different clients, not just the current egui binary.
- Spirit should integrate with Criome first through a localhost one-of-one / auto-approve contract that mirrors the current “any authorized key has full access” behavior, then grow into a cluster where one-of-any is enough but every node’s approval behavior can be logged and compared.
- Maintainer’s role in this arc is continuous production audit: what is live, what is on main, what is actually merged, and what is safe to deploy.
- Treat this as an epic boundary: “beginning of working with Mentci” as the observation/debugging/approval console for components and the cluster.

## Spirit gate result

The prompt was durable and record-worthy. Existing Spirit records already covered several arrows, and the guardian rejected duplicates/clarification-needed records. One new record landed:

- `jwm9` — Mentci-lib as the asynchronous engine layer with actor system, Nexus/SEMA room, and portable GUI/client embedding.

Relevant existing records surfaced by the guardian include:

- `cx2m` — canonical spellings: `criome`, `criomos`, `mentci`.
- `7x5z` — Mentci as first-class component triad and Criome-facing approval client.
- `xlrk` — Mentci-egui ordinary observation/light-operation mode plus root-like meta/write mode.
- `80bl` — Mentci querying introspect for component behavior by component type, message type, and schema-derived signal input/output shape.
- `mu0o` — current Mentci stack moves from sandbox-only proof toward available deployed test surface.
- `p43g` / `pviw` — Criome key custody, authorization, quorum, auto-approve/bootstrap, and Mentci approval-client role.

## Dispatch method

Per psyche instruction, this is being fanned out with parallel subagents. The parent remains available to the psyche; child outputs land in this report directory. The fanout is read/planning/audit first, not concurrent writing into code repos.
