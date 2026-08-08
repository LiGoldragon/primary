# Audited cloud/domain prototype implementation — cloud-operator

## Source used

This pass used the cloud-designer cycle report at
`reports/cloud-designer/4-fully-working-prototype-cycle-2026-05-27/` as the
operator implementation checklist. The actionable standard was: mine existing
intent/reports/prototypes, implement a working prototype that uses the designed
components, then critique gaps as component-growth work instead of bypassing
those components.

## What landed

Implemented a fuller working prototype across the cloud/domain component set:

- `signal-domain-criome` now carries delegation targets.
- `owner-signal-domain-criome` now carries provider-neutral projection
  declarations with `SetProjection`.
- `domain-criome` now has real `domain-criome` and `domain-criome-daemon`
  binaries, socket handling, owner/ordinary Signal dispatch, in-memory registry
  and projection state, projection policy, and runtime tests.
- `owner-signal-cloud` now carries `PrepareProjection`, taking a
  `signal-domain-criome::Projection` as the cloud/domain handoff record.
- `cloud` now lowers `domain-criome` projections into cloud desired state,
  prepares diff-aware DNS plans, validates malformed DNS/redirect content, and
  applies the resulting Cloudflare DNS plan through the existing owner approval
  ceremony.
- The `cloud` flake now uses the gopass-backed `flarectl` wrapper from the
  designer cycle and fails loudly if `cloudflare/api-token` cannot be read.
- Redirect observation now returns a typed unsupported reply instead of silently
  pretending an empty Cloudflare redirect listing is the truth.

## Pushed commits

- `signal-domain-criome` `a89e36f0` — add delegation targets.
- `signal-domain-criome` `88c04bc3` — document delegation targets.
- `owner-signal-domain-criome` `8127744d` — configure projections.
- `owner-signal-domain-criome` `ad8038be` — document projection declarations.
- `domain-criome` `1fbb92ef` — implement projection daemon prototype.
- `domain-criome` `86eb544f` — add flake lock.
- `owner-signal-cloud` `927eb165` — prepare domain projections.
- `owner-signal-cloud` `851850c8` — document projection preparation.
- `cloud` `9d3f96dc` — prepare and apply domain projections.

## Working path now proven

The prototype now proves this path with production contract types:

1. Owner registers a domain in `domain-criome`.
2. Owner records provider-neutral DNS/redirect projection state in
   `domain-criome`.
3. Ordinary `domain-criome::Project` returns that projection through the daemon
   socket path.
4. Owner sends the projection to `cloud::PrepareProjection`.
5. `cloud` converts the projection into provider desired state.
6. `cloud` fetches current Cloudflare DNS state, emits create/update/delete
   plan sections, owner approves, and `ApplyPlan` executes through the
   Cloudflare provider adapter.

## Validation run

- `signal-domain-criome`: `cargo test`; `nix flake check`.
- `owner-signal-domain-criome`: `cargo test`; `nix flake check`.
- `owner-signal-cloud`: `cargo test`; `nix flake check`.
- `domain-criome`: `cargo test`; `nix flake check`.
- `cloud`: `cargo test`; `nix flake check`.

No live Cloudflare credential was used; Cloudflare mutation remains fixture/test
verified until a real scoped token is provided.

## Audit after implementation

This pass closed several designer-cycle audit gaps:

- `Validate` is no longer a total no-op for DNS/redirect shape.
- `PreparePlan` is now diff-aware for DNS records.
- `CredentialHandleUnknown` is now emitted on Cloudflare account registration
  when the credential source cannot resolve the handle.
- Redirect observation no longer silently returns empty truth.
- The cloud/domain boundary now uses the designed `domain-criome` and `cloud`
  components rather than a direct Cloudflare-only shortcut.

Remaining major gaps:

- Redirect read/write still needs Cloudflare Rulesets/Page-Rules API work.
- `Plan` still needs the future `Mutate` state-machine rename and lifecycle.
- Projection handoff is now typed but still caller-mediated; the designed
  daemon-to-daemon push path is a later cycle.
- Persistence is still in-memory by intent for this prototype cycle.
