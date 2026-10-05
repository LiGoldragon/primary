# Context build contract

Governing sources: [The anatomy 3](../../edf227/books/the-anatomy-3.md) and
[Curriculum: the context standard](../../edf227/books/curriculum-the-context-standard.md).

## Current contract status

The books specify authored Ethos shapes for `ModuleType`, `Module`, `Selection`,
`Placement`, `Placed`, `Role`, `RoleConfiguration`, Registry, ordinary launch,
and meta registration/configuration. They are the required target. The current
Flow generator has only an Operation root; the four context roots and their
cross-root generated-module integration remain proposed and uncompiled until
`ethos-zero Check` and generation prove the exact import/module layout. Do not
fabricate a wire before that proof.

The known signal-flow boundary is separate: `BindingRefusal` is carried by
`StartRejection.BindingRefused` in the existing signal root. Flow consumer
integration remains blocked by incompatible meta-signal-flow/native signal
pins; this contract does not authorize an adapter workaround.

Curriculum may parse the manifest now. Its Flow meta integration waits for the
checked Registry/registration contract.

## Increments and acceptance

1. **Four context roots.** Check and generate fully commented Library, Memory,
   ordinary Signal, and meta Signal roots. Acceptance: each authored root is
   accepted by ethos-zero and its generated Rust is fresh.
2. **Registry.** Implement durable Registry and exact Register/Forget handling.
   Acceptance: same type/name registration and removal semantics survive restart.
3. **Role configuration.** Implement Configure and ordered RoleConfiguration,
   including the Psyche.Primary example. Acceptance: selection and placement
   order round-trip and unknown role/module refuses.
4. **Launch.** Implement Launch.Role resolution, deterministic prompt
   composition, session and hook path, and typed Bind. Acceptance: configured
   role yields one real first-turn path while preserving existing first-turn
   constraints.
5. **Curriculum.** Implement manifest to meta registration and same-registry
   loadable trees/agent definitions. Acceptance: one manifest produces
   registration plus both trees/definitions without hand editing.
6. **Configured-role witness.** Field launches one real configured role.
   Acceptance: the Flow launch evidence and Curriculum output agree.

Dependencies are 1 → 2 → 3 → 4. Increment 5 may parse the manifest now, but
wire integration follows 1 and 2. Increment 6 integrates 4 and 5.

## Ownership

Living allocation supersedes the earlier division: Mind Astra dea0ba owns the
authored design shapes only. Opus 28d847 owns generation, implementation, and
tests for all six increments, including the four-root integration and the
Curriculum compiler/manifest slice. Field 42265e is the witness seat; db38f8 is
publisher only. The signal-flow Bind owner keeps its existing
`BindingRefusal` vocabulary and does not overlap this contract.

No implementation was started in the Flow source by dea0ba. The concrete
hand-off is this report plus the governing books; the context-root import and
generation layout remains proposed until Opus proves it with the current
generator.
