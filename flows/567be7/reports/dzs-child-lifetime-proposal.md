# dzs — proposal only

Immutable baseline: c537aec8eaf6a4bea34ef022744d1df89283db97; belief-pair blob db0e42d2883a77f3a43befedf76f2877805b394b.

This is an illustrative, uncompiled ownership/exit shape applying Primary's direction. It is not a source edit or an implementation-authority claim. No build, publication or runtime action accompanies it.

## Existing exits

`belief-pair` main owns both Child values after lines 120–123. Existing stop (98–101) sends SIGTERM and then waits, ignoring both results. Spawn-two failure stops/reaps Nexus before the pair exists. After both spawn: owner mismatch (126), Configure transport (169), decode (170–171), and supervision wait failure (180) can return without cleanup. Bootstrap failure (152), socket timeout (157), and typed configuration failure (175) explicitly stop both. Normal supervision (180–182) reaps one then stops/reaps its survivor.

## Proposed Rust shape

```rust
struct PairedChildren {
    nexus: Option<Child>,
    translator: Option<Child>,
}

trait ChildLifetime {
    fn process_id(&self) -> Pid;
    fn stop_and_reap(&mut self);
}

impl ChildLifetime for Child {
    fn process_id(&self) -> Pid {
        Pid::from_raw(i32::try_from(self.id()).expect("child pid fits i32"))
    }

    fn stop_and_reap(&mut self) {
        let pid = ChildLifetime::process_id(self);
        let _ = kill(pid, Signal::SIGTERM);
        let _ = waitpid(pid, None);
    }
}

trait PairedChildLifetime {
    fn nexus_mut(&mut self) -> &mut Child;
    fn translator_mut(&mut self) -> &mut Child;
    fn wait_for_owned_end(&mut self) -> Result<WaitStatus, Box<dyn std::error::Error>>;
    fn stop_live(&mut self);
}

impl PairedChildLifetime for PairedChildren {
    fn nexus_mut(&mut self) -> &mut Child {
        self.nexus.as_mut().expect("live Nexus child")
    }

    fn translator_mut(&mut self) -> &mut Child {
        self.translator.as_mut().expect("live Translator child")
    }

    fn wait_for_owned_end(&mut self) -> Result<WaitStatus, Box<dyn std::error::Error>> {
        let nexus_pid = ChildLifetime::process_id(
            self.nexus.as_ref().expect("live Nexus child"));
        let translator_pid = ChildLifetime::process_id(
            self.translator.as_ref().expect("live Translator child"));
        let ended = waitpid(Pid::from_raw(-1), None)?;
        match ended.pid() {
            Some(pid) if pid == nexus_pid => {
                drop(std::mem::take(&mut self.nexus));
            }
            Some(pid) if pid == translator_pid => {
                drop(std::mem::take(&mut self.translator));
            }
            observed => return Err(format!(
                "wait returned a process outside the Belief pair: {observed:?}"
            ).into()),
        }
        Ok(ended)
    }

    fn stop_live(&mut self) {
        if let Some(mut child) = std::mem::take(&mut self.nexus) {
            ChildLifetime::stop_and_reap(&mut child);
        }
        if let Some(mut child) = std::mem::take(&mut self.translator) {
            ChildLifetime::stop_and_reap(&mut child);
        }
    }
}

impl Drop for PairedChildren {
    fn drop(&mut self) {
        PairedChildLifetime::stop_live(self);
    }
}
```

Placement, immediately at the existing spawn boundary:

```rust
let mut nexus = Command::new(/* unchanged configuration */).spawn()?;
let translator = match Command::new(/* unchanged configuration */).spawn() {
    Ok(child) => child,
    Err(error) => {
        ChildLifetime::stop_and_reap(&mut nexus);
        return Err(error.into());
    }
};
let mut children = PairedChildren {
    nexus: Some(nexus),
    translator: Some(translator),
};
```

Every subsequent exit crosses this owner. Existing explicit post-spawn stop branches become error returns; the owner performs cleanup once. Bootstrap/stdin/PID accesses use the narrow trait accessors; existing values and ordering stay unchanged. At supervision:

```rust
let ended = PairedChildLifetime::wait_for_owned_end(&mut children)?;
Err(format!("paired Belief process ended: {ended:?}").into())
```

A reaped owned child is taken out before the survivor is stopped. An outer wait error leaves both owned and triggers cleanup on return. Spawn-two failure remains the pre-owner single-child cleanup.

## Failure semantics and judgment boundaries

- Existing ignored SIGTERM and child-specific wait results are preserved, not improved by assertion. Drop cannot return those errors. A failed signal followed by blocking wait may still hang; cleanup wait failure remains silent.
- No timeout, retry, escalation or new typed cleanup evidence is proposed under this direction.
- The shape rejects a wait result for an unrelated PID rather than treating every non-Nexus child as Translator. This exact-PID boundary needs Primary's judgment; it is not silently claimed as approved.
- The proposal still uses waitpid(-1) as the existing supervisor does. Whether to narrow waiting itself is a separate decision.
- Option removal prevents duplicate normal termination/reap. It does not create evidence that an ignored cleanup wait succeeded.
- No socket cleanup, placement, configuration, bootstrap or deployment policy changes are included.

This report is derived from the implementation flow's bounded read-only analysis; no independent compile/runtime evidence exists for the illustrative code.

## Append-only review correction — proposal remains unapproved

Primary required two corrections to the illustrative code above. A `WaitStatus` carrying a PID is not necessarily terminal/reaped. Only matching `Exited` or `Signaled` may remove the owned live child; nonterminal statuses retain ownership and continue waiting. Also `waitpid(-1)` may already reap an unrelated child before PID rejection, so the initial shape cannot claim owned-only waiting. The earlier illustrative shape is superseded by these requirements and is not suitable for implementation as written.

A subsequent exact-PID waiter-thread exploration was rejected before any source change: a waiter can reap before its channel event is consumed, leaving `Some` with a stale PID that early-return cleanup could signal; thread construction can also panic before safe owner establishment. No claim of adequate synchronization is made.

Bounded current-source facts: standalone main has exactly two direct spawn calls at 120/121; no further creation/subreaper setup was found in the post-spawn path. Ordinary execution absent externally arranged tracer/subreaper state has those two direct children. Source alone does not establish absence of externally arranged state. The smallest conditional Option-owner proposal retains waitpid(-1) under that explicit scope and removes only matching terminal statuses. An unrelated terminal child may already have been reaped before violation reporting. Whether that scope is acceptable is Primary's pending judgment. Stronger intrinsic owned-only first-exit observation requires a separate OS-handle/dependency decision; none is chosen here.

No dzs source edit, build or publication accompanied these refinements. The b7c isolated test-only verification is a separate handoff and grants no dzs implementation authority.
