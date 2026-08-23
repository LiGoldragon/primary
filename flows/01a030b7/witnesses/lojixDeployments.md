# Lojix deployments

Method: probe `LOJIX_ORDINARY_SOCKET=<configured ordinary socket> lojix 'Query.ByNode.(goldragon zeus None)'`.

## Observations

- Deployment 53 used immutable CriomOS `d04f6dafce19b7b4f093c35716739f36d75973ba` and terminally failed at `Activate` with `ActivationFailed`, after its closure copied successfully.
- Deployment 54 used immutable CriomOS `35fc6e9896d012bf6f54a9916bd8e725af3fcea0`; its `CompleteHost` `TestActivation` terminal record is `Completed` / `Succeeded` at state marker `(1246 1246)`.
- Deployment 55 used the same source; its `CompleteHost` `ActivateNow` terminal record is `Completed` / `Succeeded` at marker `(1284 1284)`.
- The accepted `Query.ByDeployment` request for deployments 30 and 53 failed in the ordinary-client ingress path with an EOF/WireShapeError. `Query.ByNode` supplied the terminal records above.

## Hypotheses

None. The direct-id query fault is distinct from the deployment terminal records.

## Unknowns

The public Lojix event-range query returned no event payload for deployment 53, so it does not supply remote activation stderr.
