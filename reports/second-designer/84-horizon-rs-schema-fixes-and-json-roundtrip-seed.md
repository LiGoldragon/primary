# 84 — horizon-rs schema fixes and JSON round-trip seed

*Three fixes land on horizon-rs `horizon-re-engineering`. The `System`
enum now emits Nix's dashed system tuple on the wire; `KnownModel`
recognises every model string the goldragon datom uses (tiger,
prometheus, balboa); and the `view::*` codec acquires the JSON
round-trip discipline that audit/83 found missing. Twenty-nine new
tests pass, the project pipeline still parses `datom.nota`
end-to-end, and the bookmark is at the FIX 3 commit on origin.*

---

## TL;DR

Three coherent fixes landed on `horizon-re-engineering` across
horizon-rs and goldragon: per-variant `serde(rename)` on `System`
so JSON consumers see `"x86_64-linux"`/`"aarch64-linux"`;
`KnownModel` expanded with `ThinkPadE15Gen2Intel`, `GmktecEvoX2`,
and `Rock64` (with `ComputerIs` flags) plus the datom rewrites
that switch balboa's `rock64` and prometheus's `"GMKtec EVO-X2"`
to closed-enum tokens; and a `view::*` JSON round-trip test seed
covering every consumer-facing record. Twenty-nine new tests pass
(6 system, 17 view, 4 extra name, 2 thinkpad/non-thinkpad flag);
three pre-existing failures (`metal_arch_unresolvable_when_no_arch_set`,
`node_proposal_size_zero_decodes_via_renamed_variant`,
`nordvpn_profile_decodes_from_nota_record`) survive and are *not*
mine — they were red before FIX 1 and remain red. Four commits
pushed: three on `horizon-rs`, one on `goldragon`. Branch tip on
both remotes is the FIX 3 commit / datom-rewrite commit
respectively.

---

## §1 — System serde fix

**Change (`lib/src/species.rs`):** per-variant `#[serde(rename =
...)]` on the two-variant `System` enum so each variant carries
its Nix system-tuple shape on the JSON path.

Before — JSON form was the PascalCase Rust identifier; consumers in
CriomOS / CriomOS-home that read `inputs.horizon` see a value
that no Nix idiom recognises as a system tuple:

```jsonc
{ "system": "X86_64Linux" }    // wrong
```

After — JSON renders the Nix-shaped tuple every consumer already
expects (Nix's own builtins, `nixpkgs.legacyPackages.<system>`,
`buildMachines.<n>.system`, etc.):

```jsonc
{ "system": "x86_64-linux" }   // right
```

`#[serde(rename_all = "kebab-case")]` does **not** produce this
shape — it would emit `"x86-64-linux"` (dash where the underscore
belongs). Per-variant rename is the only correct form. The
`NotaEnum` derive is unaffected: it inspects the Rust identifier,
not the serde attribute set; the workspace already mixes
`#[serde(rename = "...")]` with `NotaEnum` (`WlanBand` is the
witness in `lib/src/proposal/router.rs`).

**Witness (`lib/tests/system_json_roundtrip.rs`):** six tests —
two serialise-to-value, two parse-from-value, two full
serialise-then-parse round-trips — one pair per variant. The
file is a fresh dev-dep on `serde_json` (added to `lib/Cargo.toml`
via `[dev-dependencies] serde_json = { workspace = true }`); the
workspace already declared `serde_json` at the workspace level so
no `Cargo.toml` ripple beyond the dev-dep alias.

End-to-end witness lives in `lib/tests/view_json_roundtrip.rs`
under `horizon_end_to_end_node_system_renders_as_nix_system_tuple`
— project a small `ClusterProposal`, serialise the resulting
`view::Horizon`, read `horizon.node.system`, assert
`"x86_64-linux"`. The fix is now witnessed both at the type level
and through the full projection pipeline.

---

## §2 — KnownModel expansion

**Change (`lib/src/species.rs`):** `KnownModel` gains three
variants — `ThinkPadE15Gen2Intel`, `GmktecEvoX2`, `Rock64`. The
`is_thinkpad` predicate gains the `ThinkPadE15Gen2Intel` case
(Gmktec and Rock64 explicitly do not gate `is_thinkpad`).

**Change (`lib/src/name.rs`):** `ModelName::known()` learns the
three new strings — `"ThinkPadE15Gen2Intel"`, `"GmktecEvoX2"`,
`"Rock64"`. The existing `"rpi3B"` (lower-r) is left alone for
back-compat; new model variants use the closed-enum PascalCase
convention from system-assistant/15 §"Closed design decisions"
#6 (closed-enum variants are PascalCase no spaces; `"GMKtec
EVO-X2"` becomes `GmktecEvoX2`).

**Change (`lib/src/view/node.rs`):** `ComputerIs` gains
`thinkpad_e15_gen2_intel`, `gmktec_evo_x2`, `rock64`. The
`from_model` mapping populates them. Nix consumers can now gate
on `horizon.node.computerIs.gmktecEvoX2 = true;` and friends.

**Datom rewrite (`goldragon/datom.nota`):**

| Node       | Before                | After          |
|------------|-----------------------|----------------|
| balboa     | `rock64`              | `Rock64`       |
| prometheus | `"GMKtec EVO-X2"`     | `GmktecEvoX2`  |
| tiger      | `ThinkPadE15Gen2Intel`| *(unchanged)*  |

Tiger's record was already in the closed-enum spelling. The two
strings that change drop the quoted-with-space form (`"GMKtec
EVO-X2"`) and the lowercase form (`rock64`) for the PascalCase
closed-enum identifiers that `ModelName::known()` recognises.

**End-to-end witness:** built `horizon-cli` and ran it against
the updated datom for both viewpoints. Balboa renders
`computerIs.rock64 = true`; prometheus renders
`computerIs.gmktecEvoX2 = true`. Pre-fix both fell through to
`None` and every `computerIs.*` flag was false. The fix is
visible end-to-end from datom string → typed `KnownModel` →
projection → JSON wire field.

**Test additions (`lib/tests/name.rs`):** the existing
`model_name_known_returns_typed_known_model` test now asserts
all three new strings parse to their typed variants; two new
tests pin `ThinkPadE15Gen2Intel.is_thinkpad()` and
`!GmktecEvoX2.is_thinkpad() && !Rock64.is_thinkpad()`.

---

## §3 — JSON round-trip test seed

**New file (`lib/tests/view_json_roundtrip.rs`):** seventeen
tests, one per top-level `view::*` record kind plus an
end-to-end horizon round-trip. The discipline is
`skills/contract-repo.md` §"Examples-first round-trip
discipline" applied to the view side of horizon's wire surface.

**Coverage matrix (one test per record):**

| Record                         | Witnesses |
|--------------------------------|-----------|
| `view::NixCache`               | round-trip + camelCase keys |
| `view::LidSwitchAction`        | lowercase string shape + RT for all three variants |
| `view::Machine`                | RT with all optional fields populated + camelCase keys |
| `view::Io`                     | RT + camelCase keys |
| `view::BehavesAs`              | RT + camelCase keys (`nextGen`, `lowPower`, `bareMetal`, `virtualMachine`, `largeAi`) |
| `view::TypeIs`                 | RT + camelCase keys (`edgeTesting`, `largeAi`, `largeAiRouter`, `mediaBroadcast`, `routerTesting`) |
| `view::ComputerIs` (known)     | RT + every camelCase model flag present including the three new ones |
| `view::ComputerIs` (unknown)   | RT + every flag asserts false when `model = None` |
| `view::BuilderConfig`          | byte-stable RT + camelCase keys (`hostName`, `sshUser`, `sshKey`, `supportedFeatures`, `system`, `maxJobs`, `publicHostKey`, `publicHostKeyLine`) |
| `view::ProjectedNodeView`      | RT + camelCase keys (`ramGb`) |
| `view::Cluster`                | byte-stable RT + camelCase keys (`trustedBuildPubKeys`, `aiProviders`, `vpnProfiles`) |
| `view::User`                   | byte-stable RT + camelCase keys (`hasPubKey`, `emailAddress`, `matrixId`, `useColemak`, `useFastRepeat`, `isMultimediaDev`, `isCodeDev`, `preferredEditor`, `textSize`, `sshPubKeys`, `extraGroups`, `enableLinger`, `githubId`) |
| `view::Node` (no viewpoint fields) | byte-stable RT + every camelCase always-derived key + all viewpoint-only `Option` fields **absent** from JSON when `None` |
| `view::Node` (viewpoint populated) | byte-stable RT + the nine viewpoint-only keys (`io`, `useColemak`, `computerIs`, `builderConfigs`, `cacheUrls`, `exNodesSshPubKeys`, `dispatchersSshPubKeys`, `adminSshPubKeys`, `wireguardUntrustedProxies`) all present |
| `view::AtLeast` (size/trust)   | RT + camelCase keys |
| `view::Horizon` (end-to-end)   | project a 2-node cluster → serialise → parse → re-serialise → byte-equal; top-level keys (`cluster`, `node`, `exNodes`, `users`, `containedNodes`) all camelCase |
| `view::System` end-to-end      | full horizon projection shows `node.system == "x86_64-linux"` (FIX 1 surfacing through the pipeline) |

**Discipline notes:**

- **Byte-stable round-trip on larger records.** `Cluster`, `User`,
  `Node`, `BuilderConfig`, `Horizon` use `to_vec → from_slice →
  to_vec` and `assert_eq!(bytes, bytes_again)`. A field-by-field
  `PartialEq` would not catch a codec asymmetry where the second
  serialisation reorders or drops a field; the byte-stable form
  does. This is the discipline shape audit/83 calls for.
- **`skip_serializing_if = "Option::is_none"` enforcement.** The
  `view::Node` test in its absent-fields shape explicitly asserts
  that every viewpoint-only optional field is *not* present in
  the JSON object. A regression that drops `skip_serializing_if`
  would surface `null`-valued fields at every ex-node — bloating
  every Nix consumer's view — and the test would fail loudly.
- **camelCase keys asserted, not just present.** Each record-
  level test names the camelCase keys consumers depend on. A
  regression that changes `criomeDomainName` to `criome_domain_name`
  on the wire is one of the failure modes audit/83 worried about
  most; the per-record key assertions catch it.

**Records not in scope of FIX 3:** the closed sub-enums on the
proposal side (`NodeSpecies`, `NodeServices`, `RouterInterfaces`,
`NodePlacement`, etc.) — these surface inside `view::Node` and
are round-tripped via the `Node` byte-stable test, but each does
not yet have its own per-record JSON round-trip witness. Open
follow-up.

---

## §4 — Commits pushed

| Repo            | Branch                  | Commit subject |
|-----------------|-------------------------|----------------|
| horizon-rs      | horizon-re-engineering  | System: per-variant serde rename to Nix system-tuple shape + JSON round-trip witness |
| horizon-rs      | horizon-re-engineering  | KnownModel: add ThinkPadE15Gen2Intel, GmktecEvoX2, Rock64 + ComputerIs flags for Nix consumers |
| horizon-rs      | horizon-re-engineering  | tests: seed JSON round-trip witnesses for every view::* record (closes audit/83 view-side codec gap) |
| goldragon       | horizon-re-engineering  | datom: rewrite balboa rock64 and prometheus "GMKtec EVO-X2" to closed-enum forms (Rock64, GmktecEvoX2) |

A peer agent's `cluster: project secret_bindings into view as
BTreeMap<SecretName, SecretBackend>` commit landed between
FIX 1 and FIX 2 in the horizon-rs branch (visible in `jj log`).
That work is not mine and was already in the working copy when
this task started; the FIX 2 commit reaches it through `jj`'s
rebase semantics and depends on it (the peer's commit added the
new `Cluster.secret_bindings` field, which FIX 3's `Cluster`
fixture had to populate with an empty `BTreeMap` to compile).

---

## §5 — Verification

`cargo test --jobs 1 --no-fail-fast -p horizon-lib -- --test-threads=1`
from
`/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-re-engineering`.

Result summary:

```
194 tests passed across 22 test files
3 tests failed (all pre-existing, not introduced by this work)
```

The three pre-existing failures:

| File                       | Test name                                                | Failure shape |
|----------------------------|----------------------------------------------------------|---------------|
| `lib/tests/node.rs:281`    | `metal_arch_unresolvable_when_no_arch_set`               | `error.to_string().contains("no architecture")` — the error message text drifted; the typed error is still raised |
| `lib/tests/proposal.rs:165`| `node_proposal_size_zero_decodes_via_renamed_variant`    | Nota-codec decode panic; unrelated to JSON path |
| `lib/tests/vpn.rs:58`      | `nordvpn_profile_decodes_from_nota_record`               | Nota-codec decode panic; unrelated to JSON path |

All three were red on the parent commit `lsyvmoqy f38be592`
(`cluster: add public_domain field; user.rs reads it for
email/matrix`) before FIX 1 landed. Recorded here so the next
agent inherits the same baseline and doesn't blame the green
tests added in this work.

End-to-end witness: built `horizon-cli`, ran it against
`/home/li/wt/github.com/LiGoldragon/goldragon/horizon-re-engineering/datom.nota`
for two viewpoints (prometheus, balboa). Output JSON:

- `cluster.node.system` reads `"x86_64-linux"` for prometheus,
  `"aarch64-linux"` for balboa (FIX 1 surfaces through projection).
- `cluster.node.computerIs.gmktecEvoX2 = true` for prometheus
  (FIX 2 — model `"GMKtec EVO-X2"` now resolves via
  `KnownModel::GmktecEvoX2`).
- `cluster.node.computerIs.rock64 = true` for balboa (FIX 2 —
  model `rock64` now resolves via `KnownModel::Rock64`).

The datom parses cleanly via `Decoder::new` →
`ClusterProposal::decode`; projection succeeds without error.

---

## §6 — Open follow-ups

These surfaced during the work but are out of FIX 1–3 scope.
Each is a *finding*, not a blocker.

**Pre-existing test failures.** Three failures in
`lib/tests/node.rs`, `lib/tests/proposal.rs`, and
`lib/tests/vpn.rs` predate FIX 1 and reproduce on the parent
commit. The first is a string-match drift (`"no architecture"`
no longer appears verbatim in the error). The other two are
nota-codec decode failures — likely a derive-vs-codec drift on
the proposal side that landed in an earlier commit. Worth a
separate audit pass.

**Pre-existing dead-code warnings.** `lib/tests/tailnet.rs`
warns on unused `UserName` and `UserProposal` imports;
`lib/tests/ai.rs` warns on unused `AiModelFetchurl`. Small;
not mine; flagged here for the next agent in the area.

**Per-record proposal-side round-trips.** Closed sub-enums on
the proposal side (`NodeSpecies`, `RouterInterfaces`,
`NodePlacement`, `TailnetControllerRole`, `VpnProfile`, etc.)
participate in the `view::Node` byte-stable round-trip but
have no per-record JSON round-trip witness of their own. The
audit/83 systemic finding is closed for the *top-level* view
records this report adds; tightening it to every record kind
that surfaces in JSON is the next discipline step.

**`view::Machine` shape mirrors `proposal::Machine`.** The
view's `Machine` is shape-equivalent to the proposal's today
— the `From<proposal::Machine>` impl is the constructor. As
the arc lands data-bearing variants in later steps (per
`view/machine.rs` doc-comment), the duplication will diverge.
Until then, two types per concept lurks as a smell; not
urgent to resolve.

**`rock64` vs `Rock64` migration.** Some downstream consumers
of `inputs.horizon` may still gate on the old
`computerIs.rock64` field name — that field still emits
correctly, so no consumer breaks. But any old Nix code that
parsed the raw model string (`builders.${node.machine.model}`,
say) and matched the lowercase form will silently miss after
this fix. Sweep CriomOS modules for raw model-string matches
and switch them to `computerIs.*` flags — outside this work's
scope but a known consequence.

**ARCH document update.** `horizon-rs/ARCHITECTURE.md` does not
yet name the dashed-tuple wire shape for `System` as a
commitment. When the architecture pass reaches that doc,
inline the rule per `skills/reporting.md` §"What gets
absorbed, not kept" so the report can retire.

---

*End report 84.*
