# Psyche recovery: d8df70 and e51411 transcripts

Subflow of da88cf, 2026-09-25. Source audit: Field Luna e71dab (its message to Field Astra 504461, logged at flows/504461/log.md:226).

Transcripts (line numbers are JSONL record lines):

- d8df70: `~/.claude/projects/-home-li-primary/d8df703d-d083-4c29-9597-6b32e7411b75.jsonl` (3369 records)
- e51411: `~/.claude/projects/-home-li-primary/e5141130-9a4a-4b8f-b405-67d941a7b320.jsonl` (6631 records)

Method: I enumerated `user` records (not tool results or meta) and `queued_command` attachments, and removed duplicates by payload. A `queue-operation` enqueue with no delivered twin was also checked: none carried the living's words. I split out command turns, `Machine.Relay`/`#msg`/`#psyche`/`{:machine/relay}` bodies and launcher prompts. Each remaining turn was checked against `Vision/`, `Intent/`, `vision-raw/`, `flows/*/vision/` and `flows/*/notion/`, using 5-word shingles with a per-sentence 4-word check, and then read by hand.

A concurrent recovery landed while this ran: 88475f's Opus subflow, commit `0bce2d029` ("88475f: recover unlogged vision and notion from e51411 and d8df70 transcripts"), recorded 14 records (2 in d8df70, 12 in e51411). Those turns are counted below as already logged and cite that work. Nothing was duplicated.

Classes: **L** already logged (target is the carrying record), **V** vision recovered here, **N** notion recovered here, **W** working instruction (list only), **Q** question or process talk (not psyche), **C** context/observation/transcription clarification, **U** unfinished sentence, **P** proposal for the living's review (not logged).

## d8df70: the ten candidate lines

| line | time (UTC) | class | action | target |
|---|---|---|---|---|
| 387 | 09-23 22:02 | L | logged by 88475f ("Skills loaded one prompt after another are inefficient"); first sentence is a working instruction kept as context | flows/d8df70/vision/launch.md |
| 566 | 09-23 22:29 | W | "Talk to Psyche Fable. Tell him about your existence..." list only | — |
| 1063 | 09-24 13:49 | Q | "how long does it take to make images? Are you just fucking with me?" process complaint (a hung `codex exec`); not psyche | — |
| 1182 | 09-24 13:52 | P | "Why is Psyche not there? Do you not count?" needs heavy context; see proposal P1 | — |
| 1240 | 09-24 14:03 | L / W | quoted whole at flows/836818/vision/flowNexus.md (heard by d8df70, logged by 836818); substance is a working instruction (all hands, fix the Prometheus firewall, deploy Flow and Message); no d8df70 vision owed | flows/836818/vision/flowNexus.md |
| 1518 | 09-24 14:33 | W | "Talk to Fable about all this and get Mind and Field to adapt the answers into code and deploy." quoted as context in flows/836818/vision/flowNexus.md; the answers themselves (artifact comments) are logged in d8df70's flowLifecycle, building, flowTool and messaging files | — |
| 1632 | 09-24 14:59 | L / W | quoted in flows/836818/vision/flashbooks.md; substance is a working instruction (context survey, then the Dawn flashbook). "we can change the scale" is unclear and not read into | flows/836818/vision/flashbooks.md |
| 2172 | 09-24 15:58 | W | "Okay you're getting really held up ... let Field refresh you." a refresh order to this seat; garbled by speech-to-text ("give your make reexecute a new fresh flow"); list only | — |
| 2553 | 09-24 19:44 | L / C | vision part ("Why don't we start making a log of the things that are recurring and not getting solved ...") logged by d8df70's own logging audit, but filed under e51411 rather than the flow that heard it; the rest is observation of Prometheus's link lights and complaint. Left in place, not duplicated | flows/e51411/vision/infrastructure.md |
| 2739 | 09-24 19:49 | L / W | first paragraph logged by 88475f ("Two live sessions of one flow split the living's psyche"); second paragraph (amalgamate, log the vision, re-inject into a Flow-started flow) is a working instruction, named in that record's provenance | flows/d8df70/vision/flowLifecycle.md |

d8df70 counts: 10 candidates; 4 carried by a record (387, 2739 by 88475f; 1240 and 1632 by 836818 as quotes); 1 vision part carried in another flow's file (2553); 4 working instructions or questions (566, 1063, 1518, 2172); 1 proposal (1182); 0 new records written here.

Other d8df70 human turns outside the ten, spot-checked: all are carried except queued questions or orders (2479, 2514, 2612, 2861), launcher turns (12 to 377), and machine relays. As 88475f also flagged: flows/d8df70/vision/flowTool.md logs the unfinished sentence at line 2055 ("Well you obviously have to recompile the CLI, the"). The 752e0f reconstructions in d8df70's building, flowTool, herdrSessions, remoteAccess and titles files log plain questions as vision. Both are left unedited; records are superseded by appending, never edited.
