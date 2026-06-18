# 138/4 — Track D: the cross-machine quorum guard is NOT a bug (no change made)

*The honesty constraint working as intended: the agent investigated, found the
claim wrong, and **refused to "fix" a correct invariant into a regression.** No
code changed; criome main untouched (commit `068f9db`). This also **retracts
report 137 §7 item 3**, which had reported this as a correctness bug.*

## What report 685 (Woe-3) claimed

That a quorum-majority check (around `language.rs:578` and `:414`) compares with
`>` against the full member count, where a fork-safe cross-machine majority needs
`k > n/2` — and prescribed that rewrite.

## What the code actually does

Both named sites are **admission-time well-formedness guards on a caller-declared
m-of-n threshold**, not majority computations:

- `Threshold::validate_shape` (`language.rs:414`): `required == 0 || required >
  self.members().len()`
- `AttestedMoment::rejection_reason` (`language.rs:578`): `required == 0 ||
  required > authorities.len()`

`required` is the value of the `required_signatures` field
(`RequiredSignatureThreshold`) that the **contract author** sets on `Threshold` /
`AttestedMomentProposition` (`signal-criome` schema:137-140, 171-175). It is the
**`m` of an m-of-n policy**, not a tally of collected signatures. So `required >
members().len()` means `m > n` (demands more signatures than members exist =
unsatisfiable); with `required == 0` it is the textbook `0 < m ≤ n` validity
guard.

The **actual quorum-satisfaction test** is a different comparison: `satisfied >=
required` (`language.rs:387`, `:602`) — distinct admitted-signer count must meet
the declared `m`. Using `>=` against the author's declared threshold is correct
for m-of-n. The test `threshold_contract_accepts_only_enough_distinct_admitted_authorities`
(`tests/language.rs:269`) builds an explicit 2-of-3 and asserts 1 sig rejected /
2 authorized. The strings `majority` / `n/2` / `half` appear **nowhere** in
`src/` or `tests/`.

## Why a `> n/2` rewrite would be a regression

It would silently override the author's declared threshold: a legitimate
`required=1` "any-one-of-named-delegates" contract would be forced up to 2, and a
`required=n` unanimity contract forced below `n`. criome's model is explicitly
**configurable m-of-n** (`ARCHITECTURE.md:535-543`: "weighted thresholds, m-of-n
with veto").

## Disposition

- **The general threshold evaluator (`:414`) needs no change.** Report 137 §7
  item 3 is retracted (corrected in 137).
- When the future cross-machine head loop genuinely wants fork-safe majority, the
  head-loop *object contract* expresses it by **setting `required = floor(n/2)+1`**
  over the `n` head-authorities — no change to the (correct) general `:414`
  evaluator.

## Reconciliation with designer handoff 688 (2026-06-18) — there ARE two sites

The designer's handoff (688) said the `k > n/2` guard (their Woe-3) IS needed and
operator-endorsed. On re-reading the code, **both positions are right because they
name different sites** — see report 139:

- **`language.rs:414` `Threshold::validate_shape`** (general m-of-n) — stays
  caller-declared. My finding above holds; do NOT add a majority guard here.
- **`language.rs:578` `AttestedMoment::rejection_reason`** (the time-attestation /
  head-quorum path) — *this* is where the majority guard belongs. A decentralized
  quorum clock (`ay3y`) and quorum-backed objects (`m0p2`) must not be
  single-node-attestable, so this path should require `required >
  authorities.len()/2`. My 138/4 was wrong only in lumping `:578` in with `:414`
  as "no change needed." The `n=1` single-machine self-quorum (`9s52`) still passes
  (`1 > 0`). The scoped fix is being built on branch
  `attested-moment-majority-guard-139` (Track H) — the danger it guards against is
  someone applying the majority clause to `:414` instead.
