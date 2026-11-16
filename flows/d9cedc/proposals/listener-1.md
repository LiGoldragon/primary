Presentation.{ «The Listener, version 1» Proposal }

# The Listener, version 1

Created by Fable. Readers of Opus's and of mine read the listener as built and collected his words on it.

### Proposal 1: What versions 0 and 1 share · psyche-belief › vision/listener/0-1.md

::: description
+ The Nexus that turns the living's speech into text: what its versions share.
:::

+ The Listener turns speech into text, for each user of a host, on keys he binds.

+ A recording begins at once, whatever is still being transcribed.

+ The text is what he said, raw and whole: his hesitations, his stutters, his silences, his self-corrections and his rewordings are kept, and nothing is edited.

+ Nothing he says is lost: the audio is kept, whatever becomes of its transcription.

### Proposal 2: Version 0 stays as it is · psyche-belief › vision/listener/0.md

::: description
+ The Nexus that turns the living's speech into text, as it runs until version 1 replaces it.
:::

+ Version 0 starts on one key and stops on another, and leaves the text on the clipboard. It runs unchanged, on its own keys, until version 1 has replaced it; then it is removed.

### Proposal 3: Version 1 · psyche-belief › vision/listener/1.md

::: description
+ The Nexus that turns the living's speech into text: its jobs, its backends, its delivery and its configuration.
:::

+ # The Listener

+ A Nexus of vision:nexus:1, written whole and new, on a branch of its own. While it is tested it runs beside version 0, on a key of its own. Every type below is tentative in its name.

+ ## The types

+ ```ethos
+ Library
+ []                                          ; imports
+ [ JobId.String                              ; types: one recording
+   Text.String                               ;   what was said
+   AudioFile.String                          ;   where a job's Opus audio is kept
+   BackendName.String
+   ModelName.String
+   ServiceAddress.String                     ;   where the service is reached
+   SecretEntry.String                        ;   where the backend's key is kept, never the key
+   Language.String
+   Instruction.String                        ;   what the backend is told about how to transcribe
+   Reason.String                             ;   why a backend failed, in its own words
+   Window.String                             ;   a desktop window, by the desktop's own id
+   Days.Integer
+   Protocol.[ OpenAiBatch                    ;   how a service is spoken to: the recording sent whole at its end,
+              OpenAiRealtime ]               ;     or the audio sent as he speaks; a new protocol is a new variant
+   Backend.{ BackendName Protocol ServiceAddress ModelName
+             SecretEntry Language Instruction }
+   Delivery.[ Pasted                         ;   the text pasted, once and whole, where the focus is
+              Clipboard                      ;     or left on the clipboard
+              Returned ]                     ;     or only answered to the caller
+   LateDelivery.[ WhereFocused               ;   a text ready after he moved on: pasted wherever the focus is,
+                  WhereRecorded              ;     or only in the window it was recorded in, else the clipboard and a notice,
+                  OnRequest ]                ;     or held until he asks
+   Retention.[ Forever                       ;   how long audio and text are kept
+               Days ]
+   Attempt.{ BackendName Reason }            ;   one backend tried, and why it failed
+   State.[ Recording Transcribing            ;   where a job stands
+           Waiting                           ;     its text ready, not yet delivered
+           Delivered Failed Cancelled ]
+   JobStatus.{ JobId State } ]
+ []                                          ; traits
+ []                                          ; associations
+ ```

+ ## A recording is a job

+ A recording begins whenever he asks, with a hundred jobs still being transcribed as with none.

+ ```mermaid
+ flowchart TB
+     k["the key, pressed"] -- "Toggle begins" --> r["Recording: audio written to its file as he speaks"]
+     r -- "the key again: Toggle ends" --> t["Transcribing"]
+     r -- "Cancel" --> c["Cancelled: nothing transcribed"]
+     t -- "a backend answers" --> w["Waiting: the text is ready"]
+     t -- "every backend failed" --> f["Failed: the audio is kept"]
+     f -- "Retranscribe" --> t
+     w -- "its turn comes" --> d["Delivered"]
+     t -- "the key, pressed meanwhile" --> r2["another job, Recording at once"]
+ ```

+ ## What it says

+ ```ethos
+ Signal
+ [ listener:[ JobId Text BackendName Delivery Attempt JobStatus ] ] ; imports
+ [ Toggle                                    ; inputs: the default, one key: begins a recording,
+                                             ;   or ends the one in progress, transcribed and delivered
+   ToggleReturned                            ;   a variation: the text answered and not delivered
+   ToggleCustom.{ Delivery                   ;   every option: the delivery,
+                  Vector<BackendName> }      ;     and the backends to try, in order
+   Cancel                                    ;   the recording in progress is dropped
+   Deliver                                   ;   the next waiting text, delivered now
+   Recall                                    ;   the last text, delivered again
+   RecallJob.JobId                           ;   a variation: the text of that job
+   Retranscribe.JobId                        ;   a job's kept audio, transcribed again
+   Jobs                                      ;   the jobs not yet delivered
+   History ]                                 ;   every job kept
+ [ Toggled.[ Began.JobId                     ; outputs: a Toggle began a recording,
+             Ended.JobId ]                   ;   or ended one, answered at once; the transcription goes on
+   Cancelled.JobId
+   Delivering.JobId                          ;   answers Deliver
+   Recalled.Text
+   Retranscribing.JobId
+   Jobs.Vector<JobStatus>
+   History.Vector<JobStatus>
+   Transcribed.{ JobId Text }                ;   a reaction: the job's text, when it is ready
+   Failed.{ JobId Vector<Attempt> }          ;   a reaction: every backend failed
+   Refused.[ NothingRecording                ;   Cancel with no recording in progress
+             NothingWaiting                  ;   Deliver with no text waiting
+             NoBackend                       ;   no backend is configured
+             NoSuchJob.JobId ] ]
+ []                                          ; types
+ ```

+ ```datom
+ ; one key, pressed three times while the first job is still being transcribed
+ Toggle
+ Toggled.Began.a1
+ Toggle
+ Toggled.Ended.a1
+ Toggle
+ Toggled.Began.a2
+ Transcribed.{ a1 «So, um, what I, what I wanted to say is» }
+ ```

+ ## Backends, and the fallback

+ The executable names no service and no model. A backend is any service that speaks a protocol the Listener knows, so a model served that way is used by naming it.

+ ```mermaid
+ flowchart TB
+     j["a job: Transcribing"] -- "is given to" --> b1["the first backend configured"]
+     b1 -- "answers" --> x["Transcribed"]
+     b1 -- "fails: an Attempt is recorded, the job goes to" --> b2["the next backend"]
+     b2 -- "answers" --> x
+     b2 -- "fails, and none is left" --> f["Failed, with every Attempt; the audio waits for Retranscribe"]
+ ```

+ ## Real time

+ ```mermaid
+ flowchart TB
+     m["the microphone"] -- "each piece of audio, as he speaks, is written to" --> a["the job's Opus file"]
+     m -- "and, when the backend's protocol is real time, is sent to" --> b["the backend"]
+     b -- "sends back, as he speaks" --> t["the text so far"]
+     t -- "the key again: the text is whole within a moment, becomes" --> w["Waiting"]
+     a -- "the stream failed: the file is sent whole to" --> n["the next backend"]
+ ```

+ ## Delivery

+ A text is delivered by one paste, whole; it is never typed key by key. Texts are delivered in the order they were recorded.

+ ```mermaid
+ flowchart TB
+     w["a text is Waiting"] -- "every job recorded before it is delivered, failed or cancelled" --> q["its turn"]
+     q -- "he is still where he recorded it" --> p["one paste, where the focus is"]
+     q -- "he has moved on: LateDelivery is read from the configuration" --> l["the late delivery"]
+     l -- "WhereFocused" --> p
+     l -- "WhereRecorded" --> c["the clipboard, and a notice"]
+     l -- "OnRequest" --> h["held until Deliver"]
+     h -- "Deliver" --> p
+ ```

+ ## What it attempts

+ ```ethos
+ Operation
+ [ listener:[ JobId Text BackendName Delivery Attempt ] ] ; imports
+ [ Recording.JobId                           ; attempts: the audio captured to its file
+   Transcribing.{ JobId Vector<BackendName> } ;   the backends tried in order
+   Delivering.{ JobId Delivery }             ;   the text, in its turn
+   Cancelling.JobId
+   Recalling.JobId
+   Pruning ]                                 ;   what is past its retention, removed
+ [ Recorded.JobId                            ; outcomes
+   Transcribed.{ JobId Text }
+   Exhausted.{ JobId Vector<Attempt> }       ;   every backend failed
+   Delivered.JobId
+   Held.JobId                                ;   its turn has not come, or it waits for Deliver
+   Cancelled.JobId
+   Recalled.Text
+   Pruned.Vector<JobId> ]
+ []                                          ; types
+ ```

+ ## Every action answers an event

+ ```mermaid
+ flowchart TB
+     e1["the key is pressed"] -- "causes" --> a1["Recording, or its end and Transcribing"]
+     e2["a backend answers or fails"] -- "causes" --> a2["Transcribed, or the next backend"]
+     e3["a job is delivered, failed or cancelled"] -- "causes" --> a3["Delivering the next text waiting"]
+     e4["a recording is stored"] -- "causes" --> a4["Pruning what is past its retention"]
+     e5["Configure arrives on the meta socket"] -- "causes" --> a5["one value changed, for the next job"]
+ ```

+ ## What it remembers

+ A recording is stored as Opus, the most efficient format for voice, beside the text it became. Together they are the data a model of his own is one day trained on. Every past transcription is recalled, those made before version 1 among them.

+ ```ethos
+ Memory
+ [ listener:[ JobId Text AudioFile State Backend    ; imports
+              Delivery LateDelivery Retention ] ]
+ [ Job.{ JobId AudioFile Option<Text> State }        ; records: a job, its audio, and its text once transcribed
+   Configuration.{ Vector<Backend>                   ;   the backends, in the order they are tried
+                   Delivery                          ;   the default delivery
+                   LateDelivery
+                   Retention }
+   Answer.[ Succeeded Failed ] ]
+ ```

+ ## What it sends into the world

+ ```ethos
+ Emission
+ [ listener:[ Text AudioFile Backend Window Reason ] ] ; imports
+ [ Capture.[ Begin.AudioFile                 ; emissions: the microphone, written to the file as it records
+             End ]
+   Transcribe.{ Backend AudioFile }          ;   one call to one backend, the recording whole
+   Stream.{ Backend AudioFile }              ;   real time: the audio sent as it is recorded
+   Deliver.{ Delivery Text }                 ;   one paste, clipboard copy or desktop notice
+   Focus ]                                   ;   which window has the focus
+ [ Capturing.[ Captured                     ; outcomes: what the translator observed of each,
+               Uncaptured.Reason ]           ;   one for each emission, in the same order
+   Hearing.[ Heard.Text                      ;   a backend's transcription
+             Unheard.Reason ]
+   Streaming.[ Streamed.Text
+               Broken.Reason ]
+   Delivering.[ Delivered
+                Undelivered.Reason ]
+   Focused.Window ]
+ [ Delivery.[ Paste Copy Notify ] ]           ; types: how the text is delivered
+ ```

+ ## Everything is configuration

+ ```ethos
+ Signal
+ [ listener:[ Backend BackendName Delivery LateDelivery Retention ] ] ; imports
+ [ Configure.Set ]                           ; inputs: the meta socket, one value at a time
+ [ Configured.Set                            ; outputs: the change made
+   ConfigureRefused.[ UnknownBackend.BackendName
+                      DuplicateBackend.BackendName ] ]
+ [ Set.[ Backend                             ; types: one backend, added or replaced
+         RemoveBackend.BackendName
+         Order.Vector<BackendName>           ;   the order they are tried in, which is the fallback
+         Delivery                            ;   the default delivery
+         LateDelivery
+         Retention ] ]
+ ```

+ ```datom
+ ; every name and address is an example
+ Configure.Backend.{ first OpenAiRealtime «https://first.example» transcribe-live «example/first-key» en «Write every word as it is said, with every hesitation and repetition.» }
+ Configure.Backend.{ second OpenAiBatch «https://second.example» transcribe-large «example/second-key» en «Write every word as it is said, with every hesitation and repetition.» }
+ Configure.Order.[ first second ]
+ Configure.Delivery.Pasted
+ Configure.LateDelivery.WhereRecorded
+ Configure.Retention.Forever
+ ```

+ ```mermaid
+ flowchart TB
+     m["listener-meta, one datom"] -- "Configure, one value" --> n["the Listener"]
+     n -- "writes it to" --> c["Configuration, in Memory"]
+     c -- "is read by" --> j["the next job: its backends, its delivery, its retention"]
+ ```
