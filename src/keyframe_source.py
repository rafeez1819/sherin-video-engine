"""Image keyframe source and cache."""

from __future__ import annotations

from collections.abc import Callable
from hashlib import sha256

from PIL import Image, ImageDraw, ImageFilter

from .kulexicon.lookup import SceneBlueprint

KeyframeCallback = Callable[[str, float, SceneBlueprint, tuple[int, int]], Image.Image]


class KeyframeGenerator:
    def __init__(self, callback: KeyframeCallback | None = None) -> None:
        self.cache: dict[float, Image.Image] = {}
        self.connected = callback is not None
        self.callback = callback

    def connect(self, callback: KeyframeCallback | None = None, **credentials) -> bool:
        if callback is not None:
            self.callback = callback
        self.connected = self.callback is not None
        return self.connected

    def create(
        self,
        prompt: str,
        timestamp: float,
        blueprint: SceneBlueprint,
        dimensions: tuple[int, int] = (3840, 2160),
    ) -> Image.Image:
        key = round(timestamp, 6)
        if key in self.cache:
            return self.cache[key]

        if self.callback is not None:
            image = self.callback(prompt, timestamp, blueprint, dimensions)
        else:
            image = self._procedural_frame(prompt, timestamp, dimensions)

        self.cache[key] = image
        return image

    def _procedural_frame(
        self, prompt: str, timestamp: float, dimensions: tuple[int, int]
    ) -> Image.Image:
        width, height = dimensions
        seed = int(sha256(prompt.encode("utf-8")).hexdigest()[:8], 16)
        shift = int((timestamp * 30) % max(1, width // 8))
        top = (8 + seed % 20, 24 + seed % 35, 70 + seed % 55)
        bottom = (18 + seed % 35, 50 + seed % 55, 120 + seed % 90)

        image = Image.new("RGB", dimensions)
        pixels = image.load()
        for y in range(height):
            ratio = y / max(1, height - 1)
            for x in range(width):
                glow = max(0.0, 1.0 - abs(x - width * 0.58) / (width * 0.45))
                r = int(top[0] * (1 - ratio) + bottom[0] * ratio + glow * 30)
                g = int(top[1] * (1 - ratio) + bottom[1] * ratio + glow * 70)
                b = int(top[2] * (1 - ratio) + bottom[2] * ratio + glow * 95)
                pixels[x, y] = (min(255, r), min(255, g), min(255, b))

        draw = ImageDraw.Draw(image, "RGBA")
        horizon = int(height * 0.72)
        for index in range(12):
            building_width = width // 18
            x = (index * width // 11 - shift) % (
                width + building_width
            ) - building_width
            building_height = height // 5 + ((seed + index * 97) % (height // 4))
            draw.rectangle(
                (x, horizon - building_height, x + building_width, horizon),
                fill=(10 + index * 3, 30 + index * 4, 55 + index * 6, 220),
                outline=(100, 210, 255, 100),
            )

        glow = Image.new("RGBA", dimensions, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        center_x = int(width * (0.35 + 0.2 * (shift / max(1, width / 8))))
        glow_draw.ellipse(
            (
                center_x - width // 12,
                height // 3 - height // 18,
                center_x + width // 12,
                height // 3 + height // 18,
            ),
            fill=(120, 230, 255, 180),
        )
        image = Image.alpha_composite(
            image.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(width // 35))
        )
        return image.convert("RGB")

    def clear_cache(self) -> None:
        self.cache.clear()
