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
use unity_poc_persona_seat::{known_claude, known_codex};

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
        [mode] | [mode, _] | [mode, _, _] if mode == "read" => {
            let flow_id = args.get(1).map(String::as_str).unwrap_or("effa1b");
            let (source_path, native_uuid) = match flow_id {
                "effa1b" => (known_codex::EXACT_ROLLOUT, known_codex::NATIVE_UUID),
                "c8d79f" => (known_claude::EXACT_TRANSCRIPT, known_claude::NATIVE_UUID),
                _ => return Err("read flow must be effa1b or c8d79f".into()),
            };
            let max_pages = args.get(2).map_or(Ok(1_usize), |value| value.parse::<usize>())?;
            if !(1..=16).contains(&max_pages) { return Err("page count must be 1..16".into()); }
            let roster = exchange(Query::ObserveRoster(RosterObservation {
                request_identifier: "poc-probe-roster".into(),
            })).await?;
            match roster {
                Response::RosterObserved(snapshot) => {
                    println!("roster status={:?} flows={}", snapshot.source_status, snapshot.flows.len());
                    for flow in snapshot.flows.iter() {
                        println!("roster pane_id={} flow_id={} correlation={:?} state={:?}",
                            flow.pane_identifier, flow.flow_identifier_option.as_deref().unwrap_or("none"),
                            flow.correlation_status, flow.flow_state);
                    }
                }
                Response::OperationUnavailable(failure) => println!("roster unavailable={:?}", failure.unavailability),
                _ => return Err("unexpected roster response".into()),
            }
            let mut cursor = None;
            for page in 0..max_pages {
                let conversation = exchange(Query::ObserveConversation(ConversationObservation {
                    request_identifier: format!("poc-probe-conversation-{page}"),
                    flow_identifier: flow_id.into(),
                    conversation_cursor_option: cursor,
                })).await?;
                match conversation {
                Response::ConversationObserved(snapshot) => {
                    println!("conversation page={} status={:?} entries={} flow_id={}",
                        page + 1, snapshot.source_status, snapshot.entries.len(), snapshot.flow_identifier);
                    println!("coverage snapshot_bytes={} current_bytes={} window={}..{} older={}",
                        snapshot.snapshot_bytes, snapshot.current_bytes, snapshot.window_start,
                        snapshot.window_end, snapshot.conversation_cursor_option.is_some());
                    println!("source_path={source_path} full_uuid={native_uuid}");
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
                    cursor = snapshot.conversation_cursor_option;
                }
                Response::OperationUnavailable(failure) => {
                    println!("conversation unavailable={:?}", failure.unavailability);
                    break;
                }
                _ => return Err("unexpected conversation response".into()),
                }
                if cursor.is_none() { break; }
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
        _ => return Err("usage: unity-poc-mentci-probe read [effa1b|c8d79f [pages 1..16]] | send <explicit-request-id> <verbatim-text>".into()),
    }
    Ok(())
}
