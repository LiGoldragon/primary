# 8 · Open questions — psyche + cloud-operator

Per spirit 987 (cloud-designer scope principle), this report
carries TWO open-question sections — one for the psyche
(direction needed before implementation can proceed cleanly)
and one for cloud-operator (clarifications to resolve as
they implement). Passing forward open questions is part of
the lane handoff.

## For the psyche — direction needed before / during implementation

**P1. GPT-5.5 orchestrator integration shape.**
The three-tier picture (cloud GPT-5.5 → browser-use → atlas
Gemma → Chrome) is settled in concept. The cloud-side wiring
is unspecified. Two plausible shapes:

- **(a)** A new `signal-cloud` operation
  `RemoteBrowse(BrowseRequest)` whose handler invokes the
  cloud GPT-5.5 model to produce a stepwise plan, then
  spawns `browser-use` locally with each step's instruction.
  Routes cleanly through the cloud daemon's existing socket
  surface.
- **(b)** A new component (`browse-cloud`?) sibling to the
  cloud component, with its own triad. Cleaner separation but
  more substrate to maintain.

Which shape? My read says (a) is right because browser
control is a *use* of cloud-provider model APIs (GPT-5.5
counts), but I'd rather have your call before cloud-operator
starts wiring.

**P2. Where does the browser-use wrapper live in the nix
closure?**
Three plausible homes:

- Max's personal profile
  (`CriomOS-home/modules/home/profiles/max/`) — narrowest
  blast radius, available only to interactive sessions on
  Max's machine.
- System-wide on CriomOS (every host with browser support
  gets it) — broadest, also pulls atlas dependency into more
  hosts.
- A package in `CriomOS-pkgs` that other consumers opt into
  — middle ground.

Likely answer is Max's profile for now, but a system-wide
position becomes natural once `browser-use` is consumed by
non-interactive flows (e.g. the GPT-5.5 orchestration above).
What's your default?

**P3. Atlas authentication posture.**
Today: API key file at `/var/lib/llama/api-key` is empty,
server runs unauth. Report `0036-llm-api-key-review.md`
documents a known plan for declarative secret integration.
The browser-use wrapper sets `OPENAI_API_KEY` from gopass
(`atlas/llama-api-key`) with a `dummy` fallback. Three
postures:

- Keep unauth (gopass entry empty) — atlas is Tailnet-only
  so the trust boundary is the Tailnet.
- Populate gopass with a real key, populate atlas's key file
  the same way. Now atlas enforces it.
- Defer the decision; ship the wrapper with the fallback
  shape that works either way.

Which?

**P4. Gemma 4 gating / Unsloth proxy.**
`google/gemma-4-E4B-it` requires Google's acceptance click
on Hugging Face (gated). `unsloth/gemma-4-E4B-it-GGUF` is
the redistribution that sidesteps the gate. The design uses
Unsloth's GGUF because llama.cpp needs GGUF anyway. Is the
license-acceptance posture acceptable, or do you want the
fetcher to demand the official Google repo with explicit
token plumbing?

**P5. Where in the cluster does atlas actually live?**
Scout 2 found atlas is declarative-but-not-deployed. The
test fixture at
`CriomOS-test-cluster/fixtures/horizon/atlas.json` defines
hostname + node-type but no production host has
`behavesAs.largeAi=true` per the survey. Which physical or
virtualised node will be atlas? Or should it be a fresh
provisioning task before implementation begins?

## For cloud-operator — resolve as you implement

**O1. Branch landing shape.**
The prototype branch `designer-hf-prefetch-utility-2026-05-27`
adds files at `tools/` and `lib/`. Two judgement calls when
merging:

- Repo convention says `tools/` vs `scripts/` vs
  `bin/` — pick whichever matches existing structure.
- The smoke test (`tools/smoke-fetch-tiny-model.nix`) is a
  fixture that uses `<nixpkgs>` impurely. Keep as
  documentation, move to a `tests/` location, or remove
  before merge?

**O2. Extending llm.nix's `mkModelStorePath` dispatch.**
The existing `source.kind` enum handles `"multi-shard"` and
`"fetchurl"`. Adding `"hfModel"` requires extending the
dispatch in `CriomOS/modules/nixos/llm.nix`. Two sub-questions:

- Should `hfModel` source.kind ALSO support file-filtering
  (the prototype's `files = ["*Q4_K_M*.gguf"]` use case for
  multi-quant repos)?
- For backwards compat with the existing 8 `multi-shard`
  entries, leave them alone and use `hfModel` only for new
  additions? Or migrate them gradually?

**O3. browser-use packaging — Python derivation specifics.**
Per `CriomOS/reports/0031-browser-use-packaging-plan.md`,
browser-use is a Python project. Open: which
`buildPythonApplication` flavour, what Python version pin
(3.11? 3.12?), how to handle the `cdp-use` dep if it's not
in nixpkgs (vendored requirements? poetry2nix? pip install
in postInstall?). The pre-implementation plan should already
cover this — confirm during landing.

**O4. Gemma 4 multimodal in llama.cpp Strix Halo.**
The `llama-cpp-strix-halo` package at
`CriomOS/packages/llama-cpp-strix-halo.nix` is the Vulkan
build. Gemma 4 multimodal needs the LLaVA-style mmproj file
(per llama.cpp's vision support); confirm Strix Halo's
build flags include vision before assuming image input works.
If not: rebuild with `-DLLAMA_VISION=ON` or equivalent.

**O5. Token rotation for atlas.**
The browser-use wrapper fetches the token via `gopass show`
at every spawn. If atlas's API key changes (rotation), the
next browser-use invocation picks it up free. But if the
gopass entry is missing, the fallback is `dummy` which atlas
currently accepts (unauth). Once atlas enforces auth, the
`dummy` fallback becomes a silent failure. Switch the
fallback to a fail-loud `exit 78` (sysexits EX_CONFIG) per
the cloud cycle's audit finding D2.

**O6. Chrome dev port collision.**
Chrome on port 9222 is configured by hexis wrapper. If
browser-use spawns its own Chrome instance, it could collide
with the user's existing Chrome session. browser-use's docs
should be checked — does it attach to an existing CDP port,
or spawn fresh? If fresh, the port number needs separation
(9223? a randomly-allocated port?) so the user's interactive
Chrome stays usable.

**O7. End-to-end smoke recipe — non-destructive sites.**
The acceptance criterion is "navigate to example.com and
screenshot". example.com is a safe choice. For more
substantial smoke tests, what's the workspace policy on
hitting real services from automated browser tests? Probably:
keep smoke recipes against example.com / httpbin.org /
similar static targets, leave production-site automation to
deliberate manual runs.

## How to track resolution

The five psyche questions are dependencies on cloud-operator
unblocking. Recommend filing them as `bd` items with
`role:psyche` style label so they surface as blockers in
`bd ready`. Or simpler: psyche replies in chat, this report
gets a follow-up `8a-answers.md` superseding the relevant
items.

The seven operator questions live with the work; each bead's
acceptance can grow a note as operator settles the answer
during implementation.
