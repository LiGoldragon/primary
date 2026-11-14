# Lojix next-version defect: activation stdout omitted

Reported by Mind core Primary on Psyche Primary's request, not independently audited here.

Installed `schema_runtime.rs:7429–7460` performs user SSH activation; `7472–7498` sets the profile then activates. The command runner at `7859–7924` captures stdout and stderr but on a nonzero exit retains trimmed stderr only. Deployment 239's `ActivateFailed` exit 1 therefore lacks its diagnostic stdout.

For the next version: retain both captured streams in failure evidence. No immediate fix or deployment authorized. The colon rollout holder alone is authorized for one separate combined-output diagnostic.

Forwarded to Mind lojix Secondary; Flow accepted delivery 19227 as Queued, not a consumption receipt.
