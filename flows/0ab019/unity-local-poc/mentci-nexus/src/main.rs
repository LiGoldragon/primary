//! Explicit-start localhost Unity bridge for the restricted Mentci Signal POC.

use std::{env, net::SocketAddr, path::PathBuf, sync::Arc, time::{SystemTime, UNIX_EPOCH}};

use axum::{
    extract::{ConnectInfo, State, WebSocketUpgrade, ws::{Message, WebSocket}},
    http::{HeaderMap, StatusCode, header::CONTENT_TYPE},
    response::{IntoResponse, Response as HttpResponse},
    routing::get,
    Router,
};
use futures_util::{SinkExt, StreamExt};
use signal::{FrameCapacity, Framable};
use signal_mentci::{
    OperationFailure, Query, ReceiptGrade, Response, Restorable, Signal,
    Signalizable, SubmissionDisposition, SubmissionReason, SubmissionReceipt,
    Unavailability,
};
use tokio::{io::{AsyncReadExt, AsyncWriteExt}, net::{TcpListener, UnixStream}};
use unity_poc_mentci_nexus::{
    dispatch::accepted_unity_submission,
    ingress::{AcceptedUnityRoute, LocalUnityListener},
    wire::{frame_response, restore_query},
};
use unity_poc_persona_seat::protocol::{PersonaApply, PersonaEnvelope, PersonaRequest};

const MAX_BODY_BYTES: usize = 256 * 1024;

#[derive(Clone)]
struct AppState {
    listener: LocalUnityListener,
    persona_socket: PathBuf,
    asset_root: PathBuf,
}

fn now_nanos() -> Option<i64> {
    i64::try_from(SystemTime::now().duration_since(UNIX_EPOCH).ok()?.as_nanos()).ok()
}

async fn persona_exchange(request: PersonaRequest, socket_path: PathBuf) -> Option<Response> {
    let mut stream = UnixStream::connect(socket_path).await.ok()?;
    let request = PersonaEnvelope::new(request).signalize().ok()?
        .framed(FrameCapacity::from(MAX_BODY_BYTES)).ok()?;
    stream.write_all(&request).await.ok()?;
    let mut prefix = [0_u8; 4];
    stream.read_exact(&mut prefix).await.ok()?;
    let length = u32::from_be_bytes(prefix) as usize;
    if length > MAX_BODY_BYTES { return None; }
    let mut body = vec![0_u8; length];
    stream.read_exact(&mut body).await.ok()?;
    Signal::<Response>::from(body).restore().ok()
}

async fn dispatch(query: Query, route: &AcceptedUnityRoute, socket: PathBuf) -> Option<Response> {
    match query {
        Query::ObserveRoster(observation) => {
            let request_id = observation.request_identifier.clone();
            let result = tokio::time::timeout(
                std::time::Duration::from_secs(10),
                persona_exchange(PersonaRequest::ObserveRoster(observation), socket),
            ).await.ok().flatten();
            Some(result.unwrap_or_else(|| Response::OperationUnavailable(OperationFailure {
                request_identifier: request_id,
                unavailability: Unavailability::PersonaUnavailable,
            })))
        }
        Query::ObserveConversation(observation) => {
            let request_id = observation.request_identifier.clone();
            let result = tokio::time::timeout(
                std::time::Duration::from_secs(10),
                persona_exchange(PersonaRequest::ObserveConversation(observation), socket),
            ).await.ok().flatten();
            Some(result.unwrap_or_else(|| Response::OperationUnavailable(OperationFailure {
                request_identifier: request_id,
                unavailability: Unavailability::PersonaUnavailable,
            })))
        }
        Query::SubmitPsyche(submission) => {
            let request_id = submission.request_identifier.clone();
            let input = accepted_unity_submission(route, submission);
            let (result, hold_reason) = match input {
                Ok(input) => {
                    // Rewrap only the Mentci-minted typed input for the private
                    // Persona socket. The decoded browser query alone cannot
                    // reach this call.
                    let persona_request = PersonaRequest::ApplyPsyche(
                        PersonaApply::from_accepted_unity(
                            input.request_id().to_owned(),
                            input.flow_id().to_owned(),
                            input.text().to_owned(),
                        )
                    );
                    let result = tokio::time::timeout(
                        std::time::Duration::from_secs(10),
                        persona_exchange(persona_request, socket),
                    ).await.ok().flatten();
                    (result, SubmissionReason::TargetUnavailable)
                }
                Err(unity_poc_mentci_nexus::dispatch::SubmissionHold::EmptyText) =>
                    (None, SubmissionReason::EmptyText),
                Err(unity_poc_mentci_nexus::dispatch::SubmissionHold::TextTooLarge) =>
                    (None, SubmissionReason::PolicyHold),
            };
            if let Some(Response::PsycheSubmitted(receipt)) = result {
                if receipt.request_identifier == request_id {
                    return Some(Response::PsycheSubmitted(receipt));
                }
            }
            Some(Response::PsycheSubmitted(SubmissionReceipt {
                request_identifier: request_id,
                submission_disposition: SubmissionDisposition::Held,
                submission_reason_option: Some(hold_reason),
                relay_identifier_option: None,
                event_identifier_option: None,
                timestamp_nanos: now_nanos()?,
                receipt_grade: ReceiptGrade::IngressAccepted,
            }))
        }
        _ => None,
    }
}

async fn signal_socket(mut socket: WebSocket, route: AcceptedUnityRoute, persona: PathBuf) {
    let Some(Ok(Message::Binary(message))) = socket.next().await else { return; };
    let Ok(query) = restore_query(&message) else { return; };
    let Some(response) = dispatch(query, &route, persona).await else { return; };
    let Ok(reply) = frame_response(response) else { return; };
    let _ = socket.send(Message::Binary(reply.into())).await;
    let _ = socket.close().await;
}

async fn signal_upgrade(
    State(state): State<Arc<AppState>>,
    ConnectInfo(peer): ConnectInfo<SocketAddr>,
    headers: HeaderMap,
    upgrade: WebSocketUpgrade,
) -> Result<impl IntoResponse, StatusCode> {
    let origin = headers.get("origin").and_then(|value| value.to_str().ok())
        .ok_or(StatusCode::FORBIDDEN)?;
    let route = state.listener.accept(peer, "/signal", origin)
        .map_err(|_| StatusCode::FORBIDDEN)?;
    let persona = state.persona_socket.clone();
    Ok(upgrade.on_upgrade(move |socket| signal_socket(socket, route, persona)))
}

async fn asset(state: &AppState, name: &str, mime: &'static str) -> HttpResponse {
    let path = state.asset_root.join(name);
    match tokio::fs::read(path).await {
        Ok(bytes) => ([(CONTENT_TYPE, mime)], bytes).into_response(),
        Err(_) => StatusCode::SERVICE_UNAVAILABLE.into_response(),
    }
}

async fn index(State(state): State<Arc<AppState>>) -> HttpResponse {
    asset(&state, "unity-web-draft/index.html", "text/html; charset=utf-8").await
}
async fn app(State(state): State<Arc<AppState>>) -> HttpResponse {
    asset(&state, "unity-web-draft/app.js", "text/javascript; charset=utf-8").await
}
async fn css(State(state): State<Arc<AppState>>) -> HttpResponse {
    asset(&state, "unity-web-draft/unity.css", "text/css; charset=utf-8").await
}
async fn codec_js(State(state): State<Arc<AppState>>) -> HttpResponse {
    asset(&state, "unity-local-poc/browser-signal-codec/pkg/browser_signal_codec.js", "text/javascript; charset=utf-8").await
}
async fn codec_wasm(State(state): State<Arc<AppState>>) -> HttpResponse {
    asset(&state, "unity-local-poc/browser-signal-codec/pkg/browser_signal_codec_bg.wasm", "application/wasm").await
}

#[tokio::main(flavor = "multi_thread", worker_threads = 2)]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let bound: SocketAddr = env::var("UNITY_POC_BIND")?.parse()?;
    let listener = LocalUnityListener::new(bound).map_err(|_| "loopback bind required")?;
    let persona_socket = PathBuf::from(env::var("UNITY_POC_PERSONA_SOCKET")?);
    let asset_root = PathBuf::from(env::var("UNITY_POC_FLOW_ROOT")?);
    if !asset_root.is_absolute() || !persona_socket.is_absolute() {
        return Err("POC paths must be absolute".into());
    }
    let state = Arc::new(AppState { listener, persona_socket, asset_root });
    let app = Router::new()
        .route("/", get(index))
        .route("/app.js", get(app))
        .route("/unity.css", get(css))
        .route("/signal", get(signal_upgrade))
        .route("/unity-local-poc/browser-signal-codec/pkg/browser_signal_codec.js", get(codec_js))
        .route("/unity-local-poc/browser-signal-codec/pkg/browser_signal_codec_bg.wasm", get(codec_wasm))
        .with_state(state);
    axum::serve(TcpListener::bind(bound).await?, app.into_make_service_with_connect_info::<SocketAddr>()).await?;
    Ok(())
}
