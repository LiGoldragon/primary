# Durable agent host

Flow `0d557b`. Subflow report — a carried account of a design, not a witness.
Nothing was run; every estate claim is a file I read, cited in `## Sources`.
The living's brief is verbatim at `flows/0d557b/vision/durableAgentHost.md`.
Decisions below are the flow's, open for the living's ruling.

## 1 · What it is, what is wanted, why

A rented server that is a CriomOS node like any other, deployed through Lojix,
carrying one long-lived agent user whose whole life is a clone of the primary
workspace. Inside that user: a tmux session, Claude Code and Codex running in
it, and a dedicated Chromium holding the logged-in sessions those two need.
The server never sleeps, never closes its lid, never leaves the café — which
is the point, because a person's laptop is a bad home for an agent that should
still be working tomorrow morning.

The living: *"I'm going to run a primary workspace-based durable agent on a
rented server somewhere."* And the hard part: *"I need a way for the agent to
be able to create software that can remotely inject the password to log in to
my Cloud and my ChatGPT."* The agent must end up authenticated to Claude and
ChatGPT — so, to Google — without the password ever being on that server or in
any agent's context.

Why this shape: the login is a human act performed **once**, from the secure
laptop, **through** the remote browser — not a credential copied to the
server. *"The remote session has no password after it's logged in besides the
token, obviously."* The host keeps the residue of a login, never the means to
perform one.

The brief's second half — *"Do you have the whole terminal, terminal window,
and interactive terminal in a hurdler or something? Is that figured out?"* —
is answered honestly in §4: no.

## 2 · Reachability

**Decision.** The host joins the tailnet; nothing else is public. CriomOS
carries `modules/nixos/network/tailscale.nix` and `headscale.nix`, though the
former says of itself *"Phase 1 scaffolding only: enrollment remains manual"*
— a real module with a manual step, not a turnkey path. sshd is already
keys-only estate-wide: `normalize.nix` sets
`services.openssh.settings.PasswordAuthentication = false`, *"Keys only — no
password auth, ever."* Everything this design adds — CDP, the terminal viewer
— binds `127.0.0.1` and is reached over an SSH tunnel or the tailnet.

## 3 · The browser and the login

**Decision.** One dedicated Chromium, one persistent profile, CDP on loopback.
Not new: `protocols/cloud-maintainer-browser-profile.md` fixes the shape (a
dedicated profile, CDP at `127.0.0.1:9223`, a launcher that reuses the running
instance, and the rule that this and not the daily profile is the production
path), and `CriomOS-home/modules/home/profiles/max/browser-use.nix` realizes it
in Nix as `browser-agent-chrome` — reusable dedicated profile, uid-derived port
(`9223 + uid % 1000`), `--cdp-url`/`--status`, and the explicit comment that it
is *"intentionally NOT the user's ordinary logged-in profile."* The agent
host's browser is that, moved onto a server with no display of its own.

The living, at the secure laptop, opens an SSH tunnel to the loopback CDP port
and does two things.

**Sees and drives.** `chrome://inspect` in the laptop's own Chrome, pointed at
the tunnelled port, gives a screencast of the remote tab with input forwarded
back. He navigates to the Google sign-in and clicks the password field.

**Delivers the password without seeing it, and without the agent seeing it.**

```sh
set -o pipefail
gopass show -o google/… | ssh agent-host cdp-stdin-type
```

`cdp-stdin-type` reads the secret on **stdin** and hands it to the focused
element through CDP `Input.insertText`. Producer piped straight into consumer
stdin, per the secrets skill: no command substitution, no argv, no
environment, no temporary file, no clipboard, no `tee`.

**The boundary, named honestly.** The bytes exist in the gopass process, the
pipe, the SSH transport, `cdp-stdin-type`'s memory, the loopback CDP frame,
and Chromium's input path — the unavoidable producer/transport/consumer
boundary and the kernel beneath it. What this buys is exactly: the bytes never
land in a file, an argument vector, an environment, a log, or an agent's
context. It is not a claim that someone already holding root on the box cannot
observe a login in flight.

**Two-factor** goes the same way: the prompt renders in the screencast and the
living answers it from the laptop, by phone tap or by the same pipe for a TOTP.

**After login** the server holds only the profile's cookies and refresh tokens
for Google, Claude, and ChatGPT. The agents' own vendor tokens are obtained
once in that same browser — a consequence of a login the living performed, not
of a credential he copied.

## 4 · The terminal in a browser

**Answering the living directly: no, this is not figured out anywhere in the
estate.** `terminal-cell` is the active terminal primitive — a daemon-owned
PTY/transcript cell with control and data **Unix sockets** and a raw attach
path — and it has no browser-reachable transport. `terminal` is archived. No
`ttyd`, `wetty`, or `gotty` module, package, or mention exists in CriomOS,
CriomOS-home, lojix, harness, or primary; I grepped all five.

**Decision, proof of concept.** tmux session `primary`, fronted by `ttyd` on
loopback, reached over the tunnel or tailnet. Shortest path to the living
seeing and typing into the real session from any device, and deliberately
disposable.

**The better end-shape.** The viewer belongs to `terminal-cell`, which should
gain a viewer transport of its own — so the browser view is a view *of the
cell*, sharing its transcript, lifecycle, and durable-PTY guarantees, rather
than a second unrelated multiplexer stacked in front. The harness repo's
`skills.md` already writes the rule down: *"Keep durable PTY and viewer
transport in `terminal`."* Either way the durable-harness invariant holds and
is what makes a browser terminal safe: closing the viewer must not kill the
harness. ttyd-over-tmux satisfies it by accident; terminal-cell by design.

## 5 · The agent

**Decision.** Claude Code and Codex run inside that tmux session, in the
primary-workspace clone, started with `--remote` / Remote Control so the phone
and web clients attach through the **vendors' own authenticated relays** —
nothing this design must expose. The precedent runs today:
`CriomOS-home/modules/home/profiles/min/agent-intercom.nix` declares
`codex-remote-control` with
`ExecStart = "…/bin/codex app-server --remote-control --listen unix://"`,
`Restart = "always"`, `UMask = "0077"`, commented *"Its default Unix socket is
local to the user, while remote control reaches the phone through Codex's
authenticated relay."*

Flow `564f55`'s `reports/codexLaunch.md` carries the operating knowledge this
design inherits: the daemon is Nix-owned, so `codex remote-control start` is
the wrong path on a CriomOS node; a session must be started with `--remote`
from its **first** invocation, because no attach-or-convert command exists;
pairing is a one-time human act (`codex remote-control pair --json`, code
entered in the ChatGPT app); and remote control requires ChatGPT
authentication — an API key will not do. That last point is why §3's browser
is load-bearing rather than a convenience. Claude Code's Remote Control sits
alongside it, authenticated from the same profile.

## 6 · How this realizes `s8lq`

`harness/ARCHITECTURE.md` §3.1 records the archived intent **`s8lq`**:
*"Browser automation for real user accounts should support attaching to a
visible browser tab/session so the human can watch, intervene, and keep
login/2FA secrets out of agent prompts and logs."* Each clause lands on a
named part here. *Attach to a visible tab*: the agent attaches over CDP to the
same persistent-profile tab the living drove — one browser, one session, not a
headless clone. *Watch*: the `chrome://inspect` screencast over the tunnel.
*Intervene*: that screencast forwards input, so the living takes the keyboard
at any moment. *Secrets out of prompts and logs*: `gopass | ssh
cdp-stdin-type` touches no prompt, transcript, journal, or file. `s8lq` is
archived intent in that document; this is the first place in the estate where
all four clauses land together on one host.

The launch side is already typed: `harness/src/launch.rs` routes production
harness kinds through the terminal-cell CLI *"so the child lives inside a
PTY-owning session directory"* (`TerminalCellRuntimeRoot`:
`TERMINAL_CELL_RUNTIME_DIR`, then `XDG_RUNTIME_DIR`, then temp). Another
reason the browser terminal should be a terminal-cell viewer: the session it
must show is a terminal-cell session already.

## 7 · Durability and renting

`loginctl enable-linger` for the agent user, so its services and tmux session
survive logout and reboot. `Restart = always` on the Chromium, the agent
daemons, and the viewer, matching `agent-intercom.nix`. The workspace clone is
committed and pushed under the file-editing discipline — **this is the real
durability story**: the box is rented and can be destroyed or lost, so what
matters lives in git; what lives only on the box is the profile and the vendor
tokens, reconstructible by repeating §3.

Renting is existing machinery. `protocols/active-repositories.md` names the
`cloud` repository as the runtime repo for provider API management —
DigitalOcean the lead and the only compute provider shipped in a daemon build,
Hetzner and Cloudflare adapters alongside — with the behavioral axis closed (a
droplet witnessed end-to-end) and the artifact axis open (no committed
re-runnable socket-apply test). The host is a CriomOS node deployed through
Lojix like the others.

## 8 · Threat model

**What an attacker owning the server gets:** the Chromium profile (Google,
Claude, ChatGPT session cookies and refresh tokens), the Claude Code and Codex
vendor tokens, the workspace clone and whatever push credentials it carries,
and the ability to speak as the agent through the vendors' relays.

**What he does not get:** the password — never at rest there, present only as
transient bytes inside a running process during a login the living is watching
— nor the laptop, the gopass store, or the second factor. He can ride open
sessions; he cannot perform a new login.

**Revoking** is session revocation, not password rotation: sign out all
sessions on the Google account's device page; revoke the Claude and ChatGPT
sessions in account settings; unpair the Codex device; remove the node key
from the tailnet and the public key from `authorized_keys`; destroy the
droplet through `cloud`. The password needs no change because it was never
there — the whole reason the login is shaped this way. Rotating anyway is
prudence, not necessity.

**Residual:** a rented host is one somebody else's hypervisor can read. This
is a design against an attacker who gets the disk or a shell, not against the
provider.

## 9 · Open questions for the living's ruling

1. **Which vendor Google account.** Both vendor logins come through Google.
   The living's ordinary account, or a dedicated one carrying only these two
   sessions? Dedicated makes §8's revocation surgical and shrinks what a
   compromised host reaches; ordinary keeps one identity. The flow leans
   dedicated.
2. **Whether Google blocks headless logins.** Google may refuse an
   automation-flagged or headless browser. The fallback keeps the design
   intact and changes one thing: run the same Chromium on a **virtual
   display** (Xvfb) so it is headed with a window nobody looks at, keeping the
   identical CDP path, screencast, and `cdp-stdin-type`. Likely the real
   shape rather than a contingency.
3. **Tailnet or plain SSH tunnel first.** The tailscale module's enrollment is
   manual; a tunnel works the moment the node exists. The flow's decision is
   tailnet as end-shape, tunnel as first step — the living may prefer to do
   enrollment once, up front.
4. **Whether the terminal viewer belongs to `terminal-cell`.** The flow says
   yes. And does `skills.md`'s *"keep … viewer transport in `terminal`"* now
   mean `terminal-cell`, given `terminal` is archived and `terminal-cell` is
   *"not currently subordinate to `terminal`"*?

## 10 · First-run sequence

1. Rent the node through `cloud`'s DigitalOcean adapter; deploy CriomOS via
   Lojix as with any node.
2. Confirm sshd is keys-only (inherited from `normalize.nix`) and no other
   port is public.
3. Enroll on the tailnet — manually, per the module's Phase 1 note — or defer
   and use an SSH tunnel (question 3).
4. Create the agent user, `enable-linger` it, clone the primary workspace.
5. Start the dedicated Chromium with persistent profile and loopback CDP under
   `Restart = always`; on a virtual display if question 2 rules that way.
6. From the laptop, open the tunnel and attach `chrome://inspect`; confirm the
   screencast shows the remote tab and input reaches it.
7. Navigate to the Google sign-in, focus the password field, run
   `set -o pipefail; gopass show -o … | ssh agent-host cdp-stdin-type`;
   answer the second factor through the screencast.
8. In that same browser, complete the Claude and ChatGPT logins so the vendor
   tokens land in the profile.
9. Start tmux session `primary`; start Claude Code and Codex inside it with
   `--remote` / Remote Control **from their first invocation** — a plain
   session cannot be converted afterward.
10. Pair the phone (`codex remote-control pair --json`, code into the ChatGPT
    app; the equivalent for Claude's client).
11. Bring up the terminal viewer on loopback; confirm over tunnel or tailnet,
    and confirm closing the viewer does not kill the session.
12. Push a commit from the clone to prove the durability discipline, then
    disconnect and confirm the agent is still reachable from the phone.

## 11 · Sibling proof of concept

Three artifacts are being produced by sibling subflows. **None exists on disk
yet** — there is no `cdp-stdin-type` or `agent-host-login` under
`CriomOS-home/packages/`, and no path matching `*agent-host*` in either
CriomOS repository. Described by intended shape only; no claim any works.

- `/home/user/CriomOS-home/packages/cdp-stdin-type/` — §3's consumer. Reads
  a secret on stdin, connects to the loopback CDP endpoint, delivers it to the
  focused element via `Input.insertText`. Its whole contract is that it has no
  other input channel: no flag, no environment variable, no file.
- **The agent-host modules in CriomOS and CriomOS-home** — node- and user-level
  Nix: browser service, linger, tmux session, agent services, terminal viewer,
  all `Restart = always`, following `agent-intercom.nix`'s shape.
- `/home/user/CriomOS-home/packages/agent-host-login/` — laptop-side
  orchestration of §10 steps 6–8: open the tunnel, put the browser on the
  sign-in page, stand ready for the `gopass | ssh` hand-off, so the living's
  part is watching and answering rather than assembling a command line.

## Sources

- `/home/user/primary/flows/0d557b/vision/durableAgentHost.md` — the brief,
  verbatim; both dictated passages quoted above.
- `/home/user/primary/flows/0d557b/vision/launchPrompt.md` and
  `/home/user/primary/flows/0d557b/vision/subflows.md` — sibling vision files.
- `/home/user/primary/protocols/cloud-maintainer-browser-profile.md` —
  dedicated profile, `127.0.0.1:9223`, launcher reuse, secret handling.
- `/home/user/CriomOS-home/modules/home/profiles/max/browser-use.nix` —
  `browser-agent-chrome`; uid-derived port; "intentionally NOT the user's
  ordinary logged-in profile".
- `/home/user/CriomOS-home/modules/home/profiles/min/agent-intercom.nix` —
  `codex-remote-control.service` (~lines 112–128) and the relay comment.
- `/home/user/CriomOS/modules/nixos/network/tailscale.nix` line 12 — "Phase 1
  scaffolding only: enrollment remains manual"; and `.../headscale.nix` —
  Phase 1 self-signed cert, direct TLS.
- `/home/user/CriomOS/modules/nixos/normalize.nix` lines 184–190 —
  `PasswordAuthentication = false`, "Keys only — no password auth, ever."
- `/home/user/harness/ARCHITECTURE.md` §3.1 — `s8lq`, quoted in full in §6.
- `/home/user/harness/skills.md` line 11 — "Keep durable PTY and viewer
  transport in `terminal`."
- `/home/user/harness/src/launch.rs` — `SessionLauncher` routes production
  kinds through the terminal-cell CLI; `TerminalCellRuntimeRoot` resolution.
- `/home/user/primary/flows/564f55/reports/codexLaunch.md` — Remote Control vs
  Codex Cloud; Nix-owned daemon; `--remote` from first invocation; pairing;
  ChatGPT-auth requirement.
- `/home/user/primary/protocols/active-repositories.md` — `cloud` (line 110);
  `terminal-cell` active (line 39); `terminal` archived (line 100).
- Negative results, by grep over `/home/user/CriomOS`,
  `/home/user/CriomOS-home`, `/home/user/lojix`, `/home/user/harness`,
  `/home/user/primary`: no `ttyd`, `wetty`, or `gotty` anywhere; no
  `packages/cdp-stdin-type`, no `packages/agent-host-login`, no
  `*agent-host*`.
