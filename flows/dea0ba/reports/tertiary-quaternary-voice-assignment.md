# Tertiary and Quaternary voice disposition

## Settled and selected configuration

The living's 2026-10-05 order limits these layers to Psyche and Mind:

> We'd like the tertiary and quaternary seats to be up and there should be no
> fields on it. That's a mistake.

The current Fable record preserves Field 42265e's relay of that order at
[voices](../../8475a9/vision/datom.md). No Field Tertiary or Field Quaternary
voice may be started.

The living's directly relayed clarification is: “All I said was the model for
the tertiary is Luna Medium and Sonnet Medium.” It is retained in
`flows/bad807/log.md` and independently summarized in `flows/aa887c/log.md`.
The authored `knowledge-layer-models` table carries the same Tertiary and
Quaternary model/effort rows. The Quaternary ruling remains Claude Sonnet low
and Codex Luna low.

Astra's operational stack allocation selects one harness per voice. It is a
designer selection to minimize the first additive launch set; it is not an
additional attributed living ruling.

| Voice | Harness | Model family | Effort | Behavioral power | Source/status |
|---|---|---|---|---|---|
| Psyche.Tertiary | Claude | Sonnet | Medium | Unassigned | Living model/effort ruling; Astra selects Claude. |
| Mind.Tertiary | Codex | Luna | Medium | Unassigned | Living model/effort ruling; Astra selects Codex. |
| Psyche.Quaternary | Claude | Sonnet | Low | Unassigned | Living Quaternary ruling; Astra selects Claude. |
| Mind.Quaternary | Codex | Luna | Low | Unassigned | Living Quaternary ruling; Astra selects Codex. |

“Low” and “Medium” here are harness effort settings. They are not a typed Flow
`PowerLevel`, and no behavioral-power value is inferred or required to launch
these additive voices. The old three-by-four voice table is nonbinding.

## Smallest Field implementation disposition

Use the existing native **main-launcher** route for four fresh additive seats.
Do not use `Replace`, `Restart`, predecessor close, routing release, or a
predecessor message. Each seat needs an exact new layer registration and a
separate native identity/readiness receipt; it must not take or rewrite an
existing binding.

The current Claude launcher already accepts `--model` and `--effort`, so it can
receive the two selected Claude model families at the settled effort after Field
chooses an exact supported native model identifier from the display/client map.
The current Codex launcher accepts `--model` but hardcodes
`model_reasoning_effort="medium"` and verifies medium in its rollout. That is
correct for Mind.Tertiary but would silently mislaunch Mind.Quaternary.

The smallest required Field change is localized to that launcher:

1. accept `--effort low|medium` with the current medium default;
2. put the selected value into the Codex harness command; and
3. verify the native turn context against the requested value instead of a
   literal medium.

No typed Flow `PowerLevel` addition, layer-wide model default, or new launcher
is required for this launch. A layer-aware registration/configuration record is
still required to name each new voice exactly; current shared launcher titles
and client selection use aspect/model and do not themselves persist `Layer`.
That record must be added without changing existing registrations.

Startup context must be one compact, versioned pointer to the configured role
and generated skills, plus the task-only brief. Do not reuse the six-slash
command producer or paste a duplicate large corpus. The configured role remains
the durable place for standing instructions.

## One-time verification and boundary

For each launch, Field verifies once: requested versus observed native model and
effort, exact new native identity, exact layer registration, generated skill
input availability, and one readiness receipt. A failed or ambiguous result is
returned as a supported-route receipt; it is not retried here.

Current source supports a richer successor route through fresh `Start` inside
`Replace`, but that is intentionally out of scope. The existing native Claude
refresh helper is bootstrap-only and explicitly does not retire, replace, or
reroute a predecessor. Neither mechanism is used for this additive launch.

No launch, registration, retirement, or predecessor contact was performed by
this design flow. Field 42265e is authorized to implement and launch the
bounded configuration above.
