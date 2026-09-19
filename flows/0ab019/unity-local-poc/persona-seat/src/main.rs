//! Explicit-start, single-worker local Persona Signal seat.

use std::{env, fs, io::Write, os::{fd::AsRawFd, unix::{fs::PermissionsExt, net::{UnixListener, UnixStream}}}, path::Path};

use signal::{FrameCapacity, FrameReading, Framable};
use signal_mentci::{ByteViewable, Restorable, Signal, Signalizable};
use unity_poc_persona_seat::observe::respond;
use unity_poc_persona_seat::ledger::AttemptLedger;
use unity_poc_persona_seat::protocol::PersonaEnvelope;

const MAX_BODY_BYTES: usize = 256 * 1024;

fn peer_pid(stream: &UnixStream) -> Option<u32> {
    let mut credential = std::mem::MaybeUninit::<libc::ucred>::uninit();
    let mut length = std::mem::size_of::<libc::ucred>() as libc::socklen_t;
    // Linux supplies SO_PEERCRED from the connected Unix socket; the client
    // cannot choose this PID in its serialized Signal body.
    let status = unsafe {
        libc::getsockopt(stream.as_raw_fd(), libc::SOL_SOCKET, libc::SO_PEERCRED,
            credential.as_mut_ptr().cast(), &mut length)
    };
    if status != 0 || length as usize != std::mem::size_of::<libc::ucred>() { return None; }
    let credential = unsafe { credential.assume_init() };
    u32::try_from(credential.pid).ok()
}

fn handle(mut stream: UnixStream, mentci_pid: u32, ledger: &AttemptLedger) {
    if peer_pid(&stream) != Some(mentci_pid) { return; }
    let Ok(body) = stream.read_frame(FrameCapacity::from(MAX_BODY_BYTES)) else { return; };
    let Ok(envelope) = Signal::<PersonaEnvelope>::from(body.bytes().to_vec()).restore() else { return; };
    let Some(request) = envelope.into_request() else { return; };
    let response = respond(request, ledger);
    let Ok(archive) = response.signalize() else { return; };
    let Ok(frame) = archive.framed(FrameCapacity::from(MAX_BODY_BYTES)) else { return; };
    let _ = stream.write_all(&frame);
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let socket = env::var("UNITY_POC_PERSONA_SOCKET")?;
    let mentci_pid: u32 = env::var("UNITY_POC_MENTCI_PID")?.parse()?;
    let ledger_dir = env::var("UNITY_POC_ATTEMPT_DIR")?;
    let ledger_path = Path::new(&ledger_dir);
    if !ledger_path.is_absolute() { return Err("attempt directory must be absolute".into()); }
    let ledger = AttemptLedger::open(ledger_path)?;
    let path = Path::new(&socket);
    if !path.is_absolute() || path.exists() {
        return Err("Persona socket must be an unused absolute path".into());
    }
    let listener = UnixListener::bind(path)?;
    fs::set_permissions(path, fs::Permissions::from_mode(0o600))?;
    for stream in listener.incoming() {
        if let Ok(stream) = stream { handle(stream, mentci_pid, &ledger); }
    }
    Ok(())
}
