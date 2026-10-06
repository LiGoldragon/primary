<!-- to-the-living:start -->
Presentation.{ «Jev proposals and implementation choices» }

# Jev proposals and implementation choices

A private working book of open choices. It records evidence and candidate paths; it does not authorize an implementation.

> **Current state:** no Jev call, key access, package installation, rollout, or default reaping policy has happened. The OpenRouter credential is **missing or inaccessible** from this review's viewpoint; that does not show whether a user key exists.

## 1. First choice: reuse a released direct Decisions client

### Proposal A — evaluate `fuzzy-jev` 0.6.0 as transport only

**Why it is on the table.** The released crates.io artifact was inspected on 2026-10-04. It is MIT-licensed and sends typed requests directly to OpenRouter's documented `POST /api/alpha/decisions` endpoint. It has request validation and checks typed replies against the submitted questions.

**What is known.** Artifact SHA-256: `d1b1a4e0c61e72dea37907c6634315e53f0467ac7adede496181902a4608f84f`. Its embedded source pointer is `6e55c5b8ed527e934efb0b51d322805ae7be2aa2`. It defaults to a CLI feature and also contains fuzzy rules, SVG rendering, skills, fixtures, and a live-test source.

**Possible file targets if an owner selects this path.** Existing caller: `judge/Cargo.toml` and `judge/src/lib.rs`. Home has not changed.

```toml
# Candidate declaration only — no installation or implementation approved.
[dependencies]
fuzzy-jev = { version = "=0.6.0", default-features = false }
```

The exact pin and feature opt-out are grounded in the inspected release manifest. They do **not** select the crate, create a request, or import the crate's fuzzy policy.

**Open decisions.**
- Does the caller need only typed Decisions transport, or any fuzzy-rule behavior?
- What state is allowed to leave the caller, and which answer is allowed to affect a decision?
- What timeout, retry, idempotency, and cost ceiling should the caller own?
- Is a benign compatibility call authorized through the approved secret path?

## 2. Alternative: System One gateway client

### Proposal B — complete an immutable audit of `typesafe-system-one` 0.1.1 before choosing it

The source reviewed for this candidate is a moving public repository, not its released 0.1.1 artifact. It models Noul, Choice, and Score and documents OpenRouter configuration as a base URL plus `/v1/systemone`.

That surface is provider-documented, but the published-artifact/source equivalence and live gateway compatibility remain unwitnessed. Its direct-TypeSafe defaults must be overridden for OpenRouter.

**Why this stays open.** It may be a smaller fit for an existing typed client, but it has more release-equivalence uncertainty than the inspected `fuzzy-jev` artifact. No comparison here decides a winner.

## 3. First consumer: guide or decision point?

### Proposal C — keep the Field monitor's reaping behavior as a guide until its owner chooses a decision

The proposed first consumer has been described as a Field monitor/reaping guide. No fork-specific consumer has been established. Neither a guide nor a retired-response path has been selected, and there is no default reaping policy.

A guide can show evidence and leave the action to its owner. A decision point would require a defined state contract, typed question, confidence threshold, fallback, audit record, and a clear person or component accountable for the result.

**Real target remains conditional.** No reaping target file is selected. Do not add Jev to a default reaping path from this book.

## 4. Three boundaries that need an owner

| Boundary | Current fact | Decision still needed |
| --- | --- | --- |
| Client | `fuzzy-jev` 0.6.0 artifact was audited; `typesafe-system-one` 0.1.1 source only | Reuse which dependency, or keep the custom alpha adapter held? |
| Policy | Jev returns typed probabilities, not prose | Which question, threshold, fallback, and cost ceiling are acceptable? |
| Consumer | Field monitor/reaping guide and retired-response are unselected | Where does a response act, and who owns the result? |

## Reading a typed decision without making it policy

```json
{
  "model": "typesafe/jev-1.13",
  "state": { "statement": "1 equals 1" },
  "questions": {
    "is_true": { "type": "noul", "instructions": "Is the statement true?" }
  }
}
```

This is an illustrative shape for the documented Decisions API, not a permitted request or a chosen schema. Its essential distinction is that the model returns a typed answer; code must still define what that answer is allowed to do.

## Evidence and limits

- OpenRouter documents both Decisions (`/api/alpha/decisions`) and System One (`/api/v1/systemone`) for Jev.
- The custom alpha adapter is unpublished and not installed. Source/fixtures were reviewed; its 21/21 offline result and Cargo release are executor-reported, not rerun here.
- Credentials remain unknown: the metadata lookup only established **missing or inaccessible**, not absence.
- The book's unruled topics include guide versus decide, a cost ceiling, JSON convention, and change-sharing. They remain questions for their owners.

## Sources

- [Jev Rust reuse evidence](/home/li/primary/flows/d66c26/reports/jev-reuse-book-evidence.md)
- [Fable's ecosystem report](/home/li/primary/flows/bad807/reports/jev-ecosystem.md)
- [OpenRouter Jev guide](https://openrouter.ai/docs/guides/community/jev)
- [fuzzy-jev 0.6.0](https://crates.io/crates/fuzzy-jev/0.6.0)

<!-- to-the-living:end -->
