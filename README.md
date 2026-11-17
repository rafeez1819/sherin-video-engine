# SHERIN Video Engine

![Uploading image.png…]()


**4K Ultra HD · 60 FPS · Image-First Video Assembly**

SHERIN converts a text prompt into a complete video through modular keyframe generation,
frame interpolation, enhancement, and encoding.

## Features

- 60-slot circular frame buffer
- KuLexicon prompt-to-blueprint resolution
- Keyframe generation with a pluggable image backend
- Smooth blend, hold, and pan transition strategies
- 1080p, 2K, and 4K output
- MP4 and WebM assembly
- Procedural local keyframes for use without an external API

## Installation

```bash
pip install -e .
```

## Quick Start

```bash
python examples/01_basic_generation.py
```

```python
from src.engine import VideoEngine
from src.config import Settings

engine = VideoEngine(
    Settings(
        fps=60,
        resolution="4K",
        duration=5,
        keyframe_interval=1.5,
    )
)

result = engine.generate(
    prompt="A futuristic cityscape at night with glowing neon lights",
    style="cinematic",
)
result.save("output/neon_city.mp4")
```

## Architecture

```text
Prompt -> KuLexicon -> Keyframes -> Circular Buffer ->
Micro-Variations -> Resolution Enhancement -> MP4/WebM Assembly
```

## Development

```bash
python -m pytest
python -m ruff check .
```

## License

MIT License. See [LICENSE](LICENSE).
