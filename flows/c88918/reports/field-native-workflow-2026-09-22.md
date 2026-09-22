# Field native workflow preflight — documented handoff

Owner: Field Ultra Low Luna `c88918`. This is scoped source evidence and a
passive lifecycle gate. It is not a deployment, native refresh, route change,
registration, or readiness claim.

## Handoff and provenance

Field Medium Sol `753e69` landed the implementation on branch
`field-flow-preflight-753e69`, remote-verified at
`5579e9cb71edb7e2b1634e410c6d541702d2006e`, from isolated Primary base
`09074869b294648dc535803126cb351b024e2f8`. The landing contained exactly the
two tool paths and Sol's draft report. Before this documentation commit, the
latest `origin/main` was `8a03d3f981a973bdb849694c8e6a886d8587d8e0`; all three
destination preimages were absent there. Only the tested tool bytes were
integrated, and the report was rewritten under this flow's path.

Terra `0347d0` independently tested the exact tool bytes: MJS SHA-256
`e8cfc0e27e69414ad4fa04a1a6724ac2c2da7f8d3826a1d39afcb215d643f134`, test
SHA-256 `54732b2fe5646232643f2da9dee522309d0d67b7b0127cbdeb5123c6773cd891`;
local `3/3`. The tested cases include blocked `UnknownFlow`, exact native/HM
identity checks, stale Herdr evidence, a positive synthetic route, and one
typed fallback after legacy syntax refusal. Legacy `UnknownFlow` does not
fallback; unresolved paths fail closed. The positive path is synthetic only.

The handoff was accepted after Sol's landing. Orchestrate lock `4565` reserved
exactly the two tool paths and this report path for the documented commit. No
foreign dirty paths, generated skill trees, round `4494`, routes, seats, or
held Psyche High state were in scope.

## What the gate does

`tools/field-flow-preflight.mjs` reads operator-supplied native receipt, HM
registry, optional current Herdr binding, and optional source attestation. It
hashes the installed Flow and Nexus binaries and an explicitly supplied running
Nexus executable. It performs only read-only recipient resolution: first the
installed positional `flow resolve <six-hex-id>` form, and only after syntax
refusal the candidate one-Datom `ResolveRecipient.<six-hex-id>` form. A
successful answer is never silently retried.

The gate reports exact native/HM matching, resolution grade, running-versus-
installed Nexus identity, current Herdr binding evidence, source/install
parity, and blockers. `readyForFlowLifecycle` is true only when every gate is
present. Unknown Flow, absent or stale Herdr evidence, native/HM mismatch,
unrecognized replies, and source parity gaps fail closed.

## Source versus installed boundary

The installed witness remains separate from this source landing. The installed
`/home/li/.local/bin/flow` previously exposed the positional `start`/`restart`/
`resolve` CLI and returned `RecipientResolutionRejected.UnknownFlow` for live
HM-known IDs. The installed Nexus service and its Sema state were not rebuilt,
restarted, registered, or changed by this work. This commit therefore makes no
claim of installed parity, native route readiness, lifecycle readiness, or
deployment.

## Remaining production gates

The following remain open and belong to the existing owners/controller:

- Sol/Terra must return to the source owners for any behavior change.
- A current exact native/HM/Herdr binding must be witnessed for the target.
- Installed Flow/Nexus bytes must be tied to a reviewed source revision and
  running-process digest.
- The typed Flow store/Nexus must be coherently built, deployed, and tested;
  this passive gate does not import HM records or repair the installed Sema
  store.
- A disposable end-to-end recipient receipt is still required before any
  lifecycle operation.

Field High `03e825` retains design/orchestration ownership and round `4494`.
Field Medium `753e69` owns implementation. Field Low `0347d0` owns
independent testing. Luna owns this scoped documentation commit only. The
conditional `6db4fe` reap remains separately gated; no reap or route withdrawal
is authorized by this report.

## Sources

- Sol landing `5579e9cb71edb7e2b1634e410c6d541702d2006e` and its exact three-path
  diff, read from the remote-verified branch.
- Terra's independent exact-byte test verdict and SHA-256 receipts supplied in
  the handoff.
- Latest fetched `origin/main` `8a03d3f981a973bdb849694c8e6a886d8587d8e0` and
  preimage checks for the three destination paths.
- Installed Flow/Nexus observations and the prior source review recorded in
  the preceding Field workflow diagnosis.
