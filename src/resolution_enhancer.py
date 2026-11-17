"""Image enhancement and output resizing."""

from PIL import Image, ImageEnhance, ImageFilter


class Magnifier:
    def __init__(self, target_resolution: tuple[int, int]) -> None:
        self.target_resolution = target_resolution

    def upgrade(self, frame: Image.Image) -> Image.Image:
        if frame.size != self.target_resolution:
            frame = frame.resize(self.target_resolution, Image.Resampling.LANCZOS)
        frame = frame.filter(
            ImageFilter.UnsharpMask(radius=1.2, percent=125, threshold=3)
        )
        frame = ImageEnhance.Contrast(frame).enhance(1.04)
        frame = ImageEnhance.Color(frame).enhance(1.03)
        return frame
