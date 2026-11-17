"""Smooth frame interpolation."""

from dataclasses import dataclass

from PIL import Image

from .frame_buffer import CircularBuffer


@dataclass
class TransitionPlan:
    from_frame: object
    to_frame: object
    total_steps: int
    strategy: str = "blend"


class TransitionSystem:
    def __init__(self, default_strategy: str = "blend") -> None:
        self.default_strategy = default_strategy

    def complete_frame(
        self,
        buffer: CircularBuffer,
        previous_keyframe: Image.Image | None,
        next_keyframe: Image.Image | None,
        progress: float,
    ) -> Image.Image | None:
        if previous_keyframe is None:
            return next_keyframe
        if next_keyframe is None:
            return previous_keyframe

        if self.default_strategy == "hold":
            return previous_keyframe
        if self.default_strategy == "pan":
            return self._pan(previous_keyframe, next_keyframe, progress)
        return self._blend(previous_keyframe, next_keyframe, progress)

    def _blend(
        self, first: Image.Image, second: Image.Image, progress: float
    ) -> Image.Image:
        return Image.blend(first, second, max(0.0, min(1.0, progress)))

    def _pan(
        self, first: Image.Image, second: Image.Image, progress: float
    ) -> Image.Image:
        return self._blend(first, second, progress * 0.35)
