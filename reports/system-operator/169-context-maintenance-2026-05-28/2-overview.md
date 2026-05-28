# Overview

System-operator context-maintenance pass following
`reports/system-designer/44-cross-lane-context-maintenance-2026-05-28/6-overview.md`.

## What Dropped

The pass retired fifteen stale reports:

- `3` — external video notes, not active system-operator state.
- `4`, `5`, `6` — old NOTA reports absorbed by workspace NOTA guidance and
  the schema-derived stack intent.
- `7` — old persona-spirit deployment event log superseded by current Spirit
  production wiring and `skills/spirit-cli.md`.
- `156`, `157`, `158`, `159`, `160` — cloud foundation reports forwarded into
  the cloud lanes. Current destinations are `cloud-designer/4` and
  `cloud-operator/9` / `cloud-operator/10`; `cloud-designer/4` explicitly
  mined `system-operator/156-160`.
- `161` — DJI mic keepalive report superseded by `166`.
- `162`, `163`, `165` — Lojix / Horizon / CriomOS rewrite reports superseded
  by the schema-next re-grounding in `system-designer/40`, `system-designer/42`,
  and `system-operator/167`.
- `164` — broad production-vision report forwarded into `system-designer/40`,
  `cloud-operator/11`, `system-operator/167`, and `system-designer/42`.

## What Stayed

The lane now keeps:

- `1` and `2` — old STT / Persona speech reports. These remain until their
  durable-first Whisrs and transcription-boundary substance is migrated into
  Whisrs or CriomOS-home docs.
- `139` — Arca architecture. This remains until its `/arca`, locator, digest,
  and `signal-arca` substance migrates into Arca docs.
- `166` — current DJI mic profile-churn fix.
- `167` — current Horizon pure-schema concept prototype.
- `168` — current Spirit signal-surface bad-pattern audit.
- `169/` — this context-maintenance meta-report.

## Current Production Spirit Work

The interrupted production Spirit work is still active and should resume next:

- `signal-persona-spirit` is pushed at `b222fb98`.
- `persona-spirit` has passing Cargo tests and still needs `nix flake check`,
  commit, and push.
- `CriomOS-home` still needs the production Spirit input repin and HomeOnly
  activation.
- `skills/spirit-cli.md` still needs a scoped primary commit after the live
  surface is deployed.

## Result

`reports/system-operator/` is back under the soft cap without dropping the
current Spirit, Horizon, DJI, STT, or Arca work surfaces.

