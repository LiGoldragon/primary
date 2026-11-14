# Final Home proof non-activating realization

## Terminal result

Deployment `543` realized proof consumer
`1d3cee5405ad30ad02d50edaf8f70376e7eee930` successfully.

- Watcher `71` acknowledged `Watching` at marker `13001` before submission.
- The request was submitted exactly once and admitted at marker `13002`.
- The stream observed `Submitted`, `Building`, then `Completed Some.Succeeded`
  at marker `13017`.
- The watcher was closed at terminal; the Lojix journal records
  `DeploymentWatchEnded.{ 71 PeerClosed }`, and no watcher process remains.
- One post-terminal `Query.ByDeployment.{ 543 }` confirmed
  `UserEnvironment.Realize`, `ProfileOnly`, `RequireImmutable`, the exact proof
  revision, and `Completed / Some.Succeeded`.

Realized output:

- derivation: `/nix/store/8rbsavzw9wx31m2jg2ji9h76x7qw6s9x-home-manager-generation.drv`
- output: `/nix/store/jj5mqpvl7jrwsjz320lbh9873ymcmp0z-home-manager-generation`

The deployment-to-output association is retained as a bounded exact match from
Lojix Memory in `raw/deployment-543-job-association.txt`. Read-only target Nix
queries independently confirm the output/derivation pair in
`raw/target-output-validation.txt`.

## Exact generated input references

```text
horizon=path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon?narHash=sha256-9n6IJ%2BTIk7SkREyhSXVz%2FZP%2FhS3iYc%2BgVdPG5g0rDq8%3D
system=path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system?narHash=sha256-KW3DUTifDJ6m2JuYiTVtJz%2B9ieAgqjCb46wgrMqxJJU%3D
deployment=None
secrets=path:/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/secrets?narHash=sha256-UXfrzp0B%2BuwSwvYhoW8v9Hg9tTtsJire8YmSf4h8SDQ%3D
```

The three references were re-hashed from the exact Lojix-generated input
folders and matched against the exact references retained in Lojix Memory.
Pinned Lojix revision `da0ad8ad363efe6751efe7e8f01f974bdd10cf06`
explicitly maps `UserEnvironment` to no generated `deployment` override; the
deployment path is absent. This is the contract result, not a guessed
replacement. `generated-input-contract.txt`, `generated-input-refs.txt`, and
`raw/lojix-memory-generated-ref-matches.txt` retain the evidence. Secret
contents were never written to this report or its evidence.

## Request and preflight

`request.datom` is the retained stage-one request with exactly one replacement:
the obsolete consumer revision became final proof revision `1d3cee…`; every
other byte-level field stayed fixed. It names `Realize RequireImmutable`,
`Horizon`, `homeConfigurations.li.activationPackage`, the explicit li/ouranos
transport, existing proposal and secrets directory, configured builder, and no
extra substituters.

Before submission:

- the explicit user destination reported hostname `ouranos` and user `li`,
  matching logical target `goldragon/ouranos/li`;
- the proposal was an existing absolute regular non-symlink;
- the secrets input was an existing absolute directory non-symlink; contents
  were suppressed;
- Lojix was active/running with PID `1637` and invocation
  `cab761e707f94dfeb26321aa7b6599e7`;
- no earlier watcher process existed;
- the pinned streaming watch contract was verified from source.

## Unchanged live state

Independent post-state reads show these are byte-identical to pre-state:

- Home Manager profile;
- user profile;
- system profile;
- runtime system;
- target hostname/user;
- Lojix active/substate, PID and invocation.

`state-comparison.tsv` holds the exact pairs. No activation, SetProfile, boot,
replay, service action, protected-network action, retry or main promotion was
performed.

## Evidence

- `request.datom`, `request-delta.txt`, `request.sha256`
- `watcher-contract.txt`, `generated-input-contract.txt`
- `pre-state.txt`, `post-state.txt`, `state-comparison.tsv`
- `raw/watch.log`, `raw/admission.txt`, `raw/record.txt`
- `generated-input-refs.txt`, `raw/generated-input-hashes.tsv`
- `raw/deployment-543-job-association.txt`
- `raw/target-output-validation.txt`
- `raw/lojix-memory-generated-ref-matches.txt`
- `raw/lojix-journal.txt`
