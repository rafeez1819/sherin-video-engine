from PIL import Image

from src.frame_buffer import CircularBuffer
from src.micro_variation import TransitionSystem


def test_blend_returns_middle_frame():
    first = Image.new("RGB", (16, 16), "black")
    second = Image.new("RGB", (16, 16), "white")
    result = TransitionSystem().complete_frame(CircularBuffer(), first, second, 0.5)

    assert result is not None
    pixel = result.getpixel((0, 0))
    assert pixel is not None
    assert max(pixel) - min(pixel) == 0
    assert 126 <= pixel[0] <= 128
