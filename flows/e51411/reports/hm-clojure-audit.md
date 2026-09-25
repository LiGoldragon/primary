# Audit: the Clojure proof of concept of Hacking Messenger

Target: branch `hm-clojure-00f95a` at `30c0b1ca` (re-targeted from
`d478c928` at the main flow's instruction) in
`/git/github.com/LiGoldragon/HackingMessenger`. It adds Datalevin 0.8.25
through the Babashka pod (`src/hacking_messenger/store.clj`). The Python
reference is `hm.py` on the same tree (merge base `055d057`). Line references
are `core.clj`, `main.clj` and `store.clj` under `src/hacking_messenger/`
at `30c0b1ca`.

Method: `git archive` of both revisions into a scratch directory. The shared
checkout was left alone; it holds another flow's uncommitted `hm.py`. The
runtime was Babashka v1.13.219. Every write went to a scratch `HM_REGISTRY`.
No `herdr agent prompt` was issued. The only Herdr call was
`herdr --definitely-not-a-flag`, and `hm-clj list` ran once against the real
registry, which is read-only.

## Overall verdict

**Not met.** It is not a working proof of concept. The shipped `bin/hm-clj-*`
entry points fail to load. Every EDN read and write on disk throws. Because the
attempt write throws after the prompt is delivered, every successful send reports
failure, and a retry sends the message again. Malli is used at a few edges only.
The code is not object-oriented. Datalevin is written to but never read by the
program. Only the relay envelope (EDN, one line, at most 800 characters, with a
round-trip check) works as specified.

## Verdict per requirement

| Requirement | Verdict | Evidence |
|---|---|---|
| An object-oriented version of the Rust approach | **Not met** | Free functions only: no `defprotocol`, `defrecord` or `deftype` anywhere (`core.clj:25-114`). The Python version is itself a `Messenger` class (`hm.py:79`). |
| Typed with Malli / "Malli on every value" | **Partly met** (edges only) | See the Malli findings below. Herdr replies (`core.clj:55,64,93`), the Datalevin writes (`store.clj:26-41`) and the environment are not validated. `FlowId` and `NativeThread` match partially (`core.clj:13-14`). `:reason` and `:grade` are bare `:keyword` (`core.clj:18`). Four schemas are never applied to a value (`core.clj:16,19-21`). Line 23 builds validators and throws them away. |
| Pure Clojure on EDN and the Datomic-family libraries, emulating Ethos, no porting | **Partly met** | Pure Babashka Clojure with EDN; nothing is ported from Datom or Ethos, which is right. Datalevin, a Datalog store in the Datomic family, is transacted (`store.clj:26-41`), but the program never queries it. `attempts-for` (`store.clj:43`) is called only from the test (`core_test.clj:23`). Routes are still read from EDN files (`core.clj:47-51`), and those reads are broken (F2). DataScript was removed in `d478c928`. |
| Machine messages are real EDN and actually processed | **Partly met** | `relay` (`core.clj:31-41`) builds `{:machine/relay [...]}`, validates it against `MachineRelay`, prints it and reads it back. Tested: quotes, `«»`, backslashes and a newline in the body all round-trip, and the line stays one line. Only the sender processes it, though: nothing receives or parses a relay. The output uses namespaced-map syntax, `#:machine{:relay ...}`, which is a Clojure-reader extension and not in the edn-format spec (F11). |
| The living's words are never EDN | **Met** (by construction) | HM wraps only the machine sender's body (`core.clj:35`). The living's input never passes through HM. |
| Pane fallback (held, unregistered or stale send prompts the pane directly, with its own grade) | **Not met** | The title lookup never matches (F3). The stored-route fallback branch is unreachable (F4). A held route has no model: no retirement, `route_hold` or transition check. A stale route is never detected (F5). `Fallback-Presented` is claimed without a presentation wait (F6). Held sends are not recorded (F7). Only an explicit `--pane session:pane` can work, and then the post-send write throws (F1). |
| No new features | **Met**, with reservation | No features beyond the fallback and the approved changes. The Datalevin index is infrastructure, not a feature. |
| EDN on disk | **Not met** | `spit` and `slurp` are given a `java.nio` `Path` (`core.clj:45,50,88`). Clojure's `io` cannot open that, so every call throws `Cannot open <UnixPath ...>`. Reproduced for `atomic-edn!`, `read-route` and `append-attempt!`. |
| `--help` names the compensation-hacking-messenger skill | **Partly met** | `bb -m hacking-messenger.main --help` prints the skill note (`main.clj:3,8`) and exits 0. The wrappers cannot print it (F1). `send --help` gives `hm: Invalid MessageBody ...` with exit 1, and `register --help` gives `register requires --session ...` with exit 1. Python prints the note on every subcommand's help (`hm.py:779-780`). |
| One line of 800 characters or less | **Met** | `core.clj:37-38` refuses a newline or more than 800 characters, and `pr-str` escapes newlines. The largest ASCII body that fits is 705 characters with `MESSAGING_SEAT=probe`. The count is in UTF-16 units, so emoji count double, which errs on the safe side. The failure text says "message held", but nothing is held (F7). |
| Parity with Python's argv, output and exit codes | **Not met** | See F8. |

## Findings, most severe first

**F1. Critical: the shipped entry points do not run.** `bin/hm-clj-{send,list,register}:4`
pass `-cp "$here/../src"`, and that replaces the classpath that `bb.edn`'s
`:deps` would supply. Every wrapper therefore dies at `core.clj:8` with
`Could not locate malli/core.bb` and exits 1. Reproduced at both
`d478c928` and `30c0b1ca`. The tests pass only because they are run with
`bb.edn` in the working directory and no `-cp`.

**F2. Critical: all EDN file I/O throws.** See the "EDN on disk" row. The
consequences:
- `read-route` always fails. `send!` swallows the error (`core.clj:104`), so
  `stored` is always nil and every send takes the fallback.
- `register!` queries Herdr and then throws before writing (`core.clj:97`).
- `listing!` (`core.clj:113`) throws as soon as any `*.edn` file exists,
  including `attempts.edn`.

`hm-clj list` against the real registry printed only the header and exited 0.
That registry holds only `*.json` files.

**F3. Critical: a retry sends the message again.** `send!` prompts the pane
first (`core.clj:108`) and writes the attempt afterwards (`core.clj:110`). That
write always throws (F2). Even once fixed, it can still fail after delivery: the
disk may be full, or the pod may be unavailable (`store.clj:7,89`). The
exception reaches `main.clj:16` as a plain `hm: ...` with exit 1. There is no
`Uncertain.{ flow attempt-... }` framing and no "do not retry" text, so the
caller sees a failed send for a message that was delivered.

The same applies to a Herdr error after injection, such as
`agent_prompt_stalled` or a `--wait` timeout. Python turns that into
`Uncertain`/`Stalled` with a recorded attempt (`hm.py:687-692`).

Herdr calls have no timeout (`core.clj:53`); Python uses 15 seconds
(`hm.py:35`). The `exit` check at `core.clj:54` is dead code, because
`babashka.process/shell` throws on a nonzero exit before it is reached. Tested:
`:hm/failure` is absent on that path.

**F4. High: the fallback by Flow title never matches.**
`(re-pattern (str "\\\\b" ...))` at `core.clj:79` compiles to the regex
`\\b\Qe51411\E$`, which requires a literal backslash followed by `b`. Tested:
it returns false against `"Psyche Medium e51411"`. Combined with F2, every send
without `--pane` ends at `Held: Flow title has no unique live Herdr agent`.

**F5. High (latent until F2 is fixed): a stale or recycled stored route is
prompted blindly.** When `stored` exists, `send!` prompts `(:pane_id stored)`
directly (`core.clj:105`). It makes none of these checks:
- no `agent get` identity check;
- no `interactive_ready` or `blocked` status check;
- no native-thread process match;
- no post-send check;
- no retirement check;
- no Orchestrate reservation.

Python makes all of them (`hm.py:636-699`). A pane ID that was reused after a
Flow ended would receive another Flow's message. The `stored` branch of
`fallback-route` (`core.clj:76-78`) is the one that would re-resolve a stale
route. It is unreachable, because `send!` calls `fallback-route` only when
`--pane` is given or `stored` is nil. If it were reached, its result would not
be Malli-validated.

**F6. High: the grade overclaims.** Every fallback send is graded
`Fallback-Presented` (`core.clj:109`), even without `--wait-presented`, when
only transport happened. The success line always says `working`
(`core.clj:111`); Python reports the live `agent_status` (`hm.py:702`). With
`--pane` and no stored route, the attempt records a made-up
`native_thread` of `00000000-0000-0000-0000-000000000000` as the binding
(`core.clj:75,82`).

**F7. High: held sends are not recorded.** This confirms Mind's own account.
`store/index-pending!` (`store.clj:37`) and the `PendingIntent` schema
(`core.clj:19`) are never called. Every `Held:` path is a bare `fail`
(`core.clj:74,77,81`) that writes no attempt and no pending intent. The same is
true of the 800-character refusal that says "message held" (`core.clj:38`).
Python writes `attempts.jsonl` plus `pending/<id>.json` for a held send
(`hm.py:107-118,121-123`), bounded-waits with `--hold-seconds`, and prints
`Held.{ flow reason attempt-... }`. The fallback rule depends on knowing what was
held, and here a held message is lost.

**F8. Medium: parity gaps with Python.**
- **Missing subcommands:** `send-abrupt`, `deregister`, `rebind`, `move`, `retire`
  and `import-retirement`.
- **`--hold-seconds`:** ignored silently.
- **Unknown flags:** ignored (`main.clj:4,10`).
- **`register`:** it needs `--session` and `--native-thread`, which Python makes
  optional. It also drops `--readiness-probe` and `--rollout`. It skips the
  `interactive_ready` check, the retirement check, the reservation, and the check
  for a prior binding to a different terminal, so it would silently overwrite
  that binding (`core.clj:91-99` against `hm.py:303-345`).
- **Exit codes:** Python's argparse errors (missing body, unknown operation) exit
  2; Clojure exits 1.
- **Held output:** Python prints `Held.{...}` without the `hm:` prefix; Clojure
  prints `hm: Held: ...`.
- **`list`:** Python lists live agents with their status and marks stale ones
  `STALE`. Clojure lists only registry files and marks every one `REGISTERED`.
- **Registry:** both use the same `~/.local/state/hacky-messenger` directory, as
  `*.json` and `*.edn` respectively. A Flow registered by one implementation is
  `NotRegistered` to the other.

Where it matched on the same inputs: a missing `FLOW_ID`, an empty body and a
control character all give the same message and exit 1.

**F9. Medium: Malli validates only at the edges, and weakly there.**
- **Partial matches:** Malli's `:re` uses `re-find`, so `FlowId` accepts
  `"../../etc/x"` and `"a b!"`, and `NativeThread` accepts
  `"!!!!!!!!!!!!!!!!a"` (all tested). The result is path traversal:
  `(hm/path "../../etc/x")` resolves outside the registry. Python uses
  `re.fullmatch` (`hm.py:85`).
- **Unconstrained reason and grade:** `:reason` and `:grade` are `:keyword`
  although the enums exist (`core.clj:11-12,18`). Tested:
  `{:reason :anything :grade :NotAGrade}` validates.
- **Discarded validators:** line 23 compiles validators and throws them away.
- **Values never checked:** Herdr JSON, live-agent maps, `MESSAGING_SEAT`, the
  wait flag, and every value handed to Datalevin.
- **Schemas never applied:** `ReadinessProof` beyond its optional slot,
  `PendingIntent`, `RetirementMarker` and `Reservation`.

**F10. Medium: a relay can be nested inside a relay.** A relay line given as
the body becomes an escaped string inside a second `{:machine/relay ...}`
(tested). There is no guard. The EDN structure is not nested, so it stays
unambiguous, but a forwarded relay gains a second header. The sender `FLOW_ID`
`"a b"` passed `MachineRelay` because of F9's partial matching.

**F11. Low: the relay uses namespaced-map syntax.** Babashka's `pr-str`
prints `#:machine{:relay [...]}`. `clojure.edn` reads it, but the syntax is not
part of the edn-format spec, so a non-Clojure EDN reader (for example the Rust
reader Ethos would have) may reject it. Binding `*print-namespace-maps*` to
false would give `{:machine/relay [...]}`.

**F12. Low: Datalevin is written, never read, and not in step with the EDN
files.** Each write opens and closes a pod connection (`store.clj:21-24`). It
runs after the EDN `spit` (`core.clj:88-89,97-98`), so a failure between the two
leaves the file and the index disagreeing. The pod loads when the namespace
loads (`store.clj:7`), so even `--help` and `list` need the pod, and a fresh
machine must download it. Tested in isolation, the store works: an attempt with
a nested `:binding`, a route, and the `attempts-for` query all worked on a
scratch root.

**F13. Low: the tests and docs do not cover the Clojure code.** The tests
cover only the relay and a direct pod round trip (`core_test.clj`). Nothing
exercises `send!`, `register!`, `listing!` or a wrapper, which is how F1 and F2
got through. `check.nix` runs only the Python unit tests. `README.md` and
`ARCHITECTURE.md` do not mention the Clojure version. `quote-datom`
(`core.clj:30`) is unused.

## What held up

- The relay envelope works as specified: bounded, one line, escaped and
  round-tripped.
- The `Fallback-Presented` grade is kept apart from the ordinary grades, so the
  grading intent is visible.
- `--pane` requires exactly one live match (`core.clj:74`).
- The control-character rule is equivalent to Python's.
- The Datalevin pod transacts and queries under this Babashka.
- The tests pass: 2 tests with 6 assertions at `30c0b1ca`; 34 Python tests
  pass on the same tree.

## Sources

- `git -C /git/github.com/LiGoldragon/HackingMessenger log 055d057..30c0b1ca`:
  `45f0e18`, `51f0319`, `d478c92`, `9698533`, `30c0b1c`.
- Files at `30c0b1ca`: `bb.edn`, `bin/hm-clj-{send,list,register}`,
  `src/hacking_messenger/{core,main,store}.clj`,
  `test/hacking_messenger/core_test.clj`, `check.nix`, `hm.py`.
- Probes run in scratch copies with a scratch `HM_REGISTRY`: the wrapper runs,
  `bb -m hacking-messenger.main --help|list|send|register`, and a `bb -e`
  harness calling `hm/relay`, `hm/path`, `hm/atomic-edn!`, `hm/read-route`,
  `hm/append-attempt!`, `hm/listing!`, `hm/herdr!`, `m/validate`,
  `store/index-attempt!`, `store/index-route!` and `store/attempts-for`.
  Python was run with `python3 hm.py` on the same argv.
- Requirements: `flows/e51411/vision/messaging.md`,
  `flows/e51411/notion/stack.md`, `flows/e51411/vision/launch.md`,
  `flows/e51411/reports/pasted-content-threshold.md`.

## Re-audit 514f297f

Target: branch `clojure` at `514f297f` (`00f95a: add Hacky Messenger Clojure
value protocols and strict IDs`) in
`github.com/LiGoldragon/HackyMessenger` (repo renamed from
`HackingMessenger`). Compared against `main` at the same clone
(`hm.py` unchanged in relevant parts). Method: `git archive` of `514f297f`
and `main` into scratch trees, Babashka v1.13.219, a scratch `HM_REGISTRY`
for both implementations; no real pane; `herdr` reachable but no session
attached, so live-agent lookups fail cleanly. Ran `bb -e` against
`hacky-messenger.core-test`, each `bin/hm-clj-*` wrapper's `--help`, a
traversal probe (`FlowId = "../../etc/x"`), and `hm.py`/`hm-clj-*` argv
comparisons for `register`, `send`, `list`.

**Tests: 6 tests, 21 assertions, 0 failures** (up from 2 tests/6 assertions
at `30c0b1ca`). `test/hacky_messenger/core_test.clj` now exercises `send!`,
`held!`, `resolve-send-route`, and the Datalevin store directly.

**F1 (entry points don't run): Fixed.** `bin/hm-clj-{send,list,register}`
now `exec bb --config "$here/../bb.edn" -m hacky-messenger.main ...`
instead of `-cp "$here/../src"`. All three wrappers' `--help` print the
skill note and exit 0.

**F2 (all EDN file I/O throws): Fixed.** `atomic-edn!`, `read-route` and
`listing!` now `spit`/`slurp` `(str destination)`/`(str p)` instead of a
raw `java.nio.Path`. `register!`, `send!` and `list` all run past disk I/O
without the `Cannot open <UnixPath ...>` error.

**F3 (retry sends the message again): Fixed.** `send!` now writes a
`:Submitting`/`:Uncertain` attempt (`core.clj:165`) before prompting; a
prompt failure surfaces as `Uncertain.{ flow attempt-... } prompt failed or
is uncertain: ...` (`core.clj:172`), not a bare `hm: ...`. `herdr!` now
passes `:timeout 15000`, matching Python's 15s. Confirmed by the passing
test `stale-route-is-fallback-presented-and-prompt-failure-is-not-retried`
(prompt called exactly once).

**F4 (title-fallback regex never matches): Fixed.** `core.clj:113` is now
`(re-pattern (str "\\b" (java.util.regex.Pattern/quote flow) "$"))` — a
single backslash, a real `\b` anchor — not the old quadruple-backslash dead
pattern. The passing test `identifiers-and-title-fallback-are-strict`
covers the by-title match.

**F5 (stale/recycled route prompted blindly): Partly fixed.**
`exact-live-route?` (`core.clj:117-123`) now requires all five fields
(session, name, pane_id, terminal_id, agent) to match a live agent before
skipping fallback; a mismatch re-resolves through `fallback-route`, which is
reachable now. `verify-target!` (`core.clj:84-94`) runs before every prompt
and checks identity, `interactive_ready`, and `blocked`. Still missing vs
`hm.py:636-699`: no native-thread/process match, no retirement check, no
Orchestrate reservation.

**F6 (grade overclaims): Partly fixed.** The success line now reports the
live `agent_status` (`core.clj:170`, `(or (:agent_status live) "unknown")`)
instead of a hardcoded `"working"`. `Fallback-Presented` is still forced on
every fallback send regardless of `--wait-presented` (`core.clj:168`) —
unchanged overclaim.

**F7 (held sends not recorded): Fixed.** `held!` (`core.clj:138-144`) now
writes a `:Held` attempt to `attempts.edn`, a `pending/<id>.edn` file, and
calls `store/index-pending!`. Verified live: a traversal probe (`send
../../etc/x`) produced `pending/<uuid>.edn` and an `attempts.edn` line, and
the test `held-unregistered-writes-edn-and-datalog-pending-without-prompt`
passes.

**F8 (parity gaps): mostly open.** See the parity list below — nothing here
changed except the exit/output shape of the traversal case.

**F9 (Malli validates weakly / traversal): partly fixed, with a new
wrinkle.** Traversal is blocked in practice: `hm/path` still throws for
`"../../etc/x"` and `"a b!"` (test `identifiers-and-title-fallback-are-strict`
passes), because `path` calls the manual `flow-id!` guard
(`core.clj:28-30`, `re-matches` on `[A-Za-z0-9][A-Za-z0-9_-]{0,95}`), which
gates every path-construction site. But `send!`/`register!` validate the
raw flow argument with `(valid! FlowId flow "FlowId")` — the *Malli* schema
— not `flow-id!`. Tested directly: `(m/validate FlowId "../../etc/x")` and
`(m/validate FlowId "a/b")` both return `true`. Malli's `:re` property on a
`[:string {...}]` schema is not "weak/partial-match via re-find" as the
prior audit described — it is a complete no-op (`[:re pattern]` is a
separate schema type; `:re` is not a recognized `:string` property).
Consequence: `hm-clj-send '../../etc/x' body` does not reject the ID up
front the way `hm.py` does (`Flow ID must contain only letters, digits,
underscores, or hyphens`, exit 1, nothing written); instead it falls
through to `held!` and writes `{:flow "../../etc/x" ...}` verbatim into
`attempts.edn` and Datalevin (confirmed on disk). No file escape occurs,
only because `path`'s independent strict check still guards every actual
filesystem write.

**F10 (nested relay): unchanged/open**, not re-probed this pass; `relay`'s
code is unchanged in this branch.

**F11 (namespaced-map EDN syntax): open, unchanged.** `(hm/relay ...)`
still prints `#:machine{:relay [...]}` (confirmed live); no
`*print-namespace-maps*` binding was added.

**F12 (Datalevin written, never read by the program): partly fixed.**
`store/attempts-for` and `store/pending-for` exist and are exercised by
tests, and `held!` now calls `store/index-pending!`. But
`grep -n "store/" src/hacky_messenger/*.clj` shows only
`index-attempt!`/`index-pending!`/`index-route!` calls — `attempts-for` and
`pending-for` are never called from `core.clj` or `main.clj`. `listing!`
still reads only `*.edn` files; Datalevin stays write-only in the running
program.

**F13 (tests/docs don't cover the Clojure code): partly fixed.** Tests grew
from 2/6 to 6/21 assertions and now cover `send!`, `held!`,
`resolve-send-route` and the store — exactly the gap F13 named. `check.nix`,
`README.md` and `ARCHITECTURE.md` still have no mention of the Clojure tree
(grep, no hits). `quote-datom` (`core.clj:53`) is still unused.

**Object-oriented requirement: moved from Not met to Partly met, decorative.**
`core.clj:39-47` now declares `defprotocol Registry`, `HerdrTransport`,
`Ledger`, `Clock` and `defrecord SystemClock`, `EdnRegistry` — real OO
syntax, satisfying the letter of the requirement. But
`grep -n "EdnRegistry\|SystemClock\|HerdrTransport\|Ledger" src/*.clj`
shows no instantiation (`->EdnRegistry`, `->SystemClock`) and no dispatch
through these protocols anywhere: `HerdrTransport` and `Ledger` have zero
implementing records at all. `send!`, `register!` and `listing!` still call
the free functions (`read-route`, `atomic-edn!`, `herdr!`, `append-attempt!`)
directly. The protocols are dead scaffolding, not the control-flow
mechanism.

**Parity with `hm.py` on `main`, re-verified this pass:**
- **Still missing subcommands:** `send-abrupt`, `deregister`, `rebind`,
  `move`, `retire`, `import-retirement` — `bin/hm-move`, `hm-rebind`,
  `hm-retire`, `hm-send-abrupt` still shell to `python3 hm.py`; no Clojure
  equivalents exist.
- **`--hold-seconds`:** still absent from `main.clj`'s arg parsing; silently
  ignored if passed.
- **Unknown flags:** still silently ignored (`main.clj`'s `arg` helper).
  Python's argparse rejects an unknown flag with exit 2.
- **`register`:** still hard-requires `--session` and `--native-thread`
  (Python makes them optional with fallback probing); still no
  `--readiness-probe`/`--rollout`; still no `interactive_ready` check, no
  retirement check, no reservation, no check for an existing binding to a
  different terminal before overwrite (`core.clj:145-153` vs
  `hm.py:303-345`, unchanged).
- **Exit codes:** confirmed again — `hm.py send` with missing args exits 2
  (argparse) and prints a `usage:` block; `hm-clj-send` with missing args
  exits 1 with `hm: Invalid FlowId: ...`. An unknown top-level operation:
  `hm.py bogus` exits 2 (argparse `invalid choice`); `bb -m
  hacky-messenger.main bogus` exits 1 and prints the usage text via `fail`.
- **Held output:** Python prints the bare `Held.{...}` message (no `hm:`
  prefix — `hm.py:853`, `isinstance(error, Held)`); Clojure still prints
  `hm: Held.{ ... }` for every failure including Held, since `main.clj`
  does not distinguish Held from any other exception.
- **`list`:** confirmed unchanged. `hm.py list` queries live Herdr agents
  and prints their real `agent_status` (tested against the live registry:
  11 real rows with statuses like `idle`/`working`/`done`). `hm-clj-list`
  against an empty scratch `HM_REGISTRY` prints only the header — it reads
  local `*.edn` route files, not live agents, and has no `STALE` marking.
- **Registry format:** unchanged — `*.json` (Python) vs `*.edn` (Clojure)
  in the same `~/.local/state/hacky-messenger` directory; a Flow registered
  by one is `NotRegistered` to the other.
- **New this pass — traversal-ID rejection shape differs:** `hm.py send
  '../../etc/x' hi` rejects immediately (`Flow ID must contain only
  letters, digits, underscores, or hyphens`, exit 1, nothing written).
  `hm-clj-send '../../etc/x' hi` does not reject the ID at the same layer
  (F9 above); it exits 1 too, but only after writing a Held attempt/pending
  record carrying the unsanitized ID.

Where it still matches: `--help` text and exit 0 for all three subcommands
on both sides (module-level usage differs in wording/formatting, but both
name the compensation-hacky-messenger skill and exit 0); a missing/empty
body still gives exit 1 on both.

## Re-audit 47dc463d

Target: branch `clojure` at `47dc463d` (`00f95a: join live Hacky Messenger
listing`) in `github.com/LiGoldragon/HackyMessenger`
(`/git/github.com/LiGoldragon/HackyMessenger`, fetched fresh). 11 commits
past `514f297f`, all `src/hacky_messenger/{core,main}.clj` (194/29 lines
changed; `store.clj` untouched). Method: `git archive` of `47dc463d` into a
scratch tree, Babashka v1.13.219, a scratch `HM_REGISTRY`. Ran the full
test namespace, `hm-clj-list` once read-only against the real registry
(no writes — it only lists), and targeted `bb -e`/wrapper probes for each
open item below. No code changed, no message sent.

**Tests: 10 tests, 40 assertions, 0 failures** (up from 6/21 at
`514f297f`). New tests cover route gates end-to-end
(`route-gates-precede-the-prompt`: IdentityChanged, NotReady,
ProcessMismatch, Retired, Reservation-refused, then a real Transported
send), ledger-failure-blocks-prompt, and `listing!` joining live agents.

**Protocols/records actually used: Fixed.** `grep -n "->EdnRegistry\|
->ShellHerdr\|->EdnLedger\|->SystemClock" core.clj` shows each record
instantiated at its call site (`core.clj:63,89,107→113,183,222,234`), and
dispatch goes through the protocol methods (`load-route`/`save-route!`
on `EdnRegistry`, `record-attempt!`/`record-pending!` on `EdnLedger`,
`live-agents*`/`target-agent*`/`process-info*`/`prompt!*` on `ShellHerdr`
via `transport`, `current-time` on `SystemClock`). The test suite's
`fake-transport` (`core_test.clj:13-18`) and the `failing` `Ledger` reify
(`core_test.clj:109-111`) exercise this dispatch directly — a fake
implementation swapped in changes `send!`'s behavior, which only happens
if the protocol is the real control-flow mechanism, not scaffolding.

**Malli regex traversal: Fixed.** `FlowId` is now `[:and [:string ...]
[:re #"^[A-Za-z0-9][A-Za-z0-9_-]*$"]]` with `^`/`$` anchors
(`core.clj:13`); `NativeThread` similarly anchored (`core.clj:14`).
Tested directly: `(m/validate hm/FlowId "../../etc/x")` → `false`,
`(m/validate hm/FlowId "a b!")` → `false`,
`(m/validate hm/NativeThread "!!!!!!!!!!!!!!!!a")` → `false`. End to end,
`FLOW_ID=sender hm-clj-send '../../etc/x' hi` now rejects at
`flow-id!` (`core.clj:238`) with `hm: Flow ID must contain only letters,
digits, underscores, or hyphens`, exit 1, and writes nothing (confirmed:
`attempts.edn` and `pending/` in the scratch registry hold only the
unrelated `nosuchflow` probe, nothing for the traversal string). This
also closes the "new wrinkle" the previous pass found (traversal used to
fall through to `held!` and write the raw ID to disk).

**Stale route / native-thread / retirement / reservation checks:
Fixed.** All three gaps the previous pass listed as still missing are
now present and wired into `send!` via `with-reservation`
(`core.clj:242`): `process-matches!` (`core.clj:121-127,140`) checks the
live pane's `foreground_processes` argv against `:native_thread`;
`assert-not-retired!` (`core.clj:114-120,245`) reads and Malli-validates
a `RetirementMarker` and fails `Retired: <flow>`; `reserve!`/`release!`
(`core.clj:190-207`) shell out to `orchestrate` for a
`Lock.{ HackyMessengerDelivery ... }` around the whole delivery, parsing
the `Locked.{ <id> ...}` reply into a validated `Reservation`. The new
test `route-gates-precede-the-prompt` (`core_test.clj:122-149`) exercises
all four gates (`IdentityChanged`, `NotReady`, `ProcessMismatch`,
`Retired`, `Reservation refused`) plus a final real `Transported` send,
and asserts zero prompts fired before the last case — passing.

**Fallback-Presented without a wait: Fixed.** Fallback sends now force
`wait?` true (`core.clj:256`, `(or fallback? wait-presented)`) and the
grade is only assigned after `presented!` (`core.clj:101-106,258`)
confirms `(:presented reply)` is `true`; otherwise it throws
"Presentation was not observed; do not retry blindly" and no
`Fallback-Presented` attempt is recorded. Test
`fallback-presentation-requires-an-observed-wait-without-retry`
(`core_test.clj:77-104`) covers the granted case, the submission-only
case, and the timeout case, each asserting the prompt ran exactly once
(no retry) — passing.

**`attempts-for`/`pending-for` used: Fixed.** `grep -n "store/" core.clj`
now shows both called from production code, not only the test:
`append-attempt!` (`core.clj:187`) queries `store/attempts-for` to
confirm the just-written attempt is indexed before returning, and
`held!` (`core.clj:224`) does the same with `store/pending-for` for
pending intents — each fails loudly ("... did not confirm persistence")
if the Datalevin index and the EDN write disagree. `listing!` still
reads only `route-records` (EDN files) plus live agents, not the
Datalevin index, for its own output — the store is used as a
write-confirmation oracle, not yet as a read path for listing.

**Nested-relay guard: Fixed.** `nested-relay?` (`core.clj:76-80`) is now
called from `send!` (`core.clj:240`) before validation: a body that
parses as EDN containing `:machine/relay` is rejected with "Nested
Machine.Relay is not a message body". Test
`nested-machine-relay-is-rejected-before-send` (`core_test.clj:39-42`)
passes. F11 (namespaced-map `#:machine{...}` syntax) is unchanged and
still open — confirmed live: `(hm/relay "sender" "e51411" "body")` still
prints `#:machine{:relay [...]}`; no `*print-namespace-maps*` binding
was added.

**Parity, re-verified this pass:**
- **Unknown flags: Fixed.** `unknown-flags!` (`main.clj:6-8`) now rejects
  any `--`-prefixed argument not in the subcommand's allow-list. Tested:
  `hm-clj-send 00f95a hi --bogus` → `usage: ... hm-clj: error:
  unrecognized arguments: --bogus`, exit 2.
- **Argv exit code 2: Fixed.** `parse-error` (`main.clj:5`) is caught
  separately in `-main` and exits 2 (`main.clj:34`), matching argparse.
  Tested: missing `send` args, and an unknown top-level op
  (`bb -m hacky-messenger.main bogus`), both now exit 2 with a
  `usage: ...` prefix, matching Python's shape (Python still differs in
  exact wording, not exit code or prefix).
- **Held output prefix: Fixed.** `-main`'s catch (`main.clj:29-34`) omits
  the `hm: ` prefix when `(:hm/held (ex-data e))` is set. Tested live:
  `hm-clj-send nosuchflow hello` → `Held.{ nosuchflow NotRegistered
  attempt-... }` with no `hm:` prefix, exit 1 — matches `hm.py`'s
  `Held.{...}` shape.
- **`list` from live Herdr: Fixed.** `listing!` (`core.clj:278-293`) now
  joins `route-records` against `live-agents`, one row per live agent
  (flow names comma-joined, `-` if none) plus `STALE` rows for routes
  matching no live agent. Ran read-only against the real registry:
  `hm-clj list` printed 12 rows with real session/status data
  (`messaging-build`, statuses `idle`/`working`/`done`), all showing `-`
  for FLOW because none of those live agents' `{session, name, pane_id,
  terminal_id, agent}` five-tuple matches a stored `*.edn` route in this
  registry — expected, since this registry holds no Clojory-written
  routes for those flows. Test
  `listing-joins-live-agents-and-never-reads-ledger-files-as-routes`
  (`core_test.clj:151-166`) confirms the join and confirms `attempts.edn`
  and `pending/*.edn` files are excluded from route parsing.
- **Still open, unchanged:** missing subcommands (`send-abrupt`,
  `deregister`, `rebind`, `move`, `retire`, `import-retirement` — `bin/
  hm-move`, `hm-rebind`, `hm-retire`, `hm-send-abrupt` still `exec
  python3 hm.py`, confirmed by reading their first lines); `register`
  still hard-requires `--session`/`--native-thread` and has no
  `--readiness-probe`/`--rollout`, no prior-binding-overwrite check
  (`main.clj:22-26`, `core.clj:228-236`); `--hold-seconds` is parsed and
  range-checked (`main.clj:18-20`, new this pass) but still not passed
  to `send!` or enforced as an actual hold; registry format is still
  `*.json` (Python) vs `*.edn` (Clojure) in the same directory — cross-
  implementation registration still fails.

**Mind's four claims, checked one by one:**
1. **Live list** — true. `hm-clj list` against the real registry printed
   real session/status rows (see above), not a stale registry-only
   listing.
2. **Relay guard** — true. `nested-relay?` is now called from `send!`
   and the test exercises the rejection path; verified by reading
   `core.clj:240` and rerunning the test.
3. **Pane parsing** — unchanged from `514f297f` and still correct:
   `parse-pane` requires a `session:pane` shape (`core.clj:148-151`,
   test `core_test.clj:24`); not part of this pass's commit range but
   re-confirmed passing.
4. **Datalevin readback** — true but narrow: `attempts-for`/
   `pending-for` are read back for write-confirmation inside
   `append-attempt!`/`held!` (see above), and the direct pod test
   (`datalevin-pod-indexes-and-queries-attempts`) passes. `listing!`
   itself still does not read Datalevin; the readback is a persistence
   check, not a query surface used by any subcommand's output.

**Verdict: this revision is a working proof of concept of the audited
scope.** Every item this pass tracked as still-open at `514f297f` is now
fixed or verified working, except: F8's remaining subcommand/registry-
format parity gaps (by design deferral, not a defect in scope), F11's
cosmetic namespaced-map EDN syntax, and `listing!` not yet querying
Datalevin. `send`, `register`, and `list` all run end to end against a
live Herdr session with real gating (identity, readiness, process,
retirement, reservation, presentation) and real persistence
(EDN + Datalevin, index-confirmed) — the shape F1–F7 were blocking.

## Full audit a8bd811b

Target: `clojure` at `a8bd811b` in github.com/LiGoldragon/HackyMessenger,
compared with `hm.py` on `origin/main`. Lines are `core.clj`/`main.clj`/
`store.clj` under `src/hacky_messenger/`. Method: `git archive` of both into
scratch; the 16-test suite (82 assertions) passes; a 24-case argv matrix ran
both CLIs against fake `herdr`/`orchestrate` and empty scratch registries;
failure paths ran through an injected `HerdrTransport`. One live cycle ran
against Herdr session `messaging-build`, with real `orchestrate` locks on a
scratch `HM_REGISTRY`. The disposable pane `w16:p1` ran a `python3` stdin sink,
started through a symlink named `codex` so that Herdr detects an agent, with the
test native thread in its argv. The cycle ran register (readiness probe), list,
send, send `--wait-presented`, move, retire (twice), the gates, import-retirement
and deregister. The pane was then closed and `herdr pane list` shows no `w16`
pane. The live registry has no `.edn` file and no `datalevin/`. No real flow was
messaged.

**Verdict: Partial.** The happy path runs end to end on live Herdr. The
identity, readiness, retirement, native-reuse and reservation gates work.
Parity is incomplete, and one route-hold bypass, two data-loss paths and one
double-send path remain.

| Requirement | Verdict | Evidence |
|---|---|---|
| Nine commands exist | Met | `main.clj:14-68`; `bin/hm-clj-*` all exec bb |
| argv / exit parity | Partial | 7 of 24 cases differ; see gap 11 |
| Readiness probe | Met (live) | Registered through the Codex rollout witness; accepts a pre-written witness (Python does too) `core.clj:187-207` |
| List backed by Datalevin | Partial | `routes-for` gates which rows appear, but rows still come from the EDN; `:533` discards its query; send never reads Datalevin |
| One-line EDN relay ≤800, no nesting | Partial | One line and round-trip hold (`:71-81`); overflow drops the message (gap 3); nesting guard is shallow (gap 7) |
| Fallback grading | Partial | Requires an observed presentation (`:521-524`); a title fallback or `--pane` fallback without a stored route always fails with ProcessMismatch (zero native thread, `:237,244`) |
| Route gate | Partial | IdentityChanged, NotReady, Blocked and ProcessMismatch hold; `route_hold` and non-idle/working/done status are not checked (gaps 1, 6) |
| Retirement gate | Met (live) | Retire, idempotent retire, send/send-abrupt refused, native reuse refused, import-retirement |
| Attempt ledger | Partial | Pre-prompt `Submitting` is index-confirmed (`:258-269`); post-prompt failure is mislabelled (gap 4) |
| Reservation gate | Partial | send, send-abrupt, deregister, rebind, move and retire take the lock; `register!` does not (gap 2) |
| Malli on every value | Not met | Gap 9 |
| Protocols really used | Partial | HerdrTransport and Ledger are used; Clock and Registry are mostly for show (gap 10) |
| EDN state separate from live JSON | Not met by default | Gap 5 |

Remaining gaps, most severe first:

1. **`route_hold` ignored.** `send!` (`core.clj:502-528`), `send-abrupt!`
   (`:475-501`) and `rebind!` (`:375-393`) never read `:route_hold`. Python holds
   RouteHold. Witnessed live: a route with `route_hold "pane_move_in_progress"`
   gave `Transported`. A failed move compensation (`:463-472`) leaves exactly
   that hold, and, unlike Python, does not rebind the verified destination.
2. **`register!` has no reservation and no check of the prior binding**
   (`:308-324`). Witnessed live: re-registering over a stored route with a
   different `terminal_id` and a `route_hold` printed `Registered`. Python
   refuses: "already registered to a different terminal" or "held for route
   repair". No check that `:agent` is nonempty.
3. **Data loss.** (a) An envelope over 800 characters fails with "message held"
   but writes no pending record and no overflow file (`:77-78`, called at `:518`
   after the gates). Python writes the body under the flow's directory and sends
   a pointer. (b) Any Herdr or process error from `verify-target!` becomes
   `(keyword message)` (`:484,517`), and `delivery-attempt!` rejects it
   (`:39-40`). Witnessed: the only result is "Invalid DeliveryAttempt grade or
   reason", with no Held and no pending record. Python maps it to PaneMissing.
4. **Double-send.** If the `:sent` append fails after a delivered prompt, the
   output is "prompt failed or is uncertain" (`:525-528`); witnessed with 1
   prompt issued. `send!` has no post-prompt identity recheck (`:520-526`), which
   Python and `send-abrupt!` (`:496`) both have. A failing `release!` in
   `finally` (`:287`) turns a delivered send into exit 1; Python does the same.
5. **Default root is the live Python registry** (`:66`,
   `~/.local/state/hacky-messenger`). Without `HM_REGISTRY` it writes `*.edn`,
   `datalevin/`, `pending/*.edn` and `retired/*.edn` beside the live JSON, and
   `retired!` (`:125-143`) cannot see Python's `retired/*.json`. This breaks the
   separation ruling.
6. **Python gates missing:** holding when status is not idle/working/done
   (`:208-221`); `--hold-seconds` parsed but never passed, so there is no
   InTransition wait (`main.clj:18-21,25-28`); Claude `~/.claude/sessions/<pid>.json`
   process match (`:144-150`); `verify-move-target!` requires the native thread
   in argv for Codex too (`:420`; Python requires it only for Claude), so moving
   a Codex remote pane always fails.
7. **Nested-relay guard reads only the first EDN form.** It is a top-level map
   check (`:82-86`). `see {:machine/relay …}`, `[{:machine/relay …}]` and a
   `Machine.Relay.{ … }` datom all sent (witnessed).
8. **The Datalevin index is not the list's source.** `route-records`
   (`:529-541`) hides an EDN route that is sendable but not indexed (witnessed:
   list showed `-`). `:533` calls `attempts-for` and discards the result. No
   path reads a route from Datalevin.
9. **Malli gaps.** The maps are open and `:string` accepts `""` (`:17,20`);
   Python requires nonempty fields. Herdr replies, live agents and Datalevin
   results are never validated (`:97-101,222-226`, `store.clj:126-154`). The
   stored-fallback route is unvalidated (`:240`), and so is `move-route!`'s
   write (`:394-400`). `:25` builds validators and discards them.
   `MessageBody` counts characters, not the 64 KiB byte limit (`:15`).
10. **Protocols partly for show.** Nothing injects `Clock` (`:69`).
    `deregister!`, `rebind!` and `move-route!` write through `fs/delete` and
    `atomic-edn!`, bypassing `Registry` (`:337,391,398`). `register!` calls
    `herdr!` directly (`:312`). The store has no protocol.
11. **argv parity** (`main.clj`):
    - Bare `hm` exits 0 where Python exits 2 (`:12`).
    - Extra positionals are ignored: `send f hi extra` and `list extra` run
      (`:15,67`).
    - Options before positionals are misparsed: `send --wait-presented f hi`
      treats the flag as the flow (`:15`).
    - `--opt=value` gives exit 2 where Python gives 1 (`:4`).
    - A non-numeric `--hold-seconds` or `--process-pid` exits 1 where Python
      exits 2. `parse-long` returns nil and does not throw (`:19,57`).
    - `register` hard-requires `--session` and `--native-thread` (`:33`).
    - Cosmetic: Held attempt IDs are UUID prefixes with hyphens (`core.clj:306`).

## P0 check 63618441

Target: `clojure` at `63618441` in github.com/LiGoldragon/HackyMessenger
(fetched fresh), `git archive`d into a scratch tree; `bb --config bb.edn`
ran the 17-test suite (89 assertions, 0 failures) unmodified, then a
`bb probe.clj` harness with a scratch `HM_REGISTRY` per case, an injected
`HerdrTransport` (no real Herdr), and `*with-reservation*` bound to a
pass-through that counts calls, so `orchestrate` was never actually shelled
out to. No real pane or flow was touched.

1. **route_hold: Held, never Transported. Holds.** `send!` on a route with
   `:route_hold "pane_move_in_progress"` threw
   `Held.{ held-flow RouteHold attempt-... }`; `send-abrupt!` on the same
   route threw the identical `Held.{ ... RouteHold ... }`; `rebind!` on the
   same route threw "Registration is held for route repair" before touching
   the pane. The injected transport's prompt counter stayed at 0 across all
   three calls — nothing was typed.
2. **register: reservation taken, held/other-terminal binding refused.
   Holds.** `register!` over an existing binding carrying `:route_hold`
   threw "Registration is held for route repair"; a second `register!` over
   a binding with a different `:terminal_id` threw "Flow is already
   registered to a different terminal". `*with-reservation*`'s call counter
   read 2 after the two `register!` calls, confirming both went through the
   reservation wrapper (`with-reservation`) rather than around it.
3. **Overflow >800 chars: durable record, truthful report. Holds.** `send!`
   with a 780-character body wrapped in the `Machine.Relay` envelope (which
   pushes the line over 800) threw
   `Held.{ overflow-flow RelayOverflow attempt-... }` with 0 prompts issued.
   `pending/<id>.edn` was written with `:reason :RelayOverflow` and its
   `:message` field held the exact original body (length-matched), and
   `attempts.edn` gained a matching `:reason :RelayOverflow, :grade :Held`
   line — the report and the durable record agree, and nothing was typed.
4. **Post-delivery ledger-append failure: Uncertain, no retry. Holds.** With
   a `Ledger` whose `record-attempt!` failed only on its second call (the
   post-prompt "sent" append, after the pre-prompt "Submitting" append
   already succeeded), `send!` threw
   `Uncertain.{ ledger-flow attempt-... } prompt was delivered but ledger
   confirmation failed; do not retry: simulated ledger outage`. The
   injected transport's prompt counter read exactly 1 — the failure was not
   retried as a resend.
5. **Default state root is not the live Python registry. Holds.** With
   `HM_REGISTRY` unset and `*root*` unbound, `(hm/root)` resolved to
   `~/.local/state/hacky-messenger-clojure`, distinct from Python's
   `~/.local/state/hacky-messenger` (confirmed unequal paths at runtime).

## Re-audit 246b963a

Target: `clojure` at `246b963a375807f9e47bc8f1e74bffb30c926516` in
`github.com/LiGoldragon/HackyMessenger` (fetched fresh; 2 commits past
`63618441`: `7088780` "enforce remaining Clojure route gates",
`246b963` "tighten Clojure CLI and protocol seams"). Method: `git archive`
into a scratch tree, Babashka v1.13.219, a scratch `HM_REGISTRY` per case,
`bb -e` probes with injected `HerdrTransport`/`Registry`/`Clock` fakes (no
real Herdr), `python3 hm.py` on the same tree for argv comparison. No real
pane or flow touched. Items 1-5 of the "Full audit a8bd811b" gap list stay
verified fixed per "P0 check 63618441"; this pass checks items 6-11.

**Tests: 18 tests, 92 assertions, 0 failures** (up from 17/89 at `63618441`).

6. **Route-status/InTransition/Claude/Codex-move gates: partly fixed.**
   The Uncertain gate is real: an injected agent with `agent_status
   "launch_pending"` (not idle/working/done) produced `Held.{ flow1
   Uncertain attempt-... }` (`core.clj:238`). The Claude session-file
   match is new and works structurally: `claude-session-matches?`
   (`core.clj:152-157`) reads `~/.claude/sessions/<pid>.json` and compares
   `:sessionId` to the native thread, OR'd into `process-matches!`
   (`core.clj:159-166`). But `--hold-seconds`/InTransition is still not
   fixed: `in-transition?` (`core.clj:276`) makes `send!`/`send-abrupt!`
   Held immediately on a transitioning route (confirmed live: 18ms
   elapsed, no wait) — `--hold-seconds` is parsed and range-validated in
   `main.clj` but never passed into `send!`/`send-abrupt!` at all, so
   there is no poll loop matching `hm.py`'s `_wait_for_route`
   (`hm.py:129-138`, up to `hold_seconds`). And Codex moves are still
   broken: `verify-move-target!` (`core.clj:439-458`) requires the native
   thread in a live process's argv unconditionally, but `hm.py`'s
   `_verify_move_target` (`hm.py:504-506`) requires that only when
   `expected['agent'] == 'claude'` — a Codex move still can't pass this
   check the way Python's can.
7. **Nested-relay guard at depth: fixed.** `nested-relay?` (`core.clj:89-95`)
   now walks the whole structure with `tree-seq` and also matches a
   literal `"Machine.Relay.{"` substring. Tested directly: a relay map
   nested at any depth (`[{:machine/relay [...]}]`,
   `{:a {:b {:c {:machine/relay [...]}}}}`) and the literal
   `"Machine.Relay.{ relayed }"` string all return `true`; a plain body
   returns `false`.
8. **List using the Datalevin query: fixed.** `route-records`
   (`core.clj:585-596`) now gates every listed route on
   `store/routes-for` (Datalevin) before reading its EDN file, and queries
   `store/attempts-for` per indexed flow. Confirmed by the passing test
   `listing-joins-live-agents-and-never-reads-ledger-files-as-routes`,
   whose `with-redefs` on `store/routes-for`/`store/attempts-for` shows
   both are actually called (`[:routes [:attempts "00f95a"]]`) during
   `listing!`, not discarded. The Datalevin index gates which rows are
   even candidates for listing, closing the audit's "sendable route
   hidden from list" complaint.
9. **Malli closed maps / non-empty strings / validated Herdr+Datalevin
   values: partly fixed.** Closed maps: fixed. Every record schema
   (`RouteBinding`, `DeliveryAttempt`, `PendingIntent`, `RouteIdentity`,
   `RetirementEvidence`, `RetirementMarker`, `Reservation`,
   `ReadinessProof`) now carries `{:closed true}` (`core.clj:16-23`);
   tested: `(m/validate RouteBinding (assoc route :unexpected true))` →
   `false`. Non-empty strings: still open at the schema level — tested
   directly, `(m/validate RouteBinding {:session "" :name "" :pane_id ""
   :terminal_id "" :agent "" :native_thread "0000000000000000"})` and
   `(m/validate DeliveryAttempt {:id "" :at "" :flow "f" :reason :x})`
   both still return `true`; the fields are still bare `:string`.
   Emptiness is only screened by scattered manual `nonempty-strings!`
   calls at `register!`/`deregister!`/`retire!`/`rebind!`/`move!`
   call sites (`core.clj:360` + call sites), not by the schema itself.
   Herdr replies and Datalevin query results are still never
   Malli-validated (only the maps HM itself constructs before writing —
   `RouteBinding`, `DeliveryAttempt`, etc. — are `valid!`-checked;
   `target-agent*`/`live-agents*`/`process-info*` replies and
   `store/attempts-for`/`pending-for`/`routes-for` results are consumed
   raw).
10. **Clock and Registry protocols really used: fixed.** `registry`
    (`core.clj:74`) and `now` (`core.clj:75`) now resolve through new
    `*registry*`/`*clock*` dynamic vars, defaulting to `->EdnRegistry`/
    `->SystemClock` only when unbound, and `read-route` (`core.clj:103`)
    and `register!`'s save (`core.clj:357`) go through `(registry)`.
    Verified live by injecting a `reify hm/Registry` whose `load-route`
    returns a synthetic map and recording the call: `hm/read-route`
    returned exactly that synthetic map and the call log showed
    `[:load "abc"]` — swapping the record changed `send!`'s observed
    route, proving real dispatch, not decoration.
11. **argv parity with `hm.py` on `main`: partly fixed.** Bare `hm-clj`
    (no operation) now exits 2 with a `usage:`-prefixed
    `hm-clj: error: invalid choice: ` message, matching `hm.py`'s exit 2
    (`main.clj:14,69`, tested). Non-numeric `--process-pid` and
    non-numeric `--hold-seconds` both now exit 2 (`main.clj:20,27,57-58`,
    tested: previously-silent `parse-long` nil was replaced with an
    explicit `(or ... (parse-error ...))`, and `--hold-seconds`'s failure
    was switched from `hm/fail` (exit 1) to `parse-error` (exit 2)) —
    matches Python's argparse exit 2 for both. Still open: extra
    positionals are rejected only for `list` (`main.clj:68`, new this
    pass); `send 00f95a hi extra` still runs to completion silently
    ignoring `extra` (tested: fails only on missing `FLOW_ID`, never on
    the stray arg), where `hm.py send 00f95a hi extra` exits 2 with
    "unrecognized arguments: extra". `--opt=value` syntax (e.g.
    `--hold-seconds=5`) is still unsupported by the hand-rolled parser:
    tested `send 00f95a hi --hold-seconds=5` → exits 2, "unrecognized
    arguments: --hold-seconds=5", whereas `hm.py`'s argparse accepts that
    syntax and proceeds (getting only as far as a missing-`FLOW_ID`
    failure) — the two now diverge in the opposite direction from the
    original gap (Python succeeds, Clojure now refuses instead of
    misparsing).

**Verdict summary for items 6-11:** 7 and 10 fixed; 8 fixed; 6, 9 and 11
partly fixed with specific gaps named above (Codex-move argv check and
missing hold-seconds wait for 6; schema-level non-empty strings and
unvalidated Herdr/Datalevin values for 9; extra-positional and
`--opt=value` parsing for 11); none regressed.
