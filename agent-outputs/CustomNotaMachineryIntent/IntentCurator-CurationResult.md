# Custom NOTA Machinery Intent Curation Result

## Task And Scope

Curate the psyche-authorized direction that components must not implement custom
NOTA parsing, encoding, decoding, or hand-decoded command shapes when canonical
NOTA/schema/contract machinery is available. The work was scoped as durable and
public, not Mind-specific, and did not inspect Mind implementation.

## Consulted

- `AGENTS.md`
- `ARCHITECTURE.md`
- `.agents/skills/intent-log/SKILL.md`
- `.agents/skills/intent-maintenance/SKILL.md`
- `.agents/skills/intent-manifestation/SKILL.md`
- `.agents/skills/spirit-cli/SKILL.md`
- `.agents/skills/spirit-query/SKILL.md`
- `.agents/skills/edit-coordination/SKILL.md`
- `.agents/skills/architecture-editor/SKILL.md`
- `.agents/skills/repo-intent/SKILL.md`
- Spirit public searches for `custom NOTA`, `custom encoding decoding`,
  `canonical NOTA machinery`, `hand decoded command shapes`, `nota`, `codec`,
  `parsing`, `hand-decoded`, and `schema derived`.

## Spirit Outcome

This was not recorded as a new Spirit record and no existing record was
maintained.

Relevant existing public record:

- `w312`: general principle that deterministic routing, dispatch, lookup,
  classification, projection, and address resolution belong in code or
  schema-derived machinery, not agent judgment.

Operations:

- `PublicTextSearch` found no direct existing record for custom NOTA codecs,
  parsing, or hand-decoded command shapes.
- A first `Record` attempt was rejected by the NOTA parser because the request
  had an extra tuple delimiter; no record was created.
- The corrected `Record` attempt returned `GuardianRejected (Matter ...)`.
  The guardian classified the NOTA-specific rule as data-format mechanism
  matter and directed it to architecture documentation or the NOTA
  specification instead of Spirit. The rejection also identified `w312` as
  nearby general intent.

Exact blocker for Spirit capture:

```text
GuardianRejected Matter: The rule is scoped to NOTA parsing and handling,
making it a policy specific to that data format mechanism. The directive is
welded to NOTA matter; the clean general principle of preferring canonical
machinery can be recaptured without coupling to NOTA. Record this in the
architecture documentation or NOTA specification instead of Spirit.
```

## Manifestation

Changed `ARCHITECTURE.md` under `Wire and identity discipline`.

Added the constraint that components do not implement custom NOTA parsers,
encoders, decoders, or hand-decoded command shapes when canonical NOTA schema,
generated codec, or contract machinery can express the shape. The wording also
preserves the psyche clarification that NOTA itself remains the allowed text
data format for authored and projection surfaces; the rejected pattern is
application-specific parsing or malformed command structure leaking through
NOTA instead of being fixed in schema or contract.

This is a narrow architecture manifestation of the task's psyche statement and
the guardian's routing decision, with `w312` remaining the only Spirit-level
general canonical-machinery record observed.

## Validation

- `orchestrate "(Observe Roles)"` showed no claim on `/home/li/primary`.
- Claimed `/home/li/primary/ARCHITECTURE.md` and
  `/home/li/primary/agent-outputs/CustomNotaMachineryIntent` under
  `IntentCurator`.
- `rg -n "Canonical NOTA machinery only|custom NOTA|hand-decoded|application-specific parsing|w312" ARCHITECTURE.md agent-outputs/CustomNotaMachineryIntent`
  confirmed the new architecture wording.
- `nl -ba ARCHITECTURE.md | sed -n '195,222p'` confirmed placement under
  `Wire and identity discipline`.
- `jj diff --stat` showed only `ARCHITECTURE.md` before this output file was
  created.

## Follow-Up For Mind Implementation Worker

Use `ARCHITECTURE.md` as the durable guidance source. In Mind, remove or replace
custom NOTA parsing, encoding, decoding, and hand-decoded command shapes when a
canonical NOTA schema, generated codec, or typed contract can express the data.
Do not treat this as a rejection of NOTA; NOTA remains valid for authored input,
diagnostics, tests, and human-readable projections.
