use chronos_toy::{Aspect, Chronos, Layer, Location, Placement, Voice, generated::signal::{Query, Refused_Data, Response}};
use nexus_entry::Entering;

fn frame(query: &Query) -> Vec<u8> { rkyv::to_bytes::<rkyv::rancor::Error>(query).unwrap().to_vec() }
fn response(bytes: &[u8]) -> Response { rkyv::from_bytes::<Response, rkyv::rancor::Error>(bytes).unwrap() }

#[tokio::test]
async fn a_placement_goes_through_operation_to_memory_and_back() {
    let directory = tempfile::tempdir().unwrap();
    let (_main, door) = Chronos::open(directory.path().to_path_buf()).unwrap();
    assert_eq!(response(&door.knock(frame(&Query::Locate)).await), Response::Refused(Refused_Data::Unplaced));
    let here = Placement {
        location: Location { latitude: 47.6.try_into().unwrap(), longitude: (-122.3).try_into().unwrap() },
        voice: Voice { aspect: Aspect::Psyche, layer: Layer::Primary },
    };
    assert_eq!(response(&door.knock(frame(&Query::Place(here.clone()))).await), Response::Placed);
    assert_eq!(response(&door.knock(frame(&Query::Locate)).await), Response::Located(here));
}
