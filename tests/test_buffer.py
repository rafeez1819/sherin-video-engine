from src.frame_buffer import CircularBuffer


def test_buffer_injects_and_extracts_frames():
    buffer = CircularBuffer(size=3)
    buffer.inject("oldest", 0.0)
    buffer.inject("middle", 1.0)
    buffer.inject("newest", 2.0)

    frames = buffer.extract_chronological()
    assert [frame.timestamp for frame in frames] == [0.0, 1.0, 2.0]


def test_buffer_wraps_after_full_rotation():
    buffer = CircularBuffer(size=2)
    buffer.inject("first", 0.0)
    buffer.inject("second", 1.0)
    buffer.inject("third", 2.0)

    frames = buffer.extract_chronological()
    assert [frame.timestamp for frame in frames] == [1.0, 2.0]
