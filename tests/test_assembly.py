from PIL import Image

from src.video_assembler import VideoWriter


def test_video_writer_creates_mp4(tmp_path):
    writer = VideoWriter(
        fps=12,
        dimensions=(64, 36),
        fmt="mp4",
        output_directory=str(tmp_path),
    )
    frames = [Image.new("RGB", (64, 36), color) for color in ("red", "blue", "green")]
    output = writer.compose(frames)

    assert output.exists()
    assert output.suffix == ".mp4"
