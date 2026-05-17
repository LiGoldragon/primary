# lojix Criome-mediated authorization decision - 2026-05-17

## Trigger

The system-assistant asked for direction on two open implementation
questions:

1. Should authorization be per-daemon identity keys, an
   operator-signed attestation chain, or something else?
2. Should the caller shape be a thin CLI talking to one cluster daemon,
   or should the operator run its own `lojix-daemon`?

The user's answers:

- authorization needs `criome-daemon`;
- authorization propagates through the `criome-daemon` topology first;
- the `signal-lojix` call is the signed object;
- Criome holds the permission data: which key or quorum has which
  permission;
- clients only initiate deploys;
- daemons talk to each other;
- the receiving `lojix-daemon` forwards the request to
  `criome-daemon`, which may route request signatures to concerned
  clients.

This closes an open question in
`reports/system-specialist/138-lojix-arca-distributed-deploy-architecture-2026-05-17.md`.

## Decision

`lojix` does not own the permission model.

`lojix` owns deployment coordination after Criome authorizes a typed
request. Criome owns authorization topology, permission records, quorum
rules, and signature collection.

The deployment request is a signed `signal-lojix` object. The
authorization answer is a Criome-produced authorization object tied to
the exact request digest.

## Corrected flow

```mermaid
flowchart LR
    client["client<br/>CLI or any caller"]
    lojix["receiving lojix-daemon"]
    criome["local criome-daemon"]
    mesh["criome-daemon topology"]
    participants["concerned clients / keys / quorum"]
    arca["arca-daemon<br/>artifact plane"]
    peer["peer lojix-daemons"]

    client -->|signal-lojix request object| lojix
    lojix -->|AuthorizeSignalCall(request digest)| criome
    criome -->|route authorization work| mesh
    mesh --> participants
    participants -->|sign / deny / abstain| mesh
    mesh --> criome
    criome -->|authorization object| lojix
    lojix -->|store request + authorization artifacts| arca
    lojix -->|authorized daemon requests| peer
```

The CLI remains a text adapter and initiator. It does not speak to
Horizon, does not project cluster state, does not choose topology, and
does not coordinate authorization across daemons.

## Authorization object shape

The exact type belongs in `signal-criome` / Criome, not in `lojix`, but
the required fields are clear enough to guide implementation:

```text
CriomeAuthorization {
  authorized_object_digest,
  authorized_contract = signal-lojix,
  authorized_verb,
  permission_slot,
  authorization_scope,
  quorum_result,
  signatures,
  issued_by_criome_identity,
  issued_at,
  expires_at,
}
```

`lojix` should treat this as an authorization envelope, not as an ACL.
The policy facts stay in Criome's sema state.

## What exactly is signed

The signed object must be canonical binary request content, not CLI
text and not a transport wrapper with incidental fields.

Candidate:

```text
SignalObjectDigest = blake3(canonical signal-lojix request payload)
```

The important rule:

> every authorization proof refers to the exact `signal-lojix` request
> object digest that `lojix-daemon` will execute.

If a plan artifact is later derived from the request, the plan must
carry a back-reference to the authorized request digest. The plan may
also be signed by the coordinator for integrity, but the permission to
execute comes from Criome.

## Relationship to Arca

Arca is the right artifact plane for the immutable authorization
evidence:

```text
DeploymentArtifactSet {
  signal_lojix_request = blake3:...
  criome_authorization = blake3:...
  horizon_proposal = blake3:...
  cluster_proposal = blake3:...
  viewpoint = blake3:...
  projected_horizon = blake3:...
  generated_nix_inputs = blake3:...
  deployment_plan = blake3:...
}
```

Participant `lojix-daemon`s should receive the Arca refs and verify
that:

- the Criome authorization object names the exact request digest;
- the deployment plan names the exact request digest;
- the local Criome trust root accepts the authorization object;
- the requested local effect is within the authorization scope.

This preserves the report 138 boundary:

- Arca carries exact artifacts;
- Criome authorizes action;
- `lojix` executes deployment state machines;
- Nix carries realized output closures.

## Consequences for lojix implementation

### Add a Criome authorization actor

`lojix-daemon` needs a local actor before planner/build/activation:

```text
CriomeAuthorizationActor
  accepts:
    AuthorizeDeploymentSubmission
    VerifyDeploymentAuthorization

  calls:
    local criome-daemon through signal-criome

  emits:
    AuthorizationPending
    AuthorizationGranted
    AuthorizationDenied
    AuthorizationExpired
    AuthorizationUnavailable
```

Build, cache, import, and activation actors must not run before the
authorization actor emits `AuthorizationGranted`.

### Preserve CLI one-peer rule

The CLI still sends one request to one `lojix-daemon`. It does not call
Criome directly. If authorization needs more signatures, the daemon
returns a typed pending/observation state to the client.

### Treat pending authorization as a first-class state

Signature collection may be asynchronous. `lojix` needs a state such as:

```text
DeploymentAuthorizationPending {
  request_digest,
  criome_request_slot,
  missing_authorities,
  observation_subscription,
}
```

This is not a build failure. It is a deployment job waiting for
authorization.

### Authorization scope must follow local effects

The authorization object should scope the effects it permits:

- build only;
- publish store source;
- import closure;
- activate FullOs;
- activate HomeOnly;
- modify target Nix trust for a temporary store source;
- restart `nix-daemon`.

The exact vocabulary belongs in the permission schema, but `lojix`
needs to check that the local effect it is about to run is in scope.

## Consequences for Criome

Criome needs to own:

- permission records;
- key and quorum records;
- topology for routing authorization requests;
- signature collection state;
- authorization-object issuance;
- expiration and replay policy;
- local verification of authorization objects received from peer
  `lojix-daemon`s.

This means "per-daemon identity keys" are necessary but not sufficient.
Host keys identify daemons. Criome decides what those identities and
operator/client keys may authorize.

## Consequences for signal contracts

### `signal-lojix`

`signal-lojix` request types should be canonicalizable and digestible.
They may need an optional authorization reference after the initial
submission phase:

```text
DeploymentSubmission {
  request_body,
  caller_signature_set,
}

AuthorizedDeploymentCommand {
  request_digest,
  criome_authorization_digest,
  deployment_plan_digest,
}
```

Do not put Criome policy data inside `signal-lojix`.

### `signal-criome`

Criome needs verbs shaped like:

```text
AuthorizeSignalCall
ObserveAuthorization
VerifyAuthorization
RouteSignatureRequest
SubmitSignature
RejectAuthorization
```

Those names are illustrative; the important boundary is that Criome
receives the signed object digest plus requested permission scope and
returns a typed authorization object or pending/denied state.

## Tests implied

### Boundary tests

- `lojix` cannot start build/import/activation without a
  `CriomeAuthorization`.
- CLI does not import or call `signal-criome`; only daemon code does.
- `signal-lojix` request digest changes when request content changes.
- authorization for request A cannot be used for request B.
- authorization with missing scope cannot start target-local
  activation.

### Actor tests

- `CriomeAuthorizationActor` emits pending when Criome asks for quorum.
- pending authorization later resumes the deployment when Criome emits
  granted.
- denial records a terminal deployment observation without starting any
  Nix process.
- authorization expiry stops a queued deployment before local effects.

### Integration tests

- fake `criome-daemon` grants authorization and fake `lojix-daemon`
  proceeds.
- fake `criome-daemon` denies authorization and fake `lojix-daemon`
  does not invoke fake Nix.
- fake peer `lojix-daemon` verifies the Arca-carried authorization
  object before running a target-local effect.

## Open implementation details

### Canonical bytes

The signed object should be the canonical `signal-lojix` payload. The
implementation still has to choose the exact canonical byte encoding
and make it a shared helper so the CLI, daemon, Criome, and tests do
not compute subtly different digests.

### Anti-replay

Authorization objects need freshness:

- issued time;
- expiry;
- nonce or deployment slot;
- target scope;
- maybe one-time-use semantics for activation.

Criome should own replay policy. `lojix` should enforce what Criome
states in the authorization object.

### Plan derivation proof

The plan is derived after authorization. Participants need proof that
the plan belongs to the authorized request. Minimum viable proof:

- plan artifact names the authorized request digest;
- coordinator signs the plan artifact;
- participant verifies both the plan signature and Criome
  authorization.

Eventually, this may become a sema-engine slot relation rather than a
plain digest field.

## Update to report 138's open question

Report 138 asked which key should sign plan authority:

- operator identity key;
- coordinating daemon host key;
- cluster deployment authority key;
- sema-engine slot authorization through Criome/BLS.

The decision is now:

> permission comes from Criome-mediated authorization of the
> `signal-lojix` request object.

The coordinator may sign the derived plan for integrity, but that is
not the permission source. Criome's authorization object is.

## Recommendation

Implement authorization as its own prerequisite lane before expanding
distributed deploy effects:

1. define canonical digesting for `signal-lojix` requests;
2. add `signal-criome` authorization verbs;
3. add a `CriomeAuthorizationActor` in `lojix-daemon`;
4. add fake-Criome tests proving no Nix effect runs before
   authorization;
5. include the authorization object in the Arca deployment artifact
   set;
6. only then attach build/cache/import/activation actors to the
   authorized path.

This keeps the architecture clean: clients initiate, Criome authorizes,
Arca preserves exact artifacts, and `lojix` executes local deployment
effects through daemon-to-daemon coordination.
