"""Configuration for the SHERIN video pipeline."""

from dataclasses import dataclass
from typing import Literal

Resolution = Literal["1080p", "2K", "4K"]
OutputFormat = Literal["mp4", "webm"]

RESOLUTION_MAP = {
    "1080p": (1920, 1080),
    "2K": (2560, 1440),
    "4K": (3840, 2160),
}


@dataclass
class Settings:
    fps: int = 60
    resolution: Resolution = "4K"
    duration: float = 5
    keyframe_interval: float = 1.5
    enable_micro_variation: bool = True
    enable_enhancement: bool = True
    output_format: OutputFormat = "mp4"
    output_quality: int = 22
    output_directory: str = "output"

    def __post_init__(self) -> None:
        if self.fps < 1:
            raise ValueError("fps must be at least 1")
        if self.resolution not in RESOLUTION_MAP:
            raise ValueError(f"unsupported resolution: {self.resolution}")
        if self.duration <= 0:
            raise ValueError("duration must be positive")
        if self.keyframe_interval <= 0:
            raise ValueError("keyframe_interval must be positive")

    @property
    def dimensions(self) -> tuple[int, int]:
        return RESOLUTION_MAP[self.resolution]
