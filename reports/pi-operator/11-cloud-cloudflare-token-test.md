# Cloud Cloudflare Token Test

## Scope

Psyche added a candidate Cloudflare secret at `gopass cloudflare.com/api-token` and asked for cloud testing. I treated this as authorization for non-destructive Cloudflare credential/API checks and local cloud repo checks only. I did not run DigitalOcean live lifecycle tests, daemon live activation, mutations, commits, or pushes.

`/git/github.com/LiGoldragon/cloud` was locked by `cloud-maintainer`, so I did not edit the repo.

## Results

- `gopass show -o cloudflare.com/api-token` succeeds. The value is 32 alphanumeric bytes. Secret bytes were not printed.
- `gopass show -o cloudflare/api-token` fails or is absent.
- Cloudflare bearer-token verification against `https://api.cloudflare.com/client/v4/user/tokens/verify` returned HTTP 400 with Cloudflare error code `6003` and message `Invalid request headers`.
- `cloud` currently packages the flarectl wrapper with `gopass show -o cloudflare/api-token`, not `cloudflare.com/api-token`.
- `cargo test --locked --features cloudflare --all-targets` passed.
- `cargo clippy --locked --features cloudflare --all-targets -- -D warnings` passed.
- `nix eval --raw .#packages.x86_64-linux.default.drvPath` passed.

## Interpretation

The local cloud code is healthy for non-live checks, but the newly added gopass secret is not currently usable by the packaged Cloudflare path:

1. The stored path differs from the path encoded in `cloud/flake.nix`, `cloud/README.md`, and `cloud/docs/first-cloudflare-slice.md`.
2. The value at `cloudflare.com/api-token` is rejected by Cloudflare as a bearer API token before authorization reaches a zone-permission decision.

The likely next action is to either add the actual Cloudflare API token at `cloudflare/api-token` to match the repo, or have the `cloud-maintainer` lock owner intentionally change the repo wrapper/docs to `cloudflare.com/api-token` after confirming that path is the desired credential convention. The secret itself still needs to be a Cloudflare API Token bearer value, not another Cloudflare identifier or global-key credential.
