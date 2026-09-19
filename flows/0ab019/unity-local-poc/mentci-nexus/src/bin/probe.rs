//! Read-only by default. A send requires an explicit request ID and verbatim
//! text; the probe prints receipt metadata only, never transcript contents.

use std::{env, error::Error};

use futures_util::{SinkExt, StreamExt};
use sha2::{Digest, Sha256};
use signal::{FrameCapacity, Framable};
use signal_mentci::{
    ConversationObservation, PsycheSubmission, Query, Response, Restorable,
    RosterObservation, Signal, Signalizable,
};
use tokio_tungstenite::{connect_async, tungstenite::{client::IntoClientRequest, http::HeaderValue, Message}};
use unity_poc_persona_seat::known_codex::{EXACT_ROLLOUT, NATIVE_UUID};

const MAX_BODY_BYTES: usize = 256 * 1024;

async fn exchange(query: Query) -> Result<Response, Box<dyn Error>> {
    let mut request = "ws://127.0.0.1:38081/signal".into_client_request()?;
    request.headers_mut().insert("Origin", HeaderValue::from_static("http://127.0.0.1:38081"));
    let (mut socket, _) = connect_async(request).await?;
    let frame = query.signalize()?.framed(FrameCapacity::from(MAX_BODY_BYTES))?;
    socket.send(Message::Binary(frame.into())).await?;
    let Some(message) = socket.next().await else { return Err("Signal socket closed without reply".into()); };
    let bytes = match message? {
        Message::Binary(bytes) => bytes,
        _ => return Err("Signal reply was not binary".into()),
    };
    if bytes.len() < 4 { return Err("Signal reply was shorter than prefix".into()); }
    let declared = u32::from_be_bytes(bytes[0..4].try_into()?) as usize;
    if declared > MAX_BODY_BYTES || declared + 4 != bytes.len() {
        return Err("Signal reply length mismatch".into());
    }
    Ok(Signal::<Response>::from(bytes[4..].to_vec()).restore()?)
}

#[tokio::main(flavor = "current_thread")]
async fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = env::args().skip(1).collect();
    match args.as_slice() {
        [mode] if mode == "read" => {
            let roster = exchange(Query::ObserveRoster(RosterObservation {
                request_identifier: "poc-probe-roster".into(),
            })).await?;
            match roster {
                Response::RosterObserved(snapshot) => {
                    println!("roster status={:?} flows={}", snapshot.source_status, snapshot.flows.len());
                    for flow in snapshot.flows.iter().take(8) {
                        println!("roster flow_id={} state={:?}", flow.flow_identifier, flow.flow_state);
                    }
                }
                Response::OperationUnavailable(failure) => println!("roster unavailable={:?}", failure.unavailability),
                _ => return Err("unexpected roster response".into()),
            }
            let conversation = exchange(Query::ObserveConversation(ConversationObservation {
                request_identifier: "poc-probe-conversation".into(),
                flow_identifier: "effa1b".into(),
            })).await?;
            match conversation {
                Response::ConversationObserved(snapshot) => {
                    println!("conversation status={:?} entries={} flow_id={}",
                        snapshot.source_status, snapshot.entries.len(), snapshot.flow_identifier);
                    println!("source_path={EXACT_ROLLOUT} full_uuid={NATIVE_UUID}");
                    if let Some(entry) = snapshot.entries.last() {
                        let digest = Sha256::digest(entry.entry_text.as_bytes());
                        let hash: String = digest.iter().map(|byte| format!("{byte:02x}")).collect();
                        let excerpt: String = entry.entry_text.chars().take(80)
                            .map(|character| if character.is_control() { ' ' } else { character })
                            .collect();
                        println!("selected=last_in_bounded_page entry_id={} source_ordinal={} source_kind={:?} provenance={:?} sha256={} excerpt={:?}",
                            entry.entry_identifier, entry.source_ordinal, entry.source_kind,
                            entry.provenance, hash, excerpt);
                    } else {
                        println!("selected=none");
                    }
                }
                Response::OperationUnavailable(failure) => println!(
                    "conversation unavailable={:?}", failure.unavailability
                ),
                _ => return Err("unexpected conversation response".into()),
            }
        }
        [mode, request_id, text] if mode == "send" && !request_id.is_empty() => {
            let response = exchange(Query::SubmitPsyche(PsycheSubmission {
                request_identifier: request_id.clone(),
                flow_identifier: "effa1b".into(),
                psyche_text: text.clone(),
            })).await?;
            match response {
                Response::PsycheSubmitted(receipt) => println!(
                    "send request_id={} disposition={:?} grade={:?} reason={:?}",
                    receipt.request_identifier, receipt.submission_disposition,
                    receipt.receipt_grade, receipt.submission_reason_option
                ),
                Response::OperationUnavailable(failure) => println!("send unavailable={:?}", failure.unavailability),
                _ => return Err("unexpected send response".into()),
            }
        }
        _ => return Err("usage: unity-poc-mentci-probe read | send <explicit-request-id> <verbatim-text>".into()),
    }
    Ok(())
}
