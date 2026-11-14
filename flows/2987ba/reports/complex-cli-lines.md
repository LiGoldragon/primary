vision/complex/1.md, three lines, each removed then added:

```sh
- flow-nexus 'Launch.{ designer fable «Read the book» }'
+ flow 'Launch.{ designer fable «Read the book» }'
- herdr-nexus 'Prompt.{ { main wQ:pT } «hello» }'
+ herdr 'Prompt.{ { main wQ:pT } «hello» }'
```

```sh
- for f in definitions/*.datom; do flow-nexus "Define.$(cat "$f")"; done
+ for f in definitions/*.datom; do flow "Define.$(cat "$f")"; done
```

Open to you: Define is configuration; if it belongs on the meta socket, the last line takes flow-meta.
