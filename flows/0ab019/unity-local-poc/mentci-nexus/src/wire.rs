//! One WebSocket binary message is exactly one canonical Signal frame.
//! Signal owns the prefix and archive body; the bridge checks full-message
//! consumption so a trailing second frame or junk cannot be smuggled in.

use std::io::Cursor;

use signal::{FrameCapacity, FrameReading, Framable};
use signal_mentci::{ByteViewable, Query, Response, Restorable, Signal, Signalizable};

const POC_MAX_BODY_BYTES: usize = 256 * 1024;
const SIGNAL_PREFIX_BYTES: usize = 4;

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum WireRefusal {
    NonCanonicalLength,
    InvalidArchive,
    ArchiveTooLarge,
}

pub fn restore_query(message: &[u8]) -> Result<Query, WireRefusal> {
    if message.len() < SIGNAL_PREFIX_BYTES
        || message.len() > POC_MAX_BODY_BYTES + SIGNAL_PREFIX_BYTES
    {
        return Err(WireRefusal::ArchiveTooLarge);
    }
    let mut cursor = Cursor::new(message);
    let body = cursor.read_frame(FrameCapacity::from(POC_MAX_BODY_BYTES))
        .map_err(|_| WireRefusal::NonCanonicalLength)?;
    if cursor.position() != message.len() as u64 {
        return Err(WireRefusal::NonCanonicalLength);
    }
    Signal::<Query>::from(body.bytes().to_vec())
        .restore()
        .map_err(|_| WireRefusal::InvalidArchive)
}

pub fn frame_response(response: Response) -> Result<Vec<u8>, WireRefusal> {
    response.signalize()
        .map_err(|_| WireRefusal::InvalidArchive)?
        .framed(FrameCapacity::from(POC_MAX_BODY_BYTES))
        .map_err(|_| WireRefusal::ArchiveTooLarge)
}

#[cfg(test)]
mod tests {
    use super::{frame_response, restore_query, WireRefusal};
    use signal_mentci::{Query, RosterObservation, Signalizable};
    use signal::{FrameCapacity, Framable};

    #[test]
    fn full_canonical_query_is_required() {
        let query = Query::ObserveRoster(RosterObservation {
            request_identifier: String::from("synthetic-request"),
        });
        let frame = query.clone().signalize().expect("archive")
            .framed(FrameCapacity::from(256 * 1024)).expect("frame");
        assert_eq!(restore_query(&frame), Ok(query));
        let mut trailing = frame.clone();
        trailing.push(0);
        assert_eq!(restore_query(&trailing), Err(WireRefusal::NonCanonicalLength));
        assert_eq!(restore_query(&frame[..frame.len() - 1]), Err(WireRefusal::NonCanonicalLength));
    }
}
