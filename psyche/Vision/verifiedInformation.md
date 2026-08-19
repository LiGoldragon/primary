# Verified information

## 2026-08-19 — a protocol to keep track of verified information, so we don't re-verify the same thing a thousand times

Design session `7c3f0c1d`, typed (captured 2026-08-19T13:05+02:00). The
Designer had said that grounding the context strata in the LLM's message roles
was "a claim about the model and the API I have not verified in code". The
psyche:

> obviously you cant inspect the model, nor its training code. and you have
> looked into this in a previous flow. If you want to check again, you can, but
> we should agree on a protocol to keep track of verified information, so that
> we dont end up re-verifying the same thing a thousand times, and even if we
> do, we can compare the thousand verifications with each other at least.

## 2026-08-19 — skills can't cite the ledger by path; the ledger is `verified/`; re-verifications append

Design session `7c3f0c1d`, typed (captured 2026-08-19T13:40+02:00). On the
Designer's proposed line "when stating a harness fact, a skill or report
cites the record":

> skills cant use file paths. the report would have to be published and be
> referred to by its publicly available name and version. thats quite complex
> and I dont want to go there right now.

On the two questions — (a) ledger at root `verified/` or inside `reports/`;
(b) does a record expire with a version bump or does the heading stay and the
new version append:

> 2.a. verified/ b. append
