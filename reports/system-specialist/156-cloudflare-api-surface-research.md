# Cloudflare API surface for the future cloud component

Date: 2026-05-23

Scope: official Cloudflare sources only. This is a surface map for the first
`cloud` component provider plane: DNS records and redirects/page-rule
behavior. It does not design Google, Hetzner, or the broader cloud daemon.

## Bottom line

Cloudflare has enough official API surface to manage the needed state without
dashboard scraping. DNS records are managed through the DNS Records API.
Redirects should be managed through Rulesets-backed Single Redirects and
Bulk Redirects, not new Page Rules. Page Rules remain useful as a legacy
read/import surface because the API still exists and forwarding URL rules may
already be present.

For a Rust daemon, the most direct runtime path is the HTTPS v4 API through an
internal typed client. Cloudflare's official SDK list is Go, TypeScript, and
Python, plus the Terraform provider; there is no official Rust SDK in the
current SDK list.

## 1. DNS records API

Use the Cloudflare DNS Records API under:

- `GET /zones/{zone_id}/dns_records` to list/search/filter records.
- `POST /zones/{zone_id}/dns_records` to create records.
- `GET /zones/{zone_id}/dns_records/{dns_record_id}` to read one record.
- `PATCH /zones/{zone_id}/dns_records/{dns_record_id}` to edit fields.
- `PUT /zones/{zone_id}/dns_records/{dns_record_id}` to overwrite a record.
- `DELETE /zones/{zone_id}/dns_records/{dns_record_id}` to delete a record.
- `POST /zones/{zone_id}/dns_records/batch` for batched creates, updates,
  patches, and deletes.

Cloudflare documents important constraints directly on create/update: A/AAAA
records cannot coexist at the same name with CNAME records; NS records cannot
coexist at the same name with any other record type; returned domain names are
Punycode. DNS record comments and tags have no effect on DNS responses, which
makes them suitable for managed-state markers.

The batch API executes the requested DNS changes in one Cloudflare database
transaction, but Cloudflare explicitly says propagation through its distributed
KV store is not atomic. A `cloud` daemon should treat batch as a convenience
for fewer API calls, not as an externally atomic DNS rollout primitive.

Sources:

- DNS records list API: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/list/
- DNS record create API: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/create/
- DNS record patch API: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/edit/
- DNS record overwrite API: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/update/
- DNS record delete API: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/delete/
- DNS record batch API: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/batch/

## 2. Redirect, page-rule, ruleset, and bulk-redirect APIs

Cloudflare's current redirect documentation points at three modern redirect
products:

- Single Redirects: zone-level static or dynamic redirects. Use the Rulesets
  API, zone phase `http_request_dynamic_redirect`, with rules whose action is
  `redirect`.
- Bulk Redirects: account-level large static redirect maps. Create a Rules
  List with `kind = "redirect"`, add list items, then create/update an account
  Ruleset in the `http_request_redirect` phase to enable that list.
- Snippets: JavaScript for more complex redirect behavior. This is not the
  first target for the `cloud` component, but it is the official path when
  redirect logic exceeds Single/Bulk Redirects.

Cloudflare's redirect overview says Single Redirects and Bulk Redirects
require proxied DNS records for the hostname receiving requests. It also says
Rules products take precedence over Page Rules. The Page Rules migration guide
shows Forwarding URL migrating to Single Redirects. Therefore the `cloud`
component should create new redirect behavior as Single Redirects or Bulk
Redirects and reserve Page Rules for observing/importing existing legacy
configuration.

The Page Rules API still exists:

- `GET /zones/{zone_id}/pagerules`
- `POST /zones/{zone_id}/pagerules`
- `PUT`, `PATCH`, and `DELETE` on `/zones/{zone_id}/pagerules/{pagerule_id}`

Page Rule `forwarding_url` can still express 301/302 URL forwarding, but using
it for new state would encode the old control plane.

Sources:

- Redirect overview and recommendations: https://developers.cloudflare.com/rules/url-forwarding/
- Single Redirect API guide: https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-api/
- Rulesets API: https://developers.cloudflare.com/api/resources/rulesets/
- Bulk Redirect API guide: https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/create-api/
- Bulk Redirect concepts: https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/concepts/
- Rules Lists API: https://developers.cloudflare.com/api/resources/rules/
- Page Rules API: https://developers.cloudflare.com/api/resources/page_rules/
- Page Rules migration guide: https://developers.cloudflare.com/rules/reference/page-rules-migration/

## 3. Auth model and minimum token scopes

Cloudflare v4 APIs use `Authorization: Bearer <API_TOKEN>` and Cloudflare says
API tokens are preferred over the older email plus global API key flow. The
stable API base URL is `https://api.cloudflare.com/client/v4/`.

Minimum practical scopes for this first provider plane:

- Zone discovery by name: `Zone Read`.
- DNS observation: `DNS Read`.
- DNS mutation: `DNS Write`.
- Single Redirect observation/mutation: current permission docs name
  `Single Redirect Read/Edit`; the API schema vocabulary also exposes
  `Dynamic URL Redirects Read/Write`. Use the narrow Single Redirect/Dynamic
  URL Redirect permission rather than broad `Zone Write` or `Account Rulesets
  Edit`.
- Bulk Redirect list observation/mutation: `Account Filter Lists Read/Edit`
  for redirect lists and items.
- Bulk Redirect ruleset observation/mutation: current permission docs name
  `Bulk URL Redirects Read/Edit`; endpoint examples still show older/broader
  names such as `Mass URL Redirects Write` and `Account Rulesets Write`.
  Token tooling should query Cloudflare's permission groups endpoint rather
  than baking old permission labels.
- Page Rules legacy import: `Page Rules Read`; only use `Page Rules Edit` if
  there is an explicit migration operation that disables or deletes legacy page
  rules after validation.

Credential storage is not a Cloudflare problem; in our system it belongs in
the daemon's policy/secret layer. The Signal request should name a provider
capability, not carry token bytes.

Sources:

- Make API calls/auth/base URL: https://developers.cloudflare.com/fundamentals/api/how-to/make-api-calls/
- Token permission reference: https://developers.cloudflare.com/fundamentals/api/reference/permissions/
- DNS list accepted permissions: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/list/
- DNS create accepted permissions: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/create/
- Single Redirect API permissions: https://developers.cloudflare.com/rules/url-forwarding/single-redirects/create-api/
- Bulk Redirect API permissions: https://developers.cloudflare.com/rules/url-forwarding/bulk-redirects/create-api/
- Rules List permissions: https://developers.cloudflare.com/api/resources/rules/subresources/lists/methods/list/
- Page Rules list/create permissions: https://developers.cloudflare.com/api/resources/page_rules/methods/list/ and https://developers.cloudflare.com/api/resources/page_rules/methods/create/

## 4. Rate limits, idempotency, and list-before-mutate

Cloudflare's global API limit is 1,200 requests per five minutes per user or
account token, plus 200 requests per second per IP. It returns rate-limit
headers and `retry-after` on limit hits. Cloudflare also notes that specific
API families, including Rulesets and Lists, can have their own limits.

The `cloud` daemon should assume there is no universal idempotency key on these
REST mutations. The safe shape is reconcile-first:

- Resolve account and zone IDs once, then cache with periodic refresh.
- List before create. For DNS, compare by managed logical key plus
  Cloudflare record ID; use comments/tags for `managed-by-cloud` style
  discovery rather than relying only on name/type/content.
- Use `PATCH` for narrow DNS edits and `PUT` only when the daemon intends to
  overwrite the full record representation.
- Before delete, re-read the resource and verify it is still the record/rule
  the daemon thinks it owns.
- For Rulesets, use stable rule `ref` values so the daemon can reconcile rules
  without depending only on Cloudflare-generated IDs.
- For Bulk Redirect Lists, use stable list names and poll list bulk-operation
  status after item create/update/delete because list item mutations return
  asynchronous operation IDs.
- Treat DNS batch as a transaction inside Cloudflare's database only; do not
  assume externally atomic propagation.

Sources:

- API rate limits: https://developers.cloudflare.com/fundamentals/api/reference/limits/
- API pagination and filtering guidance: https://developers.cloudflare.com/fundamentals/api/how-to/make-api-calls/
- DNS batch non-atomic propagation note: https://developers.cloudflare.com/api/resources/dns/subresources/records/methods/batch/
- Rulesets `ref` field: https://developers.cloudflare.com/api/resources/rulesets/
- Rules Lists bulk operations: https://developers.cloudflare.com/api/resources/rules/

## 5. Signal split for the future cloud triad

Ordinary `signal-cloud` should expose operations that are safe for ordinary
authenticated peers and agents:

- Observe Cloudflare accounts/zones visible to the configured capability.
- Observe DNS records, Single Redirect rules, Bulk Redirect lists/items, and
  legacy Page Rules.
- Validate a proposed DNS/redirect shape against Cloudflare constraints and
  local policy.
- Plan a reconciliation and return a diff, including which Cloudflare API
  operations would be called.
- Submit a desired-state proposal into daemon state when policy allows the
  caller to propose, but not necessarily apply.

Owner/policy signal should own authority and provider configuration:

- Register or rotate Cloudflare credentials and bind them to named provider
  capabilities.
- Authorize which zones/domains this daemon may manage.
- Set per-zone/per-domain policy: allowed record types, redirect targets,
  deletion policy, proxy requirements, and whether legacy Page Rules may be
  modified.
- Approve/apply live mutation plans to Cloudflare.
- Delete or disable remote resources.
- Enable optional provider support in daemon policy/build selection.

If the workspace renames `owner-signal-*` to `meta-signal-*`, this boundary is
unchanged: the ordinary contract observes, validates, and proposes; the policy
contract configures credentials, authority, and live mutation.

## 6. Risks and gaps

- Permission names are in flux. The permission reference includes both old
  "Write" labels and newer "Edit" labels, while product docs and API schema
  examples do not always use the same human-facing name. The daemon should not
  hard-code permission display names as protocol truth.
- Redirects require proxied DNS. DNS-only records will not receive Single or
  Bulk Redirect behavior.
- Page Rules are still API-addressable but are the wrong future write target.
  Legacy state may conflict with modern Rules products; Cloudflare says modern
  Rules products take precedence.
- Cloudflare plan quotas matter for Single/Bulk Redirect counts and regex
  support. The daemon must observe plan/entitlement failures as ordinary
  provider rejections, not treat them as schema errors.
- Bulk Redirect item mutation is asynchronous. A daemon needs operation polling
  and state that can represent pending/failed remote operations.
- DNS record identity is not always a simple `(name, type)` pair: TXT/MX and
  other record classes may have multiple records with the same name and type.
  The daemon needs stable managed identifiers in comments/tags plus stored
  Cloudflare IDs.
- Official SDKs exist for Go, TypeScript, and Python, plus Terraform. A Rust
  implementation should call the REST API directly or generate a local client
  from the API schema; pulling a community SDK into the component should be a
  deliberate dependency decision, not the default.
