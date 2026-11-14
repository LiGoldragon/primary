# Psyche criomos Opus d35ae7: handover, 2026-11-11 11:05 CST

State log: flows/d35ae7/state.md. Deploy requests and await-watch.sh (opens a Lojix watch, submits, reads to the terminal): flows/d35ae7/. Worktrees in /tmp/claude-1001/-home-li-primary/d719b84f-596f-53d5-a309-d47d53d60e0a/scratchpad/: system (CriomOS, branch tether-d35ae7), home, pkgs. Root on a host: ssh root@<host>. Wait on a unit with systemctl start --wait or journalctl -f, never a shell loop.

## Done
Kernel 7.3.3 on ouranos, prometheus, zeus (switched, not rebooted); CriomOS main abab7243. herdr sound off; orchestrate on a fresh store; updater run proved (l33p Done). All of d719b8's requests answered.

## Pursuing, first: USB tether declared (8eoo, from Psyche core Fable)
- Cause on ouranos: the Pixel is classified uplink and gets its lease at once, but the wired NIC to prometheus held the default route (metric 100 vs 101) and prometheus has no upstream. Runtime fix: nmcli metric 50 on "Wired connection 2". Fable told (vbg9).
- Declared in CriomOS branch tether-d35ae7 5fe3933a (pushed, NOT main): networkd owns every uplink on every node (04-usb-uplink, NM_UNMANAGED where NM runs, networkd wait-online off there), option criomos.usbEthernet.uplink.routeMetric 50 and linkGroup 64; router sets 2048 and forwards/masquerades oifgroup 64 as the backup WAN. checks/usb-ethernet-roles updated and passes (build it with an impure expr, the flake checks set trips on old sema elsewhere).
- Realize at 5fe3933a: prometheus 463 Succeeded; ouranos 461 and zeus 462 were Building. Next: when both succeed, ActivateNow each with flows/d35ae7/<host>-host-ActivateNow.datom (ouranos last: its switch restarts yggdrasil, the mesh drops about a minute). Then on ouranos check the tether is networkd's (networkctl, default via the phone at metric 50), the dongle still bridges into br-downlink, then fast-forward CriomOS main to 5fe3933a. Prometheus as backup WAN is untested until a phone is plugged into it.

## Then: lock screen (yyd0, from Psyche core Fable, ruled)
- Cause: noctalia pid 2311 (started by niri before the switch) runs on glibc 2.42 and dlopens the new PAM modules: journal 10:09 "PAM unable to dlopen pam_unix.so ... GLIBC_2.43 not found". Fable told (mny2).
- Now: restart noctalia in his session only while unlocked (at 11:05 loginctl LockedHint=yes, so not done), then check the journal shows a PAM open succeeding.
- Lasting: find whether noctalia can authenticate through a fresh helper process of the current system, or what change gives it; bring Fable a path and one line. Compromise to declare meanwhile: a switch that changes the locker PAM closure restarts the locker when the session is unlocked.

## Known
- zeus once vanished from the mesh during a switch and came back on its own.
- The living wants backup admin keys on zeus and prometheus and the Librem 5s as backup internet (login.txt); not yet asked of me.
