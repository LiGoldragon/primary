# Audit — Spirit captures `hcp8`/`iprx`, cloud `INTENT.md`, active-repositories

Sub-agent audit (read-only) of the durable artifacts produced this session:
the two new Spirit records, the cloud-designer-intent-refresh `INTENT.md`, and
the `protocols/active-repositories.md` cloud / domain-criome rows. Every claim
is cited to `file:line`, Spirit `(Lookup …)` output, or git history. Production
behavior is distinguished from report/test assertions throughout.

## Verdicts at a glance

| # | Claim / artifact | Verdict |
|---|---|---|
| 1 | `hcp8` — DO is lead, supersedes `g7zd` | Stands (with note: `g7zd` retired, not a recorded supersession edge) |
| 2 | `g7zd` correctly superseded, no orphaned intent | Stands |
| 3 | `iprx` — credential custody → system creds | Stands (one overstated cross-ref: "sops-nix … of h03z") |
| 4 | INTENT.md: DO handle `DIGITALOCEAN_ACCESS_TOKEN` | Stands |
| 5 | INTENT.md: Hetzner handle `HCLOUD_TOKEN` | Stands |
| 6 | INTENT.md: Cloudflare handle `CF_API_TOKEN` | Overstated — conflates daemon-read handle with the env var `flarectl` reads |
| 7 | INTENT.md gopass paths (DO, Hetzner) | Stands |
| 8 | INTENT.md gopass path (Cloudflare `cloudflare/api-token`) | Stale-risk — report 69 (same session) flags it should be `cloudflare.com/token` |
| 9 | active-repositories cloud row | Stands |
| 10 | active-repositories domain-criome row | Stands |

## 1 · `hcp8` — DigitalOcean is lead, supersedes `g7zd`

`(Lookup hcp8)` returns a well-formed `Decision` under topic
`(Technology (Software (Engineering Architecture)))`, magnitude `High Minimum
Zero`, domain vector `[cloud DigitalOcean Hetzner]`. Body: DO is the lead
compute provider superseding the earlier Hetzner-lead position; Hetzner remains
built/supported but not lead; DO bills by second/minute so the `6ks1` reuse
pool is unnecessary for it; Hetzner hourly reuse still applies.

Correctly scoped and not over/under-stated. It does NOT carry a bare opaque
identifier in the body where one would mislead — it names `6ks1` with prose
context ("the billing-hour reuse pool of record 6ks1"). The cross-reference to
`6ks1` resolves (`(Lookup 6ks1)` = `RecordFound`).

Note on "supersedes `g7zd`": the body does not cite the literal id `g7zd`; it
says "superseding the earlier Hetzner-lead position." The session frame doc
(`0-frame-and-method.md:11-12`) is what labels this "supersedes g7zd." `g7zd`
itself is the record prior reports called "the DigitalOcean per-second provider"
(report `60:3`, report `65:314`). It now returns `(Error [record not found])` —
genuinely retired/removed, not merely a lookup quirk (a sibling lookup of `150a`
in the same call returned `RecordFound`). Spirit exposes no `History`/
`Supersededby` input variant (`unknown Input variant History`), so there is no
machine-readable supersession edge to verify — the supersession is by-removal +
new-record, which is consistent with the workspace edit-existing flow.

## 2 · `g7zd` superseded cleanly — no orphaned or duplicated intent

- `g7zd` no longer resolves; its DO-lead intent now lives wholly in `hcp8`.
- No duplicate live record carries the Hetzner-lead position: a
  `PublicTextSearch [Hetzner lead compute provider]` surfaces `hcp8` (the
  superseding record), `6ks1`, `150a` (next-capability provisioning), and
  `mcwa` (cloud is the home for provider machinery, incl. Hetzner) — none
  re-asserts Hetzner-as-lead. `150a` and `mcwa` are adjacent, not duplicative.

Verdict: clean supersession, no orphaned/duplicated intent.

## 3 · `iprx` — credential custody → system credentials

`(Lookup iprx)`: `Decision`, topic `(Technology (Software (Security
SecretsManagement)))`, magnitude `Low Minimum Zero`, domain vector
`[cloud meta-signal-cloud CredentialHandle]`. Body: the current model — a
wire-supplied `CredentialHandle` the daemon resolves to a process env var behind
the `0o600` owner socket — is the accepted transitional shape; the eventual
direction is system-custodied machine credentials following the criome-custodied
and sops-nix machine-identity pattern of `h03z`.

Grounding:
- "wire-supplied CredentialHandle the daemon resolves to a process env var" —
  exactly what `EnvironmentCredentialSource::token` does:
  `std::env::var(handle.as_str())` (`src/cloudflare.rs:53`, `src/digitalocean.rs:84`,
  `src/hetzner.rs:71`). Stands.
- "behind the 0o600 owner socket" — grounded: `META_SOCKET_MODE: u32 = 0o600`
  (`build.rs:12`), daemon defaults the meta socket to `SocketMode::new(0o600)`
  (`src/schema/daemon.rs:189`). Stands.
- Magnitude `Low` correctly marks this as a low-certainty directional decision
  (transitional shape accepted, eventual direction stated). Appropriately scoped.

One overstated cross-reference: iprx attributes a "criome-custodied AND sops-nix
machine-identity pattern" to `h03z`. `(Lookup h03z)` is purely about lojix
custodying its operational credentials / unattended machine identity through
**criome** (rather than borrowing the operator's GPG/SSH agent session). h03z
does NOT mention sops-nix. The criome-custody half is grounded in h03z; the
"sops-nix" half is not in h03z (`PublicTextSearch [sops-nix]` does not place it
in h03z). The directional intent is sound; the specific "sops-nix … of h03z"
attribution overstates what h03z says. Minor — does not undermine the record.

## 4-6 · Credential-handle env-var names — the central check

The mechanism is data-driven, NOT hardcoded per provider. Each adapter's
production `EnvironmentCredentialSource` resolves the token by reading the
environment variable **named by the handle the wire supplied**:

```
std::env::var(handle.as_str())            // cloudflare.rs:53, digitalocean.rs:84, hetzner.rs:71
```

The handle is whatever a `RegisterAccount` meta operation carries
(`src/lib.rs:1392 register_account`). So "the handle" is the
`RegisterAccount`-supplied env-var name, exactly as the prompt frames it.

**DigitalOcean — `DIGITALOCEAN_ACCESS_TOKEN` — Stands.** The daemon reads the
REST API in-process, so the handle IS the env var the daemon reads. The doc-
comment convention and the `TOKEN_ENVIRONMENT_VARIABLE` constant agree
(`src/digitalocean.rs:79`), the flake injects it from gopass
(`flake.nix:71,98,116`), and tests register the account with this exact handle
(`tests/digitalocean.rs:127` etc.). Grounded end to end.

**Hetzner — `HCLOUD_TOKEN` — Stands.** Same in-process REST shape; constant at
`src/hetzner.rs:66`, flake injection `flake.nix:59,97`, tests
`tests/hetzner.rs:123` etc. Grounded.

**Cloudflare — `CF_API_TOKEN` — Overstated / conflated.** Cloudflare is NOT
read in-process; it shells out to `flarectl`. The token flow has TWO distinct
names that INTENT.md collapses into one:

1. The daemon resolves the handle: `std::env::var(handle.as_str())`
   (`cloudflare.rs:53`). The handle is whatever `RegisterAccount` supplied. The
   only in-repo evidence of a registered Cloudflare handle is the runtime tests,
   which use `CLOUDFLARE_DNS_TOKEN` (`tests/runtime.rs:470,513,561,…`) — NOT
   `CF_API_TOKEN`.
2. The resolved `Token` value is then handed to the `flarectl` subprocess via
   `.env(TOKEN_ENVIRONMENT_VARIABLE, token.as_str())` where
   `TOKEN_ENVIRONMENT_VARIABLE = "CF_API_TOKEN"` (`cloudflare_cli.rs:18,50`).
   So `CF_API_TOKEN` is the env var **`flarectl` reads downstream**, not the
   handle the daemon reads.

`CF_API_TOKEN` is therefore real and grounded (`cloudflare_cli.rs:18`,
`flake.nix:46`, README:14), but INTENT.md's line "Cloudflare from `CF_API_TOKEN`"
— presented in parallel with the DO/Hetzner handles as "the env var the daemon
reads via the credential handle" — is inaccurate for Cloudflare. The daemon-read
handle and the flarectl-read env var are different layers; the in-repo handle is
`CLOUDFLARE_DNS_TOKEN`. Not invented, but mis-attributed.

## 7-8 · gopass paths

- DO `digitalocean.com/api-token` and Hetzner `hetzner/api-token` match the
  flake (`flake.nix:71` / `:59`). Stands. The DO `.com` form is the corrected
  one: git shows `7f190c3 cloud: read DigitalOcean token from domain gopass
  path` moved it to `digitalocean.com/api-token`; bead `primary-hpkj` records
  the P0 "digitalocean/api-token -> digitalocean.com/api-token" fix as landed at
  `3b38cdd`.
- Cloudflare `cloudflare/api-token` matches the current flake (`flake.nix:46`),
  README (`:15`), and `cloudflare_cli.rs` convention — so INTENT.md faithfully
  documents today's code. BUT the same session's report `69:128-131` explicitly
  recommends this should become `cloudflare.com/token` ("same fix shape as the
  DO `.com` correction"), and DO already took that `.com` correction. So
  INTENT.md codifies a path the session itself flags as wrong-direction. Stale-
  risk: either the report-69 recommendation should be retracted, or INTENT.md +
  flake should move to `cloudflare.com/token`. The actual gopass entry name is a
  secret-store key not inspectable here, so the true ground truth is unverified —
  flagging the internal inconsistency rather than asserting which is right.

## 9-10 · active-repositories.md cloud / domain-criome rows

`cloud` row (`active-repositories.md:91`): DigitalOcean/Hetzner/Cloudflare
adapters — confirmed (three adapter modules). "single `EngineActor` over a
synchronous sema-engine `Store`" — consistent with `handle_ordinary_request`/
`handle_meta_request` synchronous signatures (`src/lib.rs:657,671`).
"DigitalOcean is the only compute provider shipped in a daemon build
(`apps.daemon-digitalocean`)" — `apps.daemon-digitalocean` exists in flake
(`flake.nix:194`) on both the branch and `main`. Birth bead `primary-kbmi`
CLOSED — confirmed (`bd show primary-kbmi` = CLOSED, close reason cites cloud +
domain-criome main shipping daemon + thin CLI). Land/hardening tracked by
`primary-hpkj` — confirmed OPEN, P2. Stands.

`domain-criome` row (`active-repositories.md:94`): "daemon + thin CLI ship with
sema-engine persisted registry state (birth bead `primary-kbmi` closed)" —
`primary-kbmi`'s close reason explicitly names "domain-criome … sema-engine
persisted registry state." Repo exists with `main` at `271bddc`. Stands.

## Net

Both new Spirit records are well-formed, correctly scoped, and free of orphaned/
duplicated intent; `g7zd` is cleanly retired. Two corrections for the INTENT.md
on the cloud-designer-intent-refresh branch: (1) the Cloudflare credential line
conflates the daemon-read handle (`CLOUDFLARE_DNS_TOKEN` in-repo) with the env
var `flarectl` reads downstream (`CF_API_TOKEN`); (2) the Cloudflare gopass path
`cloudflare/api-token` contradicts this session's own report-69 recommendation
to use `cloudflare.com/token`. One minor blemish in `iprx`: the "sops-nix …
pattern of h03z" attribution overstates h03z (criome-custody only). The
active-repositories rows are accurate.
