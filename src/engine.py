"""Main SHERIN pipeline orchestration."""

from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image

from .config import Settings
from .frame_buffer import CircularBuffer
from .keyframe_source import KeyframeGenerator
from .kulexicon.lookup import AssetResolver
from .micro_variation import TransitionSystem
from .resolution_enhancer import Magnifier
from .video_assembler import VideoWriter


class VideoEngine:
    def __init__(
        self,
        config: Settings | None = None,
        keyframe_generator: KeyframeGenerator | None = None,
    ) -> None:
        self.config = config or Settings()
        self.resolver = AssetResolver()
        self.buffer = CircularBuffer(size=60)
        self.keyframes = keyframe_generator or KeyframeGenerator()
        self.transitions = TransitionSystem()
        self.magnifier = Magnifier(target_resolution=self.config.dimensions)
        self.assembler = VideoWriter(
            fps=self.config.fps,
            dimensions=self.config.dimensions,
            fmt=self.config.output_format,
            quality=self.config.output_quality,
            output_directory=self.config.output_directory,
        )

    def generate(self, prompt: str, **options) -> VideoOutput:
        blueprint = self.resolver.analyze(prompt)
        style = options.get("style")
        if style:
            blueprint.style_hint = str(style)

        self.clear()
        total_frames = round(self.config.fps * self.config.duration)
        interval_frames = max(
            1, round(self.config.keyframe_interval * self.config.fps)
        )

        keyframes: dict[int, Image.Image] = {}
        for frame_number in range(0, total_frames, interval_frames):
            timestamp = frame_number / self.config.fps
            frame = self.keyframes.create(
                prompt,
                timestamp,
                blueprint,
                dimensions=self.config.dimensions,
            )
            keyframes[frame_number] = frame

        if not keyframes:
            keyframes[0] = self.keyframes.create(
                prompt, 0.0, blueprint, dimensions=self.config.dimensions
            )
        if total_frames - 1 not in keyframes:
            keyframes[total_frames - 1] = next(reversed(keyframes.values()))

        keyframe_positions = sorted(keyframes)
        sequence: list[Image.Image] = []
        for frame_number in range(total_frames):
            if frame_number in keyframes:
                sequence.append(keyframes[frame_number])
                continue

            left = max(
                (
                    position
                    for position in keyframe_positions
                    if position <= frame_number
                ),
                default=0,
            )
            right = min(
                (
                    position
                    for position in keyframe_positions
                    if position >= frame_number
                ),
                default=left,
            )
            if left == right:
                sequence.append(keyframes[left])
                continue

            progress = (frame_number - left) / (right - left)
            if self.config.enable_micro_variation:
                frame = self.transitions.complete_frame(
                    self.buffer, keyframes[left], keyframes[right], progress
                )
            else:
                frame = keyframes[left]
            sequence.append(frame or keyframes[left])

        if self.config.enable_enhancement:
            sequence = [self.magnifier.upgrade(frame) for frame in sequence]

        name = options.get("name", "sherin_output")
        output_path = self.assembler.compose(sequence, name=str(name))
        return VideoOutput(
            path=output_path,
            duration=self.config.duration,
            fps=self.config.fps,
            resolution=self.config.resolution,
        )

    def clear(self) -> None:
        self.buffer.reset()
        self.keyframes.clear_cache()


class VideoOutput:
    def __init__(self, path: Path, duration: float, fps: int, resolution: str) -> None:
        self.path = path
        self.duration = duration
        self.fps = fps
        self.resolution = resolution

    def save(self, destination: str) -> None:
        dest = Path(destination)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.path, dest)
