# Durable agent host

Flow `0d557b`. Subflow report — a carried account of the design, not a
witness. Nothing here was run; every claim about the estate is a file I
read, cited in `## Sources`. The living's brief is recorded verbatim at
`flows/0d557b/vision/durableAgentHost.md`; this report is the anatomy
fleshed onto it, and every decision below is open for the living's ruling.

---

## 1 · What the thing is

A rented server that is a CriomOS node like any other, deployed through
Lojix, carrying one long-lived agent user whose whole life is a clone of
the primary workspace. Inside that user: a tmux session, Claude Code and
Codex running in it, and a dedicated Chromium holding the logged-in
sessions those two need. The server never sleeps, never closes its lid,
never leaves the café. That is the whole point — the living's laptop is
where a person sits, and a person's machine is a bad place to keep an
agent that is supposed to still be working tomorrow morning.

What is wanted from it, in the living's own words: *"I'm going to run a
primary workspace-based durable agent on a rented server somewhere."*
And the hard part, also in his words: *"I need a way for the agent to be
able to create software that can remotely inject the password to log in
to my Cloud and my ChatGPT."* The agent must end up authenticated to
Claude and to ChatGPT, which means authenticated to Google, without the
password ever being on that server and without it ever entering an
agent's context.

Why it is shaped this way: the login is a human act performed *once*,
from the secure laptop, *through* the remote browser — not a credential
copied to the server. *"The remote session has no password after it's
logged in besides the token, obviously."* The server holds the residue of
a login, never the means to perform one.

The second half of the brief — *"Do you have the whole terminal, terminal
window, and interactive terminal in a hurdler or something? Is that
figured out?"* — is answered honestly in §5: no, it is not figured out
anywhere in the estate.

---

## 2 · Reachability

**Flow's decision.** The host joins the tailnet and exposes nothing else.
CriomOS already carries `modules/nixos/network/tailscale.nix` and
`headscale.nix`, but the tailscale module says of itself *"Phase 1
scaffolding only: enrollment remains manual"* — so the tailnet is a real
module with a manual enrollment step, not a turnkey path.

sshd is already keys-only estate-wide: `modules/nixos/normalize.nix`
enables OpenSSH with `settings.PasswordAuthentication = false` and the
comment *"Keys only — no password auth, ever."* Nothing further is needed
for that half.

Everything the design adds — the CDP endpoint, the terminal viewer — binds
to `127.0.0.1` and is reached over an SSH tunnel or over the tailnet. No
port on the rented box's public address but 22.

Open question in §8: whether the first step is the tailnet at all, or a
plain SSH tunnel, with the tailnet arriving once enrollment stops being
manual.

---

## 3 · The browser

**Flow's decision.** One dedicated Chromium, one persistent profile
directory, CDP on loopback. This is not a new invention; it is the shape
the estate has already settled on twice:

- `protocols/cloud-maintainer-browser-profile.md` — a dedicated profile at
  a fixed state path, CDP at `http://127.0.0.1:9223`, a launcher that
  reuses the running instance rather than spawning a window per
  navigation, and the standing rule that this, not the real daily profile,
  is the production path.
- `CriomOS-home/modules/home/profiles/max/browser-use.nix` —
  `browser-agent-chrome`, which is that protocol realized in Nix: a
  reusable dedicated automation profile with native CDP, port derived from
  the uid (`9223 + uid % 1000`) so users do not collide, and
  `--cdp-url` / `--status` subcommands. Its own comment is explicit that
  it is *"intentionally NOT the user's ordinary logged-in profile."*

The agent host's browser is `browser-agent-chrome` moved onto a server:
same profile-and-CDP shape, no display of its own.

### The login act

The living, at the secure laptop, opens an SSH tunnel to the loopback CDP
port and does two things:

1. **Sees and drives the page.** `chrome://inspect` in the laptop's own
   Chrome, pointed at the tunnelled port, gives a screencast of the remote
   tab with input forwarded back. The living navigates to the Google sign-in,
   clicks the password field, and *watches* — this is the same posture the
   harness repo calls for (§6).

2. **Delivers the password without seeing it and without the agent seeing
   it.** From the laptop:

   ```sh
   set -o pipefail
   gopass show -o google/… | ssh agent-host cdp-secret-type
   ```

   `cdp-secret-type` reads the secret on **stdin** and hands it to the
   focused element through CDP `Input.insertText`. Producer piped straight
   into consumer stdin, per the secrets skill: no command substitution, no
   argv, no environment variable, no temporary file, no clipboard, no
   `tee`, nothing in a shell history or a systemd journal.

**The boundary, named honestly.** The password bytes exist in the gopass
process, in the pipe, in the SSH transport, in `cdp-secret-type`'s memory,
in the CDP WebSocket frame on loopback, and in Chromium's input path. That
is the unavoidable producer/transport/consumer boundary and the kernel
underneath it. What this buys is precise and no more: the bytes never
land in a file, an argument vector, an environment, a log, or an agent's
context. It is not a claim that the server cannot be made to observe them
by someone who already owns root on it while a login is in flight.

**Two-factor** goes the same way. The prompt renders in the screencast;
the living answers it from the laptop — a tap on a phone, or a TOTP
delivered by the same `gopass | ssh cdp-secret-type` path.

**After login**, the server holds only what the profile holds: cookies and
refresh tokens for Google, Claude, and ChatGPT. The vendor auth the agents
themselves use is obtained the same way, once, in that same browser — the
Claude Code and Codex tokens land in their profile directories as a
consequence of a login the living performed, not of a credential he
copied.

---

## 4 · The agent

**Flow's decision.** Claude Code and Codex run inside the tmux session,
in the primary-workspace clone, started with `--remote` / Remote Control
so the phone and web clients attach through the vendors' own authenticated
relays rather than through anything this design has to expose.

The precedent is realized and running in the estate:
`CriomOS-home/modules/home/profiles/min/agent-intercom.nix` declares

```nix
systemd.user.services.codex-remote-control = {
  ExecStart = "…/bin/codex app-server --remote-control --listen unix://";
  UMask = "0077";
  Restart = "always";
};
```

with the comment that *"Its default Unix socket is local to the user,
while remote control reaches the phone through Codex's authenticated
relay."* That is exactly the property the agent host needs: the relay is
the vendor's problem, the socket never leaves the box.

Flow `564f55`'s `reports/codexLaunch.md` carries the operating knowledge
this design inherits and must not relearn: the daemon is Nix-owned, so
`codex remote-control start` is the wrong path on a CriomOS node; a
session must be started with `--remote` from its *first* invocation
because no attach-or-convert command exists; pairing is a one-time human
act (`codex remote-control pair --json`, code entered in the ChatGPT app);
and remote control requires ChatGPT authentication — an API key will not
do. That last point is why the browser of §3 is load-bearing rather than
a convenience.

Claude Code's equivalent Remote Control sits alongside it in the same tmux
session, authenticated from the same profile.

---

## 5 · The terminal in a browser

**Answering the living's question directly: no, this is not figured out
anywhere in the estate.** `terminal-cell` is the active terminal
primitive — a daemon-owned PTY/transcript cell with control and data
**Unix sockets** and a raw attach path (`active-repositories.md`); it has
no browser-reachable transport. `terminal` is archived. No `ttyd`,
`wetty`, or `gotty` module, package, or reference exists anywhere in
CriomOS, CriomOS-home, lojix, harness, or primary — I grepped all five.

**Flow's decision, proof of concept.** tmux session named `primary`,
fronted by `ttyd` bound to loopback, reached over the SSH tunnel or the
tailnet. This is the shortest path to the living seeing and typing into
the real session from a browser on any device, and it is deliberately
disposable.

**The better end-shape.** The viewer belongs to `terminal-cell` — it
should gain a viewer transport of its own, so that the browser view is a
view *of the cell*, sharing the cell's transcript, lifecycle, and durable-
PTY guarantees, rather than a second unrelated PTY multiplexer stacked in
front of it. The harness repo's own `skills.md` already writes this rule
down: *"Keep durable PTY and viewer transport in `terminal`."* The
open question is only whether that line still points at the archived
`terminal` or at `terminal-cell`, which superseded it as the active
primitive (§8).

Either way the durable-harness invariant holds and is what makes a
browser terminal safe here: closing the viewer must not kill the harness.
ttyd-in-front-of-tmux satisfies it by accident; terminal-cell satisfies it
by design.

---

## 6 · How this realizes `s8lq`

`harness/ARCHITECTURE.md` §3.1 records the archived intent
**`s8lq` — browser-automation attach-to-visible-tab**:

> Browser automation for real user accounts should support attaching to a
> visible browser tab/session so the human can watch, intervene, and keep
> login/2FA secrets out of agent prompts and logs.

Each clause is realized by a named part of this design. *Attaching to a
visible tab*: the agent attaches over CDP to the same persistent-profile
tab the living drove — one browser, one profile, one session, not a
headless clone of it. *So the human can watch*: `chrome://inspect`
screencast over the tunnel is the human's window onto that exact tab.
*And intervene*: the same screencast forwards input, so the living takes
the keyboard at any moment. *Keep login/2FA secrets out of agent prompts
and logs*: `gopass … | ssh … cdp-secret-type` puts the password into the
page through `Input.insertText` on a path that touches no prompt, no
transcript, no journal, and no file.

`s8lq` is an archived *intent* in that document; this design is the first
place in the estate where all four clauses land together on one host.

The launch side is already typed: `harness/src/launch.rs` routes
production harness kinds through the terminal-cell CLI *"so the child
lives inside a PTY-owning session directory"*, resolving the runtime root
from `TERMINAL_CELL_RUNTIME_DIR`, then `XDG_RUNTIME_DIR`, then the temp
directory. When the agent host's agents are launched by the harness rather
than by hand, that is the path they take, and it is another reason the
browser terminal should be a terminal-cell viewer: the session it needs to
show is a terminal-cell session already.

---

## 7 · Durability

- `loginctl enable-linger` for the agent user, so its user services and
  its tmux session survive every logout and every reboot.
- `Restart = always` on the browser service, the CDP-holding Chromium, the
  agent daemons, and the terminal viewer — matching the posture
  `agent-intercom.nix` already takes for `codex-remote-control`.
- The workspace clone is committed and pushed under the ordinary
  file-editing discipline. **This is the real durability story.** The
  server is rented: it can be destroyed, resized, or lost, and nothing of
  value should be one disk away from gone. What must survive lives in git;
  what lives only on the box is the browser profile and the vendor tokens,
  and those are reconstructible by repeating §3's login.
- Renting is not new machinery. `protocols/active-repositories.md` names
  the `cloud` repository (`/git/github.com/LiGoldragon/cloud`) as the
  runtime repo for provider API management — DigitalOcean is the lead
  adapter and the only compute provider shipped in a daemon build, with
  Hetzner and Cloudflare adapters alongside. That protocol also records
  that the behavioral axis is closed (a droplet was witnessed end-to-end)
  while the artifact axis is open — no committed re-runnable socket-apply
  test. The host is a CriomOS node deployed through Lojix like every other
  node; renting is a `cloud` request, not a new capability.

---

## 8 · Threat model

**What an attacker who owns the server gets.** The Chromium profile —
Google, Claude, and ChatGPT session cookies and refresh tokens — and the
Claude Code and Codex vendor tokens in their profile directories. Also the
workspace clone and whatever git push credentials it carries, and the
ability to speak as the agent through the vendors' relays.

**What he does not get.** The password. It is never at rest on that host;
it exists there only as transient bytes inside a running process during a
login the living is watching. He does not get the laptop, the gopass
store, or the second factor. He cannot perform a *new* login to any of
these accounts — he can only ride the ones already open.

**Revoking.** It is a session revocation, not a password rotation, and it
is cheap: sign out all sessions in the Google account's device page, and
revoke the Claude and ChatGPT sessions from their respective account
settings; unpair the Codex Remote Control device; remove the host's node
key from the tailnet and its public key from `authorized_keys`; destroy
the droplet through `cloud`. The password does not need changing because
it was never there — which is the whole reason the login is shaped the way
it is. Rotating it anyway is prudence, not necessity.

**The residual risk, stated plainly.** A rented host is a host somebody
else's hypervisor can read. Everything above is a design against an
attacker who obtains the disk or a shell — not against the provider.

---

## 9 · Open questions for the living's ruling

1. **Which Google account.** The vendor logins (Claude, ChatGPT) both come
   through Google. Should the agent host use the living's ordinary
   account, or a dedicated one that carries only these two vendor
   sessions? A dedicated account makes §8's revocation surgical and
   shrinks what a compromised host reaches; the ordinary account is
   simpler and keeps one identity. The flow leans dedicated, but this is
   the living's to rule.

2. **Headless logins and the display fallback.** Google is known to treat
   automation-flagged and headless browsers differently, and may refuse
   the sign-in outright. The fallback keeps the entire design intact and
   changes one thing: run the same Chromium on a **virtual display**
   (Xvfb, or a headless-shell-free X session) so it is a headed browser
   with a real window nobody looks at, and keep the identical CDP path,
   the identical screencast, and the identical `cdp-secret-type`. This
   should be treated as the likely shape rather than a contingency.

3. **Tailnet first, or SSH tunnel first.** The tailscale module's own
   comment says enrollment remains manual. A plain SSH tunnel is available
   the moment the node exists and needs nothing new. The flow's decision
   is the tailnet as the end-shape and the tunnel as the first step; the
   living may prefer to do the tailnet enrollment once, up front, and
   never use the tunnel.

4. **Where the terminal viewer belongs.** Does the browser terminal become
   a `terminal-cell` transport (the flow's answer), or does it stay an
   independent ttyd fronting tmux? And does `skills.md`'s *"Keep durable
   PTY and viewer transport in `terminal`"* now mean `terminal-cell`,
   given that `terminal` is archived and `terminal-cell` is *"not
   currently subordinate to `terminal`"*?

---

## 10 · First-run sequence

1. Rent the node through the `cloud` repository's DigitalOcean adapter and
   deploy CriomOS onto it through Lojix, as with any other node.
2. Confirm sshd is keys-only (inherited from `normalize.nix`) and that no
   other port is open on the public address.
3. Enroll the host on the tailnet — manually, per the module's Phase 1
   note — or defer this and use an SSH tunnel for step 6 (question 3).
4. Create the agent user, `enable-linger` it, and clone the primary
   workspace into it.
5. Start the dedicated Chromium with its persistent profile and loopback
   CDP, under `Restart = always`; on a virtual display if question 2 rules
   that way.
6. From the secure laptop, open the SSH tunnel and attach
   `chrome://inspect` to the tunnelled CDP port; confirm the screencast
   shows the remote tab and that input reaches it.
7. Navigate to the Google sign-in, focus the password field, and run
   `set -o pipefail; gopass show -o … | ssh agent-host cdp-secret-type`.
   Answer the second factor through the same screencast.
8. In that same browser, complete the Claude and ChatGPT logins so the
   vendor tokens land in the profile.
9. Start the tmux session `primary`; start Claude Code and Codex inside it
   with `--remote` / Remote Control **from their first invocation** — a
   plain session cannot be converted afterward.
10. Pair the phone: `codex remote-control pair --json`, enter the code in
    the ChatGPT app; do the equivalent for Claude's client.
11. Bring up the terminal viewer on loopback and confirm it over the
    tunnel or tailnet; confirm that closing the viewer does not kill the
    session.
12. Push a commit from the workspace clone to prove the durability
    discipline works end to end, then disconnect and confirm the agent is
    still reachable from the phone.

---

## 11 · Sibling proof of concept

Three artifacts are being produced by sibling subflows of this flow.
At the time of writing none of them exists on disk yet — I checked; there
is no `cdp-secret-type` or `agent-host-login` under
`CriomOS-home/packages/`, and no file matching `*agent-host*` in either
CriomOS repository. They are described here **by intended shape only**,
and this report makes no claim that any of them works.

- **`/home/user/CriomOS-home/packages/cdp-secret-type/`** — the §3
  consumer. Reads a secret on stdin, connects to the loopback CDP
  endpoint, and delivers it to the focused element via `Input.insertText`.
  Its whole contract is that it has no other input channel: no flag, no
  environment variable, no file.
- **The agent-host modules in CriomOS and CriomOS-home** — the node-level
  and user-level Nix declarations: the browser service, the linger, the
  tmux session, the agent services, the terminal viewer, all under
  `Restart = always`, following `agent-intercom.nix`'s shape.
- **`/home/user/CriomOS-home/packages/agent-host-login/`** — the
  laptop-side orchestration of §10 steps 6–8: open the tunnel, put the
  browser on the sign-in page, and stand ready for the `gopass | ssh`
  hand-off, so the living's part is watching and answering rather than
  assembling a command line.

---

## Sources

Files read for this report, all paths absolute.

- `/home/user/primary/flows/0d557b/vision/durableAgentHost.md` — the
  living's brief, verbatim; both dictated passages quoted above.
- `/home/user/primary/flows/0d557b/vision/launchPrompt.md`,
  `/home/user/primary/flows/0d557b/vision/subflows.md` — the two sibling
  vision files.
- `/home/user/primary/protocols/cloud-maintainer-browser-profile.md` —
  dedicated profile, `127.0.0.1:9223`, launcher reuse, secret handling.
- `/home/user/CriomOS-home/modules/home/profiles/max/browser-use.nix` —
  `browser-agent-chrome`; dedicated automation profile, uid-derived port,
  "intentionally NOT the user's ordinary logged-in profile".
- `/home/user/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
  — `codex-remote-control.service` (lines ~112–128): `app-server
  --remote-control --listen unix://`, `Restart = "always"`,
  `UMask = "0077"`, and the relay comment.
- `/home/user/CriomOS/modules/nixos/network/tailscale.nix` — line 12,
  "Phase 1 scaffolding only: enrollment remains manual."
- `/home/user/CriomOS/modules/nixos/network/headscale.nix` — Phase 1
  self-signed cert, direct TLS, no reverse proxy.
- `/home/user/CriomOS/modules/nixos/normalize.nix` — lines 184–190,
  `services.openssh` with `PasswordAuthentication = false`, "Keys only —
  no password auth, ever."
- `/home/user/harness/ARCHITECTURE.md` §3.1 — `s8lq`, attach-to-visible-
  tab, quoted in full in §6.
- `/home/user/harness/skills.md` — line 11, "Keep durable PTY and viewer
  transport in `terminal`."
- `/home/user/harness/src/launch.rs` — `SessionLauncher` routes production
  kinds through the terminal-cell CLI; `TerminalCellRuntimeRoot`
  resolution order.
- `/home/user/primary/flows/564f55/reports/codexLaunch.md` — Remote
  Control vs Codex Cloud; Nix-owned daemon; `--remote` from first
  invocation; pairing; ChatGPT-auth requirement.
- `/home/user/primary/protocols/active-repositories.md` — the `cloud`
  repository (line 110) and its provider adapters and open artifact axis;
  `terminal-cell` (line 39) as the active primitive; `terminal` (line 100)
  archived.
- Negative results, by grep over `/home/user/CriomOS`,
  `/home/user/CriomOS-home`, `/home/user/lojix`, `/home/user/harness`,
  `/home/user/primary`: no `ttyd`, `wetty`, or `gotty` anywhere; no
  `packages/cdp-secret-type`, no `packages/agent-host-login`, no path
  matching `*agent-host*`.
