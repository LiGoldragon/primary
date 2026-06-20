# Cloud Cloudflare Token Test

## Scope

Psyche added a candidate Cloudflare secret at `gopass cloudflare.com/api-token` and asked for cloud testing. I treated this as authorization for non-destructive Cloudflare credential/API checks and local cloud repo checks only. I did not run DigitalOcean live lifecycle tests, daemon live activation, mutations, commits, or pushes.

`/git/github.com/LiGoldragon/cloud` was locked by `cloud-maintainer`, so I did not edit the repo.

## Results

- Original `gopass show -o cloudflare.com/api-token` value was 32 alphanumeric bytes and was rejected as an API token; the psyche later corrected that this had been the account id, not the token.
- After replacement, `gopass show -o cloudflare.com/api-token` succeeds with a 53-byte value. Secret bytes were not printed.
- `gopass show -o cloudflare/api-token` fails or is absent.
- With the corrected token, direct Cloudflare read-only zone listing returns HTTP 200, `success=true`, `count=5`, `total_count=5`.
- With the corrected token, `flarectl --json zone list` with `CF_API_TOKEN` populated from `gopass cloudflare.com/api-token` returns exit `0` and JSON list count `5`.
- With the corrected token, direct read-only DNS-record listing succeeds for all five visible zones, with counts `1`, `10`, `1`, `0`, and `1` respectively. Zone names, identifiers, and record contents were not printed.
- `https://api.cloudflare.com/client/v4/user/tokens/verify` still returns HTTP 401 / code `1000 Invalid API Token`; this conflicts with the successful zone and DNS-record reads, so it is not blocking the actual Cloudflare read path cloud uses.
- `cloud` currently packages the flarectl wrapper with `gopass show -o cloudflare/api-token`, not `cloudflare.com/api-token`.
- `cargo test --locked --features cloudflare --all-targets` passed.
- `cargo clippy --locked --features cloudflare --all-targets -- -D warnings` passed.
- `nix eval --raw .#packages.x86_64-linux.default.drvPath` passed.

## Interpretation

The local cloud code is healthy for non-live checks. The corrected token at `cloudflare.com/api-token` is now usable for the read-only Cloudflare paths cloud needs: zone list through both HTTP and `flarectl`, plus DNS-record listing through HTTP.

The remaining mismatch is repository wiring: the stored path differs from the path encoded in `cloud/flake.nix`, `cloud/README.md`, and `cloud/docs/first-cloudflare-slice.md`.

The psyche explicitly chose to change the repo convention to `cloudflare.com/api-token`. Spirit record `nsi2` was changed in place to make `cloudflare.com/api-token` the canonical cloud Cloudflare token path.

Code/doc patching is blocked by coordination: `cloud-maintainer` currently holds a broad `/git/github.com/LiGoldragon/cloud` lock, and the claim tool rejected the attempted narrow claim for `flake.nix`, `README.md`, `docs/first-cloudflare-slice.md`, and `INTENT.md`. The needed code/doc change is to replace `cloudflare/api-token` with `cloudflare.com/api-token` in those files once the lock owner applies it or the psyche explicitly authorizes a lock override.
