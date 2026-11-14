# Energy on its Ethos, step one: the two contracts generated

Bead primary-juh8. Each repository has a branch `ethos-565bc8`, cut from main and pushed. Each has a worktree at `/git/worktrees/<repo>-ethos-565bc8`. Nothing is merged and nothing live was touched. energy-nexus's `schedule-pace` branch and the dirty local clone (on `energy-stage-one-a9a8d6`) were left alone.

The generator is **ethos-zero 28.0.0, main 970459d**. Nothing forced 27. The binary was built on the builder from `github:LiGoldragon/ethos-zero/970459d…`.

The inventory is `/home/li/primary/flows/565bc8/energy-ethos-inventory.md`.

## Branches, revisions and gates

| repository | base | head | gate (nix-fast-build by revision on prometheus) | log |
|---|---|---|---|---|
| signal-energy-nexus | 7ca10eb | **e0eb9b77373c1e1b10d3656220996fea0785c505** | exit 0. Unit tests 3, hand_and_generated 2, wire_fixtures 1: all pass | gate-energy-signal-energy-nexus-e0eb9b7.log |
| meta-signal-energy-nexus | 3264d6f | **fb69426cc01327b81bb7946160529e48a2397702** | exit 0. Unit tests 2, hand_and_generated 2, wire_fixtures 1: all pass | gate-energy-meta-signal-energy-nexus-fb69426.log |
| energy-nexus | 2623947 | **0b9e6b43dad523ca8e2f8e691ea00f27d72d65ba** | exit 0. `test` passes: 73 passed, 0 failed, the same 73 as main. `nexus-dependency-boundary` passes | gate-energy-energy-nexus-0b9e6b4.log |

- Every log is in `/home/li/primary/flows/565bc8/`.
- Before each commit, the same tree passed `nix flake check --max-jobs 0` from a path flake on the builder.
- Locks were made with build-base 9706bad's toolchain, by `cargo metadata`. Nothing was compiled locally.

## What was done

**signal-energy-nexus:**
- **The Library.** `ethos/library.ethos` is the Energy vocabulary, moved from energy-nexus's `ethos/library.ethos`. Its Flow import is now `signal_flow:[ Address ]`. It generates `src/generated/library.rs`.
- **The ordinary Signal.** `ethos/signal.ethos` generates `src/generated/signal.rs`.
  - It imports `crate:[ … ]`.
  - Its inputs and outputs stand alone, and `Call.{ Caller Input }` is in its types section. The 0.5.0 text nested Input inside Call, which ethos-zero 28 refuses with `Duplicate.Input`.
- **The build check.** `build.rs` runs ethos-zero as a build-dependency on both files and asserts the committed Rust equals its output.
- **The hand types are gone.** The `wire!` macro and the dev-dependency on ethos-zero 19.2 are removed. Address is still re-exported from signal-flow.
- **The digest.** `CONTRACT_SOURCE` is still the text of `ethos/signal.ethos`.

**meta-signal-energy-nexus:**
- `ethos/signal.ethos` generates `src/generated/signal.rs`, under the same `build.rs` check.
- It imports `Caller`, `ProviderTarget` and `WindowTarget` from signal-energy-nexus, so each is one type. 0.5.0 had its own twins of ProviderTarget and WindowTarget and an in-place `Target.{ Provider Target }`.
- The ordinary types it used are re-exported as before.

**energy-nexus:**
- The two contracts are repinned.
- The code uses the generated names:
  - `Input`, `Output` and `Refused_Data` in the ordinary contract;
  - `Input`, `Output` and `Program_Data` in the meta contract;
  - the newtypes the Ethos names, such as `Window.used: Used(Percent)`, `Reading.at: At(Instant)` and `Caller.process_id: ProcessId`.
- No adapter and no twin remain for the contract types.
- UPGRADES has an "Unreleased" entry. Versions are unchanged.

## The byte proof

Each contract has `tests/hand_and_generated.rs`, which freezes the 0.5.0 hand declarations verbatim. The meta test also carries the ordinary hand types it used.

For a value of every type and every variant (Reminder and Recipient across every aspect and model, every Set variant, every Output), the test checks four things:
1. the value is archived through the hand type;
2. those bytes are read as the generated type and archived again, and the two archives are asserted equal;
3. the generated archive is read back as the hand type and asserted equal to the original;
4. under `datom` (the gate runs `--all-features`), the two datom texts are asserted equal.

**Result: no difference in any type.** The rkyv bytes and the datom text are identical for every type of both contracts.

The independent 0.4.0 fixture test also holds every binary and datom line unchanged, now built from the generated types.

**The one thing that moves is the contract digest.** ethos-zero 28 refuses the 0.5.0 Ethos text, so the text had to change, and the digest is the hash of that text:

| contract | 0.5.0 digest | generated digest |
|---|---|---|
| ordinary | -301146476426041394 | 5566004852532848722 |
| meta | -4620172360499517031 | 192963525083358617 |

- `tests/fixtures/contract.txt` now holds the new identity: the digest, the greeting and the receipts.
- `hand_and_generated` asserts the old digest and that the two differ.

**Why that does not move the live wire.** No socket on Energy main greets: the daemon reads a `Call` frame with no handshake. The digest is read only by tests, and by energy-nexus-tests on its unreleased stage-one branch.

The store is unaffected: energy-nexus's `memory_admission` still reads the e5722529 `energy.rkyv` fixture and passes.

I did not change any byte, so there is no wire version for you to decide in this step. Whether the moved digest counts as a contract version is question 2.

## Design questions, each with my plainest reading

1. **Position pairing makes `Redeem` answer `Changed`.**
   - **Why.** I kept the outputs in 0.5.0 order (Read, Subscribed, Changed, Redeemed, Refused), because reordering is a wire change, and the brief reserves that to you. Under position pairing, the generated `Answering::redeem` yields `Changed_Data`, and Redeemed comes back only through the refusal arm.
   - **Plainest reading:** move Redeemed before Changed, as Fable ruled for Flow (fm07), before this contract is released. Only the rkyv tags of `Output::Changed` and `Output::Redeemed` swap (2↔3). The CLIs speak datom, which carries names, not tags, so they are unaffected. The only binary peers are the daemon and the translator, which ship in one package. Nothing outside energy-nexus needs rebuilding.
   - **This is the choice the code forced in step one.** I stopped there, with nothing reordered.
2. **The digest moved.**
   - **Plainest reading:** at release, the contracts become 0.6.0 with this identity. The version is yours to set; the branches leave it at 0.5.0, marked "Unreleased".
   - Whether Energy's sockets should greet, as Flow's do, is a separate step. energy-nexus-tests' stage-one branch already has that work.
3. **Where the Library lives.**
   - I put it in signal-energy-nexus, where the hand types lived and every consumer already imported them. Flow keeps its library in a crate of its own Nexus repository (flow-ethos), but that would make energy-nexus a dependency of its own contracts, at a revision.
   - **Plainest reading:** keep it in the contract. In step two, energy-nexus's own `ethos/library.ethos`, now a stale copy read only by a test, is removed. Its Memory, Operation and Emission then import `signal_energy_nexus:[ … ]`.
4. **The digest covers `signal.ethos` alone, not the library**, as in Flow. A change to a library type's shape would pass the greeting unseen.
   - **Plainest reading:** follow Flow for now. Ask Fable whether a contract's identity should include the library it imports.
5. **`Refused` is declared in place, so it is generated as `Refused_Data`.** The Operation's `Failed` carries the same type, and the Ethos vision says a type used in more than one place is declared once and named.
   - **Plainest reading:** declare `Refused` in the Signal's types section, so the Rust name is `Refused` and the bytes are the same. Fold it into the same unreleased digest as question 1, so the identity moves once.
6. **The operation outcome's shape.** operation.ethos says `Levelled.Option<Level>` and `Failed.[ ProviderDown NoReset … ]`. The code carries `LevelChange { old, latest }` and the Signal's `Refused`, whose ProviderDown carries the Provider. Nothing archives these types.
   - **Plainest reading:** the Ethos follows the code: `Levelled.LevelChange` and `Failed.Refused`, imported.
7. **Memory.**
   - memory.ethos lacks the stored root `Memory.{ Vector<Latest> History Configuration }` and has no envelope or version. ethos-zero 28 cannot generate an upgrade from an earlier layout. `Answer` has no counterpart in the code.
   - **Plainest reading:**
     - declare the root;
     - keep the envelope and the frozen `unversioned` and `version1` layouts hand-written, as Flow kept its frozen predecessors;
     - write Configuration's defaults and rules as trait impls on the generated type;
     - prove the store by archiving both ways and reading the e5722529 fixture.
8. **Emission.** emission.ethos is a Signal wrapper over the daemon–translator socket, not an Emission root. ethos-zero 28 cannot express four things here:
   - Emittable on emissions that carry nothing (the code uses unit structs);
   - two emissions that share the outcome `Observed`;
   - `TurnEnds`, which is one emission with a stream of outcomes.
   - **Plainest reading:** an Emission root for the four calls, each with an outcome of its own, plus a Signal over the socket that imports them. TurnEnds stays a Signal subscription. The internal tags may move, since both ends ship together.
   - **For Fable**, beside Flow's open Herdr-events and Codex app-server questions.
9. **The translator's Memory (`Programs`, `energy-translator.rkyv`) has no Ethos.**
   - **Plainest reading:** a second Memory root, the translator's own, since it is its own process and store.
10. **The CLI configuration datom** (`CliConfiguration`, `ConfigurationRefusal`) has no root.
    - **Plainest reading:** a Library in energy-nexus.
11. **The reminder is a `format!` datom string** of Flow's Send.
    - **Plainest reading:** build signal-flow 63's typed `Input::Send` and datomize it. This is a translator change, not an Ethos one.

## Not done here

- **Step two.** The Memory, Operation and Emission roots, the translator Memory, the stale library copy, and the audit rerun.
- **The CriomOS-home relock.** Nothing to relock until a release.
- **energy-nexus-tests.** Not moved. It is not a live client.
- **The audit verdict.** At 0b9e6b4, Energy's Signal and meta Signal are generated and checked at every build. Memory, Operation and Emission are not, so the verdict is still not "yes".
