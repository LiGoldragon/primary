# 21 — Audit of cluster-operator/6 (Pi harness defaults and extension packaging)

*Third-designer audit + critique of cluster-operator's v1 Pi-as-Codex-
replacement implementation slice per psyche request. Implementation
landed in `CriomOS-home` change `pmrrqvkn`; live-active on `ouranos`
via `lojix-cli HomeOnly Activate`. The Codex-replacement target from
intent 227 is largely hit; one psyche-stated hard requirement is
absent and three v1-class operator-safety gaps remain.*

## 1. Verdict

**Ship-worthy as a Codex-replacement minimum**, with three gaps that
should land in a quick follow-up slice before the harness handles
sensitive production work. The work hits intent 227's target shape
(GPT-5.5 xhigh default, GPT-5.4-mini available, packaged extensions,
Ghostty spawn) and the verification discipline is strong (51-token
theme assertion + check on declared defaults + live `pi` probes).
Cluster-operator's lane discipline held — they correctly stopped at
the persona-lock boundary and didn't edit the broken smoke script.

## 2. Strengths

- **Nix-declared profile replaces hand-edited `~/.pi/agent/settings.json`.**
  Pure workspace discipline win; the previous state was the kind of
  hidden ambient-state config the workspace rules out everywhere else.
- **Real verification, not just compile-check.** `nix flake check` +
  `lojix-cli HomeOnly Activate` + live `pi` probes returning `pi-ok`
  and `default-ok`. The check derivation asserts 51 color tokens
  exist per theme — falsifiable, structural.
- **My /20 Q2 (rewind mechanism) closed elegantly.**
  `doubleEscapeAction = "tree"` routes Pi's built-in session-tree
  feature as the rewind primitive. No community extension needed; Pi
  has it native through `session_tree` / `session_before_fork` events.
  Better answer than my /20 sketched.
- **`pi-subagents` is the right first extension package.** Matches
  intent 227's "packaged Pi extensions" and the psyche's explicit
  "best sub-agent feature so GPT can have sub-agents" request. 0.25.0
  pinned cleanly.
- **Both themes packaged** (`criomos-dark` + `criomos-light`) — the
  raw material for day/night switching is on disk even though the
  switcher itself is absent (§3 below).
- **Honest gap-listing.** Cluster-operator names the broken
  terminal-cell smoke and the missing persona-pi triad explicitly,
  with proper lane-discipline (didn't edit `persona/` because
  another lane holds it). Good agent hygiene.

## 3. Gaps to close (priority order)

### 3.1 — Mid-task day/night theme auto-switching (HARD GAP)

**Psyche's stated hard requirement was not addressed.** From the
voice prompt: *"the nighttime and daytime theme switch doesn't even
work on Codex while it's running on a task, so now I have to see
this wrong theme go by and the inverted terminal is barely readable
and it's offensive at night."*

v1 ships static `criomos-dark` as the default. Both themes are
packaged but no extension listens for a system theme change and
swaps Pi's active palette mid-session. /20 §3 named three mechanism
options (system signal listener / file-watch / time-based schedule);
the report addresses none.

**Recommended follow-up slice**: add a `pi-criomos-theme-switcher`
extension that registers a Pi `tool_call` / `before_provider_request`
hook to re-read the theme indicator and apply via Pi's theme API.
Source of truth — open question Q1 in §5 below.

### 3.2 — Operator-safety extensions absent

Pi is replacing Codex for operator work in a jj-driven workspace
that touches sensitive paths (`intent/*.nota`, `~/.local/state/persona-spirit/`,
production lojix-cli flake.lock). v1 should include workspace-discipline
safety extensions before it touches `primary-wvdl`-class work:

- **`confirm_destructive`** — guards `rm -rf`, `jj abandon`,
  `git push --force`, etc.
- **`dirty_repo_guard`** — refuses operations when the working copy
  has unrelated changes from other lanes (matches the partial-commit
  pattern this workspace lives in).
- **`protected_paths`** — `intent/*.nota`, `~/.local/state/persona-*/`,
  CriomOS-home flake.lock should require explicit unlock to edit.

None of these are in v1. They're community extensions per /281; package
the same way `pi-subagents` was packaged.

### 3.3 — Sub-agent default stance undeclared

/20 §4 raised: when `pi-subagents` is installed, does the GPT agent
dispatch sub-agents autonomously (Pi-native) or require explicit
per-session authorization (workspace symmetric with AGENTS.md
no-subagents-by-default for Claude/Codex)? v1 packages the extension
but the `pi-models.nix` doesn't configure default sub-agent
authorization. The psyche enabled sub-agents in the cluster-operator
testing session by saying "use sub-agents to get a sense"; standing
workspace default is open.

Concrete artefact to add: a setting in `pi-models.nix` or a
`pi-subagents` config field controlling whether the extension's
agent-launch is autorun or requires user/owner explicit approval.

## 4. Smaller items

- **`pi-linkup` is undocumented in the report.** Third package
  alongside `pi-criomos` and `pi-subagents`. What does it provide?
  Web-search? Operator workflow tool? Should be named in §"Result"
  with one line on capability.
- **No bead filed for the broken terminal-cell smoke.** The error
  (`terminal-cell-wait failed: unknown wait argument: --socket`) is
  a real persona-side regression — likely from intent 215/216's
  rename pressure or older drift. `bd create` would let
  whichever lane picks up `persona` next know about it without
  re-discovering. Suggest title: *"persona-engine-sandbox-terminal-cell-smoke:
  update --socket call to current terminal-cell-wait shape"*.
- **No bead filed for the persona-pi triad next slice.** Cluster-operator
  names "no `persona-pi` triad component" as a remaining gap; the
  bead exists as `primary-u7gc` (blocked, per /283 §"Beads filed")
  but the path from v1 to v2 isn't explicit. The recommended
  `--mode rpc` framing in the report's §"Remaining Gaps" matches
  /281's headless RPC finding + /20 §6's terminal-cell-as-next-slice
  recommendation; the bead's description should incorporate that.
- **Not pushed.** Local-only landing on `ouranos`. If Bird/Zeus need
  the same Pi setup (cluster-operator/1 + intent 176), the change
  needs pushing through CriomOS-home main. Operator note flags this;
  closes when pushed.
- **`openai-codex` as provider name** — interesting. The provider
  routes GPT-5.5/5.4 through Codex API endpoints rather than
  OpenAI-direct. Not a critique, just worth knowing for future
  provider config decisions.
- **No `model_status` / `working_indicator` / `status_line`
  extensions** — Pi UI polish from /20 §2. Lower priority than the
  three gaps in §3; could land in a single "polish" follow-up slice.

## 5. Open questions

- **Q1 — Theme indicator source**. What system signal does CriomOS-home
  track for day/night? `gsettings get org.gnome.desktop.interface
  color-scheme`, Hyprland's session theme, a file under
  `~/.local/state/criomos/theme`, or a new mechanism? The
  `pi-criomos-theme-switcher` extension needs a concrete listen-target.
- **Q2 — What `pi-linkup` provides**. Naming suggests link/URL handling
  or a connector extension. Confirm scope so it can be documented.
- **Q3 — Sub-agent default authorization shape** (carry-over from
  /20 §4). Pi-native autonomous, or workspace-symmetric require-explicit?
- **Q4 — When does v2 (persona-pi triad) land relative to /249
  gap-closure?** Intent 166 parked persona-pi; intent 209 + 215/216
  prioritize Persona. v1 ships as a Codex replacement; v2 timing
  is psyche-decided. Cluster-operator's report leaves it open.
- **Q5 — Push CriomOS-home `pmrrqvkn` upstream?** Once Bird/Zeus
  want this Pi setup, push is required. Operator scheduling.

## 6. Recommended next slice

**Single follow-up slice covering §3 (the three v1 gaps):**

1. Implement `pi-criomos-theme-switcher` extension (Q1 source TBD).
2. Package `confirm_destructive`, `dirty_repo_guard`, `protected_paths`
   community extensions as Nix derivations (same shape as
   `pi-subagents`).
3. Set sub-agent default authorization mode in `pi-models.nix` (Q3
   answer).
4. File two beads (terminal-cell smoke fix, persona-pi v2 transition
   plan).

Estimated cluster-operator-day. The verification discipline is
already established from this slice (typed checks, live probes);
follow-up only needs to extend the check assertion set.

## 7. References

- **`reports/cluster-operator/6-pi-harness-defaults-and-extension-packaging-2026-05-22.md`**
  — the slice this audit covers.
- **`reports/third-designer/20-pi-as-codex-replacement-design-2026-05-22.md`**
  — the designer-side design preceding this slice.
- **`reports/cluster-operator/5-refresh-after-new-intents-and-reports-2026-05-22.md`**
  — cluster-operator's prior refresh context.
- **Intent record 227** — Pi target shape settled.
- **Intent records 215 + 216** — Persona naming; relevant to the
  terminal-cell smoke regression's likely root cause.
- **`reports/designer/281-headless-pi-research.md`** — Pi headless
  RPC mode; relevant to persona-pi v2 transition.

This audit retires when §3's three gaps are addressed in a follow-up
slice, OR psyche explicitly accepts v1 as sufficient.
