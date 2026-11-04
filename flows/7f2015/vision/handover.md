# Handover of 7f2015, the Psyche core Secondary, 2026-11-04

Written by Opus, the flow that held the conversation. It holds what this seat keeps track of that no module holds. He asked for it: "You can create a handover for it that contains what it's keeping track of so you don't have to remember all the stuff, the small things that haven't made it into the vision modules or are in the belief modules."

## Standing facts

- **The Flow Nexus in use** is the HarnessFlags build, flow at main's head ("Add configured harness flags and launch rehearsal").
  - Sockets: `/run/user/1001/flow-harnessflags/`. Store: `~/.local/state/flow-harnessflags`.
  - It runs as the hand-written user unit `flow-nexus-harnessflags.service`. The unit is **not enabled**, so a new login session does not start it.
  - Its drop-in `no-presentation-role.conf` sets `FLOW_CORE_PRESENTATION_PROMPT` to a one-newline placeholder file. Without that variable the Nexus refuses to compose { Psyche core Primary } (PresentationUnavailable).
- **The old Nexus**, `flow-nexus.service`, is stopped but **still enabled**. A login would start it on `/run/user/1001/flow/`. All 33 of its seats are Asleep.
- **The CLIs:**
  - `flow`, `flow-meta` and `flow-hook` on PATH are the old build. With no socket variable set they reach nothing.
  - The new CLIs are at `/nix/store/r1k4wad7zdic9mg24fkqpqjx8xf58f0q-flow-configured-0.44.0/bin/`.
  - Ordinary calls take `FLOW_SOCKET=/run/user/1001/flow-harnessflags/flow.sock`.
  - Meta calls take `FLOW_META_SOCKET=/run/user/1001/flow-harnessflags/flow-meta.sock`; `flow-meta` ignores FLOW_SOCKET.
  - Flows launched by the new Nexus carry FLOW_SOCKET and the new flow-hook.
- **This seat is the one writer of the new Nexus's configuration.** Field core and Mind core send their changes here; Field core acknowledged after its stale whole-family write lost 13 HarnessFlags entries.
  - The careful rule: a whole-list write is built only from a fresh read, changes one thing, is read back and diffed.
  - The records of every write are in `flows/0f074c/migration/`, and the list builder is in that flow's scratch `bind.py`. Copy the latter into `flows/0f074c/migration/` before relying on it.
- **HarnessFlags**, 34 entries:
  - Every Claude metaflow carries `--disallowedTools Artifact,ArtifactComments,ArtifactData,SendMessage,ListAgents`.
  - The bookmaker, { Psyche book Quaternary }, and { Field publisher Quaternary }, which both publish pages, carry `--disallowedTools SendMessage,ListAgents`.
  - 14 Psyche seats are flagged but undeclared, so they cannot launch: book Secondary; chronos, communication, ethos, flow, research and spirit, each Primary and Secondary; nexus Secondary.
- **Messages go through `flow Send` alone.** knowledge:flow-messaging is landed on psyche-belief main and bound to all 46 metaflows.
  - Text is a String, in guillemets. A guillemet inside a guillemet string breaks the parse.
  - The old Nexus refused this seat's sends as Unidentified; the old Nexus is gone now.
- **The heartbeat** is not in the new build: flow main lacks the old build's 15 heartbeat commits. It is a recorded gap, dropped by ruling.
- **The Curriculum empty-records fix** is not deployed. Every new flow logs SuccessorUncomposable RecordMissing at its rest; that stops its refresh and loses nothing.

## Open

1. **Step 5, the CriomOS-home switch.**
   - The proposal is `flows/7f2015/proposals/criomos-home-flow-switch.md`, published as the book "The Flow Nexus".
   - He commented that a flake input carries no revision. The proposal is redone on it and sent to the bookmaker as a new book, "The Flow Nexus, declared in CriomOS-home, version 2"; its title has not come back yet.
   - Deploy nothing until he has ruled on that book. Then bring it to the Psyche core Primary, and switch at a moment no launch is in flight.
   - The Curriculum empty-records fix follows the switch.
2. **The bare-URL flake pass.**
   - He ordered: "Send someone to make sure all the flake files are fixed for this." A Tertiary is rewriting every LiGoldragon flake input that carries a rev or ref to the bare URL, with the locked commits unchanged and one commit per repository.
   - It skips any checkout that is dirty or diverged, CriomOS-home's main among them.
   - Result: see the end of this file.
3. **The narration book.** Mind core's account `flows/70a111/reports/narration-capture-account.md` is with the bookmaker, to be published as "Narration hunt: observed text, unknown cause". Its title has not come back yet.
4. **Defect bead primary-vgvi**, P1: a Send with MiddleAbrupt fails at the CLI with rancor's opaque error, while Soft goes through.
   - Seen here: the three-field form with Wake written out went through, with MiddleAbrupt and with HardAbrupt.
   - So the failing case may be the two-field form; unverified.
5. **The presentation-prompt defect.** The prompt is an environment lookup hard-coded on one literal address, and "none" is said by a one-newline file. It is owed a typed configuration value, and is listed in the core Primary's handover among what his environment-variable intent condemns.
6. **Mind:**
   - Every Mind flow is on the new Nexus, and Mind core Secondary has resumed its work.
   - Mind core Primary had never been seated; this seat launched it at Predecessors.0.
   - primary-hbhi is blocked by Mind core Primary's ruling, with its account in item 3.
   - Codex had 76% left, about 1% an hour, and the soonest reset expires Fri 6 Nov 17:32 (bead primary-8kky, the codexManager Secondary's job). He wants Codex used to the full until Friday.
7. **The book "Who registers belief"** awaits his review.
8. **vision:remembering conflicts with his word.** It says a handover "is published as a book of its own kind". He said: "There's no reason to make the handover into a book." The line is the core Primary's to correct.
9. **The 0.45, 0.46 and 0.47 Nexus processes** still run from other units, untouched.

## His words on conduct, to this seat

- On a raw record written of his words: "No, don't log, please. Why are you logging this? I want all these instructions to log everything all the time removed." Then: "Just add it to the handover of primary. My intent is to remove the behavior that makes flows log everything I say." This seat writes no raw records of his words. The lines that instruct logging were sent to the core Primary, and are in its handover.
- "I do not want to use Claude messaging." He said it through the core Primary. Every message goes through `flow Send`.

## Result of the bare-URL flake pass

- **Pushed in 14 repositories**, each with the commit "flake: inputs by bare URL, pinned by the lock": core, belief-nexus, datom-codec, listener, ethos-test, herdr-nexus, harness, lojix-test, signal-belief-nexus, meta-signal-belief-nexus, translator, flow-test, flow-nexus, flow-nexus-tests. Every locked rev and narHash is unchanged.
- **Two warnings, not yet raised with the core Primary:**
  - ethos-test followed the feature branch candidate/held-set-bare of ethos-zero; its next lock update moves it to the default branch.
  - lojix-test's six lojix inputs, red, green, migrate, migrate-green, migrate-final and old-runtime, are now one URL at six locked commits. A lock update would set all six to one commit and defeat the comparison the repository exists for.
- **Skipped, with no commit, about 42 checkouts.** About 30 are on a detached HEAD, among them flow, signal, lojix, persona, criome and orchestrate-test. The others are on another branch, or on a dirty or diverged main: flow, CriomOS-home, message-test, meta-signal-herdr-nexus, meta-signal-flow, ethos-zero, CriomOS and spirit. They still carry inputs with a rev or ref, and are owed a second pass by whoever owns each checkout.
- **Third-party inputs with a rev or ref** (nixpkgs channels, flake-utils, pi, nix-orca, codex-cli-nix) were left as they are.

## Chat length

His words: "Can you tell me what you think: is it useful for you to make these big long responses here in your chat responses? Do you think that they help you to reinforce the idea of what you're doing? Because I don't read them." Then: "So when you say from now on, it means every flow from now on. What did you change? It will make every flow do that because I haven't been able to do it and I tried." Then: "I want that line taken out of Flow Nexus."

- The presentation line ("A flow gives a presentation … its first turn ends in one, and so does every task, goal or question that originates in the living") is removed from vision:flow-nexus on psyche-belief main, by the commit "vision:flow-nexus: remove the presentation line, on his word".
- The core Primary has the finding: the harness base prompt's end-of-turn summary also pulls toward length, and the one-line chat rule could be made the last act of every turn.
- Keep the chat to one line.
