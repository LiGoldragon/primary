//! Durable, one-attempt POC ledger. No transcript text is persisted. A linked
//! attempt record is synced before any bridge call; an uncertain crash/restart
//! can never turn into a second send for the same request identifier.

use std::{
    fs::{self, File, OpenOptions},
    io::{self, Read, Write},
    os::unix::fs::{OpenOptionsExt, PermissionsExt},
    path::{Path, PathBuf},
    sync::atomic::{AtomicU64, Ordering},
};

use sha2::{Digest, Sha256};

static TEMP_SEQUENCE: AtomicU64 = AtomicU64::new(0);
const TARGET: &str = "effa1b\0mind-sol-of-0ab019\0wC:p2\0term_65bc91cf241bf2b\001a0b68e-e703-7d21-b908-7a7effa1bf8b";

#[derive(Debug, Eq, PartialEq)]
pub enum Begin {
    Fresh,
    PreviousAccepted(i64),
    PreviousUncertain,
    Conflict,
}

pub struct AttemptLedger {
    directory: PathBuf,
}

fn hex_hash(parts: &[&[u8]]) -> String {
    let mut hasher = Sha256::new();
    for part in parts {
        hasher.update((*part).len().to_be_bytes());
        hasher.update(part);
    }
    hasher.finalize().iter().map(|byte| format!("{byte:02x}")).collect()
}

impl AttemptLedger {
    pub fn open(directory: &Path) -> io::Result<Self> {
        let metadata = fs::symlink_metadata(directory)?;
        if !metadata.is_dir() || metadata.file_type().is_symlink()
            || metadata.permissions().mode() & 0o777 != 0o700
        {
            return Err(io::Error::new(io::ErrorKind::PermissionDenied, "ledger must be a real mode-0700 directory"));
        }
        Ok(Self { directory: directory.to_path_buf() })
    }

    fn paths(&self, request_id: &str) -> (PathBuf, PathBuf) {
        let key = hex_hash(&[request_id.as_bytes()]);
        (
            self.directory.join(format!("{key}.attempt")),
            self.directory.join(format!("{key}.receipt")),
        )
    }

    fn expected_record(flow_id: &str, text: &str) -> String {
        let fingerprint = hex_hash(&[flow_id.as_bytes(), TARGET.as_bytes(), text.as_bytes()]);
        format!("v1\n{fingerprint}\nstate=attempted-uncertain\n")
    }

    fn previous(&self, attempt: &Path, receipt: &Path, expected: &str) -> io::Result<Begin> {
        let mut actual = String::new();
        File::open(attempt)?.take(256).read_to_string(&mut actual)?;
        if actual != expected { return Ok(Begin::Conflict); }
        let mut recorded = String::new();
        match File::open(receipt) {
            Ok(file) => { file.take(128).read_to_string(&mut recorded)?; }
            Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(Begin::PreviousUncertain),
            Err(error) => return Err(error),
        }
        let Some(stamp) = recorded.strip_prefix("v1\naccepted-at=")
            .and_then(|value| value.strip_suffix('\n'))
            .and_then(|value| value.parse::<i64>().ok()) else {
                return Ok(Begin::PreviousUncertain);
            };
        Ok(Begin::PreviousAccepted(stamp))
    }

    pub fn begin(&self, request_id: &str, flow_id: &str, text: &str) -> io::Result<Begin> {
        let (attempt, receipt) = self.paths(request_id);
        let expected = Self::expected_record(flow_id, text);
        let temp = self.directory.join(format!(
            ".attempt-{}-{}", std::process::id(), TEMP_SEQUENCE.fetch_add(1, Ordering::Relaxed)
        ));
        let mut file = OpenOptions::new().write(true).create_new(true).mode(0o600).open(&temp)?;
        file.write_all(expected.as_bytes())?;
        file.sync_all()?;
        drop(file);
        let linked = fs::hard_link(&temp, &attempt);
        let _ = fs::remove_file(&temp);
        match linked {
            Ok(()) => {
                File::open(&self.directory)?.sync_all()?;
                Ok(Begin::Fresh)
            }
            Err(error) if error.kind() == io::ErrorKind::AlreadyExists =>
                self.previous(&attempt, &receipt, &expected),
            Err(error) => Err(error),
        }
    }

    pub fn record_transport_accepted(&self, request_id: &str, timestamp_nanos: i64) -> io::Result<()> {
        let (_, receipt) = self.paths(request_id);
        let mut file = OpenOptions::new().write(true).create_new(true).mode(0o600).open(receipt)?;
        write!(file, "v1\naccepted-at={timestamp_nanos}\n")?;
        file.sync_all()?;
        File::open(&self.directory)?.sync_all()
    }
}

#[cfg(test)]
mod tests {
    use std::{fs, os::unix::fs::DirBuilderExt, path::PathBuf};

    use super::{AttemptLedger, Begin};

    fn fixture() -> PathBuf {
        let path = std::env::temp_dir().join(format!("persona-ledger-test-{}-{}", std::process::id(),
            super::TEMP_SEQUENCE.fetch_add(1, std::sync::atomic::Ordering::Relaxed)));
        fs::DirBuilder::new().mode(0o700).create(&path).expect("private test directory");
        path
    }

    #[test]
    fn same_id_retry_never_reenters_bridge() {
        let path = fixture();
        let ledger = AttemptLedger::open(&path).expect("ledger");
        assert_eq!(ledger.begin("request-1", "effa1b", "synthetic").expect("first"), Begin::Fresh);
        assert_eq!(ledger.begin("request-1", "effa1b", "synthetic").expect("retry"), Begin::PreviousUncertain);
        fs::remove_dir_all(path).expect("remove private fixture");
    }

    #[test]
    fn same_id_different_body_or_target_is_conflict() {
        let path = fixture();
        let ledger = AttemptLedger::open(&path).expect("ledger");
        assert_eq!(ledger.begin("request-2", "effa1b", "first").expect("first"), Begin::Fresh);
        assert_eq!(ledger.begin("request-2", "effa1b", "second").expect("body"), Begin::Conflict);
        assert_eq!(ledger.begin("request-2", "different", "first").expect("target"), Begin::Conflict);
        fs::remove_dir_all(path).expect("remove private fixture");
    }

    #[test]
    fn restart_preserves_uncertain_and_accepted_receipts() {
        let path = fixture();
        let first = AttemptLedger::open(&path).expect("first ledger");
        assert_eq!(first.begin("request-3", "effa1b", "synthetic").expect("first"), Begin::Fresh);
        drop(first);
        let reopened = AttemptLedger::open(&path).expect("reopened ledger");
        assert_eq!(reopened.begin("request-3", "effa1b", "synthetic").expect("uncertain"), Begin::PreviousUncertain);
        reopened.record_transport_accepted("request-3", 1234).expect("durable accepted receipt");
        drop(reopened);
        let restarted = AttemptLedger::open(&path).expect("restarted ledger");
        assert_eq!(restarted.begin("request-3", "effa1b", "synthetic").expect("accepted"), Begin::PreviousAccepted(1234));
        fs::remove_dir_all(path).expect("remove private fixture");
    }
}
