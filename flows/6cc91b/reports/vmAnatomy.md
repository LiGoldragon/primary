# Anatomy of the virtual machine testing node

For the living to point at. Plain words, no code. Every claim is marked
**witnessed** (this flow read it) or **claimed** (a proposal, nothing built).

Read first, because it changes the shape of the work: **most of this already
exists.** The living is not asking for a new thing to be invented. They are
asking for two existing halves to be joined — a persistent VM-testing node on
Prometheus, and a dummy CriomOS desktop that today only lives for the length
of a hermetic test — and then for ten terminals to be put on its screen.

## 1. What the node is

**The host.** Prometheus, `prometheus.goldragon.criome` (witnessed,
`/home/li/primary/SKILL_VARIABLES.md:6`). It is already the machine every
heavy check is sent to, over plain SSH (witnessed,
`/git/github.com/LiGoldragon/CriomOS-test-cluster/scripts/run-on-prometheus`).

**The hypervisor.** QEMU/KVM, with libvirtd and a Spice remote display, plus
a persistent guest declared through microvm.nix. This is not a proposal: it
is a finished CriomOS module, `criomos.vmTesting` (witnessed,
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/vm-testing/default.nix`).
It turns on when a node's cluster data declares a `VmTesting` service, and it
publishes the guest as `vm-testing.<cluster>.criome`.

A policy check already pins Prometheus's shape: VM testing **on**, GPU
passthrough **off**, VFIO never armed, no IOMMU kernel parameters — because
Prometheus is an AI node whose GPU must not be handed to a guest (witnessed,
`/git/github.com/LiGoldragon/CriomOS/checks/vm-testing-prometheus-policy/default.nix`).

**The gap.** The persistent guest that module declares is a stub: two cores,
2 GB, graphics enabled, hostname `vm-testing`, and nothing else. No user, no
desktop, no home. Its own comment says so — the desktop surface is left to the
ephemeral test checks (witnessed, same file). That stub is what must grow into
the living's node.

**The image source.** The desktop the living wants already exists, built from
CriomOS, with a dummy user. It is the `edge-desktop` node of the `fieldlab`
fixture cluster (witnessed,
`/git/github.com/LiGoldragon/CriomOS-test-cluster/fixtures/horizon/edge-desktop.json`):
an Edge Pod, 4 cores, 8 GB RAM, 40 GB disk, hosted on a VM host, super-user
**`aria`**. Being an Edge node lights up the whole desktop tree by declaration
alone — greetd with the regreet greeter, dbus, polkit, gnome-keyring, and
**niri** — and it keeps the production home profile. All of that is asserted in
a test that runs today (witnessed,
`/git/github.com/LiGoldragon/CriomOS-test-cluster/flake.nix`, `customTests.edge-desktop`).

`aria` is a complete fixture identity: a fake SSH key, the email
`aria@fieldlab.criome.net`, a home-manager generation that actually activates
(witnessed, `clusters/fieldlab.dotos` and the `base-home` test). This is
already "a dummy desktop with a dummy name and everything."

**What is deliberately not inside.** No goldragon cluster data, no sops keys,
no real secrets, no tailnet identity of the living's, no GPU, and none of the
living's home. The test cluster repo exists precisely to prove production host
facts do not leak into it (witnessed, its README).

**About the branch.** `enable-vm-hosting-prometheus` is three commits from
**19 June**, diverged from a main that has since moved to 12 September. Its
one substantive change — making the guest route prefix family-aware — is
**already on main** (witnessed, `modules/nixos/test-vm-host.nix` lines 34 and
315). The branch is superseded. Nothing should be built on it. It should be
abandoned, not merged.

## 2. Inputs and outputs

**How it starts and stops.** By declaration, not by command: the guest is a
microvm.nix VM owned by the host's system configuration, so it comes up with
the host and is started and stopped as an ordinary system service (claimed —
the module declares the VM; this flow did not witness the unit running).

**Who may start it.** Primary tests it; **secondary implements and deploys it**
once primary's test passes; the **third layer** then uses it to debug, observe
the desktop and take screenshots. That ordering is the living's own
(witnessed, `flows/6cc91b/vision/virtualMachine.md`, both entries, and
`flows/6cc91b/vision/pairHierarchy.md`).

**How a flow reaches it.** Three doors, in order of preference:

- **SSH** into the guest at its Criome domain — the ordinary door, for
  everything that is not visual.
- **Spice** — already the module's declared default display, chosen for
  interactive latency and clipboard (witnessed). This is the door for a human
  who wants to *watch*.
- **Screenshots from inside the guest.** This is the good one. The guest runs
  niri, and the living's own desktop already takes screenshots by asking niri
  for them — `niri msg action screenshot-screen` writing into
  `~/Pictures/Screenshots`, plus `grim` and `slurp` for region grabs
  (witnessed, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix`
  and `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix:64`). The third
  layer should use the identical path, then copy the file out over SSH. No
  framebuffer scraping, no new tool: the guest photographs itself the same way
  the living's laptop does.

## 3. The desktop layout

Every value below is the living's **current** setting, read from the running
machine and from source.

- **Compositor: niri** (witnessed, `min/niri.nix`; hyprland and sway files
  exist but are imported nowhere — dead).
- **Terminal: ghostty** (witnessed, `min/default.nix`), configured by chroma,
  not by stylix.
- **Font: `IosevkaTerm Nerd Font`, size `12`** (witnessed verbatim in the live
  file `/home/li/.config/ghostty/config`, generated from `min/chroma.nix`; the
  12 comes from text size `Small` on the `text-scale.nix` ladder).
- **Screen: physical 1920x1200, scale 1.25, logical 1536x960**; the panel is
  300x190 mm, which is a **14-inch** diagonal, not 12 (witnessed via
  `niri msg outputs`). Flag: the Nix source declares scale `1.0` while the
  machine runs `1.25`. Anything computing geometry from source will be 25% off.
- **Half and half is one setting away.** niri's preset column widths are
  exactly 1/3, **1/2**, 2/3, 1/1 (witnessed, `min/niri.nix`) — so "half the
  screen" is a width the living's own compositor already names. But new windows
  open at full width by default, so half must be asked for, not assumed.
- **Terminal size in columns and rows is declared nowhere** (witnessed
  absence — no columns, rows, window-width or padding in any config). Ghostty's
  defaults apply. Half of 1536 logical pixels, less an 8-pixel gap, is about
  **760 logical pixels per terminal**. Turning that into exact columns and rows
  at 12-point IosevkaTerm needs one measurement on the living's screen, not a
  guess.

**Proposed layout (claimed).** Five layers — core, primary, secondary,
tertiary, quaternary (witnessed, `flows/6cc91b/vision/pairHierarchy.md`) — on
the five numbered workspaces niri already binds to Mod+1 through Mod+5. Two
ghostty windows per workspace, each set to the 0.5 preset. Claude on the left,
Codex on the right, the same way on every layer.

There is already a seam for exactly this: a named workspace
`criomos-agent-tests` and a window rule that sends any window with the app-id
`org.criome.AgentTestWindow` onto it, unfocused (witnessed, `min/niri.nix`).
One workspace exists; five per-layer ones do not.

## 4. How the five pairs populate the windows

**The Codex half is already built.** `codex-desktop resume <thread-uuid>
<directory>` opens a ghostty window, classed `criomos-codex-desktop`, running
the Codex CLI against the app-server over its local socket (witnessed,
`/git/github.com/LiGoldragon/CriomOS-home/owned-agents/codex/remote.nix`). The
app-server itself is a declared user service, `codex app-server
--remote-control --listen unix://` (witnessed, `min/agent-intercom.nix`).
Nothing new is needed here.

**The Claude half is not.** There is no declared equivalent. Today a session is
started with `claude --bg` and re-entered with `claude attach <id>` (witnessed
in the CLI's own help), against a daemon control socket under
`/tmp/cc-daemon-<uid>/` authorised by `~/.claude/daemon/control.key`
(witnessed: the socket directory exists, and `/home/li/primary/tools/prompt-relay`
reads both). This asymmetry — Codex owned by a Nix-declared service, Claude
ad-hoc — is the single largest piece of unbuilt work in the whole picture.

**What synchronizes a pair.** It already exists: `prompt-relay` takes one human
turn and delivers it to *both* halves — to Codex by thread id over the
app-server socket, to Claude by session id over the daemon socket — carrying a
provenance envelope, and **refusing** to deliver to a Claude session it cannot
witness as uniquely idle (witnessed, `/home/li/primary/tools/prompt-relay`).
This exact bootstrap has been done by hand once already, for the secondary pair
(witnessed, `flows/6cc91b/reports/secondaryBootstrap.md`).

**What is missing (claimed).** A per-layer manifest: for each of the five
layers, its Claude session id, its Codex thread id, and its working directory.
The window spawner reads it; when a pair refreshes, the ids change, the manifest
is rewritten, and the two windows for that layer alone are re-spawned. Nothing
like this file exists today.

## 5. The security boundary

- **Dummy identity.** `aria`, a fixture user with a fixture key and a fixture
  email in a cluster deliberately named `fieldlab` and not `goldragon`
  (witnessed). None of the living's data is there. This is why the living said
  screenshots are safe, and they are right: there is nothing on that screen to
  leak.
- **No secrets stored.** The living's ruling is that secrets are loaded
  remotely into the process that needs them, never stored on the host, and lost
  when the host shuts down (witnessed, `flows/6cc91b/vision/secrets.md`). The
  node holds none. **The subscription-token question is not settled by that
  ruling and should not be treated as settled** — the living raised copying a
  login token into the VM as a question, ending in their own uncertainty
  (witnessed, `flows/024bc7/vision/sandbox.md`). Without an answer, the agents
  inside the guest cannot reach models at all. This is question 1 below.
- **Screenshots: allowed, and the preferred observation channel.**
- **Network reach.** The guest sits on a tap interface inside the host's
  declared guest subnet and is published under one Criome name. In the fixture
  cluster that subnet is a link-local `/22` with KVM available and a ceiling of
  six guests (witnessed, `fixtures/horizon/atlas.json`) — fixture values, not
  Prometheus's. The guest should reach the outside only as far as the model
  endpoints require, and nothing on the living's tailnet should reach it.

## 6. The test that says it works, and what secondary deploys

**Primary's test, in two halves.** The first half exists and passes today: boot
the desktop guest and assert dbus, greetd, niri, gnome-keyring and polkit came
up (witnessed, `vm-edge-desktop`). The second half is new (claimed): ten ghostty
windows land on five workspaces, two to a workspace, each at half width, in
IosevkaTerm 12; a screenshot taken *by the guest's own niri* is non-empty; and
that file arrives on the host over SSH.

**What secondary deploys (claimed).** Three things, in order.
1. The cluster-data addition that declares Prometheus a VM host running the
   desktop guest. The test-cluster flake already anticipates this in writing —
   "a second host (prometheus) is a data-only addition that this same iteration
   would pick up" (witnessed, its `flake.nix`). Declaring the node *is* getting
   the test.
2. Growing the `criomos.vmTesting` persistent guest from its 2-core stub into
   the Edge desktop profile with `aria`.
3. The window spawner, the five workspaces, and the per-layer manifest.

And it abandons the June branch rather than merging it.

## 7. Five questions for the living

1. **The token.** Without a model credential inside the guest, the ten
   terminals will open onto agents that cannot think. Your own words left this
   open ("I don't know if we use GoPass..."). Which is it: a throwaway
   in-memory key pushed in at start, a separate dummy subscription, or does the
   VM run agents at all in the first round — showing only the desktop and the
   windows?
2. **One VM or five?** One guest holding all ten terminals is simple, cheap,
   and means one screenshot shows every layer at once. Five guests, one per
   layer, means a layer can be rebooted without disturbing the others and gives
   each layer a real security boundary — which your four-layers-of-security
   statement seems to want. One costs about 8 GB on Prometheus; five, about 40.
3. **Does your real desktop ever mirror it?** You said the pairs should be
   "populated on the right windows in the Neary desktop **if the desktop is
   running**." Two readings: (a) the VM is the only place these ten windows
   ever appear, and your laptop just looks at it; or (b) the same layout is
   spawned on *your* laptop when it is up, and the VM is the headless stand-in
   when it is not. (b) is more useful and much more invasive — it would put ten
   windows on your actual screen.
4. **The terminal size.** Nothing in your configuration declares columns and
   rows; ghostty uses its defaults, and your panel is 14 inches at logical
   1536x960, not 12. Should the VM simply reproduce 1536x960 at scale 1.25 so
   half-width is 760 pixels — or do you want a specific column count, say 100
   columns each, which would fix the size regardless of screen?
5. **Who holds the keyboard?** The third layer is to observe and take
   screenshots. May it also *type* into those ten terminals — driving the other
   layers' sessions — or is it strictly an eye, reading the screen and relaying
   upward? Your layer rules say a layer may ask upward but only that layer may
   speak higher; a debugging layer with a keyboard into all five pairs would cut
   across that.

## Sources

- `/home/li/primary/flows/6cc91b/vision/virtualMachine.md` (both entries),
  `sandbox.md`, `secrets.md`, `pairHierarchy.md`, `terminal.md`, `layerZero.md`
- `/home/li/primary/flows/024bc7/vision/sandbox.md`,
  `/home/li/primary/flows/bcd02a/notion/sandbox.md`
- `/home/li/primary/flows/6cc91b/reports/secondaryBootstrap.md`,
  `terminalAndActors.md`
- `/home/li/primary/tools/prompt-relay`; `/home/li/primary/SKILL_VARIABLES.md`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/vm-testing/default.nix`,
  `modules/nixos/test-vm-host.nix`,
  `checks/vm-testing-prometheus-policy/default.nix`; bookmark
  `enable-vm-hosting-prometheus` (`ec198d46`, 2026-06-19) against `main`
  (`36653a12`, 2026-09-12)
- `/git/github.com/LiGoldragon/CriomOS-test-cluster/flake.nix`,
  `lib/mkVmTest.nix`, `lib/standardTest.nix`, `lib/mkDeployTest.nix`,
  `clusters/fieldlab.dotos`, `fixtures/horizon/{edge-desktop,atlas,mercury}.json`,
  `scripts/run-on-prometheus`, `README.md`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/niri.nix`,
  `chroma.nix`, `default.nix`, `agent-intercom.nix`, `sfwbar.nix`,
  `modules/home/base.nix`, `modules/home/text-scale.nix`,
  `owned-agents/codex/remote.nix`;
  `/git/github.com/LiGoldragon/CriomOS-lib/lib/default.nix`
- Live host `ouranos`: `/home/li/.config/ghostty/config`,
  `/home/li/.config/niri/config.kdl`, `niri msg outputs`,
  `/tmp/cc-daemon-1001/`, `~/.codex/app-server-control/`, `claude --help`,
  `codex --help`
