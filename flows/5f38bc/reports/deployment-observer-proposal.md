# Passive deployment observer proposal

## Purpose

Provide durable, reviewable deployment evidence for Zeus, Prometheus, and Ouranos without creating another deploy controller. This is a proposal only.

## Existing evidence and ingress

Lojix already has typed deployment admission and terminal records. The observed deployment 29 record contains a deployment identifier, requested target/action, terminal stage, activation path, exit code, and an empty error field; it does not contain the failing command, stderr, target service outcome, or reliable wall-clock chronology. [Deployment 29 causal diagnosis, 2026-09-26](../504461/reports/deployment-29-cause.md) therefore supports consuming existing Lojix deployment/event records, not inferring causality when fields are absent.

The Sep. 26 preflight shows strict SSH transport to Zeus and Prometheus, current and booted generation identities, and historical records on Prometheus but no active Zeus row. [Preflight, 2026-09-26](../b7da5d/receipts/deployment-preflight-2026-09-26.md) It is a point-in-time witness, not a current-state feed.

The deployment-38 reconciliation found no retained self-switch unit. [Reconciliation, 2026-09-26](../b7da5d/reports/deployment38-reconcile-2026-09-26.md) This proposal does not replace that missing mechanism.

The living's current deployment direction is: once the tested environment is declared usable, deploy `main` to the rest of the network. [Vision, 2026-09-26](../e167d8/vision/deployment.md) The declaration remains an external input, not an observer decision.

## Proposed append-only record

For every observed deployment, append an evidence record outside mutable checkouts containing:

- request identity, target host, requested action, immutable source revision and locked-input digest;
- selected output/closure, build execution host, builder result, and materialization reference;
- state transitions: requested, admitted, building, built, activation requested, activated, booted-generation matched, each Home user generation verified, declared service/downstream checks verified, or unverified;
- bounded diagnostics: Lojix record/event identifiers, activation log references, unit status references, and redacted command-output references;
- collection time and observer version.

A status projection may say `unverified`; it must not turn missing logs into success, failure cause, or a retry instruction.

## Passive behavior

The observer may query existing Lojix records and read existing generation, journal, and service evidence. It may write append-only records and send a status to the current Psyche route. It cannot submit deploys, execute arbitrary commands, retry, reboot, change configuration, alter a registry, or initiate a native seat.

Example failure report: `deployment=29; admitted=true; terminal=Failed/Activate; activate_exit=1; failing_command=unavailable; stderr=unavailable; Flow environment panic=separate time-correlated service observation; causality=unproved; next=review durable diagnostics before an explicit new request.`

Example success report: `deployment=<id>; immutable_source=<sha>; closure=<store path>; build_host=Prometheus; host_generation=current=booted; home_users={name:generation}; declared_checks={service:pass,...}; evidence_refs=[...].`

## Location and downstream scope

The current bounded research did not establish an authored geographic-location to timezone/theme/warmth consumer chain or a live proof of those consumer values. Network topology must not be substituted for this missing geographical source chain. Location fields should therefore remain optional/unverified until their authoritative source and consumers are named.

## Decisions for living approval

1. The exact declaration object or authority that marks an environment usable for network-wide `main` rollout.
2. Required per-host and per-user activation proofs, including Zeus users.
3. Required downstream/service checks per host role.
4. Authoritative geographic-location source and permitted theme/warmth consumers.
5. Retention, access, and redaction policy for append-only diagnostics.

## Clarified non-authority boundary

The observer does **not** run SSH, `systemctl`, test commands, builds, timers, or native seats. It consumes supplied producer receipts and existing durable Lojix records only. A missing producer receipt is `unknown`, never a probe trigger. Its only writes are append-only observer evidence/outbox records and status delivery.

Its source fields are deliberately split into `requested_source` and `observed_installed_source`; generation fields are split into `activated_current_generation` and `booted_generation`. A mismatch is reported without action. Exact Lojix streaming ingress is unverified in this evidence set; the initial design may ingest retained records/receipts, and requires a separate contract decision before any subscription API is assumed.

Default approval position: no automatic retry, reboot, deploy, configuration mutation, registry mutation, or local execution authority; status delivery only after a verified recipient route exists.
