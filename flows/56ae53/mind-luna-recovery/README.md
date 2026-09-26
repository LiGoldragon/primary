# Mind Luna recovery launch packet

Prepared on 2026-09-26 for the requested three-aspect by three-power recovery.
This is a launch packet only. It creates no Flow, Herdr, or Message record,
starts no native thread, and sends no message.

## Identity and lineage

`mind-luna-recovery.profile.json` defines a fresh `gpt-6-luna` Mind Low seat
at medium effort. The launcher claims a distinct Flow ID, sets and reads back
`MindV2.{ Luna <FLOW_ID> }`, and constructs the sole startup input with the
current structured `main-flow` block first. It then supplies every listed
startup-only skill and the bounded source manifest.

The latest genuine Mind Luna predecessor located is `23d977`. Its 2026-09-20
native receipt records `gpt-5.6-luna` at medium effort, a verified rollout,
and a historical Herdr/HM acknowledgement. It is evidence for unfinished Mind
Low work, not a live identity, route, or predecessor transfer. This new seat
is deliberately fresh and does not replace, retire, bind, or deregister it.

`flows/19ff9f/log.md` is an incomplete Field-Luna-adjacent coordination record.
It is included only as current raw context and must not be revived, adopted, or
treated as the Mind Luna predecessor.

## Recovery work

The first useful work is a read-only recovery census: identify one valid live
seat for every requested aspect/power cell, preserve predecessor and duplicate
evidence, and report the exact missing or duplicate cells. It must accept a
routed useful-work request only after all readiness gates below have evidence.
It does not launch, restart, retire, rebind, or send on behalf of another seat.

## Prelaunch proof

Run from `/home/li/primary`. These commands do not launch a native thread:

```
node tools/native-seat-launch.mjs --seat mind-luna-recovery --profile-file flows/56ae53/mind-luna-recovery/mind-luna-recovery.profile.json --fresh --cwd /home/li/primary
node tools/native-seat-launch.mjs --seat mind-luna-recovery --profile-file flows/56ae53/mind-luna-recovery/mind-luna-recovery.profile.json --fresh --cwd /home/li/primary --prompt
```

Do not run a live launch, Flow/Herdr binding, HM registration, or routed
request until Flow 0.17.1 and Message 0.17.0 pass the service gate and the
launcher can produce all of the following in one fresh receipt set:

1. one native startup input with expanded `main-flow` first and every startup
   skill injected;
2. launcher-claimed distinct Flow ID and read-back `MindV2` title;
3. exact live Herdr binding, Flow registration, and Message/HM binding; and
4. a routed useful-work request with a target-side accepted reply, recorded at
   its actual receipt grade.

The required accepted reply is a concise acknowledgement that identifies the
recovered census task and names the recipient binding used. A transport or
presentation grade alone does not satisfy it.

## Current gate

Flow 0.17.1 and Message 0.17.0 remain a future-build/service gate in the
available recovery evidence. This packet therefore has no ready claim and no
live command. The two prelaunch commands above are the concrete next action.
