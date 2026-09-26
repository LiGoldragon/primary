# Field recovery launch packets

Prepared on 2026-09-26 after the power failure. These are launch plans only.
They create no Flow, Herdr, or Message record and launch no native seat.

`field-sol-of-b7da5d.profile.json` is the supported non-fresh Field Sol
successor profile. It preserves `b7da5d` through readiness and keeps that
seat's deployment ownership: Flow 0.17.1 deployment remains its work.

`field-luna-recovery.profile.json` is the supported *fresh* `gpt-6-luna`
recovery profile. The launcher authorizes that seat name only as `Field Ultra
Low`, so it deliberately does not assert that it replaces `e71dab`. Its source
bundle retains the applicable Luna lineage and the current instruction that
Luna executes authorized stop/start and reaping work after being told.

Both profiles require medium effort. `launcherClaimsIdentity: true` makes the
launcher claim the Flow ID before the only startup prompt and bind the native
title as `FieldV2.{ <mapped model> <FLOW_ID> }`. The launcher constructs the
prompt from the current `tools/main-flow-mode/system-prompt.md`, so its exact
main-flow text is the leading block; it follows with the typed startup skills
and the source-linked packet. Do not copy this mechanism into the obsolete
2026-09-24 `flows/752e0f/field-launch` files.

## Prelaunch checks

Run these from `/home/li/primary`; neither command starts a native thread:

```
node tools/native-seat-launch.mjs --seat field-sol-of-b7da5d --profile-file flows/56ae53/field-recovery-launch/field-sol-of-b7da5d.profile.json --predecessor b7da5d --cwd /home/li/primary
node tools/native-seat-launch.mjs --seat field-luna-recovery --profile-file flows/56ae53/field-recovery-launch/field-luna-recovery.profile.json --fresh --cwd /home/li/primary
```

Append `--prompt` to render and inspect the one exact startup input. A real
launch additionally requires the current runner hash, a new explicit receipt
path, and the launcher acknowledgement. It must then pass all readiness gates:

1. native receipt with one typed startup prompt, expanded `main-flow`, and a
   receipt-only first response;
2. launcher Flow-ID claim and V2 title set/readback;
3. exact Herdr binding; Flow registration; and Message/HM binding;
4. a verified routed reply and an accepted handoff before any predecessor is
   retired or a role is announced ready.

Current deployment context is a source-bound brief only: stable Flow 0.12.2
remains; Flow 0.17.1 and Message 0.17.0 need their projected-Horizon remote
build and declarative side-by-side activation. Do not restart Message or clean
up an old route from these packets.

## Field Astra assessment

No Astra profile is prepared. The 2026-09-26 nine-flow request calls for three
main powers across three aspects and describes Astra as the high model, but it
does not designate a new Field Astra successor or transfer work to it. Current
operational evidence reports Astra `6fe957` fully bound. A fresh Astra packet
would therefore create an unjustified duplicate or implied role transfer.
