# 417 — Pass-through feedback on Designer 682

Reviewed:

- `reports/designer/682-overview-and-context-maintenance/3-overview.md`
- `reports/system-designer/135-caught-up-*`
- current `schema-next` main
- current `signal-criome` main and lockfile
- Spirit `p3td`, `w2g3`, `2st7`

## Verdict

Designer 682 is mostly right: the major action item is now a coordinated contract migration to current schema syntax before `signal-standard` can land cleanly. The interest-bearing token slice is already landed, and the remaining Fork-A delivery work is router-side.

But the pass-through should include three corrections so the next operator slice does not start from stale framing.

## Corrections / additions

### 1. The schema syntax state is even newer than 682 says

Designer is right that `schema-next` main has moved past name-value struct fields. The old form is retired.

The current head is one commit beyond the two commits Designer named:

- `af3705c7` — rejects retired struct field pair syntax.
- `95f1ee7c` — rejects redundant explicit field roles.
- `1de72dde` — supports explicit structural field roles.

That last commit matters. The current syntax is not just "dot-differentiator"; it is:

- bare type for derived field role: `Entry { Topics Kind Description }`
- dot explicit role for a plain reference: `ImportDeclaration { Name source.TypeReference }`
- parenthesized explicit role for composite references: `Query { (Topics (Vector Topic)) (Limit (Optional Integer)) }`

So the implementation should target current schema-next main's positional/explicit-role grammar, not just the older dot-only mental model.

### 2. signal-criome is stale against schema-next main, but not red under its own lock

The stale-contract finding is real: `signal-criome/schema/lib.schema` still contains old fields such as:

```text
DaemonPath { value String }
CriomeDaemonConfiguration { socket_path DaemonPath ... }
AuthorizedObjectUpdateToken { subscriber Identity interest AuthorizedObjectInterest }
```

Those need migration.

But `cargo test --features nota-text --test round_trip` still passes today because `signal-criome/Cargo.lock` pins:

```text
schema-next     e7216260
schema-rust-next 6e04d70f
```

That predates the strict syntax. So the precise statement is: `signal-criome` is not broken under its current lock, but it will fail as soon as its schema dependencies are refreshed to current main or the stack is built with current local overrides. The migration is still a prerequisite, but the failure mode is dependency-refresh gated.

### 3. Router verbs are now Attend / Withdraw, not Attend / Retract

Designer 682 repeats `Attend` / `Retract`. System-Designer 135 corrected this: `Retract` is one of the forbidden SEMA words, so the router surface should be `Attend` / `Withdraw`.

That should be reflected in any next design/report before implementation.

## The live design question

System-Designer 135 surfaced the actual fork now gating router work:

- router as sole operational matcher: criome emits unfiltered authorized-object references; router holds attendance, matches, and delivers.
- criome keeps an internal observation registry and router also has an attendance table: criome supports direct local observation clients, router owns inter-component delivery.

My lean: router should be the sole operational delivery matcher. Criome may keep its own `ObserveAuthorizedObjects` registry as a criome-local observation surface, but it should not decide which components are affected in the universal fan-out path. That keeps `wckt` clean: criome authenticates and emits references; router transports.

This distinction also makes my existing criome `SubscriptionRegistry` less dangerous: it is acceptable as a local observation stream mechanism, but should not become the cross-component delivery table.

## Intent-maintenance notes

Verified:

- `p3td` is now `Importance VeryLow`, as Designer said.
- `w2g3` still says the envelope design is open.
- `2st7` explicitly settles the envelope design left open by `w2g3`.

I agree with deferring the `w2g3` maintenance if the guardian is likely to reject a quote-less maintenance edit.

The stronger intent hygiene item is now `m0p2` vs `l2ha`: `m0p2` says criome pushes updates to affected components; `l2ha` says router matches subscriptions and fans references out. Once the registry-owner fork is settled, the old phrasing should be clarified or superseded. Do not add a sibling clarification record.

System-Designer also flags that the `ComponentPrincipal` collapse is described as "psyche-decided" in Designer 681 but lacks a Spirit anchor. That should either be captured from the original psyche wording if available, or the reports should stop relying on "psyche-decided" as a durable source.

## Implementation sequence I would use

1. Migrate `signal-criome` to current positional/explicit-role struct syntax and refresh generated Rust.
2. Check `signal-persona` and `signal-message` for the same syntax break; migrate them in the same syntax pass if they are still on name-value fields.
3. Create `signal-standard` in current syntax.
4. Move the differentiator and interest types from `signal-criome` into `signal-standard`.
5. Migrate `signal-criome`, `signal-persona`, and likely `signal-message::ComponentName` onto the shared `ComponentKind`.
6. Then implement router `Attend` / `Withdraw` plus the durable attendance table and reference delivery.
