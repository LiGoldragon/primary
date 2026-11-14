# dzs final paired-child ownership proposal

Status: proposal only. This report does not authorize or contain a production source edit, build, publication, deployment, or approved implementation.

Immutable baseline: `c537aec8eaf6a4bea34ef022744d1df89283db97`.

Immutable `crates/translator/src/bin/belief-pair.rs` blob: `db0e42d2883a77f3a43befedf76f2877805b394b`.

The private type, trait, and error body below is proposed. It is uncompiled, untested, and not an approved implementation.

```rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum PairMember { Nexus, Translator }

#[derive(Debug)]
enum PairSupervisionError {
    Wait(nix::errno::Errno),
    UnexpectedTerminal {
        observed_pid: Pid,
        observed_status: WaitStatus,
    },
}

impl std::fmt::Display for PairSupervisionError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Wait(error) => write!(formatter, "waiting for the Belief pair failed: {error}"),
            Self::UnexpectedTerminal { observed_pid, .. } =>
                write!(formatter, "wait returned an unexpected terminal child: {observed_pid}"),
        }
    }
}
impl std::error::Error for PairSupervisionError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self { Self::Wait(error) => Some(error), Self::UnexpectedTerminal { .. } => None }
    }
}
impl From<nix::errno::Errno> for PairSupervisionError {
    fn from(error: nix::errno::Errno) -> Self { Self::Wait(error) }
}

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
        // Existing semantics: attempt SIGTERM, then block attempting reap;
        // both results remain best-effort and ignored.
        let _ = kill(pid, Signal::SIGTERM);
        let _ = waitpid(pid, None);
    }
}

trait PairedChildLifetime {
    fn nexus_process_id(&self) -> Pid;
    fn translator_process_id(&self) -> Pid;
    fn take_nexus_input(&mut self) -> Option<std::process::ChildStdin>;
    fn take_translator_input(&mut self) -> Option<std::process::ChildStdin>;
    fn retain_or_take_terminal(
        &mut self,
        status: WaitStatus,
    ) -> Result<Option<WaitStatus>, PairSupervisionError>;
    fn wait_for_first_terminal(&mut self) -> Result<WaitStatus, PairSupervisionError>;
    fn stop_live(&mut self);
}

impl PairedChildLifetime for PairedChildren {
    fn nexus_process_id(&self) -> Pid {
        ChildLifetime::process_id(self.nexus.as_ref().expect("live Nexus child"))
    }
    fn translator_process_id(&self) -> Pid {
        ChildLifetime::process_id(self.translator.as_ref().expect("live Translator child"))
    }
    fn take_nexus_input(&mut self) -> Option<std::process::ChildStdin> {
        self.nexus.as_mut().expect("live Nexus child").stdin.take()
    }
    fn take_translator_input(&mut self) -> Option<std::process::ChildStdin> {
        self.translator.as_mut().expect("live Translator child").stdin.take()
    }

    fn retain_or_take_terminal(
        &mut self,
        status: WaitStatus,
    ) -> Result<Option<WaitStatus>, PairSupervisionError> {
        match status {
            terminal @ WaitStatus::Exited(pid, _)
            | terminal @ WaitStatus::Signaled(pid, _, _) => {
                if pid == PairedChildLifetime::nexus_process_id(self) {
                    // waitpid already reaped it; relinquish before any cleanup runs.
                    drop(std::mem::take(&mut self.nexus));
                    Ok(Some(terminal))
                } else if pid == PairedChildLifetime::translator_process_id(self) {
                    drop(std::mem::take(&mut self.translator));
                    Ok(Some(terminal))
                } else {
                    // This terminal child is already reaped, but is never classified
                    // as either owned child. Both owned slots remain live.
                    Err(PairSupervisionError::UnexpectedTerminal {
                        observed_pid: pid,
                        observed_status: terminal,
                    })
                }
            }
            WaitStatus::Stopped(..)
            | WaitStatus::Continued(..)
            | WaitStatus::PtraceEvent(..)
            | WaitStatus::PtraceSyscall(..)
            | WaitStatus::StillAlive => Ok(None),
        }
    }

    fn wait_for_first_terminal(&mut self) -> Result<WaitStatus, PairSupervisionError> {
        // Bounded source invariant: standalone belief-pair directly creates only
        // these two children. waitpid(-1) is not intrinsically owned-only; an
        // externally arranged tracer/subreaper can violate this scope.
        loop {
            let status = waitpid(Pid::from_raw(-1), None)?;
            if let Some(terminal) =
                PairedChildLifetime::retain_or_take_terminal(self, status)?
            {
                return Ok(terminal);
            }
        }
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
    fn drop(&mut self) { PairedChildLifetime::stop_live(self); }
}
```

## Illustrative integration shape

The following integration comments, elisions, and placeholder calls are illustrative and uncompiled. They show ownership and exit coverage, not exact compilable source.

```rust
let mut nexus = Command::new(&deployment.nexus_executable.0)
    .stdin(Stdio::piped()).spawn()?;
let translator = match Command::new(&deployment.translator_executable.0)
    .stdin(Stdio::piped()).spawn()
{
    Ok(child) => child,
    Err(error) => {
        ChildLifetime::stop_and_reap(&mut nexus); // spawn2 failure remains single-child
        return Err(error.into());
    }
};
let mut children = PairedChildren {
    nexus: Some(nexus),
    translator: Some(translator),
}; // owner exists immediately after successful spawn2

let uid = UserId(i64::from(Uid::current().as_raw()));
let gid = shared_translator::GroupId(i64::from(Gid::current().as_raw()));
if deployment.owner != Owner::Login(uid.clone()) {
    return Err("deployment owner is not the launching login".into()); // Drop both
}

let bootstrapped = (|| -> Result<(), Box<dyn std::error::Error>> {
    let mut input = PairedChildLifetime::take_nexus_input(&mut children)
        .ok_or("Nexus bootstrap pipe")?;
    let nexus_pid = PairedChildLifetime::nexus_process_id(&children);
    let translator_pid = PairedChildLifetime::translator_process_id(&children);
    // Build/write the existing Nexus bootstrap using translator_pid.
    // Build/write the existing Translator bootstrap using nexus_pid.
    Ok(())
})();
if let Err(error) = bootstrapped { return Err(error); } // Drop both

// Existing bounded socket wait is unchanged.
if !meta_translator.exists() {
    return Err("meta translator socket did not appear".into()); // Drop both
}

for (revision, set) in sets.into_iter().enumerate() {
    // Existing text_request `?` and decode `?`: either error drops both.
    let text = belief_nexus_translator::text_request(...)?;
    let response = belief_nexus_translator::decode_meta_response_text(&text)?;
    match response {
        meta::Response::Configured(_) => {}
        meta::Response::ConfigureRefused(meta::ConfigurationRefusal::StaleRevision(_))
            if revision == 0 => break,
        other => return Err(format!("deployment configuration failed: {other:?}").into()),
        // Drop both; old duplicate explicit stop calls are removed.
    }
}

let ended = PairedChildLifetime::wait_for_first_terminal(&mut children)?;
// Matching terminal child was reaped and taken. Function return drops owner,
// which attempts SIGTERM + blocking reap only for the surviving Some slot.
Err(format!("paired Belief process ended: {ended:?}").into())
```

`PairSupervisionError::Wait` preserves the existing `waitpid` error as a source through the private boundary. `UnexpectedTerminal` is a named typed variant carrying the exact PID and `WaitStatus`; the status is acknowledged as already reaped, neither owned slot is removed, and dropping the owner cleans both owned children.

## Bounded regression plan

1. **Classification unit table.** Construct a pair fixture and feed `Stopped`, `Continued`, `PtraceEvent`, `PtraceSyscall`, and `StillAlive` to `retain_or_take_terminal`; assert `Ok(None)` and both slots remain `Some`. This has no OS timing assumption.
2. **Nexus terminal.** Start two controllable child processes and end Nexus. `wait_for_first_terminal` returns the exact Nexus `Exited` or `Signaled`, the Nexus slot is `None`, and Translator remains `Some`. Dropping the owner terminates and reaps Translator, with no second Nexus termination or reap attempt.
3. **Translator terminal.** Prove the symmetric behavior.
4. **Unexpected terminal classification.** Feed a terminal status carrying a third PID to the classification method; assert the exact `UnexpectedTerminal { observed_pid, observed_status }` and that both owned slots remain `Some`. This tests classification only; it does not claim `waitpid` did not already reap that external status.
5. **Original error exits.** Controllable binaries make owner validation fail, the bootstrap pipe fail, socket appearance fail, Configure transport fail after the socket appears, and the Configure response malformed. After `belief-pair` exits, both recorded owned PIDs are absent and reaped. A spawn2 failure separately proves only Nexus is stopped and reaped.
6. **Wait error boundary.** An injectable private wait seam returns a chosen `Errno`; assert `PairSupervisionError::Wait` preserves it and owner cleanup attempts both children. The seam supplies a wait result only and adds no runtime policy.
7. **Valid supervision control.** Either owned child ends normally; survivor cleanup remains SIGTERM followed by blocking wait. Cleanup return values remain ignored, with no retry, timeout, or escalation assertion.

## Explicit bounds

The proposal retains `waitpid(-1)` under the source-supported standalone two-child scope. It is not intrinsically owned-only. Cleanup errors remain best-effort and ignored, and cleanup may block. The proposal adds no threads, pidfds, timeout, escalation, socket behavior, placement behavior, startup policy, deployment, or runtime activation.
