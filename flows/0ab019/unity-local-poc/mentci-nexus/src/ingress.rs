//! Mentci mints the Unity ingress capability from the accepted local route.
//! Browser payloads cannot provide or override this classification.

use std::net::{IpAddr, SocketAddr};

const UNITY_SIGNAL_PATH: &str = "/signal";

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum IngressRefusal {
    NonLoopbackPeer,
    WrongRoute,
    WrongOrigin,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AcceptedUnityRoute {
    peer: SocketAddr,
}

impl AcceptedUnityRoute {
    pub fn peer(&self) -> SocketAddr {
        self.peer
    }
}

/// A local listener's own address, not a browser-supplied claim.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct LocalUnityListener {
    bound: SocketAddr,
}

impl LocalUnityListener {
    pub fn new(bound: SocketAddr) -> Result<Self, IngressRefusal> {
        if !bound.ip().is_loopback() {
            return Err(IngressRefusal::NonLoopbackPeer);
        }
        Ok(Self { bound })
    }

    pub fn accept(
        &self,
        peer: SocketAddr,
        request_path: &str,
        origin_header: &str,
    ) -> Result<AcceptedUnityRoute, IngressRefusal> {
        if !peer.ip().is_loopback() {
            return Err(IngressRefusal::NonLoopbackPeer);
        }
        if request_path != UNITY_SIGNAL_PATH {
            return Err(IngressRefusal::WrongRoute);
        }
        let expected_origin = match self.bound.ip() {
            IpAddr::V4(address) => format!("http://{address}:{}", self.bound.port()),
            IpAddr::V6(address) => format!("http://[{address}]:{}", self.bound.port()),
        };
        if origin_header != expected_origin {
            return Err(IngressRefusal::WrongOrigin);
        }
        Ok(AcceptedUnityRoute { peer })
    }
}

#[cfg(test)]
mod tests {
    use super::{IngressRefusal, LocalUnityListener};
    use std::net::SocketAddr;

    #[test]
    fn only_exact_local_unity_route_is_accepted() {
        let listener = LocalUnityListener::new("127.0.0.1:38081".parse().expect("address"))
            .expect("loopback listener");
        let peer: SocketAddr = "127.0.0.1:42000".parse().expect("peer");
        assert!(listener.accept(peer, "/signal", "http://127.0.0.1:38081").is_ok());
        assert_eq!(listener.accept(peer, "/other", "http://127.0.0.1:38081"), Err(IngressRefusal::WrongRoute));
        assert_eq!(listener.accept(peer, "/signal", "http://other.invalid"), Err(IngressRefusal::WrongOrigin));
    }

    #[test]
    fn nonlocal_peers_are_refused() {
        let listener = LocalUnityListener::new("127.0.0.1:38081".parse().expect("address"))
            .expect("loopback listener");
        let peer: SocketAddr = "192.0.2.2:42000".parse().expect("peer");
        assert_eq!(listener.accept(peer, "/signal", "http://127.0.0.1:38081"), Err(IngressRefusal::NonLoopbackPeer));
    }
}
