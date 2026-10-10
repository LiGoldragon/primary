# The framing tests were seen failing

## Method

The nine new framing tests in `signal` assert the wire's shape, so they
must be shown to bite before they are trusted. In the `signal` checkout,
`src/frame.rs`'s single byte-order call was inverted:

    sed -i 's/length.to_be_bytes()/length.to_le_bytes()/' src/frame.rs
    cargo test --all-features --test framing
    sed -i 's/length.to_le_bytes()/length.to_be_bytes()/' src/frame.rs

Run on 2026-09-12, before the change was committed.

## Result

Three of the seven blocking tests failed on the inverted byte order and
four passed, which is the correct split — the four that passed assert
capacity and prefix decoding, neither of which the write path touches:

    test a_body_past_capacity_is_refused_rather_than_written ... ok
    test a_declared_length_past_capacity_is_refused_before_the_body_is_allocated ... ok
    test a_prefix_declares_the_length_its_bytes_spell ... ok
    test the_default_capacity_admits_exactly_eight_mebibytes ... ok
    test a_framed_body_carries_the_hand_computed_big_endian_prefix ... FAILED
    test a_written_frame_reads_back_as_the_same_body ... FAILED
    test a_signalized_value_frames_and_restores_across_the_wire ... FAILED
    test result: FAILED. 4 passed; 3 failed

The three that failed are the ones that carry bytes end to end: the
hand-written expected prefix `00 00 00 03 AA BB CC`, the write-then-read
round trip, and the full signalize-frame-read-restore path over a typed
contract value.

After restoring `to_be_bytes`, all seven pass; the passing run is in
`signal-framing-tests.txt`.
