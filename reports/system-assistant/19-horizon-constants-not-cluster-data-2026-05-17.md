# 19 — Horizon constants don't belong on the cluster-author boundary

*System-assistant report on a structural smell the user surfaced
during peer review of /18. `ClusterProposal.domain` and
`ClusterProposal.public_domain` carry values that are facts about
the Horizon, not facts about any cluster within it. The smell is a
category, not a one-off: `tailnet.baseDomain` carries it too. This
report names the category, the affected fields, the question of
where horizon constants ought to live, and the open question of
whether the wrapping newtypes still earn their place once their
values are fixed.*

> **Status (2026-05-17):** Design observation, no code edits.
> Pairs with `reports/system-specialist/132-horizon-domain-constants-not-cluster-data.md`,
> which prescribes the operator-side fix (drop the two fields,
> add `ClusterDomain::criome()` / `PublicDomain::criome_net()`
> constructors, scrub goldragon's datom tail). This report works
> the designer-side question — what *kind* of thing was being
> smuggled across the wrong boundary, and which other fields
> show the same smell.

## 0 · The user's observation

> *"there shouldn't be criome and criome.net in cluster data — those
> are horizon constants"* — Li, 2026-05-17.

`ClusterProposal` is the schema every cluster owner authors
against. By the proposal/view distinction in
`horizon-rs/ARCHITECTURE.md` (the leaner-shape version), the
proposal carries **facts about this cluster**; the view carries
**facts derived during projection**. A field whose value is a
constant of the Horizon — the same string for every cluster that
will ever exist on this stack — does not belong on the proposal
boundary at all. It's leakage from the projector into the schema
the cluster author edits.

The two named instances:

- `ClusterProposal.domain: ClusterDomain` — currently `"criome"`
  on goldragon. Used as the internal-DNS suffix in
  `<node>.<cluster>.<domain>`.
- `ClusterProposal.public_domain: PublicDomain` — currently
  `"criome.net"` on goldragon. Used as the suffix in
  `<user>@<cluster>.<public_domain>` and
  `@<user>:<cluster>.<public_domain>`.

Both values are the same across every cluster Li operates today
and every cluster the Horizon shape envisions tomorrow. They are
not cluster facts — they are horizon facts.

## 1 · The category — horizon constant vs cluster data

The decision rule that should sit on every proposal field:

> *"Will another cluster owner using this same Horizon ever
> author a different value here?"*

If the answer is *no*, the field is a horizon constant. It belongs
in horizon-rs itself (as a constant, an associated function, a
small policy record), not on the proposal-side boundary.

If the answer is *yes*, the field is cluster data. It stays on
the proposal, validated by the newtype, authored in the cluster's
datom.

If the answer is *"only as transition debt during a migration"*
— that's a real third case, but it earns explicit naming as such
(per ESSENCE §"Today and eventually"). It does not get to wear
the same field shape as genuine cluster data.

Today's two fields fail the test in the negative direction: every
cluster using CriomOS authors `"criome"` and `"criome.net"`, and
the schema would be improved by the cluster *not* being able to
author anything else.

## 2 · Other suspects

A grep for "domain"-shaped or "horizon"-shaped fields in the
current proposal surface, with the test applied:

| Field | Current type | Today's value(s) | Horizon-constant? |
|---|---|---|---|
| `ClusterProposal.domain` | `ClusterDomain` | `"criome"` | **Yes** — leak. |
| `ClusterProposal.public_domain` | `PublicDomain` | `"criome.net"` | **Yes** — leak. |
| `ClusterProposal.tailnet.base_domain` | `DomainName` | `"tailnet.goldragon.criome"` | **Probably yes, after a rename** — the suffix is `<service>.<cluster>.<internal-domain>`; the cluster only really chooses the `<service>` slug. Smuggling the whole composed string in is the same smell. |
| `ClusterProposal.lan.cidr` / `gateway` / `dhcp_pool` | `LanCidr` etc. | `10.18.0.0/24`, `10.18.0.1`, … | Ambiguous. The values *can* vary per cluster but in practice every CriomOS deploy uses the same `10.18.0.0/24` shape. Probably real cluster data — different LANs are a real future. |
| `ClusterProposal.resolver.upstream_servers` | `Vec<IpAddress>` | Cloudflare + Quad9 today | Probably real cluster data — resolver choice is a real policy axis. |
| `ClusterProposal.ai_providers` | `Vec<AiProvider>` | per-cluster | Real cluster data. |
| `ClusterProposal.vpn_profiles` | `Vec<VpnProfile>` | per-cluster | Real cluster data. |
| `ClusterProposal.secret_bindings` | `Vec<ClusterSecretBinding>` | per-cluster | Real cluster data. |
| `ClusterTrust.cluster`, `nodes`, `users` | per-cluster magnitudes | per-cluster | Real cluster data. |

Two fields fail the test outright (`domain`, `public_domain`).
One fails after a small reframing (`tailnet.base_domain` carries
the *whole composed* domain, including the horizon constant; the
cluster only owns the leading service slug). The rest are
plausibly real cluster data, with the caveat that "every cluster
happens to use the same value today" doesn't *prove* the field is
horizon-constant — Li may genuinely intend the resolver list to
be cluster-authorable even when today's value is uniform.

This needs the user's read on each ambiguous case, not an
automated rule.

## 3 · The newtype question

`ClusterDomain` is a `string_newtype!` macro instance — a
`String` wrapper with non-empty validation. Once its value is a
fixed horizon constant supplied by `ClusterDomain::criome()`, the
newtype's earned identity changes shape:

- **Before:** the newtype identity says *"this string is a
  cluster's internal-DNS suffix, authored by the cluster owner."*
  The newtype distinguishes it at the type level from
  `ClusterName`, `NodeName`, etc.
- **After (with `::criome()` constructor):** the newtype identity
  says *"this string is the horizon's internal-DNS suffix,
  supplied by horizon-rs."* It has exactly one constructor and
  one value. The newtype is now decorating a constant.

Three plausible shapes for the after-state, in order of weight:

1. **Keep the newtype, add the constructor** (SYS/132's
   prescription). Cheap, minimal churn. The cost is that the
   newtype now reads as a frozen wrapper around a constant —
   a smell the next pass might want to revisit.
2. **Retire the newtype, inline the literal in the projector.**
   `format!("{node}.{cluster}.criome")` literally, inside
   `NodeProposal::project`. The discipline that "internal domain
   is horizon-controlled" lives in the projection function;
   nothing in the type system enforces it because nothing in the
   type system needs to. Saves a type; loses a typed boundary at
   a place where typed boundary is meaningless because the value
   never varies.
3. **Promote the constants to a typed policy record.** A
   `HorizonDomainPolicy { internal_suffix, public_suffix }` value
   defined once in horizon-rs, threaded through projection.
   Earns its place only if the suffixes are likely to grow
   another axis (e.g., "internal" vs "internal-staging"). For
   today's shape, this is over-engineering.

(1) and (2) both work. (1) preserves the type system signal;
(2) is more honest about what the value actually is. The
designer-side question is: *is the newtype identity load-bearing
for any consumer, or is it only load-bearing for the projector?*
If only the projector, (2) is cleaner.

## 4 · Implication for the leaner-shape arc

This is the same class of finding as `TypeIs` / `ComputerIs` in
/17: a wire shape carrying ceremony rather than substance.
There, the ceremony was *enum-shadow structs* — 11 booleans
shadowing the species enum. Here, the ceremony is *cluster
fields carrying constants* — two fields surfaced on the
authoring boundary that the cluster cannot meaningfully change.

The leaner-shape arc has already established the precedent:
break the wire format if the typed shape is wrong. ESSENCE
§"Backward compatibility is not a constraint" applies. The same
mechanism — sibling branch, single-commit phase, downstream
pickup — accommodates this fix cleanly.

Per SYS/132's "Recommendation": *"Treat this as part of the
`horizon-leaner-shape` wire break rather than as a follow-up
compatibility patch."* I agree. The arc is breaking shape
deliberately; this is the same category of correction.

## 5 · Correction to /18

`reports/system-assistant/18-horizon-leaner-shape-downstream-pickup-2026-05-17.md`
§2.4 said:

> *"Goldragon's `datom.nota` on `horizon-re-engineering` does NOT
> carry a `publicDomain` value... add `"criome.net"` at the tail
> of the `ClusterProposal` record."*

That was stale on two counts. The peer review found that the
literal *is* present at `datom.nota:481` (the verification I had
done earlier missed it). And the user's response made the deeper
point — adding the literal is the wrong fix; *removing the field*
is the right one.

So /18 §2.4 should be read as: ignore. SYS/132 supersedes that
section; this report frames its design question.

Other corrections to /18 from the same peer review:

- The CriomOS punch-list misses `checks/nspawn-role-policy/default.nix:19,26`
  (also has `buildCores`). The count "three live files, eight
  references" undercounts.
- The verification command "`horizon-cli project goldragon --viewpoint
  goldragon:prometheus`" is wrong — the binary takes `--cluster` /
  `--node` flags and reads nota from stdin.
- Line numbers for the `metal/default.nix` references were stale:
  `computerIs.rpi3b` is at line 329 (not 277); the lid-switch
  lines are 505–507 (not 453–455).
- Doc drift not fully named: `horizon-rs/skills.md:19`,
  `horizon-rs/lib/src/proposal/ai.rs:4`, and
  `horizon-rs/docs/DESIGN.md:{69, 351, 356, 379, 391}` all still
  refer to `TypeIs` / `ComputerIs` / `computer_is` after Phase A.

These are mechanical fixes to /18. None of them changes the
shape of the arc; all of them widen the pickup scope by a small
amount.

## 6 · Open questions for the user

### Q1 — Land SYS/132's fix as Phase F of horizon-leaner-shape?

The branch already carries Phase A–E. Phase F would:

- Drop `ClusterProposal.domain` and `ClusterProposal.public_domain`.
- Add `ClusterDomain::criome()` and `PublicDomain::criome_net()`
  (or whichever shape from §3 you prefer).
- Thread them through `NodeProjection.cluster_domain` and
  `UserProjection.cluster_public_domain`.
- Drop the trailing `"criome"` and `"criome.net"` from goldragon's
  `datom.nota`.
- Drop the corresponding fields from every test fixture.

Scope: roughly equivalent to Phase C (the typed-newtypes phase) —
a focused half-day. Authorize and I'll land it on the same
branch, run tests, push.

### Q2 — Newtype shape after the fix (§3 above)

Three options. SYS/132 prescribes (1). My designer read leans
(2). Worth a sentence from you before Phase F lands, because the
choice shapes the eventual ARCH text.

### Q3 — `tailnet.base_domain` — same category?

Today's value `"tailnet.goldragon.criome"` includes the cluster
name AND the horizon constant. If the field stays, it's still
authoring horizon facts on the cluster boundary. Two paths:

- (a) Compose the base domain in the projector:
  `<service-slug>.<cluster>.<horizon-internal>` where the
  cluster only authors the service slug (`"tailnet"`).
- (b) Keep `base_domain` as-is, accepting that some cluster
  fields will continue to carry composed values that include
  horizon constants.

Recommendation: (a), as a Phase G after F lands. Same category
of fix; smaller blast radius (single field, fewer consumers).

### Q4 — Other potentially-horizon-constant fields

§2's table flags `lan.*` and `resolver.*` as ambiguous —
"every cluster happens to use the same value today" doesn't
prove they're horizon constants. Worth a read from you on each:
*is this genuinely cluster-authorable, or is it transition debt
toward a horizon-controlled value?*

## 7 · See also

- `reports/system-specialist/132-horizon-domain-constants-not-cluster-data.md`
  — operator-side prescription for the fix this report frames.
  Carries the specific Rust impls, the goldragon edit, the
  verification gates.
- `reports/system-assistant/18-horizon-leaner-shape-downstream-pickup-2026-05-17.md`
  §2.4 — superseded by SYS/132 + this report; mechanical
  corrections in §5 above.
- `reports/system-assistant/17-horizon-rs-overbuild-audit-2026-05-16.md`
  — the parent audit; this finding is the same class as the
  audit's "TypeIs / ComputerIs are enum-shadow structs" finding
  (ceremony where substance is meant to live).
- `~/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape/`
  — the worktree carrying Phase A–E; Phase F would land here
  pending Q1.
- `~/primary/ESSENCE.md` §"Perfect specificity at boundaries"
  — the rule that domain values are types, not primitives. The
  inverse also applies: typed boundaries should carry actual
  cluster-authorable data, not horizon constants dressed up as
  cluster choices.
- `~/primary/ESSENCE.md` §"Today and eventually" — transition
  debt is real, but it earns explicit naming. Horizon constants
  surfacing as cluster fields without that naming is the
  default-bad shape.

*End report 103.*
