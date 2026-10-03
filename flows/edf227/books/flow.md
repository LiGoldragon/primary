Presentation.{ «Flow» }

## 1. What Flow does

Flow launches a seat. It makes the place the seat runs, writes its system prompt and first prompt, starts the harness, and hears every event from the harness's hooks through the Flow CLI. When a seat nears its context limit, Flow builds its successor and ends it. Flow locks sessions; Orchestrate locks files.

## 2. A voice

A seat is a voice: an aspect carrying a layer.

```
Aspect.[ Psyche
         Mind
         Field ]
Layer.[ Primary
        Secondary
        Tertiary
        Quaternary ]
Voice.[ Psyche.Layer
        Mind.Layer
        Field.Layer ]
```

The model behind a layer is configuration in a knowledge skill. A title is the voice and the flow id in words: `Psyche.Secondary abandonAbilityAble`.

## 3. The id in words

A flow id is 33 bits of the harness's own session id, rendered as three words, reversible: from the words, tools find the transcript. The rendering is a generic kind, usable for any width:

```
Wordable.{ []
           [ Dictionary<WordDictionary>
             Words<WordSequence> ]
           [ WIDTH_BITS.Integer
             as_words.[ Words ]
             parse_words:{ [ Words ]
                           [ Result<Self WordParseError> ] } ] }
```

## 4. The Capsule and the hooks

The Capsule makes where a seat runs: its own home, sockets and store, with only the credentials carried in. Every harness event — started, tool used, stopped — reaches Flow through a hook calling the Flow CLI, which knows its caller by process; Flow turns the events into Running, Idle, Ended. Nothing polls.

1. Build this.
2. Comment what to change.
