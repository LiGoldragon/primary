# 20 — Pi as Codex replacement, design phase

*Designer-phase contribution to cluster-operator's CriomOS-home Pi
work (cluster-operator.lock on `/git/github.com/LiGoldragon/CriomOS-home`,
"package and configure Pi harness defaults/extensions"). Psyche
intent record 227 settles target shape: Pi as Codex replacement with
GPT-5.5 xhigh default, GPT-5.4-mini available, packaged Pi extensions,
Ghostty or terminal-cell spawn testing. This report sketches the
design substance cluster-operator's implementation slice needs but
does not duplicate /266 (persona-pi triad longer-term) or /268
(operator brief).*

## 1. Where this fits

Intent 227 is **v1 Pi-as-Codex-replacement** — a deployment slice
that ships Pi as a ready Codex substitute through CriomOS-home. It
is NOT yet the persona-pi triad (/266 + /268), which remains
parked per intent 166 (designer pivot to /249 gap-closure). v1 is
a CriomOS-home profile + extension bundle; v2 (later) wraps Pi as
a persona-pi triad with dual-path signal contract.

v1 deliberately stays light:

- One Nix-managed `pi` binary in the user profile.
- One bundled Pi extension set.
- Provider configuration via Pi's native config (GPT subscription
  login, model defaults).
- No new signal contract, no daemon, no triad.

The bridge to v2 is implicit: when persona-pi ships, v1's profile
becomes the harness bootstrap; v2 wraps the Pi harness API path
into a typed signal-persona-pi contract.

## 2. Pi extensions to Nix-package

Per psyche intent ("nix-package the extensions that Pi should just
have because they're basically becoming a community standard"). The
selection criteria, from intent 227 + the Pi extension surface in
`reports/designer/pi-api-surface-notes.md` §"Concrete flat-function
namespace examples":

| Extension | Why | Source |
|---|---|---|
| `subagent` | Psyche explicitly named it. GPT lacks Pi's sub-agent feature; community extension provides it. | community Pi extension (likely under `pi-mono/packages/coding-agent/examples/extensions/` or third-party). |
| `rewind` / session-rewind | Psyche named it as a Pi feature Codex lacks. | Pi has built-in session-fork / session-compact / session-tree hooks per pi-api-surface-notes §"Event surface"; rewind extension or pi-native mechanism. **Verify which.** |
| `mac_system_theme` equivalent for Linux/NixOS | Psyche named theme-switching as broken in Codex; Pi must do it right. Day/night switch must work even during a running task. | community extension; Linux equivalent likely needs adaptation since `mac_system_theme` is macOS-specific. |
| `working_indicator` / `status_line` | Standard Pi polish; matches psyche's "make it look like nice and super duper." | community extension. |
| `model_status` | Shows current model + thinking level in status bar — relevant given multi-model provider chain. | community extension. |
| `confirm_destructive` + `dirty_repo_guard` + `protected_paths` | Workspace safety — `confirm_destructive` for `rm -rf`/`git push --force`/etc.; `dirty_repo_guard` for jj-driven workspace; `protected_paths` for `intent/`, `~/.local/state/persona-spirit/`, etc. | community extensions; selection per workspace discipline. |
| `git_checkpoint` / `auto_commit_on_exit` | Aligns with jj-driven workspace + the no-branches-by-default discipline. | community extensions; verify they compose with jj. |
| `web_search` | Operator workflow includes web research. | community extension. |
| `prompt_customizer` | Allows per-session prompt overrides for specialized roles. | community extension. |
| `summarize` / `trigger_compact` | Context maintenance polish — explicit triggers for compaction. | community extensions. |

**Explicitly NOT bundled in v1:**

- `plan_mode` — psyche has been clear about Codex's plan mode being
  unhelpful (Mario's thesis per `reports/second-system-assistant/3`).
  Skip unless Pi's plan_mode is structurally different.
- `interactive_shell` — overlaps with `user_bash` built-in; conflict
  risk.
- Game extensions (`snake`, `space_invaders`, `doom_overlay`) — out
  of scope for an operator-class harness.

## 3. Theme-switching design

Psyche's stated requirement: "the nighttime and daytime theme switch
doesn't even work on Codex while it's running on a task." Pi must
do it right.

Mechanism options:

- **Option A — system signal listener.** A Pi extension listens for
  GTK/Qt/X11 theme-change signals (or NixOS's home-manager theme
  state) and reloads Pi's color palette on the fly. Lowest latency;
  needs Linux equivalent to `mac_system_theme`.
- **Option B — time-based switcher.** Pi extension reads a config
  (day-start / night-start times) and re-themes on schedule, plus
  on session-start. Simpler but doesn't respond to manual override.
- **Option C — file-watch on a system theme indicator.** Pi extension
  watches `/etc/theme-state` or similar; CriomOS-home maintains the
  indicator. Decouples Pi from the desktop environment.

Designer lean: **Option A first, Option C as fallback.** A first
because it responds in real time to whatever desktop signal the
psyche uses (manual override included); C if A turns out to be
fragile across NixOS/Hyprland/etc. configurations.

Hard requirement per psyche: theme switch MUST work **during a
running task**, not just at session start. Verify the chosen
mechanism survives mid-task — Pi's render layer must accept theme
changes without restarting the session.

## 4. Sub-agent extension

GPT lacks Pi's native sub-agent shape; community extension fills
the gap. Workspace constraint: the AGENTS.md hard override "Do not
dispatch subagents unless the psyche explicitly asks" applies to
agents in the workspace.

**Design question (designer concern, not blocking implementation):**
Pi's `subagent` extension lets the LLM (GPT) dispatch sub-agents
autonomously. The workspace's no-subagents-by-default discipline
was authored for Claude/Codex; whether it transfers to a Pi-driven
GPT agent is a separate decision.

Two stances:

- **Stance A — discipline transfers**: GPT in Pi follows the same
  hard override; sub-agent extension installed but the system prompt
  disables it unless the psyche explicitly authorizes. (Symmetric
  with Claude/Codex.)
- **Stance B — discipline scoped to Claude/Codex**: GPT in Pi is
  free to dispatch sub-agents as Pi natively supports. The
  workspace-wide rule was about Claude/Codex's specific behavior
  (overrun, lane-violation risk); Pi's sub-agent shape is different
  (configurable, scoped, observable through pi events).

Designer lean: **Stance A** for v1 — keep the discipline
symmetric until psyche explicitly relaxes it. The sub-agent
extension installs; the system prompt or default config disables
autonomous dispatch. Operator can enable per-session if the task
warrants. Per /264 the designing protocol is psyche-to-agent — and
the psyche just authorized Pi sub-agents in their voice prompt to
cluster-operator. So Pi sub-agents are enabled NOW for cluster-operator's
testing; whether they stay enabled by default is the open question.

## 5. Provider configuration

Per intent 227: GPT-5.5 xhigh default, GPT-5.4-mini available.
Mentioned also in psyche prompt: GLM 4.7, Magistral, Qwen 3.x
(retire), Gemma (add).

Concrete provider list for v1 bootstrap config:

```
default: GPT-5.5 with thinking_level=xhigh
fallback (per intent 40 fallback chain):
  - GPT-5.5 with thinking_level=high
  - GPT-5.4-mini (for quick searches; user-selectable)
available local models:
  - GLM 4.7
  - Magistral
  - Gemma (latest)
retired:
  - Qwen 3 / Qwen 3.5 (per psyche prompt: "we don't need Qwen 3.5 anymore")
```

Per intent 44 (per-role model selection): Pi's default role-mapping
is GPT-latest with Maximum Thinking. Intent 47 (Persona Pi default
config) puts this in `bootstrap-policy.nota` for the eventual
persona-pi triad. v1 just sets it via Pi's native config + a Pi
extension that registers the provider chain.

Login: psyche has a GPT subscription. Pi must be logged in. Likely
a Pi profile config + token stored via NixOS home-manager secrets
(matches the workspace's sops-nix discipline).

## 6. Terminal-cell vs Ghostty spawn

Psyche named both as acceptable spawn surfaces. For v1 testing
either works; the design pressure is on which path persona-pi (v2)
ultimately uses.

- **Ghostty spawn** — Pi runs as a normal terminal application
  under Ghostty. Simplest; what Codex does today. No persona-stack
  integration.
- **Terminal-cell spawn** — Pi runs inside a persona-terminal cell.
  Brings Pi under persona-terminal's lifecycle, observable surface,
  and transcript capture. Aligns with /266 §2 (dual-path: terminal
  cell + harness API).

Designer lean for v1: **Ghostty first, terminal-cell as next-slice.**
v1 ships fast as a Codex replacement under Ghostty; terminal-cell
integration is a follow-up that brings Pi under persona discipline
without blocking v1. Operator can test both per psyche request
("get a test for that too"). Terminal-cell integration is also
where /281's headless RPC mode becomes relevant — the persona-terminal
can speak Pi's RPC protocol directly without going through Ghostty.

## 7. Open questions for psyche

Each waits on psyche direction. Not blocking v1 ship, but resolution
shapes follow-up slices.

- **Q1 — Sub-agent default**: enabled or disabled by default? (See
  §4 Stance A vs B.) Psyche enabled for cluster-operator's testing
  session; standing default unset.
- **Q2 — Rewind mechanism**: Pi-built-in session-tree/session-fork
  feature, or community extension? Verify with `pi --help` /
  Pi docs.
- **Q3 — Theme-switching system signal source**: which NixOS/Hyprland/
  desktop signal does Pi listen to? `gsettings`, `dconf`, a
  home-manager-maintained file, or another path?
- **Q4 — Bundle scope for v1**: does the v1 extension list above
  (§2) match psyche's "community standard" filter, or are there
  additions / subtractions? Especially: is `web_search` in v1,
  or operator-only via per-session enable?
- **Q5 — v2 timing**: when does the persona-pi triad (/266) land
  relative to v1's deployment? Park per intent 166, or bring
  forward if v1 hits a fundamental design tension?

## 8. References

- **Intent record 227** — target shape settled.
- **Intent record 44 + 47** — Pi default = GPT-latest + Maximum
  Thinking (refers to xhigh equivalent).
- **Intent record 40** — LLM call fallback chain.
- **Intent record 166** — designer pivots to /249 gap-closure;
  parks persona-pi triad work. v1 is the immediate practical
  pickup; v2 is parked.
- **`reports/designer/266-persona-pi-triad-design.md`** — long-term
  triad shape; v1 stays compatible.
- **`reports/designer/268-persona-pi-operator-input.md`** — operator
  brief; v1 doesn't need to answer its 7 forks (those are v2 forks).
- **`reports/designer/281-headless-pi-research.md`** — Pi headless
  modes, extension surface; banner notes "depend on pi-ai"
  recommendation superseded by persona-llm-client direction.
- **`reports/cluster-operator/5-refresh-after-new-intents-and-reports-2026-05-22.md`**
  — cluster-operator's current implementation plan.

This report retires when v1 ships in CriomOS-home + the extension
bundle is documented + theme-switching is verified to work mid-task.
