# 4 · Overview — what's done, and the deploy decision

## Done this cycle (safe, in-lane, reversible) — all blind

1. **Secret-handling discipline documented.** New skill
   `skills/secrets.md` (Craft / Keystroke), registered in
   `skills/skills.nota`: the never-show absolute, the gopass-wrap
   pattern at the daemon-wrapper layer, minting blind, the sops-nix
   host mechanics, and the blind gopass→sops bridge. Per intent
   1011–1014.

2. **Token minted into gopass.** `goldragon.criome/local-llm-api-token`
   — 256-bit, generated from `/dev/urandom` and piped straight into
   `gopass insert`. The mint script was made openssl-free first
   (openssl is absent locally). Verified by exit code + entry name;
   **the value was never displayed.** (Mint script improvement is on
   branch `designer-hf-prefetch-utility-2026-05-27` @ `74d19a96`.)

3. **Token sops-encrypted for prometheus.**
   `goldragon/secrets/local-llm-api-token.sops`, created by
   `gopass show -o ... | sops --encrypt --age <prometheus> ...` — the
   plaintext flowed gopass→pipe→sops, never to a terminal or argv.
   Verified blind: `DATA-ENCRYPTED-OK`, sole recipient = prometheus's
   age key (derived two independent ways). **Uncommitted** in the
   goldragon checkout.

So the token now exists in both layers (gopass session + sops
ciphertext) and prometheus can decrypt it. The discipline the directive
asked for is captured.

## Why the deploy is not a bulldoze

The research (which the directive explicitly asked for — "research how
you would do this cleanly") found the clean path is gated by two things
on the **system-operator** surface:

- **A.** `lojix-cli` hardcodes the secret set — deploying ANY new sops
  secret needs a Rust change to the cluster deploy tooling (file 1).
- **B.** system-operator has an **in-flight reconcile** of the exact
  module + inventory I'd edit: `horizon-re-engineering` moves the model
  inventory to `horizon.cluster.aiProviders` (deleting `llm.json`) and
  already carries the full sops `resolveSecret` api-key wiring (file 2).
  Editing `llm.nix` / `llm.json` on main now would likely be obsoleted
  by this reconcile and could collide with their work.

Plus two Gemma specifics: the prefetched hash is a `fetchHfModel`
snapshot hash (not a per-file `fetchurl` sha256), and multimodal needs
an mmproj fetch + `--mmproj` wiring that doesn't exist — **text-only
Gemma 4 is clean today; vision is a follow-up.**

## Recommendation

Coordinate, don't bulldoze. The secret is prepped and verified; the
deploy wiring lives on system-operator's surface and overlaps their
in-flight reconcile. Cleanest: land the api-key onto the
`horizon-re-engineering` `resolveSecret(Sops)` mechanism (which already
does exactly this) **with** system-operator, and add Gemma 4 (text-only
first) as a typed `aiProviders` model there. Deploy with
`builder = prometheus` (file 3) once wired.

The alternative — push the whole thing through on `main` now (extend
`llm.nix` for sops + `hfModel`, edit `lojix-cli`, deploy) — is higher
momentum but edits production deploy tooling and races the reconcile.

## Open questions

### For the psyche

- **Deploy path:** coordinate the wiring onto the horizon reconcile
  (recommended), push through on main now, or deploy the Gemma model
  text-only now and wire auth as a separate coordinated step?
- **Gemma scope:** text-only now with multimodal as an immediate
  follow-up (recommended — mmproj isn't wired), or block on full
  multimodal?
- **goldragon push:** the encrypted `.sops` file is uncommitted. OK to
  commit it to goldragon (it is ciphertext, the established pattern)
  when the path is chosen?

### For system-operator (the lojix-cli + llm.nix owner)

- Will the `resolveSecret(Sops)` api-key wiring on
  `horizon-re-engineering` carry a binding for the llm api token
  (name `localLlmApiToken`?) pointing at
  `goldragon/secrets/local-llm-api-token.sops`?
- Generalize `lojix-cli/src/artifact.rs` to enumerate `secrets/`
  rather than hardcode each file? That unblocks every future secret.

### For cloud-operator

- Once `fetchHfModel` lands (bead `primary-3dqf`) and CriomOS bumps its
  CriomOS-lib lock, add Gemma 4 via a `kind: "hfModel"` inventory entry
  using the existing snapshot hash, plus the mmproj fetch for vision.

## Anchors

- Skill: `skills/secrets.md`; index `skills/skills.nota`.
- Secret artifacts: gopass `goldragon.criome/local-llm-api-token`;
  `goldragon/secrets/local-llm-api-token.sops` (uncommitted).
- Branch: `designer-hf-prefetch-utility-2026-05-27` @ `74d19a96`.
- Deploy command: file 3.
- Intent: spirit 1011–1017.
