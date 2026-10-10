# Anatomy of the virtual machine testing node

For the living to point at. Plain words, no code. Marked **witnessed** (this flow read it) or **claimed** (proposed, nothing built).

The headline, because it changes what the work is: **the node already exists and is already called `vm-testing`.** Prometheus is already declared a VM host, and already declares a guest of that name at 4 cores / 8 GB / 40 GB (witnessed, `/git/github.com/LiGoldragon/goldragon/proposal.datom`). Nothing needs creating. One thing needs changing — the guest is declared a *lean* test VM, which is exactly the role that switches the desktop and the home profile **off** — and then ten terminals need putting on its screen.

## 1. What the node is

**Host.** Prometheus: a GMKtec EVO-X2, 8 cores, **128 GB RAM**, Btrfs subvolumes on one disk, IPv6 address `5::5`, species `LargeAiRouter` (witnessed, `proposal.datom`). Its declared capabilities include `VmHost{169.254.100.0/22, KVM Available, maximum 4 guests}`, `NixBuilder` with 6 jobs, and `NixCache`. It is the only place a build ever runs (witnessed, `CriomOS/modules/nixos/nix/client.nix`). It is a server: `edge = false`, so CriomOS's entire graphical tree is inert on the host itself (witnessed, `modules/nixos/edge/default.nix:93`). No desktop on Prometheus, and none wanted.

**Hypervisor.** QEMU with real KVM acceleration, through microvm.nix, driven from cluster data by `test-vm-host.nix` — each guest gets its own kernel and a disk image under `/var/lib/microvms/<guest>/root.img` (witnessed). **This is live on `main` today.**

**Guests Prometheus already declares** (witnessed): `vm-testing` (4 cores, 8 GB, 40 GB, `5::6`), `mirror-alpha` (`5::7`), `mirror-beta` (`5::8`). All three are species `TestVm`.

**The gap, in one sentence.** `TestVm` is the lean role: it exists to be a deploy target and deliberately suppresses the home profile and the desktop. An `Edge` Pod is the opposite — its projection alone lights greetd with the regreet greeter, dbus, polkit, gnome-keyring and **niri**, and keeps the production home profile (witnessed, `CriomOS-test-cluster/lib/mkVmTest.nix`, `lib/standardTest.nix`). The desktop the living wants is **a role change in cluster data**, not new code.

**Image source, and the proof it works.** An Edge Pod desktop with a dummy user is already built and tested: `edge-desktop` in the `fieldlab` fixture cluster — 4 cores, 8 GB, 40 GB, super-user **`aria`** — asserted booting to dbus, greetd, niri, gnome-keyring and polkit (witnessed, `fixtures/horizon/edge-desktop.json` and its `flake.nix`). `aria` is a complete fixture identity: fake SSH key, email `aria@fieldlab.criome.net`, a home generation that really activates. It exists nowhere in the real cluster — fixture only (witnessed). That is already "a dummy desktop with a dummy name and everything."

**Deliberately not inside.** No GPU — VFIO is forbidden on Prometheus, whose GPU serves the AI router. No real user home: neither `li` nor `bird` holds a key on Prometheus, so no human home is built there at all (witnessed, `modules/nixos/userHomes.nix`). No sops secrets, no tailnet identity of the living's.

**The branch.** `enable-vm-hosting-prometheus` (`ec198d46`, **19 June**) is three commits, long behind a main now at `36653a12` (12 September). Its name misleads: **VM hosting on Prometheus is already enabled on main.** Its one good idea — deleting the superseded `modules/nixos/vm-testing/default.nix` (the old libvirtd/Spice/VFIO module, inert on Prometheus, which declares no `VmTesting` capability) — is unmerged; its edits to `test-vm-host.nix` are a **strict regression** against main, which has since gained kind-tagged capabilities, guest-side networking and guest-side SSH. Take the deletion, discard the rest.

## 2. Inputs and outputs

**Start and stop — witnessed, not proposed.** Each guest is a **non-autostart** systemd unit, `microvm@vm-testing.service` (witnessed: `guestAutostart = _entry: false;`). It is started and stopped by name. Inventory is `systemctl list-units 'microvm@*'` and `ls /var/lib/microvms` — explicitly, not `microvm -l` (witnessed, `CriomOS/AGENTS.md:42`).

**Where the command must run.** On Prometheus itself. The laptop is forbidden to fire QEMU, and Prometheus's builder entry lacks the `nixos-test` feature, so a boot cannot be remote-scheduled (witnessed, `scripts/run-criome-auth-on-prometheus`). The door is plain SSH to `prometheus.goldragon.criome`, how every heavy check already travels (witnessed, `scripts/run-on-prometheus`).

**Who may start it.** Primary tests it; **secondary implements and deploys it** once primary's test passes; the **third layer** then debugs in it, observing the desktop and taking screenshots. The living's own ordering (witnessed, `flows/6cc91b/vision/virtualMachine.md`, both entries; `pairHierarchy.md`).

**How a flow reaches the guest.** SSH to its IPv6 node address — `5::6` for `vm-testing` — with guest-side sshd and root keys already emitted from cluster data on main (witnessed).

**Screenshots.** The guest will run niri, and the living's own desktop already screenshots by asking niri: `niri msg action screenshot-screen` writing into `~/Pictures/Screenshots`, with `grim` and `slurp` for regions (witnessed, `CriomOS-home/modules/home/profiles/min/niri.nix`; `CriomOS-lib/lib/default.nix:64`). The third layer should use the identical path and copy the file out over SSH. No framebuffer scraping, no new tool: the guest photographs itself exactly as the living's laptop does.

**One real unknown (claimed).** There is **no VNC and no Spice on the live path** — the old Spice module is inert, and CriomOS has no VNC at all (witnessed absence). A compositor needs an output to draw into. Either the guest declares graphics and someone watches through QEMU, or niri runs headless against a virtual output and only screenshots come out. This flow did not witness which works. It is the first thing to try.

## 3. The desktop layout

Every value below is the living's **current** setting, read from source and from the running machine.

- **Compositor: niri** (witnessed; the hyprland and sway files are imported nowhere — dead). **Terminal: ghostty**, configured by chroma (witnessed, `min/default.nix`).
- **Font: `IosevkaTerm Nerd Font`, size `12`** — witnessed verbatim in the live `/home/li/.config/ghostty/config`; the 12 comes from text size `Small` on the `text-scale.nix` ladder, and `li`'s cluster record does say `Some.Small` (witnessed, `proposal.datom`).
- **Screen: physical 1920x1200, scale 1.25, logical 1536x960**; the panel is 300x190 mm — a **14-inch** diagonal, not 12 (witnessed, `niri msg outputs`). Flag: source declares scale `1.0` while the machine runs `1.25`, so geometry computed from source will be 25% off.
- **Half and half is one setting away.** niri's preset column widths are exactly 1/3, **1/2**, 2/3, 1/1 (witnessed) — "half the screen" is a width the living's own compositor already names. New windows open full width by default, so half must be asked for, never assumed.
- **Terminal size in columns and rows is declared nowhere** (witnessed absence — no columns, rows, width or padding anywhere). Ghostty's defaults apply. Half of 1536 logical pixels less an 8-pixel gap is about **760 logical pixels** per terminal. Turning that into exact columns and rows at 12-point IosevkaTerm needs one measurement, not a guess.

**Proposed layout (claimed).** Five layers — core, primary, secondary, tertiary, quaternary (witnessed, `pairHierarchy.md`) — on the five numbered workspaces niri already binds to Mod+1..Mod+5. Two ghostty windows per workspace, each at the 0.5 preset, Claude left and Codex right, the same on every layer. A seam already exists: a named workspace `criomos-agent-tests` and a rule sending any window with app-id `org.criome.AgentTestWindow` onto it, unfocused (witnessed, `min/niri.nix`). One workspace exists; five per-layer ones do not.

## 4. How the five pairs populate the windows

**The Codex half is built.** `codex-desktop resume <thread-uuid> <directory>` opens a ghostty window, classed `criomos-codex-desktop`, running the Codex CLI against the app-server over its local socket (witnessed, `CriomOS-home/owned-agents/codex/remote.nix`). The app-server is itself a declared user service, `codex app-server --remote-control --listen unix://` (witnessed, `min/agent-intercom.nix`). Nothing new is needed.

**The Claude half is not.** No declared equivalent. Today a session starts with `claude --bg` and is re-entered with `claude attach <id>` (witnessed in the CLI's help), against a daemon control socket under `/tmp/cc-daemon-<uid>/` authorised by `~/.claude/daemon/control.key` (witnessed: the socket directory exists; `tools/prompt-relay` reads both). This asymmetry — Codex owned by a Nix-declared service, Claude ad-hoc — is the largest piece of unbuilt work here.

**What synchronizes a pair.** Already built: `prompt-relay` takes one human turn and delivers it to **both** halves — Codex by thread id over the app-server socket, Claude by session id over the daemon socket — carrying a provenance envelope, and **refusing** to deliver to a Claude session it cannot witness as uniquely idle (witnessed, `tools/prompt-relay`). The same bootstrap was done by hand once already, for the secondary pair (witnessed, `flows/6cc91b/reports/secondaryBootstrap.md`).

**What is missing (claimed).** A per-layer manifest: for each of the five layers, its Claude session id, Codex thread id, and working directory. The spawner reads it; when a pair refreshes the ids change, the manifest is rewritten, and that layer's two windows alone are re-spawned. No such file exists today.

## 5. The security boundary

- **Dummy identity.** `aria` — fixture user, fixture key, fixture email, living only in a cluster deliberately named `fieldlab` and not `goldragon` (witnessed). CriomOS forbids its own source from even naming a real host (witnessed, `checks/source-constraints.nix`). The living is right that screenshots are safe: there is nothing on that screen.
- **No secrets stored.** The living's ruling is that secrets load remotely into the process that needs them, never onto the host, and are lost when it shuts down (witnessed, `flows/6cc91b/vision/secrets.md`). The node holds none. **The subscription-token question is not settled by that ruling** — the living raised copying a login token into the VM as a question ending in their own uncertainty (witnessed, `flows/024bc7/vision/sandbox.md`). Unanswered, the agents inside cannot reach models at all. Question 1 below.
- **Screenshots: allowed, and the preferred observation channel.**
- **Network.** Guests sit on taps in Prometheus's declared guest subnet `169.254.100.0/22`, each with one IPv6 node address (witnessed). The ceiling is **4 guests** and three are already declared — a fourth fits, a fifth does not without raising it. The guest should reach out only as far as model endpoints require; nothing on the living's tailnet should reach in.

## 6. The test that says it works, and what secondary deploys

**Primary's test, two halves.** The first passes today in the fixture cluster: boot an Edge desktop guest and assert dbus, greetd, niri, gnome-keyring and polkit came up (witnessed, `vm-edge-desktop`). The second is new (claimed): on Prometheus, `microvm@vm-testing` starts; ten ghostty windows land on five workspaces, two to a workspace, each at half width in IosevkaTerm 12; a screenshot taken by the guest's own niri is non-empty; that file arrives over SSH.

**What secondary deploys (claimed), in order.**
1. The cluster-data change in `goldragon/proposal.datom`: give the desktop guest the **Edge** role instead of lean `TestVm`, and give it a dummy user with a key so a home is actually built. Everything else — niri, greetd, the home profile — follows from the projection with no code written. This is the whole substance of the request.
2. Whatever the display answer turns out to be (guest graphics, or headless niri).
3. The window spawner, the five workspaces, and the per-layer manifest.
4. The branch cleanup: take its deletion of the superseded `vm-testing` module and its check; discard its `test-vm-host.nix` edits, which regress main.

## 7. Five questions for the living

1. **The token.** Without a model credential inside the guest, the ten terminals open onto agents that cannot think. Your own words left this open ("I don't know if we use GoPass..."). Which is it — a throwaway in-memory key pushed in at start, a separate dummy subscription, or does round one run no agents at all, showing only the desktop and the windows?
2. **Change `vm-testing`, or add a sixth node?** `vm-testing` exists but is lean by declaration; making it a desktop changes what the existing deploy tests boot into. Adding a new Edge Pod beside it — say `vm-desktop` — leaves them alone, but Prometheus's declared ceiling is 4 guests and 3 are taken, so the ceiling would have to go up. Which?
3. **One VM or five?** One guest holding all ten terminals is simple and cheap, and one screenshot shows every layer at once. Five guests, one per layer, lets a layer reboot without disturbing the others and gives each a real boundary — which your four-layers-of-security statement seems to want. Prometheus has 128 GB, so five 8 GB guests fit easily; the ceiling of 4 does not.
4. **Does your real desktop ever mirror it?** You said the pairs go on the right windows "**if the desktop is running**." Two readings: (a) the VM is the only place these ten windows ever appear and your laptop just looks at it; or (b) the same layout is spawned on *your* laptop when it is up, the VM standing in when it is not. (b) is more useful and far more invasive — ten windows on your actual screen.
5. **Who holds the keyboard?** The third layer observes and screenshots. May it also *type* into those ten terminals, driving the other layers' sessions — or is it strictly an eye, reading and relaying upward? Your layer rules say a layer may ask upward but only that layer may speak higher; a debugging layer with a keyboard into all five pairs would cut across that.

## Sources

Psyche: `flows/6cc91b/vision/{virtualMachine,sandbox,secrets,pairHierarchy,terminal,layerZero}.md`; `flows/024bc7/vision/sandbox.md`; `flows/bcd02a/notion/sandbox.md`.
Primary: `flows/6cc91b/reports/{secondaryBootstrap,terminalAndActors}.md`; `tools/prompt-relay`; `SKILL_VARIABLES.md`.
Cluster data: `/git/github.com/LiGoldragon/goldragon/proposal.datom` (prometheus, vm-testing, mirror-alpha, mirror-beta, users li and bird).
CriomOS: `modules/nixos/{test-vm-host,test-vm-guest,test-substrate,vm-testing/default,edge/default,users,userHomes,nix/client,nix/builder,metal/default}.nix`; `checks/vm-testing-prometheus-policy/default.nix`; `AGENTS.md`; bookmarks `enable-vm-hosting-prometheus` (`ec198d46`) and `main` (`36653a12`).
CriomOS-test-cluster: `flake.nix`; `lib/{mkVmTest,standardTest,mkDeployTest,nestedSpike,nestedReachability}.nix`; `clusters/fieldlab.dotos`; `fixtures/horizon/{edge-desktop,atlas,mercury}.json`; `checks/source-constraints.nix`; `scripts/{run-on-prometheus,run-criome-auth-on-prometheus}`.
CriomOS-home: `modules/home/profiles/min/{niri,chroma,default,agent-intercom,sfwbar}.nix`; `modules/home/{base,text-scale}.nix`; `owned-agents/codex/remote.nix`. CriomOS-lib: `lib/default.nix`.
Live host `ouranos`: `~/.config/ghostty/config`; `~/.config/niri/config.kdl`; `niri msg outputs`; `/tmp/cc-daemon-1001/`; `~/.codex/app-server-control/`; `claude --help`; `codex --help`.
