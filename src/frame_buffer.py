"""Circular frame buffer used throughout the generation pipeline."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Frame:
    index: int
    timestamp: float
    data: Any
    is_keyframe: bool = False


class CircularBuffer:
    def __init__(self, size: int = 60) -> None:
        if size < 1:
            raise ValueError("buffer size must be at least 1")
        self.size = size
        self.slots: list[Frame | None] = [None] * size
        self.head = 0
        self.frame_count = 0

    def reset(self) -> None:
        self.slots = [None] * self.size
        self.head = 0
        self.frame_count = 0

    def inject(
        self, frame_data: Any, timestamp: float, is_keyframe: bool = False
    ) -> int:
        frame = Frame(self.head, timestamp, frame_data, is_keyframe)
        self.slots[self.head] = frame
        position = self.head
        self.head = (self.head + 1) % self.size
        self.frame_count += 1
        return position

    def get_frame_at(self, logical_index: int) -> Frame | None:
        if not self.is_ready():
            if logical_index < self.frame_count:
                return self.slots[logical_index]
            return None
        actual_pos = (self.head + logical_index) % self.size
        return self.slots[actual_pos]

    def extract_chronological(self) -> list[Frame]:
        if not self.is_ready():
            return [frame for frame in self.slots if frame is not None]

        ordered = []
        for index in range(self.size):
            frame = self.get_frame_at(index)
            if frame is not None:
                ordered.append(frame)
        return ordered

    def is_ready(self) -> bool:
        return self.frame_count >= self.size

    def get_pair_for_interpolation(
        self, current_idx: int
    ) -> tuple[Frame | None, Frame | None]:
        frames = [frame for frame in self.slots if frame is not None]
        if current_idx <= 0:
            return None, frames[0] if frames else None
        if current_idx >= len(frames):
            return frames[-1] if frames else None, None
        return frames[max(0, current_idx - 1)], frames[
            min(len(frames) - 1, current_idx)
        ]
