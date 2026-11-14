# Psyche core Opus 4429a6: handover

The living moved house on 11 November. Claude usage goes to Fable for design, with Opus assisting and Psyche book Haiku publishing; Codex does the implementing, Sol before Astra unless he names Astra. When he talks to Opus rather than Fable, it is so as not to wake Fable: act on his words yourself and relay to Fable only what needs Fable's judgment. Write to him plainly, as a person, concepts over logs.

## Who holds what
- Mind flowNexus Astra leads Mind flowNexus Sol on the Flow Nexus, mirroring Fable over Opus; Mind flowNexus Opus publishes and deploys. 0.54.4 to 0.54.6 are live. 0.54.7 is accepted (Codex rest settles at every rest, typed reap/handover pending, ordinary-socket handshake, energy-nexus updated with it) and deploys third in the order below. Codex delivery is unreliable: SendAccepted Uncertain means placed; do not retype it, type into a pane only on refusal or failure.
- Mind core Sol (a57a68, chain 121cc5 then d76b4c) holds the open-fix inventory flows/121cc5/open-fixes.md, the Horizon wireless implementation, the prometheus boot-capture, and the zoekt hook source fix.
- Field core Sol (1cc5ce) holds the ouranos network, zeus LAN, the idle/lock fault, the AP declared profile deploy and proof, and the zoekt damage repairs (done; 31 shallow-only repos untouched).
- Psyche criomos Opus holds Lojix rollouts for every host.

## Deploy order, serialized on the Home and CriomOS heads
1. boot capture (watchdog bootstatus at boot) together with the zoekt hook fix; the ~/.gitconfig line `hook.zoekt-index.command = true` I added is removed in that same deploy. Hook adapter ruled: accept exactly Git's payload per event, refuse anything else.
2. Flow 0.54.7 (Mind flowNexus Opus; its hold 4fv9 lifts when 1 lands).
3. /tmp: boot.tmp.cleanOnBoot (CriomOS d082b568, branch tmp-clean-40fefd) plus PrivateTmp=true on home-manager activation units, every host; Nix 2.35.3 nix profile install leaks ~1.1M inodes into /tmp per Home activation. Prove on zeus. Tell him first that ouranos /tmp (61G) clears at its next boot; he has not answered whether to keep anything.
4. The Horizon wireless types (Fable ruled 9ckl and wm4a: AP declared once on the router, every Wi-Fi node a client by derivation, LinkKind ordering Tether, Wired, Wireless by default, router Wired, Tether, Wireless). Secret: routerWifiSaePasswords in goldragon, already one raw password, its age recipient is the prometheus host key; client recipients added with sops when the projection is final. Needs his answer: do tiger and balboa have Wi-Fi.

## Open with him
- Lock screen: fix deployed (noctalia honors NOCTALIA_PAM_SERVICE). He owes a log out and in, then an ordinary unlock; the full check at the next nixpkgs advance (flows/fb0a2c/noctalia-pam-selection.md).
- Screen not locking: proven that non-input resets of the regular idle stop the 1h lock; the Claude app is the sole visible candidate. His test: tell Field core Sol before he leaves, move the Claude window to another workspace.
- ouranos is on the goldragon.criome AP by the stopgap (never-default lifted), which also restored Yggdrasil and the builder route.
- zeus LAN works since 11:37; why its carrier was missing 11:03 to 11:30 is unknown. His lead: a second USB adapter added on prometheus. Field is reading enumeration and br-lan membership (etrv, 025i). If names by USB path are the cause, membership must not depend on path.
- prometheus abrupt endings: 21 of 26 boots, two this morning around 09:17 to 09:21; he has not said whether power was cut. Capture is in deploy step 1.
- Fable's own open design lines are in a section of open-fixes.md.
