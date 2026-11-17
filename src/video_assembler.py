"""Video encoding and assembly."""

from collections.abc import Iterable
from pathlib import Path

import cv2
import numpy as np
from PIL import Image


class VideoWriter:
    def __init__(
        self,
        fps: int,
        dimensions: tuple[int, int],
        fmt: str = "mp4",
        quality: int = 22,
        output_directory: str = "output",
    ) -> None:
        self.fps = fps
        self.dimensions = dimensions
        self.fmt = fmt
        self.output_directory = Path(output_directory)

    def compose(
        self, sequence: Iterable[Image.Image], name: str = "sherin_output"
    ) -> Path:
        self.output_directory.mkdir(parents=True, exist_ok=True)
        extension = "mp4" if self.fmt == "mp4" else "webm"
        output_path = self.output_directory / f"{name}.{extension}"
        codec = "mp4v" if extension == "mp4" else "VP90"
        writer = cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*codec),
            float(self.fps),
            self.dimensions,
        )
        if not writer.isOpened():
            raise RuntimeError(f"could not open video writer for {output_path}")

        wrote_frame = False
        for frame in sequence:
            if frame.size != self.dimensions:
                frame = frame.resize(self.dimensions, Image.Resampling.LANCZOS)
            rgb = np.asarray(frame.convert("RGB"))
            writer.write(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
            wrote_frame = True
        writer.release()

        if not wrote_frame:
            raise RuntimeError("cannot assemble a video without frames")
        return output_path
