Presentation.{ «Who registers belief» }

# Who registers belief

Created by Opus from Fable's ruling; assembled by Sonnet.

### Proposal 1: The owner registers; an admitted peer furnishes · psyche-belief › vision/belief-nexus-v1.md

**Comment** First launch found that the module does not say who registers a repository. The ruling places registration with the owner, as Define is, and furnishing with any admitted peer.

  ## Signal
+ The owner registers a belief repository at the Belief Nexus's own CLI, by his login, as he defines a complex at the Flow Nexus.
+ A peer the meta peer list names furnishes over any registered repository.
+
  A registered repository is watched: when its main moves, every workspace furnished with a module it changed is furnished again, and the Flow Nexus is told which flows now run on old belief, so a perma flow can be refreshed on it. A module is named by kind and subject; its front matter names its placement, system prompt or skill. The skills directory is the harness's.

```datom
+ Register.
+   /git/github.com/LiGoldragon/psyche-belief
+ Registered.
+   /git/github.com/LiGoldragon/psyche-belief
```

```sh
+ belief-nexus main '
+   Register.
+     /git/github.com/LiGoldragon/psyche-belief'
```

### Proposal 2: The meta peer list · psyche-belief › vision/belief-nexus-v1.md

**Comment** Tentative. The lines name a meta peer list that this module's meta Signal lacks, so it gains one, in the shape the herdr Nexus's meta already has.

  ## Meta

```ethos
  Signal
  [ belief:[ Kind Placement ] ]        ; imports
  [ Configure.Set ]                    ; inputs: one value at a time
  [ Configured.Set ]                   ; outputs: the value set
  [ Set.[ Placement.{ Kind             ; types: the default
-                     Placement } ] ]  ;   placement per Kind
+                     Placement }      ;   per Kind
+         Peer.PeerBinding  ; a peer admitted
+                           ;   to Furnish
+         RemovePeer.PeerId ]  ; a peer removed
+   UserId.Integer                     ; a login
+   ProcessId.Integer
+   PeerId.String                      ; a peer's name
+   PeerIdentity.{ UserId ProcessId }  ; checked by
+                                      ;   kernel
+                                      ;   credentials
+   PeerBinding.{ PeerId               ; a peer, bound
+                 PeerIdentity } ]
```
