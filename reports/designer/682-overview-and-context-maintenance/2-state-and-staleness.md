# 682 · State and staleness — landed / designed / open + the SO struct-syntax fix

Grounding subagent pass. All commits fetched 2026-06-18.

## 1 · Landed on main

### criome (`/git/github.com/LiGoldragon/criome`, origin/main)

```
4250cbb criome: use interest-bearing authorized object tokens
b9bc29f criome: add classified authorized object pulse POC
255660a criome: document contract-programmed time pulses
0cf326c criome: publish authorized object update references
3c05122 criome: persist policy contracts and stamp quorum signatures
5cf4087 criome: repair stale scope-discipline references
```

Confirmed: real BLS (`blst = "0.3"`, daemon described as "Spartan
BLS-signature authentication and attestation daemon"); persisted policy
contracts with stamped quorum signatures (`3c05122`); content-addressed
contracts via `ContractDigest`; the reference-only pulse — criome
publishes `AuthorizedObjectUpdate` *references* (`0cf326c`), not payloads;
interest-bearing tokens (`4250cbb`) so the daemon matches `token.interest`
and retracts per `(subscriber, interest)`.

### signal-criome (origin/main)

```
e33ea04 signal-criome: bind authorized object interest into stream token
f779f02 signal-criome: document classified object pulses
4ea7319 signal-criome: add subscriber-filtered object pulse POC
346df58 signal-criome: witness authorized object pulse contract
caad934 signal-criome: add authorized object update pulse
9d8ea38 signal-criome: stamp quorum signature surfaces
```

Confirmed reference-only pulse in `schema/lib.schema`:
`ObserveAuthorizedObjects … opens AuthorizedObjectUpdateStream`,
`AuthorizedObjectUpdate { object AuthorizedObjectReference … }`,
`AuthorizedObjectUpdateToken { subscriber interest }`,
`AuthorizedObjectKind [Operation Contract Agreement Time]`. The
attested-moment / contract-programmed time pulse is present (`Time` kind +
`255660a`). The persisted criome-contract SEMA family and quorum surfaces
are in the contract.

## 2 · The SO struct-syntax fix — already landed on schema-next main

This is the headline correction to the operator-416 assumption. The
positional dot-differentiator struct syntax is **not** still epic-branch
only; SO landed it on `schema-next` **main** on 2026-06-18:

```
95f1ee7 schema-next: reject redundant explicit field roles      (13:14)
af3705c schema-next: reject retired struct field pair syntax     (11:18)
```

`af3705c` removes the `FieldPairs` mode from both front doors
(`src/source.rs`, `src/declarative.rs`), adds
`SchemaError::RetiredStructFieldSyntax`, and migrates schema-next's own
schemas (`core.schema`, `root.schema`, `spirit-min.schema`) + all fixtures
to positional form (`CoreSchema { BuiltinMacroPositions … }`,
`MacroPatternDelimited { delimiter.MacroDelimiter MacroPatternObjects }`).
`95f1ee7` adds `RedundantExplicitFieldRole` — closing the Spirit `i3p0`
caveat: `topic.Topic` is now rejected (use `Topic`).

What SO is landing: the positional struct body (bare type → derived field
name; `key.TypeReference` dot differentiator for an explicit role) as the
**only** accepted form on main, with both retired forms (`field Type`
name-value, `Type *` star) rejected loudly.

**Resolves the 681 validation caveat.** Operator 416 line 71 said "build
against the validated name-value form, not the structural-forms branch,
because the positional form is not buildable on main." That caveat is now
void: as of `af3705c` the positional form *is* main, and the name-value
form *fails to parse* on main. signal-standard and any new contract must
be authored in positional form. Designer 681's canonical positional sketch
is now the buildable one.

## 3 · Designed but unbuilt

- **signal-standard (681):** the cross-component vocabulary library
  (`ComponentKind`, `AuthorizedObjectKind`, `Differentiator`,
  `*Interest`, `AuthorizedObjectReference`, `ComponentClassification`).
  Not created. Migration of `signal-persona::ComponentPrincipal` and the
  third roster `signal-message::ComponentName` (System-Designer 134) still
  pending.
- **Interest in AuthorizedObjectUpdateToken / Fork A live fan-out:** token
  type and local criome matching landed; router `Attend`/`Retract` + a
  durable attendance table keyed by the standard interest coordinate are
  unbuilt.
- **Adjudicator ladder beyond escalate-to-psyche:** designed (677/680),
  only escalate-to-psyche exists.
- **Multi-node self-quorum:** designed, single-node only in practice.
- **Live cluster + cluster-root admission-signing ceremony:** designed,
  not stood up.

## 4 · Staleness flags

- **`skills/structural-forms.md` is now stale against main.** Line 47 attributes positional syntax to "Spirit `adnn`" as forward design and line 154 points the code at "(epic branch `next/structural-forms`)". As of `af3705c`/`95f1ee7` the syntax is **landed on schema-next main**; the skill should drop the epic-branch qualifier and add the `RedundantExplicitFieldRole` reject (`i3p0`). The skills.nota index entry is fine.
- **signal-criome main still uses name-value struct bodies** (`ComponentObjectInterest { component ComponentKind kind AuthorizedObjectKind }`, `AuthorizedObjectUpdateToken { subscriber Identity interest … }`). It landed 13:00, ~2h after `af3705c` made that form un-parseable on schema-next main. The criome contract repos are now stale against schema-next main and need a positional-form migration + regenerate — a real, trackable coordinated break.
- **No obuf slips** in designer 674-681 (clean). **No Telos-as-agreement-machine mislabel:** 677/678/680 consistently frame *criome* as the agreement machine and *Telos* as the meta-project, grounded in Spirit `pviw`/`p3td`/`m0p2`. The `/tmp/telos-poc` crate (680) is correctly flagged throwaway/committed-nowhere.
