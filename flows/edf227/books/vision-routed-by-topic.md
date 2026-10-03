# Vision, routed by topic

What you said: a flow's topics are known; when new vision or a notion touching a topic arrives, it is routed to the flow holding that topic, delivered with its next messages after a minimum window, not pushed each time. This is that, as the machine would hold it.

## 1. A topic is a typed value

A topic is a variant tree: a subject, then its subtopics as deeper variants. Subtopics grow by submitting a variant; once approved it enters the ethos and the component is recompiled. The same Library also holds the raw psyche record, described in section 2, so every component shares it.

```
Library                              ; the topic vocabulary, shared by every component
[ flow:[ FlowId ] ]                  ; from Flow's Library
[ Topic.[ Flow.[ Launch               ; the Flow Nexus and its parts
                 Role
                 Capsule
                 Identity ]
          Curriculum.[ Module         ; context modules and their placement
                       Placement
                       Registry ]
          Ethos.[ Syntax              ; the schema language
                  Kinds
                  Library ]
          Nexus.[ Signal              ; nexuses in general
                  Memory
                  Deployment ]
          Psyche.[ Logging            ; how the living's words are kept and reach seats
                   Distillation
                   Routing ]
          Operations.[ Monitoring     ; the cluster, quota, reaching you
                       Quota
                       Contact ] ]
  Record.{ Topic                     ; one raw psyche record
           Level.[ Vision Notion ]   ; the level the hearing flow gave it
           Verbatim.String           ; his words, exact
           Provenance.String         ; where and when they were said
           Heard.FlowId } ]          ; the flow that logged it
[]
[]
```

<svg viewBox="0 0 360 696" role="img" aria-label="The topic tree: six subjects, each with its subtopics, one subtopic lit.">
<defs>
<linearGradient id="gTrunk1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="var(--bark)"/><stop offset="1" stop-color="var(--leaf)"/></linearGradient>
<linearGradient id="gBox1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--panel2)"/><stop offset="1" stop-color="var(--panel)"/></linearGradient>
<radialGradient id="gGlow1"><stop offset="0" stop-color="var(--hot)" stop-opacity=".55"/><stop offset="1" stop-color="var(--hot)" stop-opacity="0"/></radialGradient>
</defs>
<path d="M14 6 C 8 209, 20 418, 14 626" stroke="url(#gTrunk1)" stroke-width="9" fill="none" stroke-linecap="round"/>
<path d="M14 80 C 30 80, 36 80, 50 80" stroke="var(--bark)" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="96" cy="80" rx="48" ry="17" fill="var(--root)"/>
<text x="96" y="85" text-anchor="middle" class="tb">Flow</text>
<path d="M144 80 C 164 80, 154 41, 176 41" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="30" width="60" height="22" rx="11" fill="var(--leafbg)"/>
<text x="206" y="46" text-anchor="middle" class="tl">Launch</text>
<path d="M144 80 C 164 80, 154 67, 176 67" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="56" width="42" height="22" rx="11" fill="var(--leafbg)"/>
<text x="197" y="72" text-anchor="middle" class="tl">Role</text>
<path d="M144 80 C 164 80, 154 93, 176 93" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="82" width="68" height="22" rx="11" fill="var(--leafbg)"/>
<text x="210" y="98" text-anchor="middle" class="tl">Capsule</text>
<path d="M144 80 C 164 80, 154 119, 176 119" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="108" width="77" height="22" rx="11" fill="var(--leafbg)"/>
<text x="214" y="124" text-anchor="middle" class="tl">Identity</text>
<path d="M14 191 C 30 191, 36 191, 50 191" stroke="var(--bark)" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="96" cy="191" rx="48" ry="17" fill="var(--root)"/>
<text x="96" y="196" text-anchor="middle" class="tb">Curriculum</text>
<path d="M144 191 C 164 191, 154 165, 176 165" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="154" width="60" height="22" rx="11" fill="var(--leafbg)"/>
<text x="206" y="170" text-anchor="middle" class="tl">Module</text>
<path d="M144 191 C 164 191, 154 191, 176 191" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="180" width="85" height="22" rx="11" fill="var(--leafbg)"/>
<text x="219" y="196" text-anchor="middle" class="tl">Placement</text>
<path d="M144 191 C 164 191, 154 217, 176 217" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="206" width="77" height="22" rx="11" fill="var(--leafbg)"/>
<text x="214" y="222" text-anchor="middle" class="tl">Registry</text>
<path d="M14 289 C 30 289, 36 289, 50 289" stroke="var(--bark)" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="96" cy="289" rx="48" ry="17" fill="var(--root)"/>
<text x="96" y="294" text-anchor="middle" class="tb">Ethos</text>
<path d="M144 289 C 164 289, 154 263, 176 263" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="252" width="60" height="22" rx="11" fill="var(--leafbg)"/>
<text x="206" y="268" text-anchor="middle" class="tl">Syntax</text>
<path d="M144 289 C 164 289, 154 289, 176 289" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="278" width="51" height="22" rx="11" fill="var(--leafbg)"/>
<text x="202" y="294" text-anchor="middle" class="tl">Kinds</text>
<path d="M144 289 C 164 289, 154 315, 176 315" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="304" width="68" height="22" rx="11" fill="var(--leafbg)"/>
<text x="210" y="320" text-anchor="middle" class="tl">Library</text>
<path d="M14 387 C 30 387, 36 387, 50 387" stroke="var(--bark)" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="96" cy="387" rx="48" ry="17" fill="var(--root)"/>
<text x="96" y="392" text-anchor="middle" class="tb">Nexus</text>
<path d="M144 387 C 164 387, 154 361, 176 361" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="350" width="60" height="22" rx="11" fill="var(--leafbg)"/>
<text x="206" y="366" text-anchor="middle" class="tl">Signal</text>
<path d="M144 387 C 164 387, 154 387, 176 387" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="376" width="60" height="22" rx="11" fill="var(--leafbg)"/>
<text x="206" y="392" text-anchor="middle" class="tl">Memory</text>
<path d="M144 387 C 164 387, 154 413, 176 413" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="402" width="94" height="22" rx="11" fill="var(--leafbg)"/>
<text x="223" y="418" text-anchor="middle" class="tl">Deployment</text>
<path d="M14 485 C 30 485, 36 485, 50 485" stroke="var(--bark)" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="96" cy="485" rx="48" ry="17" fill="var(--root)"/>
<text x="96" y="490" text-anchor="middle" class="tb">Psyche</text>
<path d="M144 485 C 164 485, 154 459, 176 459" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="448" width="68" height="22" rx="11" fill="var(--leafbg)"/>
<text x="210" y="464" text-anchor="middle" class="tl">Logging</text>
<path d="M144 485 C 164 485, 154 485, 176 485" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="474" width="111" height="22" rx="11" fill="var(--leafbg)"/>
<text x="232" y="490" text-anchor="middle" class="tl">Distillation</text>
<path d="M144 485 C 164 485, 154 511, 176 511" stroke="var(--hot)" stroke-width="4" fill="none" stroke-linecap="round"/>
<circle cx="230" cy="511" r="52" fill="url(#gGlow1)"/>
<rect x="176" y="500" width="68" height="22" rx="11" fill="var(--hot)"/>
<text x="210" y="516" text-anchor="middle" class="tl hot">Routing</text>
<path d="M14 583 C 30 583, 36 583, 50 583" stroke="var(--bark)" stroke-width="5" fill="none" stroke-linecap="round"/>
<ellipse cx="96" cy="583" rx="48" ry="17" fill="var(--root)"/>
<text x="96" y="588" text-anchor="middle" class="tb">Operations</text>
<path d="M144 583 C 164 583, 154 557, 176 557" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="546" width="94" height="22" rx="11" fill="var(--leafbg)"/>
<text x="223" y="562" text-anchor="middle" class="tl">Monitoring</text>
<path d="M144 583 C 164 583, 154 583, 176 583" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="572" width="51" height="22" rx="11" fill="var(--leafbg)"/>
<text x="202" y="588" text-anchor="middle" class="tl">Quota</text>
<path d="M144 583 C 164 583, 154 609, 176 609" stroke="var(--leaf)" stroke-width="2" fill="none" stroke-linecap="round"/>
<rect x="176" y="598" width="68" height="22" rx="11" fill="var(--leafbg)"/>
<text x="210" y="614" text-anchor="middle" class="tl">Contact</text>
<text x="180" y="662" text-anchor="middle" class="tc">a flow declares the branches it holds</text>
</svg>

## 2. A flow declares its topics; a record names its topic

A flow's record in Flow's memory carries the topics it holds. A raw psyche record — vision or notion, verbatim with provenance — carries the topic it touches, said by the flow that heard it, and is a shared type: it lives in the topic Library, and Memory and Signal both import it.

```
Memory                               ; what Flow remembers for routing
[ flow:[ FlowId ]                    ; from Flow's Library
  topic:[ Topic Record ] ]           ; from the topic Library
[ Holding.{ FlowId                   ; which topics a flow holds
            Vector<Topic> }
  Pending.{ FlowId                   ; records waiting for a flow's next delivery
            Vector<Record> } ]
```

<svg viewBox="0 0 360 470" role="img" aria-label="A record and a holding joined by a match line on the same topic.">
<defs>
<linearGradient id="gTrunk2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="var(--bark)"/><stop offset="1" stop-color="var(--leaf)"/></linearGradient>
<linearGradient id="gBox2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--panel2)"/><stop offset="1" stop-color="var(--panel)"/></linearGradient>
<radialGradient id="gGlow2"><stop offset="0" stop-color="var(--hot)" stop-opacity=".55"/><stop offset="1" stop-color="var(--hot)" stop-opacity="0"/></radialGradient>
</defs>
<rect x="30" y="14" width="300" height="196" rx="18" fill="url(#gBox2)" stroke="var(--root)" stroke-width="3"/>
<text x="50" y="42" class="tt">Record</text>
<rect x="46" y="62" width="268" height="24" rx="12" fill="var(--hot)"/>
<text x="62" y="79" class="tl hot">Topic</text>
<rect x="46" y="91" width="268" height="24" rx="12" fill="var(--leafbg)"/>
<text x="62" y="108" class="tl">Level</text>
<rect x="46" y="120" width="268" height="24" rx="12" fill="var(--leafbg)"/>
<text x="62" y="137" class="tl">Verbatim</text>
<rect x="46" y="149" width="268" height="24" rx="12" fill="var(--leafbg)"/>
<text x="62" y="166" class="tl">Provenance</text>
<rect x="46" y="178" width="268" height="24" rx="12" fill="var(--leafbg)"/>
<text x="62" y="195" class="tl">Heard</text>
<rect x="30" y="290" width="300" height="140" rx="18" fill="url(#gBox2)" stroke="var(--leaf)" stroke-width="3"/>
<text x="50" y="318" class="tt">Holding</text>
<rect x="46" y="332" width="268" height="24" rx="12" fill="var(--leafbg)"/><text x="62" y="349" class="tl">FlowId</text>
<rect x="46" y="364" width="268" height="24" rx="12" fill="var(--hot)"/><text x="62" y="381" class="tl hot">Topics</text>
<text x="62" y="415" class="tm">a flow and the topics it holds</text>
<circle cx="314" cy="75" r="40" fill="url(#gGlow2)"/><circle cx="314" cy="376" r="40" fill="url(#gGlow2)"/>
<path d="M314 74 C 356 120, 356 330, 314 376" stroke="var(--hot)" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="1 0"/>
<path d="M326 360 L314 378 L300 364" stroke="var(--hot)" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="132" y="228" width="96" height="36" rx="18" fill="var(--hot)"/><text x="180" y="252" text-anchor="middle" class="tl hot">match</text>
<path d="M180 210 L180 228 M180 264 L180 290" stroke="var(--hot)" stroke-width="3" stroke-dasharray="4 4" fill="none"/>
</svg>

## 3. Routing and delivery

The flow that hears vision logs it and reports it. Flow matches the record's topic against every holding and queues it for each holder. Delivery rides the holder's next message after a minimum window, never a wake per record. Nothing polls; a crash never claims a delivery it did not make.

```
Signal                               ; what the ordinary socket says about psyche records
[ flow:[ FlowId ]
  topic:[ Topic Record ] ]
[ Hold.{ FlowId                      ; a flow declares a topic it now holds
         Topic }
  Release.{ FlowId                   ; a flow drops a topic
            Topic }
  Heard.Record ]                     ; a flow reports a record it logged
[ Held
  Released
  Queued.Vector<FlowId>              ; the holders it was queued for
  Refused.[ UnknownFlow.FlowId
            UnknownTopic.Topic ] ]
[]
```

<svg viewBox="0 0 360 454" role="img" aria-label="Seven steps from speech to delivery.">
<defs>
<linearGradient id="gTrunk3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="var(--bark)"/><stop offset="1" stop-color="var(--leaf)"/></linearGradient>
<linearGradient id="gBox3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--panel2)"/><stop offset="1" stop-color="var(--panel)"/></linearGradient>
<radialGradient id="gGlow3"><stop offset="0" stop-color="var(--hot)" stop-opacity=".55"/><stop offset="1" stop-color="var(--hot)" stop-opacity="0"/></radialGradient>
</defs>
<path d="M60 40 C 94 60, 26 82, 60 102 C 26 122, 94 144, 60 164 C 94 184, 26 206, 60 226 C 26 246, 94 268, 60 288 C 94 308, 26 330, 60 350 C 26 370, 94 392, 60 412" stroke="var(--hot)" stroke-width="9" fill="none" stroke-linecap="round" opacity=".9"/>
<circle cx="60" cy="40" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="45" text-anchor="middle" class="tl hot">1</text>
<rect x="92" y="23" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="45" class="tl">the living speaks</text>
<circle cx="60" cy="102" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="107" text-anchor="middle" class="tl hot">2</text>
<rect x="92" y="85" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="107" class="tl">a seat logs the record</text>
<circle cx="60" cy="164" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="169" text-anchor="middle" class="tl hot">3</text>
<rect x="92" y="147" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="169" class="tl">Heard to Flow</text>
<circle cx="60" cy="226" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="231" text-anchor="middle" class="tl hot">4</text>
<rect x="92" y="209" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="231" class="tl">Flow matches holdings</text>
<circle cx="60" cy="288" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="293" text-anchor="middle" class="tl hot">5</text>
<rect x="92" y="271" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="293" class="tl">Pending per holder</text>
<circle cx="60" cy="350" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="355" text-anchor="middle" class="tl hot">6</text>
<rect x="92" y="333" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="355" class="tl">the window passes</text>
<circle cx="60" cy="412" r="19" fill="var(--root)" stroke="var(--bg)" stroke-width="3"/><text x="60" y="417" text-anchor="middle" class="tl hot">7</text>
<rect x="92" y="395" width="256" height="34" rx="17" fill="var(--leafbg)"/><text x="106" y="417" class="tl">rides the holder's next message</text>
</svg>

## 4. The window and what it costs

The minimum window is configuration in Flow's memory, set over the meta socket. A long window batches more and costs less context; a short one brings you to a seat sooner. Delivery is one message carrying every pending record for that flow, verbatim, each with its provenance.

<svg viewBox="0 0 360 240" role="img" aria-label="Records arrive as dots; after the window one delivery carries them all.">
<defs>
<linearGradient id="gTrunk4" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="var(--bark)"/><stop offset="1" stop-color="var(--leaf)"/></linearGradient>
<linearGradient id="gBox4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--panel2)"/><stop offset="1" stop-color="var(--panel)"/></linearGradient>
<radialGradient id="gGlow4"><stop offset="0" stop-color="var(--hot)" stop-opacity=".55"/><stop offset="1" stop-color="var(--hot)" stop-opacity="0"/></radialGradient>
</defs>
<path d="M16 120 L330 120" stroke="var(--bark)" stroke-width="6" stroke-linecap="round" fill="none"/>
<text x="16" y="150" class="tm">time</text>
<circle cx="40" cy="120" r="9" fill="var(--root)"/>
<circle cx="78" cy="120" r="9" fill="var(--root)"/>
<circle cx="104" cy="120" r="9" fill="var(--root)"/>
<circle cx="160" cy="120" r="9" fill="var(--root)"/>
<circle cx="196" cy="120" r="9" fill="var(--root)"/>
<path d="M28 86 L28 74 L214 74 L214 86" stroke="var(--leaf)" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<text x="121" y="62" text-anchor="middle" class="tl2">the window</text>
<circle cx="270" cy="120" r="44" fill="url(#gGlow4)"/>
<path d="M214 120 C 240 190, 280 190, 308 128" stroke="var(--hot)" stroke-width="8" fill="none" stroke-linecap="round"/>
<path d="M286 120 L310 124 L300 146" stroke="var(--hot)" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<text x="180" y="226" text-anchor="middle" class="tl2">one delivery, all records</text>
</svg>

1. Build it as drawn.
2. The topic tree is wrong or incomplete — comment the branches you want.
3. Comment what else to change.
