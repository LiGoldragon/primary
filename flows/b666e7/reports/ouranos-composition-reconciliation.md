# Ouranos composition reconciliation

Evidence cut: 2026-09-29. This is a review artifact for Mind Astra’s joint
plan. It records what the evidence settles and leaves unresolved source and
Field questions explicit. No host command, build, deployment, or secret read
was performed for this report.

## Declared whole-system composition

The one acceptable Ouranos composition is a **CompleteHost-like whole-system
composition**, with the Home projection included and reviewed change by
change. The passive USB observer is one component of that composition. It is
not a second lifecycle, a parallel OS-only deployment, or a promotion toggle.
The observer owns neither routing nor network management: the USB module has
one manager, while the observer only observes passively. Any one runtime-only
transient observer witness is an allowed Field witness for the next physical
plug; it disappears at reboot and is never deployment evidence.

This follows Fable’s ruling: prove a way back on the target, and do not switch
until the dry plan proves that nothing unintended will stop. The current plan
therefore holds activation. The exact BaseHost artifact is useful evidence of
the observer closure, but its `includeHome=false/includeAllFirmware=false`
projection is not the settled long-term composition. The handoff records the
candidate and its source inputs, while also recording that its dry plan would
stop Home units ([observer handoff](../../d5b96b/reports/observer-deployment-handoff.md)).

## Change-wise reconciliation

| Identity | What it is | Evidence class and consequence |
|---|---|---|
| **R — `dbhsh7`** | Running `/run/current-system`, `nixos-system-ouranos-26.11.20260813.0e251e2` | **Direct Field observation.** This is the running system that must remain recoverable; it is not interchangeable with P, L, or C. |
| **P — `hm7z` generation 188** | Selected persistent boot/profile system path, a different store path from R | **Direct Field observation.** Generation 187 is not a tested rollback. P is the selected boot/profile identity, not proof that R can be restored safely. |
| **L — `41cvi`** | Historical/current Lojix `CompleteHost` generation 4, revision `36653a` (with UserEnvironment generation 27 at `cef111`) | **Direct Lojix readback, historical deployment state.** It is not a current BaseHost and must not substitute for R, P, or C. |
| **C — `hs9mi4`** | BuildOnly BaseHost candidate; NarHash `sha256-Td6ruNaeZqunzbMUXnBOHsMMMs4n2r0c6RJ06F9hQhI=`; includes the observer binary/unit | **Source/build receipt plus readback.** It is exactly `includeHome=false/includeAllFirmware=false`, so its closure inspection proves observer inclusion, not whole-system equivalence or safe activation. |

The only observed dry activation of C exited 0 and left the observed R/P
identities unchanged. Its planned reconciliation would stop
`home-manager-li.service`, `accounts-daemon`, `polkit`, and `tmpfiles-resetup`,
reload dbus, and restart nix-daemon. That fails the no-unintended-Home-change
gate. A historical R test exited 4 after stopping NetworkManager, restarting
Home Manager, and failing `tailnet-enroll`/NetworkManager-wait-online. It is
historical failure evidence, not a rollback procedure. The dry run also left
an empty `/run/secrets.d/3` residue; this records a runtime side effect but
does not prove that secret material never existed. No cleanup or secret-content
read is inferred ([handoff details](../../d5b96b/reports/observer-deployment-handoff.md)).

## Home, Codex, and ownership boundaries

Home is part of the composition. CriomOS constructs the canonical
`nixosConfigurations.target`; when `includeHome` is true it imports the
embedded Home Manager path, including `userHomes.nix`, which filters the
projected users and imports `inputs.criomos-home.homeModules.default`. The
`userHomes` selection is therefore a source projection decision, not a live
promotion switch ([architecture witness](../../0062e8/reports/current-architecture.md)).

Codex-next activation remains **HOLD**. The historical transient service/socket
collision is a stale operational witness and needs a fresh Field observation;
it cannot be promoted into a current fact or used to justify activation. The
current Codex source witness establishes a managed per-user
`codex-remote-control.service` and its private socket, while stable and next
surfaces are separate; it does not establish that a full Ouranos switch is
safe ([current Codex witness](../../ea1e56/witnesses/current-desktop-codex-state.md),
[stable/next handoff](../../9ddcbc/refresh-handoff.md)). The Home aggregate
auto-imports the Codex remote-control Min+ surface, but source review found no
observed enable option. Do not claim an automatic Codex promotion toggle.

The USB module has one service/network manager. The observer is passive and
must not acquire Router, recognizer, timer, or network ownership. The existing
network services (networkd, Kea, NetworkManager, firewall) were directly
observed active in the Field handoff; their ownership and any observer unit
delta still require the final Field review.

## Direct Field witness: downstream link

On 2026-09-29 at 18:05:46–18:06, Field Sol directly relayed a passive Ouranos
snapshot: USB NIC `enp0s20f0u1c2` was administratively UP but NO-CARRIER; the
sole `br-downlink` slave was disabled; the bridge was administratively UP but
NO-CARRIER; and its FDB count was zero. After the 15:26:41 carrier gain, the
recorded flaps were losses at 15:46:31 and 15:46:36, gains at 15:46:34 and
15:48:54, and final loss at 17:01:17. No USB disconnect/reprobe or networkd
restart was observed. Kea ACKed `10.44.0.10` at 15:48:54 with renewals through
16:55:36, but that client is not Zeus-confirmed. This is a direct Field
observation, not a causal conclusion: cable, adapter, power, and NIC causes
remain undifferentiated. The next discriminating witness is Zeus-console
power/link state, NIC carrier/MAC/address, and exact cable mapping
([Field source log](../../d5b96b/log.md)).

## Authored pins and source boundary

The reviewed BuildOnly packet names CriomOS
`0fe91588d60b642de851dee3f08073082989de2b`, Goldragon main `dc57e801` with
secrets identity `HRtH`, and Horizon only as the abbreviated materialized
`/nix/store/6i5…` (`M2LE`). The report must not silently turn those
abbreviations into full identities. The exact Home and Lojix pins, and their
consumer relationship, remain source-review questions; an older Home pin or
Lojix historical revision cannot be inferred from C. The source boundary is
CriomOS’s `nixosConfigurations.target` plus its declared projected Horizon,
deployment, system, and secrets inputs; `userHomes.nix` is the OS-to-Home
embedding boundary. Source review must reconcile the authored pins for
CriomOS, Home, Goldragon, Horizon, and Lojix before any candidate is called
the joint composition.

## Proposal and open questions

Adopt one CompleteHost-like composition only after Mind/source review settles
Home and Codex disposition and all five authored pins. Then Field must obtain a
fresh witness of the actual generated projection, unit delta, network/USB
ownership, and a target-proven restoration from the exact running R and
selected P states. Until those witnesses exist there is no safe switch, no
automatic Codex promotion, and no claim that a future full switch is safe.

Questions for that review are: which exact Home and Lojix commits are in the
candidate consumer; does the generated composition include the intended Home
users and Codex remote-control surface; what exact unit owns the USB module;
and can the target dry plan stop nothing outside the reviewed change set while
proving restoration of both R and P? The source agent’s finding that
CompleteHost imports Home/userHomes/broad firmware, while Home’s aggregate
auto-imports Codex remote-control Min+, is a source observation to verify
against the final pins, not permission to promote Codex.

The resulting judgment is deliberately narrow: whole-system composition,
Home included, reviewed change by change; one transient observer witness is
permitted as a witness only; no switch until the dry plan and way-back proof
close the unintended-stop and rollback gates.
