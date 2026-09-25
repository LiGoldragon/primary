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
