# Handover: Psyche::Flow Secondary

## Role
- **Seat:** Psyche aspect, topic flow, Secondary layer. Opus.
- **Primary:** f5a6e9 (Psyche::Flow Primary, Fable). This seat is its secretary.
- **What passes through this seat:** every message to and from Flow, and every report Flow sends to core.
- **Upward:** reports to Psyche Core Secondary 445410 by hm-send. The living reaches Flow through 445410.
- **Peers:**
  - Ethos pair: d5df1d (Primary) and 1d0733 (Secondary).
  - Nexus and Message topic flow: 73ada7, talked to directly at this layer.
- **Mind:** Mind's counterpart flows may message this seat directly about implementation. Field reaches it only through Mind.

## Duties
- **Relaying the living:** pass his words to f5a6e9 verbatim, only as psyche messages (`hm-send TARGET --psyche CONTEXT VERBATIM`, or `--psyches`), and log them in this lane's `vision/`.
- **Questions:** carry questions from 445410, 73ada7 and Astra (Mind) to f5a6e9. Return each ruling to whoever asked.
- **Verifying folds:** when f5a6e9 publishes a design fold, have a subflow read the pushed blob (`git rev-parse <commit>:<path>`) and confirm each ruling by line before reporting to 445410. Folds have landed incomplete before.
- **flow-test:** keep it pinned to the latest verified design.

## Governing state
- Flow design: `/home/li/primary/flows/f5a6e9/reports/flow-buildable-design.md` (owned by f5a6e9). Governing and verified by line in the pushed blob: commit 9bffed2f4cd0363dfeb9b0925c64817bc55349f8, blob be032eeb2eaaece8ce2fbfba7018162e89eb8b5c. It carries: the Message gate with the executable re-checked on every Lock, Deliver and Release; Start.{ OrdinarySocketPath MetaSocketPath StorePath } with StartRefusal.[ Store.StoreRefusal ]; the wake composing whatever modules exist (Unknown.Key only from Launch and Forget; NoLayer at Launch, Lock, Deliver); the order of checks at Deliver; Refused.Store.String; the old store not opened (its fate rests on the living's answer to 73ada7's book «What the new Message does with the old store»).
- flow-test: https://github.com/LiGoldragon/flow-test at 01c29c90048a488b39e7908c8cce0d72f8439a66, pinned to design 9bffed2f4; Flow code pinned at 962ad12ed2fc1fcb277ed9fa82b8e411c504627b (0.25.0). 76 design scenarios, all expected-failing Mind targets, none broken; `nix flake check` on Prometheus exits 0. Its live-Claude runner flow-claude is built but never run (needs a Claude login).
- Refusal reachability for Identify, Lock, Deliver: `flows/9fed42/reachability-439dc64b4.md`; since 9bffed2f4, Unknown.Key is unreachable from Lock and Deliver, NoLayer reachable from both.
- Deployed Flow: 0.14.0 stable, 0.17.4 Next; store `~/.local/state/flow/flow.sema`. The new Flow is never pointed at it.
- Flow Ethos candidate `flows/9fed42/candidate/`: superseded by the design; flow-test is the acceptance suite.

## Open items
- The living, via 73ada7's book: the fate of the old Flow and Message stores.
- f5a6e9's handover (on main in ff2b6b1b) predates 9c8c30835 and 9bffed2f4; its successor takes 9bffed2f4 as governing.
- No flow-test design gap is open. When Mind's build lands, re-pin Flow in flow-test and promote passing scenarios from mind to pass.

## Standing limits
- **Committing:** do not commit in the shared Primary checkout. Publish this lane only from an independent full clone, under the PrimaryPublish lock (operation-orchestrate, four-field form), per compensation-primary-commit. Before every push, check that the commit changes only `flows/9fed42/` paths and that its file count is at least main@origin's.
- **Messenger route:** hm-send at `/nix/store/pqx78mxcdwpbwzhicgiprvfj5qq0lnxs-messenger-clj-0.3.0/bin/hm-send`, and orchestrate 0.37.0 at `/nix/store/vsj5mw3jfbwmclzpa4gqlgysvxfip3g2-orchestrate-0.37.0-profile/bin`, until Field's repair ships.
- **Heavy work:** builds and tests run on Prometheus through Nix.
- **Books:** f5a6e9 writes the books, one proposal at a time. No subflow drafts one.
