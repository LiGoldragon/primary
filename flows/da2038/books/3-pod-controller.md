Presentation.{ «The pod controller» }

## How write access passes between containers

Machine: the pod controller holds the only grant on a path.

```text
+------------------------+
| agent asks the pod     |
| controller for a path  |
+-----------+------------+
            |
            | checks the grant
            v
+------------------------+
| pod controller         |
+-----+------------+-----+
      |            |
      | permits    | refuses
      v            v
+-----------+ +-----------+
| controller| | agent     |
| stops     | | keeps its |
| accepting | | access;   |
| writes on | | no write  |
| the path  | | opens     |
+-----+-----+ +-----------+
      |
      | waits for
      v
+------------------------+
| kernel flush complete  |
+-----------+------------+
            |
            | switches
            v
+------------------------+
| permission switched    |
+-----------+------------+
            |
            | grants
            v
+------------------------+
| other container holds  |
| the only write access  |
+------------------------+
```

## What the pod controller owns

Machine: one controller owns processes, input and sockets; the caller is known by the master process, never by a name it states.

```text
+------------------------+
| pod controller         |
+---+--------+--------+--+
    |        |        |
    | owns   | locks  | listens on
    v        v        v
+-------+ +-------+ +--------+
|process| | PTY   | | socket |
|       | | input | |        |
+-------+ +-------+ +----+---+
                         |
                         | asks who called
                         v
                    +----------+
                    | master   |
                    | process  |
                    +----+-----+
                         |
                         | answers
                         v
                    +----------+
                    | caller   |
                    | identity |
                    +----------+
```

## 1. Crystallization: the pod, long-term

Machine: a new long-term psyche module.

File: `psyche-context/skills/vision-pod.md` (new)

```text
+ ---
+ description: The pod controller — the pod as container, who may write which path, process and PTY control — is being designed or judged against what the living wants.
+ dependencies: [vision-ethos, vision-datom]
+ ---
+
+ Long-term vision.
+
+ ## The pod is the container
+
+ The pod is the container: lighter than a virtual machine, which carries its own kernel; both may exist. The pod becomes part of CriomOS and, through it, controls the environment of every process.
+
+ ## The meta pod holds who may access what
+
+ The meta pod is a data structure of permissions: who may access, at different levels of access. Callers are known by who called the socket, so authentication is verified through the master process; sockets may differ per level, and eventually they need not.
+
+ ## One owner for every process
+
+ Control of all processes gives a complete lock and a single owner of each process. A process can be locked, or its input in the PTY can be locked.
+
+ ## One writer per path, switched atomically
+
+ Writable access to a path, recursively or not, is passed around in datom; Ethos is the language that controls it. The permission switches between containers atomically, and at most one writer holds a path at any time.
+
+ ## Flush before the switch
+
+ After the pod controller stops accepting writes on a path, the kernel has no operation left to flush to the system. Only then is the permission changed and opened on the other side.
+
+ ## Agents ask; the controller decides
+
+ Agents ask the pod controller for access to files and the access is controlled programmatically. An agent without write access through the pod controller cannot write the file.
+
+ ## The security of the system arrives later
+
+ Until the pod controller exists the system is open, and the harness sandbox is not used for security; the system's own sandbox and correctness come after.
```

## 2. Crystallization: the Ethos anatomy of the pod controller

Machine: the pod controller's ethos anatomy: Library, Signal, Operation, Memory.

File: `pod-controller/pod.ethos` (new)

```ethos
+ Library
+ []                              ; imports
+ [ Path.String                   ; types
+   Access.[ Read Write ]         ; levels
+   Recursive.Boolean             ; subtree?
+   Owner.String                  ; flow holding
+   Pod.String                    ; container
+   Process.Integer               ; pid
+   Grant.{ Path Access           ; one grant
+           Recursive Owner Pod } ]
+ []                              ; traits
+ []                              ; associations
+
+ Signal
+ [ pod:[ Path Access Recursive   ; imports
+         Process Grant ] ]
+ [ AskAccess.AccessRequest       ; queries
+   Release.Path
+   LockInput.Process
+   UnlockInput.Process ]
+ [ Granted.Grant                 ; responses
+   Released.Path
+   Refused.Refusal
+   InputLocked.Process
+   InputUnlocked.Process ]
+ [ AccessRequest.{ Path Access   ; types
+                   Recursive }
+   Refusal.[ NoAccess            ; no access
+             Held.Grant ] ]      ;   another writer
+
+ Operation
+ [ pod:[ Path Access Pod ] ]       ; imports
+ [ StopWrites.Path               ; one per effect
+   AwaitFlush.Path
+   SwitchPermission.{ Path       ;   to the next
+                      Access Pod }
+   Grant ]                       ; opens other
+
+ Memory
+ [ pod:[ Grant Process Owner     ; imports
+         Pod ] ]
+ [ Grant                         ; one writer
+   Ownership.{ Process Owner     ; process owner
+               Pod } ]
```

Machine: the caller is no field in a request; the socket's caller identity, verified through the master process, supplies it.

Numbered choices:

1. Sockets are 1a «one socket» · 1b «one socket per level of access».
2. A grant without the Recursive flag covers 2a «the path alone» · 2b «the whole subtree below it». Default: 2a.
3. Primary flows 3a «pass through the pod controller like every flow» · 3b «keep unrestricted access».
4. The pod 4a «contains the Capsule» · 4b «stays separate from the Capsule».
