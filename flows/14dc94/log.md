# Deployment reconciliation

Remembered: 33a4d4 — depth 1

Recovery subflow read the remembered log and last main response (Codex transcript ordinal 2206). They claim Chroma/Home activation completed, while fixed-location/system activation did not. Current-state and Chroma audit subflows independently observed the running static GeoClue source disabled and Chroma SolarClockUnavailable.

Current-source recovery found the old hardware migration resolved in CriomOS 2985c813; vector user consumers and source pins still require reconciliation. Implementation is delegated to isolated Home and system worktrees. Activation is authorized by the current request; reboot is not authorized.

Sources: flows/33a4d4/log.md; /home/li/.codex/sessions/2026/09/11/rollout-2026-09-11T19-55-48-01a0919c-83d8-7113-9274-46633a4d40cf.jsonl; recover, current_state, and chroma_audit subflow evidence in this flow's transcripts.

## Deployment closeout

System reconciliation reports immutable CriomOS 36653a125de8f14518af2dddf89333610891d140 built remotely and typed deployment 4 Completed/Succeeded. Home and Chroma source work is carried in reports/home-reconcile.md; system implementation and deployment evidence are delegated to system_reconcile. The independent chroma_audit subflow returned a passing final runtime observation in its transcript; system_reconcile carries it with provenance in the deployment report. No reboot was performed.

The integration required direct consumption of current Horizon fields, coherent dependency pins, Chroma resume reapplication, and GeoClue Exact requests while preserving the 1 km acceptance rule. The first live activation was partial because the temporary Lojix bridge held the database; the managed service recovered after the bridge stopped, and subsequent typed activations succeeded. Earlier location audit objections from a stale producer checkout were withdrawn; the consumed immutable proposal already carried the intended coordinates.
