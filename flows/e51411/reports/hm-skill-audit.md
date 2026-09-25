# Audit of Mind 00f95a's HM skill change

Curriculum b52929d, Primary projection 644422cc4, HackyMessenger clojure c8eb491. Audited by an Opus subflow of e51411, 2026-09-25, read-only.

Pass: pane shape is #msg [sender text], metadata only in Datalevin; skill matches installed code; only a body that is itself one whole #msg is refused; projection matches sources and remotes.

Fix:
1. One home per meaning. The envelope shape (messaging.md:10, testing-datom-messaging.md:6), the no-nesting rule (messaging.md:18, testing-datom-messaging.md:6) and "HM constructs the envelope" (operational-status-presentation.md:18, testing-message-route.md:6) live only in compensation-hacky-messenger.md:8. messaging.md:10 becomes: "Hacky Messenger is the live compatibility bridge: it resolves a running target and prompts it through Herdr. A successful submission is not a read receipt." The other lines keep only "with the body only."
2. Receipt rules weakened. Restore "Preserve the submitted bytes in the receipt." (messaging.md:18) and the Held reasons, NotRegistered and InTransition keeping the text pending.
3. compensation-hacky-messenger.md:6: nine commands, adding hm-heartbeat-state; mention --pane and Fallback-Presented.
4. Primary has uncommitted hand edits in the generated .claude/.agents compensation-hacky-messenger SKILL.md. Generated trees are read-only: move the change to the Curriculum source and regenerate.
5. The Curriculum checkout is detached at 8563235 on messaging-basics-5f38bc, not main.
6. Code: plain hm-send --wait-presented (core.clj:656-659) reports Presented without calling presented!; only the --pane fallback and hm-send-abrupt check it. Make it observe, or refuse the flag.

## Sources

Opus subflow audit of the commits above; core.clj on HackyMessenger clojure.
