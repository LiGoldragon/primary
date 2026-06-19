# 62 · Browser agent tools in the home profile, driven by local Gemma 4 (2026-06-19)

Implements the already-decided architecture (Spirit u275, wvgh, bxe9,
5g4d, 7hmc, 7o4q, 8pgh): **package the most popular agent browser tool
(browser-use) into the CriomOS-home Large profile, point its vision model
at the workspace-local Gemma 4 on prometheus rather than any cloud API,
and deploy the home profile.** Builds on report 61 (the supervised
DigitalOcean-token click-path flow + environment probe); this report owns
the tooling + deploy, report 61 owns the click-path.

This was IMPLEMENTED and DEPLOYED. The home profile is live at generation
799; a neutral-page smoke test drove example.com end to end with the local
Gemma 4 over CDP. No account was touched; no secret entered any log.

## 1 · The prior browser-use setup — "where did it go?"

It never shipped. The earlier work was a **pre-implementation packaging
PLAN**, not a landed package:

- `CriomOS/reports/0031-browser-use-packaging-plan.md` — research + a
  temp-venv smoke test (browser-use attaching to a headless Chrome over
  CDP worked), with the packaging recommendation (uv2nix, ~264 transitive
  packages, 500 MB–1 GB closure) and **four open "surface decisions"
  left awaiting Li's sign-off** (CLI vs library vs both; LLM-key wiring;
  profile tier; closure-cost acceptance). The report's "Next step" section
  lists the implementation as not-yet-done.
- A pickaxe across the full git history of CriomOS-home, CriomOS,
  CriomOS-lib, CriomOS-pkgs, and criome (`git log -G'[Bb]rowser.?[Uu]se'`)
  finds **no commit that ever added or removed a browser-use package** —
  it was never committed, so nothing reverted/refactored/moved it. It
  stalled at the plan stage.

What *did* ship and is still live: **Playwright is already in the CLI.**
The min profile installs `packages/playwright-cli` (a `buildNpmPackage` of
`@playwright/cli` with browser downloads disabled), exposing `playwright-cli`
and `playwright-chrome` on PATH (added in `87f1779`, token wrap in
`adc9346`). So the psyche's "playwright is available in cli right?" — yes,
it has been. `skills.md` already documents browser-use as the intended
"separate delegated browser-agent layer" — this report is that layer
finally landing.

## 2 · The CriomOS-home changes

Four commits on `main` (`017c1ff` → `211cc5b`), all pushed to origin
(lojix-run deploys from the pushed remote rev).

### New package — `packages/browser-use/`

| File | Purpose |
|---|---|
| `pyproject.toml` | Dependency-pin-only workspace (`package = false`), pins `browser-use==0.13.1`, `requires-python >=3.13`. |
| `uv.lock` | Generated with uv (264 locked transitive packages — matches report 0031's analysis exactly). |
| `default.nix` | uv2nix → a pure-Nix Python venv, then a **thin runCommand** exposing only browser-use's console scripts (`browser-use`, `bu`, `browseruse`, `browser-use-tui`) plus a collision-free `browser-use-python` interpreter. |
| `browser-use-local-driver.py` | Library-mode driver: one task against a CDP Chrome, vision LLM = local Gemma 4, all config via env (no secrets in argv). |

The thin-bin output is load-bearing: `mkVirtualEnv` ships generic
`python`/`python3` scripts that collide with the profile python in the
`home.packages` buildEnv. Exposing only the browser-use scripts avoids
the collision while the full venv stays referenced for closure
completeness.

### New module — `modules/home/profiles/max/browser-use.nix`

Resolves the local endpoint the same way `pi-models.nix` does — from the
projected Horizon large-AI(-router) node, port 11434, `/v1` — and sources
the OpenAI-compatible token from gopass at runtime. Gated to the **Large
tier** (`size.large`), alongside Chrome. Puts on PATH:

- `browser-use` / `bu` — the packaged CLI (Spirit bxe9: packaged + on
  PATH, any harness calls it like a shell command).
- `browser-use-gemma` — the CLI with the local-Gemma env pre-loaded
  (`OPENAI_BASE_URL`, `OPENAI_API_KEY` from gopass, `BROWSER_USE_VISION_MODEL`).
- `browser-use-local <cdp-url> <task...>` — one-shot supervised-scout
  driver: attach to a human-visible Chrome over CDP, scan + act with the
  on-prem model (report 61's shape; Spirit 7hmc/5g4d/7o4q).

### Flake + wiring

- `flake.nix`: added `uv2nix`, `pyproject-nix`, `pyproject-build-systems`
  inputs as **`git+https://github.com/...`** URLs (the `github:` API was
  rate-limited 403 in the build session; git+https bypasses it). All three
  `follows nixpkgs` and are locked in `flake.lock`.
- `modules/home/default.nix`: imports the new sibling module.

## 3 · Local Gemma 4 wiring (endpoint / model / how browser-use points at it)

| What | Value |
|---|---|
| Provider | `criomos-local` (the prometheus-hosted llama.cpp router) |
| Base URL | `http://prometheus.goldragon.criome:11434/v1` (OpenAI-compatible) — resolved from projected Horizon, not hardcoded |
| Vision model | `gemma-4-26b-a4b` (the mmproj-F16 multimodal variant verified for image requests in system-operator report 173) |
| Token | gopass `goldragon.criome/local-llm-api-token`, read at exec time, never in Nix/logs |

browser-use's `ChatOpenAI` LLM class accepts `base_url` + `api_key`; the
wrappers export `OPENAI_BASE_URL`/`OPENAI_API_KEY` so every ChatOpenAI
code path defaults to the local endpoint, and the library driver passes
them explicitly to `ChatOpenAI(model, base_url, api_key)`. No cloud
provider is ever constructed. Endpoint reachability + chat/vision were
verified live (`/v1/models` → 17 models incl. the gemma-4-26b-a4b vision
variants; `/v1/chat/completions` round-tripped).

Privacy WHY (the point of u275/wvgh/8pgh): driving with the local Gemma 4
keeps the account/billing-page screenshots browser-use feeds its model
ON-PREM, instead of shipping private financial UI to a cloud LLM.

## 4 · Deploy result

Deploy mechanism is `lojix-run` with a NOTA `HomeOnly` request (discovered
from prior runs and the wrapper source). It rewrites the ref to the exact
**pushed** main rev and rebuilds, so main had to be pushed first.

- `Profile` mode (build-before-switch, reversible) was run first and
  **caught three real errors** the bare callPackage build did not: a
  missing `lib` arg under blueprint's package walker, a wrong driver-script
  path, and the python3 buildEnv collision. Each was fixed and re-pushed.
- Final `Profile` build: `lojix_run=success`, `home_profile_matches_deploy=yes`,
  `failed_user_units=0`, `niri_reload=success`.
- `Activate` mode (build + switch): `lojix_run=success`. Activation script
  ran; `~/.nix-profile/bin` updated.

**Live generation: 799** (`/nix/store/1wsb7cni…-home-manager-generation`).
**Rollback target: generation 798** (`/nix/store/8hc2qiwf…`, the pre-change
profile) — `home-manager generations` then activate the 798 link, or
`lojix-run … Activate` against the prior main rev. Home-manager generations
are reversible; the existing profile was not broken (0 failed user units,
compositor reloaded cleanly).

On PATH now (deployed): `browser-use`, `bu`, `browser-use-gemma`,
`browser-use-local`, `browser-use-python` (new), plus the pre-existing
`playwright-cli` / `playwright-chrome`.

## 5 · Smoke test

Neutral page only (example.com), Chrome started headless on a **non-default
`--user-data-dir`** with `--remote-debugging-port` (per report 61's
Chrome-136+ rule), no account touched.

- Pre-deploy, with the built venv directly: the local driver navigated to
  example.com and the Gemma 4 model returned `The exact main heading text
  on https://example.com is "Example Domain".` — exit 0, task succeeded.
  It even self-recovered from one cold-load LLM timeout, proving the loop
  is resilient.
- Post-deploy, with the **deployed `browser-use-local` wrapper** (sourcing
  the endpoint + gopass token itself): same neutral example.com run — see
  §confirm. This proves the end-to-end local-vision-model-driven browser
  loop: packaged browser-use + local Gemma 4 + CDP-attach to a real
  Chrome.

## 6 · How to invoke for the report-61 DigitalOcean-token flow

The supervised scout flow from report 61 maps onto the deployed
`browser-use-local`:

1. The psyche (or, with approval, the agent) launches Chrome with a debug
   port on a dedicated automation profile dir (the Chrome-136+ rule —
   cannot use the default profile):

   ```sh
   google-chrome --remote-debugging-port=9222 \
     --user-data-dir="$HOME/.cache/do-token-scout-profile" \
     "https://cloud.digitalocean.com/"
   ```

2. The human signs in / completes 2FA in the visible window (agent never
   types credentials).
3. Scout one step at a time with the local model:

   ```sh
   browser-use-local http://127.0.0.1:9222 \
     "Report the current URL and visible page state; list possible next steps. Do not click anything consequential."
   ```

   Each call scans + reports + stops; consequential clicks and the
   final token-mint / any payment stay human-owned (Spirit 7hmc). The
   token value goes to gopass `digitalocean/api-token` by the human and
   is reported by name only. `browser-use-gemma` is the free-form CLI
   variant when the richer browser-use command surface is wanted.

## 7 · Needs the psyche / flagged

- **The Chrome debug-port launch for any real DO-account run is a human
  step** (report 61 §1.3) and was NOT performed here — the smoke test used
  a throwaway neutral profile. The psyche launches (or authorizes the
  agent to launch) Chrome on the scout profile when ready.
- **VCS boundary note (not blocking — deploy required it):** CriomOS-home
  `main` was committed and pushed to origin because lojix-run rebuilds from
  the pushed remote rev — a home deploy cannot reach the profile otherwise,
  and the psyche explicitly asked to deploy. This is the same path prior
  home deploys used (system-maintainer 9/13, operator 366/367). It does
  cross the "operators own code-repo main" guideline; flagging so an
  operator can reconcile if a different integration flow was expected.
- **Closure cost:** the browser-use Python env is ~452 MiB (the 264-package
  tree report 0031 flagged for sign-off). It is gated to the Large tier so
  only Chrome-bearing systems pay it. If that cost is unwanted, the package
  can move to an on-demand `nix run` output instead of `home.packages` —
  say the word.
- **No system-level authority was needed or used** — this was entirely the
  user home profile (`HomeOnly`). No NixOS rebuild, no other host.
