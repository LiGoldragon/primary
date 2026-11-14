# Order: knowledge and role fixes, landed on Fable's word

From Psyche beliefReview Fable. These are the machine's own modules (knowledge, role); by the living's word of 12 November Fable writes and deploys them on its own word. A worker makes each change in the module's repository, one commit per module, and lists every changed line, before and after, in flows/4fb10a/review/knowledge-fixes-landed.md. That file becomes a review page (landed changes, dark shades) for the living to skim. Where a quoted line does not match the module as it stands, the worker changes nothing in that module and says so.

1. knowledge:flow-messaging, section «Running permaflows and their routing». Remove the table of addresses and the sentence dating it («The table below was read from both on 2026-11-07 … on 2026-11-10.»). Keep the two queries, the Observe sentence, the three sentences on Purpose (routing description, blank Purpose, declared historical task) and the closing line «Read both queries again before routing work», reworded only as far as «again» and «the table below» need. Reason: a table of running flows is stale the day after it is read, and belief names no particular flows; what each role does is in its role module.

2. knowledge:codex-reset. Remove the two dated observations: «Observed 2026-11-03: three resets listed …» and «On 2026-11-03, `/nix/store/…-codex-0.163.0/bin/codex` worked.» If a sentence around them only introduces them, it goes too.

3. knowledge:nix-rust-builds. Remove the two measurement parentheticals («(herdr-nexus on prometheus: its members' builds … unchanged)» and the Clippy sentence's figures from «(herdr-nexus on prometheus:» to its end, keeping the claim that linting adds little to a test build). In the two example lines that name his builder, write `<builder>` for the host name.

4. knowledge:criomos. In the passage on the ext4 directory limit, keep the mechanism (the limit, the kernel's refusal, `tune2fs -O large_dir` clearing it on a mounted root, btrfs having no such limit) and remove what is his machines' alone: the host names, the entry count of one host, «zeus is unchecked», and the path `flows/121cc5/ext4-fix.md`.

5. role:book-publishing-procedure. Remove the sentence beginning «A watch this flow holds by an order passes to its successor», which the same module contradicts («this flow arms no watch»).

6. role:comment-watch. It sends the living's comment as `Soft.Psyche.{ «context» «verbatim» }`. Check the Flow CLI's own answer for the Send input (knowledge:flow-messaging says `Living.{ Context Verbatim }` as of Flow 0.54.3); if the CLI says Living, change the role to `Soft.Living.{ «context» «verbatim» }`.

7. role:comment-relay, role:comment-relay-description, role:psyche-core-tertiary-description. Report only, change nothing: which flow or subagent each is bound to today (the roles datom and the Flow Nexus configuration), and whether role:comment-watch has taken their work. I rule after the report.
