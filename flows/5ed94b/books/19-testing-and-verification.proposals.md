Presentation.{ «Testing and verification» }

Testing is how you know a thing works: a test starts the real machinery and watches it, and a witness is something anyone can run again. Everything else said about a thing is a claim. Say "yes" to a number to land it; for two texts, name the number.

**1. Skills are tested by running agents**
Kind: intent. Module: skill-designing. Action: edit.
> A skill is tested by running one agent with it and one without through the same scenario. A skill whose scenario does not show the skilled agent doing better is not released.

Rests on: 20 Aug, 2 Oct.

**2. Proof of concept starts in a sandbox**
Kind: intent. Module: testing. Action: edit.
> A proof of concept is first tested in a sandbox that never touches the running system: a virtual machine by default, except where it needs his own browser login.

Rests on: 19 Sep, 22 Aug.

**3. The semi-sandbox**
Kind: knowledge. Module: compensation-nix. Action: edit.
Text 1:
> A semi-sandbox on the host is the default for anything that needs a live model. It copies only the logins, builds all other configuration fresh on its own socket, and uses small cheap models.

Text 2:
> The same semi-sandbox also runs inside a virtual machine on Prometheus.

Rests on: 2 Oct, 26 Sep.

**4. Logins never in the automatic check**
Kind: knowledge. Module: compensation-nix. Action: edit.
> A scenario that needs no login and no network is a check the build runs on every push. A scenario that needs his logins or a live model is a runner started by hand, never a check.

Rests on: 26 Sep.

**5. Built by Nix, on the builder**
Kind: intent. Module: testing. Action: edit.
> Every test uses Nix-built binaries and scripts, so it is built on the remote builder and never on his laptop.

Rests on: 18 Sep.

**6. A witness can be rerun**
Kind: spirit. Module: behavior. Action: edit.
> A witness records its steps and versions so someone else can rerun it. What cannot be rerun is a claim, and a claim is not written into a file as a report.

Rests on: 5 Sep, "What is a report but hearsay put into a file?"

**7. Where witnesses live**
Kind: operation. Module: flow-evidence. Action: edit.
Text 1:
> Verified things are kept in one shared ledger; a new check is added to the old one, so nothing is verified twice.

Text 2:
> A witness lives in a folder in the flow that made it, found by the same layout in every flow.

Rests on: 19 Aug for 1; 3 and 5 Sep for 2.

**8. No model review in front of a gate**
Kind: intent. Module: testing. Action: edit.
> Where a build, a test or an activation can catch a failure, no model review stands in front of it.

Rests on: 28 Sep, "Green builds".

**9. The tester**
Kind: operation. Module: tester. Action: create.
> The tester gets only the target, a fixed revision, its limits and what counts as passing. It picks its own failure cases and its own source of the expected answer, then grades its evidence.

Rests on: 21 Sep, as relayed.

**10. Who tests**
Kind: intent. Module: testing. Action: edit.
Text 1:
> The layer that implements also tests, through a fresh flow of the same harness.

Text 2:
> The layer that implements also tests, through a flow of the other harness.

Rests on: 3 Oct.

**11. Travesties are removed at the root**
Kind: intent. Module: testing. Action: edit.
> A test that proves nothing, such as one that restates 1 + 1 = 2 piece by piece, is a travesty. Remove it at the root. Keep only tests shown reliable in real use.

Rests on: 10 Aug, 8 Sep, 1 Oct.

**12. A check is code at a boundary**
Kind: intent. Module: testing. Action: edit.
> Whatever is deterministic is done by cheap code, never by a model. A check is code at a real boundary that refuses a real failure. A prose line asking a model to check, or a probe message, is not a check. One tool checks any repository.

Rests on: 3 Oct, 29 Sep, 18 Aug.
