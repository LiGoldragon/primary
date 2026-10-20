Presentation.{ «Flow: sleeping and waking seats» }

Machine: development branch of Flow, not yet deployed.

## A seat's life

Machine: a seat that is not running keeps no harness.

```text
+------------------------+
| seat awake             |
| harness running        |
+-----------+------------+
            |
            | turn ends
            v
+------------------------+
| seat idle              |
| harness waiting        |
+-----------+------------+
            |
            | goes to sleep
            v
+------------------------+
| seat asleep            |
| harness closed         |
| transcript kept        |
+------------------------+
```

## A message wakes a sleeping seat

Machine: the waking request starts the seat; the queue arrives with it.

```text
+------------------------+
| seat asleep            |
| harness closed         |
| transcript kept        |
+-----------+------------+
            |
            | message arrives
            v
+------------------------+
| waking request         |
+------+-------------+---+
       |             |
       | has a       | has no
       | transcript  | transcript
       v             v
+-----------+ +-----------+
| resumed   | | started   |
| from its  | | fresh from|
| transcript| | its       |
|           | | modules   |
+-----+-----+ +-----+-----+
      |             |
      +------+------+
             |
             | hands over
             v
+------------------------+
| whole queue, oldest    |
| first, in first prompt |
+------------------------+
```

## 1. Crystallization: what puts a seat to sleep

Machine: the harness's turn-end report can arrive early or twice, so 1a also waits for an idle harness. A Codex seat lives in a shared server, so closing its pane may free less memory than a Claude seat's; this is not measured.

File: `psyche-context/skills/vision-flow.md`

```text
  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.
+
+ A metaflow sleeps so that a session not running keeps no harness: as soon as its turn ends and the harness is idle, with nothing waiting in its queue, the harness closes; the transcript stays and the address stays.
  
  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id.
```

1. A metaflow sleeps 1a «as soon as its turn ends and the harness is idle, with nothing waiting in its queue» · 1b «once its harness has stayed idle for a set time, with nothing waiting in its queue; the timer is a poller, registered and reported» · 1c «when it is ordered to sleep». Default: 1a.

## 2. Crystallization: which requests wake a sleeping seat

Machine: the closed set of request types already exists; 2c is the judgment by a small model that the line above it already describes for the living's own touch on a topic. Proposals 2, 4 and 5 edit one paragraph and merge.

File: `psyche-context/skills/vision-flow.md`

```text
  A request reaching a metaflow is one of a closed set of types, each with its waking effect: an order, a question, the living's words, a result, a notice. Message asks Flow to send a request to a metaflow; …
- A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A metaflow asleep is woken by an order, a question or the living's words and receives its whole queue, oldest first, in the first prompt, a result or a notice waiting there until a waking; a metaflow under refresh queues what arrives until its successor has started.
  A metaflow a request needs is started whether or not it is running; …
```

2. A metaflow asleep is woken by 2a «an order, a question or the living's words» with the added words «, a result or a notice waiting there until a waking» · 2b «any request», no added words · 2c «a request that a small model judges worth a waking», no added words. Default: 2a.

## 3. Crystallization: whether a Primary wakes automatically

Machine: two readings of his orders. 3a follows the low-usage order, where every Fable call goes through him: a Primary runs on Fable, so a waking by message spends Fable without his word. 3b follows his record that a Primary is not started without a Secondary: it wakes on a request whenever its Secondary is awake, spending Fable each time that holds. 3c treats a Primary as any layer.

File: `psyche-context/skills/vision-flow.md`

```text
  A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+
+ A sleeping Primary stays asleep until it is started on the living's permission; requests for it wait in its queue.
  
  Flow exposes everything from the harness, the bare input: …
```

3. A sleeping Primary 3a «stays asleep until it is started on the living's permission; requests for it wait in its queue» · 3b «is woken only while its Secondary is awake; requests for it wait in its queue until then» · 3c «is woken like any other layer». Default: 3a.

## 4. Crystallization: resume the old transcript or start fresh

Machine: whether a resumed Claude session keeps its session id, and so its flow id, is unverified; the build checks it before this lands. 4b uses each layer's existing refresh threshold as the measure of a young transcript, pending his proposal on what a young context is.

File: `psyche-context/skills/vision-flow.md`

```text
  A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; …
- A metaflow a request needs is started whether or not it is running; with no working transcript to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
+ A metaflow a request needs is started whether or not it is running; with no transcript kept from its sleep to reawaken, it is fed the metaflow's context modules and the prompt it is to get now.
```

4. A started metaflow is fed its context modules and prompt 4a «with no transcript kept from its sleep to reawaken» · 4b «with no transcript below its layer's refresh threshold to reawaken» · 4c «on every waking». Default: 4a, moving to 4b once the proposal on a young context is ruled.

## 5. Crystallization: what waking holds meanwhile

Machine: the waking runs on a worker, the metaflow locked by a held lease, as a refresh locks it; 5b serves one launch at a time and holds Flow's other deliveries for its length.

File: `psyche-context/skills/vision-flow.md`

```text
  A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; …
- A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh queues what arrives until its successor has started.
+ A metaflow idle is woken by a waking request and receives its whole queue, oldest first, in the first prompt; a metaflow under refresh or waking queues what arrives until its successor or woken seat has started, while Flow keeps serving every other request.
```

5. A metaflow under refresh or waking queues what arrives until its seat has started 5a «, while Flow keeps serving every other request» · 5b «, while Flow serves one waking at a time and holds its other deliveries until then». Default: 5a.
