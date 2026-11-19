# API spend, credit balance and expiry — step 1 findings

Research: Mind research Sol, flow 85ab00. Checked 19 November 2026, about 05:52 UTC. Authority: Opus xmy4 and energy-credits.md step 1. **Read-only research complete; no paid model call or implementation.**

## Result for implementation

Both providers document administrative cost-report APIs. The available credentials did not obtain a cost report in the two safe probes below. Neither provider's public documentation inspected here exposes a supported API-key call returning promotional credit balance and grant expiry. **Current OpenAI balance and expiry remain unknown.** Use the owner's Credit and Spent settings where provider evidence is unavailable; an authentication refusal is not zero spend. A configured grant minus reported cost is a derived estimate, not an observed provider credit balance.

## Claude API

For a new integration, the documented call is `GET https://api.anthropic.com/v1/organizations/analytics/cost`, with `starting_at` and `ending_at` RFC 3339 timestamps. Console organizations require an **Admin API key**, or another administrative credential such as OAuth with `org:admin`; an inference key is not the documented credential. Required headers include `anthropic-version` and beta `analytics-usage-cost-2026-08-24`.

Cost `amount` is after discounts, **before credits**, expressed as a decimal string in **cents**, despite currency USD; retain fractional cents when aggregating. Fetch all pages, without narrowing organization coverage. Ranges are at most 31 days, within the last 365 days and no earlier than 2026-01-01. Boundaries round down to the selected UTC bucket, or hour without a bucket. `data_refreshed_at` marks coverage; refresh normally takes up to four hours and can take 24, with later revisions. Thus a fresh exact credit debit since an arbitrary instant is not guaranteed. [Analytics contract](https://platform.claude.com/docs/en/manage-claude/usage-cost-analytics-api).

The older `GET /v1/organizations/cost_report?starting_at=...&ending_at=...` remains documented, with administrative authentication; the provider now recommends Analytics for new integrations. Token usage reports are distinct from cost reports. [Legacy guide](https://platform.claude.com/docs/en/manage-claude/usage-cost-api), [cost-report reference](https://platform.claude.com/docs/en/api/beta/organization/cost_report/retrieve).

Balance and expiry are shown in the Console's **Promotional credits** section. Subscription credits renew on their billing cycle and expire without rollover; all keys/workspaces in the linked organization share them. This describes the mechanism, not this account's current amount or dates. No supported grant-balance/expiry endpoint was found in the inspected administrative/reporting documentation. [Credit documentation](https://platform.claude.com/docs/en/about-claude/api-credits-for-subscribers).

## OpenAI API

The documented call is `GET https://api.openai.com/v1/organization/costs?start_time=<Unix-seconds>&end_time=<Unix-seconds>`, authenticated with an **organization Admin API key** using Bearer authentication. Start is inclusive and end exclusive. Cost buckets currently support only `1d`; follow `has_more`/`next_page` with `page`. Sum monetary `amount.value` values only after checking currency and coverage. Use organization-wide scope, rather than silently selecting one project or key. Check returned bucket boundaries before claiming exact coverage of a mid-day grant start. [Costs reference](https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/usage/methods/costs). Administrative keys are separate from project credentials and are not model-inference keys. [Admin authentication](https://developers.openai.com/api/docs/guides/admin-apis).

OpenAI directs owners to the linked organization's Billing/Credit grants page for grant details. Usage costs and grants answer different questions; reported cost need not equal cash charged after credits. Recent usage can arrive late. I found no documented supported API-key balance/expiry call in the inspected public reference. Browser-session/private billing endpoints were not used. [Usage and grants](https://help.openai.com/en/articles/10478918-reviewing-api-usage-and-costs). Subscription grants expire with the applicable billing cycle; generic product rules do not establish this account's expiry. [Subscription-credit guide](https://developers.openai.com/api/docs/guides/chatgpt-api-credits).

## Tried result with our available keys

Two single GET requests covered the preceding day, with page size one, solely to test read access:

| Stored credential reference | Read-only endpoint | Observation |
|---|---|---|
| `openai/api-key` | OpenAI `/v1/organization/costs` | HTTP **403**; no cost, balance or expiry obtained. |
| `platform.claude.com/ligoldragon-api-key` | Claude `/v1/organizations/analytics/cost` | HTTP **401**; no cost, balance or expiry obtained. |

These statuses establish refusal for these requests, not the underlying cause, account balance, exhaustion, or absence of an administrative credential elsewhere. The inspected GoPass names contained no separately named provider Admin key. No key was created, rotated or modified.

GoPass password output was piped directly to the pinned Python consumer's stdin. The consumer held headers only in memory, used HTTPS to the documented provider hosts, disabled redirects, and emitted only endpoint/status metadata. Credential values, response bodies and error messages were suppressed; none was placed in argv, environment assignments, files, logs or messages. The stdin interface was verified against Python's [standard-stream documentation](https://docs.python.org/3/library/sys.html#sys.stdin) and [request interface](https://docs.python.org/3/library/urllib.request.html#urllib.request.Request). No ledger, worker, billing configuration or model endpoint was touched.

**Boundary:** administrative spend reporting needs a suitable credential; actual grant balance/expiry needs owner-supplied billing evidence unless a supported provider contract is subsequently established. Preserve observation time, period coverage, precision and availability. Research's local reservation ledger is neither organization-wide provider spending nor a credit balance. The owner's separately reported Claude grant/date remains owner-supplied evidence, not a result of these probes.
