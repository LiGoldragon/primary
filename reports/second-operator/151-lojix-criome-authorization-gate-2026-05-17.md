# Lojix Criome Authorization Gate

Date: 2026-05-17

Role: operator-assistant

Input context:

- `reports/designer/214-criome-architecture-record-2026-05-17.md`
- `reports/system-specialist/141-lojix-criome-arca-implementation-synthesis-2026-05-17.md`

## Summary

I ported the highest-signal part of SYS/141 into code and architecture:
Lojix now has an explicit Criome authorization actor on the deployment
path, and `signal-lojix` now owns a canonical deployment request digest
that Lojix can present to Criome.

The slice deliberately stops before the real `signal-criome` socket
client and before Arca artifact preservation. It is still useful because
it proves the load-bearing invariant SYS/141 asked for: no Nix/SSH/rsync
deployment effect starts until the authorization path grants the typed
deployment request.

## Commits

- `signal-lojix` `horizon-leaner-shape`: `df49dae1`
  `signal-lojix: add canonical deployment request digest`
- `lojix` `horizon-leaner-shape`: `6a799dac`
  `lojix: gate build effects on criome authorization`

Both worktrees are clean and both bookmarks are pushed.

## Contract Work

Repository:
`/home/li/wt/github.com/LiGoldragon/signal-lojix/horizon-leaner-shape`

Files changed:

- `src/lib.rs`
- `tests/round_trip.rs`
- `Cargo.toml`
- `Cargo.lock`
- `ARCHITECTURE.md`
- `skills.md`

`signal-lojix` now defines `DeploymentRequestDigest` and
`DeploymentSubmission::canonical_digest()`.

The digest is:

1. derived from the typed `DeploymentSubmission`,
2. encoded through rkyv canonical bytes,
3. hashed with BLAKE3,
4. exposed as a contract-owned type.

Representative code:

```rust
impl DeploymentRequestDigest {
    pub fn from_canonical_bytes(bytes: &[u8]) -> Self {
        Self(blake3::hash(bytes).to_hex().to_string())
    }
}

impl DeploymentSubmission {
    pub fn canonical_digest(&self) -> Result<DeploymentRequestDigest> {
        let bytes = rkyv::to_bytes::<rkyv::rancor::Error>(self)
            .map_err(|error| Error::CanonicalDeploymentRequestUnavailable(error.to_string()))?;
        Ok(DeploymentRequestDigest::from_canonical_bytes(&bytes))
    }
}
```

This avoids deriving authorization identity from CLI text or from
daemon-local reconstruction. The contract type owns the digest.

Tests added:

- `deployment_submission_digest_is_stable_over_canonical_bytes`
- `deployment_submission_digest_changes_when_request_content_changes`

## Lojix Work

Repository:
`/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape`

Files changed:

- `src/authorization.rs`
- `src/runtime.rs`
- `src/deploy.rs`
- `src/lib.rs`
- `tests/build_pipeline.rs`
- `Cargo.toml`
- `Cargo.lock`
- `ARCHITECTURE.md`
- `README.md`
- `skills.md`

I added `CriomeAuthorization` as a Kameo actor. It receives typed
deployment submissions, computes the `signal-lojix` canonical request
digest, maps the request into a `signal-criome::AuthorizationScope`, and
returns a grant or denial.

Representative code:

```rust
impl Message<AuthorizeDeployment> for CriomeAuthorization {
    type Reply = Result<DeploymentAuthorizationGrant>;

    async fn handle(
        &mut self,
        message: AuthorizeDeployment,
        _context: &mut Context<Self, Self::Reply>,
    ) -> Self::Reply {
        let request = DeploymentAuthorizationRequest::from_submission(
            message.deployment,
            &message.submission,
        )?;
        self.policy.authorize(request)
    }
}
```

The deployment path now validates unsupported local/activation requests
first, then asks `CriomeAuthorization`, then spawns the build job only
after authorization succeeds.

Representative deployment gate:

```rust
let authorization = match self
    .criome_authorization
    .ask(AuthorizeDeployment::new(
        message.deployment.clone(),
        message.submission.clone(),
    ))
    .await
{
    Ok(grant) => grant,
    Err(error) => {
        return Ok(wire::Reply::DeploymentRejected(
            DeploymentError::new(error.to_string()).into_rejection(),
        ));
    }
};
let _authorized_request_digest = authorization.request_digest();
let _authorized_scope = authorization.scope();

let job = BuildJobActor::spawn(BuildJobActor::new(
    self.configuration.clone(),
    self.deployment_ledger.clone(),
    self.garbage_collection_roots.clone(),
    message.deployment.clone(),
    message.submission,
));
```

The runtime root now owns the authorization actor as part of the actor
tree. In-process tests use `GrantForTests`; daemon configuration fails
closed with `Unavailable` until the real `signal-criome` daemon client
lands.

## Test Witness

The new Lojix witness is:

`criome_authorization_denial_blocks_every_fake_nix_effect`

The test configures the runtime with a denying authorization policy,
submits an otherwise valid deployment request, asserts the deployment is
rejected with the denial reason, and asserts the fake Nix/SSH/rsync log
is empty.

Representative assertion:

```rust
assert_rejected_with(reply, "fixture criome denied deployment");
assert_eq!(fixture.tool_log(), "");
```

This is the current proof that the authorization gate sits before the
deployment effect boundary.

## Verification

`signal-lojix`:

- `cargo fmt`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `nix --option max-jobs 1 --option cores 2 flake check -L`

`lojix`:

- `cargo fmt`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `nix --option max-jobs 1 --option cores 2 flake check -L`

The Lojix Nix check passed all package, fmt, clippy, unit, socket,
build-pipeline, event-log, configuration-boundary, and daemon/CLI
integration checks.

## Architecture Updates

`signal-lojix/ARCHITECTURE.md` now says the canonical deployment request
digest belongs to the contract layer and is derived from typed rkyv bytes.

`lojix/ARCHITECTURE.md` now says:

- build jobs pass through `CriomeAuthorization`;
- `signal-criome` is the authorization vocabulary;
- no local Nix, SSH, rsync, GC-root, cache, or activation effect starts
  until the authorization gate grants the canonical digest and scope;
- the test witness proves denial leaves the fake effect log empty.

`lojix/README.md` now warns that the real daemon path fails closed until
the real Criome socket client lands. That is intentional. In-process
tests can still use a fake grant policy.

## Shortcomings

The worst part is that `CriomeAuthorization` is still a local policy
actor, not a real Criome client. It gives the deployment graph the right
place to ask for permission, and it makes the effect boundary testable,
but it does not yet send a routed authorization request to Criome.

The authorization scope is a string-backed
`signal_criome::AuthorizationScope`. The shape is adequate for a first
gate, but it should become more typed once `signal-criome` or
`signal-lojix` owns richer scope vocabulary for Lojix deployment plans.

The grant is consumed only as a gate today. Lojix does not persist the
grant, attach it to an Arca artifact set, or include it in a durable
deployment provenance record yet.

The production daemon path now fails closed for deployments because the
real Criome socket client does not exist yet. That is the correct safety
default, but it means the `real-build-smoke` app is parked until the next
slice lands.

No Arca path was implemented. SYS/141's artifact-preservation direction
still needs a follow-up pass after the real authorization request/response
shape is in place.

## Next Work

1. Replace `CriomeAuthorizationPolicy::Unavailable` with a real
   signal-criome client policy that presents the canonical request digest
   and scope to Criome.
2. Extend `signal-criome` if needed so Lojix can express pending,
   signed, denied, expired, and observed authorization outcomes without
   inventing local proof language.
3. Persist authorization grant metadata in Lojix's Sema-backed deployment
   ledger.
4. Introduce Arca artifact-set recording after authorization succeeds and
   before deployment effects are considered complete.
5. Add a Nix-wired stateful integration test that runs the daemon path
   with a fake Criome responder instead of only an in-process policy.
