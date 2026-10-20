Audit of book 14 v1 (source line refs), to fold into the revision you are making:
- Proposal 1 (L8–59) is not red/green: no File: line, no -/+ lines. Make the figure context and each choice a concrete landing (e.g. the files removed/added per choice), or the choices themselves the proposal with their code.
- Remove: quotes L10, L12, L57; counts L14, L142; L63 narration of the draft's non-existent files; L65–84 already-landed changes (they are state, not proposals; show only the current file around any proposed change).
- Code: L148 proposes new .mjs (Clojure only). L127–129, L190 hard-code "/shared.edn" and "/metaflow/" (values to EDN). L93–96 Malli `Launch` defined, unused. L118–120 bug: metaflow EDN holds keywords, result reads ":Mind :Core :Primary". L105–120 drop the landed reader's checks (template must contain modules, handover, raw psyche; non-empty source paths). L182 calls values.clj the one reader of every value, but it reads only shared.edn while L154/L178 put values in mind.edn and metaflow/.
- Already exists: commit 3f1cf6c40 also added EDN_FIRST_PROMPT, a bb Clojure template reader inside tools/claude-native-seat-refresh.py. Proposal 2 must reckon with it.
- Figure: arrow L37 subject wrong (context-modules box does not "send through hm-*"); L43 says hm-* commits through field; L41 counts statusline.sh as a hook (it is the statusLine renderer).
- Code lines over 52 cols: L68, L81, L82, L160, L172.
- Runtime facts: /home/li/primary (L160, L166; use the skill variable), native session UUID (L172, L179), herdrSession 'default' (L160), flow id 41fa34 in authored config (L178), "primary/tools" (L23).
- Ambiguous choice refs: L78 "choices 1 and 2", L144 "choice 4".
- L81–83 shortened function closes with a } not in the real code.
