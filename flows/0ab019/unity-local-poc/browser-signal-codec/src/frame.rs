//! The browser bridge admits one complete canonical Signal frame per binary
//! WebSocket message. The archive body is restored by `signal`, never by this
//! framing boundary.

use std::convert::TryFrom;

pub const SIGNAL_FRAME_PREFIX_BYTES: usize = 4;
pub const SIGNAL_MAX_BODY_BYTES: usize = 8 * 1024 * 1024;
pub const POC_MAX_BODY_BYTES: usize = 256 * 1024;

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CanonicalFrame {
    body: Vec<u8>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum FrameRefusal {
    MissingPrefix,
    DeclaredLengthMismatch,
    BodyTooLarge,
}

impl TryFrom<&[u8]> for CanonicalFrame {
    type Error = FrameRefusal;

    fn try_from(message: &[u8]) -> Result<Self, Self::Error> {
        let prefix = message
            .get(..SIGNAL_FRAME_PREFIX_BYTES)
            .ok_or(FrameRefusal::MissingPrefix)?;
        let declared = u32::from_be_bytes(
            prefix.try_into().map_err(|_| FrameRefusal::MissingPrefix)?,
        ) as usize;
        if declared > SIGNAL_MAX_BODY_BYTES || declared > POC_MAX_BODY_BYTES {
            return Err(FrameRefusal::BodyTooLarge);
        }
        if message.len() - SIGNAL_FRAME_PREFIX_BYTES != declared {
            return Err(FrameRefusal::DeclaredLengthMismatch);
        }
        Ok(Self {
            body: message[SIGNAL_FRAME_PREFIX_BYTES..].to_vec(),
        })
    }
}

impl CanonicalFrame {
    pub fn body(&self) -> &[u8] {
        &self.body
    }

    pub fn from_body(body: Vec<u8>) -> Result<Self, FrameRefusal> {
        if body.len() > SIGNAL_MAX_BODY_BYTES || body.len() > POC_MAX_BODY_BYTES {
            return Err(FrameRefusal::BodyTooLarge);
        }
        Ok(Self { body })
    }

    pub fn into_message(self) -> Vec<u8> {
        let mut message = Vec::with_capacity(SIGNAL_FRAME_PREFIX_BYTES + self.body.len());
        message.extend_from_slice(&(self.body.len() as u32).to_be_bytes());
        message.extend_from_slice(&self.body);
        message
    }
}

#[cfg(test)]
mod tests {
    use super::{CanonicalFrame, FrameRefusal, POC_MAX_BODY_BYTES};

    #[test]
    fn exact_length_round_trip() {
        let original = CanonicalFrame::from_body(vec![1, 2, 3]).expect("small body");
        let message = original.clone().into_message();
        assert_eq!(message, [0, 0, 0, 3, 1, 2, 3]);
        assert_eq!(CanonicalFrame::try_from(message.as_slice()), Ok(original));
    }

    #[test]
    fn refuses_trailing_or_missing_bytes() {
        assert_eq!(CanonicalFrame::try_from([0, 0, 0, 1, 1, 2].as_slice()), Err(FrameRefusal::DeclaredLengthMismatch));
        assert_eq!(CanonicalFrame::try_from([0, 0, 0, 2, 1].as_slice()), Err(FrameRefusal::DeclaredLengthMismatch));
        assert_eq!(CanonicalFrame::try_from([0, 0, 0].as_slice()), Err(FrameRefusal::MissingPrefix));
    }

    #[test]
    fn refuses_bodies_beyond_poc_limit() {
        assert_eq!(CanonicalFrame::from_body(vec![0; POC_MAX_BODY_BYTES + 1]), Err(FrameRefusal::BodyTooLarge));
    }
}
